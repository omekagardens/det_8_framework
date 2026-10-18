#!/usr/bin/env python3
"""RI191 source-only exact pair witness; execution requires separate admission.

No argument can replace a production path or pin. evaluate_payload is an
UNBOUND_ARGUMENT_ONLY boundary for future synthetic qualification, never an
attestation of the prescribed law. No graph or scientific helper is loaded.
The original declared root list is inherited, not independently reconstructed.
Self/interpreter trust, hard resource limits and complete output custody remain
external root/tool obligations. A cooperative deadline cannot bound kernel stalls.
"""

from fractions import Fraction
import hashlib
import json
import os
import stat
import sys
import time


MAX_CERTIFICATE_BYTES = 65536
MAX_FIXED_FILE_BYTES = 262144
MAX_DEPTH = 8
MAX_TOKENS = 4096
MAX_CONTAINERS = 512
MAX_CONTAINER_ITEMS = 128
MAX_STRING_CHARACTERS = 256
MAX_RATIONAL_DIGITS = 64
MAX_JSON_INTEGER_DIGITS = 10
MAX_OUTPUT_BYTES = 16384
MAX_ERROR_BYTES = 8192
COOPERATIVE_SECONDS = 20
TARGETS = ((2254, 7, 0), (2254, 7, 1))
DOMAIN = {
    "schema": "ri41-height-primal-v1",
    "seed": "interior_a",
    "parent_size": 4,
    "potential": "RI-38 maximal-deletion",
    "component_order": "increasing minimum canonical-local-key",
}
REQUIRED_KEYS = frozenset(DOMAIN) | {"roots", "default_alpha", "overrides"}
SCOPE = "PAIR_SEPARATION_ONLY_NOT_ACTUAL_W_H30_OR_PHYSICAL_ACCEPTANCE"

# Root-approved opaque certificate identity is not execution or extraction
# admission. These nine identities exclude this file and any self-pin cycle.
FIXED_INPUTS = {
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
    "prefix_completion": {
        "path": "/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md",
        "bytes": 17102,
        "sha256": "e99ea92b13687d7de6ad4db2bec9161397edb8ddacac18f6b32966e58ca85122",
    },
    "component_routing": {
        "path": "/Volumes/AI_DATA/development/det-review-evidence/ri189-coupled-record-contrast-y5nubaac/COMPONENT_ROUTING.md",
        "bytes": 14511,
        "sha256": "dd22418d9f2c864473354be301045514d3bd8e0026af4dd7244db243a26b908b",
    },
    "coupled_contrast": {
        "path": "/Volumes/AI_DATA/development/det-review-evidence/ri189-coupled-record-contrast-y5nubaac/COUPLED_CONTRAST.md",
        "bytes": 14099,
        "sha256": "d4aae718f0e23c3f3e70ba529e3020fd85114d586ba4e86d58f380402087091a",
    },
    "accepted_predecessor": {
        "path": "/Volumes/AI_DATA/development/det-review-evidence/ri188-root-endpoint-profile-review-1jg_i948/RI189_ROOT_ADJUDICATION.json",
        "bytes": 1267,
        "sha256": "44985b1f471baa3ae3f3f34392bf60bc8629dda641bfab6f0b7317a191c46c4c",
    },
    "accepted_manual_review": {
        "path": "/Volumes/AI_DATA/development/det-review-evidence/ri188-root-endpoint-profile-review-1jg_i948/RI189_ROOT_PROOF_REVIEW.md",
        "bytes": 4796,
        "sha256": "39e71e42be19cf68c62138374a8601b0820b8553d6dc9ea3d31f5d7003e924dd",
    },
    "assignment": {
        "path": "/Volumes/AI_DATA/development/det-review-evidence/ri188-root-endpoint-profile-review-1jg_i948/RI191_NATIVE_ASSIGNMENT.json",
        "bytes": 2614,
        "sha256": "c2995ccdc6798e2d1606f4aff42403d93ecac2727c1747b061833b13acf7b302",
    },
}


class Refused(Exception):
    def __init__(self, code, message, secondary_errors=()):
        super().__init__(message)
        self.code = code
        self.message = message
        self.secondary_errors = tuple(secondary_errors)


def require(condition, code, message):
    if not condition:
        raise Refused(code, message)


def error_detail(error):
    if isinstance(error, Refused):
        return {"code": error.code, "message": error.message}
    return {"code": "UNEXPECTED_EXCEPTION", "message": type(error).__name__}


def refuse_with_later(first, later):
    detail = error_detail(first)
    retained = first.secondary_errors if isinstance(first, Refused) else ()
    raise Refused(detail["code"], detail["message"], (*retained, *later))


