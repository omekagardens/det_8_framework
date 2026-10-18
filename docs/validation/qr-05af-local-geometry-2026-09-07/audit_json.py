"""Independent stdlib JSON-only QR-05AF geometry/observation audit.

No engine, runner or test imports. Sources are read only as identity bytes.
The narrow packet oracle has no coordinate or hidden-source access. Separate
raw generation and full-law checks supply moments and geometry comparisons.
"""

import argparse
import hashlib
import itertools
import json
import math
import re
import sys
import time
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DDIR = ROOT / "docs/validation/qr-05d-geometric-correspondence-2026-09-05"
EDIR = ROOT / "docs/validation/qr-05e-sampling-aware-2026-09-06"
AEDIR = ROOT / "docs/validation/qr-05ae-history-safety-2026-09-07"
AE_PRIOR = "qr-05ae-history-safety-2026-09-07/results.json"
AE_ID = {
    "bytes": 6327929,
    "sha256": "5b7946512ea77e076387a25d5cf46c30d25a42d37fdd66ae39a4edadb179bbde",
}
D1_ID = {
    "bytes": 2523350,
    "sha256": "ea3404f9401573c833965fc259b0f01dc28e3e3968ef79b4b3438e6535cd1238",
}
D2_ID = {
    "bytes": 2523927,
    "sha256": "18499d8a126a3677fb0f0e54a98659df7934c7429c39cc0f531adfc063d40b32",
}
E_ID = {
    "bytes": 6400976,
    "sha256": "362e7f0c00f00491cd3820fd840faca63b244ed4a0c2156bcb3d0924baa52f41",
}
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
COUNTS = defaultdict(int)


def check(condition, message):
    COUNTS["checks"] += 1
    if not condition:
        raise RuntimeError(message)


def eq(left, right, message):
    check(left == right, message)


