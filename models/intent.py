from mongoengine import Document, EmbeddedDocument
from mongoengine import ObjectIdField, StringField, ListField, BooleanField, IntField

class Context(EmbeddedDocument):
    name = StringField(required=True)
    turns_to_expiry = IntField()

class Parameter(EmbeddedDocument):
    name = StringField(required=True)
    required = BooleanField(required=True, default=True)
    entity = ObjectIdField(required=True)
    # TODO: is_list
    prompts = ListField(StringField(), required=True) # TODO default

class Intent(Document):
    agent_id = ObjectIdField(required=True)
    name = StringField(required=True)
    input_context = ListField(Context())
    output_context = ListField(Context())
    training_phrases = ListField(StringField())
    parameters = ListField(Parameter())
    end_of_conversation = BooleanField(required=True, default=False)
    responses = ListField(StringField())
    enable_webhook = BooleanField(required=True, default=False)
    enable_slot_filling_webhook = BooleanField(required=True, default=False)