from datetime import datetime, timedelta

from app.services.nvd.downloader import NVDDownloader
from app.services.nvd.importer import NVDImporter
from app.services.nvd.parser import NVDParser


class NVDUpdater:

    WINDOW_DAYS = 119

    def __init__(self):

        self.downloader = NVDDownloader()
        self.parser = NVDParser()
        self.importer = NVDImporter()

    def sync_range(self, start_date: datetime, end_date: datetime):

        start_index = 0
        total = None

        while total is None or start_index < total:

            print("=" * 70)
            print(start_date.date(), "->", end_date.date())
            print("Página:", start_index)
            print("=" * 70)

            file = self.downloader.download(
                start_index=start_index,
                pub_start_date=start_date.strftime("%Y-%m-%dT00:00:00.000"),
                pub_end_date=end_date.strftime("%Y-%m-%dT23:59:59.999"),
            )

            data = self.parser.load(file)

            if total is None:
                total = data["totalResults"]

            self.importer.import_data(data)

            results = data["resultsPerPage"]

            if results == 0:
                break

            start_index += results

    def full_sync(self):

        current = datetime(2024, 1, 1)
        finish = datetime.now()

        while current < finish:

            end = current + timedelta(days=self.WINDOW_DAYS)

            if end > finish:
                end = finish

            self.sync_range(current, end)

            current = end + timedelta(days=1)
