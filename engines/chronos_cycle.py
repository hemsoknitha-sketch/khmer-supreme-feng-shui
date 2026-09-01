"""
FS-Chronos-Cycle (100-Year Historical & Macro-Period Engine)
Time-Series analysis of Earth Ages, San Yuan 20-Year Periods (1 to 9),
and Macro Energetic Trends (1924 - 2043+).
Memory footprint: < 10MB.
"""

import json
from typing import Dict, Any, List, Optional
from config import config


class ChronosCycleEngine:
    """FS-Chronos-Cycle: The Macro-Cosmic Time Series & Earth Age Engine."""

    def __init__(self):
        self.cycles_data = self._load_historical_cycles()

    def _load_historical_cycles(self) -> Dict[str, Any]:
        cycle_file = config.DATA_DIR / "historical_cycles.json"
        if cycle_file.exists():
            try:
                with open(cycle_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"current_period": 9, "cycles": []}

    def analyze_year_macro_cycle(self, year: int) -> Dict[str, Any]:
        """
        Analyze macro Feng Shui period and cosmic element for any year (1864 - 2063+).
        """
        cycles = self.cycles_data.get("cycles", [])
        matched_cycle = None

        for c in cycles:
            parts = c.get("years", "").split("-")
            if len(parts) == 2:
                try:
                    s_yr, e_yr = int(parts[0]), int(parts[1])
                    if s_yr <= year <= e_yr:
                        matched_cycle = c
                        break
                except ValueError:
                    continue

        if not matched_cycle:
            # Mathematical extrapolation
            period = ((year - 1864) // 20) % 9 + 1
            matched_cycle = {
                "period": period,
                "years": f"{year - (year % 20)}-{year - (year % 20) + 19}",
                "element": "Fire" if period == 9 else "Earth" if period in [2, 5, 8] else "Metal" if period in [6, 7] else "Wood" if period in [3, 4] else "Water",
                "name_kh": f"យុគទី {period}",
                "energy_theme": "វដ្តថាមពលធម្មជាតិតាមក្បួន San Yuan"
            }

        return {
            "query_year": year,
            "period": matched_cycle.get("period"),
            "period_title": matched_cycle.get("name_kh"),
            "element": matched_cycle.get("element"),
            "energy_theme": matched_cycle.get("energy_theme"),
            "is_current_period": matched_cycle.get("period") == 9 and (2024 <= year <= 2043),
            "macro_strategy": self._get_macro_strategy(matched_cycle.get("period"))
        }

    def _get_macro_strategy(self, period: int) -> Dict[str, Any]:
        if period == 9:
            return {
                "ruling_star": "九紫右弼星 (Star 9 Purple Fire)",
                "booming_sectors": [
                    "បច្ចេកវិទ្យាបញ្ញាសិប្បនិម្មិត (AI) និង Robotics",
                    "ថាមពលកកើតឡើងវិញ និង Solar Energy",
                    "វិស័យសុខភាពផ្លូវចិត្ត និងវិជ្ជាខាងវិញ្ញាណ",
                    "ឧស្សាហកម្មកែសម្ផស្ស និងម៉ូដច្នៃប្រឌិត"
                ],
                "wealth_strategy": "រៀបចំទីតាំងទឹកនៅទិសខាងជើង (North) និងទីតាំងសកម្មភាព/ពន្លឺនៅទិសខាងត្បូង (South) ដើម្បីទទួលបានលាភសក្ការៈធំបំផុត។"
            }
        elif period == 8:
            return {
                "ruling_star": "八白左辅星 (Star 8 White Earth)",
                "booming_sectors": ["អចលនទ្រព្យ", "សំណង់", "រ៉ែ"],
                "wealth_strategy": "ទិសឦសាន និងទិសនិរតីជាទិសទ្រព្យសំខាន់។"
            }
        else:
            return {
                "ruling_star": f"Star {period}",
                "booming_sectors": ["ពាណិជ្ជកម្មទូទៅ"],
                "wealth_strategy": "ពង្រឹងតុល្យភាពយិនយ៉ាំងតាមធម្មជាតិ។"
            }
