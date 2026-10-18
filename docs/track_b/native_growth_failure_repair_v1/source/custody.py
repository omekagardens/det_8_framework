"""RI138 bounded external custody mechanisms; source-only until root admission.

This module has no CLI, loader, process launcher, discovery mode or authority
writer. Its own bootstrap trust belongs to the genuine root/tool boundary.
Only fixed administrative manifests are decoded; protected bodies are opaque.
"""

from hashlib import sha256
from pathlib import Path
import errno
import json
import os
import plistlib
import stat
import time


BASE = Path('/Volumes/AI_DATA/development/det-review-evidence')
ANCESTRY = BASE/'ri122-native-caller-source-jgehvvxx'
RI136 = BASE/'ri136-native-policy-dispatch-source-g_z472z7'
MAX_BYTES = 67108864
MAX_DIRECTORY_ENTRIES = 16384
MAX_OBJECTS = 10000
PREP_SECONDS = 60
PHASE_SECONDS = 300
PYTHON = '/opt/homebrew/bin/python3'
PS = '/bin/ps'
MANIFEST_PINS = {
    'dependency': {'path': str(RI136/'SOURCE_DEPENDENCIES.json'), 'bytes': 652822,
                   'sha256': 'da5708eb15abbb4da7a8c17b5a6c737b2fce9e8663c2177e4dbb1b9e2107d42c'},
    'runtime': {'path': str(ANCESTRY/'RUNTIME_CLOSURE.json'), 'bytes': 2862854,
                'sha256': '35a58d48fce8e00e87d61034b13ef4fba2571d68630d55616ea27e3b786a7920'},
    'history': {'path': str(ANCESTRY/'HISTORY_RECONCILIATION.json'), 'bytes': 2170307,
                'sha256': 'b00d94f5d81f22e6c18715bed9519eb17f8252d12871e3254a9f3e5dac92435c'},
}
GROUPS = ('manifests', 'source_dependencies', 'history', 'runtime_files',
          'runtime_directories', 'runtime_absences', 'host', 'supplemental')


