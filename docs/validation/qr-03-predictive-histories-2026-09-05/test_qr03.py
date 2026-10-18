"""Independent finite fixtures for predictive-history equivalence, not study fixtures."""

import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, pairwise, product
from pathlib import Path
from types import SimpleNamespace

import predictive
import pytest
import reference_qr03

H = Fraction(1, 2)


def matrix(rows):
    result = []
    for row in rows:
        cells = []
        for value in row:
            real, imag = value if type(value) is tuple else (value, 0)
            cells.append([str(Fraction(real)), str(Fraction(imag))])
        result.append(cells)
    return result


I = matrix(((1, 0), (0, 1)))
Z = matrix(((1, 0), (0, -1)))
X = matrix(((0, 1), (1, 0)))
P0 = matrix(((1, 0), (0, 0)))
P1 = matrix(((0, 0), (0, 1)))
PX = (matrix(((H, H), (H, H))), matrix(((H, -H), (-H, H))))
PY = (matrix(((H, (0, -H)), ((0, H), H))), matrix(((H, (0, H)), ((0, -H), H))))
ZERO = matrix(((0, 0), (0, 0)))
MONOMIALS = [(i, j) for i in range(4) for j in range(i, 4)]
PROBES = [
    (0, 0, 0),
    (H, 0, 0),
    (-H, 0, 0),
    (0, H, 0),
    (0, -H, 0),
    (0, 0, H),
    (0, 0, -H),
    (H, H, 0),
    (H, 0, H),
    (0, H, H),
]


def weight(operator, amplitude):
    return [
        [[str(Fraction(real) * amplitude), str(Fraction(imag) * amplitude)] for real, imag in row]
        for row in operator
    ]


def instrument(outcomes):
    return {
        "support": [0],
        "outcomes": [{"label": label, "kraus": deepcopy(kraus)} for label, kraus in outcomes],
    }


def measurement(setting):
    labels, operators = (
        (("0", "1"), (P0, P1))
        if setting == "Z"
        else ((("+", "-"), PX) if setting == "X" else (("+", "-"), PY))
    )
    return instrument(tuple((label, [op]) for label, op in zip(labels, operators, strict=True)))


def event(name, inst, record=None):
    return {"event_id": name, "record_id": record or name, **deepcopy(inst)}


def source(events):
    return {
        "schema_version": "det8-qr01-problem-v1",
        "qubits": 1,
        "events": deepcopy(events),
        "precedence": [[a["event_id"], b["event_id"]] for a, b in pairwise(events)],
    }


def wire(events=None, settings=("X", "Y", "Z"), summary=None):
    events = events or [event("A", measurement("Z"))]
    records = sorted(
        [list(pair) for pair in sorted(zip([e["record_id"] for e in events], labels, strict=True))]
        for labels in product(*[[o["label"] for o in e["outcomes"]] for e in events])
    )
    return {
        "schema_version": "det8-qr03-problem-v1",
        "source": source(events),
        "schedule": [e["event_id"] for e in events],
        "futures": [
            {"setting": setting, "instrument": measurement(setting)} for setting in settings
        ],
        "summary": [
            {"record": record, "label": summary(record) if summary else "merged"}
            for record in records
        ],
    }


def coin_wire(*, phase=False, settings=("X", "Y", "Z"), summary=None):
    inst = instrument(
        (("a", [weight(I, Fraction(3, 5))]), ("b", [weight(Z if phase else I, Fraction(4, 5))]))
    )
    return wire([event("coin", inst)], settings, summary)


def two_stage(*, repeated=False, summary=None):
    events = [event("A", measurement("Z")), event("B", measurement("Z" if repeated else "X"))]
    return wire(events, summary=summary or (lambda record: dict(record)["B"]))


def zero_wire():
    return wire([event("A", instrument((("0", [I]), ("1", [ZERO]))))], ("Z",))


def record_key(record):
    return tuple(tuple(pair) for pair in record)


