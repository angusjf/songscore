from flask import Flask, render_template, flash, redirect, url_for, request, session, logging, g, Response, jsonify
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import psycopg2, psycopg2.extras
from functools import wraps
import os
import datetime
from hashlib import md5

app = Flask(__name__) # creates an instance of flask
app.config.from_object(__name__) # load config from this file (songscore.py)
app.config.update({
    'SECRET_KEY' : os.environ['SECRET_KEY'],
    'DATABASE_URL' : os.environ['DATABASE_URL']
})

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)]) #they must input a name between 1 and 50 characters
    username = StringField('Username', [validators.Length(min=4, max=25)]) #they must input a username between 4 and 25 characters
    email = StringField('Email', [validators.Length(min=6, max=50)]) #they must input a username between 4 and 25 characters
    password = PasswordField (
        'Password',
        [
            validators.DataRequired(),
            validators.EqualTo('confirm', message='The passwords need to match yo'),
            validators.Length(min=8, max=100, message='password should be at least 8 characters')
        ]
    )
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

############
#          #
#  ROUTES  #
#          #
############

@app.route('/')
def index():
    if session.get('logged_in', False):
        return redirect(url_for('feed'))
    else:
        return redirect(url_for('register'))

###########################
# LOG IN / OUT / REGISTER #
###########################

@app.route('/register', methods=['GET', 'POST']) # needs to accept posts to collect data from the form
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate(): # need to make sure the request is post, and that it matches the validation
        picture = "https://www.gravatar.com/avatar/" + md5(form.email.data.encode('utf-8')).hexdigest()
        query_db("INSERT INTO users(name, email, username, password, picture) VALUES(%s, %s, %s, %s, %s)",
            (form.name.data, form.email.data, form.username.data, sha256_crypt.encrypt(str(form.password.data)), picture))
        flash('You are now registered and can log in', 'success') # format this for a good message
        return redirect(url_for('login'))
    else:
        return render_template('register.html', form=form) # if not a POST, it must be a get. Serve the form.

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Not using WTForms cos there's no point
    if request.method == 'POST': # if they submit some data, catch it from the form
        data = query_db("SELECT * FROM users WHERE username = %s", (request.form['username'], ), one=True)

        if data != None: # user exists
            if sha256_crypt.verify(request.form['password'], data['password']): # pass the password entered and the actual password found into sha256
                session['logged_in'] = True
                session['user_id'] = data['id']
                session['username'] = data['username']
                flash('You will hopefully now be logged in (no promises lol)', 'success')
                return redirect(url_for('index'))
            else:
                error = 'Password is incorrect'
                return render_template('login.html', error=error)
        else:
            error = 'Username does not exist'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html') # else, they're not submitting anything. Redirect to login page.

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

########
# FEED #
########

@app.route('/feed')
@is_logged_in
def feed():
    return redirect(url_for('feed_all'))

@app.route('/feed/all')
@is_logged_in
def feed_all():
    return render_template('feed.html', reviews=get_reviews_from_all())

@app.route('/feed/following')
@is_logged_in
def feed_following():
    return render_template('feed.html', reviews=get_reviews_from_following())

#################
# USER PROFILES #
#################

@app.route('/profile')
@is_logged_in
def profile():
    return redirect(url_for('user_page', username=session['username']))

@app.route('/user/<username>')
def user_page(username):
    data = query_db("SELECT * FROM users WHERE username = %s", (username,), one=True)
    if data != None:
        return render_template('profile.html', id=data['id'], name=data['name'], username=data['username'],
            picture=data['picture'], reviews=get_reviews_from_user(data['id']))
    else:
        return "user does not exist"

@app.route('/user/<username>/following')
def user_following(username):
    data = query_db("""
        SELECT
        users_following.*
        FROM follows
        INNER JOIN users AS users_following ON users_following.id = follows.following_id
        INNER JOIN users AS users_followers ON users_followers.id = follows.follower_id
        WHERE users_followers.username = %s
        """,
        (username,)
    )
    print(data)
    if data != None:
        return render_template('following.html', username=username, following=data)
    else:
        return "user does not exist"

@app.route('/user/<username>/followers')
def user_followers(username):
    data = query_db("""
        SELECT
        users_followers.*
        FROM follows
        INNER JOIN users AS users_followers ON users_followers.id = follows.follower_id
        INNER JOIN users AS users_following ON users_following.id = follows.following_id
        WHERE users_following.username = %s
        """,
        (username,)
    )
    print(data)
    if data != None:
        return render_template('following.html', username=username, following=data)
    else:
        return "user does not exist"

@app.route('/user/<username>/likes') # TODO
def user_likes(username):
    data = query_db("""
        SELECT
        reviews.*
        FROM likes
        INNER JOIN users ON users.id = votes.follower_id
        INNER JOIN users AS users_following ON users_following.id = follows.following_id
        WHERE users.username = %s
        """,
        (username,)
    )
    print(data)
    if data != None:
        return render_template('following.html', username=username, following=data)
    else:
        return "user does not exist"

