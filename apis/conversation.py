from flask import Blueprint, request
from response import make_response

conversation_apis = Blueprint('conversation_apis', __name__)

@conversation_apis.route('/query', method='POST')
def list_all():
    agent_id = request.args['agent']
    session
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

