import logging

from error import InternalServerError

import peewee as pw
from schemas import Users_projects, Projects, Users
from schemas.baseModel import db

LOG = logging.getLogger(__name__)


def find_users_projects(uid):
    try:
        unsubscribed = []
        subscribed = []

        LOG.debug(f"fetching unsubscribed projects for {uid}...")
        unsub_cursor = db.execute_sql(
            f'SELECT t1.id, t1.name FROM projects t1 LEFT JOIN (SELECT * FROM users_projects WHERE users_projects.user_id = "{uid}") AS t2 ON t2.project_id = t1.id WHERE t2.project_id IS NULL'
        )

        for row in unsub_cursor.fetchall():
            unsub_project = {"id": row[0], "name": row[1]}
            unsubscribed.append(unsub_project)

        LOG.debug(f"fetching subscribed projects for {uid}...")
        sub_cursor = (
            Projects.select().join(Users_projects).join(Users).where(Users.id == uid)
        )

        for row in sub_cursor:
            sub_project = {"id": row.id, "name": row.name}
            subscribed.append(sub_project)

        LOG.info(f"SUCCESSFULLY GATHERED {uid} PROJECTS")
        return {"unsubscribed": unsubscribed, "subscribed": subscribed}

    except (pw.DatabaseError) as err:
        raise InternalServerError(err)
