"""Frozen RI-55 synthetic qualification; no scientific input is opened here.

The exact DFI oracle, adjoint engine, published binary64 filter and independently
authored Decimal-80 recurrence have separate source identities. Every dependency
snapshot is checked before parsing or executing it. A successful report is a
receipt for these fixed tests, not a physical continuation or roundoff bound.
"""

from decimal import Decimal
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import stat
import struct
import sys


N, L = 2769, 4096
T = N + 2 * L
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
MANIFEST_SHA256 = "700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0"
RECIPE_SHA256 = "872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a"
DESIGN_SHA256 = "e672cea6c5f06c5927b54b0021636793c14b01e8efe57aa8e719fd464a527e45"
ENGINE_PIN = {"bytes": 24882, "sha256": "3a7b847bd8bec752a48af2c339a5cebd6d923c3b307c2c54910abddbf51703b4"}
ORACLE_PIN = {"bytes": 9484, "sha256": "37f3dea8ccbc495e90123b51e35150c8e5324c18c598954182e76943a285a651"}
DEPENDENCIES = {
    "filtering": {"path": "gwosc_nominal_processing_v1/filtering.py", "bytes": 8805,
                  "sha256": "9a93c1f218fecfa6fdf7ee0e30e054ad0973dfb1f04ae339dfbb0e7a6f8ae1be"},
    "reference": {"path": "gwosc_nominal_processing_v1/reference.py", "bytes": 7253,
                  "sha256": "c8cffaac8bf0c1647a120ecb00ba1505ef69b60f80cda653d60b2a2f7e9da305"},
    "coefficients": {"path": "gwosc_nominal_processing_v1/COEFFICIENTS.json", "bytes": 7698,
                     "sha256": MANIFEST_SHA256},
    "prior_qualification": {"path": "gwosc_nominal_processing_v1/SYNTHETIC_REPORT.json", "bytes": 107468,
                            "sha256": "2522ca70a1402700e644feba25bf70abf2b5720a80031304f82225ea0e5808c3"},
    "recipe": {"path": "gwosc_nominal_display_v1/RECIPE.md", "bytes": 14014,
               "sha256": RECIPE_SHA256},
    "design": {"path": "gwosc_context_sensitivity_v1/DESIGN.md", "bytes": 21702,
               "sha256": DESIGN_SHA256},
}
FIXTURE_NAMES = ("zeros", "ones", "impulse_first", "impulse_middle", "impulse_last",
                 "alternating", "period17")
TOY_NAMES = ("identity", "first_order", "biquad", "two_sections", "two_stages", "fir",
             "zero_dc", "zero_dc_then_biquad")
REFUSAL_NAMES = ("changed_bytes", "changed_coefficients", "changed_stage_order",
                 "changed_padding", "wrong_length", "nonfinite", "unknown_arithmetic",
                 "missing_qualification", "failed_qualification", "unsupported_rows",
                 "unsupported_context", "invalid_envelope", "missing_exact_toy_value",
                 "false_nonzero", "overwide_interval")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def export_json(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True,
                       allow_nan=False) + "\n").encode("ascii")


def identity(payload):
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def verify_payload(payload, pin, label):
    require(type(payload) is bytes and identity(payload) == pin,
            label + ": snapshot identity mismatch")
    return payload


def bound_bytes(path, pin, label):
    require(type(pin.get("bytes")) is int and pin["bytes"] > 0 and
            type(pin.get("sha256")) is str and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]),
            label + ": source or receipt pin not frozen")
    try:
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_size == pin["bytes"],
                label + ": expected pinned regular file")
        with path.open("rb") as stream:
            payload = stream.read(pin["bytes"] + 1)
    except OSError as error:
        raise ValueError(label + ": cannot read file") from error
    return verify_payload(payload, {"bytes": pin["bytes"], "sha256": pin["sha256"]}, label)


def parse_json(payload):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    def constant(value):
        raise ValueError("nonfinite JSON value: " + value)
    return json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)


