from songscore_api.app import auth
from songscore_api.common.models import User
from flask import g

@auth.verify_token
def verify_token(token):
    print(token)
    g.current_user = User.query.filter_by(token=token).first()
    return g.current_user is not None