def histories(result):
    return {record_key(row["record"]): row for row in result["histories"]}


def numerators(history):
    return {(row["setting"], row["outcome"]): row["coefficients"] for row in history["numerators"]}


def dot(coefficients, coordinates):
    return sum(
        (Fraction(a) * b for a, b in zip(coefficients, coordinates, strict=True)), Fraction(0)
    )


def cross_coefficients(left_num, left_den, right_num, right_den):
    b, a, e, c = (list(map(Fraction, row)) for row in (left_num, left_den, right_num, right_den))
    return [
        str(
            b[i] * c[j] - e[i] * a[j]
            if i == j
            else b[i] * c[j] + b[j] * c[i] - e[i] * a[j] - e[j] * a[i]
        )
        for i, j in MONOMIALS
    ]


def polynomial(coefficients, coordinates):
    return sum(
        (
            Fraction(value) * coordinates[i] * coordinates[j]
            for value, (i, j) in zip(coefficients, MONOMIALS, strict=True)
        ),
        Fraction(0),
    )


@pytest.mark.parametrize(
    "problem,class_count,never_count,valid",
    [
        (coin_wire(), 1, 0, True),
        (coin_wire(phase=True, settings=("Z",)), 1, 0, True),
        (coin_wire(phase=True), 2, 0, False),
        (wire(settings=("X",)), 1, 0, True),
        (wire(), 2, 0, False),
        (two_stage(), 2, 0, True),
        (two_stage(repeated=True), 2, 2, True),
        (zero_wire(), 1, 1, True),
    ],
    ids=[
        "coin",
        "phase-Z",
        "phase-tomography",
        "Z-X-only",
        "Z-tomography",
        "last-X",
        "last-Z-zeros",
        "zero-branch",
    ],
)
def test_full_results_match_independent_reference(problem, class_count, never_count, valid):
    actual = predictive.analyze(problem)
    assert actual == reference_qr03.analyze(problem)
    assert actual["basis"] == ["P0", "P1", "X", "Y"]
    assert actual["monomials"] == [list(pair) for pair in MONOMIALS]
    assert len(actual["classes"]) == class_count
    assert len(actual["never_possible"]) == never_count
    assert actual["candidate_valid"] is valid


@pytest.mark.parametrize(
    "problem",
    [
        coin_wire(phase=True),
        wire(),
        two_stage(),
        two_stage(repeated=True, summary=lambda record: "all"),
    ],
)
def test_pair_polynomials_and_physical_witnesses_independently(problem):
    result = predictive.analyze(problem)
    by_record = histories(result)
    live = [key for key, row in by_record.items() if row["status"] == "POSSIBLE"]
    assert len(result["pairs"]) == len(live) * (len(live) - 1) // 2
    assert {(record_key(row["left"]), record_key(row["right"])) for row in result["pairs"]} == set(
        combinations(live, 2)
    )
    for pair in result["pairs"]:
        left, right = by_record[record_key(pair["left"])], by_record[record_key(pair["right"])]
        left_nums, right_nums = numerators(left), numerators(right)
        zero = True
        for question in pair["questions"]:
            question_key = question["setting"], question["outcome"]
            expected = cross_coefficients(
                left_nums[question_key],
                left["denominator"],
                right_nums[question_key],
                right["denominator"],
            )
            assert question["coefficients"] == expected
            zero = zero and all(value == "0" for value in expected)
            for coefficient in expected:
                assert str(Fraction(coefficient)) == coefficient
        assert pair["equal"] is zero
        witness = pair["witness"]
        if pair["equal"]:
            assert witness is None
            continue
        assert witness is not None
        x, y, z = map(Fraction, witness["bloch"])
        assert (x, y, z) in PROBES
        assert x * x + y * y + z * z < 1
        expected_density = matrix((((1 + z) / 2, (x / 2, -y / 2)), ((x / 2, y / 2), (1 - z) / 2)))
        assert witness["density"] == expected_density
        coordinates = ((1 + z) / 2, (1 - z) / 2, x / 2, y / 2)
        dl, dr = dot(left["denominator"], coordinates), dot(right["denominator"], coordinates)
        question_key = witness["setting"], witness["outcome"]
        pl, pr = (
            dot(left_nums[question_key], coordinates) / dl,
            dot(right_nums[question_key], coordinates) / dr,
        )
        assert 0 < dl <= 1 and 0 < dr <= 1
        assert 0 <= pl <= 1 and 0 <= pr <= 1 and pl != pr
        assert witness["left_history_probability"] == str(dl)
        assert witness["right_history_probability"] == str(dr)
        assert witness["left_conditional"] == str(pl)
        assert witness["right_conditional"] == str(pr)
        assert witness["delta"] == str(pl - pr)


