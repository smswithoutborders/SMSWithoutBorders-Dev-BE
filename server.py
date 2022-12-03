import logging
import argparse
import ssl

from settings import Configurations
ssl_cert = Configurations.SSL_CERTIFICATE
ssl_port = Configurations.SSL_PORT
ssl_key = Configurations.SSL_KEY
ssl_pem = Configurations.SSL_PEM
api_host = Configurations.HOST
api_port = Configurations.PORT
api_origins = Configurations.ORIGINS

# logger
parser = argparse.ArgumentParser()

parser = argparse.ArgumentParser()
parser.add_argument("--logs", help="Set log level")
args = parser.parse_args()

log_level = args.logs or "info"
numeric_level = getattr(logging, log_level.upper(), None)

if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: %s" % log_level)

logging.basicConfig(level=numeric_level)

from flask import Flask
from flask_cors import CORS

from src.api_v1 import v1

from utils.SSL import isSSL

app = Flask(__name__)

CORS(
    app,
    origins=api_origins,
    supports_credentials=True,
)

app.register_blueprint(v1, url_prefix="/v1")

checkSSL = isSSL(path_crt_file=ssl_cert, path_key_file=ssl_key, path_pem_file=ssl_pem)

if __name__ == "__main__":
    if checkSSL:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(ssl_cert, ssl_key)

        app.logger.info("Running on secure port: %s" % ssl_port)
        app.run(host=api_host, port=ssl_port, ssl_context=context)
    else:
        app.logger.info("Running on un-secure port: %s" % api_port)
        app.run(host=api_host, port=api_port)
