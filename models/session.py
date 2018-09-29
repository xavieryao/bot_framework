from mongoengine import Document, EmbeddedDocument
from mongoengine import LazyReferenceField, StringField, EmbeddedDocumentListField, IntField, DateTimeField
from .agent import Agent

import datetime

class Parameter(EmbeddedDocument):
    name = StringField(required=True)
    value = StringField(required=True)

class Context(EmbeddedDocument):
    name = StringField(required=True)
    parameters = EmbeddedDocumentListField(Parameter)
    turns_to_expiry = IntField(required=True)

class Session(Document):
    agent = LazyReferenceField(Agent, required=True)
    contexts = EmbeddedDocumentListField(Context)
    start_time = DateTimeField(required=True, default=datetime.datetime.utcnow)

    # TODO: session expire, use mongodb ttl
