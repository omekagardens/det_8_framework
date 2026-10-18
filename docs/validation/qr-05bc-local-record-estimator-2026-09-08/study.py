"""Source-bound QR-05BC orchestration; no physics or fixed computation at import."""

from __future__ import annotations

import argparse
import hashlib
import itertools
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
PROTOCOL_SHA256 = "7b07d4961163f4241c2eb0452fc78d992f38995918418b20fd38acdf911cf340"
BB_DIRECTORY = ROOT.parent / "qr-05bb-operational-bridge-design-2026-09-08"
BB_IDENTITIES = {
    "README.md": "0b7c1e048f0d96775691001df54a4dbbc64b52d49f74744de9149ff9ca1d543e",
    "RESULTS.md": "d4d8b7152f06bba3a495819a10d1ae3541450af4d8cac21583b81c41b83d4841",
}
STATIONS = ("00", "10", "01", "11")
CONTEXT = {
    "run_id": "run",
    "trial_id": "trial",
    "setting_id": "Z",
    "preparation_protocol_id": "fresh-independent",
    "readout_calibration_id": "ideal-Z",
    "frame_id": "unit-null-frame",
    "collector_id": "collector",
}
RECORD_KEYS = frozenset(CONTEXT) | {
    "station_id",
    "shot_id",
    "raw_registration_ref",
    "attempted",
    "status",
    "outcome",
    "available",
}
MAX_JSON_BYTES = 2_000_000


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
    path = ROOT / "protocol.json"
    require(identity(path)["sha256"] == PROTOCOL_SHA256, "protocol identity changed")
    protocol = read_json(path)
    require(type(protocol) is dict, "protocol must be an object")
    require(tuple(protocol["stations"]) == STATIONS, "station contract differs")
    require(same(protocol["public_context"], CONTEXT), "public context differs")
    require(frozenset(protocol["record_keys"]) == RECORD_KEYS, "record schema differs")
    return protocol


def source_identities():
    load_protocol()
    for name, digest in BB_IDENTITIES.items():
        require(
            identity(BB_DIRECTORY / name)["sha256"] == digest,
            "preceding BB source changed: " + name,
        )
    files = [
        ROOT / name
        for name in (
            "README.md",
            "protocol.json",
            "quantum.py",
            "reference.py",
            "study.py",
            "test_qr05bc.py",
        )
    ] + [BB_DIRECTORY / name for name in BB_IDENTITIES]
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
        "schema": "QR-05BC-source-freeze-v1",
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
    require(freeze["schema"] == "QR-05BC-source-freeze-v1", "unknown freeze version")
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


def make_records(outcomes):
    require(type(outcomes) in (list, tuple) and len(outcomes) == 4, "four ideal outcomes required")
    records = []
    for station, outcome in zip(STATIONS, outcomes):
        require(type(outcome) is int and outcome in (-1, 1), "invalid ideal outcome")
        records.append(
            {
                **CONTEXT,
                "station_id": station,
                "shot_id": 1,
                "raw_registration_ref": "packet:" + station + ":1",
                "attempted": True,
                "status": "registered",
                "outcome": outcome,
                "available": True,
            }
        )
    return records


def estimate(records, weights):
    """Public record-only decoder: no private protocol/profile/state/target reads."""
    require(type(records) is list and len(records) == 4, "complete four-shot record required")
    require(type(weights) is dict and set(weights) == set(STATIONS), "invalid weight labels")
    require(
        all(type(key) is str and type(value) is Fraction for key, value in weights.items()),
        "weights must be exact Fraction values",
    )
    seen = set()
    total = Fraction(0)
    for record in records:
        require(type(record) is dict and set(record) == RECORD_KEYS, "invalid record fields")
        require(all(type(key) is str for key in record), "invalid record key type")
        station = record["station_id"]
        require(type(station) is str and station in STATIONS, "invalid station")
        require(station not in seen, "duplicate station/shot")
        seen.add(station)
        for key, expected in CONTEXT.items():
            require(
                type(record[key]) is str and record[key] == expected, "context mismatch: " + key
            )
        require(type(record["shot_id"]) is int and record["shot_id"] == 1, "invalid shot quota/id")
        require(
            type(record["raw_registration_ref"]) is str
            and record["raw_registration_ref"] == "packet:" + station + ":1",
            "invalid registration reference",
        )
        require(
            record["attempted"] is True and record["available"] is True,
            "unattempted or unavailable record",
        )
        require(
            type(record["status"]) is str and record["status"] == "registered",
            "nonregistered outcome/status",
        )
        require(
            type(record["outcome"]) is int and record["outcome"] in (-1, 1),
            "invalid binary outcome",
        )
        total += weights[station] * record["outcome"]
    return total


def invert_readout(mean, *, offset=None, contrast=None):
    require(
        all(type(value) is Fraction for value in (mean, offset, contrast)),
        "readout mean, offset and contrast must be known exact Fractions",
    )
    require(-1 <= mean <= 1, "registered mean outside binary range")
    require(contrast != 0, "zero contrast is nonidentifying")
    alpha = (1 - contrast - offset) / 2
    beta = (1 - contrast + offset) / 2
    require(0 <= alpha <= 1 and 0 <= beta <= 1, "invalid assignment channel")
    # Finite-shot corrected estimates need not lie in the physical state interval.
    return (mean - offset) / contrast


