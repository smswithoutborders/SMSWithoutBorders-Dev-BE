import logging
logger = logging.getLogger(__name__)

from config_init import configuration
config = configuration()
api = config["API"]

secure = api["SECURE_SESSIONS"]
hour = eval(api["SESSION_MAXAGE"])

from peewee import DatabaseError

from schemas.sessions import Sessions

from datetime import datetime
from datetime import timedelta

import json

from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import InternalServerError

class Session_Model:
    def __init__(self) -> None:
        self.Sessions = Sessions

    def create(self, unique_identifier: str, user_agent: str) -> dict:
        """
        """
        try:
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

            session = self.Sessions.create(
                unique_identifier=unique_identifier,
                user_agent=user_agent,
                expires=expires,
                data=json.dumps(data)
            )

            logger.info("- SUCCESSFULLY CREATED SESSION %s FOR %s" % (str(session), unique_identifier))

            return {
                "sid": str(session.sid),
                "uid": session.unique_identifier,
                "data": session.data
            }

        except DatabaseError as err:
            logger.error("FAILED TO CREATE SESSION FOR %s CHECK LOGS" % unique_identifier)
            raise InternalServerError(err)

    def find(self, sid: str, unique_identifier: str, user_agent: str, cookie: dict) -> str:
        """
        """
        try:
            logger.debug("finding session %s for user %s ..." % (sid, unique_identifier))

            sessions = (
                self.Sessions.select()
                .where(
                    self.Sessions.sid == sid,
                    self.Sessions.unique_identifier == unique_identifier,
                    self.Sessions.user_agent == user_agent,
                )
                .dicts()
            )

            # check for duplicates
            if len(sessions) > 1:
                logger.error("Multiple sessions %s found" % sid)
                raise Conflict()

            # check for no user
            if len(sessions) < 1:
                logger.error("No session %s found" % sid)
                raise Unauthorized()

            expires = sessions[0]["expires"]
            age = expires.timestamp() - datetime.now().timestamp()

            if age <= 0:
                logger.error("Expired session %s" % sid)
                raise Unauthorized()

            if sessions[0]["data"] != cookie:
                logger.error("Invalid cookie data")
                logger.error('Original cokkie: %s' % sessions[0]["data"])
                logger.error("Invalid cokkie: %s" % cookie)
                raise Unauthorized()

            logger.info("- SESSION %s FOUND" % sid)
            return str(sessions[0]["unique_identifier"])

        except DatabaseError as err:
            logger.error("FAILED FINDING SESSION %s CHECK LOGS" % sid)
            raise InternalServerError(err)

    def update(self, sid: str, unique_identifier: str) -> dict:
        """
        """
        try:
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
                self.Sessions.select()
                .where(self.Sessions.sid == sid, self.Sessions.unique_identifier == unique_identifier)
                .dicts()
            )
        
            # check for duplicates
            if len(sessions) > 1:
                logger.error("Multiple sessions %s found" % sid)
                raise Conflict()

            # check for no user
            if len(sessions) < 1:
                logger.error("No session %s found" % sid)
                raise Unauthorized()

            logger.debug("updating session %s for user %s ..." % (sid, unique_identifier))

            upd_session = (
                self.Sessions.update(
                    expires=expires,
                    data=json.dumps(data)
                )
                .where(
                    self.Sessions.sid == sid
                )
            )

            upd_session.execute()

            logger.info("- SUCCESSFULLY UPDATED SESSION %s" % sid)

            return {
                "sid": sid, 
                "uid": unique_identifier, 
                "data": json.dumps(data)
            }

        except DatabaseError as err:
            logger.error("FAILED UPDATING SESSION %s CHECK LOGS" % sid)
            raise InternalServerError(err)