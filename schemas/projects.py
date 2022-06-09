from peewee import CharField
from peewee import DateTimeField

from schemas.baseModel import BaseModel

from datetime import datetime

class Products(BaseModel):
    name = CharField(null=True)
    description = CharField(null=True)
    label = CharField(null=True)
    documentation = CharField(null=True)
    createdAt = DateTimeField(null=True, default=datetime.now)
