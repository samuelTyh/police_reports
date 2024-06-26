from urllib.parse import urlparse, urlunparse, urlencode
from dotenv import load_dotenv
import os

from peewee import DatabaseProxy
from playhouse.db_url import connect
from playhouse.postgres_ext import PostgresqlExtDatabase


load_dotenv()


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        if (
            not isinstance(cls._instance.obj, PostgresqlExtDatabase)
            and "db_uri" in kwargs
        ):
            db_uri = kwargs["db_uri"]
            parsed = urlparse(db_uri)
            if parsed.scheme == "postgres":
                parsed = parsed._replace(scheme="postgresext")
            db_uri = urlunparse(parsed)
            conn = connect(db_uri, unquote_password=True)
            cls._instance.initialize(conn)
        return cls._instance


class CustomDatabaseProxy(DatabaseProxy, metaclass=SingletonMeta):
    def __init__(self, db_uri=None):
        super().__init__()


def get_proxy_url(url):
    api_key = os.getenv("SCRAPEOPS_API_KEY")
    payload = {'api_key': api_key, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url
