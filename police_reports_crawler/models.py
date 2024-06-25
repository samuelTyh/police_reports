import datetime

from peewee import *
from playhouse.postgres_ext import JSONField

from police_reports_crawler.utils.utils import CustomDatabaseProxy


class BaseModel(Model):
    class Meta:
        database = CustomDatabaseProxy()


class CasesItemModel(BaseModel):

    filed_at = DateTimeField(null=False)
    url = TextField(null=False)
    title = TextField(null=True)
    location = TextField(null=True, default='bezirksübergreifend')
    case_number = TextField(null=True)
    text_content = TextField(null=True)
    additional_text_content = TextField(null=True)

    metadata = JSONField(null=True)

    class Meta:
        db_table = "police_reports"
        primary_key = CompositeKey('filed_at', 'url')


def connect_to_db(db_uri):
    db_handle = CustomDatabaseProxy(db_uri=db_uri)
    db_handle.create_tables([CasesItemModel])  # table creation example
    return db_handle
