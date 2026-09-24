"""Render only the fixed RI-47 crop; no strain loading or numerical filtering."""

import argparse
import hashlib
import importlib.metadata
import io
import json
import math
import os
from pathlib import Path
import platform
import struct
import sys
import tempfile


SCHEMA = "ri47-nominal-strain-crop-v1"
COEFFICIENT_SHA256 = "700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0"
RECIPE_SHA256 = "872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a"
FILES = (
    ("H1", "H-H1_LOSC_4_V2-1126259446-32.hdf5", 1040592,
     "50441a42c13fc1f14e5c4ea5527f1515",
     "6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6"),
    ("L1", "L-L1_LOSC_4_V2-1126259446-32.hdf5", 1007420,
     "361ae6a040a9fef7897b1e0124d5b0a1",
     "56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189"),
)
ANNOTATION_SHA256 = (
    "da67bb7ba8e4bd7638cb04872e0f52dec06531099dbf1e3db6d25f3c5db337d2",
    "109d1ffec046b36e7fab31811fc6240b40f92250a47dc16c3359482869335515",
)
CW_ANNOTATIONS = (
    "H1 NO_CW_HW_INJ flag is set throughout input interval.",
    "L1 NO_CW_HW_INJ flag is clear throughout input interval; samples retained. "
    "Injection absence and negligible effect are not claimed.",
)
GRID = {
    "rate_hz": 4096,
    "source_start_gps": 1126259446,
    "source_sample_count": 131072,
    "source_crop": [65536, 69632],
    "sample_count": 4096,
    "time_origin_gps": 1126259462,
    "interval_gps": [1126259462, 1126259463],
    "interval_convention": "[start,end)",
    "offset_step_rational": "1/4096",
    "offset_last_rational": "4095/4096",
    "sample_indices": list(range(4096)),
    "source_sample_indices": list(range(65536, 69632)),
}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def _sha256(payload):
    return hashlib.sha256(payload).hexdigest()


def _object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("nonfinite JSON constant: " + value)


def _expect(actual, expected, label):
    _require(_canonical(actual) == _canonical(expected), label + ": mismatch")


def load_crop(path):
    """Read one JSON snapshot and validate the fixed exported display contract."""
    payload = Path(path).read_bytes()
    _require(len(payload) <= 4 * 1024 * 1024, "crop exceeds 4 MiB")
    crop = json.loads(payload, object_pairs_hook=_object,
                      parse_constant=_invalid_constant)
    _require(type(crop) is dict, "crop must be an object")
    for key, expected in {
        "schema_version": SCHEMA,
        "event": "GW150914",
        "quantity": "nominal dimensionless strain",
        "coefficient_manifest_sha256": COEFFICIENT_SHA256,
        "recipe_sha256": RECIPE_SHA256,
    }.items():
        _expect(crop.get(key), expected, key)
    _expect(crop.get("grid"), GRID, "fixed index grid")
    detectors = crop.get("detectors")
    _require(type(detectors) is list and len(detectors) == 2,
             "exactly two ordered detectors required")
    arrays = []
    for index, (item, expected) in enumerate(zip(detectors, FILES)):
        _require(type(item) is dict, "detector must be an object")
        name, filename, size, md5, sha256 = expected
        _expect(item.get("detector"), name, "detector order")
        _expect(item.get("input_filename"), filename, name + " source filename")
        _expect(item.get("input_identity"),
                {"bytes": size, "md5": md5, "sha256": sha256},
                name + " source identity")
        annotations = item.get("annotations")
        _require(_sha256(_canonical(annotations)) == ANNOTATION_SHA256[index],
                 name + " complete quality/injection annotations: mismatch")
        _expect(annotations.get("cw_display_annotation"), CW_ANNOTATIONS[index],
                name + " CW annotation")
        tokens = item.get("values_hex")
        _require(type(tokens) is list and len(tokens) == 4096,
                 name + " requires 4096 binary64 hex samples")
        values = []
        for token in tokens:
            _require(type(token) is str, name + " sample must be a hex string")
            value = float.fromhex(token)
            _require(math.isfinite(value) and value.hex() == token,
                     name + " sample must be canonical finite float.hex")
            values.append(value)
        raw = b"".join(struct.pack("<d", value) for value in values)
        _expect(item.get("crop_identity"), {
            "shape": [4096], "dtype": "little-endian binary64", "order": "C",
            "bytes": 32768, "sha256": _sha256(raw),
        }, name + " crop byte identity")
        arrays.append(values)
    return crop, arrays, payload


