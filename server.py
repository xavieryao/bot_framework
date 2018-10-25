from flask import Flask
import apis
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'bot_framework'
}

db = MongoEngine(app)

app.register_blueprint(apis.intent_apis, url_prefix='/v1/agent/<agent_id>/intent/')
app.register_blueprint(apis.entity_apis, url_prefix='/v1/agent/<agent_id>/entity/')
app.register_blueprint(apis.agent_apis, url_prefix='/v1/agent/')
app.register_blueprint(apis.user_apis, url_prefix='/v1/user/')

print(app.url_map)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()