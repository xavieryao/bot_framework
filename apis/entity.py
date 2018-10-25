from flask import Blueprint, request, g, jsonify
from models.agent import Agent
from models.entity import Entity, EntityEntry
from .auth import auth_required
from .error import api_error
from mongoengine import DoesNotExist

entity_apis = Blueprint('entity_apis', __name__)

@entity_apis.url_value_preprocessor
def get_agent(_, values):
    g.agent_id = values['agent_id']
    g.agent = Agent.objects.get(id=g.agent_id)

@entity_apis.route('/', methods=['GET', 'POST'])
@auth_required
def route_entity(agent_id):
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
    return jsonify(entities)

def create_entity():
    body = request.get_json()
    entries = []
    for e in body['entries']:
        entries.append(EntityEntry(reference_value=e['reference_value'], alias=e['alias']))
    entity = Entity(
        name=body['name'],
        description=body.get('description', ''),
        entries=entries,
        agent=g.agent
    ).save()
    return str(entity.id)

def get_entity(entity):
    return jsonify(entity.to_view())

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
    return 'done'

@entity_apis.route('/<entity_id>/addEntry', methods=['POST'])
@auth_required
def add_entry(agent_id, entity_id):
    try:
        entity = Entity.objects.get(id=entity_id)
        assert str(entity.agent.id) == agent_id
    except (DoesNotExist, AssertionError):
        return api_error("not found", "invalid entity id"), 400

    body = request.get_json()
    entry = EntityEntry(reference_value=body['reference_value'], alias=body['alias'])
    entity.entries.append(entry)
    entity.save()
    return jsonify(entity.to_view())

@entity_apis.route('/<entity_id>/uploadEntryList', methods=['POST'])
@auth_required
def upload_entry(agent_id, entity_id):
    try:
        entity = Entity.objects.get(id=entity_id)
        assert str(entity.agent.id) == agent_id
    except (DoesNotExist, AssertionError):
        return api_error("not found", "invalid entity id"), 400

    return api_error("not implemented", "this API hasn't been implemented"), 400