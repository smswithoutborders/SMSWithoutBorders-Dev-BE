import logging
logger = logging.getLogger(__name__)

from config_init import configuration
config = configuration()

from peewee import DatabaseError

from uuid import uuid4

from schemas.users import Users

from werkzeug.exceptions import InternalServerError

def generate_token(uid: str) -> dict:
    """
    """
    try:
        logger.debug("generating tokens for %s ..." % uid)

        auth_key = uuid4().hex
        auth_id = uuid4().hex
        
        user = Users.update(auth_key=auth_key, auth_id=auth_id).where(Users.id == uid)
        user.execute()

        logger.info("- SUCCESSFULLY GENERATED TOKENS FOR %s" % uid)

        return {"auth_key": auth_key, "auth_id": auth_id}

    except DatabaseError as err:
        logger.error("GENERATING TOKENS FOR %s FAILED CHECK LOGS" % uid)
        raise InternalServerError(err) from None
