import logging
logger = logging.getLogger(__name__)

from config_init import configuration
config = configuration()

from peewee import DatabaseError

from schemas.users import Users

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized

def verify_token(auth_id: str, auth_key: str) -> str:
    """
    """
    try:
        logger.debug("verifying tokens --> AUTH_ID: %s, AUTH_KEY: %s ..." % (auth_id, auth_key))

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
            logger.error("Multiple tokens found")
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error("No token found")
            raise Unauthorized()

        logger.info("- SUCCESSFULLY VERIFIED TOKENS")
        return str(result[0]["id"])

    except DatabaseError as err:
        logger.error("FAILED TO VERIFY TOKENS CHECK LOGS")
        raise InternalServerError(err) from None
