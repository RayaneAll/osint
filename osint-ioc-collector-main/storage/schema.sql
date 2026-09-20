-- IOC Collector Database Schema

CREATE TABLE IF NOT EXISTS iocs (
    id TEXT PRIMARY KEY,
    ioc_value TEXT NOT NULL,
    ioc_type TEXT NOT NULL,
    threat_type TEXT,
    source TEXT NOT NULL,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    confidence_score INTEGER DEFAULT 50,
    tags TEXT,
    raw_data TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ioc_value ON iocs(ioc_value);
CREATE INDEX IF NOT EXISTS idx_source ON iocs(source);
CREATE INDEX IF NOT EXISTS idx_last_seen ON iocs(last_seen);
CREATE INDEX IF NOT EXISTS idx_is_active ON iocs(is_active);

CREATE TABLE IF NOT EXISTS collection_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    status TEXT NOT NULL,
    iocs_collected INTEGER DEFAULT 0,
    iocs_new INTEGER DEFAULT 0,
    iocs_updated INTEGER DEFAULT 0,
    execution_time REAL,
    error_message TEXT,
    timestamp TEXT NOT NULL
);
