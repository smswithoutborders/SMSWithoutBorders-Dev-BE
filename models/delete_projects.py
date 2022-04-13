import logging

from error import Unauthorized, Forbidden, InternalServerError

import peewee as pw
from schemas import Users_projects, Products, Users
from products import openapi
import requests

from config_init import configuration

config = configuration()

logger = logging.getLogger(__name__)


def delete_projects(uid, product_name):
    try:
        logger.debug(f"checking {uid}'s status for {product_name}...")

        try:
            pid = Products.get(Products.name == product_name)
        except Products.DoesNotExist:
            logger.error("INVALID PROJECT")
            raise Forbidden()

        try:
            user = Users.get(Users.id == uid)
        except Users.DoesNotExist:
            logger.error("USER DOESN'T EXIST")
            raise Forbidden()

        try:
            project = Users_projects.get(
                Users_projects.user_id == uid, Users_projects.product_id == pid
            )
        except Users_projects.DoesNotExist:
            logger.error(f"User is not subscribed for {product_name}")
            return True

        logger.debug(f"requesting for {product_name}'s unsubscription for {uid} ...")

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
            URL = f"{HOST}:{PORT}/{VERSION}/unsubscribe"

            response = requests.delete(url=URL, json=data)
            if response.status_code == 401:
                logger.error("INVALID SETUP CREDENTIALS")
                raise Unauthorized()
            elif response.status_code == 200:
                remove_project = project.delete().where(
                    Users_projects.user_id == uid, Users_projects.product_id == pid
                )
                remove_project.execute()

                logger.info(f"SUCCESSFULLY UNSUBSCRIBED {uid} FOR {product_name}")
                return True
            else:
                logger.error(
                    f"OPENAPI SERVER FAILED WITH STATUS CODE {response.status_code}"
                )
                raise InternalServerError(response.text)
        else:
            logger.error("INVALID PRODUCT")
            raise Forbidden()
    except (pw.DatabaseError) as err:
        raise InternalServerError(err)
