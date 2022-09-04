from peewee import CharField
from peewee import DateTimeField

from schemas.baseModel import BaseModel

from datetime import datetime
from uuid import uuid1

class Users(BaseModel):
    id = CharField(primary_key=True, default=uuid1)
    email = CharField(unique=True, null=True)
    password = CharField(null=True)
    auth_key = CharField(unique=True, null=True)
    auth_id = CharField(unique=True, null=True)
    createdAt = DateTimeField(null=True, default=datetime.now)
