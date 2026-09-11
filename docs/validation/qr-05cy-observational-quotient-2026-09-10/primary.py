"""Primary route for QR-05CY: observational quotient and internal-reference no-go.

Let W be a finite class of admissible DET-style worlds and O a declared
observational interface on the DET primitives (V, ≺, #, L, 𝔇). Worlds are
observationally equivalent, W1 ~_O W2, when O cannot tell them apart. A target
tau is identifiable through O iff W1 ~_O W2 => tau(W1) = tau(W2) (the
factorization criterion), i.e. tau is constant on every O-class.

This gate (a) computes the O-classes exactly on a small declared world class,
(b) classifies each target as IDENTIFIED or NON_IDENTIFIABLE with a witness
pair, (c) demonstrates the internal-reference no-go on BW's reference channel
(every reference built from O is blind on a witness class), and (d) checks that
its blockage taxonomy maps onto the existing det8.claims axes without adding a
new vocabulary. It makes NO ontological claim: observational equivalence is not
ontological identity (GOVERNANCE §3 F8-OPEN v2; ONTOLOGY.md §5).
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


def causality(points):
    n = len(points)
    prec = [[False] * n for _ in range(n)]
    for i in range(n):
        pi = points[i]
        for j in range(n):
            if i == j:
                continue
            dt = points[j][0] - pi[0]
            spatial = sum((points[j][k] - pi[k]) ** 2 for k in range(1, len(pi)))
            if dt > 0 and spatial < dt * dt:
                prec[i][j] = True
    return prec


def chain_matrix(prec, order):
    n = len(prec)
    chain = [[0] * n for _ in range(n)]
    for src in order:
        dist = [-1] * n
        dist[src] = 0
        for j in order:
            best = -1
            for i in range(n):
                if prec[i][j] and dist[i] >= 0 and dist[i] + 1 > best:
                    best = dist[i] + 1
            if best > dist[j]:
                dist[j] = best
        chain[src] = [value if value > 0 else 0 for value in dist]
    return chain


def normalize(matrix):
    positive = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix)) if matrix[i][j] > 0]
    if not positive:
        return [[0.0] * len(matrix) for _ in matrix]
    mean = sum(positive) / len(positive)
    return [[matrix[i][j] / mean for j in range(len(matrix))] for i in range(len(matrix))]


def _matrix_signature(matrix, places=9):
    return tuple(sorted(_round(matrix[i][j], places)
                        for i in range(len(matrix)) for j in range(len(matrix))))


def _sign_pattern(points):
    """Signs of the pairwise intervals; invariant under any conformal factor."""
    out = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dt = points[j][0] - points[i][0]
            spatial = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, len(points[i])))
            d = dt * dt - spatial
            out.append((d > 0) - (d < 0))
    return tuple(out)


def _count_profile(points, n_bins):
    bins = [0] * n_bins
    for p in points:
        idx = min(int(p[1] * n_bins), n_bins - 1)
        bins[idx] += 1
    mean_count = sum(bins) / n_bins
    return tuple(_round(c / mean_count, 9) for c in bins)


def equivalent(left, right, rtol=1e-9):
    if isinstance(left, (bool,)) or isinstance(right, (bool,)):
        return left is right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return abs(left - right) <= rtol * max(1.0, abs(left), abs(right))
    if isinstance(left, (tuple, list)) and isinstance(right, (tuple, list)):
        return len(left) == len(right) and all(equivalent(a, b, rtol) for a, b in zip(left, right))
    return left == right


def build_worlds(module, protocol):
    """The declared finite world class, grouped into families."""
    seed = protocol["seed"]
    families = {}

    dim_worlds = []
    for d in protocol["dims"]:
        points = module.sprinkle_diamond(d, protocol["n_dim"], seed=seed)
        dim_worlds.append({
            "label": f"dim{d}",
            "obs": {"order": (_round(module.ordering_fraction(points)),)},
            "targets": {"dimension": d},
        })
    families["dimension"] = dim_worlds

    base = module.sprinkle_diamond(2, protocol["n_base"], seed=seed)
    prec = causality(base)
    order = sorted(range(len(base)), key=lambda i: base[i][0])
    raw = chain_matrix(prec, order)
    scale_worlds = []
    for c in protocol["scale_factors"]:
        scaled = [[value * c for value in row] for row in raw]
        signature = _matrix_signature(normalize(scaled))
        scale_worlds.append({
            "label": f"scale{c}",
            "obs": {"scaled_distance": signature,
                    "scaled_distance+anchor": (signature, _round(float(c)))},
            "targets": {"absolute_scale": c},
        })
    families["scale"] = scale_worlds

    fixed_points, _ = module.conformal_sprinkle_1d(protocol["n_base"], 0.0, seed=seed)
    signs = _sign_pattern(fixed_points)
    conformal_sign_worlds = []
    for b in protocol["conformal_b"]:
        conformal_sign_worlds.append({
            "label": f"omega{b}",
            "obs": {"order_signs": signs},
            "targets": {"conformal_factor": b},
        })
    families["conformal_signs"] = conformal_sign_worlds

    conformal_count_worlds = []
    for b in protocol["conformal_b"]:
        points, _weight = module.conformal_sprinkle_1d(protocol["n_base"], b, seed=seed)
        conformal_count_worlds.append({
            "label": f"omega{b}",
            "obs": {"counts": _count_profile(points, protocol["n_bins"])},
            "targets": {"conformal_factor": b},
        })
    families["conformal_counts"] = conformal_count_worlds

    return families


def _partition(worlds, interface):
    n = len(worlds)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(n):
        for j in range(i + 1, n):
            if equivalent(worlds[i]["obs"][interface], worlds[j]["obs"][interface]):
                parent[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return [sorted(members) for members in groups.values()]


def classify(worlds, interface, target):
    """IDENTIFIED iff every pair with equal observation has equal target."""
    result = "IDENTIFIED"
    witness = None
    for members in _partition(worlds, interface):
        differing = [i for i in members
                     if not equivalent(worlds[i]["targets"][target], worlds[members[0]]["targets"][target])]
        if differing:
            result = "NON_IDENTIFIABLE"
            pair = sorted([worlds[members[0]]["label"], worlds[differing[0]]["label"]])
            if witness is None or pair < witness:
                witness = pair
    return result, witness


def classify_probe(families, probe):
    worlds = families[probe["family"]]
    verdict, witness = classify(worlds, probe["interface"], probe["target"])
    return {"family": probe["family"], "interface": probe["interface"], "target": probe["target"],
            "n_worlds": len(worlds), "verdict": verdict, "witness": witness}


REFERENCE_FAMILY = {
    "mean": lambda values: sum(values) / len(values),
    "max": max,
    "min": min,
    "median": lambda values: sorted(values)[len(values) // 2],
    "rms": lambda values: math.sqrt(sum(v * v for v in values) / len(values)),
    "positive_fraction": lambda values: sum(1 for v in values if v > 0) / len(values),
}


def internal_reference_no_go(families, probe):
    """Every reference r_ref = f(O) built from the same channel is blind on the
    witness class: if O agrees then so does f(O) for every f."""
    worlds = families[probe["family"]]
    verdict, witness = classify(worlds, probe["interface"], probe["target"])
    member = [w for w in worlds if w["label"] in witness[0]][0]
    other = [w for w in worlds if w["label"] == witness[1]][0]
    signature = member["obs"][probe["interface"]]
    other_signature = other["obs"][probe["interface"]]
    values = {name: _round(f(signature)) for name, f in sorted(REFERENCE_FAMILY.items())}
    other_values = {name: _round(f(other_signature)) for name, f in sorted(REFERENCE_FAMILY.items())}
    all_blind = values == other_values and equivalent(signature, other_signature)
    return {"family": probe["family"], "interface": probe["interface"], "target": probe["target"],
            "witness": list(witness), "reference_family": sorted(REFERENCE_FAMILY),
            "targets_differ": not equivalent(member["targets"][probe["target"]],
                                             other["targets"][probe["target"]]),
            "all_blind": bool(all_blind),
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
    for target, entry in sorted(protocol["taxonomy"].items()):
        if entry["evidence_status"] not in evidence:
            raise AssertionError(f"unregistered evidence status {entry['evidence_status']!r}")
        if entry["blockage"] not in blocking:
            raise AssertionError(f"unknown blockage kind {entry['blockage']!r}")
        checked[target] = dict(entry)
    return {"mapping": checked, "validated_against": "det8.claims",
            "new_status_introduced": False, "blockage_kinds": sorted(blocking)}


def build_report(protocol):
    module = load_module("_qr05cy_t7", MODULE_PATH)
    claims_module = load_module("_qr05cy_claims", CLAIMS_PATH)
    families = build_worlds(module, protocol)
    probes = [classify_probe(families, probe) for probe in protocol["probes"]]

    no_go_probe = next(p for p in protocol["probes"] if p["interface"] == "scaled_distance")
    no_go = internal_reference_no_go(families, no_go_probe)

    anchor_probe = next(p for p in protocol["probes"] if p["interface"] == "scaled_distance+anchor")
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
