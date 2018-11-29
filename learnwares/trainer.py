from .sentence_simulator import SentenceGenerator
import mongoengine
import os
import multiprocessing as mp
from models.agent import Agent



def init_task(agent_id):
    mongo_config = {
        'db': os.environ['MONGO_DBNAME'],
        'host': os.environ['MONGO_SERVER'],
        'port': int(os.environ['MONGO_PORT']),
        'username': os.environ.get('MONGO_USERNAME'),
        'password': os.environ.get('MONGO_PASSWORD'),
    }
    mongoengine.connect(**mongo_config)

    agent = Agent.objects.get(id=agent_id)
    train(agent)

def train(agent):
    agent.training_state = "started"
    agent.save()

    try:
        sent_simulator = SentenceGenerator(agent)
        sent_simulator.generate_rules()
        sent_simulator.generate_data()
    except Exception as e:
        print(e)
        agent.training_state = "failed at sent generate"
        print(agent.training_state)
        agent.save()
        return
    agent.training_state = "sent generation done"
    agent.save()

    print("done")
    agent.training_state = "done"
    agent.save()

def start_training_process(agent):
    proc = mp.Process(target=init_task, args=(str(agent.id),))
    proc.start()

def test():
    from models.agent import Agent
    for agent in Agent.objects:
        print(agent.id)
        start_training_process(agent)

