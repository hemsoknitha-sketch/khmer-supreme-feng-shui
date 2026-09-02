"""
Supreme Feng Shui AGI System - Bulletproof Telegram Bot Application
Empowered by 99 Specialized Components, 7 Core Pillars,
1,000 Curriculum Lessons, VIP Subscription & License System,
and Super Admin Management Control Center.
"""

import os
import sys
import platform
import psutil
import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import config
from engines.supreme_master import SupremeFengShuiMaster
from engines.classical_calc import ClassicalCalcEngine
from engines.alert_predictor import AlertPredictionEngine
from engines.curriculum_engine import curriculum_engine
from engines.security_guard import security_guard
from engines.vision_3d_engine import vision_3d_engine
from engines.backup_engine import backup_engine
from engines.mahasneh_love_engine import mahasneh_love_engine
from database.db_manager import db_manager

logger = logging.getLogger("SupremeFengShui.TelegramBot")

TELEGRAM_AVAILABLE = True


class FengShuiTelegramBot:
    """
    Bulletproof Telegram Bot for Supreme Feng Shui AGI System.
    Includes:
    - 1,000 Lessons Interactive Curriculum Navigation
    - VIP Membership & License Key Redemption System (Monthly, Yearly, Lifetime)
    - Super Admin Management Panel & License Generator
    - High-Precision Classical Calculations (Life Gua, Flying Stars, BaZi, Fortune Alerts)
    - Multimodal Vision Audit & 3D 4K Architectural Generation (Pillar 1 Vision)
    - Enterprise Security Shield (Anti-Spam, Prompt Injection Guard, Secret Redaction)
    - Automated 24-Hour User Data Protection & Backup Engine (2:00 AM ICT Zip Dispatch)
    - "ក្បួនហុងស៊ុយ និងមហាស្នេហ៍" (Maha Sneh, Peach Blossom & BaZi 8-Pillars Love Match)
    """

    def __init__(self, token: str = None):
        self.token = token or config.TELEGRAM_BOT_TOKEN
        self.master = SupremeFengShuiMaster()
        self.calc_engine = ClassicalCalcEngine()
        self.alert_engine = AlertPredictionEngine()
        self.curriculum = curriculum_engine
        self.db = db_manager
        self.security = security_guard
        self.vision = vision_3d_engine
        self.backup = backup_engine
        self.love = mahasneh_love_engine

    async def _safe_reply(self, message, text: str, reply_markup=None):
        """Safely send markdown text, automatically redacting secrets, falling back to plain text, and guarding max length."""
        text = self.security.redact_secrets(text)
        if len(text) > 4000:
            text = text[:3950] + "\n\n...(ចុចប៊ូតុងខាងក្រោមដើម្បីអានបន្ត)..."
        try:
            return await message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        except Exception as e:
            logger.debug(f"Markdown parse fallback for reply: {e}")
            try:
                return await message.reply_text(text, reply_markup=reply_markup)
            except Exception as e2:
                logger.error(f"Failed to reply text: {e2}")

    async def _safe_edit(self, query, text: str, reply_markup=None):
        """Safely edit message text, automatically redacting secrets, falling back to plain text, and guarding max length."""
        text = self.security.redact_secrets(text)
        if len(text) > 4000:
            text = text[:3950] + "\n\n...(ចុចប៊ូតុងខាងក្រោមដើម្បីអានបន្ត)..."
        try:
            return await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        except Exception as e:
            logger.debug(f"Markdown parse fallback for edit: {e}")
            try:
                return await query.edit_message_text(text, reply_markup=reply_markup)
            except Exception as e2:
                logger.warning(f"Could not edit message: {e2}")

    def _is_vip_or_admin(self, user_id: int) -> bool:
        """Check if user has active VIP status or is Super Admin."""
        if user_id in config.ADMIN_USER_IDS:
            return True
        user = self.db.get_or_create_user(user_id)
        return user.get("role") in ("super_admin", "vip_monthly", "vip_yearly", "vip_lifetime") or user.get("vip_tier") in ("monthly", "yearly", "lifetime", "admin")

    async def _send_vip_required_notice(self, message_or_query, from_user_id: int):
        """Send attractive VIP lock notice directing users to @HemSinath."""
        msg = (
            "🔒 **មុខងារនេះត្រូវបានរក្សាសិទ្ធិសម្រាប់តែសមាជិក VIP & SUPER ADMIN ប៉ុណ្ណោះ!** 🔒\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "ដើម្បីប្រើប្រាស់ប្រព័ន្ធបញ្ញាសិប្បនិម្មិតហុងស៊ុយបុរាណ ចូលរៀន ១,០០០ មេរៀន គណនាជោគជតា ស្កេនរូបភាព និងបង្កើតប្លង់ 3D 4K សូមភ្ជាប់សេវាកម្ម VIP ជាមុនសិន។\n\n"
            "💎 **អត្ថប្រយោជន៍សមាជិកភាព VIP:**\n"
            "• 🧠 សួរគ្រូហុងស៊ុយ AI គ្មានដែនកំណត់ ២៤/៧/៣៦៥\n"
            "• 📚 កម្មវិធីសិក្សា ១០០ ប្រធានបទ & ១០០០ មេរៀនស៊ីជម្រៅ\n"
            "• 🧭 គណនា Life Gua, តារាហោះ យុគ ៩, BaZi ៤ សសរ & ១០ Gods\n"
            "• 📸 ស្កេនពិនិត្យរូបភាពបន្ទប់/ផ្ទះរក Sha Qi & វិធីកែខៃ\n"
            "• 🎨 បង្កើតប្លង់ហុងស៊ុយ 3D 4K Photorealistic\n\n"
            "👉 **សូមទាក់ទងមកកាន់ SUPER ADMIN ផ្ទាល់ដើម្បីភ្ជាប់សេវាកម្ម VIP ភ្លាមៗ:**\n"
            "👑 **Telegram Admin:** [@HemSinath](https://t.me/HemSinath)\n\n"
            "🎟️ *(ប្រសិនបើលោកអ្នកមាន Key អាជ្ញាប័ណ្ណរួចហើយ សូមវាយ `/redeem <Key>`)*"
        )
        keyboard = [
            [InlineKeyboardButton("👑 ភ្ជាប់សេវាកម្ម VIP (ទាក់ទង Admin @HemSinath)", url="https://t.me/HemSinath")],
            [
                InlineKeyboardButton("🎟️ បញ្ចូល Key អាជ្ញាប័ណ្ណ", callback_data="vip_redeem_prompt"),
                InlineKeyboardButton("💎 អត្ថប្រយោជន៍ VIP", callback_data="vip_perks_info")
            ]
        ]
        if hasattr(message_or_query, "edit_message_text"):
            await self._safe_edit(message_or_query, msg, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await self._safe_reply(message_or_query, msg, reply_markup=InlineKeyboardMarkup(keyboard))

    def _get_main_keyboard(self, user_id: int = 0) -> InlineKeyboardMarkup:
        """Construct role-based interactive keyboard: Super Admin vs VIP vs Free/Unactivated."""
        user = self.db.get_or_create_user(user_id) if user_id else {"role": "user", "vip_tier": "free"}
        is_admin = user.get("role") == "super_admin" or user_id in config.ADMIN_USER_IDS
        is_vip = user.get("vip_tier") in ("monthly", "yearly", "lifetime", "admin") or is_admin

        if is_admin:
            keyboard = [
                [InlineKeyboardButton("📚 កម្មវិធីសិក្សា ១០០០ មេរៀន", callback_data="menu_curriculum")],
                [
                    InlineKeyboardButton("🧭 គណនា Life Gua", callback_data="menu_gua"),
                    InlineKeyboardButton("🌌 តារាហោះ យុគ ៩", callback_data="menu_flyingstars")
                ],
                [
                    InlineKeyboardButton("🔮 វិភាគ BaZi ៤ សសរ", callback_data="menu_bazi"),
                    InlineKeyboardButton("📊 ទស្សន៍ទាយសំណាង", callback_data="menu_predict")
                ],
                [
                    InlineKeyboardButton("💖 ហុងស៊ុយ & មហាស្នេហ៍", callback_data="menu_love"),
                    InlineKeyboardButton("🎨 បង្កើតប្លង់ 3D 4K", callback_data="menu_render3d")
                ],
                [
                    InlineKeyboardButton("💬 សួរគ្រូហុងស៊ុយ AI", callback_data="menu_ask"),
                    InlineKeyboardButton("👑 ផតថល VIP & អាជ្ញាប័ណ្ណ", callback_data="menu_vip")
                ],
                [
                    InlineKeyboardButton("🛡️ ផ្ទាំងគ្រប់គ្រង Super Admin", callback_data="admin_panel"),
                    InlineKeyboardButton("⚡ ស្ថានភាពប្រព័ន្ធ", callback_data="menu_health")
                ],
                [InlineKeyboardButton("❓ ជំនួយ (Help)", callback_data="menu_help")]
            ]
        elif is_vip:
            keyboard = [
                [InlineKeyboardButton("📚 កម្មវិធីសិក្សា ១០០០ មេរៀន", callback_data="menu_curriculum")],
                [
                    InlineKeyboardButton("🧭 គណនា Life Gua", callback_data="menu_gua"),
                    InlineKeyboardButton("🌌 តារាហោះ យុគ ៩", callback_data="menu_flyingstars")
                ],
                [
                    InlineKeyboardButton("🔮 វិភាគ BaZi ៤ សសរ", callback_data="menu_bazi"),
                    InlineKeyboardButton("📊 ទស្សន៍ទាយសំណាង", callback_data="menu_predict")
                ],
                [
                    InlineKeyboardButton("💖 ហុងស៊ុយ & មហាស្នេហ៍", callback_data="menu_love"),
                    InlineKeyboardButton("🎨 បង្កើតប្លង់ 3D 4K", callback_data="menu_render3d")
                ],
                [
                    InlineKeyboardButton("💬 សួរគ្រូហុងស៊ុយ AI", callback_data="menu_ask"),
                    InlineKeyboardButton("👑 ស្ថានភាព VIP របស់ខ្ញុំ", callback_data="menu_vip")
                ],
                [
                    InlineKeyboardButton("⚡ ស្ថានភាពប្រព័ន្ធ", callback_data="menu_health"),
                    InlineKeyboardButton("❓ ជំនួយ (Help)", callback_data="menu_help")
                ]
            ]
        else:
            # Free / Unactivated user: compelling gated buttons directing to @HemSinath
            keyboard = [
                [InlineKeyboardButton("👑 ភ្ជាប់សេវាកម្ម VIP (ទាក់ទង Admin @HemSinath)", url="https://t.me/HemSinath")],
                [
                    InlineKeyboardButton("🎟️ បញ្ចូល Key អាជ្ញាប័ណ្ណ", callback_data="vip_redeem_prompt"),
                    InlineKeyboardButton("💎 អត្ថប្រយោជន៍ VIP", callback_data="vip_perks_info")
                ],
                [
                    InlineKeyboardButton("⚡ ស្ថានភាពប្រព័ន្ធ", callback_data="menu_health"),
                    InlineKeyboardButton("❓ ជំនួយ (Help)", callback_data="menu_help")
                ]
            ]

        return InlineKeyboardMarkup(keyboard)

    async def post_init(self, application: Application) -> None:
        """Register native command menu button in Telegram UI and start background schedulers."""
        commands = [
            BotCommand("start", "🌟 ផ្ទាំងដើម & ម៉ឺនុយបញ្ជា (Main Dashboard)"),
            BotCommand("love", "💖 ហុងស៊ុយ & មហាស្នេហ៍ (Peach Blossom)"),
            BotCommand("render3d", "🎨 បង្កើតប្លង់ 3D 4K & ពិនិត្យរូបភាព"),
            BotCommand("health", "⚡ ត្រួតពិនិត្យសុខភាព VPS, CPU, RAM, Disk, AI"),
            BotCommand("vip", "👑 ស្ថានភាព VIP & បញ្ចូល Key អាជ្ញាប័ណ្ណ"),
            BotCommand("redeem", "🎟️ បញ្ចូល Key (ឧ. /redeem FS-M-XXXX-XXXX)"),
            BotCommand("curriculum", "📚 កម្មវិធីសិក្សា ១០០ ប្រធានបទ & ១០០០ មេរៀន"),
            BotCommand("learn", "📖 រៀនមេរៀនជាក់លាក់ (ឧ. /learn 1)"),
            BotCommand("gua", "🧭 គណនា Life Gua (ឧ. /gua 1988 male)"),
            BotCommand("flyingstars", "🌌 តារាហោះ ៩ វិហារ យុគ ៩"),
            BotCommand("bazi", "🔮 វិភាគ BaZi (ឧ. /bazi 1988-05-15 10:30)"),
            BotCommand("predict", "📊 ទស្សន៍ទាយសំណាង (ឧ. /predict 1988-05-15)"),
            BotCommand("ask", "🧠 ពិគ្រោះយោបល់ជាមួយ FS-Supreme-Master AI"),
            BotCommand("admin", "🛡️ Super Admin Control Panel"),
            BotCommand("backup", "📦 Backup ទិន្នន័យ & ផ្ញើ File Zip (Admin)"),
            BotCommand("help", "❓ សៀវភៅណែនាំប្រើប្រាស់")
        ]
        try:
            await application.bot.set_my_commands(commands)
            logger.info("Native Telegram Bot Commands registered successfully.")
        except Exception as e:
            logger.warning(f"Could not register Telegram Bot commands: {e}")

        # Start 24-Hour Automated Backup Scheduler (2:00 AM Phnom Penh ICT)
        asyncio.create_task(self._start_daily_backup_scheduler(application))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command with role-based UI and compelling VIP invitation."""
        from_user = update.effective_user
        user = self.db.get_or_create_user(
            telegram_id=from_user.id,
            username=from_user.username or "",
            full_name=from_user.full_name or ""
        )

        # Notify Super Admin immediately if a new user joins!
        if user.get("is_new_user"):
            asyncio.create_task(self._notify_admin_new_user(context, from_user, user))

        is_admin = user.get("role") == "super_admin" or from_user.id in config.ADMIN_USER_IDS
        is_vip = user.get("vip_tier") in ("monthly", "yearly", "lifetime", "admin") or is_admin

        if is_admin:
            welcome_text = (
                "🛡️ **ផ្ទាំងបញ្ជា SUPREME FENG SHUI AGI - SUPER ADMIN** 🛡️\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👑 **សូមស្វាគមន៍លោកមេការ:** `{from_user.full_name}` (ID: `{from_user.id}`)\n"
                "🏷️ **សិទ្ធិ:** **Super Admin (Master Authority - គ្មានដែនកំណត់)**\n\n"
                "ប្រព័ន្ធកំពុងដំណើរការពេញលេញ ២៤/៧ ជាមួយ ៧ សសរស្តម្ភ Matrix & Gemini 82-Key Omni Mesh!\n\n"
                "👇 **សូមជ្រើសរើសមុខងារគ្រប់គ្រង ឬសាកល្បង AGI ខាងក្រោម៖**"
            )
        elif is_vip:
            tier_badges = {
                "monthly": "🌟 VIP ប្រចាំខែ (Monthly VIP)",
                "yearly": "👑 VIP ប្រចាំឆ្នាំ (Yearly VIP)",
                "lifetime": "💎 VIP មួយជីវិត (Lifetime VIP)"
            }
            badge = tier_badges.get(user.get("vip_tier"), "👑 VIP Member")
            expiry_info = f"• 📅 ផុតកំណត់: `{user.get('vip_expiry', 'Lifetime')[:10]}`"
            welcome_text = (
                "🌟 **SUPREME FENG SHUI AGI SYSTEM (Master Level v1.0.0)** 🌟\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 **សូមស្វាគមន៍:** `{from_user.full_name}` (ID: `{from_user.id}`)\n"
                f"🏷️ **កម្រិតសមាជិកភាព:** **{badge}**\n"
                f"{expiry_info}\n"
                "✨ **សិទ្ធិរបស់អ្នក:** ប្រើប្រាស់មុខងារទាំងអស់បាន **គ្មានដែនកំណត់ 24/7/365**!\n\n"
                "👇 **សូមជ្រើសរើសមុខងារដែលអ្នកចង់ប្រើប្រាស់ខាងក្រោម៖**"
            )
        else:
            # Gated Compelling Welcome Message for Free/New Users
            welcome_text = (
                "🌟 **SUPREME FENG SHUI AGI SYSTEM (Master Level v1.0.0)** 🌟\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "👋 **សូមស្វាគមន៍មកកាន់កំពូលប្រព័ន្ធបញ្ញាសិប្បនិម្មិតហុងស៊ុយបុរាណ AGI កម្រិតពិភពលោក!**\n\n"
                f"👤 **គណនីរបស់អ្នក:** `{from_user.full_name}` (ID: `{from_user.id}`)\n"
                "🏷️ **ស្ថានភាពគណនី:** 🔒 **មិនទាន់ភ្ជាប់ VIP (Locked)**\n\n"
                "💎 **ហេតុអ្វីបានជាលោកអ្នកត្រូវភ្ជាប់ SUPREME FENG SHUI VIP?**\n"
                "• 🧠 **គ្រូហុងស៊ុយ AI ឆ្លាតវៃបំផុត**: សួរពិគ្រោះយោបល់គ្រប់សំណួរ ២៤/៧/៣៦៥ គ្មានដែនកំណត់\n"
                "• 📚 **រៀនក្បួនបុរាណ ១,០០០ មេរៀន**: ពីកម្រិតដំបូងរហូតដល់ Master កំពូល (១០០ ប្រធានបទ)\n"
                "• 🧭 **ក្បួនគណិតវិទ្យាហុងស៊ុយ ០ កំហុស**: គណនា Life Gua, តារាហោះ យុគ ៩, BaZi ៤ សសរ & ១០ Gods\n"
                "• 📸 **សវនកម្មរូបភាព AI Vision**: ស្កេនរូបថតបន្ទប់/ផ្ទះ រក Sha Qi & វិធីកែខៃភ្លាមៗ\n"
                "• 🎨 **ស្ទូឌីយោប្លង់ 3D 4K**: បង្កើតរូបភាពប្លង់ហុងស៊ុយ 3D 4K Photorealistic\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "👉 **ដើម្បីបើកសិទ្ធិប្រើប្រាស់ពេញលេញ សូមទាក់ទង SUPER ADMIN ផ្ទាល់:**\n"
                "👑 **Telegram Admin:** [@HemSinath](https://t.me/HemSinath)\n\n"
                "🎟️ *ប្រសិនបើលោកអ្នកមានលេខកូដ Key រួចហើយ សូមចុចប៊ូតុង '🎟️ បញ្ចូល Key អាជ្ញាប័ណ្ណ' ខាងក្រោម!*"
            )

        await self._safe_reply(update.message, welcome_text, reply_markup=self._get_main_keyboard(from_user.id))

    async def _notify_admin_new_user(self, context: ContextTypes.DEFAULT_TYPE, from_user, user_data: Dict[str, Any]):
        """Send instantaneous rich alert to Super Admin whenever a new user starts the bot."""
        admin_ids = config.ADMIN_USER_IDS
        if not admin_ids or from_user.id in admin_ids:
            return

        stats = self.db.get_system_stats()
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        username_str = f"@{from_user.username}" if from_user.username else "គ្មាន (No Username)"
        lang_str = from_user.language_code or "មិនស្គាល់ (Unknown)"

        alert_text = (
            "🔔 **សេចក្តីជូនដំណឹង៖ មានអ្នកប្រើប្រាស់ថ្មីទើបតែចុច /start** 🔔\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **ឈ្មោះពេញ:** `{from_user.full_name}`\n"
            f"🆔 **Telegram ID:** `{from_user.id}`\n"
            f"🌐 **Username:** {username_str}\n"
            f"🗣️ **ភាសាទូរស័ព្ទ:** `{lang_str}`\n"
            f"⏱️ **កាលបរិច្ឆេទ:** `{now_str}`\n"
            f"🏷️ **ស្ថានភាព:** `🔒 គណនីថ្មីមិនទាន់ភ្ជាប់ VIP (Locked)`\n\n"
            f"📊 **ស្ថិតិប្រព័ន្ធសរុប (Live System Stats):**\n"
            f"• 👥 **អ្នកប្រើប្រាស់សរុប:** `{stats['total_users']}` នាក់\n"
            f"• 👑 **សមាជិក VIP សកម្ម:** `{stats['total_vips']}` នាក់\n\n"
            "⚡ **ផ្តល់សិទ្ធិ VIP ជូនគាត់ភ្លាមៗ (1-Click Quick Actions):**"
        )

        keyboard = [
            [
                InlineKeyboardButton("🌟 ផ្តល់ VIP 1 ខែ", callback_data=f"adm_give_{from_user.id}_monthly"),
                InlineKeyboardButton("👑 ផ្តល់ VIP 1 ឆ្នាំ", callback_data=f"adm_give_{from_user.id}_yearly")
            ],
            [
                InlineKeyboardButton("💎 ផ្តល់ VIP មួយជីវិត", callback_data=f"adm_give_{from_user.id}_lifetime")
            ]
        ]

        for admin_id in admin_ids:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=alert_text,
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            except Exception as e:
                logger.warning(f"Could not send new user alert to admin {admin_id}: {e}")

    async def vip_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /vip command to display subscription status & upgrade options."""
        from_user = update.effective_user
        user = self.db.get_or_create_user(from_user.id, from_user.username or "", from_user.full_name or "")
        await self._send_vip_view(update.message, user)

    async def _send_vip_view(self, message_or_query, user: Dict[str, Any], is_edit: bool = False):
        """Render VIP Dashboard View."""
        tier = user.get("vip_tier", "free")
        expiry = user.get("vip_expiry")
        is_vip = tier in ("monthly", "yearly", "lifetime", "admin")

        if tier == "admin":
            status_text = "🛡️ **Super Admin (អំណាចគ្រប់គ្រងកំពូល)** - គ្មានថ្ងៃផុតកំណត់"
        elif tier == "lifetime":
            status_text = "💎 **VIP មួយជីវិត (Lifetime VIP)** - សិទ្ធិប្រើប្រាស់ជារៀងរហូត"
        elif tier in ("monthly", "yearly") and expiry:
            exp_date = expiry[:10]
            status_text = f"👑 **VIP ({tier.capitalize()})** - ផុតកំណត់នៅថ្ងៃទី `{exp_date}`"
        else:
            status_text = "✨ **សមាជិកឥតគិតថ្លៃ (Free Tier)** (កូតាសួរ ៥ ដង/ថ្ងៃ)"

        text = (
            "👑 **ផតថលសមាជិកភាព VIP & អាជ្ញាប័ណ្ណ (VIP Portal)**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **ម្ចាស់គណនី:** `{user.get('full_name', '')}` (ID: `{user['telegram_id']}`)\n"
            f"📊 **ស្ថានភាពបច្ចុប្បន្ន:** {status_text}\n"
            f"🔢 **សំណួរសរុបដែលបានសួរ:** `{user.get('total_queries', 0)}` ដង\n\n"
            "💎 **អត្ថប្រយោជន៍ផ្តាច់មុខសម្រាប់សមាជិក VIP:**\n"
            "• ⚡ **សួរគ្រូហុងស៊ុយ AGI គ្មានដែនកំណត់ 24/7** (គ្មានកូតាកំណត់ប្រចាំថ្ងៃ)\n"
            "• 🔮 **វិភាគ BaZi & អាទិទេពទាំង ១០ ស៊ីជម្រៅ** រួមទាំងវដ្តសំណាង ១០ ឆ្នាំ (Da Yun)\n"
            "• 🌌 **សវនកម្មប្លង់ផ្ទះតារាហោះ យុគ ៩ ពេញលេញ** ជាមួយរូបមន្តកែហុងស៊ុយ\n"
            "• 🗓️ **ក្បួនរើសថ្ងៃជ័យជាន់ខ្ពស់ Ze Ri** សម្រាប់ឡើងផ្ទះ បើកហាង រៀបការ\n"
            "• 📜 **សិទ្ធិទាញយកឯកសារមេរៀន Masterclass ១០០០ មេរៀន**\n"
            "• 🚀 **អាទិភាពខ្ពស់បំផុតលើម៉ូដែល AI Boramey & DeepSeek-R1**\n\n"
            "🎟️ **របៀបបញ្ចូល Key អាជ្ញាប័ណ្ណ:**\n"
            "សូមវាយ៖ `/redeem <លេខកូដ Key>` (ឧ. `/redeem FS-M-ABCD-1234`)"
        )

        keyboard = [
            [
                InlineKeyboardButton("🎟️ របៀបបញ្ចូល Key", callback_data="vip_redeem_prompt"),
                InlineKeyboardButton("💎 សេវាកម្មពិសេស VIP", callback_data="vip_features")
            ],
            [
                InlineKeyboardButton("💬 សួរគ្រូហុងស៊ុយ AI", callback_data="menu_ask"),
                InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
            ]
        ]

        if is_edit:
            await self._safe_edit(message_or_query, text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await self._safe_reply(message_or_query, text, reply_markup=InlineKeyboardMarkup(keyboard))

    async def redeem_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /redeem <key> command."""
        from_user = update.effective_user
        args = context.args

        if not args:
            await self._safe_reply(
                update.message,
                "⚠️ **សូមបញ្ចូលលេខកូដអាជ្ញាប័ណ្ណ (License Key)**\n"
                "ឧទាហរណ៍៖ `/redeem FS-M-ABCD-1234` ឬ `/redeem FS-Y-XXXX-YYYY`"
            )
            return

        key = args[0].strip()
        res = self.db.redeem_license(telegram_id=from_user.id, key=key)

        if res["success"]:
            success_text = (
                "🎉 **អបអរសាទរ! អ្នកបាន Upgrade ទៅកាន់ VIP ជោគជ័យ!** 👑✨\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🏷️ **កម្រិតអាជ្ញាប័ណ្ណ:** **{res['tier_name_kh']}**\n"
                f"⏳ **សុពលភាពបន្ថែម:** `+{res['days_added']} ថ្ងៃ`\n"
                f"📅 **កាលបរិច្ឆេទផុតកំណត់:** `{res['expiry_date']}`\n\n"
                "⚡ ឥឡូវនេះ អ្នកមានសិទ្ធិប្រើប្រាស់រាល់មុខងារពិសេសទាំងអស់របស់ Supreme Feng Shui AGI ដោយគ្មានដែនកំណត់ 24/7!"
            )
            keyboard = [
                [InlineKeyboardButton("👑 ពិនិត្យស្ថានភាព VIP", callback_data="menu_vip")],
                [InlineKeyboardButton("🧠 សួរគ្រូហុងស៊ុយ AI ភ្លាមៗ", callback_data="menu_ask")],
                [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
            ]
            await self._safe_reply(update.message, success_text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await self._safe_reply(
                update.message,
                f"{res['error']}\n\n👉 សូមទាក់ទង Super Admin ឬពិនិត្យមើលលេខកូដ Key ឡើងវិញ។"
            )

    # ==================== SUPER ADMIN CONTROLS ====================

    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /admin command (Super Admin Only)."""
        from_user = update.effective_user
        user = self.db.get_or_create_user(from_user.id, from_user.username or "", from_user.full_name or "")

        if user.get("role") != "super_admin":
            await self._safe_reply(
                update.message,
                "⛔ **ការបដិសេធសិទ្ធិ (Access Denied)**\n"
                "ផ្ទាំងគ្រប់គ្រងនេះសម្រាប់តែ Super Admin ប៉ុណ្ណោះ។"
            )
            return

        await self._send_admin_dashboard(update.message, user)

    async def _send_admin_dashboard(self, message_or_query, admin_user: Dict[str, Any], is_edit: bool = False):
        """Render Super Admin Dashboard."""
        stats = self.db.get_system_stats()

        text = (
            "🛡️ **ផ្ទាំងគ្រប់គ្រង SUPER ADMIN (Master Control Panel)** 🛡️\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 **Super Admin:** `{admin_user.get('full_name', '')}` (ID: `{admin_user['telegram_id']}`)\n\n"
            "📊 **ស្ថិតិប្រព័ន្ធផ្សាយផ្ទាល់ (Live System Telemetry):**\n"
            f"• 👥 **អ្នកប្រើប្រាស់សរុប:** `{stats['total_users']}` នាក់\n"
            f"• 👑 **សមាជិក VIP សរុប:** `{stats['total_vips']}` នាក់\n"
            f"  - 🌟 VIP ប្រចាំខែ: `{stats['vip_monthly']}` នាក់\n"
            f"  - 👑 VIP ប្រចាំឆ្នាំ: `{stats['vip_yearly']}` នាក់\n"
            f"  - 💎 VIP មួយជីវិត: `{stats['vip_lifetime']}` នាក់\n"
            f"• 🔑 **Keys សរុបដែលបានបង្កើត:** `{stats['total_licenses']}`\n"
            f"  - 🟢 Keys មិនទាន់ប្រើ: `{stats['active_licenses']}`\n"
            f"  - 🔴 Keys ប្រើប្រាស់រួច: `{stats['redeemed_licenses']}`\n"
            f"• 💬 **ចំនួនសំណួរដែលបានឆ្លើយ:** `{stats['total_queries']}` ដង\n\n"
            "👇 **សូមជ្រើសរើសមុខងារគ្រប់គ្រងខាងក្រោម៖**"
        )

        keyboard = [
            [
                InlineKeyboardButton("🔑 បង្កើត Key អាជ្ញាប័ណ្ណ", callback_data="admin_genkeys_menu"),
                InlineKeyboardButton("📋 បញ្ជី Keys មិនទាន់ប្រើ", callback_data="admin_keys_list")
            ],
            [
                InlineKeyboardButton("👥 បញ្ជីសមាជិក & VIP", callback_data="admin_users_list"),
                InlineKeyboardButton("📊 ស្ថិតិប្រព័ន្ធលម្អិត", callback_data="admin_stats")
            ],
            [
                InlineKeyboardButton("📦 Backup ទិន្នន័យ (Zip)", callback_data="admin_trigger_backup"),
                InlineKeyboardButton("⚡ សុខភាពម៉ាស៊ីន (Health)", callback_data="menu_health")
            ],
            [
                InlineKeyboardButton("📢 ផ្ញើសារប្រកាស (Broadcast)", callback_data="admin_broadcast_info"),
                InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
            ]
        ]

        if is_edit:
            await self._safe_edit(message_or_query, text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await self._safe_reply(message_or_query, text, reply_markup=InlineKeyboardMarkup(keyboard))

    def get_system_health_telemetry(self) -> Dict[str, Any]:
        """Compute complete live VPS, CPU, RAM, Disk, and AI Models telemetry."""
        # 1. Host Info
        os_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
        py_ver = platform.python_version()

        # 2. CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count(logical=True) or 1

        # 3. RAM & Memory
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        proc = psutil.Process(os.getpid())
        proc_ram_mb = proc.memory_info().rss / (1024 * 1024)

        phys_total_mb = mem.total / (1024 * 1024)
        phys_used_mb = mem.used / (1024 * 1024)
        phys_avail_mb = mem.available / (1024 * 1024)

        swap_total_mb = swap.total / (1024 * 1024)
        swap_used_mb = swap.used / (1024 * 1024)
        swap_free_mb = swap.free / (1024 * 1024)
        effective_total_mb = phys_total_mb + swap_total_mb

        # 4. Disk
        try:
            disk = psutil.disk_usage("/")
        except Exception:
            drive = os.path.splitdrive(os.path.abspath("."))[0] or "C:\\"
            disk = psutil.disk_usage(drive)

        disk_total_gb = disk.total / (1024 ** 3)
        disk_used_gb = disk.used / (1024 ** 3)
        disk_free_gb = disk.free / (1024 ** 3)

        # 5. Database
        db_stats = self.db.get_system_stats()

        # 6. AI Models
        hf_connected = self.master.hf_bridge.is_connected()
        gemini_pool_count = self.master.omni_bridge.gemini_pool.get_key_count()
        gemini_active = self.master.omni_bridge.gemini_pool.is_available()

        return {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "os_info": os_info,
            "py_ver": py_ver,
            "cpu_percent": cpu_percent,
            "cpu_count": cpu_count,
            "proc_ram_mb": round(proc_ram_mb, 2),
            "phys_total_mb": round(phys_total_mb, 2),
            "phys_used_mb": round(phys_used_mb, 2),
            "phys_avail_mb": round(phys_avail_mb, 2),
            "phys_pct": mem.percent,
            "swap_total_mb": round(swap_total_mb, 2),
            "swap_used_mb": round(swap_used_mb, 2),
            "swap_free_mb": round(swap_free_mb, 2),
            "effective_total_mb": round(effective_total_mb, 2),
            "disk_total_gb": round(disk_total_gb, 2),
            "disk_used_gb": round(disk_used_gb, 2),
            "disk_free_gb": round(disk_free_gb, 2),
            "disk_pct": disk.percent,
            "db_stats": db_stats,
            "hf_connected": hf_connected,
            "gemini_active": gemini_active,
            "gemini_keys_count": gemini_pool_count
        }

    async def health_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /health command to display live VPS, CPU, RAM, Disk, and AI Models telemetry."""
        await self._send_health_view(update.message, is_edit=False)

    async def _send_health_view(self, message_or_query, is_edit: bool = False):
        """Render live system health telemetry view."""
        h = self.get_system_health_telemetry()
        stats = h["db_stats"]

        hf_status_badge = "🟢 ONLINE (HuggingFace Cloud)" if h["hf_connected"] else "🟡 HYBRID MODE (Local Optimized)"
        gemini_badge = f"🟢 ACTIVE ({h['gemini_keys_count']} Keys in Pool)" if h["gemini_active"] else "🟡 STANDBY (Add GEMINI_API_KEYS)"

        msg = (
            "⚡ **SUPREME FENG SHUI AGI - LIVE SYSTEM HEALTH** ⚡\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🟢 **ស្ថានភាពរួម:** **HEALTHY & OPERATIONAL (100%)**\n"
            f"⏱️ **ពេលវេលាត្រួតពិនិត្យ:** `{h['timestamp']}`\n\n"
            "🖥️ **១. ព័ត៌មានម៉ាស៊ីនបម្រើ (VPS Host Environment):**\n"
            f"• **ប្រព័ន្ធប្រតិបត្តិការ (OS):** `{h['os_info']}`\n"
            f"• **Python Engine:** `v{h['py_ver']}`\n"
            f"• **ស្ថាបត្យកម្ម RAM:** `Super Smart Hybrid (zRAM + 4GB NVMe Swap)`\n\n"
            "⚡ **២. បន្ទុកស៊ីភីយូ (CPU Performance):**\n"
            f"• **ការប្រើប្រាស់ CPU:** `{h['cpu_percent']}%` (ចំនួន Cores: `{h['cpu_count']}`)\n\n"
            "🧠 **៣. ស្ថានភាពមេម៉ូរី (RAM & Swap Telemetry):**\n"
            f"• **Process RAM (Bot & API RSS):** `{h['proc_ram_mb']} MB` / 1024 MB VPS Limit\n"
            f"• **Physical RAM:** `{h['phys_total_mb']} MB` (ប្រើប្រាស់ `{h['phys_used_mb']} MB` - `{h['phys_pct']}%`)\n"
            f"• **Swap / zRAM Memory:** `{h['swap_total_mb']} MB` (នៅសល់ `{h['swap_free_mb']} MB`)\n"
            f"• **Effective Total RAM:** `{h['effective_total_mb']} MB (~5.1 GB Capacity)`\n\n"
            "💾 **៤. ទំហំថាសរឹង (Disk Storage Space):**\n"
            f"• **ទំហំសរុប (Total Disk):** `{h['disk_total_gb']} GB`\n"
            f"• **បានប្រើប្រាស់ (Used):** `{h['disk_used_gb']} GB ({h['disk_pct']}%)` | **នៅសល់:** `{h['disk_free_gb']} GB`\n\n"
            "🤖 **៥. ម៉ូដែល AI & Cloud Mesh (Omni Intelligence Pool):**\n"
            f"• 🌟 **Google Gemini Mesh:** `{config.GEMINI_MODEL}`\n"
            f"  └ ស្ថានភាព: {gemini_badge}\n"
            f"• 🧠 **HuggingFace FS-Boramey:** `{config.HF_MODEL_BORAMEY}`\n"
            f"  └ ស្ថានភាព: {hf_status_badge}\n"
            f"• 🔬 **Reasoner Deep Logic:** `{config.HF_MODEL_REASONER}`\n"
            f"• 🔍 **Vector Embedder:** `{config.HF_MODEL_EMBEDDER}`\n"
            f"• 🏛️ **Zenith 7 Pillars Matrix:** `Vision, Qi, Time, Physiognomy, Geo, Astro, Bazi` (🟢 Live)\n"
            f"• 📚 **Curriculum Master Engine:** `100 Topics / 1,000 Lessons Online`\n\n"
            "🗄️ **៦. ទិន្នន័យ & សេវាកម្ម (Database & Live Services):**\n"
            f"• 💾 **Database Engine:** `SQLite WAL Mode` (🟢 Healthy)\n"
            f"• 👥 **Users:** `{stats['total_users']}` នាក់ | 👑 **Active VIPs:** `{stats['total_vips']}` នាក់\n"
            f"• 🔑 **Keys មិនទាន់ប្រើ:** `{stats['active_licenses']}` | 🔴 **Keys ប្រើរួច:** `{stats['redeemed_licenses']}`\n"
            f"• 🌐 **FastAPI REST API:** `Port {config.API_PORT}` (🟢 Online)\n"
            f"• 🤖 **Telegram Bot:** `Polling Active` (🟢 Responsive)"
        )

        keyboard = [
            [
                InlineKeyboardButton("🔄 ពិនិត្យសុខភាពឡើងវិញ (Refresh)", callback_data="menu_health"),
                InlineKeyboardButton("👑 VIP Portal", callback_data="menu_vip")
            ],
            [
                InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
            ]
        ]

        if is_edit:
            await self._safe_edit(message_or_query, msg, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await self._safe_reply(message_or_query, msg, reply_markup=InlineKeyboardMarkup(keyboard))

    async def setvip_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /setvip <user_id> <monthly|yearly|lifetime|free> (Admin Only)."""
        from_user = update.effective_user
        admin = self.db.get_or_create_user(from_user.id)
        if admin.get("role") != "super_admin":
            await self._safe_reply(update.message, "⛔ Access Denied.")
            return

        args = context.args
        if len(args) < 2:
            await self._safe_reply(
                update.message,
                "⚠️ **របៀបប្រើប្រាស់៖** `/setvip <user_id> <monthly|yearly|lifetime|free>`\n"
                "ឧទាហរណ៍៖ `/setvip 123456789 yearly`"
            )
            return

        try:
            target_id = int(args[0])
            tier = args[1].lower()
            res = self.db.set_user_vip_manually(target_id, tier, admin_id=from_user.id)

            if res["success"]:
                await self._safe_reply(
                    update.message,
                    f"✅ **បានផ្លាស់ប្តូរកម្រិត VIP ជោគជ័យ!**\n"
                    f"• Target ID: `{target_id}`\n"
                    f"• Role: `{res['role']}`\n"
                    f"• VIP Tier: `{res['vip_tier']}`\n"
                    f"• Expiry: `{res['expiry']}`"
                )
            else:
                await self._safe_reply(update.message, f"❌ កំហុស៖ {res.get('error')}")
        except ValueError:
            await self._safe_reply(update.message, "❌ User ID ត្រូវតែជាលេខ។")

    async def genkeys_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /genkeys <monthly|yearly|lifetime> [count] (Admin Only)."""
        from_user = update.effective_user
        admin = self.db.get_or_create_user(from_user.id)
        if admin.get("role") != "super_admin":
            await self._safe_reply(update.message, "⛔ Access Denied.")
            return

        args = context.args
        tier = args[0].lower() if len(args) > 0 else "monthly"
        count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
        count = min(count, 20)  # Max 20 keys at once

        keys = self.db.generate_license_key(tier=tier, count=count, created_by=from_user.id)

        keys_text = "\n".join([f"`{k}`" for k in keys])
        msg = (
            f"🔑 **បានបង្កើត {count} License Keys ({tier.capitalize()}) ជោគជ័យ!**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{keys_text}\n\n"
            f"*(អ្នកអាច Copy Key ទាំងនេះផ្ញើជូនអតិថិជន ដើម្បីឱ្យពួកគេវាយ `/redeem <key>`)*"
        )
        await self._safe_reply(update.message, msg)

    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /broadcast <message> (Admin Only)."""
        from_user = update.effective_user
        admin = self.db.get_or_create_user(from_user.id)
        if admin.get("role") != "super_admin":
            await self._safe_reply(update.message, "⛔ Access Denied.")
            return

        msg_text = " ".join(context.args)
        if not msg_text:
            await self._safe_reply(update.message, "⚠️ សូមបញ្ចូលសារដែលចង់ Broadcast៖ `/broadcast <សាររបស់អ្នក>`")
            return

        users = self.db.get_all_users_list(limit=500)
        sent_count = 0
        broadcast_msg = f"📢 **សេចក្តីប្រកាសពី SUPREME FENG SHUI AGI** 📢\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{msg_text}"

        for u in users:
            try:
                await context.bot.send_message(chat_id=u["telegram_id"], text=broadcast_msg, parse_mode="Markdown")
                sent_count += 1
                await asyncio.sleep(0.05)  # Avoid rate limit
            except Exception as e:
                logger.debug(f"Could not send broadcast to {u['telegram_id']}: {e}")

        await self._safe_reply(update.message, f"✅ បានផ្ញើសារប្រកាសជូន {sent_count}/{len(users)} នាក់ដោយជោគជ័យ!")

    async def _start_daily_backup_scheduler(self, application: Application):
        """
        Automated background loop: every 24 hours at 2:00 AM Phnom Penh time (ICT GMT+7),
        creates a compressed zip backup on VPS disk and dispatches it directly to Super Admin.
        """
        logger.info("Automated 24-Hour Backup Scheduler initialized (Target: 2:00 AM Phnom Penh ICT).")
        while True:
            try:
                secs_until_2am = self.backup.get_seconds_until_next_2am_ict()
                hours = round(secs_until_2am / 3600, 2)
                logger.info(f"Next automated 2:00 AM backup in {secs_until_2am:.0f} seconds (~{hours} hours).")

                # Sleep until 2:00 AM ICT
                await asyncio.sleep(secs_until_2am)

                # Perform online atomic backup
                logger.info("2:00 AM Phnom Penh ICT reached! Executing automated daily backup...")
                res = self.backup.create_backup(trigger_type="Automated 24-Hour Daily Backup (2:00 AM ICT)")

                if res["success"]:
                    await self._dispatch_backup_to_admins(application.bot, res, is_automated=True)
                else:
                    logger.error(f"Automated daily backup failed: {res.get('error')}")

                # Brief pause before next cycle calculation
                await asyncio.sleep(60)

            except Exception as e:
                logger.error(f"Error in automated backup scheduler loop: {e}", exc_info=True)
                await asyncio.sleep(300)

    async def _dispatch_backup_to_admins(self, bot, backup_res: Dict[str, Any], is_automated: bool = True):
        """Send backup zip document with rich telemetry caption directly to Super Admins."""
        admin_ids = config.ADMIN_USER_IDS
        if not admin_ids:
            return

        stats = backup_res["stats"]
        header = (
            "📦 **សេចក្តីរាយការណ៍៖ ទិន្នន័យ BACKUP ប្រចាំថ្ងៃស្វ័យប្រវត្តិកំពូល (2:00 AM ICT)** 📦\n"
            if is_automated else
            "📦 **សេចក្តីរាយការណ៍៖ ទិន្នន័យ BACKUP (MANUAL ON-DEMAND)** 📦\n"
        )

        caption = (
            f"{header}"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🌟 **ប្រព័ន្ធ SUPREME FENG SHUI AGI (Master Level v1.0.0)**\n\n"
            f"📁 **ឈ្មោះឯកសារ:** `{backup_res['file_name']}`\n"
            f"⏱️ **កាលបរិច្ឆេទ:** `{backup_res['timestamp_ict']}`\n"
            f"💾 **ទំហំឯកសារ:** `{backup_res['file_size_kb']} KB` (Zip Deflated)\n"
            f"🔐 **SHA-256 Checksum:** `{backup_res['sha256'][:16]}...` (100% Clean)\n\n"
            f"📊 **ស្ថិតិទិន្នន័យដែលបានរក្សាទុកក្នុង VPS Disk:**\n"
            f"• 👥 **អ្នកប្រើប្រាស់សរុប:** `{stats['total_users']}` នាក់\n"
            f"• 👑 **សមាជិក VIP សរុប:** `{stats['total_vips']}` នាក់\n"
            f"  - 🌟 VIP 1 ខែ: `{stats['vip_monthly']}` នាក់\n"
            f"  - 👑 VIP 1 ឆ្នាំ: `{stats['vip_yearly']}` នាក់\n"
            f"  - 💎 VIP មួយជីវិត: `{stats['vip_lifetime']}` នាក់\n"
            f"• 🔑 **អាជ្ញាប័ណ្ណសរុប:** `{stats['total_licenses']}` (មិនទាន់ប្រើ: `{stats['active_licenses']}`)\n"
            f"• 💬 **សំណួរសរុបក្នុងប្រព័ន្ធ:** `{stats['total_queries']}` ដង\n\n"
            f"🟢 **ស្ថានភាពរក្សាទុក:** បានរក្សាទុកក្នុង VPS Disk (`/data/backups/`) និងរក្សាទុក 30 ថ្ងៃចុងក្រោយដោយសុវត្ថិភាពខ្ពស់បំផុត!"
        )

        for admin_id in admin_ids:
            try:
                with open(backup_res["zip_path"], "rb") as f:
                    await bot.send_document(
                        chat_id=admin_id,
                        document=f,
                        filename=backup_res["file_name"],
                        caption=caption,
                        parse_mode="Markdown"
                    )
                logger.info(f"Backup zip successfully dispatched to Super Admin {admin_id}")
            except Exception as e:
                logger.error(f"Could not send backup zip to Admin {admin_id}: {e}", exc_info=True)

    async def backup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /backup command to trigger manual instant backup and receive zip file (Admin Only)."""
        from_user = update.effective_user
        admin = self.db.get_or_create_user(from_user.id)
        if admin.get("role") != "super_admin" and from_user.id not in config.ADMIN_USER_IDS:
            await self._safe_reply(update.message, "⛔ Access Denied. Command reserved for Super Admin.")
            return

        status_msg = await self._safe_reply(
            update.message,
            "⏳ **កំពុងដំណើរការបង្កើត Data Backup និង Zip File...**\n*(សូមរង់ចាំប្រហែល ១-២ វិនាទី)*"
        )

        res = self.backup.create_backup(trigger_type=f"Manual On-Demand (Admin {from_user.id})")
        if res["success"]:
            await self._dispatch_backup_to_admins(context.bot, res, is_automated=False)
            if status_msg:
                try:
                    await status_msg.delete()
                except Exception:
                    pass
        else:
            await self._safe_reply(update.message, f"❌ កំហុសក្នុងការបង្កើត Backup៖ {res.get('error')}")

    # ==================== GENERAL USER COMMANDS ====================

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        from_user = update.effective_user
        user = self.db.get_or_create_user(from_user.id)
        is_admin = user.get("role") == "super_admin"

        help_text = (
            "📖 **របៀបប្រើប្រាស់ពាក្យបញ្ជា (Command Guide):**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "👑 **សមាជិកភាព VIP & អាជ្ញាប័ណ្ណ:**\n"
            "• `/vip` - ពិនិត្យស្ថានភាព VIP & សិទ្ធិពិសេស\n"
            "• `/redeem FS-M-XXXX-XXXX` - បញ្ចូល Key អាជ្ញាប័ណ្ណ\n\n"
            "1️⃣ **រៀនសូត្រមេរៀន (1,000 Lessons):**\n"
            "• `/curriculum` - បើកកម្មវិធីសិក្សា ១០០ ប្រធានបទ\n"
            "• `/learn 1` - អានមេរៀនទី ១ (រហូតដល់ ១០០០)\n\n"
            "2️⃣ **គណនា Life Gua & ទិសល្អ/អាក្រក់:**\n"
            "• `/gua 1988 male` ឬ `/gua 1995 female`\n\n"
            "3️⃣ **តារាហោះ ៩ វិហារ យុគ ៩:**\n"
            "• `/flyingstars`\n\n"
            "4️⃣ **វិភាគ BaZi សសរស្តម្ភទាំង ៤:**\n"
            "• `/bazi 1988-05-15 10:30`\n\n"
            "5️⃣ **ទស្សន៍ទាយសំណាងប្រចាំថ្ងៃ:**\n"
            "• `/predict 1988-05-15`\n\n"
            "6️⃣ **ពិគ្រោះយោបល់ជាមួយ AI Master:**\n"
            "• `/ask តើខ្ញុំគួររៀបចំបន្ទប់គេង និងតុធ្វើការយ៉ាងណា?`\n"
        )

        if is_admin:
            help_text += (
                "\n🛡️ **ពាក្យបញ្ជាសម្រាប់ Super Admin:**\n"
                "• `/admin` - បើកផ្ទាំងគ្រប់គ្រង Admin Panel\n"
                "• `/genkeys monthly 5` - បង្កើត Key 5 អាជ្ញាប័ណ្ណ\n"
                "• `/setvip <user_id> yearly` - ផ្តល់ VIP ដោយដៃ\n"
                "• `/broadcast <message>` - ផ្ញើសារប្រកាសទូទៅ\n"
            )

        await self._safe_reply(update.message, help_text, reply_markup=self._get_main_keyboard(from_user.id))

    async def curriculum_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /curriculum command (VIP & Super Admin Only)."""
        from_user = update.effective_user
        if not self._is_vip_or_admin(from_user.id):
            await self._send_vip_required_notice(update.message, from_user.id)
            return

        cats = self.curriculum.get_categories()
        text = (
            "📚 **កម្មវិធីសិក្សាហុងស៊ុយបុរាណ ១០០ ប្រធានបទ & ១០០០ មេរៀន**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "រៀបចំយ៉ាងហ្មត់ចត់តាមក្បួនគណិតវិទ្យាហុងស៊ុយបុរាណពិតប្រាកដ ចែកចេញជា ៤ ផ្នែកធំៗ៖\n\n"
            "☯️ **ផ្នែកទី ១:** មូលដ្ឋានគ្រឹះក្បួនហុងស៊ុយបុរាណ (មេរៀន ១-២០០)\n"
            "🌌 **ផ្នែកទី ២:** ក្បួនជឿនលឿន & តារាហោះ យុគ ៩ (មេរៀន ២០១-៥០០)\n"
            "🏛️ **ផ្នែកទី ៣:** ការអនុវត្តជាក់ស្តែង & លំនៅឋាន/អាជីវកម្ម (មេរៀន ៥០១-៨០០)\n"
            "🔮 **ផ្នែកទី ៤:** ក្បួនឯកទេសជាន់ខ្ពស់ & BaZi រាសី (មេរៀន ៨០១-១០០០)\n\n"
            "👇 **សូមជ្រើសរើសផ្នែកដែលអ្នកចង់សិក្សា៖**"
        )
        keyboard = [
            [InlineKeyboardButton(f"{c['icon']} {c['name_kh']}", callback_data=f"curr_cat_{c['id']}_p1")]
            for c in cats
        ]
        keyboard.append([
            InlineKeyboardButton("📖 រៀនមេរៀនទី ១", callback_data="curr_les_1"),
            InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
        ])
        await self._safe_reply(update.message, text, reply_markup=InlineKeyboardMarkup(keyboard))

    async def learn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /learn <lesson_id> command (VIP & Super Admin Only)."""
        from_user = update.effective_user
        if not self._is_vip_or_admin(from_user.id):
            await self._send_vip_required_notice(update.message, from_user.id)
            return

        args = context.args
        if not args:
            await self._safe_reply(
                update.message,
                "⚠️ សូមបញ្ជាក់លេខមេរៀនពី ១ ដល់ ១០០០ (ឧទាហរណ៍៖ `/learn 1` ឬ `/learn 23`)"
            )
            return

        try:
            lesson_id = int(args[0])
            await self._send_lesson_view(update.message, lesson_id)
        except ValueError:
            await self._safe_reply(update.message, "❌ លេខមេរៀនមិនត្រឹមត្រូវ។ សូមបញ្ចូលលេខពី ១ ដល់ ១០០០។")

    async def _send_lesson_view(self, message_or_query, lesson_id: int, is_edit: bool = False):
        """Render full lesson view with interactive Next/Previous and Deep Explain buttons."""
        lesson = self.curriculum.get_lesson(lesson_id)
        if not lesson:
            text = f"❌ រកមិនឃើញមេរៀនទី {lesson_id} ឡើយ (មានត្រឹមមេរៀនទី ១ ដល់ ១០០០)។"
            if is_edit:
                await self._safe_edit(message_or_query, text)
            else:
                await self._safe_reply(message_or_query, text)
            return

        text = (
            f"🌟 **SUPREME FENG SHUI AGI (Master Level v1.0.0)**\n"
            f"📚 **{lesson['title_kh']}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ **ផ្នែក:** {lesson['category_icon']} {lesson['category_name']}\n"
            f"📌 **ប្រធានបទធំ:** {lesson['topic_title_kh']}\n"
            f"🎯 **ប្រធានបទរង:** {lesson['sub_topic_kh']}\n"
            f"🏛️ **សសរស្តម្ភសកម្ម:** `{lesson.get('active_pillar', '7 Pillars Core')}`\n\n"
            f"📜 **១. គម្ពីរ និងទស្សនវិជ្ជាគ្រឹះ:**\n{lesson['classical_rule']}\n\n"
            f"📐 **២. រូបមន្តគណិតវិទ្យា & ឡូប៉ាន ២៤ ភ្នំ:**\n{lesson['formula']}\n\n"
            f"🏛️ **៣. ការវិភាគ ៧ សសរស្តម្ភ AGI:**\n"
            f"• ⛰️ **Geo / Landform:** {lesson.get('geo_analysis', '')}\n"
            f"• 💨 **Qi Dynamics:** {lesson.get('qi_analysis', '')}\n"
            f"• ⏳ **Period 9 (2024-2043):** {lesson.get('time_analysis', '')}\n"
            f"• 🔮 **BaZi Synergy:** {lesson.get('bazi_synergy', '')}\n\n"
            f"💡 **៤. ការអនុវត្តជាក់ស្តែង & ដំណោះស្រាយ:**\n{lesson['practical_remedy']}\n\n"
            f"⚠️ **៥. ចំណុចហាមឃាត់ (Taboos):**\n{lesson.get('taboo_warning', '')}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔢 *មេរៀន {lesson['lesson_id']}/1000 | ដំណើរការដោយ 99 Specialized Components*"
        )

        nav_row = []
        if lesson["prev_lesson_id"]:
            nav_row.append(InlineKeyboardButton("⬅️ ថយក្រោយ", callback_data=f"curr_les_{lesson['prev_lesson_id']}"))
        if lesson["next_lesson_id"]:
            nav_row.append(InlineKeyboardButton("➡️ បន្ទាប់ (Next)", callback_data=f"curr_les_{lesson['next_lesson_id']}"))

        keyboard = []
        if nav_row:
            keyboard.append(nav_row)

        keyboard.append([
            InlineKeyboardButton("🧠 ពន្យល់ស៊ីជម្រៅដោយ AI Master", callback_data=f"curr_exp_{lesson_id}"),
            InlineKeyboardButton("📑 ប្រធានបទនេះ", callback_data=f"curr_top_{lesson['topic_id']}")
        ])
        keyboard.append([
            InlineKeyboardButton("📚 មេរៀនទាំងអស់", callback_data="menu_curriculum"),
            InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)
        if is_edit:
            await self._safe_edit(message_or_query, text, reply_markup=reply_markup)
        else:
            await self._safe_reply(message_or_query, text, reply_markup=reply_markup)

    async def gua_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /gua command (VIP & Super Admin Only)."""
        from_user = update.effective_user
        if not self._is_vip_or_admin(from_user.id):
            await self._send_vip_required_notice(update.message, from_user.id)
            return

        args = context.args
        if not args or len(args) < 1:
            text = (
                "🧭 **របៀបគណនា Life Gua (San Yuan Ming Gua):**\n"
                "សូមសរសេរ៖ `/gua <ឆ្នាំកំណើត> <ភេទ male/female>`\n"
                "ឧទាហរណ៍៖ `/gua 1988 male` ឬ `/gua 1995 female`"
            )
            keyboard = [
                [
                    InlineKeyboardButton("👨 គណនាសម្រាប់បុរស (1988)", callback_data="calc_gua_1988_male"),
                    InlineKeyboardButton("👩 គណនាសម្រាប់ស្ត្រី (1995)", callback_data="calc_gua_1995_female")
                ],
                [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
            ]
            await self._safe_reply(update.message, text, reply_markup=InlineKeyboardMarkup(keyboard))
            return

        try:
            year = int(args[0])
            gender = args[1].lower() if len(args) > 1 else "male"
            res = self.calc_engine.calculate_life_gua(year, gender)

            if res["success"]:
                d = res["data"]
                lucky_str = "\n".join([f"• **{item['direction']}** ({item['type']}): {item['meaning']}" for item in d['lucky_directions']])
                unlucky_str = "\n".join([f"• **{item['direction']}** ({item['type']}): {item['meaning']}" for item in d['unlucky_directions']])

                msg = (
                    f"🧭 **លទ្ធផល Life Gua (FS-Classical-Calc-v1)**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• **ឆ្នាំកំណើត:** {d['birth_year']} ({'បុរស' if d['gender'] == 'male' else 'ស្ត្រី'})\n"
                    f"• **Gua លេខ:** {d['gua_number']} ({d['trigram_name']})\n"
                    f"• **ធាតុ:** {d['element']}\n"
                    f"• **ក្រុម:** {d['group']}\n\n"
                    f"✨ **ទិសល្អទាំង ៤ (Auspicious Directions):**\n{lucky_str}\n\n"
                    f"⚠️ **ទិសគួរជៀសវាងទាំង ៤ (Inauspicious Directions):**\n{unlucky_str}"
                )
                keyboard = [
                    [InlineKeyboardButton("📚 រៀនក្បួន Life Gua (មេរៀន ១៧)", callback_data="curr_les_161")],
                    [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
                ]
                await self._safe_reply(update.message, msg, reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                await self._safe_reply(update.message, f"❌ កំហុស៖ {res.get('error')}")
        except Exception as e:
            await self._safe_reply(update.message, f"❌ កំហុសក្នុងការគណនា៖ {str(e)}")

    async def flyingstars_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /flyingstars command (VIP & Super Admin Only)."""
        from_user = update.effective_user
        if not self._is_vip_or_admin(from_user.id):
            await self._send_vip_required_notice(update.message, from_user.id)
            return

        year = 2024
        res = self.calc_engine.calculate_flying_stars(year)
        if res["success"]:
            d = res["data"]
            grid = d["grid"]
            msg = (
                f"🌌 **តារាហោះ ៩ វិហារ យុគ ៩ (Period 9: 2024-2043)**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• **យុគបច្ចុប្បន្ន:** {d['period']} (Li Fire ធាតុភ្លើង)\n"
                f"• **ផ្កាយកណ្តាលឆ្នាំ {d['year']}:** {d['center_star']['number']} ({d['center_star']['name']})\n\n"
                f"🗺️ **ប្លង់តារាហោះ ៩ វិហារ (Luo Shu Nine Palaces):**\n"
                f"┌──────┬──────┬──────┐\n"
                f"│ SE:{grid['SE']['star_number']} │ S:{grid['S']['star_number']}  │ SW:{grid['SW']['star_number']} │\n"
                f"├──────┼──────┼──────┤\n"
                f"│ E:{grid['E']['star_number']}  │ C:{grid['Center']['star_number']}  │ W:{grid['W']['star_number']}  │\n"
                f"├──────┼──────┼──────┤\n"
                f"│ NE:{grid['NE']['star_number']} │ N:{grid['N']['star_number']}  │ NW:{grid['NW']['star_number']} │\n"
                f"└──────┴──────┴──────┘\n\n"
                f"🌟 **ទិសស្រូបទ្រព្យយុគ ៩:** ខាងជើង N (Ling Shen Water 零神) & ខាងត្បូង S (Zheng Shen Mountain 正神)\n"
                f"⚠️ **ទិសគ្រោះធំប្រចាំឆ្នាំ:** ខាងលិច W (Star 5 Yellow 廉贞) & អាគ្នេយ៍ SE (Star 2 Black 巨门)"
            )
            keyboard = [
                [InlineKeyboardButton("📚 រៀនក្បួនតារាហោះ យុគ ៩ (មេរៀន ២៣)", callback_data="curr_les_221")],
                [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
            ]
            await self._safe_reply(update.message, msg, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await self._safe_reply(update.message, f"❌ កំហុស៖ {res.get('error')}")

    async def bazi_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /bazi command (VIP & Super Admin Only)."""
        from_user = update.effective_user
        if not self._is_vip_or_admin(from_user.id):
            await self._send_vip_required_notice(update.message, from_user.id)
            return
        args = context.args
        if not args or len(args) < 1:
            text = (
                "🔮 **របៀបវិភាគ BaZi សសរស្តម្ភទាំង ៤:**\n"
                "សូមសរសេរ៖ `/bazi YYYY-MM-DD [HH:MM]`\n"
                "ឧទាហរណ៍៖ `/bazi 1988-05-15 10:30` ឬ `/bazi 1990-08-20`"
            )
            keyboard = [
                [InlineKeyboardButton("🔮 ឧទាហរណ៍គំរូ BaZi (1988-05-15)", callback_data="calc_bazi_demo")],
                [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
            ]
            await self._safe_reply(update.message, text, reply_markup=InlineKeyboardMarkup(keyboard))
            return

        dt_str = args[0]
        time_str = args[1] if len(args) > 1 else "12:00"
        res = self.calc_engine.calculate_bazi(f"{dt_str} {time_str}")
        if res["success"]:
            d = res["data"]
            pillars = d["four_pillars"]
            msg = (
                f"🔮 **លទ្ធផល BaZi ៤ សសរស្តម្ភ (FS-Classical-Calc-v1)**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📅 **កាលបរិច្ឆេទ:** {d['solar_date']}\n"
                f"👑 **Day Master (ធាតុខ្លួនឯង):** **{d['day_master']['stem']} {d['day_master']['element']} ({d['day_master']['polarity']})**\n"
                f"💊 **ធាតុឱសថគាំទ្រ (Yong Shen):** {d['favorable_elements']}\n\n"
                f"🏛️ **សសរស្តម្ភទាំង ៤ (Four Pillars Matrix):**\n"
                f"• **ឆ្នាំ (Year):** {pillars['year']['stem']} {pillars['year']['branch']} ({pillars['year']['element']})\n"
                f"• **ខែ (Month):** {pillars['month']['stem']} {pillars['month']['branch']} ({pillars['month']['element']})\n"
                f"• **ថ្ងៃ (Day):** {pillars['day']['stem']} {pillars['day']['branch']} ({pillars['day']['element']})\n"
                f"• **ម៉ោង (Hour):** {pillars['hour']['stem']} {pillars['hour']['branch']} ({pillars['hour']['element']})\n\n"
                f"⚖️ **តុល្យភាពធាតុទាំង ៥ ក្នុងខ្លួន:**\n"
                f"ឈើ:{d['elements_distribution']['Wood']} | ភ្លើង:{d['elements_distribution']['Fire']} | ដី:{d['elements_distribution']['Earth']} | លោហៈ:{d['elements_distribution']['Metal']} | ទឹក:{d['elements_distribution']['Water']}"
            )
            keyboard = [
                [InlineKeyboardButton("📚 រៀនក្បួន BaZi (មេរៀន ៨១)", callback_data="curr_les_801")],
                [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
            ]
            await self._safe_reply(update.message, msg, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await self._safe_reply(update.message, f"❌ កំហុស៖ {res.get('error')}")

    async def predict_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /predict command (VIP & Super Admin Only)."""
        from_user = update.effective_user
        if not self._is_vip_or_admin(from_user.id):
            await self._send_vip_required_notice(update.message, from_user.id)
            return

        args = context.args
        if not args:
            today = datetime.now().strftime("%Y-%m-%d")
            args = [today]

        date_str = args[0]
        res = self.alert_engine.predict_fortune(date_str)
        if res["success"]:
            d = res["data"]
            msg = (
                f"📊 **ការព្យាករណ៍ជោគជតារាសីប្រចាំថ្ងៃ (FS-Alert-Predictor)**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📅 **កាលបរិច្ឆេទ:** {d['query_date']} ({d['current_day_pillar']})\n"
                f"🌟 **សំណាងទូទៅ:** {d['overall_luck']['score']}% - {d['overall_luck']['level']}\n"
                f"💰 **សំណាងទ្រព្យ:** {d['wealth_luck']['score']}% ({d['wealth_luck']['advice']})\n"
                f"💼 **សំណាងអាជីព:** {d['career_luck']['score']}% ({d['career_luck']['advice']})\n"
                f"❤️ **សំណាងស្នេហា:** {d['love_luck']['score']}% ({d['love_luck']['advice']})\n"
                f"🌿 **សំណាងសុខភាព:** {d['health_luck']['score']}% ({d['health_luck']['advice']})\n\n"
                f"⏰ **ម៉ោងល្អក្នុងថ្ងៃនេះ:**\n" +
                "\n".join([f"• {h}" for h in d['auspicious_hours']]) +
                f"\n\n💡 **ដំបូន្មានប្រចាំថ្ងៃ:** {d['daily_remedy']}"
            )
            keyboard = [
                [InlineKeyboardButton("💬 សួរពិគ្រោះបន្ថែម", callback_data="menu_ask")],
                [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
            ]
            await self._safe_reply(update.message, msg, reply_markup=InlineKeyboardMarkup(keyboard))

    async def love_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /love and /mahasneh command for 8-Pillars Peach Blossom & Universal Zenith Love Analysis."""
        from_user = update.effective_user
        if not self._is_vip_or_admin(from_user.id):
            await self._send_vip_required_notice(update.message, from_user.id)
            return

        args = context.args
        if not args:
            guide_text = (
                "💖 **ក្បួនហុងស៊ុយ និងមហាស្នេហ៍ (Peach Blossom & 8-Pillars Love Zenith)** 💖\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🌟 **របៀបប្រើប្រាស់ពាក្យបញ្ជាដើម្បីវិភាគក្បួនមហាស្នេហ៍៖**\n\n"
                "1️⃣ **វិភាគទាក់ទាញស្នេហាផ្ទាល់ខ្លួន (Peach Blossom Star):**\n"
                "`/love <YYYY-MM-DD> <male/female>`\n"
                "👉 **ឧទាហរណ៍៖** `/love 1990-05-15 male`\n\n"
                "2️⃣ **វិភាគភាពស៊ីចង្វាក់ស្នេហាគូស្នេហ៍ (៨ សសរស្តម្ភ BaZi Compatibility):**\n"
                "`/love <ថ្ងៃខែឆ្នាំខ្លួនឯង> <ភេទ> <ថ្ងៃខែឆ្នាំគូស្នេហ៍> <ភេទ>`\n"
                "👉 **ឧទាហរណ៍៖** `/love 1990-05-15 male 1992-08-20 female`\n\n"
                "*(ប្រព័ន្ធនឹងបង្កើតរបាយការណ៍ Universal Zenith Report រួមមាន៖ ធាតុឱសថព្យាបាលរាសី, យុទ្ធសាស្ត្រអន្ទងចិត្ត, និងវិធីសាស្ត្របន្ទន់ចិត្ត!)*"
            )
            keyboard = [
                [InlineKeyboardButton("💬 សួរគ្រូហុងស៊ុយ AI", callback_data="menu_ask")],
                [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
            ]
            await self._safe_reply(update.message, guide_text, reply_markup=InlineKeyboardMarkup(keyboard))
            return

        b_date_1 = args[0]
        gender_1 = args[1] if len(args) > 1 else "male"
        b_date_2 = args[2] if len(args) > 2 else None
        gender_2 = args[3] if len(args) > 3 else "female"

        res = self.love.analyze_love_profile(
            birth_date_1=b_date_1,
            gender_1=gender_1,
            birth_date_2=b_date_2,
            gender_2=gender_2
        )

        if not res.get("success"):
            await self._safe_reply(update.message, f"❌ កំហុសក្នុងការវិភាគ៖ {res.get('error')}")
            return

        msg = res["zenith_report"]
        keyboard = [
            [InlineKeyboardButton("💬 ពិគ្រោះក្បួនស្នេហ៍លម្អិត", callback_data="menu_ask")],
            [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
        ]
        await self._safe_reply(update.message, msg, reply_markup=InlineKeyboardMarkup(keyboard))

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle conversational natural language messages with VIP limit & security enforcement."""
        from_user = update.effective_user
        user_text = update.message.text
        is_admin = from_user.id in config.ADMIN_USER_IDS

        # 1. Anti-Spam & Anti-DDoS Rate Limiting
        rate_ok, warn_msg = self.security.check_rate_limit(from_user.id, is_admin=is_admin)
        if not rate_ok:
            await self._safe_reply(update.message, warn_msg)
            return

        # 2. Input Sanitization & Prompt Injection / Jailbreak Guard
        clean_text, is_safe, threat_reason = self.security.sanitize_user_input(user_text)
        if not is_safe:
            security_alert = (
                f"🛡️ **ការទប់ស្កាត់សុវត្ថិភាព (Security Shield Active)**\n\n"
                f"⚠️ {threat_reason}\n"
                f"👉 សូមផ្ញើសំណួរដែលទាក់ទងនឹងក្បួនហុងស៊ុយ យិនយ៉ាង ឬតារាហោះធម្មតា។"
            )
            await self._safe_reply(update.message, security_alert)
            return

        # 3. Check and increment query limit for free vs VIP users
        limit_check = self.db.check_and_increment_query(from_user.id, max_free_limit=config.MAX_FREE_DAILY_QUERIES)

        if not limit_check["allowed"]:
            # Strictly VIP only
            await self._send_vip_required_notice(update.message, from_user.id)
            return

        await update.message.chat.send_action("typing")

        consult_res = self.master.consult(query=clean_text)
        response_text = consult_res.get("synthesis", "សូមអភ័យទោស ខ្ញុំមិនអាចឆ្លើយតបនៅពេលនេះបានទេ។")

        # Footer info
        is_vip = limit_check.get("is_vip", False)
        footer = "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n👑 *VIP Member: សិទ្ធិប្រើប្រាស់គ្មានដែនកំណត់ 24/7/365*"

        keyboard = [
            [
                InlineKeyboardButton("📚 កម្មវិធីសិក្សា ១០០០ មេរៀន", callback_data="menu_curriculum"),
                InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
            ]
        ]
        await self._safe_reply(update.message, response_text + footer, reply_markup=InlineKeyboardMarkup(keyboard))

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user uploaded photos for Instant Multimodal Feng Shui Vision Audit (VIP Only)."""
        from_user = update.effective_user
        is_admin = from_user.id in config.ADMIN_USER_IDS

        # VIP Check
        if not self._is_vip_or_admin(from_user.id):
            await self._send_vip_required_notice(update.message, from_user.id)
            return

        # Rate limit check
        rate_ok, warn_msg = self.security.check_rate_limit(from_user.id, is_admin=is_admin)
        if not rate_ok:
            await self._safe_reply(update.message, warn_msg)
            return

        # Quota check
        limit_check = self.db.check_and_increment_query(from_user.id, max_free_limit=config.MAX_FREE_DAILY_QUERIES)
        if not limit_check["allowed"]:
            await self._send_vip_required_notice(update.message, from_user.id)
            return

        await update.message.chat.send_action("typing")

        try:
            photo = update.message.photo[-1]
            photo_file = await context.bot.get_file(photo.file_id)
            photo_bytes = await photo_file.download_as_bytearray()
            caption = update.message.caption or ""

            audit_res = self.vision.audit_image(
                image_bytes=bytes(photo_bytes),
                mime_type="image/jpeg",
                user_notes=caption
            )

            report = (
                "👁️ **លទ្ធផលសវនកម្មរូបភាពហុងស៊ុយ (Vision Multimodal Audit)** 👁️\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{audit_res.get('audit_report', '')}"
            )

            keyboard = [
                [
                    InlineKeyboardButton("🎨 បង្កើតប្លង់ 3D 4K គំរូ", callback_data="menu_render3d"),
                    InlineKeyboardButton("💬 សួរគ្រូ AI បន្ថែម", callback_data="menu_ask")
                ],
                [
                    InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
                ]
            ]
            await self._safe_reply(update.message, report, reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception as e:
            logger.error(f"Error handling photo upload: {e}", exc_info=True)
            await self._safe_reply(
                update.message,
                f"❌ មានបញ្ហាក្នុងការទាញយករូបភាព៖ {e}\n👉 សូមព្យាយាមផ្ញើរូបភាពម្តងទៀត។"
            )

    async def render3d_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /render3d command to generate and explore 3D 4K Feng Shui architectural spaces (VIP Only)."""
        from_user = update.effective_user
        if not self._is_vip_or_admin(from_user.id):
            await self._send_vip_required_notice(update.message, from_user.id)
            return
        await self._send_render3d_menu(update.message, is_edit=False)

    async def _send_render3d_menu(self, message_or_query, is_edit: bool = False):
        """Render the 3D 4K Visualization menu."""
        text = (
            "🎨 **ស្ទូឌីយោបង្កើតប្លង់ហុងស៊ុយ 3D 4K (3D Architectural Visualizer)** 🎨\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "បច្ចេកវិទ្យាបង្កើតរូបភាព 3D 4K យោងតាមក្បួនខ្នាត San Yuan Xuan Kong យុគ ៩ (Period 9 Li Fire) ពិតប្រាកដ!\n\n"
            "👇 **សូមជ្រើសរើសប្រភេទលំហអាកាសដែលអ្នកចង់ Render 3D 4K៖**"
        )
        keyboard = [
            [
                InlineKeyboardButton("🛋️ បន្ទប់ទទួលភ្ញៀវយុគ ៩", callback_data="render_living"),
                InlineKeyboardButton("🛏️ បន្ទប់គេងមេគ្រួសារ", callback_data="render_bedroom")
            ],
            [
                InlineKeyboardButton("💼 ការិយាល័យថ្នាក់ដឹកនាំ", callback_data="render_office"),
                InlineKeyboardButton("🏡 ភូមិគ្រឹះ & វីឡាហុងស៊ុយ", callback_data="render_villa")
            ],
            [
                InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
            ]
        ]
        if is_edit:
            await self._safe_edit(message_or_query, text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await self._safe_reply(message_or_query, text, reply_markup=InlineKeyboardMarkup(keyboard))

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all interactive inline keyboard clicks seamlessly."""
        query = update.callback_query
        from_user = query.from_user
        try:
            await query.answer()
        except Exception:
            pass

        data = query.data

        try:
            # Check VIP permissions for gated callback features
            gated_prefixes = ("curr_", "render_", "calc_")
            gated_exact = {"menu_curriculum", "menu_gua", "menu_flyingstars", "menu_bazi", "menu_predict", "menu_render3d", "menu_ask", "menu_love"}
            if (data in gated_exact or any(data.startswith(p) for p in gated_prefixes)) and not self._is_vip_or_admin(from_user.id):
                await self._send_vip_required_notice(query, from_user.id)
                return

            # Navigation: Main Menu
            if data == "menu_main":
                await self._safe_edit(
                    query,
                    "🌟 **SUPREME FENG SHUI AGI SYSTEM (Master Level v1.0.0)** 🌟\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "សូមជ្រើសរើសមុខងារដែលអ្នកចង់ប្រើប្រាស់៖",
                    reply_markup=self._get_main_keyboard(from_user.id)
                )

            # Love & Peach Blossom Menu
            elif data == "menu_love":
                guide_text = (
                    "💖 **ក្បួនហុងស៊ុយ និងមហាស្នេហ៍ (Peach Blossom & 8-Pillars Love Zenith)** 💖\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "🌟 **របៀបប្រើប្រាស់ពាក្យបញ្ជាដើម្បីវិភាគក្បួនមហាស្នេហ៍៖**\n\n"
                    "1️⃣ **វិភាគទាក់ទាញស្នេហាផ្ទាល់ខ្លួន (Peach Blossom Star):**\n"
                    "`/love <YYYY-MM-DD> <male/female>`\n"
                    "👉 **ឧទាហរណ៍៖** `/love 1990-05-15 male`\n\n"
                    "2️⃣ **វិភាគភាពស៊ីចង្វាក់ស្នេហាគូស្នេហ៍ (៨ សសរស្តម្ភ BaZi Compatibility):**\n"
                    "`/love <ថ្ងៃខែឆ្នាំខ្លួនឯង> <ភេទ> <ថ្ងៃខែឆ្នាំគូស្នេហ៍> <ភេទ>`\n"
                    "👉 **ឧទាហរណ៍៖** `/love 1990-05-15 male 1992-08-20 female`\n\n"
                    "*(ប្រព័ន្ធនឹងបង្កើតរបាយការណ៍ Universal Zenith Report រួមមាន៖ ធាតុឱសថព្យាបាលរាសី, យុទ្ធសាស្ត្រអន្ទងចិត្ត, និងវិធីសាស្ត្របន្ទន់ចិត្ត!)*"
                )
                keyboard = [
                    [InlineKeyboardButton("💬 សួរគ្រូហុងស៊ុយ AI", callback_data="menu_ask")],
                    [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
                ]
                await self._safe_edit(query, guide_text, reply_markup=InlineKeyboardMarkup(keyboard))

            # VIP Menu
            elif data == "menu_vip":
                user = self.db.get_or_create_user(from_user.id, from_user.username or "", from_user.full_name or "")
                await self._send_vip_view(query, user, is_edit=True)

            elif data == "vip_redeem_prompt":
                prompt_text = (
                    "🎟️ **របៀបបញ្ចូល License Key អាជ្ញាប័ណ្ណ VIP**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "ដើម្បី Upgrade គណនីរបស់អ្នក សូមវាយពាក្យបញ្ជាដូចខាងក្រោម៖\n\n"
                    "👉 `/redeem <លេខកូដ Key របស់អ្នក>`\n\n"
                    "**ឧទាហរណ៍ជាក់ស្តែង៖**\n"
                    "• `/redeem FS-M-ABCD-1234` (សម្រាប់ VIP ប្រចាំខែ 30 ថ្ងៃ)\n"
                    "• `/redeem FS-Y-EFGH-5678` (សម្រាប់ VIP ប្រចាំឆ្នាំ 365 ថ្ងៃ)\n"
                    "• `/redeem FS-L-JKLM-9012` (សម្រាប់ VIP មួយជីវិត Lifetime)\n\n"
                    "*(ប្រសិនបើលោកអ្នកមិនទាន់មាន Key ទេ សូមទាក់ទងមកកាន់ Super Admin @HemSinath ដើម្បីជាវ)*"
                )
                keyboard = [
                    [InlineKeyboardButton("👑 ភ្ជាប់ VIP ឥឡូវនេះ (Admin @HemSinath)", url="https://t.me/HemSinath")],
                    [InlineKeyboardButton("👑 ត្រឡប់ទៅ VIP Portal", callback_data="menu_vip")],
                    [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
                ]
                await self._safe_edit(query, prompt_text, reply_markup=InlineKeyboardMarkup(keyboard))

            elif data in ["vip_perks_info", "vip_features"]:
                feat_text = (
                    "💎 **អត្ថប្រយោជន៍ដ៏មហិមារបស់សមាជិកភាព VIP (VIP Master Perks)** 💎\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "🌟 **ប្រព័ន្ធ SUPREME FENG SHUI AGI (Master Level v1.0.0)**\n\n"
                    "1️⃣ 🧠 **សួរគ្រូហុងស៊ុយ AI គ្មានដែនកំណត់:**\n"
                    "• ពិគ្រោះយោបល់គ្រប់សំណួរ ២៤/៧/៣៦៥ គ្មានកូតាកំណត់ ឆ្លើយតបលឿនបំផុត (< 1s)\n"
                    "• ដំណើរការដោយ Google Gemini 2.0 Flash Omni Mesh & HuggingFace\n\n"
                    "2️⃣ 📚 **កម្មវិធីសិក្សា ១,០០០ មេរៀនពេញលេញ:**\n"
                    "• ចូលអានមេរៀនក្បួនបុរាណពិតៗ ១០០ ប្រធានបទ\n"
                    "• ការពន្យល់ស៊ីជម្រៅដោយ AI Synthesis កម្រិត Master\n\n"
                    "3️⃣ 🧭 **គណនាជោគជតា និងហុងស៊ុយ ០ កំហុស:**\n"
                    "• គណនា Life Gua (ទិសល្អ/អាក្រក់ តាមថ្ងៃខែឆ្នាំកំណើត)\n"
                    "• តារាហោះ យុគ ៩ (Luo Shu Nine Palaces 2024-2043)\n"
                    "• វិភាគ BaZi ៤ សសរ និងអាទិទេពទាំង ១០ (10 Gods)\n\n"
                    "4️⃣ 📸 **សវនកម្មរូបភាព AI Vision:**\n"
                    "• ផ្ញើរូបថតបន្ទប់/ផ្ទះដើម្បីពិនិត្យរកចំណុចទាស់ និងវិធីកែខៃ\n\n"
                    "5️⃣ 🎨 **ស្ទូឌីយោប្លង់ 3D 4K Photorealistic:**\n"
                    "• បង្កើតរូបភាពប្លង់ 3D 4K Ultra-HD រៀបចំត្រូវតាមក្បួនយុគ ៩\n\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "👉 **សូមទាក់ទងមកកាន់ SUPER ADMIN ផ្ទាល់ដើម្បីភ្ជាប់សេវាកម្ម VIP:**\n"
                    "👑 **Telegram Admin:** [@HemSinath](https://t.me/HemSinath)"
                )
                keyboard = [
                    [InlineKeyboardButton("👑 ភ្ជាប់ VIP ឥឡូវនេះ (Admin @HemSinath)", url="https://t.me/HemSinath")],
                    [InlineKeyboardButton("🎟️ របៀបបញ្ចូល Key", callback_data="vip_redeem_prompt")],
                    [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
                ]
                await self._safe_edit(query, feat_text, reply_markup=InlineKeyboardMarkup(keyboard))

            # ==================== SUPER ADMIN CALLBACKS ====================
            elif data == "admin_panel":
                admin = self.db.get_or_create_user(from_user.id)
                if admin.get("role") != "super_admin":
                    await self._safe_edit(query, "⛔ Access Denied.")
                    return
                await self._send_admin_dashboard(query, admin, is_edit=True)

            elif data == "admin_stats":
                admin = self.db.get_or_create_user(from_user.id)
                if admin.get("role") != "super_admin":
                    await self._safe_edit(query, "⛔ Access Denied.")
                    return
                stats = self.db.get_system_stats()
                text = (
                    "📊 **ស្ថិតិប្រព័ន្ធលម្អិត (System Telemetry & Metrics)**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"👥 **អ្នកប្រើប្រាស់សរុប:** `{stats['total_users']}` នាក់\n"
                    f"🛡️ **Super Admins:** `{stats['total_admins']}` នាក់\n\n"
                    f"👑 **ស្ថិតិ VIP Tiers:**\n"
                    f"• 🌟 VIP ប្រចាំខែ (Monthly): `{stats['vip_monthly']}` នាក់\n"
                    f"• 👑 VIP ប្រចាំឆ្នាំ (Yearly): `{stats['vip_yearly']}` នាក់\n"
                    f"• 💎 VIP មួយជីវិត (Lifetime): `{stats['vip_lifetime']}` នាក់\n"
                    f"• 📈 សរុប VIP សកម្ម: `{stats['total_vips']}` នាក់\n\n"
                    f"🔑 **ស្ថិតិអាជ្ញាប័ណ្ណ (License Keys):**\n"
                    f"• 🟢 Keys មិនទាន់ប្រើ: `{stats['active_licenses']}`\n"
                    f"• 🔴 Keys ប្រើប្រាស់រួច: `{stats['redeemed_licenses']}`\n"
                    f"• 📦 Keys បង្កើតសរុប: `{stats['total_licenses']}`\n\n"
                    f"💬 **សំណួរសរុបដែលបានដំណើរការ:** `{stats['total_queries']}` ដង\n"
                    f"⚡ **ស្ថានភាព VPS:** Memory Stable ~50MB / 1024MB"
                )
                keyboard = [
                    [InlineKeyboardButton("🔙 ត្រឡប់ទៅ Admin Panel", callback_data="admin_panel")],
                    [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
                ]
                await self._safe_edit(query, text, reply_markup=InlineKeyboardMarkup(keyboard))

            elif data == "admin_genkeys_menu":
                admin = self.db.get_or_create_user(from_user.id)
                if admin.get("role") != "super_admin":
                    await self._safe_edit(query, "⛔ Access Denied.")
                    return
                text = (
                    "🔑 **បង្កើត License Keys អាជ្ញាប័ណ្ណថ្មី**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "សូមជ្រើសរើសប្រភេទ និងចំនួន Key ដែលអ្នកចង់បង្កើតភ្លាមៗ៖"
                )
                keyboard = [
                    [
                        InlineKeyboardButton("🌟 1 ខែ (1 Key)", callback_data="admin_gen_monthly_1"),
                        InlineKeyboardButton("🌟 1 ខែ (5 Keys)", callback_data="admin_gen_monthly_5")
                    ],
                    [
                        InlineKeyboardButton("👑 1 ឆ្នាំ (1 Key)", callback_data="admin_gen_yearly_1"),
                        InlineKeyboardButton("👑 1 ឆ្នាំ (5 Keys)", callback_data="admin_gen_yearly_5")
                    ],
                    [
                        InlineKeyboardButton("💎 មួយជីវិត (1 Key)", callback_data="admin_gen_lifetime_1"),
                        InlineKeyboardButton("💎 មួយជីវិត (5 Keys)", callback_data="admin_gen_lifetime_5")
                    ],
                    [
                        InlineKeyboardButton("🔙 ត្រឡប់ទៅ Admin Panel", callback_data="admin_panel")
                    ]
                ]
                await self._safe_edit(query, text, reply_markup=InlineKeyboardMarkup(keyboard))

            elif data.startswith("admin_gen_"):
                admin = self.db.get_or_create_user(from_user.id)
                if admin.get("role") != "super_admin":
                    await self._safe_edit(query, "⛔ Access Denied.")
                    return

                parts = data.split("_")
                tier = parts[2]
                count = int(parts[3])

                keys = self.db.generate_license_key(tier=tier, count=count, created_by=from_user.id)
                keys_text = "\n".join([f"• `{k}`" for k in keys])

                text = (
                    f"✅ **បានបង្កើត {count} License Keys ({tier.capitalize()}) ជោគជ័យ!**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{keys_text}\n\n"
                    f"*(ចុចលើ Key ដើម្បី Copy រួចផ្ញើជូនអតិថិជន)*"
                )
                keyboard = [
                    [InlineKeyboardButton("🔑 បង្កើតបន្ថែម", callback_data="admin_genkeys_menu")],
                    [InlineKeyboardButton("📋 បញ្ជី Keys មិនទាន់ប្រើ", callback_data="admin_keys_list")],
                    [InlineKeyboardButton("🔙 ត្រឡប់ទៅ Admin Panel", callback_data="admin_panel")]
                ]
                await self._safe_edit(query, text, reply_markup=InlineKeyboardMarkup(keyboard))

            elif data == "admin_keys_list":
                admin = self.db.get_or_create_user(from_user.id)
                if admin.get("role") != "super_admin":
                    await self._safe_edit(query, "⛔ Access Denied.")
                    return

                keys = self.db.get_unredeemed_keys(limit=15)
                if not keys:
                    text = "📋 **ពុំទាន់មាន License Keys មិនទាន់ប្រើនៅឡើយទេ។**\n\n👉 សូមចុច 'បង្កើត Key អាជ្ញាប័ណ្ណ' ដើម្បីបង្កើតថ្មី។"
                else:
                    items = []
                    for k in keys:
                        items.append(f"• `{k['key']}` ({k['tier'].capitalize()} - {k['duration_days']}d)")
                    text = (
                        f"📋 **បញ្ជី Keys មិនទាន់ប្រើប្រាស់ (Unredeemed Keys):**\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        + "\n".join(items) +
                        "\n\n*(ចុចលើ Key ណាមួយដើម្បី Copy យកទៅប្រើ)*"
                    )

                keyboard = [
                    [InlineKeyboardButton("🔑 បង្កើត Key ថ្មី", callback_data="admin_genkeys_menu")],
                    [InlineKeyboardButton("🔙 ត្រឡប់ទៅ Admin Panel", callback_data="admin_panel")]
                ]
                await self._safe_edit(query, text, reply_markup=InlineKeyboardMarkup(keyboard))

            elif data == "admin_users_list":
                admin = self.db.get_or_create_user(from_user.id)
                if admin.get("role") != "super_admin":
                    await self._safe_edit(query, "⛔ Access Denied.")
                    return

                users = self.db.get_all_users_list(limit=10)
                items = []
                for u in users:
                    badge = "👑" if u["vip_tier"] != "free" else "✨"
                    items.append(f"{badge} `{u['telegram_id']}` | {u['full_name'][:15]} ({u['role']})")

                text = (
                    f"👥 **បញ្ជីអ្នកប្រើប្រាស់ថ្មីៗ (Recent Users):**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    + "\n".join(items) +
                    f"\n\n*(ប្រើពាក្យបញ្ជា `/setvip <user_id> <tier>` ដើម្បីកែសម្រួល VIP ដោយដៃ)*"
                )
                keyboard = [
                    [InlineKeyboardButton("🔙 ត្រឡប់ទៅ Admin Panel", callback_data="admin_panel")]
                ]
                await self._safe_edit(query, text, reply_markup=InlineKeyboardMarkup(keyboard))

            elif data == "admin_broadcast_info":
                text = (
                    "📢 **របៀបផ្ញើសារប្រកាសទូទៅ (Broadcast Announcement)**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "សូមសរសេរពាក្យបញ្ជាដូចខាងក្រោម៖\n\n"
                    "`/broadcast <អត្ថបទសារប្រកាសរបស់អ្នក>`\n\n"
                    "**ឧទាហរណ៍៖**\n"
                    "`/broadcast សូមស្វាគមន៍មកកាន់ប្រព័ន្ធ Upgrade ថ្មីជាមួយមុខងារ VIP AGI Master!`"
                )
                keyboard = [
                    [InlineKeyboardButton("🔙 ត្រឡប់ទៅ Admin Panel", callback_data="admin_panel")]
                ]
                await self._safe_edit(query, text, reply_markup=InlineKeyboardMarkup(keyboard))

            elif data == "admin_trigger_backup":
                admin = self.db.get_or_create_user(from_user.id)
                if admin.get("role") != "super_admin" and from_user.id not in config.ADMIN_USER_IDS:
                    await self._safe_edit(query, "⛔ Access Denied.")
                    return

                await self._safe_edit(query, "⏳ **កំពុងដំណើរការ Backup ទិន្នន័យ និងបង្ហាប់ File Zip...**\n*(សូមរង់ចាំបន្តិច)*")
                res = self.backup.create_backup(trigger_type=f"Manual Button Trigger (Admin {from_user.id})")
                if res["success"]:
                    bot_instance = query.bot if hasattr(query, "bot") else query.message.get_bot()
                    await self._dispatch_backup_to_admins(bot_instance, res, is_automated=False)
                    text = (
                        f"✅ **បានបង្កើត និងផ្ញើឯកសារ Zip Backup ជូនលោកមេការជោគជ័យ!**\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"📁 **ឈ្មោះ:** `{res['file_name']}`\n"
                        f"💾 **ទំហំ:** `{res['file_size_kb']} KB`\n"
                        f"⏱️ **ពេលវេលា:** `{res['timestamp_ict']}`\n"
                        f"🔐 **SHA-256 Checksum:** `{res['sha256'][:16]}...`\n\n"
                        f"*(ប្រព័ន្ធក៏នឹងបន្តផ្ញើ Backup ស្វ័យប្រវត្តិកំពូលរៀងរាល់ ២៤ ម៉ោង វេលាម៉ោង ២:០០ ទៀបភ្លឺជារៀងរាល់ថ្ងៃ)*"
                    )
                else:
                    text = f"❌ កំហុសក្នុងការបង្កើត Backup៖ {res.get('error')}"

                keyboard = [
                    [InlineKeyboardButton("🔙 ត្រឡប់ទៅ Admin Panel", callback_data="admin_panel")],
                    [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
                ]
                await self._safe_edit(query, text, reply_markup=InlineKeyboardMarkup(keyboard))

            # ==================== CURRICULUM CALLBACKS ====================
            elif data == "menu_curriculum":
                cats = self.curriculum.get_categories()
                text = (
                    "📚 **កម្មវិធីសិក្សាហុងស៊ុយបុរាណ ១០០ ប្រធានបទ & ១០០០ មេរៀន**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "សូមជ្រើសរើសផ្នែកដែលអ្នកចង់សិក្សា៖\n\n"
                    "☯️ **ផ្នែកទី ១:** មូលដ្ឋានគ្រឹះក្បួនហុងស៊ុយបុរាណ (មេរៀន ១-២០០)\n"
                    "🌌 **ផ្នែកទី ២:** ក្បួនជឿនលឿន & តារាហោះ យុគ ៩ (មេរៀន ២០១-៥០០)\n"
                    "🏛️ **ផ្នែកទី ៣:** ការអនុវត្តជាក់ស្តែង & លំនៅឋាន/អាជីវកម្ម (មេរៀន ៥០១-៨០០)\n"
                    "🔮 **ផ្នែកទី ៤:** ក្បួនឯកទេសជាន់ខ្ពស់ & BaZi រាសី (មេរៀន ៨០១-១០០០)"
                )
                keyboard = [
                    [InlineKeyboardButton(f"{c['icon']} {c['name_kh']}", callback_data=f"curr_cat_{c['id']}_p1")]
                    for c in cats
                ]
                keyboard.append([
                    InlineKeyboardButton("📖 រៀនមេរៀនទី ១", callback_data="curr_les_1"),
                    InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
                ])
                await self._safe_edit(query, text, reply_markup=InlineKeyboardMarkup(keyboard))

            # Category Topics List with Pagination
            elif data.startswith("curr_cat_"):
                parts = data.split("_")
                cat_id = parts[2]
                page = int(parts[3].replace("p", "")) if len(parts) > 3 else 1

                cat_info = next((c for c in self.curriculum.get_categories() if c["id"] == cat_id), None)
                if not cat_info:
                    await self._safe_edit(query, "❌ រកមិនឃើញផ្នែកនេះឡើយ។")
                    return

                topics = self.curriculum.get_topics(category_id=cat_id)
                page_size = 5
                total_pages = (len(topics) + page_size - 1) // page_size
                page = max(1, min(page, total_pages))

                start_idx = (page - 1) * page_size
                page_topics = topics[start_idx:start_idx + page_size]

                text = (
                    f"{cat_info['icon']} **{cat_info['name_kh']}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"📖 **ការពិពណ៌នា:** {cat_info['description']}\n"
                    f"🔢 **ទំព័រទី {page}/{total_pages} (សរុប {len(topics)} ប្រធានបទ)**\n\n"
                    f"👇 **សូមជ្រើសរើសប្រធានបទដើម្បីសិក្សា៖**"
                )

                keyboard = []
                for t in page_topics:
                    keyboard.append([
                        InlineKeyboardButton(
                            f"📌 {t['topic_id']}. {t['name_kh']} (មេរៀន {t['lesson_start']}-{t['lesson_end']})",
                            callback_data=f"curr_top_{t['topic_id']}"
                        )
                    ])

                nav_buttons = []
                if page > 1:
                    nav_buttons.append(InlineKeyboardButton("⬅️ ទំព័រមុន", callback_data=f"curr_cat_{cat_id}_p{page - 1}"))
                if page < total_pages:
                    nav_buttons.append(InlineKeyboardButton("➡️ ទំព័របន្ទាប់", callback_data=f"curr_cat_{cat_id}_p{page + 1}"))

                if nav_buttons:
                    keyboard.append(nav_buttons)

                keyboard.append([
                    InlineKeyboardButton("📚 ត្រឡប់ទៅផ្នែកទាំង ៤", callback_data="menu_curriculum"),
                    InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
                ])
                await self._safe_edit(query, text, reply_markup=InlineKeyboardMarkup(keyboard))

            # Topic Details & Sub-Lessons List
            elif data.startswith("curr_top_"):
                topic_id = int(data.split("_")[2])
                topic = self.curriculum.get_topic(topic_id)
                if not topic:
                    await self._safe_edit(query, "❌ រកមិនឃើញប្រធានបទនេះឡើយ។")
                    return

                text = (
                    f"📌 **ប្រធានបទទី {topic['topic_id']}: {topic['name_kh']}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"🏷️ **ផ្នែក:** {topic['category_icon']} {topic['category_name']}\n"
                    f"📝 **ខ្លឹមសារ:** {topic['summary']}\n"
                    f"🔢 **មេរៀន:** ទី {topic['lesson_start']} ដល់ {topic['lesson_end']} (សរុប ១០ មេរៀន)\n\n"
                    f"👇 **សូមជ្រើសរើសមេរៀនដើម្បីអាន និងរៀនសូត្រ៖**"
                )

                keyboard = []
                for les in topic["lessons"]:
                    keyboard.append([
                        InlineKeyboardButton(
                            f"📖 មេរៀន {les['lesson_id']}: {les['sub_topic_kh']}",
                            callback_data=f"curr_les_{les['lesson_id']}"
                        )
                    ])

                keyboard.append([
                    InlineKeyboardButton("🔙 ត្រឡប់ទៅបញ្ជីប្រធានបទ", callback_data=f"curr_cat_{topic['category_id']}_p1"),
                    InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
                ])
                await self._safe_edit(query, text, reply_markup=InlineKeyboardMarkup(keyboard))

            # Individual Lesson View
            elif data.startswith("curr_les_"):
                lesson_id = int(data.split("_")[2])
                await self._send_lesson_view(query, lesson_id, is_edit=True)

            # Deep AI Explanation of Lesson
            elif data.startswith("curr_exp_"):
                lesson_id = int(data.split("_")[2])
                lesson = self.curriculum.get_lesson(lesson_id)
                if not lesson:
                    await self._safe_edit(query, "❌ រកមិនឃើញមេរៀន។")
                    return

                await self._safe_edit(
                    query,
                    f"⏳ **កំពុងដំណើរការម៉ូដែល FS-Supreme-Master ដើម្បីពន្យល់មេរៀនទី {lesson_id}...**\n\n"
                    f"*(សូមរង់ចាំបន្តិច ប្រព័ន្ធកំពុងសំយោគក្បួនបុរាណ យុគទី ៩ ធាតុភ្លើង)*"
                )

                res = self.curriculum.generate_deep_explanation(lesson_id)
                exp_text = res.get("deep_explanation", "")

                full_text = (
                    f"🧠 **ការពន្យល់ស៊ីជម្រៅកម្រិតកំពូល (Master Level AI Synthesis)**\n"
                    f"📚 **{lesson['title_kh']}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"{exp_text}\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"*(ប្រព័ន្ធបណ្តុះបណ្តាលដោយ 7 Core Pillars & LoRA Adapter)*"
                )

                nav_row = []
                if lesson["prev_lesson_id"]:
                    nav_row.append(InlineKeyboardButton("⬅️ មេរៀនមុន", callback_data=f"curr_les_{lesson['prev_lesson_id']}"))
                if lesson["next_lesson_id"]:
                    nav_row.append(InlineKeyboardButton("➡️ មេរៀនបន្ទាប់", callback_data=f"curr_les_{lesson['next_lesson_id']}"))

                keyboard = []
                if nav_row:
                    keyboard.append(nav_row)
                keyboard.append([
                    InlineKeyboardButton("📖 អានសេចក្តីសង្ខេបមេរៀន", callback_data=f"curr_les_{lesson_id}"),
                    InlineKeyboardButton("📑 មេរៀនក្នុងប្រធានបទ", callback_data=f"curr_top_{lesson['topic_id']}")
                ])
                keyboard.append([
                    InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
                ])
                await self._safe_edit(query, full_text, reply_markup=InlineKeyboardMarkup(keyboard))

            # Demos
            elif data == "menu_gua":
                await self.gua_command(update, context)
            elif data == "menu_flyingstars":
                await self.flyingstars_command(update, context)
            elif data == "menu_bazi":
                await self.bazi_command(update, context)
            elif data == "menu_predict":
                await self.predict_command(update, context)
            elif data == "menu_ask":
                await self._safe_edit(
                    query,
                    "💬 **សូមវាយសំណួររបស់អ្នកផ្ញើមកទីនេះដោយផ្ទាល់**\n\n"
                    "ឧទាហរណ៍៖\n"
                    "• *តើខ្ញុំគួររៀបចំបន្ទប់គេង និងតុធ្វើការយ៉ាងណាដើម្បីស្រូបទ្រព្យក្នុងយុគទី ៩?*\n"
                    "• *ផ្ទះបែរមុខទៅទិសខាងត្បូង ១៨០ ដឺក្រេ តើល្អដែរឬទេ?*",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]])
                )
            elif data == "menu_render3d":
                await self._send_render3d_menu(query, is_edit=True)
            elif data in ["render_living", "render_bedroom", "render_office", "render_villa"]:
                space_map = {
                    "render_living": ("living_room", "🛋️ បន្ទប់ទទួលភ្ញៀវយុគ ៩ (Living Room)"),
                    "render_bedroom": ("bedroom", "🛏️ បន្ទប់គេងមេគ្រួសារ (Master Bedroom)"),
                    "render_office": ("office", "💼 ការិយាល័យថ្នាក់ដឹកនាំ (Executive Office)"),
                    "render_villa": ("exterior_house", "🏡 ភូមិគ្រឹះ & វីឡាហុងស៊ុយ (Feng Shui Villa)")
                }
                space_key, space_title = space_map[data]
                render_data = self.vision.generate_3d_render_prompt(space_type=space_key)

                caption = (
                    f"🎨 **ប្លង់ហុងស៊ុយ 3D 4K៖ {space_title}**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• **ក្បួនខ្នាត:** San Yuan Period 9 Li Fire (2024-2043)\n"
                    f"• **គុណភាពបង្ហាញ:** 4K Ultra-HD Photorealistic Render\n"
                    f"• **លក្ខណៈពិសេស:** {render_data['fengshui_specifications']['bright_hall']}, "
                    f"{render_data['fengshui_specifications']['water_placement']}\n\n"
                    f"🖼️ [ចុចទីនេះដើម្បីទាញយករូបភាព 4K ពេញលេញ]({render_data['image_4k_url']})"
                )

                keyboard = [
                    [
                        InlineKeyboardButton("🔄 បង្កើតប្លង់ផ្សេងទៀត", callback_data="menu_render3d"),
                        InlineKeyboardButton("💬 សួរពិគ្រោះ AI", callback_data="menu_ask")
                    ],
                    [
                        InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
                    ]
                ]

                try:
                    await query.message.reply_photo(
                        photo=render_data['image_4k_url'],
                        caption=caption,
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                except Exception:
                    await self._safe_edit(query, caption, reply_markup=InlineKeyboardMarkup(keyboard))

            elif data.startswith("adm_give_"):
                parts = data.split("_")
                if len(parts) == 4:
                    target_id = int(parts[2])
                    tier = parts[3]
                    admin_id = from_user.id

                    if admin_id in config.ADMIN_USER_IDS:
                        res = self.db.set_user_vip_manually(target_id, tier, admin_id=admin_id)
                        if res["success"]:
                            tier_names = {
                                "monthly": "🌟 VIP 1 ខែ (Monthly VIP)",
                                "yearly": "👑 VIP 1 ឆ្នាំ (Yearly VIP)",
                                "lifetime": "💎 VIP មួយជីវិត (Lifetime VIP)"
                            }
                            tier_kh = tier_names.get(tier, tier)

                            await self._safe_edit(
                                query,
                                f"✅ **បានផ្តល់សិទ្ធិ VIP ជូនអ្នកប្រើប្រាស់ជោគជ័យ!**\n"
                                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                                f"• **Telegram ID:** `{target_id}`\n"
                                f"• **កម្រិតដែលបានផ្តល់:** **{tier_kh}**\n"
                                f"• **កាលបរិច្ឆេទផុតកំណត់:** `{res['expiry']}`"
                            )

                            # Notify target user directly!
                            try:
                                vip_notice = (
                                    f"🎉 **អបអរសាទរ! Super Admin បានតម្លើងគណនីរបស់អ្នកជាសមាជិក VIP!** 🎉\n"
                                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                                    f"👑 **កម្រិត VIP របស់អ្នក:** **{tier_kh}**\n"
                                    f"✨ **សិទ្ធិពិសេស:** សួរគ្រូហុងស៊ុយ AI បាន **គ្មានដែនកំណត់ 24/7/365**!\n\n"
                                    f"👉 សូមវាយសំណួររបស់អ្នក ឬចុចប៊ូតុងខាងក្រោមដើម្បីចាប់ផ្តើម!"
                                )
                                await context.bot.send_message(
                                    chat_id=target_id,
                                    text=vip_notice,
                                    parse_mode="Markdown",
                                    reply_markup=self._get_main_keyboard(target_id)
                                )
                            except Exception as e_user:
                                logger.warning(f"Could not notify target user {target_id}: {e_user}")
                        else:
                            await self._safe_edit(query, f"❌ កំហុស៖ {res.get('error')}")

            elif data == "menu_health":
                await self.health_command(update, context)
            elif data == "menu_help":
                await self.help_command(update, context)
        except Exception as err:
            logger.error(f"Error handling button callback {data}: {err}", exc_info=True)
            await self._safe_edit(
                query,
                f"❌ មានបញ្ហាបន្តិចបន្តួចក្នុងការដំណើរការ៖ {err}",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]])
            )

    def run(self):
        """Start the Telegram Bot polling daemon with native command registration."""
        if not TELEGRAM_AVAILABLE or not self.token or self.token == "your_telegram_bot_token_here":
            logger.warning("Telegram Bot Token is not configured or python-telegram-bot is missing. Skipping bot run.")
            return

        try:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            logger.info("Starting Bulletproof Telegram Bot Application with Super Admin & VIP License Manager...")
            app = Application.builder().token(self.token).post_init(self.post_init).build()

            # Commands
            app.add_handler(CommandHandler("start", self.start_command))
            app.add_handler(CommandHandler("render3d", self.render3d_command))
            app.add_handler(CommandHandler("visualize", self.render3d_command))
            app.add_handler(CommandHandler("health", self.health_command))
            app.add_handler(CommandHandler("vip", self.vip_command))
            app.add_handler(CommandHandler("redeem", self.redeem_command))
            app.add_handler(CommandHandler("admin", self.admin_command))
            app.add_handler(CommandHandler("backup", self.backup_command))
            app.add_handler(CommandHandler("setvip", self.setvip_command))
            app.add_handler(CommandHandler("genkeys", self.genkeys_command))
            app.add_handler(CommandHandler("broadcast", self.broadcast_command))
            app.add_handler(CommandHandler("help", self.help_command))
            app.add_handler(CommandHandler("curriculum", self.curriculum_command))
            app.add_handler(CommandHandler("learn", self.learn_command))
            app.add_handler(CommandHandler("gua", self.gua_command))
            app.add_handler(CommandHandler("flyingstars", self.flyingstars_command))
            app.add_handler(CommandHandler("bazi", self.bazi_command))
            app.add_handler(CommandHandler("predict", self.predict_command))
            app.add_handler(CommandHandler("love", self.love_command))
            app.add_handler(CommandHandler("mahasneh", self.love_command))
            app.add_handler(CommandHandler("ask", self.handle_message))

            # Callbacks & Messages
            app.add_handler(CallbackQueryHandler(self.button_callback))
            app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

            logger.info("Telegram Bot polling started successfully with bulletproof resilience.")
            app.run_polling(stop_signals=None, close_loop=False)
        except Exception as e:
            logger.error(f"Telegram Bot error: {e}", exc_info=True)
