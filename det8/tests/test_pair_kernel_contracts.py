"""Independent domain checks for the experimental pair-kernel calculus."""

import itertools
import math

import pytest

from det8.models.pair_kernel import PairKernel, make_pair_kernel
from det8.models.record_extendability import gram_sum_rule, marginal, product_blocks


def assert_factor_reconstructs(matrix, factor, *, abs_tol=1e-12):
    """Compare every entry with the independently assembled row Gram matrix."""
    for i, row in enumerate(matrix):
        for j, expected in enumerate(row):
            actual = sum(a * b.conjugate() for a, b in zip(factor[i], factor[j]))
            assert actual == pytest.approx(expected, rel=1e-12, abs=abs_tol)


@pytest.mark.parametrize("matrix", [
    [[1, 0], [0, 0]],
    [[0, 0], [0, 1]],
    [[0, 0], [0, 0]],
    [[0.25, 0.25], [0.25, 0.25]],
    [[0.5, -0.5j], [0.5j, 0.5]],
])
def test_singular_psd_including_zero_and_complex_kernel(matrix):
    kernel = PairKernel(matrix)
    assert kernel.is_positive_semidefinite()
    assert_factor_reconstructs(matrix, kernel.cholesky())
    assert kernel.gram_check()["gram_holds"]


def test_rank_two_complex_factor_is_equivariant_under_event_permutations():
    # Four rows in C^2: PSD with rank two by construction, including a zero row.
    rows = [(0, 0), (1, 1j), (2j, 1), (1 + 2j, 1 + 1j)]
    original = [[sum(a * complex(b).conjugate() for a, b in zip(u, v))
                 for v in rows] for u in rows]
    for order in itertools.permutations(range(4)):
        matrix = [[original[i][j] for j in order] for i in order]
        kernel = PairKernel(matrix)
        assert kernel.is_positive_semidefinite()
        assert_factor_reconstructs(matrix, kernel.gram_vectors())


@pytest.mark.parametrize("scale", [1e-250, 1e250])
def test_factorization_scales_without_regularizing_null_directions(scale):
    matrix = [[scale, -1j * scale], [1j * scale, scale]]
    kernel = PairKernel(matrix)
    factor = kernel.cholesky()
    assert_factor_reconstructs(matrix, factor, abs_tol=scale * 1e-12)
    assert sum(any(value != 0 for value in column) for column in zip(*factor)) == 1


@pytest.mark.parametrize("matrix", [
    [[1, 2], [2, 1]],                  # Eigenvalues 3 and -1.
    [[0, 1], [1, 0]],                  # Zero diagonal cannot hide cross terms.
    [[1, 0], [0, -0.01]],
    [[1, 1j], [1j, 1]],               # Symmetric, not Hermitian.
    [[1 + 0.1j]],
])
def test_indefinite_or_nonhermitian_matrices_have_no_gram_factor(matrix):
    kernel = PairKernel(matrix)
    assert not kernel.is_positive_semidefinite()
    assert not kernel.validate()["valid"]
    with pytest.raises(ValueError):
        kernel.cholesky()


def test_psd_tolerance_is_explicit_backward_error_not_exact_positivity():
    kernel = PairKernel([[1, 0], [0, -1e-13]])
    assert kernel.is_positive_semidefinite(tol=1e-12)
    assert not kernel.is_positive_semidefinite(tol=1e-14)
    assert kernel.D[1][1] == -1e-13  # No repair of the supplied matrix.
    with pytest.raises(ValueError):
        kernel.commit_kernel([{0}, {1}])  # No negative probability escapes.


@pytest.mark.parametrize("matrix", [
    [], [[1, 0]], [[float("nan")]], [[float("inf")]],
    [[complex(1, float("inf"))]], [[True]], [["1"]], [[10 ** 400]],
])
def test_nonfinite_nonnumeric_or_empty_matrix_is_rejected(matrix):
    with pytest.raises(ValueError):
        PairKernel(matrix)


def test_mutated_nonfinite_matrix_fails_before_factorization_or_commit():
    kernel = PairKernel([[1, 0], [0, 0]])
    kernel.D[1][1] = float("nan")
    assert not kernel.validate()["valid"]
    with pytest.raises(ValueError):
        kernel.gram_vectors()
    with pytest.raises(ValueError):
        kernel.commit_kernel([{0}, {1}])


@pytest.mark.parametrize("tol", [-1, float("nan"), float("inf"), True, "small"])
def test_invalid_tolerance_is_rejected(tol):
    kernel = PairKernel([[1]])
    for operation in [kernel.cholesky, kernel.is_positive_semidefinite,
                      kernel.is_hermitian, kernel.is_normalized]:
        with pytest.raises((TypeError, ValueError)):
            operation(tol=tol)


