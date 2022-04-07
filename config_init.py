import os
from configparser import ConfigParser


def configuration():
    config = ConfigParser()
    config_filepath = os.path.join(os.path.dirname(__file__), ".config", "default.ini")
    config.read(config_filepath)
    return {
        "DATABASE": config["DATABASE"],
        "API": config["API"],
        "SSL_API": config["SSL_API"],
    }
