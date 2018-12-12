import mongoengine
from models.entity import Entity
import os

mongo_settings = {
    'db': os.environ['MONGO_DBNAME'],
    'host': os.environ['MONGO_SERVER'],
    'port': int(os.environ['MONGO_PORT']),
    'username': os.environ.get('MONGO_USERNAME'),
    'password': os.environ.get('MONGO_PASSWORD')
}

mongoengine.connect(**mongo_settings)

org_id = "5bfe2702c4952fd462c4af3f"
entity = Entity.objects.get(id=org_id)

entity.entries_file.delete()
with open("data/file.txt") as f:
    cnt = f.read()
    entity.entries_file.new_file()
    entity.entries_file.write(cnt.encode("utf8"))
    entity.entries_file.close()
entity.save()
