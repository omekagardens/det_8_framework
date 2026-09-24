"""Fixed RI-42 filter design, numerical application and coefficient identities.

This module does not read strain, fetch inputs, plot, write files or certify
its candidates. Independent synthetic qualification must precede observed use.
"""

import hashlib
import math
import os
import sys

import h5py
import numpy as np
import scipy
from scipy import signal


_FS = 4096.0
_NOTCHES = (
    (14.0, 1.0, 0.1), (34.70, 1.0, 0.1), (35.30, 1.0, 0.1),
    (35.90, 1.0, 0.1), (36.70, 1.0, 0.1), (37.30, 1.0, 0.1),
    (40.95, 1.0, 0.1), (60.0, 1.0, 0.1), (120.0, 1.0, 0.1),
    (179.99, 1.0, 0.1), (304.99, 1.0, 0.1), (331.49, 1.0, 0.1),
    (510.02, 1.0, 0.1), (1009.99, 1.0, 0.1),
    (510.0, 200.0, 20.0), (331.5, 10.0, 1.0),
)
_STAGE_KEYS = {"index", "spec", "sos", "padlen", "z", "p", "k"}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _check_runtime():
    _require(sys.implementation.name == "cpython" and
             sys.version_info[:3] == (3, 11, 6), "RI-42 requires CPython 3.11.6")
    for package, actual, expected in (
        ("NumPy", np.__version__, "2.1.3"),
        ("SciPy", scipy.__version__, "1.14.1"),
        ("h5py", h5py.__version__, "3.12.1"),
    ):
        _require(actual == expected, f"RI-42 requires {package} {expected}; found {actual}")
    _require(not os.environ.get("SCIPY_ARRAY_API"),
             "RI-42 does not admit an optional SciPy array backend")
    _require(sys.float_info.radix == 2 and sys.float_info.mant_dig == 53 and
             np.dtype(np.float64).itemsize == 8, "RI-42 requires IEEE binary64")


def _specifications():
    specifications = [{
        "function": "butter", "N": 4, "Wn": [43.0, 260.0],
        "btype": "bandpass", "analog": False, "fs": _FS,
    }]
    for center, pass_width, stop_width in _NOTCHES:
        specifications.append({
            "function": "iirdesign",
            "wp": [center - pass_width, center + pass_width],
            "ws": [center - stop_width, center + stop_width],
            "gpass": 1.0, "gstop": 6.0, "analog": False,
            "ftype": "ellip", "fs": _FS,
        })
    return specifications


def _padding_length(sos):
    numerator_zeros = int(np.count_nonzero(sos[:, 2] == 0.0))
    denominator_zeros = int(np.count_nonzero(sos[:, 5] == 0.0))
    return 3 * (2 * len(sos) + 1 - min(numerator_zeros, denominator_zeros))


def _validate_stages(stages):
    _require(type(stages) is list and len(stages) == 17, "expected all 17 ordered stages")
    for index, (stage, expected_spec) in enumerate(zip(stages, _specifications())):
        label = f"stage {index}"
        _require(type(stage) is dict and set(stage) == _STAGE_KEYS,
                 f"{label}: unexpected stage fields")
        _require(type(stage["index"]) is int and stage["index"] == index,
                 f"{label}: stage order mismatch")
        _require(type(stage["spec"]) is dict and stage["spec"] == expected_spec,
                 f"{label}: specification differs from RI-42")
        sos = stage["sos"]
        _require(type(sos) is np.ndarray and sos.dtype == np.dtype(np.float64),
                 f"{label}: SOS must be a NumPy float64 array")
        _require(sos.ndim == 2 and sos.shape[0] > 0 and sos.shape[1] == 6,
                 f"{label}: invalid SOS shape")
        _require(bool(np.isfinite(sos).all()), f"{label}: nonfinite coefficient")
        _require(bool((sos[:, 3] == 1.0).all()), f"{label}: a0 must equal one")
        if index == 0:
            _require(sos.shape == (4, 6), "bandpass must contain four SOS sections")
        dc_denominators = sos[:, 3] + sos[:, 4] + sos[:, 5]
        _require(bool((dc_denominators != 0.0).all()), f"{label}: zero DC denominator")
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            try:
                dc_gains = (sos[:, 0] + sos[:, 1] + sos[:, 2]) / dc_denominators
            except FloatingPointError as error:
                raise ValueError(f"{label}: invalid DC gain") from error
        _require(bool(np.isfinite(dc_gains).all()), f"{label}: nonfinite DC gain")
        for section in sos:
            poles = np.roots(section[3:])
            _require(bool(np.isfinite(poles).all()) and bool((np.abs(poles) < 1.0).all()),
                     f"{label}: SOS pole is not strictly stable")
        for field in ("z", "p"):
            values = stage[field]
            _require(type(values) is np.ndarray and values.dtype == np.dtype(np.complex128)
                     and values.ndim == 1 and len(values) == 2 * len(sos),
                     f"{label}: invalid {field} array")
            _require(bool(np.isfinite(values).all()), f"{label}: nonfinite {field}")
        _require(bool((np.abs(stage["p"]) < 1.0).all()),
                 f"{label}: ZPK pole is not strictly stable")
        _require(type(stage["k"]) is float and math.isfinite(stage["k"]),
                 f"{label}: invalid ZPK gain")
        _require(type(stage["padlen"]) is int and
                 stage["padlen"] == _padding_length(sos),
                 f"{label}: padding differs from RI-42")


