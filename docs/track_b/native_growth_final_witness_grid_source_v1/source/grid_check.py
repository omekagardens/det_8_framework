#!/usr/bin/env python3
"""RI159 source-only grid-checker proposal; no execution is claimed.

Production has no input-path or pin override. It authenticates the complete
historical files before decoding the certificate and rechecks all six files
before emitting a result. Original graph/order/law verification is inherited,
not repeated. Pure decode/reconstruct functions are untrusted-input boundaries
for separately authorized future controls, never production acceptance.
"""

from fractions import Fraction
import hashlib
import json
import os
import re
import stat
import sys


CERTIFICATE_LIMIT = 65536
RESULT_LIMIT = 262144
REFUSAL_LIMIT = 8192
CERTIFICATE_DEPTH = 8
RATIONAL_DIGITS = 64
INTEGER_DIGITS = 10
COMPONENTS = 109
GRID = 1000

# Fixed production identities. No current-file self pin or operational path is
# supplied by this module; the sealed-source/interpreter bootstrap is external.
FIXED_IDENTITIES = (
    ("certificate",
     "/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/CERTIFICATE.json",
     2845, "3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969"),
    ("original_source",
     "/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/check.py",
     13219, "f33a2345608867138f1036da6a020beb6608e3f58fc3032ceb1d3c3d5c9f90c5"),
    ("original_manuscript",
     "/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md",
     16243, "567596a17c69e20b33328b2d0c39f22d98a78f7d25d81949fd57cd07df5e53c8"),
    ("assignment",
     "/Volumes/AI_DATA/development/det-review-evidence/ri157-root-adjudication-q_wj4pny/NATIVE_SUCCESSOR_ASSIGNMENT.json",
     4916, "782b057624a35094093558e52e40a78d3a61b3ff1cbb61d2c3dd675171b1911e"),
    ("accepted_predecessor",
     "/Volumes/AI_DATA/development/det-review-evidence/ri157-root-adjudication-q_wj4pny/RI157_ROOT_ADJUDICATION.json",
     2404, "d052d2c1f51691a861792690a89d8175755c8bffd5016a81b892c8d7abd76950"),
    ("accepted_manual_review",
     "/Volumes/AI_DATA/development/det-review-evidence/ri157-root-adjudication-q_wj4pny/ROOT_MANUAL_REVIEW.md",
     4362, "3040fadd824a82b8aee1c51338719ff79da7a3eb0d1c56ce9c1816588dba2b05"),
)


class GridRefused(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def require(condition, code, message):
    if not condition:
        raise GridRefused(code, message)


def duplicate_free(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, "JSON_DUPLICATE_KEY", "duplicate JSON object key")
        value[key] = item
    return value


def bounded_integer(token):
    digits = token[1:] if token.startswith("-") else token
    require(len(digits) <= INTEGER_DIGITS,
            "JSON_INTEGER", "JSON integer exceeds ten digits")
    return int(token)


def forbidden_number(token):
    raise GridRefused("JSON_NUMBER", "floating or nonfinite JSON number is forbidden")


def decode_certificate(raw):
    """Decode only; this pure function does not authenticate historical bytes."""
    require(type(raw) is bytes and 0 < len(raw) <= CERTIFICATE_LIMIT,
            "CERTIFICATE_BYTES", "certificate must be nonempty bounded bytes")
    depth = 0
    quoted = False
    escaped = False
    for byte in raw:
        if quoted:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (91, 123):
            depth += 1
            require(depth <= CERTIFICATE_DEPTH,
                    "JSON_DEPTH", "certificate JSON nesting exceeds eight")
        elif byte in (93, 125):
            depth -= 1
            require(depth >= 0, "JSON_SYNTAX", "unbalanced certificate JSON")
    require(depth == 0 and not quoted,
            "JSON_SYNTAX", "unbalanced certificate JSON")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=duplicate_free,
                          parse_int=bounded_integer, parse_float=forbidden_number,
                          parse_constant=forbidden_number)
    except (UnicodeError, json.JSONDecodeError, RecursionError):
        raise GridRefused("JSON_SYNTAX", "invalid certificate UTF-8 JSON") from None


def exact_positive(value):
    require(type(value) is str, "RATIONAL_TYPE", "coefficient must be a string")
    require(0 < len(value) <= 2 * RATIONAL_DIGITS + 1,
            "RATIONAL_LENGTH", "coefficient string exceeds the rational bound")
    require(re.fullmatch(r"[0-9]+(?:/[0-9]+)?", value) is not None,
            "RATIONAL_SYNTAX", "coefficient must use ASCII digits and optional slash")
    terms = value.split("/")
    require(all(len(term) <= RATIONAL_DIGITS for term in terms),
            "RATIONAL_LENGTH", "rational term exceeds sixty-four digits")
    numerator = int(terms[0])
    denominator = int(terms[1]) if len(terms) == 2 else 1
    require(numerator > 0 and denominator > 0,
            "RATIONAL_POSITIVITY", "coefficient numerator and denominator must be positive")
    return Fraction(numerator, denominator)


