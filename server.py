from flask import Flask
import apis
from flask_mongoengine import MongoEngine
from flask_cors import CORS
import os
from apis.error import api_error

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': os.environ['MONGO_DBNAME'],
    'host': os.environ['MONGO_SERVER'],
    'port': int(os.environ['MONGO_PORT']),
    'username': os.environ.get('MONGO_USERNAME'),
    'password': os.environ.get('MONGO_PASSWORD')
}

app.config['DEBUG'] = os.environ.get('DEBUG', False)
CORS(app)

app.url_map.strict_slashes = False

db = MongoEngine(app)

app.register_blueprint(apis.workflow_apis, url_prefix='/v1/agent/<agent_id>/workflow/')
app.register_blueprint(apis.intent_apis, url_prefix='/v1/agent/<agent_id>/intent/')
app.register_blueprint(apis.entity_apis, url_prefix='/v1/agent/<agent_id>/entity/')
app.register_blueprint(apis.agent_apis, url_prefix='/v1/agent/')
app.register_blueprint(apis.user_apis, url_prefix='/v1/user/')

@app.errorhandler(500)
def internal_error(err):
    return api_error("internal error", "internal error {}".format(repr(err))), 500


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/mk500')
def make_500():
    raise ValueError

@app.route('/test')
def test():
    from learnwares import sentence_simulator
    sentence_simulator.test()
    return 'done'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8765)

