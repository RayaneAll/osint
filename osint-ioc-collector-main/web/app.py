#!/usr/bin/env python3
"""
Flask Web Application for IOC Collector Dashboard
"""

import os
import sys
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, send_file
from threading import Thread
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from storage import IOCDatabase
from scheduler import JobScheduler
from utils import setup_logger


def create_app(config_path=None):
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ioc-collector-secret-key-change-in-production'
    app.config['JSON_SORT_KEYS'] = False

    if config_path is None:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.json')

    with open(config_path, 'r') as f:
        settings = json.load(f)

    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), settings['database']['path'])
    app.config['DB_PATH'] = db_path
    app.config['SETTINGS'] = settings

    logger = setup_logger(
        'web_app',
        os.path.join(os.path.dirname(os.path.dirname(__file__)), settings['logging']['file']),
        level=getattr(__import__('logging'), settings['logging']['level'])
    )
    app.logger = logger

    @app.route('/')
    def index():
        """Dashboard home page."""
        return render_template('index.html')

    @app.route('/iocs')
    def iocs_page():
        """IOCs list page."""
        return render_template('iocs.html')

    @app.route('/api/stats')
    def get_stats():
        """Get database statistics."""
        try:
            db = IOCDatabase(app.config['DB_PATH'])
            stats = db.get_statistics()
            db.close()

            return jsonify({
                'success': True,
                'stats': stats
            })
        except Exception as e:
            app.logger.error(f"Error fetching stats: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/iocs')
    def get_iocs():
        """Get IOCs list with pagination."""
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 50))
            ioc_type = request.args.get('type', None)
            source = request.args.get('source', None)

            db = IOCDatabase(app.config['DB_PATH'])

            query = 'SELECT * FROM iocs WHERE is_active = 1'
            params = []

            if ioc_type:
                query += ' AND ioc_type = ?'
                params.append(ioc_type)

            if source:
                query += ' AND source LIKE ?'
                params.append(f'%{source}%')

            query += ' ORDER BY last_seen DESC LIMIT ? OFFSET ?'
            params.extend([per_page, (page - 1) * per_page])

            cursor = db.conn.execute(query, params)
            iocs = [dict(row) for row in cursor.fetchall()]

            count_query = 'SELECT COUNT(*) FROM iocs WHERE is_active = 1'
            count_params = []
            if ioc_type:
                count_query += ' AND ioc_type = ?'
                count_params.append(ioc_type)
            if source:
                count_query += ' AND source LIKE ?'
                count_params.append(f'%{source}%')

            cursor = db.conn.execute(count_query, count_params)
            total = cursor.fetchone()[0]

            db.close()

            return jsonify({
                'success': True,
                'iocs': iocs,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            })
        except Exception as e:
            app.logger.error(f"Error fetching IOCs: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/collect', methods=['POST'])
    def trigger_collection():
        """Trigger manual collection."""
        try:
            def run_collection():
                scheduler = JobScheduler(config_path, app.logger)
                scheduler.collect_all()
                scheduler.stop()

            thread = Thread(target=run_collection)
            thread.daemon = True
            thread.start()

            return jsonify({
                'success': True,
                'message': 'Collection started in background'
            })
        except Exception as e:
            app.logger.error(f"Error starting collection: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/export', methods=['POST'])
    def trigger_export():
        """Trigger data export."""
        try:
            export_format = request.json.get('format', 'csv')

            scheduler = JobScheduler(config_path, app.logger)
            files = scheduler.export_data()
            scheduler.stop()

            matching_files = [f for f in files if export_format in f.lower()]

            return jsonify({
                'success': True,
                'message': f'Exported {len(matching_files)} files',
                'files': matching_files
            })
        except Exception as e:
            app.logger.error(f"Error exporting data: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/recent-activity')
    def get_recent_activity():
        """Get recent collection activity."""
        try:
            db = IOCDatabase(app.config['DB_PATH'])

            cursor = db.conn.execute('''
                SELECT source, status, iocs_collected, iocs_new,
                       iocs_updated, timestamp, error_message
                FROM collection_logs
                ORDER BY timestamp DESC
                LIMIT 20
            ''')

            activities = [dict(row) for row in cursor.fetchall()]
            db.close()

            return jsonify({
                'success': True,
                'activities': activities
            })
        except Exception as e:
            app.logger.error(f"Error fetching activity: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/chart-data')
    def get_chart_data():
        """Get data for charts."""
        try:
            db = IOCDatabase(app.config['DB_PATH'])
            stats = db.get_statistics()

            cursor = db.conn.execute('''
                SELECT DATE(last_seen) as date, COUNT(*) as count
                FROM iocs
                WHERE is_active = 1
                AND last_seen >= datetime('now', '-30 days')
                GROUP BY DATE(last_seen)
                ORDER BY date
            ''')
            timeline = [dict(row) for row in cursor.fetchall()]

            db.close()

            return jsonify({
                'success': True,
                'data': {
                    'by_type': stats.get('by_type', {}),
                    'by_source': stats.get('by_source', {}),
                    'timeline': timeline
                }
            })
        except Exception as e:
            app.logger.error(f"Error fetching chart data: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    return app


def main():
    """Run the Flask application."""
    app = create_app()
    print("\n" + "="*60)
    print("IOC Collector Dashboard")
    print("="*60)
    print(f"\n📊 Dashboard available at: http://localhost:5000")
    print(f"🔄 Use Ctrl+C to stop the server\n")

    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    main()
