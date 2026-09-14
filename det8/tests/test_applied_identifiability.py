"""Exact substitution oracles for structural identification, without a second RREF."""

from dataclasses import FrozenInstanceError
from fractions import Fraction as F

import pytest

from det8.applied_physics import identifiability as ident


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


def verify_certificate(certificate, design, target):
    """Substitute the returned proof into the original problem, not reduced rows."""
    design = tuple(tuple(F(value) for value in row) for row in design)
    target = tuple(F(value) for value in target)
    assert certificate.design == design
    assert certificate.target == target
    assert certificate.n_rows == len(design)
    assert certificate.n_parameters == len(target)
    assert isinstance(certificate.design, tuple)
    assert isinstance(certificate.target, tuple)
    assert all(isinstance(row, tuple) for row in certificate.design)
    assert all(type(value) is F for row in certificate.design for value in row)
    assert all(type(value) is F for value in certificate.target)
    assert 0 <= certificate.rank <= min(len(design), len(target))
    if certificate.identified:
        assert certificate.null_direction is None
        weights = certificate.row_weights
        assert isinstance(weights, tuple) and len(weights) == len(design)
        assert all(type(value) is F for value in weights)
        represented = tuple(
            sum((weight * row[j] for weight, row in zip(weights, design, strict=True)), F(0))
            for j in range(len(target))
        )
        assert represented == target
    else:
        assert certificate.row_weights is None
        direction = certificate.null_direction
        assert isinstance(direction, tuple) and len(direction) == len(target)
        assert all(type(value) is F for value in direction)
        assert all(dot(row, direction) == 0 for row in design)
        assert dot(target, direction) == 1
        # Over the explicitly unrestricted parameter space both alternatives
        # are admissible, have identical means, and differ in target by one.
        theta = tuple(F(i - 2, 3) for i in range(len(target)))
        alternative = tuple(a + b for a, b in zip(theta, direction, strict=True))
        assert [dot(row, theta) for row in design] == [dot(row, alternative) for row in design]
        assert dot(target, alternative) - dot(target, theta) == 1


def verify_candidates(analysis):
    assert isinstance(analysis.candidates, tuple)
    for candidate in analysis.candidates:
        assert isinstance(candidate.row, tuple)
        assert all(type(value) is F for value in candidate.row)
        verify_certificate(
            candidate.certificate, analysis.design + (candidate.row,), analysis.target
        )
        if analysis.identified:
            assert candidate.separation is None
            assert candidate.separates_displayed_pair is None
            assert candidate.certificate.identified
        else:
            separation = dot(candidate.row, analysis.null_direction)
            assert type(candidate.separation) is F
            assert candidate.separation == separation
            assert candidate.separates_displayed_pair is (separation != 0)


@pytest.mark.parametrize("target", [(0,), (0, 0, 0), (1,), (0, F(2, 3), -1)])
def test_empty_design_has_zero_rank_and_proves_or_refutes_the_requested_quantity(target):
    result = ident.analyze_identifiability([], target)
    verify_certificate(result, [], target)
    assert result.rank == 0
    assert result.identified is (not any(target))
    if result.identified:
        assert result.row_weights == ()


def test_zero_target_stays_identified_with_zero_rows_and_arbitrary_candidates():
    design = [(0, 0), (0, 0)]
    result = ident.analyze_identifiability(design, (0, 0), [("new direction", (1, -3))])
    verify_certificate(result, design, (0, 0))
    verify_candidates(result)
    assert result.identified and result.rank == 0
    assert result.row_weights == (0, 0)


@pytest.mark.parametrize(
    "target, identified",
    [((2, 1), True), ((4, 2), True), ((1, 0), False), ((0, 1), False), ((3, 1), False)],
)
def test_one_reference_level_identifies_its_response_but_not_gain_offset_or_unseen_response(
    target, identified
):
    # theta=(gain,offset), with every observed reference at x=2.
    design = [(2, 1), (2, 1), (2, 1)]
    candidates = [("repeat x=2", (2, 1)), ("measure zero", (0, 1)), ("measure x=-1", (-1, 1))]
    result = ident.analyze_identifiability(design, target, candidates)
    verify_certificate(result, design, target)
    verify_candidates(result)
    assert result.rank == 1 and result.identified is identified
    assert result.candidates[0].certificate.identified is identified
    assert all(candidate.certificate.identified for candidate in result.candidates[1:])
    if not identified:
        assert result.candidates[0].separates_displayed_pair is False


