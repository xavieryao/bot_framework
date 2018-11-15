from mongoengine import Document
from mongoengine import StringField

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    display_name = StringField()

    meta = {
        'collection': 'bot_user'
    }

    def to_view(self):
        obj = self.to_mongo()
        obj['id'] = str(self.id)
        del obj['_id']
        del obj['password']
        return obj