import logging
logger = logging.getLogger(__name__)

from config_init import configuration
config = configuration()

from peewee import DatabaseError

from models.security import Security

from schemas.users import Users

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized

def verify_user(email: str, password: str) -> dict:
    """
    """
    try:
        logger.debug("verifying user %s ..." % email)
        hash_password = Security.hash(password)
        users = (
            Users.select()
            .where(Users.email == email, Users.password == hash_password)
            .dicts()
        )
        result = []
        for user in users:
            result.append(user)

        # check for duplicates
        if len(result) > 1:
            logger.error("Multiple users %s found" % email)
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error("No user found")
            raise Unauthorized()

        logger.info("- User %s successfully verified" % email)
        return {
            "uid": result[0]["id"],
            "email": result[0]["email"],
            "auth_id": result[0]["auth_id"],
            "auth_key": result[0]["auth_key"],
        }
        
    except DatabaseError as err:
        logger.error("verifying user %s failed check logs" % email)
        raise InternalServerError(err) from None
