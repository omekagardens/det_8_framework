"""RI87 independent, deterministic tiny-rational qualification.

Source preparation only until a separately reviewed execution freeze admits
this module.  The oracle below uses an explicit four-point cosine table and
dense Fraction products.  It does not import a numerical package, open a
predecessor result, reconstruct a filter, or call the primary mapping routine
to obtain its expected answers.
"""

from copy import deepcopy
from fractions import Fraction
import hashlib
import json
import struct


class QualificationError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def _need(condition, message):
    if not condition:
        raise QualificationError("QUALIFICATION", message)


def _same(actual, expected, label):
    _need(type(actual) is type(expected), label + ": type differs")
    if isinstance(expected, dict):
        _need(set(actual) == set(expected), label + ": keys differ")
        for key in expected:
            _same(actual[key], expected[key], label + "." + str(key))
    elif isinstance(expected, (list, tuple)):
        _need(len(actual) == len(expected), label + ": length differs")
        for index, (a, b) in enumerate(zip(actual, expected)):
            _same(a, b, label + "[" + str(index) + "]")
    else:
        _need(actual == expected, label + ": value differs")


def _fraction_matrix(rows):
    return tuple(tuple(Fraction(value) for value in row) for row in rows)


def _transpose(matrix):
    return tuple(tuple(row[j] for row in matrix) for j in range(len(matrix[0])))


def _multiply(left, right):
    _need(bool(left) and bool(right), "empty oracle matrix")
    _need(all(len(row) == len(right) for row in left), "oracle product shape")
    _need(all(len(row) == len(right[0]) for row in right), "ragged oracle matrix")
    return tuple(tuple(sum((row[k] * right[k][j] for k in range(len(right))),
                           Fraction(0))
                       for j in range(len(right[0]))) for row in left)


def _scale(matrix, value):
    return tuple(tuple(value * x for x in row) for row in matrix)


def _add(left, right):
    _need(len(left) == len(right)
          and all(len(a) == len(b) for a, b in zip(left, right)),
          "oracle sum shape")
    return tuple(tuple(a + b for a, b in zip(ar, br))
                 for ar, br in zip(left, right))


def _subtract(left, right):
    return _add(left, _scale(right, Fraction(-1)))


def _gram(matrix):
    return _multiply(matrix, _transpose(matrix))


def _sandwich(left, covariance, right=None):
    if right is None:
        right = left
    return _multiply(_multiply(left, covariance), _transpose(right))


def _circulant4(psd, fs=Fraction(4)):
    """Direct lag formula; no call to the consumer or eigenvalue mapper."""
    _need(len(psd) == 3, "four-point oracle needs three one-sided bins")
    p0, p1, pn = map(Fraction, psd)
    cosine = (1, 0, -1, 0)
    return tuple(tuple(fs / 4 * (p0 + pn * (-1 if (a - b) % 2 else 1)
                                + p1 * cosine[(a - b) % 4])
                       for b in range(4)) for a in range(4))


def _rank_psd_small(matrix):
    """Exact rank/PSD oracle only for symmetric one- or two-row fixtures."""
    _need(len(matrix) in (1, 2) and all(len(r) == len(matrix) for r in matrix),
          "small PSD oracle dimension")
    _same(matrix, _transpose(matrix), "small PSD symmetry")
    if len(matrix) == 1:
        _need(matrix[0][0] >= 0, "negative scalar covariance")
        return int(matrix[0][0] > 0)
    a, b, d = matrix[0][0], matrix[0][1], matrix[1][1]
    determinant = a * d - b * b
    _need(a >= 0 and d >= 0 and determinant >= 0, "negative PSD principal minor")
    return 2 if determinant > 0 else (1 if a > 0 or d > 0 else 0)


def _seed_matrices():
    p = _fraction_matrix(((0, Fraction(7, 4), Fraction(1, 2), 0),
                          (0, Fraction(3, 4), Fraction(3, 2), 0)))
    q = _fraction_matrix(((Fraction(1, 2), Fraction(5, 4), Fraction(1, 2), 0),
                          (0, Fraction(1, 2), Fraction(5, 4), Fraction(1, 2))))
    a = _fraction_matrix(((Fraction(1, 2), Fraction(-1, 2), 0, 0),
                          (0, Fraction(-1, 4), Fraction(-1, 4), Fraction(1, 2))))
    g = _fraction_matrix(((Fraction(1, 2), Fraction(1, 8)),
                          (Fraction(1, 8), Fraction(3, 8))))
    _same(_subtract(q, p), a, "held tiny Q-P")
    _same(_gram(a), g, "held tiny Gram")
    _need(all(sum(row, Fraction(0)) == 0 for row in a), "held tiny DC annihilation")
    return p, q, a, g


def _array_record(values):
    """Fabricated binary64 metadata; does not read any observed values."""
    values = tuple(float(value) for value in values)
    body = b"".join(struct.pack("<d", value) for value in values)
    return {"dtype": "<f8", "shape": [len(values)],
            "values_hex": [value.hex() for value in values],
            "sha256": hashlib.sha256(body).hexdigest()}


