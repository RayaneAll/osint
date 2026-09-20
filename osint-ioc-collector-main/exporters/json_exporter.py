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
        raise NotImplementedError

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
        raise NotImplementedError
