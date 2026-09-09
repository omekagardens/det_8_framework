"""QR-05AX bounded bilinear field-error orchestration."""

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
SCHEMA = "det8-qr05ax-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05ax.py")
AW = HERE.parent / "qr-05aw-local-bank-errors-2026-09-08/results.json"
AW_ID = {
    "bytes": 1341549,
    "sha256": "e14e357309ff98f9f93c8f23c603f62d9bf17b01b4515ee122a464671b205916",
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
    "coordinate_entries",
    "baseline_entries",
    "map_entries",
    "gain_entries",
    "comparison_entries",
    "positivity_entries",
    "field_witnesses",
    "field_sign_entries",
    "field_witness_entries",
    "enclosure_witnesses",
    "enclosure_sign_entries",
    "enclosure_witness_entries",
    "constant_witnesses",
    "constant_witness_entries",
    "field_maximizers",
    "enclosure_maximizers",
    "field_enclosure_strict",
    "field_local_strict",
    "enclosure_local_strict",
    "receiver_strict",
    "nonnegative_rows",
    "nonpositive_rows",
    "mixed_rows",
    "zero_rows",
)
CHECK_FIELDS = (
    "geometry_partitions",
    "bank_label_identity",
    "coordinate_inverse",
    "moment_integrals",
    "moment_inverse",
    "local_box_containment",
    "frozen_bank_identity",
    "error_map_identity",
    "baseline_dominance",
    "normalization_domain",
    "field_bound",
    "field_pipeline",
    "field_attainment",
    "enclosure_box",
    "enclosure_attainment",
    "constant_fields",
    "coefficient_sign_partition",
    "complete_gain_partitions",
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
    "stochastic_independence_assumed",
    "total_source_nonnegativity_guaranteed",
    "global_field_continuity_required",
    "arbitrary_bounded_field_sharpness_claimed",
    "common_bank_feasibility_solved",
    "same_error_domain_as_AW_claimed",
    "equal_noise_sensor_improvement_claimed",
    "field_coordinate_dimension_reduced",
    "full_field_stability_tested",
    "minimality_recomputed",
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
    require(ident(AW) == AW_ID, "AW artifact changed")
    return json.loads(plain_bytes(AW))


def identities():
    previous = prior_document()
    prior = {str(AW.relative_to(HERE.parent)): AW_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AW.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def project_inputs(previous):
    require(type(previous) is list and len(previous) == 2, "AW family inventory")
    require(
        all(type(f) is dict and type(f.get("problem")) is dict for f in previous),
        "AW family problem records",
    )
    require([f["problem"].get("family") for f in previous] == list(FAMILIES), "AW family order")
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
        require(set(p) == fields, "selected AW problem fields")
        for key, length in (
            ("probe", 4),
            ("cells", 8),
            ("tiles", 12),
            ("bank_labels", 48),
            ("target_labels", 64),
        ):
            require(type(p[key]) is list and len(p[key]) == length, "selected AW inventory")
        for key, rows, width in (("interface", 37, 48), ("geometric", 64, 48), ("decoder", 64, 37)):
            require(
                type(p[key]) is list
                and len(p[key]) == rows
                and all(type(row) is list and len(row) == width for row in p[key]),
                "selected AW matrix inventory",
            )
        native(p)
        problems.append(copy.deepcopy(p))
    return problems, previous


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05ax_" + name, HERE / filename)
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
        "coordinates",
        "baseline",
        "maps",
        "field",
        "enclosure",
        "comparison",
        "positivity",
        "checks",
        "counts",
    }
    for f in families:
        require(type(f) is dict and set(f) == fields, "complete family fields")
        require(
            set(f["checks"]) == set(CHECK_FIELDS) and all(v is True for v in f["checks"].values()),
            "complete family checks",
        )
        p, g = f["problem"], f["geometry"]
        q, r, s, t = len(p["geometric"]), 4 * len(p["tiles"]), len(p["interface"]), len(p["tiles"])
        defined, undefined = g["defined_rows"], g["undefined_rows"]
        index_rows(defined, q)
        index_rows(undefined, q)
        require(sorted(defined + undefined) == list(range(q)), "normalization partition")
        require(len(g["target_scales"]) == q, "target scale inventory")
        for i, scale in enumerate(g["target_scales"]):
            require((scale == [0, 1]) == (i in undefined), "scale domain")
        for group, key, width in (
            ("maps", "normalized_target", r),
            ("maps", "enclosure_target", s),
            ("baseline", "normalized_target", r),
        ):
            rows = f[group][key]
            require(type(rows) is list and len(rows) == q, "normalized matrix inventory")
            for i, row in enumerate(rows):
                require(
                    row is None if i in undefined else type(row) is list and len(row) == width,
                    "normalized matrix domain/shape",
                )
        field_widths = {
            k: r
            for k in (
                "corners",
                "local_coefficients",
                "global_coefficients",
                "local_moments",
                "bank_error",
                "integrated_bank_error",
                "roundtrip_local",
                "roundtrip_corners",
            )
        }
        field_widths.update(
            {
                "tile_minima": t,
                "tile_maxima": t,
                "observed_error": s,
                "direct_error": q,
                "decoded_error": q,
                "normalized_error": q,
            }
        )
        enclosure_widths = {"observed_error": s, "decoded_error": q, "normalized_error": q}

        def endpoint(e, widths, attained, undefined=undefined, field_widths=field_widths):
            require(
                type(e) is dict
                and set(e) == set(widths).union({"attained"} if attained else set()),
                "complete endpoint",
            )
            for key, width in widths.items():
                require(type(e[key]) is list and len(e[key]) == width, "full endpoint vector")
            for j, value in enumerate(e["normalized_error"]):
                require((value is None) == (j in undefined), "endpoint normalized domain")
            if widths is field_widths:
                verify_suite(e["corners"], e["roundtrip_corners"])
                verify_suite(e["local_moments"], e["roundtrip_local"])
                verify_suite(e["bank_error"], e["integrated_bank_error"])
                verify_suite(e["direct_error"], e["decoded_error"])

        for group, sign_width, widths in (
            ("field", r, field_widths),
            ("enclosure", s, enclosure_widths),
        ):
            part = f[group]
            require(
                type(part["row_gains"]) is list
                and len(part["row_gains"]) == q
                and type(part["witnesses"]) is list
                and len(part["witnesses"]) == q,
                "all gain/witness rows",
            )
            index_rows(part["max_rows"], q, bool(defined))
            require(
                all(i in defined for i in part["max_rows"])
                and (part["max_gain"] is None) == (not defined),
                "maximum domain",
            )
            for i in part["max_rows"]:
                verify_suite(part["row_gains"][i], part["max_gain"])
            for i, row in enumerate(part["witnesses"]):
                require((part["row_gains"][i] is None) == (i in undefined), "gain domain")
                if i in undefined:
                    require(row is None, "undefined designated witness")
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
                    "canonical sign vector",
                )
                for direction in ("positive", "negative"):
                    e = row[direction]
                    endpoint(e, widths, True)
                    verify_suite(e["attained"], e["normalized_error"][i])
        require(
            f["enclosure"]["common_bank_feasibility_tested"] is False, "no enclosure preimage claim"
        )
        for group, key, width in (
            ("enclosure", "receiver_radii", s),
            ("baseline", "receiver_radii", s),
            ("baseline", "shared_gains", q),
            ("baseline", "enclosure_gains", q),
        ):
            require(
                type(f[group][key]) is list and len(f[group][key]) == width, "gain vector width"
            )
        for key in ("shared_gains", "enclosure_gains"):
            for i, value in enumerate(f["baseline"][key]):
                require((value is None) == (i in undefined), "baseline gain domain")
        require(
            set(f["comparison"])
            == {"field_vs_enclosure", "field_vs_local", "enclosure_vs_local", "receiver_reduction"},
            "complete gain comparisons",
        )
        for name, c in f["comparison"].items():
            receiver = name == "receiver_reduction"
            n = s if receiver else q
            domain = list(range(s)) if receiver else defined
            null = [] if receiver else undefined
            expected = {"gain_gap", "strict_rows", "tied_rows", "max_gap", "max_gap_rows"}
            if not receiver:
                expected.add("undefined_rows")
            require(type(c) is dict and set(c) == expected, "complete gain comparison")
            require(type(c["gain_gap"]) is list and len(c["gain_gap"]) == n, "all gain gaps")
            for i, value in enumerate(c["gain_gap"]):
                require((value is None) == (i in null), "comparison domain")
            if not receiver:
                verify_suite(c["undefined_rows"], undefined)
            for key in ("strict_rows", "tied_rows"):
                index_rows(c[key], n)
            require(
                sorted(c["strict_rows"] + c["tied_rows"] + null) == list(range(n)),
                "complete gain partition",
            )
            index_rows(c["max_gap_rows"], n, bool(domain))
            require(
                all(i in domain for i in c["max_gap_rows"])
                and (c["max_gap"] is None) == (not domain),
                "comparison maximum domain",
            )
            for i in c["max_gap_rows"]:
                verify_suite(c["gain_gap"][i], c["max_gap"])
        pos = f["positivity"]
        require(
            set(pos)
            == {
                "nonnegative_rows",
                "nonpositive_rows",
                "mixed_rows",
                "zero_rows",
                "constant_response",
                "positive_constant_attains",
                "negative_constant_attains",
                "constant_positive",
                "constant_negative",
            },
            "complete positivity fields",
        )
        for name in (
            "nonnegative_rows",
            "nonpositive_rows",
            "mixed_rows",
            "zero_rows",
            "positive_constant_attains",
            "negative_constant_attains",
        ):
            index_rows(pos[name], q)
            require(all(i in defined for i in pos[name]), "defined sign rows")
        nonneg, nonpos = set(pos["nonnegative_rows"]), set(pos["nonpositive_rows"])
        require(
            set(pos["zero_rows"]) == nonneg & nonpos
            and set(pos["mixed_rows"]) == set(defined) - (nonneg | nonpos),
            "sign partition",
        )
        require(
            pos["positive_constant_attains"] == pos["nonnegative_rows"]
            and pos["negative_constant_attains"] == pos["nonpositive_rows"],
            "constant sign attainment",
        )
        require(
            type(pos["constant_response"]) is list and len(pos["constant_response"]) == q,
            "all constant responses",
        )
        for i, value in enumerate(pos["constant_response"]):
            require((value is None) == (i in undefined), "constant response domain")
        for key in ("constant_positive", "constant_negative"):
            endpoint(pos[key], field_widths, False)
        verify_suite(pos["constant_positive"]["normalized_error"], pos["constant_response"])
    return dict.fromkeys(CHECK_FIELDS, True)


