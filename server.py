from flask import Flask
from apis.entity import entity_apis
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'bot_framework'
}
db = MongoEngine(app)
app.register_blueprint(entity_apis, url_prefix='/v1/entity/')

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()