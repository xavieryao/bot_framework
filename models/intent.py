from mongoengine import Document, DynamicEmbeddedDocument
from mongoengine import LazyReferenceField, StringField, EmbeddedDocumentField
from .agent import Agent

class IntentTree(DynamicEmbeddedDocument):
    pass

class Intent(Document):
    agent = LazyReferenceField(Agent, required=True)
    name = StringField(required=True)
    description = StringField(default="")
    tree = EmbeddedDocumentField(IntentTree)