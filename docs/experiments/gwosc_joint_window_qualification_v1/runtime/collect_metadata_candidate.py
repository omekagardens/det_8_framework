"""Independent opaque-file collector; never import or execute candidate bytes.

Run only with /usr/bin/python3 -I -B. Writes inert candidate artifacts in this
fresh reservation. It does not call the accepted runtime helper or candidate
interpreter and creates no profile, production inventory, freeze or admission.
"""
import hashlib
import json
import os
from pathlib import Path
import stat

OUT = Path('/Volumes/AI_DATA/development/det-review-evidence/ri121-runtime-candidate-rIMnamYh')
HELPER = Path('/Volumes/AI_DATA/development/det-review-evidence/ri121-synthetic-caller-repair-7ys8vsc3/runtime_support.py')
HELPER_SHA = '525314ee292722c50ab0bdf635123d3c36acbb96a76d60368c9677872fc2c40f'
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
    guard(stat.S_ISREG(before.st_mode), 'nonregular file: ' + name)
    digest = hashlib.sha256()
    size = 0
    header = b''
    with p.open('rb') as stream:
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
        stack = [root]
        while stack:
            parent = stack.pop()
            with os.scandir(parent) as entries:
                members = sorted(entries, key=lambda entry: entry.name)
            for member in members:
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
        result.append({'root': name, 'recursive_members_no_symlink_traversal':
                       sorted(members, key=lambda item: item['relative_path'])})
    return result


def emit(name, value):
    body = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    with (OUT / name).open('xb') as stream:
        stream.write(body)
        stream.flush()
        os.fsync(stream.fileno())
    return {'file': name, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def main():
    helper_pin, _ = observe_file(str(HELPER))
    guard(helper_pin['sha256'] == HELPER_SHA, 'accepted helper pin differs')
    absences = absent_observations()
    namespaces = directory_namespaces()
    loaders = [binding(name) for name in sorted(LOADER_NAMES)]
    required_crypto = next(row for row in loaders if row['named_path'] == LOADER_NAMES[0])
    guard(required_crypto == {
        'named_path': LOADER_NAMES[0],
        'resolved_path': '/opt/homebrew/Cellar/openssl@3/3.6.0/lib/libcrypto.3.dylib',
        'symlink_chain': [{'path': '/opt/homebrew/opt/openssl@3', 'target': '../Cellar/openssl@3/3.6.0'}],
        'target': {'bytes': 4874704, 'sha256': 'e7731484e003229df06b3945b198a557110ba5bbbf7d735a79130540c6fb2480'},
    }, 'required literal crypto binding differs from accepted v2')
    interpreter = binding(VENV + '/bin/python')
    extras = sorted(set(MANDATORY_EXTRAS + [row['resolved_path'] for row in loaders]))
    paths, links, counts = walk_members(ROOTS)
    guard(links == LINKS, 'tree symlink membership differs')
    paths.update(extras)
    pins, selection = [], []
    for name in sorted(paths):
        pin, meta = observe_file(name)
        pins.append(pin)
        selection.append(meta)
    final_paths, final_links, final_counts = walk_members(ROOTS)
    final_paths.update(extras)
    guard((final_paths, final_links, final_counts) == (paths, links, counts), 'whole tree membership changed')
    for item in selection:
        guard(metadata(Path(item['path']).lstat()) == {key: item[key] for key in
              ('device', 'inode', 'mode', 'bytes', 'mtime_ns', 'ctime_ns')},
              'post-capture selection metadata changed: ' + item['path'])
    guard(absent_observations() == absences, 'absence state changed')
    guard(directory_namespaces() == namespaces, 'optional namespace changed')
    guard([binding(name) for name in sorted(LOADER_NAMES)] == loaders, 'loader binding changed')
    guard(binding(VENV + '/bin/python') == interpreter, 'interpreter binding changed')
    guard(observe_file(str(HELPER))[0] == helper_pin, 'accepted helper changed')
    scope = {
        'status': 'INERT_METADATA_CANDIDATE_NOT_RUNTIME_ACCEPTANCE_OR_EXECUTION_PROFILE',
        'core': 'Exact accepted runtime_support.py v2 three roots, allowed links, eight absences, required files and crypto binding.',
        'conservative_optional': 'Three additional extension dylibs and four OpenSSL provider/engine files from independently read static graph; inclusion does not claim loading.',
        'bytecode': 'All existing pyc preserved as executable alternatives; separate selection metadata records bytes, timestamps and opaque headers, without payload interpretation.',
        'platform': 'Apple kernel/loader/shared-cache implementation remains explicit trusted platform premise; no whole-OS byte closure claim.',
        'boundary': 'No candidate interpreter, accepted helper or scientific target invoked; root must independently review and establish profile before any admission.',
    }
    inventory = {'schema': 'ri121-complete-stdlib-runtime-inventory-v2',
                 'roots': ROOTS, 'extra_files': extras, 'files': pins,
                 'symlinks': LINKS, 'absent_paths': ABSENCES,
                 'loader_bindings': loaders, 'scope': scope}
    outputs = []
    outputs.append(emit('RUNTIME_INVENTORY.candidate.json', inventory))
    outputs.append(emit('INTERPRETER_BINDING.candidate.json', interpreter))
    outputs.append(emit('FILE_SELECTION_METADATA.candidate.json', {
        'status': 'INERT_SELECTION_METADATA_NOT_A_PROVEN_IMPORT_TRACE',
        'notes': ['No pyc payload parsed, unmarshalled, compiled or executed.',
                  'Source mtime/size can select timestamp caches; content pins alone do not prove route or equivalence.',
                  'This captures all candidate members, not just predicted direct imports.'],
        'files': selection}))
    outputs.append(emit('OPTIONAL_NATIVE_NAMESPACES.candidate.json', {
        'status': 'STATIC_NAMESPACE_CANDIDATE_NOT_ACTIVE_GUARD',
        'notes': ['Exact recursive names/types/link-text only, without symlink traversal.',
                  'Directory membership is separate from the accepted v2 file/binding checks; root must explicitly adjudicate its prospective custody.',
                  'Unselected archives/headers/pkgconfig bytes are not claimed necessary executable closure.'],
        'directories': namespaces}))
    outputs.append(emit('CAPTURE_OBSERVATIONS.json', {
        'status': 'SUCCESSFUL_METADATA_CAPTURE_ONLY', 'accepted_helper': helper_pin,
        'root_regular_file_counts': counts, 'inventory_file_count': len(pins),
        'inventory_total_bytes': sum(row['bytes'] for row in pins),
        'pyc_count': sum('pyc_first16_hex' in row for row in selection),
        'source_py_count': sum(row['path'].endswith('.py') for row in selection),
        'extra_files_count': len(extras), 'loader_bindings_count': len(loaders),
        'mandatory_absences': absences, 'all_membership_metadata_and_binding_postchecks_passed': True,
        'outputs': outputs,
        'tooling': '/usr/bin/python3 -I -B collect_metadata_candidate.py; independent metadata code only',
    }))
    print(json.dumps({'files': len(pins), 'bytes': sum(row['bytes'] for row in pins),
                      'roots': counts, 'outputs': outputs}, indent=2))


if __name__ == '__main__':
    main()
