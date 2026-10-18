"""Training-only interval/linear-inversion tomography; no generator import.

All certificate arithmetic is rational. A frozen comparison band is constructed
before score() receives held-out records. Supplied calibration/drift bounds are
deterministic premises, not estimates from the withheld observations.
"""

import re
from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256

from records import ERASURE_MODEL, TrialRecord, canonical_json, fresh_identity

TRAIN_AXES = ("X", "Y", "Z")
W = (F(0), F(3, 5), F(4, 5))


class InferenceRefusal(ValueError):
    """Records remain retained by the caller; this refusal never filters them."""


def rational(value):
    if type(value) is int:
        return F(value)
    if type(value) is F:
        return value
    raise InferenceRefusal("budgets require exact Fractions/integers, not floats")


def encode(value):
    if type(value) is F:
        return str(value)
    if type(value) is tuple or type(value) is list:
        return [encode(x) for x in value]
    if type(value) is dict:
        return {k: encode(v) for k, v in value.items()}
    return value


def tail_certificate(n, epsilon, alpha, terms=64):
    """S<=exp(2 N eps²), S>=2/alpha certifies Hoeffding's two-sided tail.

    False means this chosen finite truncation did not certify the claim.
    """
    if type(n) is not int or n <= 0 or type(terms) is not int or terms < 0:
        raise InferenceRefusal("invalid finite-count certificate request")
    epsilon, alpha = rational(epsilon), rational(alpha)
    if epsilon < 0 or not 0 < alpha < 1:
        raise InferenceRefusal("invalid epsilon or failure allocation")
    x = 2 * n * epsilon * epsilon
    term = total = F(1)
    for j in range(1, terms + 1):
        term *= x / j
        total += term
    return total * alpha >= 2


@dataclass(frozen=True)
class ExperimentPlan:
    recipe_ids: tuple[str, ...] = ("phase_plus", "phase_minus", "mixed")
    session_id: str = "session-v1"
    shots: int = 512
    frame_id: str = "pauli-frame-v1"
    calibration_id: str = "sim-calibration-v1"
    provenance: str = "simulation:qubit_record_v1"
    training_epsilon: F = F(1, 10)
    calibration: F = F(1, 100)
    drift: F = F(1, 100)
    alpha_train: F = F(1, 100)
    held_epsilon: F = F(1, 10)
    future_calibration: F = F(1, 100)
    future_drift: F = F(1, 100)
    alpha_score: F = F(1, 100)
    preparation_contract: str = "fresh-successful-comparable-v1"
    sampling_contract: str = "fixed-independent-underlying-binary-v1"
    calibration_contract: str = "supplied-average-per-trial-probability-bound-v1"

    def __post_init__(self):
        names = (self.session_id, self.frame_id, self.calibration_id)
        if (
            type(self.recipe_ids) is not tuple
            or not self.recipe_ids
            or len(set(self.recipe_ids)) != len(self.recipe_ids)
            or any(
                type(s) is not str or not re.fullmatch(r"[A-Za-z0-9_.-]{1,48}", s)
                for s in (*self.recipe_ids, *names)
            )
        ):
            raise InferenceRefusal("plan needs unique canonical recipe/context identities")
        if type(self.shots) is not int or self.shots <= 0:
            raise InferenceRefusal("zero or invalid scheduled shot count")
        if type(self.provenance) is not str or not self.provenance:
            raise InferenceRefusal("missing provenance contract")
        for name in (
            "training_epsilon",
            "calibration",
            "drift",
            "alpha_train",
            "held_epsilon",
            "future_calibration",
            "future_drift",
            "alpha_score",
        ):
            value = rational(getattr(self, name))
            object.__setattr__(self, name, value)
            if value < 0:
                raise InferenceRefusal("negative probability/error budget")
        if (
            not 0 < self.alpha_train < 1
            or not 0 < self.alpha_score < 1
            or self.alpha_train + self.alpha_score >= 1
        ):
            raise InferenceRefusal("global failure allocations must be positive and sum below one")
        if (
            self.preparation_contract != "fresh-successful-comparable-v1"
            or self.sampling_contract != "fixed-independent-underlying-binary-v1"
            or self.calibration_contract != "supplied-average-per-trial-probability-bound-v1"
        ):
            raise InferenceRefusal("unsupported acquisition/comparability premise")
        if not tail_certificate(
            self.shots, self.training_epsilon, self.alpha_train / self.training_strata
        ):
            raise InferenceRefusal("training Hoeffding allocation not rationally certified")
        if not tail_certificate(
            self.shots, self.held_epsilon, self.alpha_score / len(self.recipe_ids)
        ):
            raise InferenceRefusal("held-out Hoeffding allocation not rationally certified")

    @property
    def training_strata(self):
        return 3 * len(self.recipe_ids)

    def to_dict(self):
        return encode({name: getattr(self, name) for name in self.__dataclass_fields__})

    @property
    def fingerprint(self):
        return sha256(canonical_json(self.to_dict()).encode()).hexdigest()


