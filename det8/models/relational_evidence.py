"""Likelihood-agnostic evidence inference for relational discovery.

This module complements :mod:`det8.models.relational_tomography`.  The older
core is intentionally optimized for Gaussian parameter states and vector
observations; this layer compares arbitrary *predictive distributions* while
preserving provenance, an explicit robust/open hypothesis, question-directed
action ranking, and prequential scoring.

The standard-library-only implementation is deliberately small and explicit.
Hypotheses supply predictive distributions and may optionally carry immutable
user-defined state.  Distribution parameters are therefore predictions made
before an evidence record is committed, rather than values fitted to that same
record.  Posterior weights are conditional support within the declared set;
they are not proof or ontology probabilities.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterable,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Union,
    runtime_checkable,
)


Number = Union[int, float]
Observation = Any
OPEN_EVIDENCE_NAME = "M_bottom"
EVIDENCE_POSTERIOR_WARNING = (
    "Evidence posterior probability is conditional predictive support within "
    "the declared hypothesis set; it is not a proof or ontology probability."
)


def _freeze_evidence_value(value: object, label: str = "evidence value") -> object:
    """Recursively copy JSON-like evidence into immutable containers.

    The evidence core intentionally accepts a small, serialization-friendly
    value algebra.  Rejecting opaque mutable objects is preferable to making a
    frozen dataclass whose payload can still change through an external alias.
    """

    if value is None or isinstance(value, (str, bytes, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("%s contains a non-finite float" % label)
        return value
    if isinstance(value, Mapping):
        frozen = {}
        for key, item in value.items():
            if not isinstance(key, str) or not key:
                raise ValueError("%s mapping keys must be nonempty strings" % label)
            frozen[key] = _freeze_evidence_value(item, label)
        return MappingProxyType(frozen)
    if isinstance(value, (tuple, list)):
        return tuple(_freeze_evidence_value(item, label) for item in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(_freeze_evidence_value(item, label) for item in value)
    if isinstance(value, bytearray):
        return bytes(value)
    raise TypeError(
        "%s must contain only scalars, mappings, sequences, sets, or bytes"
        % label
    )


def _canonical_evidence_value(value: object) -> object:
    """Return a deterministic, type-tagged representation for a payload."""

    if value is None:
        return ["none"]
    if isinstance(value, bool):
        return ["bool", value]
    if isinstance(value, int):
        return ["int", str(value)]
    if isinstance(value, str):
        return ["str", value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("evidence payload contains a non-finite float")
        return ["float", value.hex()]
    if isinstance(value, bytes):
        return ["bytes", value.hex()]
    if isinstance(value, Mapping):
        result = []
        for key, item in value.items():
            if not isinstance(key, str) or not key:
                raise ValueError(
                    "evidence payload mapping keys must be nonempty strings"
                )
            result.append([key, _canonical_evidence_value(item)])
        result.sort(key=lambda item: item[0])
        return ["mapping", result]
    if isinstance(value, (tuple, list)):
        return ["sequence", [_canonical_evidence_value(item) for item in value]]
    if isinstance(value, (set, frozenset)):
        encoded = [_canonical_evidence_value(item) for item in value]
        encoded.sort(
            key=lambda item: json.dumps(
                item, sort_keys=True, separators=(",", ":"), allow_nan=False
            )
        )
        return ["set", encoded]
    if isinstance(value, bytearray):
        return ["bytes", bytes(value).hex()]
    raise TypeError("evidence payload is not canonically serializable")


def evidence_payload_digest(value: object) -> str:
    """Return the canonical SHA-256 digest required by ``EvidenceRecord``."""

    payload = json.dumps(
        _canonical_evidence_value(value),
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _immutable_mapping(values: Optional[Mapping[str, object]]) -> Mapping[str, object]:
    """Return a recursively immutable copy suitable for a frozen record."""

    frozen = _freeze_evidence_value(dict(values or {}), "metadata")
    assert isinstance(frozen, Mapping)
    return frozen


def _is_real(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _finite_float(value: object, label: str) -> float:
    if not _is_real(value):
        raise ValueError("%s must be a real number" % label)
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("%s must be finite" % label)
    return result


def _count(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError("%s must be a nonnegative integer" % label)
    return value


def _probability(value: object, label: str, *, open_interval: bool = False) -> float:
    result = _finite_float(value, label)
    valid = 0.0 < result < 1.0 if open_interval else 0.0 <= result <= 1.0
    if not valid:
        interval = "(0, 1)" if open_interval else "[0, 1]"
        raise ValueError("%s must lie in %s" % (label, interval))
    return result


def _log_or_impossible(probability: float, count: int) -> float:
    if count == 0:
        return 0.0
    if probability == 0.0:
        return -math.inf
    return count * math.log(probability)


def _logsumexp(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("log-sum-exp requires at least one value")
    maximum = max(values)
    if maximum == -math.inf:
        return -math.inf
    return maximum + math.log(sum(math.exp(value - maximum) for value in values))


def _log_weight(value: float) -> float:
    """Preserve exact zero support rather than resurrecting it with a floor."""

    return -math.inf if value == 0.0 else math.log(value)


def _stable_seed(seed: int, hypothesis_name: str, sample_index: int) -> int:
    """Derive a seed independent of candidate-action ordering."""

    payload = "%s\x1f%s\x1f%s" % (seed, hypothesis_name, sample_index)
    return int.from_bytes(hashlib.sha256(payload.encode("utf-8")).digest()[:8], "big")


def _validate_probabilities(probabilities: Iterable[object]) -> Tuple[float, ...]:
    values = tuple(_probability(value, "category probability") for value in probabilities)
    if len(values) < 2:
        raise ValueError("categorical distributions require at least two categories")
    if abs(sum(values) - 1.0) > 1.0e-12:
        raise ValueError("category probabilities must sum to one")
    if not any(value > 0.0 for value in values):
        raise ValueError("at least one category probability must be positive")
    return values


def _validate_count_vector(
    observation: object,
    dimension: int,
    trials: int,
) -> Tuple[int, ...]:
    if isinstance(observation, (str, bytes)) or not isinstance(observation, Sequence):
        raise ValueError("count-vector observation must be a sequence")
    counts = tuple(_count(value, "category count") for value in observation)
    if len(counts) != dimension:
        raise ValueError("count-vector dimension does not match distribution")
    if sum(counts) != trials:
        raise ValueError("category counts must sum to the declared trial count")
    return counts


def _binomial_sample(trials: int, probability: float, rng: random.Random) -> int:
    return sum(rng.random() < probability for _ in range(trials))


def _poisson_sample(rate: float, rng: random.Random) -> int:
    """Draw a Poisson variate using inversion or PTRS rejection."""

    if rate == 0.0:
        return 0
    if rate < 30.0:
        threshold = math.exp(-rate)
        product = 1.0
        count = 0
        while product > threshold:
            count += 1
            product *= rng.random()
        return count - 1

    # Hörmann's transformed-rejection method (PTRS).
    root = math.sqrt(rate)
    b = 0.931 + 2.53 * root
    a = -0.059 + 0.02483 * b
    inverse_alpha = 1.1239 + 1.1328 / (b - 3.4)
    squeeze = 0.9277 - 3.6224 / (b - 2.0)
    while True:
        u = rng.random() - 0.5
        v = rng.random()
        us = 0.5 - abs(u)
        candidate = math.floor((2.0 * a / us + b) * u + rate + 0.43)
        if us >= 0.07 and v <= squeeze:
            return int(candidate)
        if candidate < 0 or (us < 0.013 and v > us):
            continue
        acceptance = math.log(
            v * inverse_alpha / (a / (us * us) + b)
        )
        target = -rate + candidate * math.log(rate) - math.lgamma(candidate + 1.0)
        if acceptance <= target:
            return int(candidate)


def _multinomial_sample(
    trials: int,
    probabilities: Sequence[float],
    rng: random.Random,
) -> Tuple[int, ...]:
    counts = [0] * len(probabilities)
    cumulative = []
    running = 0.0
    for probability in probabilities:
        running += probability
        cumulative.append(running)
    cumulative[-1] = 1.0
    for _ in range(trials):
        draw = rng.random()
        for index, boundary in enumerate(cumulative):
            if draw < boundary:
                counts[index] += 1
                break
    return tuple(counts)


@runtime_checkable
class PredictiveDistribution(Protocol):
    """Structural interface used by evidence hypotheses and the scheduler."""

    family: str

    def validate(self, observation: Observation) -> None:
        """Raise :class:`ValueError` when an observation is outside support."""

    def log_prob(self, observation: Observation) -> float:
        """Return the normalized predictive log probability or log density."""

    def sample(self, rng: random.Random) -> Observation:
        """Draw one predictive observation using the supplied generator."""

    def mean(self) -> object:
        """Return the predictive mean when it exists, otherwise ``None``."""

    def diagnostics(self, observation: Optional[Observation] = None) -> Mapping[str, object]:
        """Return distribution metadata and optional observation diagnostics."""


@dataclass(frozen=True)
class Gaussian:
    """Univariate or multivariate Gaussian with variance/covariance input."""

    location: Union[Number, Sequence[Number]]
    covariance: Union[Number, Sequence[Sequence[Number]]]
    family: ClassVar[str] = "gaussian"
    _location: Tuple[float, ...] = field(init=False, repr=False)
    _covariance: Tuple[Tuple[float, ...], ...] = field(init=False, repr=False)
    _cholesky: Tuple[Tuple[float, ...], ...] = field(init=False, repr=False)
    _scalar: bool = field(init=False, repr=False)

    def __post_init__(self) -> None:
        scalar = _is_real(self.location)
        if scalar:
            location = (_finite_float(self.location, "Gaussian location"),)
        else:
            if isinstance(self.location, (str, bytes)) or not isinstance(
                self.location, Sequence
            ):
                raise ValueError("Gaussian location must be a number or sequence")
            location = tuple(
                _finite_float(value, "Gaussian location") for value in self.location
            )
            if not location:
                raise ValueError("Gaussian location cannot be empty")

        dimension = len(location)
        if _is_real(self.covariance):
            variance = _finite_float(self.covariance, "Gaussian variance")
            if variance <= 0.0:
                raise ValueError("Gaussian variance must be positive")
            covariance = tuple(
                tuple(variance if row == column else 0.0 for column in range(dimension))
                for row in range(dimension)
            )
        else:
            if isinstance(self.covariance, (str, bytes)) or not isinstance(
                self.covariance, Sequence
            ):
                raise ValueError("Gaussian covariance must be numeric or square")
            covariance = tuple(
                tuple(_finite_float(value, "Gaussian covariance") for value in row)
                for row in self.covariance
            )
            if len(covariance) != dimension or any(
                len(row) != dimension for row in covariance
            ):
                raise ValueError("Gaussian covariance dimension does not match location")
            for row in range(dimension):
                for column in range(dimension):
                    if abs(covariance[row][column] - covariance[column][row]) > 1.0e-12:
                        raise ValueError("Gaussian covariance must be symmetric")

        lower = [[0.0] * dimension for _ in range(dimension)]
        for row in range(dimension):
            for column in range(row + 1):
                remainder = covariance[row][column] - sum(
                    lower[row][inner] * lower[column][inner]
                    for inner in range(column)
                )
                if row == column:
                    if remainder <= 0.0:
                        raise ValueError("Gaussian covariance must be positive definite")
                    lower[row][column] = math.sqrt(remainder)
                else:
                    lower[row][column] = remainder / lower[column][column]

        object.__setattr__(self, "_location", location)
        object.__setattr__(self, "_covariance", covariance)
        object.__setattr__(self, "_cholesky", tuple(tuple(row) for row in lower))
        object.__setattr__(self, "_scalar", scalar)

    def _observation(self, observation: Observation) -> Tuple[float, ...]:
        if self._scalar:
            return (_finite_float(observation, "Gaussian observation"),)
        if isinstance(observation, (str, bytes)) or not isinstance(observation, Sequence):
            raise ValueError("multivariate Gaussian observation must be a sequence")
        vector = tuple(_finite_float(value, "Gaussian observation") for value in observation)
        if len(vector) != len(self._location):
            raise ValueError("Gaussian observation dimension does not match location")
        return vector

    def validate(self, observation: Observation) -> None:
        self._observation(observation)

    def _mahalanobis(self, observation: Observation) -> float:
        residual = [
            value - center for value, center in zip(self._observation(observation), self._location)
        ]
        solved = [0.0] * len(residual)
        for row in range(len(residual)):
            solved[row] = (
                residual[row]
                - sum(self._cholesky[row][column] * solved[column] for column in range(row))
            ) / self._cholesky[row][row]
        return sum(value * value for value in solved)

    def log_prob(self, observation: Observation) -> float:
        dimension = len(self._location)
        log_determinant = 2.0 * sum(
            math.log(self._cholesky[index][index]) for index in range(dimension)
        )
        return -0.5 * (
            dimension * math.log(2.0 * math.pi)
            + log_determinant
            + self._mahalanobis(observation)
        )

    def sample(self, rng: random.Random) -> Observation:
        standard = [rng.gauss(0.0, 1.0) for _ in self._location]
        value = tuple(
            self._location[row]
            + sum(
                self._cholesky[row][column] * standard[column]
                for column in range(row + 1)
            )
            for row in range(len(self._location))
        )
        return value[0] if self._scalar else value

    def mean(self) -> object:
        return self._location[0] if self._scalar else self._location

    def diagnostics(self, observation: Optional[Observation] = None) -> Mapping[str, object]:
        result: Dict[str, object] = {
            "family": self.family,
            "dimension": len(self._location),
            "mean": self.mean(),
            "covariance": self._covariance,
        }
        if observation is not None:
            result.update(
                log_probability=self.log_prob(observation),
                mahalanobis_squared=self._mahalanobis(observation),
            )
        return result


@dataclass(frozen=True)
class StudentT:
    """Univariate Student-t distribution using a positive scale parameter."""

    location: float
    scale: float
    degrees_of_freedom: float
    family: ClassVar[str] = "student_t"

    def __post_init__(self) -> None:
        object.__setattr__(self, "location", _finite_float(self.location, "Student-t location"))
        scale = _finite_float(self.scale, "Student-t scale")
        degrees = _finite_float(self.degrees_of_freedom, "Student-t degrees of freedom")
        if scale <= 0.0 or degrees <= 0.0:
            raise ValueError("Student-t scale and degrees of freedom must be positive")
        object.__setattr__(self, "scale", scale)
        object.__setattr__(self, "degrees_of_freedom", degrees)

    def validate(self, observation: Observation) -> None:
        _finite_float(observation, "Student-t observation")

    def log_prob(self, observation: Observation) -> float:
        value = _finite_float(observation, "Student-t observation")
        degrees = self.degrees_of_freedom
        standardized_squared = ((value - self.location) / self.scale) ** 2
        return (
            math.lgamma((degrees + 1.0) / 2.0)
            - math.lgamma(degrees / 2.0)
            - 0.5 * math.log(degrees * math.pi)
            - math.log(self.scale)
            - (degrees + 1.0) / 2.0 * math.log1p(standardized_squared / degrees)
        )

    def sample(self, rng: random.Random) -> float:
        numerator = rng.gauss(0.0, 1.0)
        denominator = math.sqrt(
            rng.gammavariate(self.degrees_of_freedom / 2.0, 2.0)
            / self.degrees_of_freedom
        )
        return self.location + self.scale * numerator / denominator

    def mean(self) -> Optional[float]:
        return self.location if self.degrees_of_freedom > 1.0 else None

    def diagnostics(self, observation: Optional[Observation] = None) -> Mapping[str, object]:
        variance = (
            self.scale**2 * self.degrees_of_freedom / (self.degrees_of_freedom - 2.0)
            if self.degrees_of_freedom > 2.0
            else None
        )
        result: Dict[str, object] = {
            "family": self.family,
            "mean": self.mean(),
            "variance": variance,
            "degrees_of_freedom": self.degrees_of_freedom,
        }
        if observation is not None:
            result["log_probability"] = self.log_prob(observation)
        return result


@dataclass(frozen=True)
class Binomial:
    """Binomial predictive distribution for a fixed number of trials."""

    trials: int
    probability: float
    family: ClassVar[str] = "binomial"

    def __post_init__(self) -> None:
        object.__setattr__(self, "trials", _count(self.trials, "binomial trials"))
        object.__setattr__(self, "probability", _probability(self.probability, "binomial probability"))

    def validate(self, observation: Observation) -> None:
        value = _count(observation, "binomial observation")
        if value > self.trials:
            raise ValueError("binomial observation cannot exceed trials")

    def log_prob(self, observation: Observation) -> float:
        self.validate(observation)
        count = int(observation)
        failures = self.trials - count
        return (
            math.lgamma(self.trials + 1.0)
            - math.lgamma(count + 1.0)
            - math.lgamma(failures + 1.0)
            + _log_or_impossible(self.probability, count)
            + _log_or_impossible(1.0 - self.probability, failures)
        )

    def sample(self, rng: random.Random) -> int:
        return _binomial_sample(self.trials, self.probability, rng)

    def mean(self) -> float:
        return self.trials * self.probability

    def diagnostics(self, observation: Optional[Observation] = None) -> Mapping[str, object]:
        variance = self.trials * self.probability * (1.0 - self.probability)
        result: Dict[str, object] = {
            "family": self.family,
            "mean": self.mean(),
            "variance": variance,
            "trials": self.trials,
        }
        if observation is not None:
            result["log_probability"] = self.log_prob(observation)
        return result


@dataclass(frozen=True)
class BetaBinomial:
    """Overdispersed binomial with a beta-distributed success probability."""

    trials: int
    alpha: float
    beta: float
    family: ClassVar[str] = "beta_binomial"

    def __post_init__(self) -> None:
        object.__setattr__(self, "trials", _count(self.trials, "beta-binomial trials"))
        alpha = _finite_float(self.alpha, "beta-binomial alpha")
        beta = _finite_float(self.beta, "beta-binomial beta")
        if alpha <= 0.0 or beta <= 0.0:
            raise ValueError("beta-binomial concentrations must be positive")
        object.__setattr__(self, "alpha", alpha)
        object.__setattr__(self, "beta", beta)

    def validate(self, observation: Observation) -> None:
        value = _count(observation, "beta-binomial observation")
        if value > self.trials:
            raise ValueError("beta-binomial observation cannot exceed trials")

    def log_prob(self, observation: Observation) -> float:
        self.validate(observation)
        count = int(observation)
        failures = self.trials - count
        return (
            math.lgamma(self.trials + 1.0)
            - math.lgamma(count + 1.0)
            - math.lgamma(failures + 1.0)
            + math.lgamma(count + self.alpha)
            + math.lgamma(failures + self.beta)
            - math.lgamma(self.trials + self.alpha + self.beta)
            - math.lgamma(self.alpha)
            - math.lgamma(self.beta)
            + math.lgamma(self.alpha + self.beta)
        )

    def sample(self, rng: random.Random) -> int:
        probability = rng.betavariate(self.alpha, self.beta)
        return _binomial_sample(self.trials, probability, rng)

    def mean(self) -> float:
        return self.trials * self.alpha / (self.alpha + self.beta)

    def diagnostics(self, observation: Optional[Observation] = None) -> Mapping[str, object]:
        total = self.alpha + self.beta
        variance = (
            self.trials
            * self.alpha
            * self.beta
            * (total + self.trials)
            / (total * total * (total + 1.0))
        )
        result: Dict[str, object] = {
            "family": self.family,
            "mean": self.mean(),
            "variance": variance,
            "trials": self.trials,
            "concentration": total,
        }
        if observation is not None:
            result["log_probability"] = self.log_prob(observation)
        return result


@dataclass(frozen=True)
class Poisson:
    """Poisson predictive distribution for nonnegative integer counts."""

    rate: float
    family: ClassVar[str] = "poisson"

    def __post_init__(self) -> None:
        rate = _finite_float(self.rate, "Poisson rate")
        if rate < 0.0:
            raise ValueError("Poisson rate cannot be negative")
        object.__setattr__(self, "rate", rate)

    def validate(self, observation: Observation) -> None:
        _count(observation, "Poisson observation")

    def log_prob(self, observation: Observation) -> float:
        count = _count(observation, "Poisson observation")
        if self.rate == 0.0:
            return 0.0 if count == 0 else -math.inf
        return count * math.log(self.rate) - self.rate - math.lgamma(count + 1.0)

    def sample(self, rng: random.Random) -> int:
        return _poisson_sample(self.rate, rng)

    def mean(self) -> float:
        return self.rate

    def diagnostics(self, observation: Optional[Observation] = None) -> Mapping[str, object]:
        result: Dict[str, object] = {
            "family": self.family,
            "mean": self.rate,
            "variance": self.rate,
        }
        if observation is not None:
            result["log_probability"] = self.log_prob(observation)
        return result


@dataclass(frozen=True)
class NegativeBinomial:
    """Negative binomial count before ``dispersion`` successes.

    ``dispersion`` may be nonintegral.  With success probability ``p``, the
    mean count is ``dispersion * (1-p) / p``.
    """

    dispersion: float
    success_probability: float
    family: ClassVar[str] = "negative_binomial"

    def __post_init__(self) -> None:
        dispersion = _finite_float(self.dispersion, "negative-binomial dispersion")
        if dispersion <= 0.0:
            raise ValueError("negative-binomial dispersion must be positive")
        probability = _probability(
            self.success_probability,
            "negative-binomial success probability",
            open_interval=True,
        )
        object.__setattr__(self, "dispersion", dispersion)
        object.__setattr__(self, "success_probability", probability)

    def validate(self, observation: Observation) -> None:
        _count(observation, "negative-binomial observation")

    def log_prob(self, observation: Observation) -> float:
        count = _count(observation, "negative-binomial observation")
        probability = self.success_probability
        return (
            math.lgamma(count + self.dispersion)
            - math.lgamma(self.dispersion)
            - math.lgamma(count + 1.0)
            + self.dispersion * math.log(probability)
            + count * math.log1p(-probability)
        )

    def sample(self, rng: random.Random) -> int:
        scale = (1.0 - self.success_probability) / self.success_probability
        rate = rng.gammavariate(self.dispersion, scale)
        return _poisson_sample(rate, rng)

    def mean(self) -> float:
        return self.dispersion * (1.0 - self.success_probability) / self.success_probability

    def diagnostics(self, observation: Optional[Observation] = None) -> Mapping[str, object]:
        variance = (
            self.dispersion
            * (1.0 - self.success_probability)
            / self.success_probability**2
        )
        result: Dict[str, object] = {
            "family": self.family,
            "mean": self.mean(),
            "variance": variance,
            "dispersion": self.dispersion,
        }
        if observation is not None:
            result["log_probability"] = self.log_prob(observation)
        return result


@dataclass(frozen=True)
class Multinomial:
    """Multinomial distribution over a fixed count-vector dimension."""

    trials: int
    probabilities: Sequence[float]
    family: ClassVar[str] = "multinomial"

    def __post_init__(self) -> None:
        object.__setattr__(self, "trials", _count(self.trials, "multinomial trials"))
        object.__setattr__(self, "probabilities", _validate_probabilities(self.probabilities))

    def validate(self, observation: Observation) -> None:
        _validate_count_vector(observation, len(self.probabilities), self.trials)

    def log_prob(self, observation: Observation) -> float:
        counts = _validate_count_vector(observation, len(self.probabilities), self.trials)
        value = math.lgamma(self.trials + 1.0) - sum(
            math.lgamma(count + 1.0) for count in counts
        )
        for count, probability in zip(counts, self.probabilities):
            term = _log_or_impossible(probability, count)
            if term == -math.inf:
                return -math.inf
            value += term
        return value

    def sample(self, rng: random.Random) -> Tuple[int, ...]:
        return _multinomial_sample(self.trials, self.probabilities, rng)

    def mean(self) -> Tuple[float, ...]:
        return tuple(self.trials * probability for probability in self.probabilities)

    def diagnostics(self, observation: Optional[Observation] = None) -> Mapping[str, object]:
        result: Dict[str, object] = {
            "family": self.family,
            "mean": self.mean(),
            "trials": self.trials,
            "probabilities": self.probabilities,
        }
        if observation is not None:
            counts = _validate_count_vector(
                observation, len(self.probabilities), self.trials
            )
            result["log_probability"] = self.log_prob(counts)
            result["pearson_statistic"] = sum(
                (count - expected) ** 2 / expected
                for count, expected in zip(counts, self.mean())
                if expected > 0.0
            )
        return result


@dataclass(frozen=True)
class DirichletMultinomial:
    """Overdispersed multinomial with positive Dirichlet concentrations."""

    trials: int
    concentration: Sequence[float]
    family: ClassVar[str] = "dirichlet_multinomial"

    def __post_init__(self) -> None:
        object.__setattr__(self, "trials", _count(self.trials, "Dirichlet-multinomial trials"))
        values = tuple(
            _finite_float(value, "Dirichlet concentration") for value in self.concentration
        )
        if len(values) < 2 or any(value <= 0.0 for value in values):
            raise ValueError("Dirichlet concentrations must contain at least two positive values")
        object.__setattr__(self, "concentration", values)

    @property
    def probabilities(self) -> Tuple[float, ...]:
        total = sum(self.concentration)
        return tuple(value / total for value in self.concentration)

    def validate(self, observation: Observation) -> None:
        _validate_count_vector(observation, len(self.concentration), self.trials)

    def log_prob(self, observation: Observation) -> float:
        counts = _validate_count_vector(observation, len(self.concentration), self.trials)
        total = sum(self.concentration)
        return (
            math.lgamma(self.trials + 1.0)
            - sum(math.lgamma(count + 1.0) for count in counts)
            + math.lgamma(total)
            - math.lgamma(total + self.trials)
            + sum(
                math.lgamma(alpha + count) - math.lgamma(alpha)
                for alpha, count in zip(self.concentration, counts)
            )
        )

    def sample(self, rng: random.Random) -> Tuple[int, ...]:
        draws = tuple(rng.gammavariate(alpha, 1.0) for alpha in self.concentration)
        total = sum(draws)
        probabilities = tuple(value / total for value in draws)
        return _multinomial_sample(self.trials, probabilities, rng)

    def mean(self) -> Tuple[float, ...]:
        return tuple(self.trials * probability for probability in self.probabilities)

    def diagnostics(self, observation: Optional[Observation] = None) -> Mapping[str, object]:
        result: Dict[str, object] = {
            "family": self.family,
            "mean": self.mean(),
            "trials": self.trials,
            "probabilities": self.probabilities,
            "total_concentration": sum(self.concentration),
        }
        if observation is not None:
            result["log_probability"] = self.log_prob(observation)
        return result


@dataclass(frozen=True)
class EvidenceAction:
    """A prospective evidence-producing action used by adaptive ranking.

    ``family`` names the observation schema presented to predictive factories;
    competing hypotheses may intentionally emit different distribution
    families for that same schema.
    """

    name: str
    family: str
    coordinate: Optional[float] = None
    metadata: Mapping[str, object] = field(default_factory=dict)
    cost: float = 0.0

    def __post_init__(self) -> None:
        if not self.name or not self.family:
            raise ValueError("evidence action name and family are required")
        if self.coordinate is not None:
            object.__setattr__(self, "coordinate", _finite_float(self.coordinate, "action coordinate"))
        cost = _finite_float(self.cost, "action cost")
        if cost < 0.0:
            raise ValueError("action cost cannot be negative")
        object.__setattr__(self, "cost", cost)
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))


@dataclass(frozen=True)
class EvidenceRecord:
    """Immutable evidence plus provenance.

    ``source_ids`` identify atomic data inputs. A coherent joint likelihood is
    encoded as one record with ``joint=True`` and every constituent source
    listed once. The flag never authorizes overlap with an earlier record.
    ``digest`` must be the canonical SHA-256 of ``observation``; construction
    rejects a mismatch. ``scope`` distinguishes, for example, statistical
    evidence from bounded exact computation. ``family`` is the observation
    schema label, not a requirement that every hypothesis use one distribution
    family.
    """

    record_id: str
    source_ids: Sequence[str]
    action: str
    coordinate: Optional[float]
    digest: str
    family: str
    scope: str
    observation: Observation
    metadata: Mapping[str, object] = field(default_factory=dict)
    joint: bool = False

    def __post_init__(self) -> None:
        if not self.record_id or not self.action or not self.digest:
            raise ValueError("record ID, action, and digest are required")
        if not self.family or not self.scope:
            raise ValueError("record family and scope are required")
        if isinstance(self.source_ids, (str, bytes)) or not isinstance(
            self.source_ids, Sequence
        ):
            raise ValueError("source IDs must be a sequence of strings")
        sources = tuple(self.source_ids)
        if not sources or any(
            not isinstance(value, str) or not value for value in sources
        ):
            raise ValueError("evidence records require nonempty source IDs")
        if len(set(sources)) != len(sources):
            raise ValueError("source IDs must be unique within an evidence record")
        if self.coordinate is not None:
            object.__setattr__(self, "coordinate", _finite_float(self.coordinate, "record coordinate"))
        if not isinstance(self.joint, bool):
            raise ValueError("joint flag must be Boolean")
        expected_digest = evidence_payload_digest(self.observation)
        if self.digest != expected_digest:
            raise ValueError(
                "record digest does not match the canonical observation payload"
            )
        object.__setattr__(self, "source_ids", sources)
        object.__setattr__(
            self,
            "observation",
            _freeze_evidence_value(self.observation, "record observation"),
        )
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))

    def as_action(self) -> EvidenceAction:
        """Return the prospective-action view used by hypothesis factories."""

        cost = self.metadata.get("cost", 0.0)
        return EvidenceAction(
            self.action,
            self.family,
            self.coordinate,
            self.metadata,
            float(cost) if _is_real(cost) else 0.0,
        )


@dataclass(frozen=True)
class EvidenceLedger:
    """Persistent provenance ledger with duplicate and overlap protection."""

    records: Sequence[EvidenceRecord] = ()

    def __post_init__(self) -> None:
        records = tuple(self.records)
        identifiers = set()
        sources = set()
        for record in records:
            if not isinstance(record, EvidenceRecord):
                raise ValueError("evidence ledger accepts EvidenceRecord values only")
            if record.record_id in identifiers:
                raise ValueError("duplicate evidence record ID: %s" % record.record_id)
            overlap = sources.intersection(record.source_ids)
            if overlap:
                raise ValueError(
                    "evidence sources may occur in only one record; encode a "
                    "joint likelihood as one record: %s"
                    % ", ".join(sorted(overlap))
                )
            identifiers.add(record.record_id)
            sources.update(record.source_ids)
        object.__setattr__(self, "records", records)

    def append(self, record: EvidenceRecord) -> "EvidenceLedger":
        """Return a new ledger containing ``record`` after provenance checks."""

        if any(item.record_id == record.record_id for item in self.records):
            raise ValueError("duplicate evidence record ID: %s" % record.record_id)
        existing_sources = {
            source for item in self.records for source in item.source_ids
        }
        overlap = existing_sources.intersection(record.source_ids)
        if overlap:
            raise ValueError(
                "evidence sources may occur in only one record; encode a "
                "joint likelihood as one record: %s"
                % ", ".join(sorted(overlap))
            )
        return EvidenceLedger(self.records + (record,))

    add = append

    @property
    def record_ids(self) -> Tuple[str, ...]:
        return tuple(record.record_id for record in self.records)

    @property
    def source_ids(self) -> Tuple[str, ...]:
        return tuple(
            sorted({source for record in self.records for source in record.source_ids})
        )


PredictiveFactory = Callable[[EvidenceAction, object], PredictiveDistribution]
StateUpdater = Callable[[object, EvidenceRecord, PredictiveDistribution], object]


@dataclass(frozen=True)
class EvidenceHypothesis:
    """A relational hypothesis that emits normalized predictive distributions."""

    name: str
    family: str
    predictive: PredictiveFactory = field(repr=False, compare=False)
    complexity: float = 0.0
    initial_state: object = None
    state_update: Optional[StateUpdater] = field(default=None, repr=False, compare=False)
    robust: bool = False
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name or not self.family or not callable(self.predictive):
            raise ValueError("hypothesis name, family, and predictive factory are required")
        complexity = _finite_float(self.complexity, "hypothesis complexity")
        if complexity < 0.0:
            raise ValueError("hypothesis complexity cannot be negative")
        if self.state_update is not None and not callable(self.state_update):
            raise ValueError("state updater must be callable")
        if not isinstance(self.robust, bool):
            raise ValueError("robust flag must be Boolean")
        object.__setattr__(self, "complexity", complexity)
        object.__setattr__(
            self,
            "initial_state",
            _freeze_evidence_value(self.initial_state, "hypothesis state"),
        )
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))

    def distribution(self, action: EvidenceAction, state: object) -> PredictiveDistribution:
        distribution = self.predictive(action, state)
        required = ("validate", "log_prob", "sample", "mean", "diagnostics")
        if not all(callable(getattr(distribution, item, None)) for item in required):
            raise TypeError("predictive factory did not return a PredictiveDistribution")
        if not isinstance(getattr(distribution, "family", None), str):
            raise TypeError("predictive distribution must declare a family")
        return distribution


@dataclass(frozen=True)
class EvidenceQuestion:
    """Map hypotheses to answers so scheduling can target a scientific question."""

    name: str
    answer_by_hypothesis: Mapping[str, str]
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("evidence question name is required")
        answers = dict(self.answer_by_hypothesis)
        if not answers or any(not key or not value for key, value in answers.items()):
            raise ValueError("question answers must be nonempty")
        object.__setattr__(self, "answer_by_hypothesis", MappingProxyType(answers))

    def answer(self, hypothesis_name: str) -> str:
        if hypothesis_name == OPEN_EVIDENCE_NAME:
            return "model_inadequate"
        try:
            return self.answer_by_hypothesis[hypothesis_name]
        except KeyError:
            raise ValueError("question does not cover hypothesis %s" % hypothesis_name)


@dataclass(frozen=True)
class EvidencePosterior:
    """Immutable model support, optional states, provenance, and log scores.

    Normalized ``log_weights`` are authoritative. ``weights`` is their
    display-space projection and may underflow to zero without turning a
    mathematically nonzero hypothesis into a structural impossibility.
    """

    hypotheses: Mapping[str, EvidenceHypothesis]
    weights: Mapping[str, float]
    states: Mapping[str, object]
    ledger: EvidenceLedger
    cumulative_log_scores: Mapping[str, float]
    mixture_prequential_log_score: float = 0.0
    observations: int = 0
    log_weights: Mapping[str, float] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        hypotheses = dict(self.hypotheses)
        supplied_weights = {
            name: float(value) for name, value in self.weights.items()
        }
        states = {
            name: _freeze_evidence_value(value, "posterior state")
            for name, value in self.states.items()
        }
        scores = {name: float(value) for name, value in self.cumulative_log_scores.items()}
        names = set(hypotheses)
        if OPEN_EVIDENCE_NAME not in names:
            raise ValueError("evidence posterior requires explicit M_bottom")
        if not hypotheses[OPEN_EVIDENCE_NAME].robust:
            raise ValueError("M_bottom must be declared robust")
        if (
            set(supplied_weights) != names
            or set(states) != names
            or set(scores) != names
        ):
            raise ValueError("weights, states, and scores must cover every hypothesis")
        if any(
            not math.isfinite(value) or value < 0.0
            for value in supplied_weights.values()
        ):
            raise ValueError("posterior weights must be finite and nonnegative")
        if abs(sum(supplied_weights.values()) - 1.0) > 1.0e-9:
            raise ValueError("posterior weights must sum to one")
        if self.log_weights:
            log_weights = {
                name: float(value) for name, value in self.log_weights.items()
            }
            if set(log_weights) != names:
                raise ValueError("log weights must cover every hypothesis")
            if any(
                math.isnan(value) or value == math.inf
                for value in log_weights.values()
            ):
                raise ValueError("log weights must be finite or -infinity")
            normalization = _logsumexp(tuple(log_weights.values()))
            if normalization == -math.inf:
                raise ValueError("at least one hypothesis must have nonzero support")
            log_weights = {
                name: value - normalization for name, value in log_weights.items()
            }
            weights = {
                name: math.exp(value) for name, value in log_weights.items()
            }
            if any(
                abs(weights[name] - supplied_weights[name]) > 1.0e-12
                for name in names
            ):
                raise ValueError("linear and log weights are inconsistent")
        else:
            weights = supplied_weights
            log_weights = {
                name: _log_weight(value) for name, value in weights.items()
            }
        if self.observations < 0 or self.observations != len(self.ledger.records):
            raise ValueError("observation count must match the evidence ledger")
        if not math.isfinite(self.mixture_prequential_log_score):
            raise ValueError("mixture prequential log score must be finite")
        object.__setattr__(self, "hypotheses", MappingProxyType(hypotheses))
        object.__setattr__(self, "weights", MappingProxyType(weights))
        object.__setattr__(self, "log_weights", MappingProxyType(log_weights))
        object.__setattr__(self, "states", MappingProxyType(states))
        object.__setattr__(self, "cumulative_log_scores", MappingProxyType(scores))


def initialize_evidence_posterior(
    hypotheses: Sequence[EvidenceHypothesis],
    open_hypothesis: EvidenceHypothesis,
    *,
    complexity_penalty: float = 1.0,
    open_prior: float = 0.02,
    explicit_priors: Optional[Mapping[str, float]] = None,
) -> EvidencePosterior:
    """Initialize declared hypotheses plus an explicit robust ``M_bottom``."""

    penalty = _finite_float(complexity_penalty, "complexity penalty")
    if penalty < 0.0:
        raise ValueError("complexity penalty cannot be negative")
    open_weight = _probability(open_prior, "open prior", open_interval=True)
    declared = {hypothesis.name: hypothesis for hypothesis in hypotheses}
    if len(declared) != len(hypotheses) or not declared:
        raise ValueError("declared hypothesis names must be nonempty and unique")
    if OPEN_EVIDENCE_NAME in declared:
        raise ValueError("declared hypotheses cannot use M_bottom")
    if open_hypothesis.name != OPEN_EVIDENCE_NAME or not open_hypothesis.robust:
        raise ValueError("open hypothesis must be robust and named M_bottom")

    if explicit_priors is None:
        log_raw = {
            name: -penalty * hypothesis.complexity
            for name, hypothesis in declared.items()
        }
    else:
        if set(explicit_priors) != set(declared):
            raise ValueError("explicit priors must cover every declared hypothesis")
        log_raw = {}
        for name, value in explicit_priors.items():
            prior = _finite_float(value, "explicit hypothesis prior")
            if prior <= 0.0:
                raise ValueError("explicit hypothesis priors must be positive")
            log_raw[name] = math.log(prior)
    normalization = _logsumexp(tuple(log_raw.values()))
    weights = {
        name: (1.0 - open_weight) * math.exp(value - normalization)
        for name, value in log_raw.items()
    }
    weights[OPEN_EVIDENCE_NAME] = open_weight
    log_weights = {
        name: math.log(1.0 - open_weight) + value - normalization
        for name, value in log_raw.items()
    }
    log_weights[OPEN_EVIDENCE_NAME] = math.log(open_weight)
    all_hypotheses = dict(declared)
    all_hypotheses[OPEN_EVIDENCE_NAME] = open_hypothesis
    states = {
        name: hypothesis.initial_state for name, hypothesis in all_hypotheses.items()
    }
    scores = {name: 0.0 for name in all_hypotheses}
    return EvidencePosterior(
        all_hypotheses,
        weights,
        states,
        EvidenceLedger(),
        scores,
        0.0,
        0,
        log_weights,
    )


def update_evidence_posterior(
    posterior: EvidencePosterior,
    record: EvidenceRecord,
) -> EvidencePosterior:
    """Assimilate one provenance-checked record using each predictive family."""

    ledger = posterior.ledger.append(record)
    action = record.as_action()
    distributions: Dict[str, PredictiveDistribution] = {}
    log_likelihoods: Dict[str, float] = {}
    for name, hypothesis in posterior.hypotheses.items():
        distribution = hypothesis.distribution(action, posterior.states[name])
        distribution.validate(record.observation)
        value = float(distribution.log_prob(record.observation))
        if math.isnan(value) or value == math.inf:
            raise ValueError("predictive log probability must not be NaN or +infinity")
        distributions[name] = distribution
        log_likelihoods[name] = value

    joint = {
        name: posterior.log_weights[name] + value
        for name, value in log_likelihoods.items()
    }
    mixture_log_probability = _logsumexp(tuple(joint.values()))
    if mixture_log_probability == -math.inf:
        raise ValueError("every hypothesis assigns zero probability to evidence")
    weights = {
        name: math.exp(value - mixture_log_probability)
        for name, value in joint.items()
    }
    log_weights = {
        name: value - mixture_log_probability for name, value in joint.items()
    }
    states = {}
    for name, hypothesis in posterior.hypotheses.items():
        if hypothesis.state_update is None:
            states[name] = posterior.states[name]
        else:
            states[name] = hypothesis.state_update(
                posterior.states[name], record, distributions[name]
            )
    scores = {
        name: posterior.cumulative_log_scores[name] + log_likelihoods[name]
        for name in posterior.hypotheses
    }
    return EvidencePosterior(
        posterior.hypotheses,
        weights,
        states,
        ledger,
        scores,
        posterior.mixture_prequential_log_score + mixture_log_probability,
        posterior.observations + 1,
        log_weights,
    )


def evidence_question_probabilities(
    posterior: EvidencePosterior,
    question: EvidenceQuestion,
) -> Dict[str, float]:
    """Aggregate hypothesis weights by a question's declared answers."""

    probabilities: Dict[str, float] = {}
    for name, weight in posterior.weights.items():
        answer = question.answer(name)
        probabilities[answer] = probabilities.get(answer, 0.0) + weight
    return probabilities


