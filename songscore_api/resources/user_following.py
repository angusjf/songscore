from flask_restful import Resource

class UserFollowing(Resource):
	def get(self, user_id):
		# all the people that follow that user
		User.query.filter_by(id=user_id).followers
		return 'X', 501
