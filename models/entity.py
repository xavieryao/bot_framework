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
        obj['entries'] = self.entries_to_view()
        if 'entries_file' in obj:
            del obj['entries_file']
        del obj['_id']
        del obj['agent']
        return dict(obj)

    def entries_to_view(self):
        if len(self.entries) == 0:
            try:
                entries = self.entries_file.read().decode("utf8").split("\n")
                return entries
            except:
                return []
        else:
            return self.to_mongo()['entries']
