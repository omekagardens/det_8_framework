"""QR-05AZ bounded-field refinement-stability orchestration."""

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
SCHEMA = "det8-qr05az-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05az.py")
AY = HERE.parent / "qr-05ay-kernel-sign-certificates-2026-09-08/results.json"
AY_ID = {
    "bytes": 2115070,
    "sha256": "a4dda392b4dd8f148389cb82c4187611c10b11e3f3e05f82e2779fbe3bf90874",
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
    "input_geometry_entries",
    "input_matrix_entries",
    "child_problem_geometry_entries",
    "child_problem_matrix_entries",
    "geometry_entries",
    "restriction_entries",
    "parent_kernel_entries",
    "child_kernel_entries",
    "parent_map_entries",
    "child_map_entries",
    "bound_entries",
    "certification_bridge_entries",
    "transport_entries",
    "comparison_entries",
    "parent_paired_witnesses",
    "child_witnesses",
    "sign_entries",
    "witness_entries",
    "constant_strict",
    "bilinear_strict",
    "upper_strict",
    "inherited_rows",
    "newly_certified_rows",
    "still_uncertified_rows",
)
CHECK_FIELDS = (
    "parent_geometry",
    "child_partition",
    "lineage_identity",
    "frozen_bank_identity",
    "restriction_convexity",
    "raw_moment_additivity",
    "kernel_restriction",
    "kernel_integral_additivity",
    "bernstein_transport",
    "response_transport",
    "normalization_domain",
    "bound_monotonicity",
    "certification_inheritance",
    "parent_field_pipelines",
    "child_extremizer_pipelines",
    "constant_controls",
    "complete_comparisons",
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
    "total_source_nonnegativity_guaranteed",
    "global_field_continuity_required",
    "mixed_absolute_kernel_integrated",
    "uncertified_exact_gain_claimed",
    "corner_envelope_sharpness_claimed",
    "independent_child_fields_called_parent_fields",
    "full_bounded_field_domain_changed",
    "equal_noise_sensor_improvement_claimed",
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
    require(ident(AY) == AY_ID, "AY artifact changed")
    return json.loads(plain_bytes(AY))


def identities():
    previous = prior_document()
    prior = {str(AY.relative_to(HERE.parent)): AY_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AY.parent / name).relative_to(HERE.parent))] = want
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
    require(type(previous) is list and len(previous) == 2, "AY family inventory")
    require(
        all(type(f) is dict and type(f.get("problem")) is dict for f in previous),
        "AY family problem records",
    )
    require([f["problem"].get("family") for f in previous] == list(FAMILIES), "AY family order")
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
        p = family["problem"]
        require(set(p) == fields, "selected AY problem fields")
        for key, length in (
            ("probe", 4),
            ("cells", 8),
            ("tiles", 12),
            ("bank_labels", 48),
            ("target_labels", 64),
        ):
            require(type(p[key]) is list and len(p[key]) == length, "selected AY inventory")
        for key, rows, width in (("interface", 37, 48), ("geometric", 64, 48), ("decoder", 64, 37)):
            require(
                type(p[key]) is list
                and len(p[key]) == rows
                and all(type(row) is list and len(row) == width for row in p[key]),
                "selected AY matrix inventory",
            )
        native(p)
        for tile in p["tiles"]:
            require(
                type(tile) is dict
                and set(tile) == {"event", "bounds"}
                and type(tile["bounds"]) is list
                and len(tile["bounds"]) == 4,
                "selected AY tile shape",
            )
        children = []
        for j, tile in enumerate(p["tiles"]):
            u0, u1, v0, v1 = map(rational, tile["bounds"])
            require(u0 < u1 and v0 < v1, "positive selected AY tile")
            um, vm = (u0 + u1) / 2, (v0 + v1) / 2
            for box in ((u0, um, v0, vm), (um, u1, v0, vm), (u0, um, vm, v1), (um, u1, vm, v1)):
                children.append({"parent": j, "bounds": list(map(fw, box))})
        supplied = {"parent": copy.deepcopy(p), "children": children}
        native(supplied)
        inputs.append(supplied)
    return inputs, previous


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05az_" + name, HERE / filename)
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


