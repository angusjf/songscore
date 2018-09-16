from .models import *
from .app import ma

class ReviewCommentSchema(ma.ModelSchema):
	class Meta:
		model = ReviewComment

class ReviewSchema(ma.ModelSchema):
	class Meta:
		model = Review

class SubjectSchema(ma.ModelSchema):
	class Meta:
		model = Subject

class UserSchema(ma.ModelSchema):
	class Meta:
		model = User

review_comment_schema = ReviewCommentSchema()
review_comments_schema = ReviewCommentSchema(many=True)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
subject_schema = SubjectSchema()
subjects_schema = SubjectSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
