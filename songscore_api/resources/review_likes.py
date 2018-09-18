from flask_restful import Resource

class ReviewLikes(Resource):
	def post(self):
		# like that review
		return 'X', 501
