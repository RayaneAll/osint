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
        raise NotImplementedError
