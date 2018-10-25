from flask import Flask
from apis.agent import agent_apis
from apis.user import user_apis
from apis.entity import entity_apis
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'bot_framework'
}

db = MongoEngine(app)
app.register_blueprint(entity_apis, url_prefix='/v1/agent/<agent_id>/entity/')
app.register_blueprint(agent_apis, url_prefix='/v1/agent/')
app.register_blueprint(user_apis, url_prefix='/v1/user/')

print(app.url_map)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()