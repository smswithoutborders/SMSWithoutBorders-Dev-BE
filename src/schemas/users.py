from peewee import Model, CharField, DateTimeField

from src.schemas.db_connector import db

from datetime import datetime
from uuid import uuid1

class Users(Model):
    id = CharField(primary_key=True, default=uuid1)
    email = CharField(unique=True, null=True)
    password = CharField(null=True)
    auth_key = CharField(unique=True, null=True)
    auth_id = CharField(unique=True, null=True)
    createdAt = DateTimeField(null=True, default=datetime.now)

    class Meta:
        database = db

if db.table_exists('users') is False:
    db.create_tables([Users])