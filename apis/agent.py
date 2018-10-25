from flask import Blueprint, request, g, jsonify
from bson import ObjectId
from models.agent import Agent
from models.user import User
from response import make_response

agent_apis = Blueprint('agent_apis', __name__)

@agent_apis.before_request
def before_req():
    g.user_id = "5bd1255f97d4030dfbf320e5"
    g.user = User.objects.get(id=g.user_id)

@agent_apis.route('/', methods=['GET', 'POST'])
def manage_agent():
    if request.method == 'GET':
        return list_all()
    elif request.method == 'POST':
        return create_agent()

def list_all():
    agents = Agent.objects(user__id=g.user_id)
    for a in agents:
        a['user_id'] = str(a['user']['_id'])
        del a['user']
    return jsonify(agents)

def create_agent():
    body = request.get_json()
    agent = Agent(name=body['name'],
                  description=body.get('description', ''),
                  user=g.user,
                  webhook=body.get('webhook')).save()
    return str(agent.id)

@agent_apis.route('/register')
def register():
    return 'register'
