from police_reports_crawler.models import (
    CasesItemModel,
)
from police_reports_crawler.pipelines import BaseDBPipeline


class PoliceReportsDBPipeline(BaseDBPipeline):

    max_items = 1000

    def insert_to_db(self, items):
        CasesItemModel.insert_many(items).execute()
