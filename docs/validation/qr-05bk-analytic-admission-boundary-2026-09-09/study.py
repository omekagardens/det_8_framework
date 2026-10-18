"""Source-bound QR-05BK orchestration; no physics or fixed computation at import."""

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
PROTOCOL_SHA256 = "924461cf18794bae1e6b022b92550f544246aad7595b59b8afb535968f7a86f5"
BJ_DIRECTORY = ROOT.parent / "qr-05bj-fixed-interval-refinement-2026-09-09"
BJ_IDENTITIES = {
    "README.md": "d9dcfadd19d06281672d1007d41b502312498fdd1f9d76f82dbbddde0eec93ec",
    "RESULTS.md": "2256dd9983f507caf0136cfaa6a7e19f57333b7eb9d2365930abae0bca0bf60f",
    "protocol.json": "533e807f943f1e37c7231f86300cf6b85d62a06b077ba5541f7d841549d00967",
    "source-freeze.json": "f8a4f5935abf7b99212878e794fe17f0caccbce82d4585edf574b2b067e19fcc",
    "results.json": "04c2092edca46a329e73798a6701985b83a9870b3916c7ff59f65d3396ec969f",
}
PROTOCOL_FIELDS = [
    "study",
    "version",
    "base_commit",
    "classification",
    "model",
    "boundary",
    "comparison",
    "no_claims",
]
BOUNDARY = {
    "case_id": "asymmetric",
    "A": ["3", "-1"],
    "C": ["5", "2"],
    "D": ["0", "1", "-1"],
    "delta": ["-1", "2"],
    "target_offset": "13/216",
    "target_slope": "1/144",
    "isolation": {"depth": 24, "max_depth": 64, "max_nodes": 4096, "max_degree": 12},
    "polynomial_order": "ascending; exact Fractions; primitive integer leading-positive squarefree defining polynomial",
    "root_filter": "v>1/2 and k>0; k=C*D-2*A*(A+C)*delta",
    "endpoint_rule": "exact beta rational image; beta-affine endpoints; unresolved rational-enclosure comparison raises",
    "negative_rule": "data-restricted negative BJ inner and outer must agree; do not solve the global negative boundary",
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
    if left is None or type(left) in (str, int, bool, Fraction):
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
    require(protocol["study"] == "QR-05BK", "study differs")
    require(type(protocol["version"]) is int and protocol["version"] == 1, "version differs")
    require(
        protocol["base_commit"] == "e608e472b9fd6251e294a988010ee4c1bc04f183", "base commit differs"
    )
    require(raw_same(protocol["boundary"], BOUNDARY), "boundary contract differs")
    model_data = _read_bounded(BJ_DIRECTORY / "protocol.json")
    require(
        _bytes_identity(model_data)["sha256"] == BJ_IDENTITIES["protocol.json"],
        "preceding BJ protocol identity changed",
    )
    expected_model = _parse_json(model_data)
    require(raw_same(protocol["model"], expected_model), "complete BJ input differs")
    return protocol


def source_identities():
    load_protocol()
    for name, digest in BJ_IDENTITIES.items():
        require(
            identity(BJ_DIRECTORY / name)["sha256"] == digest,
            "preceding BJ source changed: " + name,
        )
    files = [
        ROOT / name
        for name in (
            "README.md",
            "protocol.json",
            "quantum.py",
            "reference.py",
            "study.py",
            "test_qr05bk.py",
        )
    ] + [BJ_DIRECTORY / name for name in BJ_IDENTITIES]
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
        "schema": "QR-05BK-source-freeze-v1",
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
    require(freeze["schema"] == "QR-05BK-source-freeze-v1", "unknown freeze version")
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
    module = ModuleType("_qr05bk_" + name)
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


def _bj_restriction(report):
    """Compare whole recomputed BJ mathematics, without replaying its BI lifecycle."""
    data = _read_bounded(BJ_DIRECTORY / "results.json")
    require(
        _bytes_identity(data)["sha256"] == BJ_IDENTITIES["results.json"],
        "preceding BJ capture identity changed",
    )
    previous = _parse_json(data)
    require(
        type(report) is dict and set(report) == {"bj_model", "certificate", "resolution"},
        "current report fields differ",
    )
    current = report["bj_model"]
    require(raw_same(current, current), "unsupported native baseline report")
    require(same(current, previous["analysis"]["mathematics"]), "complete BJ mathematics differs")
    cases = current["refinement"]
    budgets = [budget for case in cases for budget in case["budgets"]]
    receipt = {
        "status": "matched",
        "positions": len(current["bi_model"]["positions"]),
        "cases": len(cases),
        "budgets": len(budgets),
        "hypothesis_intervals": sum(len(budget["positions"]) for budget in budgets),
        "menus": sum(len(budget["menus"]) for budget in budgets),
        "affine_patches": sum(len(case["constraints"]["patches"]) for case in cases),
        "affine_coefficients": sum(
            len(row)
            for case in cases
            for patch in case["constraints"]["patches"]
            for row in patch["coefficients"]
        ),
        "affine_witnesses": sum(len(case["constraints"]["witnesses"]) for case in cases),
        "exact_menus": sum(
            menu["target_set_status"] == "exact" for budget in budgets for menu in budget["menus"]
        ),
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
                "affine_patches": 112,
                "affine_coefficients": 1008,
                "affine_witnesses": 175,
                "exact_menus": 103,
            },
        ),
        "BJ coverage differs",
    )
    return receipt


def analysis(freeze_path=FREEZE_PATH):
    before = _frozen(freeze_path)
    report = compare_routes(freeze_path)
    result = encode(
        {
            "mathematics": report,
            "bj_restriction": _bj_restriction(report),
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
        "schema": "QR-05BK-evidence-v1",
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
    require(evidence["schema"] == "QR-05BK-evidence-v1", "unknown evidence version")
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
                    "certificate": report["certificate"]["status"],
                    "beta_interval": report["certificate"]["beta_interval"],
                    "summary": report["resolution"]["summary"],
                    "sources": len(result["sources"]),
                    "artifact": identity(path),
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
