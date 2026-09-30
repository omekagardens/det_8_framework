#!/usr/bin/env python3
"""Check RI139 published bytes and saved agreement without running archived code."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

ARCHIVE = 'gwosc_focused25_result_v1'
PUBLISHED_COMMIT = '878ef6041d937abd4ecdc7b0d4fa9adbc81a5005'
MANIFEST_BYTES = 25566
MANIFEST_SHA256 = 'da4ccad5e3f06e313ad0ba2a0b00b23c4a6aa7b5faaa6b28043c6259998024ee'
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_TOTAL_BYTES = 32 * 1024 * 1024
MAX_NAMES = 512


class InvalidArchive(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise InvalidArchive(message)


def pin(body):
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def pure(row):
    return {key: row[key] for key in ('bytes', 'sha256')}


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def reject_constant(value):
    raise InvalidArchive('nonfinite JSON constant: ' + value)


def decode(body):
    return json.loads(body.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=reject_constant)


def same(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(same(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
    return left == right


def relative(value):
    require(type(value) is str and value != '' and '\\' not in value and '\x00' not in value,
            'invalid relative path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and path.as_posix() == value
            and all(part not in ('', '.', '..') for part in path.parts), 'unsafe relative path')
    return value


def read_regular(path, size):
    require(type(size) is int and 0 <= size <= MAX_FILE_BYTES, 'file size bound')
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_size == size, 'nonregular or changed-size file: ' + str(path))
    fields = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        require(fields(opened) == fields(before), 'file changed on open')
        body = stream.read(size + 1)
        final = os.fstat(stream.fileno())
    require(fields(before) == fields(opened) == fields(final) == fields(path.lstat()), 'file changed during read')
    require(len(body) == size, 'read size mismatch')
    return body


def inventory(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'archive root must be a real directory')
    files, directories = set(), set()
    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in dirs:
            path = Path(directory)/name
            require(stat.S_ISDIR(path.lstat().st_mode), 'nonregular archive directory')
            directories.add(path.relative_to(root).as_posix())
        for name in names:
            path = Path(directory)/name
            require(stat.S_ISREG(path.lstat().st_mode), 'nonregular archive member')
            files.add(path.relative_to(root).as_posix())
        require(len(files) + len(directories) <= MAX_NAMES, 'archive namespace bound')
    return files, directories


def verify(root):
    files, directories = inventory(root)
    raw = read_regular(root/'PUBLICATION_MANIFEST.json', MANIFEST_BYTES)
    require(pin(raw)['sha256'] == MANIFEST_SHA256, 'pinned publication manifest differs')
    manifest = decode(raw)
    require(manifest['source_only'] is False and manifest['relocated_execution_authorized'] is False,
            'publication scope differs')
    rows = manifest['payload']
    require(type(rows) is list and len(rows) == 134 and manifest['exact_copies'] == 132, 'manifest counts')
    identities = {}
    for row in rows:
        require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'}, 'manifest row fields')
        name = relative(row['path'])
        require(name not in identities and type(row['bytes']) is int and 0 <= row['bytes'] <= MAX_FILE_BYTES
                and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}', row['sha256']), 'manifest row identity')
        identities[name] = pure(row)
    require(files == set(identities) | {'PUBLICATION_MANIFEST.json'}, 'complete archive file inventory differs')
    # Git does not store empty directories. Only directories implied by payload
    # names are allowed here; historical empty directories are checked below as
    # saved namespace records, not required to exist in this portable archive.
    expected_dirs = {p.as_posix() for name in files for p in PurePosixPath(name).parents if p.as_posix() != '.'}
    require(directories == expected_dirs, 'unexpected empty or other directory')
    require(sum(x['bytes'] for x in identities.values()) + MANIFEST_BYTES <= MAX_TOTAL_BYTES, 'total byte bound')
    bodies = {}
    for name, expected in identities.items():
        body = read_regular(root/name, expected['bytes'])
        require(same(pin(body), expected), 'payload bytes differ: ' + name)
        bodies[name] = body
    mapping = decode(bodies['DEPENDENCY_MAP.json'])
    copies = mapping['copies']
    require(len(copies) == 132 and mapping['complete_runtime_archive'] is False
            and mapping['all_transitive_dependencies_archived'] is False
            and mapping['relocated_execution_authorized'] is False, 'dependency scope')
    originals = {}
    for row in copies:
        name = relative(row['path'])
        require(name in identities and same(pure(row['original']), identities[name]), 'original-copy identity')
        require(row['original']['path'] not in originals, 'duplicate original path')
        originals[row['original']['path']] = name
    require(len({row['path'] for row in copies}) == 132, 'duplicate copy path')
    def saved_ref(row):
        require(row['path'] in originals, 'saved reference has no archived copy')
        name = originals[row['path']]
        require(same(pure(row), identities[name]), 'saved reference pin differs')
        return name
    # No original absolute path or dependency-map external/Git operand is opened.
    reconciliation = decode(bodies['root/ROOT_ACTUAL_RECONCILIATION.json'])
    namespace = reconciliation['complete_operation_namespace']
    operation_files, operation_dirs = set(), set()
    for row in namespace:
        name = relative(row['relative'])
        require(name not in operation_files | operation_dirs, 'duplicate operation entry')
        if row['kind'] == 'file':
            operation_files.add(name)
            require('operation/'+name in identities and same(pure(row), identities['operation/'+name]), 'operation file differs')
        else:
            require(row['kind'] == 'directory' and set(row) == {'relative', 'kind'}, 'operation entry kind')
            operation_dirs.add(name)
    require(len(operation_files) == 89 and operation_files == {name[len('operation/'):] for name in identities if name.startswith('operation/')}, 'complete operation files')
    for name in operation_files | operation_dirs:
        require(all(p.as_posix() in operation_dirs for p in PurePosixPath(name).parents if p.as_posix() != '.'), 'missing saved parent directory')
    require('environment/tmp' in operation_dirs, 'saved empty environment directory absent')
    accept = decode(bodies['root/RI139_ACTUAL_ROOT_ACCEPTANCE.json'])
    report = decode(bodies[saved_ref(accept['report'])])
    require(accept['status'] == 'ACCEPT_SINGLE_FOCUSED25_OUTCOME_UNDER_RETAINED_PREMISES', 'saved root decision')
    require(same(accept['counts'], dict(total=25, passed=25, positives=2, expected_refusals=23))
            and same(report['counts'], dict(total=25, passed=25, failed=0)), 'saved counts')
    card = decode(bodies['operation/cards/controls.json'])
    require(same(report['order'], card['controls']) and len(set(report['order'])) == 25
            and same([x['id'] for x in report['controls']], report['order']), 'saved control order')
    require(all(x['passed'] is True and x['error'] is None for x in report['controls']), 'saved outcome assertion')
    require(accept['future_execution_admitted'] is False and accept['current_scientific_runtime_qualified'] is False
            and accept['physical_calibration_or_native_forward_map_established'] is False
            and accept['previous_RI137_rejected'] is True, 'acceptance boundary')
    complete = decode(bodies['operation/output/COMPLETE.json'])
    monitor = decode(bodies['operation/output/FOCUSED25.COMPLETION.json'])
    require(same(complete['child'], monitor), 'saved child completion disagreement')
    require(monitor['child_exit_code'] == 0 and monitor['first_error'] is None
            and monitor['stop_reason'] is None and monitor['tail_errors'] == [], 'saved child failure')
    samples, attempts = monitor['samples'], monitor['monitor_attempts']
    require(len(samples) == len(attempts) == 30, 'saved monitor counts')
    previous = 0.0
    for sample, attempt in zip(samples, attempts):
        elapsed = sample['elapsed_seconds']
        require(type(elapsed) is float and math.isfinite(elapsed) and elapsed > previous, 'saved sample time')
        require(attempt['returncode'] == 0 and attempt['stderr'] == '' and attempt['stdout'].strip().isdigit()
                and same(sample['rss_kib'], int(attempt['stdout'])) and elapsed == attempt['elapsed_seconds'], 'saved raw sample')
        require(abs((elapsed-previous)-sample['gap_seconds']) < 1e-12 and 0 <= sample['gap_seconds'] <= 0.1
                and type(sample['rss_kib']) is int and 0 <= sample['rss_kib'] <= 524288, 'saved sample bound')
        previous = elapsed
    gap = monitor['elapsed_seconds']-previous
    require(0 <= gap <= 0.1 and abs(gap-monitor['final_sample_to_reap_gap_seconds']) < 1e-12
            and 0 < monitor['elapsed_seconds'] <= 180
            and monitor['peak_sampled_rss_kib'] == max(x['rss_kib'] for x in samples), 'saved terminal bound')
    require(bodies['root/BOOTSTRAP_PRE.json'] == bodies['root/BOOTSTRAP_POST.json'], 'saved bootstrap mismatch')
    require(inventory(root) == (files, directories), 'archive namespace changed during check')
    return dict(status='PUBLISHED_BYTES_AND_SAVED_AGREEMENT_PASS',published_commit=PUBLISHED_COMMIT,
                archived_files=len(files),exact_copies=132,operation_files=89,saved_control_outcomes=25,
                saved_monitor_samples=30,historical_empty_directories_required_on_disk=False,
                archived_code_executed=False,external_paths_opened=False,current_runtime_qualified=False,
                historical_tool_origin_independently_authenticated=False,scientific_claim_established=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=Path(__file__).resolve().parent.parent/ARCHIVE)
    args = parser.parse_args()
    try:
        result = verify(args.archive)
    except (InvalidArchive, OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, OverflowError) as error:
        print(json.dumps({'status':'REFUSED','error':str(error)},sort_keys=True),file=sys.stderr)
        return 1
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
