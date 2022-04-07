import logging
import ssl

from flask import Flask
from configparser import ConfigParser
from routes.v1 import v1
from schemas import create_tables
from flask_swagger_ui import get_swaggerui_blueprint
from logger import logger
from models.isSSL import isSSL

logger()
server_logger = logging.getLogger(__name__)

config = ConfigParser()
config_filepath = os.path.join(os.path.dirname(__file__), '.config', 'default.ini')
config.read(config_filepath)

api = config["API"]
SSL = config["SSL_API"]

create_tables()

app = Flask(__name__)

swaggerui_blueprint = get_swaggerui_blueprint(
    "/v1/api-docs", "/static/v1-api-docs.json"
)

app.register_blueprint(swaggerui_blueprint)

app.register_blueprint(v1, url_prefix="/v1")

checkSSL = isSSL(SSL["CERTIFICATE"], SSL["KEY"], SSL["PEM"])

if __name__ == "__main__":
    if checkSSL:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(SSL["CERTIFICATE"], SSL["KEY"])

        server_logger.info(f"Running on secure port: {SSL['PORT']}")
        app.run(host=api["HOST"], port=SSL["PORT"], ssl_context=context)
    else:
        server_logger.info(f"Running on un-secure port: {api['PORT']}")
        app.run(host=api["HOST"], port=api["PORT"])