"""RI119 independent exact validator; source preparation, no execution authority.

This implementation derives every expected field from fixed selectors and
second moments of independent unit-variance latent coordinates. It never
imports the primary or enumerates its sign cubes. There is no import-time I/O.
"""

from fractions import Fraction
import json
import re


MAX_BODY_BYTES = 2 * 1024 * 1024
MAX_RATIONAL_BITS = 8192
MAX_DECIMAL_COMPONENT = 2467
MAX_RAW_LENGTH = 8
MAX_OUTPUT_DIMENSION = 2
MAX_WINDOWS = 3
MAX_LATENT_DIMENSION = 8

ROOT_KEYS = (
    "schema", "phase", "status", "method", "cases", "bounds", "groups",
    "limitations",
)
CASE_KEYS = (
    "id", "model", "selectors_M", "selectors_T", "output_map", "raw_mean",
    "raw_covariance", "window_marginal_covariances", "stacked_output_mean",
    "stacked_output_covariance", "cross_blocks", "mean_output_covariance",
    "centered_covariance_average", "mean_dispersion",
    "covariance_contribution", "expected_V", "direct_average_V", "expected_U",
    "mean_output_energy", "sign_count",
)
MODEL_KEYS = (
    "kind", "M", "T", "stride", "n", "starts", "raw_length",
    "latent_dimension", "output_dimension", "A", "raw_factor", "raw_mean",
    "scale",
)
DIMENSION_KEYS = (
    "M", "T", "stride", "n", "raw_length", "latent_dimension",
    "output_dimension",
)
CASE_IDS = (
    "Q02_white_two", "Q03_periodic_two", "Q05_white_three",
    "Q06_constant_mean", "Q07_quadratic_mean", "Q08_scale_minus_one",
    "Q08_scale_two", "Q09_oriented_matrix", "Q10_zero_map",
)
BOUND_IDS = (
    "Q12_calibrated_constant", "Q12_covariance_error",
    "Q12_calibration_error",
)
GROUPS = tuple("Q%02d" % i for i in range(1, 13))
METHOD = {
    "rational_encoding": "reduced_decimal_strings",
    "arithmetic": "exact_rational",
    "primary_route": "complete_sign_enumeration",
    "validator_route": "independent_moment_selector_factor_algebra",
    "inputs": "fixed_synthetic_only",
    "divisor": "n",
    "real_operator_evaluated": False,
    "empirical_inputs_evaluated": False,
    "physical_model_validated": False,
}
LIMITATIONS = (
    "Synthetic joint-window arithmetic only; no empirical data or actual coefficient capture.",
    "Shared sample and covariance refusals concern the declared fixed model, not every alternative model.",
    "Finite circulant marginals do not select a physical joint window law.",
    "Mean, calibration and model-error premises are explicit and not estimated here.",
    "No significance, physical calibration, protected validation or native forward claim; RET remains paused.",
)
_RATIONAL = re.compile(r"(?:0|-?[1-9][0-9]*)(?:/[1-9][0-9]*)?", re.ASCII)


class ValidationError(Exception):
    """Deliberate protocol refusal with a stable first-refusal code."""

    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def _fail(code, message):
    raise ValidationError(code, message)


def _bounded(value):
    if type(value) is not Fraction:
        value = Fraction(value)
    if (value.numerator.bit_length() > MAX_RATIONAL_BITS
            or value.denominator.bit_length() > MAX_RATIONAL_BITS):
        _fail("RESOURCE", "Reduced rational exceeds the bit bound")
    return value


