"""Independent U raw-path filtering and partial-observation tests.

Only pinned T JSON supplies the declared raw observation model; no previous
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
from itertools import combinations, product
from math import comb
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
T_SHA = "f7bf6db5dd822c27a3087c6ad48af3ae76fdce653536cff8d381bfae905a5fe8"


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


@pytest.fixture(scope="session")
def pinned_t():
    path = HERE.parent / "qr-05t-local-refinement-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 6805377 and hashlib.sha256(raw).hexdigest() == T_SHA
    envelope = json.loads(raw)
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


@pytest.fixture(scope="session")
def supplied(pinned_t):
    a = pinned_t["analysis"]
    raw = copy.deepcopy(pinned_t["problem"]["model"])
    classes = [
        {
            key: copy.deepcopy(row[key])
            for key in ("class_id", "frame_id", "parent_color_sizes", "odd", "even")
        }
        for row in a["terminal"]["local_rows"]
    ]
    labels = []
    for row in a["terminal"]["local_rows"]:
        sid = row["representative_state"]
        feature = a["features"][sid]
        observation = [raw["states"][sid]["frame_id"], *feature["chain_counts"]]
        labels.append(
            {
                "class_id": row["class_id"],
                "observation": observation,
                "question": observation + [feature["motif_count"], feature["path_count"]],
            }
        )
    vector = a["local_refinement"]["state_classes"]
    schedules = [
        ([[1, 2], [1, 2]], [[2, 3], [1, 3]], [[1, 2], [1, 2]]),
        ([[2, 3], [1, 3]], [[1, 3], [2, 3]], [[2, 3], [2, 3]]),
    ]
    cases = []
    for name, raw_prior in [
        ("left", {612: F(1)}),
        ("right", {625: F(1)}),
        ("mixture", {612: F(1, 2), 625: F(1, 2)}),
    ]:
        masses = {}
        for sid, probability in raw_prior.items():
            accumulate(masses, vector[sid], probability)
        for schedule, rates in zip(("balanced", "biased"), schedules, strict=True):
            cases.append(
                {
                    "case_id": name + "_" + schedule,
                    "prior": belief(masses),
                    "rates": copy.deepcopy(list(rates)),
                    "raw_prior": raw_prior.copy(),
                }
            )
    return raw, {"classes": classes, "labels": labels}, cases


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05u_test_direct", "filtering.py"),
        private_module("_qr05u_test_reference", "reference_qr05u.py"),
    )


def problem_for(model, case):
    return {
        "schema_version": "det8-qr05u-problem-v1",
        "family": "qr05u_partial_observation",
        "model": model,
        "prior": case["prior"],
        "rates": case["rates"],
    }


@pytest.fixture(scope="session")
def analyses(executors, supplied):
    _, model, cases = supplied
    result = []
    for case in cases:
        problem = problem_for(model, case)
        before = wire(problem)
        values = tuple(module.analyze(problem) for module in executors)
        assert wire(problem) == before
        result.append(values)
    return result


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05u_test_runner", "study.py")
    return runner, runner.run_suite()


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


@pytest.fixture(scope="session")
def oracle(supplied):
    return RawOracle(supplied[0])


def normalized(values):
    mass = sum(values.values())
    assert mass > 0
    return {key: value / mass for key, value in values.items() if value}


def raw_analysis(oracle, case, raw_prior=None):
    prior = case["raw_prior"] if raw_prior is None else raw_prior
    rates = tuple(tuple(fraction(rate) for rate in stage) for stage in case["rates"])
    first_mass, history_mass, latest_mass = {}, {}, {}
    after1 = oracle.advance(prior, rates[0])
    for sid, mass in after1.items():
        accumulate(first_mass.setdefault(oracle.observations[sid], {}), sid, mass)
    for y1, masses in first_mass.items():
        for sid, mass in oracle.advance(masses, rates[1]).items():
            y2 = oracle.observations[sid]
            accumulate(history_mass.setdefault((y1, y2), {}), sid, mass)
            accumulate(latest_mass.setdefault(y2, {}), sid, mass)
    first, histories, latest = [], [], []
    for observation, masses in sorted(first_mass.items()):
        first.append(
            {
                "observation": list(observation),
                "likelihood": fw(sum(masses.values())),
                "posterior": belief(oracle.coarse(normalized(masses))),
            }
        )
    predictions, latest_predictions = {}, {}
    for history, masses in sorted(history_mass.items()):
        probability = sum(masses.values())
        posterior_raw = normalized(masses)
        prediction = oracle.predict(posterior_raw, rates[2])
        predictions[history] = prediction
        histories.append(
            {
                "observations": [list(y) for y in history],
                "likelihood": fw(probability),
                "conditional_likelihood": fw(probability / sum(first_mass[history[0]].values())),
                "posterior": belief(oracle.coarse(posterior_raw)),
                "prediction": question_law(prediction),
            }
        )
    for observation, masses in sorted(latest_mass.items()):
        prediction = oracle.predict(normalized(masses), rates[2])
        latest_predictions[observation] = prediction
        latest.append(
            {
                "observation": list(observation),
                "likelihood": fw(sum(masses.values())),
                "posterior": belief(oracle.coarse(normalized(masses))),
                "prediction": question_law(prediction),
            }
        )
    after2 = oracle.advance(after1, rates[1])
    after3 = oracle.advance(after2, rates[2])
    products = (rates[0][0] * rates[1][0] * rates[2][0], rates[0][1] * rates[1][1] * rates[2][1])
    assert after3 == oracle.advance(prior, products)
    assert (
        sum(fraction(row["likelihood"]) for row in first)
        == sum(fraction(row["likelihood"]) for row in histories)
        == 1
    )
    for y1, masses in first_mass.items():
        total, posterior_marginal, prediction_marginal = F(0), {}, {}
        for history, joint in history_mass.items():
            if history[0] != y1:
                continue
            conditional = sum(joint.values()) / sum(masses.values())
            total += conditional
            for cid, p in oracle.coarse(normalized(joint)).items():
                accumulate(posterior_marginal, cid, conditional * p)
            for question, p in predictions[history].items():
                accumulate(prediction_marginal, question, conditional * p)
        assert total == 1
        second = oracle.advance(normalized(masses), rates[1])
        assert posterior_marginal == oracle.coarse(second)
        assert prediction_marginal == oracle.predict(second, rates[2])
    for y2, masses in latest_mass.items():
        posterior_marginal, prediction_marginal = {}, {}
        for history, joint in history_mass.items():
            if history[1] != y2:
                continue
            probability = sum(joint.values()) / sum(masses.values())
            for cid, p in oracle.coarse(normalized(joint)).items():
                accumulate(posterior_marginal, cid, probability * p)
            for question, p in predictions[history].items():
                accumulate(prediction_marginal, question, probability * p)
        assert posterior_marginal == oracle.coarse(normalized(masses))
        assert prediction_marginal == latest_predictions[y2]
    for history, masses in history_mass.items():
        posterior = oracle.coarse(normalized(masses))
        assert sum(posterior.values()) == 1
        assert all(tuple(oracle.labels[cid]["observation"]) == history[1] for cid in posterior)
        assert sum(predictions[history].values()) == 1
    history_witness = forgetting_witness = map_witness = None
    pair_comparisons = pair_differences = forgetting_differences = map_differences = 0
    for left, right in combinations(sorted(predictions), 2):
        if left[1] != right[1]:
            continue
        pair_comparisons += 1
        difference = first_difference(predictions[left], predictions[right])
        pair_differences += difference is not None
        if difference is not None and history_witness is None:
            question, a, b = difference
            history_witness = {
                "left": [list(y) for y in left],
                "right": [list(y) for y in right],
                "question": list(question),
                "left_probability": fw(a),
                "right_probability": fw(b),
            }
    for history in sorted(predictions):
        difference = first_difference(predictions[history], latest_predictions[history[1]])
        forgetting_differences += difference is not None
        if difference is not None and forgetting_witness is None:
            question, a, b = difference
            forgetting_witness = {
                "observations": [list(y) for y in history],
                "question": list(question),
                "history_probability": fw(a),
                "latest_only_probability": fw(b),
            }
        posterior = oracle.coarse(normalized(history_mass[history]))
        winner = min(posterior, key=lambda cid: (-posterior[cid], cid))
        representative = oracle.partition["classes"][winner]["members"][0]
        map_law = oracle.predict({representative: F(1)}, rates[2])
        difference = first_difference(predictions[history], map_law)
        map_differences += difference is not None
        if difference is not None and map_witness is None:
            question, a, b = difference
            map_witness = {
                "observations": [list(y) for y in history],
                "map_class_id": winner,
                "question": list(question),
                "mixture_probability": fw(a),
                "map_probability": fw(b),
            }
    kernels = [oracle.class_kernel(*rate) for rate in rates]
    result = {
        "model_sha256": digest(oracle.model),
        "reconstruction": oracle.reconstruction,
        "prior": belief(oracle.coarse(prior)),
        "rates": case["rates"],
        "kernel_sha256": [digest(rows) for rows in kernels],
        "first": first,
        "histories": histories,
        "latest_only": latest,
        "unconditional": {
            "after_first": belief(oracle.coarse(after1)),
            "after_second": belief(oracle.coarse(after2)),
            "after_third": belief(oracle.coarse(after3)),
            "next_prediction": question_law(oracle.predict(after2, rates[2])),
        },
        "controls": {
            "history_witness": history_witness,
            "forgetting_witness": forgetting_witness,
            "map_witness": map_witness,
        },
        "checks": {
            "first_normalization": True,
            "joint_normalization": True,
            "posterior_normalization": True,
            "posterior_support": True,
            "tower_first": True,
            "tower_latest": True,
            "three_step_composition": True,
            "max_abs_residual": [0, 1],
        },
        "counts": {
            "classes": len(oracle.classes),
            "profile_atoms": oracle.reconstruction["profile_atoms"],
            "kernel_atoms": [sum(len(row["transitions"]) for row in rows) for rows in kernels],
            "first_histories": len(first),
            "histories": len(histories),
            "first_posterior_atoms": sum(len(row["posterior"]) for row in first),
            "history_posterior_atoms": sum(len(row["posterior"]) for row in histories),
            "history_prediction_atoms": sum(len(row["prediction"]) for row in histories),
            "latest_observations": len(latest),
            "latest_posterior_atoms": sum(len(row["posterior"]) for row in latest),
            "latest_prediction_atoms": sum(len(row["prediction"]) for row in latest),
            "history_pairs_compared": pair_comparisons,
            "history_pairs_different": pair_differences,
            "forgetting_comparisons": len(histories),
            "forgetting_differences": forgetting_differences,
            "map_comparisons": len(histories),
            "map_differences": map_differences,
        },
    }
    return result, history_mass


@pytest.fixture(scope="session")
def expected(oracle, supplied):
    return [raw_analysis(oracle, case) for case in supplied[2]]


def test_raw_bridge_reconstructs_features_actual_fibers_local_rows_and_declared_labels(
    oracle, supplied, pinned_t
):
    raw, model, cases = supplied
    prior = pinned_t["analysis"]
    assert wire(oracle.features) == wire(prior["features"])
    assert wire(oracle.partition) == wire(prior["partitions"]["H"])
    assert oracle.vector == prior["local_refinement"]["state_classes"]
    assert wire(oracle.model) == wire(model)
    assert digest(oracle.fine) == prior["fine_kernel"]["sha256"]
    assert len(raw["states"]) == 4447 and len(model["classes"]) == 416
    assert [case["case_id"] for case in cases] == [
        "left_balanced",
        "left_biased",
        "right_balanced",
        "right_biased",
        "mixture_balanced",
        "mixture_biased",
    ]
    for sid, path_count in ((612, 0), (625, 1)):
        assert oracle.features[sid]["color_sizes"] == [3, 3]
        assert oracle.features[sid]["chain_counts"] == [1, 6, 4, 0]
        assert (
            oracle.features[sid]["motif_count"] == 0
            and oracle.features[sid]["path_count"] == path_count
        )
    assert oracle.vector[612] != oracle.vector[625]


@pytest.mark.parametrize("case_index", range(6))
def test_all_native_outputs_equal_unnormalized_raw_nested_path_oracle(
    analyses, expected, case_index
):
    primary, reference = analyses[case_index]
    wanted, _ = expected[case_index]
    assert wire(primary) == wire(reference) == wire(wanted)
    assert wire(json.loads(wire(primary))) == wire(primary)
    assert len(wire(primary)) < 64 * 1024 * 1024


def test_all_raw_members_match_class_kernels_at_schedule_rates_and_composed_products(
    oracle, supplied
):
    rates = set()
    for case in supplied[2]:
        stages = [tuple(fraction(rate) for rate in stage) for stage in case["rates"]]
        rates.update(stages)
        rates.add(
            (stages[0][0] * stages[1][0] * stages[2][0], stages[0][1] * stages[1][1] * stages[2][1])
        )
    for x, y in rates:
        kernels = oracle.class_kernel(x, y)
        for sid, cid in enumerate(oracle.vector):
            actual = oracle.coarse(dict(oracle.transition(sid, x, y)))
            wanted = {
                atom["target_class"]: fraction(atom["probability"])
                for atom in kernels[cid]["transitions"]
            }
            assert actual == wanted


@pytest.mark.parametrize("case_index", range(6))
def test_prior_lifts_preserve_evidence_current_class_beliefs_and_questions_not_raw_identity(
    oracle, supplied, expected, case_index
):
    case = supplied[2][case_index]
    wanted, raw_posteriors = expected[case_index]
    for endpoint in (0, -1):
        lift = {}
        for atom in case["prior"]:
            sid = oracle.partition["classes"][atom["class_id"]]["members"][endpoint]
            accumulate(lift, sid, fraction(atom["probability"]))
        actual, lifted_raw = raw_analysis(oracle, case, lift)
        assert wire(actual) == wire(wanted)
        assert set(lifted_raw) == set(raw_posteriors)
        for history in lifted_raw:
            assert oracle.coarse(normalized(lifted_raw[history])) == oracle.coarse(
                normalized(raw_posteriors[history])
            )


def test_bayes_evidence_current_state_support_and_total_probability_towers(expected):
    for a, _ in expected:
        first = {tuple(row["observation"]): row for row in a["first"]}
        latest = {tuple(row["observation"]): row for row in a["latest_only"]}
        unconditional = {
            name: {
                atom["class_id"]: fraction(atom["probability"]) for atom in a["unconditional"][name]
            }
            for name in ("after_first", "after_second", "after_third")
        }
        for rows, marginal in (
            (a["first"], "after_first"),
            (a["histories"], "after_second"),
            (a["latest_only"], "after_second"),
        ):
            total = {}
            for row in rows:
                likelihood = fraction(row["likelihood"])
                assert (
                    likelihood > 0
                    and sum(fraction(atom["probability"]) for atom in row["posterior"]) == 1
                )
                for atom in row["posterior"]:
                    accumulate(total, atom["class_id"], likelihood * fraction(atom["probability"]))
            assert total == unconditional[marginal]
        for row in a["histories"]:
            y1, y2 = map(tuple, row["observations"])
            assert fraction(row["likelihood"]) == fraction(first[y1]["likelihood"]) * fraction(
                row["conditional_likelihood"]
            )
            assert fraction(row["likelihood"]) <= fraction(latest[y2]["likelihood"])
        weighted_prediction = {}
        for row in a["histories"]:
            for atom in row["prediction"]:
                accumulate(
                    weighted_prediction,
                    tuple(atom["value"]),
                    fraction(row["likelihood"]) * fraction(atom["probability"]),
                )
        assert question_law(weighted_prediction) == a["unconditional"]["next_prediction"]


def test_witnesses_require_changed_whole_future_laws_and_canonical_actual_comparisons(
    expected, oracle
):
    for a, _ in expected:
        histories = {tuple(map(tuple, row["observations"])): row for row in a["histories"]}
        counts = a["counts"]
        eligible = sum(1 for left, right in combinations(histories, 2) if left[1] == right[1])
        assert counts["history_pairs_compared"] == eligible
        assert counts["map_comparisons"] == counts["forgetting_comparisons"] == len(histories)
        for name, witness in a["controls"].items():
            difference_key = {
                "history_witness": "history_pairs_different",
                "forgetting_witness": "forgetting_differences",
                "map_witness": "map_differences",
            }[name]
            assert (witness is None) == (counts[difference_key] == 0)
            if witness is None:
                continue
            if name == "history_witness":
                assert (
                    witness["left"] < witness["right"] and witness["left"][1] == witness["right"][1]
                )
                assert fraction(witness["left_probability"]) != fraction(
                    witness["right_probability"]
                )
            else:
                row = histories[tuple(map(tuple, witness["observations"]))]
                if name == "map_witness":
                    winner = min(
                        row["posterior"],
                        key=lambda atom: (-fraction(atom["probability"]), atom["class_id"]),
                    )["class_id"]
                    assert witness["map_class_id"] == winner
                    assert fraction(witness["mixture_probability"]) != fraction(
                        witness["map_probability"]
                    )
                else:
                    assert fraction(witness["history_probability"]) != fraction(
                        witness["latest_only_probability"]
                    )
        for row in a["histories"]:
            assert all(
                oracle.labels[atom["class_id"]]["observation"] == row["observations"][1]
                for atom in row["posterior"]
            )


def micro_model():
    ranks, frames = [[0, 0], [1, 0], [0, 0], [2, 0], [0, 1]], [0, 0, 1, 0, 0]
    odd = [[], [(0, 1)], [], [(1, 2)], []]
    even = [[], [], [], [], [(0, 1)]]
    classes = [
        {
            "class_id": cid,
            "frame_id": frames[cid],
            "parent_color_sizes": rank,
            "odd": [{"target_class": target, "multiplicity": mult} for target, mult in odd[cid]],
            "even": [{"target_class": target, "multiplicity": mult} for target, mult in even[cid]],
        }
        for cid, rank in enumerate(ranks)
    ]
    observations = [
        [0, 1, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 1, 2, 1, 0],
        [0, 1, 1, 0, 0],
    ]
    return {
        "classes": classes,
        "labels": [
            {"class_id": cid, "observation": obs, "question": obs + [0, 0]}
            for cid, obs in enumerate(observations)
        ],
    }


def micro_problem(kind="history"):
    model = micro_model()
    if kind == "history":
        prior, rates = (
            [{"class_id": 3, "probability": [1, 2]}, {"class_id": 4, "probability": [1, 2]}],
            [[[1, 2], [1, 2]], [[1, 2], [1, 2]], [[1, 3], [2, 3]]],
        )
    elif kind in ("tie", "unique"):
        prior = [
            {"class_id": 1, "probability": [1, 2] if kind == "tie" else [2, 3]},
            {"class_id": 4, "probability": [1, 2] if kind == "tie" else [1, 3]},
        ]
        rates = [[[1, 1], [1, 1]], [[1, 1], [1, 1]], [[1, 3], [2, 3]]]
    else:
        prior = [{"class_id": 1, "probability": [1, 2]}, {"class_id": 2, "probability": [1, 2]}]
        rates = (
            [[[1, 1], [1, 1]]] * 3
            if kind == "identity"
            else [[[0, 1], [0, 1]], [[2, 3], [1, 3]], [[1, 1], [1, 1]]]
        )
    return {
        "schema_version": "det8-qr05u-problem-v1",
        "family": "qr05u_partial_observation",
        "model": model,
        "prior": prior,
        "rates": rates,
    }


@pytest.fixture(scope="session")
def micro_analyses(executors):
    result = {}
    for kind in ("history", "tie", "unique", "identity", "delete"):
        values = tuple(module.analyze(micro_problem(kind)) for module in executors)
        assert wire(values[0]) == wire(values[1])
        result[kind] = values[0]
    return result


def atom_probability(law, value):
    return next((fraction(atom["probability"]) for atom in law if atom["value"] == value), F(0))


def test_hand_calculated_history_likelihood_current_belief_and_forgetting(micro_analyses):
    a = micro_analyses["history"]
    one, two = [0, 1, 1, 0, 0], [0, 1, 2, 1, 0]
    histories = {tuple(map(tuple, row["observations"])): row for row in a["histories"]}
    same, informative = histories[(tuple(one), tuple(one))], histories[(tuple(two), tuple(one))]
    assert same["likelihood"] == [1, 4] and same["conditional_likelihood"] == [1, 2]
    assert same["posterior"] == [
        {"class_id": 1, "probability": [1, 2]},
        {"class_id": 4, "probability": [1, 2]},
    ]
    assert informative["likelihood"] == [1, 16] and informative["conditional_likelihood"] == [1, 2]
    assert informative["posterior"] == [{"class_id": 1, "probability": [1, 1]}]
    assert atom_probability(same["prediction"], one + [0, 0]) == F(1, 2)
    assert atom_probability(informative["prediction"], one + [0, 0]) == F(1, 3)
    latest = next(row for row in a["latest_only"] if row["observation"] == one)
    assert latest["likelihood"] == [5, 16]
    assert latest["posterior"] == [
        {"class_id": 1, "probability": [3, 5]},
        {"class_id": 4, "probability": [2, 5]},
    ]
    assert atom_probability(latest["prediction"], one + [0, 0]) == F(7, 15)
    assert {atom["class_id"] for atom in informative["posterior"]} != {
        atom["class_id"] for atom in a["prior"]
    }


@pytest.mark.parametrize("kind,retention", [("tie", F(1, 2)), ("unique", F(4, 9))])
def test_map_plugin_is_not_posterior_mixture_and_ties_have_declared_resolution(
    micro_analyses, kind, retention
):
    a = micro_analyses[kind]
    assert len(a["histories"]) == 1
    row = a["histories"][0]
    assert row["posterior"] == a["prior"]
    assert atom_probability(row["prediction"], [0, 1, 1, 0, 0, 0, 0]) == retention
    witness = a["controls"]["map_witness"]
    assert witness["map_class_id"] == 1
    assert witness["question"] == [0, 1, 0, 0, 0, 0, 0]
    assert fraction(witness["mixture_probability"]) == 1 - retention
    assert witness["map_probability"] == [2, 3]


@pytest.mark.parametrize("kind", ["identity", "delete"])
def test_boundary_rates_identity_idempotence_and_absorbing_fixed_frames(micro_analyses, kind):
    a = micro_analyses[kind]
    expected = [
        {"class_id": 1 if kind == "identity" else 0, "probability": [1, 2]},
        {"class_id": 2, "probability": [1, 2]},
    ]
    assert (
        a["unconditional"]["after_first"]
        == a["unconditional"]["after_second"]
        == a["unconditional"]["after_third"]
        == expected
    )
    assert len(a["histories"]) == 2
    for row in a["histories"]:
        assert row["observations"][0] == row["observations"][1]
        assert row["likelihood"] == [1, 2] and row["conditional_likelihood"] == [1, 1]
        assert len(row["posterior"]) == len(row["prediction"]) == 1
        assert row["posterior"][0]["probability"] == row["prediction"][0]["probability"] == [1, 1]
    assert all(witness is None for witness in a["controls"].values())


def possible(row):
    return {
        "status": "possible",
        "failed_stage": None,
        "likelihood": row["likelihood"],
        "posterior": row["posterior"],
        "prediction": row["prediction"],
    }


def impossible(stage):
    return {
        "status": "impossible",
        "failed_stage": stage,
        "likelihood": [0, 1],
        "posterior": None,
        "prediction": None,
    }


@pytest.mark.parametrize("case_index", range(6))
def test_public_conditioning_matches_joint_current_posterior_and_full_future_law(
    executors, supplied, expected, case_index
):
    problem = problem_for(supplied[1], supplied[2][case_index])
    row = expected[case_index][0]["histories"][0]
    for module in executors:
        assert wire(module.filter_history(problem, row["observations"])) == wire(possible(row))


def test_known_impossibility_reports_its_stage_without_reset_or_pseudoposterior(
    executors, micro_analyses
):
    p = micro_problem()
    good = micro_analyses["history"]["histories"][0]
    frame1 = [1, 1, 1, 0, 0]
    for module in executors:
        assert module.filter_history(p, [frame1, frame1]) == impossible(1)
        assert module.filter_history(p, [good["observations"][0], frame1]) == impossible(2)
        assert wire(module.filter_history(p, good["observations"])) == wire(possible(good))
        identity = micro_problem("identity")
        assert module.filter_history(identity, [[0, 1, 1, 0, 0], [0, 1, 0, 0, 0]]) == impossible(2)


class IntSubclass(int):
    pass


class StrSubclass(str):
    pass


class ListSubclass(list):
    pass


class DictSubclass(dict):
    pass


INPUT_MUTATIONS = [
    (("schema_version",), "det8-qr05t-problem-v1"),
    (("family",), "bad"),
    (("extra",), 0),
    (("model", "raw_orders"), []),
    (("prior",), []),
    (("prior", 0, "class_id"), False),
    (("prior", 0, "class_id"), 5),
    (("prior", 0, "probability"), [0, 1]),
    (("prior", 0, "probability"), [1, 3]),
    (("prior", 0, "probability"), [2, 4]),
    (("prior", 0, "probability"), [1, 0]),
    (("prior", 0, "probability"), [-1, 2]),
    (("prior", 0, "probability"), [1, -2]),
    (("prior", 0, "probability"), [True, 2]),
    (("prior", 0, "probability"), [1, 1 << 64]),
    (("prior", 0, "probability"), [IntSubclass(1), 2]),
    (("prior", 0, "probability"), "1/2"),
    (("prior", 0, "probability"), [1.0, 2]),
    (("prior", 0, "probability"), (1, 2)),
    (("rates",), []),
    (("rates", 0), [[1, 2]]),
    (("rates", 0, 0), [2, 1]),
    (("rates", 0, 0), [0, 2]),
    (("rates", 0, 0), [2, 2]),
    (("rates", 0, 0), [1, 1 << 64]),
    (("model", "classes", 0, "class_id"), False),
    (("model", "classes", 0, "frame_id"), False),
    (("model", "classes", 1, "parent_color_sizes", 1), False),
    (("model", "classes", 1, "odd", 0, "target_class"), False),
    (("model", "classes", 1, "odd", 0, "multiplicity"), True),
    (("model", "classes", 1, "odd", 0, "multiplicity"), 2),
    (("model", "classes", 3, "odd"), []),
    (("model", "labels", 0, "class_id"), False),
    (("model", "labels", 0, "observation", 0), False),
    (("model", "labels", 0, "observation", 1), True),
    (("model", "labels", 1, "observation", 3), 1),
    (("model", "labels", 0, "question", 0), 1),
    (("model", "labels", 0, "question", 5), 1),
    (("model", "labels", 0, "question", 6), 1),
    (("model", "labels", 3, "observation", 2), 3),
    (("model", "labels", 1, "observation", 4), 1),
]


@pytest.mark.parametrize("path,value", INPUT_MUTATIONS)
def test_both_public_entries_validate_native_rationals_model_labels_prior_and_rates(
    executors, path, value
):
    malformed = replaced(micro_problem(), path, value)
    records = [[0, 1, 0, 0, 0]] * 2
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(malformed)
        with pytest.raises(ValueError):
            module.filter_history(malformed, records)


@pytest.mark.parametrize(
    "kind",
    [
        "duplicate_prior",
        "unsorted_prior",
        "too_many_prior",
        "missing_label",
        "duplicate_local",
        "wrong_frame",
        "class_bound",
    ],
)
def test_model_and_prior_canonical_support_and_resource_constraints(executors, kind):
    p = micro_problem()
    if kind == "duplicate_prior":
        p["prior"] = [{"class_id": 3, "probability": [1, 2]}] * 2
    elif kind == "unsorted_prior":
        p["prior"].reverse()
    elif kind == "too_many_prior":
        p["model"] = {
            "classes": [
                {**copy.deepcopy(p["model"]["classes"][0]), "class_id": cid} for cid in range(17)
            ],
            "labels": [
                {**copy.deepcopy(p["model"]["labels"][0]), "class_id": cid} for cid in range(17)
            ],
        }
        p["prior"] = [{"class_id": i, "probability": [1, 16]} for i in range(16)]
        for module in executors:
            module.analyze(p)
        p["prior"] = [{"class_id": i, "probability": [1, 17]} for i in range(17)]
    elif kind == "missing_label":
        p["model"]["labels"].pop()
    elif kind == "duplicate_local":
        p["model"]["classes"][3]["odd"] = [{"target_class": 1, "multiplicity": 1}] * 2
    elif kind == "wrong_frame":
        p["model"]["classes"][0]["frame_id"] = 1
    else:
        p["model"]["classes"] = [p["model"]["classes"][0]] * 513
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(p)


@pytest.mark.parametrize(
    "records",
    [
        [],
        [[0, 1, 0, 0, 0]],
        [[0, 1, 0, 0, 0]] * 3,
        ([0, 1, 0, 0, 0], [0, 1, 0, 0, 0]),
        [[False, 1, 0, 0, 0], [0, 1, 0, 0, 0]],
        [[0, True, 0, 0, 0], [0, 1, 0, 0, 0]],
        [[0, 1, 3, 0, 0], [0, 1, 0, 0, 0]],
        [[1, 1, 1, 0, 0], [0, 1, 3, 0, 0]],
        [[0, 1, 0, 0], [0, 1, 0, 0, 0]],
        [[0, 1, 0, 0, 0], "unknown"],
    ],
)
def test_unknown_or_malformed_records_are_rejected_even_after_an_impossible_first_record(
    executors, records
):
    for module in executors:
        with pytest.raises(ValueError):
            module.filter_history(micro_problem(), records)


def test_record_labels_are_declared_maps_not_determined_or_authenticated_by_local_rows(executors):
    original = micro_problem()
    alternative = copy.deepcopy(original)
    alternative["model"]["labels"][3]["observation"][3] = 0
    alternative["model"]["labels"][3]["question"][3] = 0
    for module in executors:
        before, after = module.analyze(original), module.analyze(alternative)
        assert before["reconstruction"] == after["reconstruction"]
        assert before["kernel_sha256"] == after["kernel_sha256"]
        assert before["model_sha256"] != after["model_sha256"]
        assert before["first"] != after["first"]


def mutable_ids(value):
    seen, stack = set(), [value]
    while stack:
        item = stack.pop()
        if type(item) not in (dict, list) or id(item) in seen:
            continue
        seen.add(id(item))
        stack.extend(item.values() if type(item) is dict else item)
    return seen


@pytest.mark.parametrize("method", ["analyze", "filter_history"])
def test_all_returned_containers_are_detached_from_inputs_records_and_other_calls(
    executors, method
):
    for module in executors:
        p = micro_problem()
        records = [[0, 1, 1, 0, 0]] * 2
        call = (
            (lambda module=module, p=p: module.analyze(p))
            if method == "analyze"
            else (lambda module=module, p=p, records=records: module.filter_history(p, records))
        )
        a, b = call(), call()
        before, wanted = wire([p, records]), wire(b)
        assert mutable_ids(a).isdisjoint(mutable_ids([p, records]))
        assert mutable_ids(a).isdisjoint(mutable_ids(b))
        assert wire(a) == wanted
        if method == "analyze":
            a["histories"][0]["posterior"][0]["probability"][0] = -99
        else:
            a["posterior"][0]["probability"][0] = -99
        assert wire([p, records]) == before and wire(b) == wanted and wire(call()) == wanted
        p["prior"][0]["probability"][0] = -88
        assert wire(b) == wanted
        with pytest.raises(ValueError):
            call()


@pytest.mark.parametrize(
    "constant",
    ["WORKING_CAP", "FIRST_CAP", "HISTORY_CAP", "POSTERIOR_CAP", "PREDICTION_CAP", "BIT_LIMIT"],
)
def test_aggregate_and_arithmetic_caps_fail_instead_of_truncating_or_returning_unbounded_fractions(
    executors, monkeypatch, constant
):
    p = micro_problem()
    if constant == "BIT_LIMIT":
        p["model"] = {key: value[:2] for key, value in p["model"].items()}
        p["prior"] = [{"class_id": 1, "probability": [1, 1]}]
        p["rates"] = [[[1, 11], [1, 1]]] * 3
    for module in executors:
        wanted = wire(module.analyze(p))
        with monkeypatch.context() as limited:
            limited.setattr(
                module,
                constant,
                32 if constant == "WORKING_CAP" else 8 if constant == "BIT_LIMIT" else 1,
            )
            with pytest.raises(ValueError):
                module.analyze(p)
        assert wire(module.analyze(p)) == wanted


def case_wire(case):
    return {
        **case,
        "raw_prior": [
            {"state_id": sid, "probability": fw(p)} for sid, p in sorted(case["raw_prior"].items())
        ],
    }


def test_whole_aggregate_native_wire_dependencies_lifts_rates_and_unsupported_predicate(
    aggregate, supplied, oracle, expected
):
    runner, suite = aggregate
    raw, model, cases = supplied
    assert set(suite) == {
        "raw_model",
        "model",
        "cases",
        "independent_route_equal",
        "raw_bridge",
        "rate_audit",
        "prior_lifts",
        "unsupported_observation",
        "public_controls",
        "totals",
    }
    assert wire(suite) == runner.canonical(suite) == wire(json.loads(wire(suite)))
    assert wire(suite["raw_model"]) == wire(raw) and wire(suite["model"]) == wire(model)
    assert suite["independent_route_equal"] is True
    for result, case, (a, _) in zip(suite["cases"], cases, expected, strict=True):
        assert wire(result) == wire({**case_wire(case), "analysis": a})
    bridge = suite["raw_bridge"]
    assert bridge["prior_artifact"] == "qr-05t-local-refinement-2026-09-06/results.json"
    assert (
        bridge["states"] == 4447
        and bridge["classes"] == 416
        and bridge["member_comparisons"] == 4447 - 416
    )
    assert bridge["features_sha256"] == digest(oracle.features) and bridge["H_sha256"] == digest(
        oracle.partition
    )
    assert bridge["fine_sha256"] == digest(oracle.fine) and bridge["fine_atoms"] == 168388
    assert bridge["profiles_sha256"] == oracle.reconstruction["profiles_sha256"]
    assert (
        bridge["raw_local_labels_declared_input_dependencies"] is True
        and bridge["all_members_labels_local_and_profiles_equal"] is True
    )
    assert (
        bridge["T_refinement_or_minimality_replayed"]
        is bridge["source_aliases_regenerated"]
        is bridge["P_consumer_R_helper_Q_certificate_replayed"]
        is False
    )
    reports = suite["rate_audit"]["rates"]
    assert len(reports) == 6
    for report in reports:
        rate = tuple(fraction(pair) for pair in report["rates"])
        kernel_rows = oracle.class_kernel(*rate)
        assert report["kernel_sha256"] == digest(kernel_rows)
        assert report["raw_rows_checked"] == 4447
        assert report["raw_positive_atoms"] == sum(
            len(oracle.transition(sid, *rate)) for sid in range(4447)
        )
        assert report["class_positive_atoms"] == sum(len(row["transitions"]) for row in kernel_rows)
        assert report["max_abs_residual"] == [0, 1]
    assert suite["rate_audit"]["raw_row_comparisons"] == 6 * 4447
    assert suite["rate_audit"]["raw_positive_atoms"] == sum(
        row["raw_positive_atoms"] for row in reports
    )
    assert suite["rate_audit"]["all_raw_members_checked"] is True
    for row, case, (a, _) in zip(suite["prior_lifts"], cases, expected, strict=True):
        assert row["case_id"] == case["case_id"]
        for name, endpoint in (("first", 0), ("last", -1)):
            lifted = {}
            for atom in case["prior"]:
                accumulate(
                    lifted,
                    oracle.partition["classes"][atom["class_id"]]["members"][endpoint],
                    fraction(atom["probability"]),
                )
            assert row[name] == {
                "raw_prior": [
                    {"state_id": sid, "probability": fw(p)} for sid, p in sorted(lifted.items())
                ],
                "analysis_sha256": digest(a),
                "H_filtering_equal": True,
                "raw_posterior_equality_claimed": False,
            }
    witness = None
    for group in oracle.partition["classes"]:
        for left, right in combinations(group["members"], 2):
            a, b = int(1 in raw["states"][left]["kept"]), int(1 in raw["states"][right]["kept"])
            if a != b:
                witness = {
                    "class_id": group["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "left_value": a,
                    "right_value": b,
                }
                break
        if witness is not None:
            break
    assert suite["unsupported_observation"] == {
        "predicate": "original_vertex_1_present",
        "H_measurable": witness is None,
        "witness": witness,
        "public_custom_predicate_supported": False,
    }
    assert suite["public_controls"] == {
        "conditioning_calls": 18,
        "impossible_conditioning_calls": 4,
        "invalid_analyze_calls_rejected": 14,
        "raw_orders_or_artifacts_given_to_core": False,
    }
    all_a = [a for a, _ in expected]
    assert suite["totals"] == {
        "raw_states": 4447,
        "classes": 416,
        "cases": 6,
        "analyze_calls": 12,
        "conditioning_calls": 18,
        "prior_lift_comparisons": 12,
        "histories": sum(a["counts"]["histories"] for a in all_a),
        "history_posterior_atoms": sum(a["counts"]["history_posterior_atoms"] for a in all_a),
        "history_prediction_atoms": sum(a["counts"]["history_prediction_atoms"] for a in all_a),
        **{
            name + "_witness_cases": sum(
                a["controls"][name + "_witness"] is not None for a in all_a
            )
            for name in ("history", "forgetting", "map")
        },
        "raw_rate_rows_checked": 6 * 4447,
    }
    assert len(runner.SOURCES) == 6 and len(runner.PRIORS) == 25
    assert runner.PRIORS["qr-05t-local-refinement-2026-09-06/results.json"] == T_SHA


@pytest.mark.parametrize(
    "kind",
    [
        "joint",
        "conditional",
        "posterior_initial",
        "posterior_weight",
        "prediction",
        "omitted_history",
        "reordered_history",
        "first_weight",
        "latest_weight",
        "kernel",
        "checks",
        "comparison_count",
        "history_witness",
        "map_class",
        "fraction_bool",
    ],
)
def test_complete_raw_audit_rejects_bayes_state_time_witness_and_native_corruptions(
    aggregate, kind
):
    runner, suite = aggregate
    case = suite["cases"][0]
    a = case["analysis"]
    if kind == "joint":
        bad = replaced(a, ("histories", 0, "likelihood"), [1, 1])
    elif kind == "conditional":
        bad = replaced(a, ("histories", 0, "conditional_likelihood"), [0, 1])
    elif kind == "posterior_initial":
        bad = replaced(a, ("histories", 0, "posterior"), a["prior"])
    elif kind == "posterior_weight":
        bad = replaced(a, ("histories", 0, "posterior", 0, "probability"), [1, 2])
    elif kind == "prediction":
        bad = replaced(a, ("histories", 0, "prediction"), [])
    elif kind == "omitted_history":
        bad = replaced(a, ("histories",), a["histories"][1:])
    elif kind == "reordered_history":
        bad = replaced(a, ("histories",), list(reversed(a["histories"])))
    elif kind == "first_weight":
        bad = replaced(a, ("first", 0, "likelihood"), [0, 1])
    elif kind == "latest_weight":
        bad = replaced(a, ("latest_only", 0, "likelihood"), [0, 1])
    elif kind == "kernel":
        bad = replaced(a, ("kernel_sha256", 0), "0" * 64)
    elif kind == "checks":
        bad = replaced(a, ("checks", "three_step_composition"), 1)
    elif kind == "comparison_count":
        bad = replaced(a, ("counts", "history_pairs_compared"), 0)
    elif kind == "history_witness":
        bad = replaced(a, ("controls", "history_witness"), None)
    elif kind == "map_class":
        bad = replaced(a, ("controls", "map_witness", "map_class_id"), -1)
    else:
        bad = replaced(a, ("checks", "max_abs_residual", 0), False)
    assert wire(bad) != wire(a)
    declared = {key: value for key, value in case.items() if key != "analysis"}
    with pytest.raises(ValueError):
        runner.check_analysis(bad, suite["raw_model"], declared)


@pytest.mark.parametrize(
    "kind",
    [
        "raw_id_subclass",
        "raw_key_subclass",
        "prior_bool",
        "rate_subclass",
        "case_key_subclass",
        "semantic_prior",
    ],
)
def test_raw_audit_cache_revalidates_native_model_case_and_prior_content(aggregate, kind):
    runner, suite = aggregate
    case = {key: value for key, value in suite["cases"][0].items() if key != "analysis"}
    a, raw = suite["cases"][0]["analysis"], suite["raw_model"]
    wanted = runner.check_analysis(a, raw, case)
    if kind == "raw_id_subclass":
        raw = replaced(raw, ("states", 0, "state_id"), IntSubclass(0))
    elif kind == "raw_key_subclass":
        raw = raw.copy()
        raw[StrSubclass("states")] = raw.pop("states")
    elif kind == "prior_bool":
        case = replaced(case, ("raw_prior", 0, "probability", 0), True)
    elif kind == "rate_subclass":
        case = replaced(case, ("rates", 0, 0, 0), IntSubclass(1))
    elif kind == "case_key_subclass":
        case = case.copy()
        case[StrSubclass("rates")] = case.pop("rates")
    else:
        case = replaced(case, ("raw_prior", 0, "probability"), [1, 2])
    with pytest.raises(ValueError):
        runner.check_analysis(a, raw, case)
    assert wanted == {"analysis_sha256": digest(a), "complete_native_output_equal": True}


def algebraically_invalid_problem(kind):
    if kind == "fractional":
        ranks = [[3, 0], [2, 0], [2, 0], [1, 0], [1, 0], [0, 0]]
        odd = [[(1, 1), (2, 2)], [(3, 1), (4, 1)], [(4, 2)], [(5, 1)], [(5, 1)], []]
        even = [[] for _ in ranks]
    else:
        ranks = [[1, 1], [0, 1], [1, 0], [0, 0], [0, 0]]
        odd = [[(1, 1)], [], [(4, 1)], [], []]
        even = [[(2, 1)], [(3, 1)], [], [], []]
    classes = [
        {
            "class_id": cid,
            "frame_id": 0,
            "parent_color_sizes": rank,
            "odd": [{"target_class": target, "multiplicity": p} for target, p in odd[cid]],
            "even": [{"target_class": target, "multiplicity": p} for target, p in even[cid]],
        }
        for cid, rank in enumerate(ranks)
    ]
    labels = [
        {
            "class_id": cid,
            "observation": [0, 1, sum(rank), 0, 0],
            "question": [0, 1, sum(rank), 0, 0, 0, 0],
        }
        for cid, rank in enumerate(ranks)
    ]
    return {
        "schema_version": "det8-qr05u-problem-v1",
        "family": "qr05u_partial_observation",
        "model": {"classes": classes, "labels": labels},
        "prior": [{"class_id": 0, "probability": [1, 1]}],
        "rates": [[[1, 2], [1, 2]]] * 3,
    }


@pytest.mark.parametrize("kind", ["fractional", "mixed"])
def test_both_filtering_entries_retain_local_integrality_and_mixed_operator_validation(
    executors, kind
):
    p = algebraically_invalid_problem(kind)
    for row in p["model"]["classes"]:
        assert sum(atom["multiplicity"] for atom in row["odd"]) == row["parent_color_sizes"][0]
        assert sum(atom["multiplicity"] for atom in row["even"]) == row["parent_color_sizes"][1]
    records = [p["model"]["labels"][0]["observation"]] * 2
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(p)
        with pytest.raises(ValueError):
            module.filter_history(p, records)


def test_unsigned_64_bit_input_boundary_is_not_confused_with_output_fraction_limit(executors):
    p = micro_problem()
    p["model"] = {key: value[:2] for key, value in p["model"].items()}
    p["prior"] = [{"class_id": 1, "probability": [1, 1]}]
    denominator = (1 << 64) - 1
    p["rates"] = [[[1, denominator], [1, 1]], [[1, 1], [1, 1]], [[1, 1], [1, 1]]]
    wanted = [
        {"class_id": 0, "probability": [denominator - 1, denominator]},
        {"class_id": 1, "probability": [1, denominator]},
    ]
    for module in executors:
        result = module.analyze(p)
        assert (
            result["unconditional"]["after_first"]
            == result["unconditional"]["after_third"]
            == wanted
        )
        assert module.filter_history(p, [[0, 1, 1, 0, 0]] * 2)["likelihood"] == [1, denominator]


@pytest.mark.parametrize("optimized", [False, True])
def test_public_native_dag_record_and_arithmetic_guards_in_bounded_subprocess(tmp_path, optimized):
    payload = {
        "valid": micro_problem(),
        "fractional": algebraically_invalid_problem("fractional"),
        "mixed": algebraically_invalid_problem("mixed"),
    }
    program = r"""
