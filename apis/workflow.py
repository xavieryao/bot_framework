from flask import Blueprint, request, g, jsonify
from models.user import User
from models.agent import Agent
from models.entity import Entity
from models.intent import Intent
from models.workflow import Workflow, Parameter, Context

workflow_apis = Blueprint('workflow_apis', __name__)

@workflow_apis.url_value_preprocessor
def get_agent(_, values):
    g.agent_id = values['agent_id']
    g.agent = Agent.objects.get(id=g.agent_id)

@workflow_apis.before_request
def before_req():
    g.user_id = "5bd1255f97d4030dfbf320e5"
    g.user = User.objects.get(id=g.user_id)

@workflow_apis.route("/", methods=['GET', 'POST'])
def route_workflow(agent_id):
    if request.method == 'GET':
        return list_workflows()
    elif request.method == 'POST':
        return create_workflow()

def list_workflows():
    workflows = Workflow.objects(agent=g.agent)
    workflows = [x.to_view() for x in workflows]
    return jsonify(workflows)

def create_workflow():
    body = request.get_json()

    input_contexts = []
    for c in body.get('input_context', []):
        input_contexts.append(Context(name=c['name'], turns_to_expire=c['turns_to_expire']))

    output_contexts = []
    for c in body.get('output_context', []):
        output_contexts.append(Context(name=c['name'], turns_to_expire=c['turns_to_expire']))

    parameters = []
    for p in body.get('parameters', []):
        entity = Entity.objects.get(id=p['entity_type_id'])
        # TODO 404

        parameters.append(Parameter(
            name=p['name'],
            required=p.get('required', False),
            entity=entity,
            prompts=p.get('prompts', []),
            call_webhook=p.get('call_webhook', False)
        ))

    intent = Intent.objects.get(id=body['intent_id'])
    workflow = Workflow(
        name=body['name'],
        description=body.get('description', ''),
        agent=g.agent,
        intent=intent,
        input_contexts=input_contexts,
        output_contexts=output_contexts,
        parameters=parameters,
        end_of_conversation=body.get('end_of_conversation', False),
        responses=body.get('responses', []),
        call_webhook=body.get('call_webhook', False)
    ).save()
    return jsonify(workflow)

@workflow_apis.route('/<workflow_id>', methods=['GET', 'PUT', 'DELETE'])
def route_single_entity(agent_id, workflow_id):
    workflow = Workflow.objects.get(id=workflow_id)
    assert str(workflow.agent.id) == agent_id
    if request.method == 'GET':
        return get_workflow(workflow)
    elif request.method == 'PUT':
        return update_workflow(workflow)
    elif request.method == 'DELETE':
        return delete_workflow(workflow)

def get_workflow(workflow):
    return jsonify(workflow.to_view())

def update_workflow(workflow):
    body = request.get_json()
    if 'parameters' in body:
        parameters = []
        for p in body['parameters']:
            entity = Entity.objects.get(id=p['entity_type_id'])
            # TODO 404

            parameters.append(Parameter(
                name=p['name'],
                required=p.get('required', False),
                entity=entity,
                prompts=p.get('prompts', []),
                call_webhook=p.get('call_webhook', False)
            ))
        workflow.parameters = parameters

    if 'input_context' in body:
        input_contexts = []
        for c in body.get('input_context', []):
            input_contexts.append(Context(name=c['name'], turns_to_expire=c['turns_to_expire']))
        workflow.input_context = input_contexts

    if 'output_context' in body:
        output_contexts = []
        for c in body.get('output_context', []):
            output_contexts.append(Context(name=c['name'], turns_to_expire=c['turns_to_expire']))
        workflow.output_context = output_contexts

    if 'intent_id' in body:
        intent = Intent.objects.get(id=body['intent_id'])
        assert intent
        workflow.intent = intent

    if 'name' in body:
        workflow.name = body['name']
    if 'description' in body:
        workflow.description = body['description']
    if 'end_of_conversation' in body:
        workflow.end_of_conversation = body['end_of_conversation']
    if 'responses' in body:
        workflow.responses = body['responses']
    if 'call_webhook' in body:
        workflow.call_webhook = body['call_webhook']

    workflow.save()
    return jsonify(workflow.to_view())

def delete_workflow(workflow):
    workflow.delete()
    return 'done'