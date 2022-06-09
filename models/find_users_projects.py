import logging
logger = logging.getLogger(__name__)

from config_init import configuration
config = configuration()

from peewee import DatabaseError

from schemas.baseModel import db
from schemas.users_projects import Users_projects
from schemas.projects import Products
from schemas.users import Users

from werkzeug.exceptions import InternalServerError

def find_users_projects(uid: str) -> dict:
    """
    """
    try:
        unsubscribed = []
        subscribed = []

        logger.debug("fetching unsubscribed projects for %s..." % uid)
        unsub_cursor = db.execute_sql('SELECT t1.id, t1.name, t1.label, t1.description, t1.documentation FROM products t1 LEFT JOIN (SELECT * FROM users_projects WHERE users_projects.user_id = "%s") AS t2 ON t2.product_id = t1.id WHERE t2.product_id IS NULL' % uid)

        for row in unsub_cursor.fetchall():
            unsub_project = {
                "id": row[0],
                "name": row[1],
                "label": row[2],
                "description": row[3],
                "documentation": row[4],
            }
            unsubscribed.append(unsub_project)

        logger.debug("fetching subscribed products for %s..." % uid)
        sub_cursor = (Products.select().join(Users_projects).join(Users).where(Users.id == uid))

        for row in sub_cursor:
            sub_project = {
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "label": row.label,
                "documentation": row.documentation,
            }
            subscribed.append(sub_project)

        logger.info("- SUCCESSFULLY GATHERED %s PRODUCTS" % uid)
        return {"unsubscribed": unsubscribed, "subscribed": subscribed}

    except DatabaseError as err:
        raise InternalServerError(err) from None
