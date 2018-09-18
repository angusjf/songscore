import flask_marshmallow

from songscore_api.common.models import ReviewComment, Review, Subject, User
from songscore_api.app import app

ma = flask_marshmallow.Marshmallow(app)

class ReviewComment(ma.ModelSchema):
	class Meta:
		model = ReviewComment

class Review(ma.ModelSchema):
	class Meta:
		model = Review

class Subject(ma.ModelSchema):
	class Meta:
		model = Subject

class User(ma.ModelSchema):
	class Meta:
		model = User
