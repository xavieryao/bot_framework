from mongoengine import Document
from mongoengine import StringField, LazyReferenceField
from .user import User

class Agent(Document):
    name = StringField(required=True)
    description = StringField()
    user = LazyReferenceField(User, required=True)
    webhook = StringField()