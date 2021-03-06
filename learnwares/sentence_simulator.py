from models.intent import Intent
from models.entity import Entity
from models.agent import Agent
import json
import subprocess
import os

class SentenceGenerator:
    SENTENCE_GENERATOR_PATH = '../sentence-simulator/main.py'
    SENT_COUNT = 1_000_000
    NER_COUNT =  1_000_000

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
            intent_dict['name'] = str(intent.id)
            rules['rule']['children'].append(intent_dict)
        entities = Entity.objects(agent=self.agent)
        for entity in entities:
            entity_dict = entity.to_view()
            del entity_dict['description']
            del entity_dict['agent_id']
            entity_dict['entries'] = entity.entries_to_view()
            print(len(entity_dict['entries']))
            if len(entity_dict['entries']) == 0:
                print('EMPTY')
                entity_dict['entries'].append('PLACEHOLDER')
            rules['entity'].append(entity_dict)
        return rules

    def generate_data(self):
        data_path = "data/{}/data/".format(self.agent.id)
        try:
            os.makedirs(data_path)
        except FileExistsError:
            pass
        rules = self.generate_rules()

        rules_path = os.path.join(data_path, "sent_sim_rules.json")
        sent_path = os.path.join(data_path, "sents.txt")
        word_path = os.path.join(data_path, "words.txt")
        map_path = os.path.join(data_path, "mapping.json")

        with open(rules_path, 'w') as f:
            json.dump(rules, f)
        print('rules generated')

        cmd = [
            "python3",
            self.SENTENCE_GENERATOR_PATH,
            "-f",
            rules_path,
            "-c",
            str(self.SENT_COUNT),
            "-w",
            word_path,
            "-s",
            sent_path,
            "-m",
            map_path
        ] #, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(cmd)
        cp = subprocess.run(cmd)
        cp.check_returncode()

def test():
    for agent in Agent.objects:
        print(agent.id)
        generator = SentenceGenerator(agent)
        rules = generator.generate_rules()
        print(rules)
        with open("data/{}.json".format(agent.id), "w") as f:
            json.dump(rules, f, indent=2)
