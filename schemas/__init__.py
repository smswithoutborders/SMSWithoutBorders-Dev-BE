import logging

logger = logging.getLogger(__name__)

from configparser import ConfigParser
from mysql.connector import connect, Error

config = ConfigParser()
config.read(".config/default.ini")

database = config["DATABASE"]

try:
    with connect(
        user=database["MYSQL_USER"],
        password=database["MYSQL_PASSWORD"],
        host=database["MYSQL_HOST"],
        auth_plugin="mysql_native_password"
    ) as connection:
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {database['MYSQL_DATABASE']};"
        with connection.cursor() as cursor:
            logger.debug(f"Creating database {database['MYSQL_DATABASE']} ...")
            cursor.execute(create_db_query)
            logger.info(f"Database {database['MYSQL_DATABASE']} successfully created")
except Error as e:
    print(e)
    raise

from schemas.baseModel import db
from schemas.users import Users
from schemas.sessions import Sessions
from schemas.projects import Products
from schemas.users_projects import Users_projects


def create_tables():
    logger.debug(f"Syncing database {database['MYSQL_DATABASE']} ...")
    db.create_tables([Users, Sessions, Products, Users_projects])

    product_info = ConfigParser()
    product_info.read("./products_info.ini")

    openApi_info = product_info["OPENAPI"]

    try:
        Products.get(Products.name == openApi_info["name"])
    except Products.DoesNotExist:
        logger.debug(f"Adding product {openApi_info['name']} ...")
        Products.create(
            name=openApi_info["name"],
            label=openApi_info["label"],
            description=openApi_info["description"],
            documentation=openApi_info["documentation"],
        )

    logger.info(f"Successfully Sync database {database['MYSQL_DATABASE']}")
