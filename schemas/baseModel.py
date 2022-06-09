from config_init import configuration
config = configuration()
database = config["DATABASE"]

from peewee import MySQLDatabase
from peewee import Model
from peewee import DatabaseError

from werkzeug.exceptions import InternalServerError

try:
    db = MySQLDatabase(
        database["MYSQL_DATABASE"],
        user=database["MYSQL_USER"],
        password=database["MYSQL_PASSWORD"],
        host=database["MYSQL_HOST"],
    )

    class BaseModel(Model):
        """
        Users database model.
        """
        class Meta:
            database = db

except DatabaseError as err:
    raise InternalServerError(err) from None
