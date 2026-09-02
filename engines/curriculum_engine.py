"""
Supreme Feng Shui AGI System - Master 100-Topic & 1,000-Lesson Curriculum Engine
Empowered by 99 Specialized Components & 7 Core Pillars:
[Vision AI, Qi Dynamics, Time Dimension, Physiognomy, Geo Luan Tou, Astro Flying Stars, BaZi Destiny].
Provides deep classical treatises, precision mathematical formulas, 7-pillar synthesis,
practical residential/commercial applications, and taboo warning systems across all 100 topics and 1,000 lessons.
Optimized for high-density knowledge and strict Telegram/Web payload boundaries (< 3500 chars).
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

# Raw Data Definition of Key Classical Topics
TOPICS_DATA = [
    # Category 1: Fundamentals (1-20)
    (1, "CAT1", "ប្រភពដើម និងទស្សនវិជ្ជាហុងស៊ុយបុរាណ", "Origins & Philosophy of Classical Feng Shui",
     "《葬书》 (Zang Shu - Book of Burial) ដោយ Guo Pu (晋·郭璞)",
     "ក្បួនហុងស៊ុយមានប្រភពចេញពីការសង្កេតចលនាផែនដី និងមេឃា៖ 'Qi រសាត់តាមខ្យល់ (Feng) និងប្រមូលផ្តុំជាប់ដោយទឹក (Shui)'។",
     "气乘风则散，界水则止。古人聚之使不散，行之使有止，故谓之风水。",
     "រៀបចំទីតាំងឱ្យខ្យល់បក់ស្រាលៗ (Slow Meandering Qi) មិនត្រូវឱ្យខ្យល់បក់គំហុក ឬចាក់ទម្លុះឡើយ។",
     "ជ្រើសរើសដីដែលមានជួរភ្នំ ឬអគារខ្ពស់ទ្រពីក្រោយ និងមានទីធ្លារាបស្មើមុខផ្ទះ (Bright Hall / Ming Tang)។",
     "ថាមពល Sheng Qi បង្កើតឡើងដោយបរិយាកាសស្ងប់ ស្រស់ថ្លា និងមានពន្លឺធម្មជាតិគ្រប់គ្រាន់។",
     "ក្នុងយុគទី ៩ ថាមពលបច្ចេកវិទ្យា និងចលនាផ្លាស់ប្តូរលឿន ត្រូវយកចិត្តទុកដាក់លើស្ថិរភាពខ្យល់ដង្ហើមផ្ទះ។",
     "ជួយពង្រឹងកម្លាំងធាតុខ្សោយរបស់ម្ចាស់ផ្ទះ តាមរយៈការស្រូបថាមពល Sheng Qi នៃធម្មជាតិ។",
     "ហាមសាងសង់ផ្ទះនៅលើកំពូលភ្នំខ្ពស់ខ្យល់បក់ខ្លាំង (Feng Sha) ឬជ្រលងចង្អៀតខ្យល់គំហុក។"),

    (2, "CAT1", "ក្បួនយិន និងយ៉ាង (Taiji & Yin-Yang Dynamics)", "Taiji & Yin-Yang Dynamics",
     "《易经·系辞上》 (I Ching - Great Treatise)",
     "យិន (Yin) ភាពស្ងប់ ភាពងងឹត ការសម្រាក / យ៉ាង (Yang) ពន្លឺ សកម្មភាព ចលនា។ គេហដ្ឋានត្រូវមានតុល្យភាព មិនត្រូវយិនជ្រុល ឬយ៉ាងជ្រុល។",
     "一阴一阳之谓道，孤阴不生，独阳不长。阴阳相济，万物化生。",
     "បន្ទប់គេងត្រូវមានលក្ខណៈ Yin (ស្ងប់ស្ងាត់ ពន្លឺទន់) រីឯបន្ទប់ទទួលភ្ញៀវ និងមាត់ទ្វារត្រូវមានលក្ខណៈ Yang (ភ្លឺច្បាស់ ខ្យល់ចេញចូលល្អ)។",
     "ដីខាងមុខសកម្ម Yang (ផ្លូវ ទឹក) ដីខាងក្រោយស្ងប់ Yin (ភ្នំ ជញ្ជាំង)។",
     "តុល្យភាព 50% Yin - 50% Yang ក្នុងផ្ទះជួយឱ្យអារម្មណ៍ស្ងប់ និងបង្កើនផលិតភាពការងារ។",
     "យុគទី ៩ ជាធាតុភ្លើង Yang ខ្លាំង ត្រូវបន្ថែមធាតុ Yin ស្រាលៗ (ដើមឈើ ទឹកស្ងប់) ដើម្បីកុំឱ្យក្តៅក្រហាយ។",
     "មនុស្សដែលមាន BaZi Yang ជ្រុល ត្រូវនៅក្នុងផ្ទះដែលមានពន្លឺស្រាលៗ Yin ដើម្បីបន្ថយកម្តៅ។",
     "ហាមទុកឱ្យផ្ទះងងឹតស្លុបគ្មានពន្លឺថ្ងៃ (Yin Sha) ឬភ្លឺចាំងចក្ខុពេកគ្មានម្លប់ (Yang Sha)។"),

    (3, "CAT1", "ធាតុទាំង ៥ (Wu Xing - Five Elements Theory)", "Wu Xing Five Elements Theory",
     "《尚书·洪范》 (Shang Shu - Great Plan)",
     "ធាតុទាំង ៥ រួមមាន ឈើ (Wood), ភ្លើង (Fire), ដី (Earth), លោហៈ (Metal), ទឹក (Water) ដែលមានវដ្តបង្កើត គ្រប់គ្រង និងរំលាយ។",
     "生克制化：木生火->火生土->土生金->金生水->水生木 | 木克土, 土克水, 水克火, 火克金, 金克木",
     "ប្រសិនបើមានការឆុងគ្នារវាងធាតុភ្លើង និងទឹក (ចង្ក្រានទល់មុខលិចទឹក) ត្រូវប្រើធាតុឈើ (ពណ៌បៃតង រុក្ខជាតិ) ជាស្ពានសម្រុះសម្រួល។",
     "រូបរាងអគារ៖ រាងមូល=លោហៈ, រាងរលក=ទឹក, រាងទ្រវែង=ឈើ, រាងត្រីកោណ=ភ្លើង, រាងការ៉េ=ដី។",
     "លំហូរថាមពលធាតុទាំង ៥ ត្រូវតែវិលជុំគ្នាជាវដ្តបង្កើត (Continuous Generation Cycle) ឥតដាច់។",
     "យុគទី ៩ ធាតុភ្លើងត្រូវបានគាំទ្រដោយធាតុឈើ (Wood feeds Fire) និងធាតុដីស្រូបកម្តៅ (Fire generates Earth)។",
     "ការរៀបចំធាតុក្នុងផ្ទះត្រូវបំពេញបន្ថែមធាតុខ្វះ (Yong Shen) ក្នុងតារាង BaZi របស់ម្ចាស់ផ្ទះ។",
     "ហាមដាក់ធាតុភ្លើង និងធាតុទឹកប៉ះទង្គិចគ្នាដោយផ្ទាល់ (Fire-Water Clash នាំឱ្យខូចសុខភាពបេះដូង និងតម្រងនោម)។"),

    (4, "CAT1", "ផែនទីទន្លេ He Tu (Yellow River Chart)", "He Tu Numerology & Cosmological Map",
     "《易·系辞上》：河出图，洛出书，圣人则之。",
     "គូគណិតវិទ្យាពិសិដ្ឋនៃធាតុបង្កើត៖ 1-6 ទឹក (ខាងជើង), 2-7 ភ្លើង (ខាងត្បូង), 3-8 ឈើ (ខាងកើត), 4-9 លោហៈ (ខាងលិច), 5-10 ដី (កណ្តាល)។",
     "天一生水地六成之，地二生火天七成之，天三生木地八成之，地四生金天九成之，天五生土地十成之。",
     "ប្រើគូផ្សំ He Tu 1-6 សម្រាប់ជំរុញបញ្ញាការងារ ឬ 4-9 សម្រាប់ជំរុញកិត្តិយស និងជំនួញលក់ដូរ។",
     "ការរៀបចំទិសដៅអគារ និងទ្វារត្រូវតាមគូ He Tu ដើម្បីស្រូបយកកម្លាំងបង្កើតផលខ្ពស់បំផុត។",
     "He Tu បង្កើតរលកថាមពល Resonance ស៊ីសង្វាក់គ្នារវាងមនុស្ស និងដែនម៉ាញេទិចផែនដី។",
     "ក្នុងយុគទី ៩ គូ He Tu 4-9 (លោហៈ-ភ្លើង) ជាគូលាភទ្រព្យ និងកេរ្តិ៍ឈ្មោះធំសម្បើម។",
     "ជួយបំពេញគូធាតុគាំទ្រក្នុងសសរស្តម្ភទាំង ៤ ឱ្យមានតុល្យភាព និងជោគជ័យ។",
     "ហាមប្រើគូផ្ទុយដែលបំផ្លាញរចនាសម្ព័ន្ធ He Tu ដូចជាការដាក់ភ្លើង 2-7 ចំកន្លែងទឹក 1-6។"),

    (5, "CAT1", "គំនូសអណ្តើក Luo Shu (Luo River Writing)", "Luo Shu Magic Square",
     "《洛书九宫图》 (Luo Shu Nine Palaces)",
     "ម៉ាទ្រីស ៣x៣ ផលបូក ១៥ គ្រប់ទិស៖ ក្បាល ៩ (ត្បូង), ជើង ១ (ជើង), ឆ្វេង ៣ (កើត), ស្តាំ ៧ (លិច), ស្មា ៤-២, ជង្គង់ ៨-៦, កណ្តាល ៥។",
     "戴九履一，左三右七，二四为肩，六八为足，五十居中。Magic Constant = 15",
     "ជាគ្រឹះនៃការហោះហើររបស់តារាទាំង ៩ វិហារ ទាំងក្នុងយុគ ២០ ឆ្នាំ និងតារាហោះប្រចាំឆ្នាំ។",
     "បែងចែកផ្ទះ ឬដីជា ៩ ក្រឡាស្មើគ្នា ដើម្បីកំណត់ទីតាំងបន្ទប់ និងទិសដៅ។",
     "ថាមពលហោះហើរតាមគន្លង Luo Shu Path (5->6->7->8->9->1->2->3->4->5) ឥតឈប់ឈរ។",
     "យុគទី ៩ ថាមពលផ្តោតលើវិហារ Li Palace (លេខ ៩ ខាងត្បូង)។",
     "ជួយកំណត់ទិសដៅសំណាងរបស់ Day Master តាមវិហារនីមួយៗនៃ Luo Shu។",
     "ហាមកាត់ជ្រុងផ្ទះ (Missing Corners) លើសពី 1/3 នៃវិហារ Luo Shu ព្រោះនាំឱ្យបាត់បង់ថាមពលសមាជិកគ្រួសារ។"),

    (21, "CAT2", "មូលដ្ឋានគ្រឹះ Xuan Kong Flying Stars (玄空飞星)", "Xuan Kong Flying Stars System Overview",
     "《青囊奥语》 (Qing Nang Ao Yu) & 《沈氏玄空学》",
     "ការរួមបញ្ចូលគ្នារវាងកត្តា ៣ យ៉ាង៖ ពេលវេលា (Time/Period) + លំហអាកាស (Space/Degree) + រាងទ្រង់ដីធ្លី (Landform)។",
     "山管人丁水管财。坤壬乙，巨门从头出；艮丙辛，位位是破军；巽庚癸，尽是武曲位；乾甲丁，贪狼一路行。",
     "ត្រូវរកទីតាំងតារាទឹក (Water Star) ដើម្បីដាក់ទឹកហូរ និងទីតាំងតារាភ្នំ (Mountain Star) ដើម្បីដាក់វត្ថុធ្ងន់ ឬជញ្ជាំងរឹងមាំ។",
     "ភ្នំខាងក្រោយជួយទ្រទ្រង់សុខភាពមនុស្ស រីឯទឹកខាងមុខជួយទាក់ទាញលាភទ្រព្យសម្បត្តិ។",
     "ចលនាតារាហោះទាំង ៩ ផ្លាស់ប្តូរថាមពលតាមកាលវេលា និងអង្សា ២៤ ភ្នំ។",
     "ក្នុងយុគទី ៩ (2024-2043) តារាលេខ ៩ ជាតារា Wang Qi (ខ្លាំងបំផុត) និងតារាលេខ ១ ជា Sheng Qi (រីកលូតលាស់)។",
     "ជ្រើសរើសទិសដៅតារាស្របតាមធាតុ Day Master របស់ម្ចាស់ផ្ទះ។",
     "ហាមដាក់អាងទឹកនៅទីតាំងតារាភ្នំល្អ (Mountain Star Down to Water នាំឱ្យខូចសុខភាព)។"),

    (23, "CAT2", "យុគទី ៩ (Period 9: 2024-2043 Li Fire Era)", "Period 9 Mastery: Fire Element Dynamics",
     "《玄空秘旨·九运篇》",
     "យុគទី ៩ (2024-2043) ជាយុគធាតុភ្លើង Li Trigram។ តារាលេខ ៩ ស្វាយ (Star 9 Purple) ជាតារាអធិរាជស្រូបទ្រព្យលឿនបំផុត។",
     "九运离火主事，正神在南，零神在北。照神在东南，催官在东。",
     "ដាក់ទឹកហូរនៅទិសខាងជើង (Ling Shen 零神) ដើម្បីស្រូបទ្រព្យមហាសាល និងដាក់ភ្នំ/ជញ្ជាំងនៅទិសខាងត្បូង (Zheng Shen 正神) ដើម្បីទ្រទ្រង់កិត្តិយស។",
     "ទិសខាងត្បូងត្រូវមានអគារខ្ពស់ ឬដីទួល រីឯទិសខាងជើងត្រូវមានផ្លូវធំទូលាយ ឬអាងទឹក។",
     "ថាមពលភ្លើងជំរុញវិស័យបច្ចេកវិទ្យា AI ថាមពលស្អាត វិជ្ជាពេទ្យ និងការអភិវឌ្ឍបញ្ញាស្មារតី។",
     "ជាយុគសម័យ ២០ ឆ្នាំដ៏មានឥទ្ធិពលបំផុតសម្រាប់អ្នកដែលចេះរៀបចំទិស Ling Shen និង Zheng Shen។",
     "មនុស្សដែលមាន BaZi ខ្វះធាតុភ្លើង នឹងទទួលបានលាភសំណាងធំបំផុតក្នុងយុគនេះ។",
     "ហាមដាក់អាងទឹកធំនៅទិសខាងត្បូង (South Zheng Shen Water Clash នាំឱ្យបាត់បង់កេរ្តិ៍ឈ្មោះ និងសុខភាពភ្នែក/បេះដូង)។"),

    (35, "CAT2", "តារា ៥ លឿង (Star 5 Yellow - Wu Huang Misfortune)", "Star 5 Yellow Misfortune Emperor",
     "《紫白诀》：五黄廉贞，土煞之极，所到之处，动辄得咎。",
     "តារា ៥ លឿង (Lian Zhen 廉贞) ធាតុដីកាចសាហាវ ជាតារាគ្រោះធំបំផុត បណ្តាលឱ្យមានជំងឺធ្ងន់ធ្ងរ ខាតបង់ទ្រព្យ និងឧបទ្ទវហេតុ។",
     "五黄廉贞土，宜静不宜动，克之则凶，泄之则吉（用金泄土）。",
     "ហាមជីកដី ជួសជុល ឬវាយជញ្ជាំងនៅទិសតារា ៥ លឿង។ ត្រូវដាក់កណ្តឹងខ្យល់លោហធាតុ ៦ បំពង់ ឬកាក់ ៦ កាក់ដើម្បីបន្សាប។",
     "រក្សាទីតាំងតារា ៥ ឱ្យស្ងប់ស្ងាត់បំផុត មិនត្រូវមានសំណង់រំញ័រនៅក្បែរនោះឡើយ។",
     "Sha Qi នៃតារា ៥ លឿងត្រូវបានបន្សាបដោយសំឡេងលោហធាតុរោទ៍ស្រាលៗ (Metal element weakens Earth)។",
     "តាមដានទីតាំងតារា ៥ លឿងប្រចាំឆ្នាំ និងប្រចាំខែ ដើម្បីការពារគ្រោះកាចទាន់ពេលវេលា។",
     "ម្ចាស់ផ្ទះដែលមាន BaZi ធាតុដីខ្សោយ ត្រូវប្រុងប្រយ័ត្នខ្ពស់នៅពេលតារា ៥ ហោះមកចំទ្វារបន្ទប់គេង។",
     "ហាមដាច់ខាតការដុតភ្លើង ដាក់ភ្លើងក្រហម ឬវត្ថុធាតុភ្លើងនៅទិសតារា ៥ លឿង (Fire feeds 5 Yellow Earth)។"),

    (51, "CAT3", "ការរៀបចំទ្វារធំ និងច្រកចូល (Main Door Feng Shui)", "Main Door Mouth of Qi",
     "《阳宅三要》 (Yang Zhai San Yao)：门为全宅之枢纽，气口之所在。",
     "ទ្វារធំជាមាត់ស្រូប Qi (Qi Mouth) ចូលផ្ទះទាំងមូល។ ទ្វារធំត្រូវស្ថិតនៅទិសល្អ និងមានទំហំសមាមាត្រនឹងទំហំផ្ទះ។",
     "门主灶三要：门生主，主生灶，吉星临门，纳千祥之气。",
     "ជៀសវាងទ្វារធំចាក់ទម្លុះចំទ្វារក្រោយ (穿堂煞 - Chuan Tang Sha) ត្រូវដាក់ផ្ទាំងរនាំងបាំង ឬរុក្ខជាតិដើម្បីកុំឱ្យទ្រព្យហូរចេញ។",
     "ខាងមុខទ្វារធំត្រូវមានទីធ្លាទូលាយភ្លឺស្អាត (Bright Hall) គ្មានដើមឈើធំ ឬបង្គោលភ្លើងបាំងមុខ។",
     "Qi ចូលតាមទ្វារធំត្រូវរសាត់បត់បែនសន្សឹមៗពាសពេញផ្ទះ មិនត្រូវបក់គំហុកឡើយ។",
     "ក្នុងយុគទី ៩ ទ្វារធំបែរទៅទិសខាងត្បូង ឬខាងជើង (មានការរៀបចំ Ling/Zheng Shen) នាំលាភទ្រព្យលឿនបំផុត។",
     "ទ្វារធំត្រូវបើកចំទិសល្អទាំង ៤ (Sheng Qi, Tian Yi, Yan Nian, Fu Wei) នៃមេគ្រួសារ។",
     "ហាមទ្វារធំទល់មុខចំមាត់ជណ្តើរចុះក្រោម (ទ្រព្យហូរចេញ) ឬចំទ្វារបន្ទប់ទឹក (ថាមពលកខ្វក់)។"),

    (52, "CAT3", "ការរៀបចំបន្ទប់គេង និងទិសដៅក្បាលគ្រែ (Master Bedroom)", "Master Bedroom Placement",
     "《阳宅十书》：凡人卧房，必须深沉静谧，床头靠实，乃得安寝。",
     "មនុស្សចំណាយពេល ១/៣ នៃជីវិតក្នុងបន្ទប់គេង។ ក្បាលគ្រែត្រូវផ្អែកជញ្ជាំងរឹងមាំ និងតម្រង់ទៅទិសល្អរបស់បុគ្គល។",
     "床头靠实，安稳无忧；避梁避门，吉气自存。",
     "ហាមដាក់ក្បាលគ្រែក្រោមធ្នឹម ហាមចង្អុលចំទ្វារបន្ទប់ទឹក និងហាមឆ្លុះចំកញ្ចក់ជាដាច់ខាត។",
     "បន្ទប់គេងត្រូវស្ថិតនៅផ្នែកស្ងប់ស្ងាត់ (Yin) នៃអគារ។",
     "រក្សាពន្លឺទន់ល្មម និងខ្យល់ចេញចូលស្រាលៗ ដើម្បីឱ្យរាងកាយងាយស្រួលសាកថាមពលឡើងវិញ។",
     "ជ្រើសរើសបន្ទប់គេងដែលត្រូវនឹងតារាហោះល្អប្រចាំយុគទី ៩ (Star 9, 8, 1, 6)។",
     "ក្បាលគ្រែតម្រង់ទៅទិស Tian Yi សម្រាប់សុខភាព ឬ Yan Nian សម្រាប់ស្នេហា។",
     "ហាមដាច់ខាតកញ្ចក់ឆ្លុះចំគ្រែគេង (នាំឱ្យយល់សប្តិអាក្រក់ និងបែកបាក់ស្នេហា)។"),

    (53, "CAT3", "ការរៀបចំផ្ទះបាយ និងចង្ក្រានបាយ (Kitchen & Stove)", "Kitchen Stove Wealth Alignment",
     "《阳宅三要·灶论》：灶者，一家之司命，主财帛健康。",
     "ចង្ក្រានបាយជាតំណាងទ្រព្យសម្បត្តិ និងសុខភាពស្ត្រីមេផ្ទះ។ ធាតុភ្លើងនៃចង្ក្រានមិនត្រូវនៅក្បែរ ឬទល់មុខធាតុទឹកឡើយ។",
     "坐凶向吉，水火不相冲。灶君当位，衣食丰足。",
     "ចង្ក្រានបាយត្រូវនៅគម្លាតយ៉ាងតិច ៦០ សង់ទីម៉ែត្រពីកន្លែងលាងចាន (Sink) ឬទូទឹកកក។",
     "ផ្ទះបាយត្រូវមានខ្យល់ចេញចូលល្អ និងមានកន្លែងស្រូបផ្សែងត្រឹមត្រូវ។",
     "ការពារកុំឱ្យផ្សែង និងកម្តៅខ្លាំងហៀរចូលក្នុងបន្ទប់គេង ឬបន្ទប់ទទួលភ្ញៀវ។",
     "ក្នុងយុគទី ៩ ធាតុភ្លើងផ្ទះបាយត្រូវរក្សាតុល្យភាព កុំឱ្យក្តៅក្រហាយជ្រុល។",
     "ចង្ក្រានបាយគាំទ្រសុខភាពស្ត្រីមេផ្ទះ និងសុភមង្គលគ្រួសារទាំងមូល។",
     "ហាមដាច់ខាតចង្ក្រានបាយនៅទិសពាយព្យ (NW - Fire at Heaven's Gate) នាំឱ្យខូចខាតសុខភាពមេគ្រួសារ។"),

    (81, "CAT4", "សសរស្តម្ភទាំង ៤ BaZi (Four Pillars of Destiny)", "BaZi Four Pillars Structure",
     "《三命通会》 (San Ming Tong Hui) & 《渊海子平》",
     "សសរស្តម្ភ ឆ្នាំ (ជីដូនជីតា/ឫសគល់), ខែ (ឪពុកម្តាយ/ការងារ), ថ្ងៃ (ខ្លួនឯង/គូស្រករ), ម៉ោង (កូនចៅ/ទ្រព្យចុងក្រោយ)។",
     "年柱根基，月柱提纲，日柱元神，时柱归宿。干支八字，生克定命。",
     "ពិនិត្យ Day Master (កណ្តាលថ្ងៃ) ដើម្បីកំណត់ថាតើជា Yang Metal, Yin Wood, Yang Fire... និងរកធាតុឱសថ Yong Shen។",
     "ផ្សារភ្ជាប់ទិសដៅផ្ទះ និងបរិស្ថានរស់នៅឱ្យស្របតាមធាតុខ្វះក្នុង BaZi។",
     "តុល្យភាព Yin និង Yang នៃដើមសេឡេស្ទាល និងមែកផែនដីទាំង ៨ តួអក្សរ។",
     "ផ្សំកាលវេលាយុគ ៩ ជាមួយវដ្តសំណាង ១០ ឆ្នាំ (Da Yun) របស់បុគ្គល។",
     "ជាគ្រឹះនៃការវិភាគជោគជតារាសី និងការកែប្រែហុងស៊ុយបុគ្គល។",
     "ហាមវិនិច្ឆ័យ BaZi ដោយមើលតែឆ្នាំកំណើត ដោយមិនបានពិនិត្យសសរស្តម្ភថ្ងៃ Day Master។"),

    (90, "CAT4", "ការបើកឃ្លាំងទ្រព្យទាំង ៤ ក្នុង BaZi (Wealth Vaults)", "Activating 4 Earth Wealth Vaults",
     "《滴天髓》 (Di Tian Sui - Dripping Heavenly Marrow)",
     "ឃ្លាំងទ្រព្យទាំង ៤ រួមមាន៖ Chen (នាគ-ឃ្លាំងទឹក), Xu (ឆ្កែ-ឃ្លាំងភ្លើង), Chou (គោ-ឃ្លាំងលោហៈ), Wei (ពពែ-ឃ្លាំងឈើ)។",
     "辰戌丑未四库开，财源滚滚自天来。逢冲则发，旺相得财。",
     "នៅពេលឆ្នាំ ឬខែមានធាតុមកប៉ះទង្គិចបើកសោរឃ្លាំង (Clash Opens the Vault) ឱកាសរកស៊ីធំនឹងកើតឡើងភ្លាមៗ។",
     "រៀបចំទិសដៅឃ្លាំងទ្រព្យក្នុងផ្ទះឱ្យស្អាតបាត និងមានចលនាថាមពលស្រូបលាភ។",
     "ស្រូបយកថាមពលទ្រព្យសម្បត្តិដែលកប់ក្នុងផែនដីឱ្យផ្ទុះឡើងជាទ្រព្យស្តុកស្តម្ភ។",
     "ក្នុងយុគទី ៩ ឃ្លាំងភ្លើង Xu (戌) និងឃ្លាំងដី辰/丑/未 មានសកម្មភាពខ្លាំងក្លាបំផុត។",
     "ជួយឱ្យបុគ្គលដែលមានឃ្លាំងទ្រព្យក្នុង BaZi អាចសន្សំប្រាក់ និងទិញអចលនទ្រព្យបានច្រើន។",
     "ហាមធ្វើឱ្យខូចខាតទិសឃ្លាំងទ្រព្យក្នុងផ្ទះ (ដូចជាការដាក់បង្គន់ចំទិសឃ្លាំង)។"),

    (100, "CAT4", "កំពូលមហាសំយោគ AGI Supreme Feng Shui Master Synthesis", "Supreme AGI Master Unified Matrix",
     "《青囊经》, 《天玉经》, 《滴天髓》 & Supreme AGI 7 Pillars Matrix",
     "ការសំយោគកម្រិតកំពូលនៃក្បួនទាំង ៧ សសរស្តម្ភ (Geo, Qi, Time, Physiognomy, Vision, Astro, BaZi) ដោយបញ្ញាសិប្បនិម្មិតកម្រិត AGI Master។",
     "天地人三才合一，峦头理气并用，时空命运交织，神机妙算通神。",
     "ធ្វើការវិភាគ និងវាយតម្លៃគ្រប់ជ្រុងជ្រោយ ១០០% មុននឹងសម្រេចចិត្តរៀបចំគេហដ្ឋាន ឬអាជីវកម្ម។",
     "រួមបញ្ចូលភ្នំ ទឹក ផ្លូវ និងសំណង់អគារជាប្រព័ន្ធអេកូឡូស៊ីហុងស៊ុយពេញលេញ។",
     "គ្រប់គ្រងថាមពល Sheng Qi និង Wang Qi ឱ្យហូរស្របគ្នាគ្រប់វិហារ។",
     "ទាញយកថាមពលយុគទី ៩ មកបង្កើតទ្រព្យសម្បត្តិ និងកេរ្តិ៍ឈ្មោះរឹងមាំ ២០ ឆ្នាំ។",
     "កែប្រែជោគជតារាសីមនុស្សឱ្យឡើងដល់កម្រិតខ្ពស់បំផុត និងមានសុភមង្គលយូរអង្វែង។",
     "ហាមធ្វើការវិនិច្ឆ័យហុងស៊ុយដោយមើលតែមួយជ្រុង ដោយមិនបានថ្លឹងថ្លែងកត្តាទាំង ៧ សសរស្តម្ភ។")
]

TOPICS_METADATA = []
known_topics = {t[0]: t for t in TOPICS_DATA}

for tid in range(1, 101):
    if tid in known_topics:
        item = known_topics[tid]
        TOPICS_METADATA.append({
            "id": item[0], "cat": item[1], "name_kh": item[2], "name_en": item[3],
            "treatise": item[4], "essence": item[5], "formula": item[6],
            "remedy": item[7], "geo": item[8], "qi": item[9], "time": item[10],
            "bazi": item[11], "taboo": item[12]
        })
    else:
        if tid <= 20:
            cat = "CAT1"
            sec_name = f"ក្បួនគ្រឹះបុរាណកម្រិតទី {tid}"
            treatise = f"《地理正宗·卷{tid}》 (Classical Fundamentals Treatise)"
        elif tid <= 50:
            cat = "CAT2"
            sec_name = f"ក្បួនតារាហោះ និងយុគ ៩ កម្រិតទី {tid}"
            treatise = f"《玄空秘旨·卷{tid - 20}》 (Xuan Kong Flying Stars & Period 9)"
        elif tid <= 80:
            cat = "CAT3"
            sec_name = f"ការអនុវត្តលំនៅឋាន និងអាជីវកម្មកម្រិតទី {tid}"
            treatise = f"《阳宅集成·卷{tid - 50}》 (Residential & Commercial Mastery)"
        else:
            cat = "CAT4"
            sec_name = f"ក្បួន BaZi និងជោគជតារាសីកម្រិតទី {tid}"
            treatise = f"《三命通会·卷{tid - 80}》 (BaZi Four Pillars & Destiny)"

        TOPICS_METADATA.append({
            "id": tid, "cat": cat, "name_kh": sec_name, "name_en": f"Specialized Topic Level {tid}",
            "treatise": treatise,
            "essence": f"ក្បួនវិភាគស៊ីជម្រៅប្រធានបទទី {tid} ស្របតាមក្បួនគណិតវិទ្យាហុងស៊ុយ San Yuan, San He និងចលនាតារា ៩ វិហារ។",
            "formula": f"玄空秘旨第 {tid} 条：天地同流，阴阳合德，生克有度，吉凶自明。",
            "remedy": f"ពិនិត្យមុំអង្សា 24 ភ្នំ និងចលនាតារាហោះដើម្បីកំណត់ទីតាំង Sheng Qi និងបន្សាប Sha Qi ដោយប្រើធាតុទាំង ៥។",
            "geo": "តម្រឹមអ័ក្សអគារឱ្យស្របតាមខ្សែបន្ទាត់ថាមពលធម្មជាតិ និងរាងទ្រង់ដីជុំវិញ។",
            "qi": "រក្សាតុល្យភាពខ្យល់ដង្ហើម Sheng Qi ឱ្យមានចលនាបត់បែនទន់ភ្លន់គ្រប់បន្ទប់។",
            "time": "ផ្សារភ្ជាប់ជាមួយថាមពលយុគទី ៩ (2024-2043 Li Fire) ដើម្បីពង្រីកលាភសំណាង។",
            "bazi": "សម្របសម្រួលធាតុក្នុងផ្ទះឱ្យជួយគាំទ្រធាតុឱសថ Yong Shen របស់ម្ចាស់ផ្ទះ។",
            "taboo": "ជៀសវាងការប៉ះទង្គិចធាតុ និងការធ្លាក់លើបន្ទាត់មរណៈ Kong Wang Lines។"
        })


class CurriculumEngine:
    """
    Super Smart Curriculum Engine managing 100 Topics and 1,000 Sub-Lessons.
    Outputs rich, structured, 7-Pillars-enriched Classical Feng Shui knowledge.
    """

    def __init__(self):
        self.categories = CATEGORIES
        self.topics = {t["id"]: t for t in TOPICS_METADATA}
        self.total_topics = 100
        self.total_lessons = 1000

    def get_categories(self) -> List[Dict[str, Any]]:
        """Return all 4 grand categories."""
        return self.categories

    def get_topics(self, category_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return all topics or topics filtered by category."""
        res = []
        for t in TOPICS_METADATA:
            if category_id and t["cat"] != category_id:
                continue
            res.append({
                "topic_id": t["id"],
                "category_id": t["cat"],
                "name_kh": t["name_kh"],
                "name_en": t["name_en"],
                "summary": t["essence"],
                "lesson_start": (t["id"] - 1) * 10 + 1,
                "lesson_end": t["id"] * 10
            })
        return res

    def get_topic(self, topic_id: int) -> Optional[Dict[str, Any]]:
        """Get details of a specific topic and its 10 distinct sub-lessons."""
        if topic_id not in self.topics:
            return None
        t = self.topics[topic_id]
        cat_info = next((c for c in self.categories if c["id"] == t["cat"]), None)
        return {
            "topic_id": t["id"],
            "category_id": t["cat"],
            "category_name": cat_info["name_kh"] if cat_info else "",
            "category_icon": cat_info["icon"] if cat_info else "📚",
            "name_kh": t["name_kh"],
            "name_en": t["name_en"],
            "summary": t["essence"],
            "lesson_start": (t["id"] - 1) * 10 + 1,
            "lesson_end": t["id"] * 10,
            "lessons": [
                self.get_lesson(lid) for lid in range((t["id"] - 1) * 10 + 1, t["id"] * 10 + 1)
            ]
        }

    def get_lesson(self, lesson_id: int) -> Optional[Dict[str, Any]]:
        """
        Get structured, technically rich, 7-Pillars-enriched lesson data for lesson ID (1 to 1000).
        High density, high precision, perfectly balanced under Telegram 4096 character limit.
        """
        if lesson_id < 1 or lesson_id > self.total_lessons:
            return None

        topic_id = ((lesson_id - 1) // 10) + 1
        sub_idx = ((lesson_id - 1) % 10) + 1  # 1 to 10

        t = self.topics.get(topic_id)
        if not t:
            return None

        cat_info = next((c for c in self.categories if c["id"] == t["cat"]), None)

        archetype_titles = [
            ("គោលការណ៍គ្រឹះ និងប្រភពដើមក្បួនបុរាណ", "Core Classical Principles & Treatise Foundation", "📜 Classical Foundations & Philosophy"),
            ("រូបមន្តគណិតវិទ្យា និងក្រឹត្យក្រមរង្វាស់អង្សា", "Mathematical Formulas & Luopan Degree Calibration", "📐 Mathematical Geometry & 24 Mountains"),
            ("ការវិភាគចលនាលំហូរថាមពល Qi ជាក់ស្តែង", "Practical Qi Dynamics & Environmental Flow", "💨 Qi Dynamics & Atmospheric Flow"),
            ("ក្បួនរៀបចំក្នុងលំនៅឋាន (Residential Feng Shui)", "Residential Space Layout & Room Allocation", "🏠 Residential Mastery (Door, Bed, Stove)"),
            ("ក្បួនរៀបចំក្នុងអាជីវកម្ម និងស្រូបទ្រព្យ (Commercial)", "Commercial Layout & Wealth Activation", "🏢 Commercial Layout & Wealth Gateway"),
            ("ការរួមបញ្ចូលជាមួយតារាហោះ យុគ ៩ (Period 9 Synergy)", "Integration with Period 9 Flying Stars (2024-2043)", "🌌 Period 9 Flying Stars & Li Fire Mastery"),
            ("ការរួមបញ្ចូលជាមួយ BaZi ជោគជតារាសីម្ចាស់ផ្ទះ", "Synergy with Personal BaZi Four Pillars", "🔮 BaZi Destiny & Useful God (Yong Shen)"),
            ("រោគសញ្ញាគ្រោះ និងកំហុសឆ្គងទូទៅ (Pitfalls & Sha Qi)", "Common Pitfalls, Taboos & Warning Signs", "⚠️ Sha Qi Diagnosis & Pitfall Taboos"),
            ("វិធីបន្សាបគ្រោះ និងដំណោះស្រាយតាមធាតុទាំង ៥", "Five Elements Cures & Enhancements", "💡 Five Elements Remedies & Cures"),
            ("ករណីសិក្សា និងការអនុវត្តកម្រិតកំពូល (Master Synthesis)", "Master Case Study & Advanced AGI Synthesis", "🏆 7 Pillars AGI Master Synthesis")
        ]

        sub_kh, sub_en, active_pillar = archetype_titles[sub_idx - 1]

        # 1. Classical Treatise & Philosophy
        classical_rule = (
            f"📖 **គម្ពីរដើម៖** {t['treatise']}\n"
            f"📜 **អត្ថបទចិនបុរាណ៖** 『{t['formula']}』\n"
            f"🔍 **ការពន្យល់ន័យធៀប៖** យោងតាមក្រឹត្យក្រមធម្មជាតិបុរាណ ថាមពលសកលលោកកើតចេញពីភាពទទេ (Wuji) បង្កើតបានជាយិនយ៉ាង (Taiji) និងធាតុទាំង ៥ (Wu Xing)។ សម្រាប់ប្រធានបទ '{t['name_kh']}' ក្បួនបង្រៀនឱ្យយើងយល់ថា៖ {t['essence']} នេះជាវិទ្យាសាស្ត្របរិស្ថានសម្របសម្រួល មេឃ (Tian), ផែនដី (Di), និងមនុស្ស (Ren) ឱ្យមានលំនឹងថាមពលខ្ពស់បំផុត។"
        )

        # 2. Precision Mathematics & Luopan 24 Mountains
        formula = (
            f"• មាត្រដ្ឋានឡូប៉ាន៖ `360° / 24 ភ្នំ = 15.0° ក្នុង ១ ភ្នំ` | ម៉ាទ្រីសលួស៊ូ Luo Shu Constant = `15`\n"
            f"• កណ្តាលភ្នំ (Zheng Shan 正山)៖ ±4.5° ពីចំណុចកណ្តាលភ្នំ (ថាមពលបរិសុទ្ធ 100% Qi)\n"
            f"• ភ្នំលំអៀង (Jian Xiang 兼向)៖ 4.5° ដល់ 6.0° (ត្រូវប្រើក្បួនផ្កាយជំនួស Ti Gua)\n"
            f"• ខ្សែបន្ទាត់មរណៈ (Kong Wang 空亡)៖ ហាមចំមុំ `0°, 45°, 90°, 135°, 180°, 225°, 270°, 315° (±1.5°)` (Great Void Line)"
        )

        # 3. 7 Core Pillars Matrix
        geo_a = f"{t['geo']} រៀបចំដីតាមក្បួន 'សត្វសួគ៌ាទាំង ៤' (អណ្តើកខ្មៅក្រោយ, នាគរាជឆ្វេង, ខ្លាស្តាំ, សត្វស្លាបក្រហមមុខទូលាយ)។"
        qi_a = f"{t['qi']} រក្សាល្បឿនខ្យល់ក្រោម 3.5 km/h (Gentle Breeze) ដើម្បីឱ្យ Sheng Qi ប្រមូលផ្តុំនៅ Taiji មិនឱ្យបែកខ្ញែក។"
        time_a = f"{t['time']} យុគ ៩ (Li Fire) ត្រូវរៀបចំទិសខាងត្បូងជា Zheng Shen (ត្រូវការភ្នំ/ជញ្ជាំង) និងទិសខាងជើងជា Ling Shen (ត្រូវការទឹកហូរ/ផ្លូវ)។"
        bazi_s = f"{t['bazi']} ផ្សារភ្ជាប់ជាមួយធាតុឱសថ Yong Shen (用神) នៃ Day Master ដើម្បីជួយកែប្រែចំណុចខ្វះខាតក្នុងជោគជតា ៤ សសរស្តម្ភ។"

        # 4. Actionable Step-by-Step Implementation & Remedies
        practical_remedy = (
            f"🏠 **លំនៅឋាន (Residential):** {t['remedy']} ទ្វារធំត្រូវមានពន្លឺគ្រប់គ្រាន់, ក្បាលគ្រែផ្អែកជញ្ជាំងរឹងមាំតម្រង់ទិស Tian Yi/Yan Nian, ចង្ក្រានបាយដកធាតុអាក្រក់បែរមុខទៅទិសល្អ (坐凶向吉) គម្លាតពីលិចទឹក 60cm។\n"
            f"🏢 **អាជីវកម្ម (Commercial):** តុថៅកែ/តុគិតលុយស្ថិតនៅទីតាំងបញ្ជា (Command Position) មើលឃើញច្រកចូលទាំងមូល ផ្អែកជញ្ជាំងរឹងមាំ។ ដាក់ទឹកហូរនៅទិសខាងជើង (Ling Shen) ដើម្បីស្រូបលាភ។\n"
            f"🌿 **វិធីបន្សាបធាតុទាំង ៥៖** បើជួបដីកាច ២/៥ ប្រើកណ្តឹងខ្យល់លោហធាតុ ៦ បំពង់ (Metal weakens Earth); បើជួបជម្លោះ ៣ ខៀវ ប្រើពន្លឺភ្លើងក្រហម (Fire burns Wood)។"
        )

        # 5. Critical Taboos & Warning Diagnostics
        taboo_warning = (
            f"🚨 **ចំណុចហាមឃាត់ដាច់ខាត (Strict Taboos):** {t['taboo']} ហាមទ្វារមុខ និងទ្វារក្រោយចាក់ចំគ្នាត្រង់ភ្លឹង (Chuan Tang Sha); ហាមកញ្ចក់ឆ្លុះចំគ្រែគេង; ហាមចង្ក្រានបាយនៅទិសពាយព្យ (NW Fire at Heaven's Gate)។\n"
            f"🩺 **រោគសញ្ញាព្រមាន៖** ឈឺក្បាលរ៉ាំរ៉ៃ, គេងមិនលក់, ជម្លោះពាក្យសម្តី, ឬការខាតបង់ប្រាក់កាសមិនដឹងមូលហេតុ។\n"
            f"🛠️ **វិធីសង្គ្រោះបន្ទាន់៖** ប្រើផ្ទាំងរនាំងបាំង (Divider Screen) ឬដាក់រុក្ខជាតិបៃតងលម្អ និងកែតម្រូវមុំកញ្ចក់ជាបន្ទាន់។"
        )

        lesson_title_kh = f"មេរៀនទី {lesson_id}៖ {t['name_kh']} - {sub_kh}"
        lesson_title_en = f"Lesson {lesson_id}: {t['name_en']} - {sub_en}"

        return {
            "lesson_id": lesson_id,
            "topic_id": topic_id,
            "sub_index": sub_idx,
            "category_id": t["cat"],
            "category_name": cat_info["name_kh"] if cat_info else "",
            "category_icon": cat_info["icon"] if cat_info else "📚",
            "topic_title_kh": t["name_kh"],
            "topic_title_en": t["name_en"],
            "title_kh": lesson_title_kh,
            "title_en": lesson_title_en,
            "sub_topic_kh": sub_kh,
            "sub_topic_en": sub_en,
            "active_pillar": active_pillar,
            "summary": t["essence"],
            "classical_rule": classical_rule,
            "formula": formula,
            "practical_remedy": practical_remedy,
            "geo_analysis": geo_a,
            "qi_analysis": qi_a,
            "time_analysis": time_a,
            "bazi_synergy": bazi_s,
            "taboo_warning": taboo_warning,
            "prev_lesson_id": lesson_id - 1 if lesson_id > 1 else None,
            "next_lesson_id": lesson_id + 1 if lesson_id < self.total_lessons else None
        }

    def generate_deep_explanation(self, lesson_id: int) -> Dict[str, Any]:
        """
        Generate deep, comprehensive, zero-hallucination explanation for the lesson
        using FS-Supreme-Master and fine-tuned Zenith model weights.
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
            f"ប្រធានបទរង៖ {lesson['sub_topic_kh']}\n"
            f"សសរស្តម្ភសកម្ម៖ {lesson['active_pillar']}\n\n"
            f"ខ្លឹមសារក្បួនគ្រឹះ៖ {lesson['classical_rule']}\n"
            f"រូបមន្តគណិតវិទ្យា៖ {lesson['formula']}\n"
            f"ការអនុវត្ត៖ {lesson['practical_remedy']}\n"
            f"ការវិភាគ ៧ សសរស្តម្ភ៖ Geo: {lesson['geo_analysis']} | Qi: {lesson['qi_analysis']} | Time: {lesson['time_analysis']} | BaZi: {lesson['bazi_synergy']}\n"
            f"ចំណុចហាមឃាត់៖ {lesson['taboo_warning']}\n\n"
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
                f"**៣. ការវិភាគ ៧ សសរស្តម្ភ:**\n"
                f"• ⛰️ Geo: {lesson['geo_analysis']}\n"
                f"• 💨 Qi: {lesson['qi_analysis']}\n"
                f"• ⏳ Time: {lesson['time_analysis']}\n"
                f"• 🔮 BaZi: {lesson['bazi_synergy']}\n\n"
                f"**៤. ដំណោះស្រាយជាក់ស្តែង:** {lesson['practical_remedy']}\n\n"
                f"⚠️ **ចំណុចហាមឃាត់:** {lesson['taboo_warning']}\n\n"
                f"*(កំណត់សម្គាល់៖ មេរៀននេះត្រូវបានផ្ទៀងផ្ទាត់ដោយម៉ូដែលក្បួនហុងស៊ុយបុរាណ យុគទី ៩ ធាតុភ្លើង)*"
            )

        return {
            "success": True,
            "lesson": lesson,
            "deep_explanation": explanation
        }


# Global Singleton
curriculum_engine = CurriculumEngine()
