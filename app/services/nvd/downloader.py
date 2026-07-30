from pathlib import Path
import tempfile
import requests


class NVDDownloader:

    BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    RESULTS_PER_PAGE = 2000

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "ASP Security Platform/1.0"
        })

    def download(
        self,
        start_index: int = 0,
        pub_start_date: str | None = None,
        pub_end_date: str | None = None,
    ) -> Path:

        params = {
            "resultsPerPage": self.RESULTS_PER_PAGE,
            "startIndex": start_index,
        }

        if pub_start_date and pub_end_date:

            params["pubStartDate"] = pub_start_date
            params["pubEndDate"] = pub_end_date

        response = self.session.get(
            self.BASE_URL,
            params=params,
            timeout=300,
        )

        response.raise_for_status()

        temp = tempfile.NamedTemporaryFile(
            suffix=".json",
            delete=False,
        )

        temp.write(response.content)
        temp.close()

        return Path(temp.name)
