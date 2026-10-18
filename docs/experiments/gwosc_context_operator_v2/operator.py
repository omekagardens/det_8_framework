"""RI-60 coordinate-error enclosures for the exact finite RI-55 operator.

This separate engine revises RI-57's failed uniform-radius method.  No files,
packages, admitted coefficients or samples are loaded here.  Callers supply
exact Fraction SOS coefficients, pads and seeds.  A certificate concerns the
exact rational finite operator, not floating-point filtering or a physical
continuation.  The independent v1 oracle is not copied into this module.

Point centers use the unchanged 256-significant-bit nearest/even recurrences.
Matrix intervals use 256-bit directed rounding.  Each nonnegative error-bound
expression is evaluated exactly with Fraction and then rounded upwards once
at 256 significant bits.  Coefficients, J, h, DC gains, quadratic forms and
local rounding residuals are exact.  There is no silent underflow: a nonzero
quantity outside the declared rounding exponent range refuses certification.
Exact intermediate/proof integer sizes, dimensions and work are also capped.

For H=[[-a1,1],[-a2,0]], c=(1,0), J=(b1-a1*b0,b2-a2*b0), and
h=(g-b0,b2-a2*g), point adjoints round only lambda[0], copying
lambda[1]=next_lambda[0] exactly.  A coordinate input-error radius is r[k].
Let eL[k], eX[k], eP denote exact magnitudes of local state-first-coordinate,
output and startup-scalar rounding residuals.

For the complex class a2>0, D=a2-a1*a1/4>0, define
P=[[a2,-a1/2],[-a1/2,1]], Q=P**-1.  Exact identities
H.T*P*H=a2*P and H*Q*H.T=a2*Q imply
||H.T*error||_Q=sqrt(a2)||error||_Q.  Dual Cauchy-Schwarz gives
|J.T*error|<=sqrt(J.T*P*J)||error||_Q, likewise for h; the norm of
first-coordinate forcing is sqrt(Q[0,0])=sqrt(1/D).  Obtain upward constants
rho=sqrt_up(a2)<1, jnorm=sqrt_up(J.T*P*J), hnorm=sqrt_up(h.T*P*h),
and force=sqrt_up(1/D).  With s_next initially zero, evaluate
    output_radius[k] = up(|b0|*r[k] + jnorm*s_next + eX[k]),
    s_current = up(rho*s_next + force*(r[k] + eL[k])).
The output uses s_next BEFORE updating the state.  Startup radius is
up(hnorm*s_0+eP).  These are norm bounds on the signed stable transition,
not an absolute-matrix recurrence for complex poles.

For a2=0, exact stability gives |a1|<1.  Maintain component error bounds
(t0,t1), initially zero, using
    output_radius[k] = up(|b0|*r[k]+|J0|*t0+|J1|*t1+eX[k]),
    (t0,t1) = (up(|a1|*t0+r[k]+eL[k]), t0).
Startup radius is up(|h0|*t0+|h1|*t1+eP).  This class covers the frozen
first-order/FIR toys.  Other stable denominator classes are unresolved.

Each section's startup scalar bypasses preceding sections: multiply by that
section's exact preceding DC-gain product, accumulate its point value/error,
and add the total ONLY to the original pass input's coordinate zero, including
that addition's exact residual.  Other coordinate radii are not enlarged by
startup error.  Reversal and zero insertion apply to both points and radii;
the odd-extension transpose uses each coordinate's absolute signed weights and
its own final point-rounding residual.  Correlations are conservatively bounded.

The unchanged fixed K=2**j (j=0,...,20) outward signed-power searches must
certify contraction for H and H.T separately.  Exact P identities also bound
finite remainder powers; the a2=0 class uses direct exact remainder bounds.
These are admission checks, not a promise of passing the frozen width gates.
No precision, dimensions, row choices or qualification thresholds are adapted.

The returned scalar radius is only the maximum of the final coordinate radii;
intervals use individual radii.  Proof traces identify radius vectors by exact
canonical hashes, maxima, endpoints and counts rather than dumping all steps.
The exact small forward/adjoint helpers retain the v1 DFII formulas unchanged;
the same new validated method runs for both tiny and admitted-length requests.
"""

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from math import isqrt


