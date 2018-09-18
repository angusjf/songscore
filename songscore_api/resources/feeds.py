from flask_restful import Resource

class Feeds(Resource):
	@auth.login_required
	def get(self, user_id):
		# get that user's feed
		user = User.query.filter_by(id=user_id).one()
		feed = user.following.reviews
		return reviews_schema.jsonify(feed)
