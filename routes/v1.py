import logging

from flask import Blueprint, jsonify, request
import json
from error import BadRequest, Conflict, InternalServerError, Unauthorized
from datetime import timedelta
from schemas.baseModel import db

LOG = logging.getLogger(__name__)
v1 = Blueprint('v1', __name__)

from models import CREATE_USERS, VERIFY_USERS, CREATE_SESSION, FIND_SESSION, GENERATE_TOKEN, UPDATE_SESSION

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
            raise BadRequest()
        elif not 'password' in request.json or not request.json['password']:
            LOG.error('no password')
            raise BadRequest()
        
        email = request.json['email']
        password = request.json['password']

        CREATE_USERS(email, password)
        return '', 200
    except BadRequest as err:
        return str(err), 400
    except Conflict as err:
        return str(err), 409
    except (InternalServerError, Exception) as err:
        LOG.error(err)
        return "internal server error", 500

@v1.route('/login', methods=['POST'])
def login():
    try:
        if not 'email' in request.json or not request.json['email']:
            LOG.error('no email')
            raise BadRequest()
        elif not 'password' in request.json or not request.json['password']:
            LOG.error('no password')
            raise BadRequest()
        elif not request.headers.get('User-Agent'):
            LOG.error('no user agent')
            raise BadRequest()
        
        email = request.json['email']
        password = request.json['password']
        user_agent = request.headers.get('User-Agent')

        user = VERIFY_USERS(email, password)
        session = CREATE_SESSION(user['uid'], user_agent)
        
        res = jsonify(user)
        res.set_cookie("SWOBDev", str({"sid": session['sid'], "cookie": session['data']}), max_age=timedelta(milliseconds=session['data']['maxAge']), secure=session['data']['secure'], httponly=session['data']['httpOnly'], samesite=session['data']['sameSite'])

        return res, 200
    except BadRequest as err:
        return str(err), 400
    except Unauthorized as err:
        return str(err), 401
    except Conflict as err:
        return str(err), 409
    except (InternalServerError, Exception) as err:
        LOG.error(err)
        return "internal server error", 500

@v1.route('/users/<user_id>/tokens', methods=['GET'])
def get_tokens(user_id):
    try:
        if not user_id:
            LOG.error('no user id')
            raise BadRequest()
        elif not request.cookies.get("SWOBDev"):
            LOG.error('no cookie')
            raise Unauthorized()
        elif not request.headers.get('User-Agent'):
            LOG.error('no user agent')
            raise BadRequest()
        
        str_cookie = request.cookies.get("SWOBDev")
        str_cookie = str_cookie.replace("'", "\"")
        str_cookie = str_cookie.replace(": False", ": \"False\"")
        str_cookie = str_cookie.replace(": True", ": \"True\"")
        json_cookie = json.loads(str_cookie) 

        SID = json_cookie['sid']
        UID = user_id
        COOKIE = json_cookie['cookie']
        user_agent = request.headers.get('User-Agent')

        ID = FIND_SESSION(SID, UID, user_agent, COOKIE)
        tokens = GENERATE_TOKEN(ID)

        session = UPDATE_SESSION(SID, ID)
    
        res = jsonify(tokens)

        res.set_cookie("SWOBDev", str({"sid": session['sid'], "cookie": session['data']}), max_age=timedelta(milliseconds=session['data']['maxAge']), secure=session['data']['secure'], httponly=session['data']['httpOnly'], samesite=session['data']['sameSite'])

        return res, 200
    except BadRequest as err:
        return str(err), 400
    except Unauthorized as err:
        return str(err), 401
    except Conflict as err:
        return str(err), 409
    except (InternalServerError, Exception) as err:
        LOG.error(err)
        return "internal server error", 500