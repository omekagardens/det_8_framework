"""Independent V readout-value, raw-joint and two-replica Brier tests.

Only pinned U JSON supplies the declared raw observation model; no previous
executor is imported. Elementary helpers are carried from our test lineage.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction as F
from functools import cache
from itertools import combinations, pairwise, product
from math import comb
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
U_SHA = "a2cf4ae0bb31934c3c1aeab7071fb6f675d90d9f0b1a5c2776282e926e3e5eee"


def native(value):
    if value is None or type(value) in (bool, int, str):
        if type(value) is int:
            assert abs(value).bit_length() <= 4096
        return
    if type(value) is list:
        for item in value:
            native(item)
        return
    if type(value) is dict:
        assert all(type(key) is str for key in value)
        for item in value.values():
            native(item)
        return
    raise AssertionError(f"non-native mathematical wire type: {type(value)}")


def wire(value):
    native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


def digest(value):
    return hashlib.sha256(wire(value)).hexdigest()


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("private test module name is already in use")
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("required module unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def zero():
    return [[0] * 4 for _ in range(4)]


@cache
def kernel(odd, even, o, e):
    result = zero()
    for a in range(odd - o + 1):
        for b in range(even - e + 1):
            result[o + a][e + b] = (-1) ** (a + b) * comb(odd - o, a) * comb(even - e, b)
    return result


def add_into(left, right):
    for i, j in product(range(4), repeat=2):
        left[i][j] += right[i][j]


def relation_of(state):
    return {
        (state["kept"][i], b)
        for b, before in zip(state["kept"], state["past"], strict=True)
        for i in before
    }


def state_key(frame_id, kept, past):
    return frame_id, tuple(kept), tuple(tuple(row) for row in past)


def observed_features(state, frame):
    kept, relation = state["kept"], relation_of(state)
    eligible = set(frame["eligible"])
    chains = [[] for _ in range(4)]
    d = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for q in range(4):
        for vertices in combinations([v for v in kept if v not in (0, 7)], q):
            if not all(
                (a, b) in relation or (b, a) in relation for a, b in combinations(vertices, 2)
            ):
                continue
            support = frozenset(vertices) & eligible
            o = sum(v % 2 for v in support)
            d[q][o][len(support) - o] += 1
            chains[q].append(support)
    b = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for q, r in product(range(4), repeat=2):
        for left in chains[q]:
            for right in chains[r]:
                union = left | right
                o = sum(v % 2 for v in union)
                b[q][r][o][len(union) - o] += 1
    motifs, paths = [], []
    for four in combinations(sorted(set(kept) & eligible), 4):
        if sum(v % 2 for v in four) != 2:
            continue
        edges = [(a, z) for a, z in relation if a in four and z in four]
        if any(a % 2 == z % 2 for a, z in edges) or len({a % 2 for a, _ in edges}) != 1:
            continue
        if len(edges) == 4:
            motifs.append(list(four))
        if len(edges) == 3 and sorted(sum(v in edge for edge in edges) for v in four) == [
            1,
            1,
            2,
            2,
        ]:
            paths.append(list(four))
    odd = sum(v % 2 for v in kept if v in eligible)
    return {
        "state_id": state["state_id"],
        "color_sizes": [odd, len(set(kept) & eligible) - odd],
        "chain_counts": list(map(len, chains)),
        "mean_graded": d,
        "pair_graded": b,
        "motif_supports": motifs,
        "motif_count": len(motifs),
        "path_supports": paths,
        "path_count": len(paths),
    }


def partition(keys):
    ids, classes, registry = [], [], {}
    for sid, key in enumerate(keys):
        encoded = wire(key)
        cid = registry.setdefault(encoded, len(registry))
        if cid == len(classes):
            classes.append({"class_id": cid, "key": key, "members": []})
        ids.append(cid)
        classes[cid]["members"].append(sid)
    return {"state_classes": ids, "classes": classes}


def pushed(fine, ids):
    answer = []
    for row in fine:
        accumulated = {}
        for atom in row["transitions"]:
            add_into(
                accumulated.setdefault(ids[atom["target_state"]], zero()), atom["coefficients"]
            )
        answer.append(
            {
                "state_id": row["state_id"],
                "transitions": [
                    {"target_class": target, "coefficients": table}
                    for target, table in sorted(accumulated.items())
                ],
            }
        )
    return answer


def replaced(tree, path, value):
    """Copy only ancestors of one changed cell; do not mutate shared fixtures."""
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def induced_key(state, kept):
    relation = relation_of(state)
    past = [[i for i, u in enumerate(kept) if (u, v) in relation] for v in kept]
    return state_key(state["frame_id"], kept, past)


def local_payload(classes):
    return {
        "schema_version": "det8-qr05s-local-v1",
        "classes": [
            {
                key: copy.deepcopy(row[key])
                for key in ("class_id", "frame_id", "parent_color_sizes", "odd", "even")
            }
            for row in classes
        ],
    }


def word(rows, sid, colors):
    values = {sid: 1}
    for color in colors:
        updated = {}
        for current, count in values.items():
            for atom in rows[current][color]:
                target = atom["target_class"]
                updated[target] = updated.get(target, 0) + count * atom["multiplicity"]
        values = updated
    return values


def certificates(rows, profiles):
    count = len(rows)
    maps = [
        {atom["target_class"]: atom["multiplicity"] for atom in row["transitions"]}
        for row in profiles
    ]
    base, recurrence, reports = 0, 0, []
    for source, parent in enumerate(rows):
        odd, even = parent["parent_color_sizes"]
        for target, final in enumerate(rows):
            m, n = final["parent_color_sizes"]
            value = maps[source].get(target, 0)
            if parent["frame_id"] != final["frame_id"] or m > odd or n > even:
                assert value == 0
                continue
            if (m, n) == (odd, even):
                base += 1
                assert value == int(source == target)
            for color, denominator in (("odd", odd - m), ("even", even - n)):
                if denominator > 0:
                    recurrence += 1
                    numerator = sum(
                        atom["multiplicity"] * maps[atom["target_class"]].get(target, 0)
                        for atom in parent[color]
                    )
                    assert numerator == denominator * value
                    assert numerator % denominator == 0
        rank_totals = zero()
        for atom in profiles[source]["transitions"]:
            m, n = atom["retained_color_sizes"]
            assert rows[atom["target_class"]]["parent_color_sizes"] == [m, n]
            rank_totals[m][n] += atom["multiplicity"]
        assert rank_totals == [
            [choose(odd, m) * choose(even, n) for n in range(4)] for m in range(4)
        ]
        oo, ee = word(rows, source, ["odd", "odd"]), word(rows, source, ["even", "even"])
        oe, eo = word(rows, source, ["odd", "even"]), word(rows, source, ["even", "odd"])

        def filtered(rank, factor, source=source):
            return {
                atom["target_class"]: factor * atom["multiplicity"]
                for atom in profiles[source]["transitions"]
                if atom["retained_color_sizes"] == list(rank)
            }

        assert oo == filtered((odd - 2, even), 2)
        assert ee == filtered((odd, even - 2), 2)
        assert oe == eo == filtered((odd - 1, even - 1), 1)
        assert sum(oo.values()) == odd * (odd - 1)
        assert sum(ee.values()) == even * (even - 1)
        assert sum(oe.values()) == odd * even
        reports.append(
            {
                "class_id": source,
                "odd_odd_targets": len(oo),
                "even_even_targets": len(ee),
                "mixed_targets": len(oe),
                "coefficient_cells": len(oo) + len(ee) + 2 * len(oe),
                "odd_odd_pairs": sum(oo.values()),
                "even_even_pairs": sum(ee.values()),
                "mixed_pairs": sum(oe.values()),
                "max_abs_residual": 0,
            }
        )
    return (
        {
            "target_cells": count * count,
            "base_cells": base,
            "recurrence_cells": recurrence,
            "normalization_cells": 16 * count,
            "max_abs_residual": 0,
        },
        {
            "verified": True,
            "rows": reports,
            "totals": {
                key: sum(row[key] for row in reports)
                for key in (
                    "odd_odd_targets",
                    "even_even_targets",
                    "mixed_targets",
                    "coefficient_cells",
                    "odd_odd_pairs",
                    "even_even_pairs",
                    "mixed_pairs",
                    "max_abs_residual",
                )
            },
        },
    )


def fraction(value):
    assert type(value) is list and len(value) == 2
    numerator, denominator = value
    assert type(numerator) is int and type(denominator) is int
    result = F(numerator, denominator)
    assert result >= 0 and [result.numerator, result.denominator] == value
    assert max(result.numerator.bit_length(), result.denominator.bit_length()) <= 4096
    return result


def fw(value):
    value = F(value)
    return [value.numerator, value.denominator]


def accumulate(target, key, value):
    if value:
        target[key] = target.get(key, F(0)) + value


def belief(values):
    return [
        {"class_id": cid, "probability": fw(value)}
        for cid, value in sorted(values.items())
        if value
    ]


def question_law(values):
    return [
        {"value": list(key), "probability": fw(value)}
        for key, value in sorted(values.items())
        if value
    ]


def first_difference(left, right):
    for key in sorted(left.keys() | right.keys()):
        if left.get(key, F(0)) != right.get(key, F(0)):
            return key, left.get(key, F(0)), right.get(key, F(0))
    return None


@cache
def subset_probability(o, e, m, n, x, y):
    return x**m * (1 - x) ** (o - m) * y**n * (1 - y) ** (e - n)


class RawOracle:
    def __init__(self, raw):
        self.raw = raw
        # Per-instance caches are bounded by this one session's finite domain;
        # no global method cache retains obsolete oracle instances.
        self.subsets = cache(self.subsets)
        self.transition = cache(self.transition)
        self.class_kernel = cache(self.class_kernel)
        self.states, self.frames = raw["states"], raw["frames"]
        self.registry = {
            state_key(s["frame_id"], s["kept"], s["past"]): s["state_id"] for s in self.states
        }
        self.features = [observed_features(s, self.frames[s["frame_id"]]) for s in self.states]
        keys = []
        for state, feature in zip(self.states, self.features, strict=True):
            frame = self.frames[state["frame_id"]]
            keys.append(
                [
                    [frame["density"], list(frame["fixed"]), list(frame["eligible"])],
                    feature["pair_graded"],
                    feature["motif_count"],
                    feature["path_count"],
                ]
            )
        self.partition = partition(keys)
        self.vector = self.partition["state_classes"]
        self.observations = [
            (s["frame_id"], *feature["chain_counts"])
            for s, feature in zip(self.states, self.features, strict=True)
        ]
        self.questions = [
            obs + (feature["motif_count"], feature["path_count"])
            for obs, feature in zip(self.observations, self.features, strict=True)
        ]
        self.classes, self.labels, self.profiles, self.fine = [], [], [], []
        profiles_by_state, local_by_state = [], []
        for state, feature in zip(self.states, self.features, strict=True):
            sid = state["state_id"]
            counts = {}
            fine_atoms = []
            for target in self.subsets(sid):
                cid = self.vector[target]
                counts[cid] = counts.get(cid, 0) + 1
                fine_atoms.append(
                    {
                        "target_state": target,
                        "coefficients": copy.deepcopy(
                            kernel(*feature["color_sizes"], *self.features[target]["color_sizes"])
                        ),
                    }
                )
            self.fine.append(
                {
                    "state_id": sid,
                    "transitions": sorted(fine_atoms, key=lambda atom: atom["target_state"]),
                }
            )
            profiles_by_state.append(
                {
                    "class_id": self.vector[sid],
                    "parent_color_sizes": list(feature["color_sizes"]),
                    "transitions": [
                        {
                            "target_class": cid,
                            "retained_color_sizes": list(
                                self.features[self.partition["classes"][cid]["members"][0]][
                                    "color_sizes"
                                ]
                            ),
                            "multiplicity": count,
                        }
                        for cid, count in sorted(counts.items())
                    ],
                }
            )
            local = {
                "class_id": self.vector[sid],
                "frame_id": state["frame_id"],
                "parent_color_sizes": list(feature["color_sizes"]),
            }
            eligible = set(state["kept"]) & set(self.frames[state["frame_id"]]["eligible"])
            for color, parity in (("odd", 1), ("even", 0)):
                local_counts = {}
                for vertex in eligible:
                    if vertex % 2 == parity:
                        target = self.registry[
                            induced_key(state, [v for v in state["kept"] if v != vertex])
                        ]
                        cid = self.vector[target]
                        local_counts[cid] = local_counts.get(cid, 0) + 1
                local[color] = [
                    {"target_class": cid, "multiplicity": count}
                    for cid, count in sorted(local_counts.items())
                ]
            local_by_state.append(local)
        self.state_profiles = profiles_by_state
        self.local_by_state = local_by_state
        for group in self.partition["classes"]:
            cid, members = group["class_id"], group["members"]
            first = members[0]
            for sid in members:
                assert local_by_state[sid] == local_by_state[first]
                assert profiles_by_state[sid] == profiles_by_state[first]
                assert self.observations[sid] == self.observations[first]
                assert self.questions[sid] == self.questions[first]
            self.classes.append(local_by_state[first])
            self.profiles.append(profiles_by_state[first])
            self.labels.append(
                {
                    "class_id": cid,
                    "observation": list(self.observations[first]),
                    "question": list(self.questions[first]),
                }
            )
        cert, operators = certificates(self.classes, self.profiles)
        self.model = {"classes": self.classes, "labels": self.labels}
        self.reconstruction = {
            "profiles_sha256": digest(self.profiles),
            "profile_atoms": sum(len(row["transitions"]) for row in self.profiles),
            "certificate": cert,
            "operator_checks": operators,
        }

    def subsets(self, sid):
        state = self.states[sid]
        frame = self.frames[state["frame_id"]]
        eligible = sorted(set(state["kept"]) & set(frame["eligible"]))
        return tuple(
            self.registry[
                induced_key(
                    state,
                    sorted(frame["fixed"] + [v for i, v in enumerate(eligible) if mask & (1 << i)]),
                )
            ]
            for mask in range(1 << len(eligible))
        )

    def transition(self, sid, x, y):
        o, e = self.features[sid]["color_sizes"]
        result = []
        for target in self.subsets(sid):
            m, n = self.features[target]["color_sizes"]
            probability = subset_probability(o, e, m, n, x, y)
            if probability:
                result.append((target, probability))
        assert sum(p for _, p in result) == 1
        return tuple(result)

    def coarse(self, raw_mass):
        result = {}
        for sid, mass in raw_mass.items():
            accumulate(result, self.vector[sid], mass)
        return result

    def advance(self, raw_mass, rates):
        result = {}
        for sid, mass in raw_mass.items():
            for target, probability in self.transition(sid, *rates):
                accumulate(result, target, mass * probability)
        return result

    def predict(self, raw_mass, rates):
        result = {}
        for sid, mass in self.advance(raw_mass, rates).items():
            accumulate(result, self.questions[sid], mass)
        return result

    def class_kernel(self, x, y):
        result = []
        for group in self.partition["classes"]:
            value = self.coarse(dict(self.transition(group["members"][0], x, y)))
            result.append(
                {
                    "class_id": group["class_id"],
                    "transitions": [
                        {"target_class": cid, "probability": fw(p)}
                        for cid, p in sorted(value.items())
                    ],
                }
            )
        return result


def normalized(values):
    mass = sum(values.values())
    assert mass > 0
    return {key: value / mass for key, value in values.items() if value}


NAMES = ("N", "NMT", "H")
EDGES = (("baseline", "N"), ("N", "NMT"), ("NMT", "H"))


def squared_distance(left, right):
    return sum((left.get(q, F(0)) - right.get(q, F(0))) ** 2 for q in left.keys() | right.keys())


def bayes_risk(law):
    assert sum(law.values()) == 1
    return 1 - sum(p * p for p in law.values())


@pytest.fixture(scope="session")
def pinned_u():
    path = HERE.parent / "qr-05u-partial-observation-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 1320664 and hashlib.sha256(raw).hexdigest() == U_SHA
    envelope = json.loads(raw)
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


@pytest.fixture(scope="session")
def supplied(pinned_u):
    return {
        "raw_model": copy.deepcopy(pinned_u["raw_model"]),
        "model": copy.deepcopy(pinned_u["model"]),
        "cases": [
            {
                **{
                    key: copy.deepcopy(row[key])
                    for key in ("case_id", "raw_prior", "prior", "rates")
                },
                "u_analysis": copy.deepcopy(row["analysis"]),
            }
            for row in pinned_u["cases"]
        ],
    }


def problem_for(model, case):
    return {
        "schema_version": "det8-qr05v-problem-v1",
        "family": "qr05v_readout_value",
        "model": model,
        "rate": case["rates"][2],
        "beliefs": [
            {"belief_id": index, "weight": row["likelihood"], "posterior": row["posterior"]}
            for index, row in enumerate(case["u_analysis"]["histories"])
        ],
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05v_test_direct", "readout_value.py"),
        private_module("_qr05v_test_reference", "reference_qr05v.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors, supplied):
    result = []
    for case in supplied["cases"]:
        p = problem_for(supplied["model"], case)
        before = wire(p)
        result.append(tuple(module.analyze(p) for module in executors))
        assert wire(p) == before
    return result


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05v_test_runner", "study.py")
    return runner, runner.run_suite()


@pytest.fixture(scope="session")
def oracle(supplied):
    return RawOracle(supplied["raw_model"])


def authenticated_histories(oracle, case):
    initial = {row["state_id"]: fraction(row["probability"]) for row in case["raw_prior"]}
    rates = [tuple(fraction(pair) for pair in rate) for rate in case["rates"]]
    first, histories = {}, {}
    for sid, p in oracle.advance(initial, rates[0]).items():
        accumulate(first.setdefault(oracle.observations[sid], {}), sid, p)
    for y1, mass in first.items():
        for sid, p in oracle.advance(mass, rates[1]).items():
            accumulate(histories.setdefault((y1, oracle.observations[sid]), {}), sid, p)
    received = case["u_analysis"]["histories"]
    assert len(histories) == len(received)
    result = []
    for (history, mass), row in zip(sorted(histories.items()), received, strict=True):
        weight, posterior = sum(mass.values()), normalized(mass)
        assert [list(y) for y in history] == row["observations"]
        assert fw(weight) == row["likelihood"]
        assert fw(weight / sum(first[history[0]].values())) == row["conditional_likelihood"]
        assert belief(oracle.coarse(posterior)) == row["posterior"]
        assert question_law(oracle.predict(posterior, rates[2])) == row["prediction"]
        result.append((history, weight, posterior))
    assert sum(weight for _, weight, _ in result) == 1
    return result


def cell_wire(cell):
    return {
        "value": list(cell["value"]),
        "probability": fw(cell["probability"]),
        "posterior": belief(cell["posterior"]),
        "prediction": question_law(cell["prediction"]),
        "risk": fw(cell["risk"]),
    }


class PairRiskOracle:
    def __init__(self, oracle):
        self.oracle = oracle
        self.future = cache(self.future)
        self.disagreement = cache(self.disagreement)

    def future(self, sid, rate):
        return self.oracle.predict({sid: F(1)}, rate)

    def disagreement(self, left, right, rate):
        a, b = self.future(left, rate), self.future(right, rate)
        return sum(pa * pb for qa, pa in a.items() for qb, pb in b.items() if qa != qb)

    def risk(self, raw, rate):
        assert sum(raw.values()) == 1
        answer = sum(
            pa * pb * self.disagreement(min(a, b), max(a, b), rate)
            for a, pa in raw.items()
            for b, pb in raw.items()
        )
        assert 0 <= answer <= 1
        return answer


def raw_readout_value(oracle, pair, case):
    rate = tuple(fraction(value) for value in case["rates"][2])
    authenticated = authenticated_histories(oracle, case)
    rows = []
    for bid, (_, weight, raw) in enumerate(authenticated):
        baseline_law = oracle.predict(raw, rate)
        baseline_risk = pair.risk(raw, rate)
        assert baseline_risk == bayes_risk(baseline_law)
        current = oracle.coarse(raw)
        baseline = {
            "value": (),
            "probability": F(1),
            "posterior": current,
            "prediction": baseline_law,
            "risk": baseline_risk,
        }
        cells, readouts = {"baseline": [baseline]}, {}
        for name in NAMES:
            subgroups = {}
            for sid, p in raw.items():
                value = (
                    oracle.observations[sid]
                    if name == "N"
                    else oracle.questions[sid]
                    if name == "NMT"
                    else (oracle.vector[sid],)
                )
                accumulate(subgroups.setdefault(value, {}), sid, p)
            actual, marginal = [], {}
            for value, mass in sorted(subgroups.items()):
                probability = sum(mass.values())
                conditional = normalized(mass)
                future = oracle.predict(conditional, rate)
                risk = pair.risk(conditional, rate)
                assert risk == bayes_risk(future)
                actual.append(
                    {
                        "value": value,
                        "probability": probability,
                        "posterior": oracle.coarse(conditional),
                        "prediction": future,
                        "risk": risk,
                    }
                )
                for q, p in future.items():
                    accumulate(marginal, q, probability * p)
            assert marginal == baseline_law and sum(cell["probability"] for cell in actual) == 1
            expected_risk = sum(cell["probability"] * cell["risk"] for cell in actual)
            gain = baseline_risk - expected_risk
            variance = sum(
                cell["probability"] * squared_distance(cell["prediction"], baseline_law)
                for cell in actual
            )
            assert gain == variance >= 0
            # Independent unnormalized raw-pair route: divide each branch's
            # weighted pair contribution by that branch's own mass, not Σw².
            conditional_pair_risk = sum(
                sum(
                    pa * pb * pair.disagreement(min(a, b), max(a, b), rate)
                    for a, pa in mass.items()
                    for b, pb in mass.items()
                )
                / sum(mass.values())
                for mass in subgroups.values()
            )
            assert conditional_pair_risk == expected_risk
            cells[name] = actual
            readouts[name] = {
                "cells": [cell_wire(cell) for cell in actual],
                "expected_risk": fw(expected_risk),
                "gain": fw(gain),
                "variance_gain": fw(variance),
            }
        refinements = []
        for coarse, fine in EDGES:
            parent_checks = []
            risk_drop = variance_gain = F(0)
            for parent in cells[coarse]:
                children = [
                    child
                    for child in cells[fine]
                    if coarse == "baseline"
                    or (
                        child["value"][:5] == parent["value"]
                        if coarse == "N"
                        else tuple(oracle.labels[child["value"][0]]["question"]) == parent["value"]
                    )
                ]
                assert children
                assert sum(child["probability"] for child in children) == parent["probability"]
                current_mixture, future_mixture = {}, {}
                child_risk = conditional_variance = F(0)
                predictions_equal = True
                for child in children:
                    conditional_weight = child["probability"] / parent["probability"]
                    for cid, p in child["posterior"].items():
                        accumulate(current_mixture, cid, conditional_weight * p)
                    for q, p in child["prediction"].items():
                        accumulate(future_mixture, q, conditional_weight * p)
                    child_risk += conditional_weight * child["risk"]
                    conditional_variance += conditional_weight * squared_distance(
                        child["prediction"], parent["prediction"]
                    )
                    equal = child["prediction"] == parent["prediction"]
                    predictions_equal &= equal
                assert (
                    current_mixture == parent["posterior"]
                    and future_mixture == parent["prediction"]
                )
                conditional_drop = parent["risk"] - child_risk
                assert conditional_drop == conditional_variance >= 0
                assert (conditional_drop == 0) == predictions_equal
                risk_drop += parent["probability"] * conditional_drop
                variance_gain += parent["probability"] * conditional_variance
                parent_checks.append(
                    {
                        "value": list(parent["value"]),
                        "probability": fw(parent["probability"]),
                        "fine_values": [list(child["value"]) for child in children],
                        "mixture_sha256": digest(question_law(future_mixture)),
                        "conditional_risk_drop": fw(conditional_drop),
                        "conditional_variance_gain": fw(conditional_variance),
                        "predictions_equal": predictions_equal,
                    }
                )
            assert risk_drop == variance_gain
            assert (risk_drop == 0) == all(parent["predictions_equal"] for parent in parent_checks)
            refinements.append(
                {
                    "coarse": coarse,
                    "fine": fine,
                    "risk_drop": fw(risk_drop),
                    "variance_gain": fw(variance_gain),
                    "parent_checks": parent_checks,
                    "zero_gain_iff_equal": True,
                }
            )
        residual = sum(
            p * bayes_risk(pair.future(oracle.partition["classes"][cid]["members"][0], rate))
            for cid, p in current.items()
        )
        assert residual == fraction(readouts["H"]["expected_risk"])
        assert sum(fraction(r["risk_drop"]) for r in refinements) == fraction(readouts["H"]["gain"])
        rows.append(
            {
                "belief_id": bid,
                "weight": fw(weight),
                "posterior": belief(current),
                "baseline": {"prediction": question_law(baseline_law), "risk": fw(baseline_risk)},
                "readouts": readouts,
                "refinements": refinements,
                "oracle_residual": fw(residual),
                "checks": {
                    "probabilities_normalized": True,
                    "marginal_future_preserved": True,
                    "nested_mixtures": True,
                    "nested_risks": True,
                    "oracle_residual_identity": True,
                    "gains_telescope": True,
                    "N_already_known": len(cells["N"]) == 1,
                },
            }
        )
    aggregate_prediction = {}
    for row in rows:
        for atom in row["baseline"]["prediction"]:
            accumulate(
                aggregate_prediction,
                tuple(atom["value"]),
                fraction(row["weight"]) * fraction(atom["probability"]),
            )

    def weighted(getter):
        return fw(sum(fraction(row["weight"]) * getter(row) for row in rows))

    risk = {
        name: weighted(lambda row, name=name: fraction(row["readouts"][name]["expected_risk"]))
        for name in NAMES
    }
    gains = {
        name: weighted(lambda row, name=name: fraction(row["readouts"][name]["gain"]))
        for name in NAMES
    }
    kernel_rows = oracle.class_kernel(*rate)
    maps = {
        "NMT_to_N": [
            {"fine": list(value), "coarse": list(value[:5])}
            for value in sorted({tuple(row["question"]) for row in oracle.labels})
        ],
        "H_to_NMT": [
            {"fine": [row["class_id"]], "coarse": row["question"]} for row in oracle.labels
        ],
    }
    result = {
        "model_sha256": digest(oracle.model),
        "reconstruction": oracle.reconstruction,
        "rate": case["rates"][2],
        "kernel_sha256": digest(kernel_rows),
        "readout_maps": maps,
        "beliefs": rows,
        "aggregate": {
            "total_weight": [1, 1],
            "prediction": question_law(aggregate_prediction),
            "baseline_risk": weighted(lambda row: fraction(row["baseline"]["risk"])),
            "expected_risk": risk,
            "gain": gains,
            "adjacent_gain": [
                weighted(lambda row, index=index: fraction(row["refinements"][index]["risk_drop"]))
                for index in range(3)
            ],
            "oracle_residual": weighted(lambda row: fraction(row["oracle_residual"])),
        },
        "witnesses": {
            "first_strict": [
                next(
                    (
                        row["belief_id"]
                        for row in rows
                        if fraction(row["refinements"][i]["risk_drop"]) > 0
                    ),
                    None,
                )
                for i in range(3)
            ],
            "first_zero": [
                next(
                    (
                        row["belief_id"]
                        for row in rows
                        if fraction(row["refinements"][i]["risk_drop"]) == 0
                    ),
                    None,
                )
                for i in range(3)
            ],
            "first_positive_oracle_residual": next(
                (row["belief_id"] for row in rows if fraction(row["oracle_residual"]) > 0), None
            ),
            "first_zero_oracle_residual": next(
                (row["belief_id"] for row in rows if fraction(row["oracle_residual"]) == 0), None
            ),
        },
        "counts": {
            "classes": len(oracle.classes),
            "beliefs": len(rows),
            "profile_atoms": oracle.reconstruction["profile_atoms"],
            "kernel_atoms": sum(len(row["transitions"]) for row in kernel_rows),
            "posterior_atoms": sum(len(row["posterior"]) for row in rows),
            "readout_cells": {
                name: sum(len(row["readouts"][name]["cells"]) for row in rows) for name in NAMES
            },
            "readout_posterior_atoms": {
                name: sum(
                    len(cell["posterior"])
                    for row in rows
                    for cell in row["readouts"][name]["cells"]
                )
                for name in NAMES
            },
            "readout_prediction_atoms": {
                name: sum(
                    len(cell["prediction"])
                    for row in rows
                    for cell in row["readouts"][name]["cells"]
                )
                for name in NAMES
            },
            "refinement_parents": [
                sum(len(row["refinements"][i]["parent_checks"]) for row in rows) for i in range(3)
            ],
            "strict_gain_beliefs": {
                name: sum(fraction(row["readouts"][name]["gain"]) > 0 for row in rows)
                for name in NAMES
            },
            "no_gain_beliefs": {
                name: sum(fraction(row["readouts"][name]["gain"]) == 0 for row in rows)
                for name in NAMES
            },
            "positive_oracle_residual_beliefs": sum(
                fraction(row["oracle_residual"]) > 0 for row in rows
            ),
            "known_N_beliefs": sum(row["checks"]["N_already_known"] for row in rows),
        },
    }
    return result, authenticated


@pytest.fixture(scope="session")
def expected(oracle, supplied):
    pair = PairRiskOracle(oracle)
    return [raw_readout_value(oracle, pair, case) for case in supplied["cases"]]


def test_producer_model_and_all_482_current_beliefs_are_raw_authenticated(
    supplied, oracle, expected
):
    assert wire(supplied["model"]) == wire(oracle.model)
    assert len(oracle.states) == 4447 and len(oracle.classes) == 416
    assert sum(len(histories) for _, histories in expected) == 482
    for case, (a, histories) in zip(supplied["cases"], expected, strict=True):
        p = problem_for(supplied["model"], case)
        assert [row["posterior"] for row in a["beliefs"]] == [
            row["posterior"] for row in p["beliefs"]
        ]
        assert [row["weight"] for row in a["beliefs"]] == [
            row["likelihood"] for row in case["u_analysis"]["histories"]
        ]
        assert (
            a["aggregate"]["prediction"] == case["u_analysis"]["unconditional"]["next_prediction"]
        )
        for row, (history, _, raw) in zip(a["beliefs"], histories, strict=True):
            assert {oracle.observations[sid] for sid in raw} == {history[1]}
            assert row["checks"]["N_already_known"] is True
            assert len(row["readouts"]["N"]["cells"]) == 1
            assert row["readouts"]["N"]["gain"] == row["refinements"][0]["risk_drop"] == [0, 1]


@pytest.mark.parametrize("case_index", range(6))
def test_complete_native_outputs_equal_raw_joint_and_independent_two_replica_oracles(
    analyses, expected, case_index
):
    primary, reference = analyses[case_index]
    a, _ = expected[case_index]
    assert wire(primary) == wire(reference) == wire(a)
    assert wire(json.loads(wire(primary))) == wire(primary)
    assert len(wire(primary)) < 64 * 1024 * 1024


def test_every_raw_members_fixed_K3_law_is_equal_inside_actual_H_fibers(supplied, oracle):
    rates = {tuple(fraction(pair) for pair in case["rates"][2]) for case in supplied["cases"]}
    for rate in rates:
        classes = oracle.class_kernel(*rate)
        for sid, cid in enumerate(oracle.vector):
            raw = oracle.coarse(dict(oracle.transition(sid, *rate)))
            assert raw == {
                atom["target_class"]: fraction(atom["probability"])
                for atom in classes[cid]["transitions"]
            }


def laws_from_wire(law):
    return {tuple(atom["value"]): fraction(atom["probability"]) for atom in law}


def test_complete_alphabet_parent_mixtures_nesting_and_zero_gain_equivalences(expected):
    for a, _ in expected:
        for row in a["beliefs"]:
            base = laws_from_wire(row["baseline"]["prediction"])
            assert fraction(row["baseline"]["risk"]) == bayes_risk(base)
            risk_sequence = [fraction(row["baseline"]["risk"])] + [
                fraction(row["readouts"][name]["expected_risk"]) for name in NAMES
            ]
            assert all(left >= right >= 0 for left, right in pairwise(risk_sequence))
            assert sum(fraction(edge["risk_drop"]) for edge in row["refinements"]) == fraction(
                row["readouts"]["H"]["gain"]
            )
            assert row["oracle_residual"] == row["readouts"]["H"]["expected_risk"]
            for name in NAMES:
                cells = row["readouts"][name]["cells"]
                future, posterior = {}, {}
                for cell in cells:
                    probability = fraction(cell["probability"])
                    assert probability > 0
                    assert sum(fraction(atom["probability"]) for atom in cell["posterior"]) == 1
                    for atom in cell["prediction"]:
                        accumulate(
                            future,
                            tuple(atom["value"]),
                            probability * fraction(atom["probability"]),
                        )
                    for atom in cell["posterior"]:
                        accumulate(
                            posterior, atom["class_id"], probability * fraction(atom["probability"])
                        )
                    assert fraction(cell["risk"]) == bayes_risk(laws_from_wire(cell["prediction"]))
                assert future == base and belief(posterior) == row["posterior"]
                assert fraction(row["readouts"][name]["gain"]) == sum(
                    fraction(cell["probability"])
                    * squared_distance(laws_from_wire(cell["prediction"]), base)
                    for cell in cells
                )
            for i, edge in enumerate(row["refinements"]):
                assert (edge["coarse"], edge["fine"]) == EDGES[i]
                assert edge["risk_drop"] == edge["variance_gain"]
                assert edge["zero_gain_iff_equal"] is True
                assert (fraction(edge["risk_drop"]) == 0) == all(
                    parent["predictions_equal"] for parent in edge["parent_checks"]
                )
                assert fraction(edge["risk_drop"]) == sum(
                    fraction(parent["probability"]) * fraction(parent["conditional_risk_drop"])
                    for parent in edge["parent_checks"]
                )
                for parent in edge["parent_checks"]:
                    assert parent["conditional_risk_drop"] == parent["conditional_variance_gain"]
                    assert parent["fine_values"] == sorted(parent["fine_values"])


def test_aggregate_is_likelihood_weighted_risk_not_uniform_or_risk_of_average_prediction(expected):
    for a, _ in expected:
        rows = a["beliefs"]
        total = sum(fraction(row["weight"]) for row in rows)
        assert total == 1
        weighted_risk = sum(
            fraction(row["weight"]) * fraction(row["baseline"]["risk"]) for row in rows
        )
        assert fraction(a["aggregate"]["baseline_risk"]) == weighted_risk
        mixed = laws_from_wire(a["aggregate"]["prediction"])
        between = sum(
            fraction(row["weight"])
            * squared_distance(laws_from_wire(row["baseline"]["prediction"]), mixed)
            for row in rows
        )
        assert bayes_risk(mixed) - weighted_risk == between >= 0
        for name in NAMES:
            assert fraction(a["aggregate"]["gain"][name]) == sum(
                fraction(row["weight"]) * fraction(row["readouts"][name]["gain"]) for row in rows
            )
        assert sum(fraction(value) for value in a["aggregate"]["adjacent_gain"]) == fraction(
            a["aggregate"]["gain"]["H"]
        )


def test_witnesses_and_counts_are_actual_first_occurrences_without_existence_assumptions(expected):
    for a, _ in expected:
        rows, counts = a["beliefs"], a["counts"]
        for index in range(3):
            strict = [
                row["belief_id"]
                for row in rows
                if fraction(row["refinements"][index]["risk_drop"]) > 0
            ]
            zero = [
                row["belief_id"]
                for row in rows
                if fraction(row["refinements"][index]["risk_drop"]) == 0
            ]
            assert a["witnesses"]["first_strict"][index] == (strict[0] if strict else None)
            assert a["witnesses"]["first_zero"][index] == (zero[0] if zero else None)
            assert counts["refinement_parents"][index] == sum(
                len(row["refinements"][index]["parent_checks"]) for row in rows
            )
        for name in NAMES:
            assert counts["strict_gain_beliefs"][name] + counts["no_gain_beliefs"][name] == len(
                rows
            )
            assert counts["readout_cells"][name] == sum(
                len(row["readouts"][name]["cells"]) for row in rows
            )


def micro_model():
    classes = [
        {"class_id": 0, "frame_id": 0, "parent_color_sizes": [0, 0], "odd": [], "even": []},
        {
            "class_id": 1,
            "frame_id": 0,
            "parent_color_sizes": [1, 0],
            "odd": [{"target_class": 0, "multiplicity": 1}],
            "even": [],
        },
        {
            "class_id": 2,
            "frame_id": 0,
            "parent_color_sizes": [0, 1],
            "odd": [],
            "even": [{"target_class": 0, "multiplicity": 1}],
        },
        {"class_id": 3, "frame_id": 1, "parent_color_sizes": [0, 0], "odd": [], "even": []},
    ]
    observations = [[0, 1, 0, 0, 0], [0, 1, 1, 0, 0], [0, 1, 1, 0, 0], [1, 1, 1, 0, 0]]
    return {
        "classes": classes,
        "labels": [
            {"class_id": cid, "observation": obs, "question": obs + [0, 0]}
            for cid, obs in enumerate(observations)
        ],
    }


def micro_problem(kind="equal"):
    model = micro_model()
    if kind in ("equal", "unequal", "delete"):
        prior = [{"class_id": 1, "probability": [1, 2]}, {"class_id": 2, "probability": [1, 2]}]
        rate = (
            [[1, 2], [1, 2]]
            if kind == "equal"
            else [[1, 3], [2, 3]]
            if kind == "unequal"
            else [[0, 1], [0, 1]]
        )
    else:
        prior = [{"class_id": 0, "probability": [1, 4]}, {"class_id": 1, "probability": [3, 4]}]
        rate = [[1, 2], [1, 2]] if kind == "branch" else [[1, 1], [1, 1]]
    return {
        "schema_version": "det8-qr05v-problem-v1",
        "family": "qr05v_readout_value",
        "model": model,
        "rate": rate,
        "beliefs": [{"belief_id": 0, "weight": [1, 1], "posterior": prior}],
    }


@pytest.fixture(scope="session")
def micro_analyses(executors):
    result = {}
    for kind in ("equal", "unequal", "delete", "branch", "identity"):
        a, b = (module.analyze(micro_problem(kind)) for module in executors)
        assert wire(a) == wire(b)
        result[kind] = a
    return result


def test_changed_current_beliefs_can_have_zero_value_with_positive_oracle_residual(micro_analyses):
    row = micro_analyses["equal"]["beliefs"][0]
    assert row["baseline"]["risk"] == row["oracle_residual"] == [1, 2]
    for name in NAMES:
        assert row["readouts"][name]["gain"] == [0, 1]
        assert row["readouts"][name]["expected_risk"] == [1, 2]
    assert len(row["readouts"]["H"]["cells"]) == 2
    for cell in row["readouts"]["H"]["cells"]:
        assert cell["prediction"] == row["baseline"]["prediction"]
        assert len(cell["posterior"]) == 1 and cell["posterior"] != row["posterior"]
    assert all(
        edge["zero_gain_iff_equal"]
        and all(parent["predictions_equal"] for parent in edge["parent_checks"])
        for edge in row["refinements"]
    )
    # Two independent Bernoulli future trials disagree with probability1/2;
    # illicitly reusing a single future draw would give0.
    assert bayes_risk({0: F(1, 2), 1: F(1, 2)}) == F(1, 2)


def test_unequal_singleton_rates_have_exact_positive_H_value_but_no_NMT_gain(micro_analyses):
    row = micro_analyses["unequal"]["beliefs"][0]
    assert row["baseline"]["risk"] == [1, 2]
    assert row["readouts"]["N"]["gain"] == row["readouts"]["NMT"]["gain"] == [0, 1]
    assert row["readouts"]["H"]["expected_risk"] == row["oracle_residual"] == [4, 9]
    assert row["readouts"]["H"]["gain"] == [1, 18]
    assert [edge["risk_drop"] for edge in row["refinements"]] == [[0, 1], [0, 1], [1, 18]]


def test_unequal_readout_masses_require_per_cell_pair_normalization(micro_analyses):
    row = micro_analyses["branch"]["beliefs"][0]
    assert row["baseline"]["risk"] == [15, 32]
    assert row["oracle_residual"] == [3, 8]
    assert row["checks"]["N_already_known"] is False
    for name in NAMES:
        assert row["readouts"][name]["expected_risk"] == [3, 8]
        assert row["readouts"][name]["gain"] == [3, 32]
        assert [cell["probability"] for cell in row["readouts"][name]["cells"]] == [[1, 4], [3, 4]]
    unnormalized_same_cell_disagreement = F(3, 4) ** 2 * F(1, 2)
    global_equal_cell_conditioning = unnormalized_same_cell_disagreement / (
        F(1, 4) ** 2 + F(3, 4) ** 2
    )
    assert unnormalized_same_cell_disagreement == F(9, 32) != F(3, 8)
    assert global_equal_cell_conditioning == F(9, 20) != F(3, 8)


def test_unweighted_squared_distance_may_exceed_one_while_weighted_gain_is_valid(micro_analyses):
    row = micro_analyses["identity"]["beliefs"][0]
    assert row["baseline"]["risk"] == [3, 8]
    assert row["oracle_residual"] == [0, 1]
    assert row["checks"]["N_already_known"] is False
    base = laws_from_wire(row["baseline"]["prediction"])
    rare = row["readouts"]["N"]["cells"][0]
    distance = squared_distance(laws_from_wire(rare["prediction"]), base)
    assert distance == F(9, 8) > 1
    assert fraction(rare["probability"]) * distance == F(9, 32)
    assert row["readouts"]["N"]["gain"] == [3, 8]
    # A MAP forecast δ(singleton) has true Brier risk1/2 under this law,
    # whereas R(δ)=0 would incorrectly pretend that forecast were the truth.
    assert sum(
        p * sum((F(q == 1) - F(q == truth)) ** 2 for q in (0, 1))
        for truth, p in {0: F(1, 4), 1: F(3, 4)}.items()
    ) == F(1, 2)
    assert bayes_risk({1: F(1)}) == 0


def test_complete_deletion_leaves_no_future_risk_but_does_not_make_readouts_disturbing(
    micro_analyses,
):
    row = micro_analyses["delete"]["beliefs"][0]
    assert row["baseline"]["risk"] == row["oracle_residual"] == [0, 1]
    assert len(row["baseline"]["prediction"]) == 1
    for name in NAMES:
        assert row["readouts"][name]["gain"] == [0, 1]
        assert all(
            cell["prediction"] == row["baseline"]["prediction"]
            for cell in row["readouts"][name]["cells"]
        )


def test_supplied_history_weights_do_not_pool_distinct_forecasts_or_uniformize_risks(executors):
    p = micro_problem()
    p["beliefs"] = [
        {"belief_id": 0, "weight": [1, 4], "posterior": [{"class_id": 0, "probability": [1, 1]}]},
        {"belief_id": 1, "weight": [3, 4], "posterior": [{"class_id": 1, "probability": [1, 1]}]},
    ]
    for module in executors:
        a = module.analyze(p)
        assert [r["baseline"]["risk"] for r in a["beliefs"]] == [[0, 1], [1, 2]]
        assert a["aggregate"]["baseline_risk"] == a["aggregate"]["oracle_residual"] == [3, 8]
        assert bayes_risk(laws_from_wire(a["aggregate"]["prediction"])) == F(15, 32)
        assert F(3, 8) != F(1, 4)  # uniform history weighting is a different experiment
        assert all(a["aggregate"]["gain"][name] == [0, 1] for name in NAMES)


def test_reading_frame_can_resolve_deterministic_future_uncertainty(executors):
    p = micro_problem()
    p["beliefs"][0]["posterior"] = [
        {"class_id": 0, "probability": [1, 2]},
        {"class_id": 3, "probability": [1, 2]},
    ]
    for module in executors:
        row = module.analyze(p)["beliefs"][0]
        assert row["baseline"]["risk"] == [1, 2]
        assert row["oracle_residual"] == [0, 1]
        assert [cell["value"][0] for cell in row["readouts"]["N"]["cells"]] == [0, 1]
        assert [edge["risk_drop"] for edge in row["refinements"]] == [[1, 2], [0, 1], [0, 1]]


def test_middle_readout_gain_uses_supplied_current_NMT_labels_not_H_or_future_outcomes(executors):
    # An algebraic local model, not a newly certified raw-order family. Two
    # distinct top labels have the same ranks and deletion rows. The public
    # API validates annotations structurally; only the raw runner can certify
    # that such annotations correspond to actual observed motifs.
    classes, labels = [], []
    for odd, even in product(range(3), repeat=2):
        cid = 3 * odd + even
        classes.append(
            {
                "class_id": cid,
                "frame_id": 0,
                "parent_color_sizes": [odd, even],
                "odd": [{"target_class": cid - 3, "multiplicity": odd}] if odd else [],
                "even": [{"target_class": cid - 1, "multiplicity": even}] if even else [],
            }
        )
        obs = [0, 1, odd + even, 0, 0]
        labels.append({"class_id": cid, "observation": obs, "question": obs + [0, 0]})
    classes.append({**copy.deepcopy(classes[8]), "class_id": 9})
    labels.append(
        {
            "class_id": 9,
            "observation": list(labels[8]["observation"]),
            "question": labels[8]["observation"] + [1, 0],
        }
    )
    p = micro_problem("identity")
    p["model"] = {"classes": classes, "labels": labels}
    p["beliefs"][0]["posterior"] = [
        {"class_id": 8, "probability": [1, 2]},
        {"class_id": 9, "probability": [1, 2]},
    ]
    for module in executors:
        row = module.analyze(p)["beliefs"][0]
        assert row["checks"]["N_already_known"] is True
        assert row["baseline"]["risk"] == [1, 2]
        assert [edge["risk_drop"] for edge in row["refinements"]] == [[0, 1], [1, 2], [0, 1]]
        assert row["oracle_residual"] == [0, 1]
        assert [len(row["readouts"][name]["cells"]) for name in NAMES] == [1, 2, 2]


class IntChild(int):
    pass


class StrChild(str):
    pass


class ListChild(list):
    pass


class DictChild(dict):
    pass


def invalid_problems():
    p = micro_problem()
    cases = [
        None,
        [],
        {},
        DictChild(p),
        {**p, "extra": 0},
        {**p, "readouts": ["N"]},
        {**p, "target": "H"},
        {**p, "schema_version": "det8-qr05u-problem-v1"},
        {**p, "family": "other"},
        {**p, "beliefs": []},
        {**p, "rate": []},
    ]
    mutations = [
        (("schema_version",), StrChild(p["schema_version"])),
        (("model",), DictChild(p["model"])),
        (("model", "classes"), ListChild(p["model"]["classes"])),
        (("model", "classes", 0, "class_id"), False),
        (("model", "classes", 0, "frame_id"), IntChild(0)),
        (("model", "classes", 1, "parent_color_sizes"), [True, 0]),
        (("model", "classes", 1, "odd", 0, "multiplicity"), True),
        (("model", "classes", 1, "odd", 0, "target_class"), False),
        (("model", "classes", 1, "odd"), []),
        (("model", "classes", 1, "odd", 0, "multiplicity"), 2),
        (("model", "classes", 1, "odd", 0, "target_class"), 1),
        (("model", "labels"), []),
        (("model", "labels", 0, "class_id"), False),
        (("model", "labels", 0, "observation", 1), True),
        (("model", "labels", 0, "question", 1), IntChild(1)),
        (("model", "labels", 1, "observation", 2), 0),
        (("model", "labels", 1, "question", 5), 1),
        (("model", "labels", 1, "question", 6), 1),
        (("model", "labels", 3, "question", 0), 0),  # zero-prior class: global nesting
        (("model", "labels", 3, "observation", 0), 0),
        (("model", "labels", 3, "observation", 3), 1),
        (("model", "labels", 3, "question"), [1, 1, 1, 0, 0]),
        (("rate",), ((1, 2), (1, 2))),
        (("rate", 0), [2, 4]),
        (("rate", 0), [0, 2]),
        (("rate", 0), [2, 2]),
        (("rate", 0), [-1, 2]),
        (("rate", 0), [1, 0]),
        (("rate", 0), [2, 1]),
        (("rate", 0), [True, 2]),
        (("rate", 0), [1.0, 2]),
        (("rate", 0), [1, 1 << 64]),
        (("rate", 0), "1/2"),
        (("beliefs",), ListChild(p["beliefs"])),
        (("beliefs", 0, "belief_id"), False),
        (("beliefs", 0, "belief_id"), 1),
        (("beliefs", 0, "weight"), [0, 1]),
        (("beliefs", 0, "weight"), [1, 2]),
        (("beliefs", 0, "weight"), [2, 2]),
        (("beliefs", 0, "weight"), [True, 1]),
        (("beliefs", 0, "posterior"), []),
        (("beliefs", 0, "posterior"), list(reversed(p["beliefs"][0]["posterior"]))),
        (("beliefs", 0, "posterior", 0, "class_id"), True),
        (("beliefs", 0, "posterior", 1, "class_id"), 1),
        (("beliefs", 0, "posterior", 1, "class_id"), 4),
        (("beliefs", 0, "posterior", 0, "probability"), [0, 1]),
        (("beliefs", 0, "posterior", 0, "probability"), [1, 3]),
        (("beliefs", 0, "posterior", 0, "probability"), [2, 4]),
        (("beliefs", 0, "posterior", 0, "probability"), [1, 1 << 4096]),
        (("beliefs", 0, "posterior", 0, "probability"), (1, 2)),
    ]
    cases += [replaced(p, path, value) for path, value in mutations]
    cases.append({StrChild(k): v for k, v in p.items()})
    cases.append({**p, "beliefs": [{**p["beliefs"][0], "raw_state": 612}]})
    return cases


@pytest.mark.parametrize("index", range(len(invalid_problems())))
def test_typed_canonical_input_contract_rejects_without_silent_repair(executors, index):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problems()[index])


def test_belief_and_history_weight_components_use_4096_not_rate_64_bit_bound(executors):
    denominator = (1 << 80) + 1
    p = micro_problem()
    p["beliefs"] = [
        {
            "belief_id": 0,
            "weight": [1, denominator],
            "posterior": [
                {"class_id": 1, "probability": [1, denominator]},
                {"class_id": 2, "probability": [denominator - 1, denominator]},
            ],
        },
        {
            "belief_id": 1,
            "weight": [denominator - 1, denominator],
            "posterior": [{"class_id": 0, "probability": [1, 1]}],
        },
    ]
    for module in executors:
        a = module.analyze(p)
        assert a["beliefs"][0]["weight"] == [1, denominator]
        assert a["beliefs"][0]["posterior"] == p["beliefs"][0]["posterior"]
        assert a["aggregate"]["baseline_risk"] == [1, 2 * denominator]
        assert a["aggregate"]["gain"]["H"] == [0, 1]


def test_global_maps_include_zero_mass_states_and_reverse_class_numbering_is_valid(executors):
    p = micro_problem("unequal")
    ids = {old: 3 - old for old in range(4)}
    reverse = copy.deepcopy(p)
    reverse["model"]["classes"] = []
    reverse["model"]["labels"] = []
    for old in reversed(p["model"]["classes"]):
        reverse["model"]["classes"].append(
            {
                **old,
                "class_id": ids[old["class_id"]],
                **{
                    color: sorted(
                        [
                            {**atom, "target_class": ids[atom["target_class"]]}
                            for atom in old[color]
                        ],
                        key=lambda x: x["target_class"],
                    )
                    for color in ("odd", "even")
                },
            }
        )
    reverse["model"]["labels"] = [
        {**row, "class_id": ids[row["class_id"]]} for row in reversed(p["model"]["labels"])
    ]
    reverse["beliefs"][0]["posterior"] = sorted(
        [{**atom, "class_id": ids[atom["class_id"]]} for atom in p["beliefs"][0]["posterior"]],
        key=lambda x: x["class_id"],
    )
    for module in executors:
        a, b = module.analyze(p), module.analyze(reverse)
        assert a["aggregate"] == b["aggregate"]
        assert a["beliefs"][0]["baseline"] == b["beliefs"][0]["baseline"]
        assert len(a["readout_maps"]["H_to_NMT"]) == 4
        assert a["readout_maps"]["H_to_NMT"][3] == {"fine": [3], "coarse": [1, 1, 1, 0, 0, 0, 0]}
        assert any(atom["coarse"][0] == 1 for atom in a["readout_maps"]["NMT_to_N"])
        assert all(cell["value"] != [3] for cell in a["beliefs"][0]["readouts"]["H"]["cells"])


def malformed_algebra(kind):
    if kind == "fractional":
        ranks = [[3, 0], [2, 0], [2, 0], [1, 0], [1, 0], [0, 0]]
        odd = [[(1, 1), (2, 2)], [(3, 1), (4, 1)], [(4, 2)], [(5, 1)], [(5, 1)], []]
        even = [[] for _ in ranks]
    else:
        ranks = [[1, 1], [0, 1], [1, 0], [0, 0], [0, 0]]
        odd, even = [[(1, 1)], [], [(4, 1)], [], []], [[(2, 1)], [(3, 1)], [], [], []]
    classes = [
        {
            "class_id": cid,
            "frame_id": 0,
            "parent_color_sizes": rank,
            "odd": [{"target_class": t, "multiplicity": m} for t, m in odd[cid]],
            "even": [{"target_class": t, "multiplicity": m} for t, m in even[cid]],
        }
        for cid, rank in enumerate(ranks)
    ]
    model = {
        "classes": classes,
        "labels": [
            {
                "class_id": cid,
                "observation": [0, 1, sum(rank), 0, 0],
                "question": [0, 1, sum(rank), 0, 0, 0, 0],
            }
            for cid, rank in enumerate(ranks)
        ],
    }
    p = micro_problem()
    p["model"] = model
    p["beliefs"][0]["posterior"] = [{"class_id": 0, "probability": [1, 1]}]
    return p


@pytest.mark.parametrize("kind", ["fractional", "mixed"])
def test_readout_api_keeps_integrality_and_commuting_color_constructor_guards(executors, kind):
    p = malformed_algebra(kind)
    rows = p["model"]["classes"]
    for row in rows:
        for i, color in enumerate(("odd", "even")):
            assert sum(atom["multiplicity"] for atom in row[color]) == row["parent_color_sizes"][i]
    if kind == "fractional":
        assert word(rows, 0, ("odd", "odd"))[3] == 1  # /2! is not an integer
    else:
        assert word(rows, 0, ("odd", "even")) != word(rows, 0, ("even", "odd"))
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(p)


def mutable_ids(value):
    seen, stack = set(), [value]
    while stack:
        item = stack.pop()
        if type(item) not in (dict, list) or id(item) in seen:
            continue
        seen.add(id(item))
        stack.extend(item.values() if type(item) is dict else item)
    return seen


def test_entire_output_is_detached_from_inputs_and_other_results_in_both_directions(executors):
    for module in executors:
        p = micro_problem("branch")
        a, b = module.analyze(p), module.analyze(p)
        wanted, before = wire(b), wire(p)
        assert mutable_ids(a).isdisjoint(mutable_ids(p))
        assert mutable_ids(a).isdisjoint(mutable_ids(b))
        a["beliefs"][0]["posterior"][0]["probability"][0] = -1
        a["beliefs"][0]["readouts"]["N"]["cells"][0]["value"][0] = 99
        a["readout_maps"]["H_to_NMT"][0]["coarse"][0] = 99
        a["aggregate"]["gain"]["H"][0] = -1
        assert wire(p) == before and wire(b) == wanted and wire(module.analyze(p)) == wanted
        p["beliefs"][0]["posterior"][0]["probability"][0] = -9
        assert wire(b) == wanted
        with pytest.raises(ValueError):
            module.analyze(p)


def test_ordinary_shared_input_containers_remain_valid_and_local_reconstruction_is_used(
    executors, monkeypatch
):
    for module in executors:
        p = micro_problem()
        shared = []
        for row in p["model"]["classes"]:
            for color in ("odd", "even"):
                if not row[color]:
                    row[color] = shared
        original, seen = module.reconstruct_profiles, []

        def delegated(payload, original=original, seen=seen):
            assert set(payload) == {"schema_version", "classes"}
            assert payload["schema_version"] == "det8-qr05s-local-v1"
            seen.append(wire(payload))
            return original(payload)

        with monkeypatch.context() as patched:
            patched.setattr(module, "reconstruct_profiles", delegated)
            result = module.analyze(p)
        assert seen and result["beliefs"][0]["oracle_residual"] == [1, 2]
        assert mutable_ids(result).isdisjoint(mutable_ids(p))


@pytest.mark.parametrize(
    "constant",
    [
        "WORKING_CAP",
        "CLASS_CAP",
        "CLASS_LOCAL_CAP",
        "PROFILE_ATOM_CAP",
        "BELIEF_CAP",
        "POSTERIOR_CAP",
        "CELL_CAP",
        "READOUT_POSTERIOR_CAP",
        "PREDICTION_CAP",
        "BIT_LIMIT",
    ],
)
def test_live_resource_and_derived_arithmetic_guards_are_not_truncation(
    executors, monkeypatch, constant
):
    p = micro_problem()
    if constant == "BELIEF_CAP":
        p["beliefs"] = [
            {
                "belief_id": i,
                "weight": [1, 2],
                "posterior": [{"class_id": i, "probability": [1, 1]}],
            }
            for i in range(2)
        ]
    if constant == "BIT_LIMIT":
        p["model"] = {key: value[:2] for key, value in p["model"].items()}
        p["beliefs"][0]["posterior"] = [{"class_id": 1, "probability": [1, 1]}]
        p["rate"] = [[1, 11], [1, 1]]
    for module in executors:
        wanted = wire(module.analyze(p))
        if constant == "BIT_LIMIT":
            assert json.loads(wanted)["beliefs"][0]["baseline"]["risk"] == [20, 121]
            assert (11).bit_length() <= 6 < (121).bit_length()
        with monkeypatch.context() as limited:
            limited.setattr(
                module,
                constant,
                32 if constant == "WORKING_CAP" else 6 if constant == "BIT_LIMIT" else 1,
            )
            with pytest.raises(ValueError):
                module.analyze(p)
        assert wire(module.analyze(p)) == wanted


def test_maximum_belief_count_is_inclusive_and_extra_beliefs_fail(executors):
    p = micro_problem()
    p["model"] = {key: value[:1] for key, value in p["model"].items()}
    p["beliefs"] = [
        {"belief_id": i, "weight": [1, 512], "posterior": [{"class_id": 0, "probability": [1, 1]}]}
        for i in range(512)
    ]
    for module in executors:
        a = module.analyze(p)
        assert a["counts"]["beliefs"] == 512
        assert a["aggregate"]["baseline_risk"] == [0, 1]
        bad = {
            **p,
            "beliefs": [
                {
                    "belief_id": i,
                    "weight": [1, 513],
                    "posterior": [{"class_id": 0, "probability": [1, 1]}],
                }
                for i in range(513)
            ],
        }
        with pytest.raises(ValueError):
            module.analyze(bad)


def test_whole_aggregate_native_wire_and_pinned_dependency_audit(
    aggregate, supplied, expected, oracle
):
    runner, suite = aggregate
    assert set(suite) == {
        "raw_model",
        "model",
        "cases",
        "independent_route_equal",
        "raw_bridge",
        "rate_audit",
        "public_controls",
        "totals",
    }
    assert wire(suite) == runner.canonical(suite) == wire(json.loads(wire(suite)))
    assert wire(suite["raw_model"]) == wire(supplied["raw_model"])
    assert wire(suite["model"]) == wire(supplied["model"])
    assert suite["independent_route_equal"] is True
    assert wire(runner.fixtures()) == wire(supplied)
    for case, actual, (wanted, _) in zip(supplied["cases"], suite["cases"], expected, strict=True):
        assert wire(actual) == wire({**case, "analysis": wanted})
        assert wire(runner.case_problem(supplied["model"], case)) == wire(
            problem_for(supplied["model"], case)
        )
    bridge = suite["raw_bridge"]
    assert bridge["prior_artifact"] == "qr-05u-partial-observation-2026-09-06/results.json"
    assert bridge["states"] == 4447 and bridge["classes"] == 416
    assert bridge["member_comparisons"] == 4447 - 416
    assert bridge["H_sha256"] == digest(oracle.partition)
    assert bridge["profiles_sha256"] == digest(oracle.profiles)
    assert bridge["fine_sha256"] == digest(oracle.fine)
    assert bridge["all_raw_members_authenticated"] is True
    assert bridge["U_complete_case_evidence_recomputed"] is True
    assert bridge["raw_model_local_labels_and_beliefs_declared_dependencies"] is True
    for name in (
        "U_native_API_conditioning_calls_replayed",
        "source_aliases_regenerated",
        "T_minimality_P_consumer_R_helper_Q_certificate_replayed",
    ):
        assert bridge[name] is False
    rate_audit = suite["rate_audit"]
    assert rate_audit["all_raw_members_checked"] is True
    assert len(rate_audit["rates"]) == 2
    assert rate_audit["raw_row_comparisons"] == 2 * 4447
    for row in rate_audit["rates"]:
        rate = tuple(map(fraction, row["rate"]))
        assert row["raw_rows_checked"] == 4447
        assert row["kernel_sha256"] == digest(oracle.class_kernel(*rate))
        assert row["raw_positive_atoms"] == sum(
            len(oracle.transition(sid, *rate)) for sid in range(4447)
        )
        assert row["class_positive_atoms"] == sum(
            len(r["transitions"]) for r in oracle.class_kernel(*rate)
        )
        assert row["max_abs_residual"] == [0, 1]
    totals = suite["totals"]
    assert totals["raw_states"] == 4447 and totals["classes"] == 416
    assert totals["cases"] == 6 and totals["analyze_calls"] == 12
    assert totals["invalid_analyze_calls_rejected"] == 14
    assert totals["beliefs"] == totals["known_N_beliefs"] == 482
    assert totals["posterior_atoms"] == 1026
    assert totals["raw_rate_rows_checked"] == 8894
    for key in ("readout_cells", "readout_prediction_atoms", "strict_gain_beliefs"):
        assert totals[key] == {
            name: sum(a["counts"][key][name] for a, _ in expected) for name in NAMES
        }
    assert totals["positive_oracle_residual_beliefs"] == sum(
        a["counts"]["positive_oracle_residual_beliefs"] for a, _ in expected
    )
    assert suite["public_controls"] == {
        "analyze_calls": 12,
        "invalid_analyze_calls_rejected": 14,
        "raw_orders_histories_or_artifacts_given_to_core": False,
    }


def output_mutations(a):
    row = a["beliefs"][0]
    probability = row["baseline"]["prediction"][0]["probability"]
    return [
        (("model_sha256",), "0" * 64),
        (("kernel_sha256",), "0" * 64),
        (("reconstruction", "profile_atoms"), a["reconstruction"]["profile_atoms"] + 1),
        (("rate", 0), [1, 1]),
        (("beliefs", 0, "belief_id"), False),
        (("beliefs", 0, "weight"), [1, 1]),
        (("beliefs", 0, "posterior", 0, "class_id"), -1),
        (("beliefs", 0, "baseline", "prediction", 0, "probability"), fw(F(*probability) / 2)),
        (("beliefs", 0, "baseline", "risk"), [1, 1]),
        (("beliefs", 0, "readouts", "N", "cells", 0, "probability"), [1, 2]),
        (("beliefs", 0, "readouts", "H", "cells", 0, "posterior", 0, "probability"), [1, 2]),
        (("beliefs", 0, "readouts", "N", "gain"), [1, 1]),
        (("beliefs", 0, "readouts", "N", "variance_gain"), [1, 1]),
        (("beliefs", 0, "refinements", 0, "parent_checks", 0, "fine_values"), []),
        (("beliefs", 0, "refinements", 0, "parent_checks", 0, "mixture_sha256"), "0" * 64),
        (("beliefs", 0, "refinements", 0, "parent_checks", 0, "conditional_risk_drop"), [1, 1]),
        (("beliefs", 0, "refinements", 0, "parent_checks", 0, "conditional_variance_gain"), [1, 1]),
        (("beliefs", 0, "refinements", 0, "parent_checks", 0, "predictions_equal"), False),
        (("beliefs", 0, "refinements", 0, "zero_gain_iff_equal"), False),
        (("beliefs", 0, "refinements", 0, "risk_drop"), [1, 1]),
        (("beliefs", 0, "oracle_residual"), [1, 1]),
        (("beliefs", 0, "checks", "N_already_known"), False),
        (("aggregate", "total_weight"), [2, 1]),
        (
            ("aggregate", "baseline_risk"),
            fw(bayes_risk(laws_from_wire(a["aggregate"]["prediction"])) + 1),
        ),
        (("aggregate", "adjacent_gain", 0), [1, 1]),
        (("witnesses", "first_strict", 0), 0),
        (("witnesses", "first_zero", 0), None),
        (("counts", "strict_gain_beliefs", "N"), 1),
        (("counts", "known_N_beliefs"), 0),
        (("readout_maps", "NMT_to_N", 0, "coarse", 0), -1),
        (("readout_maps", "H_to_NMT", 0, "coarse", 0), -1),
    ]


def test_complete_raw_checker_rejects_parent_maps_weights_marginals_and_witness_tampering(
    aggregate, supplied, expected
):
    runner, _ = aggregate
    model, case, a = supplied["raw_model"], supplied["cases"][0], expected[0][0]
    assert runner.check_analysis(a, model, case)["complete_native_output_equal"] is True
    before = wire(a)
    for path, value in output_mutations(a):
        bad = replaced(a, path, value)
        assert wire(bad) != before, path
        with pytest.raises(ValueError):
            runner.check_analysis(bad, model, case)
    # Keep the complete map cardinalities and all labels, but attach a parent
    # to the wrong child. Count-only audits must not certify the nesting.
    maps = a["readout_maps"]["H_to_NMT"]
    j = next(i for i in range(1, len(maps)) if maps[i]["coarse"] != maps[0]["coarse"])
    swapped = replaced(a, ("readout_maps", "H_to_NMT", 0, "coarse"), maps[j]["coarse"])
    swapped = replaced(swapped, ("readout_maps", "H_to_NMT", j, "coarse"), maps[0]["coarse"])
    assert len(swapped["readout_maps"]["H_to_NMT"]) == len(maps)
    with pytest.raises(ValueError):
        runner.check_analysis(swapped, model, case)
    assert wire(a) == before


def test_raw_checker_validates_native_content_before_cache_and_authenticates_U_evidence(
    aggregate, supplied, expected
):
    runner, _ = aggregate
    model, case, a = supplied["raw_model"], supplied["cases"][0], expected[0][0]
    report = runner.check_analysis(a, model, case)
    assert report["analysis_sha256"] == digest(a)
    for bad_model in (
        replaced(model, ("states", 0, "state_id"), IntChild(0)),
        replaced(model, ("states", 0, "frame_id"), False),
        {StrChild(key): value for key, value in model.items()},
    ):
        with pytest.raises(ValueError):
            runner.check_analysis(a, bad_model, case)
    for bad_case in (
        replaced(
            case,
            ("u_analysis", "histories", 0, "likelihood", 0),
            IntChild(case["u_analysis"]["histories"][0]["likelihood"][0]),
        ),
        replaced(case, ("u_analysis", "histories", 0, "likelihood"), [1, 1]),
        replaced(case, ("u_analysis", "histories", 0, "posterior", 0, "class_id"), -1),
        replaced(case, ("u_analysis", "histories", 0, "observations", 0, 0), -1),
        replaced(case, ("rates", 2, 0), [1, 1]),
    ):
        with pytest.raises(ValueError):
            runner.check_analysis(a, model, bad_case)
    assert runner.check_analysis(a, model, case) == report


def test_aggregate_wire_guard_does_not_coerce_equal_native_values(aggregate):
    runner, _ = aggregate
    for value in (
        {"nested": (0,)},
        {"nested": 0.5},
        {1: "x"},
        {StrChild("x"): 0},
        {"x": IntChild(0)},
    ):
        with pytest.raises(ValueError):
            runner.require_wire(value)
    for left, right in (({"x": [True]}, {"x": [1]}), ({"x": [0]}, {"x": [False]})):
        runner.require_wire(left)
        runner.require_wire(right)
        with pytest.raises(ValueError):
            runner.require_same_wire(left, right, "typed regression")


@pytest.mark.parametrize("optimized", [False, True])
def test_public_native_guards_reject_before_serialization_in_bounded_subprocess(
    tmp_path, optimized
):
    program = r"""
