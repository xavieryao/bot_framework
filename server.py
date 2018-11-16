from flask import Flask
import apis
from flask_mongoengine import MongoEngine
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': os.environ['MONGO_DBNAME'],
    'host': os.environ['MONGO_SERVER'],
    'port': int(os.environ['MONGO_PORT']),
    'username': os.environ['MONGO_USERNAME'],
    'password': os.environ['MONGO_PASSWORD']
}

app.config['DEBUG'] = True
CORS(app)

app.url_map.strcit_slashes = False

db = MongoEngine(app)

app.register_blueprint(apis.workflow_apis, url_prefix='/v1/agent/<agent_id>/workflow/')
app.register_blueprint(apis.intent_apis, url_prefix='/v1/agent/<agent_id>/intent/')
app.register_blueprint(apis.entity_apis, url_prefix='/v1/agent/<agent_id>/entity/')
app.register_blueprint(apis.agent_apis, url_prefix='/v1/agent/')
app.register_blueprint(apis.user_apis, url_prefix='/v1/user/')

app.before_request(apis.auth.verify_api_key)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8765)
