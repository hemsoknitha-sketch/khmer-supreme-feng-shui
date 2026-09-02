"""
Supreme Feng Shui AGI System - Database & VIP License Manager
Ultra-lightweight SQLite Database Engine optimized for 1GB VPS RAM.
Manages Users, Roles, VIP Tiers (Monthly, Yearly, Lifetime),
License Key Generation & Redemption, and Super Admin Management.
"""

import sqlite3
import logging
import secrets
import string
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from config import config

logger = logging.getLogger("SupremeFengShui.Database")

# Ensure data directory exists
config.DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = config.DATA_DIR / "supreme_fengshui.db"


def get_db_connection() -> sqlite3.Connection:
    """Get optimized SQLite connection with row factory."""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")  # Write-Ahead Logging for high concurrency
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


class DatabaseManager:
    """Central Database & License Management Engine."""

    def __init__(self):
        self.init_db()

    def init_db(self):
        """Initialize database tables and indexes."""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                # 1. Users Table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    role TEXT DEFAULT 'user', -- 'user', 'vip_monthly', 'vip_yearly', 'vip_lifetime', 'super_admin'
                    vip_tier TEXT DEFAULT 'free', -- 'free', 'monthly', 'yearly', 'lifetime', 'admin'
                    vip_expiry TEXT, -- ISO DateTime string or NULL
                    daily_queries_count INTEGER DEFAULT 0,
                    last_query_date TEXT, -- YYYY-MM-DD
                    total_queries INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """)

                # 2. Licenses Table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS licenses (
                    key TEXT PRIMARY KEY,
                    tier TEXT NOT NULL, -- 'monthly', 'yearly', 'lifetime'
                    duration_days INTEGER NOT NULL,
                    created_by INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    is_redeemed INTEGER DEFAULT 0,
                    redeemed_by INTEGER,
                    redeemed_at TEXT,
                    notes TEXT
                );
                """)

                # 3. System Logs Table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    created_at TEXT NOT NULL
                );
                """)

                # 4. System Settings Table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """)

                # Migrations: Ensure birth_date, birth_time, gender, timezone, utc_offset, alert tracking columns exist
                for col_def in [
                    ("birth_date", "TEXT"),
                    ("birth_time", "TEXT DEFAULT '12:00'"),
                    ("gender", "TEXT DEFAULT 'male'"),
                    ("timezone", "TEXT DEFAULT 'Asia/Phnom_Penh'"),
                    ("utc_offset", "REAL DEFAULT 7.0"),
                    ("last_daily_alert_date", "TEXT"),
                    ("last_monthly_alert_month", "TEXT"),
                    ("last_yearly_alert_year", "TEXT")
                ]:
                    try:
                        cursor.execute(f"ALTER TABLE users ADD COLUMN {col_def[0]} {col_def[1]};")
                    except Exception:
                        pass

                # Indexes
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_vip_expiry ON users(vip_expiry);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_licenses_redeemed ON licenses(is_redeemed);")

                conn.commit()
                logger.info(f"Database initialized successfully at {DB_PATH}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")

    def get_or_create_user(self, telegram_id: int, username: str = "", full_name: str = "") -> Dict[str, Any]:
        """Fetch user or create new one. Automatically honors configured Super Admin IDs."""
        now_str = datetime.utcnow().isoformat()
        today_str = datetime.utcnow().strftime("%Y-%m-%d")

        # Check if user is in config or default super admins
        admin_ids = getattr(config, "ADMIN_USER_IDS", [])
        is_default_admin = telegram_id in admin_ids

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
                row = cursor.fetchone()

                if row:
                    user = dict(row)

                    # Auto-promote to super_admin if configured in ADMIN_USER_IDS
                    if is_default_admin and user["role"] != "super_admin":
                        cursor.execute("""
                            UPDATE users SET role = 'super_admin', vip_tier = 'admin', updated_at = ?
                            WHERE telegram_id = ?
                        """, (now_str, telegram_id))
                        conn.commit()
                        user["role"] = "super_admin"
                        user["vip_tier"] = "admin"

                    # Check VIP expiration
                    if user["vip_expiry"]:
                        try:
                            expiry = datetime.fromisoformat(user["vip_expiry"])
                            if expiry < datetime.utcnow() and user["role"] not in ("super_admin", "vip_lifetime"):
                                # Expired, revert to free
                                cursor.execute("""
                                    UPDATE users SET role = 'user', vip_tier = 'free', updated_at = ?
                                    WHERE telegram_id = ?
                                """, (now_str, telegram_id))
                                conn.commit()
                                user["role"] = "user"
                                user["vip_tier"] = "free"
                        except Exception as e:
                            logger.error(f"Date parse error for user {telegram_id}: {e}")

                    # Update username/name if changed
                    if user["username"] != username or user["full_name"] != full_name:
                        cursor.execute("""
                            UPDATE users SET username = ?, full_name = ?, updated_at = ?
                            WHERE telegram_id = ?
                        """, (username, full_name, now_str, telegram_id))
                        conn.commit()
                        user["username"] = username
                        user["full_name"] = full_name

                    user["is_new_user"] = False
                    return user
                else:
                    # Create new user
                    role = "super_admin" if is_default_admin else "user"
                    vip_tier = "admin" if is_default_admin else "free"
                    vip_expiry = None if not is_default_admin else (datetime.utcnow() + timedelta(days=36500)).isoformat()

                    cursor.execute("""
                        INSERT INTO users (
                            telegram_id, username, full_name, role, vip_tier, vip_expiry,
                            daily_queries_count, last_query_date, total_queries, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, 0, ?, 0, ?, ?)
                    """, (telegram_id, username, full_name, role, vip_tier, vip_expiry, today_str, now_str, now_str))
                    conn.commit()

                    return {
                        "telegram_id": telegram_id,
                        "username": username,
                        "full_name": full_name,
                        "role": role,
                        "vip_tier": vip_tier,
                        "vip_expiry": vip_expiry,
                        "daily_queries_count": 0,
                        "last_query_date": today_str,
                        "total_queries": 0,
                        "created_at": now_str,
                        "updated_at": now_str,
                        "is_new_user": True
                    }
        except Exception as e:
            logger.error(f"Error in get_or_create_user: {e}")
            return {
                "telegram_id": telegram_id,
                "username": username,
                "full_name": full_name,
                "role": "super_admin" if is_default_admin else "user",
                "vip_tier": "admin" if is_default_admin else "free",
                "vip_expiry": None
            }

    def generate_license_key(self, tier: str = "monthly", count: int = 1, created_by: int = 0, notes: str = "") -> List[str]:
        """
        Generate cryptographic unique license keys.
        Tiers: 'monthly' (30 days), 'yearly' (365 days), 'lifetime' (36500 days).
        Format: FS-M-XXXX-XXXX, FS-Y-XXXX-XXXX, FS-L-XXXX-XXXX
        """
        tier = tier.lower()
        if tier == "monthly":
            prefix = "FS-M"
            duration = 30
        elif tier == "yearly":
            prefix = "FS-Y"
            duration = 365
        elif tier == "lifetime":
            prefix = "FS-L"
            duration = 36500
        else:
            prefix = "FS-V"
            duration = 30
            tier = "monthly"

        alphabet = string.ascii_uppercase + string.digits
        generated_keys = []
        now_str = datetime.utcnow().isoformat()

        with get_db_connection() as conn:
            cursor = conn.cursor()
            for _ in range(count):
                part1 = "".join(secrets.choice(alphabet) for _ in range(4))
                part2 = "".join(secrets.choice(alphabet) for _ in range(4))
                key = f"{prefix}-{part1}-{part2}"

                cursor.execute("""
                    INSERT OR REPLACE INTO licenses (
                        key, tier, duration_days, created_by, created_at, is_redeemed, notes
                    ) VALUES (?, ?, ?, ?, ?, 0, ?)
                """, (key, tier, duration, created_by, now_str, notes))
                generated_keys.append(key)

            conn.commit()

        logger.info(f"Generated {count} {tier} license keys by Admin {created_by}")
        return generated_keys

    def redeem_license(self, telegram_id: int, key: str) -> Dict[str, Any]:
        """
        Redeem license key for a user and extend/activate their VIP status.
        """
        key = key.strip().upper()
        now = datetime.utcnow()
        now_str = now.isoformat()

        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check key
            cursor.execute("SELECT * FROM licenses WHERE key = ?", (key,))
            license_row = cursor.fetchone()

            if not license_row:
                return {"success": False, "error": "❌ លេខកូដអាជ្ញាប័ណ្ណ (License Key) មិនត្រឹមត្រូវឡើយ។"}

            lic = dict(license_row)
            if lic["is_redeemed"]:
                return {
                    "success": False,
                    "error": f"❌ លេខកូដអាជ្ញាប័ណ្ណនេះត្រូវបានប្រើប្រាស់រួចហើយ នៅថ្ងៃ {lic.get('redeemed_at', '')[:10]}។"
                }

            # Fetch user
            cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
            user_row = cursor.fetchone()
            if not user_row:
                self.get_or_create_user(telegram_id)
                cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
                user_row = cursor.fetchone()

            user = dict(user_row)
            tier = lic["tier"]
            duration_days = lic["duration_days"]

            # Calculate new expiration
            current_expiry = user.get("vip_expiry")
            if current_expiry and user.get("vip_tier") != "free":
                try:
                    exp_dt = datetime.fromisoformat(current_expiry)
                    if exp_dt > now:
                        new_expiry_dt = exp_dt + timedelta(days=duration_days)
                    else:
                        new_expiry_dt = now + timedelta(days=duration_days)
                except Exception:
                    new_expiry_dt = now + timedelta(days=duration_days)
            else:
                new_expiry_dt = now + timedelta(days=duration_days)

            new_expiry_str = new_expiry_dt.isoformat()
            new_role = f"vip_{tier}" if user["role"] != "super_admin" else "super_admin"
            new_vip_tier = tier if user["role"] != "super_admin" else "admin"

            # Mark license as redeemed
            cursor.execute("""
                UPDATE licenses SET is_redeemed = 1, redeemed_by = ?, redeemed_at = ?
                WHERE key = ?
            """, (telegram_id, now_str, key))

            # Update user
            cursor.execute("""
                UPDATE users SET role = ?, vip_tier = ?, vip_expiry = ?, updated_at = ?
                WHERE telegram_id = ?
            """, (new_role, new_vip_tier, new_expiry_str, now_str, telegram_id))

            # Log
            cursor.execute("""
                INSERT INTO system_logs (telegram_id, action, details, created_at)
                VALUES (?, 'REDEEM_LICENSE', ?, ?)
            """, (telegram_id, f"Redeemed {key} for tier {tier} ({duration_days} days)", now_str))

            conn.commit()

        tier_name_kh = {
            "monthly": "🌟 VIP ប្រចាំខែ (Monthly VIP - 30 ថ្ងៃ)",
            "yearly": "👑 VIP ប្រចាំឆ្នាំ (Yearly VIP - 365 ថ្ងៃ)",
            "lifetime": "💎 VIP មួយជីវិត (Lifetime VIP)"
        }.get(tier, "VIP")

        return {
            "success": True,
            "tier": tier,
            "tier_name_kh": tier_name_kh,
            "expiry_date": new_expiry_dt.strftime("%Y-%m-%d %H:%M UTC"),
            "days_added": duration_days
        }

    def set_user_vip_manually(self, telegram_id: int, tier: str, admin_id: int = 0) -> Dict[str, Any]:
        """Manually grant or revoke VIP status by Admin."""
        tier = tier.lower()
        now = datetime.utcnow()
        now_str = now.isoformat()

        if tier == "revoke" or tier == "free":
            role = "user"
            vip_tier = "free"
            expiry_str = None
        elif tier == "monthly":
            role = "vip_monthly"
            vip_tier = "monthly"
            expiry_str = (now + timedelta(days=30)).isoformat()
        elif tier == "yearly":
            role = "vip_yearly"
            vip_tier = "yearly"
            expiry_str = (now + timedelta(days=365)).isoformat()
        elif tier == "lifetime":
            role = "vip_lifetime"
            vip_tier = "lifetime"
            expiry_str = (now + timedelta(days=36500)).isoformat()
        elif tier == "admin" or tier == "super_admin":
            role = "super_admin"
            vip_tier = "admin"
            expiry_str = (now + timedelta(days=36500)).isoformat()
        else:
            return {"success": False, "error": f"Invalid tier: {tier}"}

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
            if not cursor.fetchone():
                self.get_or_create_user(telegram_id)

            cursor.execute("""
                UPDATE users SET role = ?, vip_tier = ?, vip_expiry = ?, updated_at = ?
                WHERE telegram_id = ?
            """, (role, vip_tier, expiry_str, now_str, telegram_id))

            cursor.execute("""
                INSERT INTO system_logs (telegram_id, action, details, created_at)
                VALUES (?, 'MANUAL_VIP_SET', ?, ?)
            """, (telegram_id, f"Admin {admin_id} set tier to {tier}", now_str))

            conn.commit()

        return {"success": True, "telegram_id": telegram_id, "role": role, "vip_tier": vip_tier, "expiry": expiry_str}

    def check_and_increment_query(self, telegram_id: int, max_free_limit: int = 0) -> Dict[str, Any]:
        """
        Check if user has permission to make query.
        ONLY VIP & Super Admin users have permission to use the system.
        Unactivated/Free users are strictly gated and directed to contact Admin @HemSinath.
        """
        user = self.get_or_create_user(telegram_id)
        is_vip = user["role"] in ("vip_monthly", "vip_yearly", "vip_lifetime", "super_admin") or user["vip_tier"] in ("monthly", "yearly", "lifetime", "admin")

        if is_vip:
            # VIP & Admin unlimited
            with get_db_connection() as conn:
                conn.execute("UPDATE users SET total_queries = total_queries + 1 WHERE telegram_id = ?", (telegram_id,))
                conn.commit()
            return {"allowed": True, "is_vip": True, "remaining": "∞ (Unlimited VIP)", "tier": user["vip_tier"]}

        # Free tier is strictly locked (0 free queries)
        lock_message = (
            "🔒 **មុខងារនេះត្រូវបានរក្សាសិទ្ធិសម្រាប់តែសមាជិក VIP & SUPER ADMIN ប៉ុណ្ណោះ!** 🔒\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🌟 **SUPREME FENG SHUI AGI SYSTEM (Master Level v1.0.0)** 🌟\n\n"
            "ដើម្បីប្រើប្រាស់ប្រព័ន្ធបញ្ញាសិប្បនិម្មិតហុងស៊ុយបុរាណ ចូលរៀន ១,០០០ មេរៀន គណនាជោគជតា ស្កេនរូបភាព និងបង្កើតប្លង់ 3D 4K សូមភ្ជាប់សេវាកម្ម VIP ជាមុនសិន។\n\n"
            "💎 **អត្ថប្រយោជន៍សមាជិកភាព VIP:**\n"
            "• 🧠 សួរគ្រូហុងស៊ុយ AI គ្មានដែនកំណត់ ២៤/៧/៣៦៥\n"
            "• 📚 កម្មវិធីសិក្សា ១០០ ប្រធានបទ & ១០០០ មេរៀនស៊ីជម្រៅ\n"
            "• 🧭 គណនា Life Gua, តារាហោះ យុគ ៩, BaZi ៤ សសរ & ១០ Gods\n"
            "• 📸 ស្កេនពិនិត្យរូបភាពបន្ទប់/ផ្ទះរក Sha Qi & វិធីកែខៃ\n"
            "• 🎨 បង្កើតប្លង់ហុងស៊ុយ 3D 4K Photorealistic\n\n"
            "👉 **សូមទាក់ទងមកកាន់ SUPER ADMIN ផ្ទាល់ដើម្បីភ្ជាប់សេវាកម្ម VIP ភ្លាមៗ:**\n"
            "👤 **Telegram Admin:** [@HemSinath](https://t.me/HemSinath)\n\n"
            "🎟️ *(ប្រសិនបើលោកអ្នកមាន Key អាជ្ញាប័ណ្ណរួចហើយ សូមវាយ `/redeem <Key>` ឧទាហរណ៍ `/redeem FS-M-XXXX-XXXX`)*"
        )

        return {
            "allowed": False,
            "is_vip": False,
            "remaining": 0,
            "tier": "free",
            "message": lock_message
        }

        remaining = max_free_limit - (daily_count + 1)
        return {"allowed": True, "is_vip": False, "remaining": remaining, "tier": "free"}

    def get_system_stats(self) -> Dict[str, Any]:
        """Get aggregate system and VIP user statistics."""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM users;")
            total_users = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'super_admin';")
            total_admins = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'vip_monthly' OR vip_tier = 'monthly';")
            vip_monthly = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'vip_yearly' OR vip_tier = 'yearly';")
            vip_yearly = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'vip_lifetime' OR vip_tier = 'lifetime';")
            vip_lifetime = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM licenses;")
            total_licenses = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM licenses WHERE is_redeemed = 1;")
            redeemed_licenses = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM licenses WHERE is_redeemed = 0;")
            active_licenses = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(total_queries) FROM users;")
            total_queries_row = cursor.fetchone()[0]
            total_queries = total_queries_row if total_queries_row else 0

        total_vips = vip_monthly + vip_yearly + vip_lifetime
        return {
            "total_users": total_users,
            "total_admins": total_admins,
            "total_vips": total_vips,
            "vip_monthly": vip_monthly,
            "vip_yearly": vip_yearly,
            "vip_lifetime": vip_lifetime,
            "total_licenses": total_licenses,
            "redeemed_licenses": redeemed_licenses,
            "active_licenses": active_licenses,
            "total_queries": total_queries
        }

    def get_unredeemed_keys(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get list of unredeemed license keys."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT key, tier, duration_days, created_at, notes
                FROM licenses WHERE is_redeemed = 0
                ORDER BY created_at DESC LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_all_users_list(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get list of users with roles."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT telegram_id, username, full_name, role, vip_tier, vip_expiry, total_queries, created_at, birth_date, birth_time, gender
                FROM users ORDER BY updated_at DESC LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def set_user_birth_profile(self, telegram_id: int, birth_date: str, birth_time: str = "12:00", gender: str = "male") -> bool:
        """Save or update user's birth profile for Celestial Astrology."""
        now = datetime.utcnow().isoformat()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users
                SET birth_date = ?, birth_time = ?, gender = ?, updated_at = ?
                WHERE telegram_id = ?;
            """, (birth_date.strip(), birth_time.strip(), gender.strip().lower(), now, telegram_id))
            conn.commit()
            return cursor.rowcount > 0

    def set_user_timezone(self, telegram_id: int, timezone_name: str, utc_offset: float) -> bool:
        """Save user's real-world timezone and UTC offset for localized 5:00 AM alerts."""
        now = datetime.utcnow().isoformat()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users
                SET timezone = ?, utc_offset = ?, updated_at = ?
                WHERE telegram_id = ?;
            """, (timezone_name.strip(), float(utc_offset), now, telegram_id))
            conn.commit()
            return cursor.rowcount > 0

    def update_user_alert_dispatch(self, telegram_id: int, alert_type: str, date_key: str):
        """Update last dispatched alert date/month/year to prevent duplicate delivery."""
        col_map = {
            "daily": "last_daily_alert_date",
            "monthly": "last_monthly_alert_month",
            "yearly": "last_yearly_alert_year"
        }
        col = col_map.get(alert_type, "last_daily_alert_date")
        now = datetime.utcnow().isoformat()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE users
                SET {col} = ?, updated_at = ?
                WHERE telegram_id = ?;
            """, (date_key, now, telegram_id))
            conn.commit()

    def get_active_vip_users_with_birth_profiles(self) -> List[Dict[str, Any]]:
        """Fetch all active VIP users and admins with their birth and timezone profiles."""
        now = datetime.utcnow().isoformat()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT telegram_id, username, full_name, role, vip_tier, vip_expiry, birth_date, birth_time, gender,
                       COALESCE(timezone, 'Asia/Phnom_Penh') as timezone,
                       COALESCE(utc_offset, 7.0) as utc_offset,
                       last_daily_alert_date, last_monthly_alert_month, last_yearly_alert_year
                FROM users
                WHERE (role IN ('super_admin', 'vip_monthly', 'vip_yearly', 'vip_lifetime')
                   OR vip_tier IN ('admin', 'monthly', 'yearly', 'lifetime')
                   OR (vip_expiry IS NOT NULL AND vip_expiry > ?));
            """, (now,))
            return [dict(row) for row in cursor.fetchall()]


# Global Singleton Instance
db_manager = DatabaseManager()
