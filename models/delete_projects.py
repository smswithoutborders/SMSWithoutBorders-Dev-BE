import logging

from error import Conflict, Forbidden, InternalServerError

import peewee as pw
from schemas import Users_projects, Projects

LOG = logging.getLogger(__name__)


def delete_projects(uid, project_name):
    try:
        LOG.debug(f"checking {uid}'s project status for {project_name}...")

        try:
            pid = Projects.get(Projects.name == project_name)
        except Projects.DoesNotExist:
            LOG.error("INVALID PROJECT")
            raise Forbidden()

        try:
            project = Users_projects.get(
                Users_projects.user_id == uid, Users_projects.project_id == pid
            )
        except Users_projects.DoesNotExist:
            LOG.error(f"User is not subscribed for {project_name}")
            return True

        remove_project = project.delete().where(
            Users_projects.user_id == uid, Users_projects.project_id == pid
        )
        remove_project.execute()

        LOG.info(f"SUCCESSFULLY UNSUBSCRIBED {uid} FOR {project_name}")
    except (pw.DatabaseError) as err:
        raise InternalServerError(err)
