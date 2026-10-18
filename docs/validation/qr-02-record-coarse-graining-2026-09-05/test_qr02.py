"""QR-02 independent fixtures and adversarial contracts; no study fixtures.

The exact source/reference reuse is itself checked against the frozen QR-01
artifact identity. These are finite mathematical tests, not empirical evidence.
"""

import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import coarse
import pytest
import reference_qr02

H = Fraction(1, 2)


def matrix(rows):
    output = []
    for row in rows:
        cells = []
        for value in row:
            real, imag = value if type(value) is tuple else (value, 0)
            cells.append([str(Fraction(real)), str(Fraction(imag))])
        output.append(cells)
    return output


I = matrix(((1, 0), (0, 1)))
X = matrix(((0, 1), (1, 0)))
Z = matrix(((1, 0), (0, -1)))
S = matrix(((1, 0), (0, (0, 1))))
P0 = matrix(((1, 0), (0, 0)))
P1 = matrix(((0, 0), (0, 1)))
RESET1 = matrix(((0, 1), (0, 0)))
PX = (matrix(((H, H), (H, H))), matrix(((H, -H), (-H, H))))
PY = (matrix(((H, (0, -H)), ((0, H), H))), matrix(((H, (0, H)), ((0, -H), H))))
ZERO = matrix(((0, 0), (0, 0)))


def weighted(operator, amplitude):
    return [
        [[str(Fraction(real) * amplitude), str(Fraction(imag) * amplitude)] for real, imag in row]
        for row in operator
    ]


