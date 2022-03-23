import peewee as pw
from schemas.baseModel import BaseModel
from datetime import datetime


class Projects(BaseModel):
    name = pw.CharField(null=True)
    createdAt = pw.DateTimeField(null=True, default=datetime.now())
