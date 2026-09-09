"""Source-bound QR-05BJ orchestration; no physics or fixed computation at import."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
FREEZE_PATH = ROOT / "source-freeze.json"
PROTOCOL_SHA256 = "533e807f943f1e37c7231f86300cf6b85d62a06b077ba5541f7d841549d00967"
BI_DIRECTORY = ROOT.parent / "qr-05bi-interval-valued-response-2026-09-09"
BI_IDENTITIES = {
    "README.md": "d29109c97f0d21df27fb537cbf36d6471689cce7983350d5671f259ed81516c0",
    "RESULTS.md": "ec739e9384772899ddc85e9282616399e42a67f1575bef7250937e6aa4c76cb7",
    "protocol.json": "8da402d79a93108711929ede1af63e99be2e07f8097e5f33921edcafa6134127",
    "source-freeze.json": "dafe9c9e0c04d0d49214735ac8048e097fac2402d45b75377396ecc186f448cd",
    "results.json": "79b4dc506585ab1117c39b6bee86c10c7fe0dec469cf4633a47affcf1bc1dd29",
}
STATIONS = ("00", "10", "01", "11", "cc")
POSITION_IDS = ["center", "equality_u", "equality_v", "shift_low", "shift_high", "near_corner"]
CASE_IDS = [
    "zero",
    "plus",
    "minus",
    "quarter_interior",
    "unit_interior",
    "constant_corners_zero_interior",
    "asymmetric",
]
MENU_POSITIONS = {
    "all": list(POSITION_IDS),
    "center_only": ["center"],
    "equality_pair": ["equality_u", "equality_v"],
    "shifted_pair": ["shift_low", "shift_high"],
    "center_near": ["center", "near_corner"],
}
INTERVAL_BUDGETS = [
    {"id": "point", "radius": "0"},
    {"id": "narrow", "radius": "1/64"},
    {"id": "wide", "radius": "1/8"},
]
PROTOCOL_FIELDS = [
    "study",
    "version",
    "base_commit",
    "classification",
    "model",
    "refinement",
    "comparison",
    "no_claims",
]
QUARTER_NODES = ["0", "1/4", "1/2", "3/4", "1"]
REFINEMENT_FIELDS = [
    "degree",
    "nodes",
    "leaves",
    "witness_nodes",
    "certificate_rule",
    "witness_rule",
]
MAX_JSON_BYTES = 4_000_000


def require(condition, message):
    """Keep validation active under python -O."""
    if not condition:
        raise ValueError(message)


def encode(value):
    """Encode exact rationals distinctly from native integers and booleans."""
    if type(value) is Fraction:
        return str(value)
    if value is None or type(value) in (str, int, bool):
        return value
    if type(value) is list:
        return [encode(item) for item in value]
    if type(value) is dict:
        require(all(type(key) is str for key in value), "non-string JSON key")
        return {key: encode(item) for key, item in value.items()}
    raise ValueError("unsupported evidence value type: " + type(value).__name__)


def canonical(value):
    return json.dumps(
        encode(value), sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")
    )


def same(left, right):
    return canonical(left) == canonical(right)


def raw_same(left, right):
    """Compare engine reports before encoding; Fraction is not its string form."""
    if type(left) is not type(right):
        return False
    if left is None or type(left) in (str, int, Fraction):
        return left == right
    if type(left) is list:
        return len(left) == len(right) and all(raw_same(a, b) for a, b in zip(left, right))
    if type(left) is dict:
        return (
            all(type(key) is str for key in left)
            and all(type(key) is str for key in right)
            and set(left) == set(right)
            and all(raw_same(left[key], right[key]) for key in left)
        )
    return False


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def _reject_number(value):
    raise ValueError("non-integer JSON number: " + value)


def _read_bounded(path):
    path = Path(path)
    require(not path.is_symlink() and path.is_file(), "source is not a regular non-symlink file")
    require(path.stat().st_size <= MAX_JSON_BYTES, "source exceeds size limit")
    with path.open("rb") as stream:
        data = stream.read(MAX_JSON_BYTES + 1)
    require(len(data) <= MAX_JSON_BYTES, "source grew beyond size limit")
    return data


def _parse_json(data):
    try:
        value = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=_unique_pairs,
            parse_float=_reject_number,
            parse_constant=_reject_number,
        )
        encode(value)
    except (UnicodeError, RecursionError) as exc:
        raise ValueError("invalid JSON encoding or depth") from exc
    return value


def read_json(path):
    return _parse_json(_read_bounded(path))


def _bytes_identity(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def identity(path):
    return _bytes_identity(_read_bounded(path))


def load_protocol():
    # Authenticate and parse each protocol from its own same bounded snapshot.
    data = _read_bounded(ROOT / "protocol.json")
    require(_bytes_identity(data)["sha256"] == PROTOCOL_SHA256, "protocol identity changed")
    protocol = _parse_json(data)
    require(
        type(protocol) is dict and set(protocol) == set(PROTOCOL_FIELDS),
        "protocol must be the declared object",
    )
    require(protocol["study"] == "QR-05BJ", "study differs")
    require(type(protocol["version"]) is int and protocol["version"] == 1, "version differs")
    config = protocol["refinement"]
    require(
        type(config) is dict and set(config) == set(REFINEMENT_FIELDS), "refinement fields differ"
    )
    require(raw_same(config["degree"], [2, 2]), "refinement degree differs")
    require(raw_same(config["nodes"], ["0", "1/2", "1"]), "refinement nodes differ")
    require(raw_same(config["witness_nodes"], QUARTER_NODES), "witness grid differs")
    expected_leaves = [
        {
            "id": f"q{i}{j}",
            "parent": ("ll", "lh", "hl", "hh")[2 * (i // 2) + j // 2],
            "bounds": [
                [QUARTER_NODES[i], QUARTER_NODES[i + 1]],
                [QUARTER_NODES[j], QUARTER_NODES[j + 1]],
            ],
        }
        for i in range(4)
        for j in range(4)
    ]
    require(raw_same(config["leaves"], expected_leaves), "quarter leaves differ")
    model_data = _read_bounded(BI_DIRECTORY / "protocol.json")
    require(
        _bytes_identity(model_data)["sha256"] == BI_IDENTITIES["protocol.json"],
        "preceding BI protocol identity changed",
    )
    expected_model = _parse_json(model_data)
    require(raw_same(protocol["model"], expected_model), "complete BI input differs")
    require(
        raw_same(protocol["model"]["interval_budgets"], INTERVAL_BUDGETS), "interval budget differs"
    )
    model = protocol["model"]["model"]["model"]
    require(raw_same(model["stations"], list(STATIONS)), "station contract differs")
    require(raw_same([p["id"] for p in model["positions"]], POSITION_IDS), "position menu differs")
    require(raw_same([p["id"] for p in model["cases"]], CASE_IDS), "case menu differs")
    expected = [{"id": key, "position_ids": value} for key, value in MENU_POSITIONS.items()]
    require(raw_same(model["menus"], expected), "declared menu subsets differ")
    return protocol


def source_identities():
    load_protocol()
    for name, digest in BI_IDENTITIES.items():
        require(
            identity(BI_DIRECTORY / name)["sha256"] == digest,
            "preceding BI source changed: " + name,
        )
    files = [
        ROOT / name
        for name in (
            "README.md",
            "protocol.json",
            "quantum.py",
            "reference.py",
            "study.py",
            "test_qr05bj.py",
        )
    ] + [BI_DIRECTORY / name for name in BI_IDENTITIES]
    return {str(path.relative_to(REPO)): identity(path) for path in files}


def _create_json(path, value):
    # Exclusivity is deliberate: neither a prior success nor failure is overwritten.
    data = (
        json.dumps(encode(value), indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
        + "\n"
    ).encode("utf-8")
    require(len(data) <= MAX_JSON_BYTES, "generated artifact exceeds size limit")
    with Path(path).open("xb") as stream:
        stream.write(data)
    return _bytes_identity(data)


def freeze_source(path=FREEZE_PATH):
    require(not Path(path).exists(), "source freeze already exists")
    sources = source_identities()
    freeze = {
        "schema": "QR-05BJ-source-freeze-v1",
        "runtime_at_source_freeze": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "optimized": sys.flags.optimize,
        },
        "sources": sources,
    }
    require(same(sources, source_identities()), "sources changed during freeze")
    written = _create_json(path, freeze)
    require(same(written, identity(path)), "freeze readback differs")
    require(same(sources, source_identities()), "sources changed during freeze publication")
    return freeze


def _frozen(path=FREEZE_PATH):
    freeze = read_json(path)
    require(
        type(freeze) is dict and set(freeze) == {"schema", "runtime_at_source_freeze", "sources"},
        "invalid freeze schema",
    )
    require(freeze["schema"] == "QR-05BJ-source-freeze-v1", "unknown freeze version")
    runtime = freeze["runtime_at_source_freeze"]
    require(
        type(runtime) is dict and set(runtime) == {"python", "implementation", "optimized"},
        "invalid runtime schema",
    )
    require(type(runtime["python"]) is str and bool(runtime["python"]), "invalid Python version")
    require(
        type(runtime["implementation"]) is str and bool(runtime["implementation"]),
        "invalid Python implementation",
    )
    require(
        type(runtime["optimized"]) is int and runtime["optimized"] in (0, 1, 2),
        "invalid optimized flag",
    )
    require(same(freeze["sources"], source_identities()), "current sources differ from freeze")
    return freeze


def _load_engine(name, expected_identity):
    """Execute the exact inspected source bytes, not sys.modules or a pyc cache."""
    require(name in ("quantum", "reference"), "unknown research engine")
    path = ROOT / (name + ".py")
    source = _read_bounded(path)
    require(same(_bytes_identity(source), expected_identity), "engine source changed before load")
    module = ModuleType("_qr05bj_" + name)
    module.__file__ = str(path)
    # Only the two whitelisted local engines, with checked frozen bytes, reach here.
    exec(compile(source, str(path), "exec", dont_inherit=True), module.__dict__)  # noqa: S102
    return module


def compare_routes(freeze_path=FREEZE_PATH):
    before = _frozen(freeze_path)
    quantum = _load_engine(
        "quantum", before["sources"][str((ROOT / "quantum.py").relative_to(REPO))]
    )
    reference = _load_engine(
        "reference", before["sources"][str((ROOT / "reference.py").relative_to(REPO))]
    )

    protocol = load_protocol()
    primary_input = deepcopy(protocol)
    reference_input = deepcopy(protocol)
    primary = quantum.analyze(primary_input)
    require(raw_same(primary_input, protocol), "primary mutated the frozen input")
    independent = reference.analyze(reference_input)
    require(raw_same(reference_input, protocol), "reference mutated the frozen input")
    require(raw_same(primary, independent), "complete native-type independent reports disagree")
    require(same(before, _frozen(freeze_path)), "source freeze changed during analysis")
    return primary


def _bi_restriction(report):
    """Compare whole recomputed BI mathematics; do not replay its BH lifecycle."""
    data = _read_bounded(BI_DIRECTORY / "results.json")
    require(
        _bytes_identity(data)["sha256"] == BI_IDENTITIES["results.json"],
        "preceding BI capture identity changed",
    )
    previous = _parse_json(data)
    require(
        type(report) is dict and set(report) == {"bi_model", "refinement"},
        "current report fields differ",
    )
    current = report["bi_model"]
    require(raw_same(current, current), "unsupported native baseline report")
    require(same(current, previous["analysis"]["mathematics"]), "complete BI mathematics differs")
    cases = current["cases"]
    budgets = [budget for case in cases for budget in case["budgets"]]
    receipt = {
        "status": "matched",
        "positions": len(current["positions"]),
        "cases": len(cases),
        "budgets": len(budgets),
        "hypothesis_intervals": sum(len(budget["positions"]) for budget in budgets),
        "menus": sum(len(budget["menus"]) for budget in budgets),
        "affine_branches": sum(len(case["law_family"]["rows"]) for case in cases),
        "affine_patches": sum(len(case["constraints"]["patches"]) for case in cases),
        "affine_coefficients": sum(
            len(row)
            for case in cases
            for patch in case["constraints"]["patches"]
            for row in patch["coefficients"]
        ),
        "affine_witnesses": sum(len(case["constraints"]["witnesses"]) for case in cases),
        "endpoint_checks": sum(len(budget["endpoint_checks"]) for budget in budgets),
    }
    require(
        same(
            receipt,
            {
                "status": "matched",
                "positions": 6,
                "cases": 7,
                "budgets": 21,
                "hypothesis_intervals": 126,
                "menus": 105,
                "affine_branches": 224,
                "affine_patches": 35,
                "affine_coefficients": 315,
                "affine_witnesses": 63,
                "endpoint_checks": 42,
            },
        ),
        "BI coverage differs",
    )
    return receipt


def analysis(freeze_path=FREEZE_PATH):
    before = _frozen(freeze_path)
    report = compare_routes(freeze_path)
    result = encode(
        {
            "mathematics": report,
            "bi_restriction": _bi_restriction(report),
        }
    )
    require(same(before, _frozen(freeze_path)), "sources changed during restriction checks")
    return result


def capture(path, freeze_path=FREEZE_PATH):
    require(not Path(path).exists(), "capture already exists")
    freeze = _frozen(freeze_path)
    freeze_identity = identity(freeze_path)
    result = analysis(freeze_path)
    require(
        same(freeze, _frozen(freeze_path)) and same(freeze_identity, identity(freeze_path)),
        "source/freeze changed during capture",
    )
    evidence = {
        "schema": "QR-05BJ-evidence-v1",
        "freeze": freeze_identity,
        "sources": freeze["sources"],
        "analysis": result,
    }
    written = _create_json(path, evidence)
    require(same(written, identity(path)), "capture readback differs")
    require(
        same(freeze, _frozen(freeze_path)) and same(freeze_identity, identity(freeze_path)),
        "sources/freeze changed during publication",
    )
    return evidence


def replay(path, freeze_path=FREEZE_PATH):
    data = _read_bounded(path)
    artifact_identity = _bytes_identity(data)
    evidence = _parse_json(data)
    require(
        type(evidence) is dict and set(evidence) == {"schema", "freeze", "sources", "analysis"},
        "invalid evidence schema",
    )
    require(evidence["schema"] == "QR-05BJ-evidence-v1", "unknown evidence version")
    freeze = _frozen(freeze_path)
    require(same(evidence["freeze"], identity(freeze_path)), "freeze identity mismatch")
    require(same(evidence["sources"], freeze["sources"]), "evidence source identities differ")
    expected = analysis(freeze_path)
    require(same(evidence["analysis"], expected), "complete evidence replay differs")
    require(same(freeze, _frozen(freeze_path)), "sources changed during replay")
    require(same(evidence["freeze"], identity(freeze_path)), "freeze bytes changed during replay")
    require(same(artifact_identity, identity(path)), "artifact bytes changed during replay")
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--freeze", type=Path)
    action.add_argument("--capture", type=Path)
    action.add_argument("--replay", type=Path)
    parser.add_argument("--source-freeze", type=Path, default=FREEZE_PATH)
    args = parser.parse_args()
    if args.freeze:
        result = freeze_source(args.freeze)
        print(json.dumps({"status": "source_frozen", "sources": len(result["sources"])}))
    else:
        operation = capture if args.capture else replay
        path = args.capture or args.replay
        result = operation(path, args.source_freeze)
        report = result["analysis"]["mathematics"]
        baseline = report["bi_model"]
        refined = report["refinement"]
        print(
            json.dumps(
                {
                    "status": "captured" if args.capture else "replayed",
                    "positions": len(baseline["positions"]),
                    "cases": len(baseline["cases"]),
                    "budgets": sum(len(case["budgets"]) for case in baseline["cases"]),
                    "hypothesis_intervals": sum(
                        len(budget["positions"])
                        for case in baseline["cases"]
                        for budget in case["budgets"]
                    ),
                    "menus": sum(
                        len(budget["menus"])
                        for case in baseline["cases"]
                        for budget in case["budgets"]
                    ),
                    "affine_branches": sum(
                        len(case["law_family"]["rows"]) for case in baseline["cases"]
                    ),
                    "refined_patches": sum(len(case["constraints"]["patches"]) for case in refined),
                    "refined_witnesses": sum(
                        len(case["constraints"]["witnesses"]) for case in refined
                    ),
                    "sources": len(result["sources"]),
                    "artifact": identity(path),
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
