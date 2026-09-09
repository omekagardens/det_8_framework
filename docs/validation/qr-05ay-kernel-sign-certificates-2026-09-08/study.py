"""QR-05AY bounded kernel sign-certificate orchestration."""

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
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05ay-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05ay.py")
AX = HERE.parent / "qr-05ax-bilinear-field-errors-2026-09-08/results.json"
AX_ID = {
    "bytes": 1925803,
    "sha256": "80020730e21d2c5731b6f6d5a94add1faa6739c815ac3e82087126d45667f1b0",
}
MAX_CAPTURE_BYTES = 128 * 1024 * 1024
MAX_WORKING_BYTES = 192 * 1024 * 1024
FAMILIES = ("grid", "warp")
COUNT_FIELDS = (
    "cells",
    "positive_cells",
    "tiles",
    "bank_values",
    "receiver_values",
    "target_rows",
    "defined_rows",
    "undefined_rows",
    "geometry_input_entries",
    "input_matrix_entries",
    "geometry_entries",
    "kernel_entries",
    "map_entries",
    "bound_entries",
    "comparison_entries",
    "mixed_tiles",
    "mixed_rows",
    "certified_rows",
    "pointwise_nonnegative_rows",
    "pointwise_nonpositive_rows",
    "pointwise_zero_rows",
    "integrated_nonnegative_rows",
    "integrated_nonpositive_rows",
    "integrated_zero_rows",
    "integrated_nonnegative_mixed_rows",
    "tile_constant_witnesses",
    "bilinear_witnesses",
    "constant_witnesses",
    "tile_sign_entries",
    "bilinear_sign_entries",
    "endpoint_entries",
    "constant_endpoint_entries",
    "constant_gap_strict",
    "upper_gap_strict",
    "certified_upper_gap_strict",
    "constant_maximizers",
    "bilinear_maximizers",
    "upper_maximizers",
    "certified_maximizers",
)
CHECK_FIELDS = (
    "geometry_partitions",
    "bank_label_identity",
    "frozen_bank_identity",
    "kernel_corner_identity",
    "kernel_integrals",
    "bernstein_integrals",
    "corner_envelope",
    "normalization_domain",
    "bound_order",
    "sign_partition",
    "obstruction_inventory",
    "certified_exactness",
    "endpoint_field_bound",
    "endpoint_pipeline",
    "lower_attainment",
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
    "integrated_positivity_used_as_pointwise_certificate",
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
    require(ident(AX) == AX_ID, "AX artifact changed")
    return json.loads(plain_bytes(AX))


def identities():
    previous = prior_document()
    prior = {str(AX.relative_to(HERE.parent)): AX_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AX.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def project_inputs(previous):
    require(type(previous) is list and len(previous) == 2, "AX family inventory")
    require(
        all(type(f) is dict and type(f.get("problem")) is dict for f in previous),
        "AX family problem records",
    )
    require([f["problem"].get("family") for f in previous] == list(FAMILIES), "AX family order")
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
    problems = []
    for family in previous:
        p = family["problem"]
        require(set(p) == fields, "selected AX problem fields")
        for key, length in (
            ("probe", 4),
            ("cells", 8),
            ("tiles", 12),
            ("bank_labels", 48),
            ("target_labels", 64),
        ):
            require(type(p[key]) is list and len(p[key]) == length, "selected AX inventory")
        for key, rows, width in (("interface", 37, 48), ("geometric", 64, 48), ("decoder", 64, 37)):
            require(
                type(p[key]) is list
                and len(p[key]) == rows
                and all(type(row) is list and len(row) == width for row in p[key]),
                "selected AX matrix inventory",
            )
        native(p)
        problems.append(copy.deepcopy(p))
    return problems, previous


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05ay_" + name, HERE / filename)
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


def controls(families):
    require(type(families) is list and len(families) == 2, "complete fixed inventory")
    require([f["problem"]["family"] for f in families] == list(FAMILIES), "family order")
    fields = {
        "problem",
        "geometry",
        "kernels",
        "maps",
        "bounds",
        "certification",
        "witnesses",
        "comparison",
        "checks",
        "counts",
    }
    bound_keys = ("constant_lower", "bilinear_lower", "corner_upper", "certified_gain")
    for f in families:
        require(type(f) is dict and set(f) == fields, "complete family fields")
        require(
            set(f["checks"]) == set(CHECK_FIELDS) and all(v is True for v in f["checks"].values()),
            "complete checks",
        )
        p, g, k, cert, bounds = (
            f[key] for key in ("problem", "geometry", "kernels", "certification", "bounds")
        )
        q, t, s = len(p["geometric"]), len(p["tiles"]), len(p["interface"])
        r = 4 * t
        defined, undefined = g["defined_rows"], g["undefined_rows"]
        for rows in (defined, undefined):
            index_rows(rows, q)
        require(sorted(defined + undefined) == list(range(q)), "normalization partition")
        require(len(g["target_scales"]) == q, "target scales")
        for i, scale in enumerate(g["target_scales"]):
            require((scale == [0, 1]) == (i in undefined), "scale domain")
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
        require(
            sorted(certified + uncertain + undefined) == list(range(q)), "certificate partition"
        )
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
            set(bounds) == set(bound_keys) | {"maxima"}
            and set(bounds["maxima"]) == set(bound_keys),
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
                all(i in domain for i in maximum["rows"])
                and (maximum["gain"] is None) == (not domain),
                "maximum domain",
            )
            for i in maximum["rows"]:
                verify_suite(values[i], maximum["gain"])
        for i in certified:
            verify_suite(bounds["constant_lower"][i], bounds["bilinear_lower"][i])
            verify_suite(bounds["constant_lower"][i], bounds["certified_gain"][i])
        widths = dict.fromkeys(
            ("corners", "local_coefficients", "global_coefficients", "local_moments", "bank_error"),
            r,
        )
        widths.update(
            {
                "tile_minima": t,
                "tile_maxima": t,
                "observed_error": s,
                "direct_error": q,
                "decoded_error": q,
                "normalized_error": q,
            }
        )

        def endpoint(e, attained, widths=widths, undefined=undefined):
            require(
                type(e) is dict and set(e) == set(widths) | ({"attained"} if attained else set()),
                "complete endpoint",
            )
            for key, width in widths.items():
                require(type(e[key]) is list and len(e[key]) == width, "endpoint vector")
            for j, value in enumerate(e["normalized_error"]):
                require((value is None) == (j in undefined), "endpoint null domain")
            verify_suite(e["direct_error"], e["decoded_error"])

        require(
            set(f["witnesses"])
            == {"tile_constant", "bilinear", "constant_positive", "constant_negative"},
            "complete witness groups",
        )
        for group, sign_width, gain_key in (
            ("tile_constant", t, "constant_lower"),
            ("bilinear", r, "bilinear_lower"),
        ):
            rows = f["witnesses"][group]
            require(type(rows) is list and len(rows) == q, "all designated witness rows")
            for i, row in enumerate(rows):
                if i in undefined:
                    require(row is None, "undefined witness")
                    continue
                require(
                    type(row) is dict
                    and set(row) == {"target_row", "signs", "positive", "negative"},
                    "complete signed witness",
                )
                require(
                    type(row["target_row"]) is int and row["target_row"] == i,
                    "original target indexing",
                )
                signs = row["signs"]
                require(
                    type(signs) is list
                    and len(signs) == sign_width
                    and all(type(x) is int and x in (-1, 0, 1) for x in signs),
                    "canonical signs",
                )
                for side, direction in (("positive", 1), ("negative", -1)):
                    e = row[side]
                    endpoint(e, True)
                    verify_suite(e["attained"], e["normalized_error"][i])
                    gain = bounds[gain_key][i]
                    verify_suite(e["attained"], [direction * gain[0], gain[1]])
                    expected_corners = [
                        v
                        for sign in signs
                        for v in [[direction * sign, 1]] * (4 if group == "tile_constant" else 1)
                    ]
                    verify_suite(e["corners"], expected_corners)
        for side, direction in (("constant_positive", 1), ("constant_negative", -1)):
            endpoint(f["witnesses"][side], False)
            verify_suite(f["witnesses"][side]["corners"], [[direction, 1] for _ in range(r)])
        require(
            set(f["comparison"])
            == {"bilinear_minus_constant", "upper_minus_bilinear", "upper_minus_certified"},
            "comparison inventory",
        )
        for name, c in f["comparison"].items():
            domain = certified if name == "upper_minus_certified" else defined
            unavailable = [i for i in range(q) if i not in domain]
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
            verify_suite(c["unavailable_rows"], unavailable)
            require(type(c["gain_gap"]) is list and len(c["gain_gap"]) == q, "all gaps")
            for i, value in enumerate(c["gain_gap"]):
                require((value is None) == (i in unavailable), "gap domain")
            for key in ("strict_rows", "tied_rows", "max_gap_rows"):
                index_rows(c[key], q)
            require(
                sorted(c["strict_rows"] + c["tied_rows"] + unavailable) == list(range(q)),
                "comparison partition",
            )
            require(
                bool(c["max_gap_rows"]) == bool(domain)
                and (c["max_gap"] is None) == (not domain)
                and all(i in domain for i in c["max_gap_rows"]),
                "gap maximum domain",
            )
            for i in c["max_gap_rows"]:
                verify_suite(c["gain_gap"][i], c["max_gap"])
    return dict.fromkeys(CHECK_FIELDS, True)


def historical_bridges(families, previous):
    expected, _ = project_inputs(previous)
    verify_suite([f["problem"] for f in families], expected)
    controls(families)
    for f, ax in zip(families, previous, strict=True):
        verify_suite(f["geometry"], ax["geometry"])
        verify_suite(f["maps"]["raw_bilinear_target"], ax["maps"]["target_error"])
        verify_suite(f["maps"]["normalized_bilinear_target"], ax["maps"]["normalized_target"])
        verify_suite(f["bounds"]["bilinear_lower"], ax["field"]["row_gains"])
        verify_suite(
            f["witnesses"]["constant_positive"]["normalized_error"],
            ax["positivity"]["constant_response"],
        )
    return {
        "selected_families": list(FAMILIES),
        "AX_problem_equal": True,
        "AX_geometry_equal": True,
        "AX_bilinear_map_equal": True,
        "AX_bilinear_gain_equal": True,
        "AX_constant_response_equal": True,
        "same_response_maps": True,
        "broader_field_error_domain": True,
        "AX_endpoints_replayed": False,
        "other_historical_mathematics_replayed": False,
        "older_executors_run": False,
    }


def payload_sizes(families):
    fields = {
        "input": "problem",
        "geometry": "geometry",
        "kernel": "kernels",
        "map": "maps",
        "bound": "bounds",
        "certification": "certification",
        "witness": "witnesses",
        "comparison": "comparison",
    }
    return [
        {
            "family": f["problem"]["family"],
            **{name + "_bytes": len(canonical(f[key])) for name, key in fields.items()},
            "native_family_bytes": len(canonical(f)),
        }
        for f in families
    ]


def assemble_suite(families, previous):
    expected, consumed = load_inputs()
    verify_suite(previous, consumed)
    verify_suite([f["problem"] for f in families], expected)
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
