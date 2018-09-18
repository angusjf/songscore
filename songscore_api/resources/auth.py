import secrets

from datetime import datetime, timedelta
from flask_restful import Resource
from songscore_api.common.models import User, db
from passlib.hash import sha256_crypt
from flask_restful import reqparse

class Auth(Resource):
	def post(self):
		# get a new token
		parser = reqparse.RequestParser()
		parser.add_argument('username')
		parser.add_argument('password')
		args = parser.parse_args()
		user = User.query.filter_by(username=args['username']).one_or_none()
		if sha256_crypt.verify(args['password'], user.password):
			user.token = secrets.token_hex()
			user.token_expiry_datetime = datetime.now() + timedelta(hours=1)
			db.session.commit()
			return user.token, 200
		else:
			return '', 401