class Stop(RuntimeError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def need(condition, code, message):
    if not condition:
        raise Stop(code, message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def exact_keys(value, keys, code, context):
    need(type(value) is dict and set(value) == set(keys), code, context+' fields mismatch')


def hexhash(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def same(left, right, context):
    need(canonical(left) == canonical(right), 'custody', context)


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'configuration', 'duplicate JSON key')
            result[key] = value
        return result
    def bad(value):
        raise Stop('configuration', 'JSON decimals and nonfinite constants are forbidden')
    return json.loads(raw, object_pairs_hook=pairs, parse_float=bad, parse_constant=bad)


def canonical_path(value):
    need(type(value) is str and '\x00' not in value and Path(value).is_absolute()
         and os.path.normpath(value) == value, 'configuration', 'noncanonical absolute path')
    return value


def validate_identity(value):
    exact_keys(value, ('path', 'resolved_path', 'bytes', 'sha256', 'symlinks'),
               'configuration', 'file identity')
    canonical_path(value['path'])
    canonical_path(value['resolved_path'])
    need(type(value['bytes']) is int and 0 <= value['bytes'] <= MAX_BYTES
         and hexhash(value['sha256']) and value['sha256'] != '0'*64
         and type(value['symlinks']) is list and len(value['symlinks']) <= 64,
         'configuration', 'invalid bounded file identity')
    for link in value['symlinks']:
        exact_keys(link, ('path', 'target'), 'configuration', 'symlink identity')
        canonical_path(link['path'])
        need(type(link['target']) is str, 'configuration', 'invalid symlink identity fields')


def full_identity(value):
    need(type(value) is dict, 'configuration', 'identity is not an object')
    if set(value) == {'path', 'bytes', 'sha256'}:
        result = dict(value, resolved_path=value['path'], symlinks=[])
    else:
        result = value
    validate_identity(result)
    return json.loads(canonical(result))


def check_deadline(deadline_ns):
    need(type(deadline_ns) is int and time.monotonic_ns() <= deadline_ns,
         'custody_deadline', 'custody phase deadline exhausted')


def resolve_links(path, deadline_ns):
    """RI134 component traversal, with cooperative deadline checks added."""
    need(type(path) is Path or isinstance(path, Path), 'identity', 'identity path must be a Path')
    text = str(path)
    need(path.is_absolute() and os.path.normpath(text) == text, 'identity', 'noncanonical absolute path')
    links, seen = [], set()
    current = text
    for _ in range(64):
        check_deadline(deadline_ns)
        need(current not in seen, 'identity', 'symlink resolution cycle')
        seen.add(current)
        parts = Path(current).parts
        prefix = Path(parts[0])
        for i, part in enumerate(parts[1:], 1):
            check_deadline(deadline_ns)
            prefix = prefix/part
            status = prefix.lstat()
            if stat.S_ISLNK(status.st_mode):
                target = os.readlink(prefix)
                links.append({'path': str(prefix), 'target': target})
                replacement = Path(target) if os.path.isabs(target) else prefix.parent/target
                current = os.path.normpath(str(replacement.joinpath(*parts[i+1:])))
                break
        else:
            return Path(current), links
    raise Stop('identity', 'symlink resolution limit exceeded')


def read_file(path, deadline_ns, retain_bytes=False):
    """Bounded RI134-style full identity; optionally retain administrative bytes."""
    resolved, links = resolve_links(path, deadline_ns)
    check_deadline(deadline_ns)
    need(stat.S_ISREG(resolved.lstat().st_mode), 'identity', 'input is not a regular file')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    descriptor = os.open(resolved, flags)
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode), 'identity', 'input is not a regular file')
        need(0 <= before.st_size <= MAX_BYTES, 'identity', 'input exceeds 64 MiB custody bound')
        hasher, length, blocks = sha256(), 0, []
        while True:
            check_deadline(deadline_ns)
            chunk = os.read(descriptor, min(1024*1024, MAX_BYTES+1-length))
            if not chunk:
                break
            length += len(chunk)
            need(length <= MAX_BYTES, 'identity', 'input grew beyond 64 MiB custody bound')
            hasher.update(chunk)
            if retain_bytes:
                blocks.append(chunk)
        after = os.fstat(descriptor)
        signature = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        need(signature(before) == signature(after) and length == after.st_size,
             'identity', 'input changed while hashing')
    finally:
        os.close(descriptor)
    again, again_links = resolve_links(path, deadline_ns)
    need(again == resolved and again_links == links, 'identity', 'symlink chain changed while hashing')
    need(signature(resolved.lstat()) == signature(after), 'identity', 'input replaced after hashing')
    check_deadline(deadline_ns)
    identity = {'path': str(path), 'resolved_path': str(resolved), 'bytes': length,
                'sha256': hasher.hexdigest(), 'symlinks': links}
    return (b''.join(blocks) if retain_bytes else None), identity


def file_identity(path, deadline_ns):
    return read_file(path, deadline_ns)[1]


def read_expected_manifest(name, deadline_ns):
    expected = full_identity(MANIFEST_PINS[name])
    raw, observed = read_file(Path(expected['path']), deadline_ns, retain_bytes=True)
    same(observed, expected, 'fixed '+name+' manifest identity differs before parsing')
    value = strict_json(raw)
    same(file_identity(Path(expected['path']), deadline_ns), expected,
         'fixed '+name+' manifest changed during parsing')
    return value


