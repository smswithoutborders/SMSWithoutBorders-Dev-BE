import peewee as pw
from schemas.baseModel import BaseModel
from datetime import datetime


class Products(BaseModel):
    name = pw.CharField(null=True)
    description = pw.CharField(null=True)
    label = pw.CharField(null=True)
    documentation = pw.CharField(null=True)
    createdAt = pw.DateTimeField(null=True, default=datetime.now())