def box_witness(intervals):
    """Exact iff feasibility for an axis box intersected with the unit ball."""
    if type(intervals) is not tuple or len(intervals) != 3:
        raise InferenceRefusal("three exact coordinate intervals required")
    nearest = []
    for pair in intervals:
        if type(pair) is not tuple or len(pair) != 2:
            raise InferenceRefusal("invalid coordinate interval")
        lo, hi = (rational(x) for x in pair)
        lo, hi = max(F(-1), lo), min(F(1), hi)
        if lo > hi:
            return None
        nearest.append(lo if lo > 0 else hi if hi < 0 else F(0))
    return tuple(nearest) if sum(x * x for x in nearest) <= 1 else None


def _clip_interval(lo, hi):
    return max(F(0), lo), min(F(1), hi)


def _records_for(plan, records, split, axes):
    if type(plan) is not ExperimentPlan or type(records) is not tuple:
        raise InferenceRefusal("use an immutable plan and record tuple")
    expected = {}
    for recipe in plan.recipe_ids:
        for setting in axes:
            for index in range(plan.shots):
                trial, prep, record_id = fresh_identity(
                    plan.session_id, recipe, split, setting, index
                )
                expected[record_id] = (trial, prep, recipe, setting)
    found = {}
    for record in records:
        if type(record) is not TrialRecord:
            raise InferenceRefusal("fit/score accepts observable TrialRecord objects only")
        if record.split != split or record.setting not in axes:
            raise InferenceRefusal("held-out/unsupported setting or wrong split in input")
        if record.record_id in found:
            raise InferenceRefusal("duplicate acquisition record")
        if record.record_id not in expected:
            raise InferenceRefusal("record not on frozen acquisition schedule")
        trial, prep, recipe, setting = expected[record.record_id]
        if (record.trial_id, record.preparation_id, record.recipe_id, record.setting) != (
            trial,
            prep,
            recipe,
            setting,
        ) or record.step != 0:
            raise InferenceRefusal("not a fresh scheduled preparation")
        if (
            record.session_id != plan.session_id
            or record.frame_id != plan.frame_id
            or record.calibration_id != plan.calibration_id
            or record.provenance != plan.provenance
        ):
            raise InferenceRefusal("source/session/frame/calibration mismatch")
        if (
            record.preparation_status != "successful"
            or record.acquisition_model != ERASURE_MODEL
            or record.status not in ("detected", "missing")
            or not record.measurement_occurred
        ):
            raise InferenceRefusal("attempt lacks the successful binary-read/erasure forward law")
        found[record.record_id] = record
    if set(found) != set(expected):
        raise InferenceRefusal("missing scheduled attempts; do not divide by surviving detections")
    return tuple(found[key] for key in sorted(found))


@dataclass(frozen=True)
class AxisSummary:
    setting: str
    attempted: int
    plus: int
    minus: int
    missing: int
    midpoint: F
    eta: F
    interval: tuple[F, F]

    def to_dict(self):
        return encode({name: getattr(self, name) for name in self.__dataclass_fields__})


@dataclass(frozen=True)
class RecipeFit:
    recipe_id: str
    status: str
    axes: tuple[AxisSummary, ...]
    reference_midpoint: tuple[F, F, F]
    intervals: tuple[tuple[F, F], ...]
    witness: tuple[F, F, F] | None
    point_estimate: tuple[F, F, F] | None
    trace_radius_squared: F | None
    diameter_squared: F | None
    unresolved_alternatives: tuple[tuple[F, F, F], ...]
    ideal_probability_interval: tuple[F, F] | None
    future_probability_interval: tuple[F, F] | None
    frozen_frequency_band: tuple[F, F] | None
    point_probability: F | None
    conventional_midpoint: tuple[F, F, F]
    conventional_point: tuple[F, F, F] | None

    def to_dict(self):
        result = {name: getattr(self, name) for name in self.__dataclass_fields__}
        result["axes"] = [a.to_dict() for a in self.axes]
        return encode(result)