def canon(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def digest(value):
    return hashlib.sha256(canon(value)).hexdigest()


def ident(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def native_tree(value, depth=0):
    check(depth <= 128, "native mathematical depth")
    kind = type(value)
    if value is None or kind in (str, bool):
        return
    if kind is int:
        check(abs(value).bit_length() <= 4096, "native integer bits")
        return
    check(kind in (list, dict), "native mathematical JSON value")
    if kind is dict:
        check(all(type(k) is str for k in value), "native dictionary keys")
        children = value.values()
    else:
        children = value
    for child in children:
        native_tree(child, depth + 1)


def native_eq(left, right, message):
    check(canon(left) == canon(right), message)


def fields(value, names, message):
    check(type(value) is dict and set(value) == set(names.split()), message + " fields")


def fraction(value, lower=None, upper=None):
    check(
        type(value) is list and len(value) == 2 and all(type(x) is int for x in value),
        "native reduced fraction pair",
    )
    n, d = value
    check(d > 0 and math.gcd(n, d) == 1, "canonical fraction")
    check(max(abs(n).bit_length(), d.bit_length()) <= 4096, "fraction component bits")
    result = F(n, d)
    check(
        (lower is None or result >= lower) and (upper is None or result <= upper),
        "fraction interval",
    )
    return result


def wire(value):
    check(type(value) is F, "exact retained fraction")
    check(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= 4096,
        "retained reduced component bits",
    )
    return [value.numerator, value.denominator]


def old_fraction(value):
    check(type(value) is str, "pinned D/E rational string")
    parsed = F(value)
    eq(str(parsed), value, "canonical pinned rational string")
    check(
        max(abs(parsed.numerator).bit_length(), parsed.denominator.bit_length()) <= 4096,
        "pinned rational bits",
    )
    return parsed


def exact_ids(value, n):
    check(
        type(value) is list and all(type(i) is int and 0 <= i < n for i in value),
        "native bounded ID list",
    )
    native_eq(value, sorted(set(value)), "strict sorted ID list")


def inclusions(masses):
    answer = []
    for support in range(len(masses)):
        terms = [p for mask, p in enumerate(masses) if (mask & support) == support]
        answer.append(sum(terms, F(0)))
        COUNTS["inclusion_superset_terms"] += len(terms)
    return answer


def chain_lists(kept, past, source, target, degree):
    positions = {value: i for i, value in enumerate(kept)}
    a, b = positions[source], positions[target]
    result = []
    for internal in itertools.combinations(range(len(kept)), degree):
        path = (a, *internal, b)
        if all(left in past[right] for left, right in itertools.pairwise(path)):
            result.append([kept[i] for i in internal])
        COUNTS["observed_chain_candidate_checks"] += 1
    return result


def support_mask(chain, eligible):
    return sum(1 << i for i, vertex in enumerate(eligible) if vertex in chain)


def weights_for(support, inclusion, average):
    product = F(1)
    for i in range(len(inclusion).bit_length() - 1):
        if support & (1 << i):
            product *= inclusion[1 << i]
    return {
        "raw": F(1),
        "marginal_product": 1 / product,
        "uniform_rate": 1 / average ** support.bit_count(),
        "joint_supported": 1 / inclusion[support] if inclusion[support] else None,
    }


def kernel_scale(rho, degree):
    value = F((-1) ** degree, 2 ** (degree + 1)) / rho**degree
    wire(value)
    return value


def expected_packet(problem):
    """Strict independent generic observer oracle, with no hidden-source argument."""
    native_tree(problem)
    fields(
        problem,
        "schema_version family frame_size fixed eligible probes density mask_probabilities record",
        "AF packet",
    )
    native_eq(problem["schema_version"], "det8-qr05af-problem-v1", "AF schema")
    native_eq(problem["family"], "qr05af_local_geometry", "AF family")
    n = problem["frame_size"]
    check(type(n) is int and 2 <= n <= 12, "AF frame bounds")
    fixed, eligible = problem["fixed"], problem["eligible"]
    exact_ids(fixed, n)
    exact_ids(eligible, n)
    check(1 <= len(eligible) <= 8, "AF eligible bound before exponential")
    native_eq(sorted(fixed + eligible), list(range(n)), "AF exact frame partition")
    probes = problem["probes"]
    check(type(probes) is list and 1 <= len(probes) <= 8, "AF probe bound")
    names, pairs = set(), set()
    for probe in probes:
        fields(probe, "name source target", "AF probe")
        name, source, target = (probe[k] for k in ("name", "source", "target"))
        check(
            type(name) is str and len(name) <= 40 and re.fullmatch(r"[a-z][a-z0-9_]{0,39}", name),
            "AF probe name",
        )
        check(
            type(source) is int
            and type(target) is int
            and source in fixed
            and target in fixed
            and source < target,
            "AF fixed ordered probe",
        )
        check(name not in names and (source, target) not in pairs, "AF unique probes")
        names.add(name)
        pairs.add((source, target))
    rho = fraction(problem["density"])
    check(rho > 0, "AF external positive density")
    m, L = len(eligible), 1 << len(eligible)
    check(
        type(problem["mask_probabilities"]) is list and len(problem["mask_probabilities"]) == L,
        "AF complete mask probabilities",
    )
    masses = [fraction(v, 0, 1) for v in problem["mask_probabilities"]]
    eq(sum(masses, F(0)), F(1), "AF normalized selection law")
    fields(problem["record"], "kept past", "AF observed record")
    kept, past = problem["record"]["kept"], problem["record"]["past"]
    exact_ids(kept, n)
    check(set(fixed) <= set(kept), "AF all fixed IDs observed")
    check(type(past) is list and len(past) == len(kept), "AF local past shape")
    for i, row in enumerate(past):
        exact_ids(row, i)
        check(all(set(past[v]) <= set(row) for v in row), "AF received transitive order")
    K, Q = len(kept), 3 * len(probes)
    I = 3**m
    C = len(probes) * (1 + K + K * (K - 1) // 2)
    W = L + I + 5 * C + 4 * Q
    check(
        I <= 6561 and C <= 632 and 4 * C <= 2528 and W <= 20000, "AF complete logical reservation"
    )
    inclusion = inclusions(masses)
    for probability in inclusion:
        wire(probability)
    check(all(inclusion[1 << i] > 0 for i in range(m)), "AF positive singleton marginals")
    average = sum((inclusion[1 << i] for i in range(m)), F(0)) / m
    mask = support_mask(kept, eligible)
    questions, observed = [], 0
    for probe in probes:
        for degree in range(3):
            chains = chain_lists(kept, past, probe["source"], probe["target"], degree)
            terms = [
                {
                    "vertices": chain,
                    "eligible_mask": support_mask(chain, eligible),
                    "inclusion": wire(inclusion[support_mask(chain, eligible)]),
                }
                for chain in chains
            ]
            values = dict.fromkeys(METHODS, F(0))
            for term in terms:
                term_weights = weights_for(term["eligible_mask"], inclusion, average)
                for method in METHODS:
                    if term_weights[method] is not None:
                        values[method] += term_weights[method]
            scale = kernel_scale(rho, degree)
            omitted = sum(inclusion[term["eligible_mask"]] == 0 for term in terms)
            check(not masses[mask] or omitted == 0, "AF possible record supported")
            questions.append(
                {
                    "probe": probe["name"],
                    "degree": degree,
                    "scale": wire(scale),
                    "observed_count": len(chains),
                    "observed_chains": terms,
                    "unsupported_observed_terms": omitted,
                    "count_estimates": {method: wire(values[method]) for method in METHODS},
                    "coefficient_estimates": {
                        method: wire(scale * values[method]) for method in METHODS
                    },
                }
            )
            observed += len(chains)
    result = {
        "input_sha256": digest(problem),
        "mask": mask,
        "probability": wire(masses[mask]),
        "possible": bool(masses[mask]),
        "inclusion_probabilities": [wire(p) for p in inclusion],
        "questions": questions,
        "counts": {
            "events": n,
            "eligible_events": m,
            "kept_events": K,
            "mask_rows": L,
            "questions": Q,
            "inclusion_terms": I,
            "chain_candidates": C,
            "observed_chain_terms": observed,
            "estimator_terms": 4 * observed,
            "coefficient_evaluations": 4 * Q,
            "reserved_estimator_terms": 4 * C,
            "reserved_total_work": W,
            "total_work": L + I + C + 4 * observed + 4 * Q,
        },
        "scope": dict.fromkeys(PACKET_SCOPE, False),
    }
    native_tree(result)
    check(len(canon(result)) <= 4194304, "AF complete packet wire cap")
    return json.loads(canon(result))


def vector(values):
    return [wire(F(v)) for v in values]


def matrix(rows):
    return [vector(row) for row in rows]


def supplied_source(name):
    """Rebuild the supplied null coordinates and product order independently."""
    coordinates = None
    if name.startswith("mesh3"):
        coordinates = [(F(0), F(0))]
        coordinates.extend(
            (F(12 * i + j, 52), F(12 * j + i, 52)) for i in range(1, 4) for j in range(1, 4)
        )
        coordinates.append((F(1), F(1)))
        rho = F(18)
        if name == "mesh3_boost":
            coordinates = [(u * 2, v / 2) for u, v in coordinates]
        elif name in ("mesh3_dilate", "mesh3_dilate_wrong_density"):
            coordinates = [(u * 2, v * 2) for u, v in coordinates]
            if name == "mesh3_dilate":
                rho = F(9, 2)
        elif name == "mesh3_warp":
            coordinates = [(u**2, v**2) for u, v in coordinates]
        else:
            eq(name, "mesh3", "prescribed mesh name")
        fixed = [0, 3, 5, 7, 10]
        eligible = [i for i in range(11) if i not in fixed]
        probes = [("whole", 0, 10)]
        for mark in (5, 3, 7):
            probes.extend(((f"bottom_to_p{mark}", 0, mark), (f"p{mark}_to_top", mark, 10)))
    else:
        check(name in ("ferrers6", "standard_example3", "chain6"), "prescribed abstract name")
        fixed, eligible, probes, rho = [0, 7], list(range(1, 7)), [("whole", 0, 7)], F(12)
        if name == "ferrers6":
            coordinates = [(F(0), F(0))]
            coordinates.extend(
                (F(u, 16), F(v, 16))
                for u, v in ((2, 6), (4, 4), (6, 2), (3, 14), (5, 12), (14, 10))
            )
            coordinates.append((F(1), F(1)))
    if coordinates is not None:
        past = [
            [i for i in range(j) if coordinates[i][0] < u and coordinates[i][1] < v]
            for j, (u, v) in enumerate(coordinates)
        ]
        if name == "ferrers6":
            for i in range(3):
                for j in range(3):
                    eq(i + 1 in past[j + 4], i <= j, "Ferrers independent coordinate/recipe bridge")
    elif name == "chain6":
        past = [list(range(j)) for j in range(8)]
    else:
        edges = {(0, j) for j in range(1, 8)} | {(i, 7) for i in range(7)}
        edges |= {(i + 1, j + 4) for i in range(3) for j in range(3) if i != j}
        past = [[i for i in range(j) if (i, j) in edges] for j in range(8)]
    for row in past:
        for p in row:
            check(set(past[p]) <= set(row), "full generated relation transitive")
    kind = "algebraic_only" if coordinates is None else "whole_volume_calibrated"
    if name == "mesh3_dilate_wrong_density":
        kind = "intentionally_wrong"
    return {
        "name": name,
        "coordinates": None if coordinates is None else [vector(row) for row in coordinates],
        "past": past,
        "fixed": fixed,
        "eligible": eligible,
        "probes": [{"name": label, "source": a, "target": b} for label, a, b in probes],
        "density": wire(rho),
        "density_kind": kind,
    }


def selection_law(name, m):
    """Original mass on every mask, including all impossible records."""
    law = [F(0)] * (1 << m)
    if name == "identity":
        law[-1] = F(1)
    elif name == "all_or_none":
        law[0] = law[-1] = F(1, 2)
    elif name in ("fixed_size2", "singleton"):
        size = 2 if name == "fixed_size2" else 1
        for chosen in itertools.combinations(range(m), size):
            law[sum(1 << i for i in chosen)] = F(1, math.comb(m, size))
    else:
        check(name in ("iid_half", "heterogeneous"), "prescribed independent selection law")
        rates = [F(1, 2) if name == "iid_half" else F(1 + i % 2, 3) for i in range(m)]
        for mask in range(1 << m):
            factors = [p if mask & (1 << i) else 1 - p for i, p in enumerate(rates)]
            law[mask] = math.prod(factors)
    eq(sum(law, F(0)), F(1), "normalized raw selection design")
    return {"name": name, "mask_probabilities": vector(law)}


def raw_packet(source, design, mask, override=None):
    retained = set(source["fixed"])
    retained.update(v for i, v in enumerate(source["eligible"]) if mask & (1 << i))
    kept = sorted(retained)
    position = {v: i for i, v in enumerate(kept)}
    past = [sorted(position[v] for v in source["past"][b] if v in retained) for b in kept]
    return {
        "schema_version": "det8-qr05af-problem-v1",
        "family": "qr05af_local_geometry",
        "frame_size": len(source["past"]),
        "fixed": source["fixed"],
        "eligible": source["eligible"],
        "probes": source["probes"],
        "density": source["density"],
        "mask_probabilities": design["mask_probabilities"],
        "record": {"kept": kept, "past": past if override is None else override},
    }


def full_population(source, design):
    pi = inclusions([fraction(v) for v in design["mask_probabilities"]])
    rho = fraction(source["density"])
    coords = source["coordinates"]
    geometry = None if coords is None else []
    questions = []
    for probe in source["probes"]:
        comparison = None
        if coords is not None:
            a, b = probe["source"], probe["target"]
            du = fraction(coords[b][0]) - fraction(coords[a][0])
            dv = fraction(coords[b][1]) - fraction(coords[a][1])
            check(du > 0 and dv > 0, "strict supplied timelike separation")
            tau2 = du * dv
            comparison = [F(1, 2), -tau2 / 8, tau2 * tau2 / 128]
        local = []
        for q in range(3):
            rows, missing = [], []
            for vertices in chain_lists(
                list(range(len(source["past"]))),
                source["past"],
                probe["source"],
                probe["target"],
                q,
            ):
                support = support_mask(vertices, source["eligible"])
                rows.append(
                    {"vertices": vertices, "eligible_mask": support, "inclusion": wire(pi[support])}
                )
                if not pi[support]:
                    missing.append(vertices)
            scale = kernel_scale(rho, q)
            target = scale * len(rows)
            local.append(
                {
                    "probe": probe["name"],
                    "degree": q,
                    "scale": wire(scale),
                    "chains": rows,
                    "target_count": len(rows),
                    "target_coefficient": wire(target),
                    "supported_count": len(rows) - len(missing),
                    "zero_inclusion_chains": missing,
                    "full_target_supported": not missing,
                    "continuum_coefficient": None if comparison is None else wire(comparison[q]),
                    "finite_geometry_error": None
                    if comparison is None
                    else wire(target - comparison[q]),
                }
            )
        questions.extend(local)
        if geometry is not None:
            estimate = F(local[1]["target_count"]) / rho
            geometry.append(
                {
                    "probe": probe["name"],
                    "source": probe["source"],
                    "target": probe["target"],
                    "tau_squared": wire(tau2),
                    "volume": wire(tau2 / 2),
                    "finite_count_volume": wire(estimate),
                    "volume_error": wire(estimate - tau2 / 2),
                }
            )
    return {"questions": questions, "interval_geometry": geometry}


def design_moments(population, samples):
    questions = population["questions"]
    Q = len(questions)
    scales = [fraction(row["scale"]) for row in questions]
    targets = [F(row["target_count"]) for row in questions]
    positive = [s for s in samples if s["analysis"]["possible"]]
    masses = [fraction(s["analysis"]["probability"]) for s in positive]
    result = {}
    for method in METHODS:
        values = [
            [fraction(q["count_estimates"][method]) for q in s["analysis"]["questions"]]
            for s in positive
        ]
        mean = [
            sum((p * row[i] for p, row in zip(masses, values, strict=True)), F(0)) for i in range(Q)
        ]
        covariance = [[F(0)] * Q for _ in range(Q)]
        for i in range(Q):
            for j in range(i, Q):
                second = sum(
                    (p * row[i] * row[j] for p, row in zip(masses, values, strict=True)), F(0)
                )
                centered = sum(
                    (
                        p * (row[i] - mean[i]) * (row[j] - mean[j])
                        for p, row in zip(masses, values, strict=True)
                    ),
                    F(0),
                )
                eq(
                    second - mean[i] * mean[j],
                    centered,
                    "second-moment / centered-outer-product covariance",
                )
                covariance[i][j] = covariance[j][i] = centered
                COUNTS["centered_covariance_entries"] += 1
                COUNTS["centered_outer_product_terms"] += len(masses)
            check(covariance[i][i] >= 0, "nonnegative variance from centered Gram representation")
        coefficient_mean = [scales[i] * mean[i] for i in range(Q)]
        count_bias = [mean[i] - targets[i] for i in range(Q)]
        geometry = None
        if population["interval_geometry"] is not None:
            geometry = []
            for i, q in enumerate(questions):
                continuum = fraction(q["continuum_coefficient"])
                finite = fraction(q["target_coefficient"])
                sampling = coefficient_mean[i] - finite
                discrepancy = finite - continuum
                total = coefficient_mean[i] - continuum
                eq(total, sampling + discrepancy, "separate signed sampling/geometric errors")
                geometry.append(
                    {
                        "probe": q["probe"],
                        "degree": q["degree"],
                        "continuum": wire(continuum),
                        "mean": wire(coefficient_mean[i]),
                        "sampling_bias": wire(sampling),
                        "finite_model_discrepancy": wire(discrepancy),
                        "total_discrepancy": wire(total),
                    }
                )
                COUNTS["signed_geometry_decompositions"] += 1
        result[method] = {
            "mean_counts": vector(mean),
            "bias_counts": vector(count_bias),
            "covariance_counts": matrix(covariance),
            "mean_coefficients": vector(coefficient_mean),
            "bias_coefficients": vector(scales[i] * count_bias[i] for i in range(Q)),
            "covariance_coefficients": matrix(
                [[scales[i] * scales[j] * covariance[i][j] for j in range(Q)] for i in range(Q)]
            ),
            "geometry_comparisons": geometry,
        }
    native_eq(
        result["joint_supported"]["mean_counts"],
        vector(q["supported_count"] for q in questions),
        "joint estimator targets supported chains only",
    )
    return result


def joint_covariance(population, design):
    """Support-class aggregation of the full ordered chain-pair formula."""
    pi = inclusions([fraction(p) for p in design["mask_probabilities"]])
    inventories = []
    for question in population["questions"]:
        inventory = defaultdict(int)
        for chain in question["chains"]:
            support = chain["eligible_mask"]
            if pi[support]:
                inventory[support] += 1
        inventories.append(inventory)
    result = []
    for left in inventories:
        row = []
        for right in inventories:
            value = F(0)
            for a, multiplicity_a in left.items():
                for b, multiplicity_b in right.items():
                    multiplicity = multiplicity_a * multiplicity_b
                    value += multiplicity * (pi[a | b] / (pi[a] * pi[b]) - 1)
                    COUNTS["ordered_supported_chain_pairs"] += multiplicity
                    COUNTS["support_class_covariance_terms"] += 1
                    if pi[a | b] == 0:
                        COUNTS["zero_union_chain_pairs"] += multiplicity
            row.append(value)
        result.append(row)
    return matrix(result)


def restricted_link_reachability(full, kept):
    """Construct Hasse edges, delete absent vertices, then Floyd reachability."""
    K = len(kept)
    relation = [[False] * K for _ in range(K)]
    for i, a in enumerate(kept):
        for j, b in enumerate(kept):
            if a in full[b] and not any(a in full[v] and v in full[b] for v in range(len(full))):
                relation[i][j] = True
    for k in range(K):
        for i in range(K):
            for j in range(K):
                relation[i][j] = relation[i][j] or (relation[i][k] and relation[k][j])
    return [[i for i in range(j) if relation[i][j]] for j in range(K)]


def wrong_channel_control(source, design, samples):
    mismatch, first = F(0), None
    for mask, sample in enumerate(samples):
        p = fraction(sample["analysis"]["probability"])
        if not p:
            continue
        kept = sample["problem"]["record"]["kept"]
        actual = sample["problem"]["record"]["past"]
        wrong = restricted_link_reachability(source["past"], kept)
        failed = []
        for probe in source["probes"]:
            a, b = kept.index(probe["source"]), kept.index(probe["target"])
            if (a in actual[b]) != (a in wrong[b]):
                failed.append(probe["name"])
        if failed:
            mismatch += p
            if first is None:
                packet = raw_packet(source, design, mask, wrong)
                first = {
                    "mask": mask,
                    "kept": kept,
                    "past": wrong,
                    "failed_probes": failed,
                    "analysis": expected_packet(packet),
                }
    return {"mismatch_probability": wire(mismatch), "first_mismatch": first}


def specifications():
    names = [
        ("mesh3", d)
        for d in (
            "identity",
            "iid_half",
            "heterogeneous",
            "all_or_none",
            "fixed_size2",
            "singleton",
        )
    ]
    names.extend(
        (s, d)
        for s in ("mesh3_boost", "mesh3_dilate", "mesh3_dilate_wrong_density", "mesh3_warp")
        for d in ("identity", "iid_half")
    )
    names.extend(
        (s, d) for s in ("ferrers6", "standard_example3") for d in ("identity", "iid_half")
    )
    return names + [("ferrers6", "singleton"), ("chain6", "singleton")]


def expected_case(source_name, design_name):
    source = supplied_source(source_name)
    design = selection_law(design_name, len(source["eligible"]))
    population = full_population(source, design)
    samples = []
    for mask in range(len(design["mask_probabilities"])):
        problem = raw_packet(source, design, mask)
        analysis = expected_packet(problem)
        samples.append({"problem": problem, "analysis": analysis})
    moments = design_moments(population, samples)
    covariance = joint_covariance(population, design)
    native_eq(
        covariance,
        moments["joint_supported"]["covariance_counts"],
        "complete joint covariance from two independent formulas",
    )
    return {
        "case_id": source_name + "__" + design_name,
        "source": source,
        "design": design,
        "population": population,
        "samples": samples,
        "moments": moments,
        "joint_covariance_formula": covariance,
        "hasse_control": wrong_channel_control(source, design, samples),
        "counts": {
            "events": len(source["past"]),
            "eligible_events": len(source["eligible"]),
            "mask_rows": len(samples),
            "positive_rows": sum(s["analysis"]["possible"] for s in samples),
            "questions": len(population["questions"]),
            "source_chain_terms": sum(q["target_count"] for q in population["questions"]),
            "observed_chain_terms": sum(
                s["analysis"]["counts"]["observed_chain_terms"] for s in samples
            ),
            "packet_calls": 2 * len(samples),
        },
    }


def equality_flag(left, right, message):
    native_eq(left, right, message)
    return True


def positive_law(case):
    return [
        {"problem": s["problem"], "probability": s["analysis"]["probability"]}
        for s in case["samples"]
        if s["analysis"]["possible"]
    ]


def scaled_pair(base, changed, factor, message):
    eq(fraction(changed), fraction(base) * factor, message)


def check_dilation(base, changed):
    """Fieldwise full congruence, with both signed covariance scale factors."""
    eq(
        fraction(changed["source"]["density"]) * 4,
        fraction(base["source"]["density"]),
        "quarter-density dilation",
    )
    pop_scalar = {"scale", "target_coefficient", "continuum_coefficient", "finite_geometry_error"}
    for a, b in zip(
        base["population"]["questions"], changed["population"]["questions"], strict=True
    ):
        for key in a:
            if key in pop_scalar:
                scaled_pair(
                    a[key], b[key], 4 ** a["degree"], "complete population coefficient dilation"
                )
            else:
                native_eq(a[key], b[key], "unchanged population chain/support inventory")
    for a, b in zip(
        base["population"]["interval_geometry"],
        changed["population"]["interval_geometry"],
        strict=True,
    ):
        for key in a:
            if key in ("tau_squared", "volume", "finite_count_volume", "volume_error"):
                scaled_pair(a[key], b[key], 4, "all volume/squared-length geometry dilation")
            else:
                native_eq(a[key], b[key], "fixed dilation probe metadata")
    for a, b in zip(base["samples"], changed["samples"], strict=True):
        for key in a["problem"]:
            if key != "density":
                native_eq(
                    a["problem"][key], b["problem"][key], "same public dilation count-law packet"
                )
        for key in a["analysis"]:
            if key not in ("questions", "input_sha256"):
                native_eq(a["analysis"][key], b["analysis"][key], "same dilation packet metadata")
        native_eq(b["analysis"]["input_sha256"], digest(b["problem"]), "dilation input hash")
        for old, new in zip(a["analysis"]["questions"], b["analysis"]["questions"], strict=True):
            for key in old:
                if key == "scale":
                    scaled_pair(old[key], new[key], 4 ** old["degree"], "dilation packet scale")
                elif key == "coefficient_estimates":
                    for method in METHODS:
                        scaled_pair(
                            old[key][method],
                            new[key][method],
                            4 ** old["degree"],
                            "all packet method coefficients dilate",
                        )
                else:
                    native_eq(old[key], new[key], "unchanged complete dilation count packet")
    for method in METHODS:
        a, b = base["moments"][method], changed["moments"][method]
        for key in ("mean_counts", "bias_counts", "covariance_counts"):
            native_eq(a[key], b[key], "unchanged complete count moments under dilation")
        for key in ("mean_coefficients", "bias_coefficients"):
            for i, (v, w) in enumerate(zip(a[key], b[key], strict=True)):
                scaled_pair(v, w, 4 ** (i % 3), "degree-scaled complete coefficient moments")
        for i, (arow, brow) in enumerate(
            zip(a["covariance_coefficients"], b["covariance_coefficients"], strict=True)
        ):
            for j, (v, w) in enumerate(zip(arow, brow, strict=True)):
                scaled_pair(
                    v, w, 4 ** ((i % 3) + (j % 3)), "both covariance coefficient axes scale"
                )
        for arow, brow in zip(a["geometry_comparisons"], b["geometry_comparisons"], strict=True):
            for key in arow:
                if key in ("probe", "degree"):
                    native_eq(arow[key], brow[key], "fixed dilation geometry-comparison question")
                else:
                    scaled_pair(
                        arow[key], brow[key], 4 ** arow["degree"], "complete signed error dilation"
                    )


def geometry_witness(base, changed, local_only):
    pairs = zip(
        base["population"]["interval_geometry"],
        changed["population"]["interval_geometry"],
        strict=True,
    )
    for i, (a, b) in enumerate(pairs):
        if (i > 0 or not local_only) and fraction(a["volume"]) != fraction(b["volume"]):
            return {
                "probe": a["probe"],
                "probe_index": i,
                "base_volume": a["volume"],
                "transformed_volume": b["volume"],
                "base_error": a["volume_error"],
                "transformed_error": b["volume_error"],
            }
    raise RuntimeError("missing prescribed fixed-probe supplied-geometry witness")


def expected_controls(cases):
    by_name = {case["case_id"]: case for case in cases}
    answer = {
        name: {"pairs": []}
        for name in ("boost", "correct_dilation", "wrong_density", "active_warp")
    }
    for design in ("identity", "iid_half"):
        base = by_name["mesh3__" + design]
        boost = by_name["mesh3_boost__" + design]
        answer["boost"]["pairs"].append(
            {
                "design": design,
                "public_samples_equal": equality_flag(
                    base["samples"], boost["samples"], "boost complete public samples"
                ),
                "population_equal": equality_flag(
                    base["population"],
                    boost["population"],
                    "boost entire population including supplied geometry",
                ),
                "moments_equal": equality_flag(
                    base["moments"], boost["moments"], "boost entire moments and covariance"
                ),
            }
        )
        check_dilation(base, by_name["mesh3_dilate__" + design])
        answer["correct_dilation"]["pairs"].append(
            {
                "design": design,
                "count_estimates_equal": True,
                "population_scaling": True,
                "coefficient_packet_scaling": True,
                "complete_moment_congruence": True,
                "squared_length_factor": [4, 1],
            }
        )
        for key, name in (
            ("wrong_density", "mesh3_dilate_wrong_density"),
            ("active_warp", "mesh3_warp"),
        ):
            other = by_name[name + "__" + design]
            witness = geometry_witness(base, other, key == "active_warp")
            answer[key]["pairs"].append(
                {
                    "design": design,
                    "public_samples_equal": equality_flag(
                        base["samples"],
                        other["samples"],
                        "geometric ambiguity complete public samples",
                    ),
                    "supplied_geometry_differs": True,
                    "witness": witness,
                }
            )
    ferrers, standard = by_name["ferrers6__identity"], by_name["standard_example3__identity"]
    finite = [q["target_coefficient"] for q in ferrers["population"]["questions"]]
    native_eq(
        finite,
        [q["target_coefficient"] for q in standard["population"]["questions"]],
        "endpoint truncated coefficient collision",
    )
    fm = by_name["ferrers6__iid_half"]["moments"]["joint_supported"]
    sm = by_name["standard_example3__iid_half"]["moments"]["joint_supported"]
    mean_equal = equality_flag(fm["mean_counts"], sm["mean_counts"], "complete endpoint iid means")
    covariance_equal = canon(fm["covariance_counts"]) == canon(sm["covariance_counts"])
    check(not covariance_equal, "complete endpoint iid covariance distinguishes examples")
    answer["endpoint_collision"] = {
        "identity_cases": [ferrers["case_id"], standard["case_id"]],
        "finite_coefficients": finite,
        "iid_joint_mean_equal": mean_equal,
        "iid_joint_covariance_equal": covariance_equal,
        "ferrers_iid_pair_variance": fm["covariance_counts"][2][2],
        "S3_iid_pair_variance": sm["covariance_counts"][2][2],
        "embedding_reassessed": False,
    }
    ferrers, chain = by_name["ferrers6__singleton"], by_name["chain6__singleton"]
    law = positive_law(ferrers)
    positive_equal = equality_flag(
        law, positive_law(chain), "identical complete positive observation packet laws"
    )
    targets = {
        "ferrers6": ferrers["population"]["questions"][2]["target_count"],
        "chain6": chain["population"]["questions"][2]["target_count"],
    }
    check(
        targets["ferrers6"] != targets["chain6"], "same observed law does not identify pair target"
    )
    answer["singleton_observation_collision"] = {
        "case_ids": [ferrers["case_id"], chain["case_id"]],
        "positive_packets_equal": positive_equal,
        "full_pair_targets": targets,
        "full_pair_targets_differ": True,
        "observation_law_sha256": digest(law),
    }
    return answer


def consumed_bridges(cases, old_d, d, e):
    """Recheck only the declared D/E projections; all other old math is pinned."""
    native_eq(
        old_d["suite"], d["suite"], "D-v1/v2 complete mathematical-suite identity, not old replay"
    )
    dcases = {case["analysis"]["case"]: case["analysis"] for case in d["suite"]["cases"]}
    ecases = {
        (case["analysis"]["order_name"], case["analysis"]["design"]): case["analysis"]
        for case in e["suite"]["cases"]
    }
    current = {case["case_id"]: case for case in cases}
    base = current["mesh3__identity"]
    previous = dcases["mesh3"]
    native_eq(
        base["source"]["coordinates"],
        [vector(old_fraction(x) for x in row) for row in previous["coordinates"]],
        "D full mesh3 coordinate bridge",
    )
    relation = [
        [int(i in row) for row in base["source"]["past"]]
        for i in range(len(base["source"]["past"]))
    ]
    native_eq(relation, previous["order"]["relation"], "D complete mesh3 order bridge")
    for p, probe in enumerate(base["source"]["probes"][:3]):
        for q in range(3):
            old = previous["order"]["kernel_coefficients"][q][probe["source"]][probe["target"]]
            native_eq(
                wire(old_fraction(old)),
                base["population"]["questions"][3 * p + q]["target_coefficient"],
                "D shared marked coefficient bridge",
            )
            COUNTS["D_shared_probe_coefficients"] += 1
    for name in ("ferrers6", "standard_example3"):
        for q in range(3):
            old = dcases[name]["order"]["endpoint"]["coefficients"][q]
            native_eq(
                wire(old_fraction(old)),
                current[name + "__identity"]["population"]["questions"][q]["target_coefficient"],
                "D endpoint coefficient bridge",
            )
            COUNTS["D_endpoint_coefficients"] += 1
        for design in ("identity", "iid_half"):
            new, previous = current[name + "__" + design], ecases[name, design]
            for method in METHODS:
                for key in ("mean_counts", "bias_counts", "mean_coefficients", "bias_coefficients"):
                    old = vector(old_fraction(x) for x in previous["moments"][method][key][:3])
                    native_eq(new["moments"][method][key], old, "E full q0..2 moment vector bridge")
                    COUNTS["E_moment_vector_components"] += 3
                for key in ("covariance_counts", "covariance_coefficients"):
                    old = matrix(
                        [
                            [old_fraction(x) for x in row[:3]]
                            for row in previous["moments"][method][key][:3]
                        ]
                    )
                    native_eq(
                        new["moments"][method][key], old, "E full q0..2 cross covariance bridge"
                    )
                    COUNTS["E_covariance_components"] += 9
    for name in ("ferrers6", "chain6"):
        new, previous = current[name + "__singleton"], ecases[name, "singleton"]
        newlaw = [
            {**s["problem"]["record"], "probability": s["analysis"]["probability"]}
            for s in new["samples"]
            if s["analysis"]["possible"]
        ]
        oldlaw = [
            {
                "kept": row["kept"],
                "past": row["past"],
                "probability": wire(old_fraction(row["probability"])),
            }
            for row in previous["observation_law"]
        ]
        native_eq(newlaw, oldlaw, "E complete singleton observation-law bridge")
        native_eq(
            new["population"]["questions"][2]["target_count"],
            previous["questions"][2]["target_count"],
            "E singleton hidden pair-target bridge",
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


def expected_suite(old_d, d, e):
    cases = [expected_case(source, design) for source, design in specifications()]
    totals = {"cases": len(cases)}
    totals.update({key: sum(case["counts"][key] for case in cases) for key in cases[0]["counts"]})
    return {
        "cases": cases,
        "controls": expected_controls(cases),
        "prior_bridges": consumed_bridges(cases, old_d, d, e),
        "public_controls": {
            "ordinary_packet_calls": totals["packet_calls"],
            "wrong_channel_packet_calls": 2
            * sum(case["hasse_control"]["first_mismatch"] is not None for case in cases),
            "independent_route_equal": True,
            "invalid_calls_rejected": 16,
        },
        "totals": totals,
        "scope": dict.fromkeys(SUITE_SCOPE, False),
    }


AF_SOURCES = (
    "README.md",
    "geometry.py",
    "reference_qr05af.py",
    "study.py",
    "test_qr05af.py",
    "test_capture.py",
    "audit_json.py",
)
D_SOURCES = (
    "README.md",
    "REVISION_V2.md",
    "geometry.py",
    "reference_qr05d.py",
    "study.py",
    "study_v2.py",
    "test_capture.py",
    "test_capture_v2.py",
    "test_qr05d.py",
)
E_SOURCES = (
    "README.md",
    "reference_qr05e.py",
    "study.py",
    "test_capture.py",
    "test_qr05e.py",
    "thinning.py",
)


def plain_bytes(path):
    check(path.is_file() and not path.is_symlink(), "plain evidence/source file: " + str(path))
    return path.read_bytes()


def raw_identity(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def identity_record(value):
    fields(value, "bytes sha256", "identity record")
    check(type(value["bytes"]) is int and value["bytes"] > 0, "identity positive native size")
    check(
        type(value["sha256"]) is str and re.fullmatch("[a-f0-9]{64}", value["sha256"]),
        "identity SHA256 spelling",
    )


def pinned_json(path, identity):
    raw = plain_bytes(path)
    native_eq(raw_identity(raw), identity, "pinned artifact identity: " + str(path))
    # Historical D/E packaging is immutable, not an AF serialization promise.
    # Full byte identity authenticates it; only the new AF envelope is required
    # to use AF's compact canonical byte encoding.
    return json.loads(raw)


def runtime_metadata(runtime):
    fields(
        runtime,
        "bytecode_cache executable isolated optimized platform python rss_high_water_at_suite_end rss_units scope suite_seconds",
        "runtime metadata",
    )
    native_eq(runtime["isolated"], True, "recorded isolated capture")
    check(
        type(runtime["optimized"]) is int and runtime["optimized"] in (0, 1),
        "recorded optimization metadata",
    )
    native_eq(runtime["executable"], str(ROOT / ".venv/bin/python"), "recorded executable")
    check(
        type(runtime["rss_units"]) is str and runtime["rss_units"] in ("bytes", "KiB"),
        "recorded RSS units",
    )
    native_eq(
        runtime["scope"],
        "suite and internal exact JSON checks; excludes final report serialization; no application performance claim",
        "recorded runtime scope",
    )
    for key in ("bytecode_cache", "platform", "python"):
        check(type(runtime[key]) is str and bool(runtime[key]), "recorded runtime text " + key)
    cache = Path(runtime["bytecode_cache"])
    check(
        cache.is_absolute()
        and cache != Path(cache.anchor)
        and not cache.resolve().is_relative_to(ROOT),
        "recorded external bytecode cache",
    )
    check(
        type(runtime["rss_high_water_at_suite_end"]) is int
        and runtime["rss_high_water_at_suite_end"] >= 0,
        "recorded RSS metadata",
    )
    seconds = runtime["suite_seconds"]
    check(
        type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0,
        "recorded duration outside mathematical suite",
    )


def identity_inventory(doc):
    """AE authenticates the static 35-prior lineage, without replaying its math."""
    ae = pinned_json(AEDIR / "results.json", AE_ID)
    fields(ae, "schema_version runtime source_ledger prior_artifacts suite", "pinned AE envelope")
    native_eq(ae["schema_version"], "det8-qr05ae-results-v1", "AE checkpoint schema")
    check(
        type(ae["prior_artifacts"]) is dict and len(ae["prior_artifacts"]) == 35,
        "AE authenticated 35-prior inventory",
    )
    prior_expected = {**ae["prior_artifacts"], AE_PRIOR: AE_ID}
    native_eq(
        doc["prior_artifacts"],
        prior_expected,
        "all 36 current prior identities equal pinned lineage",
    )
    native_eq(sorted(doc["source_ledger"]), sorted(AF_SOURCES), "seven exact AF source filenames")
    targets = {HERE / name: doc["source_ledger"][name] for name in AF_SOURCES}
    for name, record in prior_expected.items():
        path = Path(name)
        check(
            not path.is_absolute()
            and len(path.parts) == 2
            and path.parts[0].startswith("qr-")
            and path.parts[1] in ("results.json", "results-v2.json"),
            "bounded prior artifact path",
        )
        targets[HERE.parent / name] = record
    d1 = pinned_json(DDIR / "results.json", D1_ID)
    d2 = pinned_json(DDIR / "results-v2.json", D2_ID)
    e = pinned_json(EDIR / "results.json", E_ID)
    for prior, schema in (
        (d1, "det8-qr05d-results-v1"),
        (d2, "det8-qr05d-results-v2"),
        (e, "det8-qr05e-results-v1"),
    ):
        fields(
            prior,
            "schema_version runtime source_ledger prior_artifacts suite",
            "consumed geometric capture envelope",
        )
        native_eq(prior["schema_version"], schema, "consumed capture schema")
        native_tree(prior["suite"])
    for prior, directory, names in ((d2, DDIR, D_SOURCES), (e, EDIR, E_SOURCES)):
        native_eq(
            sorted(prior["source_ledger"]),
            sorted(names),
            "all consumed geometric source ledger names",
        )
        for name in names:
            targets[directory / name] = prior["source_ledger"][name]
    eq(len(targets), 58, "58 distinct current/prior/consumed-source identity targets")
    for path, record in targets.items():
        identity_record(record)
        native_eq(
            raw_identity(plain_bytes(path)), record, "initial source/prior identity: " + str(path)
        )
    return targets, d1, d2, e


def audit_capture(path=None):
    """Read-only full raw AF audit; no runtime executor, runner, or test imports."""
    COUNTS.clear()
    started = time.perf_counter()
    path = HERE / "results.json" if path is None else Path(path)
    raw = plain_bytes(path)
    check(len(raw) <= 64 * 1024 * 1024, "AF capture 64 MiB cap")
    before = raw_identity(raw)
    doc = json.loads(raw)
    fields(doc, "schema_version runtime source_ledger prior_artifacts suite", "AF envelope")
    native_eq(doc["schema_version"], "det8-qr05af-results-v1", "AF capture schema")
    check(canon(doc) == raw, "complete AF canonical envelope bytes")
    for key in ("suite", "source_ledger", "prior_artifacts"):
        native_tree(doc[key])
    check(len(canon(doc["suite"])) <= 128 * 1024 * 1024, "working suite cap")
    runtime_metadata(doc["runtime"])
    targets, d1, d2, e = identity_inventory(doc)
    expected = expected_suite(d1, d2, e)
    native_tree(expected)
    # Canonical equality preserves exact bool/int distinctions and all metadata.
    native_eq(expected, doc["suite"], "complete independent raw AF suite wire")
    for path_source, record in targets.items():
        native_eq(
            raw_identity(plain_bytes(path_source)),
            record,
            "final source/prior identity: " + str(path_source),
        )
    native_eq(
        raw_identity(plain_bytes(path)), before, "artifact identity unchanged during raw audit"
    )
    suite_raw = canon(expected)
    return {
        "status": "VERIFIED_JSON_ONLY_RAW_AF",
        "artifact": {**before, "path": str(path)},
        "suite": raw_identity(suite_raw),
        "seconds": time.perf_counter() - started,
        "counts": dict(sorted(COUNTS.items())),
        "totals": expected["totals"],
        "identity_targets": {
            "total": 58,
            "AF_sources": 7,
            "prior_captures": 36,
            "D_v2_sources": 9,
            "E_sources": 6,
        },
        "all_identities_unchanged": True,
        "scope": {
            "full_AF_geometry_orders_packets_moments_controls_reconstructed": True,
            "centered_and_second_moment_covariances_independently_equal": True,
            "full_joint_union_inclusion_covariance_reconstructed": True,
            "ordered_chain_pair_counter_includes_support_class_multiplicity": True,
            "consumed_D_E_math_bridges_independently_checked": True,
            "D_v1_strict_runtime_replayed": False,
            "prior_forecasting_math_replayed": False,
            "source_code_read_only_as_identity_bytes": True,
            "historical_public_API_call_counts_are_metadata_only": True,
            "runtime_metadata_is_not_a_mathematical_benchmark": True,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=HERE / "results.json")
    args = parser.parse_args()
    check(sys.flags.isolated and sys.pycache_prefix, "run with -I and an external bytecode cache")
    cache = Path(sys.pycache_prefix).resolve()
    check(
        cache != Path(cache.anchor) and not cache.is_relative_to(ROOT),
        "external bytecode cache boundary",
    )
    print(json.dumps(audit_capture(args.artifact), sort_keys=True))


if __name__ == "__main__":
    main()
