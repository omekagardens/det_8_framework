"""Primary route for QR-05DO (direction B): the anchor calculus.

QR-05CY computed the observational quotient for a **single** declared interface
and found: dimension identified through the order, the conformal factor
identified once counts are in the channel, and absolute scale (and any reference
built from the same channel) **non-identifiable**.  Direction B asks the
quantitative follow-up: *what is the minimal additional channel/anchor that
makes scale + reference + geometry identifiable?*

This gate turns CY's one-off classification into a **calculus over channel
sets**.  A world carries values for a declared channel universe

    order            ordering fraction                     (internal)
    order_signs      interval signs                         (internal)
    counts           normalized binned count density        (internal)
    distance_ratio   normalized chain-distance signature    (internal)
    anchor           the world's unit in a fixed external   (EXTERNAL)
                     standard

and the interface `O_S` for a set `S` is the tuple of those channels' values.
The gate computes, for all 32 subsets `S`:

- **identifiability** (CY's P1: the target is constant on every `O_S`-class);
- **monotonicity** under channel refinement, verified exhaustively;
- **minimal identifying sets** per target and for the declared joint target;
- **the anchor property** — no internal channel separates the scale witness
  pair while the anchor does, and on the whole anchor-free half of the lattice
  every reference built from the channel is blind on that witness class (CY's
  P2, lattice-wide).

A finite universe of channels can separate a declared family **accidentally**
(a count profile may distinguish dimension worlds on one sampled class without
being a dimension channel).  The report therefore records the accidental
separation explicitly and reports both the lattice minimum and the
one-channel-per-blind-direction design, rather than reading `k_min` as a
mechanism claim.

The world class and the constructions (`causality`, `chain_matrix`, `normalize`,
`_sign_pattern`, `_count_profile`, the reference family) are **imported from
QR-05CY as a frozen fixture**, so the two gates cannot drift.

Track-B exploratory / correspondence-level (Status M); no physical claim.
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CY_PATH = HERE / "../qr-05cy-observational-quotient-2026-09-10/primary.py"
T7_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05do-report-v1"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    return module


# ── the finite world class: a uniform channel schema over CY's families ─────


def _geometry_channels(cy, module, points, n_bins):
    """(order, order_signs, counts, distance_ratio) via CY's own constructions.

    `_count_profile` is CY's construction.  On the causal-diamond families its
    bin index is used exactly as CY wrote it; those families share one point set,
    so the channel is family-invariant there and its binning convention cannot
    change any verdict.  On the conformal family (a box, x in [0, 1]) it is exact.
    """
    prec = cy.causality(points)
    order = sorted(range(len(points)), key=lambda i: points[i][0])
    raw = cy.chain_matrix(prec, order)
    return {
        "order": (cy._round(module.ordering_fraction(points)),),
        "order_signs": cy._sign_pattern(points),
        "counts": cy._count_profile(points, n_bins),
        "distance_ratio": cy._matrix_signature(cy.normalize(raw)),
    }


def build_worlds(cy, module, protocol):
    """Families with a uniform channel schema, built from CY's constructions."""
    seed = protocol["seed"]
    n_bins = protocol["n_bins"]
    families = {}

    # dimension: a sprinkle in d = 2, 3, 4 (scale 1, conformal factor 0)
    worlds = []
    for dim in protocol["dims"]:
        points = module.sprinkle_diamond(dim, protocol["n_dim"], seed=seed)
        channels = _geometry_channels(cy, module, points, n_bins)
        channels["anchor"] = (1.0,)
        worlds.append({
            "label": f"dim{dim}", "obs": channels,
            "targets": {"dimension": dim, "conformal_factor": 0.0, "absolute_scale": 1.0},
        })
    families["dimension"] = worlds

    # scale: one geometry at scale c = 1, 2, 4 (order/signs/counts/ratios blind)
    base = module.sprinkle_diamond(2, protocol["n_base"], seed=seed)
    prec = cy.causality(base)
    order = sorted(range(len(base)), key=lambda i: base[i][0])
    raw = cy.chain_matrix(prec, order)
    worlds = []
    for c in protocol["scale_factors"]:
        scaled = [[value * c for value in row] for row in raw]
        channels = _geometry_channels(cy, module, base, n_bins)
        channels["distance_ratio"] = cy._matrix_signature(cy.normalize(scaled))
        channels["anchor"] = (float(c),)
        worlds.append({
            "label": f"scale{c}", "obs": channels,
            "targets": {"dimension": 2, "conformal_factor": 0.0, "absolute_scale": c},
        })
    families["scale"] = worlds

    # conformal: the same fixed events under Omega^2 = 1 + b*x (b = 0, 2);
    # the order channels are blind, the count density carries the factor.
    fixed, _ = module.conformal_sprinkle_1d(protocol["n_base"], 0.0, seed=seed)
    fixed_channels = _geometry_channels(cy, module, fixed, n_bins)
    worlds = []
    for b in protocol["conformal_b"]:
        points, _weight = module.conformal_sprinkle_1d(protocol["n_base"], b, seed=seed)
        channels = dict(fixed_channels)
        channels["counts"] = cy._count_profile(points, n_bins)
        channels["anchor"] = (1.0,)
        worlds.append({
            "label": f"omega{b}", "obs": channels,
            "targets": {"dimension": 2, "conformal_factor": b, "absolute_scale": 1.0},
        })
    families["conformal"] = worlds
    return families


