#!/usr/bin/env python3
"""RI161 source-only, future admitted synthetic qualification caller.

No request, interpreter, fixture, execution or qualification is supplied by
saving this source. The external root must authenticate this exact source,
the request, the interpreter AND its stdlib/bootstrap before starting:
  INTERPRETER -I -S -B caller.py --request ABS --request-sha256 SHA256
The request pins this source; this source does not pin the request (no hash
cycle). Self-rereads are finite custody checks, not proof of executed bytes,
interpreter dependencies, external admission or uninterrupted path custody.

Exactly two bounded children execute synthetic controls, never actual fixed
certificate production. Children use -I -S -B, plus -O in optimized mode.
Limits: 120s per child INCLUDING 2s reserved cleanup; 300s whole caller;
8MiB each captured stream and child report; child AS512MiB and CPU110s.
AS is an address-space rlimit, NOT an RSS monitor. Unsupported host limits
refuse. External root/tool custody remains required for kernel stalls, hard
aborts, missing tails and the bootstrap before this Python source executes.
No receipt can manufacture genuine external-tool completion or admission.
"""

import copy  # Preload the reviewed control/subject stdlib before import guards.
import contextlib
from fractions import Fraction
import hashlib
import importlib.util
import io
import json
import os
import posixpath
import re
import resource
import selectors
import signal
import stat
import subprocess
import sys
import time
import types


BASE = "/Volumes/AI_DATA/development/det-review-evidence/ri161-grid-qualification-source-679wwadg"
OLD = "/Volumes/AI_DATA/development/det-review-evidence/ri159-final-witness-grid-source-47ofu03n"
PATHS = {"caller": BASE + "/caller.py", "qualify": BASE + "/qualify_grid.py",
         "fault": BASE + "/fault_cases.py", "checker": OLD + "/grid_check.py",
         "auditor": OLD + "/grid_audit.py"}
SUBJECT_PINS = {
    "checker": {"path": PATHS["checker"], "bytes": 16091,
                "sha256": "cf9e50b061d2fcb6a040e2b1a4ce367dc802f003b0307333d561295782d87982"},
    "auditor": {"path": PATHS["auditor"], "bytes": 22760,
                "sha256": "aa0571ec5d7705367732a8579165429a9abf99c17dbf38798f8ac8d742b70277"},
}
ROLES = ("caller", "qualify", "fault", "checker", "auditor")
STREAM_LIMIT = 8 * 1024 * 1024
SOURCE_LIMIT = 2 * 1024 * 1024
REQUEST_LIMIT = 65536
RECEIPT_LIMIT = 262144
CASE_LIMIT = 10000
NS = 1000000000
CHILD_NS = 120 * NS
CLEANUP_NS = 2 * NS
TOTAL_SECONDS = 300
SCOPE = "SYNTHETIC_QUALIFICATION_ONLY_NOT_ACTUAL_GRID_OR_SCIENCE_ACCEPTANCE"


class Refusal(Exception):
    pass


class HardStop(BaseException):
    pass


def need(condition, message):
    if not condition:
        raise Refusal(message)


