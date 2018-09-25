from flask import Flask
from mongoengine import connect
from apis.user import user_apis


app = Flask(__name__)
connect('bot_framework')
app.register_blueprint(user_apis, url_prefix='/v1/user/')

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()