def embed(operator, qubit):
    result = []
    for row in range(4):
        output_row = []
        for column in range(4):
            row_bits = (row // 2, row % 2)
            col_bits = (column // 2, column % 2)
            output_row.append(
                deepcopy(operator[row_bits[qubit]][col_bits[qubit]])
                if row_bits[1 - qubit] == col_bits[1 - qubit]
                else ["0", "0"]
            )
        result.append(output_row)
    return result


def instrument(outcomes, support=(0,)):
    return {
        "support": list(support),
        "outcomes": [
            {"label": label, "kraus": deepcopy(operators)} for label, operators in outcomes
        ],
    }


def unitary(operator=I, support=(0,)):
    return instrument((("done", [operator]),), support)


def measure(operators=(P0, P1), labels=("0", "1"), support=(0,)):
    return instrument(
        tuple((label, [operator]) for label, operator in zip(labels, operators, strict=True)),
        support,
    )


def wire(source=None, fine=None, candidate=None, groups=None, qubits=1):
    source = source or measure()
    labels = [item["label"] for item in source["outcomes"]]
    groups = groups or {label: "all" for label in labels}
    fine = fine or {label: unitary() for label in labels}
    candidate = candidate or {label: unitary() for label in set(groups.values())}
    return {
        "schema_version": "det8-qr02-problem-v1",
        "qubits": qubits,
        "source": deepcopy(source),
        "groups": [{"fine": label, "coarse": value} for label, value in groups.items()],
        "fine_future": [
            {"fine": label, "instrument": deepcopy(value)} for label, value in fine.items()
        ],
        "coarse_future": [
            {"coarse": label, "instrument": deepcopy(value)} for label, value in candidate.items()
        ],
    }


def controlled_wire(*, erased=False, repair=False):
    source = measure((P0, RESET1)) if erased else measure()
    fine = {"0": unitary(), "1": unitary(X)}
    replacement = instrument((("done", [P0, RESET1]),)) if repair else unitary()
    return wire(source, fine, {"all": replacement})


def coin_wire():
    source = instrument(
        (("a", [weighted(I, Fraction(3, 5))]), ("b", [weighted(I, Fraction(4, 5))])), ()
    )
    replacement = instrument(
        (("done", [weighted(I, Fraction(3, 5)), weighted(S, Fraction(4, 5))]),)
    )
    return wire(source, {"a": unitary(), "b": unitary(S)}, {"all": replacement})


def multikraus_wire():
    source = instrument(
        (
            ("a", [weighted(P0, Fraction(3, 5)), weighted(P1, Fraction(3, 5))]),
            ("b", [weighted(P0, Fraction(4, 5)), weighted(P1, Fraction(4, 5))]),
        )
    )
    future = measure(PY, ("+", "-"))
    return wire(source, {"a": future, "b": future}, {"all": future})


def local_wire():
    source = measure((embed(P0, 0), embed(P1, 0)), support=(0,))
    future = measure((embed(PY[0], 1), embed(PY[1], 1)), ("+", "-"), (1,))
    return wire(source, {"0": future, "1": future}, {"all": future}, qubits=2)


def no_merge_wire():
    return wire(
        fine={"0": unitary(), "1": unitary(X)},
        candidate={"left": unitary(), "right": unitary(X)},
        groups={"0": "left", "1": "right"},
    )


def zero_wire():
    return wire(
        instrument((("0", [ZERO]), ("1", [I]))),
        {"0": unitary(X), "1": unitary()},
        {"all": unitary()},
    )


def pair_matrix(value):
    return tuple(tuple((cell.real, cell.imag) for cell in row) for row in value)


def pair_bundles(bundles):
    return {
        name: {key: pair_matrix(value) for key, value in blocks.items()}
        for name, blocks in bundles.items()
    }


def equal_routes(bundle):
    return (
        bundle["fine_then_forget"] == bundle["forget_then_candidate"],
        bundle["unrestricted_fine_future"] == bundle["unrestricted_coarse_future"],
    )


def state_bundles(problem, operator):
    parsed = coarse.parse(problem)
    return coarse.propagate(parsed, coarse.ex.decode_matrix(operator, parsed.dimension))


@pytest.mark.parametrize(
    "problem,expected",
    [
        (wire(), (True, True)),
        (controlled_wire(), (False, False)),
        (controlled_wire(repair=True), (True, False)),
        (controlled_wire(erased=True), (False, False)),
        (coin_wire(), (True, False)),
        (multikraus_wire(), (True, True)),
        (no_merge_wire(), (True, True)),
        (zero_wire(), (True, False)),
        (local_wire(), (True, True)),
    ],
    ids=[
        "common-future",
        "bad-candidate",
        "reachable-repair",
        "true-erasure",
        "averaged-coin",
        "four-term-group",
        "no-merge",
        "zero-unreachable",
        "two-qubit-complex",
    ],
)
def test_every_full_bundle_matches_independent_reference(problem, expected):
    observed = coarse.maps(problem)
    assert set(observed) == {
        "source_fine",
        "source_coarse",
        "fine_then_forget",
        "forget_then_candidate",
        "unrestricted_fine_future",
        "unrestricted_coarse_future",
    }
    assert pair_bundles(observed) == reference_qr02.reference_maps(problem)
    assert equal_routes(observed) == expected


def test_bad_candidate_does_not_mean_no_physical_replacement_exists():
    bad = coarse.maps(controlled_wire())
    repaired = coarse.maps(controlled_wire(repair=True))
    assert bad["fine_then_forget"] == repaired["fine_then_forget"]
    assert bad["source_coarse"] == repaired["source_coarse"]
    assert equal_routes(bad) == (False, False)
    assert equal_routes(repaired) == (True, False)


def test_true_lost_record_collision_blocks_every_coarse_only_replacement():
    problem = controlled_wire(erased=True)
    from_zero = state_bundles(problem, P0)
    from_one = state_bundles(problem, P1)
    # A deterministic function of identical available inputs cannot return both
    # different required outputs. This is stronger than candidate failure.
    assert from_zero["source_coarse"] == from_one["source_coarse"]
    assert from_zero["fine_then_forget"] != from_one["fine_then_forget"]
    key = (("coarse", "all"), ("future", "done"))
    assert from_zero["fine_then_forget"][key] == coarse.ex.decode_matrix(P0, 2)
    assert from_one["fine_then_forget"][key] == coarse.ex.decode_matrix(P1, 2)


def test_fixed_coin_average_works_only_after_aggregation_of_reachable_blocks():
    problem = coin_wire()
    observed = coarse.maps(problem)
    assert equal_routes(observed) == (True, False)
    branches = state_bundles(problem, PX[0])
    coarse_state = branches["source_coarse"][(("coarse", "all"),)]
    assert coarse_state == coarse.ex.decode_matrix(PX[0], 2)
    expected = matrix(
        ((H, (Fraction(9, 50), Fraction(-8, 25))), ((Fraction(9, 50), Fraction(8, 25)), H))
    )
    key = (("coarse", "all"), ("future", "done"))
    assert branches["fine_then_forget"][key] == coarse.ex.decode_matrix(expected, 2)


def test_grouping_four_kraus_terms_is_not_rejected_or_coherently_combined():
    problem = multikraus_wire()
    parsed = coarse.parse(problem)
    operator = coarse.ex.decode_matrix(matrix(((0, 1), (0, 0))), 2)
    blocks = coarse.propagate(parsed, operator)
    assert len(problem["source"]["outcomes"]) == 2
    assert sum(len(item["kraus"]) for item in problem["source"]["outcomes"]) == 4
    assert blocks["source_coarse"][(("coarse", "all"),)] == coarse.ex.zeros(2)
    plus = state_bundles(problem, PX[0])
    assert plus["source_coarse"][(("coarse", "all"),)] == coarse.ex.scale(
        coarse.ex.identity(2), coarse.ex.q(H)
    )


def test_forgetting_classical_record_is_not_coherent_recombination():
    future = measure(PX, ("+", "-"))
    problem = wire(fine={"0": future, "1": future}, candidate={"all": future})
    blocks = state_bundles(problem, PX[0])
    plus_key = (("coarse", "all"), ("future", "+"))
    assert coarse.ex.trace(blocks["fine_then_forget"][plus_key]) == coarse.ex.q(H)
    assert blocks["source_coarse"][(("coarse", "all"),)] != coarse.ex.decode_matrix(PX[0], 2)
    # Coherently adding P0+P1 would instead be identity, leaving X+ probability one.
    assert coarse.ex.add(
        coarse.ex.decode_matrix(P0, 2), coarse.ex.decode_matrix(P1, 2)
    ) == coarse.ex.identity(2)


def test_coarse_record_probabilities_do_not_replace_quantum_output():
    problem = wire(fine={"0": measure(), "1": measure()}, candidate={"all": measure()})
    zero = state_bundles(problem, P0)
    one = state_bundles(problem, P1)
    coarse_key = (("coarse", "all"),)
    assert coarse.ex.trace(zero["source_coarse"][coarse_key]) == coarse.ex.q(1)
    assert coarse.ex.trace(one["source_coarse"][coarse_key]) == coarse.ex.q(1)
    assert zero["source_coarse"] != one["source_coarse"]
    future_key = (("coarse", "all"), ("future", "0"))
    assert coarse.ex.trace(zero["fine_then_forget"][future_key]) == coarse.ex.q(1)
    assert coarse.ex.trace(one["fine_then_forget"][future_key]) == coarse.ex.q()


def test_identically_zero_source_branch_is_kept_but_does_not_constrain_reachable_route():
    observed = coarse.maps(zero_wire())
    assert set(observed["source_fine"]) == {(("fine", "0"),), (("fine", "1"),)}
    assert observed["source_fine"][(("fine", "0"),)] == coarse.ex.zeros(4)
    assert equal_routes(observed) == (True, False)
    # The unrestricted tables keep the impossible input block in their domain.
    key = (("fine", "0"), ("future", "done"))
    assert observed["unrestricted_fine_future"][key] != observed["unrestricted_coarse_future"][key]


def test_future_outcome_alignment_is_by_label_not_list_position():
    future = measure(PY, ("+", "-"))
    original = wire(fine={"0": future, "1": future}, candidate={"all": future})
    changed = deepcopy(original)
    changed["source"]["outcomes"].reverse()
    changed["groups"].reverse()
    changed["fine_future"].reverse()
    changed["fine_future"][0]["instrument"]["outcomes"].reverse()
    changed["coarse_future"][0]["instrument"]["outcomes"].reverse()
    assert coarse.maps(original) == coarse.maps(changed)
    assert reference_qr02.reference_maps(original) == reference_qr02.reference_maps(changed)


def test_group_image_and_output_record_inventory_are_explicit():
    merged = coarse.maps(wire())
    retained = coarse.maps(no_merge_wire())
    assert set(merged["source_coarse"]) == {(("coarse", "all"),)}
    assert set(retained["source_coarse"]) == {(("coarse", "left"),), (("coarse", "right"),)}
    assert set(retained["fine_then_forget"]) == {
        (("coarse", "left"), ("future", "done")),
        (("coarse", "right"), ("future", "done")),
    }
    assert coarse.ex.total_map(merged["source_coarse"]) == coarse.ex.total_map(
        retained["source_coarse"]
    )


def test_phase_error_linear_inverse_is_not_a_physical_recovery():
    source = instrument(
        (("a", [weighted(I, Fraction(3, 5))]), ("b", [weighted(Z, Fraction(4, 5))]))
    )
    problem = wire(source, {"a": unitary(), "b": unitary(Z)}, {"all": unitary()})
    maps = coarse.maps(problem)
    assert equal_routes(maps) == (False, False)
    assert coarse.ex.total_map(maps["fine_then_forget"]) == coarse.ex.identity(4)
    # Invert the nonzero coherence multiplier -7/25 analytically, outside the
    # validated instrument API. A negative expectation forbids a positive map.
    inverse_plus = matrix(((H, Fraction(-25, 14)), (Fraction(-25, 14), H)))
    decoded = coarse.ex.decode_matrix(inverse_plus, 2)
    expectation_plus = sum((cell.real for row in decoded for cell in row), Fraction(0)) / 2
    assert expectation_plus == Fraction(-9, 7)
    assert expectation_plus < 0


def mutate(problem, path, value):
    output = deepcopy(problem)
    item = output
    for key in path[:-1]:
        item = item[key]
    item[path[-1]] = deepcopy(value)
    return output


@pytest.mark.parametrize(
    "path,value",
    [
        (("schema_version",), "unknown"),
        (("unknown",), True),
        (("qubits",), True),
        (("qubits",), 0),
        (("qubits",), 3),
        (("source", "support"), [True]),
        (("source", "support"), [0, 0]),
        (("source", "support"), [1]),
        (("source", "unknown"), False),
        (("source", "outcomes"), []),
        (("source", "outcomes", 0, "label"), "bad label"),
        (("source", "outcomes", 0, "kraus"), []),
        (("source", "outcomes", 0, "kraus", 0), I[:1]),
        (("groups",), []),
        (("groups",), [{"fine": "0", "coarse": "all"}]),
        (("groups",), [{"fine": "0", "coarse": "all"}, {"fine": "0", "coarse": "all"}]),
        (("groups", 0, "fine"), "missing"),
        (("groups", 0, "coarse"), "bad/group"),
        (("groups", 0, "callback"), True),
        (("fine_future",), []),
        (("fine_future", 0, "fine"), "missing"),
        (("coarse_future",), []),
        (("coarse_future", 0, "coarse"), "missing"),
        (("coarse_future", 0, "instrument", "support"), [True]),
        (("fine_future", 0, "instrument", "outcomes"), measure()["outcomes"]),
        (("coarse_future", 0, "instrument", "outcomes"), measure()["outcomes"]),
    ],
)
def test_strict_schema_and_total_group_tables_reject_invalids(path, value):
    bad = mutate(wire(), path, value)
    with pytest.raises(ValueError):
        coarse.parse(bad)
    with pytest.raises(ValueError):
        reference_qr02.reference_maps(bad)


@pytest.mark.parametrize(
    "token", [True, 0.5, "01", "1/1", "NaN", "1e999999999", "1e-999999999", str(2**64), "1" * 257]
)
def test_reused_exact_parser_rejects_unbounded_or_noncanonical_cells(token):
    bad = mutate(wire(), ("source", "outcomes", 0, "kraus", 0, 0, 0, 0), token)
    with pytest.raises(ValueError):
        coarse.parse(bad)
    with pytest.raises(ValueError):
        reference_qr02.reference_maps(bad)


@pytest.mark.parametrize("field", ["fine_future", "coarse_future"])
def test_duplicate_future_bindings_rejected(field):
    bad = wire()
    bad[field].append(deepcopy(bad[field][0]))
    with pytest.raises(ValueError):
        coarse.parse(bad)
    with pytest.raises(ValueError):
        reference_qr02.reference_maps(bad)


def test_missing_zero_outcome_binding_is_invalid_even_when_unreachable():
    bad = zero_wire()
    bad["fine_future"] = [item for item in bad["fine_future"] if item["fine"] != "0"]
    with pytest.raises(ValueError):
        coarse.parse(bad)
    with pytest.raises(ValueError):
        reference_qr02.reference_maps(bad)


@pytest.mark.parametrize("location", ["source", "fine", "coarse"])
def test_hidden_two_qubit_support_violation_rejected_everywhere(location):
    bad = local_wire()
    cnot = matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)))
    if location == "source":
        bad["source"] = instrument(
            (("0", [weighted(cnot, Fraction(3, 5))]), ("1", [weighted(cnot, Fraction(4, 5))])), (0,)
        )
    else:
        field = "fine_future" if location == "fine" else "coarse_future"
        bad[field][0]["instrument"] = instrument(
            (
                ("+", [weighted(cnot, Fraction(3, 5))]),
                ("-", [weighted(cnot, Fraction(4, 5))]),
            ),
            (0,),
        )
    with pytest.raises(ValueError):
        coarse.parse(bad)
    with pytest.raises(ValueError):
        reference_qr02.reference_maps(bad)


