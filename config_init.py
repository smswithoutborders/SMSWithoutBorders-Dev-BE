import os
from configparser import ConfigParser


def configuration():
    config = ConfigParser()
    config_filepath = os.path.join(os.path.dirname(__file__), ".config", "default.ini")
    config.read(config_filepath)

    product_info = ConfigParser()
    products_info_filepath = os.path.join(
        os.path.dirname(__file__), "products_info.ini"
    )
    product_info.read(products_info_filepath)

    setup = ConfigParser()
    setup_filepath = os.path.join(os.path.dirname(__file__), "setup.ini")
    setup.read(setup_filepath)

    return {
        "DATABASE": config["DATABASE"],
        "API": config["API"],
        "SSL_API": config["SSL_API"],
        "OPENAPI_INFO": product_info["OPENAPI"],
        "SETUP_CREDS": setup["CREDENTIALS"],
    }
