"""Independent reference route for the QR-05CB open-data applicability run.

A different parse (list-of-lists via a manual scanner) and the BU
segment-parameter ideal-point formulas, with aggregation written as
explicit loops. Must reproduce the primary report exactly.
"""

from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "VBI_Coincidence_20230707.dat"
SCHEMA = "qr05cb-report-v1"


def frac(pair):
    return F(int(pair[0]), int(pair[1]))


def parse(path):
    text = Path(path).read_text()
    rows = []
    for line in text.splitlines():
        tokens = line.split()
        if tokens:
            rows.append([F(token) for token in tokens])
    return rows


def q_point(eta, delta):
    if eta == 0:
        t = delta / (4 + delta)
        return ((1 - t) * F(1, 4) + t * F(1, 16), (1 - t) * F(3, 8) + t * F(9, 64))
    t = 13 * delta / (45 + 13 * delta)

    def component(z):
        return (1 - t) * (4 * z + z * z) / 5 + t * (9 * z * z + 4 * z * z * z) / 13

    return (component(F(1, 4)), component(F(3, 8)))


def build_report(protocol):
    columns = protocol["columns"]
    rows = parse(DATA)
    family = [
        (eta, delta, q_point(eta, delta))
        for eta in protocol["family"]["eta"]
        for delta in [frac(pair) for pair in protocol["family"]["delta"]]
    ]
    e = frac(protocol["allowance"]["e_cal"])

    mappings = []
    for mapping in protocol["mappings"]:
        r1_values, r2_values, gaps, valid = [], [], [], True
        for row in rows:
            r1 = row[columns[mapping["r1"][0]] - 1] / row[columns[mapping["r1"][1]] - 1]
            r2 = row[columns[mapping["r2"][0]] - 1] / row[columns[mapping["r2"][1]] - 1]
            if not (0 <= r1 <= r2 <= 1):
                valid = False
            best = None
            for _, _, point in family:
                dx = r1 - point[0]
                dy = r2 - point[1]
                if dx < 0:
                    dx = -dx
                if dy < 0:
                    dy = -dy
                distance = dx if dx > dy else dy
                if best is None or distance < best:
                    best = distance
            r1_values.append(r1)
            r2_values.append(r2)
            gaps.append(best)
        ordered = sorted(gaps)
        mappings.append({
            "id": mapping["id"],
            "valid_all": valid,
            "r1_min": min(r1_values),
            "r1_max": max(r1_values),
            "r2_min": min(r2_values),
            "r2_max": max(r2_values),
            "dist_min": ordered[0],
            "dist_median": ordered[len(ordered) // 2],
            "dist_max": ordered[-1],
            "admitted_at_e": len([value for value in gaps if value <= e]),
        })

    q2s = [point[1] for _, _, point in family]
    return {
        "schema": SCHEMA,
        "dataset": protocol["dataset"],
        "grid": {"rows": len(rows), "cols": protocol["dataset"]["cols"],
                 "beta_step": protocol["dataset"]["beta_step"],
                 "alpha_steps": len(rows) // protocol["dataset"]["beta_step"]},
        "allowance": {"e_cal": e},
        "family_q2_min": min(q2s),
        "family_q2_max": max(q2s),
        "mappings": mappings,
    }