def _entropy_bits(probabilities: Mapping[str, float]) -> float:
    return -sum(
        value * math.log(value, 2.0)
        for value in probabilities.values()
        if value > 0.0
    )


def _answer_entropy_after_observation(
    posterior: EvidencePosterior,
    action: EvidenceAction,
    question: EvidenceQuestion,
    observation: Observation,
) -> float:
    joint = []
    names = tuple(posterior.hypotheses)
    for name in names:
        distribution = posterior.hypotheses[name].distribution(
            action, posterior.states[name]
        )
        distribution.validate(observation)
        joint.append(
            posterior.log_weights[name]
            + distribution.log_prob(observation)
        )
    normalization = _logsumexp(joint)
    if normalization == -math.inf:
        raise ValueError("every hypothesis assigns zero probability to predictive sample")
    answers: Dict[str, float] = {}
    for name, value in zip(names, joint):
        answer = question.answer(name)
        answers[answer] = answers.get(answer, 0.0) + math.exp(value - normalization)
    return _entropy_bits(answers)


def evidence_action_information(
    posterior: EvidencePosterior,
    action: EvidenceAction,
    question: EvidenceQuestion,
    *,
    samples_per_hypothesis: int = 32,
    seed: int = 0,
    cost_weight: float = 0.0,
) -> Dict[str, object]:
    """Estimate question information with stratified common random numbers.

    Seeds depend only on the global seed, generating hypothesis, and sample
    index.  Candidate action order therefore cannot change the random stream,
    and comparable actions receive common random numbers.
    """

    if samples_per_hypothesis < 1:
        raise ValueError("samples per hypothesis must be positive")
    cost_multiplier = _finite_float(cost_weight, "cost weight")
    if cost_multiplier < 0.0:
        raise ValueError("cost weight cannot be negative")
    prior_entropy = _entropy_bits(evidence_question_probabilities(posterior, question))
    expected_entropy = 0.0
    variance_of_estimator = 0.0

    for name, weight in posterior.weights.items():
        if weight <= 0.0:
            continue
        distribution = posterior.hypotheses[name].distribution(
            action, posterior.states[name]
        )
        entropies = []
        for sample_index in range(samples_per_hypothesis):
            rng = random.Random(_stable_seed(seed, name, sample_index))
            observation = distribution.sample(rng)
            distribution.validate(observation)
            entropies.append(
                _answer_entropy_after_observation(
                    posterior, action, question, observation
                )
            )
        mean_entropy = sum(entropies) / samples_per_hypothesis
        expected_entropy += weight * mean_entropy
        if samples_per_hypothesis > 1:
            sample_variance = sum(
                (value - mean_entropy) ** 2 for value in entropies
            ) / (samples_per_hypothesis - 1)
            variance_of_estimator += (
                weight * weight * sample_variance / samples_per_hypothesis
            )

    raw_information = prior_entropy - expected_entropy
    information = max(0.0, raw_information)
    burden = cost_multiplier * action.cost
    return {
        "action": action.name,
        "family": action.family,
        "prior_question_entropy_bits": prior_entropy,
        "expected_posterior_entropy_bits": expected_entropy,
        "question_information_bits": information,
        "raw_question_information_bits": raw_information,
        "monte_carlo_standard_error_bits": math.sqrt(variance_of_estimator),
        "practical_burden": burden,
        "utility": information - burden,
        "samples_per_hypothesis": samples_per_hypothesis,
    }