def _read_rational(value):
    if type(value) is not str:
        _fail("EXACT", "Rational entries must be canonical strings")
    # Bound decimal components before regex, integer conversion, or gcd work.
    if len(value) > 2 * MAX_DECIMAL_COMPONENT + 2:
        _fail("RESOURCE", "Rational string exceeds the character bound")
    components = value.split("/")
    if any(len(part.lstrip("-")) > MAX_DECIMAL_COMPONENT
           for part in components):
        _fail("RESOURCE", "Decimal rational component exceeds the bound")
    if _RATIONAL.fullmatch(value) is None:
        _fail("EXACT", "Rational string is not in the decimal grammar")
    try:
        if len(components) == 1:
            numerator, denominator = int(components[0]), 1
        else:
            numerator, denominator = int(components[0]), int(components[1])
    except (ValueError, OverflowError):
        _fail("EXACT", "Rational integer component is invalid")
    if (numerator.bit_length() > MAX_RATIONAL_BITS
            or denominator.bit_length() > MAX_RATIONAL_BITS):
        _fail("RESOURCE", "Rational component exceeds the bit bound")
    result = _bounded(Fraction(numerator, denominator))
    if str(result) != value:
        _fail("EXACT", "Rational string is not reduced and canonical")
    return result


def canonical(result):
    try:
        body = (json.dumps(result, sort_keys=True, indent=2, ensure_ascii=True,
                           allow_nan=False) + "\n").encode("ascii")
    except (ValueError, TypeError, OverflowError, RecursionError):
        _fail("CANONICAL", "Result cannot be serialized canonically")
    if len(body) > MAX_BODY_BYTES:
        _fail("RESOURCE", "Canonical result exceeds the byte bound")
    return body


def _object_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            _fail("CANONICAL", "Duplicate JSON key")
        out[key] = value
    return out


def _nonfinite(_value):
    _fail("CANONICAL", "Nonfinite JSON number")


def parse_result(body):
    if type(body) is not bytes:
        _fail("CANONICAL", "Result body must be bytes")
    if len(body) > MAX_BODY_BYTES:
        _fail("RESOURCE", "Result body exceeds the byte bound")
    try:
        result = json.loads(body.decode("ascii"), object_pairs_hook=_object_pairs,
                            parse_constant=_nonfinite)
    except ValidationError:
        raise
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        _fail("CANONICAL", "Result body is not finite canonical JSON")
    if canonical(result) != body:
        _fail("CANONICAL", "Result bytes differ from canonical JSON")
    return result


def _same(left, right):
    """Entrywise equality that never conflates bool with an integer."""
    if type(left) is not type(right):
        return False
    if type(right) is dict:
        return (left.keys() == right.keys()
                and all(_same(left[k], right[k]) for k in right))
    if type(right) is list:
        return (len(left) == len(right)
                and all(_same(a, b) for a, b in zip(left, right)))
    return left == right


def _equal(given, expected, code, label):
    if not _same(given, expected):
        _fail(code, "Mismatch in " + label)


def _keys(given, keys, label):
    if type(given) is not dict or set(given) != set(keys):
        _fail("SCHEMA", "Wrong mapping or exact keys: " + label)


def _typed_shape(given, expected, label):
    """Validate all exact-number leaves and structural integer/list types.

    Structural value identities are checked at their designated later guards;
    fixed dimension values are checked explicitly by validate_result.
    """
    if type(expected) is dict:
        _keys(given, expected.keys(), label)
        for key in expected:
            _typed_shape(given[key], expected[key], label + "." + key)
    elif type(expected) is list:
        if type(given) is not list or len(given) != len(expected):
            _fail("DIMENSION", "Wrong list shape: " + label)
        for index, (actual, wanted) in enumerate(zip(given, expected)):
            _typed_shape(actual, wanted, label + "[%d]" % index)
    elif type(expected) is int:
        if type(given) is not int:
            _fail("DIMENSION", "Structural integer required: " + label)
    elif type(expected) is bool:
        if type(given) is not bool:
            _fail("DIMENSION", "Plain boolean required: " + label)
    elif type(expected) is str:
        if type(given) is not str:
            _fail("EXACT", "Plain string required: " + label)
        if _RATIONAL.fullmatch(expected) is not None:
            _read_rational(given)


