from songscore_api.app import auth

@auth.verify_token
def verify_token(token):
    flask.g.current_user = User.query.filter_by(token=token).first()
    return g.current_user is not None
