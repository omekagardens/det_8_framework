"""RI161 source-only operational qualification proposal; nothing runs on import.

All filesystem and stream faults below are isolated in-memory boundary doubles.
No protected file is opened, no production pin is modified, and no fixture is
written. Scientific comparisons belong to qualify_grid.py; composition probes
explicitly substitute their lower boundaries. A later root admission is needed
even to instantiate these controls. P10/P11 belong to the genuine caller.
"""

from contextlib import contextmanager
from copy import deepcopy
import hashlib
import json
import posixpath
import stat
from types import SimpleNamespace


ROLES = ("certificate", "original_source", "original_manuscript", "assignment",
         "accepted_predecessor", "accepted_manual_review")
BOUNDARY = "SYNTHETIC_ISOLATED_IO_NOT_FIXED_INPUT_AUTHENTICATION"
STATE = (1, 2, 3)


class FaultFailure(Exception):
    def __init__(self, message, records=None):
        super().__init__(message)
        self.records = [] if records is None else records


def _need(condition, message):
    if not condition:
        raise FaultFailure(message)


def _encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def _same(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(_same(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    return left == right


@contextmanager
def _patched(module, **replacements):
    old = {name: getattr(module, name) for name in replacements}
    try:
        for name, value in replacements.items():
            setattr(module, name, value)
        yield
    finally:
        for name, value in old.items():
            setattr(module, name, value)


def _refusal(kind, code, message, later=None):
    return {"kind": "refusal", "exception_type": kind, "code": code,
            "message": message, "later_errors": [] if later is None else later}


def _capture(function, refusal_type=None):
    try:
        value = function()
        if type(value) is bytes:
            value = {"bytes_hex": value.hex()}
        return {"kind": "return", "value": value}
    except FaultFailure:
        raise  # A boundary-double/harness defect is not a subject refusal.
    except Exception as error:
        if refusal_type is None or type(error) is not refusal_type:
            raise FaultFailure("unexpected subject exception identity: " + type(error).__name__) from error
        return _refusal(type(error).__name__, getattr(error, "code", None),
                        str(error), deepcopy(getattr(error, "later_errors", [])))


def _metadata(mode, size=0, stamp=1, inode=7):
    return SimpleNamespace(st_dev=1, st_ino=inode, st_mode=mode, st_nlink=1,
                           st_uid=1, st_gid=1, st_size=size,
                           st_mtime_ns=stamp, st_ctime_ns=stamp)


class MemoryOS:
    """A finite single-file double, never an adapter to the host filesystem."""

    O_RDONLY = 0
    O_NOFOLLOW = 2
    O_NONBLOCK = 4

    def __init__(self, path, data, fault="none"):
        self.filename = path
        self.data = data
        self.fault = fault
        self.offset = 0
        self.stamp = 1
        self.calls = []
        self.path = SimpleNamespace(isabs=posixpath.isabs, normpath=posixpath.normpath,
                                    realpath=self.realpath)

    def realpath(self, path):
        return "/different/path" if self.fault == "realpath_alias" else path

    def lstat(self, path):
        if self.fault == "missing" and path == self.filename:
            raise FileNotFoundError("synthetic_missing")
        if path == self.filename:
            modes = {"directory": stat.S_IFDIR, "fifo": stat.S_IFIFO,
                     "device": stat.S_IFCHR, "leaf_link": stat.S_IFLNK}
            return _metadata(modes.get(self.fault, stat.S_IFREG) | 0o600,
                             len(self.data), self.stamp)
        parent = posixpath.dirname(self.filename)
        if self.fault == "ancestor_link" and path == parent:
            return _metadata(stat.S_IFLNK | 0o700, inode=8)
        return _metadata(stat.S_IFDIR | 0o700, inode=8)

    def open(self, path, flags):
        self.calls.append("open")
        _need(path == self.filename and flags == 6, "unexpected direct open")
        if self.fault == "before_open_change":
            self.stamp += 1
        return 9

    def fstat(self, descriptor):
        _need(descriptor == 9, "unexpected descriptor")
        return _metadata(stat.S_IFREG | 0o600, len(self.data), self.stamp)

    def read(self, descriptor, size):
        _need(descriptor == 9 and type(size) is int and size > 0, "invalid bounded read")
        self.calls.append("read")
        chunk = self.data[self.offset:self.offset + size]
        self.offset += len(chunk)
        if self.fault == "during_read_change" and len(self.calls) == 2:
            self.stamp += 1
        return chunk

    def close(self, descriptor):
        _need(descriptor == 9, "unexpected close descriptor")
        self.calls.append("close")
        if self.fault in ("close_only", "primary_and_close"):
            raise OSError("synthetic_close")


def _read_probe(module, implementation, fault):
    path = "/qualification/input.json"
    if fault == "relative":
        path = "qualification/input.json"
    elif fault == "nonnormal":
        path = "/qualification/../qualification/input.json"
    data = b"x"
    mock = MemoryOS(path, data, fault)
    digest = hashlib.sha256(data).hexdigest()
    if fault == "primary_and_close":
        digest = "0" * 64
    with _patched(module, os=mock):
        if implementation == "checker":
            outcome = _capture(lambda: module.read_fixed(("synthetic", path, 1, digest)), module.GridRefused)
        else:
            limit = 0 if fault == "primary_and_close" else 1
            # Drop the implementation-specific stat tuple on successful probes.
            outcome = _capture(lambda: module._read_regular_bounded(path, limit)[0],
                               FileNotFoundError if fault == "missing" else module.AuditRefusal)
    return {"subject": outcome, "calls": mock.calls}


def _read_expected(implementation, fault):
    regular_calls = ["open", "read", "read", "close"]
    if implementation == "checker":
        errors = {
            "missing": ("IDENTITY_IO", "fixed input could not be read: synthetic", []),
            "directory": ("IDENTITY_TYPE", "fixed input is not a nonsymlink regular file: synthetic", []),
            "fifo": ("IDENTITY_TYPE", "fixed input is not a nonsymlink regular file: synthetic", []),
            "device": ("IDENTITY_TYPE", "fixed input is not a nonsymlink regular file: synthetic", []),
            "leaf_link": ("IDENTITY_TYPE", "fixed input is not a nonsymlink regular file: synthetic", []),
            "ancestor_link": ("IDENTITY_ANCESTOR", "fixed input ancestor is not a nonsymlink directory: synthetic", []),
            "realpath_alias": ("IDENTITY_PATH", "fixed input path is not normalized and nonsymlink: synthetic", []),
            "relative": ("IDENTITY_PATH", "fixed input path is not normalized and nonsymlink: synthetic", []),
            "nonnormal": ("IDENTITY_PATH", "fixed input path is not normalized and nonsymlink: synthetic", []),
            "before_open_change": ("IDENTITY_METADATA", "fixed input identity or length changed: synthetic", ["open", "close"]),
            "during_read_change": ("IDENTITY_METADATA", "fixed input changed during reading: synthetic", regular_calls),
            "close_only": ("IDENTITY_CLOSE", "fixed input close failed: synthetic:OSError", regular_calls),
            "primary_and_close": ("IDENTITY_PRIMARY_AND_CLOSE", "primary=IDENTITY_BYTES:fixed input complete byte pin changed: synthetic; close=OSError", regular_calls),
        }
        code, message, calls = errors[fault]
        return {"subject": _refusal("GridRefused", code, message), "calls": calls}
    if fault == "missing":
        return {"subject": _refusal("FileNotFoundError", None, "synthetic_missing"), "calls": []}
    errors = {
        "directory": ("AUDIT_FILE_TYPE", "input must be a regular file", []),
        "fifo": ("AUDIT_FILE_TYPE", "input must be a regular file", []),
        "device": ("AUDIT_FILE_TYPE", "input must be a regular file", []),
        "leaf_link": ("AUDIT_PATH_SYMLINK", "input path must not contain a symlink", []),
        "ancestor_link": ("AUDIT_PATH_SYMLINK", "input path must not contain a symlink", []),
        "realpath_alias": ("AUDIT_PATH_REALPATH", "input real path must equal the declared path", []),
        "relative": ("AUDIT_PATH", "input path must be bounded, absolute and normalized", []),
        "nonnormal": ("AUDIT_PATH", "input path must be bounded, absolute and normalized", []),
        "before_open_change": ("AUDIT_FILE_CHANGED", "input pathname differs from the opened descriptor", ["open", "close"]),
        "during_read_change": ("AUDIT_FILE_CHANGED", "input file changed during a bounded read", regular_calls),
        "close_only": ("AUDIT_CLOSE", "input descriptor close failed", regular_calls),
        "primary_and_close": ("AUDIT_FILE_SIZE", "input file exceeds byte limit", ["open", "close"]),
    }
    code, message, calls = errors[fault]
    later = ([{"stage": "descriptor_close", "code": "AUDIT_CLOSE",
               "message": "input descriptor close failed"}]
             if fault == "primary_and_close" else [])
    return {"subject": _refusal("AuditRefusal", code, message, later), "calls": calls}


def _pin_probe(module, implementation, role, variation):
    """Isolate each fixed pin; earlier audit-role authentication is a double."""
    if implementation == "checker":
        identity = next(item for item in module.FIXED_IDENTITIES if item[0] == role)
        _, path, size, _digest = identity
        raw = b"x" * (size + (1 if variation == "length" else 0))
        mock = MemoryOS(path, raw)
        with _patched(module, os=mock):
            outcome = _capture(lambda: module.read_fixed(identity), module.GridRefused)
        return {"subject": outcome}
    pins = deepcopy(module.PINNED_FILES)
    real_identity = module._identity
    real_reader = module._read_regular_bounded
    calls = []
    target_path = pins[role]["path"]

    def reader(path, limit):
        found = next(name for name in ROLES if pins[name]["path"] == path)
        calls.append(found)
        if path == target_path:
            raw = b"x" * (pins[role]["bytes"] + (1 if variation == "length" else 0))
            mock = MemoryOS(path, raw)
            with _patched(module, os=mock):
                return real_reader(path, limit)
        return b"x", STATE

    def identity(path, raw):
        if path == target_path:
            return real_identity(path, raw)
        return deepcopy(next(pin for pin in pins.values() if pin["path"] == path))

    with _patched(module, _read_regular_bounded=reader, _identity=identity):
        outcome = _capture(module._authenticate_fixed_files, module.AuditRefusal)
    return {"subject": outcome, "calls": calls}


def _pin_expected(implementation, role, variation):
    if implementation == "checker":
        code = "IDENTITY_METADATA" if variation == "length" else "IDENTITY_BYTES"
        message = (("fixed input identity or length changed: " if variation == "length"
                    else "fixed input complete byte pin changed: ") + role)
        return {"subject": _refusal("GridRefused", code, message)}
    code = "AUDIT_FILE_SIZE" if variation == "length" else "AUDIT_FIXED_IDENTITY"
    message = ("input file exceeds byte limit" if variation == "length"
               else "fixed input identity differs for " + role)
    return {"subject": _refusal("AuditRefusal", code, message),
            "calls": list(ROLES[:ROLES.index(role) + 1])}


def _post_probe(module, implementation, scenario):
    calls = []
    failures = {"certificate", "original_manuscript", "accepted_manual_review"}
    if scenario == "late_one":
        failures = {"original_source"}
    primary = scenario in ("primary_one", "primary_many")
    if scenario == "primary_one":
        failures = {"original_source"}
    if implementation == "checker":
        counts = {role: 0 for role in ROLES}

        def reader(identity):
            role = identity[0]
            counts[role] += 1
            calls.append(("initial:" if counts[role] == 1 else "final:") + role)
            if counts[role] == 2 and role in failures:
                raise module.GridRefused("IDENTITY_IO", "fixed input could not be read: " + role)
            return b""

        def decoder(_raw):
            if primary:
                raise module.GridRefused("CERTIFICATE_BYTES", "certificate must be nonempty bounded bytes")
            return {}

        with _patched(module, read_fixed=reader, decode_certificate=decoder,
                      reconstruct_certificate=lambda _data: {"synthetic": True}):
            outcome = _capture(module.production_result, module.GridRefused)
        return {"subject": outcome, "calls": calls}

    pins = deepcopy(module.PINNED_FILES)
    captured = {role: (b"opaque", STATE) for role in ROLES}
    saved = "/qualification/saved.json"
    saved_count = 0

    def reader(path, _limit):
        nonlocal saved_count
        if path == saved:
            saved_count += 1
            calls.append("saved:" + str(saved_count))
            if saved_count == 1 and scenario == "no_baseline":
                raise OSError("synthetic_saved_initial")
            return (b"changed" if scenario == "saved_drift" and saved_count == 2
                    else b"saved"), STATE
        role = next(name for name in ROLES if pins[name]["path"] == path)
        calls.append("final:" + role)
        return (b"changed" if role in failures and scenario not in
                ("no_baseline", "saved_drift") else b"opaque"), STATE

    def identity(path, raw):
        for pin in pins.values():
            if pin["path"] == path:
                return deepcopy(pin)
        return {"path": path, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

    def comparison(_certificate, _result):
        if primary:
            raise module.AuditRefusal("AUDIT_JSON_SYNTAX", "JSON input has invalid syntax")
        return {"status": "MATCH", "boundary": "DIRECT_ARGUMENTS_NOT_AUTHENTICATED"}

    with _patched(module, _authenticate_fixed_files=lambda: captured,
                  _read_regular_bounded=reader, _identity=identity,
                  audit_arguments=comparison):
        outcome = _capture(lambda: module.audit_saved_result(saved), module.AuditRefusal)
    return {"subject": outcome, "calls": calls}


def _post_expected(implementation, scenario):
    failures = ["certificate", "original_manuscript", "accepted_manual_review"]
    if scenario in ("late_one", "primary_one"):
        failures = ["original_source"]
    primary = scenario in ("primary_one", "primary_many")
    if implementation == "checker":
        tail = ",".join(role + ":IDENTITY_IO:fixed input could not be read: " + role
                        for role in failures)
        message = ("primary=CERTIFICATE_BYTES:certificate must be nonempty bounded bytes; postchecks=" + tail
                   if primary else tail)
        outcome = _refusal("GridRefused", "PRIMARY_AND_POSTCHECK" if primary else "POSTCHECK", message)
        return {"subject": outcome,
                "calls": ["initial:" + role for role in ROLES] + ["final:" + role for role in ROLES]}
    calls = ["saved:1"] + ["final:" + role for role in ROLES] + ["saved:2"]
    if scenario == "no_baseline":
        return {"subject": _refusal("AuditRefusal", "AUDIT_IO", "input or output I/O failed",
                    [{"stage": "saved_result_recheck", "code": "AUDIT_RESULT_NO_BASELINE",
                      "message": "saved result has no successful initial capture"}]), "calls": calls}
    if scenario == "saved_drift":
        return {"subject": _refusal("AuditRefusal", "AUDIT_RESULT_RECHECK",
                                    "saved result changed after comparison"), "calls": calls}
    details = [{"stage": "fixed_recheck:" + role, "code": "AUDIT_FIXED_RECHECK",
                "message": "fixed input changed after comparison for " + role} for role in failures]
    if primary:
        error = _refusal("AuditRefusal", "AUDIT_JSON_SYNTAX", "JSON input has invalid syntax", details)
    else:
        first, rest = details[0], details[1:]
        error = _refusal("AuditRefusal", first["code"], first["message"], rest)
    return {"subject": error, "calls": calls}


class MemoryStream:
    def __init__(self, fault="none"):
        self.buffer = self
        self.fault = fault
        self.data = bytearray()
        self.calls = []

    def write(self, value):
        self.calls.append("write")
        raw = value.encode("utf-8") if type(value) is str else value
        if self.fault == "write_error":
            raise OSError("synthetic_write")
        count = len(raw) - 1 if self.fault == "short" else len(raw)
        self.data.extend(raw[:count])
        return count

    def flush(self):
        self.calls.append("flush")
        if self.fault == "flush_error":
            raise OSError("synthetic_flush")


def _main_probe(module, implementation, scenario):
    out_fault = {"short_write": "short", "flush_failure": "flush_error"}.get(scenario, "none")
    err_fault = "write_error" if scenario == "diagnostic_failure" else "none"
    output, error = MemoryStream(out_fault), MemoryStream(err_fault)
    args = ["subject"] + (["/qualification/saved.json"] if implementation == "auditor" else [])
    if scenario == "arguments":
        args = ["subject", "unexpected"] if implementation == "checker" else ["subject"]
    fake_sys = SimpleNamespace(argv=args, stdout=output, stderr=error)

    def result(*_args):
        if scenario == "diagnostic_failure":
            if implementation == "checker":
                raise module.GridRefused("IDENTITY_IO", "fixed input could not be read: certificate")
            raise module.AuditRefusal("AUDIT_IO", "input or output I/O failed")
        return {"sentinel": True}

    method = "production_result" if implementation == "checker" else "audit_saved_result"
    with _patched(module, sys=fake_sys, **{method: result}):
        outcome = _capture(module.main)
    return {"subject": outcome, "stdout_hex": bytes(output.data).hex(),
            "stderr_hex": bytes(error.data).hex(),
            "stdout_calls": output.calls, "stderr_calls": error.calls}


def _main_expected(implementation, scenario):
    stdout = b""
    stdout_calls = []
    schema = "ri159-grid-check-refusal-v1" if implementation == "checker" else "ri159-grid-audit-refusal-v1"
    if scenario == "arguments":
        code = "ARGUMENTS" if implementation == "checker" else "AUDIT_ARGUMENTS"
        message = ("grid checker accepts no arguments" if implementation == "checker"
                   else "expected one absolute saved-result path")
    elif scenario == "short_write":
        stdout = b'{"sentinel":true}'
        stdout_calls = ["write"]
        code = "OUTPUT_WRITE" if implementation == "checker" else "AUDIT_OUTPUT_SHORT_WRITE"
        message = ("grid result write was incomplete" if implementation == "checker"
                   else "audit verdict output was not completely written")
    elif scenario == "flush_failure":
        stdout = b'{"sentinel":true}\n'
        stdout_calls = ["write", "flush"]
        code = "UNEXPECTED" if implementation == "checker" else "AUDIT_IO"
        message = ("unexpected operational failure: OSError" if implementation == "checker"
                   else "input or output I/O failed")
    else:
        code = "IDENTITY_IO" if implementation == "checker" else "AUDIT_IO"
        message = ("fixed input could not be read: certificate" if implementation == "checker"
                   else "input or output I/O failed")
    diagnostic = {"schema": schema, "status": "REFUSED", "code": code, "message": message}
    if implementation == "auditor" and scenario != "flush_failure":
        diagnostic["later_errors"] = []
    stderr = b"" if scenario == "diagnostic_failure" else _encode(diagnostic) + b"\n"
    return {"subject": {"kind": "return", "value": 2}, "stdout_hex": stdout.hex(),
            "stderr_hex": stderr.hex(), "stdout_calls": stdout_calls,
            "stderr_calls": ["write"] if scenario == "diagnostic_failure" else ["write", "flush"]}


def _plan():
    cases = []
    for implementation in ("checker", "auditor"):
        for role in ROLES:
            for variation in ("length", "hash"):
                cases.append(("P01." + role + "." + variation + "." + implementation,
                              "P01", implementation, "pin", (role, variation)))
        for fault in ("missing", "directory", "fifo", "device", "leaf_link", "ancestor_link", "realpath_alias"):
            cases.append(("P02." + fault + "." + implementation, "P02", implementation, "read", fault))
        for fault in ("before_open_change", "during_read_change", "close_only", "primary_and_close"):
            cases.append(("P03." + fault + "." + implementation, "P03", implementation, "read", fault))
        for scenario in ("late_one", "late_many", "primary_one", "primary_many"):
            cases.append(("P04." + scenario + "." + implementation, "P04", implementation, "post", scenario))
        cases.append(("P05.arguments." + implementation, "P05", implementation, "main", "arguments"))
        for fault in ("relative", "nonnormal", "leaf_link", "ancestor_link"):
            cases.append(("P06." + fault + "." + implementation, "P06", implementation, "read", fault))
        for scenario in ("short_write", "flush_failure", "diagnostic_failure"):
            cases.append(("P09." + scenario + "." + implementation, "P09", implementation, "main", scenario))
    for scenario in ("no_baseline", "saved_drift"):
        cases.append(("P07." + scenario + ".auditor", "P07", "auditor", "post", scenario))
    # P08 and P12 use independent literals below, not the other implementation.
    cases.extend([
        ("P08.other_certificate.auditor", "P08", "auditor", "authority", "different"),
        ("P12.direct_boundary.checker", "P12", "checker", "authority", "direct"),
        ("P12.direct_boundary.auditor", "P12", "auditor", "authority", "direct"),
    ])
    return cases


def case_catalogue():
    return [{"id": identity, "family": family, "implementation": implementation,
             "boundary": BOUNDARY} for identity, family, implementation, _kind, _arg in _plan()]


def _literal_certificate():
    return {"schema": "ri41-height-primal-v1", "seed": "interior_a", "parent_size": 4,
            "potential": "RI-38 maximal-deletion", "component_order": "increasing minimum canonical-local-key",
            "roots": [[index, 0, 0] for index in range(109)], "default_alpha": "1/8", "overrides": {}}


def _literal_inputs():
    repo = "/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/"
    root = "/Volumes/AI_DATA/development/det-review-evidence/ri157-root-adjudication-q_wj4pny/"
    fields = [
        ("certificate", repo + "CERTIFICATE.json", 2845, "3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969"),
        ("original_source", repo + "check.py", 13219, "f33a2345608867138f1036da6a020beb6608e3f58fc3032ceb1d3c3d5c9f90c5"),
        ("original_manuscript", repo + "NORMALIZATION.md", 16243, "567596a17c69e20b33328b2d0c39f22d98a78f7d25d81949fd57cd07df5e53c8"),
        ("assignment", root + "NATIVE_SUCCESSOR_ASSIGNMENT.json", 4916, "782b057624a35094093558e52e40a78d3a61b3ff1cbb61d2c3dd675171b1911e"),
        ("accepted_predecessor", root + "RI157_ROOT_ADJUDICATION.json", 2404, "d052d2c1f51691a861792690a89d8175755c8bffd5016a81b892c8d7abd76950"),
        ("accepted_manual_review", root + "ROOT_MANUAL_REVIEW.md", 4362, "3040fadd824a82b8aee1c51338719ff79da7a3eb0d1c56ce9c1816588dba2b05"),
    ]
    return {role: {"path": path, "bytes": size, "sha256": digest} for role, path, size, digest in fields}


def _literal_result():
    cert = _literal_certificate()
    arithmetic = {"alpha": "1/8", "scaled_numerator": "125", "scaled_denominator": "1", "on_grid": True}
    domain = {key: cert[key] for key in ("schema", "seed", "parent_size", "potential", "component_order")}
    domain.update(component_count=109, grid_denominator=1000)
    return {"schema": "ri159-final-witness-grid-result-v1", "status": "GRID_PASS",
            "domain": domain, "inputs": _literal_inputs(),
            "root_order_basis": "INHERITED_PINNED_RI41_ACCEPTANCE_NOT_RECONSTRUCTED",
            "default": dict(arithmetic), "override_indices": [],
            "components": [{"index": index, "root": [index, 0, 0], "origin": "default", **arithmetic}
                           for index in range(109)],
            "counts": {"components": 109, "defaulted": 109, "overridden": 0, "on_grid": 109, "off_grid": 0},
            "off_grid_indices": [], "scope": "GRID_ONLY_NOT_LAW_CAPACITY_W_H30_OR_PHYSICAL_ACCEPTANCE"}


def _authority_probe(module, implementation, scenario):
    cert = _literal_certificate()
    if scenario == "different":
        cert["overrides"] = {"0": "1/3"}
    if implementation == "checker":
        return _capture(lambda: module.reconstruct_certificate(module.decode_certificate(_encode(cert))),
                        module.GridRefused)
    return _capture(lambda: module.audit_arguments(_encode(cert), _encode(_literal_result())), module.AuditRefusal)


def _authority_expected(implementation, scenario):
    if scenario == "different":
        return _refusal("AuditRefusal", "AUDIT_RESULT_VALUE", "saved-result value differs at result.components[0].alpha")
    if implementation == "checker":
        value = _literal_result()
        for key in ("schema", "inputs", "root_order_basis", "scope"):
            del value[key]
        return {"kind": "return", "value": value}
    return {"kind": "return", "value": {
        "schema": "ri159-grid-saved-audit-verdict-v1", "status": "MATCH", "reported_grid_status": "GRID_PASS",
        "components_compared": 109, "comparison": "ALL_RESULT_FIELDS_EXACT_TYPE_SENSITIVE_RECOMPUTATION",
        "boundary": "DIRECT_ARGUMENTS_NOT_AUTHENTICATED",
        "root_order_basis": "INHERITED_PINNED_RI41_ACCEPTANCE_NOT_RECONSTRUCTED",
        "scope": "GRID_ONLY_NOT_LAW_CAPACITY_W_H30_OR_PHYSICAL_ACCEPTANCE"}}


def _reported(value):
    raw = _encode(value)
    _need(len(raw) <= 8192 or (type(value) is dict and value.get("kind") == "return"),
          "compound observation exceeded its diagnostic bound")
    subject = value.get("subject", value) if type(value) is dict else {}
    refused = type(subject) is dict and subject.get("kind") == "refusal"
    return {"outcome": "subject_refusal_probe" if refused else "return_probe",
            "exception_type": subject.get("exception_type") if refused else None,
            "code": subject.get("code") if refused else None,
            # Full scientific positive template is compared before hashing;
            # operational records retain every bounded call/error/capture detail.
            "message": raw.decode("ascii") if len(raw) <= 8192 else None,
            "output_sha256": hashlib.sha256(raw).hexdigest()}


def run_controls(checker, auditor):
    """Later-admitted execution only. Preserve FAIL records and try later cases."""
    records = []
    originals = (deepcopy(checker.FIXED_IDENTITIES), deepcopy(auditor.PINNED_FILES))
    for identity, family, implementation, kind, argument in _plan():
        module = checker if implementation == "checker" else auditor
        expected = None
        observed = None
        compared = False
        try:
            if kind == "read":
                expected = _read_expected(implementation, argument)
                observed = _read_probe(module, implementation, argument)
            elif kind == "pin":
                expected = _pin_expected(implementation, *argument)
                observed = _pin_probe(module, implementation, *argument)
            elif kind == "post":
                expected = _post_expected(implementation, argument)
                observed = _post_probe(module, implementation, argument)
            elif kind == "main":
                expected = _main_expected(implementation, argument)
                observed = _main_probe(module, implementation, argument)
            else:
                expected = _authority_expected(implementation, argument)
                observed = _authority_probe(module, implementation, argument)
            passed = _same(expected, observed)
            compared = True
            wanted, actual = _reported(expected), _reported(observed)
        except Exception as error:
            passed = False
            wanted = _reported(expected) if expected is not None else {
                "outcome": "harness_setup", "exception_type": None, "code": None,
                "message": None, "output_sha256": None}
            actual = {"outcome": "harness_error", "exception_type": type(error).__name__,
                      "code": None, "message": str(error)[:512], "output_sha256": None}
        if not (_same(originals[0], checker.FIXED_IDENTITIES)
                and _same(originals[1], auditor.PINNED_FILES)):
            raise FaultFailure("protected production pins changed", records)
        records.append({"id": identity, "family": family, "implementation": implementation,
                        "status": "PASS" if passed else "FAIL", "boundary": BOUNDARY,
                        "expected": wanted, "observed": actual,
                        "full_output_compared": compared})
    return records
