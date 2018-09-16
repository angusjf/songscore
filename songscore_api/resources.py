from flask_restful import Resource
from songscore_api.schema import *
from songscore_api.app import api, ma

class AuthResource(Resource):
	def get(self):
		# get token
		return 'Bearer whatever', 200

class FeedResource(Resource):
	def get(self, user_id):
		# get that user's feed
		user = User.query.filter_by(id=user_id).one()
		feed = user.following.reviews
		return reviews_schema.jsonify(feed)

class UserResource(Resource):
	def get(self, user_id):
		# get the user with that id
		user = User.query.filter_by(id=user_id).one()
		return user_schema.jsonify(user)

class UsersResource(Resource):
	def get(self):
		# get user with that username
		query = "%TODO%"
		user = User.query.filter(User.name.like(query)).one()
		return 'X', 501

	def post(self):
		# add a new user
		new_user = User(
			username=form.username.data,
			email=form.email.data,
			name=form.name.data,
			password=sha256_crypt.encrypt(str(form.password.data)),
			picture = "https://www.gravatar.com/avatar/%s?d=https://songscore.herokuapp.com/static/images/profile.png" % md5(form.email.data.encode('utf-8')).hexdigest()
		)
		db.session.add(new_user)
		db.session.commit()
		return '', 201

class UserReviewsResource(Resource):
	def get(self, user_id):
		# get that user's reviews
		user = User.query.filter_by(id=user_id)
		reviews = user.reviews.order_by(db.desc(Review.datetime))
		return reviews_schema.jsonify(reviews)

class ReviewsResource(Resource):
	def get(self):
		# get all the reviews
		reviews = Review.query.order_by(db.desc(Review.datetime)).all()
		return reviews_schema.jsonify(reviews)

class ReviewResource(Resource):
	def get(self, review_id):
		# get a the review with that id
		review = Review.query.filter_by(id=review_id)
		return review_schema.jsonify(review)

	def delete(self, review_id):
		# delete that review
		review = Review.query.filter_by(id=review_id)
		db.session.delete(review)
		return '', 200

class ReviewCommentsResource(Resource):
	def post(self):
		# add a comment to that review
		return 'X', 501

class ReviewLikesResource(Resource):
	def post(self):
		# like that review
		return 'X', 501

class ReviewDislikesResource(Resource):
	def post(self):
		# dislike that review
		return 'X', 501

class UserFollowingResource(Resource):
	def get(self, user_id):
		# all the people that follow that user
		User.query.filter_by(id=user_id).followers
		return 'X', 501

class UserFollowersResource(Resource):
	def get(self, user_id):
		# all the people that user is following
		return 'X', 501

class UserFollowerResource(Resource):
	def post(self, follower_id, following_id):
		# make id 1 follow id 2
		return 'X', 501

	def delete(self, follower_id, following_id):
		# make id 1 follow id 2
		# make id 1 unfollow id 2
		return 'X', 501

api.add_resource(AuthResource, '/api/auth')
api.add_resource(FeedResource, '/api/feeds/<user_id>')
api.add_resource(UserResource, '/api/users/:id')
api.add_resource(UsersResource, '/api/users')
api.add_resource(UserReviewsResource, '/api/users/:id/reviews')
api.add_resource(ReviewsResource, '/api/reviews')
api.add_resource(ReviewResource, '/api/reviews/:id')
api.add_resource(ReviewCommentsResource, '/api/reviews/:id/comments')
api.add_resource(ReviewLikesResource, '/api/reviews/:id/likes')
api.add_resource(ReviewDislikesResource, '/api/reviews/:id/dislikes')
api.add_resource(UserFollowingResource, '/api/users/:id/followers')
api.add_resource(UserFollowersResource, '/api/users/:id/following')
api.add_resource(UserFollowerResource, '/api/users/:id/following/:id')
