from mongoengine import Document, EmbeddedDocument
from mongoengine import ObjectIdField, StringField, ListField, BooleanField

class Parameter(EmbeddedDocument):
    name = StringField(required=True)
    required = BooleanField(required=True, default=True)
    entity = ObjectIdField(required=True)
    # TODO: is_list
    prompts = ListField(StringField(), required=True) # TODO default

class Intent(Document):
    agent_id = ObjectIdField(required=True)
    name = StringField(required=True)
    input_context = ListField(StringField())
    output_context = ListField(StringField())
    training_phrases = ListField(StringField())
    parameters = ListField(Parameter())
    end_of_conversation = BooleanField(required=True, default=False)
    responses = ListField(StringField())
    enable_webhook = BooleanField(required=True, default=False)
    enable_slot_filling_webhook = BooleanField(required=True, default=False)