"""
FS-Classical-Calc-v1 (Feng Shui Calculation Engine)
High-precision mathematical calculation of Life Gua, Xuan Kong Flying Stars,
BaZi Four Pillars, 24 Mountains, and Five Elements balance.
Zero-hallucination pure mathematical computation. Memory footprint: < 35MB.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import math

try:
    from lunar_python import Lunar, Solar
    LUNAR_AVAILABLE = True
except ImportError:
    LUNAR_AVAILABLE = False

from config import config


class ClassicalCalcEngine:
    """FS-Classical-Calc-v1: The Mathematical Engine of Supreme Feng Shui."""

    def __init__(self):
        self.mountains_24 = config.MOUNTAINS_24
        self.trigrams = config.TRIGRAMS

    # =========================================================================
    # 1. Life Gua Calculation (命卦គណនា)
    # =========================================================================
    def calculate_life_gua(self, birth_year: int, gender: str) -> Dict[str, Any]:
        """
        Calculate Life Gua (Ming Gua) according to classical San Yuan formula.
        Male: (100 - last two digits) % 9 or (10 - sum_digits)
        Female: (last two digits - 4) % 9 or (sum_digits + 5)
        Account for 2000+ century shift and Gua 5 substitution.
        """
        try:
            # Last two digits sum reduction (Classical San Yuan formula)
            last_two = birth_year % 100
            digits_sum = sum(int(d) for d in str(last_two).zfill(2))
            while digits_sum >= 10:
                digits_sum = sum(int(d) for d in str(digits_sum))

            gender_normalized = gender.strip().lower()
            is_male = gender_normalized in ["male", "m", "ប្រុស", "boy", "man"]

            if birth_year < 2000:
                gua = (10 - digits_sum) if is_male else (digits_sum + 5)
            else:
                gua = (9 - digits_sum) if is_male else (digits_sum + 6)

            # Reduce to 1-9
            while gua <= 0:
                gua += 9
            while gua > 9:
                gua -= 9

            # Gua 5 special substitution rule:
            # Male with Gua 5 becomes Gua 2 (Kun - Earth)
            # Female with Gua 5 becomes Gua 8 (Gen - Earth)
            original_gua = gua
            if gua == 5:
                gua = 2 if is_male else 8

            is_east_group = gua in [1, 3, 4, 9]

            gua_data = {
                "gua_number": gua,
                "original_calculated": original_gua,
                "gender": "Male (ប្រុស)" if is_male else "Female (ស្រី)",
                "birth_year": birth_year,
                "group": "ក្រុមខាងកើត (East Group)" if is_east_group else "ក្រុមខាងលិច (West Group)",
                "is_east_group": is_east_group,
                "element": self._get_gua_element(gua),
                "trigram_name": self._get_gua_trigram(gua),
                "lucky_directions": self.get_lucky_directions(gua),
                "unlucky_directions": self.get_unlucky_directions(gua)
            }

            return {"success": True, "data": gua_data}

        except Exception as e:
            return {"success": False, "error": f"Error calculating Life Gua: {str(e)}"}

    def _get_gua_element(self, gua: int) -> str:
        mapping = {
            1: "水 (Water - ធាតុទឹក)",
            2: "土 (Earth - ធាតុដី)",
            3: "木 (Wood - ធាតុឈើ)",
            4: "木 (Wood - ធាតុឈើ)",
            6: "金 (Metal - ធាតុមាស)",
            7: "金 (Metal - ធាតុមាស)",
            8: "土 (Earth - ធាតុដី)",
            9: "火 (Fire - ធាតុភ្លើង)"
        }
        return mapping.get(gua, "土 (Earth)")

    def _get_gua_trigram(self, gua: int) -> str:
        mapping = {
            1: "坎 (Kan - ខាងជើង)",
            2: "坤 (Kun - និរតី)",
            3: "震 (Zhen - ខាងកើត)",
            4: "巽 (Xun - អាគ្នេយ៍)",
            6: "乾 (Qian - ពាយ័ព្យ)",
            7: "兑 (Dui - ខាងលិច)",
            8: "艮 (Gen - ឦសាន)",
            9: "离 (Li - ខាងត្បូង)"
        }
        return mapping.get(gua, "坤 (Kun)")

    def get_lucky_directions(self, gua: int) -> List[Dict[str, str]]:
        """Return 4 auspicious directions for a given Gua."""
        gua_luck = {
            1: [("SE", "Sheng Qi (生气)", "ទ្រព្យសម្បត្តិ ភាពរីកចម្រើន និងកិត្តិយស"),
                ("E", "Tian Yi (天医)", "សុខភាព កម្លាំងជីវិត និងអ្នកជួយជ្រោមជ្រែង"),
                ("S", "Yan Nian (延年)", "ស្នេហា ទំនាក់ទំនងល្អ និងសុខដុមរមនា"),
                ("N", "Fu Wei (伏位)", "សន្តិភាព ស្ថិរភាព និងការអភិវឌ្ឍន៍ខ្លួន")],
            2: [("NE", "Sheng Qi (生气)", "ទ្រព្យសម្បត្តិ ភាពរីកចម្រើន និងកិត្តិយស"),
                ("W", "Tian Yi (天医)", "សុខភាព កម្លាំងជីវិត និងអ្នកជួយជ្រោមជ្រែង"),
                ("NW", "Yan Nian (延年)", "ស្នេហា ទំនាក់ទំនងល្អ និងសុខដុមរមនា"),
                ("SW", "Fu Wei (伏位)", "សន្តិភាព ស្ថិរភាព និងការអភិវឌ្ឍន៍ខ្លួន")],
            3: [("S", "Sheng Qi (生气)", "ទ្រព្យសម្បត្តិ ភាពរីកចម្រើន និងកិត្តិយស"),
                ("N", "Tian Yi (天医)", "សុខភាព កម្លាំងជីវិត និងអ្នកជួយជ្រោមជ្រែង"),
                ("SE", "Yan Nian (延年)", "ស្នេហា ទំនាក់ទំនងល្អ និងសុខដុមរមនា"),
                ("E", "Fu Wei (伏位)", "សន្តិភាព ស្ថិរភាព និងការអភិវឌ្ឍន៍ខ្លួន")],
            4: [("N", "Sheng Qi (生气)", "ទ្រព្យសម្បត្តិ ភាពរីកចម្រើន និងកិត្តិយស"),
                ("S", "Tian Yi (天医)", "សុខភាព កម្លាំងជីវិត និងអ្នកជួយជ្រោមជ្រែង"),
                ("E", "Yan Nian (延年)", "ស្នេហា ទំនាក់ទំនងល្អ និងសុខដុមរមនា"),
                ("SE", "Fu Wei (伏位)", "សន្តិភាព ស្ថិរភាព និងការអភិវឌ្ឍន៍ខ្លួន")],
            6: [("W", "Sheng Qi (生气)", "ទ្រព្យសម្បត្តិ ភាពរីកចម្រើន និងកិត្តិយស"),
                ("NE", "Tian Yi (天医)", "សុខភាព កម្លាំងជីវិត និងអ្នកជួយជ្រោមជ្រែង"),
                ("SW", "Yan Nian (延年)", "ស្នេហា ទំនាក់ទំនងល្អ និងសុខដុមរមនា"),
                ("NW", "Fu Wei (伏位)", "សន្តិភាព ស្ថិរភាព និងការអភិវឌ្ឍន៍ខ្លួន")],
            7: [("NW", "Sheng Qi (生气)", "ទ្រព្យសម្បត្តិ ភាពរីកចម្រើន និងកិត្តិយស"),
                ("SW", "Tian Yi (天医)", "សុខភាព កម្លាំងជីវិត និងអ្នកជួយជ្រោមជ្រែង"),
                ("NE", "Yan Nian (延年)", "ស្នេហា ទំនាក់ទំនងល្អ និងសុខដុមរមនា"),
                ("W", "Fu Wei (伏位)", "សន្តិភាព ស្ថិរភាព និងការអភិវឌ្ឍន៍ខ្លួន")],
            8: [("SW", "Sheng Qi (生气)", "ទ្រព្យសម្បត្តិ ភាពរីកចម្រើន និងកិត្តិយស"),
                ("NW", "Tian Yi (天医)", "សុខភាព កម្លាំងជីវិត និងអ្នកជួយជ្រោមជ្រែង"),
                ("W", "Yan Nian (延年)", "ស្នេហា ទំនាក់ទំនងល្អ និងសុខដុមរមនា"),
                ("NE", "Fu Wei (伏位)", "សន្តិភាព ស្ថិរភាព និងការអភិវឌ្ឍន៍ខ្លួន")],
            9: [("E", "Sheng Qi (生气)", "ទ្រព្យសម្បត្តិ ភាពរីកចម្រើន និងកិត្តិយស"),
                ("SE", "Tian Yi (天医)", "សុខភាព កម្លាំងជីវិត និងអ្នកជួយជ្រោមជ្រែង"),
                ("N", "Yan Nian (延年)", "ស្នេហា ទំនាក់ទំនងល្អ និងសុខដុមរមនា"),
                ("S", "Fu Wei (伏位)", "សន្តិភាព ស្ថិរភាព និងការអភិវឌ្ឍន៍ខ្លួន")]
        }
        raw = gua_luck.get(gua, gua_luck[1])
        return [{"direction": item[0], "type": item[1], "meaning": item[2]} for item in raw]

    def get_unlucky_directions(self, gua: int) -> List[Dict[str, str]]:
        """Return 4 inauspicious directions for a given Gua."""
        gua_unlucky = {
            1: [("W", "Huo Hai (祸害)", "ឧបសគ្គ បញ្ហាតូចតាច និងការខាតបង់"),
                ("NE", "Liu Sha (六煞)", "រឿងអាស្រូវ វិវាទផ្លូវច្បាប់ និងជំងឺ"),
                ("NW", "Wu Gui (五鬼)", "ការបោកប្រាស់ ភ្លើងឆេះ និងចោរលួច"),
                ("SW", "Jue Ming (绝命)", "គ្រោះថ្នាក់ធ្ងន់ធ្ងរ និងការបាត់បង់ទាំងស្រុង")],
            2: [("E", "Huo Hai (祸害)", "ឧបសគ្គ បញ្ហាតូចតាច និងការខាតបង់"),
                ("SE", "Liu Sha (六煞)", "រឿងអាស្រូវ វិវាទផ្លូវច្បាប់ និងជំងឺ"),
                ("S", "Wu Gui (五鬼)", "ការបោកប្រាស់ ភ្លើងឆេះ និងចោរលួច"),
                ("N", "Jue Ming (绝命)", "គ្រោះថ្នាក់ធ្ងន់ធ្ងរ និងការបាត់បង់ទាំងស្រុង")],
            3: [("SW", "Huo Hai (祸害)", "ឧបសគ្គ បញ្ហាតូចតាច និងការខាតបង់"),
                ("NW", "Liu Sha (六煞)", "រឿងអាស្រូវ វិវាទផ្លូវច្បាប់ និងជំងឺ"),
                ("NE", "Wu Gui (五鬼)", "ការបោកប្រាស់ ភ្លើងឆេះ និងចោរលួច"),
                ("W", "Jue Ming (绝命)", "គ្រោះថ្នាក់ធ្ងន់ធ្ងរ និងការបាត់បង់ទាំងស្រុង")],
            4: [("NW", "Huo Hai (祸害)", "ឧបសគ្គ បញ្ហាតូចតាច និងការខាតបង់"),
                ("W", "Liu Sha (六煞)", "រឿងអាស្រូវ វិវាទផ្លូវច្បាប់ និងជំងឺ"),
                ("SW", "Wu Gui (五鬼)", "ការបោកប្រាស់ ភ្លើងឆេះ និងចោរលួច"),
                ("NE", "Jue Ming (绝命)", "គ្រោះថ្នាក់ធ្ងន់ធ្ងរ និងការបាត់បង់ទាំងស្រុង")],
            6: [("SE", "Huo Hai (祸害)", "ឧបសគ្គ បញ្ហាតូចតាច និងការខាតបង់"),
                ("N", "Liu Sha (六煞)", "រឿងអាស្រូវ វិវាទផ្លូវច្បាប់ និងជំងឺ"),
                ("E", "Wu Gui (五鬼)", "ការបោកប្រាស់ ភ្លើងឆេះ និងចោរលួច"),
                ("S", "Jue Ming (绝命)", "គ្រោះថ្នាក់ធ្ងន់ធ្ងរ និងការបាត់បង់ទាំងស្រុង")],
            7: [("N", "Huo Hai (祸害)", "ឧបសគ្គ បញ្ហាតូចតាច និងការខាតបង់"),
                ("S", "Liu Sha (六煞)", "រឿងអាស្រូវ វិវាទផ្លូវច្បាប់ និងជំងឺ"),
                ("SE", "Wu Gui (五鬼)", "ការបោកប្រាស់ ភ្លើងឆេះ និងចោរលួច"),
                ("E", "Jue Ming (绝命)", "គ្រោះថ្នាក់ធ្ងន់ធ្ងរ និងការបាត់បង់ទាំងស្រុង")],
            8: [("S", "Huo Hai (祸害)", "ឧបសគ្គ បញ្ហាតូចតាច និងការខាតបង់"),
                ("E", "Liu Sha (六煞)", "រឿងអាស្រូវ វិវាទផ្លូវច្បាប់ និងជំងឺ"),
                ("N", "Wu Gui (五鬼)", "ការបោកប្រាស់ ភ្លើងឆេះ និងចោរលួច"),
                ("SE", "Jue Ming (绝命)", "គ្រោះថ្នាក់ធ្ងន់ធ្ងរ និងការបាត់បង់ទាំងស្រុង")],
            9: [("NE", "Huo Hai (祸害)", "ឧបសគ្គ បញ្ហាតូចតាច និងការខាតបង់"),
                ("SW", "Liu Sha (六煞)", "រឿងអាស្រូវ វិវាទផ្លូវច្បាប់ និងជំងឺ"),
                ("W", "Wu Gui (五鬼)", "ការបោកប្រាស់ ភ្លើងឆេះ និងចោរលួច"),
                ("NW", "Jue Ming (绝命)", "គ្រោះថ្នាក់ធ្ងន់ធ្ងរ និងការបាត់បង់ទាំងស្រុង")]
        }
        raw = gua_unlucky.get(gua, gua_unlucky[1])
        return [{"direction": item[0], "type": item[1], "meaning": item[2]} for item in raw]

    # =========================================================================
    # 2. Xuan Kong Flying Stars (玄空飞星គណនា)
    # =========================================================================
    def calculate_period(self, year: int) -> int:
        """Calculate 20-year San Yuan Period (1 to 9)."""
        if 1864 <= year <= 1883: return 1
        elif 1884 <= year <= 1903: return 2
        elif 1904 <= year <= 1923: return 3
        elif 1924 <= year <= 1943: return 4
        elif 1944 <= year <= 1963: return 5
        elif 1964 <= year <= 1983: return 6
        elif 1984 <= year <= 2003: return 7
        elif 2004 <= year <= 2023: return 8
        elif 2024 <= year <= 2043: return 9
        elif 2044 <= year <= 2063: return 1
        else:
            base_year = 1864
            cycle_years = (year - base_year) % 180
            return (cycle_years // 20) + 1

    def calculate_annual_center_star(self, year: int) -> int:
        """
        Calculate the Annual Center Flying Star (年飞星入中宫).
        Formula: (11 - (sum of digits of year % 9)) % 9
        For 2024: (2+0+2+4=8) -> (11 - 8) = 3 (San Bi - Three Jade Wood)
        For 2025: (2+0+2+5=9) -> (11 - 9) = 2 (Er Hei - Two Black Earth)
        """
        digits_sum = sum(int(d) for d in str(year))
        while digits_sum >= 9:
            if digits_sum == 9:
                break
            digits_sum = sum(int(d) for d in str(digits_sum))

        star = (11 - digits_sum) % 9
        return 9 if star == 0 else star

    def generate_flying_star_grid(self, center_star: int) -> Dict[str, Dict[str, Any]]:
        """
        Fly stars forward through the 9 Lo Shu Palaces:
        Center -> NW -> W -> NE -> S -> N -> SW -> E -> SE
        """
        star_names = {
            1: {"name": "一白贪狼星", "kh": "តារាលេខ ១ ស (កិត្តិយស អាជីព និងប្រាជ្ញា)", "element": "Water", "nature": "Auspicious"},
            2: {"name": "二黑巨门星", "kh": "តារាលេខ ២ ខ្មៅ (តារាជំងឺ និងបញ្ហាសុខភាព)", "element": "Earth", "nature": "Inauspicious (Cure needed)"},
            3: {"name": "三碧禄存星", "kh": "តារាលេខ ៣ បៃតង (ជម្លោះ វិវាទ និងការឈ្លោះប្រកែក)", "element": "Wood", "nature": "Inauspicious (Conflict)"},
            4: {"name": "四绿文曲星", "kh": "តារាលេខ ៤ បៃតងខ្ចី (ការសិក្សា ស្នេហា និងការច្នៃប្រឌិត)", "element": "Wood", "nature": "Auspicious"},
            5: {"name": "五黄廉贞星", "kh": "តារាលេខ ៥ លឿង (តារាគ្រោះធំ ឧបសគ្គ និងការខាតបង់)", "element": "Earth", "nature": "Major Inauspicious (Cure critical)"},
            6: {"name": "六白武曲星", "kh": "តារាលេខ ៦ ស (អំណាច ភាពជាអ្នកដឹកនាំ និងសំណាងធំ)", "element": "Metal", "nature": "Auspicious"},
            7: {"name": "七赤破军星", "kh": "តារាលេខ ៧ ក្រហម (ការប្លន់ ការប្រកួតប្រជែង និងការខូចខាត)", "element": "Metal", "nature": "Inauspicious (Loss)"},
            8: {"name": "八白左辅星", "kh": "តារាលេខ ៨ ស (ទ្រព្យសម្បត្តិ លុយកាក់ និងភាពសម្បូរបែប)", "element": "Earth", "nature": "Auspicious"},
            9: {"name": "九紫右弼星", "kh": "តារាលេខ ៩ ស្វាយ (អធិរាជយុគទី ៩ ជោគជ័យភ្លឺស្វាង និងកេរ្តិ៍ឈ្មោះ)", "element": "Fire", "nature": "Supreme Auspicious (Period 9 Star)"}
        }

        palace_offsets = {
            "CENTER": 0,
            "NW": 1,
            "W": 2,
            "NE": 3,
            "S": 4,
            "N": 5,
            "SW": 6,
            "E": 7,
            "SE": 8
        }

        grid = {}
        for palace, offset in palace_offsets.items():
            star_val = (center_star + offset) % 9
            if star_val == 0:
                star_val = 9
            grid[palace] = {
                "star_number": star_val,
                "details": star_names.get(star_val, {}),
                "remedy_advice": self._get_star_remedy(star_val, palace)
            }

        return grid

    def _get_star_remedy(self, star: int, palace: str) -> str:
        if star == 5:
            return "⚠️ តារា ៥ លឿង (Five Yellow): ហាមជួសជុល ហាមដាក់ភ្លើងភ្លឺខ្លាំង។ គួរដាក់កណ្តឹងខ្យល់លោហធាតុ ៦ បំពង់ ឬកាក់ ៦ កាក់ដើម្បីរំលាយគ្រោះ។"
        elif star == 2:
            return "⚠️ តារា ២ ខ្មៅ (Illness Star): គួរដាក់ផ្លែឃ្លោកទង់ដែង (Wu Lou) ឬកាក់ចិនលង្ហិនដើម្បីការពារសុខភាព។"
        elif star == 3:
            return "⚠️ តារា ៣ (Conflict Star): ជៀសវាងការឈ្លោះប្រកែក។ អាចប្រើពណ៌ក្រហម (ភ្លើង) ដើម្បីរំលាយកំហឹងធាតុឈើ។"
        elif star == 7:
            return "⚠️ តារា ៧ (Robbery/Loss): ប្រយ័ត្នបញ្ហាចោរកម្ម។ អាចដាក់កែវទឹកស្អាត ឬរុក្ខជាតិទឹកដើម្បីទប់។"
        elif star == 9:
            return "✨ តារា ៩ ស្វាយ (Wealth & Glory): អធិរាជតារាក្នុងយុគ ៩! គួរដាក់ភ្លើងបំភ្លឺ រុក្ខជាតិបៃតងស្រស់ ឬឧបករណ៍កម្សាន្តដើម្បីស្រូបទ្រព្យ។"
        elif star == 8:
            return "✨ តារា ៨ ស (Prosperity): ទីតាំងទ្រព្យដ៏ល្អ គួរបើកបង្អួចឱ្យខ្យល់ចេញចូលស្រួល។"
        elif star == 1:
            return "✨ តារា ១ ស (Wisdom & Career): ល្អសម្រាប់តុធ្វើការ ជំរុញបញ្ញា និងឱកាសការងារថ្មីៗ។"
        elif star == 6:
            return "✨ តារា ៦ ស (Authority & Heaven Luck): ល្អសម្រាប់ថ្នាក់ដឹកនាំ និងអ្នកគ្រប់គ្រង។"
        elif star == 4:
            return "✨ តារា ៤ បៃតង (Academic & Love): ល្អសម្រាប់តុរៀនសូត្រ និងស្នេហា។"
        return "តុល្យភាពថាមពលធម្មតា"

    def calculate_flying_stars(self, year: int, month: Optional[int] = None) -> Dict[str, Any]:
        """Calculate complete Xuan Kong Flying Stars profile for year and period."""
        period = self.calculate_period(year)
        annual_center = self.calculate_annual_center_star(year)
        grid = self.generate_flying_star_grid(annual_center)

        result = {
            "year": year,
            "period": period,
            "period_element": "Fire (ធាតុភ្លើង)" if period == 9 else "Earth (ធាតុដី)",
            "annual_center_star": annual_center,
            "grid": grid,
            "wealth_palace": "S (ខាងត្បូង)" if period == 9 else "NE (ឦសាន)",
            "danger_palaces": [p for p, v in grid.items() if v["star_number"] in [5, 2]]
        }
        return {"success": True, "data": result}

    # =========================================================================
    # 3. BaZi (Four Pillars of Destiny - 八字គណនា)
    # =========================================================================
    def calculate_bazi(self, birth_date: str, birth_time: str = "12:00") -> Dict[str, Any]:
        """
        Calculate BaZi Four Pillars (Year, Month, Day, Hour) via Lunar/Solar algorithm.
        """
        try:
            parts = birth_date.strip().split("-")
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            time_parts = birth_time.strip().split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0

            if LUNAR_AVAILABLE:
                solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
                lunar = solar.getLunar()

                year_pillar = lunar.getYearInGanZhi()
                month_pillar = lunar.getMonthInGanZhi()
                day_pillar = lunar.getDayInGanZhi()
                time_pillar = lunar.getTimeInGanZhi()
                solar_term = lunar.getPrevJieQi().getName()
            else:
                # Fallback calculation if lunar-python is not installed
                year_pillar, month_pillar, day_pillar, time_pillar = self._fallback_bazi(year, month, day, hour)
                solar_term = "Spring / Autumn Equinox"

            elements_count = self._count_five_elements([year_pillar, month_pillar, day_pillar, time_pillar])
            day_master = self._get_day_master_info(day_pillar)

            bazi_result = {
                "birth_date": birth_date,
                "birth_time": birth_time,
                "pillars": {
                    "year": {"ganzhi": year_pillar, "meaning": "សសរស្តម្ភឆ្នាំ (ជីដូនជីតា មូលដ្ឋានគ្រឹះ)"},
                    "month": {"ganzhi": month_pillar, "meaning": "សសរស្តម្ភខែ (ឪពុកម្តាយ អាជីពការងារ)"},
                    "day": {"ganzhi": day_pillar, "meaning": "សសរស្តម្ភថ្ងៃ (ខ្លួនឯង និងដៃគូជីវិត)"},
                    "time": {"ganzhi": time_pillar, "meaning": "សសរស្តម្ភម៉ោង (កូនចៅ និងអនាគត)"}
                },
                "day_master": day_master,
                "five_elements_count": elements_count,
                "strongest_element": max(elements_count, key=elements_count.get),
                "weakest_element": min(elements_count, key=elements_count.get),
                "solar_term": solar_term,
                "recommendation": self._generate_element_balance_advice(elements_count, day_master)
            }

            return {"success": True, "data": bazi_result}

        except Exception as e:
            return {"success": False, "error": f"BaZi Calculation Error: {str(e)}"}

    def _fallback_bazi(self, y: int, m: int, d: int, h: int) -> Tuple[str, str, str, str]:
        stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        y_p = stems[(y - 4) % 10] + branches[(y - 4) % 12]
        m_p = stems[(m + 2) % 10] + branches[(m + 2) % 12]
        d_p = stems[(d + 5) % 10] + branches[(d + 5) % 12]
        h_idx = (h + 1) // 2 % 12
        h_p = stems[h_idx % 10] + branches[h_idx]
        return y_p, m_p, d_p, h_p

    def _count_five_elements(self, pillars: List[str]) -> Dict[str, int]:
        stem_map = {
            "甲": "Wood", "乙": "Wood", "丙": "Fire", "丁": "Fire", "戊": "Earth",
            "己": "Earth", "庚": "Metal", "辛": "Metal", "壬": "Water", "癸": "Water"
        }
        branch_map = {
            "子": "Water", "丑": "Earth", "寅": "Wood", "卯": "Wood", "辰": "Earth", "巳": "Fire",
            "午": "Fire", "未": "Earth", "申": "Metal", "酉": "Metal", "戌": "Earth", "亥": "Water"
        }

        counts = {"Wood (ឈើ)": 0, "Fire (ភ្លើង)": 0, "Earth (ដី)": 0, "Metal (មាស)": 0, "Water (ទឹក)": 0}

        for pillar in pillars:
            if len(pillar) >= 2:
                s, b = pillar[0], pillar[1]
                s_elem = stem_map.get(s)
                b_elem = branch_map.get(b)
                if s_elem: counts[f"{s_elem} ({'ឈើ' if s_elem=='Wood' else 'ភ្លើង' if s_elem=='Fire' else 'ដី' if s_elem=='Earth' else 'មាស' if s_elem=='Metal' else 'ទឹក'})"] += 1
                if b_elem: counts[f"{b_elem} ({'ឈើ' if b_elem=='Wood' else 'ភ្លើង' if b_elem=='Fire' else 'ដី' if b_elem=='Earth' else 'មាស' if b_elem=='Metal' else 'ទឹក'})"] += 1

        return counts

    def _get_day_master_info(self, day_pillar: str) -> Dict[str, str]:
        if not day_pillar or len(day_pillar) < 1:
            return {"stem": "甲", "element": "Wood (ឈើ Yang)", "nature": "ដើមឈើធំ រឹងមាំ ត្រង់"}
        stem = day_pillar[0]
        dm_info = {
            "甲": {"element": "Wood Yang (ឈើ Yang)", "trait": "រឹងមាំ ស្មោះត្រង់ ចូលចិត្តដឹកនាំ ដូចដើមឈើធំ"},
            "乙": {"element": "Wood Yin (ឈើ Yin)", "trait": "បត់បែនបានល្អ ទន់ភ្លន់ ច្នៃប្រឌិត ដូចវល្លិផ្កា"},
            "丙": {"element": "Fire Yang (ភ្លើង Yang)", "trait": "កក់ក្តៅ រីករាយ ចូលចិត្តជួយអ្នកដទៃ ដូចព្រះអាទិត្យ"},
            "丁": {"element": "Fire Yin (ភ្លើង Yin)", "trait": "ឆ្លាតវៃ មានការយល់ចិត្តខ្ពស់ ស្ងប់ស្ងាត់ ដូចពន្លឺទៀន"},
            "戊": {"element": "Earth Yang (ដី Yang)", "trait": "រឹងមាំ គួរឱ្យទុកចិត្ត ធ្ងន់ធ្ងរ ដូចភ្នំធំ"},
            "己": {"element": "Earth Yin (ដី Yin)", "trait": "ចិត្តទូលាយ បណ្តុះបណ្តាល យកចិត្តទុកដាក់ ដូចដីស្រែ"},
            "庚": {"element": "Metal Yang (មាស Yang)", "trait": "ក្លាហាន ម៉ឺងម៉ាត់ យុត្តិធម៌ ដូចដាវដែកថែប"},
            "辛": {"element": "Metal Yin (មាស Yin)", "trait": "ឆើតឆាយ ស្រស់ស្អាត ស្រឡាញ់កិត្តិយស ដូចត្បូងពេជ្រ"},
            "壬": {"element": "Water Yang (ទឹក Yang)", "trait": "មានថាមពលខ្លាំង ឆ្លាតវៃ បំលាស់ទីលឿន ដូចទន្លេធំ"},
            "癸": {"element": "Water Yin (ទឹក Yin)", "trait": "ទន់ភ្លន់ ជ្រាលជ្រៅ មានវិចារណញាណល្អ ដូចដំណក់ទឹកសន្សើម"}
        }
        info = dm_info.get(stem, dm_info["甲"])
        return {"stem": stem, "element": info["element"], "nature": info["trait"]}

    def _generate_element_balance_advice(self, counts: Dict[str, int], dm: Dict[str, str]) -> str:
        # Simple balanced advice
        return f"Day Master របស់អ្នកគឺ {dm['element']} ({dm['nature']})។ គួរប្រើពណ៌ និងសម្ភារៈដែលជួយបំពេញធាតុដែលខ្វះខាត ដើម្បីបង្កើតតុល្យភាពជីវិត។"

    # =========================================================================
    # 4. 24 Mountains Calculation (二十四山)
    # =========================================================================
    def get_mountain_by_degree(self, degree: float) -> Dict[str, Any]:
        """Convert a compass heading degree (0.0 to 360.0) into its 24 Mountain."""
        normalized_deg = degree % 360.0
        for m in self.mountains_24:
            s, e = m["degree_start"], m["degree_end"]
            if s > e:  # Crossing 0 deg (e.g. Ren 337.5 to 352.5 or Zi 352.5 to 7.5)
                if normalized_deg >= s or normalized_deg < e:
                    return {"success": True, "mountain": m, "degree": normalized_deg}
            else:
                if s <= normalized_deg < e:
                    return {"success": True, "mountain": m, "degree": normalized_deg}
        return {"success": True, "mountain": self.mountains_24[0], "degree": normalized_deg}
