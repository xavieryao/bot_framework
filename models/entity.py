from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, EmbeddedDocumentListField, ListField, LazyReferenceField
from .agent import Agent


class Entity(Document):
    name = StringField(required=True)
    description = StringField()
    entries = ListField(StringField())
    agent = LazyReferenceField(Agent, required=True)

    def to_view(self):
        obj = self.to_mongo()
        obj['id'] = str(self.id)
        obj['agent_id'] = str(self.agent.id)
        del obj['_id']
        del obj['agent']
        del obj['entries']
        return obj

    def entries_to_view(self):
        obj = self.to_mongo()
        return obj['entries']
