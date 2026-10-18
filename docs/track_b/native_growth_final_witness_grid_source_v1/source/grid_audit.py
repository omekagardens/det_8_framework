#!/usr/bin/env python3
"""RI159: independent, bounded saved-result audit of the fixed final vector.

Source preparation only; saving this file does not execute or admit an audit.
The future CLI accepts one absolute saved-result path, authenticates six fixed
files before decoding the scientific certificate, independently reconstructs
all 109 coefficients, compares every result field with exact types, and rereads
all inputs before emitting a verdict. It imports neither grid_check.py nor the
original RI41 checker, and performs no graph or growth-law reconstruction.

audit_arguments is a direct argument boundary for separately authorized future
synthetic controls. Its verdict explicitly does not authenticate those arguments
as original files. There is no CLI bypass of the fixed pins. A MATCH verdict can
confirm a correctly reported GRID_FAIL; it is not a grid pass or law acceptance.
File rereads are point-in-time checks, not continuous custody or admission.
"""

import hashlib
import json
import os
import stat
import sys


CERTIFICATE_LIMIT = 64 * 1024
RESULT_LIMIT = 256 * 1024
CERTIFICATE_DEPTH = 8
RESULT_DEPTH = 12
RATIONAL_DIGITS = 64
JSON_INTEGER_DIGITS = 10
COMPONENTS = 109
GRID = 1000
ROOT_BASIS = "INHERITED_PINNED_RI41_ACCEPTANCE_NOT_RECONSTRUCTED"
RESULT_SCOPE = "GRID_ONLY_NOT_LAW_CAPACITY_W_H30_OR_PHYSICAL_ACCEPTANCE"
RESULT_SCHEMA = "ri159-final-witness-grid-result-v1"

PINNED_FILES = {
    "certificate": {
        "path": "/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/CERTIFICATE.json",
        "bytes": 2845,
        "sha256": "3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969",
    },
    "original_source": {
        "path": "/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/check.py",
        "bytes": 13219,
        "sha256": "f33a2345608867138f1036da6a020beb6608e3f58fc3032ceb1d3c3d5c9f90c5",
    },
    "original_manuscript": {
        "path": "/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md",
        "bytes": 16243,
        "sha256": "567596a17c69e20b33328b2d0c39f22d98a78f7d25d81949fd57cd07df5e53c8",
    },
    "assignment": {
        "path": "/Volumes/AI_DATA/development/det-review-evidence/ri157-root-adjudication-q_wj4pny/NATIVE_SUCCESSOR_ASSIGNMENT.json",
        "bytes": 4916,
        "sha256": "782b057624a35094093558e52e40a78d3a61b3ff1cbb61d2c3dd675171b1911e",
    },
    "accepted_predecessor": {
        "path": "/Volumes/AI_DATA/development/det-review-evidence/ri157-root-adjudication-q_wj4pny/RI157_ROOT_ADJUDICATION.json",
        "bytes": 2404,
        "sha256": "d052d2c1f51691a861792690a89d8175755c8bffd5016a81b892c8d7abd76950",
    },
    "accepted_manual_review": {
        "path": "/Volumes/AI_DATA/development/det-review-evidence/ri157-root-adjudication-q_wj4pny/ROOT_MANUAL_REVIEW.md",
        "bytes": 4362,
        "sha256": "3040fadd824a82b8aee1c51338719ff79da7a3eb0d1c56ce9c1816588dba2b05",
    },
}

DOMAIN_LABELS = {
    "schema": "ri41-height-primal-v1",
    "seed": "interior_a",
    "parent_size": 4,
    "potential": "RI-38 maximal-deletion",
    "component_order": "increasing minimum canonical-local-key",
}
CERTIFICATE_KEYS = frozenset(DOMAIN_LABELS) | {
    "roots", "default_alpha", "overrides"
}


class AuditRefusal(Exception):
    """Bounded exact refusal code/message, without untrusted input excerpts."""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.later_errors = []
        super().__init__(message)


def refuse(code, message):
    raise AuditRefusal(code, message)


def require(condition, code, message):
    if not condition:
        refuse(code, message)