def _load_engine(name, expected_identity):
    """Execute the exact inspected source bytes, not sys.modules or a pyc cache."""
    require(name in ("quantum", "reference"), "unknown research engine")
    path = ROOT / (name + ".py")
    source = _read_bounded(path)
    require(same(_bytes_identity(source), expected_identity), "engine source changed before load")
    module = ModuleType("_qr05bc_" + name)
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


def _observer_analysis(report):
    weights = dict(zip(STATIONS, report["geometry"]["weights"]))
    estimates = []
    permutation_checks = 0
    for profile in report["profiles"]:
        values = []
        for row in profile["rows"]:
            records = make_records(row["outcomes"])
            answer = estimate(records, weights)
            require(answer == row["estimate"], "record-only estimator mismatch")
            for ordering in itertools.permutations(records):
                require(estimate(list(ordering), weights) == answer, "list-order dependence")
                permutation_checks += 1
            swapped = dict(weights)
            swapped["00"], swapped["11"] = swapped["11"], swapped["00"]
            outcomes = list(row["outcomes"])
            outcomes[0], outcomes[3] = outcomes[3], outcomes[0]
            changed = make_records(outcomes)
            require(
                estimate(changed, weights) == row["swapped_estimate"],
                "wrong-label control mismatch",
            )
            require(
                estimate(changed, swapped) == row["relabeled_estimate"], "joint relabel mismatch"
            )
            require(row["relabeled_estimate"] == answer, "joint relabel did not preserve estimate")
            values.append(answer)
        estimates.append({"profile": profile["id"], "estimates": values})

    base = make_records([-1, 1, -1, 1])
    malformed = []
    malformed.append(("missing_station", base[:-1]))
    malformed.append(("extra_shot", base + [deepcopy(base[0])]))
    malformed.append(
        ("duplicate_station", [deepcopy(base[0]), deepcopy(base[0]), *deepcopy(base[2:])])
    )
    for key, value in [
        ("available", False),
        ("available", 1),
        ("attempted", False),
        ("attempted", 1),
        ("status", "nondetection"),
        ("status", "postselected"),
        ("shot_id", True),
        ("shot_id", 2),
        ("outcome", True),
        ("outcome", 0),
        ("outcome", 1.0),
        ("outcome", "1"),
        ("station_id", "unknown"),
        ("raw_registration_ref", "private-profile"),
    ]:
        changed = deepcopy(base)
        changed[0][key] = value
        malformed.append((key + "=" + repr(value), changed))
    for key in CONTEXT:
        changed = deepcopy(base)
        changed[0][key] = "mismatched"
        malformed.append(("context_" + key, changed))
    for private in ("profile", "f", "rho", "likelihood", "target", "seed"):
        changed = deepcopy(base)
        changed[0][private] = "hidden"
        malformed.append(("private_" + private, changed))
    changed = deepcopy(base)
    del changed[0]["outcome"]
    malformed.append(("missing_outcome", changed))
    refusals = []
    for label, records in malformed:
        try:
            estimate(records, weights)
        except ValueError:
            refusals.append(label)
        else:
            raise ValueError("malformed record accepted: " + label)

    calibration_checks = []
    for row in report["calibrations"]:
        try:
            value = invert_readout(
                row["observed_mean"], offset=row["offset"], contrast=row["contrast"]
            )
        except ValueError:
            require(
                row["contrast"] == 0 and row["corrected_mean"] is None,
                "unexpected calibrated inversion refusal",
            )
            calibration_checks.append({"id": row["id"], "status": "zero_contrast_refused"})
        else:
            require(value == row["corrected_mean"] == row["true_mean"], "calibration mismatch")
            calibration_checks.append({"id": row["id"], "status": "known_channel_inverted"})
    for missing in (
        {"offset": None, "contrast": Fraction(1)},
        {"offset": Fraction(0), "contrast": None},
    ):
        try:
            invert_readout(Fraction(0), **missing)
        except ValueError:
            pass
        else:
            raise ValueError("unknown calibration was inverted")
    return {
        "estimates": estimates,
        "record_permutation_checks": permutation_checks,
        "record_refusals": refusals,
        "calibration_checks": calibration_checks,
        "unknown_calibration_refusals": 2,
    }


def analysis(freeze_path=FREEZE_PATH):
    before = _frozen(freeze_path)
    report = compare_routes(freeze_path)
    result = encode({"mathematics": report, "observer": _observer_analysis(report)})
    require(same(before, _frozen(freeze_path)), "sources changed during observer checks")
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
        "schema": "QR-05BC-evidence-v1",
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
    require(evidence["schema"] == "QR-05BC-evidence-v1", "unknown evidence version")
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
                    "profiles": len(math["profiles"]),
                    "branches": sum(len(case["rows"]) for case in math["profiles"]),
                    "sources": len(result["sources"]),
                    "artifact": identity(path),
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
