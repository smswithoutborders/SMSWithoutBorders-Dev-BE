import logging
logger = logging.getLogger(__name__)

from config_init import configuration
config = configuration()

from peewee import DatabaseError

from datetime import datetime

from schemas.sessions import Sessions

from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import InternalServerError

def find_session(sid: str, unique_identifier: str, user_agent: str, cookie: dict) -> str:
    """
    """
    try:
        logger.debug("finding session %s for user %s ..." % (sid, unique_identifier))
        sessions = (
            Sessions.select()
            .where(
                Sessions.sid == sid,
                Sessions.unique_identifier == unique_identifier,
                Sessions.user_agent == user_agent,
            )
            .dicts()
        )
        result = []
        for session in sessions:
            result.append(session)

        # check for duplicates
        if len(result) > 1:
            logger.error("Multiple sessions %s found" % sid)
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error("No session %s found" % sid)
            raise Unauthorized()

        expires = result[0]["expires"]
        age = expires.timestamp() - datetime.now().timestamp()

        if age <= 0:
            logger.error("Expired session %s" % sid)
            raise Unauthorized()

        str_cookie = str(cookie)
        str_cookie = str_cookie.replace(": 'False'", ": False")
        str_cookie = str_cookie.replace(": 'True'", ": True")

        if result[0]["data"] != str_cookie:
            logger.error("Invalid cookie data")
            logger.error('Original cokkie: %s' % result[0]["data"])
            logger.error("Invalid cokkie: %s" % str_cookie)
            raise Unauthorized()

        logger.info("- SESSION %s FOUND" % sid)
        return str(result[0]["unique_identifier"])

    except DatabaseError as err:
        logger.error("FAILED FINDING SESSION %s CHECK LOGS" % sid)
        raise InternalServerError(err) from None