def require_psd_2x2(matrix):
    """Exact named production guard; singular PSD matrices are accepted."""
    if (type(matrix) is not list or len(matrix) != 2
            or any(type(row) is not list or len(row) != 2 for row in matrix)):
        _fail("DIMENSION", "PSD guard requires a two by two matrix")
    a, b = (_read_rational(value) for value in matrix[0])
    d, c = (_read_rational(value) for value in matrix[1])
    if b != d or a < 0 or c < 0 or _bounded(_bounded(a * c) - _bounded(b * b)) < 0:
        _fail("PSD", "Covariance is not symmetric positive semidefinite")
    return None


# Independent matrix algebra. No producer oracle or sign-vector iteration.
def _zeros(rows, columns):
    return [[Fraction(0) for _ in range(columns)] for _ in range(rows)]


def _identity(size):
    return [[Fraction(int(i == j)) for j in range(size)] for i in range(size)]


def _transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def _multiply(left, right):
    if not left or not right or len(left[0]) != len(right):
        _fail("DIMENSION", "Internal matrix product dimensions disagree")
    columns = _transpose(right)
    answer = []
    for row in left:
        output = []
        for column in columns:
            value = Fraction(0)
            for a, b in zip(row, column):
                value = _bounded(value + _bounded(a * b))
            output.append(value)
        answer.append(output)
    return answer


def _scaled(matrix, scalar):
    return [[_bounded(value * scalar) for value in row] for row in matrix]


def _plus(left, right):
    return [[_bounded(a + b) for a, b in zip(arow, brow)]
            for arow, brow in zip(left, right)]


def _trace(matrix):
    value = Fraction(0)
    for index in range(len(matrix)):
        value = _bounded(value + matrix[index][index])
    return value


def _frobenius_squared(matrix):
    value = Fraction(0)
    for row in matrix:
        for entry in row:
            value = _bounded(value + _bounded(entry * entry))
    return value


def _column(vector):
    return [[value] for value in vector]


def _vector(matrix):
    return [row[0] for row in matrix]


def _text(value):
    if type(value) is list:
        return [_text(item) for item in value]
    return str(_bounded(value))


def _selection(length, start, width):
    # An explicit selector, not a separately sampled window.
    return [[int(column == start + row) for column in range(length)]
            for row in range(width)]


def _fraction_matrix(matrix):
    return [[Fraction(value) for value in row] for row in matrix]


def _centering(windows, outputs):
    return [[Fraction(int(a == b) - Fraction(1, windows)) * int(i == j)
             for b in range(windows) for j in range(outputs)]
            for a in range(windows) for i in range(outputs)]


def _fixed_case(identifier):
    """Literal tiny input definitions are the sole scientific inputs here."""
    windows = 3 if identifier in ("Q05_white_three", "Q07_quadratic_mean") else 2
    starts = [2 * index for index in range(windows)]
    length = starts[-1] + 4
    outputs = 2 if identifier == "Q09_oriented_matrix" else 1
    latent = 4 if identifier == "Q03_periodic_two" else length
    if (length > MAX_RAW_LENGTH or windows > MAX_WINDOWS
            or outputs > MAX_OUTPUT_DIMENSION or latent > MAX_LATENT_DIMENSION):
        _fail("RESOURCE", "Fixed scientific dimensions exceed bounds")
    if identifier == "Q09_oriented_matrix":
        operator = _fraction_matrix([[1, 0, -1], [0, 1, -1]])
    elif identifier == "Q10_zero_map":
        operator = _fraction_matrix([[0, 0, 0]])
    else:
        operator = _fraction_matrix([[1, 0, -1]])
    if identifier == "Q03_periodic_two":
        latent_index = [0, 1, 2, 3, 0, 1]
        factor = [[Fraction(int(j == latent_index[i])) for j in range(latent)]
                  for i in range(length)]
    else:
        factor = _identity(length)
    mean = [Fraction(0) for _ in range(length)]
    if identifier == "Q06_constant_mean":
        mean = [Fraction(3) for _ in range(length)]
    elif identifier == "Q07_quadratic_mean":
        mean = [Fraction(j * j) for j in range(length)]
    scale = Fraction(-1 if identifier == "Q08_scale_minus_one"
                     else 2 if identifier == "Q08_scale_two" else 1)
    model = {
        "kind": ("shared_periodic" if identifier == "Q03_periodic_two"
                 else "shared_raw_white"),
        "M": 4, "T": 3, "stride": 2, "n": windows, "starts": starts,
        "raw_length": length, "latent_dimension": latent,
        "output_dimension": outputs, "A": _text(operator),
        "raw_factor": _text(factor), "raw_mean": _text(mean),
        "scale": _text(scale),
    }
    return model, operator, factor, mean, scale