def test_unequal_raw_coin_weights_have_identical_conditional_predictions():
    result = predictive.analyze(coin_wire())
    left, right = result["histories"]
    assert left["denominator"] == ["9/25", "9/25", "0", "0"]
    assert right["denominator"] == ["16/25", "16/25", "0", "0"]
    assert numerators(left)[("Z", "0")] == ["9/25", "0", "0", "0"]
    assert numerators(right)[("Z", "0")] == ["16/25", "0", "0", "0"]
    assert result["pairs"][0]["equal"]
    assert len(result["classes"]) == 1


def test_complex_y_functional_has_the_correct_phase_sign():
    result = predictive.analyze(coin_wire(phase=True))
    left, right = result["histories"]
    assert numerators(left)[("Y", "+")] == ["9/50", "9/50", "0", "9/25"]
    assert numerators(right)[("Y", "+")] == ["8/25", "8/25", "0", "-16/25"]


def test_four_nonzero_equivalent_histories_form_one_transitive_maximal_class():
    coin = instrument((("a", [weight(I, Fraction(3, 5))]), ("b", [weight(I, Fraction(4, 5))])))
    problem = wire([event("A", coin), event("B", coin)])
    result = predictive.analyze(problem)
    assert result == reference_qr03.analyze(problem)
    assert len(result["pairs"]) == 6
    assert all(pair["equal"] for pair in result["pairs"])
    assert len(result["classes"]) == 1 and len(result["classes"][0]) == 4
    assert result["never_possible"] == []


def test_multi_kraus_source_maps_are_summed_incoherently():
    dephase = instrument((("all", [P0, P1]),))
    coin = instrument((("a", [weight(I, Fraction(3, 5))]), ("b", [weight(I, Fraction(4, 5))])))
    problem = wire([event("A", dephase), event("B", coin)])
    result = predictive.analyze(problem)
    assert result == reference_qr03.analyze(problem)
    assert len(result["classes"]) == 1
    left = result["histories"][0]
    assert numerators(left)[("X", "+")] == ["9/50", "9/50", "0", "0"]
    plus_coordinates = (H, H, H, 0)
    assert (
        dot(numerators(left)[("X", "+")], plus_coordinates)
        / dot(left["denominator"], plus_coordinates)
        == H
    )


def test_canonical_result_is_independent_of_table_and_input_inventory_order():
    original = two_stage()
    changed = deepcopy(original)
    changed["source"]["events"].reverse()
    for source_event in changed["source"]["events"]:
        source_event["outcomes"].reverse()
    changed["futures"].reverse()
    changed["summary"].reverse()
    assert predictive.analyze(original) == predictive.analyze(changed)
    assert reference_qr03.analyze(original) == reference_qr03.analyze(changed)


def test_selected_maximally_mixed_state_is_not_an_all_state_certificate():
    result = predictive.analyze(coin_wire(phase=True))
    left, right = result["histories"]
    mixed_coordinates = (H, H, 0, 0)
    for question, left_num in numerators(left).items():
        assert dot(left_num, mixed_coordinates) / dot(
            left["denominator"], mixed_coordinates
        ) == dot(numerators(right)[question], mixed_coordinates) / dot(
            right["denominator"], mixed_coordinates
        )
    assert len(result["classes"]) == 2
    assert not result["candidate_valid"]
    assert result["pairs"][0]["witness"] is not None


