import scrapy
from police_reports_crawler.items import PoliceReportCase
from police_reports_crawler.itemloaders.berlin import ItemTransformer
from police_reports_crawler.page_objects.berlin import PageItemSelector, SELECTOR_FOR_ALL, SELECTOR_FOR_NEXT_PAGE


class BerlinpolizeiSpider(scrapy.Spider):
    name = "berlinpolizei"
    allowed_domains = ["www.berlin.de"]
    start_urls = ["https://www.berlin.de/polizei/polizeimeldungen/?page_at_1_6=1#headline_1_6"]

    def parse(self, response):
        
        cases = response.css(SELECTOR_FOR_ALL)

        for case in cases:
            case_item = ItemTransformer(item=PoliceReportCase(), selector=case)
            processer = PageItemSelector(itemloader=case_item)

            yield processer.to_item()
        
        next_page = response.css(SELECTOR_FOR_NEXT_PAGE).get()
        
        if next_page is not None:
           next_page_url = 'https://www.berlin.de' + next_page
           yield response.follow(next_page_url, callback=self.parse)


class BerlinpolizeiarchivSpider(scrapy.Spider):
    name = "berlinpolizeiarchiv"
    allowed_domains = ["www.berlin.de"]
    start_urls = ["https://www.berlin.de/polizei/polizeimeldungen/archiv/2024/"]

    def parse(self, response):
        pass