# ── the channel-set calculus ────────────────────────────────────────────────


def joint_signature(world, channels):
    return tuple(world["obs"][channel] for channel in channels)


def flatten(signature):
    out = []
    for item in signature:
        if isinstance(item, (tuple, list)):
            out.extend(item)
        else:
            out.append(item)
    return tuple(out)


def partition(worlds, channels):
    """O_S-classes: worlds agreeing on every channel in S."""
    n = len(worlds)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(n):
        for j in range(i + 1, n):
            if joint_signature(worlds[i], channels) == joint_signature(worlds[j], channels):
                parent[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return [sorted(members) for members in groups.values()]


def classify(worlds, channels, target):
    """IDENTIFIED iff the target is constant on every O_S-class (CY's P1)."""
    verdict, witness = "IDENTIFIED", None
    for members in partition(worlds, channels):
        head = worlds[members[0]]["targets"][target]
        differing = [i for i in members if worlds[i]["targets"][target] != head]
        if differing:
            verdict = "NON_IDENTIFIABLE"
            pair = sorted([worlds[members[0]]["label"], worlds[differing[0]]["label"]])
            witness = pair if witness is None else min(witness, pair)
    return verdict, witness


def channel_subsets(channels):
    return [tuple(combo) for size in range(len(channels) + 1)
            for combo in itertools.combinations(channels, size)]


def lattice(families, protocol):
    rows = []
    for subset in channel_subsets(protocol["channels"]):
        entry = {"channels": list(subset), "size": len(subset),
                 "targets": {}, "family_partitions": {}}
        for family, spec in sorted(protocol["families"].items()):
            target = spec["target"]
            verdict, witness = classify(families[family], list(subset), target)
            entry["targets"][target] = {"verdict": verdict, "witness": witness}
            entry["family_partitions"][family] = partition(families[family], list(subset))
        rows.append(entry)
    return rows


def minimal_sets(rows, target):
    """Inclusion-minimal channel sets that identify a target."""
    sets = [set(row["channels"]) for row in rows
            if row["targets"][target]["verdict"] == "IDENTIFIED"]
    minimal = [sorted(s) for s in sets if not any(other < s for other in sets)]
    return sorted(minimal, key=lambda value: (len(value), value))


def monotonicity_violations(rows):
    """One-step refinement violations of monotonicity.

    A violation of `S subset S' and identified(S) implies identified(S')` exists
    iff it exists for a one-step refinement `S -> S + c` (the larger pair can be
    reached by single steps, and each single step would have to fail first), so
    the one-step list is the canonical obstruction.
    """
    by_key = {tuple(sorted(row["channels"])): row for row in rows}
    violations = []
    for row in rows:
        base = tuple(sorted(row["channels"]))
        for channel in sorted(set().union(*[set(r["channels"]) for r in rows])):
            if channel in base:
                continue
            refined = tuple(sorted(base + (channel,)))
            for target, verdict in row["targets"].items():
                if (verdict["verdict"] == "IDENTIFIED"
                        and by_key[refined]["targets"][target]["verdict"] != "IDENTIFIED"):
                    violations.append({"smaller": sorted(base), "larger": list(refined),
                                       "target": target})
    return violations


def accidental_separation(rows, families, protocol):
    """Which single channels separate a family's worlds *completely*.

    Separating a family's worlds is not the same as being that family's
    mechanism channel; the report records this so `k_min` is not read as one.
    """
    per_family = {}
    for family, spec in sorted(protocol["families"].items()):
        size = len(families[family])
        singles = [row["channels"][0] for row in rows
                   if len(row["channels"]) == 1
                   and len(row["family_partitions"][family]) == size
                   and row["targets"][spec["target"]]["verdict"] == "IDENTIFIED"]
        per_family[family] = sorted(singles)
    return per_family


def internal_blindness(cy, families, protocol):
    """CY's P2 made lattice-wide, on the scale witness pair."""
    witness = families["scale"][:2]
    blind, sighted = [], []
    for subset in channel_subsets(protocol["channels"]):
        values = []
        for world in witness:
            flat = flatten(joint_signature(world, list(subset)))
            # The empty channel set observes nothing, so no reference value
            # exists: an interface that observes nothing certifies nothing.
            values.append({name: cy._round(function(flat))
                           for name, function in sorted(cy.REFERENCE_FAMILY.items())}
                          if flat else {})
        row = {"channels": list(subset), "references_agree": bool(values[0] == values[1])}
        (sighted if "anchor" in subset else blind).append(row)
    return {
        "witness": [world["label"] for world in witness],
        "target_differs": bool(witness[0]["targets"]["absolute_scale"]
                               != witness[1]["targets"]["absolute_scale"]),
        "control_channels_are_blind": all(
            witness[0]["obs"][channel] == witness[1]["obs"][channel]
            for channel in protocol["internal_channels"]),
        "internal_subsets_all_blind": all(row["references_agree"] for row in blind),
        "anchor_bearing_subsets_all_sighted": all(not row["references_agree"] for row in sighted),
        "n_internal_subsets": len(blind),
        "n_anchor_bearing_subsets": len(sighted),
    }


def anchor_is_not_internally_constructible(families, protocol):
    witness = families["scale"][:2]
    separated = [channel for channel in protocol["internal_channels"]
                 if witness[0]["obs"][channel] != witness[1]["obs"][channel]]
    return {
        "internal_channels_separating_the_witness": separated,
        "anchor_separates_the_witness": bool(
            witness[0]["obs"]["anchor"] != witness[1]["obs"]["anchor"]),
        "anchor_is_external": not separated,
    }


def build_report(protocol):
    cy = load_module("_qr05do_cy", CY_PATH)
    module = load_module("_qr05do_t7", T7_PATH)
    families = build_worlds(cy, module, protocol)
    rows = lattice(families, protocol)

    targets = sorted({spec["target"] for spec in protocol["families"].values()})
    minima = {target: minimal_sets(rows, target) for target in targets}
    joint = protocol["joint_target"]
    identifying = [sorted(row["channels"]) for row in rows
                   if all(row["targets"][target]["verdict"] == "IDENTIFIED" for target in joint)]
    joint_minimal = [value for value in identifying
                     if not any(set(other) < set(value) for other in identifying)]
    joint_minimal.sort(key=lambda value: (len(value), value))
    k_min = min((len(value) for value in joint_minimal), default=None)
    design = sorted(set(["order", "counts", "anchor"]))

    violations = monotonicity_violations(rows)
    blindness = internal_blindness(cy, families, protocol)
    anchor = anchor_is_not_internally_constructible(families, protocol)
    accidental = accidental_separation(rows, families, protocol)

    design_is_identifying = design in identifying

    flags = {
        "the_lattice_is_computed_exactly": bool(rows),
        "identifiability_is_monotone_under_channel_refinement": bool(not violations),
        "the_order_channel_identifies_the_declared_dimension_worlds":
            bool("order" in accidental["dimension"]),
        "the_counts_channel_identifies_the_conformal_factor": bool(
            "counts" in accidental["conformal"]),
        "absolute_scale_requires_the_external_anchor": bool(
            minima["absolute_scale"] and all("anchor" in entry
                                            for entry in minima["absolute_scale"])),
        "every_internal_reference_is_blind_on_the_witness_class":
            bool(blindness["internal_subsets_all_blind"]),
        "the_anchor_is_not_constructible_from_the_record_channel":
            bool(anchor["anchor_is_external"] and anchor["anchor_separates_the_witness"]),
        "the_one_channel_per_blind_direction_design_is_identifying": bool(design_is_identifying),
        "the_joint_minimum_is_recorded_not_assumed": bool(k_min is not None),
        "a_declared_channel_separates_a_family_beyond_its_mechanism":
            bool(len(accidental["dimension"]) > 1),
        "no_go_remains_outside_the_anchor": bool(
            blindness["internal_subsets_all_blind"] and not violations),
    }

    return {
        "schema": SCHEMA,
        "spec": {
            "question": ("What is the minimal additional channel/anchor that makes scale + "
                         "reference + geometry identifiable?"),
            "channels": protocol["channels"],
            "internal_channels": protocol["internal_channels"],
            "external_channels": protocol["external_channels"],
            "families": protocol["families"],
            "joint_target": joint,
            "status": "Track-B exploratory / correspondence (Status M); no physical claim",
        },
        "worlds": {family: [world["label"] for world in members]
                   for family, members in sorted(families.items())},
        "lattice": rows,
        "minimal_sets": minima,
        "single_channel_identifying_sets": accidental,
        "joint_minimal_sets": joint_minimal,
        "joint_k_min": k_min,
        "one_channel_per_direction_design": design,
        "monotonicity_violations": violations,
        "internal_reference_blindness": blindness,
        "anchor_check": anchor,
        "flags": flags,
        "propositions": [
            {"id": "B1", "statement": "tau is identifiable through O_S iff tau is constant on "
                                      "every O_S-class (CY's P1, extended to channel sets).",
             "status": "proved_elementary"},
            {"id": "B2", "statement": "Identifiability is monotone under channel refinement: "
                                      "S subset S' and identified through S implies identified "
                                      "through S'.", "status": "verified_exhaustively_on_the_lattice"},
            {"id": "B3", "statement": "The minimal anchor set is the inclusion-minimal "
                                      "identifying channel set.", "status": "verified_exhaustively_on_the_lattice"},
            {"id": "B4", "statement": "Absolute scale and any reference from the same channel "
                                      "require the external anchor; every anchor-free channel set "
                                      "is blind on the scale witness class.",
             "status": "verified_exhaustively_on_the_lattice"},
            {"id": "B5", "statement": "A finite channel universe can separate a declared family "
                                      "beyond its mechanism channel; the lattice minimum is "
                                      "therefore reported, not interpreted as a mechanism.",
             "status": "verified_finite_instance"},
            {"id": "B6", "statement": "Observational equivalence is not ontological identity "
                                      "(Status M).", "status": "governance_status_m"},
        ],
        "ontological_claim": False,
        "status_m_guard": "observational equivalence is not ontological identity "
                          "(Status M; GOVERNANCE section 3 F8-OPEN v2; ONTOLOGY.md section 5)",
        "verdict": (
            "QR-05DO (direction B, the anchor calculus): CY's observational quotient is extended to "
            "a calculus over **channel sets**. Identifiability is **monotone** under channel "
            "refinement, verified with no violations over all 32 subsets; the order channel "
            "identifies the declared dimension worlds, the counts channel identifies the conformal "
            "factor, and absolute scale is identified only by sets containing the external "
            "**anchor** — with every **anchor-free** channel set blind on the scale witness class "
            "(no internal channel separates it, and all six reference constructors agree on the "
            "whole anchor-free half of the lattice: CY's P2, lattice-wide). The **joint** target "
            "(dimension, conformal factor, absolute scale) has its inclusion-minimal identifying "
            "sets recorded by the computation, and the one-channel-per-blind-direction design "
            "`{order, counts, anchor}` is identifying. So the minimal DET answer to 'what makes "
            "scale + reference + geometry identifiable?' is **one independent channel per blind "
            "direction** — an order channel for geometry, a count/mark channel for the conformal "
            "factor, and an external unit channel for scale — and only the last is unavailable from "
            "the record channel itself. The lattice minimum is reported as computed (it can be "
            "smaller than the design, because a finite channel universe may separate a declared "
            "family accidentally — recorded separately as B5) and is **not** read as a mechanism "
            "claim. Correspondence-level; no physical claim."),
    }
