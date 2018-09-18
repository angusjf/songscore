from flask_restful import Resource
from songscore_api.common.models import User
from passlib.hash import sha256_crypt
from flask_restful import reqparse
import secrets

class Auth(Resource):
	def post(self):
		# get a new token
		parser = reqparse.RequestParser()
		parser.add_argument('username')
		parser.add_argument('password')
		args = parser.parse_args()
		hashed_password = sha256_crypt.encrypt(args['password']),
		hashed_password = hashed_password[0]
		user = User.query.filter_by(username=args['username']).one_or_none()
		if not user.password == hashed_password:
			user.token = secrets.token_hex()
			return user.token, 200
		else:
			return '', 401
