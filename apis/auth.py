from flask import g, request
from models.user_session import UserSession
from mongoengine import DoesNotExist
from .error import api_error
from functools import wraps

def verify_api_key():
    if 'api_key' not in request.args:
        return
    api_key = request.args['api_key']
    try:
        session = UserSession.objects.get(api_key=api_key)
    except DoesNotExist:
        return api_error('authentication', 'The api_key is not valid. It might be expired.'), 403
    g.user_session = session
    g.user = g.user_session.user

def auth_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        verify_api_key()
        if 'user_session' not in g:
            return api_error('authentication', 'Authentication required. Supply api_key in query'), 403
        else:
            return func(*args, **kwargs)

    return decorated_function
