# OSINT IOC Collector

Automated collection and aggregation of Indicators of Compromise (IOCs) from public threat intelligence feeds.

## 🆕 New: Web Dashboard!

A modern, dark-themed web interface for visualizing and managing your IOC collection in real-time.

**Quick Start Dashboard**:
```bash
./run_dashboard.sh
# Open http://localhost:5000
```

See [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md) for full documentation.

## Features

- **🎨 Web Dashboard**: Modern interface with real-time statistics and charts
- **Multi-Source Collection**: Aggregates IOCs from 4 major threat feeds:
  - Feodo Tracker (Botnet C2 IPs)
  - URLhaus (Malicious URLs)
  - MalwareBazaar (Malware hashes)
  - Spamhaus DROP (Spam source networks)

- **Data Normalization**: Automatic validation and normalization of IPs, domains, URLs, and hashes

- **Deduplication**: Intelligent merging of duplicate IOCs across sources

- **Confidence Scoring**: Dynamic scoring based on source reputation, age, and cross-feed validation

- **Automated Scheduling**: Daily collection with configurable execution time

- **Multiple Export Formats**: CSV and JSON with full and delta export support

- **Data Retention**: Automatic deactivation and purging of stale IOCs

## Installation

### Requirements

- Python 3.7+
- Internet connectivity for feed access

### Setup

1. Clone or navigate to the project directory:
```bash
cd /Users/ademmedjahed/Project/ioc-collector
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Initialize the database:
```bash
python3 main.py --init
```

## Configuration

### Feed Configuration (`config/feeds.json`)

Configure which feeds to collect from:

```json
{
  "feeds": [
    {
      "name": "feodo",
      "url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
      "type": "csv",
      "collector": "feodo_collector",
      "enabled": true
    }
  ]
}
```

Set `enabled: false` to disable a specific feed.

### Application Settings (`config/settings.json`)

Key configuration options:

- **Database Path**: Location of SQLite database
- **Collection Schedule**: Time for daily automated collection (24h format)
- **Retention Policy**: Days before IOCs are deactivated/purged
- **Export Settings**: Output formats and directories
- **Logging**: Log level, file location, and rotation settings

Example:
```json
{
  "scheduler": {
    "collection_time": "02:00",
    "enabled": true
  },
  "retention": {
    "inactive_days": 30,
    "purge_days": 90
  },
  "export": {
    "auto_export": true,
    "formats": ["csv", "json"]
  }
}
```

## Usage

### Manual Collection

Collect IOCs from all enabled feeds:

```bash
python3 main.py --collect
```

Output:
```
Collection Summary:
  Total collected: 1523
  New IOCs: 142
  Updated IOCs: 1381
  Deactivated: 23
  Purged: 5
```

### Export Data

Export current IOC database:

```bash
python3 main.py --export
```

Output files:
- `data/exports/iocs_full_YYYYMMDD_HHMMSS.csv`
- `data/exports/iocs_full_YYYYMMDD_HHMMSS.json`
- `data/exports/iocs_delta_YYYYMMDD_YYYYMMDD_HHMMSS.csv` (last 24h changes)
- `data/exports/iocs_delta_YYYYMMDD_YYYYMMDD_HHMMSS.json`

### Scheduled Collection

Run continuous scheduler for automated daily collection:

```bash
python3 main.py --schedule
```

The scheduler will:
1. Run an initial collection immediately
2. Execute daily collections at the configured time (default: 02:00)
3. Auto-export after each collection
4. Log all activities to `logs/ioc_collector.log`

Stop with `Ctrl+C`.

### View Statistics

Display database statistics:

```bash
python3 main.py --stats
```

Output:
```
============================================================
IOC Database Statistics
============================================================

Total Active IOCs: 15423
Total Inactive IOCs: 1247

Average Confidence Score: 68.5

IOCs by Type:
  ip             :   8234
  url            :   4521
  hash           :   2456
  domain         :    212

IOCs by Source:
  feodo                :   8234
  urlhaus              :   4521
  malwarebazaar        :   2456
  spamhaus_drop        :    212

Recent Collections (last 7 days):
  feodo                [success ]:   7 runs
  urlhaus              [success ]:   7 runs
  malwarebazaar        [success ]:   7 runs
  spamhaus_drop        [success ]:   7 runs
