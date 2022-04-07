from os.path import exists
from configparser import ConfigParser

config = ConfigParser()
config.read(".config/default.ini")

SSL = config["SSL_API"]


def isSSL(path_crt_file, path_key_file, path_pem_file):
    if exists(path_crt_file) and exists(path_key_file) and exists(path_pem_file):
        privateKey = open(SSL["KEY"], "r").read()
        certificate = open(SSL["CERTIFICATE"], "r").read()
        pem = open(SSL["PEM"], "r")
        ca = [pem.read()]

        return {"credentials": {"key": privateKey, "cert": certificate, "ca": ca}}
    else:
        return False
