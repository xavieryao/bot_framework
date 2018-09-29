from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, EmbeddedDocumentListField, ListField, LazyReferenceField
from .agent import Agent

class EntityEntry(EmbeddedDocument):
    reference_value = StringField(required=True)
    alias = ListField(StringField())


class Entity(Document):
    name = StringField(required=True)
    description = StringField()
    entries = EmbeddedDocumentListField(EntityEntry, required=True)
    agent = LazyReferenceField(Agent, required=True)