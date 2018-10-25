from mongoengine import Document
from mongoengine import StringField, LazyReferenceField
from .user import User

class Agent(Document):
    name = StringField(required=True)
    description = StringField()
    user = LazyReferenceField(User, required=True)
    webhook = StringField()

    def to_view(self):
        obj = self.to_mongo()
        obj['id'] = str(self.id)
        obj['user_id'] = str(self.user.id)
        del obj['_id']
        del obj['user']
        return obj