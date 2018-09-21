from flask_restful import Resource
from songscore_api.app import app, auth
import songscore_api.common.models as models
import songscore_api.common.schemas as schemas

review_schema = schemas.Review()

class Review(Resource):
	@auth.login_required
	def get(self, review_id):
		# get a the review with that id
		review = models.Review.query.filter_by(id=review_id)
		return review_schema.jsonify(review)

	@auth.login_required
	def delete(self, review_id):
		# delete that review
		review = models.Review.query.filter_by(id=review_id)
		models.db.session.delete(review)
		return '', 200
