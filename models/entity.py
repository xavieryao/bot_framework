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

    def to_view(self):
        obj = self.to_mongo()
        obj['id'] = str(obj['id'])
        obj['agent_id'] = str(self.agent.id)
        del obj['_id']
        del obj['agent']
        return obj