def lexical_budget(text):
    """Bound the parser before allocating JSON containers; no JSON is evaluated."""
    stack = []
    tokens = containers = position = 0
    while position < len(text):
        char = text[position]
        if char in " \t\r\n":
            position += 1
            continue
        tokens += 1
        require(tokens <= MAX_TOKENS, "JSON_TOKEN_LIMIT", "JSON token limit exceeded")
        if char == '"':
            position += 1
            count = 0
            closed = False
            while position < len(text):
                char = text[position]
                position += 1
                if char == '"':
                    closed = True
                    break
                count += 1
                if char == "\\" and position < len(text):
                    position += 1
                    count += 1
                require(count <= MAX_STRING_CHARACTERS, "JSON_STRING_LIMIT",
                        "JSON raw string length limit exceeded")
            require(closed, "JSON_SYNTAX", "unterminated JSON string")
        elif char in "[{":
            stack.append(char)
            containers += 1
            require(len(stack) <= MAX_DEPTH, "JSON_DEPTH_LIMIT", "JSON depth limit exceeded")
            require(containers <= MAX_CONTAINERS, "JSON_CONTAINER_LIMIT",
                    "JSON container count limit exceeded")
            position += 1
        elif char in "]}":
            expected = "[" if char == "]" else "{"
            require(bool(stack) and stack[-1] == expected, "JSON_SYNTAX",
                    "mismatched JSON container delimiter")
            stack.pop()
            position += 1
        elif char in ",:":
            position += 1
        else:
            start = position
            while position < len(text) and text[position] not in ' \t\r\n[]{}:,"':
                position += 1
            require(position - start <= MAX_STRING_CHARACTERS, "JSON_TOKEN_LENGTH",
                    "JSON scalar token length limit exceeded")
    require(not stack, "JSON_SYNTAX", "unclosed JSON container")


def parse_integer(value):
    digits = value[1:] if value.startswith("-") else value
    require(len(digits) <= MAX_JSON_INTEGER_DIGITS, "JSON_INTEGER_LIMIT",
            "JSON integer digit limit exceeded")
    return int(value)


def reject_float(value):
    raise Refused("JSON_FLOAT", "JSON floating-point numbers are forbidden")


def reject_constant(value):
    raise Refused("JSON_NONFINITE", "JSON nonfinite numbers are forbidden")


def unique_object(pairs):
    require(len(pairs) <= MAX_CONTAINER_ITEMS, "JSON_CONTAINER_ITEMS",
            "JSON object item limit exceeded")
    result = {}
    for key, value in pairs:
        require(key not in result, "JSON_DUPLICATE_KEY", "duplicate JSON object key")
        result[key] = value
    return result


def check_container_items(value):
    if type(value) is list:
        require(len(value) <= MAX_CONTAINER_ITEMS, "JSON_CONTAINER_ITEMS",
                "JSON array item limit exceeded")
        for item in value:
            check_container_items(item)
    elif type(value) is dict:
        for item in value.values():
            check_container_items(item)


def decode_certificate(raw):
    require(type(raw) is bytes, "INPUT_TYPE", "certificate argument must be bytes")
    require(0 < len(raw) <= MAX_CERTIFICATE_BYTES, "INPUT_BYTES",
            "certificate byte length outside bound")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise Refused("INPUT_UTF8", "certificate is not strict UTF-8") from None
    lexical_budget(text)
    try:
        value = json.loads(text, object_pairs_hook=unique_object,
                           parse_int=parse_integer, parse_float=reject_float,
                           parse_constant=reject_constant)
    except (ValueError, RecursionError):
        raise Refused("JSON_SYNTAX", "invalid JSON syntax") from None
    check_container_items(value)
    return value


def positive_rational(value):
    require(type(value) is str, "RATIONAL_TYPE", "coefficient must be a rational string")
    parts = value.split("/")
    require(len(parts) in (1, 2), "RATIONAL_GRAMMAR",
            "coefficient must be an ASCII integer or numerator/denominator")
    for part in parts:
        require(0 < len(part) <= MAX_RATIONAL_DIGITS, "RATIONAL_DIGITS",
                "rational term digit length outside bound")
        require(all("0" <= char <= "9" for char in part), "RATIONAL_GRAMMAR",
                "coefficient must be an ASCII integer or numerator/denominator")
    numerator = int(parts[0])
    denominator = int(parts[1]) if len(parts) == 2 else 1
    require(numerator > 0 and denominator > 0, "RATIONAL_POSITIVITY",
            "rational numerator and denominator must be positive")
    return Fraction(numerator, denominator)


def rational_text(value):
    return str(value.numerator) + "/" + str(value.denominator)