def test_input_specific_zero_probability_does_not_remove_a_live_history():
    result = predictive.analyze(wire())
    by_record = histories(result)
    one = by_record[(("A", "1"),)]
    assert one["status"] == "POSSIBLE"
    assert dot(one["denominator"], (1, 0, 0, 0)) == 0
    assert dot(one["denominator"], (H, H, 0, 0)) > 0
    assert result["never_possible"] == []
    assert len(result["classes"]) == 2


def test_zero_histories_never_form_wildcard_links_between_distinct_classes():
    problem = two_stage(repeated=True, summary=lambda record: "all")
    result = predictive.analyze(problem)
    assert len(result["histories"]) == 4
    assert len(result["never_possible"]) == 2
    assert len(result["pairs"]) == 1
    assert not result["pairs"][0]["equal"]
    assert len(result["classes"]) == 2
    assert not result["candidate_valid"]
    assert len(result["candidate_conflicts"]) == 1
    live_records = {record_key(record) for group in result["classes"] for record in group}
    assert not live_records.intersection(map(record_key, result["never_possible"]))
    for record in result["never_possible"]:
        row = histories(result)[record_key(record)]
        assert row["status"] == "NEVER_POSSIBLE"
        assert row["denominator"] == ["0"] * 4


def test_last_record_suffices_but_distinct_earlier_probabilities_are_retained():
    result = predictive.analyze(two_stage())
    assert len(result["classes"]) == 2
    for group in result["classes"]:
        assert len(group) == 2
        assert len({dict(record)["B"] for record in group}) == 1
        assert {dict(record)["A"] for record in group} == {"0", "1"}
    by_record = histories(result)
    left = by_record[(("A", "0"), ("B", "+"))]
    right = by_record[(("A", "1"), ("B", "+"))]
    assert left["denominator"] == ["1/2", "0", "0", "0"]
    assert right["denominator"] == ["0", "1/2", "0", "0"]
    assert result["candidate_valid"]


def partition_pairs(result):
    return {
        frozenset((record_key(a), record_key(b)))
        for group in result["classes"]
        for a, b in combinations(group, 2)
    }


@pytest.mark.parametrize("source_kind", ["phase", "projective"])
def test_expanding_future_family_strictly_refines_and_never_merges(source_kind):
    if source_kind == "phase":
        small = coin_wire(phase=True, settings=("Z",))
        large = coin_wire(phase=True)
    else:
        small, large = wire(settings=("X",)), wire()
    small_result, large_result = predictive.analyze(small), predictive.analyze(large)
    assert partition_pairs(large_result) < partition_pairs(small_result)
    assert len(small_result["classes"]) == 1 and len(large_result["classes"]) == 2


def test_candidate_partition_is_checked_without_changing_the_maximal_partition():
    merged = predictive.analyze(coin_wire())
    finer = predictive.analyze(coin_wire(summary=lambda record: dict(record)["coin"]))
    assert merged["classes"] == finer["classes"]
    assert merged["candidate_valid"] and finer["candidate_valid"]
    assert merged["candidate_conflicts"] == finer["candidate_conflicts"] == []
    bad = predictive.analyze(wire())
    assert bad["candidate_conflicts"] == [{**bad["pairs"][0], "label": "merged"}]


