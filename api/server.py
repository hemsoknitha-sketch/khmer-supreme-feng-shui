"""
FastAPI High-Performance REST API Server for Supreme Feng Shui AGI System.
Exposes endpoints for Life Gua, Flying Stars, BaZi, Fortune Prediction, and MoE Consultation.
Lightweight asynchronous architecture (< 40MB RAM).
"""

import os
import psutil
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    birth_year: int = Field(..., ge=1900, le=2100, example=1988)
    gender: str = Field(default="male", example="male")


class FlyingStarsRequest(BaseModel):
    year: int = Field(default=2024, ge=1900, le=2100)
    month: Optional[int] = Field(default=None, ge=1, le=12)


class BaZiRequest(BaseModel):
    birth_date: str = Field(..., example="1988-05-15")
    birth_time: str = Field(default="12:00", example="10:30")


class FortunePredictRequest(BaseModel):
    birth_date: str = Field(..., example="1988-05-15")
    birth_time: str = Field(default="12:00", example="10:30")


class ConsultRequest(BaseModel):
    query: str = Field(..., example="តើខ្ញុំគួររៀបចំការិយាល័យ និងទ្វារធំយ៉ាងណាដើម្បីបង្កើនទ្រព្យក្នុងយុគ ៩?")
    birth_date: Optional[str] = Field(default=None, example="1988-05-15")
    birth_time: str = Field(default="12:00", example="10:30")
    gender: str = Field(default="male", example="male")
    house_degree: Optional[float] = Field(default=None, example=180.0)
    complex_reasoning: bool = Field(default=False)


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
def health_check():
    """System health and Super Smart Hybrid Memory telemetry (for 1GB VPS monitoring)."""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    process = psutil.Process(os.getpid())
    process_mem_mb = process.memory_info().rss / (1024 * 1024)

    total_physical_mb = mem.total / (1024 * 1024)
    total_swap_mb = swap.total / (1024 * 1024)
    effective_total_mb = total_physical_mb + total_swap_mb

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "memory_architecture": "Super Smart Hybrid (zRAM + 4GB NVMe Swap)",
        "process_ram_used_mb": round(process_mem_mb, 2),
        "physical_ram_total_mb": round(total_physical_mb, 2),
        "physical_ram_available_mb": round(mem.available / (1024 * 1024), 2),
        "physical_ram_percent": mem.percent,
        "swap_total_mb": round(total_swap_mb, 2),
        "swap_used_mb": round(swap.used / (1024 * 1024), 2),
        "swap_free_mb": round(swap.free / (1024 * 1024), 2),
        "effective_total_ram_mb": round(effective_total_mb, 2),
        "hf_connected": master.hf_bridge.is_connected()
    }


@app.post("/api/calculate/gua")
def calculate_gua(req: LifeGuaRequest):
    """Calculate Life Gua and Lucky/Unlucky directions."""
    result = calc_engine.calculate_life_gua(req.birth_year, req.gender)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


@app.post("/api/calculate/flying-stars")
def calculate_flying_stars(req: FlyingStarsRequest):
    """Calculate Xuan Kong Flying Stars 9 Palaces grid and cures."""
    result = calc_engine.calculate_flying_stars(req.year, req.month)
    return result


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
    result = alert_engine.predict_fortune(req.birth_date, req.birth_time)
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
    and FS-Boramey-7B / FS-Reasoner-7B generation.
    """
    return master.consult(
        query=req.query,
        birth_date=req.birth_date,
        birth_time=req.birth_time,
        gender=req.gender,
        house_degree=req.house_degree,
        complex_reasoning=req.complex_reasoning
    )


@app.get("/api/curriculum")
def get_curriculum():
    """Retrieve 100 Topics Feng Shui training curriculum."""
    kb_path = config.DATA_DIR / "knowledge_base.json"
    if kb_path.exists():
        import json
        with open(kb_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"categories": []}
