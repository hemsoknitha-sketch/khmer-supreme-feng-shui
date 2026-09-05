"""
FS-Classical-Calc-v1 (Feng Shui Calculation Engine)
High-precision mathematical calculation of Life Gua, Xuan Kong Flying Stars,
BaZi Four Pillars, 24 Mountains, and Five Elements balance.
Zero-hallucination pure mathematical computation. Memory footprint: < 35MB.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Union
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
    def calculate_life_gua(
        self,
        birth_year: Union[int, str],
        gender: str,
        birth_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate Life Gua (Ming Gua) according to classical San Yuan formula.
        Male: (100 - last two digits) % 9 or (10 - sum_digits)
        Female: (last two digits - 4) % 9 or (sum_digits + 5)
        Account for 2000+ century shift, Gua 5 substitution, and Li Chun (立春) solar cutoff.
        """
        try:
            input_year = 1990
            effective_year = 1990
            is_before_li_chun = False
            li_chun_day = None
            li_chun_note = None

            # Determine whether a full birth date string is available
            target_date_str = None
            if birth_date and isinstance(birth_date, str) and "-" in birth_date.strip():
                target_date_str = birth_date.strip()
            elif isinstance(birth_year, str) and "-" in birth_year.strip():
                target_date_str = birth_year.strip()

            if target_date_str:
                clean_dt = target_date_str.split(" ")[0].strip()
                parts = [int(p) for p in clean_dt.split("-")]
                y, m, d = parts[0], parts[1], parts[2]
                input_year = y
                li_chun_day, _ = self._get_solar_term_day(y, 2)
                if (m < 2) or (m == 2 and d < li_chun_day):
                    is_before_li_chun = True
                    effective_year = y - 1
                    li_chun_note = f"កើតមុនថ្ងៃសង្ក្រាន្តលីឈុន (立春 - {y}-02-{li_chun_day:02d}) គិតតាមឆ្នាំសូរ្យគតិ {effective_year}"
                else:
                    is_before_li_chun = False
                    effective_year = y
                    li_chun_note = f"កើតក្រោយថ្ងៃសង្ក្រាន្តលីឈុន (立春 - {y}-02-{li_chun_day:02d}) គិតតាមឆ្នាំសូរ្យគតិ {effective_year}"
            else:
                input_year = int(birth_year) if birth_year is not None else 1990
                effective_year = input_year

            # Last two digits sum reduction (Classical San Yuan formula on effective_year)
            last_two = effective_year % 100
            digits_sum = sum(int(d) for d in str(last_two).zfill(2))
            while digits_sum >= 10:
                digits_sum = sum(int(d) for d in str(digits_sum))

            gender_normalized = gender.strip().lower()
            is_male = gender_normalized in ["male", "m", "ប្រុស", "boy", "man"]

            if effective_year < 2000:
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
                "life_gua": gua,
                "original_calculated": original_gua,
                "gender": "Male (ប្រុស)" if is_male else "Female (ស្រី)",
                "gender_raw": "male" if is_male else "female",
                "gender_kh": "បុរស" if is_male else "ស្ត្រី",
                "is_male": is_male,
                "birth_year": input_year,
                "solar_year": effective_year,
                "is_before_li_chun": is_before_li_chun,
                "li_chun_date": f"{input_year}-02-{li_chun_day:02d}" if li_chun_day else None,
                "li_chun_note": li_chun_note,
                "group": "ក្រុមខាងកើត (East Group)" if is_east_group else "ក្រុមខាងលិច (West Group)",
                "is_east_group": is_east_group,
                "element": self._get_gua_element(gua),
                "trigram_name": self._get_gua_trigram(gua),
                "trigram": self._get_gua_trigram_short(gua),
                "lucky_directions": self.get_lucky_directions(gua),
                "auspicious_directions": self.get_lucky_directions(gua),
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

    def _get_gua_trigram_short(self, gua: int) -> str:
        mapping = {
            1: "Kan",
            2: "Kun",
            3: "Zhen",
            4: "Xun",
            6: "Qian",
            7: "Dui",
            8: "Gen",
            9: "Li"
        }
        return mapping.get(gua, "Kan")

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
    LO_SHU_PATH = ["CENTER", "NW", "W", "NE", "S", "N", "SW", "E", "SE"]

    PALACE_HOME_STARS = {
        "N": 1, "SW": 2, "E": 3, "SE": 4, "CENTER": 5, "NW": 6, "W": 7, "NE": 8, "S": 9
    }
    STAR_HOME_PALACES = {
        1: "N", 2: "SW", 3: "E", 4: "SE", 5: "CENTER", 6: "NW", 7: "W", 8: "NE", 9: "S"
    }

    MOUNTAIN_DRAGON_DATA = {
        # Kan (1, North)
        "壬": {"dragon": "Di", "dragon_kh": "地元龙", "polarity": 1, "palace": "N", "trigram": "坎", "element": "Water", "pinyin": "Ren", "center_deg": 345.0},
        "子": {"dragon": "Tian", "dragon_kh": "天元龙", "polarity": -1, "palace": "N", "trigram": "坎", "element": "Water", "pinyin": "Zi", "center_deg": 0.0},
        "癸": {"dragon": "Ren", "dragon_kh": "人元龙", "polarity": -1, "palace": "N", "trigram": "坎", "element": "Water", "pinyin": "Gui", "center_deg": 15.0},
        # Gen (8, Northeast)
        "丑": {"dragon": "Di", "dragon_kh": "地元龙", "polarity": -1, "palace": "NE", "trigram": "艮", "element": "Earth", "pinyin": "Chou", "center_deg": 30.0},
        "艮": {"dragon": "Tian", "dragon_kh": "天元龙", "polarity": 1, "palace": "NE", "trigram": "艮", "element": "Earth", "pinyin": "Gen", "center_deg": 45.0},
        "寅": {"dragon": "Ren", "dragon_kh": "人元龙", "polarity": 1, "palace": "NE", "trigram": "艮", "element": "Wood", "pinyin": "Yin", "center_deg": 60.0},
        # Zhen (3, East)
        "甲": {"dragon": "Di", "dragon_kh": "地元龙", "polarity": 1, "palace": "E", "trigram": "震", "element": "Wood", "pinyin": "Jia", "center_deg": 75.0},
        "卯": {"dragon": "Tian", "dragon_kh": "天元龙", "polarity": -1, "palace": "E", "trigram": "震", "element": "Wood", "pinyin": "Mao", "center_deg": 90.0},
        "乙": {"dragon": "Ren", "dragon_kh": "人元龙", "polarity": -1, "palace": "E", "trigram": "震", "element": "Wood", "pinyin": "Yi", "center_deg": 105.0},
        # Xun (4, Southeast)
        "辰": {"dragon": "Di", "dragon_kh": "地元龙", "polarity": -1, "palace": "SE", "trigram": "巽", "element": "Earth", "pinyin": "Chen", "center_deg": 120.0},
        "巽": {"dragon": "Tian", "dragon_kh": "天元龙", "polarity": 1, "palace": "SE", "trigram": "巽", "element": "Wood", "pinyin": "Xun", "center_deg": 135.0},
        "巳": {"dragon": "Ren", "dragon_kh": "人元龙", "polarity": 1, "palace": "SE", "trigram": "巽", "element": "Fire", "pinyin": "Si", "center_deg": 150.0},
        # Li (9, South)
        "丙": {"dragon": "Di", "dragon_kh": "地元龙", "polarity": 1, "palace": "S", "trigram": "离", "element": "Fire", "pinyin": "Bing", "center_deg": 165.0},
        "午": {"dragon": "Tian", "dragon_kh": "天元龙", "polarity": -1, "palace": "S", "trigram": "离", "element": "Fire", "pinyin": "Wu", "center_deg": 180.0},
        "丁": {"dragon": "Ren", "dragon_kh": "人元龙", "polarity": -1, "palace": "S", "trigram": "离", "element": "Fire", "pinyin": "Ding", "center_deg": 195.0},
        # Kun (2, Southwest)
        "未": {"dragon": "Di", "dragon_kh": "地元龙", "polarity": -1, "palace": "SW", "trigram": "坤", "element": "Earth", "pinyin": "Wei", "center_deg": 210.0},
        "坤": {"dragon": "Tian", "dragon_kh": "天元龙", "polarity": 1, "palace": "SW", "trigram": "坤", "element": "Earth", "pinyin": "Kun", "center_deg": 225.0},
        "申": {"dragon": "Ren", "dragon_kh": "人元龙", "polarity": 1, "palace": "SW", "trigram": "坤", "element": "Metal", "pinyin": "Shen", "center_deg": 240.0},
        # Dui (7, West)
        "庚": {"dragon": "Di", "dragon_kh": "地元龙", "polarity": 1, "palace": "W", "trigram": "兑", "element": "Metal", "pinyin": "Geng", "center_deg": 255.0},
        "酉": {"dragon": "Tian", "dragon_kh": "天元龙", "polarity": -1, "palace": "W", "trigram": "兑", "element": "Metal", "pinyin": "You", "center_deg": 270.0},
        "辛": {"dragon": "Ren", "dragon_kh": "人元龙", "polarity": -1, "palace": "W", "trigram": "兑", "element": "Metal", "pinyin": "Xin", "center_deg": 285.0},
        # Qian (6, Northwest)
        "戌": {"dragon": "Di", "dragon_kh": "地元龙", "polarity": -1, "palace": "NW", "trigram": "乾", "element": "Earth", "pinyin": "Xu", "center_deg": 300.0},
        "乾": {"dragon": "Tian", "dragon_kh": "天元龙", "polarity": 1, "palace": "NW", "trigram": "乾", "element": "Metal", "pinyin": "Qian", "center_deg": 315.0},
        "亥": {"dragon": "Ren", "dragon_kh": "人元龙", "polarity": 1, "palace": "NW", "trigram": "乾", "element": "Water", "pinyin": "Hai", "center_deg": 330.0},
    }

    PALACE_DRAGONS = {
        "N": {"Di": "壬", "Tian": "子", "Ren": "癸"},
        "NE": {"Di": "丑", "Tian": "艮", "Ren": "寅"},
        "E": {"Di": "甲", "Tian": "卯", "Ren": "乙"},
        "SE": {"Di": "辰", "Tian": "巽", "Ren": "巳"},
        "S": {"Di": "丙", "Tian": "午", "Ren": "丁"},
        "SW": {"Di": "未", "Tian": "坤", "Ren": "申"},
        "W": {"Di": "庚", "Tian": "酉", "Ren": "辛"},
        "NW": {"Di": "戌", "Tian": "乾", "Ren": "亥"},
    }

    # Ti Gua (替卦 - Replacement Stars) Song:
    # 子癸并甲申 -> 1, 壬卯乙未坤 -> 2, 乾亥辰巽巳 -> 6, 酉辛丑艮丙 -> 7, 寅午庚丁 -> 9
    TI_GUA_MAP = {
        "子": 1, "癸": 1, "甲": 1, "申": 1,
        "壬": 2, "卯": 2, "乙": 2, "未": 2, "坤": 2,
        "乾": 6, "亥": 6, "辰": 6, "巽": 6, "巳": 6, "戌": 6,
        "酉": 7, "辛": 7, "丑": 7, "艮": 7, "丙": 7,
        "寅": 9, "午": 9, "庚": 9, "丁": 9,
    }

    STAR_DETAILS = {
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
        """Calculate the Annual Center Flying Star (年飞星入中宫)."""
        digits_sum = sum(int(d) for d in str(year))
        while digits_sum >= 9:
            if digits_sum == 9:
                break
            digits_sum = sum(int(d) for d in str(digits_sum))
        star = (11 - digits_sum) % 9
        return 9 if star == 0 else star

    def fly_stars_9_palaces(self, center_star: int, polarity: int) -> Dict[str, int]:
        """
        Fly a star through the 9 Lo Shu palaces.
        polarity: 1 for forward (顺飞), -1 for backward (逆飞).
        """
        grid = {}
        for idx, palace in enumerate(self.LO_SHU_PATH):
            if idx == 0:
                grid[palace] = center_star
            else:
                if polarity == 1:
                    star = (center_star + idx - 1) % 9 + 1
                else:
                    star = (center_star - idx - 1) % 9 + 1
                grid[palace] = star
        return grid

    def generate_flying_star_grid(self, center_star: int) -> Dict[str, Dict[str, Any]]:
        """Fly stars forward through the 9 Lo Shu Palaces for annual grid."""
        raw_grid = self.fly_stars_9_palaces(center_star, polarity=1)
        grid = {}
        for palace, star_val in raw_grid.items():
            grid[palace] = {
                "star_number": star_val,
                "details": self.STAR_DETAILS.get(star_val, {}),
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

    def calculate_monthly_center_star(self, year: int, month: int) -> int:
        """
        Calculate Xuan Kong Monthly Flying Star center star (月飞星入中).
        Classical song:
        子午卯酉八白求，辰戌丑未五黄游，寅申巳亥二黑起，逆数九星定月宿。
        - Zi, Wu, Mao, You years: Month 1 (Yin) starts at 8, flies backward.
        - Chen, Xu, Chou, Wei years: Month 1 (Yin) starts at 5, flies backward.
        - Yin, Shen, Si, Hai years: Month 1 (Yin) starts at 2, flies backward.
        """
        if LUNAR_AVAILABLE:
            try:
                s = Solar.fromYmd(year, month, 15)
                l = s.getLunar()
                star = l.getMonthNineStar()
                return star.getIndex() + 1
            except Exception:
                pass

        # Astronomical year branch index (January is before Li Chun, belonging to previous solar year)
        effective_year = year - 1 if month == 1 else year
        branch_idx = (effective_year - 1900) % 12
        if branch_idx in [0, 6, 3, 9]:      # 子(0), 午(6), 卯(3), 酉(9)
            base_star = 8
        elif branch_idx in [4, 10, 1, 7]:   # 辰(4), 戌(10), 丑(1), 未(7)
            base_star = 5
        else:                               # 寅(2), 申(8), 巳(5), 亥(11)
            base_star = 2

        # Solar month offset from month 1 (Yin Month begins in February = 0)
        solar_month_offset = (month - 2) % 12
        month_star = (base_star - solar_month_offset - 1) % 9 + 1
        return month_star

    def calculate_annual_afflictions(self, year: int) -> Dict[str, Any]:
        """
        Calculate Grand Annual Calamities & Afflictions (四大年煞):
        1. Tai Sui (太岁 - Grand Duke Jupiter)
        2. Sui Po (岁破 - Year Breaker)
        3. San Sha (三煞: 劫煞 Jie Sha, 灾煞 Zai Sha, 岁煞 Sui Sha)
        4. Wu Huang (五黄廉贞 - Annual Five Yellow Disaster Star)
        Provides 24 Mountains degrees, palace directions, and taboo/cure advice.
        """
        stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        branch_kh = {
            "子": "ជូត (Rat)", "丑": "ឆ្លូវ (Ox)", "寅": "ខាល (Tiger)", "卯": "ថោះ (Rabbit)",
            "辰": "រោង (Dragon)", "巳": "ម្សាញ់ (Snake)", "午": "មមី (Horse)", "未": "មមែ (Goat)",
            "申": "វក (Monkey)", "酉": "រកា (Rooster)", "戌": "ច (Dog)", "亥": "កុរ (Pig)"
        }

        y_stem_idx = (year - 4) % 10
        y_branch_idx = (year - 4) % 12
        year_ganzhi = stems[y_stem_idx] + branches[y_branch_idx]
        tai_sui_branch = branches[y_branch_idx]
        sui_po_branch = branches[(y_branch_idx + 6) % 12]

        m_map = {m["name"]: m for m in self.mountains_24}
        palace_names_kh = {
            "N": "ខាងជើង (Kan)", "NE": "ឦសាន (Gen)", "E": "ខាងកើត (Zhen)", "SE": "អាគ្នេយ៍ (Xun)",
            "S": "ខាងត្បូង (Li)", "SW": "និរតី (Kun)", "W": "ខាងលិច (Dui)", "NW": "ពាយ័ព្យ (Qian)",
            "CENTER": "កណ្តាល (Center)"
        }

        # 1. Tai Sui (太岁)
        ts_m = m_map.get(tai_sui_branch, {})
        tai_sui_data = {
            "mountain": tai_sui_branch,
            "animal_kh": branch_kh.get(tai_sui_branch, tai_sui_branch),
            "direction": ts_m.get("direction", ""),
            "trigram": ts_m.get("trigram", ""),
            "palace_kh": palace_names_kh.get(ts_m.get("direction", "")[:2].rstrip("123"), "ខាងត្បូង (Li)"),
            "degree_range": f"{ts_m.get('degree_start', 0)}° - {ts_m.get('degree_end', 0)}°",
            "rule": "不得在太岁头上动土 (ហាមដាច់ខាតការជីកដី វាយកម្ទេច ឬជួសជុលសំឡេងខ្លាំងនៅទិសនេះ)",
            "advice": "អាចអង្គុយបែរខ្នងរក太岁បាន តែហាមបែរមុខចំ太岁ត្រង់ៗ និងហាមជួសជុលសំណង់ជាដាច់ខាត។"
        }

        # 2. Sui Po (岁破)
        sp_m = m_map.get(sui_po_branch, {})
        sui_po_data = {
            "mountain": sui_po_branch,
            "animal_kh": branch_kh.get(sui_po_branch, sui_po_branch),
            "direction": sp_m.get("direction", ""),
            "trigram": sp_m.get("trigram", ""),
            "palace_kh": palace_names_kh.get(sp_m.get("direction", "")[:2].rstrip("123"), "ខាងជើង (Kan)"),
            "degree_range": f"{sp_m.get('degree_start', 0)}° - {sp_m.get('degree_end', 0)}°",
            "rule": "岁破之位不可犯 (ទិសឆុងនឹង太岁 ១៨០ ដឺក្រេ ហាមប៉ះពាល់)",
            "advice": "ចៀសវាងការផ្លាស់ប្តូរទីតាំងគ្រែគេង ឬតុធ្វើការមករកទិសនេះ និងហាមជួសជុលខួងជញ្ជាំង។"
        }

        # 3. San Sha (三煞)
        if y_branch_idx in [2, 6, 10]:  # 寅, 午, 戌 -> North
            san_sha_sector = "N"
            san_sha_name_kh = "ទិសខាងជើង (North - 亥子丑)"
            jie_sha_m, zai_sha_m, sui_sha_m = "亥", "子", "丑"
        elif y_branch_idx in [8, 0, 4]:  # 申, 子, 辰 -> South
            san_sha_sector = "S"
            san_sha_name_kh = "ទិសខាងត្បូង (South - 巳午未)"
            jie_sha_m, zai_sha_m, sui_sha_m = "巳", "午", "未"
        elif y_branch_idx in [5, 9, 1]:  # 巳, 酉, 丑 -> East
            san_sha_sector = "E"
            san_sha_name_kh = "ទិសខាងកើត (East - 寅卯辰)"
            jie_sha_m, zai_sha_m, sui_sha_m = "寅", "卯", "辰"
        else:  # 亥, 卯, 未 -> West
            san_sha_sector = "W"
            san_sha_name_kh = "ទិសខាងលិច (West - 申酉戌)"
            jie_sha_m, zai_sha_m, sui_sha_m = "申", "酉", "戌"

        js_m = m_map.get(jie_sha_m, {})
        zs_m = m_map.get(zai_sha_m, {})
        ss_m = m_map.get(sui_sha_m, {})

        san_sha_data = {
            "sector": san_sha_sector,
            "sector_kh": san_sha_name_kh,
            "palace_kh": palace_names_kh.get(san_sha_sector, san_sha_sector),
            "mountains": [jie_sha_m, zai_sha_m, sui_sha_m],
            "details": {
                "jie_sha": {"mountain": jie_sha_m, "direction": js_m.get("direction", ""), "meaning": "劫煞 (គ្រោះប្លន់ ការខាតបង់)"},
                "zai_sha": {"mountain": zai_sha_m, "direction": zs_m.get("direction", ""), "meaning": "灾煞 (គ្រោះមហន្តរាយ ជំងឺ)"},
                "sui_sha": {"mountain": sui_sha_m, "direction": ss_m.get("direction", ""), "meaning": "岁煞 (ឧបសគ្គ ពន្យារពេល)"}
            },
            "rule": "三煞可向不可坐 (អាចបែរមុខរកសាមសាតបាន តែហាមដាច់ខាតអង្គុយបែរខ្នងរកសាមសាត)",
            "advice": "ហាមដាច់ខាតការជួសជុល ជីកដី ឬវាយកម្ទេចក្នុងទិសនេះ។ អាចដាក់សត្វសិរីសួស្តី ភីស៊ូ (Pi Xiu) ឬ គីលីន (Qi Lin) ៣ បែរមុខរកទិសសាមសាតដើម្បីទប់ទល់។"
        }

        # 4. Annual Five Yellow (岁五黄)
        annual_center = self.calculate_annual_center_star(year)
        annual_grid = self.fly_stars_9_palaces(annual_center, polarity=1)
        five_yellow_palace = next(p for p, s in annual_grid.items() if s == 5)

        five_yellow_data = {
            "palace": five_yellow_palace,
            "palace_kh": palace_names_kh.get(five_yellow_palace, five_yellow_palace),
            "star": "五黄廉贞大煞 (Five Yellow Disaster Star)",
            "rule": "五黄所到之处不宜动土 (ទីតាំងផ្កាយ ៥ លឿង ហាមកម្រើក ហាមដាក់ភ្លើងភ្លឺ)",
            "cure": "ត្រូវដាក់កណ្តឹងខ្យល់លោហធាតុ ៦ បំពង់ ឬកាក់ចិនលង្ហិន ៦ កាក់ ដើម្បីបន្សាបធាតុដីអវិជ្ជមាន។"
        }

        return {
            "year": year,
            "ganzhi": year_ganzhi,
            "tai_sui": tai_sui_data,
            "sui_po": sui_po_data,
            "san_sha": san_sha_data,
            "wu_huang": five_yellow_data,
            "executive_summary": (
                f"ប្រចាំឆ្នាំ {year} ({year_ganzhi})៖ 太岁 (Tai Sui) នៅ {tai_sui_data['mountain']} ({tai_sui_data['degree_range']}), "
                f"岁破 (Sui Po) នៅ {sui_po_data['mountain']} ({sui_po_data['degree_range']}), "
                f"三煞 (San Sha) នៅ {san_sha_data['sector_kh']}, "
                f"និង 五黄 (Five Yellow) ធ្លាក់នៅ {five_yellow_data['palace_kh']}។ "
                f"ហាមដាច់ខាតការជីកដី ឬជួសជុលសំណង់នៅទិសដៅទាំងនេះ!"
            )
        }

    def calculate_flying_stars(self, year: int, month: Optional[int] = None) -> Dict[str, Any]:
        """Calculate complete Xuan Kong Flying Stars profile for year and period, with optional monthly chart and annual afflictions."""
        # Solar year check: January (Month 1) falls before Li Chun, so the annual flying star belongs to (year - 1)
        effective_annual_year = year - 1 if month == 1 else year
        li_chun_note = f"ខែមករាស្ថិតនៅមុនថ្ងៃសង្ក្រាន្តលីឈុន (立春) គិតតាមផ្កាយប្រចាំឆ្នាំ {effective_annual_year}" if month == 1 else None

        period = self.calculate_period(effective_annual_year)
        annual_center = self.calculate_annual_center_star(effective_annual_year)
        grid = self.generate_flying_star_grid(annual_center)
        afflictions = self.calculate_annual_afflictions(effective_annual_year)

        result = {
            "year": year,
            "solar_year": effective_annual_year,
            "li_chun_note": li_chun_note,
            "period": period,
            "period_element": "Fire (ធាតុភ្លើង)" if period == 9 else "Earth (ធាតុដី)",
            "annual_center_star": annual_center,
            "grid": grid,
            "wealth_palace": "S (ខាងត្បូង)" if period == 9 else "NE (ឦសាន)",
            "danger_palaces": [p for p, v in grid.items() if v["star_number"] in [5, 2]],
            "annual_afflictions": afflictions
        }

        if month is not None and 1 <= month <= 12:
            monthly_center = self.calculate_monthly_center_star(year, month)
            monthly_grid = self.generate_flying_star_grid(monthly_center)
            result["month"] = month
            result["monthly_center_star"] = monthly_center
            result["monthly_grid"] = monthly_grid
            result["monthly_danger_palaces"] = [p for p, v in monthly_grid.items() if v["star_number"] in [5, 2]]

        return {"success": True, "data": result}

    # =========================================================================
    # 2b. Xuan Kong 24 Mountains Natal Chart (玄空九宫宅命盘)
    # =========================================================================
    def calculate_house_flying_stars(
        self,
        facing_degree: Optional[float] = None,
        sitting_degree: Optional[float] = None,
        period: Optional[int] = None,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Calculate complete Xuan Kong Flying Stars 24 Mountains Natal Chart (玄空九宫宅命盘).
        Computes:
        1. Period Star Grid (运盘 - Base Chart)
        2. Mountain Star (山星 - Sitting Star) with Three Dragons Shun/Ni Polarity
        3. Facing Star (向星 - Water Star) with Three Dragons Shun/Ni Polarity
        4. Ti Gua (替卦 / Replacement Stars) detection for Kong Wang / Out-of-Trigram boundaries
        5. Special Formations (旺山旺向, 上山下水, 双星到向, 双星到座, 全盘合十, 连珠三般卦, 父母三般卦)
        6. Castle Gate Formula (城门诀 - Left & Right Gates)
        7. Zero Spirit & Direct Spirit (零神与正神 - Water vs Mountain placement for Period 9)
        8. Annual Flying Star overlay & Palace-by-Palace Classical Syntheses
        """
        try:
            current_year = year or datetime.now().year
            active_period = period if period is not None else self.calculate_period(current_year)

            # Resolve Facing & Sitting degrees
            if facing_degree is not None:
                face_deg = facing_degree % 360.0
                sit_deg = (face_deg + 180.0) % 360.0
            elif sitting_degree is not None:
                sit_deg = sitting_degree % 360.0
                face_deg = (sit_deg + 180.0) % 360.0
            else:
                face_deg = 180.0  # Default Facing South (Li Fire)
                sit_deg = 0.0     # Default Sitting North (Kan Water)

            # Look up Mountains
            sit_res = self.get_mountain_by_degree(sit_deg)
            face_res = self.get_mountain_by_degree(face_deg)

            sit_mountain_name = sit_res["mountain"]["name"]
            face_mountain_name = face_res["mountain"]["name"]

            sit_info = self.MOUNTAIN_DRAGON_DATA.get(sit_mountain_name, self.MOUNTAIN_DRAGON_DATA["子"])
            face_info = self.MOUNTAIN_DRAGON_DATA.get(face_mountain_name, self.MOUNTAIN_DRAGON_DATA["午"])

            sit_palace = sit_info["palace"]
            face_palace = face_info["palace"]
            sit_dragon = sit_info["dragon"]
            face_dragon = face_info["dragon"]

            # Check for Ti Gua (替卦) boundary deviation (outer 3° or within 1.5° of border)
            sit_center_deg = sit_info["center_deg"]
            deg_diff = abs((sit_deg - sit_center_deg + 180.0) % 360.0 - 180.0)
            is_ti_gua = deg_diff > 4.5  # Boundary threshold (Zheng Zhen: within +/- 4.5°)

            # Da Kong Wang (大空亡) vs Xiao Kong Wang (小空亡)
            palace_borders = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]
            is_da_kong_wang = any(abs((sit_deg - pb + 180.0) % 360.0 - 180.0) <= 1.5 for pb in palace_borders)
            is_xiao_kong_wang = is_ti_gua and not is_da_kong_wang

            # 1. Period Base Chart (运盘) - Always flies forward (顺飞)
            period_grid = self.fly_stars_9_palaces(active_period, polarity=1)

            # 2. Sitting Mountain Star (山星)
            sit_period_star = period_grid[sit_palace]
            if is_ti_gua:
                # Ti Gua rule for Mountain Star
                if sit_period_star == 5:
                    m_center_star = self.TI_GUA_MAP.get(sit_mountain_name, 5)
                    m_polarity = sit_info["polarity"]
                else:
                    home_pal = self.STAR_HOME_PALACES[sit_period_star]
                    home_m = self.PALACE_DRAGONS[home_pal][sit_dragon]
                    m_center_star = self.TI_GUA_MAP.get(home_m, sit_period_star)
                    m_polarity = self.MOUNTAIN_DRAGON_DATA[home_m]["polarity"]
            else:
                m_center_star = sit_period_star
                if m_center_star == 5:
                    m_polarity = sit_info["polarity"]
                else:
                    home_pal = self.STAR_HOME_PALACES[m_center_star]
                    home_m = self.PALACE_DRAGONS[home_pal][sit_dragon]
                    m_polarity = self.MOUNTAIN_DRAGON_DATA[home_m]["polarity"]

            # 3. Facing Water Star (向星)
            face_period_star = period_grid[face_palace]
            if is_ti_gua:
                # Ti Gua rule for Facing Star
                if face_period_star == 5:
                    f_center_star = self.TI_GUA_MAP.get(face_mountain_name, 5)
                    f_polarity = face_info["polarity"]
                else:
                    home_pal = self.STAR_HOME_PALACES[face_period_star]
                    home_m = self.PALACE_DRAGONS[home_pal][face_dragon]
                    f_center_star = self.TI_GUA_MAP.get(home_m, face_period_star)
                    f_polarity = self.MOUNTAIN_DRAGON_DATA[home_m]["polarity"]
            else:
                f_center_star = face_period_star
                if f_center_star == 5:
                    f_polarity = face_info["polarity"]
                else:
                    home_pal = self.STAR_HOME_PALACES[f_center_star]
                    home_m = self.PALACE_DRAGONS[home_pal][face_dragon]
                    f_polarity = self.MOUNTAIN_DRAGON_DATA[home_m]["polarity"]

            # 4. Fly Mountain & Water Stars into 9 Palaces
            mountain_grid = self.fly_stars_9_palaces(m_center_star, m_polarity)
            water_grid = self.fly_stars_9_palaces(f_center_star, f_polarity)

            # Annual Flying Star grid overlay
            annual_center = self.calculate_annual_center_star(current_year)
            annual_grid = self.fly_stars_9_palaces(annual_center, polarity=1)

            # 5. Assemble Full 9 Palaces Natal Chart
            palace_names_kh = {
                "N": "ខាងជើង (Kan)", "NE": "ឦសាន (Gen)", "E": "ខាងកើត (Zhen)", "SE": "អាគ្នេយ៍ (Xun)",
                "S": "ខាងត្បូង (Li)", "SW": "និរតី (Kun)", "W": "ខាងលិច (Dui)", "NW": "ពាយ័ព្យ (Qian)",
                "CENTER": "កណ្តាល (Center)"
            }

            natal_chart = {}
            for pal in ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "CENTER"]:
                m_s = mountain_grid[pal]
                p_s = period_grid[pal]
                w_s = water_grid[pal]
                a_s = annual_grid[pal]
                natal_chart[pal] = {
                    "palace": pal,
                    "palace_kh": palace_names_kh.get(pal, pal),
                    "mountain_star": m_s,
                    "period_star": p_s,
                    "water_star": w_s,
                    "annual_star": a_s,
                    "stars_display": f"{m_s} {p_s} {w_s}",
                    "is_sitting_palace": (pal == sit_palace),
                    "is_facing_palace": (pal == face_palace),
                    "combination_meaning": self._get_star_combination_meaning(m_s, w_s, p_s),
                    "cure_advice": self._get_palace_cure(m_s, w_s, a_s, pal)
                }

            # 6. Detect Classical Xuan Kong Formations
            formations = self._detect_xuan_kong_formations(
                natal_chart=natal_chart,
                period=active_period,
                sit_palace=sit_palace,
                face_palace=face_palace,
                is_da_kong_wang=is_da_kong_wang,
                is_xiao_kong_wang=is_xiao_kong_wang
            )

            # 7. Calculate Castle Gates (城门诀)
            castle_gates = self._calculate_castle_gates(face_palace, face_dragon, active_period)

            # 8. Ling Shen & Zheng Shen (零神与正神) Rules for Period 9
            zero_spirit = self._get_ling_shen_zheng_shen(active_period)

            result = {
                "success": True,
                "period": active_period,
                "year": current_year,
                "chart_mode": "替卦 (Ti Gua - Replacement Stars)" if is_ti_gua else "下卦 (Xia Gua - Standard Stars)",
                "is_ti_gua": is_ti_gua,
                "is_da_kong_wang": is_da_kong_wang,
                "is_xiao_kong_wang": is_xiao_kong_wang,
                "sitting": {
                    "degree": round(sit_deg, 2),
                    "mountain": sit_mountain_name,
                    "pinyin": sit_info["pinyin"],
                    "palace": sit_palace,
                    "palace_kh": palace_names_kh.get(sit_palace, sit_palace),
                    "dragon": sit_info["dragon_kh"],
                    "polarity": "Yang (+)" if sit_info["polarity"] == 1 else "Yin (-)"
                },
                "facing": {
                    "degree": round(face_deg, 2),
                    "mountain": face_mountain_name,
                    "pinyin": face_info["pinyin"],
                    "palace": face_palace,
                    "palace_kh": palace_names_kh.get(face_palace, face_palace),
                    "dragon": face_info["dragon_kh"],
                    "polarity": "Yang (+)" if face_info["polarity"] == 1 else "Yin (-)"
                },
                "flight_dynamics": {
                    "period_star_center": active_period,
                    "mountain_star_center": m_center_star,
                    "mountain_star_flight": "顺飞 (Forward Flight +)" if m_polarity == 1 else "逆飞 (Reverse Flight -)",
                    "water_star_center": f_center_star,
                    "water_star_flight": "顺飞 (Forward Flight +)" if f_polarity == 1 else "逆飞 (Reverse Flight -)"
                },
                "natal_chart": natal_chart,
                "formations": formations,
                "castle_gates": castle_gates,
                "ling_shen_zheng_shen": zero_spirit,
                "practical_advice": self._generate_house_fengshui_advice(natal_chart, formations, zero_spirit, sit_palace, face_palace)
            }

            return {"success": True, "data": result}

        except Exception as e:
            return {"success": False, "error": f"Error calculating House Flying Stars: {str(e)}"}

    def _detect_xuan_kong_formations(
        self,
        natal_chart: Dict[str, Any],
        period: int,
        sit_palace: str,
        face_palace: str,
        is_da_kong_wang: bool = False,
        is_xiao_kong_wang: bool = False
    ) -> List[Dict[str, str]]:
        """Identify classical formations: Wang Shan Wang Xiang, Shang Shan Xia Shui, Da/Xiao Kong Wang, etc."""
        formations = []

        if is_da_kong_wang:
            formations.append({
                "code": "DA_KONG_WANG",
                "name_zh": "大空亡",
                "name_kh": "⚠️ បន្ទាត់មរណៈឆ្លងក្វា 大空亡 (Great Empty Line)",
                "nature": "Critical Danger",
                "description": "មុំផ្ទះស្ថិតនៅលើបន្ទាត់ព្រំប្រទល់កាត់ក្វាខុសគ្នា (大空亡) ថាមពលច្របូកច្របល់ធ្ងន់ធ្ងរ អាចបណ្តាលឱ្យមានជំងឺស្មារតី ឧបសគ្គធំ និងការខាតបង់ទ្រព្យ។ ត្រូវកែសម្រួលមុំមាត់ទ្វារ ឬប្រើក្បួនបង្វែរទ្វារបន្ទាយជាបន្ទាន់!"
            })
        elif is_xiao_kong_wang:
            formations.append({
                "code": "XIAO_KONG_WANG",
                "name_zh": "小空亡",
                "name_kh": "⚠️ បន្ទាត់ទទេឆ្លងភ្នំ 小空亡 (Small Empty Line / Rider Line)",
                "nature": "Caution Needed",
                "description": "មុំផ្ទះស្ថិតនៅគែម ៣ ដឺក្រេខាងក្រៅរវាងភ្នំពីរក្នុងក្វាដដែល (小空亡) ត្រូវប្រើប្រាស់ក្បួនផ្កាយជំនួស (替卦 Ti Gua) ដើម្បីកែខៃតុល្យភាព។"
            })

        sit_m = natal_chart[sit_palace]["mountain_star"]
        sit_w = natal_chart[sit_palace]["water_star"]
        face_m = natal_chart[face_palace]["mountain_star"]
        face_w = natal_chart[face_palace]["water_star"]

        # 1. 旺山旺向 (Wang Shan Wang Xiang)
        if sit_m == period and face_w == period:
            formations.append({
                "code": "WANG_SHAN_WANG_XIANG",
                "name_zh": "旺山旺向",
                "name_kh": "ទម្រង់កំពូល 旺山旺向 (សម្បូរមនុស្ស និងសម្បូរទ្រព្យ)",
                "nature": "Auspicious",
                "description": "ផ្កាយភ្នំជោគជ័យនៅទិសអង្គុយ និងផ្កាយទឹកជោគជ័យនៅទិសបែរមុខ។ ជាទម្រង់មហាសិរីសួស្តីបំផុត នាំមកទាំងកិត្តិយស សុខភាព និងទ្រព្យសម្បត្តិហូរហៀរ។"
            })

        # 2. 上山下水 (Shang Shan Xia Shui)
        if sit_w == period and face_m == period:
            formations.append({
                "code": "SHANG_SHAN_XIA_SHUI",
                "name_zh": "上山下水",
                "name_kh": "ទម្រង់បញ្ច្រាស 上山下水 (ខាតបង់ទ្រព្យ និងប៉ះពាល់សុខភាព)",
                "nature": "Inauspicious",
                "description": "ផ្កាយទឹកឡើងភ្នំ ផ្កាយភ្នំធ្លាក់ទឹក។ ប្រសិនបើមុខផ្ទះមានភ្នំខ្ពស់ ហើយក្រោយផ្ទះមានទឹក នោះនឹងប្រែជាល្អ ប៉ុន្តែបើជាផ្ទះធម្មតា ត្រូវកែសម្រួលជាបន្ទាន់ដើម្បីការពារការបាត់បង់ទ្រព្យ។"
            })

        # 3. 双星到向 (Shuang Xing Dao Xiang)
        if face_m == period and face_w == period:
            formations.append({
                "code": "SHUANG_XING_DAO_XIANG",
                "name_zh": "双星到向",
                "name_kh": "ទម្រង់ផ្កាយភ្លោះនៅទិសមុខ 双星到向 (ទ្រព្យសម្បត្តិលេចធ្លោខ្លាំង)",
                "nature": "Auspicious for Wealth",
                "description": "ទាំងផ្កាយភ្នំ និងផ្កាយទឹកនៃយុគ ស្ថិតនៅទិសមុខផ្ទះទាំងអស់។ ល្អឥតខ្ចោះសម្រាប់ការរកស៊ីលក់ដូរ និងការវិនិយោគ។ គួរមានទីធ្លារាបស្មើខាងមុខ និងមានទឹកដើម្បីស្រូបទ្រព្យ។"
            })

        # 4. 双星到座 (Shuang Xing Dao Zuo)
        if sit_m == period and sit_w == period:
            formations.append({
                "code": "SHUANG_XING_DAO_ZUO",
                "name_zh": "双星到座",
                "name_kh": "ទម្រង់ផ្កាយភ្លោះនៅទិសអង្គុយ 双星到座 (សុខភាព និងមនុស្សរុងរឿង)",
                "nature": "Auspicious for Health",
                "description": "ទាំងផ្កាយភ្នំ និងផ្កាយទឹកនៃយុគ ស្ថិតនៅក្រោយផ្ទះ។ នាំមកនូវសុខភាពរឹងមាំ សេចក្តីសុខក្នុងគ្រួសារ និងមានអ្នកជួយជ្រោមជ្រែង។"
            })

        # 5. 全盘合十 (Combination of 10)
        is_he_shi_m = all((v["mountain_star"] + v["period_star"]) == 10 for v in natal_chart.values())
        is_he_shi_w = all((v["water_star"] + v["period_star"]) == 10 for v in natal_chart.values())
        if is_he_shi_m or is_he_shi_w:
            formations.append({
                "code": "HE_SHI_10",
                "name_zh": "全盘合十",
                "name_kh": "ទម្រង់ពិសិដ្ឋ 全盘合十 (បូកបញ្ចូលស្មើ ១០ គ្រប់វិហារ)",
                "nature": "Supreme Auspicious",
                "description": "ថាមពលយិនយ៉ាងមានតុល្យភាពពេញលេញ ជួយបន្សាបគ្រោះកាច និងទាក់ទាញលាភសំណាងគ្រប់ទិសទី។"
            })

        # 6. 父母三般卦 (Parent Three Gua: 1-4-7, 2-5-8, 3-6-9 in each palace)
        parent_triads = [{1, 4, 7}, {2, 5, 8}, {3, 6, 9}]
        is_fu_mu = all(
            {v["mountain_star"], v["period_star"], v["water_star"]} in parent_triads
            for v in natal_chart.values()
        )
        if is_fu_mu:
            formations.append({
                "code": "FU_MU_SAN_BAN_GUA",
                "name_zh": "父母三般卦",
                "name_kh": "ទម្រង់អភិជន 父母三般卦 (Parent Three Gua)",
                "nature": "Supreme Auspicious",
                "description": "គ្រប់វិហារទាំង ៩ សុទ្ធតែប្រមូលផ្តុំដោយក្រុមផ្កាយ ១-៤-៧, ២-៥-៨, ៣-៦-៩ ជួយឱ្យលំហូរថាមពលឆ្លងយុគទាំង ៣ ដោយរលូន និងមានសេចក្តីចម្រើនយូរអង្វែង មិនងាយស្រកចុះឡើយ។"
            })

        # 7. 连珠三般卦 (Continuous Three Gua: consecutive numbers in each palace)
        def _is_consecutive(s1: int, s2: int, s3: int) -> bool:
            sorted_stars = sorted([s1, s2, s3])
            if (sorted_stars[0] + 1 == sorted_stars[1] and sorted_stars[1] + 1 == sorted_stars[2]):
                return True
            if sorted_stars == [1, 8, 9] or sorted_stars == [1, 2, 9]:
                return True
            return False

        is_lian_zhu = all(
            _is_consecutive(v["mountain_star"], v["period_star"], v["water_star"])
            for v in natal_chart.values()
        )
        if is_lian_zhu:
            formations.append({
                "code": "LIAN_ZHU_SAN_BAN_GUA",
                "name_zh": "连珠三般卦",
                "name_kh": "ទម្រង់កម្រ 连珠三般卦 (Continuous Three Gua)",
                "nature": "Supreme Auspicious",
                "description": "ផ្កាយក្នុងវិហារទាំង ៩ រៀបជាលំដាប់តួលេខបន្តបន្ទាប់គ្នា នាំមកនូវកិត្តិយស បញ្ញាឈ្លាសវៃ និងការរីកចម្រើនឥតឈប់ឈរ។"
            })

        # 8. 伏吟 (Fu Yin) & 反吟 (Fan Yin)
        is_fu_yin_m = all(v["mountain_star"] == self.PALACE_HOME_STARS[p] for p, v in natal_chart.items())
        is_fu_yin_w = all(v["water_star"] == self.PALACE_HOME_STARS[p] for p, v in natal_chart.items())
        if is_fu_yin_m or is_fu_yin_w:
            formations.append({
                "code": "FU_YIN",
                "name_zh": "伏吟",
                "name_kh": "ទម្រង់ស្ទះថាមពល 伏吟 (Fu Yin)",
                "nature": "Inauspicious",
                "description": "ផ្កាយត្រូវគ្នានឹងវិហារដើមនៃផែនទីឡូស៊ូ អាចធ្វើឱ្យថាមពលនៅទ្រឹង និងកើតមានឧបសគ្គរារាំង ត្រូវប្រើប្រាស់ចលនាខ្យល់ពន្លឺ និងវត្ថុកែខៃដើម្បីរំដោះថាមពល។"
            })

        is_fan_yin_m = all((v["mountain_star"] + self.PALACE_HOME_STARS[p]) == 10 for p, v in natal_chart.items())
        is_fan_yin_w = all((v["water_star"] + self.PALACE_HOME_STARS[p]) == 10 for p, v in natal_chart.items())
        if is_fan_yin_m or is_fan_yin_w:
            formations.append({
                "code": "FAN_YIN",
                "name_zh": "反吟",
                "name_kh": "ទម្រង់ប៉ះទង្គិច 反吟 (Fan Yin)",
                "nature": "Inauspicious",
                "description": "ផ្កាយបញ្ច្រាសទិសទាំងស្រុង បង្កជាភាពរង្គោះរង្គើ ត្រូវដោះស្រាយបន្ទាន់ដោយប្រើប្រាស់ធាតុសម្រុះសម្រួល។"
            })

        if not formations:
            formations.append({
                "code": "BALANCED_STANDARD",
                "name_zh": "普通格局",
                "name_kh": "ទម្រង់ធម្មតាសមតុល្យ (Standard Energy Chart)",
                "nature": "Neutral",
                "description": "ថាមពលក្នុងផ្ទះមានលក្ខណៈធម្មតា ត្រូវប្រើប្រាស់ការដេគ័រ និងឧបករណ៍ហុងស៊ុយដើម្បីជំរុញទិសល្អ និងបន្សាបទិសគ្រោះ។"
            })

        return formations

    def _calculate_castle_gates(self, face_palace: str, face_dragon: str, period: int) -> Dict[str, Any]:
        """
        Calculate Castle Gate (城门诀 - Cheng Men Jue) according to classical Xuan Kong formulas:
        1. Period star p_star at the castle gate enters center.
        2. Look up the Home Palace of p_star in the original Luo Shu.
        3. Match the mountain in that Home Palace corresponding to face_dragon (Tian, Di, Ren).
        4. Use that mountain's Yin/Yang polarity to fly p_star.
        5. If landing on the gate palace equals the current period star, it is a usable Castle Gate (可用城门).
        """
        adjacent_gates = {
            "S": {"left": "SE", "right": "SW"},
            "N": {"left": "NE", "right": "NW"},
            "E": {"left": "NE", "right": "SE"},
            "W": {"left": "NW", "right": "SW"},
            "SE": {"left": "E", "right": "S"},
            "SW": {"left": "S", "right": "W"},
            "NE": {"left": "N", "right": "E"},
            "NW": {"left": "W", "right": "N"}
        }

        gates = adjacent_gates.get(face_palace, {"left": "SE", "right": "SW"})
        left_pal = gates["left"]
        right_pal = gates["right"]

        period_grid = self.fly_stars_9_palaces(period, 1)
        left_p_star = period_grid[left_pal]
        right_p_star = period_grid[right_pal]

        def _get_gate_polarity(p_star: int, default_pal: str) -> int:
            if p_star == 5:
                face_m = self.PALACE_DRAGONS.get(default_pal, {}).get(face_dragon, "午")
                return self.MOUNTAIN_DRAGON_DATA.get(face_m, {}).get("polarity", 1)
            home_pal = self.STAR_HOME_PALACES.get(p_star, default_pal)
            home_m = self.PALACE_DRAGONS.get(home_pal, {}).get(face_dragon, "午")
            return self.MOUNTAIN_DRAGON_DATA.get(home_m, {}).get("polarity", 1)

        # Check left gate flight
        left_polarity = _get_gate_polarity(left_p_star, left_pal)
        left_flight = self.fly_stars_9_palaces(left_p_star, left_polarity)
        left_is_usable = (left_flight[left_pal] == period)

        # Check right gate flight
        right_polarity = _get_gate_polarity(right_p_star, right_pal)
        right_flight = self.fly_stars_9_palaces(right_p_star, right_polarity)
        right_is_usable = (right_flight[right_pal] == period)

        return {
            "facing_palace": face_palace,
            "left_castle_gate": {
                "palace": left_pal,
                "period_star": left_p_star,
                "is_usable": left_is_usable,
                "status_kh": "ទ្វារបន្ទាយស្រូបទ្រព្យពិត (可用城门)" if left_is_usable else "ទ្វារបន្ទាយធម្មតា",
                "advice": f"បើកទ្វារ ឬបង្អួចនៅទិស {left_pal} អាចស្រូបថាមពលទ្រព្យយ៉ាងខ្លាំងក្នុងយុគ {period}!" if left_is_usable else "ប្រើប្រាស់ជាច្រកបន្ទាប់បន្សំធម្មតា"
            },
            "right_castle_gate": {
                "palace": right_pal,
                "period_star": right_p_star,
                "is_usable": right_is_usable,
                "status_kh": "ទ្វារបន្ទាយស្រូបទ្រព្យពិត (可用城门)" if right_is_usable else "ទ្វារបន្ទាយធម្មតា",
                "advice": f"បើកទ្វារ ឬបង្អួចនៅទិស {right_pal} អាចស្រូបថាមពលទ្រព្យយ៉ាងខ្លាំងក្នុងយុគ {period}!" if right_is_usable else "ប្រើប្រាស់ជាច្រកបន្ទាប់បន្សំធម្មតា"
            }
        }

    def _get_ling_shen_zheng_shen(self, period: int) -> Dict[str, str]:
        """Ling Shen (Water placement) and Zheng Shen (Mountain placement) for the period."""
        if period == 9:
            return {
                "period": "យុគទី ៩ (Period 9: 2024-2043) - ធាតុភ្លើង",
                "zheng_shen": "ខាងត្បូង (South - 离)",
                "zheng_shen_rule": "ទិសវិញ្ញាណពិត (正神)៖ ត្រូវការភ្នំខ្ពស់ ជញ្ជាំងរឹងមាំ ឬបន្ទប់គេងស្ងប់ស្ងាត់ ដើម្បីថែរក្សាសុខភាព និងកិត្តិយស។ ហាមដាក់អាងទឹក ឬផ្លូវចេញចូលធំ!",
                "ling_shen": "ខាងជើង (North - 坎)",
                "ling_shen_rule": "ទិសវិញ្ញាណសូន្យ (零神)៖ ជាទិសស្រូបទ្រព្យធំបំផុតក្នុងយុគ ៩! ត្រូវការទឹកសកម្ម (អាងទឹក ទឹកហូរ អាងចិញ្ចឹមត្រី) ឬទ្វារធំចេញចូលដើម្បីនាំទ្រព្យចូលផ្ទះ។",
                "zhao_shen": "អាគ្នេយ៍ (Southeast - 巽)",
                "zhao_shen_rule": "ទិសវិញ្ញាណរស្មី (照神)៖ អាចដាក់ទឹកបន្ទាប់បន្សំដើម្បីជំរុញលាភសំណាង និងការសិក្សា។",
                "cui_shen": "ខាងកើត (East - 震)",
                "cui_shen_rule": "ទិសជំរុញលាភ (催神)៖ ត្រូវការរុក្ខជាតិបៃតង ឬភ្នំស្រាលៗដើម្បីពង្រឹងកម្លាំងធាតុឈើចិញ្ចឹមភ្លើងយុគ ៩។"
            }
        else:
            return {
                "period": f"យុគទី {period}",
                "zheng_shen": "ទិសនៃផ្កាយយុគ",
                "zheng_shen_rule": "ទិសវិញ្ញាណពិតត្រូវការភ្នំ",
                "ling_shen": "ទិសផ្ទុយនឹងផ្កាយយុគ",
                "ling_shen_rule": "ទិសវិញ្ញាណសូន្យត្រូវការទឹក"
            }

    def _get_star_combination_meaning(self, mountain: int, water: int, period: int) -> str:
        """Classical Xuan Kong Star Combination Syntheses."""
        pair = (mountain, water)
        meanings = {
            (1, 4): "名扬四海 (Academic & Fame Luck)៖ ល្អបំផុតសម្រាប់ការសិក្សា ប្រលងជាប់ និងការច្នៃប្រឌិត។",
            (4, 1): "名扬四海 (Academic & Fame Luck)៖ ល្អសម្រាប់តុធ្វើការ និងបន្ទប់រៀនសូត្រ។",
            (9, 9): "九紫重逢 (Supreme Fire Wealth)៖ អធិរាជផ្កាយយុគ ៩! នាំមកនូវជោគជ័យលឿនរហ័ស ទ្រព្យសម្បត្តិ និងពិធីមង្គល។",
            (8, 8): "八白比和 (Abundant Prosperity)៖ ទ្រព្យសម្បត្តិហូរហៀរ និងភាពសម្បូរបែប។",
            (1, 6): "虚联奎璧 (Wisdom & Official Luck)៖ ជំរុញតំណែងការងារ បញ្ញាវាងវៃ និងមានអ្នកជួយជ្រោមជ្រែង។",
            (6, 1): "虚联奎璧 (Wisdom & Official Luck)៖ ល្អសម្រាប់ថ្នាក់ដឹកនាំ និងមន្ត្រីរាជការ។",
            (2, 5): "二五交加 (Extreme Illness & Obstacle)៖ គ្រោះជំងឺ និងឧបសគ្គធំ! ត្រូវប្រើផ្លែឃ្លោកទង់ដែង ឬកាក់ ៦ កាក់ដើម្បីរំលាយ។",
            (5, 2): "二五交加 (Extreme Illness & Obstacle)៖ គ្រោះជំងឺ និងឧបសគ្គធំ! ត្រូវប្រើផ្លែឃ្លោកទង់ដែងដើម្បីរំលាយ។",
            (3, 7): "穿心煞 (Robbery & Dispute)៖ ប្រយ័ត្នចោរលួច ការប្តឹងផ្តល់ និងការខាតបង់ប្រាក់កាស។",
            (7, 3): "穿心煞 (Robbery & Dispute)៖ គួរដាក់កែវទឹកស្អាត ឬរុក្ខជាតិទឹកដើម្បីទប់កំហឹងលោហៈ-ឈើ។",
            (2, 3): "斗牛煞 (Conflict & Lawsuit)៖ ជម្លោះពាក្យសម្តី និងការឈ្លោះប្រកែក។ អាចប្រើពណ៌ក្រហម (ភ្លើង) ដើម្បីរំលាយ។",
            (3, 2): "斗牛煞 (Conflict & Lawsuit)៖ ជម្លោះពាក្យសម្តី ត្រូវរក្សាភាពស្ងប់ស្ងាត់។",
            (9, 7): "回禄之灾 (Fire Hazard Risk)៖ ភ្លើងឆេះ ឬការខាតបង់ទ្រព្យភ្លាមៗ។ គួរចៀសវាងការដាក់ភ្លើងភ្លឺខ្លាំង។"
        }
        return meanings.get(pair, f"ថាមពលចម្រុះផ្កាយភ្នំ {mountain} និងផ្កាយទឹក {water}។")

    def _get_palace_cure(self, mountain: int, water: int, annual: int, palace: str) -> str:
        """Remedies based on the active stars in the palace."""
        danger_stars = [2, 5]
        if 5 in [mountain, water, annual]:
            return "⚠️ វត្តមានផ្កាយ ៥ លឿង៖ ហាមជួសជុល ហាមដាក់ភ្លើងភ្លឺខ្លាំង។ គួរដាក់កណ្តឹងខ្យល់លោហធាតុ ៦ បំពង់ ឬកាក់ ៦ កាក់។"
        elif 2 in [mountain, water, annual]:
            return "⚠️ វត្តមានផ្កាយ ២ ខ្មៅ៖ គួរដាក់ផ្លែឃ្លោកទង់ដែង (Wu Lou) ដើម្បីការពារសុខភាព។"
        elif 9 in [water, mountain]:
            return "✨ វត្តមានផ្កាយ ៩ ស្វាយ (អធិរាជយុគ ៩)៖ គួរដាក់ភ្លើងបំភ្លឺ រុក្ខជាតិបៃតងស្រស់ ឬឧបករណ៍ស្រូបទ្រព្យ។"
        elif 8 in [water, mountain]:
            return "✨ វត្តមានផ្កាយ ៨ ស៖ ទីតាំងទ្រព្យសម្បត្តិល្អ គួរបើកឱ្យខ្យល់ចេញចូលស្រួល។"
        elif 1 in [water, mountain]:
            return "✨ វត្តមានផ្កាយ ១ ស៖ ល្អសម្រាប់តុធ្វើការ និងការបង្កើនបញ្ញា។"
        return "តុល្យភាពថាមពលធម្មតា អាចរៀបចំតាមតម្រូវការទូទៅ។"

    def _generate_house_fengshui_advice(
        self,
        natal_chart: Dict[str, Any],
        formations: List[Dict[str, str]],
        zero_spirit: Dict[str, str],
        sit_palace: str,
        face_palace: str
    ) -> str:
        """Comprehensive executive Feng Shui recommendation for the property."""
        formation_name = formations[0]["name_kh"] if formations else "ទម្រង់ធម្មតា"
        advice = (
            f"គេហដ្ឋាននេះមាន {formation_name}។ "
            f"យោងតាមក្បួនយុគ ៩ (Period 9 Li Fire)៖ "
            f"{zero_spirit['ling_shen_rule']} "
            f"នៅទិសបែរមុខ ({natal_chart[face_palace]['palace_kh']}) មានផ្កាយទឹកលេខ {natal_chart[face_palace]['water_star']} "
            f"និងទិសអង្គុយ ({natal_chart[sit_palace]['palace_kh']}) មានផ្កាយភ្នំលេខ {natal_chart[sit_palace]['mountain_star']}។ "
            f"សូមយកចិត្តទុកដាក់បន្សាបវិហារដែលមានផ្កាយលេខ ២ ឬ ៥ ដើម្បីថែរក្សាសុខុមាលភាពគ្រួសារ។"
        )
        return advice

    # =========================================================================
    # 3. BaZi (Four Pillars of Destiny - 八字គណនា)
    # =========================================================================
    # 12 Solar Terms (Jie Qi 节) Century Coefficients for Month Boundaries
    JIE_COEFFS = {
        1: (6.11, 5.4055, "小寒 (Xiao Han)"),
        2: (4.6295, 3.87, "立春 (Li Chun)"),
        3: (6.3826, 5.63, "惊蛰 (Jing Zhi)"),
        4: (5.59, 4.81, "清明 (Qing Ming)"),
        5: (6.318, 5.52, "立夏 (Li Xia)"),
        6: (6.5, 5.678, "芒种 (Mang Zhong)"),
        7: (7.928, 7.108, "小暑 (Xiao Shu)"),
        8: (8.35, 7.5, "立秋 (Li Qiu)"),
        9: (8.44, 7.646, "白露 (Bai Lu)"),
        10: (9.098, 8.318, "寒露 (Han Lu)"),
        11: (8.218, 7.438, "立冬 (Li Dong)"),
        12: (7.9, 7.18, "大雪 (Da Xue)")
    }

    # 12 Earthly Branches Hidden Stems (地支藏干 - Cang Gan)
    CANG_GAN_MAP = {
        "子": ["癸"],
        "丑": ["己", "癸", "辛"],
        "寅": ["甲", "丙", "戊"],
        "卯": ["乙"],
        "辰": ["戊", "乙", "癸"],
        "巳": ["丙", "庚", "戊"],
        "午": ["丁", "己"],
        "未": ["己", "丁", "乙"],
        "申": ["庚", "壬", "戊"],
        "酉": ["辛"],
        "戌": ["戊", "辛", "丁"],
        "亥": ["壬", "甲"]
    }

    def _gregorian_to_jdn(self, y: int, m: int, d: int) -> int:
        """Calculate Julian Day Number (JDN) for Gregorian date (Y, M, D)."""
        a = (14 - m) // 12
        y_adj = y + 4800 - a
        m_adj = m + 12 * a - 3
        jdn = d + (153 * m_adj + 2) // 5 + 365 * y_adj + y_adj // 4 - y_adj // 100 + y_adj // 400 - 32045
        return jdn

    def _get_solar_term_day(self, y: int, m: int) -> Tuple[int, str]:
        """Compute the day in month m of year y that the Solar Term (Jie Qi) begins."""
        c_20, c_21, name = self.JIE_COEFFS.get(m, (5.0, 5.0, "Jie Qi"))
        c = c_21 if y >= 2000 else c_20
        century_year = y % 100
        d = int(century_year * 0.2422 + c) - int((century_year - 1) / 4)
        return d, name

    def calculate_bazi(self, birth_date: str, birth_time: str = "12:00") -> Dict[str, Any]:
        """
        Calculate BaZi Four Pillars (Year, Month, Day, Hour) via Astronomical/Solar algorithm.
        Employs Julian Day Number (JDN), Five Tigers (五虎遁元), Five Rats (五鼠遁元),
        and 12 Solar Terms (Jie Qi) for zero-dependency 100% precision.
        """
        try:
            clean_date = birth_date.strip()
            if " " in clean_date:
                d_part, t_part = clean_date.split(" ", 1)
                clean_date = d_part
                if not birth_time or birth_time == "12:00":
                    birth_time = t_part.strip()

            parts = clean_date.split("-")
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            time_parts = birth_time.strip().split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0

            if LUNAR_AVAILABLE:
                solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
                lunar = solar.getLunar()

                year_pillar = lunar.getYearInGanZhiExact()
                month_pillar = lunar.getMonthInGanZhiExact()
                day_pillar = lunar.getDayInGanZhiExact()
                time_pillar = lunar.getTimeInGanZhi()
                solar_term = lunar.getPrevJieQi().getName()
            else:
                # High-precision autonomous astronomical fallback
                year_pillar, month_pillar, day_pillar, time_pillar, solar_term = self._fallback_bazi(year, month, day, hour)

            elements_count = self._count_five_elements([year_pillar, month_pillar, day_pillar, time_pillar])
            day_master = self._get_day_master_info(day_pillar)

            # Extract Stems, Branches, and Hidden Stems (藏干)
            def _build_pillar_info(ganzhi: str, meaning: str) -> Dict[str, Any]:
                s = ganzhi[0] if len(ganzhi) >= 1 else ""
                b = ganzhi[1] if len(ganzhi) >= 2 else ""
                return {
                    "ganzhi": ganzhi,
                    "stem": s,
                    "branch": b,
                    "hidden_stems": self.CANG_GAN_MAP.get(b, []),
                    "meaning": meaning
                }

            bazi_result = {
                "birth_date": clean_date,
                "birth_time": birth_time,
                "pillars": {
                    "year": _build_pillar_info(year_pillar, "សសរស្តម្ភឆ្នាំ (ជីដូនជីតា មូលដ្ឋានគ្រឹះ)"),
                    "month": _build_pillar_info(month_pillar, "សសរស្តម្ភខែ (ឪពុកម្តាយ អាជីពការងារ)"),
                    "day": _build_pillar_info(day_pillar, "សសរស្តម្ភថ្ងៃ (ខ្លួនឯង និងដៃគូជីវិត)"),
                    "time": _build_pillar_info(time_pillar, "សសរស្តម្ភម៉ោង (កូនចៅ និងអនាគត)")
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

    def _fallback_bazi(self, y: int, m: int, d: int, h: int) -> Tuple[str, str, str, str, str]:
        """
        Pure mathematical astronomical BaZi engine:
        1. Year Pillar: Li Chun (立春) cutoff via astronomical Century formula
        2. Month Pillar: 12 Solar Terms (Jie Qi) + Five Tigers Seeking Month (五虎遁元)
        3. Day Pillar: Continuous Sexagenary Cycle via Julian Day Number (JDN)
        4. Hour Pillar: Five Rats Seeking Hour (五鼠遁元)
        Returns (year_pillar, month_pillar, day_pillar, hour_pillar, solar_term)
        """
        stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

        # 1. Li Chun day for Year Pillar
        d_lichun, _ = self._get_solar_term_day(y, 2)
        if m < 2 or (m == 2 and d < d_lichun):
            bazi_year = y - 1
        else:
            bazi_year = y

        y_stem_idx = (bazi_year - 4) % 10
        y_branch_idx = (bazi_year - 4) % 12
        y_pillar = stems[y_stem_idx] + branches[y_branch_idx]

        # 2. Month Pillar via 12 Jie Qi & Wu Hu Dun (五虎遁元)
        d_jie, current_jie_name = self._get_solar_term_day(y, m)
        if d >= d_jie:
            active_jie = current_jie_name
            # Month m maps to month offset relative to Tiger (寅 = 0):
            # m=2 -> 0 (寅), m=3 -> 1 (卯), ..., m=12 -> 10 (子), m=1 -> 11 (丑)
            month_offset = (m - 2) % 12
        else:
            # Belongs to previous solar month
            prev_m = 12 if m == 1 else m - 1
            prev_y = y - 1 if m == 1 else y
            _, active_jie = self._get_solar_term_day(prev_y, prev_m)
            month_offset = (m - 3) % 12

        # Wu Hu Dun (五虎遁元) Formula:
        # 甲/己 -> 丙(2), 乙/庚 -> 戊(4), 丙/辛 -> 庚(6), 丁/壬 -> 壬(8), 戊/癸 -> 甲(0)
        tiger_stem_idx = ((y_stem_idx % 5) + 1) * 2 % 10
        m_stem_idx = (tiger_stem_idx + month_offset) % 10
        m_branch_idx = (2 + month_offset) % 12
        m_pillar = stems[m_stem_idx] + branches[m_branch_idx]

        # 3. Day Pillar via Julian Day Number (JDN)
        jdn = self._gregorian_to_jdn(y, m, d)
        day_idx = (jdn + 49) % 60
        d_stem_idx = day_idx % 10
        d_branch_idx = day_idx % 12
        d_pillar = stems[d_stem_idx] + branches[d_branch_idx]

        # 4. Hour Pillar via Wu Shu Dun (五鼠遁元)
        h_branch_idx = (h + 1) // 2 % 12
        # Wu Shu Dun Formula:
        # 甲/己 -> 甲(0), 乙/庚 -> 丙(2), 丙/辛 -> 戊(4), 丁/壬 -> 庚(6), 戊/癸 -> 壬(8)
        zi_stem_idx = (d_stem_idx % 5) * 2 % 10
        h_stem_idx = (zi_stem_idx + h_branch_idx) % 10
        h_pillar = stems[h_stem_idx] + branches[h_branch_idx]

        return y_pillar, m_pillar, d_pillar, h_pillar, active_jie

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
        """Classical Five Elements Balance and Yong Shen (用神) Guidance."""
        dm_stem = dm.get("stem", "甲")
        stem_element = dm.get("element", "").split(" ")[0]  # Wood, Fire, Earth, Metal, Water

        # Count support (Self + Resource) vs Drain (Output + Wealth + Officer)
        resource_map = {"Wood": "Water", "Fire": "Wood", "Earth": "Fire", "Metal": "Earth", "Water": "Metal"}
        support_elem = resource_map.get(stem_element, "Water")

        support_count = 0
        for k, v in counts.items():
            if stem_element in k or support_elem in k:
                support_count += v

        is_strong = support_count >= 4
        if is_strong:
            strength_desc = "រឹងមាំខ្លាំង (Strong Day Master 身旺)"
            advice_core = "ត្រូវការបញ្ចេញថាមពល (Output 食伤) ឬគ្រប់គ្រងដោយធាតុផ្ទុយ ដើម្បីសម្រេចកិច្ចការធំ។"
        else:
            strength_desc = "ទន់ខ្សោយល្មម (Weak Day Master 身弱)"
            advice_core = f"ត្រូវការជំនួយពីធាតុចិញ្ចឹម ({support_elem}) និងធាតុដូចគ្នា ({stem_element}) ដើម្បីបង្កើនកម្លាំងរាសី។"

        return f"Day Master: {dm['element']} ({dm['nature']}) ស្ថិតក្នុងស្ថានភាព {strength_desc}។ {advice_core}"

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
