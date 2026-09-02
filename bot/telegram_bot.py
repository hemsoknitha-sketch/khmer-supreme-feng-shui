"""
Telegram Bot for Supreme Feng Shui AGI System
Asynchronous, lightweight, and bulletproof interactive bot powered by FS-Supreme-Master.
Features persistent native commands menu, full inline interactive keyboards,
and an interactive 100-Topic & 1,000-Lesson Curriculum Learning Center with 7 Core Pillars.
Runs 24/7 on Google Cloud VPS 1GB RAM.
"""

import logging
import asyncio
from typing import Dict, Any, List
from datetime import datetime

from config import config
from engines.supreme_master import SupremeFengShuiMaster
from engines.classical_calc import ClassicalCalcEngine
from engines.alert_predictor import AlertPredictionEngine
from engines.curriculum_engine import curriculum_engine

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        CallbackQueryHandler,
        filters,
        ContextTypes
    )
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

logger = logging.getLogger("SupremeFengShui.TelegramBot")


class FengShuiTelegramBot:
    """Production Bulletproof Telegram Bot for Supreme Feng Shui System."""

    def __init__(self, token: str = None):
        self.token = token or config.TELEGRAM_BOT_TOKEN
        self.master = SupremeFengShuiMaster()
        self.calc_engine = ClassicalCalcEngine()
        self.alert_engine = AlertPredictionEngine()
        self.curriculum = curriculum_engine

    async def _safe_reply(self, message, text: str, reply_markup=None):
        """Safely send markdown text, automatically falling back to plain text if parsing fails."""
        if len(text) > 4000:
            text = text[:3950] + "\n\n...(ចុចប៊ូតុងខាងក្រោមដើម្បីអានបន្ត)..."
        try:
            return await message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        except Exception as e:
            logger.debug(f"Markdown parse fallback for reply: {e}")
            return await message.reply_text(text, reply_markup=reply_markup)

    async def _safe_edit(self, query, text: str, reply_markup=None):
        """Safely edit message text, automatically falling back to plain text if parsing fails."""
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

    def _get_main_keyboard(self) -> InlineKeyboardMarkup:
        """Construct the rich main dashboard interactive keyboard."""
        keyboard = [
            [
                InlineKeyboardButton("📚 កម្មវិធីសិក្សា ១០០០ មេរៀន", callback_data="menu_curriculum")
            ],
            [
                InlineKeyboardButton("🧭 គណនា Life Gua", callback_data="menu_gua"),
                InlineKeyboardButton("🌌 តារាហោះ យុគ ៩", callback_data="menu_flyingstars")
            ],
            [
                InlineKeyboardButton("🔮 វិភាគ BaZi ៤ សសរ", callback_data="menu_bazi"),
                InlineKeyboardButton("📊 ទស្សន៍ទាយសំណាង", callback_data="menu_predict")
            ],
            [
                InlineKeyboardButton("💬 សួរគ្រូហុងស៊ុយ AI", callback_data="menu_ask"),
                InlineKeyboardButton("❓ ជំនួយ (Help)", callback_data="menu_help")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    async def post_init(self, application: Application) -> None:
        """Register native command menu button in Telegram UI."""
        commands = [
            BotCommand("start", "🌟 ផ្ទាំងដើម & ម៉ឺនុយបញ្ជា (Main Dashboard)"),
            BotCommand("curriculum", "📚 កម្មវិធីសិក្សា ១០០ ប្រធានបទ & ១០០០ មេរៀន"),
            BotCommand("learn", "📖 រៀនមេរៀនជាក់លាក់ (ឧ. /learn 1)"),
            BotCommand("gua", "🧭 គណនា Life Gua (ឧ. /gua 1988 male)"),
            BotCommand("flyingstars", "🌌 តារាហោះ ៩ វិហារ យុគ ៩"),
            BotCommand("bazi", "🔮 វិភាគ BaZi (ឧ. /bazi 1988-05-15 10:30)"),
            BotCommand("predict", "📊 ទស្សន៍ទាយសំណាង (ឧ. /predict 1988-05-15)"),
            BotCommand("ask", "🧠 ពិគ្រោះយោបល់ជាមួយ FS-Supreme-Master AI"),
            BotCommand("help", "❓ សៀវភៅណែនាំប្រើប្រាស់")
        ]
        try:
            await application.bot.set_my_commands(commands)
            logger.info("Native Telegram Bot Commands registered successfully.")
        except Exception as e:
            logger.warning(f"Could not register Telegram Bot commands: {e}")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command with rich interactive dashboard."""
        welcome_text = (
            "🌟 **SUPREME FENG SHUI AGI SYSTEM (Master Level v1.0.0)** 🌟\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "សូមស្វាគមន៍មកកាន់ប្រព័ន្ធបញ្ញាសិប្បនិម្មិតហុងស៊ុយកំពូល ដែលរួមបញ្ចូលគ្នានូវ **៧ សសរស្តម្ភស្នូល** និង **កម្មវិធីសិក្សា ១០០០ មេរៀន** តាមក្បួនបុរាណពិតប្រាកដ!\n\n"
            "⚡ **សមត្ថភាពស្នូលរបស់ប្រព័ន្ធ:**\n"
            "• 📚 **1,000 Lessons Curriculum**: មេរៀនក្បួនហុងស៊ុយ ១០០០ មេរៀនលម្អិត\n"
            "• 🧠 **FS-Supreme-Master AI**: ម៉ូដែលឆ្លើយតប និងវែកញែកកម្រិតខ្ពស់\n"
            "• 🧭 **FS-Classical-Calc**: គណនា Life Gua, Flying Stars, BaZi សូន្យកំហុស\n"
            "• 📊 **FS-Alert-Predictor**: ទស្សន៍ទាយជោគជតារាសីប្រចាំថ្ងៃ 0-100%\n\n"
            "👇 **សូមចុចប៊ូតុងខាងក្រោមដើម្បីចាប់ផ្តើមប្រើប្រាស់ភ្លាមៗ:**"
        )
        await self._safe_reply(update.message, welcome_text, reply_markup=self._get_main_keyboard())

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = (
            "📖 **របៀបប្រើប្រាស់ពាក្យបញ្ជា (Command Guide):**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "1️⃣ **រៀនសូត្រមេរៀន:**\n"
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
            "• `/ask តើខ្ញុំគួររៀបចំបន្ទប់គេង និងតុធ្វើការយ៉ាងណាដើម្បីបង្កើនទ្រព្យ?`"
        )
        await self._safe_reply(update.message, help_text, reply_markup=self._get_main_keyboard())

    async def curriculum_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /curriculum command."""
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
            InlineKeyboardButton("📖 រៀនមេរៀនទី ១ ភ្លាមៗ", callback_data="curr_les_1"),
            InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
        ])
        await self._safe_reply(update.message, text, reply_markup=InlineKeyboardMarkup(keyboard))

    async def learn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /learn <lesson_id> command."""
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
            InlineKeyboardButton("🧠 ពន្យល់លម្អិតជាមួយ AI Master", callback_data=f"curr_exp_{lesson['lesson_id']}")
        ])
        keyboard.append([
            InlineKeyboardButton("📑 មេរៀនក្នុងប្រធានបទនេះ", callback_data=f"curr_top_{lesson['topic_id']}"),
            InlineKeyboardButton("📚 ផ្នែកទាំង ៤", callback_data="menu_curriculum")
        ])
        keyboard.append([
            InlineKeyboardButton("🏠 ម៉ឺនុយដើម (Main Menu)", callback_data="menu_main")
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)
        if is_edit:
            await self._safe_edit(message_or_query, text, reply_markup=reply_markup)
        else:
            await self._safe_reply(message_or_query, text, reply_markup=reply_markup)

    async def gua_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /gua command."""
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
        """Handle /flyingstars command."""
        year = 2024
        res = self.calc_engine.calculate_flying_stars(year)
        if res["success"]:
            d = res["data"]
            grid = d["grid"]
            msg = (
                f"🌌 **តារាហោះប្រចាំឆ្នាំ {year} (យុគទី {d['period']} ធាតុភ្លើង Li Fire)**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• **តារាកណ្តាល:** {d['annual_center_star']} (San Bi Wood)\n"
                f"• **ទិសទ្រព្យធំ:** {d['wealth_palace']}\n\n"
                f"📍 **ស្ថានភាពតារាទាំង ៩ វិហារ:**\n"
                f"• **ខាងត្បូង (S):** តារា {grid['S']['star_number']} ({grid['S']['details'].get('kh')})\n"
                f"• **ខាងជើង (N):** តារា {grid['N']['star_number']} ({grid['N']['details'].get('kh')})\n"
                f"• **ខាងកើត (E):** តារា {grid['E']['star_number']} ({grid['E']['details'].get('kh')})\n"
                f"• **ខាងលិច (W):** តារា {grid['W']['star_number']} ({grid['W']['details'].get('kh')})\n"
                f"• **អាគ្នេយ៍ (SE):** តារា {grid['SE']['star_number']} ({grid['SE']['details'].get('kh')})\n"
                f"• **ពាយ័ព្យ (NW):** តារា {grid['NW']['star_number']} ({grid['NW']['details'].get('kh')})\n"
                f"• **ឦសាន (NE):** តារា {grid['NE']['star_number']} ({grid['NE']['details'].get('kh')})\n"
                f"• **និរតី (SW):** តារា {grid['SW']['star_number']} ({grid['SW']['details'].get('kh')})\n\n"
                f"💡 **ការបន្សាបគ្រោះ:** ដាក់កណ្តឹងខ្យល់លោហធាតុនៅទិសខាងលិច (តារា ៥ លឿង)។"
            )
            keyboard = [
                [InlineKeyboardButton("📚 រៀនក្បួនតារាហោះ យុគ ៩", callback_data="curr_les_221")],
                [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
            ]
            await self._safe_reply(update.message, msg, reply_markup=InlineKeyboardMarkup(keyboard))

    async def bazi_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /bazi command."""
        args = context.args
        if not args:
            text = (
                "🔮 **របៀបគណនា BaZi Four Pillars:**\n"
                "សូមសរសេរ៖ `/bazi <YYYY-MM-DD> <HH:MM>`\n"
                "ឧទាហរណ៍៖ `/bazi 1988-05-15 10:30`"
            )
            keyboard = [
                [InlineKeyboardButton("🔮 តេស្ត BaZi (1988-05-15 10:30)", callback_data="calc_bazi_demo")],
                [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
            ]
            await self._safe_reply(update.message, text, reply_markup=InlineKeyboardMarkup(keyboard))
            return

        date_str = args[0]
        time_str = args[1] if len(args) > 1 else "12:00"
        res = self.calc_engine.calculate_bazi(date_str, time_str)

        if res["success"]:
            d = res["data"]
            p = d["pillars"]
            msg = (
                f"🔮 **លទ្ធផល BaZi Four Pillars (FS-Classical-Calc-v1)**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• **សសរស្តម្ភឆ្នាំ:** {p['year']['ganzhi']}\n"
                f"• **សសរស្តម្ភខែ:** {p['month']['ganzhi']}\n"
                f"• **សសរស្តម្ភថ្ងៃ:** {p['day']['ganzhi']}\n"
                f"• **សសរស្តម្ភម៉ោង:** {p['time']['ganzhi']}\n\n"
                f"👤 **Day Master:** {d['day_master']['element']} ({d['day_master']['nature']})\n\n"
                f"🌿 **តុល្យភាពធាតុទាំង ៥:**\n" +
                "\n".join([f"• {k}: {v}" for k, v in d['five_elements_count'].items()]) +
                f"\n\n💡 **ដំបូន្មាន:** {d['recommendation']}"
            )
            keyboard = [
                [InlineKeyboardButton("📚 រៀនក្បួន BaZi (មេរៀន ៨០១-១០០០)", callback_data="curr_cat_CAT4_p1")],
                [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
            ]
            await self._safe_reply(update.message, msg, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await self._safe_reply(update.message, f"❌ កំហុស៖ {res.get('error')}")

    async def predict_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /predict command."""
        args = context.args
        if not args:
            text = (
                "📊 **របៀបទស្សន៍ទាយសំណាងប្រចាំថ្ងៃ (FS-Alert-Predictor):**\n"
                "សូមសរសេរ៖ `/predict <YYYY-MM-DD>`\n"
                "ឧទាហរណ៍៖ `/predict 1988-05-15`"
            )
            keyboard = [
                [InlineKeyboardButton("📊 ទស្សន៍ទាយថ្ងៃនេះ", callback_data="calc_predict_demo")],
                [InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")]
            ]
            await self._safe_reply(update.message, text, reply_markup=InlineKeyboardMarkup(keyboard))
            return

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

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle conversational natural language messages via SupremeFengShuiMaster."""
        user_text = update.message.text
        await update.message.chat.send_action("typing")

        consult_res = self.master.consult(query=user_text)
        response_text = consult_res.get("synthesis", "សូមអភ័យទោស ខ្ញុំមិនអាចឆ្លើយតបនៅពេលនេះបានទេ។")

        keyboard = [
            [
                InlineKeyboardButton("📚 កម្មវិធីសិក្សា ១០០០ មេរៀន", callback_data="menu_curriculum"),
                InlineKeyboardButton("🏠 ម៉ឺនុយដើម", callback_data="menu_main")
            ]
        ]
        await self._safe_reply(update.message, response_text, reply_markup=InlineKeyboardMarkup(keyboard))

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all interactive inline keyboard clicks seamlessly."""
        query = update.callback_query
        try:
            await query.answer()
        except Exception:
            pass

        data = query.data

        try:
            # Navigation: Main Menu
            if data == "menu_main":
                await self._safe_edit(
                    query,
                    "🌟 **SUPREME FENG SHUI AGI SYSTEM (Master Level v1.0.0)** 🌟\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "សូមជ្រើសរើសមុខងារដែលអ្នកចង់ប្រើប្រាស់៖",
                    reply_markup=self._get_main_keyboard()
                )

            # Navigation: Curriculum Root
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
                page = int(parts[3][1:]) if len(parts) > 3 else 1

                topics = self.curriculum.get_topics(category_id=cat_id)
                page_size = 5
                total_pages = max(1, (len(topics) + page_size - 1) // page_size)
                page_topics = topics[(page - 1) * page_size: page * page_size]

                cat_info = next((c for c in self.curriculum.get_categories() if c["id"] == cat_id), None)
                text = (
                    f"📚 **{cat_info['icon'] if cat_info else '📚'} {cat_info['name_kh'] if cat_info else cat_id}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"ទំព័រ {page}/{total_pages} (ប្រធានបទសរុប៖ {len(topics)})\n\n"
                    f"👇 **សូមជ្រើសរើសប្រធានបទដើម្បីមើលមេរៀនលម្អិត៖**"
                )

                keyboard = []
                for t in page_topics:
                    keyboard.append([
                        InlineKeyboardButton(
                            f"📌 ប្រធានបទ {t['topic_id']}: {t['name_kh']}",
                            callback_data=f"curr_top_{t['topic_id']}"
                        )
                    ])

                # Pagination row
                nav_row = []
                if page > 1:
                    nav_row.append(InlineKeyboardButton("⬅️ មុន", callback_data=f"curr_cat_{cat_id}_p{page-1}"))
                if page < total_pages:
                    nav_row.append(InlineKeyboardButton("➡️ បន្ទាប់", callback_data=f"curr_cat_{cat_id}_p{page+1}"))
                if nav_row:
                    keyboard.append(nav_row)

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

            # Individual Lesson View with Next / Prev
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

                # Generate deep explanation
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

            # Interactive Calculation Quick Demos
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

            logger.info("Starting Bulletproof Telegram Bot Application...")
            app = Application.builder().token(self.token).post_init(self.post_init).build()

            app.add_handler(CommandHandler("start", self.start_command))
            app.add_handler(CommandHandler("help", self.help_command))
            app.add_handler(CommandHandler("curriculum", self.curriculum_command))
            app.add_handler(CommandHandler("learn", self.learn_command))
            app.add_handler(CommandHandler("gua", self.gua_command))
            app.add_handler(CommandHandler("flyingstars", self.flyingstars_command))
            app.add_handler(CommandHandler("bazi", self.bazi_command))
            app.add_handler(CommandHandler("predict", self.predict_command))
            app.add_handler(CommandHandler("ask", self.handle_message))
            app.add_handler(CallbackQueryHandler(self.button_callback))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

            logger.info("Telegram Bot polling started successfully with bulletproof resilience.")
            app.run_polling(stop_signals=None, close_loop=False)
        except Exception as e:
            logger.error(f"Telegram Bot error: {e}", exc_info=True)
