import peewee as pw
from schemas.baseModel import BaseModel

class Sessions(BaseModel):
    sid = pw.CharField(primary_key=True)
    unique_identifier = pw.CharField(null=True)
    user_agent = pw.CharField(null=True)
    expires = pw.DateTimeField(null=True)
    data = pw.TextField(null=True)