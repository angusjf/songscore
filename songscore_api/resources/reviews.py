from flask_restful import Resource
from songscore_api.app import app, auth
import songscore_api.common.models as models
import songscore_api.common.schemas as schemas

reviews_schema = schemas.Review(many=True)

class Reviews(Resource):
	@auth.login_required
	def get(self):
		# get all the reviews
		reviews = models.Review.query.order_by(models.db.desc(models.Review.datetime)).all()
		return reviews_schema.jsonify(reviews)

	def post(self):
		return '', 401
