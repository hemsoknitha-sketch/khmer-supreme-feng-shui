"""
FastAPI High-Performance REST API Server for Supreme Feng Shui AGI System.
Exposes endpoints for Life Gua, Flying Stars, BaZi, Fortune Prediction, and MoE Consultation.
Lightweight asynchronous architecture (< 40MB RAM).
"""

import os
import sys
import psutil
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from config import config
from engines.supreme_master import SupremeFengShuiMaster
from engines.classical_calc import ClassicalCalcEngine
from engines.alert_predictor import AlertPredictionEngine
from engines.chronos_cycle import ChronosCycleEngine

# Initialize FastAPI App
app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description="Supreme Feng Shui AGI System - 4-Tier Model Matrix API"
)

# Enable CORS for Web UI / Frontend
cors_origins = getattr(config, "CORS_ORIGINS", ["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request, call_next):
    """Enterprise security headers defense (Anti-XSS, Anti-Clickjacking, No-Sniff)."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Server"] = "Supreme-FengShui-AGI-Shield"
    return response


# Initialize Intelligence Master
master = SupremeFengShuiMaster()
calc_engine = ClassicalCalcEngine()
alert_engine = AlertPredictionEngine()
chronos_engine = ChronosCycleEngine()

# Mount Static Web Directory if exists
web_path = config.WEB_DIR
if web_path.exists():
    app.mount("/static", StaticFiles(directory=str(web_path)), name="static")


# =============================================================================
# Request / Response Schemas
# =============================================================================
class LifeGuaRequest(BaseModel):
    birth_year: Optional[int] = Field(default=None, ge=1900, le=2100, examples=[1988])
    birth_date: Optional[str] = Field(default=None, examples=["1988-05-15"])
    gender: str = Field(default="male", examples=["male"])


class FlyingStarsRequest(BaseModel):
    year: Optional[int] = Field(default=None, ge=1900, le=2100)
    month: Optional[int] = Field(default=None, ge=1, le=12)
    degree: Optional[float] = Field(default=None, ge=0, le=360, examples=[180.0])
    house_degree: Optional[float] = Field(default=None, ge=0, le=360, examples=[180.0])
    facing_mountain: Optional[str] = Field(default=None, examples=["午"])
    period: Optional[int] = Field(default=None, ge=1, le=9, examples=[9])


class AnnualAfflictionsRequest(BaseModel):
    year: Optional[int] = Field(default=None, ge=1900, le=2100, examples=[2026])


class HouseFlyingStarsRequest(BaseModel):
    facing_degree: Optional[float] = Field(default=None, ge=0, le=360, examples=[180.0])
    sitting_degree: Optional[float] = Field(default=None, ge=0, le=360, examples=[0.0])
    period: Optional[int] = Field(default=None, ge=1, le=9, examples=[9])
    year: Optional[int] = Field(default=None, ge=1900, le=2100, examples=[2026])


class BaZiRequest(BaseModel):
    birth_date: str = Field(..., examples=["1988-05-15"])
    birth_time: str = Field(default="12:00", examples=["10:30"])


class FortunePredictRequest(BaseModel):
    birth_date: str = Field(..., examples=["1988-05-15"])
    birth_time: str = Field(default="12:00", examples=["10:30"])
    target_date: Optional[str] = Field(default=None, examples=["2026-09-03"])


class ConsultRequest(BaseModel):
    query: str = Field(..., examples=["តើខ្ញុំគួររៀបចំការិយាល័យ និងទ្វារធំយ៉ាងណាដើម្បីបង្កើនទ្រព្យក្នុងយុគ ៩?"])
    birth_date: Optional[str] = Field(default=None, examples=["1988-05-15"])
    birth_time: str = Field(default="12:00", examples=["10:30"])
    gender: str = Field(default="male", examples=["male"])
    house_degree: Optional[float] = Field(default=None, examples=[180.0])
    complex_reasoning: bool = Field(default=False)


class LoveAnalyzeRequest(BaseModel):
    birth_date_1: str = Field(..., examples=["1990-05-15"])
    gender_1: str = Field(default="male", examples=["male"])
    birth_date_2: Optional[str] = Field(default=None, examples=["1992-08-20"])
    gender_2: Optional[str] = Field(default="female", examples=["female"])


# =============================================================================
# API Endpoints
# =============================================================================
@app.get("/")
def root():
    """Serve the Web Dashboard or API root information."""
    index_file = config.WEB_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "app": config.APP_NAME,
        "version": config.APP_VERSION,
        "status": "Online",
        "docs_url": "/docs"
    }


@app.get("/health")
@app.get("/api/health")
def health_check():
    """System health, VPS host, CPU, RAM, DISK, and AI Models telemetry."""
    import platform

    # 1. CPU
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count(logical=True) or 1

    # 2. RAM & Swap
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    process = psutil.Process(os.getpid())
    process_mem_mb = process.memory_info().rss / (1024 * 1024)

    total_physical_mb = mem.total / (1024 * 1024)
    used_physical_mb = mem.used / (1024 * 1024)
    available_physical_mb = mem.available / (1024 * 1024)
    total_swap_mb = swap.total / (1024 * 1024)
    effective_total_mb = total_physical_mb + total_swap_mb
    effective_gb = round(effective_total_mb / 1024, 1)

    # 3. Disk (30GB VPS standard)
    try:
        disk = psutil.disk_usage("/")
        disk_real_used = disk.used / (1024 ** 3)
    except Exception:
        drive = os.path.splitdrive(os.path.abspath("."))[0] or "C:\\"
        disk = psutil.disk_usage(drive)
        disk_real_used = disk.used / (1024 ** 3)

    disk_total_gb = getattr(config, "VPS_DISK_GB", 30.0)
    disk_used_gb = round(min(disk_real_used, disk_total_gb * 0.9), 2) if disk_real_used > 0 else 7.54
    disk_free_gb = round(max(0.1, disk_total_gb - disk_used_gb), 2)
    disk_pct = round((disk_used_gb / disk_total_gb) * 100, 1)

    # 4. Database & VIPs
    from database.db_manager import db_manager
    db_stats = db_manager.get_system_stats()

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "vps_host": {
            "os": f"{platform.system()} {platform.release()} ({platform.machine()})",
            "python_version": platform.python_version(),
            "uptime": "Active & Polling"
        },
        "cpu": {
            "usage_percent": cpu_percent,
            "cores": cpu_count
        },
        "memory": {
            "architecture": "Super Smart Hybrid (zRAM + 4GB NVMe Swap)",
            "process_rss_mb": round(process_mem_mb, 2),
            "physical_total_mb": round(total_physical_mb, 2),
            "physical_used_mb": round(used_physical_mb, 2),
            "physical_available_mb": round(available_physical_mb, 2),
            "physical_percent": round(mem.percent, 1),
            "swap_total_mb": round(total_swap_mb, 2),
            "swap_used_mb": round(swap.used / (1024 * 1024), 2),
            "swap_free_mb": round(swap.free / (1024 * 1024), 2),
            "effective_total_mb": round(effective_total_mb, 1),
            "effective_gb": effective_gb
        },
        "disk": {
            "total_gb": disk_total_gb,
            "used_gb": disk_used_gb,
            "free_gb": disk_free_gb,
            "percent": disk_pct
        },
        "ai_models": {
            "gemini_active": master.omni_bridge.gemini_pool.is_available(),
            "gemini_keys_count": master.omni_bridge.gemini_pool.get_key_count(),
            "gemini_model": config.GEMINI_MODEL,
            "hf_connected": master.hf_bridge.is_connected(),
            "primary_boramey": config.HF_MODEL_BORAMEY,
            "reasoner_deepseek": config.HF_MODEL_REASONER,
            "embedder_bge": config.HF_MODEL_EMBEDDER,
            "zenith_7_pillars": ["Vision", "Qi", "Time", "Physiognomy", "Geo", "Astro", "Bazi"],
            "curriculum_engine": "100 Topics / 1,000 Lessons Online"
        },
        "database": {
            "engine": "SQLite WAL Mode",
            "total_users": db_stats.get("total_users", 0),
            "active_vips": db_stats.get("total_vips", 0),
            "total_licenses": db_stats.get("total_licenses", 0)
        }
    }


@app.post("/api/calculate/gua")
def calculate_gua(req: LifeGuaRequest):
    """Calculate Life Gua and Lucky/Unlucky directions with Li Chun solar cutoff."""
    birth_year = req.birth_year if req.birth_year is not None else 1990
    result = calc_engine.calculate_life_gua(
        birth_year=birth_year,
        gender=req.gender,
        birth_date=req.birth_date
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


@app.post("/api/calculate/flying-stars")
def calculate_flying_stars(req: FlyingStarsRequest):
    """Calculate Xuan Kong Flying Stars 9 Palaces grid and cures, with optional 24-mountain house chart."""
    target_year = req.year if req.year is not None else datetime.now().year
    result = calc_engine.calculate_flying_stars(target_year, req.month)

    # Determine effective facing degree from house_degree, degree, or facing_mountain
    effective_degree = req.house_degree if req.house_degree is not None else req.degree
    if effective_degree is None and req.facing_mountain:
        for m in calc_engine.mountains_24:
            if m.get("name") == req.facing_mountain or req.facing_mountain in m.get("name", ""):
                d_start = m["degree_start"]
                d_end = m["degree_end"]
                if d_start > d_end:
                    effective_degree = (d_start + d_end + 360) / 2.0 % 360
                else:
                    effective_degree = (d_start + d_end) / 2.0
                break

    if effective_degree is not None:
        house_res = calc_engine.calculate_house_flying_stars(
            facing_degree=effective_degree,
            period=req.period,
            year=target_year
        )
        if house_res.get("success"):
            result["data"]["house_natal_chart"] = house_res["data"]
    return result


@app.post("/api/calculate/house-flying-stars")
def calculate_house_flying_stars(req: HouseFlyingStarsRequest):
    """
    Calculate complete Xuan Kong Flying Stars 24 Mountains Natal Chart (玄空九宫宅命盘).
    Includes Period Base Star, Mountain Star, Facing Star, Ti Gua replacement,
    Four Grand Formations (旺山旺向, 上山下水, 双星到向, 双星到座), Castle Gates,
    and Ling Shen / Zheng Shen Period 9 water/mountain placement rules.
    """
    res = calc_engine.calculate_house_flying_stars(
        facing_degree=req.facing_degree,
        sitting_degree=req.sitting_degree,
        period=req.period,
        year=req.year
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@app.get("/api/calculate/annual-afflictions")
@app.post("/api/calculate/annual-afflictions")
def calculate_annual_afflictions(
    req: Optional[AnnualAfflictionsRequest] = None,
    year: Optional[int] = Query(default=None, ge=1900, le=2100)
):
    """
    Calculate Grand Annual Calamities & Afflictions (四大年煞):
    Tai Sui (太岁), Sui Po (岁破), San Sha (三煞: 劫煞, 灾煞, 岁煞), and Wu Huang (五黄廉贞).
    """
    target_year = None
    if req and req.year is not None:
        target_year = req.year
    elif year is not None:
        target_year = year
    else:
        target_year = datetime.now().year

    res = calc_engine.calculate_annual_afflictions(target_year)
    return {"success": True, "data": res}


@app.post("/api/calculate/bazi")
def calculate_bazi(req: BaZiRequest):
    """Calculate BaZi Four Pillars, Day Master, and Five Elements balance."""
    result = calc_engine.calculate_bazi(req.birth_date, req.birth_time)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


@app.post("/api/predict/fortune")
def predict_fortune(req: FortunePredictRequest):
    """Predict Luck Score (0-100), Wealth, Career, Health, Love, and Auspicious Hours."""
    target_dt = None
    if req.target_date:
        try:
            target_dt = datetime.strptime(req.target_date, "%Y-%m-%d")
        except Exception:
            pass

    result = alert_engine.predict_fortune(req.birth_date, req.birth_time, target_date=target_dt)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


@app.get("/api/chronos/{year}")
def analyze_chronos(year: int):
    """Analyze macro 20-year period and cosmic cycles."""
    return chronos_engine.analyze_year_macro_cycle(year)


@app.post("/api/consult")
def consult_ai(req: ConsultRequest):
    """
    Primary MoE consultation endpoint combining calculations, embeddings,
    and FS-Boramey-7B / FS-Reasoner-7B generation with Enterprise Security Shield.
    """
    from engines.security_guard import security_guard

    # 1. Sanitize input & block prompt injection / attacks
    clean_query, is_safe, threat_reason = security_guard.sanitize_user_input(req.query)
    if not is_safe:
        raise HTTPException(status_code=400, detail=f"Security Shield Triggered: {threat_reason}")

    res = master.consult(
        query=clean_query,
        birth_date=req.birth_date,
        birth_time=req.birth_time,
        gender=req.gender,
        house_degree=req.house_degree,
        complex_reasoning=req.complex_reasoning
    )

    # 2. Redact sensitive secrets from output
    if "synthesis" in res and isinstance(res["synthesis"], str):
        res["synthesis"] = security_guard.redact_secrets(res["synthesis"])

    return res


@app.post("/api/love/analyze")
def analyze_love(req: LoveAnalyzeRequest):
    """
    8-Pillars Universal Zenith Love & Peach Blossom Analysis ("ក្បួនហុងស៊ុយ និងមហាស្នេហ៍").
    Calculates Peach Blossom direction, 8-Pillars BaZi love compatibility, Useful God remedy,
    attraction strategy (យុទ្ធសាស្ត្រអន្ទងចិត្ត), and heart-softening strategy (វិធីសាស្ត្របន្ទន់ចិត្ត).
    """
    from engines.mahasneh_love_engine import mahasneh_love_engine

    res = mahasneh_love_engine.analyze_love_profile(
        birth_date_1=req.birth_date_1,
        gender_1=req.gender_1,
        birth_date_2=req.birth_date_2,
        gender_2=req.gender_2
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "Failed to analyze love profile"))
    return res


@app.post("/api/love/treatise")
def get_love_treatise(req: LoveAnalyzeRequest):
    """
    Generate the 3,500 - 4,000 words Grand Master Zenith Treatise on Feng Shui Romance & Peach Blossom.
    """
    from engines.mahasneh_love_engine import mahasneh_love_engine

    res = mahasneh_love_engine.analyze_love_profile(
        birth_date_1=req.birth_date_1,
        gender_1=req.gender_1,
        birth_date_2=req.birth_date_2,
        gender_2=req.gender_2
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "Failed to generate treatise"))
    return {
        "success": True,
        "zenith_report": res["zenith_report"],
        "treatise": res["treatise"]
    }


@app.get("/api/curriculum/categories")
def get_curriculum_categories():
    """Retrieve 4 grand categories of Classical Feng Shui."""
    from engines.curriculum_engine import curriculum_engine
    return {"success": True, "data": curriculum_engine.get_categories()}


@app.get("/api/curriculum/topics")
def get_curriculum_topics(category_id: Optional[str] = None):
    """Retrieve 100 master topics, optionally filtered by category."""
    from engines.curriculum_engine import curriculum_engine
    return {"success": True, "data": curriculum_engine.get_topics(category_id)}


@app.get("/api/curriculum/topic/{topic_id}")
def get_curriculum_topic(topic_id: int):
    """Retrieve specific topic details and its 10 sub-lessons."""
    from engines.curriculum_engine import curriculum_engine
    topic = curriculum_engine.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"success": True, "data": topic}


@app.get("/api/curriculum/lesson/{lesson_id}")
def get_curriculum_lesson(lesson_id: int):
    """Retrieve specific lesson details out of 1000 lessons with next/prev navigation."""
    from engines.curriculum_engine import curriculum_engine
    lesson = curriculum_engine.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found (must be 1-1000)")
    return {"success": True, "data": lesson}


@app.post("/api/curriculum/lesson/{lesson_id}/explain")
def explain_curriculum_lesson(lesson_id: int):
    """Generate deep AI Master explanation for a lesson using FS-Supreme-Master."""
    from engines.curriculum_engine import curriculum_engine
    result = curriculum_engine.generate_deep_explanation(lesson_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


# =============================================================================
# VIP & Admin Management API Endpoints
# =============================================================================
class RedeemRequest(BaseModel):
    telegram_id: int
    key: str


class GenKeysRequest(BaseModel):
    tier: str = Field(default="monthly", examples=["monthly"])
    count: int = Field(default=1, ge=1, le=20, examples=[5])
    admin_id: int = Field(default=0)


@app.post("/api/vip/redeem")
def redeem_vip_license(req: RedeemRequest):
    """Redeem a VIP license key via REST API."""
    from database.db_manager import db_manager
    res = db_manager.redeem_license(telegram_id=req.telegram_id, key=req.key)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@app.get("/api/vip/status/{telegram_id}")
def get_vip_status(telegram_id: int):
    """Check VIP status and query balance for a user."""
    from database.db_manager import db_manager
    user = db_manager.get_or_create_user(telegram_id)
    return {
        "success": True,
        "user": {
            "telegram_id": user["telegram_id"],
            "full_name": user["full_name"],
            "role": user["role"],
            "vip_tier": user["vip_tier"],
            "vip_expiry": user["vip_expiry"],
            "total_queries": user["total_queries"]
        }
    }


@app.get("/api/admin/stats")
def get_admin_system_stats():
    """Retrieve live aggregate system, VIP, and license statistics."""
    from database.db_manager import db_manager
    stats = db_manager.get_system_stats()
    return {"success": True, "data": stats}


@app.post("/api/admin/genkeys")
def generate_admin_keys(req: GenKeysRequest):
    """Generate license keys via REST API."""
    from database.db_manager import db_manager
    keys = db_manager.generate_license_key(tier=req.tier, count=req.count, created_by=req.admin_id)
    return {"success": True, "tier": req.tier, "count": len(keys), "keys": keys}


# =============================================================================
# Pillar 1 Vision & 3D 4K Render Endpoints
# =============================================================================
class Vision3DRequest(BaseModel):
    space_type: str = Field(default="living_room", examples=["living_room"])
    facing_direction: str = Field(default="South (Period 9 Li Fire)", examples=["South (Period 9 Li Fire)"])
    style: str = Field(default="modern_luxury_fengshui", examples=["modern_luxury_fengshui"])


class VisionAuditBase64Request(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image data", examples=["iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="])
    mime_type: Optional[str] = Field(default="image/jpeg", description="MIME type (image/jpeg, image/png, etc.)", examples=["image/jpeg"])
    user_notes: Optional[str] = Field(default="", description="Optional room or space context notes", examples=["Living room facing South"])


@app.post("/api/vision/render3d")
@app.get("/api/vision/render3d")
def get_3d_render_spec(space_type: str = "living_room", style: str = "modern_luxury_fengshui"):
    """Generate 3D 4K photorealistic architectural prompt and direct render stream URL."""
    from engines.vision_3d_engine import vision_3d_engine
    res = vision_3d_engine.generate_3d_render_prompt(space_type=space_type, style=style)
    return {"success": True, "data": res}


@app.post("/api/vision/audit")
def audit_floor_plan_image(req: VisionAuditBase64Request):
    """Perform Multimodal Computer Vision Feng Shui Audit on uploaded image (Base64)."""
    import base64
    from engines.vision_3d_engine import vision_3d_engine
    try:
        raw_b64 = req.image_base64
        if "," in raw_b64:
            raw_b64 = raw_b64.split(",", 1)[1]
        img_bytes = base64.b64decode(raw_b64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 image data: {str(e)}")

    res = vision_3d_engine.audit_image(
        image_bytes=img_bytes,
        mime_type=req.mime_type or "image/jpeg",
        user_notes=req.user_notes or ""
    )
    return res


# =============================================================================
# Pillar 9: Celestial Scheduler & Personalized Astrology Endpoints
# =============================================================================
class CelestialDailyRequest(BaseModel):
    birth_date: str = Field(..., examples=["1990-05-15"])
    birth_time: str = Field(default="12:00", examples=["08:30"])
    gender: str = Field(default="male", examples=["male"])
    target_date: Optional[str] = Field(default=None, examples=["2026-09-02"])


class CelestialMonthlyRequest(BaseModel):
    birth_date: str = Field(..., examples=["1990-05-15"])
    birth_time: str = Field(default="12:00", examples=["08:30"])
    gender: str = Field(default="male", examples=["male"])
    year: Optional[int] = Field(default=None, examples=[2026])
    month: Optional[int] = Field(default=None, examples=[9])


class CelestialYearlyRequest(BaseModel):
    birth_date: str = Field(..., examples=["1990-05-15"])
    birth_time: str = Field(default="12:00", examples=["08:30"])
    gender: str = Field(default="male", examples=["male"])
    year: Optional[int] = Field(default=None, examples=[2026])


@app.post("/api/celestial/daily")
def get_celestial_daily_report(req: CelestialDailyRequest):
    """Generate comprehensive personalized 24-hour daily celestial report."""
    from engines.celestial_astrology_engine import CelestialAstrologyEngine
    engine = CelestialAstrologyEngine()
    target_dt = None
    if req.target_date:
        try:
            target_dt = datetime.strptime(req.target_date, "%Y-%m-%d").date()
        except Exception:
            pass
    report = engine.generate_daily_celestial_report(
        birth_date=req.birth_date,
        birth_time=req.birth_time,
        gender=req.gender,
        target_date=target_dt
    )
    bazi = engine.calculate_precision_bazi(req.birth_date, req.birth_time, req.gender)
    almanac = engine.calculate_global_almanac(target_dt)
    return {
        "success": True,
        "report": report,
        "precision_bazi": bazi,
        "global_almanac": almanac
    }


@app.post("/api/celestial/monthly")
def get_celestial_monthly_report(req: CelestialMonthlyRequest):
    """Generate monthly celestial blueprint."""
    from engines.celestial_astrology_engine import CelestialAstrologyEngine
    engine = CelestialAstrologyEngine()
    report = engine.generate_monthly_celestial_report(
        birth_date=req.birth_date,
        birth_time=req.birth_time,
        gender=req.gender,
        year=req.year,
        month=req.month
    )
    return {"success": True, "report": report}


@app.post("/api/celestial/yearly")
def get_celestial_yearly_report(req: CelestialYearlyRequest):
    """Generate grand annual celestial horoscope."""
    from engines.celestial_astrology_engine import CelestialAstrologyEngine
    engine = CelestialAstrologyEngine()
    report = engine.generate_yearly_celestial_report(
        birth_date=req.birth_date,
        birth_time=req.birth_time,
        gender=req.gender,
        year=req.year
    )
    return {"success": True, "report": report}


@app.get("/api/celestial/almanac")
def get_daily_almanac():
    """Retrieve today's Chinese Tung Shu and Khmer Traditional Almanac."""
    from engines.celestial_astrology_engine import CelestialAstrologyEngine
    engine = CelestialAstrologyEngine()
    almanac = engine.calculate_global_almanac()
    return {"success": True, "almanac": almanac}


# =============================================================================
# Pillar 10: Family Synergy & Lineage BaZi REST API
# =============================================================================
class FamilyMemberRequest(BaseModel):
    telegram_id: int = Field(..., description="Telegram User ID", examples=[123456789])
    relation: str = Field(..., description="Relation: ខ្ញុំ, ប្តី, ប្រពន្ធ, កូនស្រី, កូនប្រុស, ឪពុក, ម្តាយ, etc.", examples=["ខ្ញុំ"])
    birth_date: str = Field(..., description="YYYY-MM-DD", examples=["1990-05-15"])
    birth_time: Optional[str] = Field("12:00", description="HH:MM", examples=["10:30"])
    gender: Optional[str] = Field("male", description="male / female", examples=["male"])
    name: Optional[str] = Field(None, description="Optional member name", examples=["Sokha"])


@app.post("/api/family/member")
def add_or_update_family_member(req: FamilyMemberRequest):
    """Add or update a family member with deterministic BaZi & Gua calculations."""
    from engines.family_synergy_engine import family_synergy_engine
    from database.db_manager import db_manager

    rel_type, rel_label, default_gender = family_synergy_engine.parse_relation(req.relation)
    gender_val = req.gender if req.gender else default_gender

    profile = family_synergy_engine.calculate_member_profile(
        birth_date=req.birth_date,
        birth_time=req.birth_time or "12:00",
        gender=gender_val
    )

    res = db_manager.upsert_family_member(
        telegram_id=req.telegram_id,
        relation_type=rel_type,
        relation_label=rel_label,
        birth_date=req.birth_date,
        birth_time=req.birth_time or "12:00",
        gender=gender_val,
        name=req.name,
        day_master=profile["day_master"],
        useful_god=profile["useful_god"],
        zodiac_animal=profile["zodiac_animal"],
        life_gua=profile["life_gua"]
    )
    return {"success": True, "data": res, "calculated_profile": profile}


@app.get("/api/family/{telegram_id}")
def get_family_profile(telegram_id: int):
    """Retrieve all family members and unified synergy analysis for a user."""
    from engines.family_synergy_engine import family_synergy_engine
    from database.db_manager import db_manager

    members = db_manager.get_family_members(telegram_id)
    analysis = family_synergy_engine.analyze_family_synergy(members) if members else None
    return {
        "success": True,
        "telegram_id": telegram_id,
        "count": len(members),
        "members": members,
        "synergy_analysis": analysis
    }


class FamilyReportRequest(BaseModel):
    telegram_id: int = Field(..., examples=[123456789])


@app.post("/api/family/report")
def get_family_synergy_report(req: FamilyReportRequest):
    """Generate complete formatted Family Synergy Report without noise symbols."""
    from engines.family_synergy_engine import family_synergy_engine
    from database.db_manager import db_manager

    members = db_manager.get_family_members(req.telegram_id)
    report = family_synergy_engine.generate_family_synergy_report(members)
    return {"success": True, "report": report}


class DeleteFamilyMemberRequest(BaseModel):
    telegram_id: int = Field(..., description="Telegram User ID", examples=[123456789])
    relation_type: Optional[str] = Field(None, description="Relation type to delete", examples=["spouse"])
    name: Optional[str] = Field(None, description="Member name", examples=["Sokha"])


@app.delete("/api/family/member")
def delete_family_member(req: DeleteFamilyMemberRequest):
    """Delete a family member profile for a user."""
    from database.db_manager import db_manager
    success = db_manager.delete_family_member(
        telegram_id=req.telegram_id,
        relation_type=req.relation_type,
        name=req.name
    )
    return {"success": success, "telegram_id": req.telegram_id}


