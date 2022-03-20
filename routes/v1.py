import logging

from flask import Blueprint, jsonify, request
from error import Conflict, InternalServerError
from schemas.baseModel import db

LOG = logging.getLogger(__name__)
v1 = Blueprint('v1', __name__)

from models import CREATE_USERS

@v1.before_request
def before_request():
    db.connect()

@v1.after_request
def after_request(response):
    db.close()
    return response

@v1.route('/signup', methods=['POST'])
def signup():
    try:
        if not 'email' in request.json or not request.json['email']:
            LOG.error('no email')
            return 'bad request', 400
        elif not 'password' in request.json or not request.json['password']:
            LOG.error('no password')
            return 'bad request', 400
        
        email = request.json['email']
        password = request.json['password']

        CREATE_USERS(email, password)
        return jsonify({}), 200
    except Conflict as err:
        return str(err), 409
    except (InternalServerError, Exception) as err:
        LOG.error(err)
        return "internal server error", 500