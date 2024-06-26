import copy
import logging

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from police_reports_crawler.models import connect_to_db


class BaseDBPipeline:
    max_items = 10000
    items = []
    total = 0

    def __init__(self, db_uri):
        self.db_handle = connect_to_db(db_uri)

    @classmethod
    def from_settings(cls, settings):
        db_uri = settings.get("DATABASE_URI")
        params = {
            "db_uri": db_uri,
        }
        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        item_for_db = self.prepare_item(
            copy.deepcopy(item)
        )
        item_for_db.pop("parent_url", None)

        self.total += 1
        self.items.append(ItemAdapter(item_for_db).asdict())

        if self.total > self.max_items:
            self.flush_data()
        return item

    def close_spider(self, spider):
        self.flush_data()

    def flush_data(self):
        with self.db_handle.atomic() as transaction:
            try:
                self.insert_to_db(self.items)
            except Exception as e:
                logging.error(f"Error in PostgreSQLItemPipeline: {e}")
            transaction.commit()

        self.items = []
        self.total = 0
        return None

    def insert_to_db(self, items):
        pass

    def prepare_item(self, item):
        return item



class DuplicatesPipeline:

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['url'] in self.urls_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.urls_seen.add(adapter['url'])
            return item