def evaluate_payload(raw):
    """Unbound synthetic-argument boundary; never authenticates an actual law."""
    data = decode_certificate(raw)
    require(type(data) is dict and REQUIRED_KEYS <= set(data), "CERTIFICATE_FIELDS",
            "certificate must contain the eight required fields")
    for key, expected in DOMAIN.items():
        require(type(data[key]) is type(expected) and data[key] == expected,
                "CERTIFICATE_DOMAIN", "certificate domain mismatch")
    roots = data["roots"]
    require(type(roots) is list and len(roots) == 109, "ROOT_COUNT",
            "certificate must declare exactly 109 roots")
    ordered = []
    for root in roots:
        require(type(root) is list and len(root) == 3, "ROOT_SHAPE",
                "each root must be an integer triple")
        require(all(type(item) is int for item in root), "ROOT_TYPE",
                "root coordinates must be integers, not booleans")
        require(0 <= root[0] <= 65535 and 0 <= root[1] < 15
                and 0 <= root[2] <= 15, "ROOT_RANGE", "root coordinate outside bound")
        require(root[2] & ~root[1] == 0, "ROOT_MASK", "root record mask is not a subset")
        key = tuple(root)
        require(not ordered or ordered[-1] < key, "ROOT_ORDER",
                "roots must be strictly lexicographically increasing and unique")
        ordered.append(key)
    require(all(key in ordered for key in TARGETS), "PAIR_ROOT_MISSING",
            "one or both routed pair roots are absent")
    default = positive_rational(data["default_alpha"])
    overrides = data["overrides"]
    require(type(overrides) is dict, "OVERRIDE_TYPE", "overrides must be an object")
    resolved = [default] * 109
    overridden = set()
    for key, value in overrides.items():
        require(type(key) is str and 0 < len(key) <= 3
                and all("0" <= char <= "9" for char in key),
                "OVERRIDE_INDEX", "override index must be canonical decimal in 0..108")
        index = int(key)
        require(key == str(index) and 0 <= index < 109, "OVERRIDE_INDEX",
                "override index must be canonical decimal in 0..108")
        resolved[index] = positive_rational(value)
        overridden.add(index)
    pair = []
    values = []
    for key in TARGETS:
        index = ordered.index(key)
        values.append(resolved[index])
        pair.append({"root": list(key), "index": index,
                     "origin": "override" if index in overridden else "default",
                     "alpha": rational_text(resolved[index])})
    epsilon = values[0] - values[1]
    require(epsilon > 0, "INHERITED_SIGN_CONFLICT",
            "pair gap conflicts with the inherited strict positive sign")
    threshold = Fraction(44 * 1147 * 3875, 41 * 126280 * 508644)
    simple = Fraction(1, 10000)
    sufficient = epsilon >= threshold
    return {
        "schema": "ri191-pair-witness-result-v1",
        "status": "SUFFICIENT" if sufficient else "INCONCLUSIVE_SMALLER_GAP",
        "binding": "UNBOUND_ARGUMENT_ONLY",
        "inputs": {},
        "root_order_basis": "UNBOUND_DECLARED_ROOT_LIST_NOT_RECONSTRUCTED",
        "component_count": 109,
        "pair": pair,
        "epsilon": rational_text(epsilon),
        "epsilon_star": rational_text(threshold),
        "simple_threshold": rational_text(simple),
        "comparisons": {"epsilon_positive": True, "meets_epsilon_star": sufficient,
                        "meets_simple_threshold": epsilon >= simple},
        "scope": SCOPE,
    }


def check_deadline(deadline):
    require(time.monotonic() < deadline, "COOPERATIVE_DEADLINE",
            "cooperative read deadline exceeded")


def file_state(value):
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def validated_path(path, deadline):
    require(type(path) is str and 0 < len(path) <= 4096
            and os.path.isabs(path) and os.path.normpath(path) == path,
            "INPUT_PATH", "fixed path must be normalized and absolute")
    parts = path.split("/")[1:]
    require(0 < len(parts) <= 64 and all(parts), "INPUT_PATH",
            "fixed path component count outside bound")
    paths = ["/"]
    current = ""
    for part in parts:
        current += "/" + part
        paths.append(current)
    states = []
    for index, item in enumerate(paths):
        check_deadline(deadline)
        value = os.lstat(item)
        require(not stat.S_ISLNK(value.st_mode), "PATH_SYMLINK",
                "fixed path contains a symbolic link")
        if index == len(paths) - 1:
            require(stat.S_ISREG(value.st_mode), "PATH_NOT_REGULAR",
                    "fixed input is not a regular file")
        else:
            require(stat.S_ISDIR(value.st_mode), "PATH_NOT_DIRECTORY",
                    "fixed path ancestor is not a directory")
        states.append(file_state(value))
    require(os.path.realpath(path) == path, "PATH_REALPATH",
            "fixed path does not equal its real path")
    return tuple(states)