def load_module(name, path, payload):
    spec = importlib.util.spec_from_file_location("ri57_pinned_" + name, path)
    require(spec is not None and spec.loader is not None, "cannot specify pinned module")
    module = importlib.util.module_from_spec(spec)
    # A dataclass-capable module identity; execute the retained, verified bytes.
    sys.modules[spec.name] = module
    exec(compile(payload, str(path), "exec"), module.__dict__)
    return module


def runtime():
    import h5py
    import numpy as np
    import platform
    import scipy
    return {
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "scipy": scipy.__version__, "h5py": h5py.__version__},
        "python_implementation": platform.python_implementation(), "python_build": sys.version,
        "operating_system": platform.system(), "os_release": platform.release(),
        "os_version": platform.version(), "machine": platform.machine(),
        "byte_order": sys.byteorder, "hdf5_version": h5py.version.hdf5_version,
        "numpy_configuration": np.show_config(mode="dicts"),
    }


def check_coefficients(admitted):
    payload = canonical(admitted["production"].coefficient_manifest(admitted["stages"]))
    require(payload == admitted["coefficient_bytes"] and
            hashlib.sha256(payload).hexdigest() == MANIFEST_SHA256,
            "coefficients, stage order or padding differ from the frozen manifest")


def admission():
    base = Path(__file__).resolve().parent.parent
    local = Path(__file__).resolve().parent
    payloads = {name: bound_bytes(base / pin["path"], pin, name)
                for name, pin in DEPENDENCIES.items()}
    payloads["engine"] = bound_bytes(local / "operator.py", ENGINE_PIN, "engine")
    payloads["oracle"] = bound_bytes(local / "oracle.py", ORACLE_PIN, "oracle")
    # All source/report/manifest bytes are bound before parsing or execution.
    prior = parse_json(payloads["prior_qualification"])
    require(prior["schema_version"] == "ri44-synthetic-qualification-v1" and
            prior["status"] == "all_synthetic_gates_passed" and
            canonical(prior["gate_counts"]) == canonical({"total": 105, "passed": 105, "failed": 0}),
            "RI-44 qualification not admitted")
    require(canonical(prior["coefficient_manifest"]) == payloads["coefficients"] and
            prior["coefficient_manifest_sha256"] == MANIFEST_SHA256 and
            prior["source_identity"]["accepted_recipe_sha256"] == RECIPE_SHA256,
            "RI-44 manifest/recipe mismatch")
    for key in ("filtering", "reference"):
        require(prior["source_identity"][key]["sha256"] == DEPENDENCIES[key]["sha256"],
                "RI-44 source mismatch")
    current = runtime()
    require(current["versions"] == prior["runtime"]["required_versions"], "runtime versions differ")
    for key, value in current.items():
        require(canonical(value) == canonical(prior["runtime"][key]), "runtime differs: " + key)
    production = load_module("filtering", base / DEPENDENCIES["filtering"]["path"], payloads["filtering"])
    reference = load_module("reference", base / DEPENDENCIES["reference"]["path"], payloads["reference"])
    engine = load_module("engine", local / "operator.py", payloads["engine"])
    oracle = load_module("oracle", local / "oracle.py", payloads["oracle"])
    stages = production.design_stages()
    admitted = {"production": production, "reference": reference, "engine": engine,
                "oracle": oracle, "stages": stages, "coefficient_bytes": payloads["coefficients"],
                "runtime": current, "arithmetic": engine.arithmetic_contract()}
    check_coefficients(admitted)
    admitted["fraction_stages"] = tuple(tuple(tuple(Fraction.from_float(float(v)) for v in row)
        for row in stage["sos"].tolist()) for stage in stages)
    admitted["padlens"] = tuple(stage["padlen"] for stage in stages)
    require(admitted["padlens"] == (27,) + (9,) * 16, "fixed padding mismatch")
    return admitted


def rational(value):
    require(type(value) is str and len(value) <= 20000, "expected bounded canonical rational string")
    result = Fraction(value)
    require(str(result) == value, "noncanonical rational string")
    return result


def interval(value):
    require(type(value) in (tuple, list) and len(value) == 2 and
            all(type(x) is Fraction for x in value) and value[0] <= value[1],
            "expected ordered exact Fraction interval")
    return tuple(value)


def encoded_interval(value):
    return [str(x) for x in interval(value)]


