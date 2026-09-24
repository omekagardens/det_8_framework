#!/usr/bin/env python3
"""Run the isolated RI-35 tests or print deterministic worked input/output."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from fractions import Fraction
import json
from pathlib import Path
import sys
import unittest


def encode(value):
    """Keep rational output exact, including large derived denominators."""
    if type(value) is Fraction:
        return {"numerator": str(value.numerator), "denominator": str(value.denominator)}
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def worked():
    from timing import Bounds, Interval, Record, Request, infer, witness

    f = Fraction
    fixtures = (
        ("unknown_asymmetry", (0, 5, 7, 8), Bounds()),
        ("reciprocity", (0, 5, 7, 8), Bounds(asymmetry=Interval(f(0), f(0)))),
        ("bounded_asymmetry", (0, 5, 7, 8), Bounds(asymmetry=Interval(f(-1), f(1)))),
        (
            "bounded_directions",
            (0, 5, 7, 8),
            Bounds(forward=Interval(f(2), f(4)), reverse=Interval(f(2), f(4))),
        ),
        ("incompatible_asymmetry", (0, 5, 7, 8), Bounds(asymmetry=Interval(f(7), f(7)))),
        ("negative_turnaround", (0, 5, 4, 8), Bounds()),
        ("negative_roundtrip", (0, 1, 3, 1), Bounds()),
    )
    cases = []
    for name, values, bounds in fixtures:
        records = tuple(
            Record(
                record_id=f"{name}-{slot}",
                exchange_id=name,
                slot=slot,
                clock_id=clock,
                message_id=message,
                unit="seconds",
                value=f(value),
            )
            for slot, clock, message, value in zip(
                ("A1", "B2", "B3", "A4"),
                ("A", "B", "B", "A"),
                ("outbound", "outbound", "reply", "reply"),
                values,
            )
        )
        request = Request(
            exchange_id=name,
            clock_a="A",
            clock_b="B",
            unit="seconds",
            premise_id="RI33-supplied-exact-clock-fixture",
            clock_model="shared_unit_rate_constant_offsets",
            uncertainty_model="exact",
            records=records,
            bounds=bounds,
            tolerance=f(1),
        )
        report = infer(request)
        witnesses = []
        if report.interval is not None:
            for theta in (report.interval.lower, report.estimate, report.interval.upper):
                attaining = witness(request, theta)
                if attaining is None:
                    raise RuntimeError("compatible worked target has no attaining witness")
                witnesses.append(asdict(attaining))
        cases.append(
            {"name": name, "request": asdict(request), "report": asdict(report), "witnesses": witnesses}
        )
    print(json.dumps(encode({"format": "det-exact-timing-worked-v1", "cases": cases}), indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worked", action="store_true", help="print the seven RI-33 rational fixtures as JSON")
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    if args.worked:
        worked()
        return 0
    suite = unittest.defaultTestLoader.loadTestsFromName("test_timing")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = result.wasSuccessful() and result.testsRun > 0 and not result.skipped and not result.expectedFailures
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
