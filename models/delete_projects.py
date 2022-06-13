import logging
logger = logging.getLogger(__name__)

from config_init import configuration
config = configuration()

from peewee import DatabaseError

from schemas.users_projects import Users_projects
from schemas.projects import Products
from schemas.users import Users

import requests

from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import Forbidden
from werkzeug.exceptions import InternalServerError

def delete_projects(uid: str, product_name: str) -> bool:
    """
    """
    try:
        logger.debug("checking %s's status for %s..." % (uid, product_name))

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
            logger.error("User is not subscribed for %s" % product_name)
            return True

        logger.debug("requesting for %s's unsubscription for %s ..." % (product_name, uid))

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

        try:
            PRODUCTS = config["PRODUCT"]
            HOST = PRODUCTS["%s" % product_name]["host"] 
            PORT = PRODUCTS["%s" % product_name]["port"] 
            VERSION = PRODUCTS["%s" % product_name]["version"]
            URL = "%s:%s/%s/unsubscribe" % (HOST, PORT, VERSION)

            response = requests.delete(url=URL, json=data)
            if response.status_code == 401:
                logger.error("INVALID SETUP CREDENTIALS")
                raise Unauthorized()
            elif response.status_code == 200:
                remove_project = project.delete().where(Users_projects.user_id == uid, Users_projects.product_id == pid)
                remove_project.execute()

                logger.info("- SUCCESSFULLY UNSUBSCRIBED %s FOR %s" % (uid, product_name))
                return True
            else:
                logger.error("OPENAPI SERVER FAILED WITH STATUS CODE %s" % response.status_code)
                raise InternalServerError(response)

        except KeyError as error:
                logger.error("%s not found in products.ini file" % product_name)
                raise InternalServerError(error) from None 
                
        except Exception as error:
            raise InternalServerError(error) from None

    except DatabaseError as err:
        raise InternalServerError(err) from None