============================================================
```

## Data Schema

### IOC Record Structure

Each IOC contains:

| Field | Type | Description |
|-------|------|-------------|
| `ioc_value` | TEXT | The actual IOC (IP, URL, hash, etc.) |
| `ioc_type` | TEXT | Type: ip, url, hash, domain |
| `threat_type` | TEXT | Classification: botnet_c2, malware, spam_source, etc. |
| `source` | TEXT | Origin feed(s), comma-separated if multiple |
| `first_seen` | TEXT | ISO8601 timestamp of first observation |
| `last_seen` | TEXT | ISO8601 timestamp of most recent observation |
| `confidence_score` | INTEGER | Score 0-100 based on reputation and age |
| `tags` | TEXT | Comma-separated metadata tags |
| `is_active` | INTEGER | 1 if active, 0 if deactivated |

### CSV Export Format

```csv
ioc_value,ioc_type,threat_type,source,first_seen,last_seen,confidence_score,tags
192.0.2.1,ip,botnet_c2,feodo,2024-01-01T12:00:00,2024-01-02T14:30:00,75,malware:emotet,port:8080
```

### JSON Export Format

```json
{
  "metadata": {
    "generated_at": "2024-01-02T15:00:00",
    "total_iocs": 1523,
    "export_type": "full"
  },
  "iocs": [
    {
      "ioc_value": "192.0.2.1",
      "ioc_type": "ip",
      "threat_type": "botnet_c2",
      "source": "feodo",
      "first_seen": "2024-01-01T12:00:00",
      "last_seen": "2024-01-02T14:30:00",
      "confidence_score": 75,
      "tags": "malware:emotet,port:8080"
    }
  ]
}
```

## Architecture

```
ioc-collector/
├── collectors/        # Feed-specific data collectors
├── normalizers/       # IOC validation and normalization
├── storage/           # SQLite database interface
├── exporters/         # CSV/JSON export modules
├── scheduler/         # Automated job scheduling
├── utils/             # Logging and deduplication
├── config/            # Configuration files
├── data/              # Database and exports
│   ├── ioc.db
│   └── exports/
└── logs/              # Application logs
```

## Confidence Scoring Algorithm

The confidence score (0-100) is calculated based on:

- **Base score**: 50 points
- **Multiple sources**: +20 points if seen in multiple feeds
- **Reputable source**: +15 points for known reliable feeds
- **Age penalty**: -5 points per week after 7 days since last seen
- **Floor/Ceiling**: Minimum 0, maximum 100

Example:
```
IOC seen in 2 feeds (Feodo + URLhaus), last seen yesterday:
Score = 50 + 20 + 15 = 85
```

## Data Retention Policy

Default retention policy:

1. **Active IOCs**: IOCs seen within last 30 days remain active
2. **Inactive IOCs**: IOCs not seen for 30+ days are deactivated (soft delete)
3. **Purged IOCs**: Inactive IOCs older than 90 days are permanently deleted

Configure in `config/settings.json`:
```json
{
  "retention": {
    "inactive_days": 30,
    "purge_days": 90
  }
}
```

## Troubleshooting

### Database Locked Error

If you see "database is locked" errors:
```bash
# Close any running processes
pkill -f main.py

# Re-initialize if needed
python3 main.py --init
```

### Failed Feed Collection

Check logs for details:
```bash
tail -f logs/ioc_collector.log
```

Common issues:
- **Network timeout**: Increase timeout in collector code
- **Rate limiting**: Add delay between feed requests
- **Invalid SSL**: Update certificates or disable verification (not recommended)

### Empty Export Files

Verify database has data:
```bash
python3 main.py --stats
```

If no IOCs, run collection:
```bash
python3 main.py --collect
```

### Permission Errors

Ensure directories are writable:
```bash
chmod -R 755 /Users/ademmedjahed/Project/ioc-collector
```

## Logs

Application logs are stored in `logs/ioc_collector.log` with automatic rotation:

- **Max size**: 50MB
- **Backup count**: 5 files
- **Format**: `YYYY-MM-DD HH:MM:SS - LEVEL - message`

View recent logs:
```bash
tail -100 logs/ioc_collector.log
```

## Performance

Typical performance metrics:

- **Collection time**: ~30-60 seconds for all 4 feeds
- **Database size**: ~50-100MB for 50,000 IOCs
- **Memory usage**: <100MB during collection
- **Export time**: ~2-5 seconds for 50,000 IOCs

## Security Considerations

1. **No credentials required**: All feeds are public
2. **Read-only operations**: Collectors never modify source data
3. **Input validation**: All IOCs validated before storage
4. **SQL injection protection**: Parameterized queries only
5. **Local storage**: All data stored locally in SQLite

## Limitations

- No authentication support for private feeds
- Serial collection only (no parallel fetching)
- SQLite storage (not suitable for distributed deployments)
- No real-time streaming (batch collection only)

## License

This project is provided for educational and research purposes.

## Data Sources

- **Feodo Tracker**: https://feodotracker.abuse.ch/
- **URLhaus**: https://urlhaus.abuse.ch/
- **MalwareBazaar**: https://bazaar.abuse.ch/
- **Spamhaus**: https://www.spamhaus.org/

All data sources are publicly available threat intelligence feeds maintained by their respective organizations.

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review logs in `logs/ioc_collector.log`
3. Verify configuration in `config/settings.json`

## Version

Current version: 1.0.0
