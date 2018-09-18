from flask_restful import Resource

class Reviews(Resource):
	@auth.login_required
	def get(self):
		# get all the reviews
		reviews = Review.query.order_by(db.desc(Review.datetime)).all()
		return reviews_schema.jsonify(reviews)
