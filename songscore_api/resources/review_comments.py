from flask_restful import Resource

class ReviewComments(Resource):
	def post(self):
		# add a comment to that review
		return 'X', 501
