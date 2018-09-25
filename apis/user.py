from flask import Blueprint
from models.user import User

user_apis = Blueprint('user_apis', __name__)

@user_apis.route('/')
def hello():
    return 'hello from user api'

@user_apis.route('/register')
def register():
    return 'register'
