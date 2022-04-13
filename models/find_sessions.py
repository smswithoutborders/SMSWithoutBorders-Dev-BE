import logging
from error import Conflict, InternalServerError, Unauthorized

import peewee as pw
from datetime import datetime
from schemas import Sessions

logger = logging.getLogger(__name__)


def find_session(sid, unique_identifier, user_agent, cookie):
    try:
        logger.debug(f"finding session {sid} for user {unique_identifier} ...")
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
            logger.error(f"Multiple sessions {sid} found")
            raise Conflict()

        # check for no user
        if len(result) < 1:
            logger.error(f"No session {sid} found")
            raise Unauthorized()

        expires = result[0]["expires"]
        age = expires.timestamp() - datetime.now().timestamp()

        if age <= 0:
            logger.error(f"Expired session {sid}")
            raise Unauthorized()

        str_cookie = str(cookie)
        str_cookie = str_cookie.replace(": 'False'", ": False")
        str_cookie = str_cookie.replace(": 'True'", ": True")

        if result[0]["data"] != str_cookie:
            logger.error(f"Invalid cookie data")
            logger.error(f'Original cokkie: {result[0]["data"]}')
            logger.error(f"Invalid cokkie: {str_cookie}")
            raise Unauthorized()

        logger.info(f"SESSION {sid} FOUND")
        return str(result[0]["unique_identifier"])
    except (pw.DatabaseError) as err:
        logger.error(f"FAILED FINDING SESSION {sid} CHECK LOGS")
        raise InternalServerError(err)