import copy, importlib.util, json, resource, sys
from pathlib import Path

resource.setrlimit(resource.RLIMIT_CPU, (12, 12))
test_path = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("_qr05v_guard_helpers", test_path)
if spec is None or spec.loader is None:
    raise RuntimeError("test helpers unavailable")
helpers = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = helpers
spec.loader.exec_module(helpers)

rejections = 0
before_serialization = 0
def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def reject(call, value):
    global rejections
    try:
        call(value)
    except ValueError:
        rejections += 1
    else:
        raise RuntimeError("malformed input or resource overflow was accepted")

def dag():
    value = []
    for _ in range(40):
        value = [value, value]
    return value

def graph_inputs(valid):
    cycle_list = []
    cycle_list.append(cycle_list)
    cycle_dict = {}
    cycle_dict["loop"] = cycle_dict
    deep = []
    for _ in range(1500):
        deep = [deep]
    for value in (cycle_list, cycle_dict, deep, dag()):
        bad = copy.deepcopy(valid)
        bad["extra"] = value
        yield bad
    for field in ("classes", "labels"):
        bad = copy.deepcopy(valid)
        bad["model"][field] = dag()
        yield bad
    for field in ("beliefs", "rate"):
        bad = copy.deepcopy(valid)
        bad[field] = dag()
        yield bad
    for field in ("posterior", "weight"):
        bad = copy.deepcopy(valid)
        bad["beliefs"][0][field] = dag()
        yield bad
    bad = copy.deepcopy(valid)
    bad["model"]["labels"][0]["question"] = dag()
    yield bad

