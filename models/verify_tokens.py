import logging
from error import Conflict, InternalServerError, Unauthorized

import peewee as pw
from schemas import Users

logger = logging.getLogger(__name__)


def verify_token(auth_id, auth_key):
    try:
        logger.debug(
            f"verifying tokens --> AUTH_ID: {auth_id}, AUTH_KEY: {auth_key} ..."
        )
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
            logger.error(f"Multiple tokens found")
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error(f"No token found")
            raise Unauthorized()

        logger.info(f"SUCCESSFULLY VERIFIED TOKENS")
        return str(result[0]["id"])
    except (pw.DatabaseError) as err:
        logger.error(f"FAILED TO VERIFY TOKENS CHECK LOGS")
        raise InternalServerError(err)