def decoded_interval(value):
    require(type(value) is list and len(value) == 2, "bad encoded interval")
    return interval(tuple(rational(x) for x in value))


def contains(bounds, exact):
    lo, hi = interval(bounds)
    require(type(exact) is Fraction and lo <= exact <= hi,
            "enclosure misses exact value")


def abs_interval(bounds):
    lo, hi = interval(bounds)
    return (Fraction(0) if lo <= 0 <= hi else min(abs(lo), abs(hi)), max(abs(lo), abs(hi)))


def interval_sum(bounds):
    checked = [interval(value) for value in bounds]
    return (sum((x[0] for x in checked), Fraction(0)),
            sum((x[1] for x in checked), Fraction(0)))


def context_interval(coefficients, values):
    require(len(coefficients) == len(values) and all(type(x) is Fraction for x in values),
            "context length/type mismatch")
    return interval_sum([(lo * x, hi * x) if x >= 0 else (hi * x, lo * x)
                         for (lo, hi), x in zip(map(interval, coefficients), values)])


def interval_identity(values):
    return identity(canonical([encoded_interval(x) for x in values]))


def row_status(bounds):
    checked = tuple(interval(x) for x in bounds)
    require(len(checked) > 0, "empty coefficient row")
    for index, (lo, hi) in enumerate(checked):
        if lo > 0 or hi < 0:
            return {"status": "proven_nonzero", "witness_index": index,
                    "witness_interval": encoded_interval((lo, hi))}
    if all(lo == hi == 0 for lo, hi in checked):
        return {"status": "exact_zero", "proof": "Every coefficient enclosure is the singleton zero."}
    return {"status": "unresolved", "reason": "All coefficient intervals contain zero."}


def validate_row_status(status, bounds):
    require(canonical(status) == canonical(row_status(bounds)), "invalid nonzero/zero/unresolved claim")


def require_width(bounds, limit, label, exact_zero=False):
    lo, hi = interval(bounds)
    require(type(limit) is Fraction and limit >= 0 and hi - lo <= limit, label + ": width gate failed")
    if exact_zero:
        require(lo == hi == 0, label + ": exact zero interval required")


def pilot(rows=ROWS, central=N, side=L):
    require(type(rows) is tuple and all(type(x) is int for x in rows) and rows == ROWS,
            "unsupported pilot rows")
    require(type(central) is int and type(side) is int and central == N and side == L,
            "unsupported context dimensions")


def arithmetic_config(value, admitted):
    require(canonical(value) == canonical(admitted["arithmetic"]), "unknown arithmetic configuration")


def envelope(numerator=None, denominator=None, label=None):
    if numerator is None and denominator is None and label is None:
        return None
    require(type(numerator) is str and re.fullmatch(r"0|[1-9][0-9]*", numerator) and
            type(denominator) is str and re.fullmatch(r"[1-9][0-9]*", denominator) and
            len(numerator) <= 1234 and len(denominator) <= 1234,
            "envelope requires canonical nonnegative numerator/positive denominator")
    n, d = int(numerator), int(denominator)
    require(n.bit_length() <= 4096 and d.bit_length() <= 4096 and math.gcd(n, d) == 1,
            "envelope integers must be coprime and at most 4096 bits")
    require(type(label) is str and 1 <= len(label) <= 4096 and label.strip() == label,
            "envelope requires an assumption/source label")
    return {"value": Fraction(n, d), "numerator": numerator, "denominator": denominator, "label": label}


def array_identity(values, length):
    require(type(values) in (tuple, list) and len(values) == length and
            all(type(x) is float and math.isfinite(x) for x in values),
            "expected complete finite binary64 list")
    payload = b"".join(struct.pack("<d", x) for x in values)
    return {"shape": [length], "dtype": "little-endian binary64", "order": "C", **identity(payload)}


