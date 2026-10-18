"""QR-05AT frozen-map structural bank portability orchestration."""

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
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05at-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05at.py")
AS = HERE.parent / "qr-05as-query-supplements-2026-09-08/results.json"
AS_ID = {
    "bytes": 614211,
    "sha256": "901c7e1a7c53be35be5654fbb01e5bbde4044f6a50184dd80014df155129e366",
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
    "coarse_tiles",
    "bank_tiles",
    "source_columns",
    "coarse_values",
    "bank_values",
    "target_rows",
    "supplement_values",
    "receiver_values",
    "input_rational_entries",
    "coarse_map_entries",
    "effective_map_entries",
    "defect_entries",
    "nonzero_defect_entries",
    "nonzero_intercept_entries",
    "source_check_entries",
    "bank_controls",
    "bank_control_entries",
    "structural_rows",
    "restricted_only_rows",
)
CHECK_FIELDS = (
    "lineage_partition",
    "coarse_source_identity",
    "inherited_geometric_identity",
    "selected_filter_identity",
    "source_receiver_identity",
    "affine_probe_identity",
    "structural_classification",
)
SCOPE = (
    "source_dictionary_changed",
    "geometry_reintegrated",
    "old_collision_replayed",
    "decoder_refitted",
    "filters_reselected",
    "off_model_normalization_inferred",
    "physical_bank_controls_established",
    "full_field_recovery_tested",
    "measurement_interface_insufficiency_proved",
    "minimality_recomputed",
    "empirical_noise_calibrated",
    "unknown_geometry_reconstructed",
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
    require(ident(AS) == AS_ID, "AS artifact changed")
    return json.loads(plain_bytes(AS))


def ar_document():
    require(ident(AR) == AR_ID, "AR artifact changed")
    return json.loads(plain_bytes(AR))


def identities():
    previous = prior_document()
    prior = {str(AS.relative_to(HERE.parent)): AS_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AS.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def check_repair_link_bounds(child, parent):
    """Check the selected original-tile link without any moment integration."""
    for rectangle in (child, parent):
        require(type(rectangle) is list and len(rectangle) == 4, "AR link rectangle shape")
        require(all(type(x) is list and len(x) == 2 for x in rectangle), "AR link pair shapes")
    for pair in child + parent:
        n, d = pair
        require(type(n) is int and type(d) is int and d > 0, "AR link rational values")
        require(
            max(abs(n).bit_length(), d.bit_length()) <= 4096 and gcd(n, d) == 1,
            "AR link bounded reduced values",
        )

    def le(left, right):
        return left[0] * right[1] <= right[0] * left[1]

    for rectangle in (child, parent):
        require(
            not le(rectangle[1], rectangle[0]) and not le(rectangle[3], rectangle[2]),
            "AR link positive rectangles",
        )
    require(
        le(parent[0], child[0])
        and le(child[1], parent[1])
        and le(parent[2], child[2])
        and le(child[3], parent[3]),
        "AR repair outside referenced original fine tile",
    )


def project_inputs(as_families, ar_families):
    for items, label in ((as_families, "AS"), (ar_families, "AR")):
        require(type(items) is list and len(items) == 2, label + " family inventory")
        require([f["problem"]["family"] for f in items] == list(FAMILIES), label + " family order")
    problems = []
    for current, old in zip(as_families, ar_families, strict=True):
        sp, matrix, geo = current["problem"], old["matrices"], old["geometry"]
        labels = matrix["fine_response_rows"]
        verify_suite(old["repair"]["intercept"], [[0, 1] for _ in labels])
        for skey, akey in (
            ("observations", "coarse_observations"),
            ("bank", "repair_observations"),
            ("targets", "fine_targets"),
            ("target_labels", "fine_response_rows"),
        ):
            verify_suite(sp[skey], matrix[akey])
        verify_suite(sp["filters"], old["repair"]["matrix"])
        coarse, bank, fine = geo["coarse_tiles"], geo["repair_tiles"], geo["fine_tiles"]
        require(len(coarse) == 8 and len(bank) == 12 and len(fine) == 12, "AR tile inventory")
        verify_suite(
            [{k: t[k] for k in ("event", "bounds")} for t in coarse], old["problem"]["coarse_tiles"]
        )
        verify_suite(
            [{k: t[k] for k in ("event", "bounds", "coarse_tile")} for t in fine],
            old["problem"]["fine_tiles"],
        )
        for key, tiles in (("coarse_observation_rows", coarse), ("repair_observation_rows", bank)):
            verify_suite(
                matrix[key], [{"tile": i, "basis": h} for i in range(len(tiles)) for h in range(4)]
            )
        for tile in bank:
            parent, origin = tile["coarse_tile"], tile["fine_tile"]
            require(type(parent) is int and 0 <= parent < len(coarse), "AR parent index")
            require(type(origin) is int and 0 <= origin < len(fine), "AR original tile index")
            verify_suite(tile["event"], fine[origin]["event"])
            verify_suite(parent, fine[origin]["coarse_tile"])
            check_repair_link_bounds(tile["bounds"], fine[origin]["bounds"])
        p = {
            "family": sp["family"],
            "coarse_tiles": [t["bounds"] for t in coarse],
            "bank_tiles": [{k: t[k] for k in ("bounds", "coarse_tile")} for t in bank],
            "target_labels": sp["target_labels"],
            "observations": sp["observations"],
            "bank": sp["bank"],
            "targets": sp["targets"],
            "geometric": sp["filters"],
            "selected_rows": current["selection"]["target_rows"],
            "filters": current["selection"]["filters"],
            "intercept": current["decoder"]["intercept"],
            "receiver": current["decoder"]["matrix"],
        }
        require(len(p["selected_rows"]) == 5 and len(p["intercept"]) == 64, "AS map inventory")
        for key, rows, width in (
            ("observations", 32, 108),
            ("bank", 48, 108),
            ("targets", 64, 108),
            ("geometric", 64, 48),
            ("filters", 5, 48),
            ("receiver", 64, 37),
        ):
            require(
                type(p[key]) is list
                and len(p[key]) == rows
                and all(type(row) is list and len(row) == width for row in p[key]),
                "selected matrix inventory",
            )
        problems.append(copy.deepcopy(p))
    return problems, (as_families, ar_families)


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"], ar_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05at_" + name, HERE / filename)
    require(spec is not None and spec.loader is not None, "engine loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def controls(families):
    require(type(families) is list and len(families) == 2, "complete fixed inventory")
    require([f["problem"]["family"] for f in families] == list(FAMILIES), "family order")
    for family in families:
        require(set(family["checks"]) == set(CHECK_FIELDS), "complete check fields")
        require(all(v is True for v in family["checks"].values()), "family check failed")
        status = family["classification"]
        rows = len(family["problem"]["targets"])
        require(type(status["unrestricted_exact"]) is bool, "native classification")
        require(
            status["unrestricted_exact"] == (not status["restricted_only_rows"]),
            "classification flag",
        )
        require(
            (status["first_failure"] is None) == status["unrestricted_exact"],
            "first witness presence",
        )
        require(
            sorted(status["structural_rows"] + status["restricted_only_rows"]) == list(range(rows)),
            "complete row classification",
        )
        require(
            len(family["bank_controls"]) == len(family["problem"]["bank"]) + 1,
            "complete zero/unit controls",
        )
    return dict.fromkeys(CHECK_FIELDS, True)


def historical_bridges(families, previous):
    expected, _ = project_inputs(*previous)
    verify_suite([f["problem"] for f in families], expected)
    controls(families)
    return {
        "AS_selected_families": list(FAMILIES),
        "AS_frozen_maps_equal": True,
        "AS_source_inputs_equal": True,
        "AR_source_inputs_equal": True,
        "AR_lineage_inputs_equal": True,
        "AR_observation_labels_checked": True,
        "AR_repair_links_checked": True,
        "AR_zero_repair_intercept": True,
        "other_historical_mathematics_replayed": False,
        "older_executors_run": False,
    }


def payload_sizes(families):
    return [
        {
            "family": f["problem"]["family"],
            "input_bytes": len(canonical(f["problem"])),
            "lineage_bytes": len(canonical(f["lineage"])),
            "composition_bytes": len(canonical(f["composition"])),
            "classification_bytes": len(canonical(f["classification"])),
            "bank_controls_bytes": len(canonical(f["bank_controls"])),
            "receiver_map_bytes": len(
                canonical(
                    {"intercept": f["problem"]["intercept"], "matrix": f["problem"]["receiver"]}
                )
            ),
            "native_family_bytes": len(canonical(f)),
        }
        for f in families
    ]


def assemble_suite(families, previous):
    expected, consumed = load_inputs()
    verify_suite(list(previous), list(consumed))
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
