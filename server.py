from flask import Flask
from apis.entity import entity_apis
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'bot_framework'
}
