from flask import Blueprint, request, g
from models.user import User

user_apis = Blueprint('user_apis', __name__)

@user_apis.before_request
def before_req():
    g.user_id = ""

@user_apis.route('/', methods=['POST'])
def create_user():
    user_obj = request.get_json()
    user = User(username=user_obj['username'], password=user_obj['password'], display_name=user_obj.get('display_name', '')).save()
    print('created user', user)
    return 'done'
