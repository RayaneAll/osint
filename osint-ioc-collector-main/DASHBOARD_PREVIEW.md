# 📊 Dashboard Preview

## Interface Visuelle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  🛡️  IOC COLLECTOR DASHBOARD                          v1.0.0               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────────────────────────────────────────────────┐
│              │  │                                                          │
│  NAVIGATION  │  │  📊 DASHBOARD                                            │
│              │  │  Overview of your IOC collection                         │
│  Dashboard   │  │                                                          │
│  IOCs List   │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│              │  │  │   Actions   │  │             │  │             │      │
│              │  │  │ 🔄 Collect  │  │ 📄 Export   │  │ 📋 Export   │      │
│              │  │  │     Now     │  │     CSV     │  │     JSON    │      │
│              │  │  └─────────────┘  └─────────────┘  └─────────────┘      │
│              │  │                                                          │
│              │  │  ┌─────────────────────────────────────────────────────┐│
│              │  │  │        STATISTICS                                   ││
│              │  │  │                                                     ││
│              │  │  │  💾 Total IOCs    🔗 URLs      🔐 Hashes  🌐 IPs  ││
│              │  │  │     17,545       12,858        2,970      1,717   ││
│              │  │  └─────────────────────────────────────────────────────┘│
│              │  │                                                          │
│              │  │  ┌──────────────────────┐  ┌──────────────────────────┐│
│              │  │  │  IOCs by Type        │  │  IOCs by Source          ││
│              │  │  │                      │  │                          ││
│              │  │  │     ┌────────┐      │  │  URLhaus        ████████ ││
│              │  │  │     │  URL   │      │  │  MalwareBazaar  ███      ││
│              │  │  │     │  73.3% │      │  │  Spamhaus       ██       ││
│              │  │  │     │ Hash   │      │  │  Feodo          █        ││
│              │  │  │     │  16.9% │      │  │                          ││
│              │  │  │     └────────┘      │  └──────────────────────────┘│
│              │  │  └──────────────────────┘                              │
│              │  │                                                          │
│              │  │  ┌──────────────────────────────────────────────────────┐│
│              │  │  │  📋 RECENT ACTIVITY                                  ││
│              │  │  │                                                      ││
│              │  │  │  ✅ urlhaus - success                                ││
│              │  │  │     12,858 collected (234 new) • 5 minutes ago      ││
│              │  │  │                                                      ││
│              │  │  │  ✅ malwarebazaar - success                          ││
│              │  │  │     2,970 collected (45 new) • 5 minutes ago        ││
│              │  │  │                                                      ││
│              │  │  │  ✅ spamhaus_drop - success                          ││
│              │  │  │     1,712 collected (0 new) • 5 minutes ago         ││
│              │  │  └──────────────────────────────────────────────────────┘│
│              │  │                                                          │
└──────────────┘  └──────────────────────────────────────────────────────────┘
```

## IOCs List Page

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  📋 IOCs LIST                                                               │
│  Browse and filter collected indicators                                     │
│                                                                             │
│  Filters: [All Types ▼]  [All Sources ▼]                                  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │ IOC Value                        Type    Source    Score  Last Seen   │ │
│  ├───────────────────────────────────────────────────────────────────────┤ │
│  │ http://221.15.255.59:52731/i     [URL]  urlhaus    65    2h ago      │ │
│  │ 094dc09e40da906ed6c4b6ad...      [HASH] malware    65    3h ago      │ │
│  │ 223.254.0.0/16                   [IP]   spamhaus   65    1d ago      │ │
│  │ 162.243.103.246                  [IP]   feodo      65    6h ago      │ │
│  │ http://222.140.159.192:4808...   [URL]  urlhaus    65    2h ago      │ │
│  │ ...                              ...    ...        ...   ...          │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ◄ Previous    Page 1 of 351    Next ►                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Color Scheme (Dark Theme)

```
🎨 Color Palette:

