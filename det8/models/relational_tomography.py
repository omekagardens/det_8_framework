"""Experiment-agnostic Relational Endpoint Tomography (RET) inference core.

RET represents candidate relational models with Gaussian parameter states,
correlated Gaussian observation errors, and either linear or nonlinear
response maps. Optional endpoints use a spike-and-slab architecture: omission
of an endpoint is the spike at zero; models containing it carry a Gaussian
slab prior over its amplitude.

The module deliberately separates statistical support from ontology.  A high
posterior probability means that a declared model predicts the accumulated
record better under the declared assumptions.  It is not an ontological
existence probability.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Callable, Dict, Mapping, Sequence, Tuple, Union


Vector = Tuple[float, ...]
Matrix = Tuple[Tuple[float, ...], ...]
ObservationNoise = Union[float, Sequence[Sequence[float]]]
NonlinearIncrement = Callable[[Mapping[str, float]], Sequence[float]]
OPEN_MODEL_NAME = "M_bottom"
POSTERIOR_IS_NOT_ONTOLOGY = (
    "Posterior model probability is conditional predictive support within the "
    "declared model set; it is not an ontological existence probability."
)


@dataclass(frozen=True)
class GaussianPrior:
    mean: float
    standard_deviation: float
    role: str = "effect"

    def __post_init__(self) -> None:
        if self.standard_deviation <= 0.0:
            raise ValueError("prior standard deviation must be positive")
        if self.role not in ("effect", "nuisance"):
            raise ValueError("parameter role must be effect or nuisance")


@dataclass(frozen=True)
class RelationalModel:
    name: str
    family: str
    parameter_priors: Mapping[str, GaussianPrior]
    complexity: float = 0.0

    def __post_init__(self) -> None:
        if not self.name or not self.family:
            raise ValueError("model name and family are required")
        if self.complexity < 0.0:
            raise ValueError("model complexity cannot be negative")


@dataclass(frozen=True)
class PracticalCost:
    time: float = 0.0
    money: float = 0.0
    risk: float = 0.0
    wear: float = 0.0

    def __post_init__(self) -> None:
        if min(self.time, self.money, self.risk, self.wear) < 0.0:
            raise ValueError("practical costs cannot be negative")


@dataclass(frozen=True)
class RelationalAction:
    name: str
    kind: str
    known_response: Vector
    feature_vectors: Mapping[str, Vector]
    cost: PracticalCost = field(default_factory=PracticalCost)
    metadata: Mapping[str, object] = field(default_factory=dict)
    nonlinear_increment: NonlinearIncrement | None = field(
        default=None,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        if self.kind not in ("science", "calibration"):
            raise ValueError("action kind must be science or calibration")
        if not self.known_response:
            raise ValueError("action response vector cannot be empty")
        dimension = len(self.known_response)
        if any(len(vector) != dimension for vector in self.feature_vectors.values()):
            raise ValueError("all action feature vectors must share one dimension")

    @property
    def dimension(self) -> int:
        return len(self.known_response)

    @property
    def is_nonlinear(self) -> bool:
        return self.nonlinear_increment is not None


@dataclass(frozen=True)
class Question:
    name: str
    answer_by_model: Mapping[str, str]
    description: str = ""

    def answer(self, model_name: str) -> str:
        if model_name == OPEN_MODEL_NAME:
            return "model_inadequate"
        return self.answer_by_model[model_name]


@dataclass(frozen=True)
class GaussianParameterState:
    parameter_names: Tuple[str, ...]
    mean: Vector
    covariance: Matrix


@dataclass(frozen=True)
class RETPosterior:
    models: Mapping[str, RelationalModel]
    model_weights: Mapping[str, float]
    parameters: Mapping[str, GaussianParameterState]
    open_model_scale: float
    observations: int = 0

    def __post_init__(self) -> None:
        expected = set(self.models) | {OPEN_MODEL_NAME}
        if set(self.model_weights) != expected:
            raise ValueError("posterior weights must include every model and M_bottom")
        if abs(sum(self.model_weights.values()) - 1.0) > 1.0e-9:
            raise ValueError("posterior model weights must sum to one")
        if self.open_model_scale <= 0.0:
            raise ValueError("open-model scale must be positive")


def _identity(size: int) -> list[list[float]]:
    return [[1.0 if row == column else 0.0 for column in range(size)] for row in range(size)]


def _inverse_and_determinant(matrix: Sequence[Sequence[float]]) -> tuple[list[list[float]], float]:
    size = len(matrix)
    augmented = [list(matrix[row]) + _identity(size)[row] for row in range(size)]
    determinant = 1.0
    sign = 1.0
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1.0e-24:
            raise ValueError("singular covariance matrix")
        if pivot != column:
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
            sign *= -1.0
        pivot_value = augmented[column][column]
        determinant *= pivot_value
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][item] - factor * augmented[column][item]
                for item in range(2 * size)
            ]
    inverse = [row[size:] for row in augmented]
    return inverse, sign * determinant


def _cholesky(matrix: Sequence[Sequence[float]]) -> list[list[float]]:
    """Return a lower Cholesky factor for a positive-definite matrix."""

    size = len(matrix)
    if size == 0 or any(len(row) != size for row in matrix):
        raise ValueError("covariance matrix must be nonempty and square")
    lower = [[0.0 for _ in range(size)] for _ in range(size)]
    for row in range(size):
        for column in range(row + 1):
            value = matrix[row][column] - sum(
                lower[row][inner] * lower[column][inner]
                for inner in range(column)
            )
            if row == column:
                if value <= 0.0:
                    raise ValueError("covariance matrix must be positive definite")
                lower[row][column] = math.sqrt(value)
            else:
                lower[row][column] = value / lower[column][column]
    return lower


def _observation_covariance(
    observation_noise: ObservationNoise,
    dimension: int,
) -> Matrix:
    """Normalize a scalar standard deviation or full covariance matrix."""

    if isinstance(observation_noise, (int, float)) and not isinstance(
        observation_noise, bool
    ):
        sigma = float(observation_noise)
        if not math.isfinite(sigma) or sigma <= 0.0:
            raise ValueError("observation noise must be positive and finite")
        return tuple(
            tuple(sigma**2 if row == column else 0.0 for column in range(dimension))
            for row in range(dimension)
        )

    covariance = tuple(
        tuple(float(value) for value in row) for row in observation_noise
    )
    if len(covariance) != dimension or any(
        len(row) != dimension for row in covariance
    ):
        raise ValueError("observation covariance dimension does not match action")
    if any(not math.isfinite(value) for row in covariance for value in row):
        raise ValueError("observation covariance must contain finite values")
    for row in range(dimension):
        for column in range(dimension):
            if abs(covariance[row][column] - covariance[column][row]) > 1.0e-12:
                raise ValueError("observation covariance must be symmetric")
    _cholesky(covariance)
    return covariance


def _matmul(left: Sequence[Sequence[float]], right: Sequence[Sequence[float]]) -> list[list[float]]:
    return [
        [
            sum(left[row][inner] * right[inner][column] for inner in range(len(right)))
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def _transpose(matrix: Sequence[Sequence[float]]) -> list[list[float]]:
    return [list(column) for column in zip(*matrix)]


def _matvec(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
    return [sum(value * vector[column] for column, value in enumerate(row)) for row in matrix]


def _add_matrix(left: Sequence[Sequence[float]], right: Sequence[Sequence[float]]) -> list[list[float]]:
    return [
        [left[row][column] + right[row][column] for column in range(len(left[0]))]
        for row in range(len(left))
    ]


def _subtract_matrix(
    left: Sequence[Sequence[float]],
    right: Sequence[Sequence[float]],
) -> list[list[float]]:
    return [
        [left[row][column] - right[row][column] for column in range(len(left[0]))]
        for row in range(len(left))
    ]


def _symmetrize(matrix: Sequence[Sequence[float]]) -> Matrix:
    return tuple(
        tuple(
            0.5 * (matrix[row][column] + matrix[column][row])
            for column in range(len(matrix))
        )
        for row in range(len(matrix))
    )


def _design_matrix(action: RelationalAction, state: GaussianParameterState) -> list[list[float]]:
    return [
        [
            action.feature_vectors.get(parameter, (0.0,) * action.dimension)[axis]
            for parameter in state.parameter_names
        ]
        for axis in range(action.dimension)
    ]


def response_for_parameters(
    action: RelationalAction,
    parameters: Mapping[str, float],
) -> Vector:
    """Evaluate an action response for a concrete parameter assignment.

    Linear feature contributions and the optional nonlinear increment are
    additive to ``known_response``. The nonlinear callable must return one
    increment per observation dimension.
    """

    response = list(action.known_response)
    for parameter, value in parameters.items():
        feature = action.feature_vectors.get(parameter)
        if feature is None:
            continue
        for axis in range(action.dimension):
            response[axis] += value * feature[axis]
    if action.nonlinear_increment is not None:
        increment = tuple(
            float(value) for value in action.nonlinear_increment(parameters)
        )
        if len(increment) != action.dimension:
            raise ValueError("nonlinear response dimension does not match action")
        if any(not math.isfinite(value) for value in increment):
            raise ValueError("nonlinear response must contain finite values")
        for axis in range(action.dimension):
            response[axis] += increment[axis]
    return tuple(response)


def _parameter_cholesky(covariance: Matrix) -> list[list[float]]:
    """Factor a posterior covariance, adding only numerical-scale jitter."""

    try:
        return _cholesky(covariance)
    except ValueError:
        scale = max(max(row) for row in covariance)
        jitter = max(abs(scale) * 1.0e-12, 1.0e-15)
        stabilized = [list(row) for row in covariance]
        for axis in range(len(stabilized)):
            stabilized[axis][axis] += jitter
        return _cholesky(stabilized)


def _cubature_moments(
    state: GaussianParameterState,
    action: RelationalAction,
) -> tuple[Vector, Matrix, Matrix]:
    """Propagate a Gaussian parameter state through a nonlinear response.

    A spherical-radial cubature rule uses 2n equally weighted sigma points.
    The return values are observation mean, signal covariance, and
    parameter-observation cross covariance.
    """

    parameter_count = len(state.parameter_names)
    if parameter_count == 0:
        mean = response_for_parameters(action, {})
        zero_signal = tuple(
            tuple(0.0 for _ in range(action.dimension))
            for _ in range(action.dimension)
        )
        return mean, zero_signal, ()

    lower = _parameter_cholesky(state.covariance)
    radius = math.sqrt(parameter_count)
    parameter_points = []
    observation_points = []
    for column in range(parameter_count):
        for sign in (-1.0, 1.0):
            point = tuple(
                state.mean[row] + sign * radius * lower[row][column]
                for row in range(parameter_count)
            )
            parameters = dict(zip(state.parameter_names, point))
            parameter_points.append(point)
            observation_points.append(response_for_parameters(action, parameters))

    weight = 1.0 / len(observation_points)
    observation_mean = tuple(
        sum(weight * point[axis] for point in observation_points)
        for axis in range(action.dimension)
    )
    signal_covariance = tuple(
        tuple(
            sum(
                weight
                * (point[row] - observation_mean[row])
                * (point[column] - observation_mean[column])
                for point in observation_points
            )
            for column in range(action.dimension)
        )
        for row in range(action.dimension)
    )
    cross_covariance = tuple(
        tuple(
            sum(
                weight
                * (parameter_point[row] - state.mean[row])
                * (observation_point[column] - observation_mean[column])
                for parameter_point, observation_point in zip(
                    parameter_points, observation_points
                )
            )
            for column in range(action.dimension)
        )
        for row in range(parameter_count)
    )
    return observation_mean, signal_covariance, cross_covariance


def initialize_ret_posterior(
    models: Sequence[RelationalModel],
    *,
    complexity_penalty: float = 1.0,
    open_model_prior: float = 0.02,
    open_model_scale: float = 1.0,
    explicit_model_priors: Mapping[str, float] | None = None,
) -> RETPosterior:
    if not 0.0 < open_model_prior < 1.0:
        raise ValueError("open-model prior must lie between zero and one")
    model_map = {model.name: model for model in models}
    if len(model_map) != len(models) or OPEN_MODEL_NAME in model_map:
        raise ValueError("model names must be unique and cannot use M_bottom")

    if explicit_model_priors is None:
        raw = {
            model.name: math.exp(-complexity_penalty * model.complexity)
            for model in models
        }
    else:
        if set(explicit_model_priors) != set(model_map):
            raise ValueError("explicit priors must cover every declared model")
        raw = dict(explicit_model_priors)
    raw_total = sum(raw.values())
    weights = {
        name: (1.0 - open_model_prior) * value / raw_total
        for name, value in raw.items()
    }
    weights[OPEN_MODEL_NAME] = open_model_prior

    parameters = {}
    for model in models:
        names = tuple(model.parameter_priors)
        mean = tuple(model.parameter_priors[name].mean for name in names)
        covariance = tuple(
            tuple(
                model.parameter_priors[name].standard_deviation**2 if row == column else 0.0
                for column, name in enumerate(names)
            )
            for row in range(len(names))
        )
        parameters[model.name] = GaussianParameterState(names, mean, covariance)
    return RETPosterior(model_map, weights, parameters, open_model_scale, 0)


def predictive_distribution(
    posterior: RETPosterior,
    model_name: str,
    action: RelationalAction,
    observation_noise: ObservationNoise,
) -> tuple[Vector, Matrix]:
    noise = _observation_covariance(observation_noise, action.dimension)
    if model_name == OPEN_MODEL_NAME:
        broad = [
            [
                posterior.open_model_scale**2 if row == column else 0.0
                for column in range(action.dimension)
            ]
            for row in range(action.dimension)
        ]
        covariance = tuple(tuple(row) for row in _add_matrix(broad, noise))
        return response_for_parameters(action, {}), covariance

    state = posterior.parameters[model_name]
    if action.is_nonlinear:
        mean, signal_covariance, _ = _cubature_moments(state, action)
        covariance = tuple(
            tuple(row) for row in _add_matrix(signal_covariance, noise)
        )
        return mean, covariance
    if not state.parameter_names:
        return response_for_parameters(action, {}), noise
    design = _design_matrix(action, state)
    predicted_increment = _matvec(design, state.mean)
    mean = tuple(
        action.known_response[axis] + predicted_increment[axis]
        for axis in range(action.dimension)
    )
    propagated = _matmul(_matmul(design, state.covariance), _transpose(design))
    covariance = tuple(tuple(row) for row in _add_matrix(propagated, noise))
    return mean, covariance


def gaussian_log_likelihood(observation: Sequence[float], mean: Sequence[float], covariance: Matrix) -> float:
    inverse, determinant = _inverse_and_determinant(covariance)
    if determinant <= 0.0:
        raise ValueError("predictive covariance must be positive definite")
    residual = [observation[index] - mean[index] for index in range(len(mean))]
    mahalanobis = sum(
        residual[row] * inverse[row][column] * residual[column]
        for row in range(len(mean))
        for column in range(len(mean))
    )
    dimension = len(mean)
    return -0.5 * (
        dimension * math.log(2.0 * math.pi) + math.log(determinant) + mahalanobis
    )


def _update_parameter_state(
    state: GaussianParameterState,
    action: RelationalAction,
    observation: Sequence[float],
    observation_noise: ObservationNoise,
) -> GaussianParameterState:
    if not state.parameter_names:
        return state
    noise = _observation_covariance(observation_noise, action.dimension)
    covariance = [list(row) for row in state.covariance]
    if action.is_nonlinear:
        predicted, signal_covariance, cross_covariance = _cubature_moments(
            state, action
        )
        innovation_covariance = _add_matrix(signal_covariance, noise)
        cross = [list(row) for row in cross_covariance]
    else:
        design = _design_matrix(action, state)
        predicted_increment = _matvec(design, state.mean)
        predicted = tuple(
            action.known_response[axis] + predicted_increment[axis]
            for axis in range(action.dimension)
        )
        signal_covariance = _matmul(
            _matmul(design, covariance), _transpose(design)
        )
        innovation_covariance = _add_matrix(signal_covariance, noise)
        cross = _matmul(covariance, _transpose(design))
    innovation = [
        observation[axis] - predicted[axis]
        for axis in range(action.dimension)
    ]
    innovation_inverse, _ = _inverse_and_determinant(innovation_covariance)
    gain = _matmul(cross, innovation_inverse)
    new_mean = tuple(
        state.mean[row] + sum(gain[row][axis] * innovation[axis] for axis in range(action.dimension))
        for row in range(len(state.parameter_names))
    )
    removed_covariance = _matmul(
        _matmul(gain, innovation_covariance), _transpose(gain)
    )
    symmetric = _symmetrize(_subtract_matrix(covariance, removed_covariance))
    if any(symmetric[index][index] < -1.0e-12 for index in range(len(symmetric))):
        raise ValueError("posterior covariance lost positive semidefiniteness")
    symmetric = tuple(
        tuple(
            max(value, 0.0) if row == column else value
            for column, value in enumerate(values)
        )
        for row, values in enumerate(symmetric)
    )
    return GaussianParameterState(state.parameter_names, new_mean, symmetric)


def update_ret_posterior(
    posterior: RETPosterior,
    action: RelationalAction,
    observation: Sequence[float],
    observation_noise: ObservationNoise,
) -> RETPosterior:
    if len(observation) != action.dimension:
        raise ValueError("observation dimension does not match action")
    log_weights = {}
    for name, prior_weight in posterior.model_weights.items():
        mean, covariance = predictive_distribution(
            posterior, name, action, observation_noise
        )
        log_weights[name] = math.log(max(prior_weight, 1.0e-300)) + gaussian_log_likelihood(
            observation, mean, covariance
        )
    maximum = max(log_weights.values())
    raw = {name: math.exp(value - maximum) for name, value in log_weights.items()}
    total = sum(raw.values())
    weights = {name: value / total for name, value in raw.items()}
    parameters = {
        name: _update_parameter_state(
            posterior.parameters[name], action, observation, observation_noise
        )
        for name in posterior.models
    }
    return RETPosterior(
        posterior.models,
        weights,
        parameters,
        posterior.open_model_scale,
        posterior.observations + 1,
    )


def question_probabilities(posterior: RETPosterior, question: Question) -> Dict[str, float]:
    probabilities: Dict[str, float] = {}
    for model_name, weight in posterior.model_weights.items():
        answer = question.answer(model_name)
        probabilities[answer] = probabilities.get(answer, 0.0) + weight
    return probabilities


def endpoint_inclusion_probability(posterior: RETPosterior, parameter_name: str) -> float:
    return sum(
        posterior.model_weights[name]
        for name, model in posterior.models.items()
        if parameter_name in model.parameter_priors
    )


def parameter_summary(
    posterior: RETPosterior,
    model_name: str,
) -> Dict[str, Dict[str, float | str]]:
    model = posterior.models[model_name]
    state = posterior.parameters[model_name]
    summary = {}
    for index, name in enumerate(state.parameter_names):
        standard_deviation = math.sqrt(max(state.covariance[index][index], 0.0))
        summary[name] = {
            "mean": state.mean[index],
            "standard_deviation": standard_deviation,
            "lower_95": state.mean[index] - 1.96 * standard_deviation,
            "upper_95": state.mean[index] + 1.96 * standard_deviation,
            "role": model.parameter_priors[name].role,
        }
    return summary


def parameter_covariance_after_action(
    posterior: RETPosterior,
    model_name: str,
    action: RelationalAction,
    observation_noise: ObservationNoise,
) -> Matrix:
    """Return the model's Gaussian covariance after a prospective action."""

    state = posterior.parameters[model_name]
    mean, _ = predictive_distribution(posterior, model_name, action, observation_noise)
    return _update_parameter_state(
        state,
        action,
        mean,
        observation_noise,
    ).covariance


def sample_predictive(
    posterior: RETPosterior,
    model_name: str,
    action: RelationalAction,
    observation_noise: ObservationNoise,
    rng: random.Random,
) -> Vector:
    mean, covariance = predictive_distribution(posterior, model_name, action, observation_noise)
    dimension = len(mean)
    lower = _cholesky(covariance)
    standard = [rng.gauss(0.0, 1.0) for _ in range(dimension)]
    return tuple(
        mean[row] + sum(lower[row][column] * standard[column] for column in range(row + 1))
        for row in range(dimension)
    )
