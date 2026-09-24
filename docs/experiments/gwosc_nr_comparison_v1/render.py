"""Render the fixed RI-53 H1/reference comparison from two verified exports only."""

import argparse
from fractions import Fraction
import hashlib
import importlib.metadata
import io
import json
import math
import os
from pathlib import Path
import platform
import re
import stat
import struct
import sys
import tempfile


CROP_IDENTITY = {
    "bytes": 395470,
    "sha256": "a580481b9f6ea8dbb90242f12023817709ee7ac208d504110966f01f353592e7",
}
OBSERVED_OBJECT_SHA256 = "79cc42fd39adc57b28323f0409def8ddbe17de6b136de43a39985d08b3691770"
NR_IDENTITY = {
    "bytes": 142345,
    "sha256": "ed49c3e83f90e70ac85386f183031b7de3d3d6aa78e75a7d284e5a53a5cc0b76",
}
COEFFICIENT_SHA256 = "700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0"
RECIPE_SHA256 = "872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a"
PLACEMENT = {
    "offset_rational": "53/125", "time_origin_gps": 1126259462,
    "convention": "historical illustrative V1-to-V2 transfer; precise V2 alignment unresolved",
}
GRID = {
    "rate_hz": 4096, "source_start_gps": 1126259446,
    "source_sample_count": 131072, "source_crop": [65536, 69632],
    "sample_count": 4096, "time_origin_gps": 1126259462,
    "interval_gps": [1126259462, 1126259463], "interval_convention": "[start,end)",
    "offset_step_rational": "1/4096", "offset_last_rational": "4095/4096",
    "sample_indices": list(range(4096)),
    "source_sample_indices": list(range(65536, 69632)),
}
DETECTORS = (
    ("H1", "H-H1_LOSC_4_V2-1126259446-32.hdf5", 1040592,
     "50441a42c13fc1f14e5c4ea5527f1515",
     "6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6",
     "da67bb7ba8e4bd7638cb04872e0f52dec06531099dbf1e3db6d25f3c5db337d2"),
    ("L1", "L-L1_LOSC_4_V2-1126259446-32.hdf5", 1007420,
     "361ae6a040a9fef7897b1e0124d5b0a1",
     "56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189",
     "109d1ffec046b36e7fab31811fc6240b40f92250a47dc16c3359482869335515"),
)
NR_SUPPORT = (
    Fraction(-3102020544999999907, 5000000000000000000),
    Fraction(276885705000000093, 5000000000000000000),
)
DECIMAL_TOKEN = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def _sha(payload):
    return hashlib.sha256(payload).hexdigest()


def _expect(actual, expected, label):
    _require(_canonical(actual) == _canonical(expected), label + ": mismatch")


def _object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def _nonfinite(value):
    raise ValueError("nonfinite JSON constant: " + value)


def verified_bytes(path, identity):
    """Check one retained snapshot before parsing; caller pins do not prove origin."""
    count, digest = identity["bytes"], identity["sha256"]
    _require(type(count) is int and 0 < count <= 16 * 1024 * 1024,
             "expected byte count must be in [1,16777216]")
    _require(type(digest) is str and re.fullmatch(r"[0-9a-f]{64}", digest),
             "expected SHA-256 must be 64 lowercase hex characters")
    information = path.lstat()
    _require(stat.S_ISREG(information.st_mode), "export must be a regular file")
    _require(information.st_size == count, "export byte count mismatch")
    with path.open("rb") as stream:
        payload = stream.read(count + 1)
    _require(len(payload) == count and _sha(payload) == digest,
             "retained export identity mismatch")
    return payload


def _json(payload):
    result = json.loads(payload, object_pairs_hook=_object, parse_constant=_nonfinite)
    _require(type(result) is dict, "export must be a JSON object")
    return result


def _array(tokens, identity, count, label):
    _require(type(tokens) is list and len(tokens) == count, label + ": sample count")
    values = []
    for token in tokens:
        _require(type(token) is str, label + ": hexadecimal string required")
        value = float.fromhex(token)
        _require(math.isfinite(value) and token == value.hex(),
                 label + ": canonical finite binary64 required")
        values.append(value)
    raw = b"".join(struct.pack("<d", value) for value in values)
    _expect(identity, {"shape": [count], "dtype": "little-endian binary64",
                      "order": "C", "bytes": count * 8, "sha256": _sha(raw)}, label + " identity")
    return values


