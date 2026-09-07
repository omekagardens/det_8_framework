"""Independent W noisy-readout, raw-joint and two-replica Brier tests.

Pinned V JSON supplies declared U producer evidence; no previous
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


LEVELS = (F(0), F(1, 2), F(3, 4), F(1))
GARBLINGS = (F(1, 2), F(1, 2), F(1))
V_SHA = "eceb01f49624f3d5ebb5dc8041074aa04b62d8408d4a7117979fb1c6b9823ff7"


def squared_distance(left, right):
    return sum((left.get(q, F(0)) - right.get(q, F(0))) ** 2 for q in left.keys() | right.keys())


def bayes_risk(law):
    assert sum(law.values()) == 1
    return 1 - sum(p * p for p in law.values())


def laws_from_wire(law):
    return {tuple(atom["value"]): fraction(atom["probability"]) for atom in law}


@pytest.fixture(scope="session")
def pinned_v():
    path = HERE.parent / "qr-05v-readout-value-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 3493736 and hashlib.sha256(raw).hexdigest() == V_SHA
    envelope = json.loads(raw)
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


@pytest.fixture(scope="session")
def supplied(pinned_v):
    return {
        "raw_model": copy.deepcopy(pinned_v["raw_model"]),
        "model": copy.deepcopy(pinned_v["model"]),
        "cases": [
            {
                **{
                    key: copy.deepcopy(row[key])
                    for key in ("case_id", "raw_prior", "prior", "rates", "u_analysis")
                },
                "v_analysis": copy.deepcopy(row["analysis"]),
            }
            for row in pinned_v["cases"]
        ],
    }


def problem_for(model, case):
    return {
        "schema_version": "det8-qr05w-problem-v1",
        "family": "qr05w_noisy_readouts",
        "model": model,
        "rate": case["rates"][2],
        "beliefs": [
            {key: row[key] for key in ("belief_id", "weight", "posterior")}
            for row in case["v_analysis"]["beliefs"]
        ],
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05w_test_direct", "noisy_readout.py"),
        private_module("_qr05w_test_reference", "reference_qr05w.py"),
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
    runner = private_module("_qr05w_test_runner", "study.py")
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


def alphabets(labels):
    result = {}
    for row in labels:
        result.setdefault(tuple(row["observation"]), set()).add(tuple(row["question"]))
    return {n: tuple(sorted(values)) for n, values in sorted(result.items())}


def replacement(fibers, source, level):
    values = fibers[source[:5]]
    return {z: p for z in values if (p := (1 - level) * (z == source) + level / len(values))}


def channel_model(labels):
    fibers = alphabets(labels)
    sources = sorted(a for values in fibers.values() for a in values)
    channels = [
        {
            "level": fw(level),
            "rows": [
                {
                    "source": list(source),
                    "transitions": question_law(replacement(fibers, source, level)),
                }
                for source in sources
            ],
        }
        for level in LEVELS
    ]
    checks = []
    for i, extra in enumerate(GARBLINGS):
        composed, terms = [], 0
        for source in sources:
            products = {}
            for middle, left in replacement(fibers, source, LEVELS[i]).items():
                for target, right in replacement(fibers, middle, extra).items():
                    terms += 1
                    accumulate(products, target, left * right)
            assert sum(products.values()) == 1
            composed.append({"source": list(source), "transitions": question_law(products)})
        assert wire(composed) == wire(channels[i + 1]["rows"])
        checks.append(
            {
                "from_index": i,
                "to_index": i + 1,
                "garbling_level": fw(extra),
                "row_comparisons": len(sources),
                "product_terms": terms,
                "positive_composed_atoms": sum(len(row["transitions"]) for row in composed),
                "composed_sha256": digest(composed),
                "exact": True,
            }
        )
    return {
        "alphabet": [
            {"N": list(n), "values": [list(a) for a in values]} for n, values in fibers.items()
        ],
        "channels": channels,
        "composition_checks": checks,
    }


def score_raw_cells(oracle, pair, groups, rate):
    cells = []
    replica_expected = F(0)
    for value, mass in sorted(groups.items()):
        weight = sum(mass.values())
        conditional = normalized(mass)
        prediction = oracle.predict(conditional, rate)
        risk = pair.risk(conditional, rate)
        assert risk == bayes_risk(prediction)
        # Independent raw replicas must share the received noisy report, but
        # not the latent state or fresh future draw. Normalize per report.
        replica_expected += (
            sum(
                pa * pb * pair.disagreement(min(a, b), max(a, b), rate)
                for a, pa in mass.items()
                for b, pb in mass.items()
            )
            / weight
        )
        cells.append(
            {
                "value": value,
                "probability": weight,
                "posterior": oracle.coarse(conditional),
                "prediction": prediction,
                "risk": risk,
            }
        )
    assert sum(cell["probability"] for cell in cells) == 1
    assert replica_expected == sum(cell["probability"] * cell["risk"] for cell in cells)
    return cells, replica_expected


def raw_garbling(earlier, later, fibers, index):
    extra = GARBLINGS[index]
    pair_mass = {}
    for cell in earlier:
        for target, probability in replacement(fibers, cell["value"], extra).items():
            accumulate(pair_mass, (cell["value"], target), cell["probability"] * probability)
    earlier_by = {cell["value"]: cell for cell in earlier}
    later_by = {cell["value"]: cell for cell in later}
    left, right = {}, {}
    for (z, w), probability in pair_mass.items():
        accumulate(left, z, probability)
        accumulate(right, w, probability)
    assert left == {cell["value"]: cell["probability"] for cell in earlier}
    assert right == {cell["value"]: cell["probability"] for cell in later}
    receiving = []
    increase = variance = F(0)
    for w, cell in sorted(later_by.items()):
        incoming = [
            (z, probability)
            for (z, target), probability in sorted(pair_mass.items())
            if target == w
        ]
        posterior, future = {}, {}
        conditional_variance = earlier_risk = F(0)
        equalities = []
        for z, probability in incoming:
            reverse = probability / cell["probability"]
            source = earlier_by[z]
            for h, p in source["posterior"].items():
                accumulate(posterior, h, reverse * p)
            for q, p in source["prediction"].items():
                accumulate(future, q, reverse * p)
            earlier_risk += reverse * source["risk"]
            conditional_variance += reverse * squared_distance(
                source["prediction"], cell["prediction"]
            )
            equalities.append(source["prediction"] == cell["prediction"])
        assert posterior == cell["posterior"] and future == cell["prediction"]
        conditional_increase = cell["risk"] - earlier_risk
        equal = all(equalities)
        assert conditional_increase == conditional_variance >= 0
        assert (conditional_increase == 0) == equal
        increase += cell["probability"] * conditional_increase
        variance += cell["probability"] * conditional_variance
        receiving.append(
            {
                "value": list(w),
                "probability": fw(cell["probability"]),
                "earlier_values": [list(z) for z, _ in incoming],
                "posterior_mixture_sha256": digest(belief(posterior)),
                "prediction_mixture_sha256": digest(question_law(future)),
                "conditional_risk_increase": fw(conditional_increase),
                "conditional_variance_loss": fw(conditional_variance),
                "predictions_equal": equal,
            }
        )
    assert increase == variance
    assert (increase == 0) == all(row["predictions_equal"] for row in receiving)
    return {
        "from_index": index,
        "to_index": index + 1,
        "garbling_level": fw(extra),
        "risk_increase": fw(increase),
        "variance_loss": fw(variance),
        "couplings": [
            {"earlier": list(z), "later": list(w), "probability": fw(probability)}
            for (z, w), probability in sorted(pair_mass.items())
        ],
        "receiving_checks": receiving,
        "zero_loss_iff_equal": True,
    }


def raw_noisy_readout(oracle, pair, case):
    rate = tuple(fraction(value) for value in case["rates"][2])
    authenticated = authenticated_histories(oracle, case)
    fibers = alphabets(oracle.labels)
    rows = []
    for bid, (_, weight, raw) in enumerate(authenticated):
        baseline_law = oracle.predict(raw, rate)
        baseline_risk = pair.risk(raw, rate)
        assert baseline_risk == bayes_risk(baseline_law)
        current = oracle.coarse(raw)
        n_groups = {}
        for sid, p in raw.items():
            accumulate(n_groups.setdefault(oracle.observations[sid], {}), sid, p)
        n_cells, n_risk = score_raw_cells(oracle, pair, n_groups, rate)
        h_risk = sum(p * pair.risk({sid: F(1)}, rate) for sid, p in raw.items())
        channels, all_cells = [], []
        for level in LEVELS:
            groups = {}
            for sid, p in raw.items():
                for z, probability in replacement(fibers, oracle.questions[sid], level).items():
                    accumulate(groups.setdefault(z, {}), sid, p * probability)
            cells, expected_risk = score_raw_cells(oracle, pair, groups, rate)
            current_marginal, future_marginal = {}, {}
            for cell in cells:
                for h, p in cell["posterior"].items():
                    accumulate(current_marginal, h, cell["probability"] * p)
                for q, p in cell["prediction"].items():
                    accumulate(future_marginal, q, cell["probability"] * p)
            assert current_marginal == current and future_marginal == baseline_law
            gain = baseline_risk - expected_risk
            variance = sum(
                cell["probability"] * squared_distance(cell["prediction"], baseline_law)
                for cell in cells
            )
            assert gain == variance >= 0
            channels.append(
                {
                    "level": fw(level),
                    "cells": [cell_wire(cell) for cell in cells],
                    "expected_risk": fw(expected_risk),
                    "gain": fw(gain),
                    "variance_gain": fw(variance),
                    "gain_over_N": fw(n_risk - expected_risk),
                    "retained_gain_fraction": None,
                }
            )
            all_cells.append(cells)
        clean_gain = fraction(channels[0]["gain_over_N"])
        for row in channels:
            row["retained_gain_fraction"] = (
                fw(fraction(row["gain_over_N"]) / clean_gain) if clean_gain else None
            )
        edges = [raw_garbling(all_cells[i], all_cells[i + 1], fibers, i) for i in range(3)]
        risks = (
            [h_risk]
            + [fraction(row["expected_risk"]) for row in channels]
            + [n_risk, baseline_risk]
        )
        assert all(left <= right for left, right in pairwise(risks))
        assert fraction(channels[-1]["expected_risk"]) == n_risk
        assert sum(fraction(edge["risk_increase"]) for edge in edges) == clean_gain
        n_by = {cell["value"]: cell for cell in n_cells}
        for cell in all_cells[-1]:
            n = cell["value"][:5]
            assert cell["probability"] == n_by[n]["probability"] / len(fibers[n])
            assert cell["posterior"] == n_by[n]["posterior"]
            assert cell["prediction"] == n_by[n]["prediction"]
        # V producer evidence is checked by the separately reconstructed raw
        # N control, clean NMT cells, oracle residual and baseline here.
        producer = case["v_analysis"]["beliefs"][bid]
        assert producer["belief_id"] == bid and producer["weight"] == fw(weight)
        assert producer["posterior"] == belief(current)
        assert producer["baseline"] == {
            "prediction": question_law(baseline_law),
            "risk": fw(baseline_risk),
        }
        assert producer["readouts"]["N"]["cells"] == [cell_wire(cell) for cell in n_cells]
        assert producer["readouts"]["NMT"]["cells"] == channels[0]["cells"]
        assert producer["oracle_residual"] == fw(h_risk)
        rows.append(
            {
                "belief_id": bid,
                "weight": fw(weight),
                "posterior": belief(current),
                "baseline": {"prediction": question_law(baseline_law), "risk": fw(baseline_risk)},
                "controls": {
                    "N": {
                        "cells": [cell_wire(cell) for cell in n_cells],
                        "expected_risk": fw(n_risk),
                        "gain": fw(baseline_risk - n_risk),
                    },
                    "H": {"expected_risk": fw(h_risk), "gain": fw(baseline_risk - h_risk)},
                },
                "channels": channels,
                "garblings": edges,
                "checks": {
                    "probabilities_normalized": True,
                    "marginal_current_preserved": True,
                    "marginal_future_preserved": True,
                    "garbling_marginals": True,
                    "conditional_mixtures": True,
                    "risk_order": True,
                    "endpoint_information_equivalence": True,
                    "losses_telescope": True,
                    "N_already_known": len(n_cells) == 1,
                },
            }
        )

    def weighted(getter):
        return fw(sum(fraction(row["weight"]) * getter(row) for row in rows))

    total_prediction = {}
    for row in rows:
        for atom in row["baseline"]["prediction"]:
            accumulate(
                total_prediction,
                tuple(atom["value"]),
                fraction(row["weight"]) * fraction(atom["probability"]),
            )
    weighted_channels = []
    for i, level in enumerate(LEVELS):
        weighted_channels.append(
            {
                "level": fw(level),
                **{
                    key: weighted(lambda row, i=i, key=key: fraction(row["channels"][i][key]))
                    for key in ("expected_risk", "gain", "gain_over_N")
                },
                "retained_gain_fraction": None,
            }
        )
    clean = fraction(weighted_channels[0]["gain_over_N"])
    for row in weighted_channels:
        row["retained_gain_fraction"] = fw(fraction(row["gain_over_N"]) / clean) if clean else None

    def first(getter, positive):
        return next(
            (
                row["belief_id"]
                for row in rows
                if (getter(row) > 0 if positive else getter(row) == 0)
            ),
            None,
        )

    kernel_rows = oracle.class_kernel(*rate)
    channel = channel_model(oracle.labels)
    counts = {
        "classes": len(oracle.classes),
        "beliefs": len(rows),
        "profile_atoms": oracle.reconstruction["profile_atoms"],
        "kernel_atoms": sum(len(row["transitions"]) for row in kernel_rows),
        "alphabet_fibers": len(fibers),
        "alphabet_values": sum(map(len, fibers.values())),
        "global_channel_atoms": [
            sum(len(row["transitions"]) for row in c["rows"]) for c in channel["channels"]
        ],
        "posterior_atoms": sum(len(row["posterior"]) for row in rows),
        **{
            name: [
                sum(
                    sum(len(cell[field]) if field else 1 for cell in row["channels"][i]["cells"])
                    for row in rows
                )
                for i in range(4)
            ]
            for name, field in (
                ("channel_cells", None),
                ("channel_posterior_atoms", "posterior"),
                ("channel_prediction_atoms", "prediction"),
            )
        },
        **{
            name: sum(
                sum(len(cell[field]) if field else 1 for cell in row["controls"]["N"]["cells"])
                for row in rows
            )
            for name, field in (
                ("N_cells", None),
                ("N_posterior_atoms", "posterior"),
                ("N_prediction_atoms", "prediction"),
            )
        },
        "coupling_atoms": [
            sum(len(row["garblings"][i]["couplings"]) for row in rows) for i in range(3)
        ],
        "receiving_checks": [
            sum(len(row["garblings"][i]["receiving_checks"]) for row in rows) for i in range(3)
        ],
        "strict_gain_beliefs": [
            sum(fraction(row["channels"][i]["gain_over_N"]) > 0 for row in rows) for i in range(4)
        ],
        "no_gain_beliefs": [
            sum(fraction(row["channels"][i]["gain_over_N"]) == 0 for row in rows) for i in range(4)
        ],
        "strict_loss_beliefs": [
            sum(fraction(row["garblings"][i]["risk_increase"]) > 0 for row in rows)
            for i in range(3)
        ],
        "no_loss_beliefs": [
            sum(fraction(row["garblings"][i]["risk_increase"]) == 0 for row in rows)
            for i in range(3)
        ],
        "positive_oracle_residual_beliefs": sum(
            fraction(row["controls"]["H"]["expected_risk"]) > 0 for row in rows
        ),
        "known_N_beliefs": sum(row["checks"]["N_already_known"] for row in rows),
    }
    answer = {
        "model_sha256": digest(oracle.model),
        "reconstruction": oracle.reconstruction,
        "rate": case["rates"][2],
        "kernel_sha256": digest(kernel_rows),
        "channel_model": channel,
        "beliefs": rows,
        "aggregate": {
            "total_weight": [1, 1],
            "prediction": question_law(total_prediction),
            "baseline_risk": weighted(lambda row: fraction(row["baseline"]["risk"])),
            "N_risk": weighted(lambda row: fraction(row["controls"]["N"]["expected_risk"])),
            "H_risk": weighted(lambda row: fraction(row["controls"]["H"]["expected_risk"])),
            "channels": weighted_channels,
            "adjacent_risk_increase": [
                weighted(lambda row, i=i: fraction(row["garblings"][i]["risk_increase"]))
                for i in range(3)
            ],
        },
        "witnesses": {
            "first_strict_gain": [
                first(lambda row, i=i: fraction(row["channels"][i]["gain_over_N"]), True)
                for i in range(4)
            ],
            "first_zero_gain": [
                first(lambda row, i=i: fraction(row["channels"][i]["gain_over_N"]), False)
                for i in range(4)
            ],
            "first_strict_loss": [
                first(lambda row, i=i: fraction(row["garblings"][i]["risk_increase"]), True)
                for i in range(3)
            ],
            "first_zero_loss": [
                first(lambda row, i=i: fraction(row["garblings"][i]["risk_increase"]), False)
                for i in range(3)
            ],
            "first_positive_oracle_residual": first(
                lambda row: fraction(row["controls"]["H"]["expected_risk"]), True
            ),
            "first_zero_oracle_residual": first(
                lambda row: fraction(row["controls"]["H"]["expected_risk"]), False
            ),
        },
        "counts": counts,
    }
    return answer, authenticated


@pytest.fixture(scope="session")
def expected(oracle, supplied):
    pair = PairRiskOracle(oracle)
    return [raw_noisy_readout(oracle, pair, case) for case in supplied["cases"]]


def test_all_482_input_beliefs_and_raw_model_are_independently_authenticated(
    supplied, oracle, expected
):
    assert wire(supplied["model"]) == wire(oracle.model)
    assert len(oracle.states) == 4447 and len(oracle.classes) == 416
    assert sum(len(histories) for _, histories in expected) == 482
    for case, (a, histories) in zip(supplied["cases"], expected, strict=True):
        p = problem_for(supplied["model"], case)
        assert [
            {key: row[key] for key in ("belief_id", "weight", "posterior")} for row in a["beliefs"]
        ] == p["beliefs"]
        assert (
            a["aggregate"]["prediction"] == (case["u_analysis"]["unconditional"]["next_prediction"])
        )
        for row, (history, _, raw) in zip(a["beliefs"], histories, strict=True):
            assert {oracle.observations[sid] for sid in raw} == {history[1]}
            assert row["checks"]["N_already_known"] is True
            assert row["controls"]["N"]["gain"] == [0, 1]


@pytest.mark.parametrize("case_index", range(6))
def test_complete_wires_equal_raw_joint_and_independent_two_replica_risk(
    analyses, expected, case_index
):
    primary, reference = analyses[case_index]
    assert wire(primary) == wire(reference) == wire(expected[case_index][0])
    assert wire(json.loads(wire(primary))) == wire(primary)
    assert len(wire(primary)) < 64 * 1024 * 1024


def test_every_raw_member_has_the_certified_fixed_K3_class_kernel(supplied, oracle):
    rates = {tuple(map(fraction, case["rates"][2])) for case in supplied["cases"]}
    for rate in rates:
        rows = oracle.class_kernel(*rate)
        for sid, cid in enumerate(oracle.vector):
            assert oracle.coarse(dict(oracle.transition(sid, *rate))) == {
                atom["target_class"]: fraction(atom["probability"])
                for atom in rows[cid]["transitions"]
            }


def test_noise_value_formula_is_checked_not_counted_as_new_robustness_evidence(expected):
    for a, _ in expected:
        fibers = {tuple(row["N"]): row["values"] for row in a["channel_model"]["alphabet"]}
        for row in a["beliefs"]:
            by_n = {tuple(cell["value"]): cell for cell in row["controls"]["N"]["cells"]}
            clean = row["channels"][0]["cells"]
            for channel in row["channels"]:
                t = fraction(channel["level"])
                formula = F(0)
                for cell in clean:
                    n = tuple(cell["value"][:5])
                    control = by_n[n]
                    n_mass = fraction(control["probability"])
                    alpha = fraction(cell["probability"]) / n_mass
                    display_mass = (1 - t) * alpha + t / len(fibers[n])
                    formula += (
                        n_mass
                        * (1 - t) ** 2
                        * alpha**2
                        / display_mass
                        * squared_distance(
                            laws_from_wire(cell["prediction"]),
                            laws_from_wire(control["prediction"]),
                        )
                    )
                assert formula == fraction(channel["gain_over_N"])
                clean_gain = fraction(row["channels"][0]["gain_over_N"])
                assert (fraction(channel["gain_over_N"]) > 0) == (clean_gain > 0 and t < 1)
                assert channel["retained_gain_fraction"] == (
                    fw(formula / clean_gain) if clean_gain else None
                )


def test_couplings_are_overlapping_laws_with_both_marginals_and_reverse_bayes_weights(expected):
    for a, _ in expected:
        for row in a["beliefs"]:
            for i, edge in enumerate(row["garblings"]):
                earlier = {tuple(c["value"]): c for c in row["channels"][i]["cells"]}
                later = {tuple(c["value"]): c for c in row["channels"][i + 1]["cells"]}
                left, right = {}, {}
                for atom in edge["couplings"]:
                    z, w = tuple(atom["earlier"]), tuple(atom["later"])
                    probability = fraction(atom["probability"])
                    assert probability > 0 and z[:5] == w[:5]
                    accumulate(left, z, probability)
                    accumulate(right, w, probability)
                assert left == {z: fraction(c["probability"]) for z, c in earlier.items()}
                assert right == {w: fraction(c["probability"]) for w, c in later.items()}
                for receiving in edge["receiving_checks"]:
                    w = tuple(receiving["value"])
                    incoming = [atom for atom in edge["couplings"] if tuple(atom["later"]) == w]
                    assert receiving["earlier_values"] == [atom["earlier"] for atom in incoming]
                    posterior, prediction = {}, {}
                    weighted_risk = variance = F(0)
                    equalities = []
                    for atom in incoming:
                        source = earlier[tuple(atom["earlier"])]
                        reverse = fraction(atom["probability"]) / right[w]
                        for h in source["posterior"]:
                            accumulate(
                                posterior, h["class_id"], reverse * fraction(h["probability"])
                            )
                        for q in source["prediction"]:
                            accumulate(
                                prediction, tuple(q["value"]), reverse * fraction(q["probability"])
                            )
                        weighted_risk += reverse * fraction(source["risk"])
                        variance += reverse * squared_distance(
                            laws_from_wire(source["prediction"]),
                            laws_from_wire(later[w]["prediction"]),
                        )
                        equalities.append(source["prediction"] == later[w]["prediction"])
                    assert belief(posterior) == later[w]["posterior"]
                    assert question_law(prediction) == later[w]["prediction"]
                    assert receiving["posterior_mixture_sha256"] == digest(belief(posterior))
                    assert receiving["prediction_mixture_sha256"] == digest(
                        question_law(prediction)
                    )
                    assert (
                        receiving["conditional_risk_increase"]
                        == fw(fraction(later[w]["risk"]) - weighted_risk)
                        == receiving["conditional_variance_loss"]
                        == fw(variance)
                    )
                    assert receiving["predictions_equal"] == all(equalities)
                assert edge["zero_loss_iff_equal"] is True
                assert (fraction(edge["risk_increase"]) == 0) == all(
                    r["predictions_equal"] for r in edge["receiving_checks"]
                )


def test_case_risks_retention_and_witnesses_use_actual_history_weights(expected):
    for a, _ in expected:
        rows = a["beliefs"]
        assert sum(fraction(row["weight"]) for row in rows) == 1
        weighted_baseline = sum(
            fraction(row["weight"]) * fraction(row["baseline"]["risk"]) for row in rows
        )
        assert a["aggregate"]["baseline_risk"] == fw(weighted_baseline)
        assert bayes_risk(laws_from_wire(a["aggregate"]["prediction"])) >= weighted_baseline
        clean_gain = fraction(a["aggregate"]["channels"][0]["gain_over_N"])
        for i, channel in enumerate(a["aggregate"]["channels"]):
            for key in ("expected_risk", "gain", "gain_over_N"):
                assert channel[key] == fw(
                    sum(fraction(row["weight"]) * fraction(row["channels"][i][key]) for row in rows)
                )
            assert channel["retained_gain_fraction"] == (
                fw(fraction(channel["gain_over_N"]) / clean_gain) if clean_gain else None
            )
            strict = [r["belief_id"] for r in rows if fraction(r["channels"][i]["gain_over_N"]) > 0]
            zero = [r["belief_id"] for r in rows if fraction(r["channels"][i]["gain_over_N"]) == 0]
            assert a["witnesses"]["first_strict_gain"][i] == (strict[0] if strict else None)
            assert a["witnesses"]["first_zero_gain"][i] == (zero[0] if zero else None)
            assert a["counts"]["strict_gain_beliefs"][i] == len(strict)
            assert a["counts"]["no_gain_beliefs"][i] == len(zero)
        for i in range(3):
            strict = [
                r["belief_id"] for r in rows if fraction(r["garblings"][i]["risk_increase"]) > 0
            ]
            zero = [
                r["belief_id"] for r in rows if fraction(r["garblings"][i]["risk_increase"]) == 0
            ]
            assert a["witnesses"]["first_strict_loss"][i] == (strict[0] if strict else None)
            assert a["witnesses"]["first_zero_loss"][i] == (zero[0] if zero else None)
            assert a["counts"]["strict_loss_beliefs"][i] == len(strict)
            assert a["counts"]["no_loss_beliefs"][i] == len(zero)
        assert sum(map(fraction, a["aggregate"]["adjacent_risk_increase"])) == clean_gain


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
        "schema_version": "det8-qr05w-problem-v1",
        "family": "qr05w_noisy_readouts",
        "model": micro_model(),
        "rate": rate,
        "beliefs": [{"belief_id": 0, "weight": [1, 1], "posterior": prior}],
    }


def binary_problem(prior=F(1, 2), third=False, duplicate=False, rate=None):
    # This is a structurally valid local algebra with annotated labels, not
    # a newly authenticated physical or raw-order model.
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
    top = classes[8]
    classes.append({**copy.deepcopy(top), "class_id": 9})
    obs = list(labels[8]["observation"])
    labels.append({"class_id": 9, "observation": list(obs), "question": obs + [1, 0]})
    if third:
        classes.append({**copy.deepcopy(top), "class_id": len(classes)})
        labels.append({"class_id": len(labels), "observation": list(obs), "question": obs + [0, 1]})
    if duplicate:
        classes.append({**copy.deepcopy(top), "class_id": len(classes)})
        labels.append({"class_id": len(labels), "observation": list(obs), "question": obs + [0, 0]})
    p = micro_problem()
    p["model"] = {"classes": classes, "labels": labels}
    p["rate"] = rate or [[1, 1], [1, 1]]
    p["beliefs"][0]["posterior"] = [
        {"class_id": cid, "probability": fw(probability)}
        for cid, probability in ((8, prior), (9, 1 - prior))
        if probability
    ]
    return p


def test_fair_binary_unflagged_replacement_has_exact_risk_and_quadratic_retention(executors):
    for module in executors:
        a = module.analyze(binary_problem())
        row = a["beliefs"][0]
        assert row["baseline"]["risk"] == [1, 2]
        assert row["controls"]["H"]["expected_risk"] == [0, 1]
        assert [c["expected_risk"] for c in row["channels"]] == [[0, 1], [3, 8], [15, 32], [1, 2]]
        assert [c["retained_gain_fraction"] for c in row["channels"]] == [
            [1, 1],
            [1, 4],
            [1, 16],
            [0, 1],
        ]
        assert [g["risk_increase"] for g in row["garblings"]] == [[3, 8], [3, 32], [1, 32]]
        assert a["channel_model"] == channel_model(binary_problem()["model"]["labels"])
        for edge in row["garblings"]:
            assert len(edge["couplings"]) == 4
            assert all(len(c["earlier_values"]) == 2 for c in edge["receiving_checks"])


def test_revealing_noise_coin_changes_the_experiment_and_artificially_lowers_risk(executors):
    t, baseline, clean = F(1, 2), F(1, 2), F(0)
    flagged_risk = (1 - t) * clean + t * baseline
    assert flagged_risk == F(1, 4)
    for module in executors:
        channel = module.analyze(binary_problem())["beliefs"][0]["channels"][1]
        assert fraction(channel["expected_risk"]) == F(3, 8) > flagged_risk
        # Replacement can draw the original symbol; "changed symbol" is not
        # a valid replacement-coin flag either.
        assert [cell["probability"] for cell in channel["cells"]] == [[1, 2], [1, 2]]
        assert all(
            set(cell) == {"value", "probability", "posterior", "prediction", "risk"}
            for cell in channel["cells"]
        )


def test_pointwise_risk_may_fall_even_while_expected_risk_increases(executors):
    for module in executors:
        row = module.analyze(binary_problem(F(9, 10)))["beliefs"][0]
        half, three_quarters = row["channels"][1:3]
        rare_half, rare_later = half["cells"][1], three_quarters["cells"][1]
        assert rare_half["value"] == rare_later["value"]
        assert rare_half["risk"] == [3, 8]
        assert rare_later["risk"] == [135, 512]
        assert fraction(rare_later["risk"]) < fraction(rare_half["risk"])
        assert half["expected_risk"] == [9, 56]
        assert three_quarters["expected_risk"] == [45, 256]
        assert fraction(half["expected_risk"]) < fraction(three_quarters["expected_risk"])


def test_noisy_two_replica_risk_requires_each_report_own_normalization(executors):
    for module in executors:
        row = module.analyze(binary_problem(F(1, 4)))["beliefs"][0]
        channel = row["channels"][1]
        assert [c["probability"] for c in channel["cells"]] == [[3, 8], [5, 8]]
        assert channel["expected_risk"] == [3, 10]
        wrong_unnormalized = sum(
            fraction(c["probability"]) ** 2 * fraction(c["risk"]) for c in channel["cells"]
        )
        wrong_equal_report_conditioning = wrong_unnormalized / sum(
            fraction(c["probability"]) ** 2 for c in channel["cells"]
        )
        assert wrong_unnormalized == F(9, 64) != F(3, 10)
        assert wrong_equal_report_conditioning == F(9, 34) != F(3, 10)


def test_full_model_distinct_label_alphabet_includes_zero_posterior_labels(executors):
    p = binary_problem(third=True, duplicate=True)
    n = [0, 1, 4, 0, 0]
    zero_label = n + [0, 1]
    for module in executors:
        a = module.analyze(p)
        row = a["beliefs"][0]
        fiber = next(f for f in a["channel_model"]["alphabet"] if f["N"] == n)
        assert len(fiber["values"]) == 3
        assert zero_label in fiber["values"]
        assert len(row["channels"][0]["cells"]) == 2
        assert len(row["channels"][1]["cells"]) == 3
        reported = next(c for c in row["channels"][1]["cells"] if c["value"] == zero_label)
        assert reported["probability"] == [1, 6]
        assert reported["posterior"] == row["posterior"]
        assert reported["prediction"] == row["baseline"]["prediction"]
        assert all(c["probability"] == [1, 3] for c in row["channels"][-1]["cells"])
        # Removing a duplicate class must not change the channel or risk.
        no_duplicate = module.analyze(binary_problem(third=True))
        assert a["channel_model"] == no_duplicate["channel_model"]
        assert a["aggregate"] == no_duplicate["aggregate"]


def test_complete_replacement_is_N_information_equivalence_not_record_equality(executors):
    for module in executors:
        row = module.analyze(binary_problem(third=True))["beliefs"][0]
        n = row["controls"]["N"]["cells"]
        complete = row["channels"][-1]["cells"]
        assert len(n) == 1 and len(complete) == 3
        assert n != complete
        for cell in complete:
            assert cell["probability"] == [1, 3]
            assert cell["posterior"] == n[0]["posterior"]
            assert cell["prediction"] == n[0]["prediction"]
            assert cell["risk"] == n[0]["risk"]


def test_distinct_labels_can_change_posteriors_without_predictive_gain(executors):
    for module in executors:
        row = module.analyze(binary_problem(rate=[[0, 1], [1, 2]]))["beliefs"][0]
        assert row["baseline"]["risk"] == row["controls"]["H"]["expected_risk"] == [5, 8]
        for channel in row["channels"]:
            assert channel["gain_over_N"] == [0, 1]
            assert channel["retained_gain_fraction"] is None
            assert channel["expected_risk"] == [5, 8]
            assert all(
                cell["prediction"] == row["baseline"]["prediction"] for cell in channel["cells"]
            )
        assert row["channels"][0]["cells"][0]["posterior"] != row["posterior"]
        assert all(
            edge["zero_loss_iff_equal"]
            and edge["risk_increase"] == [0, 1]
            and all(c["predictions_equal"] for c in edge["receiving_checks"])
            for edge in row["garblings"]
        )


def test_future_correlated_report_can_fake_value_without_changing_report_marginal(executors):
    p = binary_problem(F(1), rate=[[0, 1], [1, 2]])
    for module in executors:
        row = module.analyze(p)["beliefs"][0]
        channel = row["channels"][1]
        assert row["baseline"]["risk"] == row["controls"]["H"]["expected_risk"] == [5, 8]
        assert [cell["probability"] for cell in channel["cells"]] == [[3, 4], [1, 4]]
        assert channel["expected_risk"] == [5, 8] and channel["gain"] == [0, 1]
        # Illicitly emit the rare report iff the FUTURE state is empty:
        # report probabilities remain (3/4,1/4), but the conditional
        # independence premise fails and the true risk drops to1/3.
        leaked_risk = F(3, 4) * bayes_risk({1: F(2, 3), 2: F(1, 3)})
        assert leaked_risk == F(1, 3) < F(5, 8)
        assert all(cell["prediction"] == row["baseline"]["prediction"] for cell in channel["cells"])


def test_single_symbol_fibers_and_generic_multi_N_gains_are_not_added_NMT_value(executors):
    for module in executors:
        a = module.analyze(micro_problem("identity"))
        row = a["beliefs"][0]
        assert row["baseline"]["risk"] == [3, 8] and row["checks"]["N_already_known"] is False
        assert row["controls"]["N"]["expected_risk"] == [0, 1]
        for channel in row["channels"]:
            assert channel["expected_risk"] == [0, 1] and channel["gain"] == [3, 8]
            assert channel["gain_over_N"] == [0, 1] and channel["retained_gain_fraction"] is None
        assert a["counts"]["strict_gain_beliefs"] == [0, 0, 0, 0]
        assert a["witnesses"]["first_strict_gain"] == [None] * 4
        assert a["witnesses"]["first_zero_gain"] == [0] * 4
        rare = row["channels"][0]["cells"][0]
        assert (
            squared_distance(
                laws_from_wire(rare["prediction"]), laws_from_wire(row["baseline"]["prediction"])
            )
            == F(9, 8)
            > 1
        )
        assert fraction(rare["probability"]) * F(9, 8) == F(9, 32)


def test_retention_aggregates_as_ratio_of_weighted_gains_not_average_ratios(executors):
    p = binary_problem()
    p["beliefs"][0]["weight"] = [1, 4]
    p["beliefs"].append(
        {
            "belief_id": 1,
            "weight": [3, 4],
            "posterior": binary_problem(F(1, 4))["beliefs"][0]["posterior"],
        }
    )
    for module in executors:
        a = module.analyze(p)
        channel = a["aggregate"]["channels"][1]
        assert channel["gain_over_N"] == [7, 80]
        assert channel["retained_gain_fraction"] == [14, 65]
        average_ratio = sum(
            fraction(r["weight"]) * fraction(r["channels"][1]["retained_gain_fraction"])
            for r in a["beliefs"]
        )
        assert average_ratio == F(17, 80) != fraction(channel["retained_gain_fraction"])


def test_history_conditioned_risks_are_not_risk_of_the_mixed_prediction(executors):
    p = micro_problem()
    p["beliefs"] = [
        {"belief_id": 0, "weight": [1, 4], "posterior": [{"class_id": 0, "probability": [1, 1]}]},
        {"belief_id": 1, "weight": [3, 4], "posterior": [{"class_id": 1, "probability": [1, 1]}]},
    ]
    for module in executors:
        a = module.analyze(p)
        assert a["aggregate"]["baseline_risk"] == [3, 8]
        assert bayes_risk(laws_from_wire(a["aggregate"]["prediction"])) == F(15, 32)
        assert all(c["gain_over_N"] == [0, 1] for c in a["aggregate"]["channels"])


def test_complete_deletion_preserves_current_posteriors_without_future_uncertainty(executors):
    for module in executors:
        row = module.analyze(binary_problem(rate=[[0, 1], [0, 1]]))["beliefs"][0]
        assert len(row["posterior"]) == 2
        assert row["baseline"]["risk"] == row["controls"]["H"]["expected_risk"] == [0, 1]
        assert row["channels"][0]["cells"][0]["posterior"] != row["posterior"]
        assert all(
            c["expected_risk"] == [0, 1] and c["retained_gain_fraction"] is None
            for c in row["channels"]
        )


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


def test_beliefs_and_history_weights_use_4096_not_rate_64_bit_bound(executors):
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
        assert all(c["gain_over_N"] == [0, 1] for c in a["aggregate"]["channels"])


def test_public_input_does_not_accept_noise_tuning_coin_flags_or_future_targets(executors):
    p = binary_problem()
    for key, value in (
        ("levels", [[0, 1], [1, 1]]),
        ("observed_coin", True),
        ("target", "future_report"),
        ("channels", []),
    ):
        for module in executors:
            with pytest.raises(ValueError):
                module.analyze({**p, key: value})


def test_non_topological_class_numbering_and_zero_mass_global_labels_remain_supported(executors):
    p = micro_problem("unequal")
    ids = {old: 3 - old for old in range(4)}
    reverse = copy.deepcopy(p)
    reverse["model"]["classes"] = [
        {
            **row,
            "class_id": ids[row["class_id"]],
            **{
                color: sorted(
                    [{**atom, "target_class": ids[atom["target_class"]]} for atom in row[color]],
                    key=lambda atom: atom["target_class"],
                )
                for color in ("odd", "even")
            },
        }
        for row in reversed(p["model"]["classes"])
    ]
    reverse["model"]["labels"] = [
        {**row, "class_id": ids[row["class_id"]]} for row in reversed(p["model"]["labels"])
    ]
    reverse["beliefs"][0]["posterior"] = sorted(
        [{**atom, "class_id": ids[atom["class_id"]]} for atom in p["beliefs"][0]["posterior"]],
        key=lambda atom: atom["class_id"],
    )
    for module in executors:
        a, b = module.analyze(p), module.analyze(reverse)
        assert a["aggregate"] == b["aggregate"] and a["channel_model"] == b["channel_model"]
        assert a["beliefs"][0]["baseline"] == b["beliefs"][0]["baseline"]
        assert any(fiber["N"][0] == 1 for fiber in a["channel_model"]["alphabet"])
        assert all(cell["value"][0] == 0 for cell in a["beliefs"][0]["channels"][0]["cells"])


def test_entire_output_is_detached_from_inputs_and_other_results_in_both_directions(executors):
    for module in executors:
        p = binary_problem()
        a, b = module.analyze(p), module.analyze(p)
        wanted, before = wire(b), wire(p)
        assert mutable_ids(a).isdisjoint(mutable_ids(p))
        assert mutable_ids(a).isdisjoint(mutable_ids(b))
        a["beliefs"][0]["posterior"][0]["probability"][0] = -1
        a["beliefs"][0]["channels"][1]["cells"][0]["value"][0] = 99
        a["channel_model"]["alphabet"][0]["values"][0][0] = 99
        a["aggregate"]["channels"][1]["gain_over_N"][0] = -1
        assert wire(p) == before and wire(b) == wanted and wire(module.analyze(p)) == wanted
        p["beliefs"][0]["posterior"][0]["probability"][0] = -9
        assert wire(b) == wanted
        with pytest.raises(ValueError):
            module.analyze(p)


def test_shared_inputs_are_legal_and_local_profile_reconstruction_is_used(executors, monkeypatch):
    for module in executors:
        p = micro_problem()
        empty = []
        for row in p["model"]["classes"]:
            for color in ("odd", "even"):
                if not row[color]:
                    row[color] = empty
        original, seen = module.reconstruct_profiles, []

        def delegated(payload, original=original, seen=seen):
            assert set(payload) == {"schema_version", "classes"}
            assert payload["schema_version"] == "det8-qr05s-local-v1"
            seen.append(wire(payload))
            return original(payload)

        with monkeypatch.context() as patched:
            patched.setattr(module, "reconstruct_profiles", delegated)
            result = module.analyze(p)
        assert seen and result["beliefs"][0]["controls"]["H"]["expected_risk"] == [1, 2]
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
        "CHANNEL_ATOM_CAP",
        "COMPOSITION_TERM_CAP",
        "COUPLING_CAP",
        "RECEIVING_CAP",
        "BIT_LIMIT",
    ],
)
def test_live_resource_and_derived_arithmetic_caps_fail_without_truncation(
    executors, monkeypatch, constant
):
    p = binary_problem()
    if constant == "BELIEF_CAP":
        p["beliefs"][0]["weight"] = [1, 2]
        p["beliefs"].append({**copy.deepcopy(p["beliefs"][0]), "belief_id": 1})
    if constant == "BIT_LIMIT":
        p = micro_problem()
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
        assert a["counts"]["beliefs"] == 512 and a["aggregate"]["baseline_risk"] == [0, 1]
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


def test_complete_runner_native_suite_raw_bridge_and_all_case_outputs(
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
    assert wire(runner.fixtures()) == wire(supplied)
    assert suite["independent_route_equal"] is True
    assert suite["raw_model"] == supplied["raw_model"] and suite["model"] == oracle.model
    for case, actual, (wanted, _) in zip(supplied["cases"], suite["cases"], expected, strict=True):
        assert wire(actual) == wire({**case, "analysis": wanted})
        assert runner.case_problem(supplied["model"], case) == problem_for(supplied["model"], case)
    bridge = suite["raw_bridge"]
    assert bridge["prior_artifact"] == "qr-05v-readout-value-2026-09-06/results.json"
    assert bridge["states"] == 4447 and bridge["classes"] == 416
    assert bridge["member_comparisons"] == 4447 - 416
    assert bridge["H_sha256"] == digest(oracle.partition)
    assert bridge["profiles_sha256"] == digest(oracle.profiles)
    assert bridge["fine_sha256"] == digest(oracle.fine)
    for name in (
        "all_raw_members_authenticated",
        "U_complete_case_evidence_recomputed",
        "V_complete_readout_evidence_recomputed",
        "raw_model_local_labels_beliefs_and_V_readouts_declared_dependencies",
    ):
        assert bridge[name] is True
    for name in (
        "U_V_native_API_calls_replayed",
        "source_aliases_regenerated",
        "T_minimality_P_consumer_R_helper_Q_certificate_replayed",
    ):
        assert bridge[name] is False
    audit = suite["rate_audit"]
    assert audit["all_raw_members_checked"] is True and len(audit["rates"]) == 2
    assert audit["raw_row_comparisons"] == 8894
    for row in audit["rates"]:
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
    assert totals["posterior_atoms"] == 1026 and totals["raw_rate_rows_checked"] == 8894
    for key in ("alphabet_fibers", "alphabet_values", "global_channel_atoms"):
        assert totals[key] == expected[0][0]["counts"][key]
    assert totals["composition_product_terms"] == sum(
        row["product_terms"] for row in expected[0][0]["channel_model"]["composition_checks"]
    )
    for count, keys in (
        (4, ("channel_cells", "channel_prediction_atoms", "strict_gain_beliefs")),
        (3, ("coupling_atoms", "receiving_checks", "strict_loss_beliefs")),
    ):
        for key in keys:
            assert totals[key] == [
                sum(a["counts"][key][i] for a, _ in expected) for i in range(count)
            ]
    assert totals["positive_oracle_residual_beliefs"] == sum(
        a["counts"]["positive_oracle_residual_beliefs"] for a, _ in expected
    )
    assert suite["public_controls"] == {
        "analyze_calls": 12,
        "invalid_analyze_calls_rejected": 14,
        "raw_orders_histories_or_artifacts_given_to_core": False,
        "intermediate_reports_or_noise_flags_given_to_forecaster": False,
    }


def output_mutations(a):
    return [
        (("model_sha256",), "0" * 64),
        (("kernel_sha256",), "0" * 64),
        (("reconstruction", "profile_atoms"), a["reconstruction"]["profile_atoms"] + 1),
        (("rate", 0), [1, 1]),
        (("channel_model", "alphabet", 0, "values"), []),
        (("channel_model", "channels", 1, "level"), [0, 1]),
        (("channel_model", "channels", 0, "rows", 0, "source", 0), -1),
        (("channel_model", "channels", 0, "rows", 0, "transitions", 0, "probability"), [1, 2]),
        (("channel_model", "composition_checks", 0, "product_terms"), 0),
        (("channel_model", "composition_checks", 0, "composed_sha256"), "0" * 64),
        (("beliefs", 0, "belief_id"), False),
        (("beliefs", 0, "weight"), [1, 1]),
        (("beliefs", 0, "baseline", "risk"), [1, 1]),
        (("beliefs", 0, "controls", "H", "expected_risk"), [1, 1]),
        (("beliefs", 0, "channels", 0, "gain_over_N"), [1, 1]),
        (("beliefs", 0, "channels", 0, "retained_gain_fraction"), [1, 1]),
        (("beliefs", 0, "channels", 0, "cells", 0, "posterior", 0, "probability"), [1, 2]),
        (("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "value", 0), -1),
        (("beliefs", 0, "channels", 0, "variance_gain"), [1, 1]),
        (("beliefs", 0, "garblings", 0, "couplings", 0, "probability"), [1, 2]),
        (("beliefs", 0, "garblings", 0, "couplings", 0, "later", 0), -1),
        (("beliefs", 0, "garblings", 0, "receiving_checks", 0, "earlier_values"), []),
        (
            ("beliefs", 0, "garblings", 0, "receiving_checks", 0, "posterior_mixture_sha256"),
            "0" * 64,
        ),
        (
            ("beliefs", 0, "garblings", 0, "receiving_checks", 0, "prediction_mixture_sha256"),
            "0" * 64,
        ),
        (
            ("beliefs", 0, "garblings", 0, "receiving_checks", 0, "conditional_risk_increase"),
            [1, 1],
        ),
        (
            ("beliefs", 0, "garblings", 0, "receiving_checks", 0, "conditional_variance_loss"),
            [1, 1],
        ),
        (("beliefs", 0, "garblings", 0, "zero_loss_iff_equal"), False),
        (("beliefs", 0, "checks", "N_already_known"), False),
        (("aggregate", "baseline_risk"), [1, 1]),
        (("aggregate", "channels", 0, "retained_gain_fraction"), [1, 1]),
        (("aggregate", "adjacent_risk_increase", 0), [1, 1]),
        (("witnesses", "first_strict_gain", 0), 0),
        (("witnesses", "first_zero_gain", 0), None),
        (("counts", "channel_cells", 0), 0),
        (("counts", "coupling_atoms", 0), 0),
        (("counts", "strict_gain_beliefs", 3), 1),
    ]


def test_raw_checker_rejects_channel_coupling_marginal_retention_and_witness_corruption(
    aggregate, supplied, expected
):
    runner, _ = aggregate
    model, case, wanted = supplied["raw_model"], supplied["cases"][0], expected[0][0]
    assert runner.check_analysis(wanted, model, case)["complete_native_output_equal"] is True
    before = wire(wanted)
    for path, value in output_mutations(wanted):
        bad = replaced(wanted, path, value)
        assert wire(bad) != before, path
        with pytest.raises(ValueError):
            runner.check_analysis(bad, model, case)
    assert wire(wanted) == before


def test_raw_checker_authenticates_both_U_and_V_producer_records_before_cache(
    aggregate, supplied, expected
):
    runner, _ = aggregate
    model, case, wanted = supplied["raw_model"], supplied["cases"][0], expected[0][0]
    report = runner.check_analysis(wanted, model, case)
    assert report["analysis_sha256"] == digest(wanted)
    for bad in (
        replaced(model, ("states", 0, "state_id"), IntChild(0)),
        replaced(model, ("states", 0, "frame_id"), False),
        {StrChild(key): value for key, value in model.items()},
    ):
        with pytest.raises(ValueError):
            runner.check_analysis(wanted, bad, case)
    for bad in (
        replaced(case, ("u_analysis", "histories", 0, "likelihood"), [1, 1]),
        replaced(case, ("u_analysis", "histories", 0, "posterior", 0, "class_id"), -1),
        replaced(case, ("v_analysis", "beliefs", 0, "belief_id"), False),
        replaced(case, ("v_analysis", "beliefs", 0, "baseline", "risk"), [1, 1]),
        replaced(case, ("v_analysis", "readout_maps", "NMT_to_N", 0, "coarse", 0), -1),
        replaced(case, ("rates", 2, 0), [1, 1]),
    ):
        with pytest.raises(ValueError):
            runner.check_analysis(wanted, model, bad)
    assert runner.check_analysis(wanted, model, case) == report


def test_runner_wire_guard_does_not_coerce_equal_native_values(aggregate):
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
spec = importlib.util.spec_from_file_location("_qr05w_guard_helpers", test_path)
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
for index, filename in enumerate(("noisy_readout.py", "reference_qr05w.py")):
    module = helpers.private_module("_qr05w_explicit_guard_" + str(index), filename)
    valid = helpers.micro_problem()
    reference = module.analyze(valid)
    require(reference["beliefs"][0]["baseline"]["risk"] == [1, 2], "true Brier baseline")
    require(reference["beliefs"][0]["controls"]["H"]["expected_risk"] == [1, 2], "fresh future uncertainty")
    require(all(channel["gain"] == [0, 1]
                for channel in reference["beliefs"][0]["channels"]),
            "equal future laws have no noisy-report gain")
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
    binary = helpers.binary_problem()
    binary_reference = module.analyze(binary)
    counts = binary_reference["counts"]
    workload_caps = (
        ("CHANNEL_ATOM_CAP", sum(counts["global_channel_atoms"]) - 1),
        ("COMPOSITION_TERM_CAP", sum(
            row["product_terms"]
            for row in binary_reference["channel_model"]["composition_checks"]
        ) - 1),
        ("COUPLING_CAP", sum(counts["coupling_atoms"]) - 1),
        ("RECEIVING_CAP", sum(counts["receiving_checks"]) - 1),
    )
    for constant, limit in workload_caps:
        original = getattr(module, constant)
        setattr(module, constant, limit)
        try:
            reject(module.analyze, binary)
        finally:
            setattr(module, constant, original)
        require(module.analyze(binary) == binary_reference,
                "restoring a workload cap did not restore the complete output")
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

runner = helpers.private_module("_qr05w_explicit_guard_runner", "study.py")
valid = helpers.micro_problem()
for bad in graph_inputs(valid):
    reject_before_dump(runner.require_wire, bad)
reject(lambda value: runner.require_same_wire({"zero": 0}, value, "typed wire"),
       {"zero": False})
require(before_serialization == 33, "pre-serialization rejection inventory")
expected = 2 * (len(invalid) + 2 + 11 + 8) + 11 + 1
require(rejections == expected, "explicit rejection inventory")
print(json.dumps({"rejections": rejections,
                  "invalid_fixture_cases": len(invalid),
                  "pre_serialization_rejections": before_serialization,
                  "optimized": bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05w.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=20, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    wanted = 2 * (len(invalid_problems()) + 2 + 11 + 8) + 11 + 1
    assert json.loads(result.stdout) == {
        "rejections": wanted,
        "invalid_fixture_cases": len(invalid_problems()),
        "pre_serialization_rejections": 33,
        "optimized": optimized,
    }
