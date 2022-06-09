import ssl
import argparse

# logger
parser = argparse.ArgumentParser()
parser.add_argument("--logs", help="Set log level")
args = parser.parse_args()
from logger import baseLogger
baseLogger(args.logs or "info")

from config_init import configuration

config = configuration()
api = config["API"]
SSL = config["SSL_API"]

from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from models.isSSL import isSSL

from routes.v1 import v1

from controllers.sync_database import create_database
from controllers.sync_database import create_tables
from controllers.sync_database import sync_products

app = Flask(__name__)

CORS(
    app,
    origins=api["ORIGINS"],
    supports_credentials=True,
)

create_database()
create_tables()
sync_products()

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

        app.logger.info("Running on secure port: %s" % SSL['PORT'])
        app.run(host=api["HOST"], port=SSL["PORT"], ssl_context=context)
    else:
        app.logger.info("Running on un-secure port: %s" % api['PORT'])
        app.run(host=api["HOST"], port=api["PORT"])
