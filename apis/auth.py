from flask import g, request, jsonify
from models.user_session import UserSession
from mongoengine import DoesNotExist

def verify_api_key():
    if 'api_key' not in request.args:
        return
    api_key = request.args['api_key']
    try:
        session = UserSession.objects.get(api_key=api_key)
    except DoesNotExist:
        err = {
            'type': 'authentication',
            'message': 'The api_key is not valid. It might be expired.'
        }
        return jsonify(err), 403
    g.user_session = session