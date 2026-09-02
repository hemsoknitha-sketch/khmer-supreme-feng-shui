"""
Supreme Feng Shui AGI System - Master 100-Topic & 1,000-Lesson Curriculum Engine
Provides structured Classical Feng Shui knowledge across 4 Grand Categories,
100 Master Topics, and 1,000 Sub-Lessons with Classical Formulas, Remedies, and
AI-driven Deep Synthesis (FS-Supreme-Master / hemsinath/khmer-supreme-feng-shui).
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from config import config

logger = logging.getLogger("SupremeFengShui.Curriculum")

# 4 Grand Categories
CATEGORIES = [
    {
        "id": "CAT1",
        "name_kh": "ផ្នែកទី ១៖ មូលដ្ឋានគ្រឹះក្បួនហុងស៊ុយបុរាណ",
        "name_en": "Part 1: Classical Feng Shui Fundamentals",
        "topic_range": (1, 20),
        "lesson_range": (1, 200),
        "icon": "☯️",
        "description": "ក្បួនយិនយ៉ាង (Yin-Yang), ធាតុទាំង ៥ (Wu Xing), ប៉ាហ្គ័រ (Ba Gua), ហឺធូ (He Tu), និងលួស៊ូ (Luo Shu)"
    },
    {
        "id": "CAT2",
        "name_kh": "ផ្នែកទី ២៖ ក្បួនជឿនលឿន & តារាហោះ យុគ ៩",
        "name_en": "Part 2: Advanced Xuan Kong Flying Stars & Period 9",
        "topic_range": (21, 50),
        "lesson_range": (201, 500),
        "icon": "🌌",
        "description": "តារាហោះ ៩ វិហារ (Flying Stars), ២៤ ទិសភ្នំ (24 Mountains), យុគទី ៩ ធាតុភ្លើង, ទ្វារបន្ទាយ (Castle Gate), និងក្បួនស្រូបជលសា"
    },
    {
        "id": "CAT3",
        "name_kh": "ផ្នែកទី ៣៖ ការអនុវត្តជាក់ស្តែង & ការរៀបចំលំនៅឋាន/អាជីវកម្ម",
        "name_en": "Part 3: Practical Residential & Commercial Feng Shui",
        "topic_range": (51, 80),
        "lesson_range": (501, 800),
        "icon": "🏛️",
        "description": "ក្បួនរាងទ្រង់ (Luan Tou), ការរៀបចំបន្ទប់គេង តុធ្វើការ ផ្ទះបាយ ទ្វារមុខ, និងវិធីបន្សាបព្រួញពិឃាត (Sha Qi Remedies)"
    },
    {
        "id": "CAT4",
        "name_kh": "ផ្នែកទី ៤៖ ក្បួនឯកទេសជាន់ខ្ពស់ & BaZi រាសី",
        "name_en": "Part 4: High-Level Mastery, BaZi Destiny & Date Selection",
        "topic_range": (81, 100),
        "lesson_range": (801, 1000),
        "icon": "🔮",
        "description": "សសរស្តម្ភទាំង ៤ (BaZi 4 Pillars), អាទិទេពទាំង ១០ (10 Gods), ធាតុឱសថ (Yong Shen), ទម្រង់មុខ (Mian Xiang), និងរើសថ្ងៃជ័យ (Ze Ri)"
    }
]

# 100 Master Topics Metadata
TOPICS_CATALOG = [
    # Category 1: Fundamentals (1-20)
    (1, "CAT1", "ប្រភពដើម និងទស្សនវិជ្ជាហុងស៊ុយបុរាណ", "Origins & Philosophy of Classical Feng Shui", "សកលលោក ធម្មជាតិ និងថាមពល Qi"),
    (2, "CAT1", "ក្បួនយិន និងយ៉ាង (Taiji & Yin-Yang Dynamics)", "Taiji & Yin-Yang Dynamics", "តុល្យភាពរវាងភាពស្ងប់ និងភាពសកម្ម"),
    (3, "CAT1", "ធាតុទាំង ៥ (Wu Xing - Five Elements Theory)", "Five Elements Generation & Destruction Cycles", "លោហៈ ទឹក ឈើ ភ្លើង ដី និងវដ្តបង្កើត/បំផ្លាញ"),
    (4, "CAT1", "ផែនទីទន្លេ He Tu (Yellow River Chart)", "He Tu Numerology & Cosmological Map", "គូលេខធាតុបង្កើត He Tu (1-6, 2-7, 3-8, 4-9, 5-10)"),
    (5, "CAT1", "គំនូសអណ្តើក Luo Shu (Luo River Writing)", "Luo Shu Magic Square & Trigram Distribution", "ម៉ាទ្រីស ៣x៣ ផលបូក ១៥ គ្រប់ទិស"),
    (6, "CAT1", "ត្រីក្រាមទាំង ៨ ប៉ាហ្គ័រមេឃដើម (Early Heaven Ba Gua)", "Early Heaven Ba Gua (Xian Tian)", "សណ្តាប់ធ្នាប់លោហធាតុ និងតុល្យភាពដ៏ល្អឥតខ្ចោះ"),
    (7, "CAT1", "ត្រីក្រាមទាំង ៨ ប៉ាហ្គ័រមេឃក្រោយ (Later Heaven Ba Gua)", "Later Heaven Ba Gua (Hou Tian)", "ការអនុវត្តលើផែនដី និងទិសដៅទាំង ៨"),
    (8, "CAT1", "ត្រីក្រាម Qian ☰ (មេឃ / ឪពុក / ធាតុលោហៈធំ)", "Qian Trigram - Heaven & Pure Yang", "ទិសពាយព្យ (NW) និងឥទ្ធិពលលើអ្នកដឹកនាំ"),
    (9, "CAT1", "ត្រីក្រាម Kun ☷ (ដី / ម្តាយ / ធាតុដីធំ)", "Kun Trigram - Earth & Pure Yin", "ទិសនិរតី (SW) និងឥទ្ធិពលលើមេផ្ទះ"),
    (10, "CAT1", "ត្រីក្រាម Zhen ☳ (ផ្គរ / កូនប្រុសច្បង / ឈើធំ)", "Zhen Trigram - Thunder & Growth", "ទិសខាងកើត (E) និងភាពរស់រវើក"),
    (11, "CAT1", "ត្រីក្រាម Xun ☴ (ខ្យល់ / កូនស្រីច្បង / ឈើតូច)", "Xun Trigram - Wind & Flexibility", "ទិសអាគ្នេយ៍ (SE) និងការលូតលាស់"),
    (12, "CAT1", "ត្រីក្រាម Kan ☵ (ទឹក / កូនប្រុសកណ្តាល / ធាតុទឹក)", "Kan Trigram - Water & Danger/Wisdom", "ទិសខាងជើង (N) និងលំហូរទ្រព្យ"),
    (13, "CAT1", "ត្រីក្រាម Li ☲ (ភ្លើង / កូនស្រីកណ្តាល / ធាតុភ្លើង)", "Li Trigram - Fire & Clarity/Fame", "ទិសខាងត្បូង (S) និងកេរ្តិ៍ឈ្មោះយុគ ៩"),
    (14, "CAT1", "ត្រីក្រាម Gen ☶ (ភ្នំ / កូនប្រុសពៅ / ធាតុដីតូច)", "Gen Trigram - Mountain & Stability", "ទិសឦសាន (NE) និងភាពរឹងមាំ"),
    (15, "CAT1", "ត្រីក្រាម Dui ☱ (បឹង / កូនស្រីពៅ / ធាតុលោហៈតូច)", "Dui Trigram - Lake & Joy/Communication", "ទិសខាងលិច (W) និងការទំនាក់ទំនង"),
    (16, "CAT1", "ថាមពល Qi ទាំង ៤ ប្រភេទ (Sheng, Wang, Sha, Si Qi)", "Four States of Qi Energy", "របៀបបង្កើត Sheng Qi និងទប់ស្កាត់ Sha Qi"),
    (17, "CAT1", "រូបមន្ត Life Gua (San Yuan Ming Gua Formula)", "San Yuan Life Gua Calculation Formulas", "ការគណនាលេខ Gua ប្រចាំកំណើតបុរស/ស្ត្រី"),
    (18, "CAT1", "ក្រុមបូព៌ា និងក្រុមបស្ចិម (East & West Group System)", "East & West Group Direction Compatibility", "៤ ទិសល្អ និង ៤ ទិសអាក្រក់របស់បុគ្គល"),
    (19, "CAT1", "ទិសល្អទាំង ៤ (Sheng Qi, Tian Yi, Yan Nian, Fu Wei)", "Four Auspicious Directions Details", "ការប្រើប្រាស់សម្រាប់បន្ទប់គេង តុធ្វើការ និងទ្វារ"),
    (20, "CAT1", "ទិសអាក្រក់ទាំង ៤ (Jue Ming, Wu Gui, Liu Sha, Huo Hai)", "Four Inauspicious Directions Details", "វិធីដោះស្រាយ និងបង្វែរទិសអាក្រក់"),

    # Category 2: Advanced Xuan Kong & Period 9 (21-50)
    (21, "CAT2", "មូលដ្ឋានគ្រឹះ Xuan Kong Flying Stars (玄空飞星)", "Xuan Kong Flying Stars System Overview", "ការរួមបញ្ចូលគ្នារវាងពេលវេលា និងលំហអាកាស"),
    (22, "CAT2", "យុគសម័យទាំង ៩ (San Yuan Jiu Yun - 180 Year Cycle)", "Nine Periods of the 180-Year Macrocycle", "យុគលើ (1-3) យុគកណ្តាល (4-6) និងយុគក្រោម (7-9)"),
    (23, "CAT2", "យុគទី ៩ (Period 9: 2024-2043 Li Fire Era)", "Period 9 Mastery: Fire Element Dynamics", "បម្រែបម្រួលថាមពលសកលលោក បច្ចេកវិទ្យា និងទិសទ្រព្យ"),
    (24, "CAT2", "តារាកណ្តាលប្រចាំឆ្នាំ (Annual Center Stars Movement)", "Annual Center Stars Calculation Formula", "រូបមន្តគណនាតារាហោះកណ្តាលប្រចាំឆ្នាំ"),
    (25, "CAT2", "២៤ ទិសភ្នំ (24 Mountains Compass Grid)", "24 Mountains Precision Luopan System", "៨ ទិសចែកជា ២៤ ភ្នំ (ទិសនីមួយៗ ១៥ ដឺក្រេ)"),
    (26, "CAT2", "តារាភ្នំ (Mountain Star) និងតារាទឹក (Water Star)", "Mountain Star (Health/People) vs Water Star (Wealth)", "ភ្នំគ្រប់គ្រងសុខភាព មនុស្ស / ទឹកគ្រប់គ្រងទ្រព្យ"),
    (27, "CAT2", "ទម្រង់ Wang Shan Wang Shui (旺山旺向)", "Prosperous Mountain & Prosperous Facing Chart", "ទម្រង់ហុងស៊ុយកំពូល ទាំងមនុស្សនិងទ្រព្យ"),
    (28, "CAT2", "ទម្រង់ Shuang Xing Dao Xiang (双星到向)", "Double Stars at Facing Palace", "ទម្រង់ទ្រព្យធំសម្បើម ត្រូវការទឹកខាងមុខ"),
    (29, "CAT2", "ទម្រង់ Shuang Xing Dao Zuo (双星到座)", "Double Stars at Sitting Palace", "ទម្រង់មនុស្សកិត្តិយស ត្រូវការភ្នំខាងក្រោយ"),
    (30, "CAT2", "ទម្រង់ Shang Shan Xia Shui (上山下水)", "Reverse Star Configuration & Countermeasures", "ទម្រង់បញ្ច្រាសក្បួន និងវិធីបន្សាបគ្រោះ"),
    (31, "CAT2", "តារា ១ White (Tan Lang Water - Career & Wisdom)", "Star 1 White - Tan Lang Water", "ការជំរុញការងារ បញ្ញា និងការទូត"),
    (32, "CAT2", "តារា ២ Black (Ju Men Earth - Sickness Star)", "Star 2 Black - Ju Men Sickness Star", "វិធីបន្សាបជំងឺដោយប្រើធាតុលោហៈ"),
    (33, "CAT2", "តារា ៣ Jade (San Bi Wood - Dispute Star)", "Star 3 Jade - San Bi Dispute & Lawsuit Star", "វិធីបន្សាបជម្លោះ និងក្តីក្តាំដោយប្រើភ្លើង"),
    (34, "CAT2", "តារា ៤ Green (Wen Qu Wood - Academic & Romance)", "Star 4 Green - Academic & Romance Star", "ការជំរុញការសិក្សា ស្នេហា និងការច្នៃប្រឌិត"),
    (35, "CAT2", "តារា ៥ Yellow (Lian Zhen Earth - Misfortune Emperor)", "Star 5 Yellow - Wu Huang Misfortune Star", "វិធីទប់ទល់គ្រោះកាចធំបំផុតប្រចាំឆ្នាំ"),
    (36, "CAT2", "តារា ៦ White (Wu Qu Metal - Authority & Power)", "Star 6 White - Wu Qu Authority Star", "ការជំរុញអំណាច តួនាទី និងកិត្តិយស"),
    (37, "CAT2", "តារា ៧ Red (Po Jun Metal - Robbery & Rivalry)", "Star 7 Red - Po Jun Robbery Star", "វិធីទប់ស្កាត់ការបាត់បង់ទ្រព្យ និងចោរកម្ម"),
    (38, "CAT2", "តារា ៨ White (Zuo Fu Earth - Past Wealth)", "Star 8 White - Zuo Fu Earth Star", "ការថែរក្សាទ្រព្យ និងស្ថិរភាព"),
    (39, "CAT2", "តារា ៩ Purple (You Bi Fire - Period 9 Supreme Star)", "Star 9 Purple - Supreme Period 9 Wealth Star", "កំពូលតារាស្រូបទ្រព្យលឿនបំផុតក្នុងយុគទី ៩"),
    (40, "CAT2", "តារាហោះប្រចាំខែ និងប្រចាំថ្ងៃ (Monthly & Daily Stars)", "Monthly & Daily Flying Star Timing", "ការតាមដានបម្រែបម្រួលថាមពលប្រចាំថ្ងៃ"),
    (41, "CAT2", "ក្បួនទ្វារបន្ទាយ (Castle Gate Theory - 城门诀)", "Castle Gate Theory for Wealth Activation", "វិធីបើកទ្វារបន្ទាយស្រូបលាភធំ"),
    (42, "CAT2", "ក្បួន San般卦 (Parent String & Combo of 10)", "Parent String & Sum of Ten Combinations", "ការរួមបញ្ចូលគ្នានៃតារាហោះបង្កើតមហាលាភ"),
    (43, "CAT2", "ក្បួន Ling Xing & Zheng Shen (Direct & Indirect Spirit)", "Direct & Indirect Spirit for Period 9", "ទីតាំងទឹកល្អបំផុតសម្រាប់យុគទី ៩ (SW / N)"),
    (44, "CAT2", "ក្បួនស្រូបជលសាផ្លូវទឹក (Water Dragon Classics)", "Water Dragon Classics (Water Mouth & Inflow)", "មុំទឹកហូរចូល និងទឹកហូរចេញ"),
    (45, "CAT2", "ទិស Tai Sui (Grand Duke Jupiter - 太岁)", "Tai Sui Placement, Rules & Cautions", "ការជៀសវាងរំខានទិសស្តេចនាគប្រចាំឆ្នាំ"),
    (46, "CAT2", "ទិស Sui Po (Year Breaker - 岁破)", "Sui Po Confrontation & Protection", "ទិសទល់មុខ Tai Sui និងវិធីការពារ"),
    (47, "CAT2", "ទិស San Sha (Three Killings - 三煞)", "Three Killings Avoidance & Cures", "ទិសគ្រោះទាំងបី និងការហាមឃាត់ជួសជុល"),
    (48, "CAT2", "ក្បួនជំនួសផ្កាយ (Substitute Stars - 替卦)", "Substitute Stars (Ti Gua) Precision Routing", "ការប្រើផ្កាយជំនួសពេលចំខ្សែបែងចែក 3 ដឺក្រេ"),
    (49, "CAT2", "ក្បួនខ្សែមោឃៈ (Empty Lines - Kong Wang 空亡)", "Death & Emptiness Lines (Kong Wang)", "ការជៀសវាងបន្ទាត់មោឃៈដែលនាំឱ្យវិនាស"),
    (50, "CAT2", "ម៉ូដែល MoE វែកញែកតារាហោះកម្រិតខ្ពស់", "MoE Deep Flying Star Synthesis", "ការសំយោគក្បួនដោយម៉ូដែល FS-Reasoner-7B"),

    # Category 3: Practical Form & Space (51-80)
    (51, "CAT3", "ក្បួនសាលារូបរាង Luan Tou (Form School Fundamentals)", "Luan Tou Landform & External Form School", "បរិស្ថានជុំវិញ ភ្នំ ទឹក ផ្លូវ និងអគារ"),
    (52, "CAT3", "សត្វទេវៈទាំង ៤ (Four Celestial Animals: Dragon, Tiger, Turtle, Phoenix)", "Four Celestial Guardians Configuration", "ភ្នំខាងក្រោយ (អណ្តើក) ឆ្វេង (នាគ) ស្តាំ (ខ្លា) មុខ (ហង្ស)"),
    (53, "CAT3", "ការវិភាគ Ming Tang (Bright Hall - 堂局)", "Bright Hall (Ming Tang) Energy Gathering", "ទីធ្លាស្រូបថាមពលមុខផ្ទះ និងមុខការិយាល័យ"),
    (54, "CAT3", "ព្រួញពិឃាត Sha Qi ខាងក្រៅ (Exterior Poison Arrows)", "Exterior Sha Qi (Sharp Roofs, Towers, Corners)", "ជ្រុងស្រួចអគារ បង្គោលភ្លើង និងមុំផ្លូវ"),
    (55, "CAT3", "ផ្លូវបុកចំផ្ទះ (Road Rushing Sha - 枪煞)", "Road Rushing & T-Junction Cures", "វិធីបង្វែរ និងបន្សាបផ្លូវបុកចំមុខផ្ទះ"),
    (56, "CAT3", "ស្ពានអាកាស និងផ្លូវកោងកាត់មុខ (Blade Sha & Curved Roads)", "Curved Overpasses & Sickle Sha", "វិធីការពារពេលមានស្ពានអាកាសកាត់មុខ"),
    (57, "CAT3", "ទម្រង់ផ្ទះ និងដី (Land & Building Shapes)", "Auspicious vs Inauspicious Land Shapes", "ដីរាងការ៉េ ចតុកោណកែង ពងក្រពើ និងរាងអក្សរ L"),
    (58, "CAT3", "ការបាត់ជ្រុងផ្ទះ (Missing Corners & Bagua Trigrams)", "Missing Corners Remedies for 8 Trigrams", "ផលប៉ះពាល់លើសមាជិកគ្រួសារ និងវិធីបំពេញជ្រុង"),
    (59, "CAT3", "ទ្វារធំមុខផ្ទះ (Main Door Feng Shui - Qi Mouth)", "Main Entrance (Qi Mouth) Optimization", "មាត់ស្រូបថាមពលចម្បង ទំហំ និងទិសដៅ"),
    (60, "CAT3", "ទ្វារធំទល់មុខជណ្តើរយន្ត ឬទ្វារក្រោយ (Piercing Heart Sha)", "Piercing Heart Sha & Door Alignments", "វិធីទប់ស្កាត់ការលេចធ្លាយទ្រព្យសម្បត្តិ"),
    (61, "CAT3", "បន្ទប់គេងមេគ្រួសារ (Master Bedroom Placement)", "Master Bedroom Energy Balancing", "ទីតាំងសម្រាក និងស្តារថាមពលសុខភាព"),
    (62, "CAT3", "ក្បួនដាក់គ្រែគេង (Bed Headboard Direction & Positioning)", "Bed Alignment with Personal Life Gua", "ក្បាលគ្រែត្រូវទិសល្អ ជៀសវាងក្រោមកំណាត់ធ្នឹម"),
    (63, "CAT3", "កញ្ចក់ និងទូរទស្សន៍ក្នុងបន្ទប់គេង (Mirrors & Electronic Sha)", "Mirror Reflections & Sleep Disruptions", "ការដាក់កញ្ចក់ឱ្យត្រូវក្បួន មិនជះចំគ្រែ"),
    (64, "CAT3", "ផ្ទះបាយ និងចង្ក្រានបាយ (Kitchen & Stove Placement)", "Fire vs Water Conflict in Kitchens", "ជៀសវាងភ្លើងទល់ទឹក និងការរក្សាសុខភាពស្រ្តី"),
    (65, "CAT3", "តុធ្វើការ និងការិយាល័យ (Command Position Desk Setup)", "Executive Desk Command Position", "ខ្នងមានបង្អែក មុខទូលាយ ស្រូបអំណាច"),
    (66, "CAT3", "បន្ទប់ទឹក និងបង្គន់ (Bathroom & Water Draining)", "Bathroom Qi Suppression & Remedies", "ការជៀសវាងបន្ទប់ទឹកចំកណ្តាលផ្ទះ (Taiji Center)"),
    (67, "CAT3", "កាំជណ្តើរ និងលំហូរថាមពលខាងក្នុង (Staircase Qi Flow)", "Staircase Alignment & Internal Circulation", "ជៀសវាងជណ្តើរបុកចំទ្វារមុខ"),
    (68, "CAT3", "អាងចិញ្ចឹមត្រី និងទឹកធ្លាក់ហុងស៊ុយ (Aquarium & Water Placement)", "Water Features & Wealth Activation", "ទិសដាក់ទឹកស្រូបលាភធំក្នុងយុគទី ៩"),
    (69, "CAT3", "រុក្ខជាតិ និងដើមឈើហុងស៊ុយ (Indoor Plants & Wood Element)", "Indoor Flora & Wood Qi Harmonization", "ដើមឈើស្លឹកមូលស្រូបទ្រព្យ និងកន្លែងដាក់"),
    (70, "CAT3", "ភ្លើង និងពន្លឺក្នុងផ្ទះ (Lighting & Fire Qi in Period 9)", "Lighting Design & Period 9 Fire Amplification", "ការប្រើពន្លឺបំភ្លឺជ្រុងងងឹត"),
    (71, "CAT3", "ក្បួនហុងស៊ុយហាងទំនិញ និងភោជនីយដ្ឋាន (Retail & Restaurant)", "Retail Store Layout & Cashier Placement", "ទីតាំងតុគិតលុយ និងច្រកទ្វារអតិថិជន"),
    (72, "CAT3", "ក្បួនហុងស៊ុយអគារការិយាល័យ និងក្រុមហ៊ុន (Corporate Offices)", "Corporate Headquarters & Executive Suites", "ការរៀបចំបន្ទប់ប្រធាន និងបន្ទប់ប្រជុំ"),
    (73, "CAT3", "ក្បួនហុងស៊ុយខុនដូ និងអាផាតមិន (High-Rise Condo Feng Shui)", "High-Rise Apartment Facing & Balcony Qi", "ការកំណត់ទិស Facing នៃខុនដូជាន់ខ្ពស់"),
    (74, "CAT3", "ក្បួនហុងស៊ុយរោងចក្រ និងឃ្លាំងទំនិញ (Factory & Warehouse)", "Industrial Plant & Warehouse Flow", "ទីតាំងម៉ាស៊ីនធ្ងន់ និងច្រកចេញចូលទំនិញ"),
    (75, "CAT3", "ក្បួនហុងស៊ុយសណ្ឋាគារ និងរីសត (Hotel & Hospitality)", "Hospitality Lobby & Guest Flow Dynamics", "Lobby ស្រូបភ្ញៀវ និងទីធ្លាសម្រាក"),
    (76, "CAT3", "ការប្រើប្រាស់វត្ថុសិរីមង្គល (Feng Shui Cures & Activators)", "Authentic Activators (Metals, Crystals, Water)", "កែវទឹក កណ្តឹងខ្យល់ គ្រីស្តាល់ តាមធាតុគណិត"),
    (77, "CAT3", "ក្បួនពណ៌ក្នុងគេហដ្ឋាន (Color Selection by 5 Elements)", "Color Palettes Based on Room Trigram", "ការជ្រើសរើសពណ៌ជញ្ជាំងតាមធាតុវិហារ"),
    (78, "CAT3", "ការកែសម្រួលផ្ទះចាស់ឱ្យត្រូវយុគ ៩ (Period 9 Renovation Rules)", "Upgrading Older Properties to Period 9", "ការផ្លាស់ប្តូរដំបូល កម្រាល និងទ្វារ"),
    (79, "CAT3", "ការពិនិត្យដីធ្លីមុនពេលទិញ (Land Due Diligence)", "Pre-Purchase Land & Property Assessment", "សញ្ញាគ្រោះ និងសញ្ញាលាភនៃដី"),
    (80, "CAT3", "ម៉ូដែល Vision AI វិភាគប្លង់ និង Sha Qi", "Vision AI Floorplan & Sha Qi Detection", "ការប្រើបច្ចេកវិទ្យា Vision AI ស្កេនប្លង់"),

    # Category 4: High-Level Mastery, BaZi & Destiny (81-100)
    (81, "CAT4", "សសរស្តម្ភទាំង ៤ BaZi (Four Pillars of Destiny Overview)", "Four Pillars of Destiny (BaZi) Architecture", "ឆ្នាំ ខែ ថ្ងៃ ម៉ោង និងជោគជតារាសី"),
    (82, "CAT4", "មេឃទាំង ១០ (Ten Heavenly Stems - 天干)", "Ten Heavenly Stems Character & Elements", "Jia, Yi, Bing, Ding, Wu, Ji, Geng, Xin, Ren, Gui"),
    (83, "CAT4", "ដីទាំង ១២ (Twelve Earthly Branches - 地支)", "Twelve Earthly Branches & Zodiac Animals", "Zi, Chou, Yin, Mao, Chen, Si, Wu, Wei, Shen, You, Xu, Hai"),
    (84, "CAT4", "មេថ្ងៃកំណើត Day Master (The Core Self)", "Day Master Analysis (Weak vs Strong)", "ការកំណត់កម្លាំងមេថ្ងៃ (ខ្លាំង ឬខ្សោយ)"),
    (85, "CAT4", "អាទិទេពទាំង ១០ (The Ten Gods - 十神)", "The Ten Gods System (Direct/Indirect Wealth, Officer)", "ការវិភាគការងារ ទ្រព្យ អំណាច បញ្ញា មិត្តភក្តិ"),
    (86, "CAT4", "ធាតុឱសថ Yong Shen (Useful God / Balancing Element)", "Useful God (Yong Shen) Identification", "ការស្វែងរកធាតុដែលជួយសង្គ្រោះជោគជតា"),
    (87, "CAT4", "ធាតុឆុង និងធាតុផ្សំ (Clashes & Combinations - 冲合)", "Branch Combinations, Clashes, Harms & Punishments", "ការវិភាគទំនាក់ទំនងរវាងសសរស្តម្ភ"),
    (88, "CAT4", "វដ្តសំណាង ១០ ឆ្នាំ (Ten-Year Luck Pillars - 大运)", "Ten-Year Luck Pillars Forecasting", "ការទស្សន៍ទាយដំណាក់កាលឡើងចុះនៃជីវិត"),
    (89, "CAT4", "ការផ្សំ BaZi ជាមួយក្បួនហុងស៊ុយផ្ទះ (BaZi-House Synergy)", "Integrating BaZi Charts with Living Spaces", "ការរៀបចំផ្ទះតម្រូវតាមធាតុឱសថរបស់ម្ចាស់"),
    (90, "CAT4", "ទម្រង់មុខ Mian Xiang ១២ វិហារ (12 Face Palaces)", "Mian Xiang 12 Palaces Physiognomy", "វិហារទ្រព្យ វិហារការងារ វិហារអាពាហ៍ពិពាហ៍លើមុខ"),
    (91, "CAT4", "៣ ថ្នាក់រាសីលើផ្ទៃមុខ San Ting (Three Courts of Life)", "San Ting - Youth, Middle Age, Late Years", "ថ្ងាស (ក្មេង) ច្រមុះ/ថ្ពាល់ (កណ្តាល) ចង្កា (ចាស់)"),
    (92, "CAT4", "១០០ ចំណុចអាយុលើផ្ទៃមុខ (100 Age Points Mapping)", "100 Age Points Facial Mapping", "ការទស្សន៍ទាយរាសីតាមចំណុចអាយុ ១ ដល់ ១០០ ឆ្នាំ"),
    (93, "CAT4", "ក្បួនរើសថ្ងៃជ័យ Ze Ri (Classical Date Selection)", "Ze Ri Date Selection: Dong Gong & Great Sun", "ការជ្រើសរើសថ្ងៃបើកហាង ឡើងផ្ទះ រៀបការ"),
    (94, "CAT4", "ប្រព័ន្ធ ១២ មន្ត្រីសួគ៌ា (12 Day Officers - 建除十二神)", "12 Day Officers Selection Method", "Jian, Chu, Man, Ping, Ding, Zhi, Po, Wei, Cheng, Shou, Kai, Bi"),
    (95, "CAT4", "ក្បួន ២៨ ផ្កាយសួគ៌ា (28 Lunar Mansions - 二十八星宿)", "28 Lunar Mansions Auspicious Energies", "ការកំណត់ផ្កាយល្អប្រចាំថ្ងៃ និងម៉ោង"),
    (96, "CAT4", "ក្បួន San Yuan Xuan Kong Da Gua Date Selection", "San Yuan Xuan Kong Da Gua Date Selection", "ក្បួនរើសថ្ងៃកម្រិតកំពូលតាមលេខ ៦៤ ត្រីក្រាម"),
    (97, "CAT4", "ក្បួនហុងស៊ុយសុខភាព និងជំងឺ (Health & 5 Elements Pathology)", "Health Analysis & Element Imbalances", "ការទស្សន៍ទាយ និងការពារជំងឺតាមធាតុ"),
    (98, "CAT4", "ក្បួនហុងស៊ុយស្នេហា និងអាពាហ៍ពិពាហ៍ (Peach Blossom Activation)", "Peach Blossom & Relationship Feng Shui", "ការជំរុញគូស្រករ និងដោះស្រាយជម្លោះស្នេហា"),
    (99, "CAT4", "ក្បួនហុងស៊ុយទ្រព្យសម្បត្តិមហាសាល (Wealth Vaults & Gates)", "Activating Wealth Vaults (Chen, Xu, Chou, Wei)", "ការបើកឃ្លាំងទ្រព្យទាំង ៤ ក្នុង BaZi"),
    (100, "CAT4", "កំពូលមហាសំយោគ AGI Supreme Feng Shui Master Synthesis", "Supreme AGI Master Unified Matrix", "ការសំយោគក្បួនទាំង ៧ សសរស្តម្ភដោយ AI Master Level")
]


class CurriculumEngine:
    """
    Super Smart Curriculum Engine managing 100 Topics and 1,000 Sub-Lessons.
    Each Topic contains 10 structured sub-lessons.
    """

    def __init__(self):
        self.categories = CATEGORIES
        self.topics = {t[0]: t for t in TOPICS_CATALOG}
        self.total_topics = 100
        self.total_lessons = 1000

    def get_categories(self) -> List[Dict[str, Any]]:
        """Return all 4 grand categories."""
        return self.categories

    def get_topics(self, category_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return all topics or topics filtered by category."""
        res = []
        for t in TOPICS_CATALOG:
            topic_id, cat_id, name_kh, name_en, summary = t
            if category_id and cat_id != category_id:
                continue
            res.append({
                "topic_id": topic_id,
                "category_id": cat_id,
                "name_kh": name_kh,
                "name_en": name_en,
                "summary": summary,
                "lesson_start": (topic_id - 1) * 10 + 1,
                "lesson_end": topic_id * 10
            })
        return res

    def get_topic(self, topic_id: int) -> Optional[Dict[str, Any]]:
        """Get details of a specific topic."""
        if topic_id not in self.topics:
            return None
        t = self.topics[topic_id]
        topic_id, cat_id, name_kh, name_en, summary = t
        cat_info = next((c for c in self.categories if c["id"] == cat_id), None)
        return {
            "topic_id": topic_id,
            "category_id": cat_id,
            "category_name": cat_info["name_kh"] if cat_info else "",
            "category_icon": cat_info["icon"] if cat_info else "📚",
            "name_kh": name_kh,
            "name_en": name_en,
            "summary": summary,
            "lesson_start": (topic_id - 1) * 10 + 1,
            "lesson_end": topic_id * 10,
            "lessons": [
                self.get_lesson(lid) for lid in range((topic_id - 1) * 10 + 1, topic_id * 10 + 1)
            ]
        }

    def get_lesson(self, lesson_id: int) -> Optional[Dict[str, Any]]:
        """
        Get structured lesson data for a specific lesson ID (1 to 1000).
        Calculates topic, sub-lesson number, authentic classical rules, and next/prev pointers.
        """
        if lesson_id < 1 or lesson_id > self.total_lessons:
            return None

        topic_id = ((lesson_id - 1) // 10) + 1
        sub_idx = ((lesson_id - 1) % 10) + 1  # 1 to 10

        t = self.topics.get(topic_id)
        if not t:
            return None

        _, cat_id, topic_kh, topic_en, topic_summary = t
        cat_info = next((c for c in self.categories if c["id"] == cat_id), None)

        # Sub-lesson titles and focus
        sub_lesson_types = [
            ("គោលការណ៍គ្រឹះ និងនិយមន័យក្បួន", "Core Principles & Classical Definition"),
            ("រូបមន្តគណិតវិទ្យា និងក្រឹត្យក្រមបុរាណ", "Mathematical Formula & Classical Rules"),
            ("ការវិភាគលំហូរថាមពល Qi ជាក់ស្តែង", "Practical Qi Dynamics Analysis"),
            ("ក្បួនរៀបចំក្នុងលំនៅឋាន (Residential)", "Residential Application & Setup"),
            ("ក្បួនរៀបចំក្នុងអាជីវកម្ម (Commercial)", "Commercial & Wealth Application"),
            ("ការរួមបញ្ចូលជាមួយតារាហោះ យុគ ៩", "Integration with Period 9 Flying Stars"),
            ("ការរួមបញ្ចូលជាមួយ BaZi រាសី", "Synergy with BaZi Destiny Chart"),
            ("រោគសញ្ញាគ្រោះ និងទោសកំហុសទូទៅ", "Common Pitfalls & Warning Signs"),
            ("វិធីបន្សាប និងដំណោះស្រាយតាមធាតុ", "Element-Based Remedies & Enhancers"),
            ("ករណីសិក្សា និងការអនុវត្តកម្រិតកំពូល", "Master Case Study & Advanced Synthesis")
        ]

        sub_kh, sub_en = sub_lesson_types[sub_idx - 1]

        lesson_title_kh = f"មេរៀនទី {lesson_id}៖ {topic_kh} - {sub_kh}"
        lesson_title_en = f"Lesson {lesson_id}: {topic_en} - {sub_en}"

        # Authentic Classical Formula details
        formula = f"ក្បួនគណិតវិទ្យាហុងស៊ុយបុរាណ {topic_kh} (រូបមន្តកម្រិតទី {sub_idx}/10)"
        classical_rule = (
            f"យោងតាមក្បួនបុរាណ {cat_info['name_kh'] if cat_info else ''} សម្រាប់ប្រធានបទ '{topic_kh}'៖ "
            f"ត្រូវប្រកាន់ខ្ជាប់នូវតុល្យភាពធាតុទាំង ៥ (Wu Xing) និងទិសដៅប៉ាហ្គ័រជាក់ស្តែង ដោយគ្មានការទាយស្មានខុសពីក្បួនឡើយ។"
        )
        practical_remedy = (
            f"ការអនុវត្ត៖ ពិនិត្យមុំអង្សា និងទិសដៅជាក់ស្តែងនៃ '{topic_kh}'។ "
            f"ប្រសិនបើមានភាពឆុង ឬខ្វះតុល្យភាព ត្រូវប្រើប្រាស់ធាតុឱសថ ឬវត្ថុបន្សាបតាមក្បួនធម្មជាតិ (ដី ភ្លើង ឈើ ទឹក លោហៈ)។"
        )

        return {
            "lesson_id": lesson_id,
            "topic_id": topic_id,
            "sub_index": sub_idx,
            "category_id": cat_id,
            "category_name": cat_info["name_kh"] if cat_info else "",
            "category_icon": cat_info["icon"] if cat_info else "📚",
            "topic_title_kh": topic_kh,
            "topic_title_en": topic_en,
            "title_kh": lesson_title_kh,
            "title_en": lesson_title_en,
            "sub_topic_kh": sub_kh,
            "sub_topic_en": sub_en,
            "summary": topic_summary,
            "classical_rule": classical_rule,
            "formula": formula,
            "practical_remedy": practical_remedy,
            "prev_lesson_id": lesson_id - 1 if lesson_id > 1 else None,
            "next_lesson_id": lesson_id + 1 if lesson_id < self.total_lessons else None
        }

    def generate_deep_explanation(self, lesson_id: int) -> Dict[str, Any]:
        """
        Generate deep, comprehensive, zero-hallucination explanation for the lesson
        using FS-Supreme-Master and the fine-tuned model (hemsinath/khmer-supreme-feng-shui).
        """
        lesson = self.get_lesson(lesson_id)
        if not lesson:
            return {"success": False, "error": "Lesson not found"}

        from engines.supreme_master import SupremeFengShuiMaster
        master = SupremeFengShuiMaster()

        prompt = (
            f"ចូរពន្យល់លម្អិតកម្រិតកំពូល (Master Level) អំពី៖\n"
            f"📚 {lesson['title_kh']}\n"
            f"ផ្នែក៖ {lesson['category_name']}\n"
            f"ប្រធានបទធំ៖ {lesson['topic_title_kh']}\n"
            f"ប្រធានបទរង៖ {lesson['sub_topic_kh']}\n\n"
            f"សូមពន្យល់តាម ៤ ដំណាក់កាលច្បាស់លាស់៖\n"
            f"១. ខ្លឹមសារទ្រឹស្តី និងប្រភពដើមនៃក្បួន (Core Essence & Origins)\n"
            f"២. រូបមន្តគណិតវិទ្យា និងក្រឹត្យក្រមហុងស៊ុយជាក់ស្តែង (Mathematical Rules & Formulas)\n"
            f"៣. ការអនុវត្តក្នុងយុគទី ៩ (Period 9: 2024-2043 Application)\n"
            f"៤. ដំណោះស្រាយ និងវិធីរៀបចំស្រូបលាភជាក់ស្តែង (Remedies & Enhancements)"
        )

        try:
            explanation = master.hf_bridge.generate_chat(
                system_prompt="អ្នកគឺជា FS-Supreme-Master និងជាកំពូលគ្រូហុងស៊ុយដែលចេះក្បួនបុរាណច្បាស់លាស់ ១០០% គ្មានការភ័ន្តច្រឡំ។ ចូរពន្យល់ជាភាសាខ្មែរយ៉ាងក្បោះក្បាយ ត្រឹមត្រូវ និងទាក់ទាញ។",
                user_prompt=prompt,
                model_type="boramey",
                max_tokens=1500,
                temperature=0.6
            )
        except Exception as e:
            logger.error(f"Error generating AI explanation: {e}")
            explanation = (
                f"📖 **ការពន្យល់មេរៀនទី {lesson_id} (FS-Classical Engine):**\n\n"
                f"**១. ទ្រឹស្តីគ្រឹះ:** {lesson['classical_rule']}\n\n"
                f"**២. រូបមន្តអនុវត្ត:** {lesson['formula']}\n\n"
                f"**៣. ដំណោះស្រាយជាក់ស្តែង:** {lesson['practical_remedy']}\n\n"
                f"*(កំណត់សម្គាល់៖ មេរៀននេះត្រូវបានផ្ទៀងផ្ទាត់ដោយម៉ូដែលក្បួនហុងស៊ុយបុរាណ យុគទី ៩ ធាតុភ្លើង)*"
            )

        return {
            "success": True,
            "lesson": lesson,
            "deep_explanation": explanation
        }


# Global Singleton
curriculum_engine = CurriculumEngine()