import copy, importlib.util, json, resource, sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (12, 12))
base, payload = Path(sys.argv[1]), json.loads(sys.argv[2])
count = 0
def require(condition, message):
    if not condition: raise RuntimeError(message)
def reject(call, value):
    global count
    try: call(value)
    except ValueError: count += 1
    else: raise RuntimeError("unsafe or malformed input accepted")
def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, base / filename)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    spec.loader.exec_module(module); return module
def dag():
    value = []
    for _ in range(40): value = [value, value]
    return value
class I(int): pass
class S(str): pass
class L(list): pass
class D(dict): pass
records = [[0, 1, 1, 0, 0]] * 2
for index, filename in enumerate(("filtering.py", "reference_qr05u.py")):
    module = load("_qr05u_guard_" + str(index), filename)
    valid = copy.deepcopy(payload["valid"])
    analysis = module.analyze(valid)
    selected = module.filter_history(valid, records)
    require(selected["status"] == "possible" and selected["likelihood"] == [1, 4], "joint evidence")
    require(selected["posterior"] == [{"class_id":1,"probability":[1,2]},{"class_id":4,"probability":[1,2]}], "current belief")
    require(module.filter_history(valid, [[1,1,1,0,0]] * 2) == {"status":"impossible","failed_stage":1,"likelihood":[0,1],"posterior":None,"prediction":None}, "first impossibility")
    require(module.filter_history(valid, [records[0], [1,1,1,0,0]])["failed_stage"] == 2, "second impossibility")
    for method in ("analyze", "filter_history"):
        call = module.analyze if method == "analyze" else lambda value: module.filter_history(value, records)
        for bad_fraction in ([2,4], [True,2], [1,0], [1,1<<64], "1/2", (1,2), [I(1),2]):
            bad = copy.deepcopy(valid); bad["prior"][0]["probability"] = bad_fraction
            reject(call, bad)
        for kind in ("dict", "key", "value", "list", "tuple", "float", "cycle", "deep", "dag"):
            bad = copy.deepcopy(valid)
            if kind == "dict": bad = D(bad)
            elif kind == "key": bad[S("schema_version")] = bad.pop("schema_version")
            elif kind == "value": bad["schema_version"] = S(bad["schema_version"])
            elif kind == "list": bad["extra"] = L()
            elif kind == "tuple": bad["extra"] = ()
            elif kind == "float": bad["extra"] = 0.0
            elif kind == "cycle":
                value = []; value.append(value); bad["extra"] = value
            elif kind == "deep":
                value = []
                for _ in range(1500): value = [value]
                bad["extra"] = value
            else: bad["extra"] = dag()
            reject(call, bad)
        for field in ("classes", "labels"):
            bad = copy.deepcopy(valid); bad["model"][field] = [dag()]; reject(call, bad)
        for field in ("prior", "rates"):
            bad = copy.deepcopy(valid); bad[field] = [dag()]; reject(call, bad)
        for name in ("fractional", "mixed"): reject(call, payload[name])
        saved = module.WORKING_CAP; module.WORKING_CAP = 32
        try: reject(call, valid)
        finally: module.WORKING_CAP = saved
    for bad_records in ([[False,1,1,0,0], records[1]], [[0,True,1,0,0], records[1]], [[1,1,1,0,0],[0,1,3,0,0]], [dag(),dag()]):
        reject(lambda value: module.filter_history(valid, value), bad_records)
    shared = copy.deepcopy(valid)
    shared["model"]["classes"][0]["even"] = shared["model"]["classes"][0]["odd"]
    require(module.analyze(shared) == analysis, "valid shared list rejected")
    selected["posterior"][0]["probability"][0] = -99
    require(module.filter_history(valid, records)["posterior"][0]["probability"] == [1,2], "output alias")
runner = load("_qr05u_guard_runner", "study.py")
reject(runner.require_wire, {"extra":dag()})
reject(lambda value: runner.require_same_wire({"zero":0},value,"typed"), {"zero":False})
print("bounded explicit rejection checks:", count)
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE), json.dumps(payload)])
    result = subprocess.run(arguments, text=True, capture_output=True, timeout=20, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "bounded explicit rejection checks: 102"