def test_homogeneous_polynomial_scaling_preserves_the_trace_one_argument():
    result = predictive.analyze(coin_wire(phase=True))
    coordinate = (Fraction(3, 5), Fraction(2, 5), Fraction(1, 5), Fraction(1, 10))
    assert coordinate[0] + coordinate[1] == 1
    # This is positive definite: rho00*rho11 > |rho01|².
    assert coordinate[0] * coordinate[1] > coordinate[2] ** 2 + coordinate[3] ** 2
    nonzero_seen = False
    for question in result["pairs"][0]["questions"]:
        value = polynomial(question["coefficients"], coordinate)
        doubled = polynomial(question["coefficients"], tuple(2 * t for t in coordinate))
        assert doubled == 4 * value
        nonzero_seen = nonzero_seen or value != 0
    assert nonzero_seen


def test_ten_full_rank_probe_points_determine_all_quadratics():
    rows = []
    for x, y, z in PROBES:
        assert x * x + y * y + z * z < 1
        rows.append(list(map(Fraction, (1, x, y, z, x * x, y * y, z * z, x * y, x * z, y * z))))
    rank = 0
    for column in range(10):
        pivot = next((i for i in range(rank, 10) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        divisor = rows[rank][column]
        rows[rank] = [entry / divisor for entry in rows[rank]]
        for i in range(10):
            if i != rank:
                factor = rows[i][column]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[rank], strict=True)]
        rank += 1
    assert rank == 10


def test_uninformative_single_outcome_questions_do_not_certify_state_equality():
    problem = wire(settings=("Z",))
    problem["futures"][0]["instrument"] = instrument((("done", [X]),))
    result = predictive.analyze(problem)
    assert len(result["classes"]) == 1
    assert result["candidate_valid"]
    for history in result["histories"]:
        assert history["numerators"][0]["coefficients"] == history["denominator"]


def mutate(problem, path, value):
    result = deepcopy(problem)
    target = result
    for item in path[:-1]:
        target = target[item]
    target[path[-1]] = deepcopy(value)
    return result


@pytest.mark.parametrize(
    "path,value",
    [
        (("schema_version",), "unknown"),
        (("extra",), True),
        (("source", "qubits"), 2),
        (("source", "qubits"), True),
        (("source", "events"), []),
        (("schedule",), []),
        (("schedule",), ["missing"]),
        (("schedule",), ["A", "A"]),
        (("futures",), []),
        (("futures", 0, "setting"), "bad setting"),
        (("futures", 0, "callback"), True),
        (("futures", 0, "instrument", "support"), [True]),
        (("futures", 0, "instrument", "support"), [1]),
        (("futures", 0, "instrument", "outcomes"), []),
        (("summary",), []),
        (("summary", 0, "label"), "bad/label"),
        (("summary", 0, "record"), [["unknown", "0"]]),
        (("summary", 0, "record"), [["A", "unknown"]]),
        (("summary", 0, "record"), [["A", "0"], ["A", "0"]]),
        (("summary", 0, "extra"), True),
    ],
)
def test_strict_schema_invalids_fail_in_both_paths(path, value):
    bad = mutate(wire(), path, value)
    with pytest.raises(ValueError):
        predictive.analyze(bad)
    with pytest.raises(ValueError):
        reference_qr03.analyze(bad)


@pytest.mark.parametrize(
    "token", [True, 0.5, "01", "1/1", "NaN", "1e999999999", "1e-999999999", str(2**64), "1" * 257]
)
def test_bounded_rational_cells_fail_before_unbounded_conversion(token):
    bad = mutate(wire(), ("source", "events", 0, "outcomes", 0, "kraus", 0, 0, 0, 0), token)
    with pytest.raises(ValueError):
        predictive.analyze(bad)
    with pytest.raises(ValueError):
        reference_qr03.analyze(bad)