@pytest.mark.parametrize("target, identified", [((0, 1), True), ((1, 0), False)])
def test_zero_reference_level_is_the_offset_exception(target, identified):
    result = ident.analyze_identifiability([(0, 1)], target, [("measure x=1", (1, 1))])
    verify_certificate(result, [(0, 1)], target)
    verify_candidates(result)
    assert result.identified is identified
    assert result.candidates[0].certificate.identified


def test_pair_separation_does_not_imply_target_identification_and_joint_rows_can_succeed():
    design, target = [(1, 0, 0)], (0, 1, 1)
    result = ident.analyze_identifiability(
        design, target, [("second coordinate", (0, 1, 0)), ("third coordinate", (0, 0, 1))]
    )
    verify_certificate(result, design, target)
    verify_candidates(result)
    assert not result.identified
    # delta_1+delta_2=1, so at least one coordinate separates the displayed
    # pair. Each action still leaves the other coordinate unobserved.
    assert any(candidate.separates_displayed_pair for candidate in result.candidates)
    assert all(not candidate.certificate.identified for candidate in result.candidates)
    assert all(candidate.certificate.rank == 2 for candidate in result.candidates)
    joint = ident.analyze_identifiability(design + [(0, 1, 0), (0, 0, 1)], target)
    verify_certificate(joint, design + [(0, 1, 0), (0, 0, 1)], target)
    assert joint.identified and joint.rank == 3


def test_candidate_separation_is_signed_and_target_observation_always_suffices():
    design, target = [(1, 0, 0)], (0, 1, 1)
    result = ident.analyze_identifiability(
        design, target, [("negative target", (0, -5, -5)), ("zero action", (0, 0, 0))]
    )
    verify_candidates(result)
    assert result.candidates[0].separation == -5
    assert result.candidates[0].certificate.identified
    assert result.candidates[0].certificate.row_weights == (0, F(-1, 5))
    assert result.candidates[1].separation == 0
    assert not result.candidates[1].certificate.identified


def test_full_rank_certificate_matches_an_independent_integer_inverse():
    # det(H)=1*(0-24)-2*(0-20)+3*(0-5)=1. The displayed inverse
    # is checked by multiplication, independently of any elimination code.
    design = ((1, 2, 3), (0, 1, 4), (5, 6, 0))
    inverse = ((-24, 18, 5), (20, -15, -4), (-5, 4, 1))
    for i in range(3):
        for j in range(3):
            assert dot(design[i], tuple(inverse[k][j] for k in range(3))) == int(i == j)
    target = (2, -1, 3)
    result = ident.analyze_identifiability(design, target)
    verify_certificate(result, design, target)
    assert result.identified and result.rank == 3
    assert result.row_weights == (-83, 63, 17)  # target^T H^-1


@pytest.mark.parametrize("target, identified", [((2, 3, -3), True), ((0, 0, 1), False)])
def test_row_permutation_duplication_scaling_and_zero_rows_preserve_identification(
    target, identified
):
    first, second = (1, 2, 0), (0, 1, 3)
    designs = [
        [first, second],
        [second, first],
        [first, first, second],
        [tuple(F(-3, 2) * value for value in first), tuple(7 * value for value in second)],
        [(0, 0, 0), second, first, (0, 0, 0)],
    ]
    for design in designs:
        result = ident.analyze_identifiability(design, target)
        verify_certificate(result, design, target)
        assert result.rank == 2 and result.identified is identified


def test_exact_near_dependence_is_not_collapsed_by_a_float_rank_tolerance():
    epsilon = F(1, 2 ** (ident.MAX_COEFFICIENT_BITS - 8))
    design, target = [(1, 1), (1, 1 + epsilon)], (0, 1)
    result = ident.analyze_identifiability(design, target)
    verify_certificate(result, design, target)
    assert result.rank == 2 and result.identified
    assert result.row_weights == (-1 / epsilon, 1 / epsilon)


