from flask import Blueprint, request, g, jsonify
from models.agent import Agent
from models.user import User

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
    agents = Agent.objects(user=g.user)
    agents = [x.to_view() for x in agents]
    return jsonify(agents)

def create_agent():
    body = request.get_json()
    agent = Agent(name=body['name'],
                  description=body.get('description', ''),
                  user=g.user,
                  webhook=body.get('webhook')).save()
    return str(agent.id)

@agent_apis.route('/<agent_id>', methods=['GET', 'PUT', 'DELETE'])
def route_agent_with_id(agent_id):
    if request.method == 'GET':
        return get_agent(agent_id)
    elif request.method == 'PUT':
        return update_agent(agent_id)
    elif request.method == 'DELETE':
        return delete_agent(agent_id)

def get_agent(agent_id):
    agent = Agent.objects.get(id=agent_id)
    agent = agent.to_view()
    return jsonify(agent)

def update_agent(agent_id):
    agent = Agent.objects.get(id=agent_id)
    body = request.get_json()
    if 'name' in body:
        agent.name = body['name']
    if 'description' in body:
        agent.description = body['description']
    if 'webhook' in body:
        agent.webhook = body['webhook']
    agent.save()
    return 'done'

def delete_agent(agent_id):
    agent = Agent.objects.get(id=agent_id)
    agent.delete()
    return 'done'