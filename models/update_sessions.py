import logging
from error import Conflict, InternalServerError, Unauthorized

import peewee as pw
from datetime import datetime, timedelta
from schemas import Sessions
from config_init import configuration

config = configuration()

api = config["API"]

logger = logging.getLogger(__name__)


def update_session(sid, unique_identifier):
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

        logger.debug(f"finding session {sid} for user {unique_identifier} ...")
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
            logger.error(f"Multiple sessions {sid} found")
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error(f"No session {sid} found")
            raise Unauthorized()

        logger.debug(f"updating session {sid} for user {unique_identifier} ...")
        upd_session = Sessions.update(expires=expires, data=str(data)).where(
            Sessions.sid == sid
        )
        upd_session.execute()

        logger.info(f"SUCCESSFULLY UPDATED SESSION {sid}")
        return {"sid": sid, "uid": unique_identifier, "data": data}
    except (pw.DatabaseError) as err:
        logger.error(f"FAILED UPDATING SESSION {sid} CHECK LOGS")
        raise InternalServerError(err)
