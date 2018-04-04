from flask import Flask, render_template, flash, redirect, url_for, request, session, logging, g, Response
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import psycopg2
from functools import wraps
import json
import psycopg2.extras

app = Flask('songscore') # creates an instance of flask
app.secret_key = "secret"
app.database = "database.db"

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)]) #they must input a name between 1 and 50 characters
    username = StringField('Username', [validators.Length(min=4, max=25)]) #they must input a username between 4 and 25 characters
    email = StringField('Email', [validators.Length(min=6, max=50)]) #they must input a username between 4 and 25 characters
    password = PasswordField ('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'The passwords need to match yo')
    ])
    confirm = PasswordField('Confirm Password')

# Check if user logged in so they can't access pages they shouldn't.
# Make a page so you need to be logged in by adding "@is_logged_in" after the @app.route
def is_logged_in(f):
    @wraps(f) #pass in 'f'
    def wrap(*args, **kwargs): #idk what this means tbh
        if 'logged_in' in session: #check they're logged into a session
            return f(*args, **kwargs)
        else:
            flash('Yo you dont have access for this get outta here', 'danger') #danger type of alert
            return redirect(url_for('login')) #prompt them to log in
    return wrap

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST']) # needs to accept posts to collect data from the form
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate(): # need to make sure the request is post, and that it matches the validation
        query_db(
            "INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
            (form.name.data, form.email.data, form.username.data, sha256_crypt.encrypt(str(form.password.data)))
        )
        flash('You are now registered and can log in', 'success') # format this for a good message
        return redirect(url_for('login'))
    else:
        return render_template('register.html', form=form) # if not a POST, it must be a get. Serve the form.

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': # if they submit some data, catch it from the form
        # Not using WTForms cos there's no point
        username = request.form['username']
        password_candidate = request.form['password'] # candidate = what they put into the login page (may or may not match)

        data = query_db("SELECT * FROM users WHERE username = %s", (username, ), one=True)

        if data != None: # user exists
            password = data['password']

            if sha256_crypt.verify(password_candidate, password): # pass the password entered and the actual password found into the statement
                session['logged_in'] = True
                session['user_id'] = data['id']
                session['username'] = username

                flash('You will hopefully now be logged in (no promises lol)', 'success')
                return redirect(url_for('index'))
            else:
                error = 'Password is incorrect'
                return render_template('login.html', error = error)
        else:
            error = 'Username does not exist'
            return render_template('login.html', error = error)
    else:
        return render_template('login.html') # else, they're not submitting anything. Redirect to login page.

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/profile')
@is_logged_in #makes it so they must be logged in to view it.
def profile():
    data = query_db("SELECT * FROM users WHERE id = %s", (session['user_id'],), one=True)
    return render_template('profile.html', id=data['id'], name=data['name'], username=data['username'], picture=data['picture'])

@app.route('/user/<username>')
def user_page(username):
    data = query_db("SELECT * FROM users WHERE username = %s", (username,), one=True)
    if data != None:
        return render_template('profile.html', id=data['id'], name=data['name'], username=data['username'], picture=data['picture'])
    else:
        return "user does not exist"

@app.route('/getreviews')
def get_reviews():
    user_id = request.args.get('user_id')
    numberOfReviews = request.args.get('n')
    if user_id == None:
        return "{}" # no user with that name
    results = query_db("SELECT * FROM reviews WHERE user_id = %s LIMIT %s", (user_id, numberOfReviews))
    return Response(reviews_to_json(results), mimetype="application/json")

@app.route('/getfeed')
def get_feed_json(): # TODO following only
    numberOfReviews = request.args.get('n')
    results = query_db("SELECT * FROM reviews WHERE user_id = %s ORDER BY date DESC LIMIT %s",
        (session['user_id'], numberOfReviews))
    return Response(reviews_to_json(results), mimetype="application/json")

@app.route('/follow')
def follow():
    query_db("INSERT INTO follows(follower_id, following_id) VALUES(%s, %s)", (session['user_id'], request.args.get('user_id')))
    return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit_review():
    subject = query_db("SELECT id FROM subjects WHERE name = %s AND artist_name = %s AND type = %s",
        (request.form['subject_name'], request.form['subject_artist_name'], request.form['subject_type']), one=True)

    if subject == None: # not yet in the database
        query_db("INSERT INTO subjects (name, artist_name, type, image) VALUES (%s, %s, %s, %s)",
            (request.form['subject_name'], request.form['subject_artist_name'], request.form['subject_type'], request.form['subject_image']) )
        subject = query_db("SELECT id FROM subjects WHERE name = %s AND artist_name = %s AND type = %s",
            (request.form['subject_name'], request.form['subject_artist_name'], request.form['subject_type']), one=True)

    query_db("INSERT INTO reviews (user_id, score, subject_id, text) VALUES (%s, %s, %s, %s)",
        (session['user_id'], request.form['rating'], subject['id'], request.form['text']))
    return redirect(url_for("index"))

def reviews_to_json(reviews):
    reviewJson = []
    for review in reviews:
        user = query_db("SELECT * FROM users WHERE id = %s", (review['user_id'],), one=True)
        subject = query_db("SELECT * FROM subjects WHERE id = %s", (review['subject_id'],), one=True)
        upvotes = query_db("SELECT COUNT(review_Id) FROM VOTES WHERE REVIEW_ID = %s AND UPVOTE = TRUE", (review['id'],), one=True)
        downvotes = query_db("SELECT COUNT(review_Id) FROM VOTES WHERE REVIEW_ID = %s AND UPVOTE = FALSE", (review['id'],), one=True)
        comments_db = query_db("SELECT * FROM comments WHERE review_id = %s", (review['user_id'],))
        comments = {}

        for comment in comments_db:
            user = query_db("SELECT * FROM users WHERE id = %s", (comment['user_id'],), one=True)
            comments.append({
                "user" : {
                    "name" : user['name'],
                    "username" : user['username'],
                    "image" : user['picture']
                },
                "upvotes" : upvotes,
                "downvotes" : downvotes,
            })

        reviewJson.append({
            "id" : review["id"],
            "user" : {
                "name" : user['name'],
                "username" : user['username'],
                "image" : user['picture']
            },
            "subject" : {
                "id" : subject['id'],
                "name" : subject['name'],
                "artist_name" : subject['artist_name'],
                "type" : subject['type'],
                "image" : subject['image']
            },
            "rating" : review['score'],
            "text" : review['text'],
            "upvotes" : upvotes,
            "downvotes" : downvotes,
            "date" : "1m ago",
            "comments" : comments
        })
    return json.dumps(reviewJson)

# database functions
def get_db():
    if not hasattr(g, 'db'):
        g.db = psycopg2.connect(
            dbname='d4muopol69lmv7',
            user='yjrybcwtcrpgic',
            host='ec2-79-125-125-97.eu-west-1.compute.amazonaws.com',
            password='3e75d7694c8707e0a868c7123d53ef904bf6c671ee94dffe057331576ff58157',
            port="5432"
        )
        init_db()
    return g.db

@app.teardown_appcontext
def close_db(exception):
    if hasattr(g, 'db'):
        g.db.close()

def query_db(query, args=(), one=False):
    cursor = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query, args)
    get_db().commit()
    if cursor.description == None: # no results
        cursor.close()
        return None
    else:
        results = cursor.fetchall()
        if one: # one -> only expect one result, else returns a dict(?)
            if len(results) > 0:
                return results[0]
            else:
                return None
        else:
            return results

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().execute(f.read())
    db.commit()