def validate_crop(crop):
    for key, expected in {
        "schema_version": "ri47-nominal-strain-crop-v1", "event": "GW150914",
        "quantity": "nominal dimensionless strain",
        "coefficient_manifest_sha256": COEFFICIENT_SHA256,
        "recipe_sha256": RECIPE_SHA256, "grid": GRID,
    }.items():
        _expect(crop.get(key), expected, "observed " + key)
    entries = crop.get("detectors")
    _require(type(entries) is list and len(entries) == 2, "two ordered detectors required")
    arrays = []
    for entry, expected in zip(entries, DETECTORS):
        name, filename, count, md5, sha256, annotations = expected
        _require(type(entry) is dict, "detector object required")
        _expect(entry.get("detector"), name, "detector order")
        _expect(entry.get("input_filename"), filename, name + " input filename")
        _expect(entry.get("input_identity"), {"bytes": count, "md5": md5, "sha256": sha256},
                name + " input identity")
        _require(_sha(_canonical(entry.get("annotations"))) == annotations,
                 name + " complete annotations mismatch")
        arrays.append(_array(entry.get("values_hex"), entry.get("crop_identity"),
                             4096, name))
    return arrays[0]


def _decimal(token):
    _require(type(token) is str and 0 < len(token) <= 128 and DECIMAL_TOKEN.fullmatch(token),
             "strict finite decimal token required")
    signed = -1 if token.startswith("-") else 1
    pieces = token.lstrip("+-").lower().split("e")
    exponent = int(pieces[1]) if len(pieces) == 2 else 0
    whole, dot, fraction = pieces[0].partition(".")
    place = exponent - len(fraction)
    _require(abs(place) <= 1152, "decimal exponent outside renderer bounds")
    return signed * int(whole + fraction) * Fraction(10) ** place


def validate_reference(reference, crop):
    _expect(reference.get("schema_version"), "ri53-nominal-nr-reference-v1", "reference schema")
    _expect(reference.get("coefficient_manifest_sha256"), COEFFICIENT_SHA256, "reference coefficients")
    _expect(reference.get("placement"), PLACEMENT, "fixed placement")
    observed = {"crop_json_identity": CROP_IDENTITY, "grid": crop["grid"], "h1": crop["detectors"][0]}
    _expect(reference.get("observed"), observed, "unchanged observed H1 export")
    _require(_sha(_canonical(observed)) == OBSERVED_OBJECT_SHA256, "accepted observed object identity")
    data = reference.get("reference")
    _require(type(data) is dict, "reference data object required")
    for key, expected in {"sample_count": 2769, "nominal_filter_rate_hz": 4096,
                          "input_identity": NR_IDENTITY}.items():
        _expect(data.get(key), expected, "reference " + key)
    rows = data.get("rows")
    _require(type(rows) is list and len(rows) == 2769, "all 2769 reference rows required")
    times, placed, inputs, filtered = [], [], [], []
    for index, row in enumerate(rows):
        _require(type(row) is dict, "reference row object required")
        _expect(row.get("index"), index, "reference index")
        _expect(row.get("line_number"), index + 1, "retained source line number")
        time, strain = _decimal(row.get("time_token")), _decimal(row.get("strain_token"))
        _expect(row.get("time_exact"), str(time), "reference exact time")
        _expect(row.get("strain_exact"), str(strain), "reference exact strain")
        coordinate = time + Fraction(53, 125)
        _expect(row.get("placed_time_exact"), str(coordinate), "exact placed time")
        _require(not times or time > times[-1], "reference times must increase")
        converted = float(row["strain_token"])
        _require(math.isfinite(converted) and row.get("input_hex") == converted.hex(),
                 "reference decimal-to-binary64 conversion mismatch")
        times.append(time)
        placed.append(coordinate)
        inputs.append(row.get("input_hex"))
        filtered.append(row.get("filtered_hex"))
    _expect([str(times[0]), str(times[-1])], [str(value) for value in NR_SUPPORT], "printed reference support")
    _array(inputs, data.get("input_array_identity"), 2769, "reference input array")
    values = _array(filtered, data.get("filtered_array_identity"), 2769, "filtered reference array")
    # Selection occurs in exact arithmetic, before either coordinate is rounded.
    selected = [index for index, coordinate in enumerate(placed) if 0 <= coordinate < 1]
    _require(bool(selected), "no supplied reference points in the display interval")
    return placed, values, selected