@pytest.mark.parametrize(
    "change",
    [
        "duplicate-setting",
        "four-settings",
        "duplicate-record",
        "missing-zero",
        "unsorted-record",
        "three-events",
        "bad-order",
    ],
)
def test_global_contract_rejections(change):
    bad = two_stage(repeated=True)
    if change == "duplicate-setting":
        bad["futures"][1]["setting"] = bad["futures"][0]["setting"]
    elif change == "four-settings":
        bad["futures"].append({"setting": "extra", "instrument": measurement("Z")})
    elif change == "duplicate-record":
        bad["summary"][1]["record"] = deepcopy(bad["summary"][0]["record"])
    elif change == "missing-zero":
        bad["summary"] = [
            item for item in bad["summary"] if dict(item["record"]) != {"A": "0", "B": "1"}
        ]
    elif change == "unsorted-record":
        bad["summary"][0]["record"].reverse()
    elif change == "three-events":
        bad["source"]["events"].append(event("C", measurement("Z")))
        bad["schedule"].append("C")
    elif change == "bad-order":
        bad["schedule"].reverse()
    with pytest.raises(ValueError):
        predictive.analyze(bad)
    with pytest.raises(ValueError):
        reference_qr03.analyze(bad)


def test_incomplete_future_is_not_a_probability_question():
    bad = wire()
    bad["futures"][0]["instrument"]["outcomes"] = bad["futures"][0]["instrument"]["outcomes"][:1]
    with pytest.raises(ValueError):
        predictive.analyze(bad)
    with pytest.raises(ValueError):
        reference_qr03.analyze(bad)


def test_frozen_qr01_dependency_bytes_are_reused_without_mutation():
    prior = Path(__file__).resolve().parent.parent / "qr-01-quantum-records-2026-09-05"
    expected = {
        "exact.py": "4238096b5de4b6aeeee2559b5200e0458a5635be88c06aa960bd50d0c2e3db56",
        "reference.py": "d7fab84717c22632e8be7cfd18aca68d439cbf611cf3a47a11abf25a8fca856f",
    }
    assert Path(predictive.ex.__file__).resolve() == (prior / "exact.py").resolve()
    for name, expected_hash in expected.items():
        assert hashlib.sha256((prior / name).read_bytes()).hexdigest() == expected_hash


def test_pinned_loader_rejects_changed_source_before_execution(monkeypatch):
    fake = SimpleNamespace(
        is_file=lambda: True,
        is_symlink=lambda: False,
        read_bytes=lambda: b"raise RuntimeError('must not execute')",
    )
    monkeypatch.setattr(predictive, "BASE_PATH", fake)
    with pytest.raises(ValueError, match="differs from pinned bytes"):
        predictive._load_exact()


def test_pinned_loader_rejects_even_a_path_spoofed_cached_module(monkeypatch):
    fake = SimpleNamespace(__file__=str(predictive.BASE_PATH))
    monkeypatch.setitem(sys.modules, "qr03_pinned_exact", fake)
    with pytest.raises(ValueError, match="private module name collision"):
        predictive._load_exact()


def test_validation_remains_active_under_optimized_python():
    bad = wire()
    bad["source"]["events"][0]["outcomes"] = bad["source"]["events"][0]["outcomes"][:1]
    script = """
import json, sys
sys.path.insert(0, sys.argv[1])
import predictive, reference_qr03
wire = json.loads(sys.argv[2])
for check in (lambda: predictive.analyze(wire), lambda: reference_qr03.analyze(wire)):
    try:
        check()
    except ValueError:
        continue
    raise SystemExit('incomplete source accepted under -O')
print('both QR-03 paths reject under -O')
"""
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-O",
            "-B",
            "-c",
            script,
            str(Path(__file__).parent),
            json.dumps(bad),
        ],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert result.stdout.strip() == "both QR-03 paths reject under -O"


class MemoryResult:
    """Only an in-memory artifact; these tests cannot create retained results."""

    def __init__(self, raw):
        self.raw = raw

    def exists(self):
        return True

    def is_file(self):
        return True

    def is_symlink(self):
        return False

    def read_bytes(self):
        return self.raw

    def open(self, *args, **kwargs):
        raise AssertionError("artifact test attempted an actual result write")


