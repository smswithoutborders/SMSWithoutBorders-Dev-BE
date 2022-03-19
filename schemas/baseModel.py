from configparser import ConfigParser
import peewee as pw

config = ConfigParser()
config.read('.config/default.ini')
database = config['DATABASE']

try:
    db = pw.MySQLDatabase(
                database['MYSQL_DATABASE'],
                user=database['MYSQL_USER'],
                password=database['MYSQL_PASSWORD'],
                host=database['MYSQL_HOST']
            )

    class BaseModel(pw.Model):
        class Meta:
            database = db
except pw.DatabaseError as e:
    print(e)