def rank_evidence_actions(
    posterior: EvidencePosterior,
    actions: Sequence[EvidenceAction],
    question: EvidenceQuestion,
    *,
    samples_per_hypothesis: int = 32,
    seed: int = 0,
    cost_weight: float = 0.0,
) -> list:
    """Rank actions reproducibly by question information minus cost."""

    names = [action.name for action in actions]
    if len(set(names)) != len(names):
        raise ValueError("candidate evidence action names must be unique")
    rows = [
        evidence_action_information(
            posterior,
            action,
            question,
            samples_per_hypothesis=samples_per_hypothesis,
            seed=seed,
            cost_weight=cost_weight,
        )
        for action in actions
    ]
    return sorted(rows, key=lambda row: (-float(row["utility"]), str(row["action"])))


def prequential_log_score(
    posterior: EvidencePosterior,
    hypothesis_name: Optional[str] = None,
    *,
    average: bool = False,
) -> float:
    """Return cumulative or per-record prequential log score.

    With no hypothesis name, the score is the sequential model-mixture score.
    Supplying a hypothesis returns its cumulative one-step-ahead log score.
    """

    if hypothesis_name is None:
        value = posterior.mixture_prequential_log_score
    else:
        if hypothesis_name not in posterior.cumulative_log_scores:
            raise ValueError("unknown evidence hypothesis: %s" % hypothesis_name)
        value = posterior.cumulative_log_scores[hypothesis_name]
    if average and posterior.observations:
        return value / posterior.observations
    return value


