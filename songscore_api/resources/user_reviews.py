from flask_restful import Resource
from songscore_api.app import api
import .common.schema as schema

class UserReviews(Resource):
	def get(self, user_id):
		# get that user's reviews
		user = User.query.filter_by(id=user_id)
		reviews = user.reviews.order_by(db.desc(Review.datetime))
		return reviews_schema.jsonify(reviews)
