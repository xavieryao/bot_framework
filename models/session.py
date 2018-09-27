from mongoengine import Document, EmbeddedDocument
from mongoengine import ObjectIdField, StringField, EmbeddedDocumentListField, IntField, DateTimeField
import datetime

# TODO: session expire

class Parameter(EmbeddedDocument):
    name = StringField(required=True)
    value = StringField(required=True)

class Context(EmbeddedDocument):
    name = StringField(required=True)
    parameters = EmbeddedDocumentListField(Parameter())
    turns_to_expiry = IntField(required=True)

class Session(Document):
    agent_id = ObjectIdField(required=True)
    contexts = EmbeddedDocumentListField(Context())
    start_time = DateTimeField(required=True, default=datetime.datetime.utcnow)