def _external_output(path):
    resolved = path.resolve()
    _require(resolved.parent.is_dir(), "output parent must exist")
    _require(not any((parent / ".git").exists() for parent in resolved.parents),
             "PNG output must be outside Git checkouts")
    _require(not path.exists(), "refusing to overwrite output")


def render_png(h1, placed, reference_values, selected):
    _require(platform.python_implementation() == "CPython" and platform.python_version() == "3.11.6",
             "requires CPython 3.11.6")
    versions = {"matplotlib": "3.11.1", "numpy": "2.4.6", "Pillow": "12.3.0"}
    for package, expected in versions.items():
        _require(importlib.metadata.version(package) == expected, package + " rendering version mismatch")
    visible = [reference_values[index] for index in selected]
    magnitude = max(abs(value) for value in h1 + visible)
    half_range = 1.05 * magnitude if magnitude else 1.0
    if half_range <= magnitude:
        half_range = math.nextafter(magnitude, math.inf)
    _require(math.isfinite(half_range) and half_range > magnitude, "unrepresentable unclipped amplitude limits")
    h1_times = [index / 4096 for index in range(4096)]
    reference_times = [float(placed[index]) for index in selected]
    prior = os.environ.get("MPLCONFIGDIR")
    with tempfile.TemporaryDirectory(prefix="det-ri53-render-") as configuration:
        os.environ["MPLCONFIGDIR"] = configuration
        try:
            import matplotlib
            matplotlib.use("Agg", force=True)
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            from matplotlib.figure import Figure
            from matplotlib import ft2font
            from matplotlib.ticker import ScalarFormatter
            _require(ft2font.__freetype_version__ == "2.14.3", "FreeType rendering version mismatch")
            with matplotlib.rc_context():
                matplotlib.rcdefaults()
                matplotlib.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                    "axes.unicode_minus": False, "text.usetex": False,
                    "path.simplify": False, "agg.path.chunksize": 0})
                figure = Figure(figsize=(12, 7), dpi=100, facecolor="white")
                canvas = FigureCanvasAgg(figure)
                axis = figure.subplots()
                figure.subplots_adjust(left=0.09, right=0.975, top=0.70, bottom=0.19)
                figure.suptitle("GW150914 V2 H1: illustrative NR comparison", y=0.965, fontsize=15)
                figure.text(0.5, 0.91, "Supplied SXS:BBH:0305 reference; publisher adjusted amplitude and phase using event data",
                            ha="center", fontsize=10)
                figure.text(0.5, 0.865, "Reference placement: printed time + 0.424 s (historical convention; precise V2 alignment unresolved)",
                            ha="center", fontsize=9)
                figure.text(0.5, 0.82, "Both vectors: frozen 43–260 Hz bandpass + 16 notch stages, offline forward–backward filtering",
                            ha="center", fontsize=9)
                axis.plot(h1_times, h1, color="#a52d32", linewidth=0.75,
                          label="H1 nominal observed strain (all 4096 samples)", clip_on=False)
                axis.plot(reference_times, visible, color="#202020", linewidth=1.2,
                          label="Supplied, data-informed NR reference (finite support)", clip_on=False)
                axis.set_xlim(0, 1)
                axis.set_ylim(-half_range, half_range)
                axis.set_xlabel("Seconds after GPS 1126259462")
                axis.set_ylabel("Nominal strain (dimensionless)")
                formatter = ScalarFormatter(useOffset=False, useMathText=True)
                formatter.set_powerlimits((0, 0))
                axis.yaxis.set_major_formatter(formatter)
                axis.grid(True, color="#dddddd", linewidth=0.5)
                axis.set_axisbelow(True)
                axis.axvline(reference_times[-1], color="#888888", linewidth=0.8, linestyle=":")
                axis.set_title("Visible reference samples: " + f"{reference_times[0]:.9f}–{reference_times[-1]:.9f} s; "
                               "no supplied continuation after the dotted line", fontsize=9, pad=14)
                axis.legend(loc="lower center", bbox_to_anchor=(0.5, 1.15),
                            ncol=2, frameon=False, fontsize=9)
                figure.text(0.09, 0.09, "H1 NO_CW_HW_INJ flag is set throughout the input interval.", fontsize=9)
                figure.text(0.09, 0.05, "Illustrative placement and numerical padding supply no timing, calibration or statistical agreement claim.", fontsize=9)
                buffer = io.BytesIO()
                canvas.print_png(buffer, metadata={"Software": "DET RI-53 export comparison renderer",
                    "Title": "GW150914 V2 H1 illustrative NR comparison",
                    "Description": "Unchanged H1 observations; supplied data-informed NR reference at fixed historical placement, limited to its supplied support."})
                png = buffer.getvalue()
            runtime = {"python_implementation": platform.python_implementation(),
                       "python_version": platform.python_version(), "python_build": sys.version,
                       "platform": platform.platform(), "machine": platform.machine(),
                       "byteorder": sys.byteorder, "backend": "Agg", **versions,
                       "freetype": ft2font.__freetype_version__}
        finally:
            if prior is None:
                os.environ.pop("MPLCONFIGDIR", None)
            else:
                os.environ["MPLCONFIGDIR"] = prior
    return png, runtime, [-half_range, half_range]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crop", required=True, type=Path)
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--expected-reference-bytes", required=True, type=int)
    parser.add_argument("--expected-reference-sha256", required=True)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args(argv)
    _external_output(arguments.output)
    reference_identity = {"bytes": arguments.expected_reference_bytes, "sha256": arguments.expected_reference_sha256}
    crop_bytes = verified_bytes(arguments.crop, CROP_IDENTITY)
    reference_bytes = verified_bytes(arguments.reference, reference_identity)
    crop, reference = _json(crop_bytes), _json(reference_bytes)
    h1 = validate_crop(crop)
    placed, values, selected = validate_reference(reference, crop)
    png, runtime, limits = render_png(h1, placed, values, selected)
    record = {"schema_version": "ri53-nominal-comparison-render-v1",
        "crop_json_identity": CROP_IDENTITY, "reference_json_identity": reference_identity,
        "png_identity": {"bytes": len(png), "sha256": _sha(png)},
        "renderer_identity": {"bytes": Path(__file__).stat().st_size, "sha256": _sha(Path(__file__).read_bytes())},
        "rendering_runtime": runtime, "placement": PLACEMENT,
        "display": {"pixel_dimensions": [1200, 700], "x_limits": [0, 1],
            "h1_sample_count": 4096, "h1_crop_identity": crop["detectors"][0]["crop_identity"],
            "reference_total_sample_count": len(values), "reference_visible_sample_count": len(selected),
            "reference_visible_indices": selected,
            "reference_full_placed_support": [str(placed[0]), str(placed[-1])],
            "reference_visible_sample_support": [str(placed[selected[0]]), str(placed[selected[-1]])],
            "exact_selection_rule": "0 <= Fraction(time_token) + 53/125 < 1; convert selected coordinates to binary64 only for plotting",
            "shared_y_limits_hex": [value.hex() for value in limits],
            "path_simplification": False, "numeric_value_rescaling": "none"},
        "identity_boundary": "Expected reference identity is supplied from a separately reviewed processing receipt; matching bytes alone does not authenticate provenance or filtering.",
        "scope": "Export-only illustrative H1 comparison; no filtering, resampling, interpolation, fitted shift, sign change, amplitude fit, uncertainty band, significance or native prediction."}
    output = _canonical(record) + b"\n"
    with arguments.output.open("xb") as stream:
        stream.write(png)
    sys.stdout.buffer.write(output)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, OSError, OverflowError,
            importlib.metadata.PackageNotFoundError) as error:
        print("comparison rendering refused: " + str(error), file=sys.stderr)
        raise SystemExit(1)
