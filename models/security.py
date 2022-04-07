import hashlib
import hmac
from config_init import configuration

config = configuration()
api = config["API"]
salt = api["SALT"]


class Security:
    def __init__(self) -> None:
        pass

    def hash(data):
        hash_data = hmac.new(salt.encode("utf-8"), data.encode("utf-8"), hashlib.sha512)
        return str(hash_data.hexdigest())
