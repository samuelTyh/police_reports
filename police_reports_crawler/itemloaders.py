from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class BerlinPoliceReportLoader(ItemLoader):

    default_output_processor = TakeFirst()
    created_at_in = MapCompose(lambda x: x.split(" Uhr")[0])
    url_in = MapCompose(lambda x: 'https://www.berlin.de' + x )
