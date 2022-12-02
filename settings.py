import os

MODE = os.environ.get("MODE")

if MODE and MODE.lower() == "production":
    class production:
        SSL_PORT = os.environ["SSL_PORT"]
        SSL_CERTIFICATE = os.environ["SSL_CERTIFICATE"]
        SSL_KEY = os.environ["SSL_KEY"]
        SSL_PEM = os.environ["SSL_PEM"]

        SECURE_COOKIE = True

    baseConfig = production

else:
    class development:
        SSL_PORT = os.environ.get("SSL_PORT") 
        SSL_CERTIFICATE = os.environ.get("SSL_CERTIFICATE") or "" 
        SSL_KEY = os.environ.get("SSL_KEY") or "" 
        SSL_PEM = os.environ.get("SSL_PEM") or "" 

        SECURE_COOKIE = False
    
    baseConfig = development

class Configurations(baseConfig):
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")

    COOKIE_NAME = "SWOBDev"
    COOKIE_MAXAGE = 7200000 #ms 2hrs

    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")
    ORIGINS = os.environ.get("ORIGINS")

    ID = os.environ.get("ID")
    KEY = os.environ.get("KEY")

    SHARED_KEY = os.environ.get("SHARED_KEY") or "de4053831a43d62d9e68fc11319270a9" 
    HASHING_SALT = os.environ.get("HASHING_SALT") or "acaad78fd9dadcb056840c09073190a8"

    PROJECTS_INFO_PATH = os.path.join(os.path.dirname(__file__), "products", "info.json")

    OPENAPI_HOST = os.environ["OPENAPI_HOST"]
    OPENAPI_PORT = os.environ["OPENAPI_PORT"]
    OPENAPI_VERSION = os.environ["OPENAPI_VERSION"]