PRECISION = 256
N, L, T = 2769, 4096, 10961
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
MAX_LENGTH = T
MAX_PASS_LENGTH = T + 54
MAX_STAGES = 17
MAX_SECTIONS = 20
MAX_PAD = 27
MAX_INPUT_BITS = 512
MAX_INTERMEDIATE_BITS = 262144
MAX_PROOF_INTEGER_BITS = 12288
MAX_EXPONENT = 16384
MAX_EXACT_LENGTH = 64
MAX_EXACT_SECTIONS = 4
MAX_STATE_UPDATES = 2 * MAX_SECTIONS * MAX_PASS_LENGTH
ZERO, ONE = Fraction(0), Fraction(1)
_PREPARED_TOKEN = object()


class CertificationError(ValueError):
    """No certificate is returned when the declared method cannot complete."""

    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def arithmetic_contract():
    return {
        "schema_version": "ri60-coordinate-operator-v2",
        "precision_bits": PRECISION,
        "point_rounding": "nearest_binary_significand_ties_to_even",
        "interval_rounding": "directed_binary_significand",
        "endpoint_and_residual_arithmetic": "exact_stdlib_Fraction",
        "error_propagation": "per_coordinate_dual_quadratic_state_norm_or_a2_zero_components",
        "bound_rounding": "exact_nonnegative_Fraction_expression_then_upward_256_bits",
        "radius_vector_encoding": "ri60-radius-vector-v1 LF; decimal length LF; numerator/denominator LF per coordinate",
        "scalar_radius_semantics": "exact_maximum_of_coordinate_radii_not_used_to_propagate",
        "point_center_compatibility": "unchanged_ri57_operation_order",
        "power_exponents": list(range(21)),
        "power_norm": "infinity_for_H_and_H_transpose_separately",
        "max_binary_exponent_magnitude": MAX_EXPONENT,
        "max_input_integer_bits": MAX_INPUT_BITS,
        "max_intermediate_integer_bits": MAX_INTERMEDIATE_BITS,
        "max_proof_integer_bits": MAX_PROOF_INTEGER_BITS,
        "max_length": MAX_LENGTH,
        "max_pass_length": MAX_PASS_LENGTH,
        "max_stages": MAX_STAGES,
        "max_sections": MAX_SECTIONS,
        "max_padding": MAX_PAD,
        "max_exact_length": MAX_EXACT_LENGTH,
        "max_exact_sections": MAX_EXACT_SECTIONS,
        "max_state_updates_per_certified_adjoint": MAX_STATE_UPDATES,
        "pilot": {"N": N, "L": L, "T": T, "rows": list(ROWS)},
        "unsupported_stable_denominator": "a2 != 0 and a2-a1*a1/4 <= 0",
        "failure_policy": "no_certificate_on_invalid_unresolved_or_resource_failure",
        "scope": "exact_finite_rational_operator_not_rounded_production",
    }


def _q(value):
    if not _bits_ok(value, MAX_PROOF_INTEGER_BITS):
        raise CertificationError("resource_proof_integer_bits", "Exact proof serialization cap exceeded")
    return [str(value.numerator), str(value.denominator)]


def _bits_ok(value, limit):
    return max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= limit


def _bounded(value):
    if not _bits_ok(value, MAX_INTERMEDIATE_BITS):
        raise CertificationError("resource_integer_bits", "Exact intermediate integer cap exceeded")
    return value


def _floor_log2_positive(value):
    e = value.numerator.bit_length() - value.denominator.bit_length()
    if e >= 0:
        if value.numerator < value.denominator << e:
            e -= 1
    elif value.numerator << -e < value.denominator:
        e -= 1
    return e


