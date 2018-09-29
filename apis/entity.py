from flask import Blueprint, request
from models.entity import Entity
from response import make_response

entity_apis = Blueprint('entity_apis', __name__)

@entity_apis.route('/list')
def list_all():
    agent_id = request.args['agent']
    entities = []
    for entity in Entity.objects(agent_id=agent_id):
        entity_dict = {
            'name': entity.name,
            'description': entity.description if entity.description else '',
            'entries': []
        }
        for entry in entity.entries:
            entity_dict['entries'].append({
                'reference_value': entry.reference_value,
                'alias': [str(x) for x in entry.alias]
            })
    return make_response({'entities': entities})

@entity_apis.route('/register')
def register():
    return 'register'
