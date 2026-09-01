"""
Supreme Feng Shui AGI System - Master Execution Entry Point
Supports running API Server, Telegram Bot, Interactive CLI, or All Concurrent Services.
Optimized for Google Cloud 1GB VPS & Hugging Face Hub Integration.
"""

import sys
import argparse
import logging
import threading
import uvicorn

from config import config
from engines.supreme_master import SupremeFengShuiMaster

# Configure Logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("SupremeFengShui.Main")


def run_api():
    """Start FastAPI REST Server and Web UI."""
    logger.info(f"Starting FastAPI server on {config.API_HOST}:{config.API_PORT}...")
    uvicorn.run("api.server:app", host=config.API_HOST, port=config.API_PORT, log_level="info")


def run_bot():
    """Start Telegram Bot."""
    from bot.telegram_bot import FengShuiTelegramBot
    if not config.TELEGRAM_BOT_TOKEN or config.TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        logger.warning("Telegram Bot Token is not set. Bot will not run.")
        return
    logger.info("Starting Telegram Bot daemon...")
    bot = FengShuiTelegramBot()
    bot.run()


def run_cli():
    """Interactive Command-Line Consultation Mode."""
    print("=" * 80)
    print("🌟 SUPREME FENG SHUI AGI SYSTEM (FS-Supreme-Master CLI) 🌟")
    print("=" * 80)

    master = SupremeFengShuiMaster()

    print("\nសូមបញ្ចូលព័ត៌មានរបស់អ្នកដើម្បីចាប់ផ្តើមវិភាគ៖")
    birth_date = input("ថ្ងៃខែឆ្នាំកំណើត (YYYY-MM-DD) [ឧ. 1988-05-15]: ").strip() or "1988-05-15"
    birth_time = input("ម៉ោងកំណើត (HH:MM) [ឧ. 10:30]: ").strip() or "10:30"
    gender = input("ភេទ (male/female) [ឧ. male]: ").strip() or "male"
    house_deg_str = input("ទិសផ្ទះជាដឺក្រេ (0-360) [ឧ. 180]: ").strip() or "180"
    house_degree = float(house_deg_str)

    print("\n✓ កំពុងដំណើរការម៉ូដែល MoE Intelligence Matrix...")
    query = input("\nសួរសំណួររបស់អ្នក (Query): ").strip() or "តើខ្ញុំគួររៀបចំផ្ទះ និងការិយាល័យយ៉ាងណាដើម្បីស្រូបទ្រព្យក្នុងយុគទី ៩?"

    result = master.consult(
        query=query,
        birth_date=birth_date,
        birth_time=birth_time,
        gender=gender,
        house_degree=house_degree,
        complex_reasoning=True
    )

    print("\n" + "=" * 80)
    print(f"🧠 MODEL USED: {result['model_used']}")
    print("=" * 80)
    print(result["synthesis"])
    print("=" * 80)


import multiprocessing

def run_all():
    """Run both FastAPI REST API and Telegram Bot concurrently in isolated processes."""
    logger.info("Starting Supreme Feng Shui All-in-One Daemon...")
    # Start bot in separate background daemon process if token exists
    if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_BOT_TOKEN != "your_telegram_bot_token_here":
        bot_proc = multiprocessing.Process(target=run_bot, daemon=True)
        bot_proc.start()
        logger.info(f"Telegram Bot process started with PID: {bot_proc.pid}")
    else:
        logger.warning("Telegram Bot is not started because TELEGRAM_BOT_TOKEN is empty or default in .env.")

    # Start FastAPI server on main process
    run_api()


def main():
    parser = argparse.ArgumentParser(description="Supreme Feng Shui AGI System Runner")
    parser.add_argument(
        "--mode",
        choices=["all", "api", "bot", "cli", "test"],
        default="all",
        help="Execution mode (default: all)"
    )
    args = parser.parse_args()

    if args.mode == "api":
        run_api()
    elif args.mode == "bot":
        run_bot()
    elif args.mode == "cli":
        run_cli()
    elif args.mode == "test":
        import unittest
        suite = unittest.defaultTestLoader.discover("tests")
        unittest.TextTestRunner().run(suite)
    else:
        run_all()


if __name__ == "__main__":
    main()