@pytest.mark.parametrize("partition", [
    [], [{0}], [{0}, set(), {1}], [{0, 1}, {1}], [{0}, {0}],
    [{0}, {2}], [{0}, {-1}], [[0, 0], [1]], [[False], [1]], [[0.0], [1]],
])
def test_commit_rejects_malformed_partitions(partition):
    kernel = PairKernel([[0.4, 0], [0, 0.6]])
    with pytest.raises(ValueError):
        kernel.commit_kernel(partition)


def test_zero_probability_nonzero_block_is_retained_without_normalization():
    matrix = [[1, -1, 0], [-1, 1, 0], [0, 0, 1]]
    kernel = PairKernel(matrix)
    assert kernel.validate()["valid"]
    assert kernel.commit_kernel([{0, 1}, {2}]) == [0.0, 1.0]
    assert kernel.D[0][0] == 1  # A zero event weight need not erase its raw block.


def test_nonrecordable_raw_weights_remain_weights_not_probabilities():
    kernel = PairKernel([[4, -2], [-2, 1]])
    assert kernel.validate()["valid"]
    assert [kernel.mu({0}), kernel.mu({1})] == [4, 1]
    with pytest.raises(ValueError, match="exactly decoherent"):
        kernel.commit_kernel([{0}, {1}])


def test_unnormalized_kernel_is_not_silently_normalized_on_commit():
    kernel = PairKernel([[0.4, 0], [0, 0.4]])
    assert kernel.is_positive_semidefinite()
    with pytest.raises(ValueError, match="normalized"):
        kernel.commit_kernel([{0}, {1}])
    assert kernel.mu({0}) == 0.4


def test_approximate_decoherence_does_not_license_a_commit():
    kernel = PairKernel([[0.5, 1e-12j], [-1e-12j, 0.5]])
    partition = [{0}, {1}]
    assert kernel.is_decoherent(partition)
    assert not kernel.is_decoherent(partition, tol=0)
    with pytest.raises(ValueError, match="exactly decoherent"):
        kernel.commit_kernel(partition)


def test_additivity_does_not_imply_exact_decoherence():
    kernel = PairKernel([[0.5, 0.25j], [-0.25j, 0.5]])
    result = kernel.classical_additivity([{0}, {1}])
    assert result["additive"]
    assert not result["decoherent"]
    assert result["consistent"]
    assert "does not imply" in result["interpretation"]
    with pytest.raises(ValueError):
        kernel.commit_kernel([{0}, {1}])


def test_additivity_accepts_exact_zero_tolerance_and_accounts_for_cross_error():
    assert PairKernel([[1, 0], [0, 0]]).classical_additivity(
        [{0}, {1}], tol=0)["additive"]
    cross = 5e-10
    diagonal = (1 - 6 * cross) / 3
    matrix = [[diagonal if i == j else cross for j in range(3)] for i in range(3)]
    result = PairKernel(matrix).classical_additivity([{0}, {1}, {2}], tol=1e-9)
    assert result["decoherent"]
    assert not result["additive"]
    assert result["consistent"]


def test_same_diagonal_coherent_kernels_have_distinct_licensed_readouts():
    weights = []
    for coherence in (0.125, -0.125):
        matrix = [[0.25, coherence, 0, 0], [coherence, 0.25, 0, 0],
                  [0, 0, 0.25, -coherence], [0, 0, -coherence, 0.25]]
        weights.append(PairKernel(matrix).commit_kernel([{0, 1}, {2, 3}]))
    assert weights == [[0.75, 0.25], [0.25, 0.75]]


def test_existing_gram_sum_consumer_accepts_singular_composition_and_marginal():
    original = PairKernel([[0.5, -0.5j], [0.5j, 0.5]])
    extension = original.compose(PairKernel([[1, 0], [0, 0]]))
    blocks = product_blocks(2, 2)
    assert extension.validate()["valid"]
    assert gram_sum_rule(extension, blocks)["sum_rule_holds"]
    recovered = marginal(extension, blocks)
    for actual, expected in zip(recovered.D, original.D):
        assert actual == pytest.approx(expected)


def test_existing_random_positive_definite_family_still_reconstructs():
    for seed in range(5):
        kernel = make_pair_kernel(4, seed=seed)
        assert kernel.validate()["valid"]
        assert_factor_reconstructs(kernel.D, kernel.cholesky())
    classical = make_pair_kernel(4, coherent=False)
    probabilities = classical.commit_kernel([{i} for i in range(4)])
    assert math.fsum(probabilities) == pytest.approx(1)