def _bounded_json(raw, byte_limit, depth_limit):
    require(type(raw) is bytes, "AUDIT_ARGUMENT_TYPE", "JSON input must be bytes")
    require(0 < len(raw) <= byte_limit, "AUDIT_INPUT_SIZE", "JSON byte limit violated")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        refuse("AUDIT_UTF8", "JSON input is not strict UTF-8")

    # Bound nesting before the standard decoder can allocate recursive objects.
    # Braces in strings are ignored; the decoder subsequently checks grammar.
    quoted = False
    escaped = False
    stack = []
    for character in text:
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
        elif character == '"':
            quoted = True
        elif character in "[{":
            stack.append(character)
            require(len(stack) <= depth_limit, "AUDIT_JSON_DEPTH", "JSON nesting limit violated")
        elif character in "]}":
            require(bool(stack), "AUDIT_JSON_SYNTAX", "JSON delimiters are unbalanced")
            opening = stack.pop()
            require((opening, character) in (("[", "]"), ("{", "}")),
                    "AUDIT_JSON_SYNTAX", "JSON delimiters are mismatched")
    require(not quoted and not stack, "AUDIT_JSON_SYNTAX", "JSON input is incomplete")

    def integer(token):
        digits = token[1:] if token.startswith("-") else token
        require(len(digits) <= JSON_INTEGER_DIGITS,
                "AUDIT_JSON_INTEGER", "JSON integer token exceeds ten digits")
        return int(token)

    def float_forbidden(_token):
        refuse("AUDIT_JSON_FLOAT", "JSON floating-point numbers are forbidden")

    def constant_forbidden(_token):
        refuse("AUDIT_JSON_CONSTANT", "JSON nonfinite constants are forbidden")

    def object_without_duplicates(pairs):
        output = {}
        for key, value in pairs:
            require(key not in output, "AUDIT_JSON_DUPLICATE_KEY", "duplicate JSON object key")
            output[key] = value
        return output

    try:
        return json.loads(text, parse_int=integer, parse_float=float_forbidden,
                          parse_constant=constant_forbidden,
                          object_pairs_hook=object_without_duplicates)
    except (json.JSONDecodeError, RecursionError):
        refuse("AUDIT_JSON_SYNTAX", "JSON input has invalid syntax")


def _integer_gcd(left, right):
    while right:
        left, right = right, left % right
    return left


def _rational_fields(value):
    require(type(value) is str, "AUDIT_RATIONAL_TYPE", "coefficient must be a rational string")
    require(0 < len(value) <= 2 * RATIONAL_DIGITS + 1,
            "AUDIT_RATIONAL_SIZE", "rational string exceeds its bound")
    pieces = value.split("/")
    require(len(pieces) in (1, 2), "AUDIT_RATIONAL_SYNTAX", "rational requires an integer or N/D")
    if len(pieces) == 1:
        pieces.append("1")
    terms = []
    for piece in pieces:
        require(0 < len(piece) <= RATIONAL_DIGITS,
                "AUDIT_RATIONAL_SIZE", "rational term requires one to 64 digits")
        require(all(character in "0123456789" for character in piece),
                "AUDIT_RATIONAL_SYNTAX", "rational terms require ASCII decimal digits")
        number = int(piece)
        require(number > 0, "AUDIT_RATIONAL_NONPOSITIVE", "rational terms must be positive")
        terms.append(number)
    numerator, denominator = terms
    divisor = _integer_gcd(numerator, denominator)
    numerator //= divisor
    denominator //= divisor
    product = GRID * numerator
    scaled_divisor = _integer_gcd(product, denominator)
    scaled_numerator = product // scaled_divisor
    scaled_denominator = denominator // scaled_divisor
    return {
        "alpha": str(numerator) + "/" + str(denominator),
        "scaled_numerator": str(scaled_numerator),
        "scaled_denominator": str(scaled_denominator),
        "on_grid": scaled_denominator == 1,
    }


