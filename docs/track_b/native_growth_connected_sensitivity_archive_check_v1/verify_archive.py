#!/usr/bin/env python3
"""Check published bytes and saved-data agreement; never run archived code."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

MANIFEST_SHA256 = 'd3ece15e443eb76a6d99af700470e47b4adb40cdbb690ff219f3393f72f827fc'
BASE_COMMIT = '3027dc6813b95cc57e8637c6598a6b07325074f0'
ARCHIVE = 'native_growth_connected_sensitivity_result_v1'
MAX_FILE_BYTES = 8 * 1024 * 1024


class InvalidArchive(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidArchive(message)


def digest(body):
    return hashlib.sha256(body).hexdigest()


def pairs(entries):
    result = {}
    for key, value in entries:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def reject_constant(value):
    raise InvalidArchive('nonfinite JSON constant: ' + value)


def decode(body):
    return json.loads(body.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=reject_constant)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'),
                       ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')


def same(left, right):
    """Type-sensitive whole-tree equality, including ordered array members."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(same(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
    return left == right


def read_regular(path, expected_size):
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), 'nonregular or symlink file: ' + str(path))
    require(before.st_size == expected_size and 0 < expected_size <= MAX_FILE_BYTES,
            'file size differs: ' + str(path))
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        require((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino),
                'file changed on open: ' + str(path))
        body = stream.read(MAX_FILE_BYTES + 1)
        after_open = os.fstat(stream.fileno())
    after_path = path.lstat()
    fields = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    require(fields(before) == fields(opened) == fields(after_open) == fields(after_path),
            'file changed during read: ' + str(path))
    require(len(body) == expected_size, 'short or oversized read: ' + str(path))
    return body


def file_inventory(root):
    require(root.is_dir() and not root.is_symlink(), 'archive must be a regular directory')
    found = set()
    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in dirs:
            require(not (Path(directory) / name).is_symlink(), 'symlink directory in archive')
        for name in names:
            path = Path(directory) / name
            require(stat.S_ISREG(path.lstat().st_mode), 'nonregular archive member: ' + str(path))
            found.add(path.relative_to(root).as_posix())
    return found


def verify_science(bodies):
    """Compare only saved objects; no coefficient, root or probability calculation."""
    certificate = decode(bodies['CERTIFICATE.json'])
    report = decode(bodies['AUDIT_REPORT.json'])
    normal = decode(bodies['NORMAL_SUMMARY.json'])
    decision = decode(bodies['ROOT_ADJUDICATION.json'])
    require(type(certificate) is dict and len(certificate) == 19,
            'certificate must retain nineteen complete sections')
    require(canonical(certificate) == bodies['CERTIFICATE.json'], 'certificate not canonical')
    require(report['status'] == 'all_saved_fields_independently_match', 'audit status differs')
    require(same(certificate, report['reconstructed_certificate']),
            'complete audit reconstruction differs')
    require(canonical(report['reconstructed_certificate']) == bodies['CERTIFICATE.json'],
            'whole reconstructed bytes differ')
    require(bodies['NORMAL_SUMMARY.json'] == bodies['OPTIMIZED_SUMMARY.json'],
            'normal and optimized summaries differ')
    require(normal['status'] == 'PASS' and normal['producer_replay_is_independent_audit'] is False,
            'producer status or independence boundary differs')
    require(normal['certificate_sha256'] == normal['witness_sha256'] == digest(bodies['CERTIFICATE.json']),
            'summary certificate identity differs')
    require(decision['status'] == 'ACCEPT_FIXED_28_CHILD_POSITIVE_REPAIR_OBSTRUCTION',
            'root decision status differs')
    require(same(certificate['decision'], normal['decision']) and
            same(certificate['decision'], decision['decision']), 'saved decisions differ')
    require(decision['all_positive_extensions_rejected'] is False and
            decision['physical_claim'] is False and decision['programme_complete'] is False,
            'root claim boundary differs')
    require(same({k: normal[k] for k in ('refusal_count', 'root_fixture_count',
                                      'family_fixture_count', 'decision_fixture_count')},
                 dict(refusal_count=166, root_fixture_count=16,
                      family_fixture_count=10, decision_fixture_count=6)), 'saved counts differ')
    return dict(complete_certificate_sections=19, complete_canonical_certificate_bytes=len(bodies['CERTIFICATE.json']),
                normal_optimized_equal=True, saved_decisions_equal=True)


def verify(root):
    manifest_path = Path(__file__).resolve().with_name('MANIFEST.json')
    manifest_body = read_regular(manifest_path, 20316)
    require(digest(manifest_body) == MANIFEST_SHA256, 'pinned manifest differs')
    manifest = decode(manifest_body)
    require(manifest['base_commit'] == BASE_COMMIT and manifest['archive'] == ARCHIVE,
            'archive identity differs')
    rows = manifest['files']
    require(type(rows) is list and len(rows) == 117, 'manifest inventory differs')
    expected = set()
    for row in rows:
        require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'}, 'manifest entry shape')
        name = row['path']
        require(type(name) is str and PurePosixPath(name).as_posix() == name and
                not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts,
                'unsafe manifest path')
        require(name not in expected and type(row['bytes']) is int and
                type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}', row['sha256']),
                'invalid manifest identity')
        expected.add(name)
    require(file_inventory(root) == expected, 'missing or unexpected archive files')
    bodies = {}
    for row in rows:
        path = root / row['path']
        # Repeat the within-archive ancestry check immediately before reading.
        require(all(not p.is_symlink() for p in [root, *tuple(path.parents)[:len(PurePosixPath(row['path']).parts)-1]]),
                'symlink archive ancestry')
        body = read_regular(path, row['bytes'])
        require(digest(body) == row['sha256'], 'content digest differs: ' + row['path'])
        bodies[row['path']] = body
    science = verify_science(bodies)
    require(file_inventory(root) == expected, 'archive inventory changed during verification')
    return dict(status='PUBLISHED_ARCHIVE_INTEGRITY_AND_SAVED_AGREEMENT_PASS',
                base_commit=BASE_COMMIT, files_checked=len(rows), **science,
                archived_code_executed=False, independent_arithmetic_rerun=False,
                external_provenance_paths_traversed=False, execution_custody_readjudicated=False,
                new_scientific_or_physical_claim=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path,
                        default=Path(__file__).resolve().parent.parent / ARCHIVE)
    args = parser.parse_args()
    try:
        result = verify(args.archive.absolute())
    except (InvalidArchive, OSError, ValueError, KeyError, TypeError, RecursionError) as error:
        print(json.dumps(dict(status='FAIL', error=str(error)), sort_keys=True), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
