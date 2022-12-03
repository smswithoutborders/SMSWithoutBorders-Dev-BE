from peewee import MySQLDatabase
from peewee import DatabaseError

from contextlib import closing
from mysql.connector import connect

from settings import Configurations
db_name = Configurations.MYSQL_DATABASE
db_host = Configurations.MYSQL_HOST
db_password = Configurations.MYSQL_PASSWORD
db_user = Configurations.MYSQL_USER

def CreateDatabase(user: str, password: str, database: str, host: str) -> None:
    """
    """
    try:
        with closing(
            connect(
                user=user,
                password=password,
                host=host,
                auth_plugin="mysql_native_password",
            )
        ) as connection:
            create_db_query = "CREATE DATABASE IF NOT EXISTS %s;" % database

            with closing(connection.cursor()) as cursor:
                cursor.execute(create_db_query)

    except Exception as error:
        raise error

try:
    CreateDatabase(
        database=db_name,
        host=db_host,
        password=db_password,
        user=db_user
    )

    db = MySQLDatabase(
        db_name,
        user=db_user,
        password=db_password,
        host=db_host,
    )

except DatabaseError as err:
    raise err