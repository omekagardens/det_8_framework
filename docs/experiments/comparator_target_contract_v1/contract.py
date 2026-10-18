"""One exact, model-conditional comparator target contract; no acquisition or RET.

The target is f(0)=b for f(x)=g*x+b+c*x*x at normalized x in {-1,0,1}.
Supplied deterministic intervals are uncertainty sets, not sampling laws.
"""

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction

VERSION = "comparator-target-v1"
MAX_RECORDS = 64
MAX_BITS = 256
REFERENCES = (Fraction(-1), Fraction(0), Fraction(1))


def _rational(value, name):
    if type(value) not in (int, Fraction):
        raise TypeError(f"{name} must be an exact built-in int or Fraction")
    value = Fraction(value)
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_BITS:
        raise ValueError(f"{name} exceeds the input bit limit")
    return value


def _text(value, name, limit=128):
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in string")
    if (
        not value
        or value.strip() != value
        or len(value) > limit
        or any(ord(char) < 32 or ord(char) == 127 for char in value)
    ):
        raise ValueError(
            f"{name} must be bounded nonblank text without edge whitespace/control characters"
        )
    return value


@dataclass(frozen=True)
class Model:
    family: str
    curvature_bound: object = None

    def __post_init__(self):
        _text(self.family, "family")
        if self.family not in ("affine", "bounded_curvature", "unbounded_curvature"):
            raise ValueError("unsupported fixed model family")
        if self.family == "bounded_curvature":
            bound = _rational(self.curvature_bound, "curvature_bound")
            if bound < 0:
                raise ValueError("curvature_bound must be nonnegative")
            object.__setattr__(self, "curvature_bound", bound)
        elif self.curvature_bound is not None:
            raise ValueError("only bounded_curvature takes a curvature_bound")

    @property
    def effective_bound(self):
        if self.family == "affine":
            return Fraction(0)
        return self.curvature_bound


@dataclass(frozen=True)
class Record:
    record_id: str
    role: str
    reference: object
    value: object = None
    error: object = None
    reason: object = None

    def __post_init__(self):
        _text(self.record_id, "record_id", 96)
        _text(self.role, "role")
        if self.role not in ("actual", "prospective", "missing", "held_out"):
            raise ValueError("unsupported record role")
        reference = _rational(self.reference, "reference")
        if reference not in REFERENCES:
            raise ValueError("only normalized references -1, 0, 1 are supported")
        object.__setattr__(self, "reference", reference)
        if self.role in ("actual", "held_out"):
            value = _rational(self.value, "value")
            error = _rational(self.error, "error")
            if error < 0 or self.reason is not None:
                raise ValueError("observed records need nonnegative error and no missing reason")
            object.__setattr__(self, "value", value)
            object.__setattr__(self, "error", error)
        elif self.role == "prospective":
            if self.value is not None or self.reason is not None:
                raise ValueError(
                    "prospective records cannot carry an observed value or missing reason"
                )
            if self.error is not None:
                error = _rational(self.error, "planned error")
                if error < 0:
                    raise ValueError("planned error must be nonnegative")
                object.__setattr__(self, "error", error)
        else:
            if self.value is not None or self.error is not None:
                raise ValueError("missing records cannot supply a value or error interval")
            _text(self.reason, "missing reason", 512)


@dataclass(frozen=True)
class Request:
    model: Model
    records: tuple
    selected_ids: tuple
    tolerance: object
    response_unit: str
    session_id: str
    calibration_id: str
    model_basis: str
    error_basis: str
    target: str = "mean_at_zero"
    reference_unit: str = "normalized"

    def __post_init__(self):
        if type(self.model) is not Model:
            raise TypeError("model must be this contract's Model")
        if type(self.records) is not tuple or type(self.selected_ids) is not tuple:
            raise TypeError("records and selected_ids must be bounded tuples")
        if len(self.records) > MAX_RECORDS or len(self.selected_ids) > MAX_RECORDS:
            raise ValueError("at most 64 supplied and selected records are supported")
        tolerance = _rational(self.tolerance, "tolerance")
        if tolerance < 0:
            raise ValueError("tolerance must be nonnegative")
        object.__setattr__(self, "tolerance", tolerance)
        for name in ("response_unit", "session_id", "calibration_id", "target", "reference_unit"):
            _text(getattr(self, name), name)
        for name in ("model_basis", "error_basis"):
            _text(getattr(self, name), name, 512)
        if self.target != "mean_at_zero" or self.reference_unit != "normalized":
            raise ValueError(
                "only the zero-input mean target and normalized references are supported"
            )
        by_id = {}
        for record in self.records:
            if type(record) is not Record:
                raise TypeError("records must use this contract's Record")
            if record.record_id in by_id:
                raise ValueError("duplicate record identity")
            by_id[record.record_id] = record
        selected = set()
        for identity in self.selected_ids:
            _text(identity, "selected identity", 96)
            if identity in selected or identity not in by_id:
                raise ValueError("selected identities must be unique and present")
            record = by_id[identity]
            if record.role != "actual":
                raise ValueError("only actual records may be selected for training")
            selected.add(identity)


def _request(request):
    if type(request) is not Request:
        raise TypeError("a validated Request is required")
    return request


