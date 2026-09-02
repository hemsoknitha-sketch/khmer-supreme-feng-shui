#!/usr/bin/env bash
# ==============================================================================
# Supreme Feng Shui AGI System - Automated 24-Hour Backup & Disaster Recovery Setup
# Schedules a daily cron at 2:00 AM Phnom Penh Time (GMT+7 = 19:00 UTC)
# ==============================================================================

set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_EXEC="${APP_DIR}/venv/bin/python"

if [ ! -f "$PYTHON_EXEC" ]; then
    PYTHON_EXEC="$(which python3)"
fi

echo "=================================================================="
echo "⚡ Setting up Automated Daily 24-Hour Backup Cronjob (2:00 AM ICT)..."
echo "📁 Application Directory: ${APP_DIR}"
echo "🐍 Python Interpreter: ${PYTHON_EXEC}"
echo "=================================================================="

# Ensure backup directory exists on VPS Disk
mkdir -p "${APP_DIR}/data/backups"
chmod 700 "${APP_DIR}/data/backups"

# 2:00 AM Phnom Penh (UTC+7) corresponds to 19:00 UTC
# Cron schedule: 0 19 * * * (Every day at 19:00 UTC / 2:00 AM ICT)
BACKUP_SCRIPT="${APP_DIR}/deploy/run_backup_now.sh"

cat << 'EOF' > "${BACKUP_SCRIPT}"
#!/usr/bin/env bash
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_EXEC="${APP_DIR}/venv/bin/python"
if [ ! -f "$PYTHON_EXEC" ]; then
    PYTHON_EXEC="$(which python3)"
fi

cd "$APP_DIR"
$PYTHON_EXEC -c "
from engines.backup_engine import backup_engine
res = backup_engine.create_backup(trigger_type='Linux Cron Automated 2:00 AM ICT')
print('Daily Backup Result:', res['success'], res.get('file_name'), res.get('file_size_kb'), 'KB')
" >> "${APP_DIR}/data/backups/backup_cron.log" 2>&1
EOF

chmod +x "${BACKUP_SCRIPT}"

# Install Cronjob for current user if not already present
CRON_CMD="0 19 * * * ${BACKUP_SCRIPT}"
(crontab -l 2>/dev/null | grep -v "run_backup_now.sh" || true; echo "${CRON_CMD}") | crontab -

echo "✅ Automated 24-Hour Backup Cronjob installed successfully!"
echo "⏱️ Scheduled Time: Everyday at 02:00 AM Phnom Penh Time (ICT GMT+7 / 19:00 UTC)"
echo "💾 Storage Location on VPS Disk: ${APP_DIR}/data/backups/"
echo "=================================================================="