def _case_expectation(identifier):
    model, operator, factor, mean, scale = _fixed_case(identifier)
    n, q, length = model["n"], model["output_dimension"], model["raw_length"]
    selectors_m = [_selection(length, start, 4) for start in model["starts"]]
    selectors_t = [_selection(length, start, 3) for start in model["starts"]]
    maps = [_multiply(operator, _fraction_matrix(selector)) for selector in selectors_t]
    stacked_map = [row for block in maps for row in block]
    scaled_factor = _scaled(factor, scale)
    raw_mean = [_bounded(scale * entry) for entry in mean]
    raw_covariance = _multiply(scaled_factor, _transpose(scaled_factor))
    output_factor = _multiply(stacked_map, scaled_factor)
    output_mean = _multiply(stacked_map, _column(raw_mean))
    covariance = _multiply(output_factor, _transpose(output_factor))
    marginal_covariances = []
    for selector in selectors_m:
        projected_factor = _multiply(_fraction_matrix(selector), scaled_factor)
        marginal_covariances.append(_multiply(projected_factor, _transpose(projected_factor)))
    blocks = [[[[covariance[a * q + i][b * q + j] for j in range(q)]
                for i in range(q)] for b in range(n)] for a in range(n)]
    mean_map = [[Fraction(int(i == j), n) for _ in range(n) for j in range(q)]
                for i in range(q)]
    mean_factor = _multiply(mean_map, output_factor)
    mean_covariance = _multiply(mean_factor, _transpose(mean_factor))
    finite_mean = _multiply(mean_map, output_mean)
    center = _centering(n, q)
    centered_factor = _multiply(center, output_factor)
    centered_stack = _multiply(centered_factor, _transpose(centered_factor))
    centered_average = _zeros(q, q)
    for a in range(n):
        for i in range(q):
            for j in range(q):
                centered_average[i][j] = _bounded(
                    centered_average[i][j] + centered_stack[a * q + i][a * q + j] / n)
    centered_mean = _multiply(center, output_mean)
    mean_dispersion = _bounded(_frobenius_squared(centered_mean) / n)
    covariance_contribution = _bounded(_frobenius_squared(centered_factor) / n)
    expected_v = _bounded(covariance_contribution + mean_dispersion)
    expected_u = _bounded((_frobenius_squared(output_factor)
                          + _frobenius_squared(output_mean)) / n)
    mean_energy = _bounded(_frobenius_squared(mean_factor)
                           + _frobenius_squared(finite_mean))
    # An algebraically distinct second-moment identity replaces sign enumeration.
    direct_average = _bounded(expected_u - mean_energy)
    if direct_average != expected_v or _trace(centered_average) != covariance_contribution:
        _fail("ENERGY", "Independent factor/centering moment identities disagree")
    return {
        "id": identifier, "model": model,
        "selectors_M": selectors_m, "selectors_T": selectors_t,
        "output_map": _text(stacked_map), "raw_mean": _text(raw_mean),
        "raw_covariance": _text(raw_covariance),
        "window_marginal_covariances": _text(marginal_covariances),
        "stacked_output_mean": _text(_vector(output_mean)),
        "stacked_output_covariance": _text(covariance),
        "cross_blocks": _text(blocks),
        "mean_output_covariance": _text(mean_covariance),
        "centered_covariance_average": _text(centered_average),
        "mean_dispersion": _text(mean_dispersion),
        "covariance_contribution": _text(covariance_contribution),
        "expected_V": _text(expected_v), "direct_average_V": _text(direct_average),
        "expected_U": _text(expected_u), "mean_output_energy": _text(mean_energy),
        "sign_count": 1 << model["latent_dimension"],
    }


