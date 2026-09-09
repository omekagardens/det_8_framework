"""Source-bound QR-05BI orchestration; no physics or fixed computation at import."""

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
PROTOCOL_SHA256 = "8da402d79a93108711929ede1af63e99be2e07f8097e5f33921edcafa6134127"
BH_DIRECTORY = ROOT.parent / "qr-05bh-global-admission-refinement-2026-09-08"
BH_IDENTITIES = {
    "README.md": "1eccd0856bdb9456e2a0c9db57ae5ee06fb5158baeb87537cd9869fc8a9af64f",
    "RESULTS.md": "cb758c2e0817961a5baa33ad5be313326d03a4534d6e43759f3c5dfd137d1b0e",
    "protocol.json": "6a9cbe4751e80e6f4783efe0ad06c0e6d0b5bb3d2127aee8ca038176b19cb4c8",
    "source-freeze.json": "14ec10d9ea284e08788faac230de79f482d53e83bce0d4a74742e4d8e87d8661",
    "results.json": "a5e1387c4de81d35641ea8b9f333d4530c66e729a3e60df2ca6e5f80e251d9f5",
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
    "interval_budgets",
    "response_rule",
    "constraint_rule",
    "inner_rule",
    "outer_rule",
    "interval_rule",
    "law_rule",
    "set_rule",
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
    require(protocol["study"] == "QR-05BI", "study differs")
    require(type(protocol["version"]) is int and protocol["version"] == 1, "version differs")
    require(raw_same(protocol["interval_budgets"], INTERVAL_BUDGETS), "interval budget differs")
    model_data = _read_bounded(BH_DIRECTORY / "protocol.json")
    require(
        _bytes_identity(model_data)["sha256"] == BH_IDENTITIES["protocol.json"],
        "preceding BH protocol identity changed",
    )
    expected_model = _parse_json(model_data)
    require(raw_same(protocol["model"], expected_model), "complete BH input differs")
    model = protocol["model"]["model"]
    require(raw_same(model["stations"], list(STATIONS)), "station contract differs")
    require(raw_same([p["id"] for p in model["positions"]], POSITION_IDS), "position menu differs")
    require(raw_same([p["id"] for p in model["cases"]], CASE_IDS), "case menu differs")
    expected = [{"id": key, "position_ids": value} for key, value in MENU_POSITIONS.items()]
    require(raw_same(model["menus"], expected), "declared menu subsets differ")
    return protocol


def source_identities():
    load_protocol()
    for name, digest in BH_IDENTITIES.items():
        require(
            identity(BH_DIRECTORY / name)["sha256"] == digest,
            "preceding BH source changed: " + name,
        )
    files = [
        ROOT / name
        for name in (
            "README.md",
            "protocol.json",
            "quantum.py",
            "reference.py",
            "study.py",
            "test_qr05bi.py",
        )
    ] + [BH_DIRECTORY / name for name in BH_IDENTITIES]
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
        "schema": "QR-05BI-source-freeze-v1",
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
    require(freeze["schema"] == "QR-05BI-source-freeze-v1", "unknown freeze version")
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
    module = ModuleType("_qr05bi_" + name)
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


def _affine_at(pair, value):
    require(
        type(pair) is list and len(pair) == 2 and all(type(x) is Fraction for x in pair),
        "native affine pair required",
    )
    return pair[0] + pair[1] * value


def _point_law(family, mean):
    return {
        "rows": [
            {
                "outcomes": row["outcomes"],
                "probability": _affine_at(row["probability"], mean),
                "state_diagonal": [_affine_at(pair, mean) for pair in row["state_diagonal"]],
            }
            for row in family["rows"]
        ],
        "averaged_state": [_affine_at(pair, mean) for pair in family["averaged_state"]],
    }


def _singleton(interval):
    require(
        type(interval) is list
        and len(interval) == 2
        and all(type(x) is Fraction for x in interval)
        and interval[0] == interval[1],
        "zero-width native interval required",
    )
    return interval[0]


def _point_targets(summary):
    return [_singleton(interval) for interval in summary["intervals"]]


def _point_entries(entries, corners):
    result = []
    for entry in entries:
        require(len(entry["theta"]) == len(entry["targets"]) == 1, "single point hypothesis")
        theta = _singleton(entry["theta"][0])
        target = _singleton(entry["targets"][0])
        result.append(
            {
                "position_id": entry["position_id"],
                "coefficients": [*corners, theta],
                "target": target,
            }
        )
    return result


def _bh_restriction(report):
    """Selected zero-width BH mathematics, authenticated before parsing."""
    data = _read_bounded(BH_DIRECTORY / "results.json")
    require(
        _bytes_identity(data)["sha256"] == BH_IDENTITIES["results.json"],
        "preceding BH capture identity changed",
    )
    previous = _parse_json(data)["analysis"]["mathematics"]
    baseline = previous["bg_model"]
    require(same(report["geometry"], baseline["geometry"]), "BH geometry differs")
    require(same(report["positions"], baseline["positions"]), "BH position geometry differs")
    require(
        [case["id"] for case in report["cases"]]
        == [case["id"] for case in baseline["cases"]]
        == [case["id"] for case in previous["refinement"]],
        "BH case identities differ",
    )
    branches = coefficients = witnesses = candidates = menus = 0
    for case, old_case, refined in zip(
        report["cases"], baseline["cases"], previous["refinement"], strict=True
    ):
        corners, mean = case["corners"], case["center_mean"]
        require(same([*corners, mean], old_case["population_means"]), "BH means differ")
        points = [budget for budget in case["budgets"] if budget["id"] == "point"]
        require(len(points) == 1, "unique point budget")
        point = points[0]
        require(_singleton(point["response_interval"]) == mean, "BH point response differs")
        law = _point_law(case["law_family"], mean)
        require(same(law, old_case["law"]), "BH public law differs")
        branches += len(law["rows"])
        require(
            len(point["positions"])
            == len(old_case["candidates"])
            == len(refined["candidates"])
            == 6,
            "six point hypotheses required",
        )
        for position, old_candidate, old_refined in zip(
            point["positions"], old_case["candidates"], refined["candidates"], strict=True
        ):
            name = position["position_id"]
            require(
                name == old_candidate["position_id"] == old_refined["position_id"],
                "BH hypothesis order",
            )
            theta = _singleton(position["data_theta"])
            target = _singleton(position["data_target"])
            require(
                same([*corners, theta], old_candidate["coefficients"]), "BH coefficients differ"
            )
            require(same(target, old_candidate["target"]), "BH target differs")
            require(
                position["point_classification"] == old_refined["classification"],
                "BH classification differs",
            )
            old_admitted = bool(position["old_theta"])
            require(
                ("admitted" if old_admitted else "outside_sufficient_class")
                == old_candidate["admission_status"]
                == old_refined["old_admission_status"],
                "BH old admission differs",
            )
            routes = (["old_bound"] if old_admitted else []) + (
                ["subdivision_bernstein"] if position["bernstein_theta"] else []
            )
            require(routes == old_refined["certificate_routes"], "BH certificate routes differ")
            require(
                position["response_intercept"] + position["response_slope"] * theta == mean,
                "point data inversion differs",
            )
            require(same(law, old_candidate["law"]), "BH candidate complete law differs")
            branches += len(law["rows"])
            patches = [old_refined["root"], *old_refined["leaves"]]
            require(len(case["constraints"]["patches"]) == len(patches) == 5, "five point patches")
            for patch, old_patch in zip(case["constraints"]["patches"], patches, strict=True):
                require(
                    same(patch["id"], old_patch["id"])
                    and same(patch["bounds"], old_patch["bounds"]),
                    "BH patch identity differs",
                )
                values = [
                    [_affine_at(pair, theta) for pair in row] for row in patch["coefficients"]
                ]
                require(
                    same(values, old_patch["coefficients"]),
                    "BH point Bernstein coefficients differ",
                )
                coefficients += sum(map(len, values))
            fixed = case["constraints"]["witnesses"]
            require(len(fixed) == len(old_refined["witnesses"]) == 9, "nine point witnesses")
            violated = []
            for i, (witness, old_witness) in enumerate(
                zip(fixed, old_refined["witnesses"], strict=True)
            ):
                value = _affine_at(witness["value"], theta)
                require(
                    same(witness["position"], old_witness["position"])
                    and same(value, old_witness["value"]),
                    "BH point witness differs",
                )
                require(
                    ("violation" if abs(value) > 1 else "within") == old_witness["status"],
                    "BH witness status differs",
                )
                if abs(value) > 1:
                    violated.append(i)
                witnesses += 1
            require(violated == old_refined["violating_indices"], "BH violation indices differ")
            candidates += 1
        require(len(point["menus"]) == len(refined["menus"]) == 5, "five point menus")
        for menu, old_menu in zip(point["menus"], refined["menus"], strict=True):
            require(
                menu["id"] == old_menu["id"] and menu["position_ids"] == old_menu["position_ids"],
                "BH menu identity differs",
            )
            for layer in ("old", "inner", "outer"):
                require(
                    same(_point_entries(menu[layer], corners), old_menu[layer]),
                    "BH point hypothesis set differs",
                )
                summary = menu["target_sets"][layer]
                require(
                    same(_point_targets(summary), old_menu[layer + "_targets"]),
                    "BH point target set differs",
                )
                if layer != "old":
                    hull = summary["hull"]
                    interval = (
                        None
                        if hull is None
                        else {
                            "minimum": hull[0],
                            "maximum": hull[1],
                            "width": hull[1] - hull[0],
                        }
                    )
                    require(same(interval, old_menu[layer + "_range"]), "BH point hull differs")
            for key in (
                "existence_status",
                "target_status",
                "hypothesis_set_status",
                "target_set_status",
            ):
                require(menu[key] == old_menu[key], "BH point set status differs")
            menus += 1
    require(
        (
            len(report["positions"]),
            len(report["cases"]),
            candidates,
            menus,
            branches,
            coefficients,
            witnesses,
        )
        == (6, 7, 42, 35, 1568, 1890, 378),
        "BH restriction coverage differs",
    )
    return {
        "status": "matched",
        "positions": 6,
        "cases": 7,
        "candidates": candidates,
        "menus": menus,
        "branches": branches,
        "coefficients": coefficients,
        "witnesses": witnesses,
    }


def analysis(freeze_path=FREEZE_PATH):
    before = _frozen(freeze_path)
    report = compare_routes(freeze_path)
    result = encode(
        {
            "mathematics": report,
            "bh_restriction": _bh_restriction(report),
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
        "schema": "QR-05BI-evidence-v1",
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
    require(evidence["schema"] == "QR-05BI-evidence-v1", "unknown evidence version")
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
        print(
            json.dumps(
                {
                    "status": "captured" if args.capture else "replayed",
                    "positions": len(report["positions"]),
                    "cases": len(report["cases"]),
                    "budgets": sum(len(case["budgets"]) for case in report["cases"]),
                    "hypothesis_intervals": sum(
                        len(budget["positions"])
                        for case in report["cases"]
                        for budget in case["budgets"]
                    ),
                    "menus": sum(
                        len(budget["menus"])
                        for case in report["cases"]
                        for budget in case["budgets"]
                    ),
                    "affine_branches": sum(
                        len(case["law_family"]["rows"]) for case in report["cases"]
                    ),
                    "sources": len(result["sources"]),
                    "artifact": identity(path),
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
