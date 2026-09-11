"""Independent reference route for QR-05CY.

Same observational-quotient computation by different mechanics: signatures are
canonicalized by rounding and grouped by exact key (rather than the primary's
pairwise tolerant union-find), and the world constructions, the sign/count
observables, the classification scan and the reference family are recoded. The
two routes must agree before the gate is published.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
CLAIMS_PATH = HERE / "../../../det8/claims.py"
SCHEMA = "qr05cy-report-v1"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)
    return module


def _round(value, places=9):
    return round(value, places)


def _prec(points):
    n = len(points)
    out = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dt = points[j][0] - points[i][0]
                spatial = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, len(points[i])))
                if dt > 0 and spatial < dt * dt:
                    out[i][j] = True
    return out


def _chains(prec, order):
    n = len(prec)
    matrix = [[0] * n for _ in range(n)]
    for src in order:
        dist = [-1] * n
        dist[src] = 0
        for j in order:
            for i in order:
                if prec[i][j] and dist[i] >= 0 and dist[i] + 1 > dist[j]:
                    dist[j] = dist[i] + 1
        matrix[src] = [v if v > 0 else 0 for v in dist]
    return matrix


def _norm(matrix):
    vals = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix)) if matrix[i][j] > 0]
    if not vals:
        return [[0.0] * len(matrix) for _ in matrix]
    m = sum(vals) / len(vals)
    return [[matrix[i][j] / m for j in range(len(matrix))] for i in range(len(matrix))]


def _canon(sig, places=9):
    if isinstance(sig, (tuple, list)):
        return tuple(_canon(item, places) for item in sig)
    if isinstance(sig, float):
        return _round(sig, places)
    return sig


def _flat(matrix):
    return tuple(sorted(_round(matrix[i][j])
                        for i in range(len(matrix)) for j in range(len(matrix))))


def _signs(points):
    out = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dt = points[j][0] - points[i][0]
            spatial = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, len(points[i])))
            d = dt * dt - spatial
            out.append(-1 if d < 0 else (1 if d > 0 else 0))
    return tuple(out)


def _profile(points, bins):
    counts = [0] * bins
    for p in points:
        counts[min(int(p[1] * bins), bins - 1)] += 1
    mean = sum(counts) / bins
    return tuple(_round(c / mean) for c in counts)


def build_worlds(module, protocol):
    seed = protocol["seed"]
    families = {}

    families["dimension"] = [
        {"label": f"dim{d}",
         "obs": {"order": (_round(module.ordering_fraction(module.sprinkle_diamond(d, protocol["n_dim"], seed=seed))),)},
         "targets": {"dimension": d}}
        for d in protocol["dims"]
    ]

    base = module.sprinkle_diamond(2, protocol["n_base"], seed=seed)
    order = sorted(range(len(base)), key=lambda i: base[i][0])
    raw = _chains(_prec(base), order)
    families["scale"] = []
    for c in protocol["scale_factors"]:
        sig = _flat(_norm([[v * c for v in row] for row in raw]))
        families["scale"].append({"label": f"scale{c}",
                                  "obs": {"scaled_distance": sig,
                                          "scaled_distance+anchor": (sig, _round(float(c)))},
                                  "targets": {"absolute_scale": c}})

    fixed, _w = module.conformal_sprinkle_1d(protocol["n_base"], 0.0, seed=seed)
    signs = _signs(fixed)
    families["conformal_signs"] = [
        {"label": f"omega{b}", "obs": {"order_signs": signs}, "targets": {"conformal_factor": b}}
        for b in protocol["conformal_b"]
    ]

    families["conformal_counts"] = []
    for b in protocol["conformal_b"]:
        pts, _weight = module.conformal_sprinkle_1d(protocol["n_base"], b, seed=seed)
        families["conformal_counts"].append(
            {"label": f"omega{b}", "obs": {"counts": _profile(pts, protocol["n_bins"])},
             "targets": {"conformal_factor": b}})
    return families


def _groups(worlds, interface):
    buckets = {}
    for index, world in enumerate(worlds):
        buckets.setdefault(_canon(world["obs"][interface]), []).append(index)
    return [sorted(members) for members in buckets.values()]


def classify(worlds, interface, target):
    result = "IDENTIFIED"
    witness = None
    for members in _groups(worlds, interface):
        base_value = worlds[members[0]]["targets"][target]
        for index in members[1:]:
            if not _same(worlds[index]["targets"][target], base_value):
                result = "NON_IDENTIFIABLE"
                pair = sorted([worlds[members[0]]["label"], worlds[index]["label"]])
                if witness is None or pair < witness:
                    witness = pair
    return result, witness


def _same(a, b, rtol=1e-9):
    return abs(a - b) <= rtol * max(1.0, abs(a), abs(b))


def classify_probe(families, probe):
    verdict, witness = classify(families[probe["family"]], probe["interface"], probe["target"])
    return {"family": probe["family"], "interface": probe["interface"], "target": probe["target"],
            "n_worlds": len(families[probe["family"]]), "verdict": verdict, "witness": witness}


REFERENCE_FAMILY = {
    "max": lambda v: max(v),
    "mean": lambda v: sum(v) / len(v),
    "median": lambda v: sorted(v)[len(v) // 2],
    "min": lambda v: min(v),
    "positive_fraction": lambda v: sum(1 for x in v if x > 0) / len(v),
    "rms": lambda v: math.sqrt(sum(x * x for x in v) / len(v)),
}


def internal_reference_no_go(families, probe):
    worlds = families[probe["family"]]
    verdict, witness = classify(worlds, probe["interface"], probe["target"])
    first = next(w for w in worlds if w["label"] == witness[0])
    second = next(w for w in worlds if w["label"] == witness[1])
    sig = first["obs"][probe["interface"]]
    sig2 = second["obs"][probe["interface"]]
    values = {name: _round(f(sig)) for name, f in sorted(REFERENCE_FAMILY.items())}
    values2 = {name: _round(f(sig2)) for name, f in sorted(REFERENCE_FAMILY.items())}
    return {"family": probe["family"], "interface": probe["interface"], "target": probe["target"],
            "witness": list(witness), "reference_family": sorted(REFERENCE_FAMILY),
            "targets_differ": not _same(first["targets"][probe["target"]], second["targets"][probe["target"]]),
            "all_blind": bool(values == values2 and _canon(sig) == _canon(sig2)),
            "blind_values": values}


def taxonomy_check(protocol, claims_module):
    evidence = {
        claims_module.VERIFIED_SOFTWARE_CONTRACT,
        claims_module.NOT_YET_VALIDATED,
        claims_module.BOUNDED_CONDITIONAL_RESULT,
        claims_module.CORRESPONDENCE_ONLY,
        claims_module.NO_EMPIRICAL_SUPPORT,
        claims_module.NOT_APPLICABLE,
    }
    blocking = {"DATA", "CHANNEL", "MATH", "GAUGE"}
    checked = {}
    for target in sorted(protocol["taxonomy"]):
        entry = protocol["taxonomy"][target]
        assert entry["evidence_status"] in evidence, entry["evidence_status"]
        assert entry["blockage"] in blocking, entry["blockage"]
        checked[target] = {"evidence_status": entry["evidence_status"], "blockage": entry["blockage"]}
    return {"mapping": checked, "validated_against": "det8.claims",
            "new_status_introduced": False, "blockage_kinds": sorted(blocking)}


def build_report(protocol):
    module = load_module("_qr05cy_t7_ref", MODULE_PATH)
    claims_module = load_module("_qr05cy_claims_ref", CLAIMS_PATH)
    families = build_worlds(module, protocol)
    probes = [classify_probe(families, probe) for probe in protocol["probes"]]
    no_go_probe = next(p for p in protocol["probes"] if p["interface"] == "scaled_distance")
    no_go = internal_reference_no_go(families, no_go_probe)
    anchor_verdict = next(p["verdict"] for p in probes if p["interface"] == "scaled_distance+anchor")
    non_identified = sorted({p["target"] for p in probes if p["verdict"] == "NON_IDENTIFIABLE"})
    identified = sorted({p["target"] for p in probes if p["verdict"] == "IDENTIFIED"})

    return {
        "schema": SCHEMA,
        "probes": probes,
        "identified_targets": identified,
        "non_identifiable_targets": non_identified,
        "internal_reference_no_go": no_go,
        "external_anchor_resolves": bool(anchor_verdict == "IDENTIFIED"),
        "taxonomy": taxonomy_check(protocol, claims_module),
        "propositions": [
            {"id": "P1", "statement": "tau is identifiable through O iff tau is constant on every O-class "
                                      "(tau factors through W/~_O).", "status": "proved_elementary"},
            {"id": "P2", "statement": "If W1 ~_O W2 and tau(W1) != tau(W2), no sigma(O)-measurable function "
                                      "-- in particular no reference r_ref = f(O) built from the same channel "
                                      "-- can identify tau on {W1,W2}.", "status": "proved_elementary"},
            {"id": "P3", "statement": "Absolute scale does not factor through any internally generated "
                                      "observable; it requires an independent external anchor.",
             "status": "verified_finite_instance"},
            {"id": "P4", "statement": "The causal order is exactly blind to the conformal factor; the count "
                                      "density identifies it.", "status": "verified_finite_instance"},
            {"id": "P5", "statement": "Observational equivalence is not ontological identity (Status M).",
             "status": "governance_status_m"},
        ],
        "ontological_claim": False,
        "status_m_guard": "observational equivalence is not ontological identity "
                          "(Status M; GOVERNANCE §3 F8-OPEN v2; ONTOLOGY.md §5)",
        "verdict": "identifiability is separable from empirical applicability: dimension is identified, the "
                   "conformal factor is identified once counts (marks) are in the channel, and absolute scale "
                   "and reference validity are NOT identifiable from the same record channel -- so an "
                   "independent anchor is logically necessary (P2/P3). This closes the non-empirical half of "
                   "the BW/P5 blockage negatively and leaves the apparatus branch open; it makes no "
                   "ontological claim.",
    }
