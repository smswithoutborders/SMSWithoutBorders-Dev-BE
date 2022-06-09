from peewee import ForeignKeyField
from peewee import DateTimeField

from schemas.baseModel import BaseModel
from schemas.users import Users
from schemas.projects import Products

from datetime import datetime

class Users_projects(BaseModel):
    user = ForeignKeyField(Users)
    product = ForeignKeyField(Products)
    createdAt = DateTimeField(null=True, default=datetime.now)