def _pow2(exponent):
    return Fraction(1 << exponent) if exponent >= 0 else Fraction(1, 1 << -exponent)


def _rounded(value, direction="nearest"):
    """Exactly determine one bounded 256-bit dyadic rounding operation."""
    _bounded(value)
    if value == 0:
        return ZERO
    sign = 1 if value > 0 else -1
    absolute = abs(value)
    exponent = _floor_log2_positive(absolute)
    if not -MAX_EXPONENT <= exponent <= MAX_EXPONENT:
        raise CertificationError("resource_exponent", "Binary exponent cap exceeded")
    quantum = _pow2(exponent - PRECISION + 1)
    scaled = absolute / quantum
    integer, remainder = divmod(scaled.numerator, scaled.denominator)
    if direction == "nearest":
        twice = 2 * remainder
        if twice > scaled.denominator or (twice == scaled.denominator and integer % 2):
            integer += 1
    elif direction == "up":
        if sign > 0 and remainder:
            integer += 1
    elif direction == "down":
        if sign < 0 and remainder:
            integer += 1
    else:
        raise ValueError("Unknown rounding direction")
    result = sign * integer * quantum
    if result and abs(_floor_log2_positive(abs(result))) > MAX_EXPONENT:
        raise CertificationError("resource_exponent", "Rounded binary exponent cap exceeded")
    return _bounded(result)


