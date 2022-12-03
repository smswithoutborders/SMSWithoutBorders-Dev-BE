import logging
import json
import base64
from datetime import timedelta

logger = logging.getLogger(__name__)

from settings import Configurations
cookie_name = Configurations.COOKIE_NAME

from flask import Blueprint
from flask import jsonify
from flask import request
v1 = Blueprint("v1", __name__)

from src.schemas.db_connector import db

from src.models.users import User_Model
from src.models.products import Product_Model
from src.models.sessions import Session_Model

from src.security.cookie import Cookie

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

        Users = User_Model()

        email = request.json["email"]
        password = request.json["password"]

        userId = Users.create(email=email, password=password)
        Users.generate_token(uid=userId)

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

        Users = User_Model()
        Sessions = Session_Model()
        cookie = Cookie()

        email = request.json["email"]
        password = request.json["password"]
        user_agent = request.headers.get("User-Agent")

        user = Users.verify(email=email, password=password)

        session = Sessions.create(
            unique_identifier=user["uid"],
            user_agent=user_agent
        )

        cookie_data = json.dumps({
            "sid": session["sid"],
            "cookie": session["data"]
        })

        e_cookie = cookie.encrypt(cookie_data)

        session_data = json.loads(session["data"])

        res = jsonify(user)

        res.set_cookie(
            cookie_name,
            e_cookie,
            max_age=timedelta(milliseconds=session_data["maxAge"]),
            secure=session_data["secure"],
            httponly=session_data["httpOnly"],
            samesite=session_data["sameSite"]
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

        Users = User_Model()
        Products = Product_Model()
        Sessions = Session_Model()
        cookie = Cookie()

        e_cookie = request.cookies.get(cookie_name)
        d_cookie = cookie.decrypt(e_cookie)
        json_cookie = json.loads(d_cookie)
        
        sid = json_cookie["sid"]
        uid = user_id
        user_cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        userId = Sessions.find(
            sid=sid,
            unique_identifier=uid,
            user_agent=user_agent,
            cookie=user_cookie
        )

        products = Products.purge(uid=uid)

        tokens = Users.generate_token(uid=userId)

        Products.resync(
            uid=uid,
            old_auth_id=tokens["old_auth_id"],
            products=products
        )

        session = Sessions.update(
            sid=sid,
            unique_identifier=userId
        )

        res = jsonify({
            "auth_key": tokens["auth_key"], 
            "auth_id": tokens["auth_id"]
        })

        cookie_data = json.dumps({
            "sid": session["sid"],
            "cookie": session["data"]
        })

        e_cookie = cookie.encrypt(cookie_data)

        session_data = json.loads(session["data"])

        res.set_cookie(
            cookie_name,
            e_cookie,
            max_age=timedelta(milliseconds=session_data["maxAge"]),
            secure=session_data["secure"],
            httponly=session_data["httpOnly"],
            samesite=session_data["sameSite"]
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

        Users = User_Model()
        Sessions = Session_Model()

        user_agent = request.headers.get("User-Agent")
        auth_id = request.json["auth_id"]
        auth_key = request.json["auth_key"]

        userId = Users.verify_token(
            auth_id=auth_id,
            auth_key=auth_key
        )
        
        session = Sessions.create(
            unique_identifier=userId,
            user_agent=user_agent
        )

        res = jsonify()

        session_data = json.loads(session["data"])

        cookie_base64 = json.dumps(
            {
                "userAgent": user_agent,
                "uid": session["uid"],
                "cookie": session["data"],
                "verification_path": f"v1/sessions/{session['sid']}"
            }
        )

        cookie_base64 = base64.b64encode(bytes(cookie_base64, "utf-8"))

        res.set_cookie(
            cookie_name,
            cookie_base64,
            max_age=timedelta(milliseconds=session_data["maxAge"]),
            secure=session_data["secure"],
            httponly=session_data["httpOnly"],
            samesite=session_data["sameSite"]
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

        Users = User_Model()
        Sessions = Session_Model()
        cookie = Cookie()

        e_cookie = request.cookies.get(cookie_name)
        d_cookie = cookie.decrypt(e_cookie)
        json_cookie = json.loads(d_cookie)

        sid = json_cookie["sid"]
        uid = user_id
        user_cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        userId = Sessions.find(
            sid=sid,
            unique_identifier=uid,
            user_agent=user_agent,
            cookie=user_cookie
        )

        projects = Users.find_projects(uid=userId)

        session = Sessions.update(
            sid=sid,
            unique_identifier=userId
        )

        res = jsonify(projects)

        cookie_data = json.dumps({
            "sid": session["sid"],
            "cookie": session["data"]
        })

        e_cookie = cookie.encrypt(cookie_data)

        session_data = json.loads(session["data"])

        res.set_cookie(
            cookie_name,
            e_cookie,
            max_age=timedelta(milliseconds=session_data["maxAge"]),
            secure=session_data["secure"],
            httponly=session_data["httpOnly"],
            samesite=session_data["sameSite"]
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

        Sessions = Session_Model()
        Products = Product_Model()
        cookie = Cookie()

        e_cookie = request.cookies.get(cookie_name)
        d_cookie = cookie.decrypt(e_cookie)
        json_cookie = json.loads(d_cookie)

        sid = json_cookie["sid"]
        uid = user_id
        projectName = product_name
        user_cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        userId = Sessions.find(
            sid=sid,
            unique_identifier=uid,
            user_agent=user_agent,
            cookie=user_cookie
        )
        
        Products.add(
            uid=userId, 
            product_name=projectName
        )

        session = Sessions.update(
            sid=sid,
            unique_identifier=userId
        )

        res = jsonify()

        cookie_data = json.dumps({
            "sid": session["sid"],
            "cookie": session["data"]
        })

        e_cookie = cookie.encrypt(cookie_data)

        session_data = json.loads(session["data"])

        res.set_cookie(
            cookie_name,
            e_cookie,
            max_age=timedelta(milliseconds=session_data["maxAge"]),
            secure=session_data["secure"],
            httponly=session_data["httpOnly"],
            samesite=session_data["sameSite"]
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

        Sessions = Session_Model()
        Products = Product_Model()
        cookie = Cookie()

        e_cookie = request.cookies.get(cookie_name)
        d_cookie = cookie.decrypt(e_cookie)
        json_cookie = json.loads(d_cookie)

        sid = json_cookie["sid"]
        uid = user_id
        projectName = product_name
        user_cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")

        userId = Sessions.find(
            sid=sid,
            unique_identifier=uid,
            user_agent=user_agent,
            cookie=user_cookie
        )

        Products.delete(uid=userId, product_name=projectName)

        session = Sessions.update(
            sid=sid,
            unique_identifier=userId
        )

        res = jsonify()

        cookie_data = json.dumps({
            "sid": session["sid"],
            "cookie": session["data"]
        })

        e_cookie = cookie.encrypt(cookie_data)

        session_data = json.loads(session["data"])

        res.set_cookie(
            cookie_name,
            e_cookie,
            max_age=timedelta(milliseconds=session_data["maxAge"]),
            secure=session_data["secure"],
            httponly=session_data["httpOnly"],
            samesite=session_data["sameSite"]
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

        Sessions = Session_Model()

        user_agent = request.json["user_agent"]
        sid = session_id
        uid = request.json["uid"]
        user_cookie = request.json["cookie"]

        Sessions.find(
            sid=sid,
            unique_identifier=uid,
            user_agent=user_agent,
            cookie=user_cookie
        )

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

@v1.route("/users/<string:user_id>/products/<string:product_name>/metrics", methods=["GET"])
def get_metrics(user_id, product_name) -> None:
    """
    """
    try:
        if not request.cookies.get("SWOBDev"):
            logger.error("no cookie")
            raise Unauthorized()
        elif not request.headers.get("User-Agent"):
            logger.error("no user agent")
            raise BadRequest()

        Sessions = Session_Model()
        Products = Product_Model()
        cookie = Cookie()

        e_cookie = request.cookies.get(cookie_name)
        d_cookie = cookie.decrypt(e_cookie)
        json_cookie = json.loads(d_cookie)

        sid = json_cookie["sid"]
        uid = user_id
        user_cookie = json_cookie["cookie"]
        user_agent = request.headers.get("User-Agent")
        projectName = product_name

        userId = Sessions.find(
            sid=sid,
            unique_identifier=uid,
            user_agent=user_agent,
            cookie=user_cookie
        )
        
        metric = Products.metric(uid=userId, product_name=projectName)

        session = Sessions.update(
            sid=sid,
            unique_identifier=userId
        )

        res = jsonify(metric)

        cookie_data = json.dumps({
            "sid": session["sid"],
            "cookie": session["data"]
        })

        e_cookie = cookie.encrypt(cookie_data)

        session_data = json.loads(session["data"])

        res.set_cookie(
            cookie_name,
            e_cookie,
            max_age=timedelta(milliseconds=session_data["maxAge"]),
            secure=session_data["secure"],
            httponly=session_data["httpOnly"],
            samesite=session_data["sameSite"]
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