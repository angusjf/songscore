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
import songscore_api.common.schema
import songscore_api.common.auth

from songscore_api.resources import Auth, Feed, User

api.add_resource(Auth, '/auth')
api.add_resource(Feed, '/feeds/<user_id>')
api.add_resource(User, '/users/<user_id>')
"""
api.add_resource(Users, '/users')
api.add_resource(UserReviews, '/users/:id/reviews')
api.add_resource(Reviews, '/reviews')
api.add_resource(Review, '/reviews/:id')
api.add_resource(ReviewComments, '/reviews/:id/comments')
api.add_resource(ReviewLikes, '/reviews/:id/likes')
api.add_resource(ReviewDislikes, '/reviews/:id/dislikes')
api.add_resource(UserFollowing, '/users/:id/followers')
api.add_resource(UserFollowers, '/api/users/:id/following')
api.add_resource(UserFollower, '/users/:id/following/:id')
"""
