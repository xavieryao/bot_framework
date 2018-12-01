from mongoengine import Document
from mongoengine import StringField, ListField, LazyReferenceField, FileField

from .agent import Agent


class Entity(Document):
    name = StringField(required=True)
    description = StringField()
    entries = ListField(StringField())
    entries_file = FileField(collection_name="bot_fs")
    agent = LazyReferenceField(Agent, required=True)

    meta = {
        'collection': 'bot_entity'
    }

    def to_view(self):
        obj = self.to_mongo()
        obj['id'] = str(self.id)
        obj['agent_id'] = str(self.agent.id)
        del obj['_id']
        del obj['agent']
        return dict(obj)

    def entries_to_view(self):
        if len(self.entries) == 0:
            entries = self.entries_file.read().decode("utf8").split("\n")
            return entries
        else:
            return self.to_mongo()['entries']
