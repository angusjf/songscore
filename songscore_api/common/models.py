import flask_sqlalchemy
from songscore_api.app import app

db = flask_sqlalchemy.SQLAlchemy(app)

dislikes = db.Table('dislikes',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
	db.Column('review_id', db.Integer, db.ForeignKey('review.id', ondelete='CASCADE')),
	db.Column('seen', db.Boolean, default=False, nullable=False)
)

follows = db.Table('follows',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
	db.Column('following_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
	db.Column('seen', db.Boolean, default=False, nullable=False)
)

likes = db.Table('likes',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
	db.Column('review_id', db.Integer, db.ForeignKey('review.id', ondelete='CASCADE')),
	db.Column('seen', db.Boolean, default=False, nullable=False)
)

class ReviewComment(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
	review_id = db.Column(db.Integer, db.ForeignKey('review.id', ondelete='CASCADE'), nullable=False)

	text = db.Column(db.Text, nullable=False)
	datetime = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
	seen = db.Column(db.Boolean, default=False, nullable=False)

	user = db.relationship("User", back_populates="comments") # ~
	review = db.relationship("Review", back_populates="comments")  # done

class Review(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)

	text = db.Column(db.Text)
	stars = db.Column(db.Integer, nullable=False) # db.Constraint("(stars >= 1) AND (stars <= 5)") TODO
	datetime = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

	user = db.relationship('User', back_populates='reviews')
	subject = db.relationship('Subject', back_populates='reviews')

	comments = db.relationship('ReviewComment', back_populates='review') #, cascade="all, delete-orphan", single-parent=True)

class Subject(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String, nullable=False) # db.Constraint("(type = 'album') OR (type ='song')" TODO

	name = db.Column(db.String, nullable=False)
	artist_name = db.Column(db.String, nullable=False)
	art = db.Column(db.String, nullable=False, default='/static/images/subject.png')

	reviews = db.relationship('Review', back_populates='subject') #, cascade="all, delete-orphan")#, single-parent=True)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String, nullable=False)
	username = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	picture = db.Column(db.String, nullable=False)
	register_datetime = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
	token = db.Column(db.String)
	token_expiry_datetime = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

	reviews = db.relationship('Review', back_populates='user', order_by='desc(Review.datetime)') #, cascade="all, delete-orphan", single-parent=True)
	comments = db.relationship('ReviewComment', back_populates='user', order_by='desc(ReviewComment.datetime)') #, cascade="all, delete-orphan") #, single-parent=True)
	likes = db.relationship('Review', secondary='likes', order_by='desc(Review.datetime)') #, cascade="all, delete-orphan", single-parent=True)
	dislikes = db.relationship('Review', secondary='dislikes', order_by='desc(Review.datetime)') #, cascade="all, delete-orphan", single-parent=True)
	following = db.relationship(
		'User', secondary=follows,
		primaryjoin=(follows.c.follower_id == id),
		secondaryjoin=(follows.c.following_id == id),
		backref=db.backref('followers', lazy='dynamic'),
		lazy='dynamic') #, cascade="all, delete-orphan")

db.create_all()
