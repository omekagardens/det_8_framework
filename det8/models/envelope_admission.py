"""Bounded D4-A component binding; scientific truth is external, always ABSTAIN.

Only a static two-arm comparison under approximate certificate A is supported.
The trusted-review keyword is a caller trust boundary, not authentication or
UI permission. No bytes, digest, review label or synthetic fixture supplies it.
This module performs no I/O, sampling, automatic acquisition or retry.
"""

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from math import gcd

from .certified_categorical_map import CategoricalMap
from .certified_probability_envelope import (
    EnvelopeResourceLimits, certify_probability_envelope,
)


MAX_JSON_BYTES = 65536
MAX_ARTIFACT_BYTES = 8192
MAX_TOTAL_BYTES = 196608
MAX_DEPTH = 10
MAX_NODES = 2048
MAX_ITEMS = 64
MAX_TEXT = 256
MAX_INTEGER_BITS = 256
# Fixed conservative reservations for BOTH arms, including fair-bit sums,
# risk sums, envelope witnesses and categorical-map arithmetic. Not OS limits.
REQUIRED_PRECISION_BITS = 32768
REQUIRED_WORK_BITS = 2048 * REQUIRED_PRECISION_BITS

REFERENCE_CLAIMS = (
    ("law_z_normalization", "original B(lambda=1), normalized z, z1=1, epsilon=1/4, h7"),
    ("parent_embedding", "D4-A labelled C3 ordinal-sum A3 width-channel embedding"),
    ("B_enclosure", "all 22 unconditional joint B ideal/bit probabilities enclosed"),
    ("Q_enclosure", "all 22 unconditional joint Q ideal/bit probabilities enclosed"),
    ("B_coverage", "B simultaneous coverage, frozen selection and justified failure bound"),
    ("Q_coverage", "Q simultaneous coverage, frozen selection and justified failure bound"),
    ("independent_review", "independent applicable enclosure review of this exact complete binding"),
)
RUN_BLOCKERS = (
    "effect: supply the certified positive effect and bias margin",
    "bit/channel: supply conditional-history and valid-return certificates",
    "availability: supply the selected decision's justified failure guarantee",
    "schedule/cost: supply feasible frozen n and total preparation/run/audit bounds",
)


def canonical_d4a_target():
    """Public syntax helper; these identifiers are not scientific credentials."""
    return {
        "labels": ["c0", "c1", "c2", "a0", "a1", "a2"],
        "strict_relations": [[i, j] for i in range(3) for j in range(i + 1, 6)],
        "old_bits": [0] * 6,
        "mask_convention": "label-index-is-lsb-bit-index",
        "sector": "complete-fair-bit-scalar-passive",
        "law": "original-B-and-original-h7-transform",
        "normalization": "original-normalized-harmonic-z-and-parent-scale",
        "lambda": [1, 1], "epsilon": [1, 4], "z1": [1, 1],
        "score": "width(new-order)-3",
        "embedding_reference": "parent_embedding",
        "law_reference": "law_z_normalization",
    }


def canonical_d4a_outcomes():
    """Regenerate order ideals from the fixed strict order; never pad a row."""
    relations = canonical_d4a_target()["strict_relations"]
    ideals = [mask for mask in range(64)
              if all(not (mask & (1 << j)) or mask & (1 << i)
                     for i, j in relations)]
    return [[mask, bit] for mask in ideals for bit in (0, 1)]


def _review_scope_digest(descriptor):
    """Only parsed bounded data reaches this identity helper; never review."""
    return sha256(json.dumps(
        {key: value for key, value in descriptor.items() if key != "review_scope_sha256"},
        sort_keys=True, separators=(",", ":"), ensure_ascii=True,
    ).encode("ascii")).hexdigest()


@dataclass(frozen=True)
class Reason:
    code: str
    field: str
    remedy: str


@dataclass(frozen=True)
class ArmBinding:
    arm: str
    original_lower: tuple
    original_upper: tuple
    coverage_failure: Fraction
    envelope: object
    categorical_map: object


