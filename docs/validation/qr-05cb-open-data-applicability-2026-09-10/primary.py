"""Primary route for the QR-05CB open-data applicability run.

Parses the acquired Bell-test dataset, applies the declared mappings to the
nested four-symbol population model, and measures the exact sup-norm gap
from each mapped population to the declared ideal family. Exact rational
arithmetic; no floats, no randomness, no network.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "VBI_Coincidence_20230707.dat"
SCHEMA = "qr05cb-report-v1"


def frac(pair):
    return F(int(pair[0]), int(pair[1]))


def parse(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        parts = line.split()
        if parts:
            rows.append([F(token) for token in parts])
    return rows


def cell(row, columns, name):
    return row[columns[name] - 1]


def q_point(eta, delta):
    def mass(z):
        return z + (eta + delta) * z * z / 4 + eta * delta * z ** 3 / 9

    norm = mass(F(1))
    return (mass(F(1, 4)) / norm, mass(F(3, 8)) / norm)


def sup_distance(left, right):
    return max(abs(left[0] - right[0]), abs(left[1] - right[1]))


def build_report(protocol):
    columns = protocol["columns"]
    rows = parse(DATA)
    beta_step = protocol["dataset"]["beta_step"]
    deltas = [frac(pair) for pair in protocol["family"]["delta"]]
    family = [(eta, delta, q_point(eta, delta)) for eta in protocol["family"]["eta"] for delta in deltas]
    e = frac(protocol["allowance"]["e_cal"])

    mappings = []
    for mapping in protocol["mappings"]:
        records = []
        for index, row in enumerate(rows):
            r1 = cell(row, columns, mapping["r1"][0]) / cell(row, columns, mapping["r1"][1])
            r2 = cell(row, columns, mapping["r2"][0]) / cell(row, columns, mapping["r2"][1])
            distances = [sup_distance((r1, r2), point) for _, _, point in family]
            records.append({"valid": 0 <= r1 <= r2 <= 1, "r1": r1, "r2": r2, "d": min(distances)})
        distances = sorted(record["d"] for record in records)
        mappings.append({
            "id": mapping["id"],
            "valid_all": all(record["valid"] for record in records),
            "r1_min": min(record["r1"] for record in records),
            "r1_max": max(record["r1"] for record in records),
            "r2_min": min(record["r2"] for record in records),
            "r2_max": max(record["r2"] for record in records),
            "dist_min": distances[0],
            "dist_median": distances[len(distances) // 2],
            "dist_max": distances[-1],
            "admitted_at_e": sum(1 for value in distances if value <= e),
        })

    return {
        "schema": SCHEMA,
        "dataset": protocol["dataset"],
        "grid": {"rows": len(rows), "cols": protocol["dataset"]["cols"],
                 "beta_step": beta_step, "alpha_steps": len(rows) // beta_step},
        "allowance": {"e_cal": e},
        "family_q2_min": min(point[1] for _, _, point in family),
        "family_q2_max": max(point[1] for _, _, point in family),
        "mappings": mappings,
    }
