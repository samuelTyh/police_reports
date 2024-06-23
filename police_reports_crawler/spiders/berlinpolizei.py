import scrapy


class BerlinpolizeiSpider(scrapy.Spider):
    name = "berlinpolizei"
    allowed_domains = ["www.berlin.de"]
    start_urls = ["https://www.berlin.de/polizei/polizeimeldungen/?page_at_1_6=1#headline_1_6"]
    
    

    def parse(self, response):
        
        cases = response.css('#layout-grid__area--maincontent > section.modul-autoteaser > ul > li')

        for case in cases:
            metadata = dict()
            metadata['date'] = case.css('div.cell.nowrap.date::text').get().replace(' Uhr', '')
            metadata['url'] = case.css('div.cell.text > a::attr(href)').get()
            metadata['title'] = case.css('div.cell.text > a::text').get()

            yield metadata
        
        next_page = response.css('#layout-grid__area--maincontent > section.modul-autoteaser > nav > ul > li.pager-item-next > a::attr(href)').get()
        
        if next_page is not None:
           next_page_url = 'https://www.berlin.de' + next_page
           yield response.follow(next_page_url, callback=self.parse)
