from peewee import CharField
from peewee import DateTimeField
from peewee import TextField

from schemas.baseModel import BaseModel

from datetime import datetime

from uuid import uuid4

class Sessions(BaseModel):
    sid = CharField(primary_key=True, default=uuid4)
    unique_identifier = CharField(null=True)
    user_agent = CharField(null=True)
    expires = DateTimeField(null=True)
    data = TextField(null=True)
    createdAt = DateTimeField(null=True, default=datetime.now)