def reconstruct_certificate(certificate_raw):
    """Pure direct boundary: resolve all109; no fixed-file authenticity claim."""
    data = _bounded_json(certificate_raw, CERTIFICATE_LIMIT, CERTIFICATE_DEPTH)
    require(type(data) is dict and set(data) == CERTIFICATE_KEYS,
            "AUDIT_CERTIFICATE_FIELDS", "certificate must have exactly the eight declared fields")
    for name, expected in DOMAIN_LABELS.items():
        require(type(data[name]) is type(expected) and data[name] == expected,
                "AUDIT_CERTIFICATE_DOMAIN", "certificate domain label differs")

    roots = data["roots"]
    require(type(roots) is list and len(roots) == COMPONENTS,
            "AUDIT_ROOT_COUNT", "certificate requires exactly 109 root triples")
    previous = None
    for root in roots:
        require(type(root) is list and len(root) == 3,
                "AUDIT_ROOT_SHAPE", "each root must be a three-integer array")
        require(all(type(number) is int for number in root),
                "AUDIT_ROOT_SHAPE", "root entries must be integers, not booleans")
        relation, precursor, marks = root
        require(0 <= relation <= 65535 and 0 <= precursor <= 15 and 0 <= marks <= 15,
                "AUDIT_ROOT_BOUNDS", "root entry is outside its four-carrier bounds")
        require(marks & ~precursor == 0,
                "AUDIT_ROOT_MARKS", "root marks are not a subset of the precursor")
        current = tuple(root)
        require(previous is None or previous < current,
                "AUDIT_ROOT_ORDER_SHAPE", "root triples must be strictly lexicographically increasing")
        previous = current
    # Shape/sort checks do not prove these are the actual graph's component roots.
    # That linkage is inherited only in the fixed-pin production wrapper below.

    default_fields = _rational_fields(data["default_alpha"])
    overrides = data["overrides"]
    require(type(overrides) is dict and len(overrides) <= COMPONENTS,
            "AUDIT_OVERRIDES_TYPE", "overrides must be a bounded index object")
    resolved = {}
    for key, raw_value in overrides.items():
        require(type(key) is str and 0 < len(key) <= 3
                and all(character in "0123456789" for character in key),
                "AUDIT_OVERRIDE_LABEL", "override label must be a canonical decimal index")
        index = int(key)
        require(str(index) == key and 0 <= index < COMPONENTS,
                "AUDIT_OVERRIDE_LABEL", "override label must be a canonical index from zero to 108")
        resolved[index] = _rational_fields(raw_value)

    entries = []
    off_grid = []
    for index in range(COMPONENTS):
        is_override = index in resolved
        arithmetic = resolved[index] if is_override else default_fields
        entry = {
            "index": index,
            "root": list(roots[index]),
            "origin": "override" if is_override else "default",
            "alpha": arithmetic["alpha"],
            "scaled_numerator": arithmetic["scaled_numerator"],
            "scaled_denominator": arithmetic["scaled_denominator"],
            "on_grid": arithmetic["on_grid"],
        }
        entries.append(entry)
        if not arithmetic["on_grid"]:
            off_grid.append(index)

    return {
        "status": "GRID_FAIL" if off_grid else "GRID_PASS",
        "default": dict(default_fields),
        "override_indices": sorted(resolved),
        "components": entries,
        "counts": {
            "components": COMPONENTS,
            "defaulted": COMPONENTS - len(resolved),
            "overridden": len(resolved),
            "on_grid": COMPONENTS - len(off_grid),
            "off_grid": len(off_grid),
        },
        "off_grid_indices": off_grid,
    }


def _expected_envelope(mathematics):
    domain = dict(DOMAIN_LABELS)
    domain.update({"component_count": COMPONENTS, "grid_denominator": GRID})
    expected = {
        "schema": RESULT_SCHEMA,
        "domain": domain,
        "inputs": {role: dict(identity) for role, identity in PINNED_FILES.items()},
        "root_order_basis": ROOT_BASIS,
        "scope": RESULT_SCOPE,
    }
    expected.update(mathematics)
    return expected


def _compare_exact(expected, observed, location="result"):
    require(type(observed) is type(expected),
            "AUDIT_RESULT_TYPE", "saved-result type differs at " + location)
    if type(expected) is dict:
        require(set(observed) == set(expected),
                "AUDIT_RESULT_KEYS", "saved-result keys differ at " + location)
        for name in sorted(expected):
            _compare_exact(expected[name], observed[name], location + "." + name)
    elif type(expected) is list:
        require(len(observed) == len(expected),
                "AUDIT_RESULT_LENGTH", "saved-result array length differs at " + location)
        for index in range(len(expected)):
            _compare_exact(expected[index], observed[index], location + "[" + str(index) + "]")
    else:
        require(observed == expected,
                "AUDIT_RESULT_VALUE", "saved-result value differs at " + location)


def audit_arguments(certificate_raw, result_raw):
    """Compare all declared fields; suitable only for future direct controls."""
    mathematics = reconstruct_certificate(certificate_raw)
    observed = _bounded_json(result_raw, RESULT_LIMIT, RESULT_DEPTH)
    _compare_exact(_expected_envelope(mathematics), observed)
    return {
        "schema": "ri159-grid-saved-audit-verdict-v1",
        "status": "MATCH",
        "reported_grid_status": mathematics["status"],
        "components_compared": COMPONENTS,
        "comparison": "ALL_RESULT_FIELDS_EXACT_TYPE_SENSITIVE_RECOMPUTATION",
        "boundary": "DIRECT_ARGUMENTS_NOT_AUTHENTICATED",
        "root_order_basis": ROOT_BASIS,
        "scope": RESULT_SCOPE,
    }


