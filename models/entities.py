from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, EmbeddedDocumentListField, ListField, ObjectIdField

class EntityEntry(EmbeddedDocument):
    reference_value = StringField(required=True)
    alias = ListField(StringField())


class Entities(Document):
    name = StringField(required=True)
    entries = EmbeddedDocumentListField(EntityEntry(), required=True)
    agent_id = ObjectIdField(required=True)