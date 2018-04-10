from flask import Flask, render_template, flash, redirect, url_for, request, session, logging, g, Response, jsonify
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import psycopg2, psycopg2.extras
from functools import wraps
import os
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
        query_db("INSERT INTO users(name, email, username, password, picture) VALUES(%s, %s, %s, %s, %s)",
            (form.name.data, form.email.data, form.username.data, sha256_crypt.encrypt(str(form.password.data)), get_user_picture(form.email.data)))
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

#################
# NOTIFICATIONS #
#################

@app.route('/notifications')
@is_logged_in
def notifications():
    notifications = {}
    notifications['likes'] = query_db("""
        SELECT users.username, subjects.name AS subject_name FROM likes
        JOIN users ON users.id = likes.user_id
        JOIN reviews ON reviews.id = likes.review_id
        JOIN subjects ON subjects.id = reviews.subject_id
        WHERE reviews.user_id = %s AND likes.seen = false
        """, (session['user_id'],)
    )
    notifications['dislikes'] = query_db("""
        SELECT users.username, subjects.name AS subject_name FROM dislikes
        JOIN users ON users.id = dislikes.user_id
        JOIN reviews ON reviews.id = dislikes.review_id
        JOIN subjects ON subjects.id = reviews.subject_id
        WHERE reviews.user_id = %s AND dislikes.seen = false
        """, (session['user_id'],)
    )
    notifications['comments'] = query_db("""
        SELECT users.username, subjects.name AS subject_name, comments.text FROM comments
        JOIN users ON users.id = comments.user_id
        JOIN reviews ON reviews.id = comments.review_id
        JOIN subjects ON subjects.id = reviews.subject_id
        WHERE reviews.user_id = %s AND comments.seen = false
        """, (session['user_id'],)
    )
    notifications['follows'] = query_db("""
        SELECT users.username FROM follows
        JOIN users ON users.id = follows.follower_id
        WHERE following_id = %s AND seen = false
        """, (session['user_id'],)
    )
    notifications['review_mentions'] = [] #query_db("SELECT * FROM review_mentions WHERE mentioned_id = %s AND seen = false", (session['user_id'],))
    notifications['comment_mentions'] = [] #query_db("SELECT * FROM comment_mentions WHERE mentioned_id = %s AND seen = false", (session['user_id'],))
    return render_template('notifications.html', notifications=notifications)

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
    user = query_db("SELECT * FROM users WHERE username = %s", (username,), one=True)
    return render_template('userpage.html', user=user, reviews=get_reviews_from_user(user['id']))

@app.route('/user/<username>/following')
def user_following(username):
    data = query_db("""
        SELECT users_following.* FROM follows
        INNER JOIN users AS users_following ON users_following.id = follows.following_id
        INNER JOIN users AS users_followers ON users_followers.id = follows.follower_id
        WHERE users_followers.username = %s
        """, (username,)
    )
    user = {'id': 3, 'name': 'test', 'username': 'test', 'picture': '/static/images/profile.png'}
    return render_template('following.html', user=user, following=data)

@app.route('/user/<username>/followers')
def user_followers(username):
    data = query_db("""
        SELECT users_followers.* FROM follows
        INNER JOIN users AS users_followers ON users_followers.id = follows.follower_id
        INNER JOIN users AS users_following ON users_following.id = follows.following_id
        WHERE users_following.username = %s
        """, (username,)
    )
    user = {'id': 3, 'name': 'test', 'username': 'test', 'picture': '/static/images/profile.png'}
    return render_template('followers.html', user=user, followers=data)

@app.route('/user/<username>/likes')
def user_likes(username):
    liked_reviews = query_db("""
        SELECT
        subjects.name AS subject_name, subjects.artist_name AS subject_artist_name, subjects.image AS subject_image,
        users.name AS user_name, users.username AS user_username, users.picture AS user_picture
        FROM likes
        INNER JOIN reviews ON reviews.id = likes.review_id
        INNER JOIN users ON reviews.user_id = users.id
        INNER JOIN subjects ON reviews.subject_id = subjects.id
        WHERE likes.user_id = (SELECT id FROM users WHERE username = %s)
        """, (username,)
    )
    user = {'id': 3, 'name': 'test', 'username': 'test', 'picture': '/static/images/profile.png'}
    return render_template('likes.html', user=user, likes=liked_reviews)

@app.route('/user/<username>/dislikes')
def user_dislikes(username):
    data = query_db("""
        SELECT reviews.* FROM dislikes
        INNER JOIN reviews ON reviews.id = dislikes.review_id
        WHERE dislikes.user_id = (SELECT id FROM users WHERE username = %s)
        """, (username,)
    )
    user = {'id': 3, 'name': 'test', 'username': 'test', 'picture': '/static/images/profile.png'}
    return render_template('dislikes.html', user=username, dislikes=data)

@app.route('/user/<username>/comments')
def user_comments(username):
    data = query_db("""
        SELECT reviews.* FROM comments
        INNER JOIN reviews ON reviews.id = comments.review_id
        WHERE comments.user_id = (SELECT id FROM users WHERE username = %s)
        """, (username,)
    )
    user = {'id': 3, 'name': 'test', 'username': 'test', 'picture': '/static/images/profile.png'}
    return render_template('comments.html', user=user, comments=data)

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

@app.route('/like', methods=['POST'])
def like():
    query_db("INSERT INTO likes (user_id, review_id) VALUES (%s, %s)",
        (session['user_id'], request.form['review_id']))
    return redirect(url_for("index"))

@app.route('/dislike', methods=['POST'])
def dislike():
    query_db("INSERT INTO dislikes (user_id, review_id) VALUES (%s, %s)",
        (session['user_id'], request.form['review_id']))
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

def get_user_picture(email):
    return "https://www.gravatar.com/avatar/%s?d=https://songscore.herokuapp.com/static/images/profile.png" % md5(email.encode('utf-8')).hexdigest()


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