def validate_entries(value, family, count):
    if family == 'dependency':
        exact_keys(value, ('schema', 'status', 'protected_files', 'scope'), 'dependency', 'dependency manifest')
        need(value['schema'] == 'ri129-source-dependencies-v1'
             and value['status'] == 'SOURCE_ONLY_CLOSED_DEPENDENCIES', 'dependency', 'dependency schema differs')
        same(value['scope'], {'scientific_execution': False, 'runtime_inventory_created': False,
             'active_execution_artifacts_created': False, 'old_history_and_runtime_preserved': True},
             'dependency scope differs')
        prefix = 'dep_'
    else:
        need(type(value) is dict and value.get('schema') == 'ri122-native-history-reconciliation-v1'
             and value.get('status') == 'SOURCE_ONLY_CURRENT_CUSTODY_CANDIDATE', 'history', 'history schema differs')
        prefix = 'hist_'
    need(type(value.get('protected_files')) is list and len(value['protected_files']) == count,
         family, 'fixed protected-file count differs')
    previous = None
    for index, item in enumerate(value['protected_files'], 1):
        exact_keys(item, ('role', 'path', 'identity', 'classification', 'access_policy', 'reference_provenance'),
                   family, 'protected entry')
        path = canonical_path(item['path'])
        need(item['role'] == prefix+str(index).zfill(4) and (previous is None or previous < path),
             family, 'protected role/order differs')
        validate_identity(item['identity'])
        need(item['identity']['path'] == path, family, 'protected identity path differs')
        if family == 'dependency':
            need(item['identity']['resolved_path'] == path and item['identity']['symlinks'] == [],
                 family, 'source dependency has a symlink or alias')
        need(type(item['classification']) is str and bool(item['classification'])
             and type(item['access_policy']) is str and bool(item['access_policy'])
             and type(item['reference_provenance']) is list, family, 'protected provenance malformed')
        previous = path
    return value['protected_files']


