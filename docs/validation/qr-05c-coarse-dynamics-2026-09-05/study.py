"""Create-only exact QR-05C study; --verify replays without rewriting evidence."""

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
SCHEMA = "det8-qr05c-results-v1"
BASE_COMMIT = "1678e8b090f0148175870368b8ade9206450f7a3"
SOURCES = (
    "README.md",
    "dynamics.py",
    "reference_qr05c.py",
    "study.py",
    "test_qr05c.py",
    "test_capture.py",
    "../qr-01-quantum-records-2026-09-05/exact.py",
)
PRIORS = {
    "qr-01-quantum-records-2026-09-05": "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b",
    "qr-02-record-coarse-graining-2026-09-05": "b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c",
    "qr-03-predictive-histories-2026-09-05": "2b92b7bd42aa9cde29722269c1a31f339e37b217d1256e50d8ea0ee34d8188c2",
    "qr-04-adaptive-causal-records-2026-09-05": "a5dc5f5e96a189ae8fd5648334e630fd4c24f6cee2fa805a45d32522bc0bcd70",
    "qr-05a-quantum-births-2026-09-05": "e0c2676ae33b36dde3edb2697ac252330ad801006fe8420acd8cfb94b87c9479",
    "qr-05b-order-summaries-2026-09-05": "2fe3fd939dcc242ee2a6b8c4abc9d6904e32bf5072cf638f7d880daaeaf2e03b",
}
CASES = (
    "weak_phase",
    "grouped_dephase",
    "zero_link_boundary",
    "chain_boundary",
    "normalized_noncovariant_growth",
)


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
    for name, sha in PRIORS.items():
        raw = plain_bytes(HERE.parent / name / "results.json")
        require(digest(raw) == sha, "prior artifact changed")
        result[name] = {"bytes": len(raw), "sha256": sha}
    return result


def prior_json(name):
    raw = plain_bytes(HERE.parent / name / "results.json")
    require(digest(raw) == PRIORS[name], "prior artifact changed")
    return json.loads(raw)


def load(name, filename):
    require(name not in sys.modules, "private study module collision")
    path = HERE / filename
    raw = plain_bytes(path)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "cannot load executor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)  # noqa: S102
    return module


def fixtures():
    return [{"schema_version": "det8-qr05c-problem-v1", "case": name} for name in CASES]


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


def decode(diag):
    return tuple((F(a), F(b)) for a, b in diag)


def check_cp(diag):
    d = decode(diag)
    require(
        d[0][1] == d[3][1] == 0 and d[1] == (d[2][0], -d[2][1]), "map not Hermiticity preserving"
    )
    require(
        d[0][0] >= 0 and d[3][0] >= 0 and d[0][0] * d[3][0] >= d[1][0] ** 2 + d[1][1] ** 2,
        "Choi block not positive",
    )


ZERO = tuple((F(0), F(0)) for _ in range(4))


def add(a, b):
    return tuple((x[0] + y[0], x[1] + y[1]) for x, y in zip(a, b, strict=True))


def compose(a, b):
    return tuple(
        (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]) for x, y in zip(a, b, strict=True)
    )


def sum_maps(maps):
    result = ZERO
    for diagonal in maps:
        result = add(result, diagonal)
    return result


def check_tp(row, bank):
    total = sum_maps(bank[index] for index in row)
    require(total[0] == total[3] == (F(1), F(0)), "instrument row not trace preserving")


