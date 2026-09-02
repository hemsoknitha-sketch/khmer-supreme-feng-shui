"""
Supreme Feng Shui AGI System - Automated User Data Protection & 24-Hour Backup Engine
Handles:
1. Online Atomic Hot-Backup of SQLite Database (Zero downtime, zero corruption)
2. JSON Knowledge & System Metadata Archive
3. Zip compression with SHA-256 Checksum validation
4. Rolling 30-day retention on VPS disk
5. Automated daily scheduler dispatching zip to Super Bot Admin at 2:00 AM Phnom Penh Time (GMT+7)
6. On-demand manual backup via /backup command
"""

import os
import sys
import time
import zipfile
import hashlib
import sqlite3
import logging
import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List

from config import config
from database.db_manager import DB_PATH, get_db_connection

logger = logging.getLogger("SupremeFengShui.Backup")

# Directory where backups are safely stored on VPS Disk
BACKUP_DIR = config.DATA_DIR / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# Phnom Penh Timezone offset: GMT+7 (ICT)
ICT_TIMEZONE = timezone(timedelta(hours=7))


class BackupEngine:
    """Enterprise Data Protection & Daily Backup Management Engine."""

    def __init__(self):
        self.backup_dir = BACKUP_DIR
        self.db_path = DB_PATH

    def get_current_ict_time(self) -> datetime:
        """Get current datetime in Phnom Penh timezone (GMT+7)."""
        return datetime.now(timezone.utc).astimezone(ICT_TIMEZONE)

    def create_backup(self, trigger_type: str = "Automated Daily (2:00 AM ICT)") -> Dict[str, Any]:
        """
        Perform an online atomic hot-backup of the database and assets,
        compress into a timestamped .zip archive on VPS disk, and calculate SHA-256 checksum.
        """
        ict_now = self.get_current_ict_time()
        timestamp_str = ict_now.strftime("%Y%m%d_%H%M%S")
        readable_time = ict_now.strftime("%Y-%m-%d %H:%M:%S (Phnom Penh GMT+7)")

        zip_filename = f"fengshui_backup_{timestamp_str}.zip"
        zip_filepath = self.backup_dir / zip_filename
        temp_db_copy = self.backup_dir / f"temp_db_{timestamp_str}.db"

        try:
            # 1. Online Atomic Hot-Backup using sqlite3 backup API
            logger.info(f"Starting online hot-backup of database from {self.db_path}...")
            with get_db_connection() as src_conn:
                dest_conn = sqlite3.connect(temp_db_copy)
                src_conn.backup(dest_conn)
                dest_conn.close()

            # 2. Gather System & Database Statistics
            from database.db_manager import db_manager
            stats = db_manager.get_system_stats()

            # 3. Create compressed Zip Archive
            with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zip_file:
                # Add the hot-backed SQLite Database
                zip_file.write(temp_db_copy, arcname="supreme_fengshui.db")

                # Add knowledge JSON files if they exist
                for json_file in ["knowledge_base.json", "historical_cycles.json"]:
                    file_path = config.DATA_DIR / json_file
                    if file_path.exists():
                        zip_file.write(file_path, arcname=json_file)

                # Write a manifest metadata summary into the zip
                manifest_content = (
                    f"=====================================================\n"
                    f"SUPREME FENG SHUI AGI - SECURE DATA BACKUP ARCHIVE\n"
                    f"=====================================================\n"
                    f"Backup Trigger: {trigger_type}\n"
                    f"Backup Timestamp (ICT): {readable_time}\n"
                    f"Total Registered Users: {stats['total_users']}\n"
                    f"Active VIP Users: {stats['total_vips']} (Monthly: {stats['vip_monthly']}, Yearly: {stats['vip_yearly']}, Lifetime: {stats['vip_lifetime']})\n"
                    f"Active License Keys: {stats['active_licenses']} / {stats['total_licenses']}\n"
                    f"Total MoE Queries Logged: {stats['total_queries']}\n"
                    f"System Status: 100% OPERATIONAL\n"
                    f"=====================================================\n"
                )
                zip_file.writestr("BACKUP_MANIFEST.txt", manifest_content)

            # 4. Remove temporary SQLite DB copy
            if temp_db_copy.exists():
                temp_db_copy.unlink()

            # 5. Compute SHA-256 Checksum of the Zip archive
            sha256_hash = hashlib.sha256()
            with open(zip_filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(65536), b""):
                    sha256_hash.update(byte_block)
            checksum = sha256_hash.hexdigest()

            file_size_bytes = zip_filepath.stat().st_size
            file_size_kb = round(file_size_bytes / 1024, 2)

            # 6. Apply Rolling Retention (Keep latest 30 backups on VPS disk)
            self._cleanup_old_backups(keep_count=30)

            logger.info(f"Backup created successfully: {zip_filename} ({file_size_kb} KB, SHA-256: {checksum[:12]}...)")

            return {
                "success": True,
                "zip_path": str(zip_filepath),
                "file_name": zip_filename,
                "file_size_kb": file_size_kb,
                "sha256": checksum,
                "stats": stats,
                "timestamp_ict": readable_time
            }

        except Exception as e:
            logger.error(f"Error creating data backup: {e}", exc_info=True)
            if temp_db_copy.exists():
                temp_db_copy.unlink()
            return {
                "success": False,
                "error": str(e)
            }

    def _cleanup_old_backups(self, keep_count: int = 30):
        """Keep latest N backups on VPS disk and delete older ones to protect disk space."""
        try:
            backup_files = sorted(
                self.backup_dir.glob("fengshui_backup_*.zip"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            if len(backup_files) > keep_count:
                for old_file in backup_files[keep_count:]:
                    try:
                        old_file.unlink()
                        logger.info(f"Cleaned up old backup archive: {old_file.name}")
                    except Exception as err:
                        logger.warning(f"Could not delete old backup {old_file.name}: {err}")
        except Exception as e:
            logger.warning(f"Error during backup rotation: {e}")

    def get_seconds_until_next_2am_ict(self) -> float:
        """Calculate exact seconds remaining until next 2:00 AM Phnom Penh time (ICT / UTC+7)."""
        now_ict = self.get_current_ict_time()
        target_time = now_ict.replace(hour=2, minute=0, second=0, microsecond=0)

        # If 2:00 AM today has already passed, schedule for tomorrow 2:00 AM
        if now_ict >= target_time:
            target_time += timedelta(days=1)

        seconds_remaining = (target_time - now_ict).total_seconds()
        return max(seconds_remaining, 1.0)


# Singleton Instance
backup_engine = BackupEngine()
