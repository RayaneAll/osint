import requests
import time
from abc import ABC, abstractmethod
from datetime import datetime


class BaseCollector(ABC):
    """
    Abstract base class for IOC collectors.
    """

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    ]

    def __init__(self, feed_config, logger):
        """
        Initialize collector.

        Args:
            feed_config: Feed configuration dictionary
            logger: Logger instance
        """
        self.feed_config = feed_config
        self.logger = logger
        self.name = feed_config.get('name', 'unknown')
        self.url = feed_config.get('url')
        self.timeout = 30
        self.max_retries = 3
        self.retry_delay = 5

    def _get_headers(self):
        """
        Get HTTP headers with user agent rotation.

        Returns:
            Headers dictionary
        """
        return {
            'User-Agent': self.USER_AGENTS[int(time.time()) % len(self.USER_AGENTS)],
            'Accept': '*/*'
        }

    def fetch(self):
        """
        Fetch data from feed URL with retry logic.

        Returns:
            Response content as text or None on failure
        """
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Fetching {self.name} (attempt {attempt + 1}/{self.max_retries})")

                response = requests.get(
                    self.url,
                    headers=self._get_headers(),
                    timeout=self.timeout
                )

                response.raise_for_status()

                self.logger.info(f"Successfully fetched {self.name}")
                return response.text

            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Fetch attempt {attempt + 1} failed for {self.name}: {e}")

                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    self.logger.error(f"Failed to fetch {self.name} after {self.max_retries} attempts")
                    return None

    @abstractmethod
    def parse(self, raw_data):
        """
        Parse raw feed data into structured IOCs.

        Args:
            raw_data: Raw data string from feed

        Returns:
            List of IOC dictionaries
        """
        pass

    def collect(self):
        """
        Execute full collection workflow: fetch and parse.

        Returns:
            Tuple of (iocs_list, status, error_message)
        """
        start_time = time.time()

        try:
            raw_data = self.fetch()

            if raw_data is None:
                return [], 'failed', 'Failed to fetch data'

            iocs = self.parse(raw_data)

            execution_time = time.time() - start_time
            self.logger.info(f"Collected {len(iocs)} IOCs from {self.name} in {execution_time:.2f}s")

            return iocs, 'success', None

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Collection error: {str(e)}"
            self.logger.error(f"{self.name}: {error_msg}")
            return [], 'failed', error_msg

    def _create_ioc_dict(self, ioc_value, ioc_type, threat_type=None, tags=None, raw_data=None):
        """
        Create standardized IOC dictionary.

        Args:
            ioc_value: The IOC value
            ioc_type: Type of IOC (ip, domain, hash, url)
            threat_type: Threat classification
            tags: Comma-separated tags
            raw_data: Original raw data

        Returns:
            IOC dictionary
        """
        now = datetime.utcnow().isoformat()

        return {
            'ioc_value': ioc_value,
            'ioc_type': ioc_type,
            'threat_type': threat_type,
            'source': self.name,
            'first_seen': now,
            'last_seen': now,
            'tags': tags,
            'raw_data': raw_data
        }
