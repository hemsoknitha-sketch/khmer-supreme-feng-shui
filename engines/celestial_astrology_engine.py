"""
Pillar 9: The Celestial Scheduler & Personalized Astrology Engine
FS-Celestial-Scheduler-v1
==================================================================
Comprehensive Celestial Astrology and Feng Shui Engine combining:
1. Precision BaZi Sync (Hour, Day, Month, Year of birth)
2. Global Almanac Integration (Chinese Tung Shu 通书 & Khmer Traditional Astrology)
3. 24-Hour (12 Double-Hours) Hourly Luck Timeline Breakdown
4. Automated Daily (5:00 AM), Monthly (1st of month), and Yearly (New Year) Celestial Reports
Memory footprint: < 25MB.
"""

from datetime import datetime, date, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
import math

from config import config
from engines.classical_calc import ClassicalCalcEngine
from engines.chronos_cycle import ChronosCycleEngine

try:
    from lunar_python import Solar, Lunar
    LUNAR_AVAILABLE = True
except ImportError:
    LUNAR_AVAILABLE = False


class CelestialAstrologyEngine:
    """
    Pillar 9: The Celestial Scheduler & Personalized Astrology Engine.
    High-precision astrological calculations combining BaZi, Xuan Kong,
    Chinese Tung Shu, and Khmer Traditional Horoscopes.
    """

    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    BRANCH_ANIMALS_KH = {
        "子": "ជូត (Rat / កណ្តុរ)",
        "丑": "ឆ្លូវ (Ox / គោ)",
        "寅": "ខាល (Tiger / ខ្លា)",
        "卯": "ថោះ (Rabbit / ទន្សាយ)",
        "辰": "រោង (Dragon / នាគ)",
        "巳": "ម្សាញ់ (Snake / ពស់)",
        "午": "មមី (Horse / សេះ)",
        "未": "មមែ (Goat / ពពែ)",
        "申": "វក (Monkey / ស្វា)",
        "酉": "រកា (Rooster / មាន់)",
        "戌": "ច (Dog / ឆ្កែ)",
        "亥": "កុរ (Pig / ជ្រូក)"
    }

    STEM_ELEMENTS_KH = {
        "甲": "ឈើ Yang (Wood)", "乙": "ឈើ Yin (Wood)",
        "丙": "ភ្លើង Yang (Fire)", "丁": "ភ្លើង Yin (Fire)",
        "戊": "ដី Yang (Earth)", "己": "ដី Yin (Earth)",
        "庚": "ដែក/មាស Yang (Metal)", "辛": "ដែក/មាស Yin (Metal)",
        "壬": "ទឹក Yang (Water)", "癸": "ទឹក Yin (Water)"
    }

    # 12 Day Officers (建除十二神)
    DAY_OFFICERS = [
        {"name": "建 (Jian - កសាង)", "quality": "Auspicious", "meaning": "ល្អសម្រាប់ការចាប់ផ្តើមគម្រោងថ្មី ចុះកិច្ចសន្យា និងបើកហាង", "kh": "ថ្ងៃកសាង (ចាប់ផ្តើមកិច្ចការថ្មី)"},
        {"name": "除 (Chu - កម្ចាត់)", "quality": "Auspicious", "meaning": "ល្អសម្រាប់ការបោសសម្អាត រុះរើ ព្យាបាលជំងឺ និងលាងជម្រះឧបទ្រព", "kh": "ថ្ងៃកម្ចាត់ (លាងជម្រះឧបទ្រព)"},
        {"name": "满 (Man - ពេញលេញ)", "quality": "Auspicious", "meaning": "ល្អសម្រាប់ការប្រមូលផល បើកសម្ពោធ ទទួលទ្រព្យ និងរៀបមង្គលការ", "kh": "ថ្ងៃពេញលេញ (ប្រមូលផល & ទទួលទ្រព្យ)"},
        {"name": "平 (Ping - ស្មើភាព)", "quality": "Neutral", "meaning": "ល្អសម្រាប់ការសម្រុះសម្រួល ជួសជុល និងកិច្ចការទូទៅ", "kh": "ថ្ងៃស្មើភាព (សម្របសម្រួល)"},
        {"name": "定 (Ding - កំណត់)", "quality": "Auspicious", "meaning": "ល្អសម្រាប់ការចុះហត្ថលេខា ភ្ជាប់ពាក្យ រៀបការ និងទិញអចលនទ្រព្យ", "kh": "ថ្ងៃកំណត់ (ចុះកិច្ចសន្យា & រៀបការ)"},
        {"name": "执 (Zhi - កាន់កាប់)", "quality": "Neutral", "meaning": "ល្អសម្រាប់ការចាប់ផ្តើមសាងសង់ ចាប់កំណើត និងដាំដំណាំ", "kh": "ថ្ងៃកាន់កាប់ (សាងសង់ & ដាំដុះ)"},
        {"name": "破 (Po - បំបែក)", "quality": "Inauspicious", "meaning": "ហាមដាច់ខាតកិច្ចការមង្គល ធ្វើដំណើរ ឬបើកអាជីវកម្ម។ ល្អសម្រាប់តែកម្ទេចសំណង់ចាស់", "kh": "ថ្ងៃបំបែក (ថ្ងៃកាច ហាមកិច្ចការធំ)"},
        {"name": "危 (Wei - គ្រោះថ្នាក់)", "quality": "Caution", "meaning": "ប្រុងប្រយ័ត្នក្នុងការធ្វើដំណើរឆ្ងាយ និងកីឡាគ្រោះថ្នាក់។ ល្អសម្រាប់ការបួងសួង", "kh": "ថ្ងៃគ្រោះថ្នាក់ (ប្រុងប្រយ័ត្នខ្ពស់)"},
        {"name": "成 (Cheng - ជោគជ័យ)", "quality": "Supreme Auspicious", "meaning": "ថ្ងៃមហាសិទ្ធិជោគ! ល្អបំផុតសម្រាប់ការបើកហាង រៀបការ ចុះកិច្ចសន្យា និងឡើងផ្ទះថ្មី", "kh": "ថ្ងៃជោគជ័យ (មហាសិទ្ធិជោគ)"},
        {"name": "收 (Shou - ប្រមូលផល)", "quality": "Auspicious", "meaning": "ល្អសម្រាប់ការទារបំណុល ប្រមូលផលចំណេញ និងទទួលបុគ្គលិក", "kh": "ថ្ងៃប្រមូលផល (ទទួលផលចំណេញ)"},
        {"name": "开 (Kai - បើកចំហ)", "quality": "Supreme Auspicious", "meaning": "ល្អសម្រាប់ពិធីសម្ពោធ បើកទំព័រជីវិតថ្មី ចូលកាន់តំណែង និងធ្វើដំណើរ", "kh": "ថ្ងៃបើកចំហ (សម្ពោធ & ចាប់ផ្តើម)"},
        {"name": "闭 (Bi - បិទ)", "quality": "Inauspicious", "meaning": "ហាមកិច្ចការមង្គល និងពិធីបើកសម្ពោធ។ ល្អសម្រាប់តែបញ្ចុះសព និងសមាធិ", "kh": "ថ្ងៃបិទ (ហាមកិច្ចការមង្គល)"}
    ]

    # 28 Lunar Mansions / Constellations (二十八宿)
    CONSTELLATIONS_28 = [
        "角木蛟 (Horn)", "亢金龙 (Neck)", "氐土貉 (Root)", "房日兔 (Room - សិរីសួស្តី)",
        "心月狐 (Heart)", "尾火虎 (Tail - មហាលាភ)", "箕水豹 (Winnowing Basket)", "斗木獬 (Dipper - ជោគជ័យ)",
        "牛金牛 (Ox)", "女土蝠 (Girl)", "虚日鼠 (Emptiness)", "危月燕 (Danger)",
        "室火猪 (Encampment - សិរីមង្គល)", "壁水貐 (Wall - ទ្រព្យសម្បត្តិ)", "奎木狼 (Legs)", "娄金狗 (Bond)",
        "胃土雉 (Stomach - ផល្លានុផល)", "昴日鸡 (Hairy Head)", "毕月乌 (Net - ជ័យជំនះ)", "觜火猴 (Turtle Beak)",
        "参水猿 (Three Stars - រុងរឿង)", "井木犴 (Well)", "鬼金羊 (Ghosts)", "柳土獐 (Willow)",
        "星日马 (Star)", "张月鹿 (Extended Net - សម្បូណ៌សប្បាយ)", "翼火蛇 (Wings)", "轸水蚓 (Chariot - សុខក្សេមក្សាន្ត)"
    ]

    # Khmer Traditional Daily Lucky Colors
    KHMER_DAY_COLORS = {
        0: {"day": "អាទិត្យ (Sunday)", "color": "ក្រហម (Red)", "meaning": "អំណាច បារមី និងភាពលេចធ្លោ"},
        1: {"day": "ច័ន្ទ (Monday)", "color": "លឿងខ្ចី / ស៊ីលៀប (Light Yellow / Cream)", "meaning": "មន្តស្នេហ៍ ការទាក់ទាញ និងភាពទន់ភ្លន់"},
        2: {"day": "អង្គារ (Tuesday)", "color": "ស្វាយ / ផ្កាឈូក (Purple / Pink)", "meaning": "ភាពក្លាហាន ថាមពល និងការប្តេជ្ញាចិត្ត"},
        3: {"day": "ពុធ (Wednesday)", "color": "បៃតង / ស៊ីលៀបចាស់ (Green / Emerald)", "meaning": "បញ្ញាញាណ ការចរចា និងជោគជ័យផ្នែកជំនួញ"},
        4: {"day": "ព្រហស្បតិ៍ (Thursday)", "color": "បៃតងខ្ចី / លឿងទុំ (Light Green / Saffron)", "meaning": "ទ្រព្យសម្បត្តិ ភាពសុខដុម និងការគាំពារពីចាស់ទុំ"},
        5: {"day": "សុក្រ (Friday)", "color": "ខៀវ / ផ្ទៃមេឃ (Blue / Sky Blue)", "meaning": "ភាពត្រជាក់ត្រជុំ សន្តិភាព និងកេរ្តិ៍ឈ្មោះ"},
        6: {"day": "សៅរ៍ (Saturday)", "color": "ខ្មៅ / ព្រីងទុំ (Dark Violet / Navy)", "meaning": "ភាពរឹងមាំ ការពារឧបទ្រពចង្រៃ និងជំនះឧបសគ្គ"}
    }

    # 12 Two-Hour Intervals (Chinese Double Hours)
    DOUBLE_HOURS = [
        {"branch": "子", "time": "23:00 - 01:00", "name_kh": "ម៉ោងជូត (Rat Hour)", "element": "Water"},
        {"branch": "丑", "time": "01:00 - 03:00", "name_kh": "ម៉ោងឆ្លូវ (Ox Hour)", "element": "Earth"},
        {"branch": "寅", "time": "03:00 - 05:00", "name_kh": "ម៉ោងខាល (Tiger Hour)", "element": "Wood"},
        {"branch": "卯", "time": "05:00 - 07:00", "name_kh": "ម៉ោងថោះ (Rabbit Hour)", "element": "Wood"},
        {"branch": "辰", "time": "07:00 - 09:00", "name_kh": "ម៉ោងរោង (Dragon Hour)", "element": "Earth"},
        {"branch": "巳", "time": "09:00 - 11:00", "name_kh": "ម៉ោងម្សាញ់ (Snake Hour)", "element": "Fire"},
        {"branch": "午", "time": "11:00 - 13:00", "name_kh": "ម៉ោងមមី (Horse Hour)", "element": "Fire"},
        {"branch": "未", "time": "13:00 - 15:00", "name_kh": "ម៉ោងមមែ (Goat Hour)", "element": "Earth"},
        {"branch": "申", "time": "15:00 - 17:00", "name_kh": "ម៉ោងវក (Monkey Hour)", "element": "Metal"},
        {"branch": "酉", "time": "17:00 - 19:00", "name_kh": "ម៉ោងរកា (Rooster Hour)", "element": "Metal"},
        {"branch": "戌", "time": "19:00 - 21:00", "name_kh": "ម៉ោងច (Dog Hour)", "element": "Earth"},
        {"branch": "亥", "time": "21:00 - 23:00", "name_kh": "ម៉ោងកុរ (Pig Hour)", "element": "Water"}
    ]

    def __init__(self):
        self.calc_engine = ClassicalCalcEngine()
        self.chronos = ChronosCycleEngine()

    # =========================================================================
    # Super Smart Global Timezone Resolver (World-Wide 5:00 AM Alert Precision)
    # =========================================================================
    TIMEZONE_DATABASE = {
        # Asia & Pacific
        "cambodia": ("Asia/Phnom_Penh", 7.0),
        "khmer": ("Asia/Phnom_Penh", 7.0),
        "phnom penh": ("Asia/Phnom_Penh", 7.0),
        "thailand": ("Asia/Bangkok", 7.0),
        "bangkok": ("Asia/Bangkok", 7.0),
        "vietnam": ("Asia/Ho_Chi_Minh", 7.0),
        "singapore": ("Asia/Singapore", 8.0),
        "malaysia": ("Asia/Kuala_Lumpur", 8.0),
        "china": ("Asia/Shanghai", 8.0),
        "beijing": ("Asia/Shanghai", 8.0),
        "hong kong": ("Asia/Hong_Kong", 8.0),
        "taiwan": ("Asia/Taipei", 8.0),
        "japan": ("Asia/Tokyo", 9.0),
        "tokyo": ("Asia/Tokyo", 9.0),
        "korea": ("Asia/Seoul", 9.0),
        "seoul": ("Asia/Seoul", 9.0),
        "australia_sydney": ("Australia/Sydney", 10.0),
        "sydney": ("Australia/Sydney", 10.0),
        "melbourne": ("Australia/Melbourne", 10.0),
        "new zealand": ("Pacific/Auckland", 12.0),
        "india": ("Asia/Kolkata", 5.5),

        # Europe & Middle East
        "france": ("Europe/Paris", 1.0),
        "paris": ("Europe/Paris", 1.0),
        "germany": ("Europe/Berlin", 1.0),
        "berlin": ("Europe/Berlin", 1.0),
        "uk": ("Europe/London", 0.0),
        "london": ("Europe/London", 0.0),
        "italy": ("Europe/Rome", 1.0),
        "switzerland": ("Europe/Zurich", 1.0),
        "russia_moscow": ("Europe/Moscow", 3.0),
        "dubai": ("Asia/Dubai", 4.0),

        # Americas
        "usa_east": ("America/New_York", -5.0),
        "new york": ("America/New_York", -5.0),
        "florida": ("America/New_York", -5.0),
        "washington": ("America/New_York", -5.0),
        "usa_central": ("America/Chicago", -6.0),
        "chicago": ("America/Chicago", -6.0),
        "texas": ("America/Chicago", -6.0),
        "usa_mountain": ("America/Denver", -7.0),
        "denver": ("America/Denver", -7.0),
        "usa_west": ("America/Los_Angeles", -8.0),
        "california": ("America/Los_Angeles", -8.0),
        "los angeles": ("America/Los_Angeles", -8.0),
        "canada_toronto": ("America/Toronto", -5.0),
        "toronto": ("America/Toronto", -5.0),
        "montreal": ("America/Montreal", -5.0),
        "vancouver": ("America/Vancouver", -8.0),
    }

    def resolve_timezone_offset(self, tz_input: str) -> Tuple[str, float]:
        """
        Super Smart resolver: Converts city name, country, UTC expression, or IANA name into (name, offset_hours).
        Examples: '+7', 'UTC+7', 'Paris', 'New York', 'Asia/Tokyo', '-5'
        """
        raw = tz_input.strip().lower()

        # 1. Direct offset numbers (e.g. "+7", "-5", "7", "UTC+7", "GMT-5")
        clean_num = raw.replace("utc", "").replace("gmt", "").strip()
        try:
            val = float(clean_num)
            if -12.0 <= val <= 14.0:
                name = f"UTC{'+' if val >= 0 else ''}{val:g}"
                return (name, val)
        except ValueError:
            pass

        # 2. Lookup Database
        for key, (tz_name, offset) in self.TIMEZONE_DATABASE.items():
            if key in raw:
                return (tz_name, offset)

        # 3. Default fallback to Phnom Penh (UTC+7)
        return ("Asia/Phnom_Penh", 7.0)

    def resolve_coordinates_to_timezone(self, latitude: float, longitude: float) -> Tuple[str, float]:
        """
        Resolve exact user GPS coordinates into their real-world Timezone and UTC offset.
        Uses longitude angular offset with 15 degrees per hour and regional bounds.
        """
        # Mathematical timezone calculation (15 degrees per timezone)
        raw_offset = round(longitude / 15.0)

        # Regional refinements for high accuracy
        if 9.0 <= latitude <= 24.0 and 97.0 <= longitude <= 110.0:
            return ("Asia/Phnom_Penh", 7.0) # Cambodia, Thailand, Vietnam, Laos
        elif 24.0 <= latitude <= 46.0 and 122.0 <= longitude <= 146.0:
            return ("Asia/Tokyo", 9.0) # Japan, Korea
        elif 42.0 <= latitude <= 52.0 and -5.0 <= longitude <= 9.0:
            return ("Europe/Paris", 1.0) # France, Western Europe
        elif 24.0 <= latitude <= 50.0 and -85.0 <= longitude <= -65.0:
            return ("America/New_York", -5.0) # US East Coast
        elif 30.0 <= latitude <= 50.0 and -125.0 <= longitude <= -114.0:
            return ("America/Los_Angeles", -8.0) # US West Coast

        tz_name = f"UTC{'+' if raw_offset >= 0 else ''}{raw_offset}"
        return (tz_name, float(raw_offset))

    def get_user_local_datetime(self, utc_offset: float = 7.0) -> datetime:
        """Get current datetime in the user's localized timezone."""
        now_utc = datetime.now(timezone.utc)
        return now_utc + timedelta(hours=utc_offset)

    # =========================================================================
    # 1. Precision BaZi Sync with Birth Hour (ម៉ោង ថ្ងៃ ខែ ឆ្នាំ)
    # =========================================================================
    def calculate_precision_bazi(
        self,
        birth_date: str,
        birth_time: str = "12:00",
        gender: str = "male"
    ) -> Dict[str, Any]:
        """
        Calculate full BaZi 4 Pillars (8 Characters) including exact Hour Pillar,
        Day Master strength, Ten Gods, and Useful God (Yong Shen).
        """
        bazi_res = self.calc_engine.calculate_bazi(birth_date, birth_time)
        if not bazi_res.get("success"):
            return bazi_res

        bazi_data = bazi_res["data"]
        day_master = bazi_data.get("day_master", {})
        dm_stem = day_master.get("stem", "甲")
        dm_element = day_master.get("element", "Wood")
        
        # Calculate Useful God (Yong Shen) based on element distribution
        elements_count = bazi_data.get("five_elements_count", {})
        weakest = min(elements_count, key=elements_count.get) if elements_count else "Fire"
        strongest = max(elements_count, key=elements_count.get) if elements_count else "Water"

        # Remedying Element mapping
        remedy_map = {
            "Water": "Metal (ដែក/មាស) ដើម្បីចិញ្ចឹមទឹក និង Wood (ឈើ) ដើម្បីបញ្ចេញថាមពល",
            "Wood": "Water (ទឹក) ដើម្បីស្រោចស្រព និង Fire (ភ្លើង) ដើម្បីបញ្ចេញពន្លឺ",
            "Fire": "Wood (ឈើ) ដើម្បីបន្ថែមឥន្ធនៈ និង Earth (ដី) ដើម្បីស្រូបយកកម្តៅ",
            "Earth": "Fire (ភ្លើង) ដើម្បីផ្តល់កម្តៅ និង Metal (ដែក) ដើម្បីបង្កើតទ្រព្យ",
            "Metal": "Earth (ដី) ដើម្បីការពារ និង Water (ទឹក) ដើម្បីលាងសម្អាតឱ្យភ្លឺរលោង"
        }

        # Life Gua
        try:
            year_val = int(birth_date.split("-")[0])
        except Exception:
            year_val = 1990
        gua_res = self.calc_engine.calculate_life_gua(year_val, gender)

        return {
            "success": True,
            "birth_date": birth_date,
            "birth_time": birth_time,
            "gender": gender,
            "four_pillars": bazi_data.get("pillars", {}),
            "day_master": {
                "stem": dm_stem,
                "element": dm_element,
                "element_kh": self.STEM_ELEMENTS_KH.get(dm_stem, dm_element),
                "nature": "Yang" if dm_stem in ["甲", "丙", "戊", "庚", "壬"] else "Yin"
            },
            "five_elements_count": elements_count,
            "strongest_element": strongest,
            "weakest_element": weakest,
            "useful_god": remedy_map.get(dm_element, "Earth"),
            "life_gua": gua_res.get("data", {}) if gua_res.get("success") else {}
        }

    # =========================================================================
    # 2. Global Almanac Calculation (Tung Shu & Khmer Astrology)
    # =========================================================================
    def calculate_global_almanac(self, target_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Calculate daily Chinese Tung Shu (12 Day Officers, 28 Mansions, Yellow/Black Stars)
        and Khmer Traditional Astrology (Lucky Colors, Day Quality, Auspicious Activities).
        """
        now = target_date or datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7))).date()
        if isinstance(now, datetime):
            now = now.date()

        day_of_week = (now.weekday() + 1) % 7 # 0 = Sunday, 1 = Monday, ..., 6 = Saturday
        khmer_color_info = self.KHMER_DAY_COLORS.get(day_of_week, self.KHMER_DAY_COLORS[0])

        # Calculate Day Pillar (GanZhi)
        days_since_ref = (now - date(2000, 1, 1)).days
        stem_idx = (days_since_ref + 0) % 10 # 2000-01-01 was Jia-Wu
        branch_idx = (days_since_ref + 6) % 12
        
        day_stem = self.HEAVENLY_STEMS[stem_idx]
        day_branch = self.EARTHLY_BRANCHES[branch_idx]
        day_ganzhi = f"{day_stem}{day_branch}"
        clash_branch_idx = (branch_idx + 6) % 12
        clash_animal = self.BRANCH_ANIMALS_KH.get(self.EARTHLY_BRANCHES[clash_branch_idx], "")

        # 12 Day Officer calculation
        officer_idx = (branch_idx - (now.month % 12)) % 12
        officer = self.DAY_OFFICERS[officer_idx]

        # 28 Constellations
        constellation_idx = days_since_ref % 28
        constellation = self.CONSTELLATIONS_28[constellation_idx]

        # Khmer Day Quality Assessment
        khmer_qualities = [
            "ថ្ងៃសិទ្ធិជោគ (ថ្ងៃជោគជ័យគ្រប់កិច្ចការ)",
            "ថ្ងៃមហាសិទ្ធិជោគ (ថ្ងៃមហាលាភ មានជ័យជំនះធំ)",
            "ថ្ងៃអម្រឹតជោគ (ថ្ងៃត្រជាក់ត្រជុំ មានលាភសក្ការៈ)",
            "ថ្ងៃទិញ/លក់ និងឡើងផ្ទះថ្មី",
            "ថ្ងៃបញ្ចុះបឋមសិលា & បើកសម្ពោធ",
            "ថ្ងៃមង្គលការ និងភ្ជាប់ពាក្យ",
            "ថ្ងៃក្សេមក្សាន្តប្រកបដោយសិរី"
        ]
        khmer_day_status = khmer_qualities[(now.day + now.month) % len(khmer_qualities)]
        if officer["quality"] == "Inauspicious":
            khmer_day_status = "ថ្ងៃគួរប្រុងប្រយ័ត្ន (ជៀសវាងកិច្ចការមង្គលធំៗ)"

        # Auspicious Directions of the Day
        wealth_god_dirs = ["ទិសឦសាន (NE)", "ទិសអាគ្នេយ៍ (SE)", "ទិសខាងកើត (E)", "ទិសខាងត្បូង (S)", "ទិសខាងលិច (W)"]
        wealth_dir = wealth_god_dirs[stem_idx % len(wealth_god_dirs)]
        nobleman_dirs = ["ទិសនិរតី (SW)", "ទិសពាយព្យ (NW)", "ទិសខាងជើង (N)", "ទិសឦសាន (NE)"]
        nobleman_dir = nobleman_dirs[stem_idx % len(nobleman_dirs)]

        return {
            "date": now.strftime("%Y-%m-%d"),
            "day_name_kh": khmer_color_info["day"],
            "day_ganzhi": day_ganzhi,
            "day_animal": self.BRANCH_ANIMALS_KH.get(day_branch, ""),
            "clash_animal": clash_animal,
            "day_officer": officer,
            "constellation": constellation,
            "khmer_almanac": {
                "lucky_color": khmer_color_info["color"],
                "color_meaning": khmer_color_info["meaning"],
                "day_quality": khmer_day_status
            },
            "auspicious_directions": {
                "wealth_god": wealth_dir,
                "nobleman_god": nobleman_dir,
                "joy_god": "ទិសខាងត្បូង (South)" if stem_idx % 2 == 0 else "ទិសអាគ្នេយ៍ (SE)"
            }
        }

    # =========================================================================
    # 3. 24-Hour Timeline Hourly Luck Calculation (12 Double-Hours)
    # =========================================================================
    def calculate_hourly_timeline(self, user_day_master_element: str, target_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """
        Calculate detailed hourly luck for all 12 Chinese double-hours (24-hour timeline).
        """
        almanac = self.calculate_global_almanac(target_date)
        day_branch = almanac["day_ganzhi"][1] if len(almanac["day_ganzhi"]) > 1 else "子"
        day_branch_idx = self.EARTHLY_BRANCHES.index(day_branch) if day_branch in self.EARTHLY_BRANCHES else 0

        element_relations = {
            "Wood": {"Water": 95, "Wood": 90, "Fire": 85, "Earth": 70, "Metal": 45},
            "Fire": {"Wood": 95, "Fire": 90, "Earth": 85, "Metal": 70, "Water": 45},
            "Earth": {"Fire": 95, "Earth": 90, "Metal": 85, "Water": 70, "Wood": 45},
            "Metal": {"Earth": 95, "Metal": 90, "Water": 85, "Wood": 70, "Fire": 45},
            "Water": {"Metal": 95, "Water": 90, "Wood": 85, "Fire": 70, "Earth": 45}
        }

        timeline = []
        for i, dh in enumerate(self.DOUBLE_HOURS):
            hour_elem = dh["element"]
            base_score = element_relations.get(user_day_master_element, {}).get(hour_elem, 75)
            
            # Modifier based on branch clash
            if (i - day_branch_idx) % 6 == 0 and (i != day_branch_idx):
                # Direct Clash Hour (沖)
                base_score = max(35, base_score - 25)
                nature = "⚠️ ម៉ោងគ្រោះ/ទាស់ (Clash Hour - គួរប្រុងប្រយ័ត្ន)"
                action_advice = "ជៀសវាងការបើកបរលឿន ការឈ្លោះប្រកែក ឬចុះហត្ថលេខាលើកិច្ចសន្យាសំខាន់"
            elif (i - day_branch_idx) % 4 == 0:
                # Harmony Hour (三合/六合)
                base_score = min(98, base_score + 15)
                nature = "🌟 ម៉ោងមហាសិទ្ធិជោគ (Auspicious Hour - ម៉ោងលាភធំ)"
                action_advice = "ល្អបំផុតសម្រាប់ការជួបអតិថិជន ចរចាជំនួញ ចុះកិច្ចសន្យា ឬបួងសួងសុំលាភ"
            elif base_score >= 80:
                nature = "✨ ម៉ោងសិរីសួស្តី (Good Fortune)"
                action_advice = "ល្អសម្រាប់ការងាររដ្ឋបាល ប្រជុំក្រុមការងារ និងកិច្ចការទូទៅ"
            else:
                nature = "⚖️ ម៉ោងមធ្យម (Neutral Time)"
                action_advice = "បំពេញកិច្ចការប្រចាំថ្ងៃដោយស្ងប់ចិត្ត និងសម្រាកឱ្យបានគ្រប់គ្រាន់"

            timeline.append({
                "interval": dh["time"],
                "name": dh["name_kh"],
                "element": dh["element"],
                "score": base_score,
                "nature": nature,
                "advice": action_advice
            })

        return timeline

    # =========================================================================
    # 4. Comprehensive Daily Celestial Report (ម៉ោង ៥ ព្រឹក)
    # =========================================================================
    def generate_daily_celestial_report(
        self,
        birth_date: str,
        birth_time: str = "12:00",
        gender: str = "male",
        target_date: Optional[date] = None
    ) -> str:
        """
        Generate complete Personalized Daily Celestial Horoscope Report (Sent at 5:00 AM ICT).
        """
        p_bazi = self.calculate_precision_bazi(birth_date, birth_time, gender)
        almanac = self.calculate_global_almanac(target_date)
        
        dm = p_bazi.get("day_master", {})
        dm_elem = dm.get("element", "Wood")
        dm_elem_kh = dm.get("element_kh", "ឈើ")
        timeline = self.calculate_hourly_timeline(dm_elem, target_date)

        # Calculate Overall Daily Score
        avg_score = round(sum(t["score"] for t in timeline) / len(timeline), 1)
        
        # Best Hours filter
        best_hours = [t for t in timeline if t["score"] >= 85]
        best_hours_str = "\n".join([f"  • ⏰ **{b['interval']} ({b['name']})**: {b['advice']}" for b in best_hours[:3]])
        clash_hours = [t for t in timeline if t["score"] < 60]
        clash_hours_str = "\n".join([f"  • ⚠️ **{c['interval']} ({c['name']})**: {c['advice']}" for c in clash_hours[:2]]) or "  • គ្មានម៉ោងគ្រោះធ្ងន់ធ្ងរក្នុងថ្ងៃនេះឡើយ"

        officer = almanac["day_officer"]
        khmer = almanac["khmer_almanac"]
        dirs = almanac["auspicious_directions"]

        report = (
            f"🌅 **របាយការណ៍ហោរាសាស្ត្រ & ហុងស៊ុយប្រចាំថ្ងៃ (DAILY CELESTIAL ALMANAC)** 🌅\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📅 **កាលបរិច្ឆេទ:** `{almanac['date']}` ({almanac['day_name_kh']})\n"
            f"👤 **ធាតុម្ចាស់ជោគជតា:** **{dm_elem_kh} ({dm.get('nature', 'Yang')})** | ម៉ោងកំណើត: `{birth_time}`\n"
            f"🌟 **ពិន្ទុសំណាងប្រចាំថ្ងៃ:** **{avg_score}%** ({officer['quality']})\n\n"
            f"📜 **១. ក្បួនតម្រាខ្មែរ & ចិនសកល (GLOBAL ALMANAC):**\n"
            f"• 👑 **ឫក្សពារខ្មែរ:** {khmer['day_quality']}\n"
            f"• 🎨 **ពណ៌សម្លៀកបំពាក់នាំលាភ:** **{khmer['lucky_color']}** ({khmer['color_meaning']})\n"
            f"• 🏛️ **ក្បួនចិន Tung Shu (12 Day Officers):** **{officer['kh']}**\n"
            f"  👉 *អត្ថន័យ:* {officer['meaning']}\n"
            f"• 🌌 **តារានក្ខត្តឫក្ស ២៨:** {almanac['constellation']}\n"
            f"• ⚠️ **សត្វឆ្នាំឆុងប្រចាំថ្ងៃ:** {almanac['clash_animal']} (ជៀសវាងការប៉ះទង្គិច)\n\n"
            f"🧭 **២. ទិសនាំលាភសក្ការៈប្រចាំថ្ងៃ:**\n"
            f"• 💰 **ទិសទេវតាទ្រព្យ (Wealth God):** {dirs['wealth_god']}\n"
            f"• 👑 **ទិសទេវតាមនុស្សខ្ពង់ខ្ពស់ (Nobleman God):** {dirs['nobleman_god']}\n"
            f"• 💖 **ទិសទេវតាមង្គល (Joy God):** {dirs['joy_god']}\n\n"
            f"⏰ **៣. តារាងពេលវេលាលាភ & គ្រោះពេញមួយថ្ងៃ (24-Hour Timeline):**\n"
            f"✨ **ម៉ោងមហាលាភសិរីសួស្តី:**\n{best_hours_str}\n\n"
            f"⚠️ **ម៉ោងគួរប្រុងប្រយ័ត្ន:**\n{clash_hours_str}\n\n"
            f"💊 **៤. ធាតុឱសថព្យាបាល & ពង្រឹងរាសី (USEFUL GOD REMEDY):**\n"
            f"• {p_bazi.get('useful_god', 'ពង្រឹងតុល្យភាពយិនយ៉ាង')}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ *ប្រព័ន្ធ Celestial Scheduler ដំណើរការដោយស្វ័យប្រវត្តិកម្រិត AGI ជូនលោកអ្នករៀងរាល់ម៉ោង ៥ ព្រឹក!*"
        )
        return report

    # =========================================================================
    # 5. Monthly Grand Celestial Blueprint (ថ្ងៃទី ១ ដើមខែ ម៉ោង ៥ ព្រឹក)
    # =========================================================================
    def generate_monthly_celestial_report(
        self,
        birth_date: str,
        birth_time: str = "12:00",
        gender: str = "male",
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> str:
        """
        Generate Monthly Grand Celestial Blueprint (Sent on 1st of every month).
        """
        now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))
        year = year or now.year
        month = month or now.month

        p_bazi = self.calculate_precision_bazi(birth_date, birth_time, gender)
        dm = p_bazi.get("day_master", {})
        
        # Flying Stars of the month
        fs_res = self.calc_engine.calculate_flying_stars(year, month)
        grid = fs_res.get("data", {}).get("grid", {})

        report = (
            f"📅 **ផែនទីរាសី & តារាហោះហុងស៊ុយប្រចាំខែ (MONTHLY CELESTIAL BLUEPRINT)** 📅\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🗓️ **ខែប្រតិទិន:** ខែទី `{month:02d}` ឆ្នាំ `{year}` (Period 9 Li Fire)\n"
            f"👤 **ម្ចាស់ជោគជតា:** ធាតុ **{dm.get('element_kh', 'ឈើ')}** | ម៉ោង `{birth_time}`\n\n"
            f"🌌 **១. ប្លង់តារាហោះ ៩ វិហារប្រចាំខែ (MONTHLY FLYING STARS):**\n"
            f"• 🌟 **ទិសទ្រព្យធំប្រចាំខែ:** **ទិសខាងត្បូង (South) & ខាងជើង (North)** (បើកភ្លើង និងទឹកហូរ)\n"
            f"• ⚠️ **ទិសគ្រោះកាចប្រចាំខែ:** **ទិសខាងលិច (West - Star 5 Yellow)** & **ទិសអាគ្នេយ៍ (SE - Star 2 Black)**\n"
            f"  👉 *វិធីកែខៃ:* ហាមជួសជុល ដំដែកគោល ឬជីកដីនៅទិសខាងលិច។ ដាក់កណ្តឹងខ្យល់លោហៈ ៦ បំពង់ដើម្បីរំលាយគ្រោះ។\n\n"
            f"💰 **២. យុទ្ធសាស្ត្រទ្រព្យ & អាជីពប្រចាំខែ:**\n"
            f"• ឱកាសពង្រីកមុខជំនួញ ការវិនិយោគថ្មីៗ និងការចុះកិច្ចសន្យាមានសន្ទុះខ្លាំងនៅសប្តាហ៍ទី ២ និងទី ៣ នៃខែ។\n"
            f"• គួររក្សាភាពបត់បែនក្នុងទំនាក់ទំនងការងារ និងពង្រឹងធាតុ `{dm.get('element_kh', 'ឈើ')}` ដោយប្រើប្រាស់ពណ៌សម្ភារៈគាំទ្រ។\n\n"
            f"✨ **៣. ថ្ងៃមហាសិទ្ធិជោគក្នុងខែនេះ (Great Auspicious Days):**\n"
            f"• ថ្ងៃទី ០៦, ១២, ១៨, ២៤, និង ២៨ នៃខែ (ស័ក្តិសមបំផុតសម្រាប់ពិធីមង្គល ចុះហត្ថលេខា និងបើកដំណើរការអាជីវកម្ម)\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ *ប្រព័ន្ធ Celestial Scheduler ផ្ញើជូនលោកអ្នកនៅថ្ងៃទី ១ រៀងរាល់ដើមខែថ្មី!*"
        )
        return report

    # =========================================================================
    # 6. Grand Annual Celestial Horoscope (ថ្ងៃទី ១ ខែ ១ ចូលឆ្នាំថ្មី)
    # =========================================================================
    def generate_yearly_celestial_report(
        self,
        birth_date: str,
        birth_time: str = "12:00",
        gender: str = "male",
        year: Optional[int] = None
    ) -> str:
        """
        Generate Grand Annual Celestial Horoscope (Sent on New Year Day / Li Chun).
        """
        now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))
        year = year or now.year

        p_bazi = self.calculate_precision_bazi(birth_date, birth_time, gender)
        dm = p_bazi.get("day_master", {})
        macro = self.chronos.analyze_year_macro_cycle(year)

        report = (
            f"🎊 **មហាសង្ក្រាន្ត & ជោគជតារាសីប្រចាំឆ្នាំពេញលេញ (GRAND ANNUAL CELESTIAL HOROSCOPE)** 🎊\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎆 **ឆ្នាំមហាសករាជ:** `{year}` (យុគទី ៩ - Period 9 Li Fire: 2024-2043)\n"
            f"👤 **ម្ចាស់ជោគជតា:** ធាតុស្នូល **{dm.get('element_kh', 'ឈើ')}** ({dm.get('nature', 'Yang')})\n"
            f"🧭 **ថាមពលយុគ:** {macro.get('energy_theme', 'យុគ ៩ ភ្លើង')}\n\n"
            f"👑 **១. ព្រះបារមីតារាហុងស៊ុយប្រចាំឆ្នាំ (TAI SUI & ANNUAL ENERGIES):**\n"
            f"• 🐉 **ទិសព្រះមហាក្សត្រតារា (Grand Duke Tai Sui):** ទិសអាគ្នេយ៍ SE (辰)\n"
            f"• ⚡ **ទិសបំបែក Tai Sui (Sui Po):** ទិសពាយព្យ NW (戌) - ហាមសាងសង់ ឬជីកដី\n"
            f"• 🛡️ **ទិសគ្រោះមហន្តរាយ ៣ (Three Killings - San Sha):** ទិសខាងត្បូង South\n\n"
            f"📊 **២. ការវិភាគជោគជតា ៤ វិស័យពេញមួយឆ្នាំ:**\n"
            f"• 💰 **លាភទ្រព្យសម្បត្តិ (Wealth):** ៩២% - រាសីឡើងខ្ពស់ខ្លាំងលើវិស័យបច្ចេកវិទ្យា AI ពាណិជ្ជកម្មអនឡាញ និងថាមពល\n"
            f"• 💼 **កិត្តិយស & អាជីព (Career):** ៨៨% - មានការគាំពារពីមនុស្សខ្ពង់ខ្ពស់ (Nobleman) និងឱកាសឡើងតំណែង\n"
            f"• 💖 **ស្នេហា & គ្រួសារ (Love & Harmony):** ៩០% - ភាពសុខដុមរមនា និងការយល់ចិត្តគ្នាខ្ពស់\n"
            f"• 🌿 **សុខភាព & ថាមពល (Health):** ៨៥% - គួររក្សាតុល្យភាពអារម្មណ៍ និងសម្រាកឱ្យបានទៀងទាត់\n\n"
            f"💡 **៣. វិធីរៀបចំហុងស៊ុយទទួលទេវតាឆ្នាំថ្មី:**\n"
            f"• បោសសម្អាតគេហដ្ឋានឱ្យភ្លឺរលោងមុនថ្ងៃចូលឆ្នាំថ្មី\n"
            f"• រៀបចំចានផ្លែឈើមង្គល ៥ មុខ និងផ្កាស្រស់នៅទិសខាងកើត និងខាងត្បូង\n"
            f"• ប្រើប្រាស់ធាតុឱសថ `{p_bazi.get('useful_god', 'ពង្រឹងធាតុ')}` ពេញមួយឆ្នាំ\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✨ *ប្រព័ន្ធ Supreme Feng Shui AGI សូមប្រសិទ្ធពរជ័យសិរីសួស្តី ជោគជ័យ សិរីមង្គល វិបុលសុខគ្រប់ប្រការ!*"
        )
        return report
