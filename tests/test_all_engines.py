"""
Comprehensive Automated Test Suite for Supreme Feng Shui AGI System
Validates precision calculations, luck forecasting, chronos cycles,
MoE orchestration, memory footprint, and Master_Plan.py integrity.
"""

import os
import unittest
import psutil
from pathlib import Path

from config import config
from engines.classical_calc import ClassicalCalcEngine
from engines.alert_predictor import AlertPredictionEngine
from engines.chronos_cycle import ChronosCycleEngine
from engines.rag_client import RAGKnowledgeRetriever
from engines.supreme_master import SupremeFengShuiMaster


class TestSupremeFengShuiSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.calc_engine = ClassicalCalcEngine()
        cls.alert_engine = AlertPredictionEngine()
        cls.chronos_engine = ChronosCycleEngine()
        cls.rag_engine = RAGKnowledgeRetriever()
        cls.master = SupremeFengShuiMaster()

    # 1. Test Master_Plan.py file integrity
    def test_01_master_plan_original_integrity(self):
        """Verify Master_Plan.py exists and is original/untouched."""
        master_plan_file = config.BASE_DIR / "Master_Plan.py"
        self.assertTrue(master_plan_file.exists(), "Master_Plan.py must exist.")
        with open(master_plan_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("ប្រព័ន្ធ AI ហុងស៊ុយកម្រិតកំពូល", content)
        self.assertIn("class SupremeFengShuiSystem:", content)
        self.assertGreater(len(content), 50000, "Master_Plan.py content intact.")

    # 2. Test Life Gua (FS-Classical-Calc-v1)
    def test_02_life_gua_calculation(self):
        """Test Life Gua formulas for Male/Female across centuries."""
        # 1988 Male -> Gua 3 (Zhen - Wood - East Group)
        res_m1988 = self.calc_engine.calculate_life_gua(1988, "male")
        self.assertTrue(res_m1988["success"])
        self.assertEqual(res_m1988["data"]["gua_number"], 3)
        self.assertTrue(res_m1988["data"]["is_east_group"])
        self.assertEqual(len(res_m1988["data"]["lucky_directions"]), 4)

        # 1990 Female -> Gua 8 (Gen - Earth - West Group, substitution from 5)
        res_f1990 = self.calc_engine.calculate_life_gua(1990, "female")
        self.assertTrue(res_f1990["success"])
        self.assertEqual(res_f1990["data"]["gua_number"], 8)
        self.assertFalse(res_f1990["data"]["is_east_group"])

    # 3. Test Xuan Kong Flying Stars (Period 9 & Annual Star)
    def test_03_flying_stars(self):
        """Test Flying Stars period and 9-palace Lo Shu layout."""
        res_2024 = self.calc_engine.calculate_flying_stars(2024)
        self.assertTrue(res_2024["success"])
        self.assertEqual(res_2024["data"]["period"], 9)
        self.assertEqual(res_2024["data"]["annual_center_star"], 3)

        grid = res_2024["data"]["grid"]
        self.assertEqual(len(grid), 9)
        self.assertIn("CENTER", grid)
        self.assertIn("S", grid)
        self.assertIn("N", grid)

    # 4. Test 24 Mountains Conversion
    def test_04_24_mountains(self):
        """Test 24 mountains mapping from degree."""
        # 180 deg -> Wu (S2)
        res = self.calc_engine.get_mountain_by_degree(180.0)
        self.assertTrue(res["success"])
        self.assertEqual(res["mountain"]["name"], "午")
        self.assertEqual(res["mountain"]["direction"], "S2")

    # 5. Test BaZi Calculation
    def test_05_bazi_calculation(self):
        """Test Four Pillars generation and Day Master analysis."""
        res = self.calc_engine.calculate_bazi("1988-05-15", "10:30")
        self.assertTrue(res["success"])
        d = res["data"]
        self.assertIn("pillars", d)
        self.assertIn("day_master", d)
        self.assertIn("five_elements_count", d)

    # 6. Test Fortune Luck Predictor (FS-Alert-Predictor)
    def test_06_fortune_predictor(self):
        """Test ML Fortune Scoring and timing advice."""
        res = self.alert_engine.predict_fortune("1988-05-15", "10:30")
        self.assertTrue(res["success"])
        d = res["data"]
        self.assertIn("overall_luck", d)
        self.assertIn("wealth_luck", d)
        self.assertIn("auspicious_hours", d)
        self.assertGreaterEqual(d["overall_luck"]["score"], 0)
        self.assertLessEqual(d["overall_luck"]["score"], 100)

    # 7. Test Chronos Cycle Engine
    def test_07_chronos_cycle(self):
        """Test 100-year macro period analysis."""
        res_2024 = self.chronos_engine.analyze_year_macro_cycle(2024)
        self.assertEqual(res_2024["period"], 9)
        self.assertEqual(res_2024["element"], "Fire")

        res_1990 = self.chronos_engine.analyze_year_macro_cycle(1990)
        self.assertEqual(res_1990["period"], 7)

    # 8. Test RAG Knowledge Retriever
    def test_08_rag_knowledge_retriever(self):
        """Test search across 100 topics Feng Shui corpus."""
        results = self.rag_engine.search_knowledge("តារាហោះ យុគទី ៩", top_k=2)
        self.assertGreater(len(results), 0)

    # 9. Test FS-Supreme-Master MoE Pipeline
    def test_09_supreme_master_consultation(self):
        """Test end-to-end MoE ensemble pipeline."""
        res = self.master.consult(
            query="តើទិសខាងត្បូងក្នុងយុគទី ៩ មានអត្ថន័យដូចម្តេច?",
            birth_date="1988-05-15",
            gender="male",
            house_degree=180.0
        )
        self.assertTrue(res["success"])
        self.assertIn("evidence", res)
        self.assertIn("synthesis", res)
        self.assertGreater(len(res["synthesis"]), 20)

    # 10. Test RAM footprint (VPS 1GB Optimization Check)
    def test_10_memory_footprint(self):
        """Ensure entire system runs well within low RAM limits (< 350MB)."""
        process = psutil.Process(os.getpid())
        ram_mb = process.memory_info().rss / (1024 * 1024)
        print(f"\n[RAM Benchmark] Current Process RAM: {ram_mb:.2f} MB / 1024 MB VPS Limit")
        self.assertLess(ram_mb, 350.0, "Process memory footprint must stay under 350MB.")

    # 11. Test Curriculum Engine Categories & 100 Topics
    def test_11_curriculum_categories_and_topics(self):
        """Verify 4 Grand Categories and 100 Topics exist and map correctly."""
        from engines.curriculum_engine import curriculum_engine
        cats = curriculum_engine.get_categories()
        self.assertEqual(len(cats), 4, "Must have 4 Grand Categories.")

        topics = curriculum_engine.get_topics()
        self.assertEqual(len(topics), 100, "Must have 100 Master Topics.")

        # Test filter by category CAT1 (1 to 20)
        cat1_topics = curriculum_engine.get_topics("CAT1")
        self.assertEqual(len(cat1_topics), 20)

    # 12. Test 1,000 Lessons Navigation and Integrity
    def test_12_curriculum_1000_lessons(self):
        """Verify boundaries and structure of 1,000 lessons."""
        from engines.curriculum_engine import curriculum_engine
        
        # Test Lesson 1
        les1 = curriculum_engine.get_lesson(1)
        self.assertIsNotNone(les1)
        self.assertEqual(les1["lesson_id"], 1)
        self.assertEqual(les1["topic_id"], 1)
        self.assertIsNone(les1["prev_lesson_id"])
        self.assertEqual(les1["next_lesson_id"], 2)

        # Test Lesson 500 (End of CAT2)
        les500 = curriculum_engine.get_lesson(500)
        self.assertIsNotNone(les500)
        self.assertEqual(les500["lesson_id"], 500)
        self.assertEqual(les500["topic_id"], 50)
        self.assertEqual(les500["prev_lesson_id"], 499)
        self.assertEqual(les500["next_lesson_id"], 501)

        # Test Lesson 1000 (Final Master Synthesis Lesson)
        les1000 = curriculum_engine.get_lesson(1000)
        self.assertIsNotNone(les1000)
        self.assertEqual(les1000["lesson_id"], 1000)
        self.assertEqual(les1000["topic_id"], 100)
        self.assertEqual(les1000["prev_lesson_id"], 999)
        self.assertIsNone(les1000["next_lesson_id"])

        # Test Invalid Bounds
        self.assertIsNone(curriculum_engine.get_lesson(0))
        self.assertIsNone(curriculum_engine.get_lesson(1001))

    # 13. Test Deep AI Master Explanation
    def test_13_curriculum_deep_explanation(self):
        """Verify deep AI explanation generation for a lesson."""
        from engines.curriculum_engine import curriculum_engine
        res = curriculum_engine.generate_deep_explanation(1)
        self.assertTrue(res["success"])
        self.assertIn("deep_explanation", res)
        self.assertGreater(len(res["deep_explanation"]), 50)

    # 14. Test Family Synergy & Data Segregation (Pillar 10)
    def test_14_family_synergy_and_data_segregation(self):
        """Verify multi-member family registration, data isolation, and synergy calculations."""
        from engines.family_synergy_engine import family_synergy_engine
        from database.db_manager import db_manager

        user_a = 999111
        user_b = 999222
        db_manager.clear_family_members(user_a)
        db_manager.clear_family_members(user_b)

        # Add family members for User A
        p1 = family_synergy_engine.calculate_member_profile("1988-06-12", "06:30", "male")
        db_manager.upsert_family_member(
            user_a, "self", "ខ្ញុំ (ម្ចាស់ផ្ទះ)", "1988-06-12", "06:30", "male",
            day_master=p1["day_master"], useful_god=p1["useful_god"],
            zodiac_animal=p1["zodiac_animal"], life_gua=p1["life_gua"]
        )

        p2 = family_synergy_engine.calculate_member_profile("1990-09-24", "15:00", "female")
        db_manager.upsert_family_member(
            user_a, "spouse", "ភរិយា", "1990-09-24", "15:00", "female",
            day_master=p2["day_master"], useful_god=p2["useful_god"],
            zodiac_animal=p2["zodiac_animal"], life_gua=p2["life_gua"]
        )

        # Add family member for User B
        p_b = family_synergy_engine.calculate_member_profile("1995-01-01", "12:00", "male")
        db_manager.upsert_family_member(
            user_b, "self", "ខ្ញុំ", "1995-01-01", "12:00", "male",
            day_master=p_b["day_master"], useful_god=p_b["useful_god"],
            zodiac_animal=p_b["zodiac_animal"], life_gua=p_b["life_gua"]
        )

        # Verify Data Segregation (User A has 2 members, User B has 1 member)
        members_a = db_manager.get_family_members(user_a)
        members_b = db_manager.get_family_members(user_b)
        self.assertEqual(len(members_a), 2, "User A must have 2 family members.")
        self.assertEqual(len(members_b), 1, "User B must have 1 family member.")
        self.assertEqual(members_a[0]["life_gua"], 3, "1988 Male must be Gua 3.")
        self.assertEqual(members_a[1]["life_gua"], 8, "1990 Female must be Gua 8.")
        self.assertEqual(members_b[0]["life_gua"], 6, "1995-01-01 Male (solar 1994) must be Gua 6.")

        # Verify Synergy Analysis
        analysis_a = family_synergy_engine.analyze_family_synergy(members_a)
        self.assertTrue(analysis_a["success"])
        self.assertEqual(analysis_a["total_members"], 2)
        self.assertIn("household_remedy", analysis_a)

        # Verify Report Generation
        report_a = family_synergy_engine.generate_family_synergy_report(members_a)
        self.assertIn("ក្បួនហុងស៊ុយ និងរាសីគ្រួសាររួមពេញលេញ", report_a)
        self.assertNotIn("របាយការណ៍", report_a)
        self.assertNotIn("**", report_a)
        self.assertNotIn("==", report_a)

    # 15. Test Mandatory Profile Gate & 1000 Curriculum Exemption
    def test_15_mandatory_profile_gate_and_curriculum_exemption(self):
        """Verify that VIP users without /data profile are gated from analysis but can study curriculum."""
        from database.db_manager import db_manager, get_db_connection
        from bot.telegram_bot import FengShuiTelegramBot

        test_vip_id = 888777
        db_manager.clear_family_members(test_vip_id)
        with get_db_connection() as conn:
            conn.cursor().execute("UPDATE users SET birth_date = NULL, birth_time = NULL WHERE telegram_id = ?", (test_vip_id,))
            conn.commit()
        # Create user without birth profile
        db_manager.get_or_create_user(test_vip_id, username="vip_test", full_name="VIP Test User")
        db_manager.set_user_vip_manually(test_vip_id, "monthly", admin_id=859271875)

        bot = FengShuiTelegramBot("8772506380:AAG_qjamcB9ETNaBllNve3-qcPuLgcncgp4")

        # 1. Initially VIP has NO registered profile in /data
        self.assertFalse(db_manager.has_registered_profile(test_vip_id))
        self.assertFalse(bot._has_registered_profile(test_vip_id))

        # 2. Super Admin always has bypass
        admin_id = 859271875
        self.assertTrue(bot._has_registered_profile(admin_id))

        # 3. Register self profile in /data
        db_manager.upsert_family_member(
            test_vip_id, "self", "ខ្ញុំ", "1990-05-15", "08:30", "male",
            day_master="Wood", useful_god="Water", zodiac_animal="Horse", life_gua=1
        )

        # 4. Now VIP has registered profile
        self.assertTrue(db_manager.has_registered_profile(test_vip_id))
        self.assertTrue(bot._has_registered_profile(test_vip_id))

    # 16. Test Super Smart Daily, Monthly, and Yearly Treatise Formatting & Length Calibration
    def test_16_super_smart_daily_monthly_yearly_treatise_formatting(self):
        """Verify that /daily, /monthly, and /yearly reports are 3500-4000 chars, 100% Khmer, and cleanly formatted."""
        from engines.celestial_astrology_engine import CelestialAstrologyEngine
        import re

        celestial = CelestialAstrologyEngine()
        birth_date = "1990-05-15"
        birth_time = "10:30"
        gender = "male"

        precision = celestial.calculate_precision_bazi(birth_date, birth_time, gender)
        self.assertTrue(precision["success"])
        self.assertEqual(precision["day_master"]["element"], "Metal")
        self.assertIn("ធាតុដីដើម្បីការពារនិងពង្រឹង", precision["useful_god"])

        from engines.mahasneh_love_engine import mahasneh_love_engine
        love_p = mahasneh_love_engine.analyze_love_profile("1990-05-15", "male", "1992-08-20", "female")
        self.assertEqual(love_p["element_1"], "Metal")
        self.assertEqual(love_p["remedy"], "Remedy for Metal")

        d_report = celestial.generate_daily_celestial_report(birth_date, birth_time, gender)
        m_report = celestial.generate_monthly_celestial_report(birth_date, birth_time, gender)
        y_report = celestial.generate_yearly_celestial_report(birth_date, birth_time, gender)

        for name, txt in [("Daily", d_report), ("Monthly", m_report), ("Yearly", y_report)]:
            # 1. Length constraint 3500 - 4000 characters
            self.assertTrue(3500 <= len(txt) <= 4000, f"{name} length is {len(txt)}, expected 3500-4000")
            # 2. No markdown bold/markup
            self.assertNotIn("**", txt, f"{name} must not contain **")
            self.assertNotIn("++", txt, f"{name} must not contain ++")
            self.assertNotIn("==", txt, f"{name} must not contain ==")
            # 3. No word របាយការណ៍
            self.assertNotIn("របាយការណ៍", txt, f"{name} must not contain របាយការណ៍")
            # 4. No English characters
            self.assertFalse(re.search(r'[a-zA-Z]', txt), f"{name} must not contain English characters")
            # 5. No double bullet icons (e.g. • 💰)
            self.assertFalse(re.search(r'•\s*[💰👑🎨🏛️🌌⚠️🧭⏰✨💊💡🌿💼💖🌸☀️🍂❄️🧹🍎🏮🚫]', txt), f"{name} must not have double bullets")
            # 6. No double section headers (e.g. 📜 ១.)
            self.assertFalse(re.search(r'[📜🧭⏰💊📊💡👑🗓️]\s*[១២៣៤៥៦៧៨៩០]+\.', txt), f"{name} must not have double section headers")

    # 17. Test Universal System-Wide 3,500-4,000 Characters Standard Across All AI & Analytical Engines
    def test_17_all_ai_models_and_engines_3500_4000_chars_standard(self):
        """Verify that ALL AI response functions & analytical engines produce 3500-4000 chars in pure Khmer typography."""
        from engines.family_synergy_engine import family_synergy_engine
        from engines.curriculum_engine import curriculum_engine
        from engines.vision_3d_engine import vision_3d_engine
        from engines.omni_ai_bridge import omni_ai_bridge
        from engines.mahasneh_love_engine import mahasneh_love_engine
        import re

        # 1. Family Synergy Engine
        fam_members = [
            {"relation_type": "self", "relation_label": "ខ្ញុំ (មេគ្រួសារ)", "birth_date": "1988-08-18", "birth_time": "08:30", "gender": "male", "day_master": "Wood", "zodiac_animal": "Dragon", "life_gua": 3},
            {"relation_type": "spouse", "relation_label": "ភរិយា", "birth_date": "1990-12-05", "birth_time": "14:20", "gender": "female", "day_master": "Fire", "zodiac_animal": "Horse", "life_gua": 8}
        ]
        fam_report = family_synergy_engine.generate_family_synergy_report(fam_members)

        # 2. Curriculum Deep Master Explanation
        curr_res = curriculum_engine.generate_deep_explanation(1)
        curr_text = curr_res["deep_explanation"]

        # 3. Vision Multimodal Audit Report
        vision_report = vision_3d_engine.generate_detailed_vision_audit()

        # 4. Omni AI Consultation Engine
        ai_consult = omni_ai_bridge.generate_supreme_consultation("", "តើគួររៀបចំបន្ទប់គេងយ៉ាងដូចម្តេច?")

        # 5. Maha Sneh Love Engine
        love_res = mahasneh_love_engine.analyze_love_profile("1990-05-15", "male")
        love_report = love_res.get("treatise", "")

        all_outputs = [
            ("Family Synergy", fam_report),
            ("Curriculum Lesson", curr_text),
            ("Vision Audit", vision_report),
            ("Omni AI Consult", ai_consult),
            ("Love Treatise", love_report)
        ]

        for name, txt in all_outputs:
            self.assertTrue(3500 <= len(txt) <= 4000, f"{name} length is {len(txt)}, expected 3500-4000")
            self.assertNotIn("**", txt, f"{name} contains **")
            self.assertNotIn("++", txt, f"{name} contains ++")
            self.assertNotIn("==", txt, f"{name} contains ==")
            self.assertNotIn("របាយការណ៍", txt, f"{name} contains របាយការណ៍")
            self.assertFalse(re.search(r'[a-zA-Z]', txt), f"{name} contains English: {re.findall(r'[a-zA-Z]+', txt)}")
            self.assertFalse(re.search(r'•\s*[💰👑🎨🏛️🌌⚠️🧭⏰✨💊💡🌿💼💖🌸☀️🍂❄️🧹🍎🏮🚫⚖️🤝🛏️👤⛰️💨⏳🔮📖📐🖼️👁️❓]', txt), f"{name} contains double bullets")
            self.assertFalse(re.search(r'[📜🧭⏰💊📊💡👑🗓️⚖️🤝🛏️📖🖼️👁️]\s*[១២៣៤៥៦៧៨៩០]+\.', txt), f"{name} contains double section headers")


    # 18. Test Telegram Bot Target Resolution, Safe Reply, and Callbacks
    def test_18_telegram_bot_target_resolution_and_callbacks(self):
        """Verify that telegram bot target resolution handles Update, Message, CallbackQuery seamlessly."""
        from bot.telegram_bot import FengShuiTelegramBot

        bot = FengShuiTelegramBot("8772506380:AAG_qjamcB9ETNaBllNve3-qcPuLgcncgp4")

        class DummyMsg:
            async def reply_text(self, text, **kwargs):
                return text

        class DummyUpdateWithEffMsg:
            def __init__(self, msg):
                self.effective_message = msg

        class DummyQuery:
            def __init__(self, msg):
                self.message = msg

        class DummyUpdateWithQuery:
            def __init__(self, query):
                self.callback_query = query

        # 1. Target is None
        self.assertIsNone(bot._resolve_target(None))

        # 2. Target is message object
        msg = DummyMsg()
        self.assertEqual(bot._resolve_target(msg), msg)

        # 3. Target is Update with effective_message
        up1 = DummyUpdateWithEffMsg(msg)
        self.assertEqual(bot._resolve_target(up1), msg)

        # 4. Target is CallbackQuery
        query = DummyQuery(msg)
        up2 = DummyUpdateWithQuery(query)
        self.assertEqual(bot._resolve_target(up2), msg)

        # 5. Verify Flying Stars grid calculation schema
        res_fs = bot.calc_engine.calculate_flying_stars(2026)
        self.assertTrue(res_fs["success"])
        grid = res_fs["data"]["grid"]
        center = grid.get("CENTER") or grid.get("Center")
        self.assertIsNotNone(center)
        self.assertIn("star_number", center)

        # 6. Verify BaZi calculation schema
        res_bazi = bot.calc_engine.calculate_bazi("1990-05-15", "12:00")
        self.assertTrue(res_bazi["success"])
        self.assertIn("pillars", res_bazi["data"])

    # 19. Test Xuan Kong 24 Mountains Natal Chart Engine (Period 9 & Period 8 Formations)
    def test_19_xuan_kong_24_mountains_natal_chart(self):
        """Verify 24 Mountains Xuan Kong Natal Chart, Three Dragons, Ti Gua, and Castle Gate."""
        # 1. Period 9 Sitting North (Zi 0°), Facing South (Wu 180°)
        res_p9 = self.calc_engine.calculate_house_flying_stars(facing_degree=180.0, period=9)
        self.assertTrue(res_p9["success"])
        data_p9 = res_p9["data"]
        self.assertEqual(data_p9["period"], 9)
        self.assertEqual(data_p9["sitting"]["mountain"], "子")
        self.assertEqual(data_p9["sitting"]["palace"], "N")
        self.assertEqual(data_p9["facing"]["mountain"], "午")
        self.assertEqual(data_p9["facing"]["palace"], "S")
        self.assertFalse(data_p9["is_ti_gua"])
        self.assertIn("下卦", data_p9["chart_mode"])

        # Check flight dynamics
        dynamics = data_p9["flight_dynamics"]
        self.assertEqual(dynamics["mountain_star_center"], 5)
        self.assertIn("逆飞", dynamics["mountain_star_flight"])
        self.assertEqual(dynamics["water_star_center"], 4)
        self.assertIn("顺飞", dynamics["water_star_flight"])

        # Check Sitting Palace (N): Mountain Star = 9, Water Star = 9 (Double 9 at Sitting)
        sitting_natal = data_p9["natal_chart"]["N"]
        self.assertEqual(sitting_natal["mountain_star"], 9)
        self.assertEqual(sitting_natal["water_star"], 9)

        # Formations detection
        formation_codes = [f["code"] for f in data_p9["formations"]]
        self.assertIn("SHUANG_XING_DAO_ZUO", formation_codes)

        # 2. Period 8 Sitting Chou (30° NE), Facing Wei (210° SW) -> Wang Shan Wang Xiang
        res_p8 = self.calc_engine.calculate_house_flying_stars(sitting_degree=30.0, period=8)
        self.assertTrue(res_p8["success"])
        data_p8 = res_p8["data"]
        p8_codes = [f["code"] for f in data_p8["formations"]]
        self.assertIn("WANG_SHAN_WANG_XIANG", p8_codes)
        self.assertIn("HE_SHI_10", p8_codes)
        self.assertEqual(data_p8["natal_chart"]["NE"]["mountain_star"], 8)
        self.assertEqual(data_p8["natal_chart"]["SW"]["water_star"], 8)

        # 3. Ti Gua boundary replacement test (> 4.5° off mountain center)
        res_ti = self.calc_engine.calculate_house_flying_stars(facing_degree=186.0, period=9)
        self.assertTrue(res_ti["success"])
        self.assertTrue(res_ti["data"]["is_ti_gua"])
        self.assertIn("替卦", res_ti["data"]["chart_mode"])

        # 4. Castle Gate verification
        castle_gates = data_p9["castle_gates"]
        self.assertEqual(castle_gates["facing_palace"], "S")
        self.assertIn("left_castle_gate", castle_gates)
        self.assertIn("right_castle_gate", castle_gates)

        # 5. Ling Shen / Zheng Shen Period 9 verification
        zero_spirit = data_p9["ling_shen_zheng_shen"]
        self.assertIn("ខាងត្បូង", zero_spirit["zheng_shen"])
        self.assertIn("ខាងជើង", zero_spirit["ling_shen"])

    # 20. Test House Flying Stars REST API Endpoint
    def test_20_house_flying_stars_api_endpoint(self):
        """Verify /api/calculate/house-flying-stars endpoint handler."""
        from api.server import calculate_house_flying_stars, HouseFlyingStarsRequest

        req = HouseFlyingStarsRequest(
            facing_degree=180.0,
            period=9
        )
        res = calculate_house_flying_stars(req)
        self.assertTrue(res["success"])
        self.assertIn("natal_chart", res["data"])
        self.assertIn("formations", res["data"])
        self.assertIn("castle_gates", res["data"])
        self.assertEqual(res["data"]["period"], 9)

    # 21. Test BaZi Mathematical Precision (JDN, Wu Hu Dun, Wu Shu Dun, Li Chun, Cang Gan)
    def test_21_bazi_mathematical_precision(self):
        """Verify astronomical JDN, Five Tigers, Five Rats, and Li Chun cutoff in BaZi."""
        # 1. Historical Anchor: 2000-01-01 12:00 -> 己卯 丙子 戊午 戊午
        res_2000 = self.calc_engine.calculate_bazi("2000-01-01", "12:00")
        self.assertTrue(res_2000["success"])
        p_2000 = res_2000["data"]["pillars"]
        self.assertEqual(p_2000["year"]["ganzhi"], "己卯")
        self.assertEqual(p_2000["month"]["ganzhi"], "丙子")
        self.assertEqual(p_2000["day"]["ganzhi"], "戊午")
        self.assertEqual(p_2000["time"]["ganzhi"], "戊午")
        self.assertEqual(res_2000["data"]["day_master"]["stem"], "戊")

        # 2. Historical Anchor: 1988-05-15 10:30 -> 戊辰 丁巳 庚午 辛巳
        res_1988 = self.calc_engine.calculate_bazi("1988-05-15", "10:30")
        self.assertTrue(res_1988["success"])
        p_1988 = res_1988["data"]["pillars"]
        self.assertEqual(p_1988["year"]["ganzhi"], "戊辰")
        self.assertEqual(p_1988["month"]["ganzhi"], "丁巳")
        self.assertEqual(p_1988["day"]["ganzhi"], "庚午")
        self.assertEqual(p_1988["time"]["ganzhi"], "辛巳")
        self.assertEqual(res_1988["data"]["day_master"]["stem"], "庚")
        self.assertIn("戊", p_1988["year"]["hidden_stems"])
        self.assertIn("丙", p_1988["month"]["hidden_stems"])

        # 3. Li Chun boundary in 2024 (Feb 4):
        # Feb 3 (Before Li Chun) belongs to 2023 癸卯 year, 乙丑 month
        res_before = self.calc_engine.calculate_bazi("2024-02-03", "12:00")
        self.assertEqual(res_before["data"]["pillars"]["year"]["ganzhi"], "癸卯")
        self.assertEqual(res_before["data"]["pillars"]["month"]["ganzhi"], "乙丑")

        # Feb 5 (After Li Chun) belongs to 2024 甲辰 year, 丙寅 month
        res_after = self.calc_engine.calculate_bazi("2024-02-05", "12:00")
        self.assertEqual(res_after["data"]["pillars"]["year"]["ganzhi"], "甲辰")
        self.assertEqual(res_after["data"]["pillars"]["month"]["ganzhi"], "丙寅")

        # 4. Five Rats Seeking Hour (五鼠遁元) test
        # Day Geng (庚) -> 00:00 is 丙子, 12:00 is 壬午, 18:00 is 乙酉
        res_zi = self.calc_engine.calculate_bazi("1988-05-15", "00:00")
        self.assertEqual(res_zi["data"]["pillars"]["time"]["ganzhi"], "丙子")
        res_wu = self.calc_engine.calculate_bazi("1988-05-15", "12:00")
        self.assertEqual(res_wu["data"]["pillars"]["time"]["ganzhi"], "壬午")
        res_you = self.calc_engine.calculate_bazi("1988-05-15", "18:00")
        self.assertEqual(res_you["data"]["pillars"]["time"]["ganzhi"], "乙酉")

    # 22. Test Tung Shu Almanac Precision (Day Stem offset & 12 Day Officers)
    def test_22_tung_shu_almanac_precision(self):
        """Verify Day Stem offset and 12 Day Officers (Dong Gong Ze Ri) in Tung Shu."""
        from datetime import date
        from engines.celestial_astrology_engine import CelestialAstrologyEngine

        celestial = CelestialAstrologyEngine()

        # 1. Reference Date: 2000-01-01 must be Wu-Wu (戊午), NOT Jia-Wu (甲午)
        alm_2000 = celestial.calculate_global_almanac(date(2000, 1, 1))
        self.assertEqual(alm_2000["day_ganzhi"], "戊午")
        # In Month Zi (Rat), Day Wu (Horse) clashes -> 破 (Po / ថ្ងៃបំបែក)
        self.assertEqual(alm_2000["day_officer"]["name"], "ថ្ងៃបំបែក")

        # 2. Date: 1988-05-15 must be Geng-Wu (庚午)
        alm_1988 = celestial.calculate_global_almanac(date(1988, 5, 15))
        self.assertEqual(alm_1988["day_ganzhi"], "庚午")
        # In Month Si (Snake), Day Wu (Horse) is Chu (除 / ថ្ងៃកម្ចាត់)
        self.assertEqual(alm_1988["day_officer"]["name"], "ថ្ងៃកម្ចាត់")

        # 3. Date: 2026-09-03 (Today) must be Geng-Chen (庚辰)
        alm_today = celestial.calculate_global_almanac(date(2026, 9, 3))
        self.assertEqual(alm_today["day_ganzhi"], "庚辰")
        # In Month Shen (Monkey), Day Chen (Dragon) is Cheng (成 / ថ្ងៃជោគជ័យ)
        self.assertEqual(alm_today["day_officer"]["name"], "ថ្ងៃជោគជ័យ")

    # 23. Test Life Gua Astronomical Li Chun Cutoff Precision
    def test_23_life_gua_li_chun_precision(self):
        """Verify Li Chun solar term cutoff for Life Gua (1990-01-15 vs 1990-05-15, etc.)."""
        # 1. Male born 1990-01-15 (Before Li Chun Feb 4) -> 1989 solar year -> Gua 2 Kun (West Group)
        g_m_bef = self.calc_engine.calculate_life_gua(birth_year="1990-01-15", gender="male")
        self.assertTrue(g_m_bef["success"])
        self.assertEqual(g_m_bef["data"]["solar_year"], 1989)
        self.assertTrue(g_m_bef["data"]["is_before_li_chun"])
        self.assertEqual(g_m_bef["data"]["gua_number"], 2)
        self.assertEqual(g_m_bef["data"]["trigram"], "Kun")
        self.assertFalse(g_m_bef["data"]["is_east_group"])
        self.assertIn("1989", g_m_bef["data"]["li_chun_note"])

        # 2. Male born 1990-05-15 (After Li Chun) -> 1990 solar year -> Gua 1 Kan (East Group)
        g_m_aft = self.calc_engine.calculate_life_gua(birth_year=1990, gender="male", birth_date="1990-05-15")
        self.assertTrue(g_m_aft["success"])
        self.assertEqual(g_m_aft["data"]["solar_year"], 1990)
        self.assertFalse(g_m_aft["data"]["is_before_li_chun"])
        self.assertEqual(g_m_aft["data"]["gua_number"], 1)
        self.assertEqual(g_m_aft["data"]["trigram"], "Kan")
        self.assertTrue(g_m_aft["data"]["is_east_group"])

        # 3. Female born 1990-01-15 (Before Li Chun) -> 1989 solar year -> Gua 4 Xun (East Group)
        g_f_bef = self.calc_engine.calculate_life_gua(birth_year="1990-01-15", gender="female")
        self.assertEqual(g_f_bef["data"]["solar_year"], 1989)
        self.assertEqual(g_f_bef["data"]["gua_number"], 4)
        self.assertEqual(g_f_bef["data"]["trigram"], "Xun")
        self.assertTrue(g_f_bef["data"]["is_east_group"])

        # 4. Female born 1990-05-15 (After Li Chun) -> 1990 solar year -> Gua 8 Gen (West Group, 5->8)
        g_f_aft = self.calc_engine.calculate_life_gua(birth_year=1990, gender="female", birth_date="1990-05-15")
        self.assertEqual(g_f_aft["data"]["solar_year"], 1990)
        self.assertEqual(g_f_aft["data"]["gua_number"], 8)
        self.assertEqual(g_f_aft["data"]["trigram"], "Gen")
        self.assertFalse(g_f_aft["data"]["is_east_group"])

        # 5. 2024 Cutoff: 2024-02-03 (Gua 4) vs 2024-02-05 (Gua 3) for Male
        g_24_bef = self.calc_engine.calculate_life_gua(2024, "male", birth_date="2024-02-03")
        self.assertEqual(g_24_bef["data"]["solar_year"], 2023)
        self.assertEqual(g_24_bef["data"]["gua_number"], 4)

        g_24_aft = self.calc_engine.calculate_life_gua(2024, "male", birth_date="2024-02-05")
        self.assertEqual(g_24_aft["data"]["solar_year"], 2024)
        self.assertEqual(g_24_aft["data"]["gua_number"], 3)

        # 6. API Endpoint check (/api/calculate/gua with birth_date)
        from api.server import calculate_gua, LifeGuaRequest
        req = LifeGuaRequest(birth_year=1990, gender="male", birth_date="1990-01-15")
        api_res = calculate_gua(req)
        self.assertTrue(api_res["success"])
        self.assertEqual(api_res["data"]["gua_number"], 2)
        self.assertEqual(api_res["data"]["solar_year"], 1989)

    # 24. Test Software Engineering Audit Fixes (Dependencies, Flying Stars Params, Gemini 404 Resilience, Web Form)
    def test_24_software_engineering_audit(self):
        """Verify Software Engineering Audit fixes across system components."""
        # 1. Dependency: lunar_python is installed and functional
        import lunar_python
        from lunar_python import Solar, Lunar
        self.assertIsNotNone(Solar)
        self.assertIsNotNone(Lunar)

        # 2. Flying Stars API Endpoint accepts house_degree / facing_mountain / period
        from api.server import calculate_flying_stars, FlyingStarsRequest
        # A: house_degree + period
        req_deg = FlyingStarsRequest(year=2026, house_degree=180.0, period=9)
        res_deg = calculate_flying_stars(req_deg)
        self.assertTrue(res_deg["success"])
        self.assertIn("house_natal_chart", res_deg["data"])
        self.assertEqual(res_deg["data"]["house_natal_chart"]["period"], 9)
        self.assertEqual(res_deg["data"]["house_natal_chart"]["facing"]["mountain"], "午")

        # B: facing_mountain + period
        req_mtn = FlyingStarsRequest(year=2026, facing_mountain="子", period=9)
        res_mtn = calculate_flying_stars(req_mtn)
        self.assertTrue(res_mtn["success"])
        self.assertIn("house_natal_chart", res_mtn["data"])
        self.assertEqual(res_mtn["data"]["house_natal_chart"]["facing"]["mountain"], "子")

        # 3. Omni AI Mesh Gemini 404 Resilience test
        from engines.omni_ai_bridge import GeminiMultiKeyPool
        pool = GeminiMultiKeyPool(key_pool=["test_dummy_key"])
        # Should gracefully return None without unhandled 404 crash
        res_pool = pool.generate_content("Sys instruction", "User query")
        self.assertIsNone(res_pool)

        # 4. Web index.html contains guaDateInput type=date for Li Chun
        import pathlib
        html_content = pathlib.Path("web/index.html").read_text(encoding="utf-8")
        self.assertIn('id="guaDateInput"', html_content)
        self.assertIn('type="date"', html_content)

    # 25. Test Extended Metaphysics Standards & Engineering Integrity
    def test_25_extended_metaphysics_and_engineering_integrity(self):
        """Verify 28 Lunar Mansions alignment, Monthly Flying Stars, and unified Li Chun across engines."""
        from datetime import date
        from engines.celestial_astrology_engine import CelestialAstrologyEngine
        from engines.family_synergy_engine import FamilySynergyEngine
        from engines.mahasneh_love_engine import MahaSnehLoveEngine

        # 1. Verify 28 Lunar Mansions (28 Xiu) Calibration
        celestial = CelestialAstrologyEngine()
        almanac_2000 = celestial.calculate_global_almanac(date(2000, 1, 1))
        # 2000-01-01 was 胃 (Wei - index 16)
        self.assertIn("តារាវេយធូជី", almanac_2000["constellation"])

        almanac_today = celestial.calculate_global_almanac(date(2026, 9, 3))
        # 2026-09-03 was 奎 (Kui - index 14)
        self.assertIn("តារាគុយម៉ុកឡាង", almanac_today["constellation"])

        # 2. Verify Xuan Kong Monthly Flying Star calculation
        # Year 2026 (Horse 午, Group 1 -> Starts at 8, Month 9 You -> Star 1)
        month_res = self.calc_engine.calculate_flying_stars(2026, month=9)
        self.assertTrue(month_res["success"])
        self.assertEqual(month_res["data"]["monthly_center_star"], 1)
        self.assertIn("monthly_grid", month_res["data"])
        self.assertIn("NW", month_res["data"]["monthly_danger_palaces"])  # 5 in NW
        self.assertIn("S", month_res["data"]["monthly_danger_palaces"])   # 2 in S

        # 3. Verify FamilySynergyEngine exact Li Chun handling
        fam_engine = FamilySynergyEngine()
        # Born 1990-01-15 -> Before Li Chun -> Belongs to 1989 (Snake)
        prof_bef = fam_engine.calculate_member_profile("1990-01-15", gender="male")
        self.assertEqual(prof_bef["zodiac_animal"], "Snake")
        # Born 1990-05-15 -> After Li Chun -> Belongs to 1990 (Horse)
        prof_aft = fam_engine.calculate_member_profile("1990-05-15", gender="male")
        self.assertEqual(prof_aft["zodiac_animal"], "Horse")

        # 4. Verify MahaSnehLoveEngine exact Li Chun handling
        love_engine = MahaSnehLoveEngine()
        solar_bef = love_engine._get_solar_year("1990-01-15")
        self.assertEqual(solar_bef, 1989)
        solar_aft = love_engine._get_solar_year("1990-05-15")
        self.assertEqual(solar_aft, 1990)

    # 26. Test Vision Audit API Endpoint
    def test_26_vision_audit_api_endpoint(self):
        """Verify that /api/vision/audit accepts base64 image data and returns structured audit."""
        from api.server import audit_floor_plan_image, VisionAuditBase64Request
        dummy_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        req = VisionAuditBase64Request(image_base64=dummy_png, mime_type="image/png", user_notes="Living room")
        res = audit_floor_plan_image(req)
        self.assertTrue(res["success"])
        self.assertIn("audit_report", res)
        self.assertGreaterEqual(len(res["audit_report"]), 3500)

    # 27. Test Family CRUD Endpoints
    def test_27_family_crud_endpoints(self):
        """Verify POST, GET, and DELETE /api/family/member endpoints."""
        from api.server import add_or_update_family_member, get_family_profile, delete_family_member, FamilyMemberRequest, DeleteFamilyMemberRequest
        test_uid = 999888777
        req_add = FamilyMemberRequest(telegram_id=test_uid, relation="spouse", birth_date="1992-06-15", name="TestingSpouse")
        res_add = add_or_update_family_member(req_add)
        self.assertTrue(res_add["success"])

        res_get = get_family_profile(test_uid)
        self.assertTrue(res_get["success"])
        self.assertGreaterEqual(res_get["count"], 1)

        req_del = DeleteFamilyMemberRequest(telegram_id=test_uid, relation_type="spouse", name="TestingSpouse")
        res_del = delete_family_member(req_del)
        self.assertTrue(res_del["success"])

    # 28. Test Zenith Master Metaphysics and Software Engineering Standards (7 Points Audit)
    def test_28_zenith_master_metaphysics_and_engineering_audit(self):
        """Verify all 7 Classical Metaphysics & Software Engineering audit points."""
        from datetime import date
        from engines.celestial_astrology_engine import CelestialAstrologyEngine
        from database.db_manager import get_db_connection

        calc = self.calc_engine
        celestial = CelestialAstrologyEngine()

        # 1. TI_GUA_MAP has all 24 mountains including 戌: 6
        self.assertEqual(len(calc.TI_GUA_MAP), 24)
        self.assertIn("戌", calc.TI_GUA_MAP)
        self.assertEqual(calc.TI_GUA_MAP["戌"], 6)

        # 2. Authentic Tung Shu Almanac Directions for 2000-01-01 (戊午)
        almanac_2000 = celestial.calculate_global_almanac(date(2000, 1, 1))
        # Day Stem 戊 -> Wealth God North (正北), Joy God Southeast (东南)
        self.assertIn("ខាងជើង (正北)", almanac_2000["auspicious_directions"]["wealth_god"])
        self.assertIn("អាគ្នេយ៍ (东南)", almanac_2000["auspicious_directions"]["joy_god"])
        # Day Branch 午 -> San Sha North (煞北)
        self.assertIn("ខាងជើង (煞北)", almanac_2000["auspicious_directions"]["inauspicious_dir"])

        # 3. Castle Gate with Home Palace Polarity
        # Sitting 0° North (Kan), Facing 180° South (Li - Wu 午, Tian Dragon) in Period 9
        res_house = calc.calculate_house_flying_stars(sitting_degree=0.0, period=9)
        self.assertTrue(res_house["success"])
        self.assertIn("castle_gates", res_house["data"])
        cg = res_house["data"]["castle_gates"]
        self.assertIn("left_castle_gate", cg)
        self.assertIn("right_castle_gate", cg)

        # 4. Da Kong Wang (大空亡) vs Xiao Kong Wang (小空亡)
        # Degree 22.0° is within 1.5° of 22.5° (border between Kan and Gen) -> Da Kong Wang
        res_dkw = calc.calculate_house_flying_stars(sitting_degree=22.0, period=9)
        self.assertTrue(res_dkw["data"]["is_da_kong_wang"])
        self.assertEqual(res_dkw["data"]["formations"][0]["code"], "DA_KONG_WANG")

        # 5. Formation Detection for Fu Mu San Ban Gua, Lian Zhu San Ban Gua, Fu Yin, Fan Yin
        # Mock natal chart for Fu Mu San Ban Gua (all palaces have 1-4-7, 2-5-8, or 3-6-9)
        mock_fu_mu = {
            p: {"mountain_star": 1, "period_star": 4, "water_star": 7} for p in calc.LO_SHU_PATH
        }
        forms_fu_mu = calc._detect_xuan_kong_formations(mock_fu_mu, 9, "N", "S")
        self.assertTrue(any(f["code"] == "FU_MU_SAN_BAN_GUA" for f in forms_fu_mu))

        # Mock natal chart for Lian Zhu San Ban Gua (consecutive 1-2-3)
        mock_lian_zhu = {
            p: {"mountain_star": 1, "period_star": 2, "water_star": 3} for p in calc.LO_SHU_PATH
        }
        forms_lian_zhu = calc._detect_xuan_kong_formations(mock_lian_zhu, 9, "N", "S")
        self.assertTrue(any(f["code"] == "LIAN_ZHU_SAN_BAN_GUA" for f in forms_lian_zhu))

        # 6. SQLite WAL Mode busy_timeout = 15000
        with get_db_connection() as conn:
            row = conn.execute("PRAGMA busy_timeout;").fetchone()
            self.assertEqual(row[0], 15000)

    # 29. Test Annual Afflictions Calculation (Tai Sui, Sui Po, San Sha, Wu Huang)
    def test_29_annual_afflictions_calculation(self):
        """Verify Grand Annual Afflictions (四大年煞) across multiple years."""
        calc = self.calc_engine

        # 2026: Year of Horse (丙午)
        # Tai Sui at 午 (S2), Sui Po at 子 (N2), San Sha at North (亥, 子, 丑), Wu Huang at South
        aff_2026 = calc.calculate_annual_afflictions(2026)
        self.assertEqual(aff_2026["tai_sui"]["mountain"], "午")
        self.assertEqual(aff_2026["sui_po"]["mountain"], "子")
        self.assertEqual(aff_2026["san_sha"]["sector"], "N")
        self.assertEqual(aff_2026["san_sha"]["mountains"], ["亥", "子", "丑"])
        self.assertEqual(aff_2026["wu_huang"]["palace"], "S")

        # 2024: Year of Dragon (甲辰)
        # Tai Sui at 辰, Sui Po at 戌, San Sha at South (巳, 午, 未), Wu Huang at West
        aff_2024 = calc.calculate_annual_afflictions(2024)
        self.assertEqual(aff_2024["tai_sui"]["mountain"], "辰")
        self.assertEqual(aff_2024["sui_po"]["mountain"], "戌")
        self.assertEqual(aff_2024["san_sha"]["sector"], "S")
        self.assertEqual(aff_2024["san_sha"]["mountains"], ["巳", "午", "未"])
        self.assertEqual(aff_2024["wu_huang"]["palace"], "W")

        # 2025: Year of Snake (乙巳)
        # Tai Sui at 巳, Sui Po at 亥, San Sha at East (寅, 卯, 辰), Wu Huang at Northeast
        aff_2025 = calc.calculate_annual_afflictions(2025)
        self.assertEqual(aff_2025["tai_sui"]["mountain"], "巳")
        self.assertEqual(aff_2025["sui_po"]["mountain"], "亥")
        self.assertEqual(aff_2025["san_sha"]["sector"], "E")
        self.assertEqual(aff_2025["san_sha"]["mountains"], ["寅", "卯", "辰"])
        self.assertEqual(aff_2025["wu_huang"]["palace"], "NE")

    # 30. Test Day Master-Specific Wealth and Career Scoring
    def test_30_bazi_day_master_specific_wealth_career(self):
        """Verify BaZi wealth (我克者为妻财) and career (克我者为官杀) adhere to Day Master elements."""
        alert = self.alert_engine

        # Day Master 庚 (Metal) -> Wealth is Wood (甲, 乙, 寅, 卯), Officer is Fire (丙, 丁, 巳, 午)
        # Day with Wood (甲寅) -> High wealth
        score_metal_on_wood = alert._compute_wealth_score("庚", "甲寅")
        # Day with Earth (戊戌) -> Earth produces Metal (Resource, not Wealth)
        score_metal_on_earth = alert._compute_wealth_score("庚", "戊戌")
        self.assertGreater(score_metal_on_wood, score_metal_on_earth)

        # Day Master 壬 (Water) -> Wealth is Fire (丙, 丁, 巳, 午), Officer is Earth (戊, 己, 辰, 戌, 丑, 未)
        # Day with Fire (丙午) -> High wealth for Water Day Master
        score_water_on_fire = alert._compute_wealth_score("壬", "丙午")
        # Day with Wood (甲寅) -> Wood drains Water (Output, not Wealth)
        score_water_on_wood = alert._compute_wealth_score("壬", "甲寅")
        self.assertGreater(score_water_on_fire, score_water_on_wood)

    # 31. Test Pre-Li Chun January Flying Star Cutoff
    def test_31_pre_lichun_january_flying_star(self):
        """Verify that January queries before Li Chun belong to previous solar year's star."""
        calc = self.calc_engine

        # 2026 Month 1 (January): before Li Chun -> Center star belongs to 2025 (Star 2)
        res_jan = calc.calculate_flying_stars(2026, month=1)
        self.assertEqual(res_jan["data"]["solar_year"], 2025)
        self.assertEqual(res_jan["data"]["annual_center_star"], 2)
        self.assertIsNotNone(res_jan["data"]["li_chun_note"])

        # 2026 Month 3 (March): after Li Chun -> Center star belongs to 2026 (Star 1)
        res_mar = calc.calculate_flying_stars(2026, month=3)
        self.assertEqual(res_mar["data"]["solar_year"], 2026)
        self.assertEqual(res_mar["data"]["annual_center_star"], 1)
        self.assertIsNone(res_mar["data"]["li_chun_note"])

    # 32. Test Annual Afflictions API Endpoint
    def test_32_annual_afflictions_api_endpoint(self):
        """Verify REST API endpoint calculate_annual_afflictions returns valid data."""
        from api.server import calculate_annual_afflictions, AnnualAfflictionsRequest

        # Test with POST body request schema
        res_post = calculate_annual_afflictions(req=AnnualAfflictionsRequest(year=2026))
        self.assertTrue(res_post["success"])
        self.assertEqual(res_post["data"]["tai_sui"]["mountain"], "午")
        self.assertEqual(res_post["data"]["san_sha"]["sector"], "N")

        # Test with GET query parameter
        res_get = calculate_annual_afflictions(year=2024)
        self.assertTrue(res_get["success"])
        self.assertEqual(res_get["data"]["tai_sui"]["mountain"], "辰")
        self.assertEqual(res_get["data"]["san_sha"]["sector"], "S")


if __name__ == "__main__":
    unittest.main()
