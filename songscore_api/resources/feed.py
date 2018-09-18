from flask import g
from flask_restful import Resource
from songscore_api.app import auth
from songscore_api.common.models import User, Review
from songscore_api.common.schema import Review as ReviewSchema

reviews_schema = ReviewSchema(many=True)

class Feed(Resource):
	@auth.login_required
	def get(self, user_id):
		# get that user's feed
		user = User.query.filter_by(id=user_id).one()
		if g.current_user != user:
			return '', 401
		# feed = user.following.reviews # TODO: FIX
		feed = Review.query.all() # TODO: unimport
		return reviews_schema.jsonify(feed)
