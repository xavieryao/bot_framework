from mongoengine import Document
from mongoengine import StringField

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    display_name = StringField()