# Quick Start Guide

Get up and running with IOC Collector in 5 minutes.

## Installation

```bash
cd /Users/ademmedjahed/Project/ioc-collector

# Install dependencies
pip3 install -r requirements.txt

# Or use the helper script (recommended)
./run.sh --init
```

## First Collection

```bash
# Option 1: Using helper script
./run.sh --collect

# Option 2: Direct Python execution
source venv/bin/activate
python3 main.py --collect
```

Expected output:
```
Collection Summary:
  Total collected: 15000+
  New IOCs: 15000+
  Updated IOCs: 0
  Deactivated: 0
  Purged: 0
```

## View Your Data

```bash
# Show statistics
./run.sh --stats

# Export to CSV/JSON
./run.sh --export

# Check exported files
ls -lh data/exports/
```

## Automated Collection

For daily automated collection:

```bash
# Start scheduler (runs in foreground)
./run.sh --schedule

# Or run in background with nohup
nohup ./run.sh --schedule > scheduler.log 2>&1 &
```

The scheduler will:
1. Run immediately on start
2. Execute daily at 02:00 AM
3. Auto-export after each collection
4. Log everything to `logs/ioc_collector.log`

## Common Tasks

### Check what's in the database
```bash
./run.sh --stats
```

### Export fresh data
```bash
./run.sh --export
ls data/exports/
```

### Update IOCs
```bash
./run.sh --collect
```

### View logs
```bash
tail -f logs/ioc_collector.log
```

## Configuration

Edit `config/settings.json` to customize:
- Collection schedule time
- Retention policies (deactivation/purging)
- Export formats (CSV, JSON)
- Logging level

Edit `config/feeds.json` to:
- Enable/disable specific feeds
- Add custom feeds (with custom collectors)

## Troubleshooting

### No data collected
```bash
# Check logs
grep "error" -i logs/ioc_collector.log

# Test individual feed
curl -s "https://feodotracker.abuse.ch/downloads/ipblocklist.csv" | head
```

### Database locked
```bash
# Stop all processes
pkill -f "python3 main.py"

# If needed, reset database
rm data/ioc.db
./run.sh --init
```

### Virtual environment issues
```bash
# Recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

- Review the full README.md for detailed documentation
- Customize collection schedule in `config/settings.json`
- Set up automated backups of `data/ioc.db`
- Integrate exports with your SIEM/threat platform

## Production Deployment

For production use:

1. **Systemd Service** (Linux):
```ini
[Unit]
Description=IOC Collector
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/ioc-collector
ExecStart=/path/to/ioc-collector/run.sh --schedule
Restart=always

[Install]
WantedBy=multi-user.target
```

2. **Cron Job** (Alternative):
```bash
# Add to crontab -e
0 2 * * * cd /path/to/ioc-collector && ./run.sh --collect >> cron.log 2>&1
```

3. **Docker** (Optional - requires Dockerfile):
```bash
docker build -t ioc-collector .
docker run -d --name ioc-collector ioc-collector
```

## Support

- Check README.md for detailed docs
- Review logs in `logs/ioc_collector.log`
- Verify configuration in `config/` directory
