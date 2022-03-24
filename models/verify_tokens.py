import logging
from error import Conflict, Forbidden, InternalServerError

import peewee as pw
from uuid import uuid1
from datetime import datetime
from schemas import Users

LOG = logging.getLogger(__name__)


def verify_token(auth_id, auth_key):
    try:
        LOG.debug(f"verifying tokens --> AUTH_ID: {auth_id}, AUTH_KEY: {auth_key} ...")
        users = (
            Users.select()
            .where(Users.auth_id == auth_id, Users.auth_key == auth_key)
            .dicts()
        )
        result = []
        for user in users:
            result.append(user)

        # check for duplicates
        if len(result) > 1:
            LOG.error(f"Multiple tokens found")
            raise Conflict()

        # check for no user
        if len(result) < 1:
            LOG.error(f"No token found")
            raise Forbidden()

        LOG.info(f"SUCCESSFULLY VERIFIED TOKENS")
        return str(result[0]["id"])
    except (pw.DatabaseError) as err:
        LOG.error(f"FAILED TO VERIFY TOKENS CHECK LOGS")
        raise InternalServerError(err)
