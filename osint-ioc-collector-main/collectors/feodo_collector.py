import csv
from io import StringIO
from .base_collector import BaseCollector
from normalizers import normalize_ip


class FeodoCollector(BaseCollector):
    """
    Collector for Feodo Tracker botnet C2 IP addresses.
    """

    def parse(self, raw_data):
        """
        Parse Feodo Tracker CSV data.

        Format: first_seen_utc,dst_ip,dst_port,c2_status,last_online,malware

        Args:
            raw_data: CSV content string

        Returns:
            List of IOC dictionaries
        """
        raise NotImplementedError
