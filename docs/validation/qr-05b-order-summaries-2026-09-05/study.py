"""Create-only QR-05B capture and byte-preserving exact replay."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import re
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05b-results-v1"
BASE_COMMIT = "9a53d55d1f37842a104c573d347808cd200dada3"
SOURCES = (
    "README.md",
    "summaries.py",
    "reference_qr05b.py",
    "study.py",
    "test_qr05b.py",
    "test_capture.py",
    "../qr-01-quantum-records-2026-09-05/exact.py",
)
PRIORS = {
    "qr-01-quantum-records-2026-09-05": "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b",
    "qr-02-record-coarse-graining-2026-09-05": "b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c",
    "qr-03-predictive-histories-2026-09-05": "2b92b7bd42aa9cde29722269c1a31f339e37b217d1256e50d8ea0ee34d8188c2",
    "qr-04-adaptive-causal-records-2026-09-05": "a5dc5f5e96a189ae8fd5648334e630fd4c24f6cee2fa805a45d32522bc0bcd70",
    "qr-05a-quantum-births-2026-09-05": "e0c2676ae33b36dde3edb2697ac252330ad801006fe8420acd8cfb94b87c9479",
}
CASES = ("weak_phase", "grouped_dephase", "zero_link_boundary", "chain_boundary")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def plain_bytes(path):
    require(path.is_file() and not path.is_symlink(), "input must be a plain file")
    return path.read_bytes()


def ledger():
    result = {}
    for name in SOURCES:
        raw = plain_bytes(HERE / name)
        result[name] = {"bytes": len(raw), "sha256": digest(raw)}
    return result


def priors():
    result = {}
    for directory, sha in PRIORS.items():
        raw = plain_bytes(HERE.parent / directory / "results.json")
        require(digest(raw) == sha, "prior artifact changed")
        result[directory] = {"bytes": len(raw), "sha256": sha}
    return result


def load(name, filename):
    require(name not in sys.modules, "private module collision")
    path = HERE / filename
    raw = plain_bytes(path)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "cannot load implementation")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)  # noqa: S102
    return module


def fixtures():
    return [{"schema_version": "det8-qr05b-problem-v1", "case": name} for name in CASES]


def invalid_fixtures():
    base = fixtures()[0]
    return [
        None,
        [],
        True,
        {},
        {"case": "weak_phase"},
        {"schema_version": base["schema_version"]},
        {**base, "extra": 1},
        {**base, "case": "parity_zx"},
        {**base, "case": True},
        {**base, "case": ["weak_phase"]},
        {**base, "case": None},
        {**base, "schema_version": "other"},
        {**base, "schema_version": 1},
        {**base, "schema_version": [base["schema_version"]]},
    ]


def check_cp(diagonal):
    d = [(F(a), F(b)) for a, b in diagonal]
    require(
        d[0][1] == d[3][1] == 0 and d[1] == (d[2][0], -d[2][1]), "map is not Hermiticity preserving"
    )
    require(d[0][0] >= 0 and d[3][0] >= 0, "negative Choi diagonal")
    require(d[0][0] * d[3][0] >= d[1][0] ** 2 + d[1][1] ** 2, "Choi 2x2 block not positive")


def all_map_leaves(value):
    if (
        type(value) is list
        and len(value) == 4
        and all(
            type(cell) is list and len(cell) == 2 and all(type(v) is str for v in cell)
            for cell in value
        )
    ):
        yield value
    elif type(value) is dict:
        for child in value.values():
            yield from all_map_leaves(child)
    elif type(value) is list:
        for child in value:
            yield from all_map_leaves(child)


def check_control_predictions(analysis, nonboundary):
    controls = analysis["controls"]
    fork, locations = controls["fork_join"], controls["record_location"]
    require(fork["source_equal"] and not fork["counts_equal"], "fork/join source control")
    require(
        locations["source_equal"] and locations["counts_equal"], "record location source control"
    )
    require(
        all(c["source_live"] == [nonboundary, nonboundary] for c in controls.values()),
        "control reachability",
    )
    if nonboundary:
        actual = [[F(v) for v in dist["size"]] for dist in fork["distributions"]]
        require(
            actual == [[F(v, 125) for v in row] for row in ((27, 18, 60, 20), (27, 36, 12, 50))],
            "fork/join analytic growth",
        )
        a, b = locations["distributions"]
        require(
            a["size"] == b["size"] and a["parity"] == b["parity"] == ["3/5", "2/5"],
            "marginal equality control",
        )
        require(
            [a["joint"][1][1], b["joint"][1][1]] == ["0", "18/125"], "joint-correlation discrepancy"
        )


def retained_bits(value):
    if type(value) is dict:
        return max((retained_bits(v) for v in value.values()), default=0)
    if type(value) is list:
        return max((retained_bits(v) for v in value), default=0)
    if type(value) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value):
        f = F(value)
        return max(abs(f.numerator).bit_length(), f.denominator.bit_length())
    return 0


def run_suite():
    implementations = (
        load("qr05b_capture_primary", "summaries.py"),
        load("qr05b_capture_reference", "reference_qr05b.py"),
    )
    cases, cp_checks = [], 0
    expected_classes = ([26, 29, 32], [26, 29, 32], [5, 5, 5], [8, 8, 8])
    averages = ("44393/78125", "44393/78125", "337/625", "1")
    for index, wire in enumerate(fixtures()):
        a, b = (m.analyze(wire) for m in implementations)
        require(a == b, "independent complete analysis differs")
        require(a["counts"]["family_classes"] == expected_classes[index], "class count differs")
        require(a["counts"]["zero_sources"] == (0 if index < 2 else 48), "zero inventory differs")
        require(
            a["aggregation"]["counts_equal"] and a["aggregation"]["totals_equal"],
            "grouping diagram failed",
        )
        require(
            a["aggregation"]["correct_trace"] == "1"
            and a["aggregation"]["wrong_average_trace"] == averages[index],
            "multiplicity control differs",
        )
        require(
            all(f["refines_previous"] is not False for f in a["families"]),
            "question expansion merged classes",
        )
        for family in a["families"]:
            require(family["candidate_checks"][-1]["valid"], "decorated order summary failed")
        if index < 2:
            require(
                a["families"][-1]["classes"] == a["candidates"][-1]["classes"],
                "nonboundary F2/isomorphism partitions differ",
            )
        check_control_predictions(a, index < 2)
        # Select only map-bearing subtrees: control probability tables also
        # have four two-string rows, but are not quantum superoperators.
        for subtree in (
            [{"source": h["source"], "next_birth": h["next_birth"]} for h in a["histories"]],
            a["aggregation"],
        ):
            for diagonal in all_map_leaves(subtree):
                check_cp(diagonal)
                cp_checks += 1
        cases.append({"input": wire, "analysis": a, "retained_component_bits": retained_bits(a)})
    rejected = []
    for wire in invalid_fixtures():
        for implementation in implementations:
            try:
                implementation.analyze(wire)
            except (ValueError, TypeError):
                pass
            else:
                raise ValueError("invalid fixed input accepted")
        rejected.append({"input": wire, "both_rejected": True})
    return {
        "cases": cases,
        "rejections": rejected,
        "research_base_commit": BASE_COMMIT,
        "claim": "FINITE_QUESTION_RELATIVE_QUANTUM_ORDER_SUMMARY_CONTRACT",
        "conditional_coarsest_partition_claimed": False,
        "gravity_derived": False,
        "empirical_data_used": False,
        "ret_integration_tested": False,
        "bounds": {
            "source_births": 3,
            "future_births": 1,
            "fixed_qubits": 1,
            "arithmetic_guard_bits": 4096,
        },
        "totals": {
            "fixtures": 4,
            "rejected_fixtures": len(rejected),
            "source_histories": 224,
            "continuation_blocks": 3584,
            "source_zero_histories": 96,
            "candidate_checks": 60,
            "candidate_conflicts": sum(
                c["analysis"]["counts"]["candidate_conflicts"] for c in cases
            ),
            "retained_choi_checks": cp_checks,
            "retained_component_bits": max(c["retained_component_bits"] for c in cases),
        },
    }


def canonical(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    require(
        sys.flags.isolated and sys.pycache_prefix, "run isolated with an external bytecode cache"
    )
    cache = Path(sys.pycache_prefix).resolve()
    require(
        cache != Path(cache.anchor) and not cache.is_relative_to(ROOT),
        "invalid bytecode cache boundary",
    )
    if not args.verify and (RESULT.exists() or RESULT.is_symlink()):
        raise FileExistsError("result exists; use --verify, never overwrite")
    frozen, previous = ledger(), priors()
    if args.verify:
        raw_before = plain_bytes(RESULT)
        existing = json.loads(raw_before)
        require(
            type(existing) is dict
            and set(existing)
            == {"schema_version", "source_ledger", "prior_artifacts", "suite", "runtime"}
            and existing["schema_version"] == SCHEMA,
            "unrecognized result schema",
        )
        require(canonical(existing) == raw_before, "result is not canonical")
        require(
            existing["source_ledger"] == frozen and existing["prior_artifacts"] == previous,
            "source/prior identity changed",
        )
    started = time.perf_counter()
    suite = run_suite()
    elapsed = time.perf_counter() - started
    require(ledger() == frozen and priors() == previous, "source/prior changed during execution")
    if args.verify:
        require(existing["suite"] == suite, "exact replay differs")
        require(plain_bytes(RESULT) == raw_before, "result changed during replay")
        print(
            json.dumps(
                {
                    "status": "VERIFIED_EXACT_REPLAY",
                    "sha256": digest(raw_before),
                    "seconds": elapsed,
                    "totals": suite["totals"],
                }
            )
        )
        return
    report = {
        "schema_version": SCHEMA,
        "source_ledger": frozen,
        "prior_artifacts": previous,
        "suite": suite,
        "runtime": {
            "python": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
            "isolated": bool(sys.flags.isolated),
            "optimized": sys.flags.optimize,
            "bytecode_cache": str(cache),
            "suite_seconds": elapsed,
            "rss_high_water_at_suite_end": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "rss_units": "bytes" if sys.platform == "darwin" else "KiB",
            "scope": "suite only; excludes serialization; no application performance claim",
        },
    }
    raw = canonical(report)
    with RESULT.open("xb") as output:
        output.write(raw)
    require(plain_bytes(RESULT) == raw, "capture readback differs")
    print(
        json.dumps(
            {
                "status": "CREATED_EXACT_FINITE_RESULT",
                "path": str(RESULT),
                "bytes": len(raw),
                "sha256": digest(raw),
                "seconds": elapsed,
                "totals": suite["totals"],
            }
        )
    )


if __name__ == "__main__":
    main()
