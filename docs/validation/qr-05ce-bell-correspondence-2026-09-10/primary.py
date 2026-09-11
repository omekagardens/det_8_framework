"""Primary route for the QR-05CE Bell-correspondence / history-distance run.

Reproduces the deposit's correlation curves E(alpha,beta) from the four-fold
coincidence counts, tests the CHSH visibility witness exactly, and evaluates
the Fisher-Rao history distance kappa between setting-conditioned kernels
(record_kernel_physics.md 2.2). Exact rationals for E and the witness; kappa
is transcendental and is reported to a declared number of decimals.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from math import acos, pi, sqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "../qr-05cb-open-data-applicability-2026-09-10/data/VBI_Coincidence_20230707.dat"
SCHEMA = "qr05ce-report-v1"


def frac(pair):
    return F(int(pair[0]), int(pair[1]))


def parse(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        parts = line.split()
        if parts:
            rows.append([F(token) for token in parts])
    return rows


def build_report(protocol):
    cc4_col = protocol["columns"]["cc4"] - 1
    rows = parse(DATA)
    cc4 = [row[cc4_col] for row in rows]
    beta_step = protocol["grid"]["beta_step"]
    alpha_steps = len(cc4) // beta_step
    grid = [cc4[a * beta_step:(a + 1) * beta_step] for a in range(alpha_steps)]
    counts = [grid[4 + i] for i in range(4)]
    decimals = protocol["kappa_decimals"]

    curves = []
    for curve in protocol["curves"]:
        left = counts[curve["row_a"]]
        right = counts[curve["row_b"]]
        values = []
        for i in range(beta_step - 4):
            num = left[i] + right[i + 4] - left[i + 4] - right[i]
            den = left[i] + right[i + 4] + left[i + 4] + right[i]
            values.append(num / den)
        low = min(values)
        high = max(values)
        amplitude = (high - low) / 2
        amplitude_sq = amplitude * amplitude
        witness = amplitude_sq > F(1, 2)
        over = sum(1 for value in values if value * value > F(1, 2))
        bh = (sqrt(float((1 + high) * (1 + low))) + sqrt(float((1 - high) * (1 - low)))) / 2
        kappa = (2 / pi) * acos(max(-1.0, min(1.0, bh)))
        curves.append({
            "id": curve["id"],
            "E_min": low,
            "E_max": high,
            "amplitude": amplitude,
            "amplitude_sq": amplitude_sq,
            "chsh_witness": witness,
            "over_threshold_count": over,
            "kappa": round(kappa, decimals),
        })

    digest = hashlib.sha256(DATA.read_bytes()).hexdigest()
    return {
        "schema": SCHEMA,
        "dataset_sha256": digest,
        "grid": {"beta_step": beta_step, "alpha_steps": alpha_steps},
        "curves": curves,
    }
