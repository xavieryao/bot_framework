from mongoengine import Document, StringField, DateTimeField, LazyReferenceField
from .user import User
import datetime
import random

class UserSession(Document):
    EXPIRE_SECS = 3600

    api_key = StringField(required=True)
    user = LazyReferenceField(User, required=True)
    created = DateTimeField(default=datetime.datetime.now(), required=True)
    meta = {
        "indexes": [
            'api_key',
            {
                'fields': ['created'],
                'expireAfterSeconds': EXPIRE_SECS
            }
        ]
    }

    @classmethod
    def generate_api_key(clz, n=48):
        k = []
        for _ in range(n):
            k.append(random.choice("1234567890abcdef"))
        return "".join(k)