def encoded(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def same(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(same(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
    return left == right


def strict_json(raw, limit):
    need(type(raw) is bytes and 0 < len(raw) <= limit, "JSON byte bound")
    quoted = escaped = False
    depth = 0
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
            need(depth <= 16, "JSON depth bound")
        elif byte in (93, 125):
            depth -= 1
            need(depth >= 0, "JSON delimiter bound")
    need(not quoted and depth == 0, "incomplete JSON")

    def pairs(items):
        answer = {}
        for key, value in items:
            need(key not in answer, "duplicate JSON key")
            answer[key] = value
        return answer

    def integer(token):
        need(len(token.lstrip("-")) <= 20, "JSON integer bound")
        return int(token)

    def forbidden(_):
        raise Refusal("floating and nonfinite JSON forbidden")

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_int=integer, parse_float=forbidden, parse_constant=forbidden)


def state(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_uid, info.st_gid, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def path_check(path, directory=False):
    need(type(path) is str and 0 < len(path) <= 4096 and "\0" not in path
         and path.startswith("/") and not path.startswith("//")
         and os.path.normpath(path) == path, "absolute normalized path required")
    parts = path.split("/")[1:]
    need(0 < len(parts) <= 128 and all(parts), "path component bound")
    current = ""
    ancestors = []
    for n, part in enumerate(parts):
        current += "/" + part
        info = os.lstat(current)
        if n + 1 < len(parts) or directory:
            need(stat.S_ISDIR(info.st_mode), "nonsymlink directory required")
            ancestors.append((current, info.st_dev, info.st_ino, info.st_mode))
        else:
            need(stat.S_ISREG(info.st_mode), "nonsymlink regular file required")
    need(os.path.realpath(path) == path, "realpath differs")
    return state(info), tuple(ancestors)


def read_file(path, limit):
    before_path, ancestors = path_check(path)
    fd = None
    primary = None
    raw = None
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        before = os.fstat(fd)
        need(state(before) == before_path and before.st_size <= limit,
             "opened file state or size differs")
        chunks = []
        size = 0
        while True:
            chunk = os.read(fd, min(65536, limit + 1 - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
            need(size <= limit, "read byte bound")
        after_path, after_ancestors = path_check(path)
        need(state(os.fstat(fd)) == before_path == after_path
             and ancestors == after_ancestors, "file changed during read")
        raw = b"".join(chunks)
        need(len(raw) == before.st_size, "captured size differs")
    except Exception as error:
        primary = error
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except Exception as error:
                if primary is None:
                    primary = error
                else:
                    primary = Refusal("read failed: " + type(primary).__name__ +
                                      "; close also failed: " + type(error).__name__)
    if primary is not None:
        raise primary
    return raw, before_path


def identity_shape(pin, maximum):
    need(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"}, "identity keys")
    need(type(pin["bytes"]) is int and 0 < pin["bytes"] <= maximum, "identity size")
    need(type(pin["sha256"]) is str and re.fullmatch("[0-9a-f]{64}", pin["sha256"]),
         "identity digest")
    need(type(pin["path"]) is str, "identity path type")


def pinned(pin, maximum):
    identity_shape(pin, maximum)
    raw, observed = read_file(pin["path"], pin["bytes"])
    need(len(raw) == pin["bytes"] and digest(raw) == pin["sha256"], "whole-file pin differs")
    return raw, observed


def request_read(path, sha):
    need(type(sha) is str and re.fullmatch("[0-9a-f]{64}", sha), "request SHA256 syntax")
    raw, snapshot = read_file(path, REQUEST_LIMIT)
    need(digest(raw) == sha, "request pin differs")
    req = strict_json(raw, REQUEST_LIMIT)
    need(type(req) is dict and set(req) == {"schema", "nonce", "interpreter", "sources",
                                          "output_directory", "trust_basis"}, "request keys")
    need(req["schema"] == "ri161-qualification-request-v1", "request schema")
    need(type(req["nonce"]) is str and re.fullmatch("[0-9a-f]{32}", req["nonce"]), "nonce")
    identity_shape(req["interpreter"], 256 * 1024 * 1024)
    need(type(req["sources"]) is dict and set(req["sources"]) == set(ROLES), "source roles")
    for role in ROLES:
        identity_shape(req["sources"][role], SOURCE_LIMIT)
        need(req["sources"][role]["path"] == PATHS[role], "source path substitution forbidden")
    for role, value in SUBJECT_PINS.items():
        need(same(req["sources"][role], value), "immutable subject pin substitution forbidden")
    basis = req["trust_basis"]
    need(type(basis) is dict and set(basis) == {"admission_reference", "stdlib_basis",
             "external_bootstrap_required", "qualification_only"}, "trust basis keys")
    for key in ("admission_reference", "stdlib_basis"):
        need(type(basis[key]) is str and 0 < len(basis[key]) <= 2048, "external trust reference")
    need(basis["external_bootstrap_required"] is True and basis["qualification_only"] is True,
         "external bootstrap and synthetic scope must be explicit")
    need(type(req["output_directory"]) is str, "output directory type")
    need(os.path.abspath(__file__) == PATHS["caller"], "caller source location differs")
    need(sys.executable == req["interpreter"]["path"], "running executable pathname differs")
    return req, (raw, snapshot)


def all_pins(req):
    answer = {"interpreter": pinned(req["interpreter"], 256 * 1024 * 1024)}
    for role in ROLES:
        answer[role] = pinned(req["sources"][role], SOURCE_LIMIT)
    return answer


def add_error(errors, stage, error):
    if len(errors) < 32:
        errors.append({"stage": stage[:80], "type": type(error).__name__,
                       "message": str(error)[:240]})
    elif len(errors) == 32:
        errors.append({"stage": "overflow", "type": "ErrorBound",
                       "message": "additional failures omitted; result remains failed"})


def recheck(req, path, sha, baseline, request_baseline, errors):
    # Independent ordinary attempts; first failure does not suppress later pins.
    for role in ("interpreter",) + ROLES:
        try:
            pin = req["interpreter"] if role == "interpreter" else req["sources"][role]
            again = pinned(pin, 256 * 1024 * 1024 if role == "interpreter" else SOURCE_LIMIT)
            need(again == baseline[role], "source/interpreter state drift")
        except Exception as error:
            add_error(errors, "postcheck:" + role, error)
    try:
        _req, again = request_read(path, sha)
        need(again == request_baseline, "request state drift")
    except Exception as error:
        add_error(errors, "postcheck:request", error)


def flags_for(mode):
    return {"optimize": 1 if mode == "optimized" else 0, "isolated": 1,
            "no_site": 1, "dont_write_bytecode": True}


def current_flags():
    return {"optimize": sys.flags.optimize, "isolated": sys.flags.isolated,
            "no_site": sys.flags.no_site, "dont_write_bytecode": sys.dont_write_bytecode}


def descriptor(case_id, family, implementation, boundary):
    return {"id": case_id, "family": family, "implementation": implementation,
            "boundary": boundary}


def observation(output):
    return {"outcome": "RETURN", "exception_type": None, "code": None,
            "message": encoded(output).decode("ascii").rstrip("\n"),
            "output_sha256": digest(encoded(output))}


def caller_catalogue():
    result = []
    for implementation in ("checker", "auditor"):
        result.append(descriptor("P10-" + implementation, "P10", implementation,
                                 "authenticated_module_import_without_main_or_side_effects"))
        result.append(descriptor("P11-" + implementation, "P11", implementation,
                                 "actual_child_interpreter_flags"))
    return result


def catalogue_check(catalogue):
    need(type(catalogue) is list and 0 < len(catalogue) <= CASE_LIMIT, "catalogue size/type")
    identifiers = set()
    for row in catalogue:
        need(type(row) is dict and set(row) == {"id", "family", "implementation", "boundary"},
             "catalogue keys")
        need(all(type(v) is str and 0 < len(v) <= 240 for v in row.values()), "catalogue strings")
        need(row["implementation"] in ("checker", "auditor"), "catalogue implementation")
        need(row["id"] not in identifiers, "duplicate case identifier")
        identifiers.add(row["id"])


def records_check(catalogue, records, complete):
    catalogue_check(catalogue)
    need(type(records) is list and len(records) <= len(catalogue), "record count/type")
    if complete:
        need(len(records) == len(catalogue), "missing case records")
    lookup = {row["id"]: row for row in catalogue}
    seen = set()
    for row in records:
        need(type(row) is dict and set(row) == {"id", "family", "implementation", "boundary",
             "status", "expected", "observed", "full_output_compared"}, "record keys")
        key = row["id"]
        need(key in lookup and key not in seen, "unexpected/duplicate case record")
        need(same({k: row[k] for k in lookup[key]}, lookup[key]), "case metadata drift")
        seen.add(key)
        need(type(row["status"]) is str and row["status"] in ("PASS", "FAIL"), "case status")
        need(type(row["full_output_compared"]) is bool, "full-output flag type")
        for side in ("expected", "observed"):
            value = row[side]
            need(type(value) is dict and set(value) == {"outcome", "exception_type", "code",
                 "message", "output_sha256"}, "observation keys")
            need(type(value["outcome"]) is str and 0 < len(value["outcome"]) <= 40, "outcome type")
            for field in ("exception_type", "code", "message", "output_sha256"):
                need(value[field] is None or (type(value[field]) is str and len(value[field]) <= 8192),
                     "observation field bound")
            if value["output_sha256"] is not None:
                need(re.fullmatch("[0-9a-f]{64}", value["output_sha256"]), "output hash syntax")
        if row["status"] == "PASS":
            need(same(row["expected"], row["observed"]), "PASS observations differ")
            need(row["expected"]["outcome"] in
                 ("RETURN", "REFUSED", "return_probe", "subject_refusal_probe"), "PASS outcome")
            if row["expected"]["outcome"] != "REFUSED":
                need(row["full_output_compared"] is True, "return PASS lacks full comparison")


class CapturedLoader:
    """Importlib loader of already authenticated source, with no file/cache I/O."""
    def __init__(self, raw, path):
        self.raw, self.path = raw, path

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        exec(compile(self.raw, self.path, "exec", dont_inherit=True), module.__dict__)


def load_module(role, raw):
    name = "ri161_authenticated_" + role
    loader = CapturedLoader(raw, PATHS[role])
    spec = importlib.util.spec_from_loader(name, loader, origin=PATHS[role])
    module = importlib.util.module_from_spec(spec)
    module.__file__ = PATHS[role]
    loader.exec_module(module)
    return module


class ChildGuard:
    """Observable guard for reviewed code, not a hostile-code security sandbox."""
    def __init__(self):
        self.importing = False
        self.events = []

    def audit(self, event, args):
        blocked = (event == "open" or event.startswith("subprocess.") or
                   event.startswith("socket.") or event in {
                       "os.system", "os.fork", "os.forkpty", "os.posix_spawn", "os.exec",
                       "os.remove", "os.rename", "os.mkdir", "os.rmdir", "os.symlink",
                       "os.link", "os.chmod", "os.chown", "os.truncate", "os.utime"})
        # All controls are argument-only/doubles. No real child filesystem opens
        # are allowed between authenticated loading and the later pin rereads.
        if self.importing and blocked:
            if len(self.events) < 32:
                self.events.append(event)
            raise Refusal("guarded real filesystem/process/network operation: " + event)


class ImportOutput(io.StringIO):
    def write(self, value):
        need(type(value) is str and self.tell() + len(value) <= 8192, "import output exceeds bound")
        return super().write(value)


def child_report(req, path, sha, mode, baseline, request_baseline):
    errors, records, catalogue = [], [], []
    guard = ChildGuard()
    sys.addaudithook(guard.audit)
    checker = auditor = None
    try:
        guard.importing = True
        imports = {}
        for role in ("checker", "auditor"):
            stdout, stderr = ImportOutput(), ImportOutput()
            oldout, olderr = sys.stdout, sys.stderr
            start = len(guard.events)
            calls = []
            need(sys.getprofile() is None, "preexisting profile hook is not replaced")

            def import_profile(frame, event, _argument):
                if (event == "call" and frame.f_code.co_filename == PATHS[role]
                        and frame.f_code.co_name == "main"):
                    calls.append("main")
                    need(len(calls) <= 1, "import repeated main entry")

            try:
                sys.stdout, sys.stderr = stdout, stderr
                sys.setprofile(import_profile)
                imports[role] = load_module(role, baseline[role][0])
            finally:
                sys.setprofile(None)
                sys.stdout, sys.stderr = oldout, olderr
            actual = {"stdout": stdout.getvalue(), "stderr": stderr.getvalue(),
                      "blocked_events": guard.events[start:], "main_calls": calls}
            expected = {"stdout": "", "stderr": "", "blocked_events": [], "main_calls": []}
            meta = descriptor("P10-" + role, "P10", role,
                              "authenticated_module_import_without_main_or_side_effects")
            records.append({**meta, "status": "PASS" if same(actual, expected) else "FAIL",
                            "expected": observation(expected), "observed": observation(actual),
                            "full_output_compared": True})
            meta = descriptor("P11-" + role, "P11", role, "actual_child_interpreter_flags")
            actual_flags = current_flags()
            records.append({**meta, "status": "PASS" if same(actual_flags, flags_for(mode)) else "FAIL",
                            "expected": observation(flags_for(mode)), "observed": observation(actual_flags),
                            "full_output_compared": True})
        checker, auditor = imports["checker"], imports["auditor"]
        suites = {role: load_module(role, baseline[role][0]) for role in ("qualify", "fault")}
        suite_catalogues = {}
        catalogue = caller_catalogue()
        for role in ("qualify", "fault"):
            declared = suites[role].case_catalogue()
            need(type(declared) in (list, tuple), "suite catalogue container")
            declared = list(declared)
            catalogue_check(declared)
            suite_catalogues[role] = declared
            catalogue.extend(declared)
        catalogue_check(catalogue)
        for role in ("qualify", "fault"):
            try:
                result = suites[role].run_controls(checker, auditor)
                need(type(result) is list, "suite result must be list")
                records_check(suite_catalogues[role], result, True)
                records.extend(result)
            except Exception as error:
                add_error(errors, "suite:" + role, error)
                partial = getattr(error, "records", None)
                if partial is not None:
                    try:
                        records_check(suite_catalogues[role], partial, False)
                        need([row["id"] for row in partial] ==
                             [row["id"] for row in suite_catalogues[role][:len(partial)]],
                             "partial suite is not its declared prefix")
                        records.extend(partial)
                    except Exception as later:
                        add_error(errors, "partial_suite:" + role, later)
        need(not guard.events, "a real protected operation was attempted by a control")
        records_check(catalogue, records, not errors)
    except Exception as error:
        add_error(errors, "child_controls", error)
    finally:
        guard.importing = False
    recheck(req, path, sha, baseline, request_baseline, errors)
    passed = sum(row.get("status") == "PASS" for row in records)
    failed = len(records) - passed
    status = "PASS" if not errors and failed == 0 and len(records) == len(catalogue) else "FAIL"
    return {"schema": "ri161-qualification-child-v1", "status": status,
            "nonce": req["nonce"], "mode": mode, "request_sha256": sha,
            "source_pins": req["sources"], "interpreter": req["interpreter"],
            "flags": current_flags(), "catalogue": catalogue, "records": records,
            "summary": {"total": len(records), "passed": passed, "failed": failed}, "errors": errors}


def child_main(path, sha, mode):
    need(mode in ("normal", "optimized"), "child mode")
    need(same(current_flags(), flags_for(mode)), "child interpreter flags differ")
    need(os.name == "posix", "POSIX ownership and limits required")
    # Actual future limit installation must succeed, otherwise no controls run.
    for limit, value in ((resource.RLIMIT_AS, 512 * 1024 * 1024),
                         (resource.RLIMIT_CPU, 110), (resource.RLIMIT_CORE, 0)):
        resource.setrlimit(limit, (value, value))
        need(resource.getrlimit(limit) == (value, value), "installed resource limit differs")
    req, request_baseline = request_read(path, sha)
    baseline = all_pins(req)
    report = child_report(req, path, sha, mode, baseline, request_baseline)
    raw = encoded(report)
    need(len(raw) <= STREAM_LIMIT, "child report exceeds bound")
    count = sys.stdout.buffer.write(raw)
    need(type(count) is int and count == len(raw), "child report short write")
    sys.stdout.buffer.flush()
    return 0 if report["status"] == "PASS" else 2


def write_all(fd, raw):
    offset = 0
    while offset < len(raw):
        count = os.write(fd, raw[offset:])
        need(type(count) is int and count > 0, "capture write made no progress")
        offset += count


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    primary = None
    try:
        os.fsync(fd)
    except Exception as error:
        primary = error
    try:
        os.close(fd)
    except Exception as error:
        if primary is None:
            primary = error
        else:
            raise Refusal("directory sync and close both failed") from primary
    if primary is not None:
        raise primary


def save_new(path, value):
    raw = encoded(value)
    need(len(raw) <= RECEIPT_LIMIT, "receipt bound")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    primary = None
    try:
        write_all(fd, raw)
        os.fsync(fd)
    except Exception as error:
        primary = error
    try:
        os.close(fd)
    except Exception as error:
        if primary is None:
            primary = error
        else:
            raise Refusal("receipt write/sync and close both failed") from primary
    if primary is not None:
        raise primary
    sync_directory(os.path.dirname(path))
    return {"path": path, "bytes": len(raw), "sha256": digest(raw)}


def validate_report(raw, req, sha, mode):
    report = strict_json(raw, STREAM_LIMIT)
    need(type(report) is dict and set(report) == {"schema", "status", "nonce", "mode",
         "request_sha256", "source_pins", "interpreter", "flags", "catalogue", "records",
         "summary", "errors"}, "child report keys")
    need(report["schema"] == "ri161-qualification-child-v1" and report["status"] == "PASS",
         "child report did not pass")
    for key, expected in (("nonce", req["nonce"]), ("mode", mode), ("request_sha256", sha),
                          ("source_pins", req["sources"]), ("interpreter", req["interpreter"]),
                          ("flags", flags_for(mode)), ("errors", [])):
        need(same(report[key], expected), "child report binding differs: " + key)
    records_check(report["catalogue"], report["records"], True)
    need(all(row["status"] == "PASS" for row in report["records"]), "case failure")
    total = len(report["records"])
    need(same(report["summary"], {"total": total, "passed": total, "failed": 0}), "child counts")
    own = {row["id"]: row for row in caller_catalogue()}
    actual = {row["id"]: row for row in report["catalogue"]}
    need(all(key in actual and same(actual[key], row) for key, row in own.items()), "P10/P11 missing")
    families = {row["family"] for row in report["catalogue"]}
    expected_families = ({"Q%02d" % n for n in range(1, 36)} |
                         {"R%02d" % n for n in range(1, 17)} |
                         {"P%02d" % n for n in range(1, 13)})
    need(families == expected_families, "exact Q/R/P family coverage differs")
    for index in range(109):
        label = str(index).zfill(3)
        for implementation in ("checker", "auditor"):
            key = "Q05." + label + "." + implementation
            need(key in actual and actual[key]["family"] == "Q05"
                 and actual[key]["implementation"] == implementation, "Q05 complete sweep missing")
        for field in ("index", "origin", "root.0", "root.1", "root.2"):
            key = "R07." + label + "." + field + ".auditor"
            need(key in actual and actual[key]["family"] == "R07"
                 and actual[key]["implementation"] == "auditor", "R07 complete sweep missing")
        for field in ("alpha", "scaled_numerator", "scaled_denominator", "on_grid"):
            key = "R08." + label + "." + field + ".auditor"
            need(key in actual and actual[key]["family"] == "R08"
                 and actual[key]["implementation"] == "auditor", "R08 complete sweep missing")
    return report


def group_exists(pgid):
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False


def run_mode(req, path, sha, mode, outer_deadline):
    start = time.monotonic_ns()
    deadline = min(start + CHILD_NS, outer_deadline)
    work_deadline = deadline - CLEANUP_NS
    directory = req["output_directory"]
    command = [req["interpreter"]["path"], "-I", "-S", "-B"]
    if mode == "optimized":
        command.append("-O")
    command += [PATHS["caller"], "--child", mode, "--request", path, "--request-sha256", sha]
    result = {"schema": "ri161-owned-child-receipt-v1", "mode": mode, "command": command,
              "start_monotonic_ns": start, "deadline_monotonic_ns": deadline,
              "pid": None, "pgid": None, "returncode": None, "reaped": False,
              "terminal_group_empty": False, "complete": False, "status": "FAILED",
              "streams": {}, "errors": []}
    errors = result["errors"]
    process = selector = None
    captures = {}
    pipes = {}
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    report = None
    hard_abort = False
    try:
        save_new(directory + "/" + mode + ".start.json", result)
        for name in ("stdout", "stderr"):
            filename = directory + "/" + mode + "." + name + ".bin"
            fd = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            captures[name] = fd
            result["streams"][name] = {"path": filename, "bytes": 0, "sha256": None,
                                        "eof": False, "overflow": False, "overflow_byte": None,
                                        "durable_close": False}
        sync_directory(directory)
        need(time.monotonic_ns() < work_deadline, "child startup deadline")
        selector = selectors.DefaultSelector()
        process = subprocess.Popen(command, cwd=directory, env={"LC_ALL": "C", "LANG": "C"},
                                   stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, start_new_session=True, close_fds=True)
        result["pid"] = process.pid
        result["pgid"] = process.pid
        need(os.getpgid(process.pid) == process.pid, "child is not its owned group leader")
        for name in ("stdout", "stderr"):
            pipe = getattr(process, name)
            pipes[name] = pipe
            os.set_blocking(pipe.fileno(), False)
            selector.register(pipe, selectors.EVENT_READ, name)
        killing = False
        while True:
            now = time.monotonic_ns()
            if now >= work_deadline and not killing:
                add_error(errors, "deadline", Refusal("118-second work budget expired"))
                killing = True
            if errors:
                killing = True
            if killing:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                except Exception as error:
                    add_error(errors, "killpg", error)
                # Kill is idempotent; at most twenty samples/second, bounded
                # error list and the same original cleanup deadline throughout.
            returncode = process.poll()  # Actual nonblocking waitpid/reap.
            if returncode is not None:
                result["returncode"] = returncode
                result["reaped"] = True
            if result["reaped"] and not selector.get_map():
                break
            if now >= deadline:
                add_error(errors, "cleanup_deadline", Refusal("bounded cleanup incomplete"))
                break
            timeout = min(0.05, max(0, (deadline - now) / NS))
            for key, _mask in selector.select(timeout):
                name = key.data
                stream = result["streams"][name]
                try:
                    chunk = os.read(key.fileobj.fileno(), min(65536, STREAM_LIMIT + 1 - len(buffers[name])))
                    if not chunk:
                        stream["eof"] = True
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
                        pipes.pop(name, None)
                        continue
                    room = STREAM_LIMIT - len(buffers[name])
                    kept = chunk[:room]
                    buffers[name].extend(kept)
                    if kept:
                        write_all(captures[name], kept)
                    if len(chunk) > room:
                        stream["overflow"] = True
                        stream["overflow_byte"] = chunk[room]
                        add_error(errors, name, Refusal("capture stream cap exceeded"))
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
                        pipes.pop(name, None)
                except BlockingIOError:
                    continue
                except Exception as error:
                    add_error(errors, "drain:" + name, error)
                    # Stop a faulty pump, retaining other stream independently.
                    try:
                        selector.unregister(key.fileobj)
                    except Exception as later:
                        add_error(errors, "unregister:" + name, later)
                    try:
                        key.fileobj.close()
                    except Exception as later:
                        add_error(errors, "pipe_close:" + name, later)
                    pipes.pop(name, None)
        if result["reaped"]:
            result["terminal_group_empty"] = not group_exists(process.pid)
        need(result["reaped"] and result["terminal_group_empty"], "owned group cleanup incomplete")
        need(result["returncode"] == 0, "child returned nonzero")
        need(all(row["eof"] and not row["overflow"] for row in result["streams"].values()),
             "capture did not complete both streams")
        need(not buffers["stderr"], "child stderr is nonempty")
        need(not errors, "child monitor failed")
        report = validate_report(bytes(buffers["stdout"]), req, sha, mode)
    except Exception as error:
        add_error(errors, "owned_child", error)
    except BaseException:
        hard_abort = True
        raise
    finally:
        # On hard abort: known-handle nonblocking kill/close only, no receipt,
        # fsync, polling, invented reaping or new cleanup budget.
        if process is not None and (hard_abort or not result["reaped"] or errors):
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except Exception as error:
                if not hard_abort and not isinstance(error, ProcessLookupError):
                    add_error(errors, "finally_kill", error)
        for name, pipe in list(pipes.items()):
            try:
                pipe.close()
            except Exception as error:
                if not hard_abort:
                    add_error(errors, "finally_pipe_close:" + name, error)
        if selector is not None:
            try:
                selector.close()
            except Exception as error:
                if not hard_abort:
                    add_error(errors, "selector_close", error)
        for name, fd in captures.items():
            durable = not hard_abort
            if not hard_abort:
                try:
                    os.fsync(fd)
                except Exception as error:
                    durable = False
                    add_error(errors, "capture_sync:" + name, error)
            try:
                os.close(fd)
            except Exception as error:
                durable = False
                if not hard_abort:
                    add_error(errors, "capture_close:" + name, error)
            if not hard_abort:
                result["streams"][name]["durable_close"] = durable
                try:
                    actual, _snapshot = read_file(result["streams"][name]["path"], STREAM_LIMIT)
                    result["streams"][name].update({"bytes": len(actual), "sha256": digest(actual)})
                    need(actual == bytes(buffers[name]), "capture file differs from drained bytes")
                except Exception as error:
                    add_error(errors, "capture_identity:" + name, error)
        if not hard_abort:
            # An unexpected selector/setup error still gets a bounded genuine
            # reap attempt, but never a blocking wait beyond the original limit.
            if process is not None and not result["reaped"]:
                while time.monotonic_ns() < deadline:
                    code = process.poll()
                    if code is not None:
                        result["returncode"], result["reaped"] = code, True
                        break
                    time.sleep(min(0.01, max(0, (deadline - time.monotonic_ns()) / NS)))
            if process is not None and result["reaped"]:
                try:
                    result["terminal_group_empty"] = not group_exists(process.pid)
                except Exception as error:
                    add_error(errors, "terminal_group_check", error)
            result["end_monotonic_ns"] = time.monotonic_ns()
            if result["end_monotonic_ns"] > deadline:
                add_error(errors, "finish_deadline", Refusal("child total deadline exceeded"))
            result["complete"] = (result["reaped"] and result["terminal_group_empty"] and
                len(result["streams"]) == 2 and all(row["eof"] and row["durable_close"] and
                not row["overflow"] for row in result["streams"].values()))
            result["status"] = "PASS" if result["complete"] and not errors and report is not None else "FAILED"
            save_new(directory + "/" + mode + ".finish.json", result)
    return result, report


def stop_signal(number, _frame):
    raise HardStop("external signal " + str(number))


def parent_main(path, sha):
    need(same(current_flags(), flags_for("normal")), "parent requires -I -S -B without -O")
    need(os.name == "posix", "POSIX host required")
    for feature in ("O_NOFOLLOW", "O_NONBLOCK", "O_DIRECTORY"):
        need(hasattr(os, feature), "missing required open flag")
    start = time.monotonic_ns()
    deadline = start + TOTAL_SECONDS * NS
    old_handlers = {}
    old_timer = signal.getitimer(signal.ITIMER_REAL)
    need(old_timer == (0.0, 0.0), "existing alarm is not replaced")
    results, reports, errors = [], [], []
    baseline = req = request_baseline = None
    directory = None
    hard_abort = False
    try:
        for number in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGALRM):
            old_handlers[number] = signal.getsignal(number)
            signal.signal(number, stop_signal)
        signal.setitimer(signal.ITIMER_REAL, TOTAL_SECONDS)
        req, request_baseline = request_read(path, sha)
        baseline = all_pins(req)
        output = req["output_directory"]
        need(type(output) is str and os.path.normpath(output) == output
             and output.startswith("/") and not output.startswith("//")
             and len(output) <= 4096 and "\0" not in output, "new output path syntax")
        parent = os.path.dirname(output)
        path_check(parent, directory=True)
        need(output not in [pin["path"] for pin in req["sources"].values()], "output/source overlap")
        os.mkdir(output, 0o700)  # Exclusive new namespace; never remove old data.
        directory = output
        path_check(directory, directory=True)
        sync_directory(parent)
        save_new(directory + "/caller.start.json", {"schema": "ri161-caller-start-v1",
                 "nonce": req["nonce"], "request_sha256": sha, "request_path": path,
                 "source_pins": req["sources"], "interpreter": req["interpreter"],
                 "trust_basis": req["trust_basis"], "pid": os.getpid(),
                 "start_monotonic_ns": start, "deadline_monotonic_ns": deadline, "scope": SCOPE})
        for mode in ("normal", "optimized"):
            try:
                recheck(req, path, sha, baseline, request_baseline, errors)
                need(not errors, "prechild source/request drift")
                result, report = run_mode(req, path, sha, mode, deadline)
                results.append(result)
                reports.append(report)
            except Exception as error:
                add_error(errors, "mode:" + mode, error)
        if len(reports) == 2 and all(report is not None for report in reports):
            need(same(reports[0]["catalogue"], reports[1]["catalogue"]), "mode catalogue mismatch")
            # P11 intentionally observes different optimize flags. All other
            # expected/observed results must agree across normal and -O.
            left = [row for row in reports[0]["records"] if row["family"] != "P11"]
            right = [row for row in reports[1]["records"] if row["family"] != "P11"]
            need(same(left, right), "normal/optimized case result mismatch")
    except Exception as error:
        add_error(errors, "caller", error)
    except BaseException:
        hard_abort = True
        raise
    finally:
        try:
            if not hard_abort:
                if req is not None and baseline is not None:
                    recheck(req, path, sha, baseline, request_baseline, errors)
                passed = (not errors and len(results) == 2 and all(r["status"] == "PASS" for r in results))
                if time.monotonic_ns() >= deadline:
                    passed = False
                    add_error(errors, "total_deadline", Refusal("caller deadline exceeded"))
                if directory is not None:
                    save_new(directory + "/caller.finish.json", {"schema": "ri161-caller-finish-v1",
                             "status": "PASS" if passed else "FAILED", "errors": errors,
                             "modes": results, "scope": SCOPE, "nonce": req["nonce"],
                             "request_sha256": sha, "end_monotonic_ns": time.monotonic_ns()})
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            # Hard aborts may prevent later restoration. No receipt claims a
            # completed tail in that case; external root must record it.
            for number, handler in old_handlers.items():
                signal.signal(number, handler)
    return 0 if passed else 2


def main():
    try:
        args = sys.argv[1:]
        if len(args) == 4 and args[0] == "--request" and args[2] == "--request-sha256":
            return parent_main(args[1], args[3])
        if (len(args) == 6 and args[0] == "--child" and args[2] == "--request"
                and args[4] == "--request-sha256"):
            return child_main(args[3], args[5], args[1])
        raise Refusal("expected exact parent request arguments or owned child arguments")
    except Exception as error:
        diagnostic = encoded({"schema": "ri161-caller-refusal-v1", "status": "REFUSED",
                              "type": type(error).__name__, "message": str(error)[:1024]})
        try:
            count = sys.stderr.buffer.write(diagnostic)
            if type(count) is not int or count != len(diagnostic):
                return 2
            sys.stderr.buffer.flush()
        except Exception:
            pass  # Failure remains nonzero; root must retain missing diagnostics.
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
