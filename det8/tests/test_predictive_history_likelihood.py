"""Two fixed regressions, exactly four helper calls.

Use the adjacent frozen candidate, or ../models/predictive_history.py when this
test is later placed in det8/tests. File loading avoids det8 package setup.
"""
import importlib.util
import math
from pathlib import Path
import unittest


def _load_subject():
    directory = Path(__file__).resolve().parent
    source = directory / "predictive_history.py"
    if not source.is_file():
        source = directory.parent / "models" / "predictive_history.py"
    if not source.is_file():
        raise FileNotFoundError("adjacent candidate or installed relative model required")
    spec = importlib.util.spec_from_file_location("_ret033_predictive_history", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the pinned source file")
    subject = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(subject)
    return subject


_SUBJECT = _load_subject()


class TwoSampleLikelihoodTests(unittest.TestCase):
    def test_primary_value_and_complete_group_swap(self):
        primary = _SUBJECT.test_history_distinction([0.8, 0.2], [0.5, 0.5], 20, 100)
        swapped = _SUBJECT.test_history_distinction([0.5, 0.5], [0.8, 0.2], 100, 20)
        # Independent closed expression from integer rows (16,4),(50,50),
        # not a second use of the implementation's row-statistic helper.
        expected = 32 * math.log(16 / 11) + 8 * math.log(4 / 9) + 100 * math.log(100 / 99)
        self.assertAlmostEqual(primary["G"], expected, delta=1e-12)
        self.assertAlmostEqual(swapped["G"], expected, delta=1e-12)
        self.assertAlmostEqual(primary["G"], swapped["G"], delta=1e-12)
        self.assertEqual(primary["distinct"], swapped["distinct"])
        self.assertTrue(primary["distinct"])  # existing diagnostic cutoff only
        for result in (primary, swapped):
            self.assertEqual(result["df"], 1)
            self.assertEqual(result["critical_value_0.05"], 3.841)
            self.assertEqual(set(result), {"G", "df", "critical_value_0.05", "distinct", "interpretation"})

    def test_equal_law_zero_in_both_group_orders(self):
        original = _SUBJECT.test_history_distinction([0.5, 0.5], [0.5, 0.5], 20, 100)
        swapped = _SUBJECT.test_history_distinction([0.5, 0.5], [0.5, 0.5], 100, 20)
        self.assertEqual(original["G"], 0.0)
        self.assertEqual(swapped["G"], 0.0)
        self.assertEqual(original["distinct"], swapped["distinct"])
        self.assertFalse(original["distinct"])
        self.assertEqual(original["df"], swapped["df"])
        self.assertEqual(original["critical_value_0.05"], swapped["critical_value_0.05"])


if __name__ == "__main__":
    unittest.main()
