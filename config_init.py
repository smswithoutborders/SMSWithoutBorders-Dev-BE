import os
from configparser import ConfigParser

def configuration() -> dict:
    """
    Read configuration files and serve throughtout the application

    Arguments:
        None
        
    Returns:
        dict
    """
    config_filepath = os.path.abspath(os.path.join(".config", "default.ini"))
    products_filepath = os.path.abspath(os.path.join(".config", "products.ini"))
    setup_filepath = os.path.abspath(os.path.join(".config", "setup.ini"))

    if not os.path.exists(config_filepath):
        error = "default.ini file not found at %s" % config_filepath
        raise FileNotFoundError(error)
    elif not os.path.exists(products_filepath):
        error = "products.ini file not found at %s" % products_filepath
        raise FileNotFoundError(error)
    elif not os.path.exists(setup_filepath):
        error = "setup.ini file not found at %s" % setup_filepath
        raise FileNotFoundError(error)

    config = ConfigParser()
    config.read(config_filepath)

    products = ConfigParser()
    products.read(products_filepath)

    setup = ConfigParser()
    setup.read(setup_filepath)

    return {
        "DATABASE": config["DATABASE"],
        "API": config["API"],
        "SSL_API": config["SSL_API"],
        "PRODUCT": products,
        "SETUP_CREDS": setup["CREDENTIALS"],
    }
