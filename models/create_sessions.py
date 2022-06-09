import logging
logger = logging.getLogger(__name__)

from config_init import configuration
config = configuration()
api = config["API"]

from peewee import DatabaseError

from schemas.sessions import Sessions

from uuid import uuid4

from datetime import datetime
from datetime import timedelta

from werkzeug.exceptions import InternalServerError

def create_session(unique_identifier: str, user_agent: str) -> dict:
    """
    """
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

        logger.debug("Secure session: %s" % secure)
        logger.debug("Session maxAge: %s" % hour)

        logger.debug("creating session for %s ..." % unique_identifier)
        session = Sessions.create(
            sid=uuid4(),
            unique_identifier=unique_identifier,
            user_agent=user_agent,
            expires=expires,
            data=str(data),
        )

        logger.info("SUCCESSFULLY CREATED SESSION %s FOR %s" % (str(session), unique_identifier))
        return {"sid": str(session), "uid": unique_identifier, "data": data}

    except DatabaseError as err:
        logger.error("FAILED TO CREATE SESSION FOR %s CHECK LOGS" % unique_identifier)
        raise InternalServerError(err)
