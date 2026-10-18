"""Source-bound QR-05BE orchestration; no physics or fixed computation at import."""

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
PROTOCOL_SHA256 = "35c28b24b399c282eaaea62410d8ac1044050462e7080abe90bb868755ece979"
BD_DIRECTORY = ROOT.parent / "qr-05bd-interior-measurement-repair-2026-09-08"
BD_IDENTITIES = {
    "README.md": "45ada4101577e805a584bacde3c5b71d380e6e742a4743bed9002ee347270a2b",
    "RESULTS.md": "6d7c80c6d296ea9b6c044b825fc30b8d08d093848f92f07c6970394540ce779a",
    "protocol.json": "68a49ef25e379663a04fa7742d06b28fe3490d12d431ed4f3adc2fddcb907d73",
    "source-freeze.json": "3ac7ac90513ca74cb2ed87949e3b629cde4cf51951c32b257990fdb00ed3997c",
    "results.json": "30872f9a461270aab14c946d03f6c71aeae8958ef6e72b0a2e01bd0d2606ed8e",
}
STATIONS = ("00", "10", "01", "11", "cc")
PLAN_SLOTS = {
    "corner4": (("00", 1), ("10", 1), ("01", 1), ("11", 1)),
    "repair5": (("00", 1), ("10", 1), ("01", 1), ("11", 1), ("cc", 1)),
    "corner5": (("00", 1), ("00", 2), ("10", 1), ("01", 1), ("11", 1)),
    "target4": (("00", 1), ("10", 1), ("01", 1), ("cc", 1)),
    "repeatcc5": (("00", 1), ("10", 1), ("01", 1), ("cc", 1), ("cc", 2)),
}

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
    "acquisition_plan_id",
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
    require(tuple(protocol["stations"]) == STATIONS, "station contract differs")
    require(raw_same(protocol["public_context"], CONTEXT), "public context differs")
    require(frozenset(protocol["record_keys"]) == RECORD_KEYS, "record schema differs")
    require([p["id"] for p in protocol["plans"]] == list(PLAN_SLOTS), "public plans differ")
    for plan in protocol["plans"]:
        expected = [list(slot) for slot in PLAN_SLOTS[plan["id"]]]
        require(raw_same(plan["slots"], expected), "plan slot contract differs")
        require(type(plan["cost"]) is int and plan["cost"] == len(expected), "shot count differs")
    return protocol


def source_identities():
    load_protocol()
    for name, digest in BD_IDENTITIES.items():
        require(
            identity(BD_DIRECTORY / name)["sha256"] == digest,
            "preceding BD source changed: " + name,
        )
    files = [
        ROOT / name
        for name in (
            "README.md",
            "protocol.json",
            "quantum.py",
            "reference.py",
            "study.py",
            "test_qr05be.py",
        )
    ] + [BD_DIRECTORY / name for name in BD_IDENTITIES]
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
        "schema": "QR-05BE-source-freeze-v1",
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
    require(freeze["schema"] == "QR-05BE-source-freeze-v1", "unknown freeze version")
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


def _slots(plan):
    require(type(plan) is str and plan in PLAN_SLOTS, "unknown acquisition plan")
    return PLAN_SLOTS[plan]


def make_records(outcomes, plan="repair5"):
    slots = _slots(plan)
    require(
        type(outcomes) in (list, tuple) and len(outcomes) == len(slots),
        "complete plan outcomes required",
    )
    records = []
    for (station, shot), outcome in zip(slots, outcomes, strict=True):
        require(type(outcome) is int and outcome in (-1, 1), "invalid ideal outcome")
        records.append(
            {
                **CONTEXT,
                "acquisition_plan_id": plan,
                "station_id": station,
                "shot_id": shot,
                "raw_registration_ref": f"packet:{station}:{shot}",
                "attempted": True,
                "status": "registered",
                "outcome": outcome,
                "available": True,
            }
        )
    return records


