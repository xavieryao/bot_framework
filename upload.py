import mongoengine
from models.entity import Entity
import os
from string import punctuation

mongo_settings = {
    'db': os.environ['MONGO_DBNAME'],
    'host': os.environ['MONGO_SERVER'],
    'port': int(os.environ['MONGO_PORT']),
    'username': os.environ.get('MONGO_USERNAME'),
    'password': os.environ.get('MONGO_PASSWORD')
}

mongoengine.connect(**mongo_settings)

def upload(entity_id, filename, limit):
    entity = Entity.objects.get(id=entity_id)

    try:
        entity.entries_file.delete()
    except:
        pass
    entity.entries_file.new_file()
    with open(filename, encoding='utf8') as f:
        i = 0
        for line in f:
            try:
                word, cnt = line[:-1].split('\t')
                word = word.strip(punctuation)
            except ValueError:
                print(line)
            if int(cnt) < limit:
                break
            out = (word + '\n').encode('utf8')
            entity.entries_file.write(out)
            i += 1
        print(filename, i)
        entity.entries_file.close()
    entity.save()

with open('input.txt') as f:
    for line in f:
        eid, fn, cnt = line.strip().split()
        cnt = int(cnt)
        upload(eid, fn, cnt)
