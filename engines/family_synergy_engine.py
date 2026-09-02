"""
Supreme Feng Shui AGI System - Family Synergy & Lineage BaZi Engine
Pillar 10: Unified Household Feng Shui & Multi-Member Energy Balance

Manages unlimited dependent family members (Self, Spouse, Children, Parents, etc.)
with 100% deterministic BaZi calculations, Main User Tai Chi Dominance,
Five Elements Household Balance, Clashes/Harmonies Matrix, and Bedroom Allocations.
Zero model retraining needed - 100% zero-hallucination pure mathematical computation.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import logging

from engines.classical_calc import ClassicalCalcEngine
from engines.celestial_astrology_engine import CelestialAstrologyEngine

logger = logging.getLogger("SupremeFengShui.FamilySynergy")


class FamilySynergyEngine:
    """Calculates comprehensive family-wide Feng Shui synergy and BaZi harmony."""

    RELATION_MAP = {
        "ខ្ញុំ": ("self", "ខ្ញុំ (ម្ចាស់ផ្ទះ/មេគ្រួសារ)", "male"),
        "self": ("self", "ខ្ញុំ (ម្ចាស់ផ្ទះ/មេគ្រួសារ)", "male"),
        "me": ("self", "ខ្ញុំ (ម្ចាស់ផ្ទះ/មេគ្រួសារ)", "male"),
        "ប្តី": ("spouse", "ស្វាមី (ប្តី)", "male"),
        "husband": ("spouse", "ស្វាមី (ប្តី)", "male"),
        "ប្រពន្ធ": ("spouse", "ភរិយា (ប្រពន្ធ)", "female"),
        "wife": ("spouse", "ភរិយា (ប្រពន្ធ)", "female"),
        "គូស្នេហ៍": ("spouse", "គូស្នេហ៍/ដៃគូ", "female"),
        "កូនស្រី": ("daughter", "កូនស្រី", "female"),
        "daughter": ("daughter", "កូនស្រី", "female"),
        "កូនប្រុស": ("son", "កូនប្រុស", "male"),
        "son": ("son", "កូនប្រុស", "male"),
        "កូន": ("child", "កូន", "male"),
        "ឪពុក": ("father", "ឪពុក", "male"),
        "ឳពុក": ("father", "ឪពុក", "male"),
        "father": ("father", "ឪពុក", "male"),
        "ម្តាយ": ("mother", "ម្តាយ", "female"),
        "mother": ("mother", "ម្តាយ", "female"),
        "បងប្រុស": ("brother", "បងប្រុស", "male"),
        "ប្អូនប្រុស": ("brother", "ប្អូនប្រុស", "male"),
        "បងស្រី": ("sister", "បងស្រី", "female"),
        "ប្អូនស្រី": ("sister", "ប្អូនស្រី", "female"),
        "ផ្សេងៗ": ("other", "សមាជិកផ្សេងទៀត", "male"),
        "other": ("other", "សមាជិកផ្សេងទៀត", "male")
    }

    ZODIAC_NAMES = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
    ZODIAC_KH = {
        "Rat": "ជូត (កណ្តុរ)", "Ox": "ឆ្លូវ (គោ)", "Tiger": "ខាល (ខ្លា)",
        "Rabbit": "ថោះ (ទន្សាយ)", "Dragon": "រោង (នាគ)", "Snake": "ម្សាញ់ (ពស់)",
        "Horse": "មមី (សេះ)", "Goat": "មមែ (ពពែ)", "Monkey": "វក (ស្វា)",
        "Rooster": "រកា (មាន់)", "Dog": "ច (ឆ្កែ)", "Pig": "កុរ (ជ្រូក)"
    }

    # 12 Earthly Branches Animal Clashes (六冲)
    CLASH_PAIRS = {
        ("Rat", "Horse"), ("Horse", "Rat"),
        ("Ox", "Goat"), ("Goat", "Ox"),
        ("Tiger", "Monkey"), ("Monkey", "Tiger"),
        ("Rabbit", "Rooster"), ("Rooster", "Rabbit"),
        ("Dragon", "Dog"), ("Dog", "Dragon"),
        ("Snake", "Pig"), ("Pig", "Snake")
    }

    # 12 Earthly Branches Six Harmonies (六合)
    SIX_HARMONIES = {
        ("Rat", "Ox"): "Metal", ("Ox", "Rat"): "Metal",
        ("Tiger", "Pig"): "Wood", ("Pig", "Tiger"): "Wood",
        ("Rabbit", "Dog"): "Fire", ("Dog", "Rabbit"): "Fire",
        ("Dragon", "Rooster"): "Metal", ("Rooster", "Dragon"): "Metal",
        ("Snake", "Monkey"): "Water", ("Monkey", "Snake"): "Water",
        ("Horse", "Goat"): "Earth", ("Goat", "Horse"): "Earth"
    }

    def __init__(self):
        self.calc = ClassicalCalcEngine()
        self.celestial = CelestialAstrologyEngine()

    def parse_relation(self, raw_input: str) -> Tuple[str, str, str]:
        """Normalize relation string into (relation_type, relation_label_kh, default_gender)."""
        cleaned = raw_input.strip().lower()
        for k, v in self.RELATION_MAP.items():
            if k in cleaned or cleaned in k:
                return v
        return ("other", raw_input.strip(), "male")

    def calculate_member_profile(
        self,
        birth_date: str,
        birth_time: str = "12:00",
        gender: str = "male"
    ) -> Dict[str, Any]:
        """Calculate individual BaZi, Day Master, Useful God, Zodiac, and Life Gua for a family member."""
        bazi = self.celestial.calculate_precision_bazi(birth_date, birth_time, gender)
        birth_year = int(birth_date.split("-")[0]) if "-" in birth_date else 1990
        
        # Calculate Zodiac animal
        zodiac_idx = (birth_year - 4) % 12
        zodiac_animal = self.ZODIAC_NAMES[zodiac_idx]

        gua_res = self.calc.calculate_life_gua(birth_year, gender)
        gua_data = gua_res.get("data", {}) if gua_res.get("success") else {}

        dm_info = bazi.get("day_master", {})
        dm_elem = dm_info.get("element", "Water")
        # Clean element string if contains "Yang" or "Yin"
        clean_elem = dm_elem.split()[0] if " " in dm_elem else dm_elem

        return {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "gender": gender,
            "day_master": clean_elem,
            "day_master_stem": dm_info.get("stem", "甲"),
            "useful_god": bazi.get("useful_god", "Metal & Water"),
            "zodiac_animal": zodiac_animal,
            "zodiac_kh": self.ZODIAC_KH.get(zodiac_animal, zodiac_animal),
            "life_gua": gua_data.get("life_gua", 1),
            "trigram": gua_data.get("trigram", "Kan"),
            "auspicious_directions": gua_data.get("auspicious_directions", {}),
            "five_elements_count": bazi.get("five_elements_count", {}),
            "four_pillars": bazi.get("four_pillars", {})
        }

    def analyze_family_synergy(
        self,
        family_members: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Unified Family Synergy Analysis centered around the Main User."""
        if not family_members:
            return {"success": False, "error": "No family members found for analysis."}

        # 1. Identify Main User (Self) vs Dependents
        main_user = None
        dependents = []
        for m in family_members:
            if m.get("relation_type") == "self" or str(m.get("relation_label", "")).startswith("ខ្ញុំ"):
                main_user = m
            else:
                dependents.append(m)

        if not main_user:
            main_user = family_members[0]
            dependents = family_members[1:]

        # 2. Household Five Elements Distribution
        household_elements = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}
        total_members = len(family_members)

        for m in family_members:
            elem = m.get("day_master", "Water")
            # Normalize element name
            for k in household_elements.keys():
                if k.lower() in elem.lower():
                    household_elements[k] += 1
                    break

        # 3. Inter-family Clashes & Harmonies
        harmonies_found = []
        clashes_found = []
        all_zodiacs = [(m.get("relation_label", m.get("name", "សមាជិក")), m.get("zodiac_animal", "Rat")) for m in family_members]

        for i in range(len(all_zodiacs)):
            for j in range(i + 1, len(all_zodiacs)):
                name1, z1 = all_zodiacs[i]
                name2, z2 = all_zodiacs[j]

                # Six Harmonies
                if (z1, z2) in self.SIX_HARMONIES:
                    harm_elem = self.SIX_HARMONIES[(z1, z2)]
                    harmonies_found.append({
                        "members": f"{name1} ({self.ZODIAC_KH.get(z1, z1)}) + {name2} ({self.ZODIAC_KH.get(z2, z2)})",
                        "type": "六合 (ត្រូវគ្នាកម្រិតកំពូល)",
                        "combined_element": harm_elem,
                        "description": f"បង្កើតថាមពលមេត្រីភាពធាតុ {harm_elem} ជួយឱ្យគ្រួសារមានសេចក្តីសុខ និងទ្រព្យសម្បត្តិហូរចូល។"
                    })

                # Six Clashes
                if (z1, z2) in self.CLASH_PAIRS:
                    clashes_found.append({
                        "members": f"{name1} ({self.ZODIAC_KH.get(z1, z1)}) vs {name2} ({self.ZODIAC_KH.get(z2, z2)})",
                        "type": "六冲 (ឆុងរាសី)",
                        "remedy": self._get_clash_remedy(z1, z2),
                        "description": "មានរលកធាតុឆុងគ្នា ងាយនឹងមានទំនាស់ពាក្យសម្តី ឬខ្វែងគំនិត។"
                    })

        # 4. Direction Allocations
        direction_allocations = []
        for m in family_members:
            label = m.get("relation_label", m.get("name", "សមាជិក"))
            gua = m.get("life_gua", 1)
            dirs = m.get("auspicious_directions", {})
            if isinstance(dirs, dict):
                best_dir = dirs.get("sheng_qi", "ទិសខាងកើត (East)")
                health_dir = dirs.get("tian_yi", "ទិសអាគ្នេយ៍ (Southeast)")
            else:
                best_dir = "ទិសខាងកើត (East)"
                health_dir = "ទិសអាគ្នេយ៍ (Southeast)"

            is_head = (m == main_user)
            role_rec = "បន្ទប់មេគ្រួសារ (Master Bedroom)" if is_head else "បន្ទប់គេងសមាជិក"
            direction_allocations.append({
                "member": label,
                "role": role_rec,
                "life_gua": gua,
                "best_bedroom_direction": best_dir,
                "health_direction": health_dir
            })

        # 5. Unified Household Remedy
        main_elem = main_user.get("day_master", "Water")
        household_remedy = self._calculate_household_remedy(main_elem, household_elements, clashes_found)

        return {
            "success": True,
            "total_members": total_members,
            "main_user": main_user,
            "dependents": dependents,
            "household_elements_distribution": household_elements,
            "harmonies": harmonies_found,
            "clashes": clashes_found,
            "direction_allocations": direction_allocations,
            "household_remedy": household_remedy
        }

    def _get_clash_remedy(self, z1: str, z2: str) -> str:
        """Provide specific Five Elements bridge remedy for zodiac clashes."""
        bridge_map = {
            ("Rat", "Horse"): "ប្រើប្រាស់ធាតុឈើ (Wood - រុក្ខជាតិបៃតង) ជាស្ពានសម្របសម្រួល (ទឹកចិញ្ចឹមឈើ ឈើបង្កើតភ្លើង)",
            ("Ox", "Goat"): "ប្រើប្រាស់ធាតុដែក (Metal - វត្ថុពណ៌ស/ប្រាក់) ដើម្បីបន្ធូរបន្ថយភាពរឹងរូសនៃធាតុដី",
            ("Tiger", "Monkey"): "ប្រើប្រាស់ធាតុទឹក (Water - ថូទឹកស្អាត/ពណ៌ខៀវ) ជាស្ពានសម្របសម្រួល (ដែកចិញ្ចឹមទឹក ទឹកចិញ្ចឹមឈើ)",
            ("Rabbit", "Rooster"): "ប្រើប្រាស់ធាតុទឹក (Water) សម្របសម្រួលរវាងដែក និងឈើ",
            ("Dragon", "Dog"): "ប្រើប្រាស់ធាតុដែក (Metal) ឬភ្លើងទន់ភ្លន់ដើម្បីស្រូបយកភាពតានតឹង",
            ("Snake", "Pig"): "ប្រើប្រាស់ធាតុឈើ (Wood) ជាស្ពានសម្របសម្រួលរវាងទឹក និងភ្លើង"
        }
        for k, v in bridge_map.items():
            if (z1, z2) == k or (z2, z1) == k:
                return v
        return "ប្រើប្រាស់ធាតុទឹក ឬរុក្ខជាតិបៃតងតូចៗជាស្ពានសម្របសម្រួល"

    def _calculate_household_remedy(
        self,
        main_element: str,
        elements_dist: Dict[str, int],
        clashes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Determine unified household remedy centered around the Main User."""
        clean_elem = "Water"
        for k in ["Water", "Wood", "Fire", "Earth", "Metal"]:
            if k.lower() in str(main_element).lower():
                clean_elem = k
                break

        remedy_map = {
            "Water": {
                "element": "Metal & Water (ដែក និងទឹក)",
                "action": "ពង្រឹងធាតុដែក និងទឹកនៅក្នុងផ្ទះ ដើម្បីចិញ្ចឹមរាសីមេគ្រួសារ និងបង្កើតភាពត្រជាក់ត្រជុំក្នុងគ្រួសារ",
                "decor": "ប្រើថូកែវថ្លា វត្ថុតុបតែងពណ៌ស/ប្រាក់/ទឹកប៊ិច និងរៀបចំឱ្យខ្យល់អាកាសចេញចូលស្រួល",
                "colors": "ពណ៌ស ពណ៌ប្រាក់ ពណ៌មាស និងពណ៌ខៀវចាស់"
            },
            "Wood": {
                "element": "Water & Wood (ទឹក និងឈើ)",
                "action": "ពង្រឹងរុក្ខជាតិបៃតង និងធាតុទឹកដើម្បីជំរុញការលូតលាស់ សុខភាព និងការរៀនសូត្ររបស់កូនៗ",
                "decor": "ដាំរុក្ខជាតិស្លឹកមូលបៃតងក្នុងផ្ទះ និងមានចលនាទឹកហូរនាំលាភ",
                "colors": "ពណ៌បៃតង ពណ៌ផ្ទៃមេឃ និងពណ៌ទឹកប៊ិច"
            },
            "Fire": {
                "element": "Wood & Fire (ឈើ និងភ្លើង)",
                "action": "ពង្រឹងពន្លឺកក់ក្តៅ និងថាមពលស្រឡាញ់រាប់អាន ដើម្បីឱ្យគ្រួសារមានភាពស្និទ្ធស្នាល និងកេរ្តិ៍ឈ្មោះល្បីល្បាញ",
                "decor": "ប្រើចង្កៀងបំភ្លឺពន្លឺលឿងទន់ និងតុបតែងផ្កាស្រស់ពណ៌ក្រហម/ផ្កាឈូក",
                "colors": "ពណ៌ក្រហម ពណ៌ផ្កាឈូក ពណ៌ស្វាយ និងពណ៌បៃតង"
            },
            "Earth": {
                "element": "Fire & Earth (ភ្លើង និងដី)",
                "action": "ពង្រឹងភាពរឹងមាំ លំនឹងចិត្ត និងទ្រព្យសម្បត្តិស្តុកស្តម្ភយូរអង្វែង",
                "decor": "ប្រើប្រាស់ថ្មគ្រីស្តាល់ធម្មជាតិ សេរ៉ាមិច និងកម្រាលព្រំពណ៌កក់ក្តៅ",
                "colors": "ពណ៌លឿង ពណ៌ត្នោត ពណ៌កាហ្វេ និងពណ៌ការ៉ុត"
            },
            "Metal": {
                "element": "Earth & Metal (ដី និងដែក)",
                "action": "ពង្រឹងភាពច្បាស់លាស់ វិន័យ សេចក្តីថ្លៃថ្នូរ និងការការពារឧបទ្រពចង្រៃ",
                "decor": "ប្រើប្រាស់កណ្តឹងខ្យល់លោហៈធាតុ ៦ បំពង់ និងវត្ថុតុបតែងធ្វើពីលង្ហិន/មាស",
                "colors": "ពណ៌ស ពណ៌ប្រាក់ ពណ៌មាស និងពណ៌លឿងខ្ចី"
            }
        }
        return remedy_map.get(clean_elem, remedy_map["Water"])

    def generate_family_synergy_report(
        self,
        family_members: List[Dict[str, Any]]
    ) -> str:
        """
        Generate comprehensive, clean Family Synergy Report strictly without **, ++, ==, or border symbols.
        Calibrated for Telegram and instant AGI Q&A consultation.
        """
        analysis = self.analyze_family_synergy(family_members)
        if not analysis.get("success"):
            return "❌ មិនមានទិន្នន័យសមាជិកគ្រួសារគ្រប់គ្រាន់សម្រាប់វិភាគឡើយ។ សូមប្រើ /data ដើម្បីបញ្ចូល។"

        main_u = analysis["main_user"]
        deps = analysis["dependents"]
        elements_dist = analysis["household_elements_distribution"]
        harmonies = analysis["harmonies"]
        clashes = analysis["clashes"]
        allocations = analysis["direction_allocations"]
        remedy = analysis["household_remedy"]

        main_zodiac = self.ZODIAC_KH.get(main_u.get("zodiac_animal", "Rat"), main_u.get("zodiac_animal", "Rat"))

        report = (
            "📜 របាយការណ៍ហុងស៊ុយរាសីគ្រួសាររួម (UNIFIED FAMILY FENG SHUI REPORT)\n\n"
            "🌟 ប្រព័ន្ធបញ្ញាសិប្បនិម្មិតកម្រិតកំពូល SUPREME FENG SHUI AGI\n"
            f"👑 មេគ្រួសារចម្បង (Tai Chi Pivot): {main_u.get('relation_label', 'ខ្ញុំ')} (ធាតុ {main_u.get('day_master', 'Water')} ឆ្នាំ {main_zodiac})\n"
            f"👨‍👩‍👧‍👦 សមាជិករួមបន្ទុកសរុប: {analysis['total_members']} នាក់\n\n"
            "✨ ១. បញ្ជីសមាជិកគ្រួសារ និងធាតុប្រចាំជោគជតា\n"
        )

        for m in family_members:
            label = m.get("relation_label", m.get("name", "សមាជិក"))
            name_str = f" [{m.get('name')}]" if m.get("name") else ""
            b_date = m.get("birth_date", "")
            b_time = m.get("birth_time", "12:00")
            elem = m.get("day_master", "Water")
            zodiac_raw = m.get("zodiac_animal", "Rat")
            zodiac_kh = self.ZODIAC_KH.get(zodiac_raw, zodiac_raw)
            gua = m.get("life_gua", 1)
            report += f"• {label}{name_str}: កើត {b_date} ម៉ោង {b_time} | ធាតុ {elem} (ឆ្នាំ {zodiac_kh}) | Life Gua {gua}\n"

        report += (
            f"\n⚖️ ២. តុល្យភាពធាតុទាំង ៥ រួមក្នុងគេហដ្ឋាន\n"
            f"ឈើ:{elements_dist.get('Wood', 0)} | ភ្លើង:{elements_dist.get('Fire', 0)} | ដី:{elements_dist.get('Earth', 0)} | ដែក:{elements_dist.get('Metal', 0)} | ទឹក:{elements_dist.get('Water', 0)}\n\n"
            "🤝 ៣. ភាពស៊ីចង្វាក់ និងក្បួនឆុងរាសីក្នុងគ្រួសារ\n"
        )

        if harmonies:
            report += "• មហាសម្ព័ន្ធមេត្រីភាព (Harmonies):\n"
            for h in harmonies:
                report += f"  - {h['members']}: {h['type']} ➔ {h['description']}\n"
        else:
            report += "• មិនមានសត្វឆ្នាំឆុងធ្ងន់ធ្ងរឡើយ រាសីគ្រួសារមានសភាពនឹងនរ។\n"

        if clashes:
            report += "• ចំណុចត្រូវប្រយ័ត្ន និងដំណោះស្រាយ (Clashes & Remedies):\n"
            for c in clashes:
                report += f"  - {c['members']}: {c['type']} ➔ ដំណោះស្រាយ: {c['remedy']}\n"

        report += "\n🛏️ ៤. ក្បួនបែងចែកទិសបន្ទប់គេងក្នុងគេហដ្ឋាន\n"
        for a in allocations:
            report += f"• {a['member']} ({a['role']}): ទិសទ្រព្យលាភ {a['best_bedroom_direction']} | ទិសសុខភាព {a['health_direction']}\n"

        report += (
            f"\n💊 ៥. ធាតុឱសថហុងស៊ុយរួមសម្រាប់គេហដ្ឋាន\n"
            f"• ធាតុឱសថចម្បង: {remedy['element']}\n"
            f"• សកម្មភាពអនុវត្ត: {remedy['action']}\n"
            f"• ពណ៌នាំលាភគ្រួសារ: {remedy['colors']}\n"
            f"• ការរៀបចំតុបតែង: {remedy['decor']}\n\n"
            "✅ ការវិភាគរាសីគ្រួសារទាំងមូលត្រូវបានថ្លឹងថ្លែងដោយជោគជ័យ!"
        )

        return report.strip()


# Singleton Instance
family_synergy_engine = FamilySynergyEngine()
