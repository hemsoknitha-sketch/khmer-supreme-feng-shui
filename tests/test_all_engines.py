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


if __name__ == "__main__":
    unittest.main()