def _file_state(metadata):
    return (metadata.st_dev, metadata.st_ino, metadata.st_mode,
            metadata.st_nlink, metadata.st_uid, metadata.st_gid, metadata.st_size,
            metadata.st_mtime_ns, metadata.st_ctime_ns)


def _validated_path(path):
    require(type(path) is str and 0 < len(path) <= 4096
            and "\x00" not in path and os.path.isabs(path)
            and not path.startswith("//") and os.path.normpath(path) == path,
            "AUDIT_PATH", "input path must be bounded, absolute and normalized")
    pieces = path.split("/")[1:]
    require(0 < len(pieces) <= 128 and all(pieces),
            "AUDIT_PATH", "input path must have one to 128 nonempty components")
    ancestors = []
    prefix = ""
    for index, piece in enumerate(pieces):
        prefix += "/" + piece
        metadata = os.lstat(prefix)
        require(not stat.S_ISLNK(metadata.st_mode),
                "AUDIT_PATH_SYMLINK", "input path must not contain a symlink")
        if index + 1 < len(pieces):
            require(stat.S_ISDIR(metadata.st_mode),
                    "AUDIT_PATH_ANCESTOR", "input path ancestor must be a directory")
            ancestors.append((prefix, _file_state(metadata)))
        else:
            require(stat.S_ISREG(metadata.st_mode),
                    "AUDIT_FILE_TYPE", "input must be a regular file")
            leaf = _file_state(metadata)
    require(os.path.realpath(path) == path,
            "AUDIT_PATH_REALPATH", "input real path must equal the declared path")
    return leaf, tuple(ancestors)


def _as_refusal(error, io_code="AUDIT_IO", io_message="input or output I/O failed"):
    if isinstance(error, AuditRefusal):
        return error
    if isinstance(error, OSError):
        return AuditRefusal(io_code, io_message)
    return AuditRefusal("AUDIT_INTERNAL", "unexpected auditor failure")


def _retain_later(primary, later, stage):
    """All callers have fixed bounded loops; preserve original code/message."""
    normalized = _as_refusal(later)
    if primary is None:
        return normalized
    primary.later_errors.append({"stage": stage, "code": normalized.code,
                                 "message": normalized.message})
    for detail in normalized.later_errors:
        primary.later_errors.append(dict(detail))
    return primary


def _read_regular_bounded(path, limit):
    before_path, before_ancestors = _validated_path(path)
    require(hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_NONBLOCK"),
            "AUDIT_HOST", "host must provide O_NOFOLLOW and O_NONBLOCK")
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    primary = None
    answer = None
    try:
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode), "AUDIT_FILE_TYPE", "input must be a regular file")
        require(_file_state(before) == before_path,
                "AUDIT_FILE_CHANGED", "input pathname differs from the opened descriptor")
        require(before.st_size <= limit, "AUDIT_FILE_SIZE", "input file exceeds byte limit")
        chunks = []
        size = 0
        while True:
            block = os.read(descriptor, min(65536, limit + 1 - size))
            if not block:
                break
            chunks.append(block)
            size += len(block)
            require(size <= limit, "AUDIT_FILE_SIZE", "input file exceeds byte limit")
        after = os.fstat(descriptor)
        after_path, after_ancestors = _validated_path(path)
        require(_file_state(before) == _file_state(after) == after_path
                and before_ancestors == after_ancestors,
                "AUDIT_FILE_CHANGED", "input file changed during a bounded read")
        raw = b"".join(chunks)
        require(len(raw) == after.st_size,
                "AUDIT_FILE_CHANGED", "input file size disagrees with captured bytes")
        answer = (raw, _file_state(after))
    except Exception as error:
        primary = _as_refusal(error)
    finally:
        try:
            os.close(descriptor)
        except Exception as error:
            close_failure = _as_refusal(error, "AUDIT_CLOSE", "input descriptor close failed")
            primary = _retain_later(primary, close_failure, "descriptor_close")
    if primary is not None:
        raise primary
    return answer


