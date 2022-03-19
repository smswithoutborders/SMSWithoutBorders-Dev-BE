import logging
from flask import Flask
from configparser import ConfigParser
from routes.v1 import v1
from schemas import create_tables

config = ConfigParser()
config.read('.config/default.ini')

api = config['API']

logging.basicConfig(level=logging.DEBUG)

create_tables()

app = Flask(__name__)
app.register_blueprint(v1, url_prefix='/v1')

if __name__ == '__main__':
    app.run(port=api["PORT"])