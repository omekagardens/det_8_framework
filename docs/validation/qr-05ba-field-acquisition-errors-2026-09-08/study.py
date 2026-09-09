"""QR-05BA field-plus-acquisition composition orchestration."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import platform
import resource
import sys
import time
from fractions import Fraction as F
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05ba-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05ba.py")
AZ = HERE.parent / "qr-05az-refinement-stability-2026-09-08/results.json"
AZ_ID = {
    "bytes": 2380556,
    "sha256": "cbb04f7a4af49a5714ecf80652393933557f490f7e16dab0848b8d32cda27585",
}
MAX_CAPTURE_BYTES = 128 * 1024 * 1024
MAX_WORKING_BYTES = 192 * 1024 * 1024
FAMILIES = ("grid", "warp")
COUNT_FIELDS = (
    "cells",
    "positive_cells",
    "parent_tiles",
    "child_tiles",
    "parent_bank_values",
    "child_bank_values",
    "receiver_values",
    "target_rows",
    "defined_rows",
    "undefined_rows",
    "budgets",
    "input_geometry_entries",
    "input_matrix_entries",
    "input_budget_entries",
    "geometry_entries",
    "restriction_entries",
    "parent_kernel_entries",
    "child_kernel_entries",
    "parent_map_entries",
    "child_map_entries",
    "field_bound_entries",
    "acquisition_entries",
    "case_bound_entries",
    "case_exact_bridge_entries",
    "case_comparison_entries",
    "parent_paired_witnesses",
    "child_witnesses",
    "sign_entries",
    "witness_entries",
    "constant_strict",
    "bilinear_strict",
    "upper_strict",
    "inherited_exact_rows",
    "newly_exact_rows",
    "unavailable_exact_rows",
)
CHECK_FIELDS = (
    "parent_geometry",
    "child_partition",
    "lineage_identity",
    "full_bank_identity",
    "same_receiver_contract",
    "restriction_convexity",
    "field_level_evidence",
    "response_transport",
    "acquisition_map",
    "normalization_domain",
    "composed_bounds",
    "exact_availability",
    "refinement_comparison",
    "paired_field_noise_pipelines",
    "joint_maximum_attainment",
    "complete_inventory",
)
SCOPE = (
    "source_dictionary_changed",
    "old_source_or_target_integrals_recomputed",
    "repair_overlay_regenerated",
    "decoder_refitted",
    "filters_reselected",
    "measurements_added",
    "normalization_row_added",
    "empirical_noise_calibrated",
    "statistical_independence_assumed",
    "field_receiver_error_double_counted",
    "total_source_nonnegativity_guaranteed",
    "global_field_continuity_required",
    "mixed_absolute_kernel_integrated",
    "uncertified_exact_gain_claimed",
    "corner_envelope_sharpness_claimed",
    "subset_exact_max_called_full_query_max",
    "independent_child_fields_called_parent_fields",
    "full_bounded_field_domain_changed",
    "equal_noise_sensor_improvement_claimed",
    "cross_geometry_physical_noise_ranking_claimed",
    "full_field_stability_tested",
    "unknown_geometry_reconstructed",
    "physical_sensor_validated",
    "quantum_channel_constructed",
    "gravity_derived",
    "ret_integration_tested",
    "lean_verification_performed",
    "generic_production_API_hardened",
    "fixed_affine_families_run",
    "older_executors_run",
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def plain_bytes(path):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), "not a plain evidence file")
    require(path.stat().st_size <= MAX_CAPTURE_BYTES, "capture byte cap")
    raw = path.read_bytes()
    require(len(raw) <= MAX_CAPTURE_BYTES, "capture byte cap")
    return raw


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def ident(path):
    raw = plain_bytes(path)
    return {"bytes": len(raw), "sha256": digest(raw)}


def native(value, depth=0):
    require(depth <= 128, "native depth")
    kind = type(value)
    if value is None or kind in (bool, str):
        return
    if kind is int:
        require(abs(value).bit_length() <= 4096, "retained component bits")
        return
    require(kind in (list, dict), "native mathematical data required")
    if kind is dict:
        require(all(type(k) is str for k in value), "native keys")
    for child in value.values() if kind is dict else value:
        native(child, depth + 1)


def canonical(value):
    raw = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")
    require(len(raw) <= MAX_WORKING_BYTES, "working byte cap")
    return raw


def verify_suite(actual, expected):
    native(actual)
    native(expected)
    require(canonical(actual) == canonical(expected), "complete mathematical wire differs")


def prior_document():
    require(ident(AZ) == AZ_ID, "AZ artifact changed")
    return json.loads(plain_bytes(AZ))


def identities():
    previous = prior_document()
    prior = {str(AZ.relative_to(HERE.parent)): AZ_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AZ.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def rational(value):
    require(type(value) is list and len(value) == 2, "rational pair shape")
    n, d = value
    require(
        type(n) is int
        and type(d) is int
        and d > 0
        and max(abs(n).bit_length(), d.bit_length()) <= 4096
        and gcd(n, d) == 1,
        "reduced bounded rational",
    )
    return F(n, d)


def fw(value):
    return [value.numerator, value.denominator]


def project_inputs(previous):
    require(type(previous) is list and len(previous) == 2, "AZ family inventory")
    require(
        all(type(f) is dict and type(f.get("input")) is dict for f in previous),
        "AZ refinement records",
    )
    require(
        all(set(f["input"]) == {"parent", "children"} for f in previous),
        "selected AZ refinement fields",
    )
    require(all(type(f["input"]["parent"]) is dict for f in previous), "AZ parent records")
    require(
        [f["input"]["parent"].get("family") for f in previous] == list(FAMILIES), "AZ family order"
    )
    fields = {
        "family",
        "probe",
        "cells",
        "tiles",
        "bank_labels",
        "target_labels",
        "interface",
        "geometric",
        "decoder",
    }
    inputs = []
    for family in previous:
        refinement = family["input"]
        p, children = refinement["parent"], refinement["children"]
        require(set(p) == fields, "selected AZ parent fields")
        for key, length in (
            ("probe", 4),
            ("cells", 8),
            ("tiles", 12),
            ("bank_labels", 48),
            ("target_labels", 64),
        ):
            require(type(p[key]) is list and len(p[key]) == length, "selected AZ inventory")
        for key, rows, width in (("interface", 37, 48), ("geometric", 64, 48), ("decoder", 64, 37)):
            require(
                type(p[key]) is list
                and len(p[key]) == rows
                and all(type(row) is list and len(row) == width for row in p[key]),
                "selected AZ matrix inventory",
            )
        require(type(children) is list and len(children) == 48, "selected AZ children")
        native(refinement)
        for tile in p["tiles"]:
            require(type(tile) is dict and set(tile) == {"event", "bounds"}, "AZ tile fields")
            require(type(tile["bounds"]) is list and len(tile["bounds"]) == 4, "AZ tile bounds")
        for child in children:
            require(
                type(child) is dict
                and set(child) == {"parent", "bounds"}
                and type(child["parent"]) is int
                and 0 <= child["parent"] < 12
                and type(child["bounds"]) is list
                and len(child["bounds"]) == 4,
                "AZ child fields",
            )
        for box in [t["bounds"] for t in p["tiles"]] + [t["bounds"] for t in children]:
            u0, u1, v0, v1 = map(rational, box)
            require(u0 < u1 and v0 < v1, "positive selected AZ rectangle")
        supplied = {
            "refinement": copy.deepcopy(refinement),
            "receiver_radii": [[1, 1] for _ in range(37)],
            "budgets": [
                {"name": name, "field": [eps, 1], "acquisition": [eta, 1]}
                for name, eps, eta in (
                    ("zero", 0, 0),
                    ("field", 1, 0),
                    ("acquisition", 0, 1),
                    ("joint", 1, 1),
                )
            ],
        }
        native(supplied)
        inputs.append(supplied)
    return inputs, previous


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05ba_" + name, HERE / filename)
    require(spec is not None and spec.loader is not None, "engine loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def index_rows(rows, q, nonempty=False):
    require(
        type(rows) is list and all(type(i) is int and 0 <= i < q for i in rows),
        "native target indices",
    )
    require(rows == sorted(set(rows)) and (bool(rows) or not nonempty), "ordered target indices")


def vector_check(values, width, nulls=()):
    require(type(values) is list and len(values) == width, "vector width")
    for i, value in enumerate(values):
        if i in nulls:
            require(value is None, "undefined value must be null")
        else:
            rational(value)


def matrix_check(rows, height, width, nulls=(), zeros=False):
    require(type(rows) is list and len(rows) == height, "matrix height")
    for i, row in enumerate(rows):
        if i in nulls:
            require(row is None, "undefined row must be null")
        else:
            vector_check(row, width)
            if zeros:
                require(all(x == [0, 1] for x in row), "zero matrix residual")


def block_check(blocks, tiles, zeros=False):
    require(type(blocks) is list and len(blocks) == tiles, "block inventory")
    for block in blocks:
        matrix_check(block, 4, 4, zeros=zeros)


def maximum_check(values, domain, maximum):
    wanted = max((rational(values[i]) for i in domain), default=None)
    require(set(maximum) == {"gain", "rows"}, "maximum fields")
    verify_suite(
        maximum,
        {
            "gain": None if wanted is None else fw(wanted),
            "rows": [i for i in domain if rational(values[i]) == wanted],
        },
    )


def sign(value):
    return (value > 0) - (value < 0)


def linear(matrix, values):
    v = list(map(rational, values))
    return [fw(sum((rational(a) * x for a, x in zip(row, v, strict=True)), F(0))) for row in matrix]


def add_vectors(left, right):
    return [fw(rational(a) + rational(b)) for a, b in zip(left, right, strict=True)]


def restrict(corners, blocks, lineage):
    c = list(map(rational, corners))
    return [
        fw(sum((rational(w) * c[4 * parent + a] for a, w in enumerate(row)), F(0)))
        for block, parent in zip(blocks, lineage, strict=True)
        for row in block
    ]


def aggregate(values, lineage, parents):
    out = [F(0)] * (4 * parents)
    for child, parent in enumerate(lineage):
        for a in range(4):
            out[4 * parent + a] += rational(values[4 * child + a])
    return list(map(fw, out))


def pipeline_check(e, problem, field_level, case_level, acquisition, g, eps, eta, rho):
    t, s, q = len(problem["tiles"]), len(problem["interface"]), len(problem["geometric"])
    undefined = g["undefined_rows"]
    widths = {
        "corners": 4 * t,
        "acquisition_coordinates": s,
        "global_coefficients": 4 * t,
        "bank_error": 4 * t,
        "field_observed_error": s,
        "acquisition_error": s,
        "total_observed_error": s,
        "field_direct_error": q,
        "field_decoded_error": q,
        "acquisition_direct_error": q,
        "acquisition_decoded_error": q,
        "total_direct_error": q,
        "total_decoded_error": q,
        "normalized_error": q,
        "tile_minima": t,
        "tile_maxima": t,
    }
    require(type(e) is dict and set(e) == set(widths), "joint pipeline fields")
    for key, width in widths.items():
        vector_check(e[key], width, undefined if key == "normalized_error" else ())
    require(all(abs(rational(x)) <= eps for x in e["corners"]), "field budget")
    require(
        all(abs(rational(x)) <= eta for x in e["acquisition_coordinates"]), "acquisition budget"
    )
    amplitude = rational(g["volume"]) ** 2
    for lo, hi in zip(e["tile_minima"], e["tile_maxima"], strict=True):
        require(
            -eps * amplitude <= rational(lo) <= rational(hi) <= eps * amplitude,
            "actual physical field extrema",
        )
    verify_suite(e["field_observed_error"], linear(problem["interface"], e["bank_error"]))
    verify_suite(e["field_direct_error"], linear(problem["geometric"], e["bank_error"]))
    verify_suite(e["field_decoded_error"], linear(problem["decoder"], e["field_observed_error"]))
    verify_suite(e["field_direct_error"], e["field_decoded_error"])
    verify_suite(
        e["acquisition_error"],
        [
            fw(radius * rational(z))
            for radius, z in zip(rho, e["acquisition_coordinates"], strict=True)
        ],
    )
    verify_suite(
        e["total_observed_error"], add_vectors(e["field_observed_error"], e["acquisition_error"])
    )
    verify_suite(
        e["acquisition_direct_error"], linear(acquisition["raw_map"], e["acquisition_coordinates"])
    )
    verify_suite(e["acquisition_decoded_error"], linear(problem["decoder"], e["acquisition_error"]))
    verify_suite(e["acquisition_direct_error"], e["acquisition_decoded_error"])
    verify_suite(
        e["total_direct_error"], add_vectors(e["field_direct_error"], e["acquisition_direct_error"])
    )
    verify_suite(e["total_decoded_error"], linear(problem["decoder"], e["total_observed_error"]))
    verify_suite(
        e["total_decoded_error"],
        add_vectors(e["field_decoded_error"], e["acquisition_decoded_error"]),
    )
    verify_suite(e["total_direct_error"], e["total_decoded_error"])
    verify_suite(
        e["field_direct_error"], linear(field_level["maps"]["raw_bilinear_target"], e["corners"])
    )
    for i in g["defined_rows"]:
        value = rational(e["total_decoded_error"][i]) / rational(g["target_scales"][i])
        verify_suite(e["normalized_error"][i], fw(value))
        require(
            abs(value)
            <= rational(case_level["bounds"]["bilinear_lower"][i])
            <= rational(case_level["bounds"]["corner_upper"][i]),
            "composed actual field bound",
        )
    # Null normalized rows remain unavailable even with nonzero raw acquisition output.


def pair_check(pair, context):
    problem, cp, field, case, acquisition, g, eps, eta, rho = context
    p, m, s, q = (
        len(problem["tiles"]),
        len(cp["tiles"]),
        len(problem["interface"]),
        len(problem["geometric"]),
    )
    undefined = g["undefined_rows"]
    widths = {
        "aggregated_bank_error": 4 * p,
        "bank_residual": 4 * p,
        "field_observed_residual": s,
        "acquisition_residual": s,
        "total_observed_residual": s,
        "field_direct_residual": q,
        "field_decoded_residual": q,
        "acquisition_direct_residual": q,
        "acquisition_decoded_residual": q,
        "total_direct_residual": q,
        "total_decoded_residual": q,
        "normalized_residual": q,
        "field_coefficient_residual": 4 * m,
    }
    require(
        type(pair) is dict and set(pair) == set(widths) | {"parent", "child"}, "joint pair fields"
    )
    for name, pr in (("parent", problem), ("child", cp)):
        pipeline_check(
            pair[name],
            pr,
            field["levels"][name],
            case["levels"][name],
            acquisition,
            g,
            eps,
            eta,
            rho,
        )
    for key, width in widths.items():
        vector_check(pair[key], width, undefined if key == "normalized_residual" else ())
        if key != "aggregated_bank_error":
            require(all(x is None or x == [0, 1] for x in pair[key]), "joint pair residual")
    verify_suite(
        pair["child"]["corners"],
        restrict(pair["parent"]["corners"], field["restriction_blocks"], g["child_parents"]),
    )
    verify_suite(
        pair["aggregated_bank_error"], aggregate(pair["child"]["bank_error"], g["child_parents"], p)
    )
    verify_suite(pair["aggregated_bank_error"], pair["parent"]["bank_error"])
    for key in (
        "acquisition_coordinates",
        "field_observed_error",
        "acquisition_error",
        "total_observed_error",
        "field_direct_error",
        "field_decoded_error",
        "acquisition_direct_error",
        "acquisition_decoded_error",
        "total_direct_error",
        "total_decoded_error",
        "normalized_error",
    ):
        verify_suite(pair["parent"][key], pair["child"][key])
    verify_suite(
        pair["child"]["global_coefficients"],
        [
            v
            for parent in g["child_parents"]
            for v in pair["parent"]["global_coefficients"][4 * parent : 4 * parent + 4]
        ],
    )


def comparison_check(comparison, parent, child, defined, undefined):
    require(
        type(comparison) is dict
        and set(comparison) == {"constant_increase", "bilinear_increase", "upper_decrease"},
        "comparison fields",
    )
    q = len(parent["constant_lower"])
    for name, key, direction in (
        ("constant_increase", "constant_lower", 1),
        ("bilinear_increase", "bilinear_lower", 1),
        ("upper_decrease", "corner_upper", -1),
    ):
        c = comparison[name]
        require(
            type(c) is dict
            and set(c)
            == {
                "gain_gap",
                "strict_rows",
                "tied_rows",
                "unavailable_rows",
                "max_gap",
                "max_gap_rows",
            },
            "comparison record",
        )
        gaps = [
            None
            if i in undefined
            else direction * (rational(child[key][i]) - rational(parent[key][i]))
            for i in range(q)
        ]
        require(all(gaps[i] >= 0 for i in defined), "composed refinement bound order")
        verify_suite(c["gain_gap"], [None if x is None else fw(x) for x in gaps])
        verify_suite(c["strict_rows"], [i for i in defined if gaps[i] > 0])
        verify_suite(c["tied_rows"], [i for i in defined if gaps[i] == 0])
        verify_suite(c["unavailable_rows"], undefined)
        maximum_check(c["gain_gap"], defined, {"gain": c["max_gap"], "rows": c["max_gap_rows"]})


def count_check(f):
    problem = f["input"]["refinement"]["parent"]
    field, g = f["field"], f["field"]["geometry"]
    cp = field["child_problem"]
    n, a = len(problem["cells"]), sum(c["bounds"] is not None for c in problem["cells"])
    p, m, s, q = (
        len(problem["tiles"]),
        len(cp["tiles"]),
        len(problem["interface"]),
        len(problem["geometric"]),
    )
    rp, rc, d, b = 4 * p, 4 * m, len(g["defined_rows"]), len(f["cases"])
    zf = [
        len(field["levels"][name]["certification"]["certified_rows"])
        for name in ("parent", "child")
    ]
    z = [
        (
            len(case["levels"]["parent"]["exactness"]["available_rows"]),
            len(case["levels"]["child"]["exactness"]["available_rows"]),
        )
        for case in f["cases"]
    ]
    pairs = [4 + 4 * bool(d) + 2 * bool(zp) for zp, _ in z]
    child = [4 * bool(d) + 2 * bool(zc) for _, zc in z]
    ep, ec = 3 * rp + 4 * s + 6 * q + d + 2 * p, 3 * rc + 4 * s + 6 * q + d + 2 * m
    epair = ep + ec + 2 * rp + 3 * s + 6 * q + d + rc
    expected = {
        "cells": n,
        "positive_cells": a,
        "parent_tiles": p,
        "child_tiles": m,
        "parent_bank_values": rp,
        "child_bank_values": rc,
        "receiver_values": s,
        "target_rows": q,
        "defined_rows": d,
        "undefined_rows": q - d,
        "budgets": b,
        "input_geometry_entries": 4 + 4 * a + 4 * p + 4 * m,
        "input_matrix_entries": s * rp + q * rp + q * s,
        "input_budget_entries": s + 2 * b,
        "geometry_entries": 1 + n + q + p + m,
        "restriction_entries": 16 * m,
        "parent_kernel_entries": 12 * q * p,
        "child_kernel_entries": 12 * q * m,
        "parent_map_entries": (3 * q + d) * rp,
        "child_map_entries": (3 * q + d) * rc,
        "field_bound_entries": sum(3 * d + x + 3 * bool(d) + bool(x) for x in zf),
        "acquisition_entries": q * s + d * s + d + bool(d),
        "case_bound_entries": sum(3 * d + x + 3 * bool(d) + bool(x) for pair in z for x in pair),
        "case_exact_bridge_entries": sum(zp for zp, _ in z),
        "case_comparison_entries": b * (3 * d + 3 * bool(d)),
        "parent_paired_witnesses": sum(pairs),
        "child_witnesses": sum(child),
        "sign_entries": sum(
            bool(d) * (p + rp + m + rc + 4 * s) + bool(zp) * (p + s) + bool(zc) * (m + s)
            for zp, zc in z
        ),
        "witness_entries": sum(k * epair + l * ec for k, l in zip(pairs, child, strict=True)),
        "constant_strict": sum(
            len(x["comparison"]["constant_increase"]["strict_rows"]) for x in f["cases"]
        ),
        "bilinear_strict": sum(
            len(x["comparison"]["bilinear_increase"]["strict_rows"]) for x in f["cases"]
        ),
        "upper_strict": sum(
            len(x["comparison"]["upper_decrease"]["strict_rows"]) for x in f["cases"]
        ),
        "inherited_exact_rows": sum(len(x["exact_bridge"]["inherited_rows"]) for x in f["cases"]),
        "newly_exact_rows": sum(len(x["exact_bridge"]["newly_exact_rows"]) for x in f["cases"]),
        "unavailable_exact_rows": sum(
            len(x["exact_bridge"]["unavailable_rows"]) for x in f["cases"]
        ),
    }
    require(set(expected) == set(COUNT_FIELDS), "internal count inventory")
    verify_suite(f["counts"], expected)


def case_controls(case, f):
    field, acq = f["field"], f["acquisition"]
    g = field["geometry"]
    problem, cp = f["input"]["refinement"]["parent"], field["child_problem"]
    p, m, s, q = (
        len(problem["tiles"]),
        len(cp["tiles"]),
        len(problem["interface"]),
        len(problem["geometric"]),
    )
    defined, undefined = g["defined_rows"], g["undefined_rows"]
    require(
        type(case) is dict
        and set(case) == {"budget", "levels", "comparison", "exact_bridge", "witnesses"},
        "budget case fields",
    )
    require(set(case["levels"]) == {"parent", "child"}, "budget levels")
    eps, eta = rational(case["budget"]["field"]), rational(case["budget"]["acquisition"])
    require(eps >= 0 and eta >= 0, "nonnegative budget")
    rho = list(map(rational, f["input"]["receiver_radii"]))
    bound_keys = ("constant_lower", "bilinear_lower", "corner_upper", "exact_gain")
    for name in ("parent", "child"):
        level = case["levels"][name]
        require(type(level) is dict and set(level) == {"bounds", "exactness"}, "case level fields")
        bounds, exactness = level["bounds"], level["exactness"]
        require(
            set(bounds) == set(bound_keys) | {"maxima"}
            and set(bounds["maxima"]) == set(bound_keys),
            "composed bound inventory",
        )
        fb = field["levels"][name]["bounds"]
        available = [i for i in defined if eps == 0 or fb["certified_gain"][i] is not None]
        unavailable = [i for i in defined if i not in available]
        reasons = [
            "undefined"
            if i in undefined
            else "zero_field_budget"
            if eps == 0
            else "field_certified"
            if i in available
            else "unavailable"
            for i in range(q)
        ]
        verify_suite(
            exactness,
            {
                "reason": reasons,
                "available_rows": available,
                "unavailable_rows": unavailable,
                "undefined_rows": undefined,
            },
        )
        for key in bound_keys:
            domain = available if key == "exact_gain" else defined
            vector_check(bounds[key], q, [i for i in range(q) if i not in domain])
            expected = []
            for i in range(q):
                if i not in domain:
                    expected.append(None)
                else:
                    source = "certified_gain" if key == "exact_gain" else key
                    value = F(0) if eps == 0 else eps * rational(fb[source][i])
                    expected.append(fw(value + eta * rational(acq["gain"][i])))
            verify_suite(bounds[key], expected)
            maximum_check(bounds[key], domain, bounds["maxima"][key])
        for i in defined:
            require(
                0
                <= rational(bounds["constant_lower"][i])
                <= rational(bounds["bilinear_lower"][i])
                <= rational(bounds["corner_upper"][i]),
                "composed bounds",
            )
            if i in available:
                require(
                    rational(bounds["bilinear_lower"][i])
                    <= rational(bounds["exact_gain"][i])
                    <= rational(bounds["corner_upper"][i]),
                    "exact composed sandwich",
                )
    comparison_check(
        case["comparison"],
        case["levels"]["parent"]["bounds"],
        case["levels"]["child"]["bounds"],
        defined,
        undefined,
    )
    pa, ca = (case["levels"][name]["exactness"]["available_rows"] for name in ("parent", "child"))
    require(set(pa) <= set(ca), "available exact row lost")
    verify_suite(
        case["exact_bridge"],
        {
            "inherited_rows": pa,
            "newly_exact_rows": [i for i in ca if i not in pa],
            "unavailable_rows": [i for i in defined if i not in ca],
            "undefined_rows": undefined,
            "inherited_gain_residuals": [[0, 1] if i in pa else None for i in range(q)],
        },
    )
    for i in pa:
        verify_suite(
            case["levels"]["parent"]["bounds"]["exact_gain"][i],
            case["levels"]["child"]["bounds"]["exact_gain"][i],
        )
    w = case["witnesses"]
    require(
        type(w) is dict
        and set(w)
        == {
            "parent_pattern",
            "parent_constant",
            "parent_constant_maximizer",
            "parent_bilinear_maximizer",
            "parent_exact_maximizer",
            "child_constant_maximizer",
            "child_bilinear_maximizer",
            "child_exact_maximizer",
        },
        "canonical witness inventory",
    )
    context = (problem, cp, field, case, acq, g, eps, eta, rho)
    pattern = [F(-1), F(0), F(1), F(1, 2)]
    for name in ("parent_pattern", "parent_constant"):
        group = w[name]
        require(type(group) is dict and set(group) == {"positive", "negative"}, "control group")
        corners = [eps * x for x in pattern] * p if name == "parent_pattern" else [eps] * (4 * p)
        z = [eta * pattern[j % 4] for j in range(s)] if name == "parent_pattern" else [eta] * s
        for side, direction in (("positive", 1), ("negative", -1)):
            pair_check(group[side], context)
            verify_suite(group[side]["parent"]["corners"], [fw(direction * x) for x in corners])
            verify_suite(
                group[side]["parent"]["acquisition_coordinates"], [fw(direction * x) for x in z]
            )
    for name, t, pr in (("parent", p, problem), ("child", m, cp)):
        level = case["levels"][name]
        for kind, key in (
            ("constant", "constant_lower"),
            ("bilinear", "bilinear_lower"),
            ("exact", "exact_gain"),
        ):
            group = w[name + "_" + kind + "_maximizer"]
            maximum = level["bounds"]["maxima"][key]
            if not maximum["rows"]:
                require(group is None, "unavailable maximum witness")
                continue
            require(
                type(group) is dict
                and set(group)
                == {"target_row", "field_signs", "acquisition_signs", "positive", "negative"},
                "maximum witness fields",
            )
            row = maximum["rows"][0]
            require(
                type(group["target_row"]) is int and group["target_row"] == row,
                "first maximum witness row",
            )
            values = (
                field["levels"][name]["maps"]["normalized_bilinear_target"][row]
                if kind == "bilinear"
                else field["levels"][name]["kernels"]["tile_integrals"][row]
            )
            fs = [sign(rational(x)) if eps else 0 for x in values]
            ns = [sign(rational(x)) if eta else 0 for x in acq["raw_map"][row]]
            verify_suite(group["field_signs"], fs)
            verify_suite(group["acquisition_signs"], ns)
            for side, direction in (("positive", 1), ("negative", -1)):
                endpoint = group[side]
                if name == "parent":
                    pair_check(endpoint, context)
                    endpoint = endpoint["parent"]
                else:
                    pipeline_check(
                        endpoint, pr, field["levels"][name], level, acq, g, eps, eta, rho
                    )
                verify_suite(
                    endpoint["corners"],
                    [
                        fw(direction * eps * x)
                        for x in fs
                        for _ in range(1 if kind == "bilinear" else 4)
                    ],
                )
                verify_suite(
                    endpoint["acquisition_coordinates"], [fw(direction * eta * x) for x in ns]
                )
                verify_suite(
                    endpoint["normalized_error"][row], fw(direction * rational(maximum["gain"]))
                )


def level_controls(f, q, t, defined, undefined):
    require(
        type(f) is dict and set(f) == {"kernels", "maps", "bounds", "certification"}, "level fields"
    )
    k, cert, bounds = (f[key] for key in ("kernels", "certification", "bounds"))
    r = 4 * t
    bound_keys = ("constant_lower", "bilinear_lower", "corner_upper", "certified_gain")
    require(
        set(k)
        == {
            "corner_values",
            "tile_integrals",
            "bernstein_integrals",
            "tile_abs_upper",
            "tile_minima",
            "tile_maxima",
            "tile_classes",
        },
        "complete kernel inventory",
    )
    for key, width in (
        ("corner_values", t),
        ("tile_integrals", t),
        ("bernstein_integrals", r),
        ("tile_abs_upper", t),
        ("tile_minima", t),
        ("tile_maxima", t),
        ("tile_classes", t),
    ):
        require(
            type(k[key]) is list
            and len(k[key]) == q
            and all(type(row) is list and len(row) == width for row in k[key]),
            "kernel matrix shape",
        )
    for i in range(q):
        for j in range(t):
            vertices = k["corner_values"][i][j]
            require(type(vertices) is list and len(vertices) == 4, "four actual corners")
            require(
                all(
                    type(x) is list
                    and len(x) == 2
                    and type(x[0]) is int
                    and type(x[1]) is int
                    and x[1] > 0
                    for x in vertices
                ),
                "native kernel corner fractions",
            )
            nums = [x[0] for x in vertices]
            want = (
                "zero"
                if all(x == 0 for x in nums)
                else "nonnegative"
                if all(x >= 0 for x in nums)
                else "nonpositive"
                if all(x <= 0 for x in nums)
                else "mixed"
            )
            require(k["tile_classes"][i][j] == want, "actual corner sign class")
    require(
        set(f["maps"])
        == {
            "decoder_bank",
            "bank_residual",
            "raw_bilinear_target",
            "normalized_bilinear_target",
        },
        "complete maps",
    )
    for key in (
        "decoder_bank",
        "bank_residual",
        "raw_bilinear_target",
        "normalized_bilinear_target",
    ):
        rows = f["maps"][key]
        require(type(rows) is list and len(rows) == q, "map rows")
        for i, row in enumerate(rows):
            null = key == "normalized_bilinear_target" and i in undefined
            require(
                row is None if null else type(row) is list and len(row) == r,
                "raw/normalized map shape",
            )
    require(
        set(cert)
        == {
            "status",
            "mixed_obstructions",
            "certified_rows",
            "uncertified_rows",
            "undefined_rows",
            "nonnegative_rows",
            "nonpositive_rows",
            "zero_rows",
            "integrated_nonnegative_rows",
            "integrated_nonpositive_rows",
            "integrated_zero_rows",
            "integrated_nonnegative_mixed_rows",
        },
        "complete certification inventory",
    )
    for key in set(cert) - {"status", "mixed_obstructions"}:
        index_rows(cert[key], q)
    verify_suite(cert["undefined_rows"], undefined)
    certified, uncertain = cert["certified_rows"], cert["uncertified_rows"]
    require(sorted(certified + uncertain + undefined) == list(range(q)), "certificate partition")
    require(
        type(cert["status"]) is list
        and len(cert["status"]) == q
        and type(cert["mixed_obstructions"]) is list
        and len(cert["mixed_obstructions"]) == q,
        "status/obstruction rows",
    )
    for i in range(q):
        mixed = [j for j, kind in enumerate(k["tile_classes"][i]) if kind == "mixed"]
        want = "undefined" if i in undefined else "uncertified" if mixed else "certified"
        require(
            cert["status"][i] == want
            and (i in certified) == (want == "certified")
            and (i in uncertain) == (want == "uncertified"),
            "certificate status",
        )
        proof = []
        for j in mixed:
            vertices = k["corner_values"][i][j]
            proof.append(
                {
                    "tile": j,
                    "positive_corner": next(a for a, x in enumerate(vertices) if x[0] > 0),
                    "negative_corner": next(a for a, x in enumerate(vertices) if x[0] < 0),
                }
            )
        verify_suite(cert["mixed_obstructions"][i], proof)
    for prefix, rows in (
        ("", [[x for tile in row for x in tile] for row in k["corner_values"]]),
        ("integrated_", f["maps"]["normalized_bilinear_target"]),
    ):
        pos = [i for i in defined if all(x[0] >= 0 for x in rows[i])]
        neg = [i for i in defined if all(x[0] <= 0 for x in rows[i])]
        verify_suite(cert[prefix + "nonnegative_rows"], pos)
        verify_suite(cert[prefix + "nonpositive_rows"], neg)
        verify_suite(cert[prefix + "zero_rows"], sorted(set(pos) & set(neg)))
    verify_suite(
        cert["integrated_nonnegative_mixed_rows"],
        sorted(set(cert["integrated_nonnegative_rows"]) & set(uncertain)),
    )
    require(
        set(bounds) == set(bound_keys) | {"maxima"} and set(bounds["maxima"]) == set(bound_keys),
        "complete bounds",
    )
    for key in bound_keys:
        domain = certified if key == "certified_gain" else defined
        values, maximum = bounds[key], bounds["maxima"][key]
        require(type(values) is list and len(values) == q, "bound vector")
        for i, value in enumerate(values):
            require((value is None) == (i not in domain), "bound null domain")
        require(set(maximum) == {"gain", "rows"}, "maximum fields")
        index_rows(maximum["rows"], q, bool(domain))
        require(
            all(i in domain for i in maximum["rows"]) and (maximum["gain"] is None) == (not domain),
            "maximum domain",
        )
        for i in maximum["rows"]:
            verify_suite(values[i], maximum["gain"])
    for i in certified:
        verify_suite(bounds["constant_lower"][i], bounds["bilinear_lower"][i])
        verify_suite(bounds["constant_lower"][i], bounds["certified_gain"][i])


def controls(families):
    require(type(families) is list and len(families) == 2, "two case families")
    for f in families:
        require(
            type(f) is dict
            and set(f) == {"input", "field", "acquisition", "cases", "checks", "counts"},
            "family fields",
        )
        native(f)
        verify_suite(f["checks"], dict.fromkeys(CHECK_FIELDS, True))
        data = f["input"]
        require(
            type(data) is dict and set(data) == {"refinement", "receiver_radii", "budgets"},
            "composition input fields",
        )
        refinement = data["refinement"]
        require(
            type(refinement) is dict and set(refinement) == {"parent", "children"},
            "refinement fields",
        )
        problem, children = refinement["parent"], refinement["children"]
        field = f["field"]
        require(
            type(field) is dict
            and set(field) == {"child_problem", "geometry", "restriction_blocks", "levels"},
            "selected field evidence",
        )
        cp, g = field["child_problem"], field["geometry"]
        p, m, s, q = (
            len(problem["tiles"]),
            len(children),
            len(problem["interface"]),
            len(problem["geometric"]),
        )
        require(set(cp) == set(problem), "child problem fields")
        for key in ("family", "probe", "cells", "target_labels", "decoder"):
            verify_suite(cp[key], problem[key])
        lineage = [x["parent"] for x in children]
        require(all(type(j) is int and 0 <= j < p for j in lineage), "native lineage")
        verify_suite(
            cp["tiles"],
            [
                {"event": problem["tiles"][x["parent"]]["event"], "bounds": x["bounds"]}
                for x in children
            ],
        )
        verify_suite(
            cp["bank_labels"], [{"tile": j, "basis": a} for j in range(m) for a in range(4)]
        )
        for key in ("interface", "geometric"):
            verify_suite(
                cp[key],
                [[v for j in lineage for v in row[4 * j : 4 * j + 4]] for row in problem[key]],
            )
        require(
            set(g)
            == {
                "volume",
                "cell_volumes",
                "target_scales",
                "defined_rows",
                "undefined_rows",
                "parent_tile_volumes",
                "child_tile_volumes",
                "child_parents",
            },
            "geometry fields",
        )
        defined, undefined = g["defined_rows"], g["undefined_rows"]
        index_rows(defined, q)
        index_rows(undefined, q)
        require(sorted(defined + undefined) == list(range(q)), "normalization partition")
        require(rational(g["volume"]) > 0, "probe volume")
        vector_check(g["cell_volumes"], len(problem["cells"]))
        vector_check(g["target_scales"], q)
        vector_check(g["parent_tile_volumes"], p)
        vector_check(g["child_tile_volumes"], m)
        verify_suite(g["child_parents"], lineage)
        require(all(rational(v) >= 0 for v in g["cell_volumes"]), "cell volumes")
        require(
            all(rational(v) > 0 for v in g["parent_tile_volumes"] + g["child_tile_volumes"]),
            "tile volumes",
        )
        for i, scale in enumerate(g["target_scales"]):
            require(
                rational(scale) == 0 if i in undefined else rational(scale) > 0,
                "normalization scale",
            )
        blocks = field["restriction_blocks"]
        block_check(blocks, m)
        for block in blocks:
            require(all(0 <= rational(x) <= 1 for row in block for x in row), "restriction weights")
            require(all(sum(map(rational, row)) == 1 for row in block), "restriction convexity")
        require(set(field["levels"]) == {"parent", "child"}, "field levels")
        for name, t, pr in (("parent", p, problem), ("child", m, cp)):
            level = field["levels"][name]
            level_controls(level, q, t, defined, undefined)
            verify_suite(level["maps"]["decoder_bank"], pr["geometric"])
            matrix_check(level["maps"]["bank_residual"], q, 4 * t, zeros=True)
            bounds = level["bounds"]
            for key in ("constant_lower", "bilinear_lower", "corner_upper", "certified_gain"):
                domain = (
                    level["certification"]["certified_rows"] if key == "certified_gain" else defined
                )
                vector_check(bounds[key], q, [i for i in range(q) if i not in domain])
                maximum_check(bounds[key], domain, bounds["maxima"][key])
            for i in defined:
                require(
                    0
                    <= rational(bounds["constant_lower"][i])
                    <= rational(bounds["bilinear_lower"][i])
                    <= rational(bounds["corner_upper"][i]),
                    "field bound order",
                )
        parent, child = (field["levels"][name] for name in ("parent", "child"))
        for i in range(q):
            for j, owner in enumerate(lineage):
                verify_suite(
                    child["kernels"]["corner_values"][i][j],
                    linear(blocks[j], parent["kernels"]["corner_values"][i][owner]),
                )
        for key in ("raw_bilinear_target", "normalized_bilinear_target"):
            for i in range(q):
                row = child["maps"][key][i]
                if row is None:
                    require(parent["maps"][key][i] is None, "response transport null domain")
                    continue
                out = [F(0)] * (4 * p)
                for j, owner in enumerate(lineage):
                    for a in range(4):
                        out[4 * owner + a] += sum(
                            (
                                rational(row[4 * j + k]) * rational(blocks[j][k][a])
                                for k in range(4)
                            ),
                            F(0),
                        )
                verify_suite(parent["maps"][key][i], list(map(fw, out)))
        rho = list(map(rational, data["receiver_radii"]))
        require(len(rho) == s and all(x >= 0 for x in rho), "receiver radii")
        acq = f["acquisition"]
        require(
            type(acq) is dict and set(acq) == {"raw_map", "normalized_map", "gain", "maxima"},
            "acquisition fields",
        )
        matrix_check(acq["raw_map"], q, s)
        matrix_check(acq["normalized_map"], q, s, undefined)
        vector_check(acq["gain"], q, undefined)
        verify_suite(
            acq["raw_map"],
            [
                [fw(rational(x) * r) for x, r in zip(row, rho, strict=True)]
                for row in problem["decoder"]
            ],
        )
        for i in defined:
            row = [fw(rational(x) / rational(g["target_scales"][i])) for x in acq["raw_map"][i]]
            verify_suite(acq["normalized_map"][i], row)
            verify_suite(acq["gain"][i], fw(sum((abs(rational(x)) for x in row), F(0))))
        maximum_check(acq["gain"], defined, acq["maxima"])
        require(
            type(data["budgets"]) is list and 1 <= len(data["budgets"]) <= 8, "budget inventory"
        )
        names = []
        for budget in data["budgets"]:
            require(
                type(budget) is dict
                and set(budget) == {"name", "field", "acquisition"}
                and type(budget["name"]) is str
                and bool(budget["name"]),
                "budget fields",
            )
            require(
                rational(budget["field"]) >= 0 and rational(budget["acquisition"]) >= 0,
                "nonnegative budget",
            )
            names.append(budget["name"])
        require(len(set(names)) == len(names), "unique budget names")
        require(
            type(f["cases"]) is list and len(f["cases"]) == len(data["budgets"]), "case inventory"
        )
        verify_suite([case["budget"] for case in f["cases"]], data["budgets"])
        for case in f["cases"]:
            case_controls(case, f)
        count_check(f)
    require(
        [f["input"]["refinement"]["parent"]["family"] for f in families] == list(FAMILIES),
        "family order",
    )
    return dict.fromkeys(CHECK_FIELDS, True)


def historical_bridges(families, previous):
    expected, _ = project_inputs(previous)
    verify_suite([f["input"] for f in families], expected)
    controls(families)
    for f, az in zip(families, previous, strict=True):
        field = f["field"]
        verify_suite(field["child_problem"], az["child_problem"])
        verify_suite(field["geometry"], az["geometry"])
        verify_suite(field["restriction_blocks"], az["restriction"]["blocks"])
        verify_suite(field["levels"], az["levels"])
    return {
        "selected_families": list(FAMILIES),
        "AZ_refinement_equal": True,
        "AZ_child_problem_equal": True,
        "AZ_geometry_equal": True,
        "AZ_restriction_blocks_equal": True,
        "AZ_levels_equal": True,
        "same_physical_field_domain": True,
        "same_receiver_contract": True,
        "AZ_endpoints_replayed": False,
        "AZ_unselected_mathematics_replayed": False,
        "older_executors_run": False,
    }


def payload_sizes(families):
    fields = {"input": "input", "field": "field", "acquisition": "acquisition", "case": "cases"}
    return [
        {
            "family": f["input"]["refinement"]["parent"]["family"],
            **{name + "_bytes": len(canonical(f[key])) for name, key in fields.items()},
            "native_family_bytes": len(canonical(f)),
        }
        for f in families
    ]


def assemble_suite(families, previous):
    expected, consumed = load_inputs()
    verify_suite(previous, consumed)
    verify_suite([f["input"] for f in families], expected)
    controls(families)
    for family in families:
        require(set(family["counts"]) == set(COUNT_FIELDS), "complete count inventory")
        require(
            all(type(v) is int and v >= 0 for v in family["counts"].values()),
            "native nonnegative counts",
        )
    return {
        "families": families,
        "prior_bridges": historical_bridges(families, previous),
        "payload_sizes": payload_sizes(families),
        "totals": {
            "families": 2,
            **{key: sum(f["counts"][key] for f in families) for key in COUNT_FIELDS},
        },
        "scope": dict.fromkeys(SCOPE, False),
    }


def run_suite(route="compare"):
    require(route in ("compare", "primary", "reference"), "unknown route")
    problems, previous = load_inputs()
    names = ("primary", "reference") if route == "compare" else (route,)
    engines = [load_engine(name) for name in names]
    families = []
    for problem in problems:
        outputs = []
        for engine in engines:
            supplied = copy.deepcopy(problem)
            outputs.append(engine.build_family(supplied))
            verify_suite(supplied, problem)
        if len(outputs) == 2:
            verify_suite(outputs[0], outputs[1])
        families.append(outputs[0])
    suite = assemble_suite(families, previous)
    native(suite)
    canonical(suite)
    return suite


def capture(path=None, route="compare", verify=False):
    path = Path(RESULT if path is None else path)
    require(
        sys.flags.isolated and sys.pycache_prefix,
        "isolated Python/external bytecode cache required",
    )
    cache = Path(sys.pycache_prefix).resolve()
    require(
        cache != Path(cache.anchor) and not cache.is_relative_to(ROOT), "external bytecode cache"
    )
    if not verify and (path.exists() or path.is_symlink()):
        raise FileExistsError("evidence exists; never overwrite")
    before = identities()
    raw_before = plain_bytes(path) if verify else None
    if verify:
        existing = json.loads(raw_before)
        require(
            type(existing) is dict
            and set(existing)
            == {
                "schema_version",
                "source_ledger",
                "prior_artifacts",
                "ancestor_sources",
                "suite",
                "runtime",
            },
            "capture fields",
        )
        require(existing["schema_version"] == SCHEMA, "capture schema")
        require(canonical(existing) == raw_before, "noncanonical capture")
        for key, value in before.items():
            verify_suite(existing[key], value)
    start = time.perf_counter()
    suite = run_suite(route)
    native(suite)
    suite_raw = canonical(suite)
    seconds = time.perf_counter() - start
    verify_suite(before, identities())
    if verify:
        verify_suite(suite, existing["suite"])
        require(plain_bytes(path) == raw_before, "capture changed during replay")
        raw = raw_before
    else:
        report = {
            "schema_version": SCHEMA,
            **before,
            "suite": suite,
            "runtime": {
                "route": route,
                "python": sys.version,
                "platform": platform.platform(),
                "executable": sys.executable,
                "isolated": bool(sys.flags.isolated),
                "optimized": sys.flags.optimize,
                "bytecode_cache": str(cache),
                "suite_seconds": seconds,
                "rss_high_water_at_suite_end": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "rss_units": "bytes" if sys.platform == "darwin" else "KiB",
                "scope": "verification timing; excludes final serialization; not application benchmark",
            },
        }
        raw = canonical(report)
        require(len(raw) <= MAX_CAPTURE_BYTES, "capture byte cap")
        with path.open("xb") as stream:
            stream.write(raw)
        require(plain_bytes(path) == raw, "capture readback")
    verify_suite(before, identities())
    return {
        "status": "VERIFIED_EXACT_REPLAY" if verify else "CREATED_EXACT_FINITE_RESULT",
        "route": route,
        "path": str(path),
        "bytes": len(raw),
        "sha256": digest(raw),
        "suite_bytes": len(suite_raw),
        "suite_sha256": digest(suite_raw),
        "seconds": seconds,
        "totals": suite["totals"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--route", choices=("compare", "primary", "reference"), default="compare")
    parser.add_argument("--artifact", type=Path, default=RESULT)
    args = parser.parse_args()
    print(json.dumps(capture(args.artifact, args.route, args.verify)))


if __name__ == "__main__":
    main()