def artifact_harness(monkeypatch, *, verify=True):
    # A unique module name keeps combined QR-01/02/03 test collection from
    # accidentally retrieving some other directory's cached top-level study.
    name = "qr03_artifact_test_study"
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("study.py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the specific QR-03 artifact runner")
    study = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, study)
    spec.loader.exec_module(study)
    ledger = {"source": {"bytes": 1, "sha256": "source-identity"}}
    priors = {
        "qr01": {"bytes": 2, "sha256": "prior-01-identity"},
        "qr02": {"bytes": 3, "sha256": "prior-02-identity"},
    }
    suite = {"totals": {"tiny_fake_cases": 1}, "exact_coefficient": "1/2"}
    result = MemoryResult(
        study.canonical(
            {
                "schema_version": "det8-qr03-results-v1",
                "source_ledger": ledger,
                "prior_artifacts": priors,
                "suite": suite,
            }
        )
    )
    monkeypatch.setattr(study, "RESULT", result)
    monkeypatch.setattr(study, "source_ledger", lambda: deepcopy(ledger))
    monkeypatch.setattr(study, "prior_identity", lambda: deepcopy(priors))
    monkeypatch.setattr(study, "run_suite", lambda: deepcopy(suite))
    monkeypatch.setattr(
        study,
        "sys",
        SimpleNamespace(
            flags=SimpleNamespace(isolated=1, optimize=0),
            pycache_prefix="/tmp/det8-qr03-test-cache-never-created",
        ),
    )
    monkeypatch.setattr(sys, "argv", ["study.py", *(["--verify"] if verify else [])])
    return study, result, ledger, priors, suite


def test_artifact_replay_rejects_concurrent_byte_replacement(monkeypatch):
    study, result, _, _, suite = artifact_harness(monkeypatch)

    def replace_during_run():
        result.raw += b" "  # JSON-equivalent replacement must still fail byte identity.
        return deepcopy(suite)

    monkeypatch.setattr(study, "run_suite", replace_during_run)
    with pytest.raises(ValueError, match="result changed during replay"):
        study.main()


@pytest.mark.parametrize("identity", ["source", "qr01", "qr02"])
def test_artifact_replay_rejects_source_or_either_prior_drift(monkeypatch, identity):
    study, _, ledger, priors, suite = artifact_harness(monkeypatch)

    def change_during_run():
        if identity == "source":
            ledger["source"]["sha256"] = "changed-source"
        else:
            priors[identity]["sha256"] = "changed-prior"
        return deepcopy(suite)

    monkeypatch.setattr(study, "run_suite", change_during_run)
    with pytest.raises(ValueError, match="source/prior changed during execution"):
        study.main()


def test_artifact_replay_rejects_coefficient_or_suite_mismatch(monkeypatch):
    study, _, _, _, suite = artifact_harness(monkeypatch)
    changed = deepcopy(suite)
    changed["exact_coefficient"] = "2/3"
    monkeypatch.setattr(study, "run_suite", lambda: changed)
    with pytest.raises(ValueError, match="exact replay differs"):
        study.main()


def test_artifact_capture_is_create_only_before_any_computation(monkeypatch):
    study, _, _, _, _ = artifact_harness(monkeypatch, verify=False)

    def forbidden_work():
        raise AssertionError("existing artifact must be refused before computation")

    monkeypatch.setattr(study, "source_ledger", forbidden_work)
    monkeypatch.setattr(study, "prior_identity", forbidden_work)
    monkeypatch.setattr(study, "run_suite", forbidden_work)
    with pytest.raises(FileExistsError, match="results.json already exists"):
        study.main()


def test_artifact_replay_hashes_the_exact_verified_bytes(monkeypatch, capsys):
    study, result, _, _, suite = artifact_harness(monkeypatch)
    original = result.raw
    study.main()
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "VERIFIED_EXACT_REPLAY"
    assert report["result_sha256"] == study.digest(original)
    assert report["totals"] == suite["totals"]
    assert result.raw == original
