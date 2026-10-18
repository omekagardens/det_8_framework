"""QR-05AI private weighted-kernel orchestration; no historical engine imports."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import platform
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05ai-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05ai.py")
AH = HERE.parent / "qr-05ah-boundary-refinement-2026-09-07/results.json"
AH_ID = {
    "bytes": 14297174,
    "sha256": "49b911c74a2e1428cb3b378ec2bf33c77feb80ab8cab213a26cd005531429bb8",
}
MAX_CAPTURE_BYTES = 96 * 1024 * 1024
MAX_WORKING_BYTES = 128 * 1024 * 1024
FAMILIES = ("grid", "warp", "warp_stale", "boost", "dilate")
SCOPE = (
    "generic_production_API_hardened",
    "unknown_geometry_reconstructed",
    "marks_authenticated",
    "kernel_error_bound_established",
    "continuum_limit_established",
    "cross_level_observation_transport_proved",
    "quantum_channel_constructed",
    "gravity_derived",
    "empirical_data_used",
    "ret_integration_tested",
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def plain_bytes(path):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), "not a plain evidence file")
    require(path.stat().st_size <= MAX_CAPTURE_BYTES, "capture byte cap")
    raw = path.read_bytes()
    require(len(raw) <= MAX_CAPTURE_BYTES, "capture byte cap")
    return raw


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def ident(path):
    raw = plain_bytes(path)
    return {"bytes": len(raw), "sha256": digest(raw)}


def native(value, depth=0):
    require(depth <= 128, "native depth")
    k = type(value)
    if value is None or k in (bool, str):
        return
    if k is int:
        require(abs(value).bit_length() <= 4096, "retained component bits")
        return
    require(k in (list, dict), "native mathematical data required")
    if k is dict:
        require(all(type(key) is str for key in value), "native keys")
    for item in value.values() if k is dict else value:
        native(item, depth + 1)


def canonical(value):
    raw = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")
    require(len(raw) <= MAX_WORKING_BYTES, "working byte cap")
    return raw


def verify_suite(actual, expected):
    native(actual)
    native(expected)
    require(canonical(actual) == canonical(expected), "complete mathematical wire differs")


def frac(pair):
    require(
        type(pair) is list and len(pair) == 2 and all(type(x) is int for x in pair), "fraction pair"
    )
    n, d = pair
    require(d > 0 and math.gcd(n, d) == 1, "reduced fraction")
    return F(n, d)


def wire(value):
    value = F(value)
    return [value.numerator, value.denominator]


def scaled(pair, factor):
    return wire(frac(pair) * factor)


def prior_document():
    require(ident(AH) == AH_ID, "AH artifact changed")
    return json.loads(plain_bytes(AH))


def identities():
    ah = prior_document()
    prior = {str(AH.relative_to(HERE.parent)): AH_ID}
    for name, want in ah["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = {}
    for name, want in ah["source_ledger"].items():
        path = AH.parent / name
        require(ident(path) == want, "AH source changed: " + name)
        ancestors[str(path.relative_to(HERE.parent))] = want
    agpath = HERE.parent / "qr-05ag-local-volume-2026-09-07/results.json"
    ag = json.loads(plain_bytes(agpath))
    for name, want in ag["source_ledger"].items():
        path = agpath.parent / name
        require(ident(path) == want, "AG source changed: " + name)
        ancestors[str(path.relative_to(HERE.parent))] = want
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def load_inputs():
    ah = prior_document()
    cases = ah["suite"]["cases"]
    require(len(cases) == 27, "bounded cases")
    require(sum(len(c["design"]["mask_probabilities"]) for c in cases) == 4032, "bounded masks")
    for c in cases:
        require(
            len(c["source"]["cells"]) <= 8 and len(c["source"]["probes"]) == 5, "bounded source"
        )
        require(len(c["design"]["mask_probabilities"]) <= 256, "bounded design")
    return cases


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05ai_" + name, HERE / filename)
    require(spec is not None and spec.loader is not None, "engine loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scaled_geometry(rows, factor):
    result = copy.deepcopy(rows)
    for row in result:
        row["volume"] = scaled(row["volume"], factor)
        for c in row["cell_clips"]:
            c["volume"] = scaled(c["volume"], factor)
        for pair in row["pair_cells"]:
            for key in ("clipped_product", "causal_integral"):
                pair[key] = scaled(pair[key], factor**2)
        row["pair_discrepancy"] = {
            k: scaled(v, factor**2) for k, v in row["pair_discrepancy"].items()
        }
    return result


def scaled_questions(rows, factor, population=False):
    result = copy.deepcopy(rows)
    for row in result:
        f = factor ** row["degree"]
        for chain in row["chains"]:
            chain["weight"] = scaled(chain["weight"], f)
        if population:
            for key in (
                "supplied_target",
                "geometric_target",
                "continuum_target",
                "supported_target",
                "annotation_error",
                "quadrature_error",
            ):
                row[key] = scaled(row[key], f)
        else:
            row["estimates"] = {k: scaled(v, f) for k, v in row["estimates"].items()}
    return result


def scaled_moments(moments, factor):
    result = copy.deepcopy(moments)
    for values in result.values():
        degrees = [e["degree"] for e in values["errors"]]
        for key in ("mean", "bias"):
            values[key] = [scaled(v, factor**q) for v, q in zip(values[key], degrees, strict=True)]
        values["covariance"] = [
            [scaled(v, factor ** (q + r)) for v, r in zip(row, degrees, strict=True)]
            for row, q in zip(values["covariance"], degrees, strict=True)
        ]
        for row in values["errors"]:
            for key in ("sampling_bias", "annotation_error", "quadrature_error", "total_error"):
                row[key] = scaled(row[key], factor ** row["degree"])
    return result


def equal(left, right):
    return canonical(left) == canonical(right)


def transform_control(base, moved, factor):
    require(equal(base["design"], moved["design"]), "scaling design")
    require(equal(base["source"]["past"], moved["source"]["past"]), "scaling order")
    sample_ok = True
    for a, b in zip(base["samples"], moved["samples"], strict=True):
        require(
            a["mask"] == b["mask"] and a["probability"] == b["probability"], "scaling sample law"
        )
        record = copy.deepcopy(a["record"])
        for mark in record["marks"]:
            mark["volume"] = scaled(mark["volume"], factor)
        packet = {
            "frame_size": len(base["source"]["past"]),
            "fixed": base["source"]["fixed"],
            "eligible": base["source"]["eligible"],
            "probes": base["source"]["probes"],
            "mask_probabilities": base["design"]["mask_probabilities"],
            "record": record,
        }
        sample_ok &= equal(record, b["record"])
        sample_ok &= equal(a["possible"], b["possible"])
        sample_ok &= digest(canonical(packet)) == b["packet_sha256"]
        sample_ok &= equal(scaled_questions(a["questions"], factor), b["questions"])
    return {
        "level": base["level"],
        "volume_factor": wire(factor),
        "full_geometry_scaling": equal(
            scaled_geometry(base["geometry"], factor), moved["geometry"]
        ),
        "full_population_scaling": equal(
            scaled_questions(base["population"], factor, True), moved["population"]
        ),
        "sample_coefficients_scaling": sample_ok,
        "full_moment_scaling": equal(scaled_moments(base["moments"], factor), moved["moments"]),
    }


def controls(cases):
    by = {(c["source"]["name"], c["level"], c["design"]["name"]): c for c in cases}
    refinement = []
    for source in FAMILIES:
        for level in range(2):
            a, b = (by[(source, "l" + str(k), "identity")] for k in (level, level + 1))
            for qi, (g, h) in enumerate(zip(a["geometry"], b["geometry"], strict=True)):
                p, q = a["population"][3 * qi + 2], b["population"][3 * qi + 2]
                refinement.append(
                    {
                        "source": source,
                        "coarse": a["level"],
                        "fine": b["level"],
                        "probe": g["probe"],
                        "geometric_coefficient_change": wire(
                            frac(q["geometric_target"]) - frac(p["geometric_target"])
                        ),
                        "signed_error_change": wire(
                            frac(q["quadrature_error"]) - frac(p["quadrature_error"])
                        ),
                        "absolute_error_change": wire(
                            abs(frac(q["quadrature_error"])) - abs(frac(p["quadrature_error"]))
                        ),
                        "within_cell_change": wire(
                            frac(h["pair_discrepancy"]["within_cell_integral"])
                            - frac(g["pair_discrepancy"]["within_cell_integral"])
                        ),
                    }
                )
    out = {"refinement": refinement, "boost": [], "dilation": [], "stale_marks": []}
    for level in ("l0", "l1", "l2"):
        base = by[("grid", level, "identity")]
        for key, source, factor in (("boost", "boost", F(1)), ("dilation", "dilate", F(4))):
            row = transform_control(base, by[(source, level, "identity")], factor)
            require(all(v for k, v in row.items() if type(v) is bool), "transformation comparison")
            out[key].append(row)
        stale = by[("warp_stale", level, "identity")]
        row = {
            "level": level,
            "public_samples_equal_grid": equal(stale["samples"], base["samples"]),
            "geometric_pair_data_equal_warp": equal(
                stale["geometry"], by[("warp", level, "identity")]["geometry"]
            ),
        }
        require(
            row["public_samples_equal_grid"] and row["geometric_pair_data_equal_warp"],
            "stale comparison",
        )
        out["stale_marks"].append(row)
    return out


def ah_bridges(cases, previous):
    require(len(cases) == len(previous), "AH case count")
    for c, old in zip(cases, previous, strict=True):
        require(c["case_id"] == old["case_id"] and c["level"] == old["level"], "AH case identity")
        verify_suite(c["source"], old["source"])
        verify_suite(c["design"], old["design"])
        require(len(c["samples"]) == len(old["samples"]), "AH sample count")
        for sample, prior in zip(c["samples"], old["samples"], strict=True):
            verify_suite(sample["record"], prior["problem"]["record"])
            for field in ("mask", "probability", "possible"):
                verify_suite(sample[field], prior["analysis"][field])
            packet = {
                k: prior["problem"][k]
                for k in (
                    "frame_size",
                    "fixed",
                    "eligible",
                    "probes",
                    "mask_probabilities",
                    "record",
                )
            }
            require(sample["packet_sha256"] == digest(canonical(packet)), "AH packet hash")
            require(len(sample["questions"]) == 15, "complete sample questions")
            for qi in range(5):
                current = sample["questions"][3 * qi + 1]
                before = prior["analysis"]["questions"][qi]
                require(current["probe"] == before["probe"], "AH sample probe")
                verify_suite(
                    [
                        {
                            "event": t["vertices"][0],
                            "volume": t["weight"],
                            "inclusion": t["inclusion"],
                        }
                        for t in current["chains"]
                    ],
                    before["observed_cells"],
                )
                for method, prior_method in (("raw", "raw"), ("joint_supported", "inclusion")):
                    require(
                        current["estimates"][method]
                        == scaled(before["estimates"][prior_method], F(-1, 4)),
                        "AH sample linear estimate",
                    )
        for qi in range(5):
            p, g = c["population"][3 * qi + 1], c["geometry"][qi]
            expected = {
                "probe": p["probe"],
                "members": [t["vertices"][0] for t in p["chains"]],
                "overlaps": g["cell_clips"],
                "supplied_target": scaled(p["supplied_target"], -4),
                "geometric_target": scaled(p["geometric_target"], -4),
                "continuum_volume": scaled(p["continuum_target"], -4),
                "annotation_error": scaled(p["annotation_error"], -4),
                "quadrature_error": scaled(p["quadrature_error"], -4),
            }
            verify_suite(expected, old["population"][qi])
        for method, oldmethod in (("raw", "raw"), ("joint_supported", "inclusion")):
            a, b = c["moments"][method], old["moments"][oldmethod]
            for key in ("mean", "bias"):
                verify_suite(
                    [a[key][3 * i + 1] for i in range(5)], [scaled(v, F(-1, 4)) for v in b[key]]
                )
            verify_suite(
                [[a["covariance"][3 * i + 1][3 * j + 1] for j in range(5)] for i in range(5)],
                [[scaled(v, F(1, 16)) for v in row] for row in b["covariance"]],
            )
    return {
        "AH_case_ids": [c["case_id"] for c in cases],
        "AH_sources_designs_equal": True,
        "AH_sample_records_equal": True,
        "AH_linear_populations_equal": True,
        "AH_raw_inclusion_means_covariances_equal": True,
        "AF_math_replayed": False,
        "other_prior_math_replayed": False,
    }


def assemble_suite(cases, ah_cases):
    require(len(cases) == 27, "bounded complete case count")
    for case in cases:
        require(
            len(case["geometry"]) == 5 and len(case["population"]) == 15, "complete case questions"
        )
        verify_suite(case["union_covariance"], case["moments"]["joint_supported"]["covariance"])
    totals = {"cases": len(cases)}
    for key in cases[0]["counts"]:
        values = [c["counts"][key] for c in cases]
        totals[key] = max(values) if key == "max_union_size" else sum(values)
    return {
        "cases": cases,
        "controls": controls(cases),
        "prior_bridges": ah_bridges(cases, ah_cases),
        "totals": totals,
        "scope": dict.fromkeys(SCOPE, False),
    }


def run_suite(route="compare"):
    require(route in ("compare", "primary", "reference"), "unknown route")
    previous = load_inputs()
    names = ("primary", "reference") if route == "compare" else (route,)
    engines = [load_engine(name) for name in names]
    cases = []
    for old in previous:
        outputs = []
        for engine in engines:
            source, design = copy.deepcopy(old["source"]), copy.deepcopy(old["design"])
            out = engine.build_case(old["case_id"], old["level"], source, design)
            verify_suite(source, old["source"])
            verify_suite(design, old["design"])
            outputs.append(out)
        if len(outputs) == 2:
            verify_suite(outputs[0], outputs[1])
        cases.append(outputs[0])
    result = assemble_suite(cases, previous)
    native(result)
    canonical(result)
    return result


def capture(path=None, route="compare", verify=False):
    path = Path(RESULT if path is None else path)
    require(
        sys.flags.isolated and sys.pycache_prefix,
        "isolated Python/external bytecode cache required",
    )
    cache = Path(sys.pycache_prefix).resolve()
    require(
        cache != Path(cache.anchor) and not cache.is_relative_to(ROOT), "external bytecode cache"
    )
    if not verify and (path.exists() or path.is_symlink()):
        raise FileExistsError("evidence exists; never overwrite")
    before = identities()
    raw_before = plain_bytes(path) if verify else None
    if verify:
        existing = json.loads(raw_before)
        require(
            type(existing) is dict
            and set(existing)
            == {
                "schema_version",
                "source_ledger",
                "prior_artifacts",
                "ancestor_sources",
                "suite",
                "runtime",
            },
            "capture fields",
        )
        require(existing["schema_version"] == SCHEMA, "capture schema")
        require(canonical(existing) == raw_before, "noncanonical capture")
        for key, value in before.items():
            verify_suite(existing[key], value)
    start = time.perf_counter()
    suite = run_suite(route)
    native(suite)
    suite_raw = canonical(suite)
    seconds = time.perf_counter() - start
    verify_suite(before, identities())
    if verify:
        verify_suite(suite, existing["suite"])
        require(plain_bytes(path) == raw_before, "capture changed during replay")
        raw = raw_before
    else:
        report = {
            "schema_version": SCHEMA,
            **before,
            "suite": suite,
            "runtime": {
                "route": route,
                "python": sys.version,
                "platform": platform.platform(),
                "executable": sys.executable,
                "isolated": bool(sys.flags.isolated),
                "optimized": sys.flags.optimize,
                "bytecode_cache": str(cache),
                "suite_seconds": seconds,
                "rss_high_water_at_suite_end": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "rss_units": "bytes" if sys.platform == "darwin" else "KiB",
                "scope": "verification timing; excludes final serialization; not application benchmark",
            },
        }
        raw = canonical(report)
        require(len(raw) <= MAX_CAPTURE_BYTES, "capture byte cap")
        with path.open("xb") as stream:
            stream.write(raw)
        require(plain_bytes(path) == raw, "capture readback")
    verify_suite(before, identities())
    return {
        "status": "VERIFIED_EXACT_REPLAY" if verify else "CREATED_EXACT_FINITE_RESULT",
        "route": route,
        "path": str(path),
        "bytes": len(raw),
        "sha256": digest(raw),
        "suite_bytes": len(suite_raw),
        "suite_sha256": digest(suite_raw),
        "seconds": seconds,
        "totals": suite["totals"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--route", choices=("compare", "primary", "reference"), default="compare")
    parser.add_argument("--artifact", type=Path, default=RESULT)
    args = parser.parse_args()
    print(json.dumps(capture(args.artifact, args.route, args.verify)))


if __name__ == "__main__":
    main()
