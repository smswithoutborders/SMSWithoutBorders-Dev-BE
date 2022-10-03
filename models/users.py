import logging
logger = logging.getLogger(__name__)

from security.data import Data

from peewee import DatabaseError

from uuid import uuid4

from schemas.baseModel import db
from schemas.users import Users
from schemas.users_projects import Users_projects
from schemas.projects import Products

from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import Forbidden
from werkzeug.exceptions import InternalServerError

class User_Model:
    def __init__(self) -> None:
        self.db = db
        self.Users = Users
        self.Users_projects = Users_projects
        self.Products = Products
        self.Data = Data

    def create(self, email: str, password: str) -> str:
        """
        """
        try:
            data = self.Data()
            
            try:
                self.Users.get(self.Users.email == email)
            except self.Users.DoesNotExist:
                logger.debug("creating user %s ..." % email)

                hash_password = data.hash(data=password)

                user = self.Users.create(
                    email=email,
                    password=hash_password
                )

                logger.info("- User %s successfully created" % email)
                return str(user)

            else:
                logger.error("user '%s' already has a record" % email)
                raise Conflict()

        except DatabaseError as err:
            logger.error("creating user %s failed check logs" % email)
            raise InternalServerError(err)

    def verify(self, email: str, password: str) -> dict:
        """
        """
        try:
            data = self.Data()

            logger.debug("verifying user %s ..." % email)

            hash_password = data.hash(data=password)

            users = (
                self.Users.select()
                .where(
                    self.Users.email == email,
                    self.Users.password == hash_password
                )
                .dicts()
            )

            # check for duplicates
            if len(users) > 1:
                logger.error("Multiple users %s found" % email)
                raise Conflict()

            # check for no user
            if len(users) < 1:
                logger.error("No user found")
                raise Unauthorized()

            logger.info("- User %s successfully verified" % email)

            return {
                "uid": users[0]["id"],
                "email": users[0]["email"],
                "auth_id": users[0]["auth_id"],
                "auth_key": users[0]["auth_key"],
            }
            
        except DatabaseError as err:
            logger.error("verifying user %s failed check logs" % email)
            raise InternalServerError(err)

    def verify_token(self, auth_id: str, auth_key: str) -> str:
        """
        """
        try:
            logger.debug("verifying tokens --> AUTH_ID: %s, AUTH_KEY: %s ..." % (auth_id, auth_key))

            users = (
                self.Users.select()
                .where(
                    self.Users.auth_id == auth_id,
                    self.Users.auth_key == auth_key
                )
                .dicts()
            )

            # check for duplicates
            if len(users) > 1:
                logger.error("Multiple tokens found")
                raise Conflict()

            # check for no user
            if len(users) < 1:
                logger.error("No token found")
                raise Unauthorized()

            logger.info("- SUCCESSFULLY VERIFIED TOKENS")
            return str(users[0]["id"])

        except DatabaseError as err:
            logger.error("FAILED TO VERIFY TOKENS CHECK LOGS")
            raise InternalServerError(err)

    def generate_token(self, uid: str) -> dict:
        """
        """
        try:
            logger.debug("generating tokens for %s ..." % uid)

            auth_key = uuid4().hex
            auth_id = uuid4().hex

            try:
                user = self.Users.get(self.Users.id == uid)
                old_auth_id = user.auth_id
                old_auth_key = user.auth_key
            except self.Users.DoesNotExist:
                logger.error("USER DOESN'T EXIST")
                raise Forbidden()
            
            user_upt = (
                self.Users.update(auth_key=auth_key, auth_id=auth_id)
                .where(self.Users.id == uid)
            )

            user_upt.execute()

            logger.info("- SUCCESSFULLY GENERATED TOKENS FOR %s" % uid)

            return {
                "auth_key": auth_key, 
                "auth_id": auth_id,
                "old_auth_id": old_auth_id,
                "old_auth_key": old_auth_key
            }

        except DatabaseError as err:
            logger.error("GENERATING TOKENS FOR %s FAILED CHECK LOGS" % uid)
            raise InternalServerError(err)

    def find_projects(self, uid: str) -> dict:
        """
        """
        try:
            unsubscribed = []
            subscribed = []

            logger.debug("fetching unsubscribed projects for %s ..." % uid)

            query = f"""SELECT t1.id, t1.name, t1.label, t1.description, t1.documentation 
            FROM products t1 
            LEFT JOIN (
                SELECT * FROM users_projects 
                WHERE users_projects.user_id = "{uid}"
                ) AS t2 ON t2.product_id = t1.id 
            WHERE t2.product_id IS NULL"""

            cursor = self.db.execute_sql(query)

            col_names = [col[0] for col in cursor.description]
            unsub_products = [dict(zip(col_names, row)) for row in cursor.fetchall()]

            for row in unsub_products:
                unsubscribed.append({
                    "id": row["id"],
                    "name": row["name"],
                    "label": row["label"],
                    "description": row["description"],
                    "documentation": row["documentation"],
                })

            logger.debug("fetching subscribed products for %s..." % uid)

            sub_cursor = (
                self.Products.select()
                .join(self.Users_projects)
                .join(self.Users)
                .where(self.Users.id == uid)
            )

            for row in sub_cursor:
                subscribed.append({
                    "id": row.id,
                    "name": row.name,
                    "description": row.description,
                    "label": row.label,
                    "documentation": row.documentation,
                })

            logger.info("- SUCCESSFULLY GATHERED %s PRODUCTS" % uid)
            return {"unsubscribed": unsubscribed, "subscribed": subscribed}

        except DatabaseError as err:
            raise InternalServerError(err)


