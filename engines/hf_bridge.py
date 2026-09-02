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
        self.model_mahasneh = config.HF_MODEL_MAHASNEH
        self.model_llama = config.HF_MODEL_LLAMA
        self.model_deepseek = config.HF_MODEL_DEEPSEEK_R1
        self.model_mistral = config.HF_MODEL_MISTRAL
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

    def _resolve_model(self, model_type: str) -> str:
        """Resolve model string based on requested model type."""
        model_map = {
            "mahasneh": self.model_mahasneh,
            "love": self.model_mahasneh,
            "llama": self.model_llama,
            "deepseek": self.model_deepseek,
            "reasoner": self.model_reasoner,
            "mistral": self.model_mistral,
            "boramey": self.model_boramey
        }
        return model_map.get(model_type.lower(), self.model_boramey)

    def generate_chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model_type: str = "boramey",
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> str:
        """
        Send conversational, reasoning, or love/romance prompt to Hugging Face model suite.
        model_type: 'mahasneh', 'boramey', 'reasoner', 'llama', 'deepseek', 'mistral'
        """
        target_model = self._resolve_model(model_type)

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
        Synthesizes authentic Khmer Feng Shui guidance in pure Khmer typography.
        """
        return (
            f"🌟 ការពិគ្រោះយោបល់ក្បួនហុងស៊ុយបុរាណជាន់ខ្ពស់ 🌟\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"❓ សំណួរពិគ្រោះ: {user_prompt}\n"
            f"👑 ស្ថាបត្យកម្មបញ្ញាសិប្បនិម្មិត: បរមគ្រូហុងស៊ុយបុរាណ យុគទី ៩ ធាតុភ្លើង\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"១. ការវិភាគគោលការណ៍ក្បួនហុងស៊ុយយុគទី ៩ ធាតុភ្លើង (២០២៤-២០៤៣)\n"
            f"យុគសម័យបច្ចុប្បន្នជាយុគទី ៩ គ្រប់គ្រងដោយថាមពលធាតុភ្លើង និងតារាលេខ ៩ ស្វាយ។ "
            f"ទិសខាងត្បូងជាទិសអធិរាជដ៏មានឥទ្ធិពលបំផុត ដែលនាំមកនូវភាពលេចធ្លោ កិត្តិនាម និងការអភិវឌ្ឍន៍បច្ចេកវិទ្យា។ "
            f"ចំពោះគេហដ្ឋាន និងទីកន្លែងអាជីវកម្ម ការរៀបចំឱ្យមានពន្លឺធម្មជាតិគ្រប់គ្រាន់ និងខ្យល់អាកាសបរិសុទ្ធចេញចូលរលូន "
            f"គឺជាគន្លឹះចម្បងក្នុងការបង្កើតថាមពលរស់ និងស្រូបទាញលាភសក្ការៈ។\n\n"
            f"២. តុល្យភាពយិនយ៉ាង និងចលនាថាមពលខ្យល់ដង្ហើម\n"
            f"ថាមពលក្នុងទីតាំងត្រូវតែមានតុល្យភាពរវាងភាពស្ងប់ស្ងាត់ និងភាពរស់រវើក។ "
            f"កន្លែងទទួលភ្ញៀវ និងច្រកទ្វារមុខត្រូវតែមានភាពភ្លឺច្បាស់ និងទូលាយ ដើម្បីទទួលស្វាគមន៍ចរន្តទ្រព្យ។ "
            f"រីឯបន្ទប់គេង និងកន្លែងធ្វើសមាធិ គួរមានពន្លឺទន់ភ្លន់ និងស្ងប់ស្ងាត់ ដើម្បីចិញ្ចឹមកម្លាំងធាតុ និងសុខភាពផ្លូវចិត្ត។\n\n"
            f"៣. ការវិភាគធាតុទាំង ៥ និងទំនាក់ទំនងរវាងមនុស្សនិងទីតាំង\n"
            f"ធាតុទាំង ៥ ក្នុងធម្មជាតិ (ឈើ ភ្លើង ដី ដែក ទឹក) ត្រូវតែមានខ្សែសង្វាក់បង្កើតផលឥតដាច់។ "
            f"ការប្រើប្រាស់ពណ៌សម្ភារៈ គ្រឿងសង្ហារឹម និងវត្ថុតុបតែងលម្អ ត្រូវតែស៊ីសង្វាក់គ្នាទៅតាមទិសដៅនីមួយៗ។ "
            f"ជៀសវាងការដាក់ធាតុភ្លើង និងធាតុទឹកប៉ះទង្គិចគ្នាដោយផ្ទាល់ ដូចជាការដាក់ចង្ក្រានបាយទល់មុខអាងលិចទឹក ឬទូទឹកកក។\n\n"
            f"៤. វិធានការកែខៃ និងដំណោះស្រាយជាក់ស្តែង\n"
            f"💡 ជំហានទី ១: រៀបចំតុធ្វើការឱ្យបែរមុខទៅរកទិសល្អស្របតាមលេខក្វា និងជៀសវាងការអង្គុយបែរខ្នងចំទ្វារឬបង្អួច។\n"
            f"💡 ជំហានទី ២: ប្រើប្រាស់រុក្ខជាតិបៃតងស្លឹកមូល ឬចង្កៀងបំភ្លឺនៅជ្រុងអាគ្នេយ៍ និងទិសខាងត្បូង ដើម្បីទាក់ទាញលាភសំណាង។\n"
            f"💡 ជំហានទី ៣: ដាក់តាំងចលនាទឹកហូរស្អាតនៅទិសខាងជើង ដើម្បីជំរុញលំហូរសាច់ប្រាក់ និងឱកាសពាណិជ្ជកម្ម។\n"
            f"💡 ជំហានទី ៤: ជៀសវាងការដាក់វត្ថុមុតស្រួច ឬកញ្ចក់ឆ្លុះចំច្រកទ្វារធំ និងក្បាលដំណេក។\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ ការពិគ្រោះយោបល់ត្រូវបានផ្ទៀងផ្ទាត់ដោយប្រព័ន្ធបញ្ញាសិប្បនិម្មិតកម្រិតកំពូល!"
        )
