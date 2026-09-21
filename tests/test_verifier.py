import copy
import json
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "verifier"))
from verify import check


class VerifierTests(unittest.TestCase):
    def setUp(self):
        fixture = Path(__file__).resolve().parents[1] / "examples" / "synthetic-venture" / "architecture.json"
        self.artifact = json.loads(fixture.read_text())

    def test_passing_fixture(self):
        self.assertTrue(all(item["status"] == "PASS" for item in check(self.artifact)))

    def test_rejects_bad_trace(self):
        bad = copy.deepcopy(self.artifact)
        bad["requirements"][0]["component_ids"] = ["MISSING"]
        self.assertTrue(any(item["rule"] == "component-trace" for item in check(bad)))

    def test_rejects_weak_margin(self):
        bad = copy.deepcopy(self.artifact)
        bad["financial_model"]["fmos"] = 0.1
        bad["financial_model"]["price_ceiling"] = 132
        self.assertTrue(any(item["rule"] == "fmos-gate" for item in check(bad)))
