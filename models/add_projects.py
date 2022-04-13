import logging

from error import BadRequest, Conflict, Forbidden, InternalServerError, Unauthorized

import peewee as pw
import requests
from schemas import Users_projects, Products, Users
from products import openapi

from config_init import configuration

config = configuration()

logger = logging.getLogger(__name__)


def add_products(uid, product_name):
    try:
        logger.debug(f"checking {uid}'s status for {product_name}...")

        try:
            pid = Products.get(Products.name == product_name)
        except Products.DoesNotExist:
            logger.error("INVALID PRODUCT")
            raise Forbidden()

        try:
            user = Users.get(Users.id == uid)
        except Users.DoesNotExist:
            logger.error("USER DOESN'T EXIST")
            raise Forbidden()

        try:
            Users_projects.get(
                Users_projects.user_id == uid, Users_projects.product_id == pid
            )
        except Users_projects.DoesNotExist:
            logger.debug(f"requesting for {product_name}'s subscription for {uid} ...")

            authId = user.auth_id
            authKey = user.auth_key

            SETUP = config["SETUP_CREDS"]
            setupId = SETUP["ID"]
            setupKey = SETUP["key"]

            data = {
                "auth_id": authId,
                "auth_key": authKey,
                "id": setupId,
                "key": setupKey,
            }

            if product_name == "openapi":
                HOST = openapi.HOST
                PORT = openapi.PORT
                VERSION = openapi.VERSION
                URL = f"{HOST}:{PORT}/{VERSION}/subscribe"

                response = requests.post(url=URL, json=data)
                if response.status_code == 401:
                    logger.error("INVALID SETUP CREDENTIALS")
                    raise Unauthorized()
                elif response.status_code == 200:
                    Users_projects.create(user_id=uid, product_id=pid)
                    logger.info(f"SUCCESSFULLY SUBSCRIBED {uid} FOR {product_name}")
                    return True
                elif response.status_code == 409:
                    logger.error(f"USER {uid} IS ALREADY SUBSCRIBED FOR {product_name}")
                    raise Conflict()
                elif response.status_code == 400:
                    logger.error(f"INCOMPLETE DATA. CHECK YOUR REQUEST BODY")
                    raise BadRequest()
                else:
                    logger.error(
                        f"OPENAPI SERVER FAILED WITH STATUS CODE {response.status_code}"
                    )
                    raise InternalServerError(response.text)
            else:
                logger.error("INVALID PRODUCT")
                raise Forbidden()

        logger.error(f"{uid} ALREADY SUBSCRIBED FOR {product_name}")
        raise Conflict()

    except pw.DatabaseError as err:
        raise InternalServerError(err)
