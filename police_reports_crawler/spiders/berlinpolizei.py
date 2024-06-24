import datetime
import scrapy
from police_reports_crawler.items import PoliceReportCase
from police_reports_crawler.itemloaders import BerlinPoliceReportLoader


class BerlinpolizeiSpider(scrapy.Spider):
    name = "berlinpolizei"
    allowed_domains = ["www.berlin.de"]
    start_urls = ["https://www.berlin.de/polizei/polizeimeldungen/?page_at_1_6=1#headline_1_6"]

    def parse(self, response):
        
        cases = response.css('#layout-grid__area--maincontent > section.modul-autoteaser > ul > li')

        for case in cases:
            case_item = BerlinPoliceReportLoader(item=PoliceReportCase(), selector=case)
            case_item.add_css('created_at', 'div.cell.nowrap.date::text')
            case_item.add_css('url', 'div.cell.text > a::attr(href)')
            case_item.add_css('title', 'div.cell.text > a::text')

            yield case_item.load_item()
        
        next_page = response.css('#layout-grid__area--maincontent > section.modul-autoteaser > nav > ul > li.pager-item-next > a::attr(href)').get()
        
        if next_page is not None:
           next_page_url = 'https://www.berlin.de' + next_page
           yield response.follow(next_page_url, callback=self.parse)
