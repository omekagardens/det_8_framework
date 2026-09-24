"""RI-57 exact finite operators and validated, selected adjoint sweeps.

No files, packages, coefficients or samples are loaded by this module.  Callers
supply exact Fraction SOS coefficients, pads and seeds.  This is an enclosure
of the exact rational RI-55 operator, not of floating-point filtering.

Arithmetic contract
-------------------
Point operations round to 256 significant binary digits, nearest/even.  Bounds
on small matrices round outwards at that same precision.  Local equation
residuals and final interval endpoints are exact Fractions.  Thus neither an
ambient floating/Decimal context nor unrecorded summation error enters a bound.
Rounded nonzero points/matrix endpoints must have binary exponent in
[-16384,16384].  Exact residuals/endpoints have separate integer-size caps;
proof integers are capped below Python's default decimal-string limit.
Dimensions and state-update counts are capped.  Exhaustion is unresolved.

For H=[[-a1,1],[-a2,0]], c=(1,0), J=(b1-a1*b0,b2-a2*b0),
h=(g-b0,b2-a2*g), the point adjoint copies lambda[1]=next_lambda[0]
exactly and rounds only lambda[0].  If the input radius is r, the largest
state/output/startup local residuals are eL/eX/eP, and
K_v >= sum(k>=0)|c H**k v|, its output radius is
    |b0|*r + K_J*(r+eL) + eX
and its startup scalar radius is K_h*(r+eL)+eP.  This follows by summing
the signed exact Green function of the first-coordinate state residual.
Every section's startup scalar is multiplied by its exact preceding DC-gain
product and accumulated at the ORIGINAL pass input's first coordinate.

For a2>0 and D=a2-a1*a1/4>0, P=[[a2,-a1/2],[-a1/2,1]] is positive
definite and H.T*P*H=a2*P exactly.  Cauchy-Schwarz bounds the Green sum by
sqrt((v.T*P*v)/D)/(1-sqrt(a2)); K_v is an outward upper enclosure of that
formula.  Square roots and the final division round upwards, so the numerator
is upper-bounded and 1-rho_upper is a proved positive lower denominator.
J and h are formed exactly before this norm,
preserving the notch cancellation.  For a2=0, the exact alternative is
K_v=|v0|+|(-a1)*v0+v1|/(1-|a1|).  Other stable denominator classes are
explicitly unsupported.  These are not naive interval recurrence bounds.

Both H and H.T must additionally pass the fixed first-contraction search at
K=2**j, j=0,...,20, with outward repeated squaring.  The P identity gives
finite remainder-power bounds through |(H**r)[i,j]| <=
sqrt((P**-1)[i,i]*P[j,j]) for all r>=0.  The a2=0 class has direct exact
remainder bounds.  The power certificates are necessary admission checks;
the sharper scalar bounds above are used for residual propagation.

There is no dense admitted matrix construction or actual-data-specific branch.
Exact small forward and adjoint helpers are separately capped, and the same
validated method is used for small and large certified adjoints.
"""

from dataclasses import dataclass
from fractions import Fraction
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
        "schema_version": "ri57-operator-v1",
        "precision_bits": PRECISION,
        "point_rounding": "nearest_binary_significand_ties_to_even",
        "interval_rounding": "directed_binary_significand",
        "endpoint_and_residual_arithmetic": "exact_stdlib_Fraction",
        "green_function": "exact_quadratic_identity_or_a2_zero_scalar",
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
    KJ: Fraction
    Kh: Fraction
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
        def scalar_bound(v):
            return _bounded(abs(v[0]) + abs(-a1 * v[0] + v[1]) / (1 - abs(a1)))
        kind = "a2_zero_exact_scalar"
        extra = {"remainder_H_infinity_upper": _q(max(ONE, 1 + abs(a1))),
                 "remainder_H_transpose_infinity_upper": _q(ONE)}
    elif a2 > 0 and determinant > 0:
        P = ((a2, -a1 / 2), (-a1 / 2, ONE))
        H = ((-a1, ONE), (-a2, ZERO))
        product = tuple(tuple(sum((H[k][i] * P[k][ell] * H[ell][j]
                                   for k in range(2) for ell in range(2)), ZERO)
                              for j in range(2)) for i in range(2))
        if product != tuple(tuple(a2 * x for x in row) for row in P):
            raise CertificationError("arithmetic_failure", "Exact quadratic identity failed")
        rho = _sqrt_up(a2)
        if rho >= 1:
            raise CertificationError("unresolved_quadratic", "Outward decay bound reaches one")
        def scalar_bound(v):
            quadratic = _bounded(a2 * v[0] * v[0] - a1 * v[0] * v[1] + v[1] * v[1])
            if quadratic < 0:
                raise CertificationError("arithmetic_failure", "Positive quadratic form failed")
            return _rounded(_sqrt_up(quadratic / determinant) / (1 - rho), "up")
        diagonal_p = (a2, ONE)
        diagonal_inverse = (1 / determinant, a2 / determinant)
        entry_bounds = tuple(tuple(_sqrt_up(diagonal_inverse[i] * diagonal_p[j])
                                   for j in range(2)) for i in range(2))
        remainder = max(sum(row, ZERO) for row in entry_bounds)
        remainder_transpose = max(sum((entry_bounds[j][i] for j in range(2)), ZERO)
                                  for i in range(2))
        kind = "exact_quadratic_identity"
        extra = {"P": [[_q(x) for x in row] for row in P],
                 "determinant": _q(determinant), "rho_upper": _q(rho),
                 "remainder_entry_bounds": [[_q(x) for x in row] for row in entry_bounds],
                 "remainder_H_infinity_upper": _q(remainder),
                 "remainder_H_transpose_infinity_upper": _q(remainder_transpose)}
    else:
        raise CertificationError("unresolved_denominator_class", "Stable denominator lacks the declared scalar certificate")
    KJ, Kh = scalar_bound(J), scalar_bound(h)
    powers = _power_certificates(a1, a2)
    proof = {"method": kind, "jury_exact": True, "powers": powers,
             "gain": _q(gain), "preceding_gain": _q(preceding_gain),
             "J": [_q(x) for x in J], "h": [_q(x) for x in h],
             "K_J_upper": _q(KJ), "K_h_upper": _q(Kh), **extra}
    return _Section(sos, gain, preceding_gain, J, h, KJ, Kh, proof)


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


