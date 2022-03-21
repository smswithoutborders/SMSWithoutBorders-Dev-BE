import logging
from unittest import result
from error import Conflict, InternalServerError, Unauthorized
from models.security import Security

import peewee as pw
from uuid import uuid1
from datetime import datetime
from schemas import Sessions

LOG = logging.getLogger(__name__)

def find_session(sid, unique_identifier, user_agent, cookie):
    try:
        LOG.debug(f'finding session {sid} for user {unique_identifier} ...')
        sessions = Sessions.select().where(Sessions.sid == sid, Sessions.unique_identifier == unique_identifier, Sessions.user_agent == user_agent).dicts()
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

        expires = result[0]['expires']
        age = expires.timestamp() - datetime.now().timestamp()

        if age <= 0:
            LOG.error(f'Expired session {sid}')
            raise Unauthorized()
       
        str_cookie = str(cookie)
        str_cookie = str_cookie.replace(": 'False'", ": False")
        str_cookie = str_cookie.replace(": 'True'", ": True")

        if result[0]['data'] != str_cookie:
            LOG.error(f'Invalid cookie data')
            LOG.error(f'Original cokkie: {result[0]["data"]}')
            LOG.error(f'Invalid cokkie: {str_cookie}')
            raise Unauthorized()

        LOG.info(f'SESSION {sid} FOUND')
        return str(result[0]['unique_identifier'])
    except (pw.DatabaseError) as err:
        LOG.error(f'FAILED FINDING SESSION {sid} CHECK LOGS')
        raise InternalServerError(err)

    