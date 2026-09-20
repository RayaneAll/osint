# 🚀 IOC Collector - Start Here

Welcome to the OSINT IOC Collector! This document will help you get started quickly.

## What is This?

An automated system that collects Indicators of Compromise (IOCs) from 4 major public threat intelligence feeds:
- **Feodo Tracker**: Botnet C2 servers
- **URLhaus**: Malicious URLs
- **MalwareBazaar**: Malware file hashes
- **Spamhaus DROP**: Spam source networks

## Quick Start (3 Steps)

### 1. Install Dependencies
```bash
cd /Users/ademmedjahed/Project/ioc-collector
pip3 install -r requirements.txt
```

### 2. Initialize Database
```bash
./run.sh --init
```

### 3. Collect IOCs
```bash
./run.sh --collect
```

**That's it!** You should see thousands of IOCs collected.

## What Can I Do?

### View Statistics
```bash
./run.sh --stats
```
Shows IOC counts by type and source.

### Export Data
```bash
./run.sh --export
```
Creates CSV and JSON files in `data/exports/`

### Automate Daily Collection
```bash
./run.sh --schedule
```
Runs continuously, collecting at 02:00 AM daily.

## Where is Everything?

```
📁 data/
  └── ioc.db              ← Your IOC database
  └── exports/            ← CSV/JSON exports

📁 logs/
  └── ioc_collector.log   ← Execution logs

📁 config/
  └── settings.json       ← Configure here
  └── feeds.json          ← Enable/disable feeds
```

## Read More

- **QUICKSTART.md** - Detailed quick start guide
- **README.md** - Complete documentation
- **DEMO_RESULTS.md** - Real test results (17k+ IOCs)
- **PROJECT_SUMMARY.md** - Technical overview

## Current Status

✅ **System is ready!** A test collection has already been run:
- **17,545 IOCs collected**
- All 4 feeds working
- Exports generated
- Tests passed

## Need Help?

1. Check the logs: `tail -f logs/ioc_collector.log`
2. Read QUICKSTART.md for troubleshooting
3. Run tests: `python3 test_system.py`

## Examples

### Daily Use
```bash
# Morning routine: check what's new
./run.sh --collect
./run.sh --stats
./run.sh --export

# Check the exports
ls -lh data/exports/
```

### Production Setup
```bash
# Set it and forget it
nohup ./run.sh --schedule > scheduler.log 2>&1 &

# Check it's running
ps aux | grep "python3 main.py"
```

### Integration
```bash
# Export to CSV for your SIEM
./run.sh --export

# Feed the data into your tools
cat data/exports/iocs_full_*.csv | your-tool
```

## Configuration

Edit `config/settings.json` to change:
- Collection schedule (default: 02:00)
- Retention policy (default: 30 days)
- Export formats
- Logging level

## Requirements

- Python 3.7+
- Internet connection
- ~100MB disk space

That's all you need!

---

**🎉 You're all set!** Start with `./run.sh --collect` and explore from there.

For detailed documentation, see README.md
