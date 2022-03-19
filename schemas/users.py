import peewee as pw
from schemas.baseModel import BaseModel

class Users(BaseModel):
    id = pw.CharField(primary_key=True)
    email = pw.CharField(unique=True, null=True)
    password = pw.CharField(null=True)
    auth_key = pw.CharField(unique=True, null=True)
    auth_id = pw.CharField(unique=True, null=True)