Background:    #0f172a  ████  (Primary - Very Dark Blue)
Cards:         #1e293b  ████  (Secondary - Dark Blue)
Borders:       #334155  ████  (Tertiary - Medium Dark)

Text Primary:  #f1f5f9  ████  (Off-White)
Text Secondary:#94a3b8  ████  (Light Gray)

Accent Blue:   #3b82f6  ████  (Primary Actions)
Accent Green:  #10b981  ████  (Success)
Accent Yellow: #f59e0b  ████  (Warning/Hashes)
Accent Purple: #8b5cf6  ████  (URLs)
Accent Red:    #ef4444  ████  (Errors)
```

## Features Showcase

### Real-time Statistics
```
┌──────────────────────┐
│ 💾 Total Active IOCs │
│                      │
│      17,545          │
│                      │
│ ▲ +234 today         │
└──────────────────────┘
```

### Interactive Charts
```
Donut Chart (IOCs by Type):
        URL 73.3%
       Hash 16.9%
         IP 9.8%

Bar Chart (IOCs by Source):
URLhaus        ████████████████ 12,858
MalwareBazaar  ████              2,970
Spamhaus       ███               1,712
Feodo          █                     5
```

### Action Buttons
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  🔄 Collect Now │  │  📄 Export CSV  │  │  📋 Export JSON │
└─────────────────┘  └─────────────────┘  └─────────────────┘
   Primary Action      Secondary Action    Secondary Action
```

### Activity Feed
```
┌─────────────────────────────────────────┐
│ ✅ urlhaus - success                    │
│    12,858 collected (234 new, 12,624   │
│    updated) • 5 minutes ago             │
├─────────────────────────────────────────┤
│ ✅ malwarebazaar - success              │
│    2,970 collected (45 new, 2,925      │
│    updated) • 5 minutes ago             │
├─────────────────────────────────────────┤
│ ❌ spamhaus_drop - failed               │
│    0 collected                          │
│    Error: Connection timeout            │
│    • 10 minutes ago                     │
└─────────────────────────────────────────┘
```

### Notifications
```
┌────────────────────────────────────┐
│ ✅ Collection started successfully! │
└────────────────────────────────────┘
     (Auto-dismiss after 5 seconds)

┌────────────────────────────────────┐
│ ❌ Failed to export data            │
└────────────────────────────────────┘
```

## Responsive Design

### Desktop (1920x1080)
- Full sidebar visible
- 4-column stats grid
- 2-column charts grid
- Wide table with all columns

### Tablet (768x1024)
- Collapsible sidebar
- 2-column stats grid
- Single column charts
- Scrollable table

### Mobile (375x667)
- Hidden sidebar (burger menu)
- Single column stats
- Stacked charts
- Compact table (essential columns only)

## Technology Stack

```
Frontend:
├── HTML5
├── CSS3 (Custom Variables)
├── JavaScript (Vanilla)
├── Chart.js 4.4.0
└── Font Awesome 6.4.0

Backend:
├── Python 3.9+
├── Flask 3.0.0
├── SQLite 3
└── Threading (Async ops)

Design:
├── Dark Theme
├── Responsive Grid
├── Flexbox Layout
└── CSS Animations
```

## Browser Compatibility

✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+

## Performance

```
Initial Load:     < 500ms
Data Refresh:     < 100ms
Chart Rendering:  < 200ms
Table Pagination: < 50ms
Export Operation: < 2s
```

## Accessibility

- ✅ Semantic HTML5
- ✅ ARIA labels
- ✅ Keyboard navigation
- ✅ High contrast ratios
- ✅ Screen reader friendly

## API Rate Limits

- Stats endpoint: No limit (cached)
- IOCs list: 1000 items max per request
- Collection: 1 concurrent operation
- Export: Synchronous (no queue)

---

**Dashboard Version**: 1.0.0
**Release Date**: 2026-09-18
**Status**: Production Ready ✅
