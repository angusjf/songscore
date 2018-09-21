from flask_restful import Resource
from songscore_api.app import api
import songscore_api.common.schemas as schemas
import songscore_api.common.models as models

reviews_schema = schemas.Review(many=True)

class UserReviews(Resource):
	def get(self, user_id):
		# get that user's reviews
		user = models.User.query.filter_by(id=user_id).one_or_none()
		if user is not None:
			reviews = user.reviews #.order_by(db.desc(models.Review.datetime))
			return reviews_schema.jsonify(reviews)
		else:
			return '', 404
