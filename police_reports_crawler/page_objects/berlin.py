from police_reports_crawler.page_objects.base_page_objects import CasesPage


class BerlinCasesPageProcesser(CasesPage):
    """
    https://www.berlin.de/polizei/polizeimeldungen/
    """
    def __init__(self, itemloader):
        super().__init__(itemloader)
    
    def get_filed_timestamp(self):
        case_filed_at = self.itemloader.add_css('filed_at', 'div.cell.nowrap.date::text')
        return case_filed_at
    
    def get_url(self):
        url = self.itemloader.add_css('url', 'div.cell.text > a::attr(href)')
        return url
    
    def get_title(self):
        title = self.itemloader.add_css('title', 'div.cell.text > a::text')
        return title
    
    def get_location(self):
        location = self.itemloader.add_css('location', 'div.cell.text > span::text')
        return location
