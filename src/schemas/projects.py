import os
import logging
import json
from datetime import datetime

from peewee import Model, CharField, DateTimeField

from src.schemas.db_connector import db

from settings import Configurations
product_info_filepath = Configurations.PROJECTS_INFO_PATH

logger = logging.getLogger(__name__)

from werkzeug.exceptions import InternalServerError

class Products(Model):
    name = CharField(null=True)
    description = CharField(null=True)
    label = CharField(null=True)
    documentation = CharField(null=True)
    createdAt = DateTimeField(null=True, default=datetime.now)

    class Meta:
        database = db

if db.table_exists('products') is False:
    db.create_tables([Products])

try:
    if not os.path.exists(product_info_filepath):
        error = "Products information file not found at %s" % product_info_filepath
        raise InternalServerError(error)

    with open(product_info_filepath, encoding="utf-8") as data_file:
        data = json.load(data_file)

    for product in data:
        try:
            Products.get(Products.name == product["name"])
        except Products.DoesNotExist:
            logger.debug("Adding product %s ..." % product['name'])
            Products.create(
                name=product["name"],
                label=product["label"],
                description=product["description"],
                documentation=product["documentation"],
            )
        else:
            logger.debug("Updating product %s ..." % product['name'])
            
            update_product = Products.update(
                name=product["name"],
                label=product["label"],
                description=product["description"],
                documentation=product["documentation"],
            ).where(
                Products.name == product["name"]
            )

            update_product.execute()
                
except Exception as error:
    raise InternalServerError(error)

