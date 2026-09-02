"""
Pillar 9: The Celestial Scheduler & Personalized Astrology Engine
FS-Celestial-Scheduler-v1
==================================================================
Comprehensive Celestial Astrology and Feng Shui Engine combining:
1. Precision BaZi Sync (Hour, Day, Month, Year of birth)
2. Global Almanac Integration (Chinese Tung Shu & Khmer Traditional Astrology)
3. 24-Hour (12 Double-Hours) Hourly Luck Timeline Breakdown
4. Automated Daily (5:00 AM), Monthly (1st of month), and Yearly (New Year) In-Depth Celestial Treatises (3,500 - 4,000 characters)
Memory footprint: < 25MB.
"""

from datetime import datetime, date, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
import math
import re

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
        "子": "ឆ្នាំជូត (កណ្តុរ)",
        "丑": "ឆ្នាំឆ្លូវ (គោ)",
        "寅": "ឆ្នាំខាល (ខ្លា)",
        "卯": "ឆ្នាំថោះ (ទន្សាយ)",
        "辰": "ឆ្នាំរោង (នាគ)",
        "巳": "ឆ្នាំម្សាញ់ (ពស់)",
        "午": "ឆ្នាំមមី (សេះ)",
        "未": "ឆ្នាំមមែ (ពពែ)",
        "申": "ឆ្នាំវក (ស្វា)",
        "酉": "ឆ្នាំរកា (មាន់)",
        "戌": "ឆ្នាំច (ឆ្កែ)",
        "亥": "ឆ្នាំកុរ (ជ្រូក)"
    }

    STEM_ELEMENTS_KH = {
        "甲": "ឈើ យ៉ាង", "乙": "ឈើ យីន",
        "丙": "ភ្លើង យ៉ាង", "丁": "ភ្លើង យីន",
        "戊": "ដី យ៉ាង", "己": "ដី យីន",
        "庚": "ដែក យ៉ាង", "辛": "ដែក យីន",
        "壬": "ទឹក យ៉ាង", "癸": "ទឹក យីន"
    }

    ELEMENT_NAMES_KH = {
        "Wood": "ធាតុឈើ",
        "Fire": "ធាតុភ្លើង",
        "Earth": "ធាតុដី",
        "Metal": "ធាតុដែក",
        "Water": "ធាតុទឹក"
    }

    # 12 Day Officers (建除十二神) in pure elegant Khmer
    DAY_OFFICERS_KH = [
        {"name": "ថ្ងៃកសាង", "quality_kh": "ថ្ងៃសិរីសួស្តី", "meaning": "ល្អសម្រាប់ការចាប់ផ្តើមគម្រោងថ្មី ចុះកិច្ចសន្យា និងបើកហាង", "detail": "ថាមពលមេឃដីកំពុងកកើតថ្មី ស័ក្តិសមបំផុតសម្រាប់ការបញ្ចុះបឋមសិលា ចាប់ផ្តើមអាជីវកម្ម ឬចុះហត្ថលេខាលើកិច្ចព្រមព្រៀងសំខាន់ៗ។"},
        {"name": "ថ្ងៃកម្ចាត់", "quality_kh": "ថ្ងៃសិរីសួស្តី", "meaning": "ល្អសម្រាប់ការបោសសម្អាត រុះរើ ព្យាបាលជំងឺ និងលាងជម្រះឧបទ្រព", "detail": "ថាមពលជួយរំលាយរឿងចាស់ៗមិនល្អ ស័ក្តិសមសម្រាប់ការសម្អាតផ្ទះ រុះរើកន្លែងចាស់ ព្យាបាលជំងឺ និងកាត់ផ្តាច់រឿងសៅហ្មង។"},
        {"name": "ថ្ងៃពេញលេញ", "quality_kh": "ថ្ងៃមហាសិទ្ធិជោគ", "meaning": "ល្អសម្រាប់ការប្រមូលផល បើកសម្ពោធ ទទួលទ្រព្យ និងរៀបមង្គលការ", "detail": "ថាមពលទ្រព្យពេញបរិបូរណ៍ ស័ក្តិសមសម្រាប់ការប្រមូលផលចំណេញ បើកសម្ពោធសាខាថ្មី រៀបមង្គលការ និងទទួលផលវិនិយោគ។"},
        {"name": "ថ្ងៃស្មើភាព", "quality_kh": "ថ្ងៃមធ្យម", "meaning": "ល្អសម្រាប់ការសម្រុះសម្រួល ជួសជុល និងកិច្ចការទូទៅ", "detail": "ថាមពលមានតុល្យភាពស្មើគ្នា ល្អសម្រាប់ការចរចាសម្រុះសម្រួលទំនាស់ ជួសជុលគេហដ្ឋាន និងការងាររដ្ឋបាលប្រចាំថ្ងៃ។"},
        {"name": "ថ្ងៃកំណត់", "quality_kh": "ថ្ងៃសិរីសួស្តី", "meaning": "ល្អសម្រាប់ការចុះហត្ថលេខា ភ្ជាប់ពាក្យ រៀបការ និងទិញអចលនទ្រព្យ", "detail": "ថាមពលមានស្ថិរភាពរឹងមាំយូរអង្វែង ល្អសម្រាប់កិច្ចសន្យារយៈពេលវែង ការភ្ជាប់ពាក្យ អាពាហ៍ពិពាហ៍ និងការទិញដីធ្លីផ្ទះសម្បែង។"},
        {"name": "ថ្ងៃកាន់កាប់", "quality_kh": "ថ្ងៃមធ្យម", "meaning": "ល្អសម្រាប់ការចាប់ផ្តើមសាងសង់ ចាប់កំណើត និងដាំដំណាំ", "detail": "ថាមពលរក្សាទ្រព្យ និងថែរក្សាកេរដំណែល ល្អសម្រាប់ការចាប់ផ្តើមការងារកសិកម្ម សាងសង់ និងការប្រគល់ភារកិច្ច។"},
        {"name": "ថ្ងៃបំបែក", "quality_kh": "ថ្ងៃគួរប្រុងប្រយ័ត្ន", "meaning": "ហាមដាច់ខាតកិច្ចការមង្គល ធ្វើដំណើរ ឬបើកអាជីវកម្ម។ ល្អសម្រាប់តែកម្ទេចសំណង់ចាស់", "detail": "ថាមពលបែកបាក់ និងប៉ះទង្គិច ត្រូវជៀសវាងពិធីមង្គល ការចុះហត្ថលេខា និងការធ្វើដំណើរឆ្ងាយ។ ល្អសម្រាប់តែកម្ទេចសំណង់ចាស់ៗចោល។"},
        {"name": "ថ្ងៃគ្រោះថ្នាក់", "quality_kh": "ថ្ងៃគួរប្រុងប្រយ័ត្ន", "meaning": "ប្រុងប្រយ័ត្នក្នុងការធ្វើដំណើរឆ្ងាយ និងកីឡាគ្រោះថ្នាក់។ ល្អសម្រាប់ការបួងសួង", "detail": "ថាមពលមិនទាន់នឹងនរ គួរប្រយ័ត្នក្នុងការបើកបរ និងការសម្រេចចិត្តហិរញ្ញវត្ថុប្រថុយប្រថាន។ ស័ក្តិសមសម្រាប់ការធ្វើសមាធិ និងបួងសួងសុំសេចក្តីសុខ។"},
        {"name": "ថ្ងៃជោគជ័យ", "quality_kh": "ថ្ងៃមហាសិទ្ធិជោគកំពូល", "meaning": "ថ្ងៃមហាសិទ្ធិជោគ! ល្អបំផុតសម្រាប់ការបើកហាង រៀបការ ចុះកិច្ចសន្យា និងឡើងផ្ទះថ្មី", "detail": "ថាមពលជោគជ័យពេញទំហឹង ធ្វើកិច្ចការអ្វីក៏ទទួលបានផលល្អហួសពីការស្មាន ទាំងទ្រព្យសម្បត្តិ កិត្តិយស និងសុភមង្គល។"},
        {"name": "ថ្ងៃប្រមូលផល", "quality_kh": "ថ្ងៃសិរីសួស្តី", "meaning": "ល្អសម្រាប់ការទារបំណុល ប្រមូលផលចំណេញ និងទទួលបុគ្គលិក", "detail": "ថាមពលច្រូតកាត់ផលលាភ ល្អសម្រាប់ការទារបំណុល ប្រមូលប្រាក់ចំណេញ ទទួលបុគ្គលិកថ្មី និងការចូលកាន់កាប់ទ្រព្យសម្បត្តិ។"},
        {"name": "ថ្ងៃបើកចំហ", "quality_kh": "ថ្ងៃមហាសិទ្ធិជោគកំពូល", "meaning": "ល្អសម្រាប់ពិធីសម្ពោធ បើកទំព័រជីវិតថ្មី ចូលកាន់តំណែង និងធ្វើដំណើរ", "detail": "ថាមពលទ្វារមេឃបើកចំហទទួលលាភ ស័ក្តិសមបំផុតសម្រាប់ពិធីសម្ពោធ បើកហាងថ្មី ឡើងកាន់តំណែង ការចេញដំណើរទៅក្រៅប្រទេស និងការរៀនសូត្រ។"},
        {"name": "ថ្ងៃបិទ", "quality_kh": "ថ្ងៃគួរប្រុងប្រយ័ត្ន", "meaning": "ហាមកិច្ចការមង្គល និងពិធីបើកសម្ពោធ។ ល្អសម្រាប់តែការបញ្ចុះសព និងការធ្វើសមាធិ", "detail": "ថាមពលស្រូបទាញចូលក្នុង ហាមដាច់ខាតការបើកសម្ពោធ និងពិធីមង្គលនានា។ ល្អសម្រាប់ការសម្រាក សមាធិ និងការបិទបញ្ជីគណនេយ្យ។"}
    ]

    # 28 Lunar Mansions / Constellations in pure Khmer
    CONSTELLATIONS_28_KH = [
        "តារាកុកម៉ុកកៀវ (ផ្កាយកសាងកិត្តិយស)", "តារាកាងជីងឡុង (ផ្កាយទ្រព្យសម្បត្តិ)", "តារាតីធូហ័រ (ផ្កាយស្ថិរភាព)", "តារាហ្វាងរីធូ (ផ្កាយសិរីសួស្តី)",
        "តារាស៊ីនយៀកហ៊ូ (ផ្កាយបញ្ញាញាណ)", "តារាវេយហ័រហ៊ូ (ផ្កាយមហាលាភធំ)", "តារាជីស៊ុយប៉ោ (ផ្កាយប្រមូលផល)", "តារាតូវម៉ុកសៀ (ផ្កាយជ័យជំនះ)",
        "តារានីវជីងនីវ (ផ្កាយការងាររឹងមាំ)", "តារានីវធូប៉ា (ផ្កាយសុខដុមរមនា)", "តារាស៊ូជីស៊ូ (ផ្កាយសមាធិផ្លូវចិត្ត)", "តារាវេយយៀកយ៉េន (ផ្កាយប្រុងប្រយ័ត្ន)",
        "តារាស៊ីហ័រជូ (ផ្កាយសិរីមង្គល)", "តារាប៊ីស៊ុយយូ (ផ្កាយឃ្លាំងទ្រព្យ)", "តារាគុយម៉ុកឡាង (ផ្កាយចំណេះដឹង)", "តារាឡូវជីងកូវ (ផ្កាយមិត្តភាព)",
        "តារាវេយធូជី (ផ្កាយផល្លានុផល)", "តារាម៉ៅរីជី (ផ្កាយភាពឧស្សាហ៍)", "តារាប៊ីយៀកអ៊ូ (ផ្កាយជោគជ័យ)", "តារាជួយហ័រហូវ (ផ្កាយចរចា)",
        "តារាសេនស៊ុយយួន (ផ្កាយរុងរឿងថ្កុំថ្កើង)", "តារាជីងម៉ុកអាន (ផ្កាយទ្រព្យត្រជាក់ត្រជុំ)", "តារាគួយជីនយ៉ាង (ផ្កាយការពារឧបទ្រព)", "តារាលីវធូយ៉ាង (ផ្កាយបត់បែន)",
        "តារាស៊ីងរីម៉ា (ផ្កាយកិត្តិនាម)", "តារាចាងយៀកលូ (ផ្កាយសម្បូណ៌សប្បាយ)", "តារាអ៊ីហ័រសឺ (ផ្កាយការពារសន្តិភាព)", "តារាចិនស៊ុយអ៊ីន (ផ្កាយសុខក្សេមក្សាន្ត)"
    ]

    # Khmer Traditional Daily Lucky Colors
    KHMER_DAY_COLORS = {
        0: {"day": "ថ្ងៃអាទិត្យ", "color": "ពណ៌ក្រហម", "meaning": "អំណាច បារមី និងភាពលេចធ្លោ"},
        1: {"day": "ថ្ងៃច័ន្ទ", "color": "ពណ៌លឿងខ្ចី ឬពណ៌ស៊ីលៀប", "meaning": "មន្តស្នេហ៍ ការទាក់ទាញ និងភាពទន់ភ្លន់"},
        2: {"day": "ថ្ងៃអង្គារ", "color": "ពណ៌ស្វាយ ឬពណ៌ផ្កាឈូក", "meaning": "ភាពក្លាហាន ថាមពល និងការប្តេជ្ញាចិត្ត"},
        3: {"day": "ថ្ងៃពុធ", "color": "ពណ៌បៃតង ឬពណ៌ស៊ីលៀបចាស់", "meaning": "បញ្ញាញាណ ការចរចា និងជោគជ័យផ្នែកជំនួញ"},
        4: {"day": "ថ្ងៃព្រហស្បតិ៍", "color": "ពណ៌បៃតងខ្ចី ឬពណ៌លឿងទុំ", "meaning": "ទ្រព្យសម្បត្តិ ភាពសុខដុម និងការគាំពារពីចាស់ទុំ"},
        5: {"day": "ថ្ងៃសុក្រ", "color": "ពណ៌ខៀវ ឬពណ៌ផ្ទៃមេឃ", "meaning": "ភាពត្រជាក់ត្រជុំ សន្តិភាព និងកេរ្តិ៍ឈ្មោះ"},
        6: {"day": "ថ្ងៃសៅរ៍", "color": "ពណ៌ខ្មៅ ឬពណ៌ស្វាយព្រីងទុំ", "meaning": "ភាពរឹងមាំ ការពារឧបទ្រពចង្រៃ និងជំនះឧបសគ្គ"}
    }

    # 12 Two-Hour Intervals
    DOUBLE_HOURS = [
        {"branch": "子", "time": "23:00 - 01:00", "name_kh": "ម៉ោងជូត (ម៉ោងកណ្តុរ)", "element": "Water", "element_kh": "ធាតុទឹក"},
        {"branch": "丑", "time": "01:00 - 03:00", "name_kh": "ម៉ោងឆ្លូវ (ម៉ោងគោ)", "element": "Earth", "element_kh": "ធាតុដី"},
        {"branch": "寅", "time": "03:00 - 05:00", "name_kh": "ម៉ោងខាល (ម៉ោងខ្លា)", "element": "Wood", "element_kh": "ធាតុឈើ"},
        {"branch": "卯", "time": "05:00 - 07:00", "name_kh": "ម៉ោងថោះ (ម៉ោងទន្សាយ)", "element": "Wood", "element_kh": "ធាតុឈើ"},
        {"branch": "辰", "time": "07:00 - 09:00", "name_kh": "ម៉ោងរោង (ម៉ោងនាគ)", "element": "Earth", "element_kh": "ធាតុដី"},
        {"branch": "巳", "time": "09:00 - 11:00", "name_kh": "ម៉ោងម្សាញ់ (ម៉ោងពស់)", "element": "Fire", "element_kh": "ធាតុភ្លើង"},
        {"branch": "午", "time": "11:00 - 13:00", "name_kh": "ម៉ោងមមី (ម៉ោងសេះ)", "element": "Fire", "element_kh": "ធាតុភ្លើង"},
        {"branch": "未", "time": "13:00 - 15:00", "name_kh": "ម៉ោងមមែ (ម៉ោងពពែ)", "element": "Earth", "element_kh": "ធាតុដី"},
        {"branch": "申", "time": "15:00 - 17:00", "name_kh": "ម៉ោងវក (ម៉ោងស្វា)", "element": "Metal", "element_kh": "ធាតុដែក"},
        {"branch": "酉", "time": "17:00 - 19:00", "name_kh": "ម៉ោងរកា (ម៉ោងមាន់)", "element": "Metal", "element_kh": "ធាតុដែក"},
        {"branch": "戌", "time": "19:00 - 21:00", "name_kh": "ម៉ោងច (ម៉ោងឆ្កែ)", "element": "Earth", "element_kh": "ធាតុដី"},
        {"branch": "亥", "time": "21:00 - 23:00", "name_kh": "ម៉ោងកុរ (ម៉ោងជ្រូក)", "element": "Water", "element_kh": "ធាតុទឹក"}
    ]

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

    def __init__(self):
        self.calc_engine = ClassicalCalcEngine()
        self.chronos = ChronosCycleEngine()

    def resolve_timezone_offset(self, tz_input: str) -> Tuple[str, float]:
        """
        Convert city name, country, UTC expression, or IANA name into (name, offset_hours).
        """
        raw = tz_input.strip().lower()
        clean_num = raw.replace("utc", "").replace("gmt", "").strip()
        try:
            val = float(clean_num)
            if -12.0 <= val <= 14.0:
                name = f"UTC{'+' if val >= 0 else ''}{val:g}"
                return (name, val)
        except ValueError:
            pass

        for key, (tz_name, offset) in self.TIMEZONE_DATABASE.items():
            if key in raw:
                return (tz_name, offset)

        return ("Asia/Phnom_Penh", 7.0)

    def resolve_coordinates_to_timezone(self, latitude: float, longitude: float) -> Tuple[str, float]:
        """
        Resolve exact user GPS coordinates into their real-world Timezone and UTC offset.
        """
        raw_offset = round(longitude / 15.0)

        if 9.0 <= latitude <= 24.0 and 97.0 <= longitude <= 110.0:
            return ("Asia/Phnom_Penh", 7.0)
        elif 24.0 <= latitude <= 46.0 and 122.0 <= longitude <= 146.0:
            return ("Asia/Tokyo", 9.0)
        elif 42.0 <= latitude <= 52.0 and -5.0 <= longitude <= 9.0:
            return ("Europe/Paris", 1.0)
        elif 24.0 <= latitude <= 50.0 and -85.0 <= longitude <= -65.0:
            return ("America/New_York", -5.0)
        elif 30.0 <= latitude <= 50.0 and -125.0 <= longitude <= -114.0:
            return ("America/Los_Angeles", -8.0)

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
        bazi_res = self.calc_engine.calculate_bazi(f"{birth_date} {birth_time}")
        if not bazi_res.get("success"):
            return bazi_res

        bazi_data = bazi_res["data"]
        day_master = bazi_data.get("day_master", {})
        dm_stem = day_master.get("stem", "甲")
        dm_element = day_master.get("element", "Wood")
        
        elements_count = bazi_data.get("five_elements_count", {})
        weakest = min(elements_count, key=elements_count.get) if elements_count else "Fire"
        strongest = max(elements_count, key=elements_count.get) if elements_count else "Water"

        remedy_map = {
            "Water": "ធាតុដែកដើម្បីចិញ្ចឹមធាតុទឹក និងធាតុឈើដើម្បីបញ្ចេញថាមពលនិងបញ្ញា",
            "Wood": "ធាតុទឹកដើម្បីស្រោចស្រពចិញ្ចឹម និងធាតុភ្លើងដើម្បីបញ្ចេញពន្លឺនិងភាពលេចធ្លោ",
            "Fire": "ធាតុឈើដើម្បីបន្ថែមឥន្ធនៈទ្រទ្រង់ និងធាតុដីដើម្បីស្រូបយកតុល្យភាពកម្តៅ",
            "Earth": "ធាតុភ្លើងដើម្បីផ្តល់កម្តៅចិញ្ចឹម និងធាតុដែកដើម្បីបង្កើតភោគទ្រព្យសម្បត្តិ",
            "Metal": "ធាតុដីដើម្បីការពារនិងពង្រឹង និងធាតុទឹកដើម្បីលាងសម្អាតឱ្យភ្លឺរលោងចែងចាំង"
        }

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
                "nature_kh": "យ៉ាង" if dm_stem in ["甲", "丙", "戊", "庚", "壬"] else "យីន"
            },
            "five_elements_count": elements_count,
            "strongest_element": strongest,
            "weakest_element": weakest,
            "useful_god": remedy_map.get(dm_element, "តុល្យភាពធាតុទាំង ៥ ក្នុងខ្លួន"),
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

        day_of_week = (now.weekday() + 1) % 7
        khmer_color_info = self.KHMER_DAY_COLORS.get(day_of_week, self.KHMER_DAY_COLORS[0])

        days_since_ref = (now - date(2000, 1, 1)).days
        stem_idx = (days_since_ref + 0) % 10
        branch_idx = (days_since_ref + 6) % 12
        
        day_stem = self.HEAVENLY_STEMS[stem_idx]
        day_branch = self.EARTHLY_BRANCHES[branch_idx]
        day_ganzhi = f"{day_stem}{day_branch}"
        clash_branch_idx = (branch_idx + 6) % 12
        clash_animal = self.BRANCH_ANIMALS_KH.get(self.EARTHLY_BRANCHES[clash_branch_idx], "")

        officer_idx = (branch_idx - (now.month % 12)) % 12
        officer = self.DAY_OFFICERS_KH[officer_idx]

        constellation_idx = days_since_ref % 28
        constellation = self.CONSTELLATIONS_28_KH[constellation_idx]

        khmer_qualities = [
            "ថ្ងៃសិទ្ធិជោគ (ថ្ងៃជោគជ័យគ្រប់កិច្ចការ)",
            "ថ្ងៃមហាសិទ្ធិជោគ (ថ្ងៃមហាលាភ មានជ័យជំនះធំ)",
            "ថ្ងៃអម្រឹតជោគ (ថ្ងៃត្រជាក់ត្រជុំ មានលាភសក្ការៈ)",
            "ថ្ងៃទិញលក់ និងឡើងផ្ទះថ្មី",
            "ថ្ងៃបញ្ចុះបឋមសិលា និងបើកសម្ពោធ",
            "ថ្ងៃមង្គលការ និងភ្ជាប់ពាក្យ",
            "ថ្ងៃក្សេមក្សាន្តប្រកបដោយសិរី"
        ]
        khmer_day_status = khmer_qualities[(now.day + now.month) % len(khmer_qualities)]
        if officer["quality_kh"] == "ថ្ងៃគួរប្រុងប្រយ័ត្ន":
            khmer_day_status = "ថ្ងៃគួរប្រុងប្រយ័ត្ន (ជៀសវាងកិច្ចការមង្គលធំៗ)"

        wealth_god_dirs = ["ទិសឦសាន", "ទិសអាគ្នេយ៍", "ទិសខាងកើត", "ទិសខាងត្បូង", "ទិសខាងលិច"]
        wealth_dir = wealth_god_dirs[stem_idx % len(wealth_god_dirs)]
        nobleman_dirs = ["ទិសនិរតី", "ទិសពាយព្យ", "ទិសខាងជើង", "ទិសឦសាន"]
        nobleman_dir = nobleman_dirs[stem_idx % len(nobleman_dirs)]
        joy_dir = "ទិសខាងត្បូង" if stem_idx % 2 == 0 else "ទិសអាគ្នេយ៍"

        inauspicious_dirs = ["ទិសខាងលិច", "ទិសពាយព្យ", "ទិសខាងជើង", "ទិសឦសាន"]
        inauspicious_dir = inauspicious_dirs[(branch_idx + 3) % len(inauspicious_dirs)]

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
                "joy_god": joy_dir,
                "inauspicious_dir": inauspicious_dir
            }
        }

    # =========================================================================
    # 3. 24-Hour Timeline Hourly Luck Calculation (12 Double-Hours)
    # =========================================================================
    def calculate_hourly_timeline(self, user_day_master_element: str, target_date: Optional[date] = None) -> List[Dict[str, Any]]:
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
            
            if (i - day_branch_idx) % 6 == 0 and (i != day_branch_idx):
                base_score = max(35, base_score - 25)
                nature = "ម៉ោងគ្រោះ ឬទាស់ (គួរប្រុងប្រយ័ត្នខ្ពស់)"
                action_advice = "ជៀសវាងការបើកបរលឿន ការឈ្លោះប្រកែក ឬចុះហត្ថលេខាលើកិច្ចសន្យាសំខាន់"
            elif (i - day_branch_idx) % 4 == 0:
                base_score = min(98, base_score + 15)
                nature = "ម៉ោងមហាសិទ្ធិជោគ (ម៉ោងលាភធំ)"
                action_advice = "ល្អបំផុតសម្រាប់ការជួបអតិថិជន ចរចាជំនួញ ចុះកិច្ចសន្យា ឬបួងសួងសុំលាភ"
            elif base_score >= 80:
                nature = "ម៉ោងសិរីសួស្តី"
                action_advice = "ល្អសម្រាប់ការងាររដ្ឋបាល ប្រជុំក្រុមការងារ និងកិច្ចការទូទៅ"
            else:
                nature = "ម៉ោងមធ្យម"
                action_advice = "បំពេញកិច្ចការប្រចាំថ្ងៃដោយស្ងប់ចិត្ត និងសម្រាកឱ្យបានគ្រប់គ្រាន់"

            timeline.append({
                "interval": dh["time"],
                "name": dh["name_kh"],
                "element": dh["element"],
                "element_kh": dh["element_kh"],
                "score": base_score,
                "nature": nature,
                "advice": action_advice
            })

        return timeline

    def _calibrate_text_length(self, text: str, min_chars: int = 3500, max_chars: int = 4000) -> str:
        """Ensure the generated output strictly falls between 3500 and 4000 characters."""
        text = text.replace("**", "").replace("++", "").replace("==", "")
        text = text.replace("របាយការណ៍", "")
        text = re.sub(r'[a-zA-Z]', '', text)
        text = re.sub(r'\(\s*\)', '', text)
        text = re.sub(r'•\s*([💰👑🎨🏛️🌌⚠️🧭⏰✨💊💡🌿💼💖🌸☀️🍂❄️🧹🍎🏮🚫])', r'\1', text)
        text = re.sub(r'([📜🧭⏰💊📊💡👑🗓️])\s*([១២៣៤៥៦៧៨៩០]+\.)', r'\2', text)

        current_len = len(text)
        if min_chars <= current_len <= max_chars:
            return text

        if current_len > max_chars:
            cut_target = max_chars - 60
            trimmed = text[:cut_target]
            last_punc = max(trimmed.rfind("។"), trimmed.rfind("\n"))
            if last_punc > 3200:
                trimmed = trimmed[:last_punc+1]
            footer = "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n✨ សូមប្រសិទ្ធពរជ័យសិរីសួស្តី ជោគជ័យ សិរីមង្គល វិបុលសុខគ្រប់ប្រការ!"
            return trimmed + footer

        diff = min_chars - current_len
        extra_blessing = (
            "\n\nវិជ្ជាហុងស៊ុយបុរាណចិន និងក្បួនតម្រាខ្មែរបានបញ្ជាក់យ៉ាងច្បាស់ថា "
            "ការយល់ដឹងពីចង្វាក់ថាមពលមេឃដី និងការកែខៃតុល្យភាពយិនយ៉ាងស្របតាមកាលវេលាពិតប្រាកដ "
            "នឹងជួយកែប្រែជោគវាសនាពីអាក្រក់ឱ្យក្លាយជាល្អ ពីលំបាកឱ្យក្លាយជាងាយស្រួល "
            "និងបើកទ្វារទទួលលាភសក្ការៈទ្រព្យសម្បត្តិហូរចូលគ្រប់ទិសទីឥតដាច់។ "
            "សូមម្ចាស់ជោគជតារក្សាភាពស្ងប់ក្នុងចិត្ត ប្រព្រឹត្តអំពើល្អ និងប្រើប្រាស់ក្បួនតម្រានេះប្រកបដោយបញ្ញាញាណដ៏ភ្លឺស្វាង!"
        )
        text = text + extra_blessing
        if len(text) > max_chars:
            return self._calibrate_text_length(text, min_chars, max_chars)
        return text

    # =========================================================================
    # 4. In-Depth Daily Celestial Report (3500 - 4000 characters)
    # =========================================================================
    def generate_daily_celestial_report(
        self,
        birth_date: str,
        birth_time: str = "12:00",
        gender: str = "male",
        target_date: Optional[date] = None
    ) -> str:
        """
        Generate complete Personalized Daily Celestial Horoscope (Sent at 5:00 AM ICT).
        """
        p_bazi = self.calculate_precision_bazi(birth_date, birth_time, gender)
        almanac = self.calculate_global_almanac(target_date)
        
        dm = p_bazi.get("day_master", {})
        dm_elem = dm.get("element", "Wood")
        dm_elem_kh = dm.get("element_kh", "ឈើ យ៉ាង")
        timeline = self.calculate_hourly_timeline(dm_elem, target_date)

        avg_score = round(sum(t["score"] for t in timeline) / len(timeline), 1)
        officer = almanac["day_officer"]
        khmer = almanac["khmer_almanac"]
        dirs = almanac["auspicious_directions"]

        best_hours = [t for t in timeline if t["score"] >= 85]
        best_hours_str = "\n".join([f"  ⏰ {b['interval']} ({b['name']}): {b['advice']}" for b in best_hours[:3]])
        clash_hours = [t for t in timeline if t["score"] < 60]
        clash_hours_str = "\n".join([f"  ⚠️ {c['interval']} ({c['name']}): {c['advice']}" for c in clash_hours[:2]]) or "  ⚠️ គ្មានម៉ោងគ្រោះធ្ងន់ធ្ងរក្នុងថ្ងៃនេះឡើយ"

        wealth_text = {
            "Wood": "សម្រាប់ម្ចាស់ជោគជតាធាតុឈើ ថាមពលធាតុដីក្នុងថ្ងៃនេះតំណាងឱ្យឃ្លាំងទ្រព្យ។ លំហូរសាច់ប្រាក់ និងឱកាសចំណេញពីការលក់ដូរ ឬការវិនិយោគមានសន្ទុះខ្លាំង ជាពិសេសនៅពេលរសៀល។ គួរផ្តោតលើការប្រមូលបំណុលចាស់ៗ និងការរៀបចំគម្រោងហិរញ្ញវត្ថុថ្មីៗប្រកបដោយការប្រុងប្រយ័ត្ន។",
            "Fire": "សម្រាប់ម្ចាស់ជោគជតាធាតុភ្លើង ថាមពលធាតុដែកក្នុងថ្ងៃនេះតំណាងឱ្យភោគទ្រព្យ និងចំណូលក្រៅផ្លូវការ។ លោកអ្នកនឹងមានឱកាសទទួលបានលាភសំណាង ឬផលចំណេញពីការចរចាពាណិជ្ជកម្ម។ គួរជៀសវាងការចំណាយលើសម្ភារៈមិនចាំបាច់ និងរក្សាប្រាក់បម្រុងទុក។",
            "Earth": "សម្រាប់ម្ចាស់ជោគជតាធាតុដី ថាមពលធាតុទឹកក្នុងថ្ងៃនេះដើរតួជាលំហូរទ្រព្យសម្បត្តិដ៏បរិបូរណ៍។ អាជីវកម្មលើវិស័យសេវាកម្ម ការដឹកជញ្ជូន និងពាណិជ្ជកម្មអនឡាញដំណើរការទៅយ៉ាងរលូន។ គួរទាញយកប្រយោជន៍ពីកិច្ចសន្យាថ្មីៗដើម្បីពង្រីកមូលដ្ឋានអតិថិជន។",
            "Metal": "សម្រាប់ម្ចាស់ជោគជតាធាតុដែក ថាមពលធាតុឈើតំណាងឱ្យផលចំណេញ និងទ្រព្យសម្បត្តិដែលកើតចេញពីការខិតខំប្រឹងប្រែង។ ការវិនិយោគរយៈពេលវែង និងការចរចាជាមួយដៃគូជំនួញធំៗនឹងផ្តល់ផលជាផ្លែផ្កាគួរជាទីពេញចិត្ត។ គួរពិនិត្យលម្អិតលើឯកសារហិរញ្ញវត្ថុ។",
            "Water": "សម្រាប់ម្ចាស់ជោគជតាធាតុទឹក ថាមពលធាតុភ្លើងតំណាងឱ្យទ្រព្យធំ និងឱកាសមហាសេដ្ឋី។ លោកអ្នកនឹងទទួលបានការគាំទ្រផ្នែកហិរញ្ញវត្ថុពីមនុស្សខ្ពង់ខ្ពស់ ឬអតិថិជនកម្រិតខ្ពស់។ ឱកាសរកប្រាក់ចំណេញកើនឡើងទ្វេដងនៅចន្លោះពេលថ្ងៃត្រង់។"
        }.get(dm_elem, "លំហូរទ្រព្យសម្បត្តិប្រចាំថ្ងៃដំណើរការទៅដោយរលូន និងមានស្ថិរភាពល្អប្រសើរ។")

        career_text = {
            "Wood": "ក្នុងវិស័យអាជីពការងារ ម្ចាស់ជោគជតាធាតុឈើទទួលបានការជឿទុកចិត្តខ្ពស់ពីថ្នាក់ដឹកនាំ។ ការប្រជុំពិភាក្សា និងការរៀបចំយុទ្ធសាស្ត្រថ្មីៗទទួលបានការគាំទ្រពេញទំហឹង។ ចូររក្សាភាពបត់បែន និងស្តាប់យោបល់សហការីដើម្បីបង្កើតបរិយាកាសការងារប្រកបដោយភាពសុខដុម។",
            "Fire": "ការងាររបស់ម្ចាស់ជោគជតាធាតុភ្លើងពោរពេញដោយថាមពល និងភាពច្នៃប្រឌិត។ លោកអ្នកអាចសម្រេចកិច្ចការលំបាកៗបានយ៉ាងឆាប់រហ័ស។ គួរជៀសវាងការប្រញាប់ប្រញាល់ជ្រុលហួសហេតុ និងត្រូវផ្ទៀងផ្ទាត់រាល់ព័ត៌មានលម្អិតមុនពេលបញ្ជូនទៅថ្នាក់លើ។",
            "Earth": "ស្ថិរភាព និងការទទួលខុសត្រូវខ្ពស់ជាចំណុចខ្លាំងរបស់ម្ចាស់ជោគជតាធាតុដីក្នុងថ្ងៃនេះ។ គម្រោងការងារដែលធ្លាប់ជាប់គាំងនឹងចាប់ផ្តើមដំណើរការទៅមុខវិញយ៉ាងរលូន។ មនុស្សខ្ពង់ខ្ពស់នឹងផ្តល់ដំបូន្មានដ៏មានតម្លៃសម្រាប់ការអភិវឌ្ឍន៍អាជីព។",
            "Metal": "ការសម្រេចចិត្តដ៏ច្បាស់លាស់ និងម៉ឺងម៉ាត់របស់ម្ចាស់ជោគជតាធាតុដែកនឹងនាំមកនូវជោគជ័យក្នុងការដោះស្រាយបញ្ហាស្មុគស្មាញ។ លោកអ្នកមានឱកាសបង្ហាញសមត្ថភាពដឹកនាំដ៏លេចធ្លោ។ ចូររក្សាភាពទន់ភ្លន់ក្នុងការប្រាស្រ័យទាក់ទង។",
            "Water": "ភាពឆ្លាតវៃ និងបញ្ញាញាណដ៏រហ័សរហួនរបស់ម្ចាស់ជោគជតាធាតុទឹកជួយឱ្យការចរចាការងារទទួលបានជោគជ័យលើសពីការរំពឹងទុក។ ការងារទាក់ទងនឹងការស្រាវជ្រាវ គំនិតច្នៃប្រឌិត និងការផ្សព្វផ្សាយមានសន្ទុះខ្លាំងក្លាបំផុត។"
        }.get(dm_elem, "កិច្ចការងារប្រចាំថ្ងៃមានដំណើរការល្អប្រសើរ និងពោរពេញដោយឱកាសរីកចម្រើន។")

        love_text = {
            "Wood": "ផ្នែកសេចក្តីស្នេហា និងចំណងមិត្តភាពមានភាពកក់ក្តៅ និងយល់ចិត្តគ្នាកាន់តែស៊ីជម្រៅ។ សម្រាប់អ្នកមានគូស្នេហ៍ ការជជែកពិភាក្សាលើគម្រោងអនាគតរួមគ្នានឹងបង្កើតភាពស្និទ្ធស្នាលទ្វេដង។ សម្រាប់អ្នកនៅលីវ នឹងមានឱកាសជួបមនុស្សដែលត្រូវចិត្តតាមរយៈការងារ។",
            "Fire": "ទំនាក់ទំនងស្នេហារបស់ម្ចាស់ជោគជតាធាតុភ្លើងពោរពេញដោយភាពរំភើប និងភាពផ្អែមល្ហែម។ ចូរផ្តល់ពេលវេលាឱ្យគ្នាទៅវិញទៅមក និងបង្ហាញក្តីស្រឡាញ់តាមរយៈសកម្មភាពតូចតាច។ ចៀសវាងការយករឿងការងារមកប៉ះពាល់ដល់អារម្មណ៍គ្រួសារ។",
            "Earth": "ភាពស្មោះត្រង់ និងការយកចិត្តទុកដាក់ខ្ពស់ជួយឱ្យទំនាក់ទំនងគ្រួសារមានសេចក្តីសុខ និងកក់ក្តៅយ៉ាងក្រៃលែង។ អ្នកទាំងពីរយល់ចិត្តគ្នាដោយមិនបាច់និយាយច្រើន។ អ្នកនៅលីវមានឱកាសទទួលបានការណែនាំពីចាស់ទុំ ឬមិត្តភក្តិជិតស្និទ្ធ។",
            "Metal": "ចំណងស្នេហារបស់ម្ចាស់ជោគជតាធាតុដែកមានភាពរឹងមាំ និងផ្អែកលើការទុកចិត្តគ្នាទៅវិញទៅមក។ ការបើកចិត្តចែករំលែកអារម្មណ៍ពិតនឹងជួយរំលាយរាល់ការយល់ច្រឡំកន្លងមក។ គួររៀបចំអាហារពេលល្ងាចជួបជុំគ្នាដើម្បីពង្រឹងភាពស្និទ្ធស្នាល។",
            "Water": "មន្តស្នេហ៍ និងភាពទាក់ទាញរបស់ម្ចាស់ជោគជតាធាតុទឹកឡើងខ្ពស់ខ្លាំង។ លោកអ្នកងាយស្រួលបង្កើតមិត្តភាពថ្មីៗ និងទទួលបានការចាប់អារម្មណ៍ពីមនុស្សជុំវិញខ្លួន។ ចូររក្សាភាពច្បាស់លាស់ក្នុងចិត្ត និងផ្តល់តម្លៃដល់មនុស្សដែលនៅក្បែរខ្លួន។"
        }.get(dm_elem, "ទំនាក់ទំនងស្នេហា និងគ្រួសារមានភាពសុខដុមរមនា និងសេចក្តីសុខ។")

        health_text = {
            "Wood": "សុខភាពទូទៅមានភាពរឹងមាំល្អ ប៉ុន្តែគួរយកចិត្តទុកដាក់លើថ្លើម ភ្នែក និងសរសៃពួរ។ ជៀសវាងការសម្លឹងអេក្រង់ទូរស័ព្ទ ឬកុំព្យូទ័រយូរពេក និងគួរទទួលទានបន្លែបៃតងឱ្យបានច្រើនដើម្បីចិញ្ចឹមរាងកាយ។",
            "Fire": "ថាមពលក្នុងខ្លួនឡើងខ្ពស់ គួរប្រយ័ត្នកម្តៅក្នុង បេះដូង និងសម្ពាធឈាម។ គួរបរិភោគទឹកឱ្យបានគ្រប់គ្រាន់ ជៀសវាងអាហារហឹរឬខ្លាញ់ច្រើន និងឆ្លៀតពេលសម្រាកកាយរយៈពេលខ្លីនៅពេលថ្ងៃត្រង់។",
            "Earth": "ប្រព័ន្ធរំលាយអាហារ ក្រពះ និងលំពែងទាមទារការថែទាំជាពិសេស។ គួរទទួលទានអាហារឱ្យបានទៀងទាត់ពេល ជៀសវាងអាហារត្រជាក់ពេក និងធ្វើលំហាត់ប្រាណស្រាលៗដើម្បីសម្រួលខ្យល់ក្នុងពោះវៀន។",
            "Metal": "គួរយកចិត្តទុកដាក់លើប្រព័ន្ធដង្ហើម សួត និងស្បែក។ ការស្រូបយកខ្យល់អាកាសបរិសុទ្ធនៅពេលព្រឹកព្រលឹម និងការទទួលទានទឹកក្តៅឧណ្ហៗនឹងជួយពង្រឹងប្រព័ន្ធភាពស៊ាំក្នុងរាងកាយឱ្យកាន់តែរឹងមាំ។",
            "Water": "តម្រងនោម និងប្រព័ន្ធទឹកនោមទាមទារការការពារឱ្យបានដិតដល់។ ជៀសវាងការអង្គុយយូរពេកដោយមិនកម្រើក និងការទទួលទានអាហារប្រៃជ្រុល។ ការគេងលក់ឱ្យបានស្កប់ស្កល់នៅពេលយប់ជាឱសថដ៏ស័ក្តិសិទ្ធិបំផុត។"
        }.get(dm_elem, "សុខភាពទូទៅមានតុល្យភាពល្អ និងមានកម្លាំងថាមពលមាំមួន។")

        fengshui_tips = (
            f"១. រៀបចំតុធ្វើការឱ្យបែរមុខទៅរក {dirs['wealth_god']} ឬ {dirs['nobleman_god']} ដើម្បីស្រូបទាញលំហូរថាមពលវិជ្ជមាន និងការគាំពារពីមនុស្សខ្ពង់ខ្ពស់។\n"
            f"២. ប្រើប្រាស់សម្លៀកបំពាក់ ឬគ្រឿងអលង្ការដែលមាន {khmer['lucky_color']} ដើម្បីពង្រឹងបារមី និងបង្កើនមន្តស្នេហ៍ក្នុងការចរចា។\n"
            f"៣. ដាក់កែវទឹកស្អាតមួយកែវនៅទិសខាងជើង ឬទិសខាងកើតនៃបន្ទប់ធ្វើការដើម្បីចិញ្ចឹមធាតុ {dm_elem_kh} និងកាត់បន្ថយភាពតានតឹង។\n"
            f"៤. ជៀសវាងការបង្កើតសំឡេងខ្លាំង ឬការជួសជុលនៅ {dirs['inauspicious_dir']} ដើម្បីការពារកុំឱ្យរំខានដល់ថាមពលអវិជ្ជមានប្រចាំថ្ងៃ។"
        )

        body = (
            f"🌅 ហោរាសាស្ត្រ និងហុងស៊ុយប្រចាំថ្ងៃ 🌅\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📅 កាលបរិច្ឆេទ: {almanac['date']} ({almanac['day_name_kh']})\n"
            f"👤 ធាតុម្ចាស់ជោគជតា: {dm_elem_kh} | ម៉ោងកំណើត: {birth_time}\n"
            f"🌟 ពិន្ទុសំណាងប្រចាំថ្ងៃ: {avg_score}% ({officer['quality_kh']})\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"១. ក្បួនតម្រាខ្មែរ និងចិនសកល\n"
            f"👑 ឫក្សពារខ្មែរ: {khmer['day_quality']}\n"
            f"🎨 ពណ៌សម្លៀកបំពាក់នាំលាភ: {khmer['lucky_color']} ({khmer['color_meaning']})\n"
            f"🏛️ ក្បួនចិនសកល (១២ មន្ត្រីប្រចាំថ្ងៃ): {officer['name']} ({officer['meaning']})\n"
            f"  👉 ការបកស្រាយលម្អិត: {officer['detail']}\n"
            f"🌌 តារានក្ខត្តឫក្ស ២៨: {almanac['constellation']}\n"
            f"⚠️ សត្វឆ្នាំឆុងប្រចាំថ្ងៃ: {almanac['clash_animal']} (ជៀសវាងការប៉ះទង្គិចពាក្យសម្តី ឬកិច្ចសន្យាប្រថុយប្រថាន)\n\n"
            f"២. ទិសនាំលាភសក្ការៈប្រចាំថ្ងៃ\n"
            f"💰 ទិសទេវតាទ្រព្យ: {dirs['wealth_god']} (ទិសដៅសម្រាប់រៀបចំតុធ្វើការ ពិភាក្សាជំនួញ និងប្រមូលលំហូរហិរញ្ញវត្ថុ)\n"
            f"👑 ទិសទេវតាមនុស្សខ្ពង់ខ្ពស់: {dirs['nobleman_god']} (ទិសដៅសម្រាប់ស្វែងរកអ្នកជួយជ្រោមជ្រែង និងការពិគ្រោះយោបល់)\n"
            f"💖 ទិសទេវតាមង្គល: {dirs['joy_god']} (ទិសដៅសម្រាប់បង្កើនមន្តស្នេហ៍ និងភាពចុះសម្រុងក្នុងគ្រួសារ)\n"
            f"🚫 ទិសដៅគួរប្រុងប្រយ័ត្ន: {dirs['inauspicious_dir']} (ជៀសវាងការជួសជុល ដំដែកគោល ឬការអង្គុយបែរមុខទៅរក)\n\n"
            f"៣. តារាងពេលវេលាលាភ និងគ្រោះពេញមួយថ្ងៃ (២៤ ម៉ោង)\n"
            f"✨ ម៉ោងមហាលាភសិរីសួស្តី:\n{best_hours_str}\n\n"
            f"⚠️ ម៉ោងគួរប្រុងប្រយ័ត្ន:\n{clash_hours_str}\n\n"
            f"៤. ការវិភាគជោគជតា ៤ វិស័យប្រចាំថ្ងៃ\n"
            f"💰 លាភទ្រព្យសម្បត្តិ និងលំហូរសាច់ប្រាក់:\n{wealth_text}\n\n"
            f"💼 កិត្តិយស អាជីពការងារ និងមុខជំនួញ:\n{career_text}\n\n"
            f"💖 សេចក្តីស្នេហា ទំនាក់ទំនង និងសុភមង្គល:\n{love_text}\n\n"
            f"🌿 សុខភាព ថាមពលជីវិត និងតុល្យភាពយិនយ៉ាង:\n{health_text}\n\n"
            f"៥. ធាតុឱសថព្យាបាល និងពង្រឹងរាសី (យុងសិន)\n"
            f"💊 ធាតុឱសថចម្បង: {p_bazi.get('useful_god', 'ពង្រឹងតុល្យភាពធាតុទាំង ៥')}\n"
            f"ការប្រើប្រាស់ធាតុឱសថខាងលើជួយបំពេញចំណុចខ្វះខាតក្នុងរាសីចក្រ ស្រោចស្រពថាមពលជីវិតឱ្យមានភាពរលូន និងកាត់បន្ថយឧបសគ្គទាំងឡាយក្នុងថ្ងៃនេះឱ្យរលាយបាត់អស់។\n\n"
            f"៦. យុទ្ធសាស្ត្រ និងវិធីសាស្ត្រប្រតិបត្តិប្រចាំថ្ងៃ\n"
            f"💡 គន្លឹះហុងស៊ុយបង្កើនថាមពល:\n{fengshui_tips}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ ប្រព័ន្ធដំណើរការដោយស្វ័យប្រវត្តិកម្រិតខ្ពស់ជូនលោកអ្នករៀងរាល់ម៉ោង ៥ ព្រឹក!"
        )
        return self._calibrate_text_length(body, 3500, 4000)

    # =========================================================================
    # 5. In-Depth Monthly Grand Blueprint (3500 - 4000 characters)
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
        Generate Monthly Grand Blueprint (Sent on 1st of every month).
        """
        now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))
        year = year or now.year
        month = month or now.month

        p_bazi = self.calculate_precision_bazi(birth_date, birth_time, gender)
        dm = p_bazi.get("day_master", {})
        dm_elem = dm.get("element", "Wood")
        dm_elem_kh = dm.get("element_kh", "ឈើ យ៉ាង")
        
        fs_res = self.calc_engine.calculate_flying_stars(year, month)
        grid = fs_res.get("data", {}).get("grid", {})

        month_score = 88.5

        wealth_strategy = (
            f"នៅក្នុងខែទី {month:02d} នេះ ថាមពលលំហូរសាច់ប្រាក់របស់ម្ចាស់ជោគជតាធាតុ {dm_elem_kh} មានការវិវត្តន៍យ៉ាងគួរឱ្យកត់សម្គាល់។ "
            "ឱកាសពង្រីកមុខជំនួញ ការបង្កើតប្រភពចំណូលថ្មីៗ និងការវិនិយោគលើវិស័យបច្ចេកវិទ្យា ពាណិជ្ជកម្ម ឬអចលនទ្រព្យ "
            "នឹងផ្តល់ផលចំណេញខ្ពស់នៅសប្តាហ៍ទី ២ និងទី ៣ នៃខែ។ "
            "ទោះជាយ៉ាងណា គួរគ្រប់គ្រងលំហូរសាច់ប្រាក់ចេញឱ្យបានច្បាស់លាស់ ជៀសវាងការឱ្យខ្ចីបុលដោយគ្មានកិច្ចសន្យាត្រឹមត្រូវ "
            "និងគួររៀបចំផែនការបម្រុងទុកសម្រាប់កិច្ចការបន្ទាន់នានា។"
        )

        career_strategy = (
            f"ដំណើរការអាជីពការងាររបស់ម្ចាស់ជោគជតាធាតុ {dm_elem_kh} ស្ថិតក្នុងសន្ទុះឡើងខ្ពស់។ "
            "លោកអ្នកនឹងទទួលបានការគាំពារពីមនុស្សខ្ពង់ខ្ពស់ ការទទួលស្គាល់ស្នាដៃពីថ្នាក់ដឹកនាំ និងមានឱកាសឡើងកាន់តំណែងថ្មី។ "
            "ការចរចាការងារធំៗ និងការចុះកិច្ចព្រមព្រៀងពាណិជ្ជកម្មគួរធ្វើឡើងនៅថ្ងៃមហាសិទ្ធិជោគ ដើម្បីទទួលបានលទ្ធផលជាទីគាប់ចិត្ត "
            "និងបង្កើនទំនុកចិត្តជាមួយដៃគូសហការរយៈពេលវែង។"
        )

        love_strategy = (
            f"ផ្នែកទំនាក់ទំនងស្នេហា និងគ្រួសារមានភាពកក់ក្តៅ និងផ្អែមល្ហែមយ៉ាងក្រៃលែង។ "
            "ថាមពលផ្កាយស្នេហាជួយបង្កើនមន្តស្នេហ៍ និងភាពចុះសម្រុងគ្នារវាងស្វាមីភរិយា។ "
            "សម្រាប់អ្នកនៅលីវ នឹងមានឱកាសជួបមនុស្សដែលមាននិស្ស័យខ្ពស់ និងមានការគិតស្របគ្នា តាមរយៈការណែនាំពីមិត្តភក្តិ ឬក្នុងពិធីជួបជុំសង្គម។ "
            "ការបើកចិត្ត និងការផ្តល់ការគោរពគ្នាទៅវិញទៅមកជាស្ពានចម្លងសុភមង្គលដ៏រឹងមាំ។"
        )

        health_strategy = (
            "សុខភាពទូទៅពេញមួយខែនេះមានភាពនឹងនរ និងរឹងមាំល្អ។ "
            "ទោះជាយ៉ាងណា គួររក្សាតុល្យភាពរវាងការងារ និងការសម្រាកកាយ ជៀសវាងការធ្វើការងារហួសកម្លាំងនៅពេលយប់ជ្រៅ។ "
            "ការហាត់ប្រាណជាប្រចាំ ការទទួលទានទឹកស្អាត និងការធ្វើសមាធិនឹងជួយរក្សាថាមពលយិនយ៉ាងក្នុងខ្លួនឱ្យមានតុល្យភាពបរិបូរណ៍ "
            "ព្រមទាំងពង្រឹងប្រព័ន្ធការពាររាងកាយឱ្យចៀសផុតពីរោគាទាំងឡាយ។"
        )

        flying_stars_detail = (
            "ប្លង់តារាហោះ ៩ វិហារប្រចាំខែនេះបង្ហាញពីការប្រែប្រួលនៃលំហូរថាមពលអាកាស៖ "
            "ទិសខាងត្បូងជាទិសអំណោយផលធំបំផុត គួររៀបចំឱ្យមានពន្លឺភ្លឺច្បាស់ និងខ្យល់ចេញចូលល្អ។ "
            "ទិសខាងជើងជាទិសស្រូបទាញលាភជ័យ គួរដាក់តាំងអាងចិញ្ចឹមត្រី ឬប្រភពទឹកស្អាតរំញោចទ្រព្យ។ "
            "ទិសខាងលិច និងទិសអាគ្នេយ៍ជាទិសដែលត្រូវប្រុងប្រយ័ត្នខ្ពស់ ហាមដាច់ខាតការជួសជុល ឬបង្កើតសំឡេងរំខានខ្លាំងៗ។"
        )

        weeks_guide = (
            f"🗓️ សប្តាហ៍ទី ១ (ថ្ងៃទី ០១ ដល់ ០៧): សប្តាហ៍នៃការរៀបចំផែនការ និងប្រមូលផ្តុំកម្លាំងថាមពល។ ល្អសម្រាប់ការសម្អាតគេហដ្ឋាន និងការរៀបចំយុទ្ធសាស្ត្រថ្មីៗ។\n"
            f"🗓️ សប្តាហ៍ទី ២ (ថ្ងៃទី ០៨ ដល់ ១៤): សប្តាហ៍នៃឱកាសមហាលាភ! លំហូរហិរញ្ញវត្ថុ និងការចរចាជំនួញចាប់ផ្តើមផ្តល់ផលចំណេញយ៉ាងច្រើន។\n"
            f"🗓️ សប្តាហ៍ទី ៣ (ថ្ងៃទី ១៥ ដល់ ២១): សប្តាហ៍នៃការពង្រីកទំនាក់ទំនង និងកិត្តិយស។ ការងារជាក្រុម និងការគាំទ្រពីមនុស្សខ្ពង់ខ្ពស់មានសន្ទុះខ្លាំង។\n"
            f"🗓️ សប្តាហ៍ទី ៤ (ថ្ងៃទី ២២ ដល់ដំណាច់ខែ): សប្តាហ៍នៃការច្រូតកាត់ផលលាភ និងបូកសរុបសមិទ្ធផល។ គួររក្សាភាពស្ងប់ចិត្ត និងត្រៀមទទួលខែបន្ទាប់។"
        )

        body = (
            f"📅 ផែនទីរាសី និងតារាហោះហុងស៊ុយប្រចាំខែ 📅\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🗓️ ខែប្រតិទិន: ខែទី {month:02d} ឆ្នាំ {year} (យុគទី ៩ ធាតុភ្លើង)\n"
            f"👤 ម្ចាស់ជោគជតា: ធាតុ {dm_elem_kh} | ម៉ោងកំណើត {birth_time}\n"
            f"🌟 ពិន្ទុសំណាងរួមប្រចាំខែ: {month_score}%\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"១. ប្លង់តារាហោះ ៩ វិហារប្រចាំខែ\n"
            f"🌟 ទិសទ្រព្យធំប្រចាំខែ: ទិសខាងត្បូង និងខាងជើង (បើកភ្លើងបំភ្លឺ និងដាក់ទឹកហូររំញោចថាមពលលាភ)\n"
            f"⚠️ ទិសគ្រោះកាចប្រចាំខែ: ទិសខាងលិច (ផ្កាយលេខ ៥ លឿងគ្រោះកាច) និងទិសអាគ្នេយ៍ (ផ្កាយលេខ ២ ខ្មៅជំងឺ)\n"
            f"  👉 វិធីកែខៃ និងដំណោះស្រាយ: ហាមដាច់ខាតការជួសជុល ដំដែកគោល ឬជីកដីនៅទិសខាងលិច។ ដាក់កណ្តឹងខ្យល់លោហៈ ៦ បំពង់ ឬដបទឹកអំបិលរំលាយគ្រោះ។\n"
            f"  👉 ការវិភាគលំហូរថាមពល: {flying_stars_detail}\n\n"
            f"២. យុទ្ធសាស្ត្រទ្រព្យសម្បត្តិ និងអាជីវកម្មប្រចាំខែ\n{wealth_strategy}\n\n"
            f"៣. អាជីពការងារ មុខតំណែង និងកិច្ចសន្យា\n{career_strategy}\n\n"
            f"៤. ស្នេហា អាពាហ៍ពិពាហ៍ និងទំនាក់ទំនងគ្រួសារ\n{love_strategy}\n\n"
            f"៥. សុខភាព ថាមពល និងការថែទាំរាងកាយ\n{health_strategy}\n\n"
            f"៦. ផែនទីពេលវេលា ៤ សប្តាហ៍ប្រចាំខែ\n{weeks_guide}\n\n"
            f"៧. ថ្ងៃមហាសិទ្ធិជោគក្នុងខែនេះ\n"
            f"✨ ថ្ងៃមង្គលលាភធំ: ថ្ងៃទី ០៦, ១២, ១៨, ២៤, និង ២៨ នៃខែ (ស័ក្តិសមបំផុតសម្រាប់ពិធីមង្គល ចុះហត្ថលេខា និងបើកដំណើរការអាជីវកម្ម)\n"
            f"⚠️ ថ្ងៃគួរជៀសវាងកិច្ចការធំ: ថ្ងៃទី ០៤, ១៤, ២២, និង ២៧ នៃខែ (ថ្ងៃឆុង ឬថាមពលប៉ះទង្គិច)\n\n"
            f"៨. ធាតុឱសថ និងវិធីរៀបចំហុងស៊ុយគេហដ្ឋានប្រចាំខែ\n"
            f"💊 ធាតុឱសថប្រចាំខែ: {p_bazi.get('useful_god', 'ពង្រឹងតុល្យភាពធាតុ')}\n"
            f"💡 វិធីតុបតែងលម្អគេហដ្ឋាន និងកន្លែងធ្វើការ: ដាក់តាំងរុក្ខជាតិបៃតងស្រស់នៅទិសខាងកើត និងបន្ថែមភ្លើងបំភ្លឺនៅទិសខាងត្បូងដើម្បីស្រូបទាញលាភសំណាងយុគទី ៩។\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ ប្រព័ន្ធដំណើរការដោយស្វ័យប្រវត្តិកម្រិតខ្ពស់ ផ្ញើជូនលោកអ្នកនៅថ្ងៃទី ១ រៀងរាល់ដើមខែថ្មី!"
        )
        return self._calibrate_text_length(body, 3500, 4000)

    # =========================================================================
    # 6. In-Depth Grand Annual Horoscope (3500 - 4000 characters)
    # =========================================================================
    def generate_yearly_celestial_report(
        self,
        birth_date: str,
        birth_time: str = "12:00",
        gender: str = "male",
        year: Optional[int] = None
    ) -> str:
        """
        Generate Grand Annual Horoscope (Sent on New Year Day / Li Chun).
        """
        now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))
        year = year or now.year

        p_bazi = self.calculate_precision_bazi(birth_date, birth_time, gender)
        dm = p_bazi.get("day_master", {})
        dm_elem = dm.get("element", "Wood")
        dm_elem_kh = dm.get("element_kh", "ឈើ យ៉ាង")
        macro = self.chronos.analyze_year_macro_cycle(year)

        yearly_wealth = (
            f"នៅក្នុងឆ្នាំមហាសករាជ {year} នេះ លំហូរទ្រព្យសម្បត្តិ និងភោគផលរបស់ម្ចាស់ជោគជតាធាតុ {dm_elem_kh} "
            "មានការកើនឡើងយ៉ាងខ្លាំងក្លាស្របតាមចលនាថាមពលយុគទី ៩ ធាតុភ្លើង។ "
            "វិស័យបច្ចេកវិទ្យា បញ្ញាសិប្បនិម្មិត ពាណិជ្ជកម្មអន្តរជាតិ និងការច្នៃប្រឌិតថ្មីៗនឹងក្លាយជាប្រភពចំណូលដ៏ធំធេង។ "
            "ការគ្រប់គ្រងហិរញ្ញវត្ថុប្រកបដោយចក្ខុវិស័យវែងឆ្ងាយ និងការវិនិយោគលើចំណេះដឹងនឹងជួយបង្កើតទ្រព្យសម្បត្តិរឹងមាំយូរអង្វែង។"
        )

        yearly_career = (
            f"ដំណើរការអាជីព និងកិត្តិយសរបស់ម្ចាស់ជោគជតាធាតុ {dm_elem_kh} នឹងឈានដល់កម្រិតកំពូលថ្មីមួយ។ "
            "លោកអ្នកនឹងមានឱកាសពង្រីកឥទ្ធិពល ទទួលបានការជឿទុកចិត្តខ្ពស់ពីដៃគូសហការ និងឡើងកាន់តំណែងដឹកនាំសំខាន់ៗ។ "
            "ការរក្សាទំនាក់ទំនងល្អជាមួយមនុស្សជុំវិញខ្លួន និងការបើកចិត្តទទួលយកបច្ចេកវិទ្យាទំនើបនឹងជំរុញឱ្យអាជីពរីកចម្រើនឥតឈប់ឈរ។"
        )

        yearly_love = (
            "ផ្នែកសេចក្តីស្នេហា និងចំណងគ្រួសារពេញមួយឆ្នាំនេះពោរពេញដោយភាពកក់ក្តៅ សុភមង្គល និងសេចក្តីសុខក្សេមក្សាន្ត។ "
            "ការយោគយល់អធ្យាស្រ័យគ្នា និងការគាំទ្រដល់ក្តីស្រមៃរបស់ដៃគូជីវិតនឹងជួយពង្រឹងគ្រឹះគ្រួសារឱ្យកាន់តែរឹងមាំ។ "
            "សម្រាប់អ្នកនៅលីវ ឆ្នាំនេះជាឆ្នាំមាសក្នុងការជួបគូព្រេងពិតប្រាកដ និងឈានទៅដល់ការកសាងគ្រួសារដ៏មានសុភមង្គល។"
        )

        yearly_health = (
            "សុខភាព និងថាមពលជីវិតពេញមួយឆ្នាំនេះមានភាពមាំមួនល្អប្រសើរ។ "
            "ការថែរក្សារបៀបរស់នៅប្រកបដោយសុខដុម ការទទួលទានអាហារធម្មជាតិ និងការធ្វើលំហាត់ប្រាណទៀងទាត់ "
            "នឹងជួយរក្សាភាពក្មេងជាងវ័យ និងពង្រឹងប្រព័ន្ធការពាររាងកាយឱ្យរឹងមាំជានិច្ច។ "
            "គួរឆ្លៀតពេលធ្វើដំណើរកម្សាន្តទៅកាន់តំបន់ធម្មជាតិដើម្បីស្រូបយកថាមពលបរិសុទ្ធពីផែនដី។"
        )

        seasons_guide = (
            f"🌸 រដូវផ្ការីក (ខែ ១ ដល់ ៣): រដូវកាលនៃការចាប់ផ្តើម និងការបណ្តុះគ្រាប់ពូជនៃភាពជោគជ័យ។ ល្អបំផុតសម្រាប់ការបើកដំណើរការគម្រោងធំៗ។\n"
            f"☀️ រដូវក្តៅ (ខែ ៤ ដល់ ៦): រដូវកាលនៃភាពរីកចម្រើន និងសន្ទុះថាមពលខ្លាំងក្លា។ លំហូរហិរញ្ញវត្ថុ និងកិច្ចសន្យាថ្មីៗកើនឡើងទ្វេដង។\n"
            f"🍂 រដូវស្លឹកឈើជ្រុះ (ខែ ៧ ដល់ ៩): រដូវកាលនៃការប្រមូលផល និងការច្រូតកាត់ផលចំណេញ។ ការងារទាំងឡាយសម្រេចបានផ្លែផ្កាគួរជាទីពេញចិត្ត។\n"
            f"❄️ រដូវរងា (ខែ ១០ ដល់ ១២): រដូវកាលនៃការរក្សាទ្រព្យ និងការរៀបចំយុទ្ធសាស្ត្រសម្រាប់ឆ្នាំបន្ទាប់។ គួរជួបជុំគ្រួសារ និងធ្វើបុណ្យទាន។"
        )

        master_advice = (
            f"គ្រូហុងស៊ុយជាន់ខ្ពស់សូមផ្តល់ដំបូន្មានមាសដល់ម្ចាស់ជោគជតាធាតុ {dm_elem_kh} ថា៖ "
            "ភាពជោគជ័យដ៏អស្ចារ្យកើតចេញពីការផ្សំគ្នារវាង 'ភ័ព្វសំណាងមេឃ (ពេលវេលាល្អ)' 'ភ័ព្វសំណាងដី (ហុងស៊ុយត្រឹមត្រូវ)' "
            "និង 'ការប្រឹងប្រែងរបស់មនុស្ស (សកម្មភាព និងចិត្តគំនិត)'។ "
            "ចូររក្សាភាពស្មោះត្រង់ ប្រកាន់ខ្ជាប់នូវគុណធម៌ និងប្រើប្រាស់ក្បួនតម្រាហុងស៊ុយនេះជាត្រីវិស័យបំភ្លឺផ្លូវជីវិតឆ្ពោះទៅរកភាពរុងរឿងជានិរន្តរ៍!"
        )

        body = (
            f"🎊 មហាសង្ក្រាន្ត និងជោគជតារាសីប្រចាំឆ្នាំពេញលេញ 🎊\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎆 ឆ្នាំមហាសករាជ: {year} (យុគទី ៩ ធាតុភ្លើង: ២០២៤-២០៤៣)\n"
            f"👤 ម្ចាស់ជោគជតា: ធាតុស្នូល {dm_elem_kh}\n"
            f"🧭 ថាមពលយុគ: យុគនៃបញ្ញាសិប្បនិម្មិត ថាមពលអគ្គិសនី ចក្ខុវិស័យ វិញ្ញាណ និងការផ្លាស់ប្តូរល្បឿនលឿន\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"១. ព្រះបារមីតារាហុងស៊ុយប្រចាំឆ្នាំ\n"
            f"🐉 ទិសព្រះមហាក្សត្រតារាប្រចាំឆ្នាំ (ថៃសួយ): ទិសអាគ្នេយ៍\n"
            f"⚡ ទិសបំបែកថៃសួយ (ស៊ុយពួរ): ទិសពាយព្យ (ហាមដាច់ខាតការសាងសង់ វាយកម្ទេច ឬជីកដី)\n"
            f"🛡️ ទិសគ្រោះមហន្តរាយទាំង ៣ (សានសា): ទិសខាងត្បូង\n"
            f"🌟 ទិសផ្កាយសំណាងធំប្រចាំឆ្នាំ: ទិសខាងជើង និងទិសនិរតី (ទិសដៅស្រូបទាញភោគទ្រព្យមហាសាល)\n\n"
            f"២. ការវិភាគជោគជតា ៤ វិស័យពេញមួយឆ្នាំ\n"
            f"💰 លាភទ្រព្យសម្បត្តិ និងលំហូរហិរញ្ញវត្ថុ:\n{yearly_wealth}\n\n"
            f"💼 កិត្តិយស មុខតំណែង និងអាជីពការងារ:\n{yearly_career}\n\n"
            f"💖 សេចក្តីស្នេហា សុភមង្គល និងគ្រួសារ:\n{yearly_love}\n\n"
            f"🌿 សុខភាព ថាមពល និងអាយុយឺនយូរ:\n{yearly_health}\n\n"
            f"៣. វដ្តរាសី ៤ រដូវកាលពេញមួយឆ្នាំ\n{seasons_guide}\n\n"
            f"៤. វិធីរៀបចំហុងស៊ុយទទួលទេវតាឆ្នាំថ្មី\n"
            f"🧹 ការបោសសម្អាត និងលាងជម្រះថាមពលចាស់: សម្អាតគ្រប់ជ្រុងនៃគេហដ្ឋានឱ្យភ្លឺរលោងមុនថ្ងៃចូលឆ្នាំថ្មី។\n"
            f"🍎 ការរៀបចំដង្វាយ និងផ្លែឈើមង្គល ៥ ពណ៌: រៀបចំចានផ្លែឈើមង្គលនៅទិសខាងកើត និងទិសខាងត្បូងដើម្បីទទួលសិរីសួស្តី។\n"
            f"🏮 ការរៀបចំទិសដៅស្រូបលាភ: ដាក់តាំងចង្កៀងបំភ្លឺ ឬវត្ថុមង្គលធាតុភ្លើងដើម្បីទទួលថាមពលយុគទី ៩។\n"
            f"💊 ធាតុឱសថប្រចាំឆ្នាំ: {p_bazi.get('useful_god', 'ពង្រឹងតុល្យភាពធាតុ')}\n\n"
            f"៥. ដំបូន្មានមហាសិទ្ធិជោគពីគ្រូហុងស៊ុយជាន់ខ្ពស់\n{master_advice}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✨ ប្រព័ន្ធ Supreme Feng Shui AGI សូមប្រសិទ្ធពរជ័យសិរីសួស្តី ជោគជ័យ សិរីមង្គល វិបុលសុខគ្រប់ប្រការ!"
        )
        return self._calibrate_text_length(body, 3500, 4000)
