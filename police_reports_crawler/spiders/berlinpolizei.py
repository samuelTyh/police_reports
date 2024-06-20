import scrapy


class BerlinpolizeiSpider(scrapy.Spider):
    name = "berlinpolizei"
    allowed_domains = ["www.berlin.de"]
    start_urls = ["https://www.berlin.de/polizei/polizeimeldungen/?page_at_1_6=1#headline_1_6"]
    
    

    def parse(self, response):
        
        cases = response.css('#layout-grid__area--maincontent > section.modul-autoteaser > ul > li')

        pass
