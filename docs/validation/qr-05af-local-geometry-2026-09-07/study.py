"""QR-05AF private supplied-geometry producer and exact record-local comparison.

Coordinates/full orders remain private to the producer and independent auditor.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import itertools
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
SCHEMA = "det8-qr05af-results-v1"
BASE_COMMIT = "7109ae7e0d46598424484aa8f0a74dae07d4b875"
SOURCES = (
    "README.md",
    "geometry.py",
    "reference_qr05af.py",
    "study.py",
    "test_qr05af.py",
    "test_capture.py",
    "audit_json.py",
)
AD_PRIOR = "qr-05ad-continuous-retention-2026-09-07/results.json"
AD_BYTES = 5003206
AD_SHA = "099c9df18db91545fdd3a08a383e2e4ed96bf5734f6b80a9e492c3bc954c611a"
AC_PRIOR = "qr-05ac-replacement-envelope-2026-09-07/results.json"
AC_BYTES = 1783649
AC_SHA = "3fc5a502c214ba408e5f539133156b0ad81a2ef243545645dc980e7936932c18"
AB_PRIOR = "qr-05ab-replacement-stress-2026-09-07/results.json"
AB_BYTES = 1805554
AB_SHA = "7cbe2668d5b022f73207502bab214078b911e25d25a3826918b916e967643009"
AA_PRIOR = "qr-05aa-uncertainty-decisions-2026-09-07/results.json"
AA_BYTES = 112206
AA_SHA = "bf5661984f9df4cb111fbe97061035967de9f7516a26154abefc7d1d3a49c424"
Z_PRIOR = "qr-05z-fixed-attenuation-2026-09-07/results.json"
Z_BYTES = 31075315
Z_SHA = "7828dafe766ae4cef9e2fd8dcc6181079fe936e8720a70367598aaf3bcbb8ccc"
Y_PRIOR = "qr-05y-explicit-fallback-2026-09-07/results.json"
Y_BYTES = 16474309
Y_SHA = "c4189b0f1bb0df4bb3e5f14c1969ede0ee754f59b4bc99e89aeac8d6b065891f"
X_PRIOR = "qr-05x-noise-misspecification-2026-09-07/results.json"
X_BYTES = 8842933
X_SHA = "1bf12e668ccaaeb20da78d849ae138ffcce2cc32e14be57f286169c74a4734c4"
W_PRIOR = "qr-05w-noisy-readouts-2026-09-07/results.json"
W_BYTES = 6756094
W_SHA = "05b20faf7feae7327113ace9168540d61db0e0e6bebae268819b2b84847cce8a"
LEVELS = [[0, 1], [1, 2], [3, 4], [1, 1]]
MAX_CAPTURE_BYTES = 64 * 1024 * 1024
MAX_WORKING_BYTES = 128 * 1024 * 1024

AE_PRIOR = "qr-05ae-history-safety-2026-09-07/results.json"
AE_SHA = "5b7946512ea77e076387a25d5cf46c30d25a42d37fdd66ae39a4edadb179bbde"

PRIORS = {
    AE_PRIOR: AE_SHA,
    AD_PRIOR: AD_SHA,
    AC_PRIOR: AC_SHA,
    AB_PRIOR: AB_SHA,
    AA_PRIOR: AA_SHA,
    Z_PRIOR: Z_SHA,
    Y_PRIOR: Y_SHA,
    X_PRIOR: X_SHA,
    W_PRIOR: W_SHA,
    "qr-05v-readout-value-2026-09-06/results.json": "eceb01f49624f3d5ebb5dc8041074aa04b62d8408d4a7117979fb1c6b9823ff7",
    "qr-05u-partial-observation-2026-09-06/results.json": "a2cf4ae0bb31934c3c1aeab7071fb6f675d90d9f0b1a5c2776282e926e3e5eee",
    "qr-05t-local-refinement-2026-09-06/results.json": "f7bf6db5dd822c27a3087c6ad48af3ae76fdce653536cff8d381bfae905a5fe8",
    "qr-05s-local-deletion-2026-09-06/results.json": "8caa59a1921dc7fb46a38e44058bfe9f2ac5608c1f2ed05e5dc8ff063ab7e3b3",
    "qr-05r-deletion-profile-2026-09-06/results.json": "cfec27d60d605ec142af96f8931e0e90b3c5ca92c72389ce8e0d84ef8b444001",
    "qr-05q-three-layer-portability-2026-09-06/results.json": "1e9b9443ee5d55cd888d5ea62e594fad197ca0baeecfee1f1efac34ada8125aa",
    "qr-05p-minimal-summary-2026-09-06/results.json": "c43435c4916e5c15efb373ff70795ed733d7c4e360ebec4e9a1b32f4e050b048",
    "qr-05o-path-observable-2026-09-06/results.json": "3364b36813f745a645d78d6d30caa292778da986cb6d1140f108a0fd4b945eb1",
    "qr-05n-domain-portability-2026-09-06/results.json": "f2d666285afef41cd8a7f977399d3626a620da39174967a38047714f5f26f93e",
    "qr-05m-observable-realization-2026-09-06/results.json": "79cb515022fdb3bb2c918a469c1ac5ffdf98a6dd18cdd289f8030fc7a38f1543",
    "qr-05l-adversarial-refinement-2026-09-06/results.json": "0df1b47e1219191783a9ec229540fd433e2129121ce2c5f6e5262e5f3c00e0ff",
    "qr-05k-recursive-closure-2026-09-06/results.json": "46d93f643c443b75ef425349cff11d7f3c437a79921e7e1ee94610998bd1a501",
    "qr-05j-uncertainty-contract-2026-09-06/results.json": "dc8f80f40861107dd7a5ee378c9813a90c1981a3c2e7e14ee343163e9d88c333",
    "qr-05i-analytic-portability-2026-09-06/results.json": "9742e602b037ce74611e7801256f86752f584438a80f9dac6c823acef671e798",
    "qr-05h-law-portability-2026-09-06/results.json": "e6d5f06d765ccca7a1da1cef15d12bc15a3287463ec3cce3732aab75af613b3a",
    "qr-05g-predictive-compression-2026-09-06/results.json": "62b13d1c46efcd5552596f37ba9ec5ab00f8e9708bab19f811cc0a0a357ffb74",
    "qr-01-quantum-records-2026-09-05/results.json": "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b",
    "qr-02-record-coarse-graining-2026-09-05/results.json": "b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c",
    "qr-03-predictive-histories-2026-09-05/results.json": "2b92b7bd42aa9cde29722269c1a31f339e37b217d1256e50d8ea0ee34d8188c2",
    "qr-04-adaptive-causal-records-2026-09-05/results.json": "a5dc5f5e96a189ae8fd5648334e630fd4c24f6cee2fa805a45d32522bc0bcd70",
    "qr-05a-quantum-births-2026-09-05/results.json": "e0c2676ae33b36dde3edb2697ac252330ad801006fe8420acd8cfb94b87c9479",
    "qr-05b-order-summaries-2026-09-05/results.json": "2fe3fd939dcc242ee2a6b8c4abc9d6904e32bf5072cf638f7d880daaeaf2e03b",
    "qr-05c-coarse-dynamics-2026-09-05/results.json": "4f7bb191e64db6bb24886cc1211cb83186d7e24f77599e56e25539c100f4dde1",
    "qr-05d-geometric-correspondence-2026-09-05/results.json": "ea3404f9401573c833965fc259b0f01dc28e3e3968ef79b4b3438e6535cd1238",
    "qr-05d-geometric-correspondence-2026-09-05/results-v2.json": "18499d8a126a3677fb0f0e54a98659df7934c7429c39cc0f531adfc063d40b32",
    "qr-05f-two-stage-2026-09-06/results.json": "0fffba7f9d8549b2e12d90551c82dc72e0ead7f4010923578af610e055683917",
    "qr-05e-sampling-aware-2026-09-06/results.json": "362e7f0c00f00491cd3820fd840faca63b244ed4a0c2156bcb3d0924baa52f41",
}


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
        raw = plain_bytes(HERE.parent / name)
        require(digest(raw) == sha, "prior artifact changed")
        result[name] = {"bytes": len(raw), "sha256": sha}
    return result


def prior_json(name):
    raw = plain_bytes(HERE.parent / name)
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


def retained_bits(value):
    if type(value) is dict:
        return max((retained_bits(v) for v in value.values()), default=0)
    if type(value) is list:
        return max((retained_bits(v) for v in value), default=0)
    if type(value) is int:
        return abs(value).bit_length()
    if type(value) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value):
        v = F(value)
        return max(abs(v.numerator).bit_length(), v.denominator.bit_length())
    return 0


def require_wire(value):
    """Native validation with per-call DAG accounting before serialization.

    Expanded value nodes lower-bound JSON bytes. Repeated references count
    each occurrence, but completed subtrees are walked only once. Depth is
    safely above valid AF schemas, including evidence envelopes.
    """
    active, completed = set(), {}
    pending = [(value, 0, False)]
    while pending:
        item, depth, leaving = pending.pop()
        identity = id(item)
        if leaving:
            children = item if type(item) is list else item.values()
            nodes, height = 1, 0
            for child in children:
                count, child_height = (
                    completed[id(child)] if type(child) in (list, dict) else (1, 0)
                )
                nodes += count
                height = max(height, child_height + 1)
                require(nodes <= MAX_WORKING_BYTES, "expanded wire exceeds working byte cap")
            completed[identity] = nodes, height
            active.remove(identity)
            continue
        require(depth <= 128, "wire exceeds bounded schema depth")
        if item is None or type(item) in (bool, int, str):
            continue
        require(type(item) in (list, dict), "mathematical suite must use native exact JSON types")
        require(identity not in active, "cyclic wire container")
        if identity in completed:
            require(depth + completed[identity][1] <= 128, "wire exceeds bounded schema depth")
            continue
        if type(item) is dict:
            require(all(type(key) is str for key in item), "wire keys must be strings")
        active.add(identity)
        pending.append((item, depth, True))
        children = item if type(item) is list else item.values()
        pending.extend((child, depth + 1, False) for child in children)


def canonical(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


def require_same_wire(left, right, message):
    require_wire(left)
    require_wire(right)
    require(canonical(left) == canonical(right), message)


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
        require(len(before) <= MAX_CAPTURE_BYTES, "artifact byte cap")
        existing = json.loads(before)
        require(
            type(existing) is dict
            and set(existing)
            == {"schema_version", "source_ledger", "prior_artifacts", "suite", "runtime"}
            and existing["schema_version"] == SCHEMA,
            "unrecognized result schema",
        )
        require(canonical(existing) == before, "result is not canonical")
        require_same_wire(existing["source_ledger"], frozen, "source identity changed")
        require_same_wire(existing["prior_artifacts"], previous, "prior identity changed")
    started = time.perf_counter()
    suite = run_suite()
    require_wire(suite)
    require(retained_bits(suite) <= 4096, "retained suite component bit bound")
    require_same_wire(suite, json.loads(canonical(suite)), "aggregate wire round trip differs")
    elapsed = time.perf_counter() - started
    require(ledger() == frozen and priors() == previous, "source/prior changed during execution")
    if args.verify:
        require_same_wire(existing["suite"], suite, "exact replay differs")
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
            "scope": "suite and internal exact JSON checks; excludes final report serialization; no application performance claim",
        },
    }
    raw = canonical(report)
    require(len(raw) <= MAX_CAPTURE_BYTES, "artifact byte cap")
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


METHODS = ("raw", "marginal_product", "uniform_rate", "joint_supported")
PACKET_SCOPE = (
    "full_target_support_inferred",
    "source_moments_inferred",
    "geometry_inferred",
    "observation_origin_authenticated",
    "kernel_is_quantum_channel",
)
SUITE_SCOPE = (
    "unknown_geometry_reconstructed",
    "continuum_limit_established",
    "poisson_ensemble_validated",
    "quantum_channel_constructed",
    "gravity_derived",
    "empirical_data_used",
    "ret_integration_tested",
    "unknown_sampling_law_inferred",
)
D_PRIOR = "qr-05d-geometric-correspondence-2026-09-05/results-v2.json"
D_OLD_PRIOR = "qr-05d-geometric-correspondence-2026-09-05/results.json"
E_PRIOR = "qr-05e-sampling-aware-2026-09-06/results.json"


def fraction(pair):
    require(type(pair) is list and len(pair) == 2, "native fraction pair")
    a, b = pair
    require(type(a) is int and type(b) is int and b > 0, "native fraction components")
    value = F(a, b)
    require([value.numerator, value.denominator] == pair, "reduced fraction")
    require(max(abs(a).bit_length(), b.bit_length()) <= 4096, "fraction component cap")
    return value


def wire(value):
    value = F(value)
    result = [value.numerator, value.denominator]
    fraction(result)
    return result


def vector(values):
    return [wire(v) for v in values]


def matrix(values):
    return [vector(row) for row in values]


def chain_vertices(past, kept, source, target, degree):
    """Literal tuple-chain test on a received local-index transitive relation."""
    rel = {(kept[i], kept[j]) for j, row in enumerate(past) for i in row}
    return [
        list(vertices)
        for vertices in itertools.combinations(kept, degree)
        if all((a, b) in rel for a, b in zip((source, *vertices), (*vertices, target)))
    ]


def inclusions(masses):
    return [sum((p for s, p in enumerate(masses) if s & t == t), F(0)) for t in range(len(masses))]


def support_mask(vertices, eligible):
    return sum(1 << eligible.index(v) for v in vertices if v in eligible)


def weights(mask, pi, pbar, m):
    product = F(1)
    for bit in range(m):
        if mask & (1 << bit):
            product *= pi[1 << bit]
    return {
        "raw": F(1),
        "marginal_product": 1 / product,
        "uniform_rate": 1 / pbar ** mask.bit_count(),
        "joint_supported": None if pi[mask] == 0 else 1 / pi[mask],
    }


def packet_oracle(problem):
    """Private exact oracle; no geometry or missing source relation is consulted."""
    kept, past = problem["record"]["kept"], problem["record"]["past"]
    eligible = problem["eligible"]
    m, k, p = len(eligible), len(kept), len(problem["probes"])
    masses = [fraction(v) for v in problem["mask_probabilities"]]
    pi = inclusions(masses)
    pbar = sum((pi[1 << b] for b in range(m)), F(0)) / m
    require(all(pi[1 << b] > 0 for b in range(m)), "positive marginal law")
    rho = fraction(problem["density"])
    questions = []
    for probe in problem["probes"]:
        for degree in range(3):
            chains = []
            estimates = dict.fromkeys(METHODS, F(0))
            omitted = 0
            for vertices in chain_vertices(past, kept, probe["source"], probe["target"], degree):
                mask = support_mask(vertices, eligible)
                chains.append(
                    {"vertices": vertices, "eligible_mask": mask, "inclusion": wire(pi[mask])}
                )
                omitted += pi[mask] == 0
                for method, weight in weights(mask, pi, pbar, m).items():
                    if weight is not None:
                        estimates[method] += weight
            scale = F((-1) ** degree, 2 ** (degree + 1)) / rho**degree
            questions.append(
                {
                    "probe": probe["name"],
                    "degree": degree,
                    "scale": wire(scale),
                    "observed_count": len(chains),
                    "observed_chains": chains,
                    "unsupported_observed_terms": omitted,
                    "count_estimates": {method: wire(estimates[method]) for method in METHODS},
                    "coefficient_estimates": {
                        method: wire(scale * estimates[method]) for method in METHODS
                    },
                }
            )
    mask = support_mask(kept, eligible)
    a = sum(row["observed_count"] for row in questions)
    length, i, c, q = 2**m, 3**m, p * (1 + k + k * (k - 1) // 2), 3 * p
    return {
        "input_sha256": digest(canonical(problem)),
        "mask": mask,
        "probability": wire(masses[mask]),
        "possible": masses[mask] > 0,
        "inclusion_probabilities": vector(pi),
        "questions": questions,
        "counts": {
            "events": problem["frame_size"],
            "eligible_events": m,
            "kept_events": k,
            "mask_rows": length,
            "questions": q,
            "inclusion_terms": i,
            "chain_candidates": c,
            "observed_chain_terms": a,
            "estimator_terms": 4 * a,
            "coefficient_evaluations": 4 * q,
            "reserved_estimator_terms": 4 * c,
            "reserved_total_work": length + i + 5 * c + 4 * q,
            "total_work": length + i + c + 4 * a + 4 * q,
        },
        "scope": dict.fromkeys(PACKET_SCOPE, False),
    }


def make_source(name):
    """Private generator: timelike (t,x) inequalities, never an observer service."""
    coords = None
    if name.startswith("mesh3"):
        eps = F(1, 12)
        coords = [(F(0), F(0))]
        coords += [
            ((i + eps * j) / (4 * (1 + eps)), (j + eps * i) / (4 * (1 + eps)))
            for i in range(1, 4)
            for j in range(1, 4)
        ]
        coords += [(F(1), F(1))]
        rho = F(18)
        if name == "mesh3_boost":
            coords = [(2 * u, v / 2) for u, v in coords]
        elif name in ("mesh3_dilate", "mesh3_dilate_wrong_density"):
            coords = [(2 * u, 2 * v) for u, v in coords]
            if name == "mesh3_dilate":
                rho /= 4
        elif name == "mesh3_warp":
            coords = [(u * u, v * v) for u, v in coords]
        else:
            require(name == "mesh3", "unknown geometry source")
        fixed, eligible = [0, 3, 5, 7, 10], [1, 2, 4, 6, 8, 9]
        probe_data = [
            ("whole", 0, 10),
            ("bottom_to_p5", 0, 5),
            ("p5_to_top", 5, 10),
            ("bottom_to_p3", 0, 3),
            ("p3_to_top", 3, 10),
            ("bottom_to_p7", 0, 7),
            ("p7_to_top", 7, 10),
        ]
    else:
        require(name in ("ferrers6", "standard_example3", "chain6"), "unknown abstract source")
        rho = F(12)
        fixed, eligible, probe_data = [0, 7], list(range(1, 7)), [("whole", 0, 7)]
        if name == "ferrers6":
            coords = [(F(0), F(0))]
            coords += [
                (F(u, 16), F(v, 16))
                for u, v in ((2, 6), (4, 4), (6, 2), (3, 14), (5, 12), (14, 10))
            ]
            coords += [(F(1), F(1))]
    if coords is not None:
        tx = [((u + v) / 2, (u - v) / 2) for u, v in coords]
        past = [
            [i for i in range(j) if tx[j][0] - tx[i][0] > abs(tx[j][1] - tx[i][1])]
            for j in range(len(tx))
        ]
    elif name == "chain6":
        past = [list(range(j)) for j in range(8)]
    else:
        past = [[]] + [[0] for _ in range(3)]
        past += [[0] + [i + 1 for i in range(3) if i != j] for j in range(3)]
        past += [list(range(7))]
    kind = "algebraic_only" if coords is None else "whole_volume_calibrated"
    if name == "mesh3_dilate_wrong_density":
        kind = "intentionally_wrong"
    return {
        "name": name,
        "coordinates": None if coords is None else [[wire(u), wire(v)] for u, v in coords],
        "past": past,
        "fixed": fixed,
        "eligible": eligible,
        "probes": [{"name": label, "source": a, "target": b} for label, a, b in probe_data],
        "density": wire(rho),
        "density_kind": kind,
    }


def design_law(name, m):
    masses = []
    for mask in range(2**m):
        size = mask.bit_count()
        if name == "identity":
            p = F(mask == 2**m - 1)
        elif name == "iid_half":
            p = F(1, 2**m)
        elif name == "heterogeneous":
            p = F(1)
            for j in range(m):
                rate = F(1 if j % 2 == 0 else 2, 3)
                p *= rate if mask & (1 << j) else 1 - rate
        elif name == "all_or_none":
            p = F(1, 2) if mask in (0, 2**m - 1) else F(0)
        elif name == "fixed_size2":
            p = F(2, m * (m - 1)) if size == 2 else F(0)
        else:
            require(name == "singleton", "unknown design")
            p = F(1, m) if size == 1 else F(0)
        masses.append(p)
    require(sum(masses, F(0)) == 1, "normalized private design")
    return {"name": name, "mask_probabilities": vector(masses)}


def restrict_past(past, kept):
    return [
        [i for i, old in enumerate(kept[:j]) if old in past[target]]
        for j, target in enumerate(kept)
    ]


def make_packet(source, design, mask, past_override=None):
    kept = sorted(
        source["fixed"] + [v for j, v in enumerate(source["eligible"]) if mask & (1 << j)]
    )
    return {
        "schema_version": "det8-qr05af-problem-v1",
        "family": "qr05af_local_geometry",
        "frame_size": len(source["past"]),
        "fixed": copy.deepcopy(source["fixed"]),
        "eligible": copy.deepcopy(source["eligible"]),
        "probes": copy.deepcopy(source["probes"]),
        "density": copy.deepcopy(source["density"]),
        "mask_probabilities": copy.deepcopy(design["mask_probabilities"]),
        "record": {
            "kept": kept,
            "past": restrict_past(source["past"], kept)
            if past_override is None
            else copy.deepcopy(past_override),
        },
    }


def analyze_packet(problem, engines):
    expected = packet_oracle(problem)
    if engines is None:
        return expected
    before = canonical(problem)
    outputs = []
    for engine in engines:
        outputs.append(engine.analyze(problem))
        require(canonical(problem) == before, "packet mutation")
    require_same_wire(outputs[0], outputs[1], "independent complete public packet equality")
    require_same_wire(outputs[0], expected, "private literal packet oracle")
    return outputs[0]


def population(source, design):
    pi = inclusions([fraction(v) for v in design["mask_probabilities"]])
    rho = fraction(source["density"])
    geometries = None if source["coordinates"] is None else []
    qs = []
    for probe in source["probes"]:
        tau2 = None
        if geometries is not None:
            u, v = [fraction(x) for x in source["coordinates"][probe["source"]]]
            uu, vv = [fraction(x) for x in source["coordinates"][probe["target"]]]
            tau2 = (uu - u) * (vv - v)
            require(uu > u and vv > v, "strictly timelike supplied coordinate probe")
        local = []
        for degree in range(3):
            chain_list = []
            for vertices in chain_vertices(
                source["past"],
                list(range(len(source["past"]))),
                probe["source"],
                probe["target"],
                degree,
            ):
                mask = support_mask(vertices, source["eligible"])
                chain_list.append(
                    {"vertices": vertices, "eligible_mask": mask, "inclusion": wire(pi[mask])}
                )
            missing = [row["vertices"] for row in chain_list if fraction(row["inclusion"]) == 0]
            scale = F((-1) ** degree, 2 ** (degree + 1)) / rho**degree
            target = scale * len(chain_list)
            continuum = None if tau2 is None else (F(1, 2), -tau2 / 8, tau2**2 / 128)[degree]
            local.append(
                {
                    "probe": probe["name"],
                    "degree": degree,
                    "scale": wire(scale),
                    "chains": chain_list,
                    "target_count": len(chain_list),
                    "target_coefficient": wire(target),
                    "supported_count": len(chain_list) - len(missing),
                    "zero_inclusion_chains": missing,
                    "full_target_supported": not missing,
                    "continuum_coefficient": None if continuum is None else wire(continuum),
                    "finite_geometry_error": None
                    if continuum is None
                    else wire(target - continuum),
                }
            )
        qs.extend(local)
        if geometries is not None:
            count_volume = F(local[1]["target_count"]) / rho
            geometries.append(
                {
                    "probe": probe["name"],
                    "source": probe["source"],
                    "target": probe["target"],
                    "tau_squared": wire(tau2),
                    "volume": wire(tau2 / 2),
                    "finite_count_volume": wire(count_volume),
                    "volume_error": wire(count_volume - tau2 / 2),
                }
            )
    return {"questions": qs, "interval_geometry": geometries}


def moments(pop, samples):
    qs = pop["questions"]
    scales = [fraction(q["scale"]) for q in qs]
    targets = [F(q["target_count"]) for q in qs]
    qn = len(qs)
    positive = [
        (fraction(s["analysis"]["probability"]), s["analysis"])
        for s in samples
        if s["analysis"]["possible"]
    ]
    result = {}
    for method in METHODS:
        rows = [
            (p, [fraction(q["count_estimates"][method]) for q in analysis["questions"]])
            for p, analysis in positive
        ]
        mean = [sum((p * values[i] for p, values in rows), F(0)) for i in range(qn)]
        covariance = [
            [
                sum((p * (v[i] - mean[i]) * (v[j] - mean[j]) for p, v in rows), F(0))
                for j in range(qn)
            ]
            for i in range(qn)
        ]
        require(all(covariance[i][i] >= 0 for i in range(qn)), "nonnegative exact variance")
        cc = [[scales[i] * scales[j] * covariance[i][j] for j in range(qn)] for i in range(qn)]
        geometry = None
        if pop["interval_geometry"] is not None:
            geometry = []
            for i, q in enumerate(qs):
                continuum = fraction(q["continuum_coefficient"])
                target = fraction(q["target_coefficient"])
                estimate = mean[i] * scales[i]
                sampling, finite = estimate - target, target - continuum
                require(
                    estimate - continuum == sampling + finite,
                    "complete two-bias geometric decomposition",
                )
                geometry.append(
                    {
                        "probe": q["probe"],
                        "degree": q["degree"],
                        "continuum": wire(continuum),
                        "mean": wire(estimate),
                        "sampling_bias": wire(sampling),
                        "finite_model_discrepancy": wire(finite),
                        "total_discrepancy": wire(estimate - continuum),
                    }
                )
        result[method] = {
            "mean_counts": vector(mean),
            "bias_counts": vector([v - t for v, t in zip(mean, targets, strict=True)]),
            "covariance_counts": matrix(covariance),
            "mean_coefficients": vector([s * v for s, v in zip(scales, mean, strict=True)]),
            "bias_coefficients": vector(
                [s * (v - t) for s, v, t in zip(scales, mean, targets, strict=True)]
            ),
            "covariance_coefficients": matrix(cc),
            "geometry_comparisons": geometry,
        }
    require_same_wire(
        result["joint_supported"]["mean_counts"],
        vector([q["supported_count"] for q in qs]),
        "supported-chain expectation identity",
    )
    return result


def covariance_oracle(pop, design):
    pi = inclusions([fraction(p) for p in design["mask_probabilities"]])
    chains = [
        [c["eligible_mask"] for c in q["chains"] if fraction(c["inclusion"]) > 0]
        for q in pop["questions"]
    ]
    return matrix(
        [
            [
                sum((pi[a | b] / (pi[a] * pi[b]) - 1 for a in left for b in right), F(0))
                for right in chains
            ]
            for left in chains
        ]
    )


def wrong_channel_past(full_past, kept):
    links = [[a for a in row if not any(a in full_past[b] for b in row)] for row in full_past]
    allowed = set(kept)
    reach = {}
    for v in kept:
        predecessors = set(links[v]) & allowed
        reach[v] = (
            predecessors | set().union(*(reach[a] for a in predecessors)) if predecessors else set()
        )
    return [[i for i, a in enumerate(kept[:j]) if a in reach[b]] for j, b in enumerate(kept)]


def hasse_control(source, design, samples, engines):
    total, first = F(0), None
    for sample in samples:
        analysis, packet = sample["analysis"], sample["problem"]
        if not analysis["possible"]:
            continue
        kept = packet["record"]["kept"]
        wrong = wrong_channel_past(source["past"], kept)
        failures = []
        for probe in source["probes"]:
            a, b = kept.index(probe["source"]), kept.index(probe["target"])
            if (a in wrong[b]) != (a in packet["record"]["past"][b]):
                failures.append(probe["name"])
        if failures:
            total += fraction(analysis["probability"])
            if first is None:
                wrong_packet = make_packet(source, design, analysis["mask"], wrong)
                first = {
                    "mask": analysis["mask"],
                    "kept": copy.deepcopy(kept),
                    "past": wrong,
                    "failed_probes": failures,
                    "analysis": analyze_packet(wrong_packet, engines),
                }
    return {"mismatch_probability": wire(total), "first_mismatch": first}


def specifications():
    designs = ("identity", "iid_half", "heterogeneous", "all_or_none", "fixed_size2", "singleton")
    cases = [("mesh3", d) for d in designs]
    cases += [
        (name, d)
        for name in ("mesh3_boost", "mesh3_dilate", "mesh3_dilate_wrong_density", "mesh3_warp")
        for d in ("identity", "iid_half")
    ]
    cases += [
        (name, d) for name in ("ferrers6", "standard_example3") for d in ("identity", "iid_half")
    ]
    return cases + [("ferrers6", "singleton"), ("chain6", "singleton")]


def build_case(name, design_name, engines=None):
    source = make_source(name)
    design = design_law(design_name, len(source["eligible"]))
    pop = population(source, design)
    samples = []
    for mask in range(len(design["mask_probabilities"])):
        packet = make_packet(source, design, mask)
        samples.append({"problem": packet, "analysis": analyze_packet(packet, engines)})
    all_moments = moments(pop, samples)
    formula = covariance_oracle(pop, design)
    require_same_wire(
        formula,
        all_moments["joint_supported"]["covariance_counts"],
        "source-chain union-inclusion covariance identity",
    )
    return {
        "case_id": name + "__" + design_name,
        "source": source,
        "design": design,
        "population": pop,
        "samples": samples,
        "moments": all_moments,
        "joint_covariance_formula": formula,
        "hasse_control": hasse_control(source, design, samples, engines),
        "counts": {
            "events": len(source["past"]),
            "eligible_events": len(source["eligible"]),
            "mask_rows": len(samples),
            "positive_rows": sum(s["analysis"]["possible"] for s in samples),
            "questions": len(pop["questions"]),
            "source_chain_terms": sum(q["target_count"] for q in pop["questions"]),
            "observed_chain_terms": sum(
                s["analysis"]["counts"]["observed_chain_terms"] for s in samples
            ),
            "packet_calls": 2 * len(samples),
        },
    }


def require_equal(left, right, label):
    require_same_wire(left, right, label)
    return True


def packet_count_vectors(case):
    return [[q["count_estimates"] for q in s["analysis"]["questions"]] for s in case["samples"]]


def public_samples_equal(a, b):
    return require_equal(a["samples"], b["samples"], "complete public packets and analyses agree")


def local_geometry_witness(base, other, local_only):
    for i, (a, b) in enumerate(
        zip(
            base["population"]["interval_geometry"],
            other["population"]["interval_geometry"],
            strict=True,
        )
    ):
        if (not local_only or i > 0) and a["volume"] != b["volume"]:
            return {
                "probe": a["probe"],
                "probe_index": i,
                "base_volume": a["volume"],
                "transformed_volume": b["volume"],
                "base_error": a["volume_error"],
                "transformed_error": b["volume_error"],
            }
    raise ValueError("required geometric ambiguity has no differing supplied volume")


def positive_packet_law(case):
    return [
        {"problem": s["problem"], "probability": s["analysis"]["probability"]}
        for s in case["samples"]
        if s["analysis"]["possible"]
    ]


def controls(cases):
    lookup = {c["case_id"]: c for c in cases}
    result = {
        k: {"pairs": []} for k in ("boost", "correct_dilation", "wrong_density", "active_warp")
    }
    for d in ("identity", "iid_half"):
        base = lookup["mesh3__" + d]
        boost = lookup["mesh3_boost__" + d]
        result["boost"]["pairs"].append(
            {
                "design": d,
                "public_samples_equal": public_samples_equal(base, boost),
                "population_equal": require_equal(
                    base["population"], boost["population"], "boost population"
                ),
                "moments_equal": require_equal(
                    base["moments"], boost["moments"], "boost complete moments"
                ),
            }
        )
        dilate = lookup["mesh3_dilate__" + d]
        require_equal(
            packet_count_vectors(base),
            packet_count_vectors(dilate),
            "dilation unchanged count estimates",
        )
        expected_pop = copy.deepcopy(base["population"])
        for q in expected_pop["questions"]:
            for field in (
                "scale",
                "target_coefficient",
                "continuum_coefficient",
                "finite_geometry_error",
            ):
                q[field] = wire(fraction(q[field]) * 4 ** q["degree"])
        for row in expected_pop["interval_geometry"]:
            for field in ("tau_squared", "volume", "finite_count_volume", "volume_error"):
                row[field] = wire(4 * fraction(row[field]))
        require_equal(expected_pop, dilate["population"], "dilation full local population scaling")
        for method in METHODS:
            expected = copy.deepcopy(base["moments"][method])
            for field in ("mean_coefficients", "bias_coefficients"):
                expected[field] = [
                    wire(fraction(v) * 4 ** (i % 3)) for i, v in enumerate(expected[field])
                ]
            expected["covariance_coefficients"] = [
                [wire(fraction(v) * 4 ** (i % 3 + j % 3)) for j, v in enumerate(row)]
                for i, row in enumerate(expected["covariance_coefficients"])
            ]
            for row in expected["geometry_comparisons"]:
                for field in (
                    "continuum",
                    "mean",
                    "sampling_bias",
                    "finite_model_discrepancy",
                    "total_discrepancy",
                ):
                    row[field] = wire(fraction(row[field]) * 4 ** row["degree"])
            require_equal(
                expected, dilate["moments"][method], "complete dilation moment congruence"
            )
        for old, new in zip(base["samples"], dilate["samples"], strict=True):
            expected = copy.deepcopy(old["analysis"])
            expected["input_sha256"] = digest(canonical(new["problem"]))
            for q in expected["questions"]:
                q["scale"] = wire(fraction(q["scale"]) * 4 ** q["degree"])
                q["coefficient_estimates"] = {
                    m: wire(fraction(v) * 4 ** q["degree"])
                    for m, v in q["coefficient_estimates"].items()
                }
            require_equal(expected, new["analysis"], "complete dilation packet coefficient scaling")
        require(
            fraction(dilate["source"]["density"]) == fraction(base["source"]["density"]) / 4,
            "dilation supplied density",
        )
        result["correct_dilation"]["pairs"].append(
            {
                "design": d,
                "count_estimates_equal": True,
                "population_scaling": True,
                "coefficient_packet_scaling": True,
                "complete_moment_congruence": True,
                "squared_length_factor": [4, 1],
            }
        )
        for key, source_name, local_only in (
            ("wrong_density", "mesh3_dilate_wrong_density", False),
            ("active_warp", "mesh3_warp", True),
        ):
            other = lookup[source_name + "__" + d]
            witness = local_geometry_witness(base, other, local_only)
            result[key]["pairs"].append(
                {
                    "design": d,
                    "public_samples_equal": public_samples_equal(base, other),
                    "supplied_geometry_differs": True,
                    "witness": witness,
                }
            )
    a, b = lookup["ferrers6__identity"], lookup["standard_example3__identity"]
    targets = [q["target_coefficient"] for q in a["population"]["questions"]]
    require_equal(
        targets,
        [q["target_coefficient"] for q in b["population"]["questions"]],
        "equal complete endpoint coefficients through z2",
    )
    aa, bb = (
        lookup["ferrers6__iid_half"]["moments"]["joint_supported"],
        lookup["standard_example3__iid_half"]["moments"]["joint_supported"],
    )
    require_equal(aa["mean_counts"], bb["mean_counts"], "equal endpoint count means")
    require(
        canonical(aa["covariance_counts"]) != canonical(bb["covariance_counts"]),
        "unequal endpoint sampling covariance",
    )
    result["endpoint_collision"] = {
        "identity_cases": [a["case_id"], b["case_id"]],
        "finite_coefficients": targets,
        "iid_joint_mean_equal": True,
        "iid_joint_covariance_equal": False,
        "ferrers_iid_pair_variance": aa["covariance_counts"][2][2],
        "S3_iid_pair_variance": bb["covariance_counts"][2][2],
        "embedding_reassessed": False,
    }
    a, b = lookup["ferrers6__singleton"], lookup["chain6__singleton"]
    law = positive_packet_law(a)
    require_equal(
        law, positive_packet_law(b), "identical positive singleton observation packet laws"
    )
    ta, tb = (
        a["population"]["questions"][2]["target_count"],
        b["population"]["questions"][2]["target_count"],
    )
    require(ta != tb, "different singleton hidden pair targets")
    result["singleton_observation_collision"] = {
        "case_ids": [a["case_id"], b["case_id"]],
        "positive_packets_equal": True,
        "full_pair_targets": {"ferrers6": ta, "chain6": tb},
        "full_pair_targets_differ": True,
        "observation_law_sha256": digest(canonical(law)),
    }
    return result


def prior_bridges(cases):
    old_d, current_d, e = (prior_json(n)["suite"] for n in (D_OLD_PRIOR, D_PRIOR, E_PRIOR))
    require_same_wire(old_d, current_d, "D v1/v2 immutable mathematical suite identity")
    ds = {c["analysis"]["case"]: c["analysis"] for c in current_d["cases"]}
    es = {(c["analysis"]["order_name"], c["analysis"]["design"]): c["analysis"] for c in e["cases"]}
    lookup = {c["case_id"]: c for c in cases}
    base = lookup["mesh3__identity"]
    old = ds["mesh3"]
    require_equal(
        base["source"]["coordinates"],
        [[wire(F(v)) for v in row] for row in old["coordinates"]],
        "D mesh3 coordinates",
    )
    rel = [
        [int(i in row) for row in base["source"]["past"]]
        for i in range(len(base["source"]["past"]))
    ]
    require_equal(rel, old["order"]["relation"], "D mesh3 complete order")
    for i, probe in enumerate(base["source"]["probes"][:3]):
        for q in range(3):
            value = wire(
                F(old["order"]["kernel_coefficients"][q][probe["source"]][probe["target"]])
            )
            require_equal(
                value,
                base["population"]["questions"][3 * i + q]["target_coefficient"],
                "D shared local coefficient",
            )
    for name in ("ferrers6", "standard_example3"):
        case = lookup[name + "__identity"]
        for q in range(3):
            require_equal(
                case["population"]["questions"][q]["target_coefficient"],
                wire(F(ds[name]["order"]["endpoint"]["coefficients"][q])),
                "D six-event endpoint coefficient",
            )
        for design in ("identity", "iid_half"):
            new, previous = lookup[name + "__" + design], es[name, design]
            for method in METHODS:
                for field in (
                    "mean_counts",
                    "bias_counts",
                    "mean_coefficients",
                    "bias_coefficients",
                ):
                    require_equal(
                        new["moments"][method][field],
                        vector([F(v) for v in previous["moments"][method][field][:3]]),
                        "E first-three moment vector",
                    )
                for field in ("covariance_counts", "covariance_coefficients"):
                    require_equal(
                        new["moments"][method][field],
                        matrix(
                            [
                                [F(v) for v in row[:3]]
                                for row in previous["moments"][method][field][:3]
                            ]
                        ),
                        "E first-three covariance",
                    )
    for name in ("ferrers6", "chain6"):
        new, old = lookup[name + "__singleton"], es[name, "singleton"]
        newlaw = [
            {
                "kept": s["problem"]["record"]["kept"],
                "past": s["problem"]["record"]["past"],
                "probability": s["analysis"]["probability"],
            }
            for s in new["samples"]
            if s["analysis"]["possible"]
        ]
        oldlaw = [
            {**row, "probability": wire(F(row["probability"]))} for row in old["observation_law"]
        ]
        require_equal(newlaw, oldlaw, "E singleton complete observation law")
        require(
            new["population"]["questions"][2]["target_count"]
            == old["questions"][2]["target_count"],
            "E singleton pair target",
        )
    return {
        "D_v1_v2_mathematical_suite_equal": True,
        "D_mesh3_order_coordinates_match": True,
        "D_shared_mesh3_probe_coefficients_checked": 9,
        "D_ferrers_S3_endpoint_coefficients_checked": 6,
        "E_matched_moment_cases": 4,
        "E_matched_q0_q1_q2_vectors_and_matrices": True,
        "E_singleton_observation_laws_preserved": True,
        "E_singleton_pair_targets_preserved": True,
        "E_other_controls_preserved_by_identity": True,
        "prior_forecasting_math_replayed": False,
    }


def malformed_packets(packet):
    bad = []
    for kind in range(8):
        value = copy.deepcopy(packet)
        if kind == 0:
            value["extra"] = 0
        elif kind == 1:
            value["coordinates"] = []
        elif kind == 2:
            value["record"]["kept"][0] = False
        elif kind == 3:
            value["mask_probabilities"][0] = [1, 1]
        elif kind == 4:
            value["record"]["kept"].remove(value["fixed"][0])
        elif kind == 5:
            # A complete kept identity packet: remove bottom from top, retaining a two-edge path.
            value["record"]["past"][-1].remove(0)
        elif kind == 6:
            value["density"] = [36, 2]
        else:
            value["family"] = "wrong"
        bad.append(value)
    return bad


def assemble_suite(cases, rejected=16):
    require(len(cases) == 20, "frozen case count")
    for case, (name, design) in zip(cases, specifications(), strict=True):
        require(case["case_id"] == name + "__" + design, "fixed case ordering")
    totals = {"cases": len(cases)}
    totals.update({k: sum(c["counts"][k] for c in cases) for k in cases[0]["counts"]})
    require(totals["mask_rows"] == 1280, "complete frozen mask rows")
    wrong_calls = 2 * sum(c["hasse_control"]["first_mismatch"] is not None for c in cases)
    return {
        "cases": cases,
        "controls": controls(cases),
        "prior_bridges": prior_bridges(cases),
        "public_controls": {
            "ordinary_packet_calls": totals["packet_calls"],
            "wrong_channel_packet_calls": wrong_calls,
            "independent_route_equal": True,
            "invalid_calls_rejected": rejected,
        },
        "totals": totals,
        "scope": dict.fromkeys(SUITE_SCOPE, False),
    }


def check_case(case, expected):
    require_same_wire(
        case, expected, "complete private source/design case including all geometry and moments"
    )


def check_suite(suite, expected):
    require_same_wire(suite, expected, "complete native AF suite including scope and prior bridges")


def run_suite():
    engines = (
        load("qr05af_primary", "geometry.py"),
        load("qr05af_reference", "reference_qr05af.py"),
    )
    cases = [build_case(name, design, engines) for name, design in specifications()]
    # All-kept identity packet, not a probability-zero or partial-order mutation accident.
    malformed = malformed_packets(cases[0]["samples"][-1]["problem"])
    rejected = 0
    for engine in engines:
        for packet in malformed:
            try:
                engine.analyze(packet)
            except ValueError:
                rejected += 1
            else:
                raise ValueError("malformed AF packet accepted")
    require(rejected == 16, "all malformed public controls rejected")
    return assemble_suite(cases, rejected)


if __name__ == "__main__":
    main()