def test_derived_certificates_may_exceed_the_input_coefficient_bit_bound():
    denominator = 2 ** (ident.MAX_COEFFICIENT_BITS - 1) - 1
    design, target = [(F(1, denominator),)], (denominator,)
    result = ident.analyze_identifiability(design, target)
    verify_certificate(result, design, target)
    assert result.row_weights == (denominator * denominator,)
    assert result.row_weights[0].numerator.bit_length() > ident.MAX_COEFFICIENT_BITS


def test_results_detach_mutable_inputs_and_freeze_nested_certificates():
    design, target, action = [[1, 0]], [0, 1], [0, 1]
    candidates = [["observe target", action]]
    result = ident.analyze_identifiability(design, target, candidates)
    design[0][0], target[0], action[0] = 99, 99, 99
    design.append([1, 1])
    candidates[0][0] = "changed"
    verify_certificate(result, [(1, 0)], (0, 1))
    verify_candidates(result)
    assert result.candidates[0].label == "observe target"
    assert result.candidates[0].row == (0, 1)
    for value, field in [
        (result, "rank"),
        (result.candidates[0], "label"),
        (result.candidates[0].certificate, "identified"),
    ]:
        with pytest.raises(FrozenInstanceError):
            setattr(value, field, None)
        assert not hasattr(value, "__dict__")
    with pytest.raises(TypeError):
        result.design[0][0] = F(3)


class OneShot:
    def __init__(self, values):
        self.values = values
        self.used = False

    def __iter__(self):
        if self.used:
            raise AssertionError("input container consumed twice")
        self.used = True
        yield from self.values


def test_every_input_container_can_be_one_shot():
    result = ident.analyze_identifiability(
        OneShot([OneShot([1, 0])]),
        OneShot([0, 1]),
        OneShot([OneShot(["observe target", OneShot([0, 1])])]),
    )
    verify_certificate(result, [(1, 0)], (0, 1))
    verify_candidates(result)
    assert result.candidates[0].certificate.identified


class IntSubclass(int):
    pass


class FractionSubclass(F):
    pass


@pytest.mark.parametrize(
    "bad",
    [True, False, 1.0, float("nan"), float("inf"), "1", 1j, IntSubclass(1), FractionSubclass(1, 2)],
)
@pytest.mark.parametrize("position", ["design", "target", "candidate"])
def test_coefficients_must_have_the_declared_exact_types(bad, position):
    design, target, candidates = [[1]], [1], [("probe", [1])]
    if position == "design":
        design = [[bad]]
    elif position == "target":
        target = [bad]
    else:
        candidates = [("probe", [bad])]
    with pytest.raises(TypeError):
        ident.analyze_identifiability(design, target, candidates)


@pytest.mark.parametrize(
    "design,target,candidates",
    [
        ([], [], []),
        ([[]], [1], []),
        ([[1, 0], [1]], [1, 0], []),
        ([[1, 0]], [1], []),
        ([[1]], [1], [("wrong width", [1, 0])]),
        ([[1]], [1], [("", [1])]),
        ([[1]], [1], [("   ", [1])]),
        ([[1]], [1], [("same", [1]), ("same", [0])]),
        ([[1]], [1], [("missing row",)]),
        ([[1]], [1], [("extra item", [1], [1])]),
    ],
)
def test_malformed_shapes_and_labels_are_rejected(design, target, candidates):
    with pytest.raises(ValueError):
        ident.analyze_identifiability(design, target, candidates)


@pytest.mark.parametrize("label", [None, 1, True, ("nested",)])
def test_candidate_labels_are_strings(label):
    with pytest.raises(TypeError):
        ident.analyze_identifiability([[1]], [1], [(label, [1])])


