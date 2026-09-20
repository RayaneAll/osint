import json
import os
from datetime import datetime


class JSONExporter:
    """
    JSON exporter for IOC data.
    """

    def __init__(self, output_dir):
        """
        Initialize JSON exporter.

        Args:
            output_dir: Directory for export files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export_full(self, iocs, filename=None):
        """
        Export full IOC dataset to JSON.

        Args:
            iocs: List of IOC dictionaries
            filename: Optional custom filename

        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"iocs_full_{timestamp}.json"

        filepath = os.path.join(self.output_dir, filename)

        export_data = {
            'metadata': {
                'generated_at': datetime.utcnow().isoformat(),
                'total_iocs': len(iocs),
                'export_type': 'full'
            },
            'iocs': iocs
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return filepath

    def export_delta(self, iocs, since, filename=None):
        """
        Export incremental IOC dataset to JSON.

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
            filename = f"iocs_delta_{since_str}_{timestamp}.json"

        filepath = os.path.join(self.output_dir, filename)

        since_iso = since.isoformat() if isinstance(since, datetime) else since

        export_data = {
            'metadata': {
                'generated_at': datetime.utcnow().isoformat(),
                'total_iocs': len(iocs),
                'export_type': 'delta',
                'since_date': since_iso
            },
            'iocs': iocs
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return filepath
