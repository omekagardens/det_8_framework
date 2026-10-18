"""Source-bound QR-05BH orchestration; no physics or fixed computation at import."""

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
PROTOCOL_SHA256 = "6a9cbe4751e80e6f4783efe0ad06c0e6d0b5bb3d2127aee8ca038176b19cb4c8"
BG_DIRECTORY = ROOT.parent / "qr-05bg-finite-position-uncertainty-2026-09-08"
BG_IDENTITIES = {
    "README.md": "e4d2de5928536322a7a36c0950d405a822d62823625bc1fd692c897d2a355a41",
    "RESULTS.md": "0109ef5417139fd78d5e7f906dd7e0a700712081115404cc479570991172bb9b",
    "protocol.json": "0944940c7da1f7e15e9d103695cc023964d602cf750056154346b01b35a98256",
    "source-freeze.json": "1b0db4a54362ac689bb52a14af78d3191db20b922b39469eba05d1054a2a979c",
    "results.json": "1f4aab687899437ffd56ff7e9565256714062a7bdb85c0b45e641bc50c9f9a56",
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
CERTIFICATE_CONTRACT = {
    "degree": [2, 2],
    "local_nodes": ["0", "1/2", "1"],
    "root": {"id": "root", "bounds": [["0", "1"], ["0", "1"]]},
    "leaves": [
        {"id": "ll", "bounds": [["0", "1/2"], ["0", "1/2"]]},
        {"id": "lh", "bounds": [["0", "1/2"], ["1/2", "1"]]},
        {"id": "hl", "bounds": [["1/2", "1"], ["0", "1/2"]]},
        {"id": "hh", "bounds": [["1/2", "1"], ["1/2", "1"]]},
    ],
    "witness_points": [
        ["0", "0"],
        ["0", "1/2"],
        ["0", "1"],
        ["1/2", "0"],
        ["1/2", "1/2"],
        ["1/2", "1"],
        ["1", "0"],
        ["1", "1/2"],
        ["1", "1"],
    ],
    "coefficient_order": "matrix rows index u Bernstein degree; columns index v; both 0,1,2",
    "reconstruction_rule": "original profile minus represented degree-(2,2) Bernstein polynomial at the local 3x3 unisolvent grid; all residuals exactly zero",
    "classification_rule": "certified iff old sufficient admission or all coefficients in all four covering leaves lie in [-1,1]; refuted iff a fixed actual witness has abs(value)>1; unresolved otherwise; certificate/refutation conflict raises",
    "root_rule": "diagnostic full-square coefficient enclosure; root failure never vetoes successful leaf certification; root bounds enclose all leaf coefficients",
    "witness_rule": "retain every actual polynomial value and every violating index; these points are mathematical checks, not measurements",
}
PROTOCOL_FIELDS = [
    "study",
    "version",
    "base_commit",
    "classification",
    "model",
    "certificate",
    "set_rule",
    "existence_rule",
    "target_rule",
    "exactness_rule",
    "comparison",
    "no_claims",
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
    # Hash and parse the same bounded byte snapshot.
    data = _read_bounded(ROOT / "protocol.json")
    require(_bytes_identity(data)["sha256"] == PROTOCOL_SHA256, "protocol identity changed")
    protocol = _parse_json(data)
    require(
        type(protocol) is dict and set(protocol) == set(PROTOCOL_FIELDS),
        "protocol must be the declared object",
    )
    require(protocol["study"] == "QR-05BH", "study differs")
    require(type(protocol["version"]) is int and protocol["version"] == 1, "version differs")
    require(raw_same(protocol["certificate"], CERTIFICATE_CONTRACT), "certificate budget differs")
    model_data = _read_bounded(BG_DIRECTORY / "protocol.json")
    require(
        _bytes_identity(model_data)["sha256"] == BG_IDENTITIES["protocol.json"],
        "preceding BG protocol identity changed",
    )
    expected_model = _parse_json(model_data)
    model = protocol["model"]
    require(raw_same(model, expected_model), "complete BG input differs")
    require(raw_same(model["stations"], list(STATIONS)), "station contract differs")
    require(raw_same([p["id"] for p in model["positions"]], POSITION_IDS), "position menu differs")
    require(raw_same([p["id"] for p in model["cases"]], CASE_IDS), "case menu differs")
    expected = [{"id": key, "position_ids": value} for key, value in MENU_POSITIONS.items()]
    require(raw_same(model["menus"], expected), "declared menu subsets differ")
    return protocol


def source_identities():
    load_protocol()
    for name, digest in BG_IDENTITIES.items():
        require(
            identity(BG_DIRECTORY / name)["sha256"] == digest,
            "preceding BG source changed: " + name,
        )
    files = [
        ROOT / name
        for name in (
            "README.md",
            "protocol.json",
            "quantum.py",
            "reference.py",
            "study.py",
            "test_qr05bh.py",
        )
    ] + [BG_DIRECTORY / name for name in BG_IDENTITIES]
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
        "schema": "QR-05BH-source-freeze-v1",
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
    require(freeze["schema"] == "QR-05BH-source-freeze-v1", "unknown freeze version")
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
    module = ModuleType("_qr05bh_" + name)
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


def _bg_restriction(report):
    """Complete recomputed BG mathematical report; never an old executor."""
    data = _read_bounded(BG_DIRECTORY / "results.json")
    require(
        _bytes_identity(data)["sha256"] == BG_IDENTITIES["results.json"],
        "preceding BG capture identity changed",
    )
    previous = _parse_json(data)["analysis"]["mathematics"]
    current = report["bg_model"]
    require(same(current, previous), "complete BG mathematical restriction differs")
    require(len(current["positions"]) == 6 and len(current["cases"]) == 7, "BG dimensions differ")
    candidates = sum(len(case["candidates"]) for case in current["cases"])
    menus = sum(len(case["menus"]) for case in current["cases"])
    branches = sum(
        len(case["law"]["rows"])
        + sum(len(candidate["law"]["rows"]) for candidate in case["candidates"])
        for case in current["cases"]
    )
    require((candidates, menus, branches) == (42, 35, 1568), "BG coverage differs")
    return {
        "status": "matched",
        "positions": 6,
        "cases": 7,
        "candidates": candidates,
        "menus": menus,
        "branches": branches,
    }


def analysis(freeze_path=FREEZE_PATH):
    before = _frozen(freeze_path)
    report = compare_routes(freeze_path)
    result = encode(
        {
            "mathematics": report,
            "bg_restriction": _bg_restriction(report),
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
        "schema": "QR-05BH-evidence-v1",
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
    require(evidence["schema"] == "QR-05BH-evidence-v1", "unknown evidence version")
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
        math = report["bg_model"]
        print(
            json.dumps(
                {
                    "status": "captured" if args.capture else "replayed",
                    "positions": len(math["positions"]),
                    "cases": len(math["cases"]),
                    "candidates": sum(len(c["candidates"]) for c in math["cases"]),
                    "menus": sum(len(c["menus"]) for c in math["cases"]),
                    "branches": sum(
                        len(case["law"]["rows"])
                        + sum(len(candidate["law"]["rows"]) for candidate in case["candidates"])
                        for case in math["cases"]
                    ),
                    "patches": sum(
                        1 + len(candidate["leaves"])
                        for case in report["refinement"]
                        for candidate in case["candidates"]
                    ),
                    "sources": len(result["sources"]),
                    "artifact": identity(path),
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
