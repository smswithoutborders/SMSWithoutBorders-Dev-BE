import logging
logger = logging.getLogger(__name__)

from config_init import configuration
config = configuration()
api = config["API"]

from peewee import DatabaseError

from datetime import datetime
from datetime import timedelta

from schemas.sessions import Sessions

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized

def update_session(sid: str, unique_identifier: str) -> dict:
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

        logger.debug("finding session %s for user %s ..." % (sid, unique_identifier))
        sessions = (
            Sessions.select()
            .where(Sessions.sid == sid, Sessions.unique_identifier == unique_identifier)
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

        logger.debug("updating session %s for user %s ..." % (sid, unique_identifier))
        upd_session = Sessions.update(expires=expires, data=str(data)).where(
            Sessions.sid == sid
        )
        upd_session.execute()

        logger.info("- SUCCESSFULLY UPDATED SESSION %s" % sid)
        return {"sid": sid, "uid": unique_identifier, "data": data}

    except DatabaseError as err:
        logger.error("FAILED UPDATING SESSION %s CHECK LOGS" % sid)
        raise InternalServerError(err) from None