def render_png(arrays):
    """Plot original sample values with an exact dyadic local-time grid."""
    _require(platform.python_implementation() == "CPython" and
             platform.python_version() == "3.11.6", "requires CPython 3.11.6")
    _require(importlib.metadata.version("matplotlib") == "3.11.1",
             "requires Matplotlib 3.11.1")
    # Keep Matplotlib's configuration/font cache outside the checkout and user cache.
    previous_config = os.environ.get("MPLCONFIGDIR")
    with tempfile.TemporaryDirectory(prefix="det-ri47-render-") as configuration:
        os.environ["MPLCONFIGDIR"] = configuration
        try:
            import matplotlib
            matplotlib.use("Agg", force=True)
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            from matplotlib.figure import Figure
            from matplotlib import ft2font
            from matplotlib.ticker import ScalarFormatter

            magnitude = max(abs(value) for values in arrays for value in values)
            half_range = magnitude * 1.05 if magnitude else 1.0
            if half_range <= magnitude:
                half_range = math.nextafter(magnitude, math.inf)
            _require(math.isfinite(half_range) and half_range > magnitude,
                     "cannot represent unclipped shared amplitude limits")
            times = [j / 4096 for j in range(4096)]
            settings = {
                "font.family": "DejaVu Sans", "font.size": 10,
                "axes.unicode_minus": False, "text.usetex": False,
                "path.simplify": False, "agg.path.chunksize": 0,
            }
            with matplotlib.rc_context(settings):
                figure = Figure(figsize=(11, 7.6), dpi=100, facecolor="white")
                canvas = FigureCanvasAgg(figure)
                axes = figure.subplots(2, 1, sharex=True, sharey=True)
                figure.subplots_adjust(left=0.095, right=0.975, top=0.82,
                                       bottom=0.105, hspace=0.62)
                figure.suptitle("GW150914 V2: nominal filtered strain", y=0.975,
                                fontsize=15)
                figure.text(0.5, 0.93,
                            "43–260 Hz bandpass + 16 notch stages; "
                            "offline forward–backward filtering",
                            ha="center", fontsize=10)
                for index, (axis, values, color) in enumerate(
                        zip(axes, arrays, ("#a52d32", "#245f9e"))):
                    axis.plot(times, values, color=color, linewidth=0.75,
                              clip_on=False)
                    axis.set_xlim(0.0, 1.0)
                    axis.set_ylim(-half_range, half_range)
                    axis.set_ylabel("Nominal strain\n(dimensionless)")
                    annotation = CW_ANNOTATIONS[index]
                    if index == 1:
                        annotation = annotation.replace("Injection absence",
                                                        "\nInjection absence")
                    axis.set_title(FILES[index][0] + "\n" + annotation,
                                   loc="left", fontsize=9, pad=10)
                    formatter = ScalarFormatter(useOffset=False, useMathText=True)
                    formatter.set_powerlimits((0, 0))
                    axis.yaxis.set_major_formatter(formatter)
                    axis.grid(True, color="#dddddd", linewidth=0.5)
                    axis.set_axisbelow(True)
                axes[-1].set_xlabel("Seconds after GPS 1126259462")
                buffer = io.BytesIO()
                canvas.print_png(buffer, metadata={
                    "Software": "DET RI-47 nominal crop renderer",
                    "Title": "GW150914 V2 nominal filtered strain",
                    "Description": "Two unshifted detector panels on one strain scale; "
                    "4096 original crop samples per panel. L1 NO_CW_HW_INJ is clear.",
                })
                png = buffer.getvalue()
            runtime = {
                "python_implementation": platform.python_implementation(),
                "python_version": platform.python_version(),
                "python_build": sys.version,
                "platform": platform.platform(), "machine": platform.machine(),
                "byteorder": sys.byteorder, "matplotlib": matplotlib.__version__,
                "numpy": importlib.metadata.version("numpy"),
                "Pillow": importlib.metadata.version("Pillow"),
                "freetype": ft2font.__freetype_version__, "backend": "Agg",
            }
        finally:
            if previous_config is None:
                os.environ.pop("MPLCONFIGDIR", None)
            else:
                os.environ["MPLCONFIGDIR"] = previous_config
    return png, runtime, [-half_range, half_range]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crop", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    _require(not arguments.output.exists(), "refusing to overwrite output")
    crop, arrays, payload = load_crop(arguments.crop)
    png, runtime, limits = render_png(arrays)
    report = {
        "schema_version": "ri47-nominal-render-record-v1",
        "crop_json_identity": {"bytes": len(payload), "sha256": _sha256(payload)},
        "png_identity": {"bytes": len(png), "sha256": _sha256(png)},
        "renderer_sha256": _sha256(Path(__file__).read_bytes()),
        "rendering_runtime": runtime,
        "display": {"panels": ["H1", "L1"], "sample_count_per_panel": 4096,
                    "pixel_dimensions": [1100, 760], "time_origin_gps": 1126259462,
                    "time_step_rational": "1/4096", "x_limits": [0, 1],
                    "shared_y_limits_hex": [value.hex() for value in limits],
                    "value_rescaling": "none", "path_simplification": False,
                    "cw_annotations": list(CW_ANNOTATIONS)},
        "plotted_crop_identities": [item["crop_identity"] for item in crop["detectors"]],
        "scope": "Crop rendering only; no HDF5 read, filtering, alignment, fitting, "
                 "uncertainty band, detection result or native prediction.",
    }
    output_json = _canonical(report) + b"\n"
    with arguments.output.open("xb") as stream:
        stream.write(png)
    sys.stdout.buffer.write(output_json)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, OSError, OverflowError,
            importlib.metadata.PackageNotFoundError) as error:
        print("render error: " + str(error), file=sys.stderr)
        raise SystemExit(1)