def test_reused_qr01_sources_match_the_frozen_result_identity():
    prior = Path(__file__).resolve().parent.parent / "qr-01-quantum-records-2026-09-05"
    expected = {
        "exact.py": "4238096b5de4b6aeeee2559b5200e0458a5635be88c06aa960bd50d0c2e3db56",
        "reference.py": "d7fab84717c22632e8be7cfd18aca68d439cbf611cf3a47a11abf25a8fca856f",
    }
    assert Path(coarse.ex.__file__).resolve() == (prior / "exact.py").resolve()
    for name, digest in expected.items():
        assert hashlib.sha256((prior / name).read_bytes()).hexdigest() == digest


def test_optimized_python_keeps_incomplete_instrument_rejections():
    bad = wire()
    bad["source"]["outcomes"] = bad["source"]["outcomes"][:1]
    script = """
import json, sys
sys.path.insert(0, sys.argv[1])
import coarse, reference_qr02
wire = json.loads(sys.argv[2])
for check in (lambda: coarse.parse(wire), lambda: reference_qr02.reference_maps(wire)):
    try:
        check()
    except ValueError:
        continue
    raise SystemExit('incomplete source accepted under -O')
print('both QR-02 validation paths reject under -O')
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
    assert result.stdout.strip() == "both QR-02 validation paths reject under -O"


def test_pinned_loader_rejects_changed_source_without_executing_it(monkeypatch):
    fake_path = SimpleNamespace(
        read_bytes=lambda: b"raise RuntimeError('must not execute')", is_symlink=lambda: False
    )
    monkeypatch.setattr(coarse, "BASE_PATH", fake_path)
    with pytest.raises(ValueError, match="pinned research dependency"):
        coarse._load_exact()


def test_pinned_loader_does_not_trust_a_spoofed_cached_module_path(monkeypatch):
    poisoned = SimpleNamespace(__file__=str(coarse.BASE_PATH), parse_problem=lambda value: value)
    monkeypatch.setitem(sys.modules, "qr02_pinned_exact", poisoned)
    try:
        loaded = coarse._load_exact()
    except ValueError:
        return  # Rejecting a private-name collision is an acceptable fail-closed policy.
    assert loaded is not poisoned
    assert callable(loaded.parse_problem)


class MemoryResult:
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
        raise AssertionError("artifact regression attempted a real result write")


def artifact_harness(monkeypatch, *, verify=True):
    # Only artifact-boundary tests import the runner; mathematical fixtures and
    # independently calculated expectations above never import study fixtures.
    # A unique test module name avoids collision with QR-01's study.py if both
    # directories are collected in one pytest process. Never import a cached
    # unrelated top-level module merely because it is also named "study".
    name = "qr02_artifact_test_study"
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("study.py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load QR-02 artifact runner for its isolated tests")
    study = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, study)
    spec.loader.exec_module(study)

    ledger = {"test-source": {"bytes": 1, "sha256": "source-identity"}}
    prior = {"bytes": 2, "sha256": "prior-identity"}
    suite = {"totals": {"tiny_fake_cases": 1}, "exact_value": ["1/2", "0"]}
    result = MemoryResult(
        study.canonical(
            {
                "schema_version": "det8-qr02-results-v1",
                "source_ledger": ledger,
                "prior_artifact": prior,
                "suite": suite,
            }
        )
    )
    monkeypatch.setattr(study, "RESULT", result)
    monkeypatch.setattr(study, "source_ledger", lambda: deepcopy(ledger))
    monkeypatch.setattr(study, "prior_identity", lambda: deepcopy(prior))
    monkeypatch.setattr(study, "run_suite", lambda: deepcopy(suite))
    monkeypatch.setattr(
        study,
        "sys",
        SimpleNamespace(
            flags=SimpleNamespace(isolated=1, optimize=0),
            pycache_prefix="/tmp/det8-qr02-test-cache-never-created",
        ),
    )
    monkeypatch.setattr(sys, "argv", ["study.py", *(["--verify"] if verify else [])])
    return study, result, ledger, prior, suite


def test_artifact_replay_rejects_concurrent_result_byte_replacement(monkeypatch):
    study, result, _, _, suite = artifact_harness(monkeypatch)

    def replace_during_run():
        result.raw += b" "
        return deepcopy(suite)

    monkeypatch.setattr(study, "run_suite", replace_during_run)
    with pytest.raises(ValueError, match="result changed during replay"):
        study.main()


@pytest.mark.parametrize("which", ["source", "prior"])
def test_artifact_replay_rejects_source_or_prior_drift(monkeypatch, which):
    study, _, ledger, prior, suite = artifact_harness(monkeypatch)

    def change_identity_during_run():
        if which == "source":
            ledger["test-source"]["sha256"] = "changed-source"
        else:
            prior["sha256"] = "changed-prior"
        return deepcopy(suite)

    monkeypatch.setattr(study, "run_suite", change_identity_during_run)
    with pytest.raises(ValueError, match="source/prior changed during execution"):
        study.main()


def test_artifact_replay_rejects_suite_mismatch(monkeypatch):
    study, _, _, _, suite = artifact_harness(monkeypatch)
    changed = deepcopy(suite)
    changed["exact_value"] = ["2/3", "0"]
    monkeypatch.setattr(study, "run_suite", lambda: changed)
    with pytest.raises(ValueError, match="exact replay differs"):
        study.main()


def test_artifact_capture_refuses_existing_result_before_computation(monkeypatch):
    study, _, _, _, _ = artifact_harness(monkeypatch, verify=False)

    def forbidden_work():
        raise AssertionError("existing result must be refused before computation")

    monkeypatch.setattr(study, "source_ledger", forbidden_work)
    monkeypatch.setattr(study, "prior_identity", forbidden_work)
    monkeypatch.setattr(study, "run_suite", forbidden_work)
    with pytest.raises(FileExistsError, match="results.json already exists"):
        study.main()


def test_artifact_replay_reports_exact_verified_byte_hash(monkeypatch, capsys):
    study, result, _, _, suite = artifact_harness(monkeypatch)
    original = result.raw
    study.main()
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "VERIFIED_EXACT_REPLAY"
    assert report["result_sha256"] == study.digest(original)
    assert report["totals"] == suite["totals"]
    assert result.raw == original