@dataclass(frozen=True)
class FrozenExperiment:
    """Trusted immutable fit output, not an authenticated or anti-forgery token.

    Direct constructors and externally edited JSON are not certified fit results.
    The worked runner binds its fit output before exposing held-out records.
    """

    plan: ExperimentPlan
    training_sha256: str
    used_axes: tuple[str, ...]
    results: tuple[RecipeFit, ...]

    def to_dict(self):
        return {
            "schema_version": 1,
            "estimator": "erasure-midpoint-linear-inversion-with-refusal-v1",
            "target_setting": "W",
            "target_axis": encode(W),
            "plan": self.plan.to_dict(),
            "plan_sha256": self.plan.fingerprint,
            "training_sha256": self.training_sha256,
            "used_axes": list(self.used_axes),
            "results": [r.to_dict() for r in self.results],
        }

    @property
    def fingerprint(self):
        return sha256(canonical_json(self.to_dict()).encode()).hexdigest()


def conventional_tomography(records, recipe, axes):
    """Conventional interval-aware linear inversion on the SAME revealed attempts.

    Loss convention is squared displacement from empirical erasure midpoints;
    no constrained projection or likelihood/MLE claim. A nonphysical or
    incompletely observed midpoint is refused as a physical point estimate.
    Local guards do not replace fit's complete frozen-schedule/context check.
    Calling this helper alone cannot certify that all attempts were supplied.
    """
    if (
        type(records) is not tuple
        or any(
            type(r) is not TrialRecord or r.split != "training" or r.setting not in axes
            for r in records
        )
        or not axes
        or any(a not in TRAIN_AXES for a in axes)
    ):
        raise InferenceRefusal("baseline requires training-only declared-axis records")
    if any(
        r.preparation_status != "successful"
        or r.acquisition_model != ERASURE_MODEL
        or r.status not in ("detected", "missing")
        or not r.measurement_occurred
        or r.step != 0
        for r in records
    ):
        raise InferenceRefusal("baseline requires fresh successful binary-read/erasure attempts")
    for identity in ("record_id", "trial_id", "preparation_id"):
        if len({getattr(r, identity) for r in records}) != len(records):
            raise InferenceRefusal("baseline refuses duplicate acquisition/preparation identities")
    coordinates = []
    observed = True
    for setting in TRAIN_AXES:
        rows = [r for r in records if r.recipe_id == recipe and r.setting == setting]
        if setting not in axes:
            coordinates.append(F(0))
            observed = False
            continue
        plus = sum(r.outcome == 1 for r in rows)
        minus = sum(r.outcome == -1 for r in rows)
        if not rows:
            raise InferenceRefusal("baseline is missing a declared training stratum")
        coordinates.append(F(plus - minus, len(rows)))
        observed = observed and plus + minus > 0
    midpoint = tuple(coordinates)
    return midpoint, midpoint if observed and sum(x * x for x in midpoint) <= 1 else None