@dataclass(frozen=True)
class AdmissionResult:
    status: str
    reasons: tuple = ()
    descriptor_bytes: bytes = b""
    comparison_bytes: bytes = b""
    reference_bytes: tuple = ()
    arms: tuple = ()
    endpoint_failure_sum: object = None
    total_certificate_risk: object = None

    @property
    def operational_admission(self):
        return "ABSTAIN"

    @property
    def operational_reasons(self):
        return RUN_BLOCKERS


class _Refusal(Exception):
    def __init__(self, code, field, remedy):
        self.reason = Reason(code, field, remedy)


def _need(condition, code, field, remedy):
    if not condition:
        raise _Refusal(code, field, remedy)


def _keys(value, expected, field):
    _need(type(value) is dict and set(value) == set(expected), "ABSTAIN_SCHEMA", field,
          "supply exactly the documented object fields; unknown/missing fields are refused")


def _parse(data, field):
    # Check nesting BEFORE json.loads; brackets in escaped strings do not count.
    depth, quoted, escaped = 0, False, False
    text = data.decode("utf-8", errors="strict")
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            _need(depth <= MAX_DEPTH, "ABSTAIN_RESOURCE", field, "reduce JSON nesting to 10")
        elif char in "]}":
            depth -= 1

    def integer(text):
        _need(len(text.lstrip("-")) <= 78, "ABSTAIN_RESOURCE", field,
              "use integers with at most 256 bits")
        value = int(text)
        _need(value.bit_length() <= MAX_INTEGER_BITS, "ABSTAIN_RESOURCE", field,
              "use integers with at most 256 bits")
        return value

    def forbidden_number(text):
        raise _Refusal("ABSTAIN_SCHEMA", field, "use exact integer pairs, never floats/NaN/Infinity")

    def pairs(items):
        result = {}
        for key, value in items:
            _need(key not in result, "ABSTAIN_SCHEMA", field, "remove duplicate JSON keys")
            result[key] = value
        return result

    value = json.loads(text, parse_int=integer, parse_float=forbidden_number,
                       parse_constant=forbidden_number, object_pairs_hook=pairs)
    pending, count = [value], 0
    while pending:
        item = pending.pop()
        count += 1
        _need(count <= MAX_NODES, "ABSTAIN_RESOURCE", field, "use at most 2048 JSON nodes")
        if type(item) in (dict, list):
            _need(len(item) <= MAX_ITEMS, "ABSTAIN_RESOURCE", field,
                  "use at most 64 items in each object or array")
            pending.extend(item.values() if type(item) is dict else item)
            if type(item) is dict:
                pending.extend(item.keys())
        elif type(item) is str:
            _need(len(item) <= MAX_TEXT, "ABSTAIN_RESOURCE", field, "use strings of at most 256 characters")
        else:
            _need(type(item) is int, "ABSTAIN_SCHEMA", field, "use only objects, arrays, strings and integers")
    return value


def _prob(pair, field):
    _need(type(pair) is list and len(pair) == 2 and all(type(x) is int for x in pair),
          "ABSTAIN_ENDPOINT_SEMANTICS", field, "supply a reduced [numerator, denominator] pair")
    n, d = pair
    _need(d > 0 and 0 <= n <= d and gcd(n, d) == 1,
          "ABSTAIN_ENDPOINT_SEMANTICS", field, "supply a reduced rational in [0,1], denominator positive")
    return Fraction(n, d)


def _digest(value, field):
    _need(type(value) is str and len(value) == 64 and all(c in "0123456789abcdef" for c in value),
          "ABSTAIN_BINDING", field, "supply the lowercase SHA-256 of the exact supplied bytes")


