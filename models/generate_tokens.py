import logging
from error import InternalServerError

import peewee as pw
from uuid import uuid4
from schemas import Users

logger = logging.getLogger(__name__)


def generate_token(uid):
    try:
        logger.debug(f"generating tokens for {uid} ...")
        auth_key = uuid4().hex
        auth_id = uuid4().hex
        user = Users.update(auth_key=auth_key, auth_id=auth_id).where(Users.id == uid)
        user.execute()
        logger.info(f"SUCCESSFULLY GENERATED TOKENS FOR {uid}")
        return {"auth_key": auth_key, "auth_id": auth_id}
    except (pw.DatabaseError) as err:
        logger.error(f"GENERATING TOKENS FOR {uid} FAILED CHECK LOGS")
        raise InternalServerError(err)
