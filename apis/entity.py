from flask import Blueprint, request, g, jsonify
from models.user import User

entity_apis = Blueprint('entity_apis', __name__)

@entity_apis.before_request
def before_req():
    g.user_id = "5bd1255f97d4030dfbf320e5"
    g.user = User.objects.get(id=g.user_id)

@entity_apis.route('/', methods=['GET', 'POST'])
def route_entity():
    if request.method == 'GET'