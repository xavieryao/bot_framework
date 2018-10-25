from flask import Blueprint, request, g, jsonify
from models.user import User
from models.agent import Agent
from models.intent import Intent

intent_apis = Blueprint('intent_apis', __name__)

@intent_apis.url_value_preprocessor
def get_agent(_, values):
    g.agent_id = values['agent_id']
    g.agent = Agent.objects.get(id=g.agent_id)

@intent_apis.before_request
def before_req():
    g.user_id = "5bd1255f97d4030dfbf320e5"
    g.user = User.objects.get(id=g.user_id)

@intent_apis.route("/", methods=['GET', 'POST'])
def route_intent(agent_id):
    if request.method == 'GET':
        return list_intents()
    elif request.method == 'POST':
        return create_intent()

def list_intents():
    intents = Intent.objects(agent=g.agent)
    intents = [x.to_view() for x in intents]
    return jsonify(intents)

def create_intent():
    body = request.get_json()
    intent = Intent(
        name=body['name'],
        description=body.get('description', ''),
        agent=g.agent,
        tree=body['tree']
    ).save()
    return jsonify(intent)

@intent_apis.route('/<intent_id>', methods=['GET', 'PUT', 'DELETE'])
def route_single_entity(agent_id, intent_id):
    intent = Intent.objects.get(id=intent_id)
    assert str(intent.agent.id) == agent_id
    if request.method == 'GET':
        return get_intent(intent)
    elif request.method == 'PUT':
        return update_intent(intent)
    elif request.method == 'DELETE':
        return delete_intent(intent)

def get_intent(intent):
    return jsonify(intent.to_view())

def update_intent(intent):
    body = request.get_json()
    if 'name' in body:
        intent.name = body['name']
    if 'description' in body:
        intent.description = body['description']
    if 'tree' in body:
        intent.tree = body['tree']
    return jsonify(intent.to_view())

def delete_intent(intent):
    intent.delete()
    return 'done'