from flask_restful import Resource, reqparse
import songscore_api.common.models as models
import songscore_api.common.schemas as schemas
from hashlib import md5
from passlib.hash import sha256_crypt
from songscore_api.common.models import db

users_schema = schemas.User(many=True)

class Users(Resource):
	def get(self):
		# get user with that username
		parser = reqparse.RequestParser()
		parser.add_argument('username')
		username = parser.parse_args()['username']
		if username is not None:
			query = '%'+username+'%'
			users = models.User.query.filter(UserModel.name.ilike(query))
			return users_schema.jsonify(users)
		else:
			return '', 200

	def post(self):
		# add a new user
		parser = reqparse.RequestParser()
		parser.add_argument('username')
		parser.add_argument('email')
		parser.add_argument('name')
		parser.add_argument('password')
		data = parser.parse_args()
		new_user = models.User(
			username=data['username'],
			email=data['email'],
			name=data['name'],
			password=sha256_crypt.encrypt(data['password']),
			picture="https://www.gravatar.com/avatar/%s?d=https://songscore.herokuapp.com/static/images/profile.png" % md5(data['email'].encode('utf-8')).hexdigest()
		)
		db.session.add(new_user)
		db.session.commit()
		return '', 201
