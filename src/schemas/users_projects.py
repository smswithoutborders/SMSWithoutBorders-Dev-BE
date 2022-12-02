from peewee import Model, ForeignKeyField, DateTimeField

from src.schemas.db_connector import db
from src.schemas.users import Users
from src.schemas.projects import Products

from datetime import datetime

class Users_projects(Model):
    user = ForeignKeyField(Users)
    product = ForeignKeyField(Products)
    createdAt = DateTimeField(null=True, default=datetime.now)

    class Meta:
        database = db

if db.table_exists('users_projects') is False:
    db.create_tables([Users_projects])
