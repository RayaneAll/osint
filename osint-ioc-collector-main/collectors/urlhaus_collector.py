import csv
from io import StringIO
from .base_collector import BaseCollector
from normalizers import normalize_url


class URLhausCollector(BaseCollector):
    """
    Collector for URLhaus malicious URLs.
    """

    def parse(self, raw_data):
        """
        Parse URLhaus CSV data.

        Format: id,dateadded,url,url_status,last_online,threat,tags,urlhaus_link,reporter

        Args:
            raw_data: CSV content string

        Returns:
            List of IOC dictionaries
        """
        raise NotImplementedError
