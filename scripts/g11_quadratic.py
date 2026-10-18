#!/usr/bin/env python3
"""Configured satellite clock series: descriptive exponential, log-linear and quadratic fits."""

from __future__ import annotations

import argparse
from pathlib import Path

from det8.applied_physics.applied_tests import aging_fit_report
from det8.applied_physics.adversarial import rss_between
from det8.applied_physics.ingest import collect_daily_clock_drifts

SVNS = ("G01", "G02", "G03", "G05", "G08", "G11",
        "G13", "G16", "G18", "G22", "G24", "G30")


def _fit_quadratic(t, y):
    n = len(t)
    S22 = sum(ti**4 for ti in t); S21 = sum(ti**3 for ti in t)
    S20 = sum(ti**2 for ti in t); S11 = S20; S10 = sum(ti for ti in t); S00 = n
    S2y = sum(ti**2 * yi for ti, yi in zip(t, y))
    S1y = sum(ti * yi for ti, yi in zip(t, y))
    S0y = sum(y)
    A = [[S22, S21, S20], [S21, S11, S10], [S20, S10, S00]]
    b = [S2y, S1y, S0y]
    for i in range(3):
        piv = A[i][i]
        if abs(piv) < 1e-15:
            return {"rss": float("inf"), "params": {"a": 0.0, "b": 0.0, "c": 0.0}}
        for j in range(i + 1, 3):
            f = A[j][i] / piv
            for k in range(i, 3):
                A[j][k] -= f * A[i][k]
            b[j] -= f * b[i]
    x = [0.0] * 3
    for i in reversed(range(3)):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, 3))) / A[i][i]
    a, bb, c = x
    pred = [a * ti**2 + bb * ti + c for ti in t]
    return {"rss": rss_between(pred, y),
            "params": {"a": a, "b": bb, "c": c}}


def analyze_clock_directory(
    clock_dir: str | Path,
    svns: tuple[str, ...] = SVNS,
    *,
    min_days: int = 10,
) -> dict:
    """Compare descriptive fits using dated products, without BIC winner claims."""
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
            report = aging_fit_report(records, extra_fitters={"quadratic": _fit_quadratic})
        except ValueError as exc:
            rows.append({"svn": svn, "n": len(records), "error": str(exc)})
            continue
        rows.append({"svn": svn, "n": len(records), **report,
                     "quadratic": report["fits"]["quadratic"]})
    return {"rows": rows, "tally": None, "n_files": ingest["n_files"],
            "accepted_rows": ingest["accepted_rows"], "rejected_rows": ingest["rejected_rows"]}


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

    print(
        f"parsed {result['n_files']} files: {result['accepted_rows']} accepted rows, "
        f"{result['rejected_rows']} rejected rows"
    )
    print("SVN  n  span_days  descriptive training RSS (exponential / log-linear / quadratic)")
    for row in result["rows"]:
        if "error" in row:
            print(f"{row['svn']:4s} {row['n']:4d}  {row['error']}")
            continue
        fits = row["fits"]
        print(f"{row['svn']:4s} {row['n']:4d} {row['span_days']:.3f} "
              f"{fits['exponential_offset_grid']['rss']} / "
              f"{fits['log_linear']['rss']} / {fits['quadratic']['rss']}")
        print(f"  BIC unavailable: {row['bic_reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
