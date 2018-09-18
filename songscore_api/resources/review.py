from flask_restful import Resource

class Review(Resource):
	@auth.login_required
	def get(self, review_id):
		# get a the review with that id
		review = Review.query.filter_by(id=review_id)
		return review_schema.jsonify(review)

	@auth.login_required
	def delete(self, review_id):
		# delete that review
		review = Review.query.filter_by(id=review_id)
		db.session.delete(review)
		return '', 200
