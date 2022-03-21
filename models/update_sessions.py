import logging
from error import Conflict, InternalServerError, Unauthorized

import peewee as pw
from datetime import datetime, timedelta
from schemas import Sessions
from configparser import ConfigParser

config = ConfigParser()
config.read('.config/default.ini')

api = config['API']

LOG = logging.getLogger(__name__)

def update_session(sid, unique_identifier):
    try:
        secure = api['SECURE_SESSIONS']
        hour = eval(api['SESSION_MAXAGE'])
        expires = datetime.now()+timedelta(milliseconds=hour)

        data = {
            "maxAge": hour,
            "secure": eval(secure),
            "httpOnly": True,
            "sameSite": "lax"
        }

        LOG.debug(f"Secure session: {secure}")
        LOG.debug(f"Session maxAge: {hour}")

        LOG.debug(f'finding session {sid} for user {unique_identifier} ...')
        sessions = Sessions.select().where(Sessions.sid == sid, Sessions.unique_identifier == unique_identifier).dicts()
        result = []
        for session in sessions:
            result.append(session)
        
        # check for duplicates
        if len(result) > 1:
            LOG.error(f'Multiple sessions {sid} found')
            raise Conflict()

        # check for no user
        if len(result) < 1:
            LOG.error(f'No session {sid} found')
            raise Unauthorized()

        LOG.debug(f'updating session {sid} for user {unique_identifier} ...')
        upd_session = Sessions.update(expires=expires, data=str(data)).where(Sessions.sid == sid)
        upd_session.execute()

        LOG.info(f'SUCCESSFULLY UPDATED SESSION {sid}')
        return {
            "sid": sid,
            "uid": unique_identifier,
            "data": data
        }
    except (pw.DatabaseError) as err:
        LOG.error(f'FAILED UPDATING SESSION {sid} CHECK LOGS')
        raise InternalServerError(err)

    