def reject_before_dump(call, value):
    global before_serialization
    original = json.dumps
    def forbidden(*args, **kwargs):
        raise RuntimeError("unsafe object reached JSON serialization before rejection")
    json.dumps = forbidden
    try:
        reject(call, value)
        before_serialization += 1
    finally:
        json.dumps = original

invalid = helpers.invalid_problems()
for index, filename in enumerate(("readout_value.py", "reference_qr05v.py")):
    module = helpers.private_module("_qr05v_explicit_guard_" + str(index), filename)
    valid = helpers.micro_problem()
    reference = module.analyze(valid)
    require(reference["beliefs"][0]["baseline"]["risk"] == [1, 2], "true Brier baseline")
    require(reference["beliefs"][0]["oracle_residual"] == [1, 2], "fresh future uncertainty")
    require(all(reference["beliefs"][0]["readouts"][name]["gain"] == [0, 1]
                for name in ("N", "NMT", "H")), "equal future laws have no readout gain")
    for bad in invalid:
        reject(module.analyze, bad)
    for kind in ("fractional", "mixed"):
        reject(module.analyze, helpers.malformed_algebra(kind))
    graphs = list(graph_inputs(valid))
    require(len(graphs) == 11, "graph placement inventory")
    for bad in graphs:
        reject_before_dump(module.analyze, bad)

    # Exercise actual output/working/arithmetic caps, restoring them after each call.
    for constant, limit in (("WORKING_CAP", 32), ("CELL_CAP", 1), ("POSTERIOR_CAP", 1)):
        original = getattr(module, constant)
        setattr(module, constant, limit)
        try:
            reject(module.analyze, valid)
        finally:
            setattr(module, constant, original)
    arithmetic = helpers.micro_problem()
    arithmetic["model"] = {key: value[:2] for key, value in arithmetic["model"].items()}
    arithmetic["beliefs"][0]["posterior"] = [{"class_id": 1, "probability": [1, 1]}]
    arithmetic["rate"] = [[1, 11], [1, 1]]
    require(module.analyze(arithmetic)["beliefs"][0]["baseline"]["risk"] == [20, 121],
            "arithmetic control must be valid before lowering the cap")
    original = module.BIT_LIMIT
    module.BIT_LIMIT = 6
    try:
        reject(module.analyze, arithmetic)
    finally:
        module.BIT_LIMIT = original

    # Repeated containers are legal when they do not create cycles or explode in size.
    shared = copy.deepcopy(valid)
    empty = []
    for row in shared["model"]["classes"]:
        for color in ("odd", "even"):
            if not row[color]:
                row[color] = empty
    require(module.analyze(shared) == reference, "benign shared lists were rejected")
    reference["beliefs"][0]["posterior"][0]["probability"][0] = -99
    require(module.analyze(valid)["beliefs"][0]["posterior"][0]["probability"] == [1, 2],
            "a caller-mutated result contaminated later output")

runner = helpers.private_module("_qr05v_explicit_guard_runner", "study.py")
valid = helpers.micro_problem()
for bad in graph_inputs(valid):
    reject_before_dump(runner.require_wire, bad)
reject(lambda value: runner.require_same_wire({"zero": 0}, value, "typed wire"),
       {"zero": False})
require(before_serialization == 33, "pre-serialization rejection inventory")
expected = 2 * (len(invalid) + 2 + 11 + 4) + 11 + 1
require(rejections == expected, "explicit rejection inventory")
print(json.dumps({"rejections": rejections,
                  "invalid_fixture_cases": len(invalid),
                  "pre_serialization_rejections": before_serialization,
                  "optimized": bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05v.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=20, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    wanted = 2 * (len(invalid_problems()) + 2 + 11 + 4) + 11 + 1
    assert json.loads(result.stdout) == {
        "rejections": wanted,
        "invalid_fixture_cases": len(invalid_problems()),
        "pre_serialization_rejections": 33,
        "optimized": optimized,
    }
