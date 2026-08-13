#!/usr/bin/env python3
"""Full-year (2023) GNSS clock-aging adversarial: single-pass parse.

The naive run_clock_aging() re-parses all 365 daily files once per satellite
(and shells out to `gzip` per file). This script decompresses with the stdlib
gzip module and parses each file ONCE, extracting the daily drift for every
satellite of interest in a single pass, then runs the κ-recovery vs IEEE-log
BIC comparison.
"""

from __future__ import annotations

import glob
import gzip
import os
import sys
from collections import defaultdict

ROOT = "/Volumes/AI_DATA/development/det_8_qwen"
sys.path.insert(0, ROOT)

from det8.applied_physics.applied_tests import _fit_exp_decay, _fit_ieee  # noqa: E402
from det8.applied_physics.ingest import daily_drift, parse_igs_clock  # noqa: E402
from det8.applied_physics import adversarial as adv  # noqa: E402

CLK_DIR = f"{ROOT}/det8/data/igs"
SVNS = ["G01", "G02", "G03", "G05", "G08", "G11",
        "G13", "G16", "G18", "G22", "G24", "G30"]


def _strength(delta: float) -> str:
    a = abs(delta)
    if a < 2:
        return "none"
    if a < 6:
        return "positive"
    if a < 10:
        return "strong"
    return "very strong"


def main() -> int:
    files = sorted(glob.glob(os.path.join(CLK_DIR, "*.CLK.gz")))
    if not files:
        print("no .CLK.gz files found in", CLK_DIR)
        return 1

    daily = defaultdict(list)
    for i, path in enumerate(files):
        with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        by_svn = defaultdict(list)
        for r in parse_igs_clock(text):
            by_svn[r["svn"]].append(r)
        for svn in SVNS:
            d = daily_drift(by_svn.get(svn, []))
            if d["drift_s_per_s"] is not None:
                daily[svn].append(d["drift_s_per_s"])
        if (i + 1) % 50 == 0 or (i + 1) == len(files):
            print(f"parsed {i + 1}/{len(files)}", flush=True)

    rows = []
    for svn in SVNS:
        y = daily[svn]
        if len(y) < 10:
            rows.append({"svn": svn, "n": len(y), "error": "too few days"})
            continue
        t = list(range(len(y)))
        det = _fit_exp_decay(t, y)
        ieee = _fit_ieee(t, y)
        n = len(y)
        bic_det = adv.bic(3, n, det["rss"])
        bic_ieee = adv.bic(3, n, ieee["rss"])
        delta = bic_det - bic_ieee
        rows.append({
            "svn": svn, "n": n,
            "verdict": "kappa" if bic_det < bic_ieee else "ieee",
            "strength": _strength(delta),
            "delta_bic": delta,
            "tau_best_days": det["tau"],
            "rss_kappa": det["rss"],
            "rss_ieee": ieee["rss"],
        })

    print("\n=== FULL-YEAR 2023 RESULTS ===")
    n_kappa = sum(1 for r in rows if r.get("verdict") == "kappa")
    n_valid = sum(1 for r in rows if "error" not in r)
    print(f"kappa wins {n_kappa}/{n_valid} satellites\n")
    for r in rows:
        if "error" in r:
            print(f"{r['svn']:4s}  {r['error']}")
        else:
            print(f"{r['svn']:4s} n={r['n']:3d}  {r['verdict']:5s}  "
                  f"{r['strength']:11s}  dBC={r['delta_bic']:+8.1f}  "
                  f"tau={r['tau_best_days']}d  rssK={r['rss_kappa']:.3e}  "
                  f"rssI={r['rss_ieee']:.3e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
