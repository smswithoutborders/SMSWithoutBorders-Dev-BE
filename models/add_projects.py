import logging

from error import Conflict, Forbidden, InternalServerError

import peewee as pw
from schemas import Users_projects, Projects

LOG = logging.getLogger(__name__)


def add_projects(uid, project_name):
    try:
        LOG.debug(f"checking {uid}'s project status for {project_name}...")

        try:
            pid = Projects.get(Projects.name == project_name)
        except Projects.DoesNotExist:
            LOG.error("INVALID PROJECT")
            raise Forbidden()

        add_project = Users_projects.get_or_create(user_id=uid, project_id=pid)

        if add_project[1] == True:
            LOG.info(f"SUCCESSFULLY SUBSCRIBED {uid} FOR {project_name}")
            return True
        else:
            LOG.error(f"{uid} ALREADY SUBSCRIBED FOR {project_name}")
            raise Conflict()

    except (pw.DatabaseError) as err:
        raise InternalServerError(err)
