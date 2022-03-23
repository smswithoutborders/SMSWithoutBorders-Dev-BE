import peewee as pw
from schemas.baseModel import BaseModel
from schemas.users import Users
from schemas.projects import Projects
from datetime import datetime


class Users_projects(BaseModel):
    user = pw.ForeignKeyField(Users)
    project = pw.ForeignKeyField(Projects)
    createdAt = pw.DateTimeField(null=True, default=datetime.now())
