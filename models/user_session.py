from mongoengine import Document, StringField, DateTimeField, LazyReferenceField
from .user import User
import datetime
import random

def generate_api_key(n=64):
    k = []
    for _ in range(n):
        k.append(random.choice("1234567890abcdef"))
    return "".join(k)

class UserSession(Document):
    EXPIRE_SECS = 3600

    api_key = StringField(required=True, default=generate_api_key())
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