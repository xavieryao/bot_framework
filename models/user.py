from mongoengine import Document, StringField

class User(Document):
    email = StringField(required=True)
    password_hash = StringField(required=True)
    display_name = StringField(required=True)