def _adjoint_point_pass(values, radius, profiles):
    startup = ZERO
    startup_radius = ZERO
    trace = []
    for section_index in range(len(profiles) - 1, -1, -1):
        profile = profiles[section_index]
        b0, _, _, _, a1, a2 = profile.sos
        lambda0 = lambda1 = ZERO
        result = [ZERO] * len(values)
        eL = eX = ZERO
        for k in range(len(values) - 1, -1, -1):
            output = b0 * values[k] + profile.J[0] * lambda0 + profile.J[1] * lambda1
            result[k], residual = _point(output)
            eX = max(eX, residual)
            next0, residual = _point(values[k] - a1 * lambda0 - a2 * lambda1)
            eL = max(eL, residual)
            lambda0, lambda1 = next0, lambda0
        scalar, eP = _point(profile.h[0] * lambda0 + profile.h[1] * lambda1)
        scalar_radius = _bounded(profile.Kh * (radius + eL) + eP)
        new_startup, eS = _point(startup + profile.preceding_gain * scalar)
        startup_radius = _bounded(startup_radius + abs(profile.preceding_gain) * scalar_radius + eS)
        next_radius = _bounded(abs(b0) * radius + profile.KJ * (radius + eL) + eX)
        trace.append({"section": section_index, "input_radius": _q(radius),
                      "state_residual_max": _q(eL), "output_residual_max": _q(eX),
                      "startup_scalar_residual": _q(eP), "startup_accumulation_residual": _q(eS),
                      "output_radius": _q(next_radius), "startup_radius_accumulated": _q(startup_radius)})
        startup, radius, values = new_startup, next_radius, tuple(result)
    result = list(values)
    result[0], final_residual = _point(result[0] + startup)
    radius = _bounded(radius + startup_radius + final_residual)
    return tuple(result), radius, {"sections_reverse_order": trace,
                                  "startup_final_add_residual": _q(final_residual),
                                  "pass_output_radius": _q(radius)}


def _odd_transpose_point(values, radius, pad, length):
    exact_centers = _odd_transpose(values, pad, length)
    # Accumulate row l1 norms directly, including overlapping reflected indices.
    row_norms = [1] * length
    for k in range(pad):
        row_norms[0] += 2
        row_norms[pad - k] += 1
        row_norms[-1] += 2
        row_norms[length - 2 - k] += 1
    results = [_point(x) for x in exact_centers]
    output_radius = max((_bounded(row_norms[k] * radius + residual)
                         for k, (_, residual) in enumerate(results)), default=ZERO)
    return tuple(point for point, _ in results), output_radius, {
        "row_l1_max": max(row_norms),
        "rounding_residual_max": _q(max((residual for _, residual in results), default=ZERO)),
        "output_radius": _q(output_radius)}


def certified_adjoint(seed, prepared):
    """Return exact rational intervals, 256-bit centers and their proof trace.

    A uniform radius is deliberately conservative.  Mathematical enclosure does
    not imply the caller's separately frozen width/qualification gates pass.
    No result is returned on a failure, and no precision is adaptively raised.
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
    radius = max((residual for _, residual in rounded), default=ZERO)
    initial_radius = radius
    traces = []
    for index in range(len(prepared.stages) - 1, -1, -1):
        pad, profiles = prepared.padlens[index], prepared.profiles[index]
        values = (ZERO,) * pad + values + (ZERO,) * pad
        values, radius, first = _adjoint_point_pass(values[::-1], radius, profiles)
        values, radius, second = _adjoint_point_pass(values[::-1], radius, profiles)
        values, radius, extension = _odd_transpose_point(values, radius, pad, length)
        traces.append({"stage": index, "padding": pad, "pass_length": length + 2 * pad,
                       "first_adjoint_pass": first, "second_adjoint_pass": second,
                       "odd_extension_transpose": extension})
    intervals = tuple((_bounded(x - radius), _bounded(x + radius)) for x in values)
    return {"status": "certified", "center": values, "radius": radius,
            "intervals": intervals,
            "proof": {"arithmetic": arithmetic_contract(), "length": length,
                      "state_updates": state_updates,
                      "initial_seed_rounding_radius": _q(initial_radius),
                      "section_certificates": [[profile.proof for profile in row]
                                               for row in prepared.profiles],
                      "stage_traces_reverse_order": traces, "final_radius": _q(radius),
                      "width_gate_applied": False,
                      "status_meaning": "rigorous_exact_operator_enclosure_only"}}