def read_fixed(role, identity, deadline):
    cap = MAX_CERTIFICATE_BYTES if role == "certificate" else MAX_FIXED_FILE_BYTES
    require(type(identity) is dict and set(identity) == {"path", "bytes", "sha256"}
            and type(identity["bytes"]) is int and 0 < identity["bytes"] <= cap
            and type(identity["sha256"]) is str and len(identity["sha256"]) == 64
            and all(char in "0123456789abcdef" for char in identity["sha256"]),
            "BINDING_CONFIGURATION", "fixed input identity is unavailable or malformed")
    require(hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_NONBLOCK"),
            "PLATFORM_FLAGS", "required no-follow/nonblocking flags are unavailable")
    fd = None
    first = None
    later = []
    raw = None
    try:
        before = validated_path(identity["path"], deadline)
        require(before[-1][4] == identity["bytes"], "INPUT_SIZE",
                "fixed input byte count mismatch")
        fd = os.open(identity["path"], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        opened = os.fstat(fd)
        require(stat.S_ISREG(opened.st_mode) and file_state(opened) == before[-1],
                "INPUT_DESCRIPTOR", "opened descriptor does not match observed regular file")
        chunks = []
        count = 0
        while True:
            check_deadline(deadline)
            chunk = os.read(fd, min(16384, cap + 1 - count))
            if not chunk:
                break
            chunks.append(chunk)
            count += len(chunk)
            require(count <= cap, "INPUT_READ_LIMIT", "fixed input grew beyond read limit")
        raw = b"".join(chunks)
        require(file_state(os.fstat(fd)) == before[-1], "INPUT_CHANGED",
                "fixed input descriptor changed during read")
        after = validated_path(identity["path"], deadline)
        require(before == after, "INPUT_CHANGED", "fixed path changed during read")
        require(len(raw) == identity["bytes"], "INPUT_SIZE", "fixed input byte count mismatch")
        require(hashlib.sha256(raw).hexdigest() == identity["sha256"], "INPUT_HASH",
                "fixed input SHA256 mismatch")
    except Exception as error:
        first = error
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except Exception as error:
                later.append({"stage": "close", "role": role, **error_detail(error)})
    if first is not None:
        refuse_with_later(first, later)
    if later:
        raise Refused("INPUT_CLOSE", "fixed input descriptor close failed", later)
    return raw


def verify_fixed():
    """Authenticate every immutable input before decode and independently after."""
    deadline = time.monotonic() + COOPERATIVE_SECONDS
    first = None
    later = []
    captured = {}
    result = None
    try:
        for role, identity in FIXED_INPUTS.items():
            captured[role] = read_fixed(role, identity, deadline)
        result = evaluate_payload(captured["certificate"])
        result["binding"] = "FIXED_ORIGINAL_PREFIX_BYTES"
        result["root_order_basis"] = "INHERITED_PINNED_RI41_ACCEPTANCE_NOT_RECONSTRUCTED"
        result["inputs"] = {role: dict(identity) for role, identity in FIXED_INPUTS.items()}
    except Exception as error:
        first = error
    # Every ordinary result/refusal gets every independent postcheck. A hard
    # BaseException abort is not converted into a purported complete check tail.
    for role, identity in FIXED_INPUTS.items():
        try:
            read_fixed(role, identity, deadline)
        except Exception as error:
            later.append({"stage": "postcheck", "role": role, **error_detail(error)})
            if isinstance(error, Refused):
                later.extend(error.secondary_errors)
    if first is not None:
        refuse_with_later(first, later)
    if later:
        raise Refused("INPUT_POSTCHECK", "one or more independent input postchecks failed", later)
    return result


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def main():
    try:
        require(not sys.argv[1:], "ARGUMENTS", "this checker accepts no arguments")
        result = verify_fixed()
        output = encoded(result)
        require(len(output) <= MAX_OUTPUT_BYTES, "OUTPUT_LIMIT", "result output bound exceeded")
        count = sys.stdout.buffer.write(output)
        require(type(count) is int and count == len(output), "OUTPUT_WRITE",
                "result output write was incomplete")
        sys.stdout.buffer.flush()
        return 0
    except Exception as error:
        detail = error_detail(error)
        later = list(error.secondary_errors) if isinstance(error, Refused) else []
        diagnostic = encoded({"schema": "ri191-pair-witness-error-v1", "status": "INVALID",
                              "error": detail, "secondary_errors": later})
        if len(diagnostic) > MAX_ERROR_BYTES:
            diagnostic = encoded({"schema": "ri191-pair-witness-error-v1", "status": "INVALID",
                                  "error": detail, "secondary_errors_omitted": len(later)})
        try:
            count = sys.stderr.buffer.write(diagnostic)
            if type(count) is not int or count != len(diagnostic):
                return 2
            sys.stderr.buffer.flush()
        except Exception:
            pass
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
