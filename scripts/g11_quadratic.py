#!/usr/bin/env python3
"""All 12 satellites: which model (κ / IEEE / quadratic) actually wins?"""

from __future__ import annotations

import glob
import gzip
import os
import sys
from collections import defaultdict

ROOT = "/Volumes/AI_DATA/development/det_8_qwen"
sys.path.insert(0, ROOT)

from det8.applied_physics.applied_tests import _fit_exp_decay, _fit_ieee  # noqa: E402
from det8.applied_physics import adversarial as adv  # noqa: E402
from det8.applied_physics.ingest import daily_drift, parse_igs_clock  # noqa: E402

CLK_DIR = f"{ROOT}/det8/data/igs"
SVNS = ["G01", "G02", "G03", "G05", "G08", "G11",
        "G13", "G16", "G18", "G22", "G24", "G30"]


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
    return {"rss": sum((yi - p) ** 2 for yi, p in zip(y, pred)),
            "params": {"a": a, "b": bb, "c": c}}


def main() -> int:
    daily = {s: [] for s in SVNS}
    files = sorted(glob.glob(os.path.join(CLK_DIR, "*.CLK.gz")))
    for path in files:
        with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        by_svn = defaultdict(list)
        for r in parse_igs_clock(text):
            by_svn[r["svn"]].append(r)
        for svn in SVNS:
            d = daily_drift(by_svn.get(svn, []))
            if d["drift_s_per_s"] is not None:
                daily[svn].append(d["drift_s_per_s"])

    print(f"{'SVN':4s} {'n':>4s} {'kappa':>10s} {'ieee':>10s} {'quad':>10s}  "
          f"{'best':>9s}  {'dBC(quad-best2)':>16s}  quad_a")
    tally = defaultdict(int)
    for svn in SVNS:
        y = daily[svn]
        t = list(range(len(y)))
        n = len(y)
        det = _fit_exp_decay(t, y)
        ieee = _fit_ieee(t, y)
        quad = _fit_quadratic(t, y)
        bics = {"kappa": adv.bic(3, n, det["rss"]),
                "ieee": adv.bic(3, n, ieee["rss"]),
                "quad": adv.bic(3, n, quad["rss"])}
        best = min(bics, key=bics.get)
        second = sorted(bics.values())[1]
        tally[best] += 1
        print(f"{svn:4s} {n:4d} {bics['kappa']:10.1f} {bics['ieee']:10.1f} "
              f"{bics['quad']:10.1f}  {best:>9s}  {bics['quad'] - second:>+16.1f}  "
              f"{quad['params']['a']:+.3e}")
    print(f"\nbest-model tally: {dict(tally)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
