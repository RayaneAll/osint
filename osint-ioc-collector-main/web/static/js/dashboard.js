// IOC Collector Dashboard JavaScript

let typeChart = null;
let sourceChart = null;

// Load dashboard data on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadCharts();
    loadActivity();

    // Refresh data every 30 seconds
    setInterval(() => {
        loadStats();
        loadActivity();
    }, 30000);
});

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        if (data.success) {
            const stats = data.stats;

            // Update total IOCs
            document.getElementById('total-iocs').textContent =
                formatNumber(stats.total_active_iocs);

            // Update by type
            const byType = stats.by_type || {};
            document.getElementById('total-urls').textContent =
                formatNumber(byType.url || 0);
            document.getElementById('total-hashes').textContent =
                formatNumber(byType.hash || 0);
            document.getElementById('total-ips').textContent =
                formatNumber(byType.ip || 0);
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load charts data
async function loadCharts() {
    try {
        const response = await fetch('/api/chart-data');
        const data = await response.json();

        if (data.success) {
            createTypeChart(data.data.by_type);
            createSourceChart(data.data.by_source);
        }
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

// Create type distribution chart
function createTypeChart(data) {
    const ctx = document.getElementById('typeChart');

    if (typeChart) {
        typeChart.destroy();
    }

    const labels = Object.keys(data);
    const values = Object.values(data);

    typeChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels.map(l => l.toUpperCase()),
            datasets: [{
                data: values,
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(16, 185, 129, 0.8)'
                ],
                borderColor: [
                    '#3b82f6',
                    '#8b5cf6',
                    '#f59e0b',
                    '#10b981'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#f1f5f9',
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${context.label}: ${formatNumber(value)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Create source distribution chart
function createSourceChart(data) {
    const ctx = document.getElementById('sourceChart');

    if (sourceChart) {
        sourceChart.destroy();
    }

    const labels = Object.keys(data);
    const values = Object.values(data);

    sourceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'IOCs',
                data: values,
                backgroundColor: 'rgba(59, 130, 246, 0.8)',
                borderColor: '#3b82f6',
                borderWidth: 2,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#94a3b8',
                        callback: function(value) {
                            return formatNumber(value);
                        }
                    },
                    grid: {
                        color: 'rgba(51, 65, 85, 0.5)'
                    }
                },
                x: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `IOCs: ${formatNumber(context.parsed.y)}`;
                        }
                    }
                }
            }
        }
    });
}

// Load recent activity
async function loadActivity() {
    try {
        const response = await fetch('/api/recent-activity');
        const data = await response.json();

        if (data.success) {
            displayActivity(data.activities);
        }
    } catch (error) {
        console.error('Error loading activity:', error);
    }
}

// Display activity feed
function displayActivity(activities) {
    const activityList = document.getElementById('activity-list');

    if (activities.length === 0) {
        activityList.innerHTML = `
            <p style="text-align: center; color: var(--text-secondary); padding: 2rem;">
                No recent activity
            </p>
        `;
        return;
    }

    activityList.innerHTML = activities.map(activity => {
        const isSuccess = activity.status === 'success';
        const icon = isSuccess ? 'fa-check-circle' : 'fa-exclamation-circle';
        const iconClass = isSuccess ? 'success' : 'error';

        return `
            <div class="activity-item">
                <div class="activity-icon ${iconClass}">
                    <i class="fas ${icon}"></i>
                </div>
                <div class="activity-content">
                    <div class="activity-title">
                        ${activity.source} - ${activity.status}
                    </div>
                    <div class="activity-meta">
                        ${activity.iocs_collected} collected
                        (${activity.iocs_new} new, ${activity.iocs_updated} updated)
                        • ${formatDate(activity.timestamp)}
                    </div>
                    ${activity.error_message ? `
                        <div style="color: var(--accent-red); font-size: 0.875rem; margin-top: 0.25rem;">
                            ${activity.error_message}
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

// Trigger collection
async function triggerCollection() {
    const btn = event.target.closest('button');
    const originalHTML = btn.innerHTML;

    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div> Collecting...';

    try {
        const response = await fetch('/api/collect', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showNotification('Collection started successfully!', 'success');

            // Refresh data after 10 seconds
            setTimeout(() => {
                loadStats();
                loadCharts();
                loadActivity();
            }, 10000);
        } else {
            showNotification('Collection failed: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error triggering collection:', error);
        showNotification('Failed to start collection', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalHTML;
    }
}

// Trigger export
async function triggerExport(format) {
    const btn = event.target.closest('button');
    const originalHTML = btn.innerHTML;

    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div> Exporting...';

    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ format })
        });

        const data = await response.json();

        if (data.success) {
            showNotification(`Successfully exported ${data.files.length} ${format.toUpperCase()} file(s)`, 'success');
        } else {
            showNotification('Export failed: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error triggering export:', error);
        showNotification('Failed to export data', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalHTML;
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        ${message}
    `;
    document.body.appendChild(notification);

    setTimeout(() => notification.remove(), 5000);
}

// Format number with thousands separator
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

// Format date relative to now
function formatDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);

    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`;
    if (diff < 604800) return `${Math.floor(diff / 86400)} days ago`;

    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}