def prior_conformance(result, prior_a, prior_b):
    name = result["case"]
    bank = list(map(decode, result["map_bank"]))
    earlier = next(c["analysis"] for c in prior_a["suite"]["cases"] if c["id"] == name)
    source_checks = 0
    for level, old_level in zip(result["levels"][:4], earlier["levels"], strict=True):
        require(level["births"] == old_level["births"], "prior layer differs")
        require(
            len(level["histories"]) == len(old_level["histories"]), "prior history count differs"
        )
        for row, old in zip(level["histories"], old_level["histories"], strict=True):
            require(
                all(row[key] == old[key] for key in ("order", "outcomes", "settings")),
                "prior fine history differs",
            )
            matrix = old["superoperator"]
            require(
                all(matrix[i][j] == ["0", "0"] for i in range(4) for j in range(4) if i != j),
                "prior map not diagonal",
            )
            require(
                bank[row["source"]] == decode([matrix[i][i] for i in range(4)]),
                "prior source map differs",
            )
            source_checks += 1
    birth_checks = 0
    if name != "normalized_noncovariant_growth":
        older = next(c["analysis"] for c in prior_b["suite"]["cases"] if c["input"]["case"] == name)
        for h, old in enumerate(older["histories"]):
            row = result["levels"][3]["histories"][h]
            grouped = {tuple(key): ZERO for key in older["birth_keys"]}
            for edge in result["fine_steps"][3]["rows"][h]:
                b = sum(row["outcomes"][i] for i in edge["precursor"]) % 2
                key = (len(edge["precursor"]), b, edge["outcome"])
                grouped[key] = add(grouped[key], compose(bank[edge["kernel"]], bank[row["source"]]))
            for key, expected in zip(older["birth_keys"], old["next_birth"], strict=True):
                require(grouped[tuple(key)] == decode(expected), "QR05B continuation differs")
                birth_checks += 1
    return source_checks, birth_checks


def expected_flags(case, summary):
    if summary == "marked_order" or case == "zero_link_boundary":
        return [True] * 4, [True] * 3
    if case == "chain_boundary":
        return ([True, True, True, False] if summary == "link_counts_ones" else [True] * 4), [
            True
        ] * 3
    return [True, True, False, False], [True, False, False]


def check_analysis(a):
    require(a["counts"]["level_histories"] == [1, 2, 8, 56, 640], "fine inventory count")
    require(a["counts"]["raw_birth_edges"] == 706, "fine edge count")
    require(a["counts"]["marked_classes"] == [1, 2, 7, 32, 192], "marked class count")
    require(
        a["counts"]["one_step_checks"] == 18940 and a["counts"]["two_step_checks"] == 2782,
        "comparison count",
    )
    for diagonal in a["map_bank"]:
        check_cp(diagonal)
    bank = list(map(decode, a["map_bank"]))
    normalized_rows = 0
    for layer in a["levels"]:
        check_tp([h["source"] for h in layer["histories"]], bank)
        normalized_rows += 1
    for layer in a["fine_steps"]:
        for row in layer["rows"]:
            check_tp([edge["kernel"] for edge in row], bank)
            normalized_rows += 1
    class_counts = ([1, 2, 7, 32, 192], [1, 2, 6, 20, 80], [1, 2, 6, 16, 50], [1, 2, 3, 4, 5])
    for q, expected_counts in zip(a["quotients"], class_counts, strict=True):
        require([len(p) for p in q["partitions"]] == expected_counts, "coarse class inventory")
        expected_one, expected_two = expected_flags(a["case"], q["name"])
        require(
            [step["consistent"] for step in q["steps"]] == expected_one,
            "one-step prediction differs",
        )
        require(
            [step["consistent"] for step in q["two_steps"]] == expected_two,
            "two-step prediction differs",
        )
        source_one = [True] * 4 if a["case"] == "chain_boundary" else expected_one
        require(
            [s["all_fixed_source_branches_equal"] for s in q["steps"]] == source_one,
            "fixed-source branch prediction differs",
        )
        require(
            [s["all_fixed_source_branches_equal"] for s in q["two_steps"]] == expected_two,
            "fixed-source two-step prediction differs",
        )
        for step in (*q["steps"], *q["two_steps"]):
            for row in (*step["actual_rows"], *step["representative_rows"]):
                check_tp(row, bank)
                normalized_rows += 1
    require(
        all(level["valid"] for ref in a["refinements"] for level in ref["levels"]),
        "resolution family not nested",
    )
    expected_covariance = (
        [True, True, True, False, False]
        if a["case"] == "normalized_noncovariant_growth"
        else [True] * 5
    )
    require(
        [r["constant"] for r in a["source_covariance"]] == expected_covariance,
        "source covariance control differs",
    )
    multiplicity = a["controls"]["wrong_parent_sum"]
    require(
        multiplicity["correct_trace"] == "1"
        and multiplicity["wrong_trace"] == "2"
        and len(multiplicity["members"]) == 2,
        "parent multiplicity control",
    )
    if a["case"] == "weak_phase":
        delayed = a["controls"]["delayed"]
        require(
            delayed["one_step_exact"]
            and delayed["probabilities_Px"] == ["147/78125", "1011/78125"],
            "delayed prediction control",
        )
        require(delayed["trace_probabilities"] == ["2022/78125"] * 2, "delayed equal trace control")
        chain = a["controls"]["chain_record"]
        require(
            bank[chain["kernels"][0]][1] == (F(72, 625), F(0))
            and bank[chain["kernels"][1]][1] == (F(0), F(-72, 625)),
            "chain coherence control",
        )
        require(
            a["controls"]["fork_join"]["probabilities"] == ["4/25", "2/5"],
            "fork/join count control",
        )
    return normalized_rows


