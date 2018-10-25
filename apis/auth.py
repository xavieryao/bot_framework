from flask import g, request, jsonify
from models.user_session import UserSession
from mongoengine import DoesNotExist
from .error import api_error

def verify_api_key():
    if 'api_key' not in request.args:
        return
    api_key = request.args['api_key']
    try:
        session = UserSession.objects.get(api_key=api_key)
    except DoesNotExist:
        return api_error('authentication', 'The api_key is not valid. It might be expired.'), 403
    g.user_session = session

def auth_required(func):
    def err_func(*args, **kwargs):
        return api_error('authentication', 'Authentication required. Supply api_key in query'), 403

    if not g.user_session:
        return err_func
    return func