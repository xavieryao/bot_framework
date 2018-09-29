from mongoengine import Document, EmbeddedDocument
from mongoengine import LazyReferenceField, StringField, ListField, BooleanField, IntField
from .entity import Entity
from .agent import Agent
from .intent import Intent

class Context(EmbeddedDocument):
    name = StringField(required=True)
    turns_to_expiry = IntField()

class Parameter(EmbeddedDocument):
    name = StringField(required=True)
    required = BooleanField(required=True, default=True)
    entity = LazyReferenceField(Entity, required=True)
    # TODO: is_list
    prompts = ListField(StringField(), required=True) # TODO default

class Workflow(Document):
    agent = LazyReferenceField(Agent, required=True)
    intent = LazyReferenceField(Intent, required=True)
    name = StringField(required=True)
    input_context = ListField(Context())
    output_context = ListField(Context())
    # TODO: reference to intent
    parameters = ListField(Parameter())
    end_of_conversation = BooleanField(required=True, default=False)
    responses = ListField(StringField())
    enable_webhook = BooleanField(required=True, default=False)
    enable_slot_filling_webhook = BooleanField(required=True, default=False)