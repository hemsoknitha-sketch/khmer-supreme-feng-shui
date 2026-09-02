"""
Supreme Feng Shui AGI System - Omni AI Bridge & Multi-Key Intelligence Mesh
Integrates:
1. Google Gemini Multi-Key Pool & Load Balancer (Round-Robin with 429 Failover)
2. Hugging Face Inference Cloud (FS-Boramey-7B & DeepSeek-R1-Distill-Qwen-7B)
3. Zenith 7-Pillars Matrix & 1,000 Lessons Grounding
Provides ultra-resilient, lightning-fast 24/7/365 AI intelligence with 0% downtime.
"""

import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from config import config
from engines.hf_bridge import HuggingFaceBridge

logger = logging.getLogger("SupremeFengShui.OmniAI")


class GeminiMultiKeyPool:
    """
    High-Concurrency Load Balancer for Google Gemini API.
    Supports single or multiple keys (e.g., 82 keys pool).
    Automatically distributes requests and fails over if a key encounters 429 rate limit.
    """

    def __init__(self, key_pool: Optional[List[str]] = None, model_name: Optional[str] = None):
        self.keys = key_pool or config.GEMINI_KEY_POOL
        self.model_name = model_name or config.GEMINI_MODEL
        self._current_index = 0
        self._failed_keys: Dict[str, float] = {}  # {key: timestamp_of_429}

    def is_available(self) -> bool:
        """Check if at least one Gemini API key is configured."""
        return len(self.keys) > 0

    def get_key_count(self) -> int:
        """Return total number of keys in the pool."""
        return len(self.keys)

    def _get_next_key(self) -> Optional[str]:
        """Get the next active key via Round-Robin rotation."""
        if not self.keys:
            return None
        key = self.keys[self._current_index % len(self.keys)]
        self._current_index += 1
        return key

    def generate_content(
        self,
        system_instruction: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = 1500
    ) -> Optional[str]:
        """
        Send prompt to Google Gemini API with automatic key rotation and failover.
        """
        if not self.is_available():
            return None

        # Attempt up to total keys count before giving up
        max_attempts = min(len(self.keys), 5)
        for attempt in range(max_attempts):
            api_key = self._get_next_key()
            if not api_key:
                break

            clean_model = self.model_name.replace("models/", "")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent?key={api_key}"

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": f"[SYSTEM INSTRUCTION]\n{system_instruction}\n\n[USER QUERY]\n{user_prompt}"}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_output_tokens,
                    "topP": 0.95
                }
            }

            headers = {
                "Content-Type": "application/json"
            }

            try:
                data_bytes = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")

                with urllib.request.urlopen(req, timeout=12) as response:
                    if response.status == 200:
                        res_json = json.loads(response.read().decode("utf-8"))
                        candidates = res_json.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts:
                                return parts[0].get("text", "")
            except urllib.error.HTTPError as http_err:
                if http_err.code == 429:
                    logger.warning(f"Gemini API key {api_key[:6]}... hit Rate Limit (429). Rotating to next key...")
                    continue
                else:
                    logger.warning(f"Gemini API HTTP Error ({http_err.code}): {http_err.reason}")
                    continue
            except Exception as e:
                logger.warning(f"Gemini API Call error: {e}")
                continue

        return None


class OmniAIBridge:
    """
    Master Intelligence Orchestrator combining:
    1. Google Gemini Multi-Key Pool (Tier 1 - Ultra Smart & Fast)
    2. Hugging Face Inference Cloud (Tier 2 - Specialized Domain Models)
    3. Zenith Master Core (Tier 3 - Bulletproof Offline Engine)
    """

    def __init__(self):
        self.gemini_pool = GeminiMultiKeyPool()
        self.hf_bridge = HuggingFaceBridge()

    def is_connected(self) -> bool:
        """Check if any cloud AI service is connected."""
        return self.gemini_pool.is_available() or self.hf_bridge.is_connected()

    def get_status_info(self) -> Dict[str, Any]:
        """Return status of all AI models and API pools."""
        return {
            "gemini_active": self.gemini_pool.is_available(),
            "gemini_keys_count": self.gemini_pool.get_key_count(),
            "gemini_model": config.GEMINI_MODEL,
            "hf_connected": self.hf_bridge.is_connected(),
            "hf_boramey": config.HF_MODEL_BORAMEY,
            "hf_reasoner": config.HF_MODEL_REASONER,
            "pillars_matrix": ["Vision", "Qi", "Time", "Physiognomy", "Geo", "Astro", "Bazi"]
        }

    def generate_supreme_consultation(
        self,
        system_prompt: str,
        user_prompt: str,
        context_knowledge: Optional[str] = None
    ) -> str:
        """
        Synthesize high-precision Feng Shui master response using the multi-tier AI mesh.
        """
        full_system = system_prompt
        if context_knowledge:
            full_system += f"\n\n[AUTHENTIC CLASSICAL KNOWLEDGE CONTEXT]\n{context_knowledge}"

        # 1. Tier 1: Try Google Gemini Multi-Key Pool
        if self.gemini_pool.is_available():
            try:
                gemini_res = self.gemini_pool.generate_content(
                    system_instruction=full_system,
                    user_prompt=user_prompt
                )
                if gemini_res and len(gemini_res.strip()) > 30:
                    logger.info("OmniAI: Response successfully generated by Google Gemini Multi-Key Mesh.")
                    return gemini_res.strip()
            except Exception as e:
                logger.warning(f"OmniAI Gemini fallback triggered: {e}")

        # 2. Tier 2: Try Hugging Face Cloud Inference
        if self.hf_bridge.is_connected():
            try:
                hf_res = self.hf_bridge.generate_chat(
                    system_prompt=full_system,
                    user_prompt=user_prompt,
                    model_type="boramey"
                )
                if hf_res and len(hf_res.strip()) > 30:
                    logger.info("OmniAI: Response successfully generated by Hugging Face Cloud.")
                    return hf_res.strip()
            except Exception as e:
                logger.warning(f"OmniAI HuggingFace fallback triggered: {e}")

        # 3. Tier 3: Local Zenith Master Core (Always available, 0% failure rate)
        return self.hf_bridge._fallback_generation(system_prompt, user_prompt, model_type="boramey")


# Global Singleton Omni AI Bridge
omni_ai_bridge = OmniAIBridge()