def admit_d4a_envelope(descriptor_bytes, comparison_bytes, reference_bytes, *,
                       trusted_review_applicable=False):
    """Bind/check two complete rows, then recompute conditional certificates.

    Inputs are plain bytes, plain bytes, and a plain dict of the seven required
    role names to plain bytes. No paths or callbacks are accepted. The separate
    exact-bool keyword asserts that the CALLER's trusted review is applicable
    to these exact target, ordered row, endpoint, coverage, selection, risk and
    reference bytes. It is not a UI approval, authenticity test, or proof check.
    Treat untrusted callers as unable to grant this assertion. Synthetic tests
    assert it only to exercise control flow, never to accept scientific input.

    Every result remains operational ABSTAIN. Ordinary exceptions refuse with
    no partial result; interruptions propagate with no result and are likewise
    non-admission. No generic proof system or scientific endpoint producer exists.
    """
    try:
        return _admit(descriptor_bytes, comparison_bytes, reference_bytes,
                      trusted_review_applicable)
    except _Refusal as error:
        return AdmissionResult(error.reason.code, (error.reason,))
    except (ValueError, TypeError, UnicodeError, RecursionError):
        return AdmissionResult("ABSTAIN_SCHEMA", (Reason(
            "ABSTAIN_SCHEMA", "input", "supply valid bounded JSON bytes and closed primitive types"),))
    except Exception:
        # Includes allocation failure: nothing returned can authorize admission.
        return AdmissionResult("ABSTAIN_EXCEPTION", (Reason(
            "ABSTAIN_EXCEPTION", "implementation", "resolve the unexpected failure; do not retry automatically"),))


