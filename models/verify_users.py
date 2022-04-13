import logging
from error import Conflict, InternalServerError, Unauthorized
from models.security import Security

import peewee as pw
from schemas import Users

logger = logging.getLogger(__name__)


def verify_user(email, password):
    try:
        logger.debug(f"verifying user {email} ...")
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
            logger.error(f"Multiple users {email} found")
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error(f"No user found")
            raise Unauthorized()

        logger.info(f"User {email} successfully verified")
        return {
            "uid": result[0]["id"],
            "email": result[0]["email"],
            "auth_id": result[0]["auth_id"],
            "auth_key": result[0]["auth_key"],
        }
    except (pw.DatabaseError) as err:
        logger.error(f"verifying user {email} failed check logs")
        raise InternalServerError(err)
