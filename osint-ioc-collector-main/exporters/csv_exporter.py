import csv
import os
from datetime import datetime


class CSVExporter:
    """
    CSV exporter for IOC data.
    """

    FIELDS = [
        'ioc_value',
        'ioc_type',
        'threat_type',
        'source',
        'first_seen',
        'last_seen',
        'confidence_score',
        'tags'
    ]

    def __init__(self, output_dir):
        """
        Initialize CSV exporter.

        Args:
            output_dir: Directory for export files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export_full(self, iocs, filename=None):
        """
        Export full IOC dataset to CSV.

        Args:
            iocs: List of IOC dictionaries
            filename: Optional custom filename

        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"iocs_full_{timestamp}.csv"

        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS, extrasaction='ignore')
            writer.writeheader()

            for ioc in iocs:
                writer.writerow(ioc)

        return filepath

    def export_delta(self, iocs, since, filename=None):
        """
        Export incremental IOC dataset to CSV.

        Args:
            iocs: List of IOC dictionaries
            since: Since date (datetime or ISO string)
            filename: Optional custom filename

        Returns:
            Path to exported file
        """
        if filename is None:
            if isinstance(since, datetime):
                since_str = since.strftime('%Y%m%d')
            else:
                since_str = since[:10].replace('-', '')
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"iocs_delta_{since_str}_{timestamp}.csv"

        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS, extrasaction='ignore')
            writer.writeheader()

            for ioc in iocs:
                writer.writerow(ioc)

        return filepath
