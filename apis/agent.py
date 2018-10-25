from flask import Blueprint, request, g
from models.agent import Agent
from response import make_response

agent_apis = Blueprint('agent_apis', __name__)

@agent_apis.before_request
def before_req():
    g.user_id = ""

@agent_apis.route('/', methods=['GET'])
def list_all():
    agents = Agent.objects.where(user__id__=g.user_id)
    print(agents)

@agent_apis.route('/register')
def register():
    return 'register'
