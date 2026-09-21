import schedule
import time
import json
import os
from datetime import datetime, timedelta
from storage import IOCDatabase
from exporters import CSVExporter, JSONExporter
from collectors import (
    FeodoCollector,
    URLhausCollector,
    MalwareBazaarCollector,
    SpamhausCollector
)


class JobScheduler:
    """
    Job scheduler for automated IOC collection and export.
    """

    COLLECTOR_MAP = {
        'feodo_collector': FeodoCollector,
        'urlhaus_collector': URLhausCollector,
        'malwarebazaar_collector': MalwareBazaarCollector,
        'spamhaus_collector': SpamhausCollector
    }

    def __init__(self, config_path, logger):
        """
        Initialize job scheduler.

        Args:
            config_path: Path to settings.json
            logger: Logger instance
        """
        self.logger = logger
        self.config = self._load_config(config_path)
        self.db = IOCDatabase(self.config['database']['path'])
        self.feeds = self._load_feeds()

    def _load_config(self, config_path):
        """Load settings configuration."""
        with open(config_path, 'r') as f:
            return json.load(f)

    def _load_feeds(self):
        """Load feed configurations."""
        feeds_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'feeds.json')
        with open(feeds_path, 'r') as f:
            data = json.load(f)
            return [feed for feed in data['feeds'] if feed.get('enabled', True)]

    def collect_all(self):
        """
        Execute collection from all enabled feeds.

        Returns:
            Dictionary with collection statistics
        """
        self.logger.info("Starting collection from all feeds")

        total_collected = 0
        total_new = 0
        total_updated = 0

        for feed_config in self.feeds:
            collector_class = self.COLLECTOR_MAP.get(feed_config['collector'])

            if not collector_class:
                self.logger.warning(f"Unknown collector type: {feed_config['collector']}")
                continue

            collector = collector_class(feed_config, self.logger)
            iocs, status, error_msg = collector.collect()

            new_count = 0
            updated_count = 0

            for ioc in iocs:
                try:
                    ioc_id, is_new = self.db.insert_ioc(ioc)
                    if is_new:
                        new_count += 1
                    else:
                        updated_count += 1
                except Exception as e:
                    self.logger.error(f"Failed to insert IOC: {e}")

            total_collected += len(iocs)
            total_new += new_count
            total_updated += updated_count

            self.db.log_collection(
                source=feed_config['name'],
                status=status,
                iocs_collected=len(iocs),
                iocs_new=new_count,
                iocs_updated=updated_count,
                error_message=error_msg
            )

            self.logger.info(
                f"{feed_config['name']}: collected={len(iocs)}, new={new_count}, updated={updated_count}"
            )

        retention_days = self.config['retention']['inactive_days']
        deactivated = self.db.deactivate_old_iocs(retention_days)
        if deactivated > 0:
            self.logger.info(f"Deactivated {deactivated} old IOCs (>{retention_days} days)")

        purge_days = self.config['retention']['purge_days']
        purged = self.db.purge_old_iocs(purge_days)
        if purged > 0:
            self.logger.info(f"Purged {purged} old IOCs (>{purge_days} days)")

        stats = {
            'total_collected': total_collected,
            'total_new': total_new,
            'total_updated': total_updated,
            'deactivated': deactivated,
            'purged': purged
        }

        self.logger.info(f"Collection complete: {stats}")
        return stats

    def export_data(self):
        """
        Export IOC data according to configuration.

        Returns:
            List of exported file paths
        """
        if not self.config['export']['auto_export']:
            self.logger.info("Auto-export disabled")
            return []

        self.logger.info("Starting data export")

        output_dir = self.config['export']['output_dir']
        formats = self.config['export']['formats']
        include_delta = self.config['export']['include_delta']

        exported_files = []

        iocs = self.db.get_all_active_iocs()
        self.logger.info(f"Exporting {len(iocs)} active IOCs")

        if 'csv' in formats:
            csv_exporter = CSVExporter(output_dir)
            csv_file = csv_exporter.export_full(iocs)
            exported_files.append(csv_file)
            self.logger.info(f"Exported CSV: {csv_file}")

        if 'json' in formats:
            json_exporter = JSONExporter(output_dir)
            json_file = json_exporter.export_full(iocs)
            exported_files.append(json_file)
            self.logger.info(f"Exported JSON: {json_file}")

        if include_delta:
            yesterday = datetime.utcnow() - timedelta(days=1)
            delta_iocs = self.db.get_iocs_since(yesterday)

            if delta_iocs:
                self.logger.info(f"Exporting {len(delta_iocs)} delta IOCs")

                if 'csv' in formats:
                    csv_exporter = CSVExporter(output_dir)
                    csv_file = csv_exporter.export_delta(delta_iocs, yesterday)
                    exported_files.append(csv_file)
                    self.logger.info(f"Exported delta CSV: {csv_file}")

                if 'json' in formats:
                    json_exporter = JSONExporter(output_dir)
                    json_file = json_exporter.export_delta(delta_iocs, yesterday)
                    exported_files.append(json_file)
                    self.logger.info(f"Exported delta JSON: {json_file}")

        return exported_files

    def scheduled_job(self):
        """Execute scheduled collection and export job."""
        self.logger.info("=" * 60)
        self.logger.info("Starting scheduled job")

        try:
            stats = self.collect_all()

            if self.config['export']['auto_export']:
                exported_files = self.export_data()
                self.logger.info(f"Exported {len(exported_files)} files")

            self.logger.info("Scheduled job completed successfully")

        except Exception as e:
            self.logger.error(f"Scheduled job failed: {e}", exc_info=True)

        self.logger.info("=" * 60)

    def start(self):
        """
        Start scheduler in daemon mode.
        """
        raise NotImplementedError

    def stop(self):
        """Stop scheduler and cleanup."""
        self.logger.info("Stopping scheduler")
        self.db.close()