def design_stages():
    """Return candidate stages from separate SOS and ZPK design calls.

    Stage dictionaries contain index, spec, sos, padlen, z, p and k. A spec
    is a flat JSON object: the function name plus its fixed keyword inputs.
    Validation here does not replace the independent RI-42 numerical gates.
    """
    _check_runtime()
    stages = []
    for index, spec in enumerate(_specifications()):
        keywords = {name: value for name, value in spec.items() if name != "function"}
        designer = signal.butter if spec["function"] == "butter" else signal.iirdesign
        sos = np.array(designer(output="sos", **keywords), dtype=np.float64,
                       copy=True, order="C")
        z, p, k = designer(output="zpk", **keywords)
        stages.append({
            "index": index, "spec": spec, "sos": sos,
            "padlen": _padding_length(sos),
            "z": np.array(z, dtype=np.complex128, copy=True),
            "p": np.array(p, dtype=np.complex128, copy=True), "k": float(k),
        })
    _validate_stages(stages)
    return stages


def apply_filter(samples, stages):
    """Filter one finite NumPy float64 vector; return a new independent array.

    The caller must use the qualified coefficient manifest before observed
    processing. This function neither loads samples nor establishes admission.
    It performs no detrending, tapering, cropping, scaling, shifting or fitting.
    """
    _check_runtime()
    _validate_stages(stages)
    _require(type(samples) is np.ndarray and samples.dtype == np.dtype(np.float64),
             "samples must be a NumPy float64 array")
    _require(samples.ndim == 1, "samples must be one-dimensional")
    _require(bool(np.isfinite(samples).all()), "samples contain nonfinite values")
    for stage in stages:
        _require(stage["padlen"] < len(samples) - 1,
                 f"stage {stage['index']}: input is too short for frozen padding")
    output = samples.copy(order="C")
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        for stage in stages:
            try:
                output = signal.sosfiltfilt(stage["sos"], output, axis=-1,
                                           padtype="odd", padlen=stage["padlen"])
            except FloatingPointError as error:
                raise ValueError(f"stage {stage['index']}: filtering arithmetic failed") from error
            _require(output.shape == samples.shape and output.dtype == np.dtype(np.float64),
                     f"stage {stage['index']}: output shape/dtype changed")
            _require(bool(np.isfinite(output).all()),
                     f"stage {stage['index']}: nonfinite output")
    return np.array(output, dtype=np.float64, copy=True, order="C")


def coefficient_manifest(stages):
    """Return coefficient identity data; the caller hashes canonical ASCII JSON.

    The manifest is an ordered design identity, not a qualification result.
    Hex strings and C-order little-endian matrix hashes preserve signed zeros.
    """
    _check_runtime()
    _validate_stages(stages)
    entries = []
    for stage, specification in zip(stages, _specifications()):
        sos = stage["sos"]
        matrix_bytes = np.asarray(sos, dtype="<f8", order="C").tobytes(order="C")
        entries.append({
            "index": stage["index"], "spec": specification,
            "shape": list(sos.shape),
            "coefficient_hex": [[float(value).hex() for value in row] for row in sos],
            "matrix_sha256": hashlib.sha256(matrix_bytes).hexdigest(),
            "padlen": stage["padlen"],
        })
    return {"schema_version": "gwosc-nominal-sos-coefficients-v1", "stages": entries}
