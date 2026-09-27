"""Numerical regression and independent integral checks, not a stability proof."""
import importlib.util
import json
from pathlib import Path
import unittest


HOME = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "self_gravity_reproduction", HOME / "复算自引力背景.py"
)
MODEL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODEL)


class SelfGravityReproduction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = MODEL.run_reproduction()

    def test_historical_branch_and_independent_mass_charge_integrals(self):
        old = json.loads((HOME / "V3_7_self_gravity_branch.json").read_text("utf-8"))
        self.assertEqual(len(self.result["branch"]), len(old["rows"]))
        for new, reference in zip(self.result["branch"], old["rows"]):
            self.assertAlmostEqual(new["G"], reference["G"])
            for key in ("ADM_mass", "w", "f0"):
                self.assertLess(abs(new[key] - reference[key]), 2e-7)
            self.assertGreater(new["min_N_sampled"], 0)
            self.assertLess(abs(new["integral_Q_error"]), 2e-7)
            self.assertLess(abs(new["integral_mass_error"]), 2e-7)
            self.assertLess(abs(new["Komar_minus_ADM"]), 2e-7)

    def test_region_refinement_and_first_law_convergence(self):
        base = self.result["branch"][-1]
        refined = self.result["refinement"]
        self.assertLess(abs(base["ADM_mass"] - refined["ADM_mass"]), 2e-7)
        errors = [abs(row["difference"]) for row in self.result["mass_charge"]]
        self.assertLess(errors[-1], 2e-8)
        for coarse, fine in zip(errors, errors[1:]):
            self.assertGreater(coarse / fine, 3.5)
            self.assertLess(coarse / fine, 4.5)


if __name__ == "__main__":
    unittest.main()
