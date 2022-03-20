import hashlib
import hmac
from configparser import ConfigParser

config = ConfigParser()
config.read('.config/default.ini')
api = config['API']
salt = api['SALT']

class Security():
    def __init__(self) -> None:
        pass

    def hash(data):
        hash_data = hmac.new(salt.encode('utf-8'), data.encode('utf-8'), hashlib.sha512)
        return str(hash_data.hexdigest())
