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
        iocs = []

        try:
            lines = []
            for line in raw_data.split('\n'):
                if not line:
                    continue
                if line.startswith('# id,'):
                    lines.append(line[2:])
                elif not line.startswith('#'):
                    lines.append(line)

            csv_data = '\n'.join(lines)
            reader = csv.DictReader(StringIO(csv_data), delimiter=',', quotechar='"')

            for row in reader:
                if not row:
                    continue

                url = normalize_url(row.get('url', '').strip())

                if not url:
                    continue

                threat = row.get('threat', '').strip()
                url_status = row.get('url_status', '').strip()
                url_tags = row.get('tags', '').strip()

                tags = []
                if threat:
                    tags.append(f"threat:{threat}")
                if url_status:
                    tags.append(f"status:{url_status}")
                if url_tags:
                    for tag in url_tags.split(','):
                        if tag.strip():
                            tags.append(tag.strip())

                ioc = self._create_ioc_dict(
                    ioc_value=url,
                    ioc_type='url',
                    threat_type='malware_distribution',
                    tags=','.join(tags) if tags else None,
                    raw_data=str(row)
                )

                iocs.append(ioc)

        except Exception as e:
            self.logger.error(f"Parse error in {self.name}: {e}")

        return iocs
