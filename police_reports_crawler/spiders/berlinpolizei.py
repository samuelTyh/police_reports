import scrapy
import logging
from police_reports_crawler.items import PoliceReportCase
from police_reports_crawler.itemloaders.berlin import ItemTransformer
from police_reports_crawler.page_objects.berlin import PageItemSelector, SELECTOR_FOR_ALL, SELECTOR_FOR_NEXT_PAGE, SELECTOR_FOR_TEXT_CONTENT
from police_reports_crawler.utils.utils import get_proxy_url


class BerlinpolizeiSpider(scrapy.Spider):
    name = "berlinpolizei"
    start_urls = ["https://www.berlin.de/polizei/polizeimeldungen/?page_at_1_6=1#headline_1_6"]
    archive_urls = [
        'https://www.berlin.de/polizei/polizeimeldungen/archiv/2024/', 
        'https://www.berlin.de/polizei/polizeimeldungen/archiv/2023/', 
        'https://www.berlin.de/polizei/polizeimeldungen/archiv/2022/', 
        'https://www.berlin.de/polizei/polizeimeldungen/archiv/2021/', 
        'https://www.berlin.de/polizei/polizeimeldungen/archiv/2020/'
        ]
    
    def __init__(self, load_archive=False, with_proxy=False, *args, **kwargs):
        super(BerlinpolizeiSpider, self).__init__(*args, **kwargs)
        self.load_archive = load_archive == 'True'  # Convert string to boolean
        self.with_proxy = with_proxy == 'True'
        if self.load_archive:
            self.start_urls.extend(self.archive_urls)
        

    def start_requests(self):
        for start_url in self.start_urls:
            url = get_proxy_url(start_url) if self.with_proxy else start_url
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        cases = response.css(SELECTOR_FOR_ALL)

        for case in cases:
            case_item = ItemTransformer(item=PoliceReportCase(), selector=case)
            processer = PageItemSelector(itemloader=case_item)
            processer.get_all()
            url = processer.retrieve_url()
            main_item = processer.to_item()
            yield scrapy.Request(url=url, callback=self.parse_case_details, meta={'main': main_item})
            
        next_page = response.css(SELECTOR_FOR_NEXT_PAGE).get()
        
        if next_page is not None:
           next_page_url = 'https://www.berlin.de' + next_page
           yield response.follow(next_page_url, callback=self.parse)

    def parse_case_details(self, response):
        all_text = response.css(SELECTOR_FOR_TEXT_CONTENT).getall()
        inner_item = " ".join([text.strip() for text in all_text]).strip()

        main_item = response.meta['main']

        main_item['text_content'] = inner_item
        yield main_item
