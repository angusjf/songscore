from flask_restful import Resource

class UserFollowers(Resource):
	@auth.login_required
	def get(self, user_id):
		# all the people that user is following
		return 'X', 501

	def post(self, follower_id, following_id):
		# make id 1 follow id 2
		return 'X', 501

	def delete(self, follower_id, following_id):
		# make id 1 follow id 2
		# make id 1 unfollow id 2
		return 'X', 501
