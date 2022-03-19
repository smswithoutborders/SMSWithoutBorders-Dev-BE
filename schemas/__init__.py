import logging
LOG = logging.getLogger(__name__)

from configparser import ConfigParser
from mysql.connector import connect, Error
  
config = ConfigParser()
config.read('.config/default.ini')

database = config['DATABASE']

try:
    with connect(
        user=database['MYSQL_USER'],
        password=database['MYSQL_PASSWORD'],
        host=database['MYSQL_HOST'],
    ) as connection:
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {database['MYSQL_DATABASE']};"
        with connection.cursor() as cursor:
            LOG.debug(f"Creating database {database['MYSQL_DATABASE']} ...")
            cursor.execute(create_db_query) 
            LOG.info(f"Database {database['MYSQL_DATABASE']} successfully created")
except Error as e:
    print(e)
    raise

from schemas.baseModel import db
from schemas.users import Users
from schemas.sessions import Sessions

def create_tables():
    LOG.debug(f"Syncing database {database['MYSQL_DATABASE']} ...")
    db.create_tables([Users, Sessions])
    LOG.info(f"Successfully Sync database {database['MYSQL_DATABASE']}")