def _bound_expectations():
    operator = _fraction_matrix([[1, 0, -1]])
    calibration = _fraction_matrix([[1, 0, 0], [0, 1, 0], [0, 0, 2]])
    constant = _fraction_matrix([[1], [1], [1]])
    output = _multiply(_multiply(operator, calibration), constant)
    first = {
        "id": "Q12_calibrated_constant", "output_dimension": 1,
        "A": _text(operator), "C_cal": _text(calibration),
        "input": _text(_vector(constant)), "output": _text(_vector(output)),
        "constant_annihilation_claim": False,
    }
    d = _fraction_matrix([[1], [-1]])
    pi = _centering(2, 1)
    centered = _multiply(pi, d)
    model_cov = _fraction_matrix([[1]])
    true_cov = _fraction_matrix([[2]])
    eta = Fraction(1)
    model_covariance = _multiply(_multiply(centered, model_cov), _transpose(centered))
    true_covariance = _multiply(_multiply(centered, true_cov), _transpose(centered))
    model_contribution = _bounded(_trace(model_covariance) / 2)
    true_contribution = _bounded(_trace(true_covariance) / 2)
    second = {
        "id": "Q12_covariance_error", "n": 2, "output_dimension": 1,
        "D": _text(d), "Pi": _text(pi), "Sigma_model": _text(model_cov),
        "Sigma_true": _text(true_cov), "eta": _text(eta),
        "model_contribution": _text(model_contribution),
        "true_contribution": _text(true_contribution),
        "absolute_difference": _text(abs(true_contribution - model_contribution)),
        "bound": _text(_bounded(eta * _frobenius_squared(centered) / 2)),
    }
    c0 = _fraction_matrix([[1]])
    delta = _fraction_matrix([[1]])
    factor = _fraction_matrix([[1]])
    model_factor = _multiply(_multiply(centered, c0), factor)
    perturbation_factor = _multiply(_multiply(centered, delta), factor)
    true_factor = _plus(model_factor, perturbation_factor)
    model_contribution = _bounded(_frobenius_squared(model_factor) / 2)
    true_contribution = _bounded(_frobenius_squared(true_factor) / 2)
    # Both fixed factors are the very same vector. Their Frobenius norm product
    # is its squared norm, exactly; no floating square root is involved.
    if model_factor != perturbation_factor:
        _fail("BOUND", "Fixed calibration toy factors unexpectedly differ")
    norm_product = _frobenius_squared(model_factor)
    bound = _bounded((2 * norm_product + _frobenius_squared(perturbation_factor)) / 2)
    third = {
        "id": "Q12_calibration_error", "n": 2, "output_dimension": 1,
        "D": _text(d), "Pi": _text(pi), "C0": _text(c0),
        "DeltaC": _text(delta), "F": _text(factor),
        "model_contribution": _text(model_contribution),
        "true_contribution": _text(true_contribution),
        "absolute_difference": _text(abs(true_contribution - model_contribution)),
        "bound": _text(bound),
    }
    return [first, second, third]


