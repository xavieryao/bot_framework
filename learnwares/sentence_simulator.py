from models.intent import Intent
from models.entity import Entity
from models.agent import Agent
import json

class SentenceGenerator:
    def __init__(self, agent):
        self.agent = agent


    def generate_rules(self):
        rules = {
            "rule": {
                "type": "root",
                "children": []
            },
            "entity": []
        }
        intents = Intent.objects(agent=self.agent)
        for intent in intents:
            intent_dict = dict(intent.tree)
            rules['rule']['children'].append(intent_dict)
        entities = Entity.objects(agent=self.agent)
        for entity in entities:
            entity_dict = entity.to_view()
            del entity_dict['description']
            del entity_dict['agent_id']
            rules['entity'].append(entity_dict)
        return rules

def test():
    for agent in Agent.objects:
        print(agent.id)
        generator = SentenceGenerator(agent)
        rules = generator.generate_rules()
        print(rules)
        with open("data/{}.json".format(agent.id), "w") as f:
            json.dump(rules, f, indent=2)