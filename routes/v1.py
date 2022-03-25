import logging

from flask import Blueprint, jsonify, request
import json
from error import BadRequest, Conflict, Forbidden, InternalServerError, Unauthorized
from datetime import timedelta
from schemas.baseModel import db

LOG = logging.getLogger(__name__)
v1 = Blueprint("v1", __name__)

from models import (
    CREATE_USERS,
    VERIFY_USERS,
    CREATE_SESSION,
    FIND_SESSION,
    GENERATE_TOKEN,
    UPDATE_SESSION,
    VERIFY_TOKEN,
    FIND_USER_PROJECT,
    ADD_PROJECT,
    DELETE_PROJECT,
)


@v1.before_request
def before_request():
    db.connect()


@v1.after_request
def after_request(response):
    db.close()
    return response


@v1.route("/signup", methods=["POST"])
def signup():
    try:
        if not "email" in request.json or not request.json["email"]:
            LOG.error("no email")
            raise BadRequest()
        elif not "password" in request.json or not request.json["password"]:
            LOG.error("no password")
            raise BadRequest()

        email = request.json["email"]
        password = request.json["password"]

        CREATE_USERS(email, password)
        return "", 200
    except BadRequest as err:
        return str(err), 400
    except Conflict as err:
        return str(err), 409
    except (InternalServerError) as err:
        LOG.error(err)
        return "internal server error", 500
    except (Exception) as err:
        LOG.error(err)
        return "internal server error", 500


@v1.route("/login", methods=["POST"])
def login():
    try:
        if not "email" in request.json or not request.json["email"]:
            LOG.error("no email")
            raise BadRequest()
        elif not "password" in request.json or not request.json["password"]:
            LOG.error("no password")
            raise BadRequest()
        elif not request.headers.get("User-Agent"):
            LOG.error("no user agent")
            raise BadRequest()

        email = request.json["email"]
        password = request.json["password"]
        user_agent = request.headers.get("User-Agent")

        user = VERIFY_USERS(email, password)
        session = CREATE_SESSION(user["uid"], user_agent)

        res = jsonify(user)
        res.set_cookie(
            "SWOBDev",
            json.dumps({"sid": session["sid"], "cookie": session["data"]}),
            max_age=timedelta(milliseconds=session["data"]["maxAge"]),
            secure=session["data"]["secure"],
            httponly=session["data"]["httpOnly"],
            samesite=session["data"]["sameSite"],
        )

        return res, 200
    except BadRequest as err:
        return str(err), 400
    except Unauthorized as err:
        return str(err), 401
    except Conflict as err:
        return str(err), 409
    except (InternalServerError) as err:
        LOG.error(err)
        return "internal server error", 500
    except (Exception) as err:
        LOG.error(err)
        return "internal server error", 500


@v1.route("/users/<user_id>/tokens", methods=["GET"])
def get_tokens(user_id):
    try:
        if not user_id:
            LOG.error("no user id")
            raise BadRequest()
        elif not request.cookies.get("SWOBDev"):
            LOG.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            LOG.error("no user agent")
            raise BadRequest()

        str_cookie = request.cookies.get("SWOBDev")
        json_cookie = json.loads(str_cookie)

        SID = json_cookie["sid"]
        UID = user_id
        COOKIE = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        ID = FIND_SESSION(SID, UID, user_agent, COOKIE)
        tokens = GENERATE_TOKEN(ID)

        session = UPDATE_SESSION(SID, ID)

        res = jsonify(tokens)

        res.set_cookie(
            "SWOBDev",
            json.dumps({"sid": session["sid"], "cookie": session["data"]}),
            max_age=timedelta(milliseconds=session["data"]["maxAge"]),
            secure=session["data"]["secure"],
            httponly=session["data"]["httpOnly"],
            samesite=session["data"]["sameSite"],
        )

        return res, 200
    except BadRequest as err:
        return str(err), 400
    except Unauthorized as err:
        return str(err), 401
    except Conflict as err:
        return str(err), 409
    except (InternalServerError) as err:
        LOG.error(err)
        return "internal server error", 500
    except (Exception) as err:
        LOG.error(err)
        return "internal server error", 500


@v1.route("/authenticate", methods=["POST"])
def authenticate():
    try:
        if not request.headers.get("User-Agent"):
            LOG.error("no user agent")
            raise BadRequest()
        elif not "auth_id" in request.json or not request.json["auth_id"]:
            LOG.error("no auth_id")
            raise BadRequest()
        elif not "auth_key" in request.json or not request.json["auth_key"]:
            LOG.error("no auth_key")
            raise BadRequest()

        user_agent = request.headers.get("User-Agent")
        AUTH_ID = request.json["auth_id"]
        AUTH_KEY = request.json["auth_key"]

        userId = VERIFY_TOKEN(AUTH_ID, AUTH_KEY)
        session = CREATE_SESSION(userId, user_agent)

        res = jsonify()

        res.set_cookie(
            "SWOBDev",
            json.dumps(
                {
                    "sid": session["sid"],
                    "userAgent": user_agent,
                    "uid": userId,
                    "cookie": session["data"],
                }
            ),
            max_age=timedelta(milliseconds=session["data"]["maxAge"]),
            secure=session["data"]["secure"],
            httponly=session["data"]["httpOnly"],
            samesite=session["data"]["sameSite"],
        )

        return res, 200
    except BadRequest as err:
        return str(err), 400
    except Unauthorized as err:
        return str(err), 401
    except Forbidden as err:
        return str(err), 403
    except Conflict as err:
        return str(err), 409
    except (InternalServerError) as err:
        LOG.error(err)
        return "internal server error", 500
    except (Exception) as err:
        LOG.error(err)
        return "internal server error", 500


