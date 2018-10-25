from mongoengine import Document, StringField, DateTimeField, LazyReferenceField
from .user import User

class UserSession(Document):
    api_key = StringField(required=True)
    user = LazyReferenceField(User, required=True)
    created = DateTimeField()
    meta = {
        "indexes": [
            'api_key',
            {
                'fields': ['created'],
                'expireAfterSeconds': 3600
            }
        ]
    }