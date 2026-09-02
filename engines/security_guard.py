"""
Supreme Feng Shui AGI System - Comprehensive Security & Protection Engine
Provides:
1. Anti-Spam & Anti-DDoS Rate Limiting (Sliding Window & Cooldown)
2. Prompt Injection & Jailbreak Defense Filter
3. Sensitive Information & Secret Redaction (Zero Leakage)
4. Input Sanitization & Attack Pattern Detection
5. Super Admin Action Audit Logging & Security Headers
"""

import re
import time
import logging
from collections import defaultdict
from typing import Dict, Any, Tuple, Optional, List
from datetime import datetime

logger = logging.getLogger("SupremeFengShui.Security")


class SecurityGuard:
    """Central Security Guard protecting Bot and API from abuse, spam, and attacks."""

    def __init__(self):
        # User Request Tracking for Rate Limiting: {user_id: [timestamps]}
        self._user_requests: Dict[int, List[float]] = defaultdict(list)
        # Blocked Users: {user_id: block_expiry_timestamp}
        self._blocked_users: Dict[int, float] = {}

        # Configurable Limits
        self.MAX_REQUESTS_PER_MINUTE = 20
        self.MAX_REQUESTS_PER_10_SECONDS = 6
        self.BLOCK_DURATION_SECONDS = 300  # 5 minutes temporary cooldown

        # Sensitive Regex Patterns to Redact (Zero Secret Leakage)
        self._secret_patterns = [
            re.compile(r"(?:bot)?[0-9]{8,12}:[a-zA-Z0-9_-]{30,50}", re.IGNORECASE),  # Telegram Token
            re.compile(r"hf_[a-zA-Z0-9]{30,50}", re.IGNORECASE),                    # HuggingFace Token
            re.compile(r"sk-[a-zA-Z0-9_-]{30,80}", re.IGNORECASE),                  # OpenAI Keys
            re.compile(r"sk-ant-[a-zA-Z0-9_-]{30,100}", re.IGNORECASE),             # Anthropic Keys
            re.compile(r"AQ\.[a-zA-Z0-9_-]{30,80}", re.IGNORECASE),                 # Gemini / Vertex Token
            re.compile(r"AIza[0-9A-Za-z-_]{35}", re.IGNORECASE),                    # Google / Gemini API Keys
            re.compile(r"password\s*[:=]\s*['\"][^'\"]+['\"]", re.IGNORECASE),
            re.compile(r"ADMIN_USER_IDS\s*=\s*[0-9,]+", re.IGNORECASE),
        ]

        # Malicious Prompt Injection Patterns
        self._prompt_injection_patterns = [
            re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions", re.IGNORECASE),
            re.compile(r"disregard\s+(all\s+)?(previous|prior)\s+rules", re.IGNORECASE),
            re.compile(r"you\s+are\s+now\s+(DAN|unrestricted|in\s+developer\s+mode)", re.IGNORECASE),
            re.compile(r"reveal\s+(your\s+)?(system\s+prompt|instructions|secret|api\s+key|token)", re.IGNORECASE),
            re.compile(r"print\s+(the\s+)?(environment|env\s+variables|\.env)", re.IGNORECASE),
            re.compile(r"bypass\s+safety\s+filters", re.IGNORECASE),
            re.compile(r"drop\s+table\s+", re.IGNORECASE),
            re.compile(r"select\s+.*\s+from\s+users", re.IGNORECASE),
            re.compile(r"<script.*?>.*?</script>", re.IGNORECASE)
        ]

    def check_rate_limit(self, user_id: int, is_admin: bool = False) -> Tuple[bool, Optional[str]]:
        """
        Check if user exceeds rate limits (Anti-Spam & Anti-DDoS).
        Admins are exempt from strict blocking.
        Returns: (allowed: bool, warning_message: Optional[str])
        """
        if is_admin:
            return True, None

        now = time.time()

        # Check if currently blocked
        if user_id in self._blocked_users:
            remaining_block = int(self._blocked_users[user_id] - now)
            if remaining_block > 0:
                return False, (
                    f"⛔ **ប្រព័ន្ធសុវត្ថិភាពបានទប់ស្កាត់ជាបណ្តោះអាសន្ន (Anti-Spam Protection)**\n\n"
                    f"ដោយសារអ្នកបានផ្ញើសារលឿនពេក ប្រព័ន្ធបានដាក់កម្រិតសម្រាកចំនួន `{remaining_block}` វិនាទី។\n"
                    f"👉 សូមរង់ចាំបន្តិចមុននឹងសាកល្បងម្តងទៀត។"
                )
            else:
                del self._blocked_users[user_id]

        # Clean old timestamps (> 60s)
        self._user_requests[user_id] = [t for t in self._user_requests[user_id] if now - t < 60]
        timestamps = self._user_requests[user_id]

        # Check 10-second burst limit
        recent_10s = [t for t in timestamps if now - t < 10]
        if len(recent_10s) >= self.MAX_REQUESTS_PER_10_SECONDS:
            self._blocked_users[user_id] = now + self.BLOCK_DURATION_SECONDS
            logger.warning(f"Security Alert: User {user_id} triggered 10s burst rate limit. Blocked for 5m.")
            return False, (
                "⚠️ **ការព្រមានសុវត្ថិភាព៖** អ្នកកំពុងផ្ញើសារញឹកញាប់ពេក (Spam Detection)!\n"
                "ប្រព័ន្ធបានផ្អាកការឆ្លើយតបរយៈពេល ៥ នាទីដើម្បីការពារស្ថិរភាពម៉ាស៊ីនបម្រើ។"
            )

        # Check 1-minute limit
        if len(timestamps) >= self.MAX_REQUESTS_PER_MINUTE:
            self._blocked_users[user_id] = now + self.BLOCK_DURATION_SECONDS
            logger.warning(f"Security Alert: User {user_id} triggered 1m rate limit. Blocked for 5m.")
            return False, (
                "⚠️ **ការព្រមានសុវត្ថិភាព៖** អ្នកបានសួរលើសពី ២០ ដងក្នុង ១ នាទី!\n"
                "ប្រព័ន្ធបានផ្អាកការឆ្លើយតបរយៈពេល ៥ នាទី។"
            )

        # Record this valid request
        self._user_requests[user_id].append(now)
        return True, None

    def sanitize_user_input(self, text: str) -> Tuple[str, bool, Optional[str]]:
        """
        Sanitize user query and detect prompt injection or attack attempts.
        Returns: (sanitized_text: str, is_safe: bool, threat_reason: Optional[str])
        """
        if not text:
            return "", True, None

        cleaned = text.strip()

        # Check prompt injection patterns
        for pattern in self._prompt_injection_patterns:
            if pattern.search(cleaned):
                logger.warning(f"Security Guard: Detected prompt injection/attack attempt: '{cleaned[:50]}...'")
                return cleaned, False, "សាររបស់អ្នកត្រូវបានត្រួតពិនិត្យឃើញថាមានទម្រង់បំពានប្រព័ន្ធសុវត្ថិភាព (Security Violation)។"

        # Prevent excessively long payload attacks (> 2000 chars)
        if len(cleaned) > 2000:
            cleaned = cleaned[:2000]

        return cleaned, True, None

    def redact_secrets(self, text: str) -> str:
        """
        Redact any sensitive API keys, tokens, or environment passwords before outputting.
        Ensures zero secret leakage.
        """
        if not text or not isinstance(text, str):
            return text

        redacted = text
        for pattern in self._secret_patterns:
            redacted = pattern.sub("[REDACTED_SECRET_KEY]", redacted)

        return redacted

    def validate_admin_access(self, user_id: int, admin_ids: List[int]) -> bool:
        """Strictly validate whether a user ID has Super Admin authority."""
        if not user_id or not isinstance(user_id, int):
            return False
        return user_id in admin_ids


# Global Singleton Security Guard
security_guard = SecurityGuard()