def validate_runtime(value):
    need(type(value) is dict and value.get('schema') == 'ri122-captured-application-runtime-v1'
         and value.get('status') == 'SOURCE_ONLY_CURRENT_RUNTIME_CANDIDATE', 'runtime', 'runtime schema differs')
    need(type(value.get('files')) is list and len(value['files']) == 2988,
         'runtime', 'fixed runtime file count differs')
    previous, by_path = None, {}
    for index, item in enumerate(value['files'], 1):
        exact_keys(item, ('role', 'path', 'identity', 'classification', 'reference_provenance'),
                   'runtime', 'runtime file entry')
        path = canonical_path(item['path'])
        need(item['role'] == 'runtime_'+str(index).zfill(4) and (previous is None or previous < path),
             'runtime', 'runtime file order or role differs')
        validate_identity(item['identity'])
        need(item['identity']['path'] == path, 'runtime', 'runtime identity path differs')
        need(type(item['classification']) is str and bool(item['classification'])
             and type(item['reference_provenance']) is str and bool(item['reference_provenance']),
             'runtime', 'runtime file provenance differs')
        previous, by_path[path] = path, item['identity']
    for path in (PYTHON, PS):
        need(path in by_path and by_path[path]['bytes'] > 0, 'runtime', 'fixed interpreter or monitor absent')
    need(type(value.get('directories')) is list and len(value['directories']) == 258,
         'runtime', 'fixed runtime directory count differs')
    previous = None
    for item in value['directories']:
        exact_keys(item, ('path', 'resolved_path', 'symlinks', 'entries'), 'runtime', 'runtime directory')
        path = canonical_path(item['path'])
        canonical_path(item['resolved_path'])
        need(previous is None or previous < path, 'runtime', 'runtime directory order differs')
        previous = path
        need(type(item['symlinks']) is list and len(item['symlinks']) <= 64
             and type(item['entries']) is list and len(item['entries']) <= MAX_DIRECTORY_ENTRIES,
             'runtime', 'directory links or entries malformed')
        for link in item['symlinks']:
            exact_keys(link, ('path', 'target'), 'runtime', 'directory symlink')
            canonical_path(link['path'])
            need(type(link['target']) is str, 'runtime', 'directory symlink target malformed')
        names = []
        for child in item['entries']:
            need(type(child) is dict and child.get('kind') in ('file', 'dir', 'symlink'),
                 'runtime', 'unsupported directory member kind')
            exact_keys(child, ('name', 'kind', 'target') if child['kind'] == 'symlink' else ('name', 'kind'),
                       'runtime', 'directory member')
            name = child['name']
            need(type(name) is str and bool(name) and name not in ('.', '..') and '/' not in name
                 and '\x00' not in name, 'runtime', 'invalid directory member name')
            if child['kind'] == 'symlink':
                need(type(child['target']) is str, 'runtime', 'invalid directory member link')
            names.append(name)
        need(names == sorted(set(names)), 'runtime', 'directory members not uniquely sorted')
    need(type(value.get('absences')) is list and len(value['absences']) == 40,
         'runtime', 'fixed runtime absence count differs')
    absent = [canonical_path(path) for path in value['absences']]
    need(absent == sorted(set(absent)) and not set(absent).intersection(by_path)
         and not set(absent).intersection(item['path'] for item in value['directories']),
         'runtime', 'runtime absences unordered, duplicate or conflicting')
    host = value['host_platform']
    exact_keys(host, ('expected_uname', 'system_version_plist', 'system_dependencies', 'scope_decision', 'trust_boundary'),
               'runtime', 'host-platform premises')
    exact_keys(host['expected_uname'], ('sysname', 'release', 'version', 'machine'), 'runtime', 'host uname')
    need(all(type(item) is str and bool(item) for item in host['expected_uname'].values())
         and host['expected_uname']['sysname'] == 'Darwin', 'runtime', 'host uname premises malformed')
    plist = host['system_version_plist']
    exact_keys(plist, ('path', 'expected_values'), 'runtime', 'system version metadata')
    need(plist['path'] == '/System/Library/CoreServices/SystemVersion.plist' and plist['path'] in by_path,
         'runtime', 'fixed system version plist unpinned')
    exact_keys(plist['expected_values'], ('ProductName', 'ProductVersion', 'ProductBuildVersion'),
               'runtime', 'system version fields')
    need(all(type(item) is str and bool(item) for item in plist['expected_values'].values()),
         'runtime', 'system version values malformed')
    need(type(host['system_dependencies']) is list and len(host['system_dependencies']) == 11,
         'runtime', 'fixed system dependency count differs')
    seen = set()
    for item in host['system_dependencies']:
        exact_keys(item, ('install_name', 'source_images', 'location_status', 'shared_cache_status'),
                   'runtime', 'system dependency')
        path = canonical_path(item['install_name'])
        need((path.startswith('/usr/lib/') or path.startswith('/System/Library/')) and path not in seen
             and item['location_status'] in ('regular_file', 'symlink', 'absent', 'unavailable')
             and item['shared_cache_status'] == 'not_independently_inspected_trusted_host_premise'
             and type(item['source_images']) is list and bool(item['source_images'])
             and all(type(source) is str and source in by_path for source in item['source_images']),
             'runtime', 'system dependency outside fixed trusted-platform boundary')
        seen.add(path)
    scope_path = str(BASE/'ri120-root-source-review-sksu97l1'/'RI122_HOST_PLATFORM_SCOPE_DECISION.json')
    validate_identity(host['scope_decision'])
    need(scope_path in by_path, 'runtime', 'owner host-platform scope decision unpinned')
    same(host['scope_decision'], by_path[scope_path], 'owner host-platform scope identity differs')
    need(type(host['trust_boundary']) is str and bool(host['trust_boundary']),
         'runtime', 'trusted host-platform boundary missing')
    return by_path


