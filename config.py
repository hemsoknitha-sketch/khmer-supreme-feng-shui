"""
Supreme Feng Shui AGI System - Central Configuration Module
Optimized for Google Cloud 1GB RAM VPS and Hugging Face Cloud Integration.
"""

import os
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file if present
load_dotenv(BASE_DIR / ".env")


class SystemConfig:
    """Core system configuration loaded from environment or defaults."""

    # Project metadata
    APP_NAME: str = "Supreme Feng Shui AGI System"
    APP_VERSION: str = "1.0.0-Supreme"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("API_DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Paths
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    WEB_DIR: Path = BASE_DIR / "web"
    CACHE_DIR: Path = BASE_DIR / "cache"
    MODELS_DIR: Path = BASE_DIR / "models"

    # Hugging Face Access Token & Model Configuration
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    HF_MODEL_TRAINED: str = os.getenv("HF_MODEL_TRAINED", "hemsinath/khmer-supreme-feng-shui")
    HF_MODEL_BORAMEY: str = os.getenv("HF_MODEL_BORAMEY", "hemsinath/khmer-supreme-feng-shui")
    HF_MODEL_REASONER: str = os.getenv("HF_MODEL_REASONER", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
    HF_MODEL_MAHASNEH: str = os.getenv("HF_MODEL_MAHASNEH", "Qwen/Qwen2.5-72B-Instruct")
    HF_MODEL_LLAMA: str = os.getenv("HF_MODEL_LLAMA", "meta-llama/Llama-3.3-70B-Instruct")
    HF_MODEL_DEEPSEEK_R1: str = os.getenv("HF_MODEL_DEEPSEEK_R1", "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B")
    HF_MODEL_MISTRAL: str = os.getenv("HF_MODEL_MISTRAL", "mistralai/Mistral-Small-24B-Instruct-2501")
    HF_MODEL_EMBEDDER: str = os.getenv("HF_MODEL_EMBEDDER", "BAAI/bge-m3")

    # Google Gemini API Multi-Key Pool & Rotation (Supports single or multiple keys comma-separated)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_API_KEYS_RAW: str = os.getenv("GEMINI_API_KEYS", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    @property
    def GEMINI_KEY_POOL(self) -> List[str]:
        """Extract and clean all available valid Gemini API keys into a resilient pool."""
        keys = []
        raw_candidates = []
        if self.GEMINI_API_KEY:
            raw_candidates.append(self.GEMINI_API_KEY.strip())
        if self.GEMINI_API_KEYS_RAW:
            for k in self.GEMINI_API_KEYS_RAW.split(","):
                raw_candidates.append(k.strip())
        for k in raw_candidates:
            # Valid Google AI Studio Gemini API keys begin with 'AIzaSy'
            if k and k.startswith("AIzaSy") and k not in keys:
                keys.append(k)
        return keys

    # Custom Dedicated Endpoint URLs (Optional)
    HF_ENDPOINT_BORAMEY: str = os.getenv("HF_ENDPOINT_BORAMEY", "")
    HF_ENDPOINT_REASONER: str = os.getenv("HF_ENDPOINT_REASONER", "")

    # Telegram Bot Token (supports both TELEGRAM_BOT_TOKEN and TELEGRAM_TOKEN)
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN") or ""

    # Super Admin Telegram User IDs (Comma-separated in .env: ADMIN_USER_IDS=1234567,7654321)
    ADMIN_USER_IDS: List[int] = [
        int(uid.strip()) for uid in os.getenv("ADMIN_USER_IDS", "").split(",") if uid.strip().isdigit()
    ]

    # API Server Settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    CORS_ORIGINS: List[str] = [
        orig.strip() for orig in os.getenv("CORS_ORIGINS", "*").split(",") if orig.strip()
    ]

    # Memory & Storage Management for 1GB VPS (30GB NVMe Disk)
    MAX_RAM_MB: int = int(os.getenv("MAX_RAM_MB", "800"))
    VPS_DISK_GB: float = float(os.getenv("VPS_DISK_GB", "30.0"))
    ENABLE_LOCAL_CACHE: bool = os.getenv("ENABLE_LOCAL_CACHE", "true").lower() == "true"
    CACHE_EXPIRATION_HOURS: int = 24
    MAX_FREE_DAILY_QUERIES: int = int(os.getenv("MAX_FREE_DAILY_QUERIES", "0"))

    # Feng Shui Classical Knowledge Constants
    FENGSHUI_SCHOOLS: List[str] = [
        "Ba Zhai (8 Mansions)",
        "Xuan Kong Flying Star",
        "Xuan Kong Da Gua",
        "BaZi (Four Pillars of Destiny)",
        "San He (Three Harmony)",
        "San Yuan (Three Cycles)",
        "Luan Tou (Landform Geomancy)",
        "I Ching Feng Shui",
        "Qi Men Dun Jia",
        "Zi Wei Dou Shu",
        "Date Selection (Ze Ri)",
        "Space Clearing & Geobiology"
    ]

    # 24 Mountains (二十四山)
    MOUNTAINS_24: List[Dict[str, Any]] = [
        {"name": "壬", "pinyin": "Ren", "degree_start": 337.5, "degree_end": 352.5, "direction": "N1", "trigram": "坎", "element": "水"},
        {"name": "子", "pinyin": "Zi", "degree_start": 352.5, "degree_end": 7.5, "direction": "N2", "trigram": "坎", "element": "水"},
        {"name": "癸", "pinyin": "Gui", "degree_start": 7.5, "degree_end": 22.5, "direction": "N3", "trigram": "坎", "element": "水"},
        {"name": "丑", "pinyin": "Chou", "degree_start": 22.5, "degree_end": 37.5, "direction": "NE1", "trigram": "艮", "element": "土"},
        {"name": "艮", "pinyin": "Gen", "degree_start": 37.5, "degree_end": 52.5, "direction": "NE2", "trigram": "艮", "element": "土"},
        {"name": "寅", "pinyin": "Yin", "degree_start": 52.5, "degree_end": 67.5, "direction": "NE3", "trigram": "艮", "element": "木"},
        {"name": "甲", "pinyin": "Jia", "degree_start": 67.5, "degree_end": 82.5, "direction": "E1", "trigram": "震", "element": "木"},
        {"name": "卯", "pinyin": "Mao", "degree_start": 82.5, "degree_end": 97.5, "direction": "E2", "trigram": "震", "element": "木"},
        {"name": "乙", "pinyin": "Yi", "degree_start": 97.5, "degree_end": 112.5, "direction": "E3", "trigram": "震", "element": "木"},
        {"name": "辰", "pinyin": "Chen", "degree_start": 112.5, "degree_end": 127.5, "direction": "SE1", "trigram": "巽", "element": "土"},
        {"name": "巽", "pinyin": "Xun", "degree_start": 127.5, "degree_end": 142.5, "direction": "SE2", "trigram": "巽", "element": "木"},
        {"name": "巳", "pinyin": "Si", "degree_start": 142.5, "degree_end": 157.5, "direction": "SE3", "trigram": "巽", "element": "火"},
        {"name": "丙", "pinyin": "Bing", "degree_start": 157.5, "degree_end": 172.5, "direction": "S1", "trigram": "离", "element": "火"},
        {"name": "午", "pinyin": "Wu", "degree_start": 172.5, "degree_end": 187.5, "direction": "S2", "trigram": "离", "element": "火"},
        {"name": "丁", "pinyin": "Ding", "degree_start": 187.5, "degree_end": 202.5, "direction": "S3", "trigram": "离", "element": "火"},
        {"name": "未", "pinyin": "Wei", "degree_start": 202.5, "degree_end": 217.5, "direction": "SW1", "trigram": "坤", "element": "土"},
        {"name": "坤", "pinyin": "Kun", "degree_start": 217.5, "degree_end": 232.5, "direction": "SW2", "trigram": "坤", "element": "土"},
        {"name": "申", "pinyin": "Shen", "degree_start": 232.5, "degree_end": 247.5, "direction": "SW3", "trigram": "坤", "element": "金"},
        {"name": "庚", "pinyin": "Geng", "degree_start": 247.5, "degree_end": 262.5, "direction": "W1", "trigram": "兑", "element": "金"},
        {"name": "酉", "pinyin": "You", "degree_start": 262.5, "degree_end": 277.5, "direction": "W2", "trigram": "兑", "element": "金"},
        {"name": "辛", "pinyin": "Xin", "degree_start": 277.5, "degree_end": 292.5, "direction": "W3", "trigram": "兑", "element": "金"},
        {"name": "戌", "pinyin": "Xu", "degree_start": 292.5, "degree_end": 307.5, "direction": "NW1", "trigram": "乾", "element": "土"},
        {"name": "乾", "pinyin": "Qian", "degree_start": 307.5, "degree_end": 322.5, "direction": "NW2", "trigram": "乾", "element": "金"},
        {"name": "亥", "pinyin": "Hai", "degree_start": 322.5, "degree_end": 337.5, "direction": "NW3", "trigram": "乾", "element": "水"}
    ]

    # Eight Trigrams (八卦)
    TRIGRAMS: Dict[str, Dict[str, Any]] = {
        "乾": {"name_kh": "ឈាន (Qian)", "direction": "NW", "element": "金 (Gold/Metal)", "number": 6, "nature": "មេឃ (Heaven)", "family": "ឪពុក (Father)"},
        "兑": {"name_kh": "ទុយ (Dui)", "direction": "W", "element": "金 (Gold/Metal)", "number": 7, "nature": "បឹង (Lake)", "family": "កូនស្រីពៅ (Youngest Daughter)"},
        "离": {"name_kh": "លី (Li)", "direction": "S", "element": "火 (Fire)", "number": 9, "nature": "ភ្លើង (Fire)", "family": "កូនស្រីកណ្តាល (Middle Daughter)"},
        "震": {"name_kh": "ជិន (Zhen)", "direction": "E", "element": "木 (Wood)", "number": 3, "nature": "ផ្គរលាន់ (Thunder)", "family": "កូនប្រុសច្បង (Eldest Son)"},
        "巽": {"name_kh": "ស៊ុន (Xun)", "direction": "SE", "element": "木 (Wood)", "number": 4, "nature": "ខ្យល់ (Wind)", "family": "កូនស្រីច្បង (Eldest Daughter)"},
        "坎": {"name_kh": "ខាំ (Kan)", "direction": "N", "element": "水 (Water)", "number": 1, "nature": "ទឹក (Water)", "family": "កូនប្រុសកណ្តាល (Middle Son)"},
        "艮": {"name_kh": "កឺន (Gen)", "direction": "NE", "element": "土 (Earth)", "number": 8, "nature": "ភ្នំ (Mountain)", "family": "កូនប្រុសពៅ (Youngest Son)"},
        "坤": {"name_kh": "ឃុន (Kun)", "direction": "SW", "element": "土 (Earth)", "number": 2, "nature": "ដី (Earth)", "family": "ម្តាយ (Mother)"}
    }


config = SystemConfig()
CORS_ORIGINS = config.CORS_ORIGINS
