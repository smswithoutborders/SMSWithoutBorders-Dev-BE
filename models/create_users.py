import logging
logger = logging.getLogger(__name__)

from models.security import Security

from peewee import DatabaseError

from uuid import uuid1

from schemas.users import Users

from werkzeug.exceptions import Conflict
from werkzeug.exceptions import InternalServerError

def create_user(email: str, password: str) -> str:
    """
    """
    try:
        try:
            Users.get(Users.email == email)
        except Users.DoesNotExist:
            logger.debug("creating user %s ..." % email)

            hash_password = Security.hash(password)
            user = Users.create(id=uuid1(), email=email, password=hash_password)

            logger.info("- User %s successfully created" % email)
            return str(user)
        else:
            logger.error("user '%s' already has a record" % email)
            raise Conflict()

    except DatabaseError as err:
        logger.error("creating user %s failed check logs" % email)
        raise InternalServerError(err) from None
