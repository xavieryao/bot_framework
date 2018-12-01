from flask import Blueprint, request, jsonify
from response import make_response
from models.agent import Agent
from models.session import Session
from models.workflow import Workflow, Context
from .error import api_error, api_success
import random
import requests

conversation_apis = Blueprint('conversation_apis', __name__)

def dummy_intent_prediction_and_ner(sentence):
    return 1, 2

@conversation_apis.route('/', methods=['POST'])
def list_all():
    body = request.get_json()
    try:
        agent_id = body['agent_id']
    except KeyError:
        return api_error('missing params', 'agent_id is missing'), 400
    try:
        sentence = body['sentence']
    except KeyError:
        return api_error('missing params', 'sentence is missing'), 400
    session_id = body.get('session_id')

    agent = Agent.objects.get(id=agent_id)
    if not agent:
        return api_error('not found', 'Agent with agent_id does not exist.'), 400

    if not session_id:
        session = Session(agent=agent).save()
    else:
        session = Session.objects.get(id=session_id)
        if not session:
            return api_error('not found', 'Session with session_id does not exist.'), 400

    current_turn = session.current_turn
    session.current_turn += 1
    new_contexts = []
    for context in session.contexts:
        if context.turns_to_expiry != 0:
            context.turns_to_expiry -= 1
            new_contexts.append(context)
    session.contexts = new_contexts
    session.save()

    model_resp = requests.get("http://166.111.5.228:55014/query/{}/{}".format(agent_id, sentence)).json()

    return jsonify({
        "session_id": str(session.id),
        "turn": current_turn,
        "intent_id": "abcd",
        "intent_name": "search scholar",
        "reply": "I don't understand.",
        "intent": model_resp
    })

    current_context_names = set(x.name for x in new_contexts)

    intent, parameters = dummy_intent_prediction_and_ner(sentence)
    matched_workflows = Workflow.objects(intent=intent)
    workflow = None
    for w in matched_workflows:
        if all(c.name in current_context_names for c in w.input_context):
            workflow = w
            break

    if not workflow:
        return api_error('no workflow', 'No matched workflow.'), 400

    for out_context in workflow.output_context:
        session.contexts.append(Context(
            name=out_context.name,
            parameters=parameters,
            turns_to_expiry=out_context.turns_to_expiry
        ))
        session.save()

    responses = list(workflow.responses)
    resp = random.choice(responses)
    return jsonify({
        "resp": resp
    })