def load_expected(supplemental_identities, deadline_ns):
    """Load only authenticated expectations; never observe their referenced bodies."""
    started = time.monotonic_ns()
    need(type(deadline_ns) is int and deadline_ns <= started+PREP_SECONDS*1000000000,
         'configuration', 'preparation deadline exceeds fixed 60 seconds')
    check_deadline(deadline_ns)
    need(type(supplemental_identities) in (tuple, list) and len(supplemental_identities) <= MAX_OBJECTS,
         'configuration', 'supplemental identities must be a bounded sequence')
    dependency = read_expected_manifest('dependency', deadline_ns)
    history = read_expected_manifest('history', deadline_ns)
    runtime = read_expected_manifest('runtime', deadline_ns)
    deps = validate_entries(dependency, 'dependency', 373)
    histories = validate_entries(history, 'history', 699)
    runtime_by_path = validate_runtime(runtime)
    objects, known = [], {}
    counts = {group: 0 for group in GROUPS}
    def add(group, kind, path, expected, auxiliary=None):
        check_deadline(deadline_ns)
        if kind == 'file':
            validate_identity(expected)
            need(expected['path'] == path, 'configuration', 'expected object path differs')
            if path in known:
                same(known[path], expected, 'conflicting frozen file expectation: '+path)
            known[path] = expected
        counts[group] += 1
        objects.append({'id': group+':'+str(counts[group]).zfill(4), 'group': group,
                        'kind': kind, 'path': path, 'expected': expected, 'auxiliary': auxiliary})
    for name, identity in MANIFEST_PINS.items():
        add('manifests', 'file', identity['path'], full_identity(identity))
    for group, entries in (('source_dependencies', deps), ('history', histories), ('runtime_files', runtime['files'])):
        for entry in entries:
            add(group, 'file', entry['path'], entry['identity'])
    for entry in runtime['directories']:
        add('runtime_directories', 'directory', entry['path'], entry)
    for path in runtime['absences']:
        add('runtime_absences', 'absence', path, True)
    host = runtime['host_platform']
    add('host', 'uname', None, host['expected_uname'])
    plist = host['system_version_plist']
    add('host', 'system_version', plist['path'], plist['expected_values'], runtime_by_path[plist['path']])
    for entry in host['system_dependencies']:
        add('host', 'system_location', entry['install_name'], {key: entry[key] for key in
            ('install_name', 'location_status', 'shared_cache_status')})
    supplemental = {}
    for item in supplemental_identities:
        identity = full_identity(item)
        path = identity['path']
        if path in supplemental:
            same(supplemental[path], identity, 'conflicting supplemental identity: '+path)
        supplemental[path] = identity
    for path in sorted(supplemental):
        add('supplemental', 'file', path, supplemental[path])
    need(len(objects) <= MAX_OBJECTS, 'configuration', 'frozen custody object count exceeds bound')
    spec = {'schema': 'ri138-frozen-custody-spec-v1', 'manifest_identities': MANIFEST_PINS,
            'frozen_counts': counts, 'expected_interpreter': runtime_by_path[PYTHON],
            'trust_boundary': host['trust_boundary'], 'objects': objects}
    raw = canonical(spec).encode('ascii')
    need(len(raw) <= MAX_BYTES, 'configuration', 'frozen custody specification exceeds bound')
    check_deadline(deadline_ns)
    return raw


