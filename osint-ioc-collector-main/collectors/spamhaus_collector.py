from .base_collector import BaseCollector
from normalizers.validators import validate_cidr


class SpamhausCollector(BaseCollector):
    """
    Collector for Spamhaus DROP list (CIDR ranges).
    """

    def parse(self, raw_data):
        """
        Parse Spamhaus DROP list text data.

        Format: CIDR ; SBL_ID ; Additional_info

        Args:
            raw_data: Text content string

        Returns:
            List of IOC dictionaries
        """
        iocs = []

        try:
            for line in raw_data.split('\n'):
                line = line.strip()

                if not line or line.startswith(';'):
                    continue

                parts = line.split(';')
                if not parts:
                    continue

                cidr = parts[0].strip()

                if not validate_cidr(cidr):
                    continue

                sbl_id = parts[1].strip() if len(parts) > 1 else ''

                tags = []
                if sbl_id:
                    tags.append(f"sbl:{sbl_id}")
                tags.append('cidr')

                ioc = self._create_ioc_dict(
                    ioc_value=cidr,
                    ioc_type='ip',
                    threat_type='spam_source',
                    tags=','.join(tags) if tags else None,
                    raw_data=line
                )

                iocs.append(ioc)

        except Exception as e:
            self.logger.error(f"Parse error in {self.name}: {e}")

        return iocs
