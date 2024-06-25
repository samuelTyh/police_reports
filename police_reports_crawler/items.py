# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PoliceReportCase(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    filed_at = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    case_number = scrapy.Field()
    text_content = scrapy.Field()
    additional_text_content = scrapy.Field()

    metadata = scrapy.Field()