def _sqrt_up(value):
    if value < 0:
        raise CertificationError("negative_square_root", "Invalid square-root certificate")
    if value == 0:
        return ZERO
    _bounded(value)
    exponent = _floor_log2_positive(value) // 2
    if not -MAX_EXPONENT <= exponent <= MAX_EXPONENT:
        raise CertificationError("resource_exponent", "Square-root exponent cap exceeded")
    quantum = _pow2(exponent - PRECISION + 1)
    square = _bounded(value / (quantum * quantum))
    integer = isqrt(square.numerator // square.denominator)
    if integer * integer * square.denominator < square.numerator:
        integer += 1
    result = _bounded(integer * quantum)
    if result * result < value:
        raise CertificationError("arithmetic_failure", "Square-root outward check failed")
    return result


def _point(value):
    result = _rounded(value)
    return result, _bounded(abs(value - result))


def _interval(value):
    return (_rounded(value, "down"), _rounded(value, "up"))


def _iadd(left, right):
    return (_rounded(left[0] + right[0], "down"),
            _rounded(left[1] + right[1], "up"))


def _imul(left, right):
    products = tuple(_bounded(x * y) for x in left for y in right)
    return (_rounded(min(products), "down"), _rounded(max(products), "up"))


def _matrix_product(left, right):
    return tuple(tuple(_iadd(_imul(left[i][0], right[0][j]),
                            _imul(left[i][1], right[1][j]))
                       for j in range(2)) for i in range(2))


def _norm_upper(matrix, transpose=False):
    return max(sum((max(abs(matrix[j][i][0]), abs(matrix[j][i][1]))
                    if transpose else max(abs(matrix[i][j][0]), abs(matrix[i][j][1]))
                    for j in range(2)), ZERO) for i in range(2))


def _power_certificates(a1, a2):
    power = tuple(tuple(_interval(x) for x in row)
                  for row in ((-a1, ONE), (-a2, ZERO)))
    witnesses = {}
    for exponent in range(21):
        for name, transposed in (("H", False), ("H_transpose", True)):
            if name not in witnesses:
                bound = _norm_upper(power, transposed)
                if bound < 1:
                    witnesses[name] = {
                        "K": 1 << exponent,
                        "norm_upper": _q(bound),
                        "power_intervals": [[[_q(x[0]), _q(x[1])] for x in row]
                                            for row in power],
                        "stored_power_is_H": True,
                        "transpose_for_this_witness": transposed,
                    }
        if len(witnesses) == 2:
            return witnesses
        if exponent < 20:
            power = _matrix_product(power, power)
    raise CertificationError("unresolved_contraction", "No contraction in fixed 21-power search")


@dataclass(frozen=True)
class _Section:
    sos: tuple
    gain: Fraction
    preceding_gain: Fraction
    J: tuple
    h: tuple
    rho: Fraction
    force: Fraction
    jnorm: Fraction
    hnorm: Fraction
    proof: dict


@dataclass(frozen=True, init=False)
class Prepared:
    stages: tuple
    padlens: tuple
    profiles: tuple

    def __init__(self, stages, padlens, profiles, *, _token=None):
        if _token is not _PREPARED_TOKEN:
            raise ValueError("Prepared objects must be obtained through prepare")
        object.__setattr__(self, "stages", stages)
        object.__setattr__(self, "padlens", padlens)
        object.__setattr__(self, "profiles", profiles)


def _validate_stages(stages, padlens):
    if type(stages) not in (list, tuple) or not 1 <= len(stages) <= MAX_STAGES:
        raise ValueError("Expected 1..17 ordered stages")
    if type(padlens) not in (list, tuple) or len(padlens) != len(stages):
        raise ValueError("One pad length is required per stage")
    result = []
    count = 0
    for stage, pad in zip(stages, padlens):
        if type(pad) is not int or not 0 <= pad <= MAX_PAD:
            raise ValueError("Padding must be an integer in [0,27]")
        if type(stage) not in (list, tuple) or not stage:
            raise ValueError("A stage must contain SOS sections")
        converted = []
        for sos in stage:
            if type(sos) not in (list, tuple) or len(sos) != 6:
                raise ValueError("A section must contain six exact Fraction coefficients")
            if any(type(x) is not Fraction or not _bits_ok(x, MAX_INPUT_BITS) for x in sos):
                raise ValueError("Coefficient type or 512-bit resource limit is invalid")
            b0, b1, b2, a0, a1, a2 = sos
            if a0 != 1 or 1 + a1 + a2 == 0:
                raise ValueError("Expected a0=1 and nonzero DC denominator")
            if not (abs(a2) < 1 and 1 + a1 + a2 > 0 and 1 - a1 + a2 > 0):
                raise ValueError("Exact Jury stability inequalities failed")
            converted.append(tuple(sos))
            count += 1
            if count > MAX_SECTIONS:
                raise ValueError("At most 20 SOS sections are supported")
        result.append(tuple(converted))
    return tuple(result), tuple(padlens)


def _profile(sos, preceding_gain):
    b0, b1, b2, _, a1, a2 = sos
    gain = _bounded((b0 + b1 + b2) / (1 + a1 + a2))
    J = (b1 - a1 * b0, b2 - a2 * b0)
    h = (gain - b0, b2 - a2 * gain)
    determinant = a2 - a1 * a1 / 4
    if a2 == 0:
        rho, force, jnorm, hnorm = abs(a1), ONE, ZERO, ZERO
        kind = "a2_zero_coordinate_components"
        extra = {"remainder_H_infinity_upper": _q(max(ONE, 1 + abs(a1))),
                 "remainder_H_transpose_infinity_upper": _q(ONE),
                 "state_component_contraction": _q(abs(a1))}
    elif a2 > 0 and determinant > 0:
        P = ((a2, -a1 / 2), (-a1 / 2, ONE))
        Q = ((1 / determinant, a1 / (2 * determinant)),
             (a1 / (2 * determinant), a2 / determinant))
        H = ((-a1, ONE), (-a2, ZERO))
        primal = tuple(tuple(sum((H[k][i] * P[k][ell] * H[ell][j]
                                  for k in range(2) for ell in range(2)), ZERO)
                             for j in range(2)) for i in range(2))
        dual = tuple(tuple(sum((H[i][k] * Q[k][ell] * H[j][ell]
                                for k in range(2) for ell in range(2)), ZERO)
                           for j in range(2)) for i in range(2))
        inverse = tuple(tuple(sum((P[i][k] * Q[k][j] for k in range(2)), ZERO)
                              for j in range(2)) for i in range(2))
        if (primal != tuple(tuple(a2 * x for x in row) for row in P)
                or dual != tuple(tuple(a2 * x for x in row) for row in Q)
                or inverse != ((ONE, ZERO), (ZERO, ONE))):
            raise CertificationError("arithmetic_failure", "Exact primal/dual quadratic identities failed")
        rho = _sqrt_up(a2)
        if rho >= 1:
            raise CertificationError("unresolved_quadratic", "Outward decay bound reaches one")
        force = _sqrt_up(1 / determinant)
        def norm_upper(v):
            quadratic = _bounded(a2 * v[0] * v[0] - a1 * v[0] * v[1] + v[1] * v[1])
            if quadratic < 0:
                raise CertificationError("arithmetic_failure", "Positive quadratic form failed")
            return _sqrt_up(quadratic)
        jnorm, hnorm = norm_upper(J), norm_upper(h)
        diagonal_p = (a2, ONE)
        diagonal_inverse = (1 / determinant, a2 / determinant)
        entry_bounds = tuple(tuple(_sqrt_up(diagonal_inverse[i] * diagonal_p[j])
                                   for j in range(2)) for i in range(2))
        remainder = max(sum(row, ZERO) for row in entry_bounds)
        remainder_transpose = max(sum((entry_bounds[j][i] for j in range(2)), ZERO)
                                  for i in range(2))
        kind = "coordinate_dual_quadratic_norm"
        extra = {"P": [[_q(x) for x in row] for row in P],
                 "Q": [[_q(x) for x in row] for row in Q],
                 "exact_primal_and_dual_identity": True,
                 "determinant": _q(determinant), "rho_upper": _q(rho),
                 "forcing_norm_upper": _q(force),
                 "J_dual_norm_upper": _q(jnorm), "h_dual_norm_upper": _q(hnorm),
                 "remainder_entry_bounds": [[_q(x) for x in row] for row in entry_bounds],
                 "remainder_H_infinity_upper": _q(remainder),
                 "remainder_H_transpose_infinity_upper": _q(remainder_transpose)}
    else:
        raise CertificationError("unresolved_denominator_class", "Stable denominator lacks the declared state-norm certificate")
    powers = _power_certificates(a1, a2)
    proof = {"method": kind, "jury_exact": True, "powers": powers,
             "gain": _q(gain), "preceding_gain": _q(preceding_gain),
             "J": [_q(x) for x in J], "h": [_q(x) for x in h], **extra}
    return _Section(sos, gain, preceding_gain, J, h, rho, force, jnorm, hnorm, proof)


def prepare(stages, padlens):
    """Validate exact coefficients and obtain input-independent certificates."""
    stages, padlens = _validate_stages(stages, padlens)
    profiles = []
    for stage in stages:
        preceding_gain = ONE
        row = []
        for sos in stage:
            profile = _profile(sos, preceding_gain)
            row.append(profile)
            preceding_gain = _bounded(preceding_gain * profile.gain)
        profiles.append(tuple(row))
    return Prepared(stages, padlens, tuple(profiles), _token=_PREPARED_TOKEN)


def _values(values, padlens, exact=False):
    if type(values) not in (list, tuple):
        raise ValueError("Expected a list or tuple of exact Fraction values")
    maximum = MAX_EXACT_LENGTH if exact else MAX_LENGTH
    if not 2 <= len(values) <= maximum:
        raise ValueError("Vector length outside the declared resource limit")
    if any(type(x) is not Fraction or not _bits_ok(x, MAX_INPUT_BITS) for x in values):
        raise ValueError("Seed/input must contain exact Fractions of at most 512 bits")
    if any(p >= len(values) - 1 or len(values) + 2 * p > MAX_PASS_LENGTH for p in padlens):
        raise ValueError("Padding incompatible with the vector length")
    return tuple(values)


def _odd(values, pad):
    return (tuple(2 * values[0] - values[k] for k in range(pad, 0, -1))
            + tuple(values)
            + tuple(2 * values[-1] - values[-k - 1] for k in range(1, pad + 1)))


def _odd_transpose(values, pad, length):
    result = list(values[pad:pad + length])
    for k in range(pad):
        result[0] += 2 * values[k]
        result[pad - k] -= values[k]
        result[-1] += 2 * values[pad + length + k]
        result[length - 2 - k] -= values[pad + length + k]
    return tuple(_bounded(x) for x in result)


def _constants(stage):
    preceding = ONE
    result = []
    for sos in stage:
        b0, b1, b2, _, a1, a2 = sos
        gain = (b0 + b1 + b2) / (1 + a1 + a2)
        result.append((sos, preceding, (b1 - a1 * b0, b2 - a2 * b0),
                       (gain - b0, b2 - a2 * gain)))
        preceding = _bounded(preceding * gain)
    return result


def _forward_exact_pass(values, stage):
    original_first = values[0]
    for sos, preceding, J, h in _constants(stage):
        b0, _, _, _, a1, a2 = sos
        z0, z1 = (h[0] * preceding * original_first, h[1] * preceding * original_first)
        result = []
        for x in values:
            result.append(_bounded(z0 + b0 * x))
            z0, z1 = (_bounded(-a1 * z0 + z1 + J[0] * x),
                      _bounded(-a2 * z0 + J[1] * x))
        values = tuple(result)
    return values


def _adjoint_exact_pass(values, stage):
    startup = ZERO
    for sos, preceding, J, h in reversed(_constants(stage)):
        b0, _, _, _, a1, a2 = sos
        lambda0 = lambda1 = ZERO
        result = [ZERO] * len(values)
        for k in range(len(values) - 1, -1, -1):
            result[k] = _bounded(b0 * values[k] + J[0] * lambda0 + J[1] * lambda1)
            lambda0, lambda1 = (_bounded(values[k] - a1 * lambda0 - a2 * lambda1), lambda0)
        startup = _bounded(startup + preceding * (h[0] * lambda0 + h[1] * lambda1))
        values = tuple(result)
    result = list(values)
    result[0] = _bounded(result[0] + startup)
    return tuple(result)


def _exact_inputs(values, stages, padlens):
    stages, padlens = _validate_stages(stages, padlens)
    if sum(len(stage) for stage in stages) > MAX_EXACT_SECTIONS:
        raise ValueError("Exact helper is limited to four SOS sections")
    return _values(values, padlens, exact=True), stages, padlens


def forward_fraction(values, stages, padlens):
    """Exact small-system forward evaluation using DFII states."""
    values, stages, padlens = _exact_inputs(values, stages, padlens)
    length = len(values)
    for stage, pad in zip(stages, padlens):
        values = _forward_exact_pass(_odd(values, pad), stage)
        values = _forward_exact_pass(values[::-1], stage)[::-1]
        values = values[pad:pad + length]
    return tuple(values)


def adjoint_fraction(seed, stages, padlens):
    """Exact small-system startup-aware DFII adjoint."""
    values, stages, padlens = _exact_inputs(seed, stages, padlens)
    length = len(values)
    for stage, pad in reversed(tuple(zip(stages, padlens))):
        values = (ZERO,) * pad + values + (ZERO,) * pad
        values = _adjoint_exact_pass(values[::-1], stage)
        values = _adjoint_exact_pass(values[::-1], stage)
        values = _odd_transpose(values, pad, length)
    return tuple(values)


def _up_bound(value):
    if value < 0:
        raise CertificationError("arithmetic_failure", "Negative error-bound expression")
    return _rounded(value, "up")


def _radius_summary(radii):
    """Bind the complete exact vector without embedding its coordinate list."""
    digest = sha256()
    header = ("ri60-radius-vector-v1\n" + str(len(radii)) + "\n").encode("ascii")
    digest.update(header)
    byte_count = len(header)
    for value in radii:
        if type(value) is not Fraction or value < 0:
            raise CertificationError("arithmetic_failure", "Invalid coordinate radius")
        numerator, denominator = _q(value)
        encoded = (numerator + "/" + denominator + "\n").encode("ascii")
        digest.update(encoded)
        byte_count += len(encoded)
    return {"count": len(radii), "nonzero_count": sum(value != 0 for value in radii),
            "maximum": _q(max(radii, default=ZERO)),
            "first": _q(radii[0]) if radii else None,
            "last": _q(radii[-1]) if radii else None,
            "encoding": "ri60-radius-vector-v1", "bytes": byte_count,
            "sha256": digest.hexdigest()}


def _adjoint_point_pass(values, radii, profiles):
    startup = ZERO
    startup_radius = ZERO
    trace = []
    input_summary = _radius_summary(radii)
    pass_input_summary = input_summary
    for section_index in range(len(profiles) - 1, -1, -1):
        profile = profiles[section_index]
        b0, _, _, _, a1, a2 = profile.sos
        lambda0 = lambda1 = ZERO
        result = [ZERO] * len(values)
        output_radii = [ZERO] * len(values)
        eL = eX = ZERO
        state_norm = maximum_state_norm = ZERO
        component0 = component1 = max_component0 = max_component1 = ZERO
        for k in range(len(values) - 1, -1, -1):
            output = b0 * values[k] + profile.J[0] * lambda0 + profile.J[1] * lambda1
            result[k], output_residual = _point(output)
            next0, state_residual = _point(values[k] - a1 * lambda0 - a2 * lambda1)
            # Output depends on the NEXT state: bound it before updating error.
            if a2 == 0:
                output_radii[k] = _up_bound(abs(b0) * radii[k]
                    + abs(profile.J[0]) * component0 + abs(profile.J[1]) * component1
                    + output_residual)
                component0, component1 = (_up_bound(abs(a1) * component0 + radii[k] + state_residual),
                                           component0)
                max_component0 = max(max_component0, component0)
                max_component1 = max(max_component1, component1)
            else:
                output_radii[k] = _up_bound(abs(b0) * radii[k]
                    + profile.jnorm * state_norm + output_residual)
                state_norm = _up_bound(profile.rho * state_norm
                    + profile.force * (radii[k] + state_residual))
                maximum_state_norm = max(maximum_state_norm, state_norm)
            eX, eL = max(eX, output_residual), max(eL, state_residual)
            lambda0, lambda1 = next0, lambda0
        scalar, eP = _point(profile.h[0] * lambda0 + profile.h[1] * lambda1)
        if a2 == 0:
            scalar_radius = _up_bound(abs(profile.h[0]) * component0
                + abs(profile.h[1]) * component1 + eP)
            state_summary = {"kind": "coordinate_components", "final": [_q(component0), _q(component1)],
                             "maximum": [_q(max_component0), _q(max_component1)]}
        else:
            scalar_radius = _up_bound(profile.hnorm * state_norm + eP)
            state_summary = {"kind": "P_inverse_norm", "final": _q(state_norm),
                             "maximum": _q(maximum_state_norm)}
        new_startup, eS = _point(startup + profile.preceding_gain * scalar)
        startup_radius = _up_bound(startup_radius + abs(profile.preceding_gain) * scalar_radius + eS)
        output_summary = _radius_summary(output_radii)
        trace.append({"section": section_index, "input_coordinate_radii": input_summary,
                      "state_residual_max": _q(eL), "output_residual_max": _q(eX),
                      "state_error": state_summary,
                      "startup_scalar_residual": _q(eP), "startup_scalar_radius": _q(scalar_radius),
                      "startup_accumulation_residual": _q(eS),
                      "output_coordinate_radii_before_direct_startup": output_summary,
                      "startup_radius_accumulated": _q(startup_radius)})
        startup, radii, values = new_startup, tuple(output_radii), tuple(result)
        input_summary = output_summary
    result, output_radii = list(values), list(radii)
    result[0], final_residual = _point(result[0] + startup)
    output_radii[0] = _up_bound(output_radii[0] + startup_radius + final_residual)
    return tuple(result), tuple(output_radii), {
        "input_coordinate_radii": pass_input_summary, "sections_reverse_order": trace,
        "startup_destination_coordinate": 0, "startup_final_add_residual": _q(final_residual),
        "pass_output_coordinate_radii": _radius_summary(output_radii)}


def _odd_transpose_point(values, radii, pad, length):
    exact_centers = _odd_transpose(values, pad, length)
    exact_radii = list(radii[pad:pad + length])
    for k in range(pad):
        exact_radii[0] += 2 * radii[k]
        exact_radii[pad - k] += radii[k]
        exact_radii[-1] += 2 * radii[pad + length + k]
        exact_radii[length - 2 - k] += radii[pad + length + k]
    results = [_point(x) for x in exact_centers]
    output_radii = tuple(_up_bound(bound + residual)
                         for bound, (_, residual) in zip(exact_radii, results))
    return tuple(point for point, _ in results), output_radii, {
        "input_coordinate_radii": _radius_summary(radii),
        "rounding_residual_max": _q(max((residual for _, residual in results), default=ZERO)),
        "output_coordinate_radii": _radius_summary(output_radii)}


def certified_adjoint(seed, prepared):
    """Return coordinate intervals for the exact operator, plus proof trace.

    The scalar radius summarizes the final vector; it is not propagated.
    Mathematical enclosure does not imply the separately frozen width gates
    pass.  No result is returned on failure and precision is never raised.
    """
    if type(prepared) is not Prepared:
        raise ValueError("Expected the result of prepare")
    values = _values(seed, prepared.padlens)
    length = len(values)
    state_updates = sum(2 * len(stage) * (length + 2 * pad)
                        for stage, pad in zip(prepared.stages, prepared.padlens))
    if state_updates > MAX_STATE_UPDATES:
        raise CertificationError("resource_state_updates", "State-update cap exceeded")
    rounded = [_point(value) for value in values]
    values = tuple(point for point, _ in rounded)
    radii = tuple(_up_bound(residual) for _, residual in rounded)
    initial_summary = _radius_summary(radii)
    traces = []
    for index in range(len(prepared.stages) - 1, -1, -1):
        pad, profiles = prepared.padlens[index], prepared.profiles[index]
        values = (ZERO,) * pad + values + (ZERO,) * pad
        radii = (ZERO,) * pad + radii + (ZERO,) * pad
        values, radii, first = _adjoint_point_pass(values[::-1], radii[::-1], profiles)
        values, radii, second = _adjoint_point_pass(values[::-1], radii[::-1], profiles)
        values, radii, extension = _odd_transpose_point(values, radii, pad, length)
        traces.append({"stage": index, "padding": pad, "pass_length": length + 2 * pad,
                       "first_adjoint_pass": first, "second_adjoint_pass": second,
                       "odd_extension_transpose": extension})
    radius = max(radii, default=ZERO)
    intervals = tuple((_bounded(x - r), _bounded(x + r)) for x, r in zip(values, radii))
    return {"status": "certified", "center": values, "radius": radius,
            "intervals": intervals,
            "proof": {"arithmetic": arithmetic_contract(), "length": length,
                      "state_updates": state_updates,
                      "initial_seed_coordinate_radii": initial_summary,
                      "section_certificates": [[profile.proof for profile in row]
                                               for row in prepared.profiles],
                      "stage_traces_reverse_order": traces,
                      "final_coordinate_radii": _radius_summary(radii), "final_radius": _q(radius),
                      "width_gate_applied": False,
                      "status_meaning": "rigorous_exact_operator_enclosure_only"}}
