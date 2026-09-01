"""
Telegram Bot for Supreme Feng Shui AGI System
Asynchronous, lightweight, and interactive bot powered by FS-Supreme-Master.
Runs 24/7 on Google Cloud VPS 1GB RAM.
"""

import logging
import asyncio
from typing import Dict, Any
from datetime import datetime

from config import config
from engines.supreme_master import SupremeFengShuiMaster
from engines.classical_calc import ClassicalCalcEngine
from engines.alert_predictor import AlertPredictionEngine

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        CallbackQueryHandler,
        filters,
        ContextTypes
    )
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

logger = logging.getLogger("SupremeFengShui.TelegramBot")


class FengShuiTelegramBot:
    """Production Telegram Bot for Supreme Feng Shui System."""

    def __init__(self, token: str = None):
        self.token = token or config.TELEGRAM_BOT_TOKEN
        self.master = SupremeFengShuiMaster()
        self.calc_engine = ClassicalCalcEngine()
        self.alert_engine = AlertPredictionEngine()
        self.scheduler = AsyncIOScheduler() if TELEGRAM_AVAILABLE else None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command with interactive menu."""
        welcome_text = (
            "🌟 **សូមស្វាគមន៍មកកាន់ Supreme Feng Shui AGI System** 🌟\n\n"
            "ខ្ញុំជា **បរមគ្រូហុងស៊ុយ AI កម្រិតកំពូល** ដែលដំណើរការដោយបច្ចេកវិទ្យា MoE Intelligence Matrix:\n"
            "• **FS-Boramey-7B**: បង្រៀន និងឆ្លើយសំណួរក្បួនហុងស៊ុយ\n"
            "• **FS-Reasoner-7B**: វិភាគក្បួនស៊ីជម្រៅ CoT\n"
            "• **FS-Classical-Calc-v1**: គណនាលេខក្បួនសូន្យកំហុស\n"
            "• **FS-Alert-Predictor**: ទស្សន៍ទាយជោគជតារាសីប្រចាំថ្ងៃ\n\n"
            "📋 **បញ្ជីពាក្យបញ្ជាសំខាន់ៗ:**\n"
            "👉 `/gua <ឆ្នាំកំណើត> <ភេទ m/f>` - គណនា Life Gua & ទិសល្អ\n"
            "👉 `/flyingstars` - មើលតារាហោះឆ្នាំ ២០២៤ យុគ ៩\n"
            "👉 `/bazi <YYYY-MM-DD> <HH:MM>` - វិភាគសសរស្តម្ភទាំង ៤\n"
            "👉 `/predict <YYYY-MM-DD>` - ទស្សន៍ទាយសំណាងប្រចាំថ្ងៃ\n"
            "👉 `/ask <សំណួរ>` - សួរសំណួរហុងស៊ុយណាមួយក៏បាន\n"
            "👉 `/help` - ជំនួយបន្ថែម"
        )

        keyboard = [
            [
                InlineKeyboardButton("🔢 គណនា Life Gua", callback_data="menu_gua"),
                InlineKeyboardButton("🌌 តារាហោះ យុគ ៩", callback_data="menu_flyingstars")
            ],
            [
                InlineKeyboardButton("🔮 វិភាគ BaZi", callback_data="menu_bazi"),
                InlineKeyboardButton("📊 ទស្សន៍ទាយសំណាង", callback_data="menu_predict")
            ],
            [
                InlineKeyboardButton("📚 កម្មវិធីសិក្សាហុងស៊ុយ", callback_data="menu_curriculum")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = (
            "📖 **សៀវភៅណែនាំពាក្យបញ្ជា (Help Guide):**\n\n"
            "1️⃣ **គណនា Life Gua:**\n"
            "ឧទាហរណ៍៖ `/gua 1988 male` ឬ `/gua 1995 female`\n\n"
            "2️⃣ **គណនា BaZi (Four Pillars):**\n"
            "ឧទាហរណ៍៖ `/bazi 1990-05-20 08:30`\n\n"
            "3️⃣ **ទស្សន៍ទាយសំណាងប្រចាំថ្ងៃ:**\n"
            "ឧទាហរណ៍៖ `/predict 1988-08-15`\n\n"
            "4️⃣ **សួរការរៀបចំផ្ទះ ឬការិយាល័យ:**\n"
            "ឧទាហរណ៍៖ `/ask តើខ្ញុំគួររៀបចំបន្ទប់គេងយ៉ាងដូចម្តេចក្នុងយុគទី ៩?`"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")

    async def gua_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /gua command."""
        args = context.args
        if not args or len(args) < 1:
            await update.message.reply_text("⚠️ សូមបញ្ជាក់ឆ្នាំកំណើត និងភេទ (ឧទាហរណ៍៖ `/gua 1988 male`)", parse_mode="Markdown")
            return

        try:
            year = int(args[0])
            gender = args[1] if len(args) > 1 else "male"
            res = self.calc_engine.calculate_life_gua(year, gender)

            if res["success"]:
                d = res["data"]
                lucky_str = "\n".join([f"• **{item['direction']}** ({item['type']}): {item['meaning']}" for item in d['lucky_directions']])
                unlucky_str = "\n".join([f"• **{item['direction']}** ({item['type']}): {item['meaning']}" for item in d['unlucky_directions']])

                msg = (
                    f"🧭 **លទ្ធផល Life Gua របស់អ្នក (FS-Classical-Calc-v1)**\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"• **Gua លេខ:** {d['gua_number']} ({d['trigram_name']})\n"
                    f"• **ធាតុ:** {d['element']}\n"
                    f"• **ក្រុម:** {d['group']}\n\n"
                    f"✨ **ទិសល្អទាំង ៤ (Auspicious Directions):**\n{lucky_str}\n\n"
                    f"⚠️ **ទិសគួរជៀសវាងទាំង ៤ (Inauspicious Directions):**\n{unlucky_str}"
                )
                await update.message.reply_text(msg, parse_mode="Markdown")
            else:
                await update.message.reply_text(f"❌ កំហុស៖ {res.get('error')}")
        except Exception as e:
            await update.message.reply_text(f"❌ កំហុសក្នុងការគណនា៖ {str(e)}")

    async def flyingstars_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /flyingstars command."""
        year = 2024
        res = self.calc_engine.calculate_flying_stars(year)
        if res["success"]:
            d = res["data"]
            grid = d["grid"]
            msg = (
                f"🌌 **តារាហោះប្រចាំឆ្នាំ {year} (យុគទី {d['period']} ធាតុភ្លើង)**\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
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
            await update.message.reply_text(msg, parse_mode="Markdown")

    async def bazi_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /bazi command."""
        args = context.args
        if not args:
            await update.message.reply_text("⚠️ សូមបញ្ជាក់ថ្ងៃខែឆ្នាំកំណើត (ឧទាហរណ៍៖ `/bazi 1988-05-15 10:30`)", parse_mode="Markdown")
            return

        date_str = args[0]
        time_str = args[1] if len(args) > 1 else "12:00"
        res = self.calc_engine.calculate_bazi(date_str, time_str)

        if res["success"]:
            d = res["data"]
            p = d["pillars"]
            msg = (
                f"🔮 **លទ្ធផល BaZi Four Pillars (FS-Classical-Calc-v1)**\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"• **សសរស្តម្ភឆ្នាំ:** {p['year']['ganzhi']}\n"
                f"• **សសរស្តម្ភខែ:** {p['month']['ganzhi']}\n"
                f"• **សសរស្តម្ភថ្ងៃ:** {p['day']['ganzhi']}\n"
                f"• **សសរស្តម្ភម៉ោង:** {p['time']['ganzhi']}\n\n"
                f"👤 **Day Master:** {d['day_master']['element']} ({d['day_master']['nature']})\n\n"
                f"🌿 **តុល្យភាពធាតុទាំង ៥:**\n" +
                "\n".join([f"• {k}: {v}" for k, v in d['five_elements_count'].items()]) +
                f"\n\n💡 **ដំបូន្មាន:** {d['recommendation']}"
            )
            await update.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text(f"❌ កំហុស៖ {res.get('error')}")

    async def predict_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /predict command."""
        args = context.args
        if not args:
            await update.message.reply_text("⚠️ សូមបញ្ជាក់ថ្ងៃខែឆ្នាំកំណើត (ឧទាហរណ៍៖ `/predict 1988-05-15`)", parse_mode="Markdown")
            return

        date_str = args[0]
        res = self.alert_engine.predict_fortune(date_str)
        if res["success"]:
            d = res["data"]
            msg = (
                f"📊 **ការព្យាករណ៍ជោគជតារាសីប្រចាំថ្ងៃ (FS-Alert-Predictor)**\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
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
            await update.message.reply_text(msg, parse_mode="Markdown")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle conversational natural language messages via SupremeFengShuiMaster."""
        user_text = update.message.text
        await update.message.chat.send_action("typing")

        consult_res = self.master.consult(query=user_text)
        response_text = consult_res.get("synthesis", "សូមអភ័យទោស ខ្ញុំមិនអាចឆ្លើយតបនៅពេលនេះបានទេ។")
        await update.message.reply_text(response_text, parse_mode="Markdown")

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button clicks."""
        query = update.callback_query
        await query.answer()

        data = query.data
        if data == "menu_gua":
            await query.edit_message_text("🔢 ដើម្បីគណនា Life Gua សូមសរសេរ៖ `/gua <ឆ្នាំកំណើត> <male/female>`\nឧទាហរណ៍៖ `/gua 1988 male`", parse_mode="Markdown")
        elif data == "menu_flyingstars":
            res = self.calc_engine.calculate_flying_stars(2024)
            if res["success"]:
                await query.edit_message_text(f"🌌 យុគទី ៩ (២០២៤-២០៤៣): តារាកណ្តាលប្រចាំឆ្នាំ ២០២៤ គឺលេខ ៣ (San Bi)។ ទិសទ្រព្យសំខាន់គឺខាងត្បូង (South) និងខាងជើង (North)។", parse_mode="Markdown")
        elif data == "menu_bazi":
            await query.edit_message_text("🔮 ដើម្បីគណនា BaZi សូមសរសេរ៖ `/bazi YYYY-MM-DD HH:MM`\nឧទាហរណ៍៖ `/bazi 1990-05-20 08:30`", parse_mode="Markdown")
        elif data == "menu_predict":
            await query.edit_message_text("📊 ដើម្បីទស្សន៍ទាយសំណាង សូមសរសេរ៖ `/predict YYYY-MM-DD`\nឧទាហរណ៍៖ `/predict 1988-08-15`", parse_mode="Markdown")
        elif data == "menu_curriculum":
            await query.edit_message_text("📚 **កម្មវិធីសិក្សាហុងស៊ុយ ១០០ ប្រធានបទ:**\n១. មូលដ្ឋានគ្រឹះ (២០ ប្រធានបទ)\n២. ក្បួនជឿនលឿន (៣០ ប្រធានបទ)\n៣. ការអនុវត្តជាក់ស្តែង (៣០ ប្រធានបទ)\n៤. ក្បួនឯកទេស (២០ ប្រធានបទ)", parse_mode="Markdown")

    def run(self):
        """Start the Telegram Bot polling daemon."""
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

            logger.info("Starting Telegram Bot Application...")
            app = Application.builder().token(self.token).build()

            app.add_handler(CommandHandler("start", self.start_command))
            app.add_handler(CommandHandler("help", self.help_command))
            app.add_handler(CommandHandler("gua", self.gua_command))
            app.add_handler(CommandHandler("flyingstars", self.flyingstars_command))
            app.add_handler(CommandHandler("bazi", self.bazi_command))
            app.add_handler(CommandHandler("predict", self.predict_command))
            app.add_handler(CommandHandler("ask", self.handle_message))
            app.add_handler(CallbackQueryHandler(self.button_callback))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

            logger.info("Telegram Bot polling started successfully.")
            app.run_polling(stop_signals=None, close_loop=False)
        except Exception as e:
            logger.error(f"Telegram Bot error: {e}", exc_info=True)
