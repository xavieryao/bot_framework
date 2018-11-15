from mongoengine import Document, DynamicEmbeddedDocument
from mongoengine import LazyReferenceField, StringField, EmbeddedDocumentField, FloatField
from .agent import Agent

class IntentTree(DynamicEmbeddedDocument):
    pass

class Intent(Document):
    agent = LazyReferenceField(Agent, required=True)
    name = StringField(required=True)
    description = StringField(default="")
    tree = EmbeddedDocumentField(IntentTree)
    weight = FloatField(required=True)

    def to_view(self):
        obj = self.to_mongo()
        obj['id'] = str(self.id)
        obj['agent_id'] = str(self.agent.id)
        del obj['_id']
        del obj['agent']
        return obj