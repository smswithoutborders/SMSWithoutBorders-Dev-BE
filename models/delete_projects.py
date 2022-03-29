import logging

from error import Conflict, Unauthorized, Forbidden, InternalServerError

import peewee as pw
from schemas import Users_projects, Products, Users
from products import openapi
import requests

from configparser import ConfigParser

LOG = logging.getLogger(__name__)


def delete_projects(uid, project_name):
    try:
        LOG.debug(f"checking {uid}'s project status for {project_name}...")

        try:
            pid = Products.get(Products.name == project_name)
        except Products.DoesNotExist:
            LOG.error("INVALID PROJECT")
            raise Forbidden()

        try:
            user = Users.get(Users.id == uid)
        except Users.DoesNotExist:
            LOG.error("USER DOESN'T EXIST")
            raise Forbidden()

        try:
            project = Users_projects.get(
                Users_projects.user_id == uid, Users_projects.product_id == pid
            )
        except Users_projects.DoesNotExist:
            LOG.error(f"User is not subscribed for {project_name}")
            return True

        LOG.debug(f"requesting for {project_name}'s unsubscription for {uid} ...")

        AUTH_ID = user.auth_id
        AUTH_KEY = user.auth_key

        setup = ConfigParser()
        setup.read("setup.ini")
        SETUP = setup["CREDENTIALS"]
        SETUP_ID = SETUP["ID"]
        SETUP_KEY = SETUP["key"]

        data = {
            "auth_id": AUTH_ID,
            "auth_key": AUTH_KEY,
            "id": SETUP_ID,
            "key": SETUP_KEY,
        }

        if project_name == "openapi":
            HOST = openapi.HOST
            PORT = openapi.PORT
            VERSION = openapi.VERSION
            URL = f"{HOST}:{PORT}/{VERSION}/unsubscribe"

            response = requests.delete(url=URL, json=data)
            if response.status_code == 401:
                LOG.error("INVALID SETUP CREDENTIALS")
                raise Unauthorized()
            elif response.status_code == 200:
                remove_project = project.delete().where(
                    Users_projects.user_id == uid, Users_projects.product_id == pid
                )
                remove_project.execute()

                LOG.info(f"SUCCESSFULLY UNSUBSCRIBED {uid} FOR {project_name}")
                return True
            else:
                LOG.error(
                    f"OPENAPI SERVER FAILED WITH STATUS CODE {response.status_code}"
                )
                raise InternalServerError(response.text)
        else:
            LOG.error("INVALID PRODUCT")
            raise Forbidden()
    except (pw.DatabaseError) as err:
        raise InternalServerError(err)
