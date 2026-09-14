#!/usr/bin/env python3
"""Configured GNSS clock-aging adversarial: single-pass parse.

The naive run_clock_aging() re-parses all 365 daily files once per satellite
(and shells out to `gzip` per file). This script decompresses with the stdlib
gzip module and parses each file ONCE, extracting the daily drift for every
satellite of interest in a single pass, then runs the exponential versus log-linear
descriptive fit-error comparison.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from det8.applied_physics.applied_tests import aging_fit_report
from det8.applied_physics.ingest import collect_daily_clock_drifts

SVNS = ("G01", "G02", "G03", "G05", "G08", "G11",
        "G13", "G16", "G18", "G22", "G24", "G30")


def _strength(delta: float) -> str:
    a = abs(delta)
    if a < 2:
        return "none"
    if a < 6:
        return "positive"
    if a < 10:
        return "strong"
    return "very strong"


def analyze_clock_directory(
    clock_dir: str | Path,
    svns: tuple[str, ...] = SVNS,
    *,
    min_days: int = 10,
) -> dict:
    """Parse once and compare descriptive fits at the actual observation times."""
    if min_days < 3:
        raise ValueError("min_days must be at least 3")
    ingest = collect_daily_clock_drifts(clock_dir, svns)
    rows = []
    for svn in svns:
        records = ingest["daily_records"][svn]
        if len(records) < min_days:
            rows.append({"svn": svn, "n": len(records), "error": "too few days"})
            continue
        try:
            report = aging_fit_report(records)
        except ValueError as exc:
            rows.append({"svn": svn, "n": len(records), "error": str(exc)})
            continue
        rows.append({"svn": svn, "n": len(records), **report})
    return {"rows": rows, "n_files": ingest["n_files"],
            "accepted_rows": ingest["accepted_rows"], "rejected_rows": ingest["rejected_rows"],
            "n_kappa": None, "n_valid": sum("error" not in row for row in rows)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clock-dir", required=True, type=Path,
                        help="directory containing validated .CLK.gz products")
    parser.add_argument("--svns", nargs="+", default=list(SVNS),
                        help="satellite identifiers to analyze")
    parser.add_argument("--min-days", type=int, default=10,
                        help="minimum daily drift values required per satellite")
    args = parser.parse_args(argv)

    try:
        result = analyze_clock_directory(
            args.clock_dir,
            tuple(dict.fromkeys(args.svns)),
            min_days=args.min_days,
        )
    except (OSError, EOFError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2
    if result["n_files"] == 0:
        print(f"no .CLK.gz files found in {args.clock_dir}")
        return 1

    print("\n=== CONFIGURED CLOCK-AGING RESULTS ===")
    print(
        f"parsed {result['n_files']} files: {result['accepted_rows']} accepted rows, "
        f"{result['rejected_rows']} rejected rows"
    )
    print(f"descriptive fits for {result['n_valid']} satellites; BIC unavailable\n")
    for r in result["rows"]:
        if "error" in r:
            print(f"{r['svn']:4s}  {r['error']}")
        else:
            fits = r["fits"]
            print(f"{r['svn']:4s} n={r['n']:3d} span={r['span_days']:.3f} days "
                  f"tau={r['tau_best_days']} days "
                  f"RSS(exp)={fits['exponential_offset_grid']['rss']} "
                  f"RSS(log-linear)={fits['log_linear']['rss']}")
            print(f"  BIC unavailable: {r['bic_reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
