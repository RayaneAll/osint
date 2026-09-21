import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class IOCDatabase:
    """
    SQLite database manager for IOC storage and retrieval.
    """

    def __init__(self, db_path):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conn = None
        self._connect()

    def _connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def initialize_schema(self):
        """Initialize database schema from SQL file."""
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        self.conn.executescript(schema_sql)
        self.conn.commit()

    def _generate_ioc_id(self, ioc_value, source):
        """
        Generate unique ID for IOC.

        Args:
            ioc_value: IOC value
            source: Source feed name

        Returns:
            SHA256 hash as ID
        """
        data = f"{ioc_value}:{source}".encode('utf-8')
        return hashlib.sha256(data).hexdigest()[:16]

    def calculate_score(self, ioc_dict):
        """
        Calculate confidence score for IOC.

        Args:
            ioc_dict: IOC data dictionary

        Returns:
            Confidence score (0-100)
        """
        return 50

    def insert_ioc(self, ioc_dict):
        """
        Insert or update IOC in database.

        Args:
            ioc_dict: Dictionary containing IOC data

        Returns:
            Tuple of (ioc_id, is_new) where is_new is True if newly inserted
        """
        ioc_value = ioc_dict.get('ioc_value')
        source = ioc_dict.get('source')

        if not ioc_value or not source:
            raise ValueError("ioc_value and source are required")

        existing = self.get_ioc_by_value(ioc_value)

        now = datetime.utcnow().isoformat()

        if existing:
            from utils.deduplicator import merge_ioc_data
            merged = merge_ioc_data(dict(existing), ioc_dict)
            merged['confidence_score'] = self.calculate_score(merged)

            self.conn.execute('''
                UPDATE iocs SET
                    last_seen = ?,
                    threat_type = ?,
                    tags = ?,
                    raw_data = ?,
                    confidence_score = ?,
                    source = ?,
                    updated_at = ?
                WHERE ioc_value = ?
            ''', (
                merged['last_seen'],
                merged.get('threat_type'),
                merged.get('tags'),
                merged.get('raw_data'),
                merged['confidence_score'],
                merged['source'],
                merged['updated_at'],
                ioc_value
            ))
            self.conn.commit()
            return existing['id'], False

        ioc_id = self._generate_ioc_id(ioc_value, source)
        ioc_dict['id'] = ioc_id
        ioc_dict['created_at'] = now
        ioc_dict['updated_at'] = now
        ioc_dict['first_seen'] = ioc_dict.get('first_seen', now)
        ioc_dict['last_seen'] = ioc_dict.get('last_seen', now)
        ioc_dict['confidence_score'] = self.calculate_score(ioc_dict)

        self.conn.execute('''
            INSERT INTO iocs (
                id, ioc_value, ioc_type, threat_type, source,
                first_seen, last_seen, confidence_score, tags,
                raw_data, is_active, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ioc_dict['id'],
            ioc_dict['ioc_value'],
            ioc_dict['ioc_type'],
            ioc_dict.get('threat_type'),
            ioc_dict['source'],
            ioc_dict['first_seen'],
            ioc_dict['last_seen'],
            ioc_dict['confidence_score'],
            ioc_dict.get('tags'),
            ioc_dict.get('raw_data'),
            ioc_dict.get('is_active', 1),
            ioc_dict['created_at'],
            ioc_dict['updated_at']
        ))
        self.conn.commit()

        return ioc_id, True

    def get_ioc_by_value(self, ioc_value):
        """
        Retrieve IOC by its value.

        Args:
            ioc_value: IOC value to search for

        Returns:
            IOC record as dict or None if not found
        """
        cursor = self.conn.execute(
            'SELECT * FROM iocs WHERE ioc_value = ?',
            (ioc_value,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_active_iocs(self):
        """
        Retrieve all active IOCs.

        Returns:
            List of IOC dictionaries
        """
        cursor = self.conn.execute(
            'SELECT * FROM iocs WHERE is_active = 1 ORDER BY last_seen DESC'
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_iocs_since(self, since_date):
        """
        Retrieve IOCs updated since a specific date.

        Args:
            since_date: ISO format date string or datetime object

        Returns:
            List of IOC dictionaries
        """
        if isinstance(since_date, datetime):
            since_date = since_date.isoformat()

        cursor = self.conn.execute(
            'SELECT * FROM iocs WHERE updated_at >= ? AND is_active = 1 ORDER BY updated_at DESC',
            (since_date,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def deactivate_old_iocs(self, days=30):
        """
        Deactivate IOCs not seen in specified days.

        Args:
            days: Number of days threshold

        Returns:
            Number of IOCs deactivated
        """
        return 0

    def purge_old_iocs(self, days=90):
        """
        Permanently delete old inactive IOCs.

        Args:
            days: Number of days threshold

        Returns:
            Number of IOCs deleted
        """
        return 0

    def log_collection(self, source, status, iocs_collected=0, iocs_new=0,
                      iocs_updated=0, execution_time=0.0, error_message=None):
        """
        Log collection execution details.

        Args:
            source: Feed source name
            status: Status string ('success', 'failed', 'partial')
            iocs_collected: Total IOCs collected
            iocs_new: Number of new IOCs
            iocs_updated: Number of updated IOCs
            execution_time: Execution time in seconds
            error_message: Error message if failed
        """
        self.conn.execute('''
            INSERT INTO collection_logs (
                source, status, iocs_collected, iocs_new, iocs_updated,
                execution_time, error_message, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            source,
            status,
            iocs_collected,
            iocs_new,
            iocs_updated,
            execution_time,
            error_message,
            datetime.utcnow().isoformat()
        ))
        self.conn.commit()

    def get_statistics(self):
        """
        Get database statistics.

        Returns:
            Dictionary with various statistics
        """
        stats = {}

        cursor = self.conn.execute('SELECT COUNT(*) FROM iocs WHERE is_active = 1')
        stats['total_active_iocs'] = cursor.fetchone()[0]

        cursor = self.conn.execute('SELECT COUNT(*) FROM iocs WHERE is_active = 0')
        stats['total_inactive_iocs'] = cursor.fetchone()[0]

        cursor = self.conn.execute('''
            SELECT ioc_type, COUNT(*) as count
            FROM iocs WHERE is_active = 1
            GROUP BY ioc_type
        ''')
        stats['by_type'] = {row['ioc_type']: row['count'] for row in cursor.fetchall()}

        cursor = self.conn.execute('''
            SELECT source, COUNT(*) as count
            FROM iocs WHERE is_active = 1
            GROUP BY source
            ORDER BY count DESC
        ''')
        stats['by_source'] = {row['source']: row['count'] for row in cursor.fetchall()}

        cursor = self.conn.execute('SELECT AVG(confidence_score) FROM iocs WHERE is_active = 1')
        stats['avg_confidence_score'] = round(cursor.fetchone()[0] or 0, 2)

        cursor = self.conn.execute('''
            SELECT source, status, COUNT(*) as count
            FROM collection_logs
            WHERE timestamp >= datetime('now', '-7 days')
            GROUP BY source, status
        ''')
        stats['recent_collections'] = [(row['source'], row['status'], row['count']) for row in cursor.fetchall()]

        return stats
