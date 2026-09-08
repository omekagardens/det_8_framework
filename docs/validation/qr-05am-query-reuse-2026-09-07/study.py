"""QR-05AM bounded query-reuse orchestration; no historical engine imports."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import platform
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05am-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05am.py")
AL = HERE.parent / "qr-05al-middle-moments-2026-09-07/results.json"
AL_ID = {
    "bytes": 13515233,
    "sha256": "1e0f3ac8822afcd4407a176e1bfa4a2c3f5e45c43724e4e70bf3f66f01580a52",
}
MAX_CAPTURE_BYTES = 128 * 1024 * 1024
MAX_WORKING_BYTES = 192 * 1024 * 1024
FAMILIES = ("grid", "warp", "warp_stale", "boost", "dilate")
LEVELS = ("l0", "l1", "l2")
SCOPE = (
    "generic_production_API_hardened",
    "untrusted_primary_moments_geometrically_authenticated",
    "minimal_grid_proved",
    "universal_query_interface",
    "unknown_geometry_reconstructed",
    "arbitrary_dynamics_closure",
    "continuum_limit_established",
    "marks_authenticated",
    "stochastic_transition_constructed",
    "quantum_channel_constructed",
    "gravity_derived",
    "empirical_data_used",
    "ret_integration_tested",
    "lean_verification_performed",
)
QUERY_NAMES = ("whole_probe", "middle_self", "incoming_kink", "outgoing_kink", "zero_endpoint")
QUERY_COUNT_FIELDS = (
    "old_tiles",
    "admissible_old_tiles",
    "unsupported_old_tiles",
    "retained_pieces",
    "derived_pieces",
    "replaced_old_tiles",
    "moment_derivation_calls",
    "forced_coefficient_vectors",
    "forced_coefficient_entries",
    "exact_coefficient_vectors",
    "exact_coefficient_entries",
    "new_moment_entries",
    "retained_moment_entries",
    "piece_bound_entries",
    "moment_blocks",
    "moment_block_entries",
)
COUNT_FIELDS = QUERY_COUNT_FIELDS + (
    "contexts",
    "middle_rows",
    "positive_middle_rows",
    "snapshot_tiles",
    "snapshot_moment_entries",
    "snapshot_bound_entries",
    "endpoint_bound_entries",
    "queries",
    "empty_middle_queries",
    "reuse_queries",
    "refinement_queries",
    "positive_exact_queries",
    "forced_positive_errors",
    "forced_zero_errors",
    "forced_negative_errors",
    "refinement_forced_equalities",
    "incoming_pair_disagreements",
    "outgoing_pair_disagreements",
)
MOMENT_EXPONENTS = tuple((i, j) for i in range(3) for j in range(3))
BASIS_EXPONENTS = ((0, 0), (1, 0), (0, 1), (1, 1))
VOLUME_FIELDS = {"middle_volume", "incoming_volume", "outgoing_volume"}
PAIR_FIELDS = {
    "incoming_pair",
    "outgoing_pair",
    "forced_incoming_pair",
    "forced_outgoing_pair",
    "incoming_pair_error",
    "outgoing_pair_error",
    "reuse_incoming_pair",
    "reuse_outgoing_pair",
    "middle_covariance",
}
TRIPLE_FIELDS = {
    "volume_product",
    "causal_integral",
    "pair_product",
    "centered_integral",
    "forced_integral",
    "forced_pair_product",
    "forced_error",
    "reuse_integral",
}


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


def frac(value):
    require(
        type(value) is list and len(value) == 2 and all(type(x) is int for x in value),
        "fraction pair",
    )
    n, d = value
    require(d > 0 and math.gcd(n, d) == 1, "reduced fraction")
    return F(n, d)


def wire(value):
    value = F(value)
    return [value.numerator, value.denominator]


def prior_document():
    require(ident(AL) == AL_ID, "AL artifact changed")
    return json.loads(plain_bytes(AL))


def identities():
    previous = prior_document()
    prior = {str(AL.relative_to(HERE.parent)): AL_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AL.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def snapshot_middle(middle):
    return {
        **{
            key: copy.deepcopy(middle[key])
            for key in ("event", "bounds", "u_breaks", "v_breaks", "moments")
        },
        "tiles": [
            {key: copy.deepcopy(tile[key]) for key in ("bounds", "moments")}
            for tile in middle["tiles"]
        ],
    }


def fixed_queries(probe_bounds, middle):
    bounds = middle["bounds"]
    if bounds is None:
        require(not middle["tiles"], "empty old middle tiles")
        left = right = None
    else:
        require(middle["tiles"], "positive old middle requires tiles")
        first = middle["tiles"][0]["bounds"]
        cut = (frac(first[0]) + frac(first[1])) / 2
        require(frac(bounds[0]) < cut < frac(bounds[1]), "interior prescribed cut")
        left = [copy.deepcopy(bounds[0]), wire(cut), *copy.deepcopy(bounds[2:])]
        right = [wire(cut), *copy.deepcopy(bounds[1:])]
    return [
        {"name": name, "incoming": copy.deepcopy(a), "outgoing": copy.deepcopy(c)}
        for name, a, c in zip(
            QUERY_NAMES,
            (probe_bounds, bounds, left, bounds, None),
            (probe_bounds, bounds, bounds, right, bounds),
            strict=True,
        )
    ]


def project_inputs(previous):
    require(len(previous) == 5, "complete AL family inventory")
    problems = []
    for old, family in zip(previous, FAMILIES, strict=True):
        source = old["problem"]
        require(source["family"] == family, "AL family order")
        require(len(old["levels"]) == len(source["levels"]) == 3, "AL level inventory")
        require(len(source["probes"]) == 5, "AL probe inventory")
        contexts = []
        for lev, original, name, size in zip(
            old["levels"], source["levels"], LEVELS, (6, 7, 8), strict=True
        ):
            require(lev["level"] == original["level"] == name, "AL level label")
            require(len(lev["geometry"]) == 5 and len(original["cells"]) == size, "AL level size")
            for geometry, probe in zip(lev["geometry"], source["probes"], strict=True):
                require(geometry["probe"] == probe["name"], "AL probe label")
                require(
                    [row["event"] for row in geometry["middles"]]
                    == [row["event"] for row in original["cells"]],
                    "complete AL middle IDs",
                )
                middles = []
                for row in geometry["middles"]:
                    middle = snapshot_middle(row)
                    middle["queries"] = fixed_queries(probe["bounds"], middle)
                    middles.append(middle)
                contexts.append(
                    {
                        "level": name,
                        "probe": probe["name"],
                        "probe_bounds": copy.deepcopy(probe["bounds"]),
                        "middles": middles,
                    }
                )
        problems.append({"family": family, "contexts": contexts})
    return problems, previous


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05am_" + name, HERE / filename)
    require(spec is not None and spec.loader is not None, "engine loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scale_family(value, alpha, beta):
    """Complete zero-translation affine transport, including retained snapshots."""
    alpha, beta = F(alpha), F(beta)
    require(alpha > 0 and beta > 0, "positive coordinate scales")
    k = alpha * beta

    def walk(item, field=None):
        if item is None:
            return None
        if field in ("bounds", "probe_bounds", "incoming", "outgoing"):
            require(type(item) is list and len(item) == 4, "rectangle shape")
            return [
                wire(frac(x) * factor)
                for x, factor in zip(item, (alpha, alpha, beta, beta), strict=True)
            ]
        if field in ("u_breaks", "v_breaks"):
            factor = alpha if field == "u_breaks" else beta
            return [wire(frac(x) * factor) for x in item]
        if field in ("moments", "old_moments", "piece_moment_sum"):
            require(type(item) is list and len(item) == 9, "nine moments")
            return [
                wire(frac(x) * k * alpha**i * beta**j)
                for x, (i, j) in zip(item, MOMENT_EXPONENTS, strict=True)
            ]
        if field in (
            "forced_incoming",
            "forced_outgoing",
            "incoming_coefficients",
            "outgoing_coefficients",
        ):
            require(type(item) is list and len(item) == 4, "four coefficients")
            return [
                wire(frac(x) * k / (alpha**i * beta**j))
                for x, (i, j) in zip(item, BASIS_EXPONENTS, strict=True)
            ]
        if field in VOLUME_FIELDS:
            return wire(frac(item) * k)
        if field in PAIR_FIELDS:
            return wire(frac(item) * k**2)
        if field in TRIPLE_FIELDS:
            return wire(frac(item) * k**3)
        if type(item) is dict:
            return {key: walk(child, key) for key, child in item.items()}
        if type(item) is list:
            return [walk(child) for child in item]
        return item

    return walk(value)


def comparison_projection(family):
    answer = copy.deepcopy(family)
    del answer["problem"]["family"]
    return answer


def controls(families):
    require(len(families) == 5, "complete control inventory")
    require([f["problem"]["family"] for f in families] == list(FAMILIES), "complete control order")
    by_name = {f["problem"]["family"]: f for f in families}
    base = comparison_projection(by_name["grid"])
    verify_suite(comparison_projection(by_name["boost"]), scale_family(base, F(2), F(1, 2)))
    verify_suite(comparison_projection(by_name["dilate"]), scale_family(base, F(2), F(2)))
    verify_suite(
        comparison_projection(by_name["warp_stale"]), comparison_projection(by_name["warp"])
    )
    return {"boost": True, "dilation": True, "stale_geometric": True}


def snapshot_projection(problem):
    return {
        "family": problem["family"],
        "contexts": [
            {
                **{key: copy.deepcopy(context[key]) for key in ("level", "probe", "probe_bounds")},
                "middles": [snapshot_middle(middle) for middle in context["middles"]],
            }
            for context in problem["contexts"]
        ],
    }


def query_projection(problem):
    return [
        {
            "level": context["level"],
            "probe": context["probe"],
            "middles": [
                {"event": middle["event"], "queries": copy.deepcopy(middle["queries"])}
                for middle in context["middles"]
            ],
        }
        for context in problem["contexts"]
    ]


def al_bridges(families, old):
    require(len(families) == len(old) == 5, "complete consumed AL inventory")
    expected, _ = project_inputs(old)
    for family, want in zip(families, expected, strict=True):
        verify_suite(family["problem"], want)
        verify_suite(snapshot_projection(family["problem"]), snapshot_projection(want))
    return {
        "AL_family_names": list(FAMILIES),
        "AL_geometry_moment_projection_equal": True,
        "AL_probe_bounds_equal": True,
        "AL_other_math_replayed": False,
        "older_math_replayed": False,
    }


def payload_sizes(families):
    output = []
    for family in families:
        update = [
            {
                "level": context["level"],
                "probe": context["probe"],
                "middles": [
                    {
                        "event": middle["event"],
                        "queries": [
                            {
                                key: copy.deepcopy(query[key])
                                for key in ("name", "admission", "pieces")
                            }
                            for query in middle["queries"]
                        ],
                    }
                    for middle in context["middles"]
                ],
            }
            for context in family["contexts"]
        ]
        output.append(
            {
                "family": family["problem"]["family"],
                "snapshot_bytes": len(canonical(snapshot_projection(family["problem"]))),
                "query_bytes": len(canonical(query_projection(family["problem"]))),
                "exact_update_bytes": len(canonical(update)),
                "native_family_bytes": len(canonical(family)),
            }
        )
    return output


def assemble_suite(families, al_families):
    require(len(families) == 5, "complete family inventory")
    expected, consumed = load_inputs()
    verify_suite(al_families, consumed)
    verify_suite([f["problem"] for f in families], expected)
    totals = {"families": len(families)}
    for family in families:
        require(set(family["counts"]) == set(COUNT_FIELDS), "complete count inventory")
        require(
            all(type(v) is int and v >= 0 for v in family["counts"].values()),
            "nonnegative native counts",
        )
    for key in COUNT_FIELDS:
        totals[key] = sum(f["counts"][key] for f in families)
    return {
        "families": families,
        "controls": controls(families),
        "prior_bridges": al_bridges(families, al_families),
        "payload_sizes": payload_sizes(families),
        "totals": totals,
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
