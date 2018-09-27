from mongoengine import Document, StringField, EmbeddedDocument, EmbeddedDocumentListField, ListField

class EntityEntry(EmbeddedDocument):
    reference_value = StringField(required=True)
    alias = ListField(StringField())


class Entities(Document):
    name = StringField(required=True)
    entries = EmbeddedDocumentListField(EntityEntry(), required=True)