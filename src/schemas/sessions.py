from datetime import datetime

from uuid import uuid4

from peewee import Model, CharField, DateTimeField, TextField

from src.schemas.db_connector import db

class Sessions(Model):
    sid = CharField(primary_key=True, default=uuid4)
    unique_identifier = CharField(null=True)
    user_agent = CharField(null=True)
    expires = DateTimeField(null=True)
    data = TextField(null=True)
    createdAt = DateTimeField(null=True, default=datetime.now)

    class Meta:
        database = db

if db.table_exists('sessions') is False:
    db.create_tables([Sessions])