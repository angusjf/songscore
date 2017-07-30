import os
import psycopg2
#import urllib.parse
from flask import Flask, session, render_template, request, redirect, url_for, g, abort, flash, Response

app = Flask(__name__)

"""
urllib.parse.urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect (
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
"""

"""
# config
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE='songscore',
    SECRET_KEY='whatever dude',
    USERNAME='root',
    PASSWORD='whodatboy'
))
"""

"""
def connect_db():
    #Connects to the specific database
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
"""

@app.route('/')
def index():
    if not session.get('logged_in') == True:
        return render_template("feed.html", profile_image="https://lastfm-img2.akamaized.net/i/u/armed/f7d5a1bd4ee759cd813cc73de4cac47c.jpg")
    else:
        return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if True:
            session['logged_in'] = True
            return redirect(url_for("index"))
    return render_template('login.html', error=error)

@app.route('/getfeed')
def getFeed():
    request.args.get('n')
    return Response("""{
    "reviews" : [
        {
            "id" : 100,
            "user" : {
                "image" : "https://pbs.twimg.com/profile_images/847818629840228354/VXyQHfn0_400x400.jpg",
                "username" : "findlang",
                "name" : "Angus Findlay"
            },
            "subject" : {
                "image" : "https://lastfm-img2.akamaized.net/i/u/armed/f7d5a1bd4ee759cd813cc73de4cac47c.jpg",
                "name" : "Madvillainy",
                "artist" : "Madvillain"
            },
            "rating" : 4,
            "text" : "i thought this song was really #terrible",
            "upvotes" : 100,
            "downvotes" : 42,
            "date" : "1 m",
            "replies" : [
                {
                    "user" : {
                        "image" : "https://pbs.twimg.com/profile_images/847818629840228354/VXyQHfn0_400x400.jpg",
                        "username" : "findlang",
                        "name" : "Angus Findlay"
                    },
                    "text" : "nice opinion idiot",
                    "upvotes" : 1000,
                    "downvotes" : 42
                }
            ]
        }
    ]
}""", mimetype="application/json")

@app.route('/submit', methods=["POST"])
def submit():
    subjectName = request.values.get("subjectName")
    rating = request.values.get("rating")
    text = request.values.get("text")
    print(subjectName)
    print(rating)
    print(text)
    return "wagwan"
    #if (isset($subjectMBID) && isset($userId) && isset($rating) && isset($text))
        #Review::addToDatabase($subjectMBID, $userId, $rating, $text);
    #else
        #echo "yo like post some data";

@app.route('/user/<username>')
def user(username):
    return render_template('user.html', image="https://pbs.twimg.com/profile_images/847818629840228354/VXyQHfn0_400x400.jpg", name="Donald J trum", username=username)

@app.route('/review/<reviewId>')
def review(reviewId):
    return "todo";

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for("index"))

@app.route('/follow', methods=['POST'])
def logout():
    # get userid
    # get followingId
    # if not following
        # INSERT INTO followings (userId, followingId) VALUES (userId, followingId)
        #return "user followed"
    # else
        #return "user followed"