def pipeline_check(e, t, s, q, undefined):
    widths = {
        "corners": 4 * t,
        "global_coefficients": 4 * t,
        "bank_error": 4 * t,
        "observed_error": s,
        "direct_error": q,
        "decoded_error": q,
        "normalized_error": q,
        "tile_minima": t,
        "tile_maxima": t,
    }
    require(type(e) is dict and set(e) == set(widths), "pipeline fields")
    for key, width in widths.items():
        vector_check(e[key], width, undefined if key == "normalized_error" else ())
    verify_suite(e["direct_error"], e["decoded_error"])
    require(all(abs(rational(v)) <= 1 for v in e["corners"]), "bounded pipeline corners")


def pair_check(pair, p, m, s, q, undefined):
    require(
        type(pair) is dict
        and set(pair)
        == {
            "parent",
            "child",
            "aggregated_bank_error",
            "bank_residual",
            "observed_residual",
            "direct_residual",
            "decoded_residual",
            "normalized_residual",
            "field_coefficient_residual",
        },
        "parent-child pair fields",
    )
    pipeline_check(pair["parent"], p, s, q, undefined)
    pipeline_check(pair["child"], m, s, q, undefined)
    widths = {
        "aggregated_bank_error": 4 * p,
        "bank_residual": 4 * p,
        "observed_residual": s,
        "direct_residual": q,
        "decoded_residual": q,
        "normalized_residual": q,
        "field_coefficient_residual": 4 * m,
    }
    for key, width in widths.items():
        vector_check(pair[key], width, undefined if key == "normalized_residual" else ())
        if key != "aggregated_bank_error":
            require(all(v is None or v == [0, 1] for v in pair[key]), "field-pair residual")
    verify_suite(pair["aggregated_bank_error"], pair["parent"]["bank_error"])
    for key in ("observed_error", "direct_error", "decoded_error", "normalized_error"):
        verify_suite(pair["parent"][key], pair["child"][key])


