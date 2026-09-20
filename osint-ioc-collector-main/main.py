#!/usr/bin/env python3
"""
OSINT IOC Collector - Main Entry Point

Automated collection of Indicators of Compromise from public threat feeds.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

from utils import setup_logger
from storage import IOCDatabase
from scheduler import JobScheduler


def load_config():
    """Load application configuration."""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.json')
    with open(config_path, 'r') as f:
        return json.load(f)


def init_database(config, logger):
    """Initialize database schema."""
    logger.info("Initializing database")
    db = IOCDatabase(config['database']['path'])
    db.initialize_schema()
    db.close()
    logger.info("Database initialized successfully")


def run_collection(config, logger):
    """Run manual collection."""
    logger.info("Starting manual collection")
    scheduler = JobScheduler(
        os.path.join(os.path.dirname(__file__), 'config', 'settings.json'),
        logger
    )
    stats = scheduler.collect_all()

    print("\nCollection Summary:")
    print(f"  Total collected: {stats['total_collected']}")
    print(f"  New IOCs: {stats['total_new']}")
    print(f"  Updated IOCs: {stats['total_updated']}")
    print(f"  Deactivated: {stats['deactivated']}")
    print(f"  Purged: {stats['purged']}")

    scheduler.stop()


def run_export(config, logger):
    """Run manual export."""
    logger.info("Starting manual export")
    scheduler = JobScheduler(
        os.path.join(os.path.dirname(__file__), 'config', 'settings.json'),
        logger
    )
    exported_files = scheduler.export_data()

    print("\nExport Summary:")
    print(f"  Files exported: {len(exported_files)}")
    for filepath in exported_files:
        print(f"    - {filepath}")

    scheduler.stop()


def run_scheduler(config, logger):
    """Run scheduler in daemon mode."""
    logger.info("Starting scheduler daemon")
    scheduler = JobScheduler(
        os.path.join(os.path.dirname(__file__), 'config', 'settings.json'),
        logger
    )

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler interrupted by user")
    finally:
        scheduler.stop()


def show_stats(config, logger):
    """Display database statistics."""
    logger.info("Fetching statistics")
    db = IOCDatabase(config['database']['path'])
    stats = db.get_statistics()
    db.close()

    print("\n" + "=" * 60)
    print("IOC Database Statistics")
    print("=" * 60)

    print(f"\nTotal Active IOCs: {stats['total_active_iocs']}")
    print(f"Total Inactive IOCs: {stats['total_inactive_iocs']}")

    print(f"\nAverage Confidence Score: {stats['avg_confidence_score']}")

    print("\nIOCs by Type:")
    for ioc_type, count in stats['by_type'].items():
        print(f"  {ioc_type:15s}: {count:6d}")

    print("\nIOCs by Source:")
    for source, count in sorted(stats['by_source'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {source:20s}: {count:6d}")

    if stats['recent_collections']:
        print("\nRecent Collections (last 7 days):")
        for source, status, count in stats['recent_collections']:
            print(f"  {source:20s} [{status:8s}]: {count:3d} runs")

    print("\n" + "=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='OSINT IOC Collector - Automated threat intelligence aggregation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --init                Initialize database
  %(prog)s --collect             Run manual collection
  %(prog)s --export              Export IOC data
  %(prog)s --schedule            Start scheduler daemon
  %(prog)s --stats               Show statistics
        """
    )

    parser.add_argument(
        '--init',
        action='store_true',
        help='Initialize database schema'
    )

    parser.add_argument(
        '--collect',
        action='store_true',
        help='Run manual collection from all feeds'
    )

    parser.add_argument(
        '--export',
        action='store_true',
        help='Export IOC data to CSV/JSON'
    )

    parser.add_argument(
        '--schedule',
        action='store_true',
        help='Start scheduler daemon for automated collection'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Display database statistics'
    )

    args = parser.parse_args()

    if not any([args.init, args.collect, args.export, args.schedule, args.stats]):
        parser.print_help()
        sys.exit(1)

    config = load_config()

    logger = setup_logger(
        name='ioc_collector',
        log_file=config['logging']['file'],
        level=getattr(__import__('logging'), config['logging']['level']),
        max_bytes=config['logging']['max_bytes'],
        backup_count=config['logging']['backup_count']
    )

    try:
        if args.init:
            init_database(config, logger)
            print("Database initialized successfully")

        elif args.collect:
            run_collection(config, logger)

        elif args.export:
            run_export(config, logger)

        elif args.schedule:
            run_scheduler(config, logger)

        elif args.stats:
            show_stats(config, logger)

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
