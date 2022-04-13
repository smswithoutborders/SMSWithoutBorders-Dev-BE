import logging
from error import InternalServerError
from config_init import configuration

config = configuration()

api = config["API"]

import peewee as pw
from uuid import uuid4
from datetime import datetime, timedelta
from schemas import Sessions

logger = logging.getLogger(__name__)


def create_session(unique_identifier, user_agent):
    try:
        secure = api["SECURE_SESSIONS"]
        hour = eval(api["SESSION_MAXAGE"])
        expires = datetime.now() + timedelta(milliseconds=hour)

        data = {
            "maxAge": hour,
            "secure": eval(secure),
            "httpOnly": True,
            "sameSite": "lax",
        }

        logger.debug(f"Secure session: {secure}")
        logger.debug(f"Session maxAge: {hour}")

        logger.debug(f"creating session for {unique_identifier} ...")
        session = Sessions.create(
            sid=uuid4(),
            unique_identifier=unique_identifier,
            user_agent=user_agent,
            expires=expires,
            data=str(data),
            createdAt=datetime.now(),
        )
        logger.info(
            f"SUCCESSFULLY CREATED SESSION {str(session)} FOR {unique_identifier}"
        )
        return {"sid": str(session), "uid": unique_identifier, "data": data}
    except (pw.DatabaseError) as err:
        logger.error(f"FAILED TO CREATE SESSION FOR {unique_identifier} CHECK LOGS")
        raise InternalServerError(err)