def _admit(raw, comparison_raw, artifacts, trusted):
    _need(type(trusted) is bool, "ABSTAIN_COVERAGE_OR_REVIEW", "trusted_review_applicable",
          "supply a separate exact-bool trusted-caller applicability decision")
    for field, value in (("descriptor", raw), ("comparison", comparison_raw)):
        _need(type(value) is bytes, "ABSTAIN_SCHEMA", field, "supply plain bytes, not objects or subclasses")
        _need(0 < len(value) <= MAX_JSON_BYTES, "ABSTAIN_RESOURCE", field, "supply 1..65536 bytes")
    roles = tuple(role for role, _ in REFERENCE_CLAIMS)
    _need(type(artifacts) is dict, "ABSTAIN_SCHEMA", "reference_bytes", "supply a plain dictionary")
    _need(len(artifacts) == len(roles) and all(type(k) is str for k in artifacts),
          "ABSTAIN_BINDING", "reference_bytes", "supply exactly the seven documented plain-string roles")
    _need(set(artifacts) == set(roles), "ABSTAIN_BINDING", "reference_bytes", "supply all seven exact roles")
    for role in roles:
        _need(type(artifacts[role]) is bytes, "ABSTAIN_SCHEMA", role, "supply plain bytes")
        _need(0 < len(artifacts[role]) <= MAX_ARTIFACT_BYTES, "ABSTAIN_RESOURCE", role,
              "supply 1..8192 reference bytes")
    _need(len(raw) + len(comparison_raw) + sum(len(x) for x in artifacts.values()) <= MAX_TOTAL_BYTES,
          "ABSTAIN_RESOURCE", "input", "reduce combined input to 196608 bytes")
    descriptor, comparison = _parse(raw, "descriptor"), _parse(comparison_raw, "comparison")
    _keys(descriptor, ("schema", "comparison_sha256", "target", "outcome_dictionary", "arms",
                       "review_scope_sha256"), "descriptor")
    _keys(comparison, ("schema", "protocol", "selection", "target", "references", "budgets"), "comparison")
    _need(descriptor["schema"] == "d4a-full-row-envelope-v1" and
          comparison["schema"] == "d4a-frozen-comparison-v1", "ABSTAIN_SCHEMA", "schema",
          "use this version's fixed two-arm bounded profile")
    _need(comparison["protocol"] == "approximate-certificate-A" and
          comparison["selection"] == "pre-held-out-fixed-comparison", "ABSTAIN_PROOF_SCOPE", "comparison",
          "supply the frozen static certificate-A comparison; other protocols need a separate adapter")
    _digest(descriptor["comparison_sha256"], "comparison_sha256")
    _need(descriptor["comparison_sha256"] == sha256(comparison_raw).hexdigest(),
          "ABSTAIN_BINDING", "comparison_sha256", "bind the exact separately supplied frozen comparison bytes")
    expected_target = canonical_d4a_target()
    _need(descriptor["target"] == expected_target and comparison["target"] == expected_target,
          "ABSTAIN_TARGET_OR_COMPLETENESS", "target", "restore the fixed labelled D4-A law/normalization/sector/parent")
    _need(descriptor["outcome_dictionary"] == canonical_d4a_outcomes(),
          "ABSTAIN_ROW_DICTIONARY", "outcome_dictionary", "supply all regenerated ideals, then bits 0/1, in exact order")
    _keys(comparison["references"], roles, "references")
    for role, claim in REFERENCE_CLAIMS:
        ref = comparison["references"][role]
        _keys(ref, ("sha256", "claim"), "references." + role)
        _digest(ref["sha256"], role)
        _need(ref["sha256"] == sha256(artifacts[role]).hexdigest() and ref["claim"] == claim,
              "ABSTAIN_BINDING", role, "supply matching exact reference bytes and the required claim scope")
    _digest(descriptor["review_scope_sha256"], "review_scope_sha256")
    _need(descriptor["review_scope_sha256"] == _review_scope_digest(descriptor),
          "ABSTAIN_COVERAGE_OR_REVIEW", "review_scope_sha256", "bind the review scope to this exact declared content")
    budgets = comparison["budgets"]
    _keys(budgets, ("B", "Q", "other_certificate_risk", "kappa_budget", "max_intermediate_bits", "max_work_bits"), "budgets")
    for name, ceiling in (("max_intermediate_bits", REQUIRED_PRECISION_BITS),
                          ("max_work_bits", REQUIRED_WORK_BITS)):
        _need(type(budgets[name]) is int and 0 <= budgets[name] <= ceiling,
              "ABSTAIN_RESOURCE", name, "declare a reservation within the documented bounded profile")
        _need(budgets[name] == ceiling, "ABSTAIN_RESOURCE", name,
              "reserve this profile's complete fixed two-arm logical arithmetic allowance")
    limits = EnvelopeResourceLimits(budgets["max_intermediate_bits"], budgets["max_work_bits"])
    other_risk = _prob(budgets["other_certificate_risk"], "other_certificate_risk")
    kappa_budget = _prob(budgets["kappa_budget"], "kappa_budget")
    _keys(descriptor["arms"], ("B", "Q"), "arms")
    parsed = []
    for arm in ("B", "Q"):
        row, budget = descriptor["arms"][arm], budgets[arm]
        _keys(row, ("arm", "endpoints", "coverage", "evidence"), arm)
        _need(row["arm"] == arm, "ABSTAIN_BINDING", arm, "keep the B and Q bindings distinct")
        _keys(budget, ("proxy", "bit_width", "rounding"), "budgets." + arm)
        proxy_budget, rounding_budget = _prob(budget["proxy"], arm + ".proxy"), _prob(budget["rounding"], arm + ".rounding")
        _need(type(budget["bit_width"]) is int and 0 <= budget["bit_width"] <= 256,
              "ABSTAIN_RESOURCE", arm + ".bit_width", "declare an integer bit width in 0..256")
        _need(type(row["endpoints"]) is list and len(row["endpoints"]) == 22,
              "ABSTAIN_ROW_COMPLETENESS", arm + ".endpoints", "retain exactly one endpoint pair for every ordered joint outcome")
        lower, upper = [], []
        for i, endpoint in enumerate(row["endpoints"]):
            field = arm + ".endpoints[" + str(i) + "]"
            _keys(endpoint, ("lower", "upper"), field)
            lo, hi = _prob(endpoint["lower"], field + ".lower"), _prob(endpoint["upper"], field + ".upper")
            _need(lo <= hi and hi > 0, "ABSTAIN_ENDPOINT_SEMANTICS", field,
                  "supply ordered bounds; an upper zero contradicts this strictly positive target")
            lower.append(lo)
            upper.append(hi)
        _need(sum(lower, Fraction(0)) <= 1 <= sum(upper, Fraction(0)),
              "ABSTAIN_ENDPOINT_SEMANTICS", arm + ".endpoints", "supply an original box containing a normalized row")
        fair_lower = [max(lower[i:i+2]) for i in range(0, 22, 2)]
        fair_upper = [min(upper[i:i+2]) for i in range(0, 22, 2)]
        _need(all(lo <= hi for lo, hi in zip(fair_lower, fair_upper)) and
              2 * sum(fair_lower, Fraction(0)) <= 1 <= 2 * sum(fair_upper, Fraction(0)),
              "ABSTAIN_ENDPOINT_SEMANTICS", arm + ".fair_bit", "supply intervals compatible with some normalized equal-bit row")
        coverage = row["coverage"]
        _keys(coverage, ("mode", "scope", "selection", "failure"), arm + ".coverage")
        _need(coverage["mode"] in ("deterministic", "statistical") and
              coverage["scope"] == "simultaneous-full-unconditional-joint-row" and
              coverage["selection"] == comparison["selection"], "ABSTAIN_PROOF_SCOPE", arm + ".coverage",
              "supply full simultaneous unconditional coverage for the frozen selection procedure")
        failure = _prob(coverage["failure"], arm + ".coverage.failure")
        _need(coverage["mode"] != "deterministic" or failure == 0,
              "ABSTAIN_COVERAGE_OR_REVIEW", arm + ".coverage", "this deterministic profile requires reviewed zero-risk enclosures")
        _need(row["evidence"] == {"derivation": arm + "_enclosure", "coverage": arm + "_coverage"},
              "ABSTAIN_BINDING", arm + ".evidence", "bind each arm to its own derivation and coverage reference bytes")
        parsed.append((arm, tuple(lower), tuple(upper), failure, proxy_budget, rounding_budget, budget["bit_width"]))
    endpoint_risk = parsed[0][3] + parsed[1][3]
    total_risk = endpoint_risk + other_risk
    _need(total_risk <= kappa_budget < Fraction(1, 20), "ABSTAIN_RISK_BUDGET", "kappa_budget",
          "justify summed endpoint plus other certificate risks within kappa < 1/20; never add them to eta")
    _need(trusted, "ABSTAIN_COVERAGE_OR_REVIEW", "trusted_review_applicable",
          "obtain an applicable independent scientific review via the trusted caller boundary")
    admitted = []
    outcomes = tuple(str(mask) + ":" + str(bit) for mask, bit in canonical_d4a_outcomes())
    for arm, lower, upper, failure, proxy_budget, rounding_budget, bit_width in parsed:
        result = certify_probability_envelope(outcomes, lower, upper, proxy_budget=proxy_budget,
                                             resource_limits=limits, provenance_reference=None)
        _need(result.status == "CONDITIONAL_PROXY_CERTIFICATE", result.status, arm + ".envelope", result.reason)
        mapping = CategoricalMap(result.certificate.proxy_weights, bit_width)
        _need(mapping.rounding_tv <= rounding_budget, "ABSTAIN_ROUNDING_BUDGET", arm + ".rounding",
              "supply an adequate predeclared map-rounding allowance; do not alter the proxy")
        admitted.append(ArmBinding(arm, tuple((x.numerator, x.denominator) for x in lower),
                                   tuple((x.numerator, x.denominator) for x in upper),
                                   failure, result, mapping))
    return AdmissionResult("COMPONENT_PREMISES_REVIEWED", descriptor_bytes=raw,
                           comparison_bytes=comparison_raw,
                           reference_bytes=tuple((role, artifacts[role]) for role in roles),
                           arms=tuple(admitted), endpoint_failure_sum=endpoint_risk,
                           total_certificate_risk=total_risk)