@pytest.mark.parametrize("bad", ["1", b"1", bytearray(b"1"), {0: 1}, None])
@pytest.mark.parametrize(
    "position", ["design", "target", "candidates", "design row", "candidate pair", "candidate row"]
)
def test_text_mappings_and_noniterables_are_not_silently_coerced_as_containers(bad, position):
    design, target, candidates = [[1]], [1], [("probe", [1])]
    if position == "design":
        design = bad
    elif position == "target":
        target = bad
    elif position == "candidates":
        candidates = bad
    elif position == "design row":
        design = [bad]
    elif position == "candidate pair":
        candidates = [bad]
    else:
        candidates = [("probe", bad)]
    with pytest.raises(TypeError):
        ident.analyze_identifiability(design, target, candidates)


def test_candidate_names_and_input_order_are_retained_without_implicit_combination():
    candidates = [(" z last alphabetically ", (0, 1, 0)), ("a first", (0, 0, 1))]
    result = ident.analyze_identifiability([(1, 0, 0)], (0, 1, 1), candidates)
    assert tuple(candidate.label for candidate in result.candidates) == tuple(
        label for label, _ in candidates
    )
    verify_candidates(result)
    assert all(not candidate.certificate.identified for candidate in result.candidates)


def test_admission_limits_allow_the_boundary_and_one_augmented_row():
    design = [(0,)] * ident.MAX_DESIGN_ROWS
    candidates = [(f"probe {i}", (1,)) for i in range(ident.MAX_CANDIDATES)]
    result = ident.analyze_identifiability(design, (1,), candidates)
    verify_certificate(result, design, (1,))
    verify_candidates(result)
    assert len(result.candidates) == ident.MAX_CANDIDATES
    assert all(
        candidate.certificate.n_rows == ident.MAX_DESIGN_ROWS + 1 for candidate in result.candidates
    )
    parameter_boundary = ident.analyze_identifiability([], [0] * ident.MAX_PARAMETERS)
    assert parameter_boundary.identified
    label_boundary = ident.analyze_identifiability([], [1], [("a" * ident.MAX_LABEL_LENGTH, [1])])
    assert label_boundary.candidates[0].certificate.identified


@pytest.mark.parametrize("position", ["design", "target", "candidate"])
@pytest.mark.parametrize(
    "bad",
    [
        2**ident.MAX_COEFFICIENT_BITS,
        -(2**ident.MAX_COEFFICIENT_BITS),
        F(1, 2**ident.MAX_COEFFICIENT_BITS),
    ],
)
def test_oversized_reduced_coefficients_are_refused_in_every_position(position, bad):
    design, target, candidates = [[1]], [1], [("probe", [1])]
    if position == "design":
        design = [[bad]]
    elif position == "target":
        target = [bad]
    else:
        candidates = [("probe", [bad])]
    with pytest.raises(ValueError):
        ident.analyze_identifiability(design, target, candidates)


def test_coefficient_boundary_uses_reduced_values_and_never_float_conversion():
    boundary = 2 ** (ident.MAX_COEFFICIENT_BITS - 1)
    for value in (boundary, -boundary, F(1, boundary), F(2**200, 2**200)):
        result = ident.analyze_identifiability([(value,)], (value,))
        verify_certificate(result, [(value,)], (value,))
        assert result.identified
    with pytest.raises(ValueError):
        ident.analyze_identifiability([], [1], [("a" * (ident.MAX_LABEL_LENGTH + 1), [1])])


@pytest.mark.parametrize("position", ["design", "target", "candidate", "row"])
def test_over_budget_streams_stop_without_materializing_the_unbounded_tail(position):
    limits = {
        "design": ident.MAX_DESIGN_ROWS,
        "target": ident.MAX_PARAMETERS,
        "candidate": ident.MAX_CANDIDATES,
        "row": ident.MAX_PARAMETERS,
    }
    consumed = []

    def stream():
        for i in range(limits[position] + 1):
            consumed.append(i)
            yield (
                (0,)
                if position == "design"
                else (f"probe {i}", [1])
                if position == "candidate"
                else 0
            )
        pytest.fail("consumer read beyond the declared bounded prefix")

    design, target, candidates = [(1,)], (1,), []
    if position == "design":
        design = stream()
    elif position == "target":
        target = stream()
    elif position == "candidate":
        candidates = stream()
    else:
        design = [stream()]
    with pytest.raises(ValueError):
        ident.analyze_identifiability(design, target, candidates)
    assert len(consumed) <= limits[position] + 1