def runtime_directory_identity(path, deadline_ns):
    resolved, links = resolve_links(path, deadline_ns)
    before = resolved.stat()
    need(stat.S_ISDIR(before.st_mode), 'runtime', 'runtime namespace path is not a directory')
    def members():
        result, encoded_bytes = [], 0
        with os.scandir(resolved) as iterator:
            for entry in iterator:
                check_deadline(deadline_ns)
                status = entry.stat(follow_symlinks=False)
                if stat.S_ISLNK(status.st_mode):
                    item = {'name': entry.name, 'kind': 'symlink', 'target': os.readlink(entry.path)}
                elif stat.S_ISREG(status.st_mode):
                    item = {'name': entry.name, 'kind': 'file'}
                elif stat.S_ISDIR(status.st_mode):
                    item = {'name': entry.name, 'kind': 'dir'}
                else:
                    raise Stop('runtime', 'unsupported runtime namespace object: '+entry.path)
                encoded_bytes += len(canonical(item).encode('ascii'))
                need(len(result) < MAX_DIRECTORY_ENTRIES and encoded_bytes <= MAX_BYTES,
                     'runtime', 'runtime directory observation exceeds bound')
                result.append(item)
        return sorted(result, key=lambda item: item['name'])
    entries = members()
    after = resolved.stat()
    signature = lambda value: (value.st_dev, value.st_ino, value.st_mode, value.st_mtime_ns, value.st_ctime_ns)
    again, again_links = resolve_links(path, deadline_ns)
    need(signature(before) == signature(after) and entries == members()
         and again == resolved and again_links == links,
         'runtime', 'runtime directory changed during observation')
    check_deadline(deadline_ns)
    return {'path': str(path), 'resolved_path': str(resolved), 'symlinks': links, 'entries': entries}


def runtime_system_location(path):
    try:
        status = Path(path).lstat()
    except FileNotFoundError as error:
        need(error.errno == errno.ENOENT, 'runtime', 'system location absence is not ENOENT')
        return 'absent'
    if stat.S_ISLNK(status.st_mode):
        return 'symlink'
    need(stat.S_ISREG(status.st_mode), 'runtime', 'system dependency is not a regular file or link')
    return 'regular_file'


def runtime_system_version(path, expected_file, deadline_ns):
    raw, before = read_file(path, deadline_ns, retain_bytes=True)
    same(before, expected_file, 'system version plist identity changed')
    value = plistlib.loads(raw)
    need(type(value) is dict, 'runtime', 'system version metadata is not a dictionary')
    result = {key: value[key] for key in ('ProductName', 'ProductVersion', 'ProductBuildVersion')}
    need(all(type(item) is str for item in result.values()), 'runtime', 'system version metadata types differ')
    same(file_identity(path, deadline_ns), expected_file, 'system version plist changed during metadata read')
    return result


def observe_object(item, deadline_ns):
    kind, path = item['kind'], item['path']
    if kind == 'file':
        return file_identity(Path(path), deadline_ns)
    if kind == 'directory':
        return runtime_directory_identity(Path(path), deadline_ns)
    if kind == 'absence':
        try:
            Path(path).lstat()
            return False
        except FileNotFoundError as error:
            need(error.errno == errno.ENOENT, 'runtime', 'runtime absence is not ENOENT')
            return True
    if kind == 'uname':
        value = os.uname()
        return {key: getattr(value, key) for key in ('sysname', 'release', 'version', 'machine')}
    if kind == 'system_version':
        return runtime_system_version(Path(path), item['auxiliary'], deadline_ns)
    if kind == 'system_location':
        return {'install_name': path, 'location_status': runtime_system_location(path),
                'shared_cache_status': item['expected']['shared_cache_status']}
    raise Stop('configuration', 'unknown frozen custody object kind')


def error_record(error):
    return {'error_type': type(error).__name__, 'code': getattr(error, 'code', None),
            'message': str(error)[:4096]}


