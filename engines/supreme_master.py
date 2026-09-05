"""
FS-Supreme-Master (The Unified MoE Ensemble Model)
Orchestrates the entire intelligence matrix:
- FS-Boramey-7B (Generator & Teacher)
- FS-Reasoner-7B (Complex Reasoning & Step-by-Step CoT)
- FS-Embedder-M3 (Memory & Classical Knowledge Retrieval)
- FS-Classical-Calc-v1 (Zero-Error Mathematical Calculator)
- FS-Alert-Predictor (Fortune Scoring & Prediction Engine)
- FS-Chronos-Cycle (Macro-Period & Cosmic Time-Series Engine)
"""

import logging
from typing import Dict, Any, List, Optional
from config import config
from engines.classical_calc import ClassicalCalcEngine
from engines.hf_bridge import HuggingFaceBridge
from engines.omni_ai_bridge import omni_ai_bridge, OmniAIBridge
from engines.rag_client import RAGKnowledgeRetriever
from engines.alert_predictor import AlertPredictionEngine
from engines.chronos_cycle import ChronosCycleEngine
from engines.mahasneh_love_engine import mahasneh_love_engine
from engines.celestial_astrology_engine import CelestialAstrologyEngine

logger = logging.getLogger("SupremeFengShui.Master")


class SupremeFengShuiMaster:
    """FS-Supreme-Master: Unified Mixture of Experts (MoE) & Multi-Cloud Omni AI Architecture."""

    def __init__(self, hf_token: Optional[str] = None):
        logger.info("Initializing Supreme Feng Shui Master Orchestrator...")
        self.calc_engine = ClassicalCalcEngine()
        self.hf_bridge = HuggingFaceBridge(token=hf_token)
        self.omni_bridge = omni_ai_bridge
        self.rag_engine = RAGKnowledgeRetriever(token=hf_token)
        self.alert_predictor = AlertPredictionEngine()
        self.chronos_engine = ChronosCycleEngine()
        self.love_engine = mahasneh_love_engine
        self.celestial_engine = CelestialAstrologyEngine()
        logger.info("All 4 Engine Groups & Omni AI Mesh successfully linked to Master Orchestrator.")

    def consult(
        self,
        query: str,
        birth_date: Optional[str] = None,
        birth_time: str = "12:00",
        gender: str = "male",
        house_degree: Optional[float] = None,
        complex_reasoning: bool = False
    ) -> Dict[str, Any]:
        """
        Primary consultation pipeline. Coordinates all 4 model groups to produce
        an authentic, mathematically-grounded, and personalized Feng Shui synthesis.
        """
        evidence_packet = {}

        # 1. Classical Calculation Engine (FS-Classical-Calc-v1)
        if birth_date:
            try:
                gua_res = self.calc_engine.calculate_life_gua(birth_year=1990, gender=gender, birth_date=birth_date)
                bazi_res = self.calc_engine.calculate_bazi(birth_date, birth_time)
                if gua_res.get("success"):
                    evidence_packet["life_gua"] = gua_res["data"]
                if bazi_res.get("success"):
                    evidence_packet["bazi"] = bazi_res["data"]
            except Exception as e:
                logger.warning(f"Error parsing birth date for calculation: {e}")

        # 2. 24 Mountains & House Flying Stars Chart (玄空九宫宅命盘)
        from datetime import datetime
        current_year = datetime.now().year

        if house_degree is not None:
            mountain_res = self.calc_engine.get_mountain_by_degree(house_degree)
            if mountain_res.get("success"):
                evidence_packet["24_mountains"] = mountain_res["mountain"]

            # Calculate complete Xuan Kong Natal Chart for the property
            house_chart = self.calc_engine.calculate_house_flying_stars(
                facing_degree=house_degree,
                year=current_year
            )
            if house_chart.get("success"):
                evidence_packet["xuan_kong_house_natal_chart"] = house_chart["data"]

        # 3. Annual Flying Stars (Current Year Period 9)
        flying_stars = self.calc_engine.calculate_flying_stars(current_year)
        if flying_stars.get("success"):
            evidence_packet[f"flying_stars_{current_year}"] = flying_stars["data"]
            evidence_packet["flying_stars_current"] = flying_stars["data"]

        # 4. Fortune Prediction (FS-Alert-Predictor)
        if birth_date:
            pred_res = self.alert_predictor.predict_fortune(birth_date, birth_time)
            if pred_res.get("success"):
                evidence_packet["fortune_prediction"] = pred_res["data"]

        # 5. Maha Sneh & Peach Blossom Engine (ក្បួនហុងស៊ុយ និងមហាស្នេហ៍)
        love_keywords = ["ស្នេហ៍", "ស្នេហា", "គូស្នេហ៍", "ផ្កាប៉េស", "peach blossom", "love", "marriage", "អន្ទងចិត្ត", "បន្ទន់ចិត្ត"]
        if any(k in query.lower() for k in love_keywords) and birth_date:
            love_res = self.love_engine.analyze_love_profile(birth_date, gender)
            if love_res.get("success"):
                evidence_packet["mahasneh_love"] = love_res

        # 6. Knowledge Retrieval (FS-Embedder-M3)
        relevant_docs = self.rag_engine.search_knowledge(query, top_k=3)
        knowledge_context = "\n".join([f"• [{d['category']}] {d['title']}: {d['text']}" for d in relevant_docs])

        # 7. Construct Verified Master System Prompt
        system_prompt = (
            "អ្នកគឺជា FS-Supreme-Master (កំពូលបរមគ្រូបញ្ញាសិប្បនិម្មិតហុងស៊ុយបុរាណ AGI - Master Level)។ "
            "ចូរឆ្លើយតបយ៉ាងពិរោះ ជ្រាលជ្រៅ និងត្រឹមត្រូវតាមក្បួនខ្នាតបុរាណចិន និងខ្មែរ ដោយផ្អែកលើទិន្នន័យជាក់ស្តែងខាងក្រោម៖\n\n"
            f"[ទិន្នន័យគណនាពិតពីម៉ាស៊ីន]:\n{evidence_packet}\n\n"
            f"[ចំណេះដឹងយោងពីបណ្ណាល័យហុងស៊ុយបុរាណ]:\n{knowledge_context}"
        )

        # 7. Generate Supreme Synthesis via Multi-Cloud Omni AI Mesh (Gemini Multi-Key + HuggingFace + Local Core)
        ai_response = self.omni_bridge.generate_supreme_consultation(
            system_prompt=system_prompt,
            user_prompt=query,
            context_knowledge=knowledge_context
        )

        model_name = "Omni-AI (Gemini Mesh + HF Boramey/Reasoner)"
        if self.omni_bridge.gemini_pool.is_available():
            model_name = f"Google {config.GEMINI_MODEL} (Multi-Key Pool: {self.omni_bridge.gemini_pool.get_key_count()} Keys)"
        elif self.hf_bridge.is_connected():
            model_name = f"HuggingFace {config.HF_MODEL_BORAMEY}"

        return {
            "success": True,
            "query": query,
            "model_used": model_name,
            "evidence": evidence_packet,
            "relevant_knowledge": relevant_docs,
            "synthesis": ai_response
        }
