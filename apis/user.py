from flask import Blueprint, request, g, jsonify
from models.user import User
from models.user_session import UserSession
from .error import api_error
from mongoengine import DoesNotExist
import datetime
from .auth import auth_required

user_apis = Blueprint('user_apis', __name__)

@user_apis.before_request
def before_req():
    g.user_id = "5bd1255f97d4030dfbf320e5"
    g.user = User.objects.get(id=g.user_id)

@user_apis.route('/', methods=['POST'])
def create_user():
    user_obj = request.get_json()
    user = User(username=user_obj['username'], password=user_obj['password'], display_name=user_obj.get('display_name', '')).save()
    return jsonify(user.to_view())

@user_apis.route('/<username>', methods=['GET', 'PUT', 'DELETE'])
@auth_required
def route_user(username):
    user = User.objects.get(username=username)
    assert user.id == g.user.id
    if request.method == 'GET':
        return get_user(user)
    elif request.method == 'PUT':
        return update_user(user)
    elif request.method == 'DELETE':
        return delete_user(user)

def get_user(user):
    return jsonify(user.to_view())

def update_user(user):
    body = request.get_json()
    if 'password' in body:
        user.password = body['password']
    if 'display_name' in body:
        user.display_name = body['display_name']
    user.save()
    return jsonify(user.to_view())

def delete_user(user):
    user.delete()
    return "done"

@user_apis.route('/login', methods=['GET'])
def login():
    username = request.args['username']
    password = request.args['password']
    try:
        user = User.objects.get(username=username)
        assert user.password == password
    except (AssertionError, DoesNotExist):
        return api_error("authentication", "username/password incorrect or does not exist")

    session = UserSession(
        user=user,
        api_key=UserSession.generate_api_key()
    ).save()

    expire_after = session.created + datetime.timedelta(seconds=UserSession.EXPIRE_SECS)
    return jsonify({
        "api_key": session.api_key,
        "rate_limit": 65535,
        "expires_after": expire_after.isoformat(timespec='milliseconds')
    })

@user_apis.route('/logout', methods=['GET'])
@auth_required
def logout():
    g.user_session.delete()
    return 'done'