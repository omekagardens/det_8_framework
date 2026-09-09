"""Source-bound QR-05BG orchestration; no physics or fixed computation at import."""

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
PROTOCOL_SHA256 = "0944940c7da1f7e15e9d103695cc023964d602cf750056154346b01b35a98256"
BF_DIRECTORY = ROOT.parent / "qr-05bf-known-placement-portability-2026-09-08"
BF_IDENTITIES = {
    "README.md": "f5a78bca5866144d75e70dff0a4f50da1dd71d197af680e38b6e5d527c41ef60",
    "RESULTS.md": "ca9c7a6b1a12e456a7d1a2ec58c39047b871309187a38153f6c12102fee848a4",
    "protocol.json": "0c874abb8290fc1d6e4d76c25c741bf778e5c721f8f7c0310693fcbf1804aa4e",
    "source-freeze.json": "7417b6b3e57e3449d600f5c8b24254fb32444d6002d9e369adc7389e4098cd8a",
    "results.json": "b70e110bf7f076fa37b13ffd0f45ef1c7f339b2b16cfcd4d5219d68e176a9e30",
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
    require(type(protocol) is dict, "protocol must be an object")
    require(raw_same(protocol["stations"], list(STATIONS)), "station contract differs")
    require(
        raw_same([p["id"] for p in protocol["positions"]], POSITION_IDS), "position menu differs"
    )
    require(raw_same([p["id"] for p in protocol["cases"]], CASE_IDS), "case menu differs")
    expected = [{"id": key, "position_ids": value} for key, value in MENU_POSITIONS.items()]
    require(raw_same(protocol["menus"], expected), "declared menu subsets differ")
    return protocol


def source_identities():
    load_protocol()
    for name, digest in BF_IDENTITIES.items():
        require(
            identity(BF_DIRECTORY / name)["sha256"] == digest,
            "preceding BF source changed: " + name,
        )
    files = [
        ROOT / name
        for name in (
            "README.md",
            "protocol.json",
            "quantum.py",
            "reference.py",
            "study.py",
            "test_qr05bg.py",
        )
    ] + [BF_DIRECTORY / name for name in BF_IDENTITIES]
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
        "schema": "QR-05BG-source-freeze-v1",
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
    require(freeze["schema"] == "QR-05BG-source-freeze-v1", "unknown freeze version")
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
    module = ModuleType("_qr05bg_" + name)
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


def _bf_restriction(report):
    """Selected position geometry and center full laws; no old executor."""
    data = _read_bounded(BF_DIRECTORY / "results.json")
    require(
        _bytes_identity(data)["sha256"] == BF_IDENTITIES["results.json"],
        "preceding BF capture identity changed",
    )
    previous = _parse_json(data)["analysis"]["mathematics"]
    for key in ("volume", "sigma", "coefficient_integrals"):
        require(
            same(report["geometry"][key], previous["geometry"][key]),
            "BF geometric integral differs: " + key,
        )
    shared = (
        "id",
        "position",
        "basis",
        "evaluation_matrix",
        "coefficient_decoder",
        "left_inverse",
        "right_inverse",
        "full_weights",
        "full_residual",
    )
    require(len(report["positions"]) == 6, "six-position geometry restriction required")
    for current, old in zip(report["positions"], previous["placements"], strict=True):
        for key in shared:
            require(same(current[key], old[key]), "BF position geometry differs: " + key)
    old_centers = [p for p in previous["placements"] if p["id"] == "center"]
    require(len(old_centers) == 1, "unique historical center required")
    old_by_id = {p["id"]: p for p in old_centers[0]["profiles"]}
    cases = {case["id"]: case for case in report["cases"]}
    require(len(cases) == len(report["cases"]), "unique case identifiers required")
    count = 0
    for current_id, previous_id in (
        ("zero", "zero"),
        ("plus", "plus"),
        ("minus", "minus"),
        ("asymmetric", "asymmetric_bubble"),
    ):
        current, old = cases[current_id], old_by_id[previous_id]
        centers = [c for c in current["candidates"] if c["position_id"] == "center"]
        require(len(centers) == 1, "unique current center candidate required")
        candidate = centers[0]
        require(
            same(current["population_means"], old["sample_means"]),
            "BF public population means differ",
        )
        for key, old_key in (
            ("coefficients", "coefficients"),
            ("admission_bound", "admission_bound"),
            ("reconstructed_means", "sample_means"),
            ("target", "target"),
        ):
            require(same(candidate[key], old[old_key]), "BF center candidate differs: " + key)
        require(candidate["admission_status"] == "admitted", "BF center profile not admitted")
        expected_rows = [
            {key: row[key] for key in ("outcomes", "probability", "state_diagonal")}
            for row in old["full"]["rows"]
        ]
        for law in (current["law"], candidate["law"]):
            require(same(law["rows"], expected_rows), "BF complete center full law differs")
        count += len(expected_rows)
    return {"status": "matched", "positions": 6, "profiles": 4, "branches": count}


def analysis(freeze_path=FREEZE_PATH):
    before = _frozen(freeze_path)
    report = compare_routes(freeze_path)
    result = encode(
        {
            "mathematics": report,
            "bf_restriction": _bf_restriction(report),
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
        "schema": "QR-05BG-evidence-v1",
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
    require(evidence["schema"] == "QR-05BG-evidence-v1", "unknown evidence version")
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
        math = result["analysis"]["mathematics"]
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
                    "sources": len(result["sources"]),
                    "artifact": identity(path),
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
