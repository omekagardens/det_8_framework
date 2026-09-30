"""RI133 opaque runtime metadata source. UNEXECUTED; no scientific imports.

RI121 collector constants and functions retained as source, with explicit size,
member and alias guards. The driver supplies separately authenticated metadata.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

CAP = 67108864
MAX_MEMBERS = 25000

BASE = '/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11'
VENV = '/Volumes/AI_DATA/development/det-review-evidence/ri73-recovery/recovery-20260924T212511Z-2403d37c/env'
STDLIB = BASE + '/lib/python3.11'
ROOTS = [STDLIB, VENV + '/lib/python3.11/site-packages', '/opt/homebrew/lib/python3.11/site-packages']
LINKS = [
    {'path': STDLIB + '/config-3.11-darwin/libpython3.11.a', 'target': '../../../Python'},
    {'path': STDLIB + '/config-3.11-darwin/libpython3.11.dylib', 'target': '../../../Python'},
    {'path': STDLIB + '/site-packages', 'target': '../../../../../../../../../lib/python3.11/site-packages'},
]
ABSENCES = [
    BASE + '/lib/python311.zip', VENV + '/bin/pyvenv.cfg',
    '/opt/homebrew/opt/python-tk@3.11', '/opt/homebrew/opt/python-gdbm@3.11',
    '/opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib',
    '/opt/homebrew/lib/libmpdec.3.dylib', '/usr/local/lib/libmpdec.3.dylib',
    '/usr/lib/libmpdec.3.dylib',
]
MANDATORY_EXTRAS = [
    VENV + '/pyvenv.cfg', BASE + '/Python', BASE + '/bin/python3.11', '/bin/ps',
    '/opt/homebrew/etc/openssl@3/openssl.cnf',
    '/opt/homebrew/Cellar/openssl@3/3.6.0/lib/libcrypto.3.dylib',
]
LOADER_NAMES = [
    '/opt/homebrew/opt/openssl@3/lib/libcrypto.3.dylib',
    '/opt/homebrew/opt/openssl@3/lib/libssl.3.dylib',
    '/opt/homebrew/opt/xz/lib/liblzma.5.dylib',
    '/opt/homebrew/opt/sqlite/lib/libsqlite3.0.dylib',
    '/opt/homebrew/Cellar/openssl@3/3.6.0/lib/ossl-modules/legacy.dylib',
    '/opt/homebrew/Cellar/openssl@3/3.6.0/lib/engines-3/loader_attic.dylib',
    '/opt/homebrew/Cellar/openssl@3/3.6.0/lib/engines-3/capi.dylib',
    '/opt/homebrew/Cellar/openssl@3/3.6.0/lib/engines-3/padlock.dylib',
]
NAMESPACE_DIRS = [
    '/opt/homebrew/Cellar/openssl@3/3.6.0/lib',
    '/opt/homebrew/Cellar/xz/5.8.2/lib',
    '/opt/homebrew/Cellar/sqlite/3.51.2/lib',
]


def guard(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def metadata(info):
    return {'device': info.st_dev, 'inode': info.st_ino,
            'mode': info.st_mode, 'bytes': info.st_size,
            'mtime_ns': info.st_mtime_ns, 'ctime_ns': info.st_ctime_ns}


def observe_file(name):
    p = Path(name)
    before = p.lstat()
    guard(p.resolve(strict=True) == p, 'nonliteral regular path: ' + name)
    guard(0 <= before.st_size <= CAP, 'opaque file exceeds preparation cap: ' + name)
    guard(stat.S_ISREG(before.st_mode), 'nonregular file: ' + name)
    digest = hashlib.sha256()
    size = 0
    header = b''
    with os.fdopen(os.open(p, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        guard(metadata(opened) == metadata(before), 'opened identity drift: ' + name)
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            if size == 0:
                header = chunk[:16]
            digest.update(chunk)
            size += len(chunk)
            guard(size <= CAP, 'opaque file grew beyond preparation cap')
        after = os.fstat(stream.fileno())
    final = p.lstat()
    guard(metadata(before) == metadata(after) == metadata(final) and size == before.st_size,
          'file changed while hashing: ' + name)
    row = {'path': name, 'bytes': size, 'sha256': digest.hexdigest()}
    selection = {'path': name, **metadata(before)}
    if p.suffix == '.pyc':
        selection['pyc_first16_hex'] = header.hex()
        selection['pyc_payload_not_parsed_or_executed'] = True
    return row, selection


def binding(name):
    # Resolve one path component at a time, retaining literal links independently
    # of the accepted helper. Directory entries are read, never executed.
    p = Path(name)
    guard(p.is_absolute(), 'binding must be absolute')
    todo = list(p.parts[1:])
    at = Path('/')
    links = []
    while todo:
        component = todo.pop(0)
        if component in ('', '.'):
            continue
        if component == '..':
            at = at.parent
            continue
        item = at / component
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode):
            guard(len(links) < 64, 'binding cycle')
            literal = os.readlink(item)
            links.append({'path': str(item), 'target': literal})
            target = Path(literal)
            if target.is_absolute():
                at = Path('/')
                todo = list(target.parts[1:]) + todo
            else:
                todo = list(target.parts) + todo
        else:
            at = item
    pin, _ = observe_file(str(at))
    return {'named_path': name, 'resolved_path': str(at), 'symlink_chain': links,
            'target': {'bytes': pin['bytes'], 'sha256': pin['sha256']}}


def walk_members(root_names):
    paths = set()
    links = []
    counts = []
    for name in root_names:
        root = Path(name)
        guard(root.is_dir() and root.resolve(strict=True) == root, 'noncanonical root: ' + name)
        count = 0
        members_seen = 0
        stack = [root]
        while stack:
            parent = stack.pop()
            with os.scandir(parent) as entries:
                members = sorted(entries, key=lambda entry: entry.name)
            for member in members:
                members_seen += 1
                guard(members_seen <= MAX_MEMBERS, 'runtime member cap')
                p = parent / member.name
                info = member.stat(follow_symlinks=False)
                if stat.S_ISLNK(info.st_mode):
                    links.append({'path': str(p), 'target': os.readlink(p)})
                    # For a directory link the matching tree is separately
                    # declared; file aliases select a regular target.
                    resolved = p.resolve(strict=True)
                    if not resolved.is_dir():
                        guard(resolved.is_file(), 'unexpected link target')
                        paths.add(str(resolved))
                elif stat.S_ISDIR(info.st_mode):
                    stack.append(p)
                else:
                    guard(stat.S_ISREG(info.st_mode), 'special tree member: ' + str(p))
                    paths.add(str(p))
                    count += 1
        counts.append({'root': name, 'regular_files': count})
    return paths, sorted(links, key=lambda item: item['path']), counts


def absent_observations():
    result = []
    for name in ABSENCES:
        p = Path(name)
        guard(not p.exists() and not p.is_symlink(), 'required absence changed: ' + name)
        result.append({'path': name, 'exists': False, 'is_symlink': False})
    return result


def directory_namespaces():
    result = []
    for name in NAMESPACE_DIRS:
        root = Path(name)
        guard(root.is_dir() and root.resolve(strict=True) == root, 'namespace root drift')
        members = []
        stack = [root]
        while stack:
            current = stack.pop()
            with os.scandir(current) as entries:
                items = sorted(entries, key=lambda entry: entry.name)
            for entry in items:
                p = current / entry.name
                info = entry.stat(follow_symlinks=False)
                row = {'relative_path': str(p.relative_to(root))}
                if stat.S_ISLNK(info.st_mode):
                    row.update(kind='symlink', literal_target=os.readlink(p))
                elif stat.S_ISDIR(info.st_mode):
                    row['kind'] = 'directory'
                    stack.append(p)
                elif stat.S_ISREG(info.st_mode):
                    row['kind'] = 'regular'
                else:
                    raise RuntimeError('special namespace member: ' + str(p))
                members.append(row)
                guard(len(members) <= MAX_MEMBERS, 'native namespace member cap')
        result.append({'root': name, 'recursive_members_no_symlink_traversal':
                       sorted(members, key=lambda item: item['relative_path'])})
    return result


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False, ensure_ascii=True) + '\n').encode('ascii')


def same(left, right, reason):
    guard(canonical(left) == canonical(right), reason)


def file_ref(path):
    return observe_file(str(path))[0]


def metadata_json(body):
    guard(type(body) is bytes and len(body) <= CAP, 'bounded immutable metadata')
    def pairs(items):
        result = {}
        for key, value in items:
            guard(key not in result, 'duplicate metadata key')
            result[key] = value
        return result
    def bad(_):
        raise ValueError('nonfinite metadata number')
    value = json.loads(body, object_pairs_hook=pairs, parse_constant=bad)
    same(body.decode('ascii'), canonical(value).decode('ascii'), 'canonical metadata bytes')
    return value


def load_ref(ref):
    guard(type(ref) is dict and set(ref) == {'path', 'bytes', 'sha256'}, 'closed metadata FilePin')
    same(file_ref(ref['path']), ref, 'metadata FilePin changed')
    body = Path(ref['path']).read_bytes()
    same({'path': ref['path'], 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}, ref, 'metadata read changed')
    return metadata_json(body)


def literal_path(name):
    guard(type(name) is str and Path(name).is_absolute() and str(Path(name)) == name
          and Path(name).resolve() == Path(name), 'literal absolute path')
    return Path(name)


def missing(name):
    try:
        Path(name).lstat()
    except FileNotFoundError:
        return True
    return False


# Every route below was present in the accepted historical complete dyld message.
# These are prospectively checked before BOTH fresh modes, then reconciled with
# the full fresh ordered message, including duplicate route attempts.
EXTRA_DYLD_ABSENCES = [
    '/System/Volumes/Preboot/Cryptexes/OS/opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib',
    '/opt/homebrew/Cellar/mpdecimal/4.0.1/lib/libmpdec.3.dylib',
    '/System/Volumes/Preboot/Cryptexes/OS/opt/homebrew/Cellar/mpdecimal/4.0.1/lib/libmpdec.3.dylib',
]
DYLD_LINK = {'path': '/opt/homebrew/opt/mpdecimal', 'target': '../Cellar/mpdecimal/4.0.1'}
DYLD_ROUTES = sorted(set(ABSENCES[4:] + EXTRA_DYLD_ABSENCES))


def dyld_routes():
    guard(all(missing(name) for name in DYLD_ROUTES), 'predeclared dyld route appeared')
    p = Path(DYLD_LINK['path'])
    guard(p.is_symlink() and os.readlink(p) == DYLD_LINK['target'], 'fixed mpdecimal alias changed')
    return {'schema': 'ri133-preobserved-dyld-route-domain-v1',
            'absent_paths': DYLD_ROUTES, 'symlinks': [DYLD_LINK],
            'scope': 'All predeclared routes; actual ordered attempts must be fully parsed and be contained here. No retrospective precheck credit.'}


def host_bootstrap():
    modules = []
    for name, module in sorted(sys.modules.items()):
        if module is None:
            continue
        spec = getattr(module, '__spec__', None)
        row = {'name': name, 'file': getattr(module, '__file__', None),
               'origin': getattr(spec, 'origin', None), 'cached': getattr(module, '__cached__', None),
               'loader_type': type(getattr(spec, 'loader', None)).__name__}
        file = row['file']
        if file is not None:
            row['binding'] = binding(file)
        modules.append(row)
    return {'uname': list(os.uname()),
            'system_version': file_ref('/System/Library/CoreServices/SystemVersion.plist'),
            'bootstrap': {'named': binding('/usr/bin/python3'), 'actual': binding(sys.executable),
                'version': sys.version, 'executable': sys.executable, 'prefix': sys.prefix,
                'base_prefix': sys.base_prefix, 'path': list(sys.path),
                'isolated': sys.flags.isolated, 'dont_write_bytecode': sys.flags.dont_write_bytecode,
                'optimize': sys.flags.optimize, 'modules': modules},
            'scope': 'Root-authenticated vendor bootstrap, Apple kernel/loader/shared cache and stable host remain supplier premises. This loaded bootstrap descriptor inventory is not the full candidate-runtime inventory or an instruction trace.'}


def tree(root):
    """Retain all names, file bytes, directory names and literal links, no traversal."""
    root = literal_path(str(root))
    guard(root.is_dir(), 'tree root directory')
    rows = []
    stack = [root]
    total = 0
    while stack:
        parent = stack.pop()
        with os.scandir(parent) as entries:
            members = sorted(entries, key=lambda item: item.name)
        for entry in members:
            path = parent / entry.name
            info = entry.stat(follow_symlinks=False)
            row = {'relative': str(path.relative_to(root))}
            if stat.S_ISLNK(info.st_mode):
                row.update(kind='symlink', target=os.readlink(path))
            elif stat.S_ISDIR(info.st_mode):
                row['kind'] = 'directory'
                stack.append(path)
            else:
                guard(stat.S_ISREG(info.st_mode), 'special retained evidence entry')
                ref = file_ref(path)
                row.update(kind='file', bytes=ref['bytes'], sha256=ref['sha256'])
                total += ref['bytes']
                guard(total <= 536870912, 'preparation retained namespace aggregate cap')
            rows.append(row)
            guard(len(rows) <= MAX_MEMBERS, 'retained namespace member cap')
    return sorted(rows, key=lambda item: item['relative'])


def source_observation(dependencies):
    observed = []
    for row in dependencies['opaque_files']:
        actual = file_ref(row['path'])
        same(actual, row, 'source/history/dependency bytes changed: ' + row['path'])
        observed.append(actual)
    actual = tree(dependencies['packet_root'])
    same(actual, dependencies['packet_namespace'], 'complete sealed RI130 namespace changed')
    return {'opaque_files': observed, 'packet_namespace': actual,
            'science_files_opened_as_opaque_hash_streams_only': True, 'scientific_body_decode': False}


def snapshot(dependencies):
    """Collect current bytes/selection twice-bracketed; never imports candidate."""
    before_host = host_bootstrap()
    source = source_observation(dependencies)
    absences = absent_observations()
    namespaces = directory_namespaces()
    same(namespaces, load_ref(dependencies['historical_optional_namespaces'])['directories'],
         'accepted static optional native namespace changed')
    routes = dyld_routes()
    loaders = [binding(name) for name in sorted(LOADER_NAMES)]
    interpreter = binding(VENV + '/bin/python')
    extras = sorted(set(MANDATORY_EXTRAS + [row['resolved_path'] for row in loaders]))
    paths, links, counts = walk_members(ROOTS)
    same(links, LINKS, 'unchanged accepted link domain')
    paths.update(extras)
    guard(len(paths) <= MAX_MEMBERS, 'complete runtime member cap')
    pins, selection = [], []
    for name in sorted(paths):
        pin, meta = observe_file(name)
        pins.append(pin)
        selection.append(meta)
    historical = load_ref(dependencies['historical_runtime'])
    # This exact identity bridge preserves applicability of the accepted static
    # native/startup reasoning. A changed installation is a new review question.
    for key, actual in [('roots', ROOTS), ('extra_files', extras), ('files', pins),
                        ('symlinks', links), ('absent_paths', ABSENCES), ('loader_bindings', loaders)]:
        same(actual, historical[key], 'historical runtime/static-closure identity changed: ' + key)
    final_paths, final_links, final_counts = walk_members(ROOTS)
    final_paths.update(extras)
    same([sorted(final_paths), final_links, final_counts], [sorted(paths), links, counts], 'runtime membership drift')
    for row in selection:
        same(metadata(Path(row['path']).lstat()), {key: row[key] for key in
             ('device', 'inode', 'mode', 'bytes', 'mtime_ns', 'ctime_ns')}, 'runtime selection changed')
    same(absent_observations(), absences, 'absence drift')
    same(directory_namespaces(), namespaces, 'native namespace drift')
    same(dyld_routes(), routes, 'dyld route drift')
    same([binding(name) for name in sorted(LOADER_NAMES)], loaders, 'native binding drift')
    same(binding(VENV + '/bin/python'), interpreter, 'interpreter binding drift')
    same(source_observation(dependencies), source, 'source/history drift')
    same(host_bootstrap(), before_host, 'host/bootstrap drift')
    return {'schema': 'ri133-complete-current-metadata-snapshot-v1',
            'runtime_inventory': historical,
            'selection': {'files': selection, 'status': 'CURRENT_OPAQUE_SELECTION_NOT_PROVEN_IMPORT_TRACE'},
            'optional_namespaces': {'directories': namespaces}, 'interpreter': interpreter,
            'preobserved_dyld_routes': routes, 'host_bootstrap': before_host, 'sources': source,
            'root_counts': counts, 'scientific_execution': False, 'actual_data_admission': False,
            'cache_scope': 'All pyc bytes pinned; first16 opaque only. Source/cache equivalence, actual execution route and trusted supplier remain separate premises.'}
