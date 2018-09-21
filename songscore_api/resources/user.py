from flask import g
from flask_restful import Resource
import songscore_api.common.models as models
import songscore_api.common.schemas as schemas
from songscore_api.app import auth

user_schema = schemas.User()

class User(Resource):
	@auth.login_required
	def get(self, user_id):
		# get the user with that id
		user = models.User.query.filter_by(id=user_id).one_or_none()
		return user_schema.jsonify(user)