def count_check(f):
    problem, child, g = f["input"]["parent"], f["child_problem"], f["geometry"]
    n, a = len(problem["cells"]), sum(c["bounds"] is not None for c in problem["cells"])
    p, m, q, s = (
        len(problem["tiles"]),
        len(child["tiles"]),
        len(problem["geometric"]),
        len(problem["interface"]),
    )
    rp, rc, d = 4 * p, 4 * m, len(g["defined_rows"])
    zp, zc = (
        len(f["levels"][name]["certification"]["certified_rows"]) for name in ("parent", "child")
    )
    ep, ec = 3 * rp + s + 2 * q + d + 2 * p, 3 * rc + s + 2 * q + d + 2 * m
    paired, child_witnesses = (8, 4) if d else (4, 0)
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
        "input_geometry_entries": 4 + 4 * a + 4 * p + 4 * m,
        "input_matrix_entries": s * rp + q * rp + q * s,
        "child_problem_geometry_entries": 4 + 4 * a + 4 * m,
        "child_problem_matrix_entries": s * rc + q * rc + q * s,
        "geometry_entries": 1 + n + q + p + m,
        "restriction_entries": 38 * m + 48 * p,
        "parent_kernel_entries": 12 * q * p,
        "child_kernel_entries": 12 * q * m,
        "parent_map_entries": (3 * q + d) * rp,
        "child_map_entries": (3 * q + d) * rc,
        "bound_entries": sum(3 * d + z + (3 if d else 0) + (1 if z else 0) for z in (zp, zc)),
        "certification_bridge_entries": zp,
        "transport_entries": 2 * q * p + 4 * q * rp + 2 * d * rp,
        "comparison_entries": 3 * d + (3 if d else 0),
        "parent_paired_witnesses": paired,
        "child_witnesses": child_witnesses,
        "sign_entries": p + rp + m + rc if d else 0,
        "witness_entries": paired * (ep + ec + 2 * rp + s + 2 * q + d + rc) + child_witnesses * ec,
        "constant_strict": len(f["comparison"]["constant_increase"]["strict_rows"]),
        "bilinear_strict": len(f["comparison"]["bilinear_increase"]["strict_rows"]),
        "upper_strict": len(f["comparison"]["upper_decrease"]["strict_rows"]),
        "inherited_rows": zp,
        "newly_certified_rows": len(f["certification_bridge"]["newly_certified_rows"]),
        "still_uncertified_rows": len(f["certification_bridge"]["still_uncertified_rows"]),
    }
    require(set(expected) == set(COUNT_FIELDS), "internal count inventory")
    verify_suite(f["counts"], expected)


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
    require(type(families) is list and len(families) == 2, "complete fixed inventory")
    fields = {
        "input",
        "child_problem",
        "geometry",
        "restriction",
        "levels",
        "transport",
        "comparison",
        "certification_bridge",
        "witnesses",
        "checks",
        "counts",
    }
    for f in families:
        native(f)
        require(type(f) is dict and set(f) == fields, "complete family fields")
        require(
            set(f["checks"]) == set(CHECK_FIELDS) and all(v is True for v in f["checks"].values()),
            "complete checks",
        )
        require(
            type(f["input"]) is dict and set(f["input"]) == {"parent", "children"}, "input fields"
        )
        problem, children = f["input"]["parent"], f["input"]["children"]
        cp, g = f["child_problem"], f["geometry"]
        p, m, s, q = (
            len(problem["tiles"]),
            len(children),
            len(problem["interface"]),
            len(problem["geometric"]),
        )
        rp = 4 * p
        require(set(cp) == set(problem), "child problem fields")
        for key in ("family", "probe", "cells", "target_labels", "decoder"):
            verify_suite(cp[key], problem[key])
        lineage = [child["parent"] for child in children]
        require(all(type(j) is int and 0 <= j < p for j in lineage), "native parent lineage")
        verify_suite(
            cp["tiles"],
            [
                {"event": problem["tiles"][item["parent"]]["event"], "bounds": item["bounds"]}
                for item in children
            ],
        )
        verify_suite(
            cp["bank_labels"], [{"tile": t, "basis": a} for t in range(m) for a in range(4)]
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
        for rows in (defined, undefined):
            index_rows(rows, q)
        require(sorted(defined + undefined) == list(range(q)), "normalization partition")
        require(rational(g["volume"]) > 0, "positive probe volume")
        vector_check(g["cell_volumes"], len(problem["cells"]))
        vector_check(g["target_scales"], q)
        vector_check(g["parent_tile_volumes"], p)
        vector_check(g["child_tile_volumes"], m)
        verify_suite(g["child_parents"], lineage)
        for i, scale in enumerate(g["target_scales"]):
            require((scale == [0, 1]) == (i in undefined), "scale domain")
        restriction = f["restriction"]
        require(
            set(restriction)
            == {
                "blocks",
                "parent_moment_blocks",
                "child_moment_blocks",
                "aggregated_moment_blocks",
                "moment_residuals",
                "row_sums",
                "min_weights",
                "max_weights",
            },
            "restriction fields",
        )
        for key, size in (
            ("blocks", m),
            ("parent_moment_blocks", p),
            ("child_moment_blocks", m),
            ("aggregated_moment_blocks", p),
            ("moment_residuals", p),
        ):
            block_check(restriction[key], size, key == "moment_residuals")
        verify_suite(restriction["aggregated_moment_blocks"], restriction["parent_moment_blocks"])
        matrix_check(restriction["row_sums"], m, 4)
        vector_check(restriction["min_weights"], m)
        vector_check(restriction["max_weights"], m)
        for j, block in enumerate(restriction["blocks"]):
            values = [rational(x) for row in block for x in row]
            require(all(0 <= x <= 1 for x in values), "restriction weights")
            require(
                all(sum(map(rational, row)) == 1 for row in block), "restriction row stochasticity"
            )
            verify_suite(restriction["row_sums"][j], [[1, 1]] * 4)
            verify_suite(restriction["min_weights"][j], fw(min(values)))
            verify_suite(restriction["max_weights"][j], fw(max(values)))
        require(set(f["levels"]) == {"parent", "child"}, "two levels")
        for name, t in (("parent", p), ("child", m)):
            level = f["levels"][name]
            level_controls(level, q, t, defined, undefined)
            verify_suite(
                level["maps"]["decoder_bank"],
                (problem if name == "parent" else cp)["geometric"],
            )
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
                    "level bound order",
                )
        transport = f["transport"]
        transport_widths = {
            "aggregate_kernel_integrals": p,
            "aggregate_bernstein_integrals": rp,
            "kernel_integral_residuals": p,
            "bernstein_residuals": rp,
            "restricted_raw_target": rp,
            "raw_target_residuals": rp,
            "restricted_normalized_target": rp,
            "normalized_target_residuals": rp,
        }
        require(set(transport) == set(transport_widths), "transport fields")
        for key, width in transport_widths.items():
            matrix_check(
                transport[key],
                q,
                width,
                undefined if "normalized" in key else (),
                key.endswith("residuals"),
            )
        parent = f["levels"]["parent"]
        for name, source in (
            ("aggregate_kernel_integrals", parent["kernels"]["tile_integrals"]),
            ("aggregate_bernstein_integrals", parent["kernels"]["bernstein_integrals"]),
            ("restricted_raw_target", parent["maps"]["raw_bilinear_target"]),
            ("restricted_normalized_target", parent["maps"]["normalized_bilinear_target"]),
        ):
            verify_suite(transport[name], source)
        bridge = f["certification_bridge"]
        require(
            set(bridge)
            == {
                "inherited_rows",
                "newly_certified_rows",
                "still_uncertified_rows",
                "undefined_rows",
                "inherited_gain_residuals",
            },
            "certificate bridge fields",
        )
        inherited = parent["certification"]["certified_rows"]
        child_cert = f["levels"]["child"]["certification"]
        require(set(inherited) <= set(child_cert["certified_rows"]), "certificate lost")
        verify_suite(bridge["inherited_rows"], inherited)
        verify_suite(
            bridge["newly_certified_rows"],
            [i for i in child_cert["certified_rows"] if i not in inherited],
        )
        verify_suite(bridge["still_uncertified_rows"], child_cert["uncertified_rows"])
        verify_suite(bridge["undefined_rows"], undefined)
        verify_suite(
            bridge["inherited_gain_residuals"],
            [[0, 1] if i in inherited else None for i in range(q)],
        )
        for i in inherited:
            verify_suite(
                parent["bounds"]["certified_gain"][i],
                f["levels"]["child"]["bounds"]["certified_gain"][i],
            )
        comparison = f["comparison"]
        require(
            set(comparison) == {"constant_increase", "bilinear_increase", "upper_decrease"},
            "comparisons",
        )
        for name, key, sign in (
            ("constant_increase", "constant_lower", 1),
            ("bilinear_increase", "bilinear_lower", 1),
            ("upper_decrease", "corner_upper", -1),
        ):
            c = comparison[name]
            require(
                set(c)
                == {
                    "gain_gap",
                    "strict_rows",
                    "tied_rows",
                    "unavailable_rows",
                    "max_gap",
                    "max_gap_rows",
                },
                "comparison fields",
            )
            gaps = [
                None
                if i in undefined
                else sign
                * (
                    rational(f["levels"]["child"]["bounds"][key][i])
                    - rational(parent["bounds"][key][i])
                )
                for i in range(q)
            ]
            require(all(gaps[i] >= 0 for i in defined), "refinement bound order")
            verify_suite(c["gain_gap"], [None if v is None else fw(v) for v in gaps])
            verify_suite(c["strict_rows"], [i for i in defined if gaps[i] > 0])
            verify_suite(c["tied_rows"], [i for i in defined if gaps[i] == 0])
            verify_suite(c["unavailable_rows"], undefined)
            maximum_check(c["gain_gap"], defined, {"gain": c["max_gap"], "rows": c["max_gap_rows"]})
        witnesses = f["witnesses"]
        require(
            set(witnesses)
            == {
                "parent_pattern",
                "parent_constant",
                "parent_constant_maximizer",
                "parent_bilinear_maximizer",
                "child_constant_maximizer",
                "child_bilinear_maximizer",
            },
            "witness groups",
        )
        for name in ("parent_pattern", "parent_constant"):
            group = witnesses[name]
            require(set(group) == {"positive", "negative"}, "control pair group")
            base = (
                [[-1, 1], [0, 1], [1, 1], [1, 2]] * p if name == "parent_pattern" else [[1, 1]] * rp
            )
            for side, direction in (("positive", 1), ("negative", -1)):
                pair_check(group[side], p, m, s, q, undefined)
                verify_suite(
                    group[side]["parent"]["corners"], [[direction * n, den] for n, den in base]
                )
        for level_name, t in (("parent", p), ("child", m)):
            level = f["levels"][level_name]
            for kind, key in (("constant", "constant_lower"), ("bilinear", "bilinear_lower")):
                group = witnesses[level_name + "_" + kind + "_maximizer"]
                if not defined:
                    require(group is None, "all-undefined maximum group")
                    continue
                require(
                    set(group) == {"target_row", "signs", "positive", "negative"},
                    "maximum witness group",
                )
                row = level["bounds"]["maxima"][key]["rows"][0]
                require(
                    type(group["target_row"]) is int and group["target_row"] == row,
                    "first maximizing row",
                )
                values = (
                    level["kernels"]["tile_integrals"][row]
                    if kind == "constant"
                    else level["maps"]["normalized_bilinear_target"][row]
                )
                signs = [(x[0] > 0) - (x[0] < 0) for x in values]
                verify_suite(group["signs"], signs)
                for side, direction in (("positive", 1), ("negative", -1)):
                    e = group[side]
                    if level_name == "parent":
                        pair_check(e, p, m, s, q, undefined)
                        e = e["parent"]
                    else:
                        pipeline_check(e, t, s, q, undefined)
                    corners = [
                        [direction * x, 1]
                        for x in signs
                        for _ in range(4 if kind == "constant" else 1)
                    ]
                    verify_suite(e["corners"], corners)
                    gain = level["bounds"][key][row]
                    verify_suite(e["normalized_error"][row], [direction * gain[0], gain[1]])
        count_check(f)
    require([f["input"]["parent"]["family"] for f in families] == list(FAMILIES), "family order")
    return dict.fromkeys(CHECK_FIELDS, True)