def fixtures(length):
    require(type(length) is int and length in (N, T), "unsupported fixture length")
    for name in FIXTURE_NAMES:
        if name == "zeros":
            values = [0.0] * length
        elif name == "ones":
            values = [1.0] * length
        elif name.startswith("impulse"):
            values = [0.0] * length
            index = {"impulse_first": 0, "impulse_middle": length // 2, "impulse_last": length - 1}[name]
            values[index] = 1.0
        elif name == "alternating":
            values = [float((-1) ** k) for k in range(length)]
        else:
            values = [((k % 17) - 8) / 8.0 for k in range(length)]
        yield name, values


def unit(length, selected):
    return tuple(Fraction(int(k == selected)) for k in range(length))


def dot(left, right):
    require(len(left) == len(right), "dot dimensions differ")
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def certified(seed, prepared, engine):
    result = engine.certified_adjoint(seed, prepared)
    require(type(result) is dict and result.get("status") == "certified", "adjoint not certified")
    centers = result["center"]
    bounds = result["intervals"]
    require(len(centers) == len(seed) == len(bounds) and all(type(x) is Fraction for x in centers),
            "invalid certified adjoint dimensions/centers")
    require(type(result["radius"]) is Fraction and result["radius"] >= 0, "invalid adjoint radius")
    for value, pair in zip(centers, bounds):
        lo, hi = interval(pair)
        require(lo <= value <= hi and value - lo <= result["radius"] and hi - value <= result["radius"],
                "invalid adjoint center/radius enclosure")
    canonical(result["proof"])
    return result


def assemble_row(row, short, long, central, side):
    a = tuple((v[0] - w[1], v[1] - w[0])
              for v, w in zip(long["intervals"][side:side + central], short["intervals"]))
    b = tuple(long["intervals"][:side]) + tuple(long["intervals"][side + central:])
    gain = interval_sum([abs_interval(value) for value in b])
    return {"row": row, "a": a, "b": b, "gain": gain,
            "operator_status": row_status(b), "short": short, "long": long}


def row_summary(row):
    return {"row": row["row"], "a_enclosure_identity": interval_identity(row["a"]),
            "b_enclosure_identity": interval_identity(row["b"]),
            "gain_interval": encoded_interval(row["gain"]),
            "operator_status": row["operator_status"],
            "short_adjoint_proof": row["short"]["proof"], "long_adjoint_proof": row["long"]["proof"],
            "short_radius_exact": str(row["short"]["radius"]),
            "long_radius_exact": str(row["long"]["radius"])}


def build_rows(admitted, prepared=None):
    pilot()
    engine = admitted["engine"]
    if prepared is None:
        prepared = engine.prepare(admitted["fraction_stages"], admitted["padlens"])
    result = []
    for index in ROWS:
        short = certified(unit(N, index), prepared, engine)
        long = certified(unit(T, L + index), prepared, engine)
        row = assemble_row(index, short, long, N, L)
        require_width(row["gain"], max(Fraction(1), row["gain"][1]) / 10**12, "gain")
        validate_row_status(row["operator_status"], row["b"])
        result.append(row)
    return tuple(result)


def toy_case(config, central, side, admitted):
    oracle, engine = admitted["oracle"], admitted["engine"]
    stages, pads = config["stages"], config["padlens"]
    total = central + 2 * side
    short_matrix = oracle.matrix_fraction(central, stages, pads)
    long_matrix = oracle.matrix_fraction(total, stages, pads)
    prepared = engine.prepare(stages, pads)
    certified_matrices = {}
    entry_count = 0
    for length, matrix in ((central, short_matrix), (total, long_matrix)):
        enclosed = []
        dc = Fraction(1)
        for stage in stages:
            for b0, b1, b2, a0, a1, a2 in stage:
                dc *= ((b0 + b1 + b2) / (a0 + a1 + a2)) ** 2
        ones = (Fraction(1),) * length
        expected_constant = (dc,) * length
        require(oracle.forward_fraction(ones, stages, pads) == expected_constant and
                tuple(engine.forward_fraction(ones, stages, pads)) == expected_constant and
                tuple(sum(row, Fraction(0)) for row in matrix) == expected_constant,
                "exact constant/zero-DC structure failed")
        for index, expected in enumerate(matrix):
            seed = unit(length, index)
            require(tuple(engine.adjoint_fraction(seed, stages, pads)) == expected, "exact transpose mismatch")
            column = tuple(matrix[k][index] for k in range(length))
            require(tuple(engine.forward_fraction(seed, stages, pads)) == column, "exact forward mismatch")
            certificate = certified(seed, prepared, engine)
            for pair, value in zip(certificate["intervals"], expected):
                contains(pair, value)
                entry_count += 1
            enclosed.append(certificate)
        certified_matrices[length] = enclosed
    x = oracle.toy_center(central)
    ex = (Fraction(0),) * side + x + (Fraction(0),) * side
    require(ex[side:side + central] == x, "CE identity failed")
    zero_u = (Fraction(1),) * side + (Fraction(0),) * central + (Fraction(1),) * side
    require(all(v == 0 for v in zero_u[side:side + central]), "CU identity failed")
    base_short = oracle.forward_fraction(x, stages, pads)
    base_long = oracle.forward_fraction(ex, stages, pads)
    corners_checked = witnesses_checked = 0
    for row_index in range(central):
        a = tuple(long_matrix[side + row_index][side + k] - short_matrix[row_index][k]
                  for k in range(central))
        b = long_matrix[side + row_index][:side] + long_matrix[side + row_index][side + central:]
        d = dot(a, x)
        require(d == base_long[side + row_index] - base_short[row_index], "zero-extension identity failed")
        row = assemble_row(row_index, certified_matrices[central][row_index],
                           certified_matrices[total][side + row_index], central, side)
        contains(row["gain"], sum(map(abs, b), Fraction(0)))
        contains(context_interval(row["a"], x), d)
        if config["name"] == "identity":
            require(all(value == 0 for value in a + b), "identity operator zero-row exception failed")
        for amplitude in oracle.TOY_AMPLITUDES:
            sharp = oracle.sharp_box_fraction(d, b, amplitude)
            attained = d + dot(b, sharp["witness"])
            require(abs(attained) == sharp["bound"] and attained == sharp["attained_value"] and
                    all(abs(value) <= amplitude for value in sharp["witness"]), "sharp witness failed")
            extrema = []
            for z in oracle.box_corners_fraction(2 * side, amplitude):
                full = z[:side] + x + z[side:]
                observed = oracle.forward_fraction(full, stages, pads)[side + row_index] - base_short[row_index]
                require(observed == d + dot(b, z), "affine context identity failed")
                require(abs(observed) <= sharp["bound"], "box bound failed")
                extrema.append(abs(observed))
                corners_checked += 1
            require(max(extrema) == sharp["bound"], "corner maximum is not sharp")
            witnesses_checked += 1
    return {"configuration": config["name"], "central": central, "side": side,
            "matrix_entries_contained": entry_count, "corners_checked": corners_checked,
            "attaining_witnesses_checked": witnesses_checked,
            "matrix_identity": identity(canonical([[str(v) for v in row] for row in long_matrix]))}


def forward_case(name, values, admitted):
    import numpy as np
    length = len(values)
    before = array_identity(values, length)
    source = np.array(values, dtype=np.float64)
    output = admitted["production"].apply_filter(source, admitted["stages"])
    require(array_identity(source.tolist(), length) == before and not np.shares_memory(source, output),
            "production input modified or output aliased")
    output_values = output.tolist()
    output_identity = array_identity(output_values, length)
    reference = admitted["reference"].reference_filter(values,
        [stage["sos"].tolist() for stage in admitted["stages"]], list(admitted["padlens"]))
    require(type(reference) is list and len(reference) == length and
            all(type(x) is Decimal and x.is_finite() for x in reference), "invalid Decimal reference")
    errors = [abs(Fraction.from_float(y) - Fraction(r)) for y, r in zip(output_values, reference)]
    threshold = max(Fraction(1), max(abs(Fraction.from_float(x)) for x in values)) / 10**9
    maximum = max(errors)
    zero = all(x == 0.0 for x in output_values) and all(x == 0 for x in reference)
    require(maximum <= threshold and (name != "zeros" or zero), "complete forward gate failed")
    return reference, {"length": length, "fixture": name, "sample_count_compared": length,
        "input_identity": before, "output_identity": output_identity,
        "decimal_output_identity": identity(canonical([str(x) for x in reference])),
        "maximum_absolute_error_exact": str(maximum), "maximum_error_index": errors.index(maximum),
        "threshold_exact": str(threshold), "exact_zero_required": name == "zeros",
        "exact_zero_output_and_reference": zero}


def gate_ids():
    result = [f"toy:{name}:{central}:{side}" for name in TOY_NAMES for central in (4, 7) for side in (1, 2)]
    result += [f"forward:{length}:{name}" for length in (N, T) for name in FIXTURE_NAMES]
    result += [f"adjoint:{length}:{seed}:{name}" for length in (N, T)
               for seed in (*map(str, ROWS), "dense") for name in FIXTURE_NAMES]
    result += [f"enclosure:{row}" for row in ROWS]
    result += ["structural_constant"]
    result += ["refusal:" + name for name in REFUSAL_NAMES]
    return result


def common_record(admitted):
    return {"schema_version": "ri57-context-qualification-v1", "dimensions": {"N": N, "L": L, "T": T},
        "rows": list(ROWS), "source_identity": identity(Path(__file__).read_bytes()),
        "engine_identity": ENGINE_PIN, "oracle_identity": ORACLE_PIN, "published_dependencies": DEPENDENCIES,
        "runtime": admitted["runtime"], "arithmetic_contract": admitted["arithmetic"],
        "coefficient_manifest_sha256": MANIFEST_SHA256, "design_sha256": DESIGN_SHA256,
        "gate_inventory": gate_ids(), "fixture_names": list(FIXTURE_NAMES),
        "comparison_arithmetic": "Exact Fraction inner products of retained 256-bit dyadic adjoint centers and finite Decimal-80 forward outputs; no additional dot-product tolerance.",
        "scope": "Fixed synthetic qualification and eight exact-operator coefficient rows only; no actual central export, physical envelope, production roundoff bound or unexamined row maximum."}


def validate_qualification(report, admitted):
    require(type(report) is dict, "missing qualification")
    for key, value in common_record(admitted).items():
        require(canonical(report.get(key)) == canonical(value), "qualification mismatch: " + key)
    ids = gate_ids()
    require(report.get("status") == "all_context_gates_passed" and
            canonical(report.get("gate_counts")) == canonical({"total": len(ids), "passed": len(ids), "failed": 0}),
            "qualification failed or incomplete")
    require(report.get("additional_failures") == [], "qualification retains engine failures")
    gates = report.get("gates")
    require(type(gates) is list and len(gates) == len(ids), "qualification gate coverage changed")
    for expected, item in zip(ids, gates):
        require(type(item) is dict and item.get("id") == expected and item.get("passed") is True,
                "qualification gate failed or changed")
        detail = item["detail"]
        if expected.startswith("forward:"):
            require(rational(detail["threshold_exact"]) == Fraction(1, 10**9) and
                    0 <= rational(detail["maximum_absolute_error_exact"]) <= Fraction(1, 10**9),
                    "forward threshold/error changed")
            if expected.endswith(":zeros"):
                require(detail["exact_zero_required"] is True and detail["exact_zero_output_and_reference"] is True and
                        rational(detail["maximum_absolute_error_exact"]) == 0, "forward zero failed")
        if expected.startswith("adjoint:"):
            require(0 <= rational(detail["absolute_residual_exact"]) <= rational(detail["threshold_exact"]) and
                    rational(detail["threshold_exact"]) == max(Fraction(1), rational(detail["scale_exact"])) / 10**9,
                    "adjoint residual/threshold failed")
        if expected.startswith("enclosure:"):
            gain = decoded_interval(detail["row"]["gain_interval"])
            require_width(gain, max(Fraction(1), gain[1]) / 10**12, "qualification gain")
            require([x["fixture"] for x in detail["centers"]] == list(FIXTURE_NAMES), "center gate coverage changed")
            for center in detail["centers"]:
                require_width(decoded_interval(center["context_interval"]),
                              (Fraction(0) if center["fixture"] == "zeros" else Fraction(1, 10**12)),
                              "qualification context", center["fixture"] == "zeros")
    return True


def refusal_cases(admitted):
    import copy
    empty = (Fraction(0), Fraction(0))
    actions = {
        "changed_bytes": lambda: verify_payload(b"changed", identity(b"original"), "controlled"),
        "wrong_length": lambda: array_identity([0.0] * (N - 1), N),
        "nonfinite": lambda: array_identity([float("nan")] + [0.0] * (N - 1), N),
        "unknown_arithmetic": lambda: arithmetic_config({"precision": 257}, admitted),
        "missing_qualification": lambda: validate_qualification(None, admitted),
        "failed_qualification": lambda: validate_qualification({**common_record(admitted), "status": "failed"}, admitted),
        "unsupported_rows": lambda: pilot((0,)),
        "unsupported_context": lambda: pilot(ROWS, N, L + 1),
        "invalid_envelope": lambda: envelope("2", "4", "hypothetical"),
        "missing_exact_toy_value": lambda: contains(empty, Fraction(1)),
        "false_nonzero": lambda: validate_row_status({"status": "proven_nonzero", "witness_index": 0,
            "witness_interval": ["-1", "1"]}, ((Fraction(-1), Fraction(1)),)),
        "overwide_interval": lambda: require_width((Fraction(-1), Fraction(1)), Fraction(1, 10**12), "controlled"),
    }
    for name in ("changed_coefficients", "changed_stage_order", "changed_padding"):
        altered = dict(admitted)
        altered["stages"] = copy.deepcopy(admitted["stages"])
        if name == "changed_coefficients":
            altered["stages"][0]["sos"][0, 0] *= 2.0
        elif name == "changed_stage_order":
            altered["stages"][1], altered["stages"][2] = altered["stages"][2], altered["stages"][1]
        else:
            altered["stages"][0]["padlen"] += 1
        actions[name] = lambda candidate=altered: check_coefficients(candidate)
    return actions


def run_qualification(admitted):
    gates = {}
    def record(identifier, work):
        try:
            detail = work()
            gates[identifier] = {"id": identifier, "passed": True, "detail": detail}
            return detail
        except (ValueError, TypeError, KeyError, ArithmeticError, RuntimeError, MemoryError) as error:
            gates[identifier] = {"id": identifier, "passed": False,
                                 "detail": {"error_type": type(error).__name__, "error": str(error)}}
            return None
    configs = admitted["oracle"].toy_configurations()
    require(tuple(c["name"] for c in configs) == TOY_NAMES, "toy declaration inventory changed")
    for config in configs:
        for central in (4, 7):
            for side in (1, 2):
                record(f"toy:{config['name']}:{central}:{side}",
                       lambda c=config, n=central, l=side: toy_case(c, n, l, admitted))
    # A failed exact-method gate cannot admit any later scientific calculation.
    if all(item["passed"] for item in gates.values()):
        references = {}
        for length in (N, T):
            for name, values in fixtures(length):
                key = (length, name)
                def forward(v=values, k=key):
                    reference, detail = forward_case(k[1], v, admitted)
                    references[k] = reference
                    return detail
                record(f"forward:{length}:{name}", forward)
        prepared = None
        try:
            prepared = admitted["engine"].prepare(admitted["fraction_stages"], admitted["padlens"])
            rows = {}
            for length in (N, T):
                for selected in (*ROWS, "dense"):
                    seed = (tuple(Fraction((-1) ** k, 16384) for k in range(length)) if selected == "dense"
                            else unit(length, selected + (L if length == T else 0)))
                    certificate = certified(seed, prepared, admitted["engine"])
                    rows[(length, selected)] = certificate
                    for name, values in fixtures(length):
                        def diagnostic(n=name, v=values, s=seed, c=certificate, m=length):
                            x = tuple(Fraction.from_float(value) for value in v)
                            ref = tuple(Fraction(value) for value in references[(m, n)])
                            left, right = dot(s, ref), dot(c["center"], x)
                            residual = abs(left - right)
                            scale = sum(map(abs, s), Fraction(0)) * max(map(abs, x))
                            threshold = max(Fraction(1), scale) / 10**9
                            require(residual <= threshold, "adjoint diagnostic failed")
                            return {"left_dot_exact": str(left), "right_dot_exact": str(right),
                                "absolute_residual_exact": str(residual), "scale_exact": str(scale),
                                "threshold_exact": str(threshold),
                                "center_identity": identity(canonical([str(value) for value in c["center"]]))}
                        record(f"adjoint:{length}:{selected}:{name}", diagnostic)
            assembled = []
            for selected in ROWS:
                def enclose(index=selected):
                    row = assemble_row(index, rows[(N, index)], rows[(T, index)], N, L)
                    require_width(row["gain"], max(Fraction(1), row["gain"][1]) / 10**12, "gain")
                    validate_row_status(row["operator_status"], row["b"])
                    centers = []
                    for name, values in fixtures(N):
                        exact = tuple(Fraction.from_float(value) for value in values)
                        bounds = context_interval(row["a"], exact)
                        require_width(bounds, max(map(abs, exact)) / 10**12, "synthetic context", name == "zeros")
                        centers.append({"fixture": name, "context_interval": encoded_interval(bounds)})
                    assembled.append(row)
                    return {"row": row_summary(row), "centers": centers}
                record(f"enclosure:{selected}", enclose)
            def constants():
                # Exact numerator-zero structure proves F_m 1=0 at any valid length.
                dc_product = Fraction(1)
                zero_numerator = False
                for stage in admitted["fraction_stages"]:
                    for b0, b1, b2, a0, a1, a2 in stage:
                        dc_product *= (b0 + b1 + b2) / (a0 + a1 + a2)
                        zero_numerator |= (b0, b1, b2) == (Fraction(1), Fraction(-2), Fraction(1))
                require(zero_numerator and dc_product == 0, "exact constant-annihilation structure absent")
                require(len(assembled) == len(ROWS), "not all structural rows certified")
                checks = []
                for row in assembled:
                    short_sum = interval_sum(row["short"]["intervals"])
                    long_sum = interval_sum(row["long"]["intervals"])
                    context_plus_extension = interval_sum((*row["a"], *row["b"]))
                    for bounds in (short_sum, long_sum, context_plus_extension):
                        contains(bounds, Fraction(0))
                    checks.append({"row": row["row"], "short_row_sum": encoded_interval(short_sum),
                                   "long_row_sum": encoded_interval(long_sum),
                                   "d_plus_B_ones": encoded_interval(context_plus_extension)})
                return {"exact_constant_output": "0", "proof": "Constant odd extension and exact DC startup remain constant; the pinned [1,-2,1] numerator annihilates them; subsequent linear stages preserve zero.", "rows": checks}
            record("structural_constant", constants)
        except (ValueError, TypeError, KeyError, ArithmeticError, RuntimeError, MemoryError) as error:
            gates["engine_failure"] = {"id": "engine_failure", "passed": False,
                                       "detail": {"error_type": type(error).__name__, "error": str(error)}}
    actions = refusal_cases(admitted)
    for name in REFUSAL_NAMES:
        def refuse(action=actions[name]):
            try:
                action()
            except (ValueError, TypeError, KeyError, ArithmeticError, RuntimeError):
                return {"refused": True}
            raise ValueError("controlled invalid request was accepted")
        record("refusal:" + name, refuse)
    check_coefficients(admitted)
    ordered = [gates.get(identifier, {"id": identifier, "passed": False,
                "detail": {"status": "not_run", "reason": "A prerequisite method or numerical gate failed."}})
               for identifier in gate_ids()]
    failed = sum(item["passed"] is not True for item in ordered)
    return {**common_record(admitted), "gates": ordered,
        "status": "all_context_gates_passed" if failed == 0 and "engine_failure" not in gates else "context_qualification_failed",
        "gate_counts": {"total": len(ordered), "passed": len(ordered) - failed, "failed": failed},
        "additional_failures": [gates["engine_failure"]] if "engine_failure" in gates else []}


def main():
    require(len(sys.argv) == 1, "check.py takes no arguments and reads no scientific inputs")
    report = run_qualification(admission())
    sys.stdout.buffer.write(export_json(report))
    return 0 if report["status"] == "all_context_gates_passed" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, TypeError, KeyError, OSError, ArithmeticError, RuntimeError, MemoryError) as error:
        print("context qualification refused: " + str(error), file=sys.stderr)
        raise SystemExit(1)