def fit(plan, training_records, axes=TRAIN_AXES):
    if (
        type(axes) is not tuple
        or not axes
        or len(set(axes)) != len(axes)
        or any(a not in TRAIN_AXES for a in axes)
        or axes != tuple(a for a in TRAIN_AXES if a in axes)
    ):
        raise InferenceRefusal("training axes must be an ordered subset of X/Y/Z, never W")
    rows = _records_for(plan, training_records, "training", axes)
    digest = sha256(canonical_json([r.to_dict() for r in rows]).encode()).hexdigest()
    results = []
    for recipe in plan.recipe_ids:
        summaries, mids, intervals, etas = [], [], [], []
        observed = True
        for setting in TRAIN_AXES:
            group = [r for r in rows if r.recipe_id == recipe and r.setting == setting]
            if setting not in axes:
                n = plus = minus = missing = 0
                midpoint, eta, interval = F(0), F(1, 2), (F(-1), F(1))
                observed = False
            else:
                n = len(group)
                plus = sum(r.outcome == 1 for r in group)
                minus = sum(r.outcome == -1 for r in group)
                missing = sum(r.status == "missing" for r in group)
                midpoint = F(2 * plus + missing, n) - 1
                eta = plan.training_epsilon + plan.calibration + plan.drift + F(missing, 2 * n)
                interval = (max(F(-1), midpoint - 2 * eta), min(F(1), midpoint + 2 * eta))
                observed = observed and plus + minus > 0
            summaries.append(AxisSummary(setting, n, plus, minus, missing, midpoint, eta, interval))
            mids.append(midpoint)
            intervals.append(interval)
            etas.append(eta)
        mids, intervals = tuple(mids), tuple(intervals)
        witness = box_witness(intervals)
        point = mids if observed and witness is not None and sum(x * x for x in mids) <= 1 else None
        conventional_mid, conventional_point = conventional_tomography(rows, recipe, axes)
        alternatives = []
        if witness is not None:
            for j, setting in enumerate(TRAIN_AXES):
                if W[j] and (setting not in axes or summaries[j].plus + summaries[j].minus == 0):
                    room = 1 - sum(witness[k] ** 2 for k in range(3) if k != j)
                    amplitude = room / 2
                    if amplitude > 0:
                        for sign in (-1, 1):
                            candidate = list(witness)
                            candidate[j] = sign * amplitude
                            if all(lo <= v <= hi for v, (lo, hi) in zip(candidate, intervals)):
                                alternatives.append(tuple(candidate))
                    break
        if witness is None:
            status = "incompatible_bounds"
            ideal = future = frequency = None
            diameter = None
        else:
            status = "point_and_interval" if point is not None else "interval_only"
            center = (1 + sum(w * x for w, x in zip(W, mids))) / 2
            halfwidth = sum(abs(w) * e for w, e in zip(W, etas))
            ideal = _clip_interval(center - halfwidth, center + halfwidth)
            future = _clip_interval(
                ideal[0] - plan.future_calibration - plan.future_drift,
                ideal[1] + plan.future_calibration + plan.future_drift,
            )
            frequency = _clip_interval(future[0] - plan.held_epsilon, future[1] + plan.held_epsilon)
            diameter = min(F(1), sum((hi - lo) ** 2 for lo, hi in intervals) / 4)
        radius = min(F(1), sum(e * e for e in etas)) if point is not None else None
        point_p = (1 + sum(w * x for w, x in zip(W, point))) / 2 if point is not None else None
        results.append(
            RecipeFit(
                recipe,
                status,
                tuple(summaries),
                mids,
                intervals,
                witness,
                point,
                radius,
                diameter,
                tuple(alternatives),
                ideal,
                future,
                frequency,
                point_p,
                conventional_mid,
                conventional_point,
            )
        )
    return FrozenExperiment(plan, digest, axes, tuple(results))


def score(frozen, heldout_records):
    if type(frozen) is not FrozenExperiment:
        raise InferenceRefusal("score requires the trusted immutable fit output")
    plan = frozen.plan
    rows = _records_for(plan, heldout_records, "heldout", ("W",))
    reports = []
    for result in frozen.results:
        group = [r for r in rows if r.recipe_id == result.recipe_id]
        n = len(group)
        plus = sum(r.outcome == 1 for r in group)
        minus = sum(r.outcome == -1 for r in group)
        missing = sum(r.status == "missing" for r in group)
        completion = (F(plus, n), F(plus + missing, n))
        band = result.frozen_frequency_band
        if band is None:
            status = "not_scored_incompatible_training"
        elif plus + minus == 0:
            status = "uninformative_all_erased"
        else:
            status = (
                "compatible_with_frozen_band"
                if max(completion[0], band[0]) <= min(completion[1], band[1])
                else "model_or_budget_mismatch"
            )
        p = result.point_probability
        zero_ids = tuple(
            r.record_id
            for r in group
            if p is not None and ((p == 0 and r.outcome == 1) or (p == 1 and r.outcome == -1))
        )
        brier = None
        if p is not None:
            detected_loss = plus * (1 - p) ** 2 + minus * p * p
            brier = (
                (detected_loss + missing * min(p * p, (1 - p) ** 2)) / n,
                (detected_loss + missing * max(p * p, (1 - p) ** 2)) / n,
            )
        reports.append(
            encode(
                {
                    "recipe_id": result.recipe_id,
                    "status": status,
                    "attempted": n,
                    "plus": plus,
                    "minus": minus,
                    "missing": missing,
                    "completion_interval": completion,
                    "frozen_frequency_band": band,
                    "point_zero_probability_record_ids": zero_ids,
                    "full_attempt_brier_interval": brier,
                    "baseline_same_point": result.point_estimate == result.conventional_point,
                }
            )
        )
    return {
        "prediction_sha256": frozen.fingerprint,
        "plan_sha256": plan.fingerprint,
        "heldout_sha256": sha256(canonical_json([r.to_dict() for r in rows]).encode()).hexdigest(),
        "coverage_premise": "joint Hoeffding event; compatibility is not validation",
        "joint_failure_budget": str(plan.alpha_train + plan.alpha_score),
        "results": reports,
    }