def _encode(value):
    if isinstance(value, Fraction):
        return [format(value.numerator, "x"), format(value.denominator, "x")]
    if isinstance(value, dict):
        return {key: _encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    return value


def _reference_case(name, psd, operator, gram, rho, eigenvalues, ell, upper,
                    expected_covariance):
    """Independently construct a tiny covariance and its exact PSD bounds."""
    psd = tuple(map(Fraction, psd))
    eigenvalues = tuple(map(Fraction, eigenvalues))
    rho, ell, upper = map(Fraction, (rho, ell, upper))
    covariance = _circulant4(psd)
    output = _sandwich(operator, covariance)
    _same(output, expected_covariance, name + ": independently stated output")
    _same(_gram(operator), gram, name + ": direct coefficient Gram")
    lower_matrix = _scale(gram, ell * (1 - rho))
    upper_matrix = _scale(gram, upper * (1 + rho))
    lower_difference = _subtract(output, lower_matrix)
    upper_difference = _subtract(upper_matrix, output)
    lower_rank = _rank_psd_small(lower_difference)
    upper_rank = _rank_psd_small(upper_difference)
    _same(covariance[0][0], sum(psd, Fraction(0)), name + ": exact zero lag")
    _same(covariance[0][0], sum(eigenvalues, Fraction(0)) / 4,
          name + ": spectral trace")
    return {"name": name, "psd": psd, "fs": Fraction(4), "G": gram,
            "rho": rho, "eigenvalues": eigenvalues, "ell": ell, "u": upper,
            "K": covariance, "Omega": output, "q_proxy": covariance[0][0],
            "Lower": lower_matrix, "Upper": upper_matrix,
            "lower_difference": lower_difference, "upper_difference": upper_difference,
            "difference_ranks": (lower_rank, upper_rank),
            "direct_output_rank": _rank_psd_small(output)}


def _tiny_oracle_families():
    """All seven RI86 families; expected answers do not use consumer code."""
    p, q, a, g = _seed_matrices()
    zero2 = _fraction_matrix(((0, 0), (0, 0)))
    colored_output = _fraction_matrix(((Fraction(5, 4), Fraction(1, 8)),
                                       (Fraction(1, 8), Fraction(13, 16))))
    colored_psd = (Fraction(7, 4), Fraction(1), Fraction(3, 4))
    white = []
    for label, variance in (("unit", Fraction(1)), ("tiny", Fraction(1, 2**140))):
        white.append(_reference_case("white_" + label,
                     (variance / 4, variance / 2, variance / 4), a, g, 0,
                     (variance,) * 4, variance, variance, _scale(g, variance)))
        _same(white[-1]["K"], tuple(tuple(variance if i == j else Fraction(0) for j in range(4))
                                   for i in range(4)), "white full covariance " + label)
    colored = _reference_case("colored", colored_psd, a, g, 0,
                              (7, 2, 3, 2), 2, 3, colored_output)
    _same(colored["K"][0], (Fraction(7, 2), Fraction(1), Fraction(3, 2), Fraction(1)),
          "colored full first covariance row")
    _same(colored["lower_difference"],
          _scale(_fraction_matrix(((4, -2), (-2, 1))), Fraction(1, 16)),
          "colored lower PSD residual")
    _same(colored["upper_difference"],
          _scale(_fraction_matrix(((4, 4), (4, 5))), Fraction(1, 16)),
          "colored upper PSD residual")
    _same(colored["upper_difference"][0][0] * colored["upper_difference"][1][1]
          - colored["upper_difference"][0][1] ** 2,
          Fraction(1, 64), "colored upper residual determinant")
    k = colored["K"]
    qq, pp = _sandwich(q, k), _sandwich(p, k)
    qp, pq = _sandwich(q, k, p), _sandwich(p, k, q)
    _same(qp[0][1], Fraction(309, 32), "oriented QKP entry01")
    _same(qp[1][0], Fraction(37, 4), "oriented QKP entry10")
    _same(pq, _transpose(qp), "opposite covariance orientation")
    _same(_subtract(_subtract(_add(qq, pp), qp), pq), colored_output,
          "complete shared-input covariance expansion")
    colored["shared_terms"] = {"QQ": qq, "PP": pp, "QP": qp, "PQ": pq}
    dc = []
    for value in (Fraction(0), Fraction(11)):
        dc.append(_reference_case("replace_DC_" + str(value),
                  (value / 4, Fraction(1), Fraction(3, 4)), a, g, 0,
                  (value, 2, 3, 2), 2, 3, colored_output))
    dc.append(_reference_case("DC_only", (1, 0, 0), a, g, 0,
                              (4, 0, 0, 0), 0, 0, zero2))
    dc.append(_reference_case("all_zero", (0, 0, 0), a, g, 0,
                              (0, 0, 0, 0), 0, 0, zero2))
    _same(dc[-2]["K"], _fraction_matrix(((1, 1, 1, 1),) * 4), "DC-only rank-one outer product")
    dc[-2]["input_rank_evidence"] = {"rank": 1, "outer_product_vector": (Fraction(1),) * 4}
    _same(dc[-1]["K"], _fraction_matrix(((0, 0, 0, 0),) * 4), "all-zero full covariance")
    identity_path = _fraction_matrix(((0, 1, 0, 0), (0, 0, 1, 0)))
    identical_marginal = _sandwich(identity_path, k)
    _need(any(value != 0 for row in identical_marginal for value in row),
          "identity cancellation needs nonzero marginal covariance")
    _same(_sandwich(_subtract(identity_path, identity_path), k), zero2,
          "identity-filter shared-noise cancellation")
    nyquist = _reference_case("Nyquist_only", (0, 0, 1), a, g, 0,
                (0, 0, 4, 0), 0, 4,
                _scale(_fraction_matrix(((4, -2), (-2, 1))), Fraction(1, 4)))
    interior = _reference_case("interior_only", (0, 1, 0), a, g, 0,
                (0, 2, 0, 2), 0, 2,
                _scale(_fraction_matrix(((4, 4), (4, 5))), Fraction(1, 8)))
    _same(nyquist["direct_output_rank"], 1, "Nyquist rank")
    _same(interior["direct_output_rank"], 2, "interior rank despite zero lower bound")
    _same(_multiply(nyquist["Omega"], ((Fraction(1),), (Fraction(2),))),
          ((Fraction(0),), (Fraction(0),)), "Nyquist perpendicular null vector")
    _need(nyquist["Omega"][0][0] > 0, "Nyquist nonzero rank-one support")
    crop_operator = _fraction_matrix(((1, -1, 0, 0),))
    crop = _reference_case("crop_congruence", colored_psd, crop_operator,
                           _fraction_matrix(((2,),)), 0, (7, 2, 3, 2), 2, 3,
                           _fraction_matrix(((5,),)))
    crop_matrix = tuple(tuple(k[i][j] for j in range(3)) for i in range(3))
    _same(_sandwich(_fraction_matrix(((1, -1, 0),)), crop_matrix),
          crop["Omega"], "three-coordinate covariance congruence")
    crop["selected_covariance"] = crop_matrix
    weak = _reference_case("weaker_valid_rho", colored_psd, a, g, Fraction(1, 4),
                           (7, 2, 3, 2), 2, 3, colored_output)
    _same(weak["Lower"], _scale(g, Fraction(3, 2)), "weaker rho lower")
    _same(weak["Upper"], _scale(g, Fraction(15, 4)), "weaker rho upper")
    scaled = _reference_case("scale_four", tuple(4 * value for value in colored_psd),
                a, g, 0, (28, 8, 12, 8), 8, 12, _scale(colored_output, Fraction(4)))
    for key in ("K", "Omega", "Lower", "Upper"):
        _same(scaled[key], _scale(colored[key], Fraction(4)), "homogeneity " + key)
    for key in ("q_proxy", "ell", "u"):
        _same(scaled[key], 4 * colored[key], "homogeneity " + key)
    return [
        {"family": "white_normalization", "cases": white},
        {"family": "colored_shared_input", "cases": [colored]},
        {"family": "DC_invariance_and_cancellation", "cases": dc,
         "identity_filter": {"marginal_covariance": identical_marginal,
                             "shared_difference_covariance": zero2}},
        {"family": "Nyquist_and_interior_support", "cases": [nyquist, interior],
         "Nyquist_support_generator": (Fraction(2), Fraction(-1)),
         "Nyquist_null_vector": (Fraction(1), Fraction(2))},
        {"family": "crop_congruence", "cases": [crop]},
        {"family": "positive_nonzero_inherited_rho", "cases": [weak]},
        {"family": "homogeneity", "cases": [scaled]},
    ]


def _expected_scenario(case):
    """Complete primary API expectation from independently stated tiny modes."""
    eigenvalues = case["eigenvalues"]
    # For M=4 the two one-sided non-DC modes are interior 1 and Nyquist 2.
    non_dc = (eigenvalues[1], eigenvalues[2])
    interior_positive = int(eigenvalues[1] > 0)
    non_dc_rank = 2 * interior_positive + int(eigenvalues[2] > 0)
    dimension = len(case["G"])
    rank_upper = min(dimension, non_dc_rank)
    ell, upper = case["ell"], case["u"]
    if ell > 0:
        status = "positive_definite_rank" + str(dimension)
    elif upper == 0:
        status = "zero_rank0"
    else:
        status = "unresolved_by_envelope"
    return {"lambda_dc": eigenvalues[0], "lambda_nyquist": eigenvalues[2],
            "non_dc_eigenvalues": non_dc, "q_proxy": case["q_proxy"],
            "ell": ell, "u": upper,
            "minimum_indices": tuple(i + 1 for i, x in enumerate(non_dc) if x == ell),
            "maximum_indices": tuple(i + 1 for i, x in enumerate(non_dc) if x == upper),
            "zero_interior_count": 1 - interior_positive,
            "positive_interior_count": interior_positive,
            "spectral_rank": non_dc_rank + int(eigenvalues[0] > 0),
            "non_dc_rank": non_dc_rank, "rank_upper": rank_upper,
            "rank_status": status, "singularity_proved": rank_upper < dimension,
            "lower": case["Lower"], "upper": case["Upper"],
            "diagonal": tuple((case["Lower"][i][i], case["Upper"][i][i])
                              for i in range(dimension)),
            "trace": (sum((case["Lower"][i][i] for i in range(dimension)), Fraction(0)),
                      sum((case["Upper"][i][i] for i in range(dimension)), Fraction(0)))}


def _refusal(name, operation, exception_type, expected_code):
    try:
        operation()
    except exception_type as error:
        _need(error.code == expected_code,
              name + ": wrong refusal code " + str(error.code))
        return {"id": name, "passed": True, "exception_type": type(error).__name__,
                "expected_code": expected_code, "code": error.code, "message": str(error)}
    except Exception as error:
        raise QualificationError("WRONG_EXCEPTION", name + ": " + type(error).__name__
                                 + ": " + str(error)) from error
    raise QualificationError("MISSING_REFUSAL", name + ": operation succeeded")


def _mutated(source, change):
    value = deepcopy(source)
    change(value)
    return value


def _certificate_projection(dimension=8):
    """Deliberately fabricated identity Gram, not an RI73 integration result."""
    identity = tuple(tuple(Fraction(i == j) for j in range(dimension))
                     for i in range(dimension))
    zero = tuple(tuple(Fraction(0) for _ in range(dimension)) for _ in range(dimension))
    return _encode({"source_gate": "integration:gram",
                    "source_model": "known_synthetic_unit_white", "G": identity,
                    "H": zero, "V": identity,
                    "ldl": {"lower": identity, "pivots": (Fraction(1),) * dimension,
                            "reconstruction": identity},
                    "delta": Fraction(0), "gamma": Fraction(1), "rho": Fraction(0),
                    "checks": ["G_symmetry", "H_symmetry_nonnegative", "positive_LDL",
                               "LDL_reconstruction", "two_sided_inverse", "delta_identity",
                               "gamma_identity", "rho_identity", "rho_mathematical", "rho_accuracy"]})


def _decoder_controls(consumer):
    baseline = _array_record((Fraction(7, 4), 1, Fraction(3, 4)))
    _same(consumer.decode_psd(baseline, bins=3),
          (Fraction(7, 4), Fraction(1), Fraction(3, 4)), "fabricated PSD decoding")
    signed_zero = _array_record((-0.0, 0.0, 0.0))
    ordinary_zero = _array_record((0.0, 0.0, 0.0))
    _need(signed_zero["sha256"] != ordinary_zero["sha256"], "signed-zero byte custody")
    _same(consumer.decode_psd(signed_zero, bins=3), (Fraction(0),) * 3,
          "signed-zero exact interpretation")
    tests = [
        ("psd_wrong_length", _mutated(baseline, lambda x: x.update(shape=[2])), "BINS"),
        ("psd_boolean_dimension", _mutated(baseline, lambda x: x.update(shape=[True])), "BINS"),
        ("psd_wrong_dtype", _mutated(baseline, lambda x: x.update(dtype=">f8")), "DTYPE"),
        ("psd_noncanonical_hex", _mutated(baseline, lambda x: x["values_hex"].__setitem__(0, "+0x1.c000000000000p+0")), "HEX"),
        ("psd_nonfinite", _mutated(baseline, lambda x: x["values_hex"].__setitem__(0, "nan")), "NONFINITE"),
        ("psd_negative", _array_record((-1, 1, 1)), "NEGATIVE_PSD"),
        ("psd_wrong_byte_hash", _mutated(baseline, lambda x: x.update(sha256="0" * 64)), "IDENTITY"),
    ]
    refusals = [_refusal(name, lambda value=value: consumer.decode_psd(value, bins=3),
                         consumer.ProxyError, code) for name, value, code in tests]
    return {"positive_record": baseline, "signed_zero_record": signed_zero,
            "positive_zero_record": ordinary_zero, "refusals": refusals}


def _certificate_controls(consumer):
    baseline = _certificate_projection()
    decoded = consumer.validate_certificate(baseline, dimension=8, application=True)
    _same(_encode(decoded), baseline, "complete fabricated identity certificate")
    fixtures = [
        ("certificate_unknown_field", lambda x: x.update(extra=0), "CERT_SCHEMA"),
        ("asymmetric_Gram", lambda x: x["G"][0].__setitem__(1, ["1", "1"]), "GRAM_SYMMETRY"),
        ("asymmetric_error", lambda x: x["H"][0].__setitem__(1, ["1", "1"]), "ERROR_SYMMETRY"),
        ("negative_error", lambda x: x["H"][0].__setitem__(0, ["-1", "1"]), "ERROR_NEGATIVE"),
        ("nonpositive_pivot", lambda x: x["ldl"]["pivots"].__setitem__(0, ["0", "1"]), "LDL_PIVOT"),
        ("wrong_LDL_reconstruction", lambda x: x["ldl"]["lower"][1].__setitem__(0, ["1", "1"]), "LDL_RECONSTRUCTION"),
        ("wrong_inverse", lambda x: x["V"][0].__setitem__(0, ["2", "1"]), "INVERSE"),
        ("wrong_delta", lambda x: x.update(delta=["1", "1"]), "DELTA"),
        ("wrong_gamma", lambda x: x.update(gamma=["2", "1"]), "GAMMA"),
        ("wrong_rho_identity", lambda x: x.update(rho=["1", "4000000000000"]), "RHO_IDENTITY"),
    ]
    refusals = []
    for name, change, code in fixtures:
        value = _mutated(baseline, change)
        refusals.append(_refusal(name,
            lambda value=value: consumer.validate_certificate(value, dimension=8, application=True),
            consumer.ProxyError, code))
    weak = deepcopy(baseline)
    weak["H"][0][0] = ["1", "4"]
    weak["delta"] = weak["rho"] = ["1", "4"]
    _same(_encode(consumer.validate_certificate(weak, dimension=8, application=False)), weak,
          "consistent weaker certificate is pure algebra only")
    refusals.append(_refusal("weaker_certificate_actual_accuracy",
        lambda: consumer.validate_certificate(weak, dimension=8, application=True),
        consumer.ProxyError, "RHO_ACCURACY"))
    return {"baseline": baseline, "weaker_fixture_only": weak, "refusals": refusals}


def _algebra_controls(consumer, families):
    _, _, _, gram = _seed_matrices()
    psd = (Fraction(7, 4), Fraction(1), Fraction(3, 4))
    refusals = []
    for name, values, fs, matrix, rho, code in [
        ("algebra_wrong_domain", (Fraction(1),) * 4, Fraction(4), gram, Fraction(0), "DOMAIN"),
        ("algebra_nonexact_psd", (1, Fraction(1), Fraction(1)), Fraction(4), gram, Fraction(0), "EXACT"),
        ("algebra_negative_psd", (Fraction(-1), Fraction(1), Fraction(1)), Fraction(4), gram, Fraction(0), "NEGATIVE_PSD"),
        ("algebra_negative_rho", psd, Fraction(4), gram, Fraction(-1), "RHO"),
        ("algebra_rho_one", psd, Fraction(4), gram, Fraction(1), "RHO"),
    ]:
        refusals.append(_refusal(name,
            lambda values=values, fs=fs, matrix=matrix, rho=rho:
                consumer.build_scenario(values, fs, matrix, rho, application=False),
            consumer.ProxyError, code))
    for family in families:
        for case in family["cases"]:
            expected = _expected_scenario(case)
            actual = consumer.build_scenario(case["psd"], case["fs"], case["G"],
                                             case["rho"], application=False)
            _same(actual, expected, case["name"] + ": complete primary derived fields")
            case["expected_primary"] = expected
            case["actual_primary"] = actual
    cases = {case["name"]: case for family in families for case in family["cases"]}
    for key in ("minimum_indices", "maximum_indices", "zero_interior_count", "positive_interior_count",
                "spectral_rank", "non_dc_rank", "rank_upper", "rank_status", "singularity_proved"):
        _same(cases["scale_four"]["actual_primary"][key], cases["colored"]["actual_primary"][key],
              "homogeneity retains " + key)
    return refusals


def _wrong_method_controls(families):
    """Reject explicit alternative formulae against the independent oracle.

    These are mathematical fixture checks, not runtime algorithm switches or
    patched consumer predicates.  Every rejected value is retained verbatim.
    """
    cases = {case["name"]: case for family in families for case in family["cases"]}
    colored, white, interior = cases["colored"], cases["white_unit"], cases["interior_only"]
    _, _, operator, gram = _seed_matrices()
    p0, p1, pn = colored["psd"]
    shared = colored["shared_terms"]
    variants = [
        ("halve_DC_endpoint", _circulant4((p0 / 2, p1, pn)), colored["K"]),
        ("halve_Nyquist_endpoint", _sandwich(operator, _circulant4((p0, p1, pn / 2))), colored["Omega"]),
        ("fail_interior_halving", _sandwich(operator, _circulant4((p0, 2 * p1, pn))), colored["Omega"]),
        ("use_df_instead_of_fs", _scale(colored["K"], Fraction(1, 4)), colored["K"]),
        ("include_DC_in_extrema", _scale(gram, Fraction(7)), colored["Upper"]),
        ("drop_Nyquist_from_extrema", _scale(gram, Fraction(2)), colored["Upper"]),
        ("drop_interior_from_extrema", _scale(gram, Fraction(3)), colored["Lower"]),
        ("lose_tied_extremizer", (1,), _expected_scenario(white)["minimum_indices"]),
        ("omit_shared_cross_term", _subtract(_add(shared["QQ"], shared["PP"]), shared["PQ"]), colored["Omega"]),
        ("invent_nonzero_lower_bound", gram, interior["Lower"]),
        ("infer_rank_from_zero_lower_bound", "zero_rank0", _expected_scenario(interior)["rank_status"]),
        ("claim_exact_rank_from_envelope", "positive_definite_rank2", _expected_scenario(interior)["rank_status"]),
    ]
    records = []
    for name, wrong, expected in variants:
        refusal = _refusal(name, lambda wrong=wrong, expected=expected, name=name:
                            _same(wrong, expected, name), QualificationError, "QUALIFICATION")
        records.append({**refusal, "rejected_value": wrong, "independent_expected": expected})
    return records


def _serialization_and_binding_controls(consumer):
    refusals = [
        _refusal("duplicate_input_JSON", lambda: consumer.parse_json(b'{"x":0,"x":1}'),
                 consumer.ProxyError, "JSON"),
        _refusal("nonfinite_input_JSON", lambda: consumer.parse_json(b'{"x":NaN}'),
                 consumer.ProxyError, "NONFINITE"),
        _refusal("overflow_input_JSON", lambda: consumer.parse_json(b'{"x":1e9999}'),
                 consumer.ProxyError, "NONFINITE"),
    ]
    for kind in ("SOURCE", "RUNTIME", "CUSTODY"):
        expected = {"bytes": 4, "sha256": hashlib.sha256(b"held").hexdigest()}
        changed = {"bytes": 4, "sha256": hashlib.sha256(b"edit").hexdigest()}
        _need(consumer.verify_binding(expected, deepcopy(expected), kind) is True,
              "unchanged fabricated " + kind + " binding")
        refusals.append(_refusal("changed_" + kind.lower() + "_binding",
            lambda kind=kind, expected=expected, changed=changed:
                consumer.verify_binding(changed, expected, kind), consumer.ProxyError, kind))
    for pair, name in [(["+1", "1"], "hex_plus"), (["01", "1"], "hex_leading_zero"),
                       (["-0", "1"], "hex_negative_zero"), (["2", "2"], "hex_unreduced"),
                       (["1", "0"], "hex_zero_denominator")]:
        refusals.append(_refusal(name, lambda pair=pair: consumer.decode_scalar(pair),
                                 consumer.ProxyError, "EXACT"))
    refusals.append(_refusal("rational_resource_cap",
        lambda: consumer.decode_scalar(["1" + "0" * 65536, "1"]),
        consumer.ProxyError, "RESOURCE"))
    refusals.append(_refusal("whole_body_identity",
        lambda: consumer.verify_body(b"changed", {"bytes": 4,
                     "sha256": hashlib.sha256(b"held").hexdigest()}),
        consumer.ProxyError, "INPUT"))
    return refusals


def _plus_one(pair):
    return _encode(Fraction(int(pair[0], 16), int(pair[1], 16)) + 1)


def _result_controls(validator, report):
    """One complete fabricated report; each mutation is independent/restored."""
    _need(validator.validate_result(report, expected_phase="fabricated_qualification") is True,
          "complete fabricated schema positive")
    payload = (json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    _same(validator.load_result(payload, expected_phase="fabricated_qualification"), report,
          "complete canonical fixture reload")
    mutations = [
        ("result_unknown_field", lambda x: x.update(extra=0), "SCHEMA"),
        ("result_source_pin_type", lambda x: x["provenance"]["sources"]["consumer"].update(bytes=True), "SOURCE"),
        ("result_changed_design", lambda x: x["provenance"]["sources"]["design"].update(sha256="0" * 64), "SOURCE"),
        ("result_runtime_pin_type", lambda x: x["provenance"]["runtime"]["inventory"].update(bytes=True), "RUNTIME"),
        ("result_missing_acceptance", lambda x: x["provenance"]["acceptance"].pop("ri86"), "CUSTODY"),
        ("result_fabricated_claims_prior_qualification", lambda x: x["provenance"]["acceptance"].update(qualification=deepcopy(x["provenance"]["acceptance"]["ri86"])), "PHASE"),
        ("result_array_hash", lambda x: x["scenarios"][0]["source_record"].update(sha256="0" * 64), "IDENTITY"),
        ("result_endpoint_mapping", lambda x: x["scenarios"][0]["derived"].update(lambda_dc=_plus_one(x["scenarios"][0]["derived"]["lambda_dc"])), "PSD_MAPPING"),
        ("result_interior_mapping", lambda x: x["scenarios"][0]["derived"]["non_dc_eigenvalues"].__setitem__(0, _plus_one(x["scenarios"][0]["derived"]["non_dc_eigenvalues"][0])), "PSD_MAPPING"),
        ("result_missing_tied_minimum", lambda x: x["scenarios"][0]["derived"]["minimum_indices"].pop(), "EXTREMA"),
        ("result_rank_overclaim", lambda x: x["scenarios"][0]["derived"].update(rank_status="zero_rank0"), "RANK"),
        ("result_singularity_flag", lambda x: x["scenarios"][0]["derived"].update(singularity_proved=True), "RANK"),
        ("result_Loewner_endpoint", lambda x: x["scenarios"][0]["derived"]["lower"][0].__setitem__(0, _plus_one(x["scenarios"][0]["derived"]["lower"][0][0])), "ENVELOPE"),
        ("result_trace", lambda x: x["scenarios"][0]["derived"]["trace"].__setitem__(0, _plus_one(x["scenarios"][0]["derived"]["trace"][0])), "ENVELOPE"),
        ("result_exact_power", lambda x: x["scenarios"][0]["derived"].update(q_proxy=_plus_one(x["scenarios"][0]["derived"]["q_proxy"])), "Q_PROXY"),
        ("result_power_difference", lambda x: x["scenarios"][0].update(q_difference=_plus_one(x["scenarios"][0]["q_difference"])), "Q_DIFFERENCE"),
        ("result_L1_injection_context", lambda x: x["scenarios"][2]["context"].update(NO_CW_HW_INJ=True), "METADATA"),
        ("result_gate_counts", lambda x: x["gates"]["counts"].update(passed=6), "GATE_INVENTORY"),
        ("result_changed_limitations", lambda x: x["limitations"].pop(), "LIMITATIONS"),
    ]
    refusals = []
    for name, change, code in mutations:
        value = _mutated(report, change)
        refusals.append(_refusal(name, lambda value=value: validator.validate_result(value),
                                 validator.ValidationError, code))
    refusals.append(_refusal("fabricated_phase_is_not_observed_admission",
        lambda: validator.validate_result(report, expected_phase="fixed_saved_application"),
        validator.ValidationError, "PHASE"))
    for name, body, code in [
        ("result_noncanonical_bytes", payload.rstrip(b"\n"), "CANONICAL_JSON"),
        ("result_duplicate_JSON", b'{"schema":0,"schema":1}\n', "DUPLICATE_JSON"),
        ("result_nonfinite_JSON", b'{"x":NaN}\n', "NONFINITE"),
        ("result_decimal_JSON", b'{"x":0.5}\n', "NONFINITE"),
    ]:
        refusals.append(_refusal(name, lambda body=body: validator.load_result(body),
                                 validator.ValidationError, code))
    _need(validator.validate_result(report, expected_phase="fabricated_qualification") is True,
          "complete fixture remains valid after independent mutations")
    return {"positive_schema_checks": 2, "canonical_reload_checks": 1,
            "canonical_fixture_pin": {"bytes": len(payload),
                                      "sha256": hashlib.sha256(payload).hexdigest()},
            "refusals": refusals}


def _canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("ascii")


def _pin(body):
    return {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}


def fabricated_runtime():
    """Schema fixture only: NEVER evidence of the qualification process runtime."""
    return {"versions": {"python": "3.11.6", "numpy": "2.1.3", "scipy": "1.14.1", "h5py": "3.12.1"},
            "python_implementation": "CPython", "python_build": ["fabricated", "not a runtime probe"],
            "operating_system": "fabricated", "os_release": "fabricated", "os_version": "fabricated",
            "machine": "fabricated", "byte_order": "little", "hdf5_version": "1.12.2",
            "numpy_configuration": "fabricated schema fixture; no numerical imports"}


def _fixed_indices():
    return {"left": {"interval": [0, 65536], "starts": [0, 8192, 16384, 24576, 32768, 40960, 49152],
                     "count": 7, "used_interval": [0, 65536], "unused_intervals": []},
            "right": {"interval": [69632, 131072], "starts": [69632, 77824, 86016, 94208, 102400, 110592],
                      "count": 6, "used_interval": [69632, 126976], "unused_intervals": [[126976, 131072]]}}


def _fixed_method():
    return {"design_pin": {"bytes": 24390,
                           "sha256": "3393eaf9252c55ddd4bb5de6fe87455dd7479f79812dbce245ec7c7611f4b4ce"},
            "fs": 4096, "segment_length": 16384, "stride": 8192, "nfft": 16384,
            "exclusion": [65536, 69632], "sides": _fixed_indices(), "bins": 8193,
            "endpoint_weights": [1, 1], "interior_weight": 2,
            "delta_f_hex": "0x1.0000000000000p-2", "detrend": "arithmetic_per_segment_mean_before_window",
            "window": "periodic_hann_sym_false", "fft": "numpy_rfft_backward",
            "scaling": "density_fs_times_actual_window_energy", "average": "arithmetic_mean_periodograms",
            "asd": "sqrt_mean_psd", "eps_hex": "0x1.0000000000000p-52", "tau_hex": "0x1.0000000000000p-40",
            "sqrt_relative_budget_hex": "0x1.0000000000000p-49"}


def fabricate_inputs(consumer, input_report):
    """Construct explicit schema fixtures, using only pinned RI37 metadata.

    The ignored prior numerical fields are labeled placeholders. These objects
    do not purport to pass RI83's spectral validator or reproduce RI73's operator
    computation. Only RI87's declared selection/admission interface is exercised.
    No actual RI83 or RI73 body is read; this function has no filesystem access.
    """
    metadata_pin = {"bytes": 31096,
                    "sha256": "a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80"}
    _same(_pin(_canonical(input_report)), metadata_pin, "held RI37 metadata body")
    _need(type(input_report) is dict and type(input_report.get("detectors")) is list
          and len(input_report["detectors"]) == 2, "held two-detector metadata")
    recovery = {"bytes": 16293,
                "sha256": "be0b518ca43e423d7e2a737b85eec0cad119a1b4cbd19ed4f056f662277d2dc0"}
    qualification = {"bytes": 63464716,
                     "sha256": "f247c20f9e112b48cc037d6256b47b5056ec354d58c0cf2817aad0363fc0fa0d"}
    fixed_inputs = (
        ("H1", "H-H1_LOSC_4_V2-1126259446-32.hdf5", 1040592, "50441a42c13fc1f14e5c4ea5527f1515",
         "6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6"),
        ("L1", "L-L1_LOSC_4_V2-1126259446-32.hdf5", 1007420, "361ae6a040a9fef7897b1e0124d5b0a1",
         "56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189"),
    )
    placeholder = {"fabricated_qualification": "unused prior numeric field; no predecessor computation"}
    spectra = {"schema": "ri78-off-event-spectra-v1", "method": _fixed_method(), "inputs": [],
               "frequency_hz": _array_record(Fraction(k, 4) for k in range(8193)),
               "window": deepcopy(placeholder), "detectors": [],
               "checks": {"identity": {"inspector_report_pin": metadata_pin,
                          "recovery_handoff_pin": recovery, "qualification_report_pin": qualification,
                          "fixed_dimensions_indices_and_flags": True}, "detectors": deepcopy(placeholder)},
               "limitations": deepcopy(consumer.RI83_LIMITATIONS)}
    # Distinct fixed synthetic powers exercise ordinary, tiny and all-zero output.
    variances = (Fraction(1), Fraction(4), Fraction(1, 2**140), Fraction(0))
    for d, (name, filename, size, md5, sha256) in enumerate(fixed_inputs):
        spectra["inputs"].append({"detector": name, "filename": filename, "bytes": size,
            "md5": md5, "sha256": sha256, "url": "https://gwosc.org/GW150914data/" + filename,
            "ri37_detector": deepcopy(input_report["detectors"][d]),
            "inspector_report_pin": deepcopy(metadata_pin), "recovery_handoff_pin": deepcopy(recovery)})
        detector = {"detector": name, "sides": []}
        for s, label in enumerate(("left", "right")):
            variance = variances[2 * d + s]
            values = (variance / 4096,) + (variance / 2048,) * 8191 + (variance / 4096,)
            spec = _fixed_indices()[label]
            side = {"side": label, **spec, "segments": [], "mean_psd": _array_record(values),
                    "asd": deepcopy(placeholder), "q": float(variance).hex(),
                    "psd_unit": "nominal_strain_squared_per_Hz", "asd_unit": "nominal_strain_per_sqrt_Hz"}
            for start in spec["starts"]:
                side["segments"].append({"start": start, "end": start + 16384,
                    "gps_offset_numerators": [start, start + 16384], "gps_offset_denominator": 4096,
                    "flag_rows": list(range(start // 4096, (start + 16384) // 4096)),
                    "dq_masks": [127] * 4, "injection_masks": [(31, 23)[d]] * 4,
                    "mean": "0x0.0p+0", "q": float(variance).hex(),
                    "raw_sha256": "0" * 64, "demeaned_sha256": "0" * 64, "windowed_sha256": "0" * 64,
                    "psd": deepcopy(placeholder)})
            detector["sides"].append(side)
        spectra["detectors"].append(detector)
    projection = _certificate_projection()
    identity, zero = projection["G"], projection["H"]
    certificate = {"mathematical_gate": True, "accuracy_gate": True,
                   "rho_limit": _encode(Fraction(1, 10**12)), "G": deepcopy(identity), "H": deepcopy(zero),
                   "delta": ["0", "1"], "eta2": ["0", "1"],
                   "ldl": {"positive": True, **deepcopy(projection["ldl"])},
                   "inverse": deepcopy(identity), "left_inverse_product": deepcopy(identity),
                   "right_inverse_product": deepcopy(identity), "gamma": ["1", "1"], "rho": ["0", "1"],
                   "status": "certified", "rank": 8, "inverse_error_norm_bound": ["0", "1"],
                   "inverse_lower": deepcopy(identity), "inverse_upper": deepcopy(identity)}
    # These gate IDs/dependency identities are static source metadata, not oracle
    # numerical answers. No accepted report is parsed or replayed to obtain them.
    prior = {"schema_version": "ri73-unit-white-operator-covariance-v1",
             "mode": "fixed_operator_covariance", "status": "fixed_operator_covariance_passed",
             "full_integration_qualified": True, "source_identity": deepcopy(consumer.RI73_SOURCE_PIN),
             "dependencies": deepcopy(consumer.RI73_DEPENDENCIES), "runtime": fabricated_runtime(),
             "inherited_arithmetic_contract": deepcopy(placeholder), "resource_contract": deepcopy(placeholder),
             "model": {"kind": "known_synthetic_unit_white", "mean": "zero", "covariance": "I_T",
                       "input_dimension": 10961, "output_dimension": 8},
             "dimensions": {"N": 2769, "L": 4096, "T": 10961}, "rows": [0, 1, 27, 805, 1384, 2741, 2767, 2768],
             "sample_spacing": ["1", "1000"], "gate_inventory": list(consumer.RI73_GATE_IDS),
             "gate_counts": {"total": 92, "passed": 92, "failed": 0}, "gates": [],
             "deterministic_fixture_admission_passed": True, "sampling_performed": False,
             "admitted_coefficient_design_requested": True, "reconstructed_rows_admitted": True,
             "exact_scalar_encoding": deepcopy(placeholder), "scope": deepcopy(placeholder)}
    for name in consumer.RI73_GATE_IDS:
        detail = {"certificate": certificate, "M_identity": deepcopy(placeholder), "R_identity": deepcopy(placeholder)} \
                 if name == "integration:gram" else deepcopy(placeholder)
        prior["gates"].append({"id": name, "passed": True, "detail": detail})
    return spectra, prior


def _admission_controls(consumer, spectra, prior, provenance):
    admitted = consumer.admit_spectra(spectra)
    _same([item["id"] for item in admitted], ["H1:left", "H1:right", "L1:left", "L1:right"],
          "four independent fixture scenarios")
    _same(consumer.admit_ri73(prior), _certificate_projection(), "complete fixture prior projection")
    altered_frequency = [Fraction(k, 4) for k in range(8193)]
    altered_frequency[1] = Fraction(1, 8)
    swapped_frequency = [Fraction(k, 4) for k in range(8193)]
    swapped_frequency[1], swapped_frequency[2] = swapped_frequency[2], swapped_frequency[1]
    specs = [
        ("spectra_unknown_field", lambda x: x.update(extra=0), "SPECTRA_SCHEMA"),
        ("spectra_changed_method", lambda x: x["method"].update(window="symmetric_hann"), "METHOD"),
        ("spectra_wrong_frequency_spacing", lambda x: x.update(frequency_hz=_array_record(altered_frequency)), "BINS"),
        ("spectra_wrong_frequency_order", lambda x: x.update(frequency_hz=_array_record(swapped_frequency)), "BINS"),
        ("spectra_changed_input_identity", lambda x: x["inputs"][0].update(sha256="0" * 64), "METADATA"),
        ("spectra_changed_complete_metadata", lambda x: x["inputs"][0]["ri37_detector"].update(fabricated_extra=True), "METADATA"),
        ("spectra_changed_prior_access", lambda x: x["limitations"].__setitem__(0, "blind validation"), "METADATA"),
        ("spectra_wrong_detector_order", lambda x: x["detectors"].reverse(), "DETECTOR_ORDER"),
        ("spectra_wrong_side_order", lambda x: x["detectors"][0]["sides"].reverse(), "SIDE"),
        ("spectra_changed_unused_tail", lambda x: x["detectors"][0]["sides"][1].update(unused_intervals=[]), "SIDE"),
        ("spectra_wrong_unit", lambda x: x["detectors"][0]["sides"][0].update(psd_unit="calibrated_covariance"), "UNITS"),
        ("spectra_changed_L1_CW_flag", lambda x: x["detectors"][1]["sides"][0]["segments"][0].update(injection_masks=[31] * 4), "METADATA"),
        ("spectra_changed_quality_flag", lambda x: x["detectors"][0]["sides"][0]["segments"][0].update(dq_masks=[0] * 4), "METADATA"),
        ("spectra_changed_segment_interval", lambda x: x["detectors"][0]["sides"][0]["segments"][0].update(end=16385), "METADATA"),
        ("spectra_negative_saved_power", lambda x: x["detectors"][0]["sides"][0].update(q="-0x1.0000000000000p+0"), "NEGATIVE_PSD"),
    ]
    refusals = []
    for name, change, code in specs:
        value = _mutated(spectra, change)
        refusals.append(_refusal(name, lambda value=value: consumer.admit_spectra(value), consumer.ProxyError, code))
    side = spectra["detectors"][0]["sides"][0]
    refusals.append(_refusal("wrong_selected_PSD_field", lambda: consumer.select_psd(side, "asd"),
                             consumer.ProxyError, "PSD_SELECTION"))
    refusals.append(_refusal("wrong_reference_PSD_field", lambda: consumer.select_psd(side, "reference_psd"),
                             consumer.ProxyError, "PSD_SELECTION"))
    refusals.append(_refusal("missing_selected_PSD", lambda: consumer.select_psd({}),
                             consumer.ProxyError, "PSD_SELECTION"))
    prior_specs = [
        ("prior_unknown_field", lambda x: x.update(extra=0), "PRIOR_SCHEMA"),
        ("prior_incomplete_status", lambda x: x.update(full_integration_qualified=False), "PRIOR_STATUS"),
        ("prior_colored_model", lambda x: x["model"].update(kind="estimated_colored"), "PRIOR_MODEL"),
        ("prior_wrong_dimensions", lambda x: x["dimensions"].update(T=10960), "DIMENSIONS"),
        ("prior_wrong_rows", lambda x: x["rows"].reverse(), "ROWS"),
        ("prior_changed_source", lambda x: x["source_identity"].update(sha256="0" * 64), "SOURCE"),
        ("prior_changed_dependency", lambda x: x["dependencies"]["engine"].update(sha256="0" * 64), "SOURCE"),
        ("prior_changed_runtime_version", lambda x: x["runtime"]["versions"].update(numpy="fabricated changed"), "RUNTIME"),
        ("prior_missing_integration_gate", lambda x: x.update(gates=[row for row in x["gates"] if row["id"] != "integration:gram"]), "GATE_INVENTORY"),
        ("prior_duplicate_integration_gate", lambda x: x["gates"][0].update(id="integration:gram"), "GATE_INVENTORY"),
        ("prior_wrong_inventory", lambda x: x["gate_inventory"].reverse(), "GATE_INVENTORY"),
        ("prior_failed_gate", lambda x: x["gates"][0].update(passed=False), "GATE_STATUS"),
        ("prior_wrong_gate_count", lambda x: x["gate_counts"].update(passed=91), "GATE_STATUS"),
    ]
    for name, change, code in prior_specs:
        value = _mutated(prior, change)
        refusals.append(_refusal(name, lambda value=value: consumer.admit_ri73(value), consumer.ProxyError, code))
    changed_runtime = _mutated(prior, lambda x: x["runtime"].update(python_build=["different", "fabricated"]))
    refusals.append(_refusal("changed_complete_runtime_fingerprint",
        lambda: consumer.build_result(spectra, changed_runtime, provenance, phase="fabricated_qualification"),
        consumer.ProxyError, "RUNTIME"))
    changed_phase = _mutated(provenance, lambda x: x["inputs"].update(ri83=deepcopy(consumer.RI83_PIN)))
    refusals.append(_refusal("fabricated_inputs_claim_actual_identity",
        lambda: consumer.validate_provenance(changed_phase, "fabricated_qualification"), consumer.ProxyError, "PHASE"))
    claimed_qualification = _mutated(provenance, lambda x: x["acceptance"].update(qualification=deepcopy(x["acceptance"]["ri86"])))
    refusals.append(_refusal("fabricated_claims_completed_qualification",
        lambda: consumer.validate_provenance(claimed_qualification, "fabricated_qualification"), consumer.ProxyError, "PHASE"))
    return {"positive_admission_checks": 2, "projected_fixture_certificate": _certificate_projection(),
            "refusals": refusals}


def _full_fixture_expected(report):
    """Independent full-size white-spectrum consequences, without filter calls."""
    identity = tuple(tuple(Fraction(i == j) for j in range(8)) for i in range(8))
    variances = (Fraction(1), Fraction(4), Fraction(1, 2**140), Fraction(0))
    expectations = []
    for scenario, variance in zip(report["scenarios"], variances, strict=True):
        matrix = _scale(identity, variance)
        expected = {"lambda_dc": variance, "lambda_nyquist": variance,
                    "non_dc_eigenvalues": (variance,) * 8192, "q_proxy": variance,
                    "ell": variance, "u": variance, "minimum_indices": tuple(range(1, 8193)),
                    "maximum_indices": tuple(range(1, 8193)), "zero_interior_count": 8191 if variance == 0 else 0,
                    "positive_interior_count": 8191 if variance > 0 else 0,
                    "spectral_rank": 16384 if variance > 0 else 0, "non_dc_rank": 16383 if variance > 0 else 0,
                    "rank_upper": 8 if variance > 0 else 0,
                    "rank_status": "positive_definite_rank8" if variance > 0 else "zero_rank0",
                    "singularity_proved": variance == 0, "lower": matrix, "upper": matrix,
                    "diagonal": ((variance, variance),) * 8, "trace": (8 * variance, 8 * variance)}
        _same(scenario["derived"], _encode(expected), scenario["id"] + ": full white-spectrum consequences")
        _same(scenario["q_difference"], ["0", "1"], scenario["id"] + ": exact saved/proxy power difference")
        expectations.append({"id": scenario["id"], "variance": variance,
                             "expected_derived": expected, "expected_q_difference": Fraction(0)})
    return expectations


def run(consumer, validator, input_report, provenance):
    """Captured-library entry point for a separately admitted qualification run.

    The caller passes modules captured under its freeze, only pinned RI37 input
    metadata, and explicit fabricated provenance. The actual outer process's
    runtime/source/resource custody is separate and is never replaced by the
    synthetic runtime field inside the schema fixture. No file I/O or imports
    of a target, numerical library, HDF or predecessor occur in this function.
    """
    spectra, prior = fabricate_inputs(consumer, input_report)
    input_pins = {"ri83": _pin(_canonical(spectra)), "ri73": _pin(_canonical(prior))}
    _same(provenance["inputs"], input_pins, "explicit fabricated whole-body identities")
    _same(provenance["runtime"]["fingerprint"], _pin(_canonical(fabricated_runtime())),
          "explicit fabricated schema runtime identity")
    consumer.validate_provenance(provenance, "fabricated_qualification")
    families = _tiny_oracle_families()
    decoder = _decoder_controls(consumer)
    certificates = _certificate_controls(consumer)
    algebra = _algebra_controls(consumer, families)
    wrong_method = _wrong_method_controls(families)
    serialization = _serialization_and_binding_controls(consumer)
    admissions = _admission_controls(consumer, spectra, prior, provenance)
    report = consumer.build_result(spectra, prior, provenance, phase="fabricated_qualification")
    full_expected = _full_fixture_expected(report)
    schema = _result_controls(validator, report)
    groups = {"decoder": decoder["refusals"], "certificate": certificates["refusals"],
              "algebra": algebra, "wrong_method_oracle": wrong_method, "serialization_binding": serialization,
              "metadata_prior_admission": admissions["refusals"], "complete_result_schema": schema["refusals"]}
    expected_counts = {"decoder": 7, "certificate": 11, "algebra": 5, "wrong_method_oracle": 12,
                       "serialization_binding": 13, "metadata_prior_admission": 34, "complete_result_schema": 24}
    _same({name: len(rows) for name, rows in groups.items()}, expected_counts, "closed refusal counts")
    inventory = [row["id"] for rows in groups.values() for row in rows]
    _need(len(inventory) == len(set(inventory)), "refusal IDs must be globally unique")
    _need(len(families) == 7 and sum(len(family["cases"]) for family in families) == 12,
          "seven fixed oracle families and twelve primary comparisons")
    # Recheck that independent mutation lifetimes left both fixtures unchanged.
    _same({"ri83": _pin(_canonical(spectra)), "ri73": _pin(_canonical(prior))}, input_pins,
          "fabricated inputs restored after all controls")
    return _encode({"schema": "ri87-colored-proxy-qualification-v1", "phase": "fabricated_qualification",
        "status": "all_declared_checks_passed", "source_provenance": deepcopy(provenance),
        "metadata_input_pin": _pin(_canonical(input_report)), "fixture_input_pins": input_pins,
        "families": families, "decoder_controls": decoder, "certificate_controls": certificates,
        "algebra_refusals": algebra, "wrong_method_oracle_refusals": wrong_method,
        "serialization_binding_refusals": serialization, "admission_controls": admissions,
        "fabricated_inputs": {"ri83": spectra, "ri73": prior}, "full_expected": full_expected,
        "complete_fabricated_result": report, "result_schema_controls": schema,
        "counts": {"oracle_families": 7, "primary_tiny_cases": 12, "full_size_scenarios": 4,
                   "refusals_by_group": expected_counts, "refusals_total": len(inventory)},
        "refusal_inventory": inventory,
        "scope": ["All numerical input values are fixed fabricated rational/binary64 fixtures.",
                  "RI37 metadata is the only predecessor object supplied; its complete canonical identity is checked.",
                  "Tiny covariance, cross terms, cropped covariance and rank use an independent M=4 cosine/dense route.",
                  "Full-size fixture expectations are white-spectrum algebra with an identity Gram, not actual filter output.",
                  "The full-result fake runtime is schema data; actual process runtime/source/resource custody is external.",
                  "Unused prior numerical fields are explicit placeholders; neither predecessor algorithm is replayed.",
                  "No actual PSD, RI73 numerical report, HDF, FFT, filter reconstruction, sampling or physical claim is involved."]})


if __name__ == "__main__":
    raise SystemExit("RI87 qualification library: execution requires the separately reviewed captured-source caller.")
