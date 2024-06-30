import datetime


class CasesPage:

    def __init__(self, itemloader):
        self.itemloader = itemloader

    def to_item(self):
        return self.itemloader.load_item()
    
    def get_all(self):
        self.get_filed_timestamp()
        self.get_url()
        self.get_title()
        self.get_location()
        self.get_text_content()
        self.get_metadata()
        
    def get_filed_timestamp(self):
        return
    
    def get_url(self):
        return
    
    def get_title(self):
        return
    
    def get_location(self):
        return
    
    def get_text_content(self):
        return
    
    def get_metadata(self):
        # Get current UTC time
        current_utc_time = datetime.datetime.now(datetime.UTC)
        # Format the time in ISO 8601 format
        formatted_time = current_utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        return self.itemloader.add_value('metadata', {"dateDownloaded": formatted_time})