def historical_bridges(families, previous):
    expected, _ = project_inputs(previous)
    verify_suite([f["problem"] for f in families], expected)
    controls(families)
    for f, aw in zip(families, previous, strict=True):
        verify_suite(f["geometry"], aw["geometry"])
        for key in ("bank_scales", "raw_from_local", "local_from_raw"):
            verify_suite(f["coordinates"][key], aw["coordinates"][key])
        for key in ("interface_error", "target_error", "normalized_target"):
            verify_suite(f["baseline"][key], aw["maps"][key])
        verify_suite(f["baseline"]["receiver_radii"], aw["enclosure"]["receiver_radii"])
        verify_suite(f["baseline"]["shared_gains"], aw["shared"]["row_gains"])
        verify_suite(f["baseline"]["enclosure_gains"], aw["enclosure"]["row_gains"])
    return {
        "selected_families": list(FAMILIES),
        "AW_problem_equal": True,
        "AW_geometry_equal": True,
        "AW_coordinates_equal": True,
        "AW_local_baseline_equal": True,
        "same_response_maps": True,
        "new_field_error_domain": True,
        "AW_endpoints_replayed": False,
        "other_historical_mathematics_replayed": False,
        "older_executors_run": False,
    }


def payload_sizes(families):
    fields = {
        "input": "problem",
        "geometry": "geometry",
        "coordinate": "coordinates",
        "baseline": "baseline",
        "map": "maps",
        "field": "field",
        "enclosure": "enclosure",
        "comparison": "comparison",
        "positivity": "positivity",
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
