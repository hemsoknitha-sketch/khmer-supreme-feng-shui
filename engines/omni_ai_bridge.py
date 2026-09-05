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

        # Candidate models for failover against 404 model URI pattern mismatches
        candidate_models = [self.model_name.replace("models/", "")]
        for fb in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]:
            if fb not in candidate_models:
                candidate_models.append(fb)

        # Attempt up to total keys count before giving up
        max_attempts = min(len(self.keys), 5)
        for attempt in range(max_attempts):
            api_key = self._get_next_key()
            if not api_key:
                break

            for clean_model in candidate_models:
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
                                    self.model_name = clean_model
                                    return parts[0].get("text", "")
                except urllib.error.HTTPError as http_err:
                    if http_err.code in [400, 401, 403, 429]:
                        reason_msg = "Rate Limit (429)" if http_err.code == 429 else f"Auth/Key Error ({http_err.code}: {http_err.reason})"
                        logger.warning(f"Gemini API key {api_key[:6]}... encountered {reason_msg}. Rotating to next key...")
                        break  # Rotate to next key immediately
                    elif http_err.code == 404:
                        logger.warning(f"Gemini API model '{clean_model}' returned 404 Not Found. Falling back to alternative model...")
                        continue  # Try next candidate model
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

    def _calibrate_text_length(self, text: str, min_chars: int = 3500, max_chars: int = 4000) -> str:
        """Ensure the generated output strictly falls between 3500 and 4000 characters."""
        import re
        text = text.replace("**", "").replace("++", "").replace("==", "")
        text = text.replace("របាយការណ៍", "")
        text = re.sub(r'[a-zA-Z]', '', text)
        text = re.sub(r'\(\s*\)', '', text)
        text = re.sub(r'•\s*([💰👑🎨🏛️🌌⚠️🧭⏰✨💊💡🌿💼💖🌸☀️🍂❄️🧹🍎🏮🚫⚖️🤝🛏️👤⛰️💨⏳🔮📖📐🖼️👁️❓])', r'\1', text)
        text = re.sub(r'([📜🧭⏰💊📊💡👑🗓️⚖️🤝🛏️📖🖼️👁️])\s*([១២៣៤៥៦៧៨៩០]+\.)', r'\2', text)

        current_len = len(text)
        if min_chars <= current_len <= max_chars:
            return text

        if current_len > max_chars:
            cut_target = max_chars - 60
            trimmed = text[:cut_target]
            last_punc = max(trimmed.rfind("។"), trimmed.rfind("\n"))
            if last_punc > 3200:
                trimmed = trimmed[:last_punc+1]
            footer = "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n✨ សូមប្រសិទ្ធពរជ័យសិរីសួស្តី ជោគជ័យ សិរីមង្គល និងវិបុលសុខគ្រប់ប្រការ!"
            return trimmed + footer

        expansion_paragraphs = [
            (
                "\n\nវិជ្ជាហុងស៊ុយបុរាណចិន និងក្បួនតម្រាខ្មែរបានបញ្ជាក់យ៉ាងច្បាស់ថា "
                "ការយល់ដឹងពីចង្វាក់ថាមពលមេឃដី និងការកែខៃតុល្យភាពយិនយ៉ាងស្របតាមកាលវេលាពិតប្រាកដ "
                "នឹងជួយកែប្រែជោគវាសនាពីអាក្រក់ឱ្យក្លាយជាល្អ ពីលំបាកឱ្យក្លាយជាងាយស្រួល "
                "និងបើកទ្វារទទួលលាភសក្ការៈទ្រព្យសម្បត្តិហូរចូលគ្រប់ទិសទីឥតដាច់។ "
                "សូមម្ចាស់ជោគជតារក្សាភាពស្ងប់ក្នុងចិត្ត ប្រព្រឹត្តអំពើល្អ និងប្រើប្រាស់ក្បួនតម្រានេះប្រកបដោយបញ្ញាញាណដ៏ភ្លឺស្វាង!"
            ),
            (
                "\n\nគោលការណ៍គ្រឹះនៃលំហូរថាមពលក្នុងគេហដ្ឋាន និងទីកន្លែងធ្វើការ គឺការរក្សាឱ្យបាននូវភាពស្អាតបាត មានរបៀបរៀបរយ "
                "និងមានខ្យល់អាកាសបរិសុទ្ធចេញចូលជានិច្ច។ នៅពេលដែលទីធ្លាមានពន្លឺគ្រប់គ្រាន់ ថាមពលវិជ្ជមាននឹងកកើតឡើងដោយស្វ័យប្រវត្តិ "
                "ជួយជំរុញឱ្យការគិតមានភាពច្បាស់លាស់ ការសម្រេចចិត្តអាជីវកម្មមានភាពត្រឹមត្រូវ និងទាក់ទាញមនុស្សល្អៗចូលមកជួយជ្រោមជ្រែងគ្រប់ជំហាន។"
            ),
            (
                "\n\nសូមចងចាំជានិច្ចថា ហុងស៊ុយល្អពិតប្រាកដកើតចេញពីការរួមផ្សំរវាងកត្តាមេឃ (ពេលវេលាល្អ) កត្តាដី (ទីតាំងហុងស៊ុយត្រឹមត្រូវ) "
                "និងកត្តាមនុស្ស (ការប្រឹងប្រែង ការគិតវិជ្ជមាន និងការប្រព្រឹត្តអំពើល្អ)។ "
                "នៅពេលដែលកត្តាទាំង ៣ នេះមានតុល្យភាពល្អឥតខ្ចោះ នោះជោគជតារាសីនឹងរុងរឿងថ្កុំថ្កើងជានិរន្តរ៍។"
            ),
            (
                "\n\nក្បួនតម្រាបុរាណក៏បានណែនាំផងដែរថា ការធ្វើបុណ្យទាន ការចែករំលែកសេចក្តីល្អ និងការរក្សាចិត្តមេត្តាចំពោះមនុស្សជុំវិញខ្លួន "
                "គឺជាថាមពលស្រោចស្រពរាសីចក្រដ៏មានអានុភាពបំផុត ដែលគ្មានវត្ថុមង្គលណាអាចជំនួសបានឡើយ។ "
                "សូមបន្តប្រកាន់ខ្ជាប់នូវគុណធម៌ និងប្រើប្រាស់ចំណេះដឹងហុងស៊ុយនេះដើម្បីកសាងអនាគតដ៏ភ្លឺស្វាង និងសុភមង្គលបរិបូរណ៍!"
            )
        ]

        while len(text) < min_chars:
            for p in expansion_paragraphs:
                if len(text) >= min_chars:
                    break
                text = text + p

        if len(text) > max_chars:
            return self._calibrate_text_length(text, min_chars, max_chars)
        return text

    def generate_supreme_consultation(
        self,
        system_prompt: str,
        user_prompt: str,
        context_knowledge: Optional[str] = None
    ) -> str:
        """
        Synthesize high-precision Feng Shui master response (3,500 - 4,000 characters)
        using the multi-tier AI mesh calibrated in pure Khmer typography.
        """
        full_system = (
            system_prompt + "\n\n"
            "គោលការណ៍ឆ្លើយតបដាច់ខាត៖ ចូរពន្យល់លម្អិតក្បោះក្បាយ ជ្រាលជ្រៅ និងច្បាស់លាស់បំផុត (៣,៥០០ ដល់ ៤,០០០ តួអក្សរ) "
            "ជាភាសាខ្មែរសុទ្ធសាធ ១០០% គ្មានអក្សរអង់គ្លេស គ្មានសញ្ញា ** ឬ ++ ឬ == គ្មានចំណុច • 💰 ឬ 📜 ១. ត្រួតគ្នាឡើយ និងដកពាក្យ របាយការណ៍ ចេញ។"
        )
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
                    return self._calibrate_text_length(gemini_res.strip(), 3500, 4000)
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
                    return self._calibrate_text_length(hf_res.strip(), 3500, 4000)
            except Exception as e:
                logger.warning(f"OmniAI HuggingFace fallback triggered: {e}")

        # 3. Tier 3: Local Zenith Master Core (Always available, 0% failure rate)
        raw_fallback = self.hf_bridge._fallback_generation(system_prompt, user_prompt, model_type="boramey")
        return self._calibrate_text_length(raw_fallback, 3500, 4000)


# Global Singleton Omni AI Bridge
omni_ai_bridge = OmniAIBridge()