def _inventory(given):
    _equal(given["groups"], list(GROUPS), "INVENTORY", "group order")
    for label, identifiers in (("cases", CASE_IDS), ("bounds", BOUND_IDS)):
        records = given[label]
        if type(records) is not list or len(records) != len(identifiers):
            _fail("INVENTORY", "Wrong " + label + " inventory")
        for record, identifier in zip(records, identifiers):
            if (type(record) is not dict or type(record.get("id")) is not str
                    or record.get("id") != identifier):
                _fail("INVENTORY", "Wrong " + label + " order or identifier")


def validate_result(given):
    """Validate every saved field against independently reconstructed moments."""
    _keys(given, ROOT_KEYS, "result")
    _equal(given["schema"], "ri119-joint-window-synthetic-v1", "SCHEMA", "schema")
    _equal(given["phase"], "fabricated_joint_window_qualification", "PHASE", "phase")
    _equal(given["status"], "all_declared_checks_passed", "RESULT", "status")
    _equal(given["method"], METHOD, "SCOPE", "method")
    _inventory(given)
    _equal(given["limitations"], list(LIMITATIONS), "SCOPE", "limitations")

    # Build exact expectations only from this module's fixed literal definitions.
    expected_cases = [_case_expectation(identifier) for identifier in CASE_IDS]
    expected_bounds = _bound_expectations()
    for actual, expected in zip(given["cases"], expected_cases):
        _keys(actual, CASE_KEYS, expected["id"])
        _keys(actual["model"], MODEL_KEYS, expected["id"] + ".model")
        _typed_shape(actual, expected, expected["id"])
    for actual, expected in zip(given["bounds"], expected_bounds):
        _typed_shape(actual, expected, expected["id"])

    covariance_fields = (
        "raw_covariance", "window_marginal_covariances",
        "stacked_output_covariance", "cross_blocks", "mean_output_covariance",
        "centered_covariance_average",
    )
    energy_fields = (
        "covariance_contribution", "expected_V", "direct_average_V",
        "expected_U", "mean_output_energy",
    )
    for actual, expected in zip(given["cases"], expected_cases):
        identifier = expected["id"]
        for key in DIMENSION_KEYS:
            if actual["model"][key] != expected["model"][key]:
                _fail("DIMENSION", "Wrong fixed model dimension " + key)
        if identifier in ("Q02_white_two", "Q03_periodic_two"):
            require_psd_2x2(actual["stacked_output_covariance"])
        _equal(actual["model"], expected["model"], "MODEL", identifier + ".model")
        _equal(actual["selectors_M"], expected["selectors_M"], "SHARED_INDEX", identifier)
        _equal(actual["selectors_T"], expected["selectors_T"], "CROP", identifier)
        _equal(actual["output_map"], expected["output_map"], "OPERATOR", identifier)
        _equal(actual["raw_mean"], expected["raw_mean"], "MEAN_TERM", identifier)
        for key in covariance_fields:
            _equal(actual[key], expected[key], "COVARIANCE_MODEL", identifier + "." + key)
        for key in ("stacked_output_mean", "mean_dispersion"):
            _equal(actual[key], expected[key], "MEAN_TERM", identifier + "." + key)
        _equal(actual["sign_count"], expected["sign_count"], "ENUMERATION", identifier)
        for key in energy_fields:
            _equal(actual[key], expected[key], "ENERGY", identifier + "." + key)
    for actual, expected in zip(given["bounds"], expected_bounds):
        for key in ("n", "output_dimension"):
            if key in expected and actual[key] != expected[key]:
                _fail("DIMENSION", "Wrong fixed bound dimension " + key)
        if actual["id"] == "Q12_calibrated_constant":
            if actual["constant_annihilation_claim"] is not False:
                _fail("CALIBRATION", "Calibrated constants are not universally annihilated")
        if "eta" in actual and _read_rational(actual["eta"]) < 0:
            _fail("BOUND", "Covariance error eta must be nonnegative")
        _equal(actual, expected, "BOUND", expected["id"])
    return {"status": "all_fields_independently_match", "cases": 9,
            "bounds": 3, "groups": 12}