def estimate(records, weights, plan="repair5"):
    """Public decoder: exact plan quotas, no private profile/file/state access."""
    slots = _slots(plan)
    stations = {station for station, _shot in slots}
    require(type(records) is list and len(records) == len(slots), "complete plan record required")
    require(type(weights) is dict and set(weights) == stations, "invalid weight labels")
    require(
        all(type(key) is str and type(value) is Fraction for key, value in weights.items()),
        "weights must be exact Fraction values",
    )
    quotas = {station: sum(s == station for s, _shot in slots) for station in stations}
    sums = {station: Fraction(0) for station in stations}
    seen = set()
    for record in records:
        require(type(record) is dict and set(record) == RECORD_KEYS, "invalid record fields")
        require(all(type(key) is str for key in record), "invalid record key type")
        station, shot = record["station_id"], record["shot_id"]
        require(type(station) is str and station in stations, "invalid station")
        require(type(shot) is int, "shot ID must be a native integer")
        slot = (station, shot)
        require(slot in slots, "undeclared station/shot")
        require(slot not in seen, "duplicate station/shot")
        seen.add(slot)
        require(
            type(record["acquisition_plan_id"]) is str and record["acquisition_plan_id"] == plan,
            "acquisition-plan mismatch",
        )
        for key, expected in CONTEXT.items():
            require(
                type(record[key]) is str and record[key] == expected, "context mismatch: " + key
            )
        require(
            type(record["raw_registration_ref"]) is str
            and record["raw_registration_ref"] == f"packet:{station}:{shot}",
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
        sums[station] += record["outcome"]
    require(seen == set(slots), "missing declared slot")
    return sum(
        (weights[station] * sums[station] / quotas[station] for station in stations), Fraction(0)
    )


def _load_engine(name, expected_identity):
    """Execute the exact inspected source bytes, not sys.modules or a pyc cache."""
    require(name in ("quantum", "reference"), "unknown research engine")
    path = ROOT / (name + ".py")
    source = _read_bounded(path)
    require(same(_bytes_identity(source), expected_identity), "engine source changed before load")
    module = ModuleType("_qr05be_" + name)
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
    repair_weights = dict(zip(STATIONS, report["geometry"]["repair_weights"], strict=True))
    corner_weights = dict(zip(STATIONS[:4], report["geometry"]["corner_weights"], strict=True))
    reduced_weights = {
        STATIONS[i]: report["geometry"]["repair_weights"][i]
        for i in report["reduction"]["retained_indices"]
    }
    plan_weights = {
        "corner4": corner_weights,
        "repair5": repair_weights,
        "corner5": corner_weights,
        "target4": reduced_weights,
        "repeatcc5": reduced_weights,
    }
    estimates = []
    order_checks = 0
    for profile in [*report["profiles"], report["off_model"]]:
        by_plan = []
        for plan in PLAN_SLOTS:
            if plan not in profile["plans"]:
                continue
            weights = plan_weights[plan]
            values = []
            for row in profile["plans"][plan]["rows"]:
                records = make_records(row["outcomes"], plan)
                answer = estimate(records, weights, plan)
                require(answer == row["estimate"], "record-only estimator mismatch")
                for ordered in (records, list(reversed(records))):
                    require(estimate(ordered, weights, plan) == answer, "record order dependence")
                    order_checks += 1
                values.append(answer)
            by_plan.append({"id": plan, "estimates": values})
        estimates.append({"profile": profile["id"], "plans": by_plan})

    refusals = []
    for plan, slots in PLAN_SLOTS.items():
        weights = plan_weights[plan]
        base = make_records([-1] * len(slots), plan)
        malformed = [
            ("missing_slot", base[:-1]),
            ("extra_slot", base + [deepcopy(base[0])]),
            ("duplicate_slot", [deepcopy(base[0]), deepcopy(base[0]), *deepcopy(base[2:])]),
        ]
        for key, value in [
            ("available", False),
            ("available", 1),
            ("attempted", False),
            ("attempted", 1),
            ("status", "nondetection"),
            ("status", "postselected"),
            ("shot_id", True),
            ("shot_id", 0),
            ("shot_id", 3),
            ("outcome", True),
            ("outcome", 0),
            ("outcome", 1.0),
            ("outcome", "1"),
            ("station_id", "unknown"),
            ("raw_registration_ref", "private-profile"),
            ("acquisition_plan_id", "unknown"),
        ]:
            changed = deepcopy(base)
            changed[0][key] = value
            malformed.append((key + "=" + repr(value), changed))
        for key in CONTEXT:
            changed = deepcopy(base)
            changed[0][key] = "mismatched"
            malformed.append(("context_" + key, changed))
        for private in ("profile", "f", "theta", "rho", "likelihood", "target", "seed"):
            changed = deepcopy(base)
            changed[0][private] = "hidden"
            malformed.append(("private_" + private, changed))
        changed = deepcopy(base)
        del changed[0]["outcome"]
        malformed.append(("missing_outcome", changed))
        for label, records in malformed:
            try:
                estimate(records, weights, plan)
            except ValueError:
                refusals.append({"plan": plan, "case": label})
            else:
                raise ValueError("malformed record accepted: " + plan + "/" + label)
    return {
        "estimates": estimates,
        "record_order_checks": order_checks,
        "record_refusals": refusals,
    }


def _bd_restriction(report):
    """Selected overlapping mathematics only; no historical executor is loaded."""
    data = _read_bounded(BD_DIRECTORY / "results.json")
    require(
        _bytes_identity(data)["sha256"] == BD_IDENTITIES["results.json"],
        "preceding BD capture identity changed",
    )
    previous = _parse_json(data)["analysis"]["mathematics"]
    for key in ("geometry", "operators", "schedule_counts"):
        require(same(encode(report[key]), previous[key]), "BD restriction differs: " + key)
    require(same(encode(report["plans"][:3]), previous["plans"]), "BD plan restriction differs")
    count = 0
    shared_fields = (
        "id",
        "corners",
        "theta",
        "admission_bound",
        "sample_means",
        "recovered_coefficients",
        "target",
        "corner_target",
    )
    for current, old in zip(report["profiles"][:10], previous["profiles"], strict=True):
        for key in shared_fields:
            require(same(encode(current[key]), old[key]), "BD profile restriction differs: " + key)
        for plan in ("corner4", "repair5", "corner5"):
            require(
                same(encode(current["plans"][plan]), old["plans"][plan]),
                "BD complete plan report differs: " + plan,
            )
            count += len(current["plans"][plan]["rows"])
    current, old = report["off_model"], previous["off_model"]
    for key in ("sample_means", "global_bound", "target"):
        require(same(encode(current[key]), old[key]), "BD off-model restriction differs: " + key)
    full = current["plans"]["repair5"]
    for key, old_key in (
        ("mean", "estimator_mean"),
        ("bias", "estimator_bias"),
        ("variance", "estimator_variance"),
        ("mse", "mse"),
    ):
        require(same(encode(full[key]), old[old_key]), "BD off-model moment differs")
    require(
        same(encode([row["probability"] for row in full["rows"]]), old["probabilities"]),
        "BD off-model complete probability law differs",
    )
    require(
        same(encode([row["state_diagonal"] for row in full["rows"]]), old["state_diagonals"]),
        "BD off-model complete state law differs",
    )
    return {
        "status": "matched",
        "profiles": 10,
        "plans": 3,
        "branches": count,
        "off_model_branches": len(full["rows"]),
    }


def analysis(freeze_path=FREEZE_PATH):
    before = _frozen(freeze_path)
    report = compare_routes(freeze_path)
    result = encode(
        {
            "mathematics": report,
            "observer": _observer_analysis(report),
            "bd_restriction": _bd_restriction(report),
        }
    )
    require(
        same(before, _frozen(freeze_path)), "sources changed during observer/restriction checks"
    )
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
        "schema": "QR-05BE-evidence-v1",
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
    require(evidence["schema"] == "QR-05BE-evidence-v1", "unknown evidence version")
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
                    "branches": sum(
                        len(plan["rows"])
                        for case in math["profiles"]
                        for plan in case["plans"].values()
                    ),
                    "off_model_branches": sum(
                        len(p["rows"]) for p in math["off_model"]["plans"].values()
                    ),
                    "sources": len(result["sources"]),
                    "artifact": identity(path),
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
