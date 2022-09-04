import logging
logger = logging.getLogger(__name__)

from config_init import configuration

config = configuration()
SETUP = config["SETUP_CREDS"]
PRODUCTS = config["PRODUCT"]

import requests

from peewee import DatabaseError

from schemas.users_projects import Users_projects
from schemas.projects import Products
from schemas.users import Users

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Forbidden
from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import BadRequest

class Product_Model:
    def __init__(self) -> None:
        self.Products = Products
        self.Users_projects = Users_projects
        self.Users = Users

    def add(self, uid: str, product_name: str) -> bool:
        """
        """
        try:
            logger.debug("checking %s's status for %s..." % (uid, product_name))

            try:
                pid = self.Products.get(self.Products.name == product_name)
            except self.Products.DoesNotExist:
                logger.error("INVALID PRODUCT: %s" % product_name)
                raise Forbidden()

            try:
                user = self.Users.get(self.Users.id == uid)
            except self.Users.DoesNotExist:
                logger.error("USER DOESN'T EXIST")
                raise Forbidden()

            try:
                self.Users_projects.get(self.Users_projects.user_id == uid, self.Users_projects.product_id == pid)
            except self.Users_projects.DoesNotExist:
                logger.debug("requesting for %s's subscription for %s ..." % (product_name, uid))

                authId = user.auth_id
                authKey = user.auth_key

                setupId = SETUP["ID"]
                setupKey = SETUP["key"]

                data = {
                    "auth_id": authId,
                    "auth_key": authKey,
                    "id": setupId,
                    "key": setupKey,
                }

                try:
                    HOST = PRODUCTS["%s" % product_name]["host"] 
                    PORT = PRODUCTS["%s" % product_name]["port"] 
                    VERSION = PRODUCTS["%s" % product_name]["version"]
                    URL = "%s:%s/%s/subscribe" % (HOST, PORT, VERSION)

                    response = requests.post(url=URL, json=data)

                    if response.status_code == 401:
                        logger.error("INVALID SETUP CREDENTIALS")
                        raise Unauthorized()

                    elif response.status_code == 200:
                        Users_projects.create(user_id=uid, product_id=pid)
                        logger.info("- SUCCESSFULLY SUBSCRIBED %s FOR %s" % (uid, product_name))
                        return True

                    elif response.status_code == 409:
                        logger.error("USER %s IS ALREADY SUBSCRIBED FOR %s" % (uid, product_name))
                        raise Conflict()
                        
                    elif response.status_code == 400:
                        logger.error("INCOMPLETE DATA. CHECK YOUR REQUEST BODY")
                        raise BadRequest()

                    else:
                        logger.error("%s SERVER FAILED WITH STATUS CODE %s" % (product_name.upper(), response.status_code))
                        raise InternalServerError(response)

                except KeyError as error:
                    logger.error("%s not found in products.ini file" % product_name)
                    raise InternalServerError(error)
                    
                except Exception as error:
                    raise InternalServerError(error)

            logger.error("%s ALREADY SUBSCRIBED FOR %s", (uid, product_name))
            raise Conflict()

        except DatabaseError as err:
            raise InternalServerError(err)

    def delete(self, uid: str, product_name: str) -> bool:
        """
        """
        try:
            logger.debug("checking %s's status for %s..." % (uid, product_name))

            try:
                pid = self.Products.get(self.Products.name == product_name)
            except self.Products.DoesNotExist:
                logger.error("INVALID PROJECT: %s" % product_name)
                raise Forbidden()

            try:
                user = self.Users.get(self.Users.id == uid)
            except self.Users.DoesNotExist:
                logger.error("USER DOESN'T EXIST")
                raise Forbidden()

            try:
                self.Users_projects.get(self.Users_projects.user_id == uid, self.Users_projects.product_id == pid)
            except self.Users_projects.DoesNotExist:
                logger.error("User is not subscribed for %s" % product_name)
                return True

            logger.debug("requesting for %s's unsubscription for %s ..." % (product_name, uid))

            authId = user.auth_id
            authKey = user.auth_key

            setupId = SETUP["ID"]
            setupKey = SETUP["key"]

            data = {
                "auth_id": authId,
                "auth_key": authKey,
                "id": setupId,
                "key": setupKey,
            }

            try:
                HOST = PRODUCTS["%s" % product_name]["host"] 
                PORT = PRODUCTS["%s" % product_name]["port"] 
                VERSION = PRODUCTS["%s" % product_name]["version"]
                URL = "%s:%s/%s/unsubscribe" % (HOST, PORT, VERSION)

                response = requests.delete(url=URL, json=data)

                if response.status_code == 401:
                    logger.error("INVALID SETUP CREDENTIALS")
                    raise Unauthorized()

                elif response.status_code == 200:
                    remove_project = (
                        self.Users_projects
                        .delete()
                        .where(
                            self.Users_projects.user_id == uid,
                            self.Users_projects.product_id == pid
                        )
                    )

                    remove_project.execute()

                    logger.info("- SUCCESSFULLY UNSUBSCRIBED %s FOR %s" % (uid, product_name))
                    return True

                else:
                    logger.error("%s SERVER FAILED WITH STATUS CODE %s" % (product_name.upper(), response.status_code))
                    raise InternalServerError(response)

            except KeyError as error:
                logger.error("%s not found in products.ini file" % product_name)
                raise InternalServerError(error)
                
            except Exception as error:
                raise InternalServerError(error)

        except DatabaseError as err:
            raise InternalServerError(err)

    def metric(self, uid: str, product_name: str) -> dict:
        """
        """
        try:
            logger.debug("checking %s's status for %s..." % (uid, product_name))

            try:
                pid = self.Products.get(self.Products.name == product_name)
            except self.Products.DoesNotExist:
                logger.error("INVALID PRODUCT: %s" % product_name)
                raise Forbidden()

            try:
                user = self.Users.get(self.Users.id == uid)
            except self.Users.DoesNotExist:
                logger.error("USER DOESN'T EXIST")
                raise Forbidden()

            try:
                self.Users_projects.get(self.Users_projects.user_id == uid, self.Users_projects.product_id == pid)
            except self.Users_projects.DoesNotExist:
                logger.error("User is not subscribed for %s" % product_name)
                return []

            logger.debug("requesting for %s's metrics for %s ..." % (product_name, uid))

            authId = user.auth_id
            authKey = user.auth_key

            setupId = SETUP["ID"]
            setupKey = SETUP["key"]

            data = {
                "auth_id": authId,
                "auth_key": authKey,
                "id": setupId,
                "key": setupKey,
            }

            try:
                HOST = PRODUCTS["%s" % product_name]["host"] 
                PORT = PRODUCTS["%s" % product_name]["port"] 
                VERSION = PRODUCTS["%s" % product_name]["version"]
                URL = "%s:%s/%s/metrics" % (HOST, PORT, VERSION)

                response = requests.post(url=URL, json=data)

                if response.status_code == 401:
                    logger.error("INVALID SETUP CREDENTIALS")
                    raise Unauthorized()

                elif response.status_code == 200:
                    logger.info("- SUCCESSFULLY FETCHED '%s' METRICS FOR '%s'" % (uid, product_name))
                    return response.json()
                    
                elif response.status_code == 400:
                    logger.error("INCOMPLETE DATA. CHECK YOUR REQUEST BODY")
                    raise BadRequest()

                else:
                    logger.error("%s SERVER FAILED WITH STATUS CODE %s" % (product_name.upper(), response.status_code))
                    raise InternalServerError(response)

            except KeyError as error:
                logger.error("%s not found in products.ini file" % product_name)
                raise InternalServerError(error)
                
            except Exception as error:
                raise InternalServerError(error)

        except DatabaseError as err:
            raise InternalServerError(err)