def canonical_payload(request):
    """Detached supplied-input content, including nontraining records and roles."""
    _request(request)
    records = []
    for record in request.records:
        records.append(
            {
                "record_id": record.record_id,
                "role": record.role,
                "reference": str(record.reference),
                "value": None if record.value is None else str(record.value),
                "error": None if record.error is None else str(record.error),
                "reason": record.reason,
            }
        )
    return {
        "contract_version": VERSION,
        "model": {
            "family": request.model.family,
            "curvature_bound": None
            if request.model.curvature_bound is None
            else str(request.model.curvature_bound),
        },
        "parameter_order": ["g", "b", "c"],
        "reference_catalogue": [str(x) for x in REFERENCES],
        "target": request.target,
        "reference_unit": request.reference_unit,
        "response_unit": request.response_unit,
        "session_id": request.session_id,
        "calibration_id": request.calibration_id,
        "model_basis": request.model_basis,
        "error_basis": request.error_basis,
        "tolerance": str(request.tolerance),
        "records": records,
        "selected_ids": list(request.selected_ids),
    }


def _digest(request):
    content = json.dumps(
        canonical_payload(request), sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _intervals(request):
    selected = set(request.selected_ids)
    intervals = {}
    for record in request.records:
        if record.record_id not in selected:
            continue
        lower, upper = record.value - record.error, record.value + record.error
        if record.reference in intervals:
            old_lower, old_upper = intervals[record.reference]
            lower, upper = max(lower, old_lower), min(upper, old_upper)
        intervals[record.reference] = (lower, upper)
    return intervals


@dataclass(frozen=True)
class Report:
    input_digest: str
    status: str
    lower: object
    upper: object
    midpoint: object
    radius: object
    precision_met: object
    structurally_identified: bool
    reason: str


def assess(request):
    """Project the declared compatibility set; no fitting, confidence or selection."""
    _request(request)
    intervals = _intervals(request)
    bound = request.model.effective_bound
    both_endpoints = Fraction(-1) in intervals and Fraction(1) in intervals
    structural = Fraction(0) in intervals or (both_endpoints and bound == 0)
    identity = _digest(request)
    if any(lower > upper for lower, upper in intervals.values()):
        return Report(
            identity,
            "incompatible",
            None,
            None,
            None,
            None,
            None,
            structural,
            "conflicting_selected_intervals",
        )
    if bound is None or not both_endpoints:
        if Fraction(0) not in intervals:
            reason = (
                "unrestricted_curvature_without_zero_reading"
                if both_endpoints
                else "insufficient_reference_locations"
            )
            return Report(identity, "unbounded", None, None, None, None, False, structural, reason)
        lower, upper = intervals[Fraction(0)]
    else:
        minus, plus = intervals[Fraction(-1)], intervals[Fraction(1)]
        lower = (minus[0] + plus[0]) / 2 - bound
        upper = (minus[1] + plus[1]) / 2 + bound
        if Fraction(0) in intervals:
            zero_lower, zero_upper = intervals[Fraction(0)]
            lower, upper = max(lower, zero_lower), min(upper, zero_upper)
        if lower > upper:
            return Report(
                identity,
                "incompatible",
                None,
                None,
                None,
                None,
                None,
                structural,
                "zero_reading_conflicts_with_endpoint_model",
            )
    midpoint, radius = (lower + upper) / 2, (upper - lower) / 2
    return Report(
        identity,
        "bounded",
        lower,
        upper,
        midpoint,
        radius,
        radius <= request.tolerance,
        structural,
        "exact_target_projection",
    )


def verify_report(request, report):
    """Recompute content and conclusions; not authentication or calibration."""
    _request(request)
    if type(report) is not Report:
        return False
    expected = assess(request)
    return all(
        type(getattr(report, name)) is type(getattr(expected, name))
        and getattr(report, name) == getattr(expected, name)
        for name in Report.__dataclass_fields__
    )


def compatible_parameters(request, target_value):
    """Construct a mathematical (g,b,c) witness, not a physical state estimate.

    Every selected interval and the declared curvature domain are satisfied.
    Arbitrary rational targets are supported within the input bit limit.
    The continuous real-domain attainability proof is in CONTRACT.md.
    """
    target = _rational(target_value, "target_value")
    report = assess(request)
    if report.status == "incompatible":
        raise ValueError("empty compatibility set")
    if report.status == "bounded" and not report.lower <= target <= report.upper:
        raise ValueError("target is outside the compatible interval")
    intervals = _intervals(request)
    if Fraction(-1) not in intervals or Fraction(1) not in intervals:
        for reference in (Fraction(-1), Fraction(1)):
            if reference in intervals:
                mean = intervals[reference][0]
                return (mean - target) / reference, target, Fraction(0)
        return Fraction(0), target, Fraction(0)
    minus, plus = intervals[Fraction(-1)], intervals[Fraction(1)]
    mean_lower, mean_upper = (minus[0] + plus[0]) / 2, (minus[1] + plus[1]) / 2
    mean = min(max(target, mean_lower), mean_upper)
    curvature = mean - target
    mu_minus = max(minus[0], 2 * mean - plus[1])
    mu_plus = 2 * mean - mu_minus
    gain = (mu_plus - mu_minus) / 2
    return gain, target, curvature
