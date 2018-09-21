import flask, flask_sqlalchemy, flask_restful, flask_marshmallow, flask_httpauth
import os

app = flask.Flask(__name__)
app.config.update(
	SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
	SQLALCHEMY_TRACK_MODIFICATIONS=True
)
api = flask_restful.Api(app, prefix="/api/v1")
ma = flask_marshmallow.Marshmallow(app)
auth = flask_httpauth.HTTPTokenAuth()

import songscore_api.common.models
import songscore_api.common.schemas
import songscore_api.common.auth

from songscore_api import resources

api.add_resource(resources.Auth, '/auth')
api.add_resource(resources.Feed, '/feeds/<user_id>')
api.add_resource(resources.User, '/users/<user_id>')
api.add_resource(resources.Users, '/users')
api.add_resource(resources.UserReviews, '/users/<user_id>/reviews')
api.add_resource(resources.Reviews, '/reviews')
"""
api.add_resource(resources.Review, '/reviews/:id')
api.add_resource(resources.UserFollowing, '/users/:id/followers')
api.add_resource(resources.UserFollowers, '/api/users/:id/following')
api.add_resource(resources.UserFollower, '/users/:id/following/:id')
api.add_resource(resources.ReviewComments, '/reviews/:id/comments')
api.add_resource(resources.ReviewLikes, '/reviews/:id/likes')
api.add_resource(resources.ReviewDislikes, '/reviews/:id/dislikes')
"""
