from flask import Flask, render_template, flash, redirect, url_for, request, session, logging, g #from flask, we want to import flask and render_template
from data import Reviews #from data.py, import the Reviews function
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import sqlite3
from functools import wraps

app = Flask(__name__) #creates an instance of flask
app.secret_key = "secret"
app.database = "database.db"

#MySQL configuration
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'localhost'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'mysql'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #makes it save as a dictionary instead of a tuple
#init MYSQL
#mysql = MySQL(app)

Reviews = Reviews()

def connect_db():
    return sqlite3.connect(app.database)

@app.route('/') #points flask to the index so it can load files
def index():
    return render_template('index.html', reviews = Reviews) #literally just return a string


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
        name = form.name.data #if the user is submitting, make the name variable equal the name they input
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data)) #encrypts the password before it's submitted.

        #Creates the DictCursor
        g.db = connect_db()
        g.db.execute("INSERT INTO users(name, email, username, password) VALUES(?, ?, ?, ?)", (name, email, username, password))
        g.db.commit()
        g.db.close()

        flash('You are now registered and can log in', 'success') #format this for a good message
        redirect(url_for('login'))

    return render_template('register.html', form=form) #if not a POST, it must be a get. Serve the form.

    #Logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':#if they submit some data, catch it from the form
        #Not using WTForms cos there's no point
        username = request.form['username']
        password_candidate = request.form['password']#candidate means taking what they put into the login page and comparing it. It may or may not match

        #Creates the DictCursor
        c = sqlite3.connect('database.db')
        cur = c.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = ?", [username])
        print("results: " + str(result))


        if result: #as long as some rows are found in the table
            print("at least one result found")
            data = cur.fetchone() #FETCHes the first ONE result that appears.
            print("data: " + str(data))

            password = data[4]
            print("password: " + str(password))
            print("password candidate: " + str(password_candidate))

            if sha256_crypt.verify(password_candidate, password):#pass the password entered and the actual password found into the statement
                session['logged_in'] = True
                session['username'] = username

                flash('You will hopefully now be logged in (no promises lol)', 'success')
                return redirect(url_for('index'))
            else:
                error = 'Password is incorrect'
                return render_template('login.html', error = error)

        else:
            error = 'Username does not exist'
            return render_template('login.html', error = error)
        cur.close()

    return render_template('login.html')#else, they're not submitting anything. Redirect to login page.

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

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/profile') #points flask to the index so it can load files
@is_logged_in #makes it so they must be logged in to view it.
def profile():
    return render_template('profile.html')

if __name__ == '__main__': #if the right application is being run...
    app.run(debug = True) #run it. debut means you don't have to reload the server for every change