def _identity(path, raw):
    return {"path": path, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def _authenticate_fixed_files():
    captures = {}
    for role, pin in PINNED_FILES.items():
        raw, state = _read_regular_bounded(pin["path"], pin["bytes"])
        require(_identity(pin["path"], raw) == pin,
                "AUDIT_FIXED_IDENTITY", "fixed input identity differs for " + role)
        captures[role] = (raw, state)
    return captures


def audit_saved_result(saved_result_path):
    """Fixed-pin future entry; no caller-supplied pins or certificate pathname."""
    captured = _authenticate_fixed_files()
    primary = None
    result_raw = None
    result_state = None
    verdict = None
    try:
        result_raw, result_state = _read_regular_bounded(saved_result_path, RESULT_LIMIT)
        verdict = audit_arguments(captured["certificate"][0], result_raw)
    except Exception as error:
        primary = _as_refusal(error)

    # Recheck every fixed file and the saved result, not only a producer digest.
    # No capture is interpreted as continuous custody or a historic execution.
    # Ordinary analysis refusal does not skip these independent attempts. A
    # non-Exception hard abort propagates without manufacturing a complete tail.
    for role, pin in PINNED_FILES.items():
        try:
            again, state = _read_regular_bounded(pin["path"], pin["bytes"])
            require(_identity(pin["path"], again) == pin and again == captured[role][0]
                    and state == captured[role][1],
                    "AUDIT_FIXED_RECHECK", "fixed input changed after comparison for " + role)
        except Exception as error:
            primary = _retain_later(primary, error, "fixed_recheck:" + role)
    try:
        result_again, state_again = _read_regular_bounded(saved_result_path, RESULT_LIMIT)
        require(result_raw is not None and result_state is not None,
                "AUDIT_RESULT_NO_BASELINE", "saved result has no successful initial capture")
        require(result_again == result_raw and state_again == result_state,
                "AUDIT_RESULT_RECHECK", "saved result changed after comparison")
    except Exception as error:
        primary = _retain_later(primary, error, "saved_result_recheck")
    if primary is not None:
        raise primary
    verdict["boundary"] = "FIXED_PIN_SAVED_RESULT_AUDIT"
    verdict["inputs"] = {role: dict(pin) for role, pin in PINNED_FILES.items()}
    verdict["saved_result"] = _identity(saved_result_path, result_raw)
    verdict["file_checks"] = "BOUNDED_PRE_POST_READS_NOT_CONTINUOUS_CUSTODY"
    return verdict


def main():
    try:
        require(len(sys.argv) == 2, "AUDIT_ARGUMENTS", "expected one absolute saved-result path")
        verdict = audit_saved_result(sys.argv[1])
        encoded = (json.dumps(verdict, sort_keys=True, separators=(",", ":"),
                              ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")
        require(len(encoded) <= 16384,
                "AUDIT_OUTPUT_SIZE", "audit verdict exceeds its output bound")
        written = sys.stdout.buffer.write(encoded)
        require(type(written) is int and written == len(encoded),
                "AUDIT_OUTPUT_SHORT_WRITE", "audit verdict output was not completely written")
        sys.stdout.buffer.flush()
        return 0
    except AuditRefusal as error:
        refusal = {"schema": "ri159-grid-audit-refusal-v1", "status": "REFUSED",
                   "code": error.code, "message": error.message,
                   "later_errors": error.later_errors}
    except OSError:
        refusal = {"schema": "ri159-grid-audit-refusal-v1", "status": "REFUSED",
                   "code": "AUDIT_IO", "message": "input or output I/O failed"}
    except Exception:
        refusal = {"schema": "ri159-grid-audit-refusal-v1", "status": "REFUSED",
                   "code": "AUDIT_INTERNAL", "message": "unexpected auditor failure"}
    # Messages are local literals or bounded schema paths, never input excerpts.
    diagnostic = json.dumps(refusal, sort_keys=True, separators=(",", ":")) + "\n"
    if len(diagnostic.encode("utf-8")) > 8192:
        bounded = {"schema": refusal["schema"], "status": "REFUSED",
                   "code": refusal["code"], "message": refusal["message"],
                   "diagnostic_bound_exceeded": True,
                   "later_errors_omitted": len(refusal.get("later_errors", []))}
        diagnostic = json.dumps(bounded, sort_keys=True, separators=(",", ":")) + "\n"
    try:
        sys.stderr.write(diagnostic)
        sys.stderr.flush()
    except OSError:
        pass  # Exit remains refusal; no diagnostic persistence is claimed.
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
