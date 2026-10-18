"""Black-box full-output, analytical, physical, and rejection checks."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
NAMES = ("weak_phase", "grouped_dephase", "zero_link_boundary", "chain_boundary")
ZERO = [["0", "0"] for _ in range(4)]
EXPECTED_CLASSES = ((26, 29, 32), (26, 29, 32), (5, 5, 5), (8, 8, 8))


def problem(name="weak_phase"):
    return {"schema_version": "det8-qr05b-problem-v1", "case": name}


def private_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load test module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def modules():
    return (
        private_module("qr05b_test_direct", "summaries.py"),
        private_module("qr05b_test_reference", "reference_qr05b.py"),
    )


@pytest.fixture(scope="session")
def analyses(modules):
    return {name: tuple(m.analyze(problem(name)) for m in modules) for name in NAMES}


def summed(maps):
    values = list(maps)
    return [[str(sum((F(d[i][j]) for d in values), F(0))) for j in range(2)] for i in range(4)]


def decode(diag):
    return [(F(a), F(b)) for a, b in diag]


def cmul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def trace_probe(diag, bloch, effect):
    x, y, z = map(F, bloch)
    rho = [[((1 + z) / 2, F(0)), (x / 2, -y / 2)], [(x / 2, y / 2), ((1 - z) / 2, F(0))]]
    d = decode(diag)
    out = [[cmul(d[2 * i + j], rho[i][j]) for j in range(2)] for i in range(2)]
    effects = {
        "I": [[(1, 0), (0, 0)], [(0, 0), (1, 0)]],
        "P0": [[(1, 0), (0, 0)], [(0, 0), (0, 0)]],
        "P1": [[(0, 0), (0, 0)], [(0, 0), (1, 0)]],
        "P+X": [[(F(1, 2), 0), (F(1, 2), 0)], [(F(1, 2), 0), (F(1, 2), 0)]],
        "P+Y": [[(F(1, 2), 0), (0, F(-1, 2))], [(0, F(1, 2)), (F(1, 2), 0)]],
    }
    terms = [cmul(effects[effect][i][j], out[j][i]) for i in range(2) for j in range(2)]
    assert sum(v[1] for v in terms) == 0
    return sum(v[0] for v in terms)


@pytest.mark.parametrize("name", NAMES)
def test_complete_dual_output(analyses, name):
    direct, reference = analyses[name]
    assert direct == reference
    assert json.loads(json.dumps(direct, allow_nan=False)) == direct


@pytest.mark.parametrize("index,name", list(enumerate(NAMES)))
def test_class_ladder_and_zero_semantics(analyses, index, name):
    result = analyses[name][0]
    assert tuple(result["counts"]["family_classes"]) == EXPECTED_CLASSES[index]
    assert result["counts"]["continuation_blocks"] == 896
    assert len(result["birth_keys"]) == 16
    assert len(result["count_keys"]) == 5
    assert result["counts"]["decorated_classes"] == 32
    zeros = [i for i, h in enumerate(result["histories"]) if h["zero_source"]]
    assert len(zeros) == (48 if index >= 2 else 0)
    for family in result["families"]:
        assert sorted(i for g in family["classes"] for i in g) == list(range(56))
        assert family["refines_previous"] in (None, True)
        if zeros:
            assert zeros in family["classes"]
    if index < 2:
        assert result["families"][-1]["classes"] == result["candidates"][-1]["classes"]


@pytest.mark.parametrize("index,name", list(enumerate(NAMES)))
def test_candidate_sufficiency_contracts(analyses, index, name):
    result = analyses[name][0]
    valid = [[c["valid"] for c in f["candidate_checks"]] for f in result["families"]]
    if index < 2:
        assert valid == [
            [False, False, True, True, True],
            [False, False, False, True, True],
            [False, False, False, False, True],
        ]
    elif index == 2:
        assert valid == [[False, True, True, True, True]] * 3
    else:
        assert valid == [[False, False, True, True, True]] * 3
    for family in result["families"]:
        for check in family["candidate_checks"]:
            assert check["valid"] == (not check["conflicts"])
            assert check["conflicts"] == sorted(check["conflicts"])
            assert (check["first_witness"] is None) == check["valid"]


@pytest.mark.parametrize("name", NAMES)
def test_probability_not_state_is_preserved_by_nonselective_birth(analyses, name):
    result = analyses[name][0]
    changes = 0
    for row in result["histories"]:
        total = summed(row["next_birth"])
        assert (total[0], total[3]) == (row["source"][0], row["source"][3])
        changes += total != row["source"]
        if row["zero_source"]:
            assert row["source"] == ZERO and all(m == ZERO for m in row["next_birth"])
        for m in (row["source"], *row["next_birth"]):
            d = decode(m)
            assert d[0][1] == d[3][1] == 0
            assert d[1] == (d[2][0], -d[2][1])
            # Exact Choi positivity for diagonal Schur-multiplier maps.
            assert d[0][0] >= 0 and d[3][0] >= 0
            assert d[0][0] * d[3][0] >= d[1][0] ** 2 + d[1][1] ** 2
    assert changes > 0


@pytest.mark.parametrize("name", NAMES)
def test_all_retained_witnesses_are_physical_and_exact(analyses, name):
    result = analyses[name][0]
    for family in result["families"]:
        for check in family["candidate_checks"]:
            witness = check["first_witness"]
            if witness is None:
                continue
            assert witness["histories"] == check["conflicts"][0]
            bloch = witness["input_bloch"]
            assert sum(F(v) ** 2 for v in bloch) < 1
            found = []
            source_probs = []
            for h in witness["histories"]:
                row = result["histories"][h]
                source_probs.append(str(trace_probe(row["source"], bloch, "I")))
                if witness["probe"] == "payload":
                    m = row["source"]
                elif witness["probe"] == "order_counts":
                    m = row["source"] if row["counts"] == witness["outcome"] else ZERO
                else:
                    m = row["next_birth"][result["birth_keys"].index(witness["outcome"])]
                found.append(str(trace_probe(m, bloch, witness["effect"])))
            assert found == witness["joint_probabilities"] and found[0] != found[1]
            assert source_probs == witness["source_probabilities"]
            assert all(0 <= F(v) <= F(p) <= 1 for v, p in zip(found, source_probs, strict=True))


@pytest.mark.parametrize("name", NAMES[:2])
def test_fork_join_analytic_future_and_loss_of_record_correlation(analyses, name):
    result = analyses[name][0]
    fork_join = result["controls"]["fork_join"]
    assert fork_join["source_equal"] and not fork_join["counts_equal"]
    assert fork_join["source_live"] == [True, True]
    assert [[F(v) for v in d["size"]] for d in fork_join["distributions"]] == [
        [F(v, 125) for v in (27, 18, 60, 20)],
        [F(v, 125) for v in (27, 36, 12, 50)],
    ]
    location = result["controls"]["record_location"]
    assert location["source_equal"] and location["counts_equal"]
    a, b = location["distributions"]
    assert a["size"] == b["size"] and a["parity"] == b["parity"] == ["3/5", "2/5"]
    assert (a["joint"][1][1], b["joint"][1][1]) == ("0", "18/125")
    for control in (fork_join, location):
        for h, distribution in zip(control["histories"], control["distributions"], strict=True):
            row = result["histories"][h]
            probability = trace_probe(row["source"], ("0", "0", "0"), "I")
            assert probability > 0
            for m in range(4):
                for parity in range(2):
                    marginal = summed(
                        row["next_birth"][i]
                        for i, key in enumerate(result["birth_keys"])
                        if key[:2] == [m, parity]
                    )
                    value = trace_probe(marginal, ("0", "0", "0"), "I") / probability
                    assert value == F(distribution["joint"][m][parity])


@pytest.mark.parametrize("name", NAMES[2:])
def test_formal_boundary_controls_do_not_claim_conditional_predictions(analyses, name):
    for control in analyses[name][0]["controls"].values():
        assert control["source_live"] == [False, False]
        for distribution in control["distributions"]:
            assert sum(map(F, distribution["size"])) == 1


def test_grouped_dephasing_has_correct_coherence_factor(analyses):
    phase, dephase = analyses["weak_phase"][0], analyses["grouped_dephase"][0]
    factor = F(-7, 25)
    for a, b in zip(phase["histories"], dephase["histories"], strict=True):
        for map_a, map_b, exponent in [
            (a["source"], b["source"], 3),
            *((x, y, 4) for x, y in zip(a["next_birth"], b["next_birth"], strict=True)),
        ]:
            for i in range(4):
                for j in range(2):
                    assert F(map_b[i][j]) == F(map_a[i][j]) * (
                        factor**exponent if i in (1, 2) else 1
                    )


@pytest.mark.parametrize("index,name", list(enumerate(NAMES)))
def test_aggregation_multiplicities_and_negative_average(analyses, index, name):
    result = analyses[name][0]
    aggregate = result["aggregation"]
    assert aggregate["counts_equal"] and aggregate["totals_equal"]
    assert aggregate["direct_counts"] == aggregate["via_decorated_counts"]
    assert (
        aggregate["direct_total"]
        == aggregate["via_counts_total"]
        == aggregate["via_decorated_total"]
    )
    assert aggregate["direct_total"]["source"] == summed(
        row["source"] for row in result["histories"]
    )
    for key_index in range(16):
        assert aggregate["direct_total"]["birth"][key_index] == summed(
            row["next_birth"][key_index] for row in result["histories"]
        )
    assert aggregate["correct_trace"] == "1"
    assert aggregate["wrong_average_trace"] == ("44393/78125", "44393/78125", "337/625", "1")[index]
    assert sorted(i for row in aggregate["direct_counts"] for i in row["members"]) == list(
        range(56)
    )


INVALID = (
    None,
    [],
    True,
    {},
    {"case": "weak_phase"},
    {"schema_version": "det8-qr05b-problem-v1"},
    {**problem(), "extra": 1},
    {**problem(), "case": "parity_zx"},
    {**problem(), "case": True},
    {**problem(), "case": ["weak_phase"]},
    {**problem(), "case": None},
    {**problem(), "schema_version": "other"},
    {**problem(), "schema_version": 1},
    {**problem(), "schema_version": ["det8-qr05b-problem-v1"]},
)


@pytest.mark.parametrize("wire", INVALID)
def test_reject_invalid_fixed_inputs(modules, wire):
    for module in modules:
        with pytest.raises((ValueError, TypeError)):
            module.analyze(wire)


@pytest.mark.parametrize("index", [0, 1])
@pytest.mark.parametrize("kind", ["modified", "symlink"])
def test_prior_identity_rejected_before_analysis(modules, monkeypatch, tmp_path, index, kind):
    fake = tmp_path / "prior.json"
    target = tmp_path / "target.json"
    target.write_bytes(b"{}")
    if kind == "symlink":
        fake.symlink_to(target)
    else:
        fake.write_bytes(b"{}")
    monkeypatch.setattr(modules[index], "SOURCE" if index == 0 else "PRIOR", fake)
    with pytest.raises(ValueError):
        modules[index].analyze(problem())


@pytest.mark.parametrize("filename", ["summaries.py", "reference_qr05b.py"])
def test_optimized_rejection_subprocess(filename, tmp_path):
    script = """import importlib.util,json,sys
spec=importlib.util.spec_from_file_location('qr05b_optimized_boundary',sys.argv[1])
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for wire in json.loads(sys.argv[2]):
 try: m.analyze(wire)
 except (ValueError,TypeError): pass
 else: raise RuntimeError('invalid input accepted under optimization')
print('OPTIMIZED_REJECTIONS_PASS')
"""
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-O",
            "-X",
            f"pycache_prefix={tmp_path / 'cache'}",
            "-c",
            script,
            str(HERE / filename),
            json.dumps(INVALID),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "OPTIMIZED_REJECTIONS_PASS"
