from models.agent import Agent
from .sentence_simulator import SentenceGenerator
import subprocess
import mongoengine
import os

def train(agent):
    agent.training_state = "started"
    agent.save()
    print("done")
    agent.training_state = "done"
    agent.save()

def start_training_task(agent):


def test():
    for agent in Agent.objects:
        print(agent.id)
        start_training_task(agent)

if __name__ == '__main__':
    mongo_config = {
        'db': os.environ['MONGO_DBNAME'],
        'host': os.environ['MONGO_SERVER'],
        'port': int(os.environ['MONGO_PORT']),
        'username': os.environ.get('MONGO_USERNAME'),
        'password': os.environ.get('MONGO_PASSWORD'),
    }
    mongoengine.connect(**mongo_config)

