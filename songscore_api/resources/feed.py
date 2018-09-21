from flask import g
from flask_restful import Resource
from songscore_api.app import auth
import songscore_api.common.models as models
import songscore_api.common.schemas as schemas

reviews_schema = schemas.Review(many=True)

class Feed(Resource):
	@auth.login_required
	def get(self, user_id):
		# get that user's feed
		user = models.User.query.filter_by(id=user_id).one()
		if user != g.current_user:
			return '', 401
		# feed = user.following.reviews # TODO: FIX
		feed = models.Review.query.all() # TODO: unimport
		return reviews_schema.jsonify(feed)
