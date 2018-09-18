from flask_restful import Resource

class Users(Resource):
	def get(self, user_id):
		# get the user with that id
		user = User.query.filter_by(id=user_id).one()
		return user_schema.jsonify(user)

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
