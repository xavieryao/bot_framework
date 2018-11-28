from mongoengine import Document, DynamicEmbeddedDocument, DynamicDocument
from mongoengine import LazyReferenceField, StringField, EmbeddedDocumentField, FloatField, DictField
from .agent import Agent


class Intent(Document):
    agent = LazyReferenceField(Agent, required=True)
    name = StringField(required=True)
    description = StringField(default="")
    tree = DictField(required=True)
    weight = FloatField(required=True)

    meta = {
        'collection': 'bot_intent'
    }

    def to_view(self):
        obj = self.to_mongo()
        obj['id'] = str(self.id)
        obj['agent_id'] = str(self.agent.id)
        del obj['_id']
        del obj['agent']
        return obj
