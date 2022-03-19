import logging

from flask import Blueprint, jsonify
import peewee as pw
from uuid import uuid1, uuid4
from datetime import datetime
from schemas import Users
from schemas.baseModel import db

LOG = logging.getLogger(__name__)
v1 = Blueprint('v1', __name__)

@v1.before_request
def before_request():
    db.connect()

@v1.after_request
def after_request(response):
    db.close()
    return response

@v1.route('/hello/')
def hello():
    try:
        user = Users.create(id=uuid1(), email="test@tesasst.com", password="test")
        return jsonify({"user": str(user)}), 200
    except (pw.DatabaseError, TypeError) as e:
        LOG.error(e)
        return "internal server error", 500