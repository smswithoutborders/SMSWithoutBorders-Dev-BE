import logging
logger = logging.getLogger(__name__)

from flask import Blueprint
from flask import jsonify
from flask import request
v1 = Blueprint("v1", __name__)

import json
import base64
from datetime import timedelta

from schemas.baseModel import db

from models.create_users import create_user
from models.verify_users import verify_user
from models.create_sessions import create_session
from models.find_sessions import find_session
from models.generate_tokens import generate_token
from models.update_sessions import update_session
from models.verify_tokens import verify_token
from models.find_users_projects import find_users_projects
from models.add_projects import add_products
from models.delete_projects import delete_projects

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Forbidden
from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import BadRequest

@v1.after_request
def after_request(response):
    db.close()
    return response

@v1.route("/signup", methods=["POST"])
def signup() -> None:
    """
    """
    try:
        if not "email" in request.json or not request.json["email"]:
            logger.error("no email")
            raise BadRequest()
        elif not "password" in request.json or not request.json["password"]:
            logger.error("no password")
            raise BadRequest()

        email = request.json["email"]
        password = request.json["password"]

        userId = create_user(email, password)
        generate_token(userId)

        return "", 200

    except BadRequest as err:
        return str(err), 400

    except Conflict as err:
        return str(err), 409

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/login", methods=["POST"])
def login() -> dict:
    """
    """
    try:
        if not "email" in request.json or not request.json["email"]:
            logger.error("no email")
            raise BadRequest()
        elif not "password" in request.json or not request.json["password"]:
            logger.error("no password")
            raise BadRequest()
        elif not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()

        email = request.json["email"]
        password = request.json["password"]
        user_agent = request.headers.get("User-Agent")

        user = verify_user(email, password)
        session = create_session(user["uid"], user_agent)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<string:user_id>/tokens", methods=["GET"])
def get_tokens(user_id) -> dict:
    """
    """
    try:
        if not user_id:
            logger.error("no user id")
            raise BadRequest()
        elif not request.cookies.get("SWOBDev"):
            logger.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()

        str_cookie = request.cookies.get("SWOBDev")
        json_cookie = json.loads(str_cookie)

        sid = json_cookie["sid"]
        uid = user_id
        cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        userId = find_session(sid, uid, user_agent, cookie)
        tokens = generate_token(userId)

        session = update_session(sid, userId)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/authenticate", methods=["POST"])
def authenticate() -> None:
    """
    """
    try:
        if not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()
        elif not "auth_id" in request.json or not request.json["auth_id"]:
            logger.error("no auth_id")
            raise BadRequest()
        elif not "auth_key" in request.json or not request.json["auth_key"]:
            logger.error("no auth_key")
            raise BadRequest()

        user_agent = request.headers.get("User-Agent")
        auth_id = request.json["auth_id"]
        auth_key = request.json["auth_key"]

        userId = verify_token(auth_id, auth_key)
        session = create_session(userId, user_agent)

        res = jsonify()

        cookie_base64 = json.dumps(
            {
                "userAgent": user_agent,
                "uid": session["uid"],
                "cookie": session["data"],
                "verification_path": f"v1/sessions/{session['sid']}",
            }
        )

        cookie_base64 = base64.b64encode(bytes(cookie_base64, "utf-8"))

        res.set_cookie(
            "SWOBDev",
            cookie_base64,
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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<string:user_id>/products", methods=["GET"])
def get_products(user_id) -> dict:
    """
    """
    try:
        if not user_id:
            logger.error("no user id")
            raise BadRequest()
        elif not request.cookies.get("SWOBDev"):
            logger.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()

        str_cookie = request.cookies.get("SWOBDev")
        json_cookie = json.loads(str_cookie)

        sid = json_cookie["sid"]
        uid = user_id
        cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        userId = find_session(sid, uid, user_agent, cookie)
        projects = find_users_projects(userId)

        session = update_session(sid, userId)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<string:user_id>/products/<string:product_name>", methods=["POST"])
def addProducts(user_id, product_name) -> None:
    """
    """
    try:
        if not user_id:
            logger.error("no user id")
            raise BadRequest()
        elif not product_name:
            logger.error("no project name")
            raise BadRequest()
        elif not request.cookies.get("SWOBDev"):
            logger.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()

        str_cookie = request.cookies.get("SWOBDev")
        json_cookie = json.loads(str_cookie)

        sid = json_cookie["sid"]
        uid = user_id
        projectName = product_name
        cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        userId = find_session(sid, uid, user_agent, cookie)
        add_products(userId, projectName)

        session = update_session(sid, userId)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/users/<string:user_id>/products/<string:product_name>", methods=["DELETE"])
def deleteProducts(user_id, product_name) -> None:
    """
    """
    try:
        if not user_id:
            logger.error("no user id")
            raise BadRequest()
        elif not product_name:
            logger.error("no project name")
            raise BadRequest()
        elif not request.cookies.get("SWOBDev"):
            logger.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()

        str_cookie = request.cookies.get("SWOBDev")
        json_cookie = json.loads(str_cookie)

        sid = json_cookie["sid"]
        uid = user_id
        projectName = product_name
        cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        userId = find_session(sid, uid, user_agent, cookie)
        delete_projects(userId, projectName)

        session = update_session(sid, userId)

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

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500

@v1.route("/sessions/<string:session_id>", methods=["POST"])
def sessions_auth(session_id) -> None:
    """
    """
    try:
        if not "user_agent" in request.json or not request.json["user_agent"]:
            logger.error("no user_agent")
            raise BadRequest()
        elif not "uid" in request.json or not request.json["uid"]:
            logger.error("no uid")
            raise BadRequest()
        elif not "cookie" in request.json or not request.json["cookie"]:
            logger.error("no cookie")
            raise BadRequest()

        user_agent = request.json["user_agent"]
        sid = session_id
        uid = request.json["uid"]
        cookie = request.json["cookie"]

        find_session(sid, uid, user_agent, cookie)

        return "", 200

    except BadRequest as err:
        return str(err), 400

    except Unauthorized as err:
        return str(err), 401

    except Forbidden as err:
        return str(err), 403

    except Conflict as err:
        return str(err), 409

    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500