"""Exact conditional proxy certificates from complete finite probability boxes.

This pure module implements the construction in PROXY_ENVELOPE.md. It neither
produces scientific intervals nor verifies their provenance/completeness. Every
result has operational_admission == "ABSTAIN", including arithmetic success.
There is no random source, sampling, I/O, automatic retry or protocol change.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Optional, Tuple

from .certified_categorical_map import MAX_OUTCOMES, MAX_WEIGHT_BITS


MAX_INPUT_BITS = 256
MAX_IDENTIFIER_CHARS = 128
MAX_PROVENANCE_CHARS = 1024
MAX_INTERMEDIATE_BITS = 262413
MAX_WORK_BITS = (32 * MAX_OUTCOMES + 64) * MAX_INTERMEDIATE_BITS


@dataclass(frozen=True)
class EnvelopeResourceLimits:
    """Logical arithmetic reservations, not an OS/RSS or timing guarantee.

    The construction and budget-comparison bounds must both fit the precision
    limit. The storage policy reserves (32*m+64)*max(256,C,C_compare) bits for
    logical integer magnitudes. Python object/allocator and gcd internals, input
    creation, text storage and process memory are not measured by that policy.
    The separate bounded string lengths constrain retained text. A deployment
    needing a hard memory limit must independently enforce one.
    """

    max_intermediate_bits: int = MAX_INTERMEDIATE_BITS
    max_work_bits: int = MAX_WORK_BITS

    def __post_init__(self) -> None:
        for name, ceiling in (("max_intermediate_bits", MAX_INTERMEDIATE_BITS),
                              ("max_work_bits", MAX_WORK_BITS)):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(name + " must be a plain integer")
            if not 0 <= value <= ceiling:
                raise ValueError(name + " is outside the supported resource profile")


@dataclass(frozen=True)
class EnvelopeResourcePlan:
    construction_bits: int
    comparison_bits: int
    integer_slots: int
    work_bits: int


@dataclass(frozen=True)
class EnvelopeCertificate:
    """Complete arithmetic witnesses; validity of the scientific box is external.

    Integers are unreduced common-denominator witnesses; Fraction fields are
    exact reduced values. Ordinary immutable records are not authenticated
    credentials. Consumers should use results from the factory below.
    """

    common_denominator: int
    original_lower_numerators: Tuple[int, ...]
    original_upper_numerators: Tuple[int, ...]
    lower_numerators: Tuple[int, ...]
    upper_numerators: Tuple[int, ...]
    lower_total: int
    upper_total: int
    lower_slack: int
    upper_slack: int
    total_slack: int
    tightened_lower: Tuple[Fraction, ...]
    tightened_upper: Tuple[Fraction, ...]
    proxy_weights: Tuple[Fraction, ...]
    tv_bound: Fraction
    budget_comparison_products: Optional[Tuple[int, int]]


@dataclass(frozen=True)
class EnvelopeResult:
    """No non-success disposition contains a partial complete certificate."""

    status: str
    reason: str
    outcomes: Tuple[str, ...]
    lower: Tuple[Fraction, ...]
    upper: Tuple[Fraction, ...]
    proxy_budget: Optional[Fraction]
    provenance_reference: Optional[str]
    resource_limits: EnvelopeResourceLimits
    resource_plan: EnvelopeResourcePlan
    certificate: Optional[EnvelopeCertificate] = None
    # A failed budget comparison may retain eta as a diagnostic, never q or a
    # complete certificate. Resource/infeasibility refusals leave this absent.
    compared_tv_bound: Optional[Fraction] = None

    @property
    def operational_admission(self) -> str:
        return "ABSTAIN"


def _exact_probability(value, name: str) -> Fraction:
    """Bounded input validation only; no large envelope arithmetic here."""
    if type(value) is int:
        numerator, denominator = value, 1
    elif type(value) is Fraction:
        numerator, denominator = value.numerator, value.denominator
    elif type(value) is tuple:
        if len(value) != 2 or any(type(x) is not int for x in value):
            raise TypeError(name + " pair must contain two plain integers")
        numerator, denominator = value
    else:
        raise TypeError(name + " must be a plain int, Fraction, or reduced integer pair")
    if (numerator.bit_length() > MAX_INPUT_BITS or
            denominator.bit_length() > MAX_INPUT_BITS):
        raise ValueError(name + " exceeds the 256-bit input profile")
    if denominator <= 0 or not 0 <= numerator <= denominator:
        raise ValueError(name + " must be a probability in [0,1] with positive denominator")
    if type(value) is tuple and gcd(numerator, denominator) != 1:
        raise ValueError(name + " pair must already be reduced")
    return value if type(value) is Fraction else Fraction(numerator, denominator)


def certify_probability_envelope(outcomes, lower, upper, *, proxy_budget=None,
                                 resource_limits=None, provenance_reference=None):
    """Return a complete conditional certificate or a precise refusal record.

    Containers must be plain lists/tuples of 1..256 entries. Outcome identifiers
    are distinct nonempty plain strings of at most 128 characters; numerical
    completeness/meaning is not inferred. Exact inputs are plain int/Fraction
    or already reduced (numerator, positive_denominator) tuples, each at most
    256 bits. Floats, bools, subclasses, generators and numeric adapters fail.

    Invalid input types/ranges raise TypeError/ValueError. After bounded input
    validation, resource admission precedes LCM, cross-products, feasibility
    and construction. Thus resource refusal can precede infeasibility. Once
    computed, consumer precision refusal precedes budget refusal. A missing
    budget means no budget claim, not a default allowance. A provenance string
    is retained verbatim and never checked. Unexpected runtime failures raise
    without a result; they must not be interpreted as operational acceptance.
    """
    for name, values in (("outcomes", outcomes), ("lower", lower), ("upper", upper)):
        if type(values) not in (list, tuple):
            raise TypeError(name + " must be a plain list or tuple")
    m = len(outcomes)
    if not 1 <= m <= MAX_OUTCOMES or len(lower) != m or len(upper) != m:
        raise ValueError("matching lists must contain 1..256 outcomes")
    if any(type(x) is not str for x in outcomes):
        raise TypeError("outcome identifiers must be plain strings")
    if any(not 1 <= len(x) <= MAX_IDENTIFIER_CHARS for x in outcomes):
        raise ValueError("outcome identifier length is outside 1..128")
    outcomes = tuple(outcomes)
    if len(set(outcomes)) != m:
        raise ValueError("outcome identifiers must be distinct")
    if provenance_reference is not None:
        if type(provenance_reference) is not str:
            raise TypeError("provenance_reference must be a plain string or None")
        if not 1 <= len(provenance_reference) <= MAX_PROVENANCE_CHARS:
            raise ValueError("provenance_reference length is outside 1..1024")
    if resource_limits is None:
        resource_limits = EnvelopeResourceLimits()
    if type(resource_limits) is not EnvelopeResourceLimits:
        raise TypeError("resource_limits must be an EnvelopeResourceLimits record")
    lower = tuple(_exact_probability(x, "lower endpoint") for x in lower)
    upper = tuple(_exact_probability(x, "upper endpoint") for x in upper)
    budget = None if proxy_budget is None else _exact_probability(proxy_budget, "proxy_budget")

    denominator_bits = sum(x.denominator.bit_length() for x in lower + upper)
    construction_bits = 2 * denominator_bits + (m - 1).bit_length() + 4
    comparison_bits = 0 if budget is None else (
        construction_bits + max(budget.numerator.bit_length(), budget.denominator.bit_length()) + 1)
    integer_slots = 32 * m + 64
    work_bits = integer_slots * max(MAX_INPUT_BITS, construction_bits, comparison_bits)
    plan = EnvelopeResourcePlan(construction_bits, comparison_bits, integer_slots, work_bits)

    def result(status, reason, certificate=None, compared_tv_bound=None):
        return EnvelopeResult(status, reason, outcomes, lower, upper, budget,
                              provenance_reference, resource_limits, plan,
                              certificate, compared_tv_bound)

    if max(construction_bits, comparison_bits) > resource_limits.max_intermediate_bits:
        return result("ABSTAIN_RESOURCE", "construction or comparison precision reservation exceeds limit")
    if work_bits > resource_limits.max_work_bits:
        return result("ABSTAIN_RESOURCE", "logical integer-storage reservation exceeds limit")

    # Every cross-product/LCM below is within the admitted construction bound.
    if any(lo.numerator * hi.denominator > hi.numerator * lo.denominator
           for lo, hi in zip(lower, upper)):
        raise ValueError("each lower endpoint must be at most its upper endpoint")
    denominator = 1
    for value in lower + upper:
        denominator = (denominator // gcd(denominator, value.denominator)) * value.denominator
    ell = tuple(x.numerator * (denominator // x.denominator) for x in lower)
    vee = tuple(x.numerator * (denominator // x.denominator) for x in upper)
    original_lower_total, original_upper_total = sum(ell), sum(vee)
    if not original_lower_total <= denominator <= original_upper_total:
        return result("INFEASIBLE_ENVELOPE", "original endpoint totals exclude normalization")
    alpha = tuple(max(lo, denominator - (original_upper_total - hi)) for lo, hi in zip(ell, vee))
    beta = tuple(min(hi, denominator - (original_lower_total - lo)) for lo, hi in zip(ell, vee))
    lower_total, upper_total = sum(alpha), sum(beta)
    a, b = denominator - lower_total, upper_total - denominator
    slack = upper_total - lower_total
    if slack == 0:
        weights = tuple(Fraction(x, denominator) for x in alpha)
        eta = Fraction(0)
    else:
        common = denominator * slack
        weights = tuple(Fraction(lo * slack + a * (hi - lo), common)
                        for lo, hi in zip(alpha, beta))
        eta = Fraction(a * b, common)
    if any(x.numerator.bit_length() > MAX_WEIGHT_BITS or
           x.denominator.bit_length() > MAX_WEIGHT_BITS for x in weights):
        return result("ABSTAIN_RESOURCE", "derived proxy exceeds categorical-map weight precision")
    products = None
    if budget is not None:
        products = (eta.numerator * budget.denominator, budget.numerator * eta.denominator)
        if products[0] > products[1]:
            return result("ABSTAIN_BUDGET", "computed TV allowance exceeds proxy_budget",
                          compared_tv_bound=eta)
    certificate = EnvelopeCertificate(
        denominator, ell, vee, alpha, beta, lower_total, upper_total, a, b, slack,
        tuple(Fraction(x, denominator) for x in alpha),
        tuple(Fraction(x, denominator) for x in beta), weights, eta, products)
    return result("CONDITIONAL_PROXY_CERTIFICATE", "arithmetic complete; scientific premises unverified",
                  certificate=certificate)