def validate_spec(spec_bytes):
    need(type(spec_bytes) is bytes and 0 < len(spec_bytes) <= MAX_BYTES,
         'configuration', 'frozen specification must be bounded immutable bytes')
    value = strict_json(spec_bytes)
    exact_keys(value, ('schema', 'manifest_identities', 'frozen_counts', 'expected_interpreter',
                      'trust_boundary', 'objects'), 'configuration', 'frozen specification')
    need(value['schema'] == 'ri138-frozen-custody-spec-v1'
         and canonical(value).encode('ascii') == spec_bytes, 'configuration', 'noncanonical frozen specification')
    same(value['manifest_identities'], MANIFEST_PINS, 'frozen manifest pins differ')
    exact_keys(value['frozen_counts'], GROUPS, 'configuration', 'frozen group counts')
    need(type(value['objects']) is list and 0 < len(value['objects']) <= MAX_OBJECTS,
         'configuration', 'frozen object list malformed')
    actual = {group: 0 for group in GROUPS}
    for item in value['objects']:
        exact_keys(item, ('id', 'group', 'kind', 'path', 'expected', 'auxiliary'), 'configuration', 'frozen object')
        need(item['group'] in GROUPS and item['kind'] in ('file', 'directory', 'absence', 'uname',
             'system_version', 'system_location'), 'configuration', 'frozen object kind/group differs')
        actual[item['group']] += 1
        need(item['id'] == item['group']+':'+str(actual[item['group']]).zfill(4),
             'configuration', 'frozen object id/order differs')
        if item['kind'] != 'uname':
            canonical_path(item['path'])
        if item['kind'] == 'file':
            validate_identity(item['expected'])
            need(item['expected']['path'] == item['path'], 'configuration', 'frozen file path differs')
    same(actual, value['frozen_counts'], 'frozen object counts differ')
    need(all(type(value['frozen_counts'][group]) is int for group in GROUPS),
         'configuration', 'frozen count is not an integer')
    same({key: actual[key] for key in GROUPS if key != 'supplemental'},
         {'manifests': 3, 'source_dependencies': 373, 'history': 699, 'runtime_files': 2988,
          'runtime_directories': 258, 'runtime_absences': 40, 'host': 13}, 'fixed frozen closure count differs')
    validate_identity(value['expected_interpreter'])
    need(value['expected_interpreter']['path'] == PYTHON and type(value['trust_boundary']) is str,
         'configuration', 'frozen interpreter/trust premise differs')
    return value


def validate_reference(reference, raw):
    exact_keys(reference, ('path', 'offset', 'bytes', 'sha256'), 'sink', 'durable record reference')
    canonical_path(reference['path'])
    need(type(reference['offset']) is int and reference['offset'] >= 0
         and type(reference['bytes']) is int and reference['bytes'] == len(raw)
         and reference['sha256'] == sha256(raw).hexdigest(), 'sink', 'durable record reference differs')


def extend_spec(spec_bytes, supplemental_identities):
    """Pure extension: preserve every old expectation even if its file changed."""
    spec = validate_spec(spec_bytes)
    need(type(supplemental_identities) in (tuple, list) and len(supplemental_identities) <= MAX_OBJECTS,
         'configuration', 'supplemental identities must be a bounded sequence')
    known = {}
    for item in spec['objects']:
        if item['kind'] == 'file':
            path = item['path']
            if path in known:
                same(known[path], item['expected'], 'conflicting existing frozen identity: '+path)
            known[path] = item['expected']
    additions = {}
    for value in supplemental_identities:
        identity = full_identity(value)
        path = identity['path']
        if path in known:
            same(known[path], identity, 'extension would replace frozen identity: '+path)
        elif path in additions:
            same(additions[path], identity, 'conflicting extension identity: '+path)
        else:
            additions[path] = identity
    for path in sorted(additions):
        spec['frozen_counts']['supplemental'] += 1
        spec['objects'].append({'id': 'supplemental:'+str(spec['frozen_counts']['supplemental']).zfill(4),
                                'group': 'supplemental', 'kind': 'file', 'path': path,
                                'expected': additions[path], 'auxiliary': None})
    need(len(spec['objects']) <= MAX_OBJECTS, 'configuration', 'extended custody object count exceeds bound')
    raw = canonical(spec).encode('ascii')
    need(len(raw) <= MAX_BYTES, 'configuration', 'extended custody specification exceeds bound')
    return raw


