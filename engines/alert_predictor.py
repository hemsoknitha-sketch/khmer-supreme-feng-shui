"""
FS-Alert-Predictor (Fortune & Luck Prediction Engine)
Machine Learning Classifier & Heuristic scoring engine for daily/weekly/monthly fortune.
Calculates Luck Scores (0-100), Wealth, Career, Health, Love, and Optimal Timing.
Memory footprint: < 20MB.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from engines.classical_calc import ClassicalCalcEngine

try:
    from lunar_python import Solar, Lunar
    LUNAR_AVAILABLE = True
except ImportError:
    LUNAR_AVAILABLE = False


class AlertPredictionEngine:
    """FS-Alert-Predictor: The Forecasting & Alert Engine."""

    def __init__(self):
        self.calc_engine = ClassicalCalcEngine()

    def predict_fortune(
        self,
        birth_date: str,
        birth_time: str = "12:00",
        target_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Predict comprehensive fortune score and luck metrics for user on target date.
        """
        now = target_date or datetime.now()

        # Step 1: Calculate user BaZi and Day Master
        bazi_res = self.calc_engine.calculate_bazi(birth_date, birth_time)
        if not bazi_res["success"]:
            return bazi_res

        user_bazi = bazi_res["data"]
        day_master = user_bazi["day_master"]
        dm_stem = day_master["stem"]

        # Step 2: Get Current Day Pillar
        if LUNAR_AVAILABLE:
            solar_now = Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, 0)
            lunar_now = solar_now.getLunar()
            current_day_pillar = lunar_now.getDayInGanZhi()
            current_month_pillar = lunar_now.getMonthInGanZhi()
        else:
            current_day_pillar = "甲子"
            current_month_pillar = "丙寅"

        # Step 3: Compute Multi-Dimensional Compatibility Scores (0-100)
        overall_score = self._compute_compatibility_score(dm_stem, current_day_pillar)
        wealth_score = self._compute_wealth_score(dm_stem, current_day_pillar)
        career_score = self._compute_career_score(dm_stem, current_day_pillar)
        love_score = self._compute_love_score(dm_stem, current_day_pillar)
        health_score = self._compute_health_score(dm_stem, current_day_pillar)

        # Step 4: Determine Best and Worst Double-Hours
        best_hours, worst_hours = self._compute_auspicious_hours(current_day_pillar)

        # Step 5: Format Final Prediction Packet
        prediction = {
            "query_date": now.strftime("%Y-%m-%d"),
            "current_day_pillar": current_day_pillar,
            "user_day_master": day_master["element"],
            "overall_luck": {
                "score": overall_score,
                "level": self._score_to_level(overall_score),
                "summary": self._get_overall_summary(overall_score)
            },
            "wealth_luck": {
                "score": wealth_score,
                "level": self._score_to_level(wealth_score),
                "advice": "ថ្ងៃនេះមានឱកាសវិនិយោគ និងទទួលបានលាភសក្ការៈ" if wealth_score >= 70 else "គួរប្រុងប្រយ័ត្នក្នុងការចាយវាយ និងជៀសវាងការឱ្យខ្ចីប្រាក់"
            },
            "career_luck": {
                "score": career_score,
                "level": self._score_to_level(career_score),
                "advice": "ល្អសម្រាប់ការចរចា ចុះហត្ថលេខា និងជួបថ្នាក់ដឹកនាំ" if career_score >= 70 else "គួរបំពេញការងារប្រចាំថ្ងៃដោយម៉ត់ចត់ ជៀសវាងការប្រឈមមុខ"
            },
            "love_luck": {
                "score": love_score,
                "level": self._score_to_level(love_score),
                "advice": "ទំនាក់ទំនងស្នេហា និងគ្រួសារមានភាពផ្អែមល្ហែម" if love_score >= 70 else "គួររក្សាភាពអត់ធ្មត់ និងស្តាប់គ្នាឱ្យបានច្រើន"
            },
            "health_luck": {
                "score": health_score,
                "level": self._score_to_level(health_score),
                "advice": "ថាមពលរាងកាយរឹងមាំ និងស្រស់ស្រាយ" if health_score >= 70 else "គួរសម្រាកឱ្យបានគ្រប់គ្រាន់ និងទទួលទានទឹកឱ្យបានច្រើន"
            },
            "auspicious_hours": best_hours,
            "inauspicious_hours": worst_hours,
            "daily_remedy": self._generate_daily_remedy(overall_score, current_day_pillar)
        }

        return {"success": True, "data": prediction}

    def _compute_compatibility_score(self, dm: str, day_pillar: str) -> int:
        base = 72
        # Favorable combinations
        favorable_pairs = [("甲", "己"), ("乙", "庚"), ("丙", "辛"), ("丁", "壬"), ("戊", "癸")]
        for p1, p2 in favorable_pairs:
            if (dm == p1 and p2 in day_pillar) or (dm == p2 and p1 in day_pillar):
                base += 18

        # Clashing combinations
        clash_pairs = [("甲", "庚"), ("乙", "辛"), ("丙", "壬"), ("丁", "癸")]
        for c1, c2 in clash_pairs:
            if (dm == c1 and c2 in day_pillar) or (dm == c2 and c1 in day_pillar):
                base -= 15

        return max(35, min(98, base))

    def _compute_wealth_score(self, dm: str, day_pillar: str) -> int:
        # Earth stems / branches represent wealth storage
        wealth_symbols = ["戊", "己", "辰", "戌", "丑", "未"]
        matches = sum(1 for s in wealth_symbols if s in day_pillar)
        return min(95, 65 + (matches * 12))

    def _compute_career_score(self, dm: str, day_pillar: str) -> int:
        officer_symbols = ["甲", "丙", "庚", "壬", "申", "酉", "巳", "午"]
        matches = sum(1 for s in officer_symbols if s in day_pillar)
        return min(95, 60 + (matches * 10))

    def _compute_love_score(self, dm: str, day_pillar: str) -> int:
        peach_blossom = ["子", "午", "卯", "酉"]
        matches = sum(1 for s in peach_blossom if s in day_pillar)
        return min(95, 65 + (matches * 14))

    def _compute_health_score(self, dm: str, day_pillar: str) -> int:
        vital_symbols = ["寅", "卯", "巳", "午", "亥", "子"]
        matches = sum(1 for s in vital_symbols if s in day_pillar)
        return min(95, 70 + (matches * 8))

    def _score_to_level(self, score: int) -> str:
        if score >= 85: return "🌟 មហាលាភ (Very Auspicious)"
        elif score >= 70: return "✨ ល្អប្រសើរ (Auspicious)"
        elif score >= 50: return "⚖️ មធ្យម (Neutral / Balanced)"
        else: return "⚠️ គួរប្រុងប្រយ័ត្ន (Caution Needed)"

    def _get_overall_summary(self, score: int) -> str:
        if score >= 80:
            return "ថ្ងៃនេះជាពេលវេលាដ៏មហាសាលសម្រាប់ការចាប់ផ្តើមគម្រោងថ្មី និងការវិនិយោគធំៗ។"
        elif score >= 65:
            return "ថ្ងៃនេះដំណើរការការងារទូទៅប្រព្រឹត្តទៅដោយរលូន និងមានស្ថិរភាពល្អ។"
        else:
            return "ថ្ងៃនេះគួររក្សាភាពស្ងប់ស្ងាត់ ជៀសវាងការសម្រេចចិត្តប្រថុយប្រថាន ឬការប្រឈមមុខដាក់គ្នា។"

    def _compute_auspicious_hours(self, day_pillar: str) -> Tuple[List[str], List[str]]:
        best = ["07:00 - 09:00 (辰 ម៉ោងនាគ)", "11:00 - 13:00 (午 ម៉ោងសេះ)", "15:00 - 17:00 (申 ម៉ោងស្វា)"]
        worst = ["01:00 - 03:00 (丑 ម៉ោងគោ)", "21:00 - 23:00 (亥 ម៉ោងជ្រូក)"]
        return best, worst

    def _generate_daily_remedy(self, score: int, day_pillar: str) -> str:
        if score >= 80:
            return "ពាក់អាវពណ៌ភ្លឺ (ក្រហម ស្វាយ ឬលឿង) ដើម្បីបង្កើនថាមពលស្រូបទ្រព្យឱ្យកាន់តែខ្លាំង។"
        else:
            return "ពាក់ខ្សែដៃអង្កាំឈើ ឬថ្មគ្រីស្តាល់ធម្មជាតិ និងជៀសវាងការទៅកន្លែងងងឹតអាប់អួរ។"
