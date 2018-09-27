from flask import Blueprint
from models.entities import Entities

entities_apis = Blueprint('entities_apis', __name__)

@entities_apis.route('/list')
def list_all():
    return 'hello from entities api'

@entities_apis.route('/register')
def register():
    return 'register'
