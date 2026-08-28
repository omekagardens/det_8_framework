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
    drift_standard_deviations: Mapping[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name or not self.family:
            raise ValueError("model name and family are required")
        if self.complexity < 0.0:
            raise ValueError("model complexity cannot be negative")
        undeclared = set(self.drift_standard_deviations) - set(self.parameter_priors)
        if undeclared:
            raise ValueError(
                "drift declared for undeclared parameters: %s"
                % ", ".join(sorted(undeclared))
            )
        if any(
            sd < 0.0 or not math.isfinite(sd)
            for sd in self.drift_standard_deviations.values()
        ):
            raise ValueError("drift standard deviations must be finite and non-negative")


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


@dataclass(frozen=True)
class MixtureParameterState:
    """A non-Gaussian parameter posterior as a weighted Gaussian mixture.

    Unlike :class:`GaussianParameterState`, a mixture preserves multimodal or
    strongly skewed parameter posteriors.  Each component is a plain Gaussian
    over the same parameter names, so the closed-form linear and
    cubature-propagated nonlinear updates remain usable per component.
    """

    parameter_names: Tuple[str, ...]
    components: Tuple[GaussianParameterState, ...]
    weights: Tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.components:
            raise ValueError("mixture must contain at least one component")
        if len(self.components) != len(self.weights):
            raise ValueError("mixture component and weight counts must match")
        if any(
            weight <= 0.0 or not math.isfinite(weight)
            for weight in self.weights
        ):
            raise ValueError("mixture weights must be positive and finite")
        if abs(sum(self.weights) - 1.0) > 1.0e-9:
            raise ValueError("mixture weights must sum to one")
        for component in self.components:
            if component.parameter_names != self.parameter_names:
                raise ValueError("all mixture components must share parameter names")


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


def predictive_for_state(
    state: GaussianParameterState,
    action: RelationalAction,
    observation_noise: ObservationNoise,
) -> tuple[Vector, Matrix]:
    """Predictive mean and covariance for one Gaussian parameter state."""

    noise = _observation_covariance(observation_noise, action.dimension)
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
    return predictive_for_state(
        posterior.parameters[model_name], action, observation_noise
    )


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
    """Return the model's Gaussian covariance after a prospective action.

    The predictive mean is used as the synthetic observation. Under this core's
    Gaussian moment approximation the covariance update is observation-
    independent for both linear and cubature-propagated nonlinear responses, so
    this equals the expected posterior covariance.
    """

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


def _logsumexp(values: Sequence[float]) -> float:
    maximum = max(values)
    return maximum + math.log(
        sum(math.exp(value - maximum) for value in values)
    )


def _add_drift(
    state: GaussianParameterState,
    drift_standard_deviations: Mapping[str, float],
    steps: int,
) -> GaussianParameterState:
    """Add per-parameter random-walk process noise to a Gaussian state."""

    covariance = [list(row) for row in state.covariance]
    for index, name in enumerate(state.parameter_names):
        increment = steps * drift_standard_deviations.get(name, 0.0) ** 2
        if increment:
            covariance[index][index] += increment
    return GaussianParameterState(
        state.parameter_names, state.mean, tuple(tuple(row) for row in covariance)
    )


def to_mixture(state: GaussianParameterState) -> MixtureParameterState:
    """Lift a single Gaussian into a one-component mixture."""

    return MixtureParameterState(state.parameter_names, (state,), (1.0,))


def mixture_log_likelihood(
    state: MixtureParameterState,
    action: RelationalAction,
    observation: Sequence[float],
    observation_noise: ObservationNoise,
) -> float:
    """Marginal log likelihood of an observation under the mixture."""

    terms = []
    for component, weight in zip(state.components, state.weights):
        mean, covariance = predictive_for_state(
            component, action, observation_noise
        )
        terms.append(
            math.log(weight)
            + gaussian_log_likelihood(observation, mean, covariance)
        )
    return _logsumexp(terms)


def update_mixture_state(
    state: MixtureParameterState,
    action: RelationalAction,
    observation: Sequence[float],
    observation_noise: ObservationNoise,
    *,
    minimum_component_weight: float = 1.0e-12,
) -> MixtureParameterState:
    """Kalman-update each component and reweight by predictive likelihood.

    Components are updated independently and reweighted by the predictive
    likelihood of the observation, so a multimodal parameter posterior is
    preserved rather than collapsed into a single Gaussian.  Components whose
    reweighted probability falls below ``minimum_component_weight`` are pruned.
    """

    if len(observation) != action.dimension:
        raise ValueError("observation dimension does not match action")
    updated_components = []
    log_weights = []
    for component, weight in zip(state.components, state.weights):
        mean, covariance = predictive_for_state(
            component, action, observation_noise
        )
        log_weights.append(
            math.log(weight)
            + gaussian_log_likelihood(observation, mean, covariance)
        )
        updated_components.append(
            _update_parameter_state(
                component, action, observation, observation_noise
            )
        )
    maximum = max(log_weights)
    weights = tuple(
        math.exp(log_weight - maximum) for log_weight in log_weights
    )
    total = sum(weights)
    weights = tuple(weight / total for weight in weights)

    kept_components = []
    kept_weights = []
    for component, weight in zip(updated_components, weights):
        if weight >= minimum_component_weight:
            kept_components.append(component)
            kept_weights.append(weight)
    if not kept_components:
        best = max(range(len(weights)), key=lambda index: weights[index])
        kept_components = [updated_components[best]]
        kept_weights = [1.0]
    else:
        total = sum(kept_weights)
        kept_weights = [weight / total for weight in kept_weights]
    return MixtureParameterState(
        state.parameter_names, tuple(kept_components), tuple(kept_weights)
    )


def collapse_mixture(state: MixtureParameterState) -> GaussianParameterState:
    """Moment-matched single Gaussian summary of a mixture."""

    size = len(state.parameter_names)
    mean = [0.0] * size
    for component, weight in zip(state.components, state.weights):
        for index in range(size):
            mean[index] += weight * component.mean[index]
    covariance = [[0.0] * size for _ in range(size)]
    for component, weight in zip(state.components, state.weights):
        delta = [component.mean[index] - mean[index] for index in range(size)]
        for row in range(size):
            for column in range(size):
                covariance[row][column] += weight * (
                    component.covariance[row][column]
                    + delta[row] * delta[column]
                )
    return GaussianParameterState(
        state.parameter_names, tuple(mean), tuple(tuple(row) for row in covariance)
    )


def evolve_mixture_state(
    state: MixtureParameterState,
    drift_standard_deviations: Mapping[str, float],
    steps: int = 1,
) -> MixtureParameterState:
    components = tuple(
        _add_drift(component, drift_standard_deviations, steps)
        for component in state.components
    )
    return MixtureParameterState(state.parameter_names, components, state.weights)


def evolve_ret_posterior(
    posterior: RETPosterior,
    steps: int = 1,
) -> RETPosterior:
    """Advance every model's parameter state by its declared drift.

    A random-walk evolution adds the declared process noise to each
    parameter's variance between separately committed actions.  Means are
    unchanged (symmetric drift), so the effect is purely to widen predictive
    uncertainty for stale states; the scheduler then assigns a larger expected
    information gain to a fresh measurement.
    """

    parameters = {
        name: _add_drift(
            posterior.parameters[name], model.drift_standard_deviations, steps
        )
        for name, model in posterior.models.items()
    }
    return RETPosterior(
        posterior.models,
        posterior.model_weights,
        parameters,
        posterior.open_model_scale,
        posterior.observations,
    )


def change_point_mixture(
    state: GaussianParameterState,
    drift_standard_deviations: Mapping[str, float],
    change_prior: float = 0.5,
) -> MixtureParameterState:
    """Two-component mixture for change-point detection.

    The first component is the stable parameter (no drift); the second is the
    same parameter advanced by the declared process noise.  Updating this
    mixture against an observation lets the record adjudicate whether a change
    occurred, mirroring the spike-and-slab idiom used for optional endpoints.
    """

    if not 0.0 < change_prior < 1.0:
        raise ValueError("change prior must lie between zero and one")
    return MixtureParameterState(
        state.parameter_names,
        (state, _add_drift(state, drift_standard_deviations, 1)),
        (1.0 - change_prior, change_prior),
    )


def change_probability(state: MixtureParameterState) -> float:
    """Posterior weight of the 'changed' component of a two-component mixture."""

    if len(state.components) != 2:
        raise ValueError("change probability requires exactly two components")
    return state.weights[1]
