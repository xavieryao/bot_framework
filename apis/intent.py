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
