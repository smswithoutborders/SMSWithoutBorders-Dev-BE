import logging

from error import InternalServerError

import peewee as pw
from schemas import Users_projects, Products, Users
from schemas.baseModel import db

logger = logging.getLogger(__name__)


def find_users_projects(uid):
    try:
        unsubscribed = []
        subscribed = []

        logger.debug(f"fetching unsubscribed projects for {uid}...")
        unsub_cursor = db.execute_sql(
            f'SELECT t1.id, t1.name, t1.label, t1.description, t1.documentation FROM products t1 LEFT JOIN (SELECT * FROM users_projects WHERE users_projects.user_id = "{uid}") AS t2 ON t2.product_id = t1.id WHERE t2.product_id IS NULL'
        )

        for row in unsub_cursor.fetchall():
            unsub_project = {
                "id": row[0],
                "name": row[1],
                "label": row[2],
                "description": row[3],
                "documentation": row[4],
            }
            unsubscribed.append(unsub_project)

        logger.debug(f"fetching subscribed products for {uid}...")
        sub_cursor = (
            Products.select().join(Users_projects).join(Users).where(Users.id == uid)
        )

        for row in sub_cursor:
            sub_project = {
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "label": row.label,
                "documentation": row.documentation,
            }
            subscribed.append(sub_project)

        logger.info(f"SUCCESSFULLY GATHERED {uid} PRODUCTS")
        return {"unsubscribed": unsubscribed, "subscribed": subscribed}

    except (pw.DatabaseError) as err:
        raise InternalServerError(err)
