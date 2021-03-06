from flask import Blueprint, request, g, jsonify
from models.agent import Agent
from models.entity import Entity
from .auth import auth_required
from .error import api_error, api_success
from mongoengine import DoesNotExist

entity_apis = Blueprint('entity_apis', __name__)

@entity_apis.url_value_preprocessor
def get_agent(_, values):
    print('entity api called')
    g.agent_id = values['agent_id']
    g.agent = Agent.objects.get(id=g.agent_id)

@entity_apis.route('/', methods=['GET', 'POST'])
@auth_required
def route_entity(agent_id):
    print('route entity')
    if request.method == 'GET':
        return list_entities()
    elif request.method == 'POST':
        return create_entity()

@entity_apis.route('/<entity_id>', methods=['GET', 'PUT', 'DELETE'])
@auth_required
def route_single_entity(agent_id, entity_id):
    try:
        entity = Entity.objects.get(id=entity_id)
        assert str(entity.agent.id) == agent_id
        assert entity.agent.fetch().user.id == g.user.id
    except (DoesNotExist, AssertionError):
        return api_error("not found", "invalid entity id"), 400
    if request.method == 'GET':
        return get_entity(entity)
    elif request.method == 'PUT':
        return update_entity(entity)
    elif request.method == 'DELETE':
        return delete_entity(entity)

def list_entities():
    entities = Entity.objects(agent=g.agent)
    entities = [x.to_view() for x in entities]
    for x in entities:
        del x['entries']
    return jsonify(entities)

def create_entity():
    body = request.get_json()
    entries = []
    for e in body['entries']:
        entries.append(e)
    entity = Entity(
        name=body['name'],
        description=body.get('description', ''),
        entries=entries,
        agent=g.agent
    ).save()
    return jsonify(entity.to_view())

def get_entity(entity):
    entity_dict = entity.to_view()
    entity_dict['entries'] = entity.entries_to_view()
    return jsonify(entity_dict)

def update_entity(entity):
    body = request.get_json()
    if 'name' in body:
        entity.name = body['name']
    if 'description' in body:
        entity.description = body['description']
    if 'entries' in body:
        entity.entries = body['entries']
    entity.save()
    return jsonify(entity.to_view())

def delete_entity(entity):
    entity.delete()
    return api_success('deleted')

@entity_apis.route('/<entity_id>/listAll', methods=['GET'])
@auth_required
def list_all_entries(agent_id, entity_id):
    try:
        entity = Entity.objects.get(id=entity_id)
        assert str(entity.agent.id) == agent_id
        assert entity.agent.fetch().user.id == g.user.id
    except (DoesNotExist, AssertionError):
        return api_error("not found", "invalid entity id"), 400

    return jsonify(entity.entries_to_view())

@entity_apis.route('/<entity_id>/addEntries', methods=['POST'])
@auth_required
def add_entries(agent_id, entity_id):
    try:
        entity = Entity.objects.get(id=entity_id)
        assert str(entity.agent.id) == agent_id
        assert entity.agent.fetch().user.id == g.user.id
    except (DoesNotExist, AssertionError):
        return api_error("not found", "invalid entity id"), 400

    body = request.get_json()
    old_entries = set(entity.entries)
    new_entries = set(body)
    entity.entries = list(old_entries | new_entries)
    entity.save()
    return api_success("added")

@entity_apis.route('/<entity_id>/deleteEntries', methods=['POST'])
@auth_required
def delete_entries(agent_id, entity_id):
    try:
        entity = Entity.objects.get(id=entity_id)
        assert str(entity.agent.id) == agent_id
        assert entity.agent.fetch().user.id == g.user.id
    except (DoesNotExist, AssertionError):
        return api_error("not found", "invalid entity id"), 400

    body = request.get_json()
    old_entries = set(entity.entries)
    new_entries = set(body)

    entity.entries = list(old_entries - new_entries)
    entity.save()
    return api_success("deleted")

@entity_apis.route('/<entity_id>/uploadEntryList', methods=['POST'])
@auth_required
def upload_entry(agent_id, entity_id):
    try:
        entity = Entity.objects.get(id=entity_id)
        assert str(entity.agent.id) == agent_id
        assert entity.agent.fetch().user.id == g.user.id
    except (DoesNotExist, AssertionError):
        return api_error("not found", "invalid entity id"), 400

    if 'file' not in request.files:
        return api_error("no file", "No file part")
    file = request.files['file']
    file_content = file.stream().read()
    entity.entries_file.delete()
    entity.entries_file.new_file()
    entity.entries_file.write(file_content)
    entity.entries_file.close()
    entity.save()
    return api_success("uploaded")
