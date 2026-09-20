# Changelog

All notable changes to the IOC Collector project will be documented in this file.

## [1.0.0] - 2026-09-18

### Added
- Initial release of OSINT IOC Collector
- Support for 4 major threat intelligence feeds:
  - Feodo Tracker (Botnet C2 IPs)
  - URLhaus (Malicious URLs)
  - MalwareBazaar (Malware hashes)
  - Spamhaus DROP (Spam source networks)
- Automatic IOC normalization and validation
- Intelligent deduplication across sources
- Confidence scoring system (0-100)
- SQLite database storage with indexing
- Automated daily collection scheduling
- CSV and JSON export formats
- Full and delta export support
- Data retention and purging policies
- Comprehensive logging with rotation
- CLI interface with multiple modes:
  - `--init`: Database initialization
  - `--collect`: Manual collection
  - `--export`: Data export
  - `--schedule`: Automated scheduling
  - `--stats`: Statistics display
- Helper script `run.sh` for easy execution
- Complete documentation in README.md

### Technical Details
- Python 3.7+ compatible
- Minimal dependencies (requests, schedule, validators)
- No external database required
- Fully autonomous operation
- Retry logic with exponential backoff
- User-agent rotation
- Proper error handling and logging

### Database Schema
- `iocs` table with 13 fields
- `collection_logs` table for audit trail
- Optimized indexes for fast queries
- Support for ~50,000+ IOCs

### Features
- Multi-source IOC aggregation
- Cross-feed validation
- Age-based scoring
- Automatic source merging
- Configurable retention policies
- Production-ready logging
