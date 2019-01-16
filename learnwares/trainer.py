from .sentence_simulator import SentenceGenerator
import datetime
import mongoengine
import os
import multiprocessing as mp
from models.agent import Agent
import subprocess

CHATBOT_GENERATOR_PATH = '../Chatbot-generate/main.py'

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

def train_chatbot(agent_id):
    data_path = "data/{}/data/".format(agent_id)
    cp = subprocess.run([
        "python3",
        CHATBOT_GENERATOR_PATH,
        agent_id,
        '../bot_framework/' + data_path + "words.txt",
        '../bot_framework/' + data_path + "sents.txt.mapped"
    ], cwd='../Chatbot-generate')
    cp.check_returncode()

def train(agent):
    data_path = "data/{}/data/".format(str(agent.id))
    try:
        os.makedirs(data_path)
    except FileExistsError:
        pass

    agent.training_state = "started at " + str(datetime.datetime.now())
    agent.save()

    try:
        print('start sent gen')
        sent_simulator = SentenceGenerator(agent)
        sent_simulator.generate_rules()
        print('done generate rules')
        sent_simulator.generate_data()
        print('done generate data')
    except Exception as e:
        print(e)
        raise e
        agent.training_state = "failed at sent generate"
        print(agent.training_state)
        agent.save()
        return
    agent.training_state = "training models at " + str(datetime.datetime.now())
    agent.save()

    try:
        train_chatbot(str(agent.id))
    except Exception as e:
        print(e)
        agent.training_state = "failed at NER/classify training"
        print(agent.training_state)
        agent.save()
        return

    agent.training_state = "done at " + str(datetime.datetime.now())
    agent.save()

def start_training_process(agent):
    proc = mp.Process(target=init_task, args=(str(agent.id),))
    proc.start()

def test():
    from models.agent import Agent
    agent = Agent.objects.get(id="5bfe0b04c4952f342f394a42")
    start_training_process(agent)