def prequential_score_table(
    posterior: EvidencePosterior,
    *,
    average: bool = False,
) -> Dict[str, float]:
    """Return mixture and per-hypothesis prequential scores."""

    result = {
        name: prequential_log_score(posterior, name, average=average)
        for name in posterior.hypotheses
    }
    result["mixture"] = prequential_log_score(posterior, average=average)
    return result


# Verbose aliases are convenient for callers that prefer explicit type names.
GaussianDistribution = Gaussian
StudentTDistribution = StudentT
BinomialDistribution = Binomial
BetaBinomialDistribution = BetaBinomial
PoissonDistribution = Poisson
NegativeBinomialDistribution = NegativeBinomial
MultinomialDistribution = Multinomial
DirichletMultinomialDistribution = DirichletMultinomial


__all__ = (
    "OPEN_EVIDENCE_NAME",
    "EVIDENCE_POSTERIOR_WARNING",
    "evidence_payload_digest",
    "PredictiveDistribution",
    "Gaussian",
    "StudentT",
    "Binomial",
    "BetaBinomial",
    "Poisson",
    "NegativeBinomial",
    "Multinomial",
    "DirichletMultinomial",
    "GaussianDistribution",
    "StudentTDistribution",
    "BinomialDistribution",
    "BetaBinomialDistribution",
    "PoissonDistribution",
    "NegativeBinomialDistribution",
    "MultinomialDistribution",
    "DirichletMultinomialDistribution",
    "EvidenceAction",
    "EvidenceRecord",
    "EvidenceLedger",
    "EvidenceHypothesis",
    "EvidenceQuestion",
    "EvidencePosterior",
    "initialize_evidence_posterior",
    "update_evidence_posterior",
    "evidence_question_probabilities",
    "evidence_action_information",
    "rank_evidence_actions",
    "prequential_log_score",
    "prequential_score_table",
)