def observe_all(spec_bytes, phase, sink, deadline_ns):
    """Attempt every frozen row independently; a durable sink is owned by root."""
    started = time.monotonic_ns()
    need(phase in ('before', 'after'), 'configuration', 'unknown custody phase')
    need(type(deadline_ns) is int and deadline_ns <= started+PHASE_SECONDS*1000000000,
         'configuration', 'custody deadline exceeds fixed 300 seconds')
    need(callable(sink), 'configuration', 'durable custody sink is not callable')
    spec = validate_spec(spec_bytes)
    spec_hash = sha256(spec_bytes).hexdigest()
    groups = {group: {'expected': spec['frozen_counts'][group], 'attempted': 0, 'matched': 0,
                     'observation_errors': 0, 'mismatches': 0, 'sink_errors': 0, 'complete': False}
              for group in GROUPS}
    records, first_error, deadline_exhausted = [], None, False
    for sequence, item in enumerate(spec['objects'], 1):
        group = groups[item['group']]
        row_started = time.monotonic_ns()
        attempted, matched = False, False
        try:
            check_deadline(deadline_ns)
            attempted = True
            group['attempted'] += 1
            actual = observe_object(item, deadline_ns)
            check_deadline(deadline_ns)
            observed = {'ok': True, 'identity': actual}
            matched = canonical(actual) == canonical(item['expected'])
            if matched:
                group['matched'] += 1
            else:
                group['mismatches'] += 1
                if first_error is None:
                    first_error = {'id': item['id'], 'stage': 'observation', 'error_type': 'IdentityMismatch',
                                   'code': 'custody_mismatch', 'message': 'actual object differs from frozen expectation'}
        except Exception as error:
            details = error_record(error)
            observed = dict(details, ok=False)
            group['observation_errors'] += 1
            deadline_exhausted = deadline_exhausted or details['code'] == 'custody_deadline'
            if first_error is None:
                first_error = dict(details, id=item['id'], stage='observation')
        record = {'schema': 'ri138-custody-object-observation-v1', 'phase': phase, 'spec_sha256': spec_hash,
                  'sequence': sequence, 'id': item['id'], 'group': item['group'], 'kind': item['kind'],
                  'path': item['path'], 'expected': item['expected'], 'observed': observed, 'matched': matched,
                  'observation_attempted': attempted, 'started_ns': row_started, 'finished_ns': time.monotonic_ns()}
        reference, sink_error = None, None
        try:
            raw = (canonical(record)+'\n').encode('ascii')
            need(len(raw) <= MAX_BYTES, 'sink', 'custody record exceeds bound')
            reference = sink(record)
            validate_reference(reference, raw)
        except Exception as error:
            sink_error = error_record(error)
            group['sink_errors'] += 1
            if first_error is None:
                first_error = dict(sink_error, id=item['id'], stage='sink')
        records.append({'id': item['id'], 'reference': reference, 'sink_error': sink_error})
    finished = time.monotonic_ns()
    deadline_exhausted = deadline_exhausted or finished > deadline_ns
    for group in groups.values():
        group['complete'] = (group['attempted'] == group['expected'] == group['matched']
                             and group['observation_errors'] == 0 and group['mismatches'] == 0
                             and group['sink_errors'] == 0)
    return {'schema': 'ri138-custody-summary-v1', 'phase': phase, 'spec_sha256': spec_hash,
            'expected_objects': len(spec['objects']), 'attempted_objects': sum(g['attempted'] for g in groups.values()),
            'matched_objects': sum(g['matched'] for g in groups.values()),
            'observation_errors': sum(g['observation_errors'] for g in groups.values()),
            'mismatches': sum(g['mismatches'] for g in groups.values()),
            'sink_errors': sum(g['sink_errors'] for g in groups.values()),
            'deadline_exhausted': deadline_exhausted,
            'complete': not deadline_exhausted and all(g['complete'] for g in groups.values()),
            'groups': groups, 'records': records, 'first_error': first_error,
            'started_ns': started, 'finished_ns': finished, 'elapsed_ns': finished-started,
            'trust_boundary': spec['trust_boundary'], 'bootstrap_provenance_established': False}