@v1.route("/users/<user_id>/products", methods=["GET"])
def get_projects(user_id):
    try:
        if not user_id:
            LOG.error("no user id")
            raise BadRequest()
        elif not request.cookies.get("SWOBDev"):
            LOG.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            LOG.error("no user agent")
            raise BadRequest()

        str_cookie = request.cookies.get("SWOBDev")
        json_cookie = json.loads(str_cookie)

        SID = json_cookie["sid"]
        UID = user_id
        COOKIE = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        ID = FIND_SESSION(SID, UID, user_agent, COOKIE)
        projects = FIND_USER_PROJECT(ID)

        session = UPDATE_SESSION(SID, ID)

        res = jsonify(projects)

        res.set_cookie(
            "SWOBDev",
            json.dumps({"sid": session["sid"], "cookie": session["data"]}),
            max_age=timedelta(milliseconds=session["data"]["maxAge"]),
            secure=session["data"]["secure"],
            httponly=session["data"]["httpOnly"],
            samesite=session["data"]["sameSite"],
        )

        return res, 200
    except BadRequest as err:
        return str(err), 400
    except Unauthorized as err:
        return str(err), 401
    except Forbidden as err:
        return str(err), 403
    except Conflict as err:
        return str(err), 409
    except (InternalServerError) as err:
        LOG.error(err)
        return "internal server error", 500
    except (Exception) as err:
        LOG.error(err)
        return "internal server error", 500


@v1.route("/users/<user_id>/products/<product_name>", methods=["POST"])
def add_project(user_id, product_name):
    try:
        if not user_id:
            LOG.error("no user id")
            raise BadRequest()
        elif not product_name:
            LOG.error("no project name")
            raise BadRequest()
        elif not request.cookies.get("SWOBDev"):
            LOG.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            LOG.error("no user agent")
            raise BadRequest()

        str_cookie = request.cookies.get("SWOBDev")
        json_cookie = json.loads(str_cookie)

        SID = json_cookie["sid"]
        UID = user_id
        PROJECT_NAME = product_name
        COOKIE = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        ID = FIND_SESSION(SID, UID, user_agent, COOKIE)
        ADD_PROJECT(ID, PROJECT_NAME)

        session = UPDATE_SESSION(SID, ID)

        res = jsonify()

        res.set_cookie(
            "SWOBDev",
            json.dumps({"sid": session["sid"], "cookie": session["data"]}),
            max_age=timedelta(milliseconds=session["data"]["maxAge"]),
            secure=session["data"]["secure"],
            httponly=session["data"]["httpOnly"],
            samesite=session["data"]["sameSite"],
        )

        return res, 200
    except BadRequest as err:
        return str(err), 400
    except Unauthorized as err:
        return str(err), 401
    except Forbidden as err:
        return str(err), 403
    except Conflict as err:
        return str(err), 409
    except (InternalServerError) as err:
        LOG.error(err)
        return "internal server error", 500
    except (Exception) as err:
        LOG.error(err)
        return "internal server error", 500


@v1.route("/users/<user_id>/products/<product_name>", methods=["DELETE"])
def delete_project(user_id, product_name):
    try:
        if not user_id:
            LOG.error("no user id")
            raise BadRequest()
        elif not product_name:
            LOG.error("no project name")
            raise BadRequest()
        elif not request.cookies.get("SWOBDev"):
            LOG.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            LOG.error("no user agent")
            raise BadRequest()

        str_cookie = request.cookies.get("SWOBDev")
        json_cookie = json.loads(str_cookie)

        SID = json_cookie["sid"]
        UID = user_id
        PROJECT_NAME = product_name
        COOKIE = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        ID = FIND_SESSION(SID, UID, user_agent, COOKIE)
        DELETE_PROJECT(ID, PROJECT_NAME)

        session = UPDATE_SESSION(SID, ID)

        res = jsonify()

        res.set_cookie(
            "SWOBDev",
            json.dumps({"sid": session["sid"], "cookie": session["data"]}),
            max_age=timedelta(milliseconds=session["data"]["maxAge"]),
            secure=session["data"]["secure"],
            httponly=session["data"]["httpOnly"],
            samesite=session["data"]["sameSite"],
        )

        return res, 200
    except BadRequest as err:
        return str(err), 400
    except Unauthorized as err:
        return str(err), 401
    except Forbidden as err:
        return str(err), 403
    except Conflict as err:
        return str(err), 409
    except (InternalServerError) as err:
        LOG.error(err)
        return "internal server error", 500
    except (Exception) as err:
        LOG.error(err)
        return "internal server error", 500
