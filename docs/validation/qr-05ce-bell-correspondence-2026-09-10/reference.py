"""Independent reference route for the QR-05CE Bell-correspondence run.

A different grid construction (column slicing) and different enumeration of
the correlation values, with the declared Fisher-Rao expression.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction as F
from math import acos, pi, sqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "../qr-05cb-open-data-applicability-2026-09-10/data/VBI_Coincidence_20230707.dat"
SCHEMA = "qr05ce-report-v1"


def parse(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        parts = line.split()
        if parts:
            rows.append([F(token) for token in parts])
    return rows


def build_report(protocol):
    cc4_col = protocol["columns"]["cc4"] - 1
    values = [row[cc4_col] for row in parse(DATA)]
    beta_step = protocol["grid"]["beta_step"]
    alpha_steps = len(values) // beta_step
    # column slicing: grid[alpha][beta] = values[alpha*beta_step + beta]
    columns = [[values[a * beta_step + b] for b in range(beta_step)] for a in range(alpha_steps)]
    counts = [columns[4 + row] for row in range(4)]
    decimals = protocol["kappa_decimals"]

    curves = []
    for curve in protocol["curves"]:
        left = counts[curve["row_a"]]
        right = counts[curve["row_b"]]
        es = []
        for i in range(beta_step - 4):
            total = left[i] + right[i + 4] + left[i + 4] + right[i]
            diff = left[i] + right[i + 4] - left[i + 4] - right[i]
            es.append(diff / total)
        low, high = min(es), max(es)
        amplitude = (high - low) / 2
        hp, hm = F(1) + high, F(1) - high
        lp, lm = F(1) + low, F(1) - low
        bhattacharyya = (sqrt(float(hp * lp)) + sqrt(float(hm * lm))) / 2
        kappa = (2 / pi) * acos(max(-1.0, min(1.0, bhattacharyya)))
        curves.append({
            "id": curve["id"],
            "E_min": low,
            "E_max": high,
            "amplitude": amplitude,
            "amplitude_sq": amplitude * amplitude,
            "chsh_witness": amplitude * amplitude > F(1, 2),
            "over_threshold_count": len([value for value in es if value * value > F(1, 2)]),
            "kappa": round(kappa, decimals),
        })

    digest = hashlib.sha256(DATA.read_bytes()).hexdigest()
    return {
        "schema": SCHEMA,
        "dataset_sha256": digest,
        "grid": {"beta_step": beta_step, "alpha_steps": alpha_steps},
        "curves": curves,
    }
