import flask, flask_sqlalchemy, flask_restful, flask_marshmallow, os

app = flask.Flask(__name__)
app.config.update(
	SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
	SQLALCHEMY_TRACK_MODIFICATIONS=True
)
api = flask_restful.Api(app)
db = flask_sqlalchemy.SQLAlchemy(app)
ma = flask_marshmallow.Marshmallow(app)

import songscore_api.models, songscore_api.resources, songscore_api.schema
