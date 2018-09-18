from flask import g
from flask_restful import Resource
from songscore_api.common.models import User as UserModel
from songscore_api.common.schema import User as UserSchema
from songscore_api.app import auth

user_schema = UserSchema()

class User(Resource):
	@auth.login_required
	def get(self, user_id):
		# get the user with that id
		user = UserModel.query.filter_by(id=user_id).one_or_none()
		return user_schema.jsonify(user)
