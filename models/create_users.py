import logging
from error import Conflict, InternalServerError
from models.security import Security

import peewee as pw
from uuid import uuid1
from datetime import datetime
from schemas import Users

logger = logging.getLogger(__name__)


def create_user(email, password):
    try:
        logger.debug(f"creating user {email} ...")
        hash_password = Security.hash(password)
        user = Users.create(
            id=uuid1(), email=email, password=hash_password, createdAt=datetime.now()
        )
        logger.info(f"User {email} successfully created")
        return str(user)
    except pw.IntegrityError as err:
        logger.error(f"user {email} already has a record")
        raise Conflict()
    except (pw.DatabaseError) as err:
        logger.error(f"creating user {email} failed check logs")
        raise InternalServerError(err)
