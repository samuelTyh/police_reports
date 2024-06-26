import datetime
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


def text_to_datetime(date_string):
    timestamp = datetime.datetime.strptime(date_string, "%d.%m.%Y %H:%M")
    return timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

def remove_uhr(date_string):
    return date_string.split(" Uhr")[0]


class ItemTransformer(ItemLoader):

    default_output_processor = TakeFirst()

    filed_at_in = MapCompose(remove_uhr, text_to_datetime)
    url_in = MapCompose(lambda x: 'https://www.berlin.de' + x )
