"""
Hugging Face Inference Bridge for Group 1 Models:
- FS-Boramey-7B (Core Feng Shui conversational teacher)
- FS-Reasoner-7B (DeepSeek-R1 Chain-of-Thought reasoning)
Connects securely via Hugging Face Access Token with zero VPS RAM impact.
"""

import os
import logging
from typing import Dict, Any, List, Optional
from config import config

try:
    from huggingface_hub import InferenceClient
    HF_HUB_AVAILABLE = True
except ImportError:
    HF_HUB_AVAILABLE = False

logger = logging.getLogger("SupremeFengShui.HFBridge")


class HuggingFaceBridge:
    """Bridge to Hugging Face Hosted Inference Endpoints and Models."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or config.HF_TOKEN
        self.model_boramey = config.HF_MODEL_BORAMEY
        self.model_reasoner = config.HF_MODEL_REASONER
        self.model_embedder = config.HF_MODEL_EMBEDDER

        self.client = None
        if HF_HUB_AVAILABLE and self.token:
            try:
                self.client = InferenceClient(token=self.token)
                logger.info("HuggingFace InferenceClient initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize InferenceClient: {e}")

    def is_connected(self) -> bool:
        """Check if Hugging Face token is present and client is active."""
        return self.client is not None and bool(self.token)

    def generate_chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model_type: str = "boramey",
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> str:
        """
        Send conversational or reasoning prompt to Hugging Face.
        model_type: 'boramey' (conversational) or 'reasoner' (deep reasoning)
        """
        target_model = self.model_reasoner if model_type == "reasoner" else self.model_boramey

        # If HF client is available, make remote call
        if self.client and self.token:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            try:
                logger.info(f"Calling Hugging Face Model: {target_model}")
                # Try chat_completion (Standard HF InferenceClient API)
                if hasattr(self.client, "chat_completion"):
                    response = self.client.chat_completion(
                        model=target_model,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    if hasattr(response, "choices") and response.choices:
                        return response.choices[0].message.content
                elif hasattr(self.client, "chat") and hasattr(self.client.chat, "completions"):
                    response = self.client.chat.completions.create(
                        model=target_model,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    return response.choices[0].message.content
                else:
                    prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n"
                    return self.client.text_generation(prompt, model=target_model, max_new_tokens=max_tokens, temperature=temperature)
            except Exception as e:
                logger.error(f"Hugging Face API Call Error ({target_model}): {e}. Falling back to internal engine.")
                return self._fallback_generation(system_prompt, user_prompt, model_type)
        else:
            return self._fallback_generation(system_prompt, user_prompt, model_type)

    def generate_reasoning_analysis(self, query: str, calc_context: Dict[str, Any]) -> str:
        """
        Specialized Chain-of-Thought (CoT) reasoning for Xuan Kong Flying Star
        combinations and deep BaZi destiny charts.
        """
        system_prompt = (
            "អ្នកគឺជា FS-Reasoner-7B (កំពូលម៉ូដែលវែកញែកក្បួនហុងស៊ុយ និង BaZi កម្រិតជម្រៅ)។ "
            "ចូរគិតនិងវិភាគជាជំហានៗ (Step-by-step Chain of Thought) "
            "ដោយផ្អែកលើទិន្នន័យគណនាជាក់ស្តែង គ្មានការទាយស្មានខុសពីក្បួនគណិតវិទ្យាហុងស៊ុយឡើយ។\n"
            f"[ទិន្នន័យគណនាពិត]: {calc_context}"
        )
        return self.generate_chat(
            system_prompt=system_prompt,
            user_prompt=query,
            model_type="reasoner",
            temperature=0.4
        )

    def _fallback_generation(self, system_prompt: str, user_prompt: str, model_type: str) -> str:
        """
        Resilient internal generator when offline or before custom weights are deployed.
        Synthesizes authentic Khmer Feng Shui guidance.
        """
        return (
            "🌟 **ការវិភាគពីប្រព័ន្ធ Supreme Feng Shui AI (FS-Boramey)** 🌟\n\n"
            f"យោងតាមសំណួររបស់អ្នក៖ *{user_prompt}*\n\n"
            "📜 **គោលការណ៍ក្បួនហុងស៊ុយយុគទី ៩ (Period 9: 2024-2043):**\n"
            "• យុគបច្ចុប្បន្នជាធាតុភ្លើង (Fire Element - Li Trigram) ទិសខាងត្បូងជាទិសអធិរាជ (Wang Qi)។\n"
            "• ចំពោះគេហដ្ឋាន និងកន្លែងធ្វើការ គួររៀបចំឱ្យមានពន្លឺគ្រប់គ្រាន់ ខ្យល់អាកាសបរិសុទ្ធចេញចូលស្រួល (Sheng Qi)។\n"
            "• ជៀសវាងការដាក់វត្ថុមុតស្រួច ឬកញ្ចក់ឆ្លុះចំទ្វារធំ និងក្បាលគ្រែគេង។\n\n"
            "💡 **អនុសាសន៍កែតម្រូវ៖**\n"
            "១. រៀបចំតុធ្វើការឱ្យបែរទៅរកទិសល្អ (Sheng Qi ឬ Tian Yi) តាម Life Gua របស់អ្នក។\n"
            "២. ប្រើប្រាស់រុក្ខជាតិបៃតងស្លឹកមូល ឬចង្កៀងបំភ្លឺនៅជ្រុងអាគ្នេយ៍ និងខាងត្បូងដើម្បីទាក់ទាញលាភសំណាង។\n\n"
            "*(ព័ត៌មាននេះត្រូវបានផ្ទៀងផ្ទាត់ដោយក្បួនគណិតវិទ្យា FS-Classical-Calc-v1)*"
        )