def rational_fields(alpha):
    scaled = GRID * alpha
    return {
        "alpha": str(alpha.numerator) + "/" + str(alpha.denominator),
        "scaled_numerator": str(scaled.numerator),
        "scaled_denominator": str(scaled.denominator),
        "on_grid": scaled.denominator == 1,
    }


def reconstruct_certificate(data):
    """Pure mathematical payload only: fabricated arguments are not history.

    Root checks are bounded shape/order checks. They do not rebuild the ratio
    graph or establish that supplied roots are the actual RI41 components.
    Production supplies that linkage only through fixed complete byte pins.
    """
    keys = {"schema", "seed", "parent_size", "potential", "component_order",
            "roots", "default_alpha", "overrides"}
    require(type(data) is dict and set(data) == keys,
            "CERTIFICATE_KEYS", "certificate requires exactly eight declared fields")
    labels = {
        "schema": "ri41-height-primal-v1",
        "seed": "interior_a",
        "potential": "RI-38 maximal-deletion",
        "component_order": "increasing minimum canonical-local-key",
    }
    for key, expected in labels.items():
        require(type(data[key]) is str and data[key] == expected,
                "CERTIFICATE_DOMAIN", "certificate domain label changed: " + key)
    require(type(data["parent_size"]) is int and data["parent_size"] == 4,
            "CERTIFICATE_DOMAIN", "certificate parent_size must be integer four")
    roots = data["roots"]
    require(type(roots) is list and len(roots) == COMPONENTS,
            "ROOT_COUNT", "certificate requires exactly 109 roots")
    previous = None
    for root in roots:
        require(type(root) is list and len(root) == 3 and
                all(type(item) is int for item in root),
                "ROOT_SHAPE", "root must be a triple of strict integers")
        require(0 <= root[0] <= 65535 and 0 <= root[1] <= 15 and
                0 <= root[2] <= 15 and root[2] & ~root[1] == 0,
                "ROOT_MASK", "root integer or record mask is outside the declared shape")
        current = tuple(root)
        require(previous is None or previous < current,
                "ROOT_ORDER", "root triples must be strictly increasing and unique")
        previous = current
    default = exact_positive(data["default_alpha"])
    overrides = data["overrides"]
    require(type(overrides) is dict and len(overrides) <= COMPONENTS,
            "OVERRIDE_SHAPE", "overrides must be an object of at most 109 entries")
    resolved = [default] * COMPONENTS
    overridden = set()
    for label, value in overrides.items():
        require(type(label) is str and
                re.fullmatch(r"0|[1-9][0-9]{0,2}", label) is not None,
                "OVERRIDE_INDEX", "override index must be a canonical decimal label")
        index = int(label)
        require(0 <= index < COMPONENTS,
                "OVERRIDE_INDEX", "override index is outside zero through 108")
        resolved[index] = exact_positive(value)
        overridden.add(index)
    components = []
    off_grid = []
    for index, alpha in enumerate(resolved):
        fields = rational_fields(alpha)
        if not fields["on_grid"]:
            off_grid.append(index)
        components.append({"index": index, "root": list(roots[index]),
                           "origin": "override" if index in overridden else "default",
                           **fields})
    domain = {**labels, "parent_size": 4,
              "component_count": COMPONENTS, "grid_denominator": GRID}
    return {
        "status": "GRID_FAIL" if off_grid else "GRID_PASS",
        "domain": domain,
        "default": rational_fields(default),
        "override_indices": sorted(overridden),
        "components": components,
        "counts": {"components": COMPONENTS,
                   "defaulted": COMPONENTS - len(overridden),
                   "overridden": len(overridden),
                   "on_grid": COMPONENTS - len(off_grid),
                   "off_grid": len(off_grid)},
        "off_grid_indices": off_grid,
    }


def stat_key(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_uid, info.st_gid, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns)


def validate_fixed_path(path, role):
    require(type(path) is str and 0 < len(path) <= 4096 and "\x00" not in path
            and os.path.isabs(path) and os.path.normpath(path) == path
            and os.path.realpath(path) == path,
            "IDENTITY_PATH", "fixed input path is not normalized and nonsymlink: " + role)
    parts = path.split("/")[1:]
    require(0 < len(parts) <= 256 and all(parts),
            "IDENTITY_PATH", "fixed input path exceeds its component bound: " + role)
    current = ""
    for position, part in enumerate(parts):
        current += "/" + part
        observed = os.lstat(current)
        if position + 1 < len(parts):
            require(stat.S_ISDIR(observed.st_mode),
                    "IDENTITY_ANCESTOR", "fixed input ancestor is not a nonsymlink directory: " + role)
        else:
            require(stat.S_ISREG(observed.st_mode),
                    "IDENTITY_TYPE", "fixed input is not a nonsymlink regular file: " + role)
    require(os.path.realpath(path) == path,
            "IDENTITY_PATH", "fixed input path changed during validation: " + role)
    return observed