###########
# ACTIONS #
###########

@app.route('/follow')
def follow():
    query_db("INSERT INTO follows(follower_id, following_id) VALUES(%s, %s)", (session['user_id'], request.args.get('user_id')))
    return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit_review():
    subject = query_db("SELECT id FROM subjects WHERE name = %s AND artist_name = %s AND type = %s",
        (request.form['subject_name'], request.form['subject_artist_name'], request.form['subject_type']), one=True)

    if subject == None: # not yet in the database
        subject = query_db("INSERT INTO subjects (name, artist_name, type, image) VALUES (%s, %s, %s, %s) RETURNING id",
            (request.form['subject_name'], request.form['subject_artist_name'], request.form['subject_type'], request.form['subject_image']), one=True)

    query_db("INSERT INTO reviews (user_id, score, subject_id, text) VALUES (%s, %s, %s, %s)",
        (session['user_id'], request.form['rating'], subject['id'], request.form['text']))
    return redirect(url_for("index"))

@app.route('/vote', methods=['POST'])
def submit_vote():
    if request['type'] == "upvote":
        upvote = "TRUE"
    elif request.form['type'] == "downvote":
        upvote = "FALSE"
    query_db("INSERT INTO votes (user_id, review_id, upvote) VALUES (%s, %s, %s)", (session['user_id'], request.form['review_id'], upvote))
    return redirect(url_for("index"))

@app.route('/comment', methods=['POST'])
def submit_comment():
    query_db("INSERT INTO comments (user_id, review_id, text) VALUES (%s, %s, %s)",
        (session['user_id'], request.form['review_id'], request.form['text']))
    return redirect(url_for("index"))

@app.route('/getfeed')
def get_feed_json():
    number_of_reviews = request.args.get('n')
    return jsonify(get_reviews_from_following(number_of_reviews))

@app.route('/getreviews')
def get_reviews():
    user_id = request.args.get('user_id')
    number_of_reviews = request.args.get('n')
    if user_id == None:
        return "{}" # no user with that name
    return jsonify(get_reviews_from_user(user_id, number_of_reviews))

################
#              #
#  NOT ROUTES  #
#              #
################

def get_reviews_from_all(amount=100):
    reviews = query_db("""
        SELECT
        subjects.name AS subject_name, subjects.artist_name AS subject_artist_name, subjects.image AS subject_image,
        users.name AS user_name, users.username AS user_username, users.picture AS user_picture,
        reviews.id AS id, reviews.text AS review_text, reviews.date AS review_date, reviews.score AS review_score
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        JOIN subjects ON reviews.subject_id = subjects.id
        ORDER BY review_date DESC
        LIMIT %s
        """,
        (amount,)
    )
    comments = query_db("""SELECT * FROM reviews
        JOIN comments ON comments.review_id = reviews.id JOIN users ON comments.user_id = users.id""")
    for review in reviews:
        # comments
        review['comments'] = []
        for comment in comments:
            if review['id'] == comment['review_id']:
                review['comments'].append(comment)
                print(comment)
        # dates
    return reviews

def get_reviews_from_following(amount=100):
    data = query_db("""
        SELECT
        subjects.name AS subject_name, subjects.artist_name AS subject_artist_name, subjects.image AS subject_image,
        users.name AS user_name, users.username AS user_username, users.picture AS user_picture,
        reviews.id AS id, reviews.text AS review_text, reviews.date AS review_date, reviews.score AS review_score
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        JOIN subjects ON reviews.subject_id = subjects.id
        WHERE reviews.user_id IN (SELECT following_id FROM follows WHERE follower_id = %s)
        ORDER BY review_date DESC
        LIMIT %s
        """,
        (session['user_id'], amount)
    )
    return data

def get_reviews_from_user(id, amount=100):
    data = query_db("""
        SELECT
        subjects.name AS subject_name, subjects.artist_name AS subject_artist_name, subjects.image AS subject_image,
        users.name AS user_name, users.username AS user_username, users.picture AS user_picture,
        reviews.text AS review_text, reviews.date AS review_date, reviews.score AS review_score
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        JOIN subjects ON reviews.subject_id = subjects.id
        WHERE reviews.user_id = %s
        ORDER BY review_date DESC
        LIMIT %s
        """,
        (id, amount)
    )
    return data

############
# DATABASE #
############

def get_db():
    if not hasattr(g, 'db'):
        g.db = psycopg2.connect(app.config['DATABASE_URL'])
    return g.db

@app.teardown_appcontext
def close_db(exception):
    if hasattr(g, 'db'):
        g.db.close()

def query_db(query, args=(), one=False):
    cursor = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor) # return dict instead of list
    cursor.execute(query, args)
    get_db().commit()
    if cursor.description != None:
        results = cursor.fetchall()
    else: # no results
        results = None
    cursor.close()
    if one: # one -> only expect one result, else returns a list
        if len(results) > 0:
            return results[0]
        else:
            return None
    else:
        return results
