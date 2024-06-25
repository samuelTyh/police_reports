from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class ItemTransformer(ItemLoader):

    default_output_processor = TakeFirst()
    filed_at_in = MapCompose(lambda x: x.split(" Uhr")[0])
    url_in = MapCompose(lambda x: 'https://www.berlin.de' + x )
