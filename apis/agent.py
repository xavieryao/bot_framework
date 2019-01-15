from flask import Blueprint, request, g, jsonify
from learnwares import trainer
from models.agent import Agent
from .auth import auth_required
from .error import api_success

agent_apis = Blueprint('agent_apis', __name__)

# FIXME bug: user not verified

@agent_apis.route('/', methods=['GET', 'POST'])
@auth_required
def route_agent():
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
    return jsonify(agent.to_view())

@agent_apis.route('/<agent_id>/train', methods=['POST'])
@auth_required
def train(agent_id):
    agent = Agent.objects.get(id=agent_id)
    trainer.start_training_process(agent)
    return api_success("started")

@agent_apis.route('/<agent_id>', methods=['GET', 'PUT', 'DELETE'])
@auth_required
def route_agent_with_id(agent_id):
    agent = Agent.objects.get(id=agent_id)
    if request.method == 'GET':
        return get_agent(agent)
    elif request.method == 'PUT':
        return update_agent(agent)
    elif request.method == 'DELETE':
        return delete_agent(agent)

def get_agent(agent):
    agent = agent.to_view()
    return jsonify(agent)

def update_agent(agent):
    body = request.get_json()
    if 'name' in body:
        agent.name = body['name']
    if 'description' in body:
        agent.description = body['description']
    if 'webhook' in body:
        agent.webhook = body['webhook']
    agent.save()
    return jsonify(agent.to_view())

def delete_agent(agent):
    agent.delete()
    return api_success('agent deleted')
