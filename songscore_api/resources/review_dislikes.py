from flask_restful import Resource

class ReviewDislikes(Resource):
	def post(self):
		# dislike that review
		return 'X', 501
