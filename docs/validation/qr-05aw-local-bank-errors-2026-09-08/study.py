"""QR-05AW local bank error orchestration."""

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
SCHEMA = "det8-qr05aw-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05aw.py")
AV = HERE.parent / "qr-05av-shared-bank-errors-2026-09-08/results.json"
AV_ID = {
    "bytes": 1265211,
    "sha256": "db498dfae4d1659f0fe35eef72efc916c6d9c8fedbd375830145e78a680c4ef5",
}
AR = HERE.parent / "qr-05ar-fine-response-sufficiency-2026-09-08/results.json"
AR_ID = {
    "bytes": 704842,
    "sha256": "c9ed0e299c057eb6503238a3bc5ce18352abe81bc111615464afaa6ed264e4f8",
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
    "map_entries",
    "gain_entries",
    "shared_witnesses",
    "shared_sign_entries",
    "shared_witness_entries",
    "enclosure_witnesses",
    "enclosure_sign_entries",
    "enclosure_witness_entries",
    "shared_maximizers",
    "enclosure_maximizers",
    "gap_maximizers",
    "strict_rows",
    "tied_rows",
)
CHECK_FIELDS = (
    "geometry_partitions",
    "bank_label_identity",
    "coordinate_inverse",
    "frozen_bank_identity",
    "error_map_identity",
    "normalization_domain",
    "primitive_box",
    "shared_pipeline",
    "shared_attainment",
    "enclosure_box",
    "enclosure_attainment",
    "complete_gain_partition",
)
SCOPE = (
    "source_dictionary_changed",
    "source_or_target_integrals_recomputed",
    "repair_overlay_regenerated",
    "decoder_refitted",
    "filters_reselected",
    "measurements_added",
    "normalization_row_added",
    "empirical_noise_calibrated",
    "stochastic_independence_assumed",
    "field_realizable_errors_required",
    "common_bank_feasibility_solved",
    "same_error_domain_as_AV_claimed",
    "equal_noise_sensor_improvement_claimed",
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
    require(ident(AV) == AV_ID, "AV artifact changed")
    return json.loads(plain_bytes(AV))


def geometry_document():
    require(ident(AR) == AR_ID, "AR artifact changed")
    return json.loads(plain_bytes(AR))


def identities():
    previous = prior_document()
    require(
        previous["prior_artifacts"].get(str(AR.relative_to(HERE.parent))) == AR_ID,
        "AR selected ancestry pin",
    )
    prior = {str(AV.relative_to(HERE.parent)): AV_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AV.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def project_inputs(previous):
    require(type(previous) is dict and set(previous) == {"AV", "AR"}, "selected producer keys")
    for name in ("AV", "AR"):
        rows = previous[name]
        require(type(rows) is list and len(rows) == 2, name + " family inventory")
        require([f["problem"]["family"] for f in rows] == list(FAMILIES), name + " family order")
    problems = []
    for av, ar in zip(previous["AV"], previous["AR"], strict=True):
        old = av["problem"]
        verify_suite(old["geometric"], ar["repair"]["matrix"])
        verify_suite(old["target_labels"], ar["matrices"]["fine_response_rows"])
        tiles = ar["geometry"]["repair_tiles"]
        require(type(tiles) is list and len(tiles) == 12, "AR repair tile inventory")
        p = {
            "family": old["family"],
            "probe": ar["problem"]["probe"],
            "cells": ar["problem"]["fine_cells"],
            "tiles": [{"event": t["event"], "bounds": t["bounds"]} for t in tiles],
            "bank_labels": ar["matrices"]["repair_observation_rows"],
            "target_labels": old["target_labels"],
            "interface": old["interface"],
            "geometric": old["geometric"],
            "decoder": old["decoder"],
        }
        for key, length in (("probe", 4), ("cells", 8), ("bank_labels", 48), ("target_labels", 64)):
            require(type(p[key]) is list and len(p[key]) == length, "selected inventory")
        for key, rows, width in (("interface", 37, 48), ("geometric", 64, 48), ("decoder", 64, 37)):
            require(
                type(p[key]) is list
                and len(p[key]) == rows
                and all(type(row) is list and len(row) == width for row in p[key]),
                "selected matrix inventory",
            )
        problems.append(copy.deepcopy(p))
    return problems, previous


def load_inputs():
    return project_inputs(
        {
            "AV": prior_document()["suite"]["families"],
            "AR": geometry_document()["suite"]["families"],
        }
    )


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05aw_" + name, HERE / filename)
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
    for family in families:
        require(set(family["checks"]) == set(CHECK_FIELDS), "complete check fields")
        require(all(v is True for v in family["checks"].values()), "family check failed")
        problem, geometry = family["problem"], family["geometry"]
        q, r, s = len(problem["geometric"]), 4 * len(problem["tiles"]), len(problem["interface"])
        defined, undefined = geometry["defined_rows"], geometry["undefined_rows"]
        index_rows(defined, q)
        index_rows(undefined, q)
        require(sorted(defined + undefined) == list(range(q)), "normalization partition")
        require(len(geometry["target_scales"]) == q, "all target scales")
        for i, scale in enumerate(geometry["target_scales"]):
            require((scale == [0, 1]) == (i in undefined), "zero scale domain")
        require(
            family["enclosure"]["common_bank_feasibility_tested"] is False,
            "no enclosure preimage claim",
        )
        for name, width in (("normalized_target", r), ("enclosure_target", s)):
            rows = family["maps"][name]
            require(type(rows) is list and len(rows) == q, "all normalized map rows")
            for i, row in enumerate(rows):
                if i in undefined:
                    require(row is None, "undefined normalized map")
                else:
                    require(type(row) is list and len(row) == width, "defined normalized map")
        for name, sign_width in (("shared", r), ("enclosure", s)):
            result = family[name]
            gains, witnesses = result["row_gains"], result["witnesses"]
            require(
                type(gains) is list
                and len(gains) == q
                and type(witnesses) is list
                and len(witnesses) == q,
                "all target results",
            )
            index_rows(result["max_rows"], q, bool(defined))
            require(all(i in defined for i in result["max_rows"]), "defined maximizers only")
            require((result["max_gain"] is None) == (not defined), "maximum domain")
            for i in result["max_rows"]:
                verify_suite(gains[i], result["max_gain"])
            for i, row in enumerate(witnesses):
                require((gains[i] is None) == (i in undefined), "undefined gain domain")
                if i in undefined:
                    require(row is None, "undefined designated witness")
                    continue
                require(
                    type(row) is dict
                    and set(row) == {"target_row", "signs", "positive", "negative"},
                    "complete witness fields",
                )
                require(
                    type(row["target_row"]) is int and row["target_row"] == i,
                    "original witness target indexing",
                )
                signs = row["signs"]
                require(
                    type(signs) is list
                    and len(signs) == sign_width
                    and all(type(v) is int and v in (-1, 0, 1) for v in signs),
                    "native canonical signs",
                )
                widths = {"observed_error": s, "decoded_error": q, "normalized_error": q}
                if name == "shared":
                    widths.update(
                        {
                            "primitive": r,
                            "bank_error": r,
                            "roundtrip_primitive": r,
                            "direct_error": q,
                        }
                    )
                for direction in ("positive", "negative"):
                    endpoint = row[direction]
                    require(
                        type(endpoint) is dict and set(endpoint) == {*widths, "attained"},
                        "complete endpoint fields",
                    )
                    for key, width in widths.items():
                        require(
                            type(endpoint[key]) is list and len(endpoint[key]) == width,
                            "full endpoint vector",
                        )
                    for j, value in enumerate(endpoint["normalized_error"]):
                        require(
                            (value is None) == (j in undefined), "endpoint normalization domain"
                        )
                    verify_suite(endpoint["attained"], endpoint["normalized_error"][i])
                    if name == "shared":
                        verify_suite(endpoint["primitive"], endpoint["roundtrip_primitive"])
                        verify_suite(endpoint["direct_error"], endpoint["decoded_error"])
        require(
            type(family["enclosure"]["receiver_radii"]) is list
            and len(family["enclosure"]["receiver_radii"]) == s,
            "all receiver radii",
        )
        comparison = family["comparison"]
        verify_suite(comparison["undefined_rows"], undefined)
        require(
            type(comparison["gain_gap"]) is list and len(comparison["gain_gap"]) == q,
            "all gain gaps",
        )
        for i, value in enumerate(comparison["gain_gap"]):
            require((value is None) == (i in undefined), "gap domain")
        for name in ("strict_rows", "tied_rows"):
            index_rows(comparison[name], q)
        require(
            sorted(comparison["strict_rows"] + comparison["tied_rows"] + undefined)
            == list(range(q)),
            "complete disjoint gain partition",
        )
        index_rows(comparison["max_gap_rows"], q, bool(defined))
        require(all(i in defined for i in comparison["max_gap_rows"]), "defined gap maximizers")
        require((comparison["max_gap"] is None) == (not defined), "maximum gap domain")
        for i in comparison["max_gap_rows"]:
            verify_suite(comparison["gain_gap"][i], comparison["max_gap"])
    return dict.fromkeys(CHECK_FIELDS, True)


def historical_bridges(families, previous):
    expected, _ = project_inputs(previous)
    verify_suite([f["problem"] for f in families], expected)
    controls(families)
    return {
        "selected_families": list(FAMILIES),
        "AV_frozen_maps_equal": True,
        "AR_selected_geometry_equal": True,
        "AR_bank_target_labels_equal": True,
        "AR_geometric_map_equal": True,
        "local_error_domain_is_new": True,
        "selected_partitions_rechecked": True,
        "frozen_bank_identity_rechecked": True,
        "old_raw_error_analysis_replayed": False,
        "other_historical_mathematics_replayed": False,
        "older_executors_run": False,
    }


def payload_sizes(families):
    return [
        {
            "family": f["problem"]["family"],
            "input_bytes": len(canonical(f["problem"])),
            "geometry_bytes": len(canonical(f["geometry"])),
            "coordinate_bytes": len(canonical(f["coordinates"])),
            "map_bytes": len(canonical(f["maps"])),
            "shared_bytes": len(canonical(f["shared"])),
            "enclosure_bytes": len(canonical(f["enclosure"])),
            "comparison_bytes": len(canonical(f["comparison"])),
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
