import logging

from error import Conflict, Forbidden, InternalServerError, Unauthorized

import peewee as pw
import requests
from schemas import Users_projects, Projects, Users
from products import openapi

from configparser import ConfigParser

LOG = logging.getLogger(__name__)


def add_projects(uid, project_name):
    try:
        LOG.debug(f"checking {uid}'s project status for {project_name}...")

        try:
            pid = Projects.get(Projects.name == project_name)
        except Projects.DoesNotExist:
            LOG.error("INVALID PRODUCT")
            raise Forbidden()

        try:
            user = Users.get(Users.id == uid)
        except Users.DoesNotExist:
            LOG.error("USER DOESN'T EXIST")
            raise Forbidden()

        try:
            Users_projects.get(
                Users_projects.user_id == uid, Users_projects.project_id == pid
            )
        except Users_projects.DoesNotExist:
            LOG.debug(f"requesting for {project_name}'s subscription for {uid} ...")

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
                URL = f"{HOST}:{PORT}/{VERSION}/subscribe"

                response = requests.post(url=URL, json=data)
                if response.status_code == 401:
                    LOG.error("INVALID SETUP CREDENTIALS")
                    raise Unauthorized()
                elif response.status_code == 200:
                    pass
            else:
                LOG.error("INVALID PRODUCT")
                raise Forbidden()

            Users_projects.create(user_id=uid, project_id=pid)
            LOG.info(f"SUCCESSFULLY SUBSCRIBED {uid} FOR {project_name}")
            return True

        LOG.error(f"{uid} ALREADY SUBSCRIBED FOR {project_name}")
        raise Conflict()

    except (pw.DatabaseError) as err:
        raise InternalServerError(err)
