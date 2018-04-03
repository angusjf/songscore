from flask import Flask, render_template, flash, redirect, url_for, request, session, logging, g, Response
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import sqlite3
from functools import wraps
import json

app = Flask('songscore') # creates an instance of flask
app.secret_key = "secret"
app.database = "database.db"

@app.route('/')
def index():
    return render_template('index.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)]) #they must input a name between 1 and 50 characters
    username = StringField('Username', [validators.Length(min=4, max=25)]) #they must input a username between 4 and 25 characters
    email = StringField('Email', [validators.Length(min=6, max=50)]) #they must input a username between 4 and 25 characters
    password = PasswordField ('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'The passwords need to match yo')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods = ['GET', 'POST']) #needs to accept posts to collect data from the form
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate(): #need to make sure the request is post, and that it matches the validation
        query_db(
            "INSERT INTO users(name, email, username, password) VALUES(?, ?, ?, ?)",
            (form.name.data, form.email.data, form.username.data, sha256_crypt.encrypt(str(form.password.data)))
        )
        flash('You are now registered and can log in', 'success') #format this for a good message
        redirect(url_for('login'))
    return render_template('register.html', form=form) #if not a POST, it must be a get. Serve the form.

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':#if they submit some data, catch it from the form
        #Not using WTForms cos there's no point
        username = request.form['username']
        password_candidate = request.form['password'] # candidate means taking what they put into the login page and comparing it. It may or may not match

        data = query_db("SELECT * FROM users WHERE username = ?", (username, ), one=True)

        if data != None: # user exists
            print("at least one result found")
            print("data: " + str(data))

            password = data['password']
            print("password:", str(password), "password candidate: ", str(password_candidate))

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
    return render_template('login.html') # else, they're not submitting anything. Redirect to login page.

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

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/profile') #points flask to the index so it can load files
@is_logged_in #makes it so they must be logged in to view it.
def profile():
    return render_template('profile.html')

@app.route('/getreviews') #points flask to the index so it can load files
def get_reviews():
    username = request.args.get('username');
    numberOfReviews = request.args.get('n');
    results = query_db("SELECT * FROM reviews WHERE user_id = (SELECT ) LIMIT ?", (session['user_id'], numberOfReviews))
    return Response(reviews_to_json(results), mimetype="application/json")

@app.route('/getfeed')
def get_feed_json(): # TODO following only
    numberOfReviews = request.args.get('n');
    results = query_db("SELECT * FROM reviews WHERE user_id = ? ORDER BY date DESC LIMIT ?", (session['user_id'], numberOfReviews))
    return Response(reviews_to_json(results), mimetype="application/json")

@app.route('/follow')
def follow():
    query_db("INSERT INTO follows(follower_id, following_id) VALUES(?, ?)", (session['user_id'], request.args.get('user_id')))
    return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit_review():
    query_db("INSERT INTO reviews (user_id, score, subject_name, text, type) VALUES (?, ?, ?, ?, ?)", (session['user_id'], request.form['rating'], request.form['subjectName'], request.form['text'], "song") )
    return redirect(url_for("index"))

def reviews_to_json(reviews):
    reviewJson = []
    for review in reviews:
        user = query_db("SELECT * FROM users WHERE id = ?", (review['user_id'],), one=True)
        upvotes = query_db("SELECT COUNT(review_Id) FROM VOTES WHERE REVIEW_ID = ? AND UPVOTE == 1", (review['id'],), one=True)
        downvotes = query_db("SELECT COUNT(review_Id) FROM VOTES WHERE REVIEW_ID = ? AND UPVOTE == 0", (review['id'],), one=True)
        comments_db = query_db("SELECT * FROM comments WHERE review_id = ?", (review['user_id'],))
        comments = {}

        for comment in comments_db:
            user = query_db("SELECT * FROM users WHERE id = ?", (comment['user_id'],), one=True)
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
            "subject_name" : review['subject_name'],
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
        g.db = sqlite3.connect(app.database)
        g.db.row_factory = dict_factory
    return g.db

@app.teardown_appcontext
def close_db(exception):
    if hasattr(g, 'db'):
        g.db.close()

def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    results = cursor.fetchall()
    get_db().commit()
    cursor.close()
    if one: # one -> only expect one result, else returns a dict(?)
        if len(results) > 0:
            return results[0]
        else:
            return None
    else:
        return results

def dict_factory(cursor, row):
    # this means execute returns a dict instead of a list
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# IMPORTANT -> if you use 'flask run' instead of 'python app.py' you can remove this. not really important but wanted u to read lol
if __name__ == '__main__': #if the right application is being run...
    app.run() #run it. debut means you don't have to reload the server for every change
