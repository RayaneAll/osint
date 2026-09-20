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
        iocs = []

        try:
            lines = [line for line in raw_data.split('\n') if line and not line.startswith('#')]
            csv_data = '\n'.join(lines)

            reader = csv.DictReader(StringIO(csv_data), delimiter=',', quotechar='"')

            for row in reader:
                if not row:
                    continue

                ip = normalize_ip(row.get('dst_ip', '').strip().strip('"'))

                if not ip:
                    continue

                malware = row.get('malware', '').strip()
                c2_status = row.get('c2_status', '').strip()
                port = row.get('dst_port', '').strip()

                tags = []
                if malware:
                    tags.append(f"malware:{malware}")
                if port:
                    tags.append(f"port:{port}")
                if c2_status:
                    tags.append(f"status:{c2_status}")

                ioc = self._create_ioc_dict(
                    ioc_value=ip,
                    ioc_type='ip',
                    threat_type='botnet_c2',
                    tags=','.join(tags) if tags else None,
                    raw_data=str(row)
                )

                iocs.append(ioc)

        except Exception as e:
            self.logger.error(f"Parse error in {self.name}: {e}")

        return iocs
