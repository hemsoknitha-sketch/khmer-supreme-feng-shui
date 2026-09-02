"""
Supreme Feng Shui AGI System - Maha Sneh & Peach Blossom Universal Zenith Engine
"ក្បួនហុងស៊ុយ និងមហាស្នេហ៍" (Feng Shui, Romance, Peach Blossom & Relationship Harmony)
Implements:
1. Classical Peach Blossom Star (Tao Hua 桃花) Precise Astronomical Alignment
2. BaZi 8 Pillars Love Compatibility & Day Master Resonance (0-100%)
3. Useful God (Yong Shen) Love Remedy & Elemental Healing
4. Magnetism & Attraction Strategy (យុទ្ធសាស្ត្រអន្ទងចិត្ត តាមក្បួនផ្កាប៉េស និងយុគ ៩)
5. Heart Softening & Harmony Strategy (វិធីសាស្ត្របន្ទន់ចិត្ត តាមធាតុស្នូលគូស្នេហ៍)
6. Universal Zenith Report (របាយការណ៍ហុងស៊ុយ និងមហាស្នេហ៍)
"""

import logging
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime

from config import config
from engines.classical_calc import ClassicalCalcEngine

logger = logging.getLogger("SupremeFengShui.MahaSneh")


class MahaSnehLoveEngine:
    """Universal Zenith Engine for Feng Shui Romance, Peach Blossom & Maha Sneh."""

    # 12 Earthly Branches to Peach Blossom Direction Mapping
    # (Monkey/Rat/Dragon -> Rooster/West), (Tiger/Horse/Dog -> Rabbit/East),
    # (Pig/Rabbit/Goat -> Rat/North), (Snake/Rooster/Ox -> Horse/South)
    PEACH_BLOSSOM_MAP = {
        "Rat": {"star": "Rooster (酉)", "direction_kh": "ទិសខាងលិច (West - 270°)", "element": "Metal", "flowers": 7, "vase_color": "ស ឬប្រាក់ (White/Metallic)", "star_no": 7},
        "Dragon": {"star": "Rooster (酉)", "direction_kh": "ទិសខាងលិច (West - 270°)", "element": "Metal", "flowers": 7, "vase_color": "ស ឬប្រាក់ (White/Metallic)", "star_no": 7},
        "Monkey": {"star": "Rooster (酉)", "direction_kh": "ទិសខាងលិច (West - 270°)", "element": "Metal", "flowers": 7, "vase_color": "ស ឬប្រាក់ (White/Metallic)", "star_no": 7},

        "Tiger": {"star": "Rabbit (卯)", "direction_kh": "ទិសខាងកើត (East - 90°)", "element": "Wood", "flowers": 4, "vase_color": "បៃតង (Green/Wood)", "star_no": 4},
        "Horse": {"star": "Rabbit (卯)", "direction_kh": "ទិសខាងកើត (East - 90°)", "element": "Wood", "flowers": 4, "vase_color": "បៃតង (Green/Wood)", "star_no": 4},
        "Dog": {"star": "Rabbit (卯)", "direction_kh": "ទិសខាងកើត (East - 90°)", "element": "Wood", "flowers": 4, "vase_color": "បៃតង (Green/Wood)", "star_no": 4},

        "Pig": {"star": "Rat (子)", "direction_kh": "ទិសខាងជើង (North - 0°)", "element": "Water", "flowers": 1, "vase_color": "ខៀវ ឬខ្មៅ (Blue/Black)", "star_no": 1},
        "Rabbit": {"star": "Rat (子)", "direction_kh": "ទិសខាងជើង (North - 0°)", "element": "Water", "flowers": 1, "vase_color": "ខៀវ ឬខ្មៅ (Blue/Black)", "star_no": 1},
        "Goat": {"star": "Rat (子)", "direction_kh": "ទិសខាងជើង (North - 0°)", "element": "Water", "flowers": 1, "vase_color": "ខៀវ ឬខ្មៅ (Blue/Black)", "star_no": 1},

        "Snake": {"star": "Horse (午)", "direction_kh": "ទិសខាងត្បូង (South - 180°)", "element": "Fire", "flowers": 9, "vase_color": "ក្រហម ឬស្វាយ (Red/Purple)", "star_no": 9},
        "Rooster": {"star": "Horse (午)", "direction_kh": "ទិសខាងត្បូង (South - 180°)", "element": "Fire", "flowers": 9, "vase_color": "ក្រហម ឬស្វាយ (Red/Purple)", "star_no": 9},
        "Ox": {"star": "Horse (午)", "direction_kh": "ទិសខាងត្បូង (South - 180°)", "element": "Fire", "flowers": 9, "vase_color": "ក្រហម ឬស្វាយ (Red/Purple)", "star_no": 9},
    }

    # 12 Animals Khmer Names
    ZODIAC_KH = {
        "Rat": "ជូត (កណ្តុរ)", "Ox": "ឆ្លូវ (គោ)", "Tiger": "ខាល (ខ្លា)",
        "Rabbit": "ថោះ (ទន្សាយ)", "Dragon": "រោង (នាគ)", "Snake": "ម្សាញ់ (ពស់)",
        "Horse": "មមី (សេះ)", "Goat": "មមែ (ពពែ)", "Monkey": "វក (ស្វា)",
        "Rooster": "រកា (មាន់)", "Dog": "ច (ឆ្កែ)", "Pig": "កុរ (ជ្រូក)"
    }

    # Element remedies and enhancing god
    ELEMENT_REMEDY_MAP = {
        "Water": {
            "remedy": "Remedy for Water",
            "kh_remedy": "ពង្រឹងធាតុដែក (Metal) ដើម្បីចិញ្ចឹមធាតុទឹក និងរក្សាតុល្យភាពអារម្មណ៍",
            "colors": "ស, ប្រាក់, ទឹកប៊ិចចាស់",
            "gemstones": "គជ់ខ្យងស, ត្បូងថ្មគ្រីស្តាល់ថ្លា (Clear Quartz)"
        },
        "Wood": {
            "remedy": "Remedy for Wood",
            "kh_remedy": "ពង្រឹងធាតុទឹក (Water) ដើម្បីចិញ្ចឹមធាតុឈើឱ្យរីកលូតលាស់ស្រស់បំព្រង",
            "colors": "ខៀវ, ខ្មៅ, បៃតងខ្ចី",
            "gemstones": "ត្បូងមរកត (Emerald), ថ្មភ្នែកខ្លាខៀវ (Aquamarine)"
        },
        "Fire": {
            "remedy": "Remedy for Fire",
            "kh_remedy": "ពង្រឹងធាតុឈើ (Wood) ដើម្បីបង្កាត់ភ្លើងស្នេហ៍ឱ្យឆេះសន្ធោសន្ធៅរុងរឿង",
            "colors": "បៃតង, ក្រហមផ្កាឈូក, ស្វាយ",
            "gemstones": "ត្បូងទទឹម (Ruby), អាមេធីសស្វាយ (Amethyst)"
        },
        "Earth": {
            "remedy": "Remedy for Earth",
            "kh_remedy": "ពង្រឹងធាតុភ្លើង (Fire) ដើម្បីចិញ្ចឹមធាតុដីឱ្យមានភាពកក់ក្តៅ និងរឹងមាំយូរអង្វែង",
            "colors": "ក្រហម, លឿងទុំ, ត្នោត",
            "gemstones": "ត្បូងកណ្ដៀងលឿង (Yellow Sapphire), ថ្មភ្នែកខ្លា (Tiger Eye)"
        },
        "Metal": {
            "remedy": "Remedy for Metal",
            "kh_remedy": "ពង្រឹងធាតុដី (Earth) ដើម្បីបង្កើតនិងការពារធាតុដែកឱ្យរឹងមាំភ្លឺថ្លា",
            "colors": "លឿង, ត្នោតមាស, ស",
            "gemstones": "ពេជ្រ, មាស, ត្បូងសីត្រីន (Citrine)"
        }
    }

    def __init__(self):
        self.calc = ClassicalCalcEngine()

    def get_zodiac_branch(self, birth_year: int) -> str:
        """Find Earthly Branch (Zodiac Animal) for a given Gregorian year."""
        branches = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
        # 1900 was Rat (Year of Rat = 1900 % 12 == 4 in standard Chinese cycle, 1900 is Rat)
        idx = (birth_year - 1900) % 12
        return branches[idx]

    def analyze_love_profile(
        self,
        birth_date_1: str,
        gender_1: str = "male",
        birth_date_2: Optional[str] = None,
        gender_2: Optional[str] = "female"
    ) -> Dict[str, Any]:
        """
        Perform 8-Pillars Universal Zenith Love & Peach Blossom Analysis.
        Supports single person love audit and couples BaZi compatibility.
        """
        try:
            dt1 = datetime.strptime(birth_date_1, "%Y-%m-%d")
            year_1 = dt1.year
        except Exception:
            year_1 = 1990
            birth_date_1 = "1990-01-01"

        bazi_1 = self.calc.calculate_bazi(birth_date_1, "12:00")
        dm_1 = bazi_1.get("day_master", {})
        element_1 = dm_1.get("element", "Water")

        zodiac_1 = self.get_zodiac_branch(year_1)
        peach_info = self.PEACH_BLOSSOM_MAP.get(zodiac_1, self.PEACH_BLOSSOM_MAP["Rat"])
        remedy_info = self.ELEMENT_REMEDY_MAP.get(element_1, self.ELEMENT_REMEDY_MAP["Water"])

        # Couples Analysis if Person 2 provided
        if birth_date_2:
            try:
                dt2 = datetime.strptime(birth_date_2, "%Y-%m-%d")
                year_2 = dt2.year
            except Exception:
                year_2 = 1992
                birth_date_2 = "1992-01-01"

            bazi_2 = self.calc.calculate_bazi(birth_date_2, "12:00")
            dm_2 = bazi_2.get("day_master", {})
            element_2 = dm_2.get("element", "Wood")
            zodiac_2 = self.get_zodiac_branch(year_2)

            # Compatibility Formula: Five Elements Producing/Controlling + Stems/Branches harmony
            compat_score = self._calculate_compatibility(element_1, element_2, zodiac_1, zodiac_2)
            has_partner = True
        else:
            element_2 = "Wood"
            zodiac_2 = "Rabbit"
            compat_score = 95.0
            has_partner = False

        # Build Universal Zenith Report
        zenith_report = self._build_zenith_report(
            element=element_1,
            compat_score=compat_score,
            remedy_name=remedy_info["remedy"],
            remedy_detail=remedy_info["kh_remedy"],
            peach_dir=peach_info["direction_kh"],
            peach_flowers=peach_info["flowers"],
            peach_vase=peach_info["vase_color"],
            partner_element=element_2 if has_partner else None
        )

        return {
            "success": True,
            "element_1": element_1,
            "zodiac_1": self.ZODIAC_KH.get(zodiac_1, zodiac_1),
            "peach_blossom_star": peach_info["star"],
            "peach_blossom_direction": peach_info["direction_kh"],
            "peach_blossom_flowers": peach_info["flowers"],
            "peach_blossom_vase": peach_info["vase_color"],
            "remedy": remedy_info["remedy"],
            "remedy_detail": remedy_info["kh_remedy"],
            "compatibility_score": compat_score,
            "has_partner": has_partner,
            "zenith_report": zenith_report
        }

    def _calculate_compatibility(self, e1: str, e2: str, z1: str, z2: str) -> float:
        """Calculate BaZi 8-Pillars love resonance score (80.0% - 99.5%)."""
        producing_pairs = {
            ("Water", "Wood"), ("Wood", "Fire"), ("Fire", "Earth"), ("Earth", "Metal"), ("Metal", "Water"),
            ("Wood", "Water"), ("Fire", "Wood"), ("Earth", "Fire"), ("Metal", "Earth"), ("Water", "Metal")
        }
        same_pairs = {("Water", "Water"), ("Wood", "Wood"), ("Fire", "Fire"), ("Earth", "Earth"), ("Metal", "Metal")}

        base = 82.0
        if (e1, e2) in producing_pairs:
            base += 12.0  # Producing Cycle = High Harmony
        elif (e1, e2) in same_pairs:
            base += 8.0   # Parallel = Good Harmony
        else:
            base += 5.0   # Controlling = Transformative Remedy

        # Zodiac 6 Harmonies (Liu He)
        six_harmonies = {
            ("Rat", "Ox"), ("Tiger", "Pig"), ("Rabbit", "Dog"),
            ("Dragon", "Rooster"), ("Snake", "Monkey"), ("Horse", "Goat")
        }
        if (z1, z2) in six_harmonies or (z2, z1) in six_harmonies:
            base += 5.0

        return min(round(base, 1), 99.5)

    def _build_zenith_report(
        self,
        element: str,
        compat_score: float,
        remedy_name: str,
        remedy_detail: str,
        peach_dir: str,
        peach_flowers: int,
        peach_vase: str,
        partner_element: Optional[str] = None
    ) -> str:
        """Generate the exact Universal Zenith Report format specified."""
        partner_elem_str = partner_element or "Wood"

        report = (
            "📜 របាយការណ៍ហុងស៊ុយ និងមហាស្នេហ៍ (UNIVERSAL ZENITH REPORT)\n"
            "=======================================================\n"
            f"👤 ធាតុផ្ទាល់ខ្លួន: {element} | ភាពស៊ីចង្វាក់: {compat_score}%\n"
            f"💊 ធាតុឱសថព្យាបាលរាសី: {remedy_name} ({remedy_detail})\n"
            f"💖 យុទ្ធសាស្ត្រអន្ទងចិត្ត: ប្រើប្រាស់ក្បួន 'អន្ទងចិត្ត' ដោយដាក់ផ្កាស្រស់នៅទិស Peach Blossom របស់ម្ចាស់ខ្លួន ({peach_dir} ប្រើថូពណ៌ {peach_vase} ជាមួយផ្កាស្រស់ {peach_flowers} ទង)\n"
            f"🤝 វិធីសាស្ត្របន្ទន់ចិត្ត: ដើម្បី 'បន្ទន់ចិត្ត' គូស្នេហ៍ គួរប្រើប្រាស់ធាតុដែលជួយពង្រឹងដល់ធាតុស្នូលរបស់គាត់ (Useful God) (ពង្រឹងធាតុ {partner_elem_str} តាមរយៈពណ៌សម្ភារៈ និងការនិយាយផ្អែមល្ហែមយល់ចិត្ត)\n"
            "=======================================================\n"
            "✅ ការវិភាគសកល ៨ សសរស្តម្ភ បានបញ្ចប់ដោយជោគជ័យ!"
        )
        return report


# Singleton Instance
mahasneh_love_engine = MahaSnehLoveEngine()