def failure_text(error):
    if isinstance(error, GridRefused):
        return error.code + ":" + str(error)
    return type(error).__name__


def read_fixed(identity):
    role, path, size, digest = identity
    descriptor = None
    primary = None
    close_error = None
    raw = None
    try:
        require(hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_NONBLOCK"),
                "IDENTITY_HOST", "host must provide O_NOFOLLOW and O_NONBLOCK")
        before_path = validate_fixed_path(path, role)
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode) and
                stat_key(before_path) == stat_key(before) and before.st_size == size,
                "IDENTITY_METADATA", "fixed input identity or length changed: " + role)
        chunks = []
        remaining = size + 1
        while remaining:
            chunk = os.read(descriptor, remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        after_path = validate_fixed_path(path, role)
        require(stat_key(before) == stat_key(after) == stat_key(after_path),
                "IDENTITY_METADATA", "fixed input changed during reading: " + role)
        require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest,
                "IDENTITY_BYTES", "fixed input complete byte pin changed: " + role)
    except OSError:
        primary = GridRefused("IDENTITY_IO", "fixed input could not be read: " + role)
    except Exception as error:
        primary = error
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except Exception as error:
                close_error = error
    if primary is not None:
        if close_error is not None:
            raise GridRefused("IDENTITY_PRIMARY_AND_CLOSE",
                              "primary=" + failure_text(primary) +
                              "; close=" + failure_text(close_error)) from primary
        raise primary
    if close_error is not None:
        raise GridRefused("IDENTITY_CLOSE",
                          "fixed input close failed: " + role + ":" +
                          failure_text(close_error)) from close_error
    return raw


def production_result():
    """Fixed-path production only; complete current-source trust is external."""
    authenticated = {}
    for identity in FIXED_IDENTITIES:
        authenticated[identity[0]] = read_fixed(identity)
    primary = None
    payload = None
    try:
        payload = reconstruct_certificate(decode_certificate(authenticated["certificate"]))
    except Exception as error:
        primary = error
    postcheck_errors = []
    for identity in FIXED_IDENTITIES:
        try:
            read_fixed(identity)
        except Exception as error:
            postcheck_errors.append(identity[0] + ":" + failure_text(error))
    if primary is not None:
        if postcheck_errors:
            raise GridRefused("PRIMARY_AND_POSTCHECK",
                              "primary=" + failure_text(primary) +
                              "; postchecks=" + ",".join(postcheck_errors)) from primary
        raise primary
    require(not postcheck_errors, "POSTCHECK", ",".join(postcheck_errors))
    inputs = {role: {"path": path, "bytes": size, "sha256": digest}
              for role, path, size, digest in FIXED_IDENTITIES}
    return {
        "schema": "ri159-final-witness-grid-result-v1",
        **payload,
        "inputs": inputs,
        "root_order_basis": "INHERITED_PINNED_RI41_ACCEPTANCE_NOT_RECONSTRUCTED",
        "scope": "GRID_ONLY_NOT_LAW_CAPACITY_W_H30_OR_PHYSICAL_ACCEPTANCE",
    }


def main():
    try:
        require(not sys.argv[1:], "ARGUMENTS", "grid checker accepts no arguments")
        result = production_result()
        output = (json.dumps(result, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")
        require(len(output) <= RESULT_LIMIT, "OUTPUT_BOUND", "grid result exceeds 256 KiB")
        written = sys.stdout.buffer.write(output)
        require(type(written) is int and written == len(output),
                "OUTPUT_WRITE", "grid result write was incomplete")
        sys.stdout.buffer.flush()
        return 0
    except Exception as error:
        refusal = {"schema": "ri159-grid-check-refusal-v1", "status": "REFUSED",
                   "code": error.code if isinstance(error, GridRefused) else "UNEXPECTED",
                   "message": str(error) if isinstance(error, GridRefused)
                   else "unexpected operational failure: " + type(error).__name__}
        output = (json.dumps(refusal, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")
        if len(output) > REFUSAL_LIMIT:
            output = b'{"schema":"ri159-grid-check-refusal-v1","status":"REFUSED","code":"REFUSAL_BOUND","message":"refusal exceeds 8 KiB"}\n'
        try:
            sys.stderr.buffer.write(output)
            sys.stderr.buffer.flush()
        except Exception:
            pass  # Refusal remains nonzero; durable diagnostics are external.
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
