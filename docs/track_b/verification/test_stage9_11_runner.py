"""Integrity regressions for the composite report, not simulated physics evidence."""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_stage9_11_verification as runner


class TestCompositeReporting(unittest.TestCase):
    def test_skipped_case_cannot_be_reported_as_all_passed(self):
        result = mock.Mock(failures=[], errors=[], skipped=[("case", "reason")], testsRun=3)
        result.wasSuccessful.return_value = True
        def one_case(_):
            return unittest.TestSuite([unittest.FunctionTestCase(lambda: None)])
        output = io.StringIO()
        with (
            mock.patch.object(unittest.TestLoader, "loadTestsFromModule", side_effect=one_case),
            mock.patch.object(unittest.TextTestRunner, "run", return_value=result),
            contextlib.redirect_stdout(output),
        ):
            report = runner.run_all_unit_tests(verbosity=0)
        self.assertFalse(report["passed"])
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(all(v["status"] == "FAIL" for v in report["breakdown"].values()))
        self.assertNotIn("[PASS]", output.getvalue())

    def test_benchmarks_only_never_reports_unit_passes(self):
        # Exercise the CLI aggregation while replacing expensive benchmarks with
        # explicit test fixtures. No benchmark result is claimed by this test.
        with tempfile.TemporaryDirectory() as directory:
            output = os.path.join(directory, "report.json")
            with (
                mock.patch.object(sys, "argv", ["runner", "--benchmarks-only", "--output", output]),
                mock.patch.object(runner, "run_all_unit_tests") as run_units,
                mock.patch.object(runner, "run_gate9_audit", return_value={"gate9_summary": {"status": "PASS"}}),
                mock.patch.object(runner, "run_gate10_audit", return_value={"status": "PASS"}),
                mock.patch.object(runner, "run_gate11_audit", return_value={"status": "PASS"}),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(runner.main(), 0)
            run_units.assert_not_called()
            with open(output, encoding="utf-8") as stream:
                report = json.load(stream)
        self.assertEqual(report["unit_tests"]["status"], "NOT_RUN")
        self.assertEqual(report["unit_tests"]["total_tests_run"], 0)
        self.assertEqual(report["metadata"]["unit_tests_passed"], 0)
        self.assertGreater(report["metadata"]["unit_tests_total"], 0)
        self.assertTrue(report["metadata"]["benchmarks_passed"])
        self.assertFalse(report["metadata"]["all_gates_passed"])
        self.assertEqual(report["metadata"]["overall_status"], "INCOMPLETE")

    def test_benchmark_failure_is_not_hidden_by_unrun_tests(self):
        report = runner.build_master_results_payload(
            runner.unrun_unit_test_summary(),
            {"gate9_summary": {"status": "PASS"}},
            {"status": "FAIL"}, {"status": "PASS"}, 0.0)
        self.assertEqual(report["metadata"]["overall_status"], "FAIL")
        self.assertFalse(report["metadata"]["benchmarks_passed"])
        self.assertEqual(report["metadata"]["unit_tests_passed"], 0)


if __name__ == "__main__":
    unittest.main()