def retained_bits(value):
    if type(value) is dict:
        return max((retained_bits(v) for v in value.values()), default=0)
    if type(value) is list:
        return max((retained_bits(v) for v in value), default=0)
    if type(value) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value):
        v = F(value)
        return max(abs(v.numerator).bit_length(), v.denominator.bit_length())
    return 0


def run_suite():
    direct, reference = (
        load("qr05c_capture_direct", "dynamics.py"),
        load("qr05c_capture_reference", "reference_qr05c.py"),
    )
    a_prior = prior_json("qr-05a-quantum-births-2026-09-05")
    b_prior = prior_json("qr-05b-order-summaries-2026-09-05")
    cases, source_checks, birth_checks, normalized = [], 0, 0, 0
    for wire in fixtures():
        a, b = direct.analyze(wire), reference.analyze(wire)
        require(a == b, "independent complete analysis differs")
        normalized += check_analysis(a)
        s, k = prior_conformance(a, a_prior, b_prior)
        source_checks += s
        birth_checks += k
        cases.append({"input": wire, "analysis": a, "retained_component_bits": retained_bits(a)})
    rejections = []
    for wire in invalid_fixtures():
        for module in (direct, reference):
            try:
                module.analyze(wire)
            except (ValueError, TypeError):
                pass
            else:
                raise ValueError("invalid fixed input accepted")
        rejections.append({"input": wire, "both_rejected": True})
    return {
        "cases": cases,
        "rejections": rejections,
        "research_base_commit": BASE_COMMIT,
        "claim": "FINITE_CQ_COARSE_TRANSITION_AND_ITERATION_CONTRACT",
        "spatial_scale_consistency_established": False,
        "gravity_derived": False,
        "empirical_data_used": False,
        "ret_integration_tested": False,
        "bounds": {
            "maximum_births": 4,
            "one_step_max_parent_births": 3,
            "two_step_max_parent_births": 2,
            "fixed_qubits": 1,
            "arithmetic_guard_bits": 4096,
        },
        "totals": {
            "fixtures": len(cases),
            "rejected_fixtures": len(rejections),
            "fine_histories": 3535,
            "raw_birth_edges": 3530,
            "one_step_map_comparisons": 94700,
            "two_step_map_comparisons": 13910,
            "prior_source_map_checks": source_checks,
            "prior_continuation_checks": birth_checks,
            "normalized_rows": normalized,
            "map_bank_choi_checks": sum(len(c["analysis"]["map_bank"]) for c in cases),
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
        before = plain_bytes(RESULT)
        existing = json.loads(before)
        require(
            type(existing) is dict
            and set(existing)
            == {"schema_version", "source_ledger", "prior_artifacts", "suite", "runtime"}
            and existing["schema_version"] == SCHEMA,
            "unrecognized result schema",
        )
        require(canonical(existing) == before, "result is not canonical")
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
        require(plain_bytes(RESULT) == before, "result changed during replay")
        print(
            json.dumps(
                {
                    "status": "VERIFIED_EXACT_REPLAY",
                    "sha256": digest(before),
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
