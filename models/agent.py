from mongoengine import Document
from mongoengine import StringField

class Agent(Document):
    name = StringField(required=True)
    description = StringField()
    # TODO: add user
    # user = ObjectIdField()
    webhook = StringField()