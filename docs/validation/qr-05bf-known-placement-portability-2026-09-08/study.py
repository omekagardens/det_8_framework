"""Source-bound QR-05BF orchestration; no physics or fixed computation at import."""

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
PROTOCOL_SHA256 = "0c874abb8290fc1d6e4d76c25c741bf778e5c721f8f7c0310693fcbf1804aa4e"
BE_DIRECTORY = ROOT.parent / "qr-05be-target-specific-measurement-reduction-2026-09-08"
BE_IDENTITIES = {
    "README.md": "3009d90e30e2f88155d14169ae0c176b733e66275d91bd7ec821f1c3da04ee9e",
    "RESULTS.md": "26b5be610e669670e730ffa23c1728b54b553163608180fdb4e5c3a2b2e298bb",
    "protocol.json": "35c28b24b399c282eaaea62410d8ac1044050462e7080abe90bb868755ece979",
    "source-freeze.json": "b1e64907147c4dab23ffb339e666b7be537881c2763130368b2bc0a226e128f8",
    "results.json": "a9c83821f194e03b41958cd5c052920325d973a3263d18b829694a1b9bf09874",
}
STATIONS = ("00", "10", "01", "11", "cc")
RETAINED_INDICES = [0, 1, 2, 4]
OMITTED_INDEX = 3
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
    require(raw_same(protocol["retained_indices"], RETAINED_INDICES), "retained rows differ")
    require(raw_same(protocol["omitted_index"], OMITTED_INDEX), "omitted row differs")
    require(
        len(protocol["placements"]) == 6 and len(protocol["profiles"]) == 4, "fixed menu differs"
    )
    return protocol


def source_identities():
    load_protocol()
    for name, digest in BE_IDENTITIES.items():
        require(
            identity(BE_DIRECTORY / name)["sha256"] == digest,
            "preceding BE source changed: " + name,
        )
    files = [
        ROOT / name
        for name in (
            "README.md",
            "protocol.json",
            "quantum.py",
            "reference.py",
            "study.py",
            "test_qr05bf.py",
        )
    ] + [BE_DIRECTORY / name for name in BE_IDENTITIES]
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
        "schema": "QR-05BF-source-freeze-v1",
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
    require(freeze["schema"] == "QR-05BF-source-freeze-v1", "unknown freeze version")
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
    module = ModuleType("_qr05bf_" + name)
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


def _be_restriction(report):
    """Selected center overlap only; no historical numerical executor."""
    data = _read_bounded(BE_DIRECTORY / "results.json")
    require(
        _bytes_identity(data)["sha256"] == BE_IDENTITIES["results.json"],
        "preceding BE capture identity changed",
    )
    previous = _parse_json(data)["analysis"]["mathematics"]
    geometry, old_geometry = report["geometry"], previous["geometry"]
    for key in ("volume", "sigma"):
        require(same(geometry[key], old_geometry[key]), "BE geometry differs: " + key)
    require(
        same(
            geometry["coefficient_integrals"],
            old_geometry["corner_weights"] + [old_geometry["bubble_target"]],
        ),
        "BE integral row differs",
    )
    require(
        same(geometry["stale_weights"], previous["reduction"]["target_weights"]),
        "BE frozen weights differ",
    )
    for key in ("retained_indices", "omitted_index"):
        require(
            same(geometry[key], previous["reduction"][key]), "BE reduction indices differ: " + key
        )
    centers = [p for p in report["placements"] if p["id"] == "center"]
    require(len(centers) == 1, "unique center comparison required")
    center = centers[0]
    require(
        same(center["position"], [Fraction(1, 2), Fraction(1, 2)]), "BE center position differs"
    )
    for key, old_key in (
        ("evaluation_matrix", "evaluation_matrix"),
        ("coefficient_decoder", "coefficient_decoder"),
        ("full_weights", "repair_weights"),
    ):
        require(same(center[key], old_geometry[old_key]), "BE center geometry differs: " + key)
    require(
        same(center["basis"], old_geometry["center_basis"] + [old_geometry["bubble_at_center"]]),
        "BE center basis differs",
    )
    for key in (
        "retained_evaluation_matrix",
        "retained_rank",
        "omission_direction",
        "retained_null_image",
        "target_null_image",
    ):
        require(
            same(center[key], previous["reduction"][key]), "BE center reduction differs: " + key
        )
    require(
        same(center["candidate_weights"], previous["reduction"]["target_weights"]),
        "BE candidate weights differ",
    )
    ids = ["zero", "plus", "minus", "asymmetric_bubble"]
    old_by_id = {p["id"]: p for p in previous["profiles"]}
    count = 0
    for current, profile_id in zip(center["profiles"][:4], ids, strict=True):
        require(current["id"] == profile_id, "BE base-profile order differs")
        old = old_by_id[profile_id]
        require(
            same(current["coefficients"], old["corners"] + [old["theta"]]), "BE coefficients differ"
        )
        for key in ("admission_bound", "sample_means", "recovered_coefficients", "target"):
            require(same(current[key], old[key]), "BE profile restriction differs: " + key)
        require(same(current["full"], old["plans"]["repair5"]), "BE full plan differs")
        reduced = current["reduced"]
        for estimate_key, score_key in (
            ("candidate_estimate", "candidate"),
            ("stale_estimate", "stale"),
        ):
            rebuilt = {
                "rows": [
                    {
                        "outcomes": row["outcomes"],
                        "probability": row["probability"],
                        "state_diagonal": row["state_diagonal"],
                        "estimate": row[estimate_key],
                    }
                    for row in reduced["rows"]
                ],
                **reduced[score_key],
            }
            require(
                same(rebuilt, old["plans"]["target4"]),
                "BE reduced complete plan differs: " + score_key,
            )
        count += len(current["full"]["rows"]) + len(reduced["rows"])
    return {"status": "matched", "placements": 1, "profiles": 4, "plans": 2, "branches": count}


def analysis(freeze_path=FREEZE_PATH):
    before = _frozen(freeze_path)
    report = compare_routes(freeze_path)
    result = encode(
        {
            "mathematics": report,
            "be_restriction": _be_restriction(report),
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
        "schema": "QR-05BF-evidence-v1",
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
    require(evidence["schema"] == "QR-05BF-evidence-v1", "unknown evidence version")
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
                    "placements": len(math["placements"]),
                    "profiles": sum(len(p["profiles"]) for p in math["placements"]),
                    "branches": sum(
                        len(case["full"]["rows"]) + len(case["reduced"]["rows"])
                        for placement in math["placements"]
                        for case in placement["profiles"]
                    ),
                    "sources": len(result["sources"]),
                    "artifact": identity(path),
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