def historical_bridges(families, previous):
    expected, _ = project_inputs(previous)
    verify_suite([f["input"] for f in families], expected)
    controls(families)
    for f, ay in zip(families, previous, strict=True):
        g = f["geometry"]
        parent_geometry = {
            key: g[key]
            for key in ("volume", "cell_volumes", "target_scales", "defined_rows", "undefined_rows")
        }
        parent_geometry["tile_volumes"] = g["parent_tile_volumes"]
        verify_suite(parent_geometry, ay["geometry"])
        for key in ("kernels", "maps", "bounds", "certification"):
            verify_suite(f["levels"]["parent"][key], ay[key])
    return {
        "selected_families": list(FAMILIES),
        "AY_problem_equal": True,
        "AY_geometry_equal": True,
        "AY_kernels_equal": True,
        "AY_maps_equal": True,
        "AY_bounds_equal": True,
        "AY_certification_equal": True,
        "same_physical_kernel": True,
        "same_receiver_observations": True,
        "same_bounded_field_domain": True,
        "AY_endpoints_replayed": False,
        "other_historical_mathematics_replayed": False,
        "older_executors_run": False,
    }


def payload_sizes(families):
    fields = {
        "input": "input",
        "child_problem": "child_problem",
        "geometry": "geometry",
        "restriction": "restriction",
        "level": "levels",
        "transport": "transport",
        "comparison": "comparison",
        "certification_bridge": "certification_bridge",
        "witness": "witnesses",
    }
    return [
        {
            "family": f["input"]["parent"]["family"],
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
