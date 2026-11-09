"""Run: python -m unittest discover -s statistics-probability-advanced-20261109 -p 'test_*.py' -v"""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("advanced_analysis.py")
spec = importlib.util.spec_from_file_location("advanced_analysis", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class AdvancedAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = module.analyze(module.DEFAULT_DATA, repetitions=500, seed=42)

    def test_data_cleaning(self):
        self.assertEqual(self.result["cleaning"]["raw_rows"], 50)
        self.assertEqual(self.result["cleaning"]["clean_rows"], 48)
        self.assertEqual(self.result["cleaning"]["duplicate_ids"], 2)
        self.assertEqual(self.result["cleaning"]["invalid_negative_visits"], 1)

    def test_bootstrap_interval(self):
        d = self.result["bootstrap_difference_B_minus_A"]
        self.assertLess(d["percentile_95_interval"][0], d["percentile_95_interval"][1])
        self.assertGreater(d["observed"], 0)

    def test_p_values_and_bh(self):
        p = self.result["multiple_comparisons_BH"]
        for key, raw in p["raw_p"].items():
            self.assertGreaterEqual(p["adjusted_p"][key], raw)
            self.assertLessEqual(p["adjusted_p"][key], 1)
        self.assertTrue(0 <= self.result["permutation_two_sided"]["p_value"] <= 1)

    def test_entropy_and_bayes(self):
        h = self.result["district_entropy"]
        self.assertAlmostEqual(h["normalized"], 1.0, places=5)
        for row in self.result["bayesian_beta_binomial"].values():
            self.assertEqual(sum(row["beta_posterior"]), row["n"] + 2)
            self.assertGreater(row["posterior_mean"], 0)
            self.assertLess(row["posterior_mean"], 1)

    def test_no_time_series_claim(self):
        self.assertTrue(any("시간축" in line for line in self.result["limitations"]))

    def test_missing_columns_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            wrong = Path(tmp) / "wrong.csv"
            wrong.write_text("member_id,program\nM1,A\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Missing required"):
                module.clean_data(wrong)

if __name__ == "__main__":
    unittest.main()
