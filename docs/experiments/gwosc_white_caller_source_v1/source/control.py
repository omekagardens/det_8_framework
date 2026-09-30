"""External RI80 custody helpers; no numerical imports or launch at import."""
import hashlib
import json
import os
from pathlib import Path
import stat


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def identity(body):
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def file_pin(path):
    path = Path(path)
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), 'not a regular nonsymlink file: ' + str(path))
    digest, length = hashlib.sha256(), 0
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        require((opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino), 'file changed during open')
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            length += len(chunk)
            digest.update(chunk)
        after = os.fstat(stream.fileno())
    final = path.lstat()
    key = lambda value: (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns)
    require(key(before) == key(after) == key(final) and length == before.st_size, 'file changed during snapshot')
    return {'bytes': length, 'sha256': digest.hexdigest()}


def binding(named):
    path = Path(named)
    require(path.is_absolute(), 'absolute interpreter name required')
    pending, current, links = list(path.parts[1:]), Path('/'), []
    while pending:
        part = pending.pop(0)
        if part in ('', '.'):
            continue
        if part == '..':
            current = current.parent
            continue
        candidate = current / part
        info = candidate.lstat()
        if stat.S_ISLNK(info.st_mode):
            require(len(links) < 64, 'symlink chain too long')
            target = os.readlink(candidate)
            links.append({'path': str(candidate), 'target': target})
            link = Path(target)
            if link.is_absolute():
                current = Path('/')
                pending = list(link.parts[1:]) + pending
            else:
                pending = list(link.parts) + pending
        else:
            current = candidate
    return {'named_path': str(path), 'symlink_chain': links, 'resolved_path': str(current), 'target': file_pin(current)}


def parse_json(body):
    def pairs(rows):
        value = {}
        for key, item in rows:
            require(key not in value, 'duplicate JSON key')
            value[key] = item
        return value
    def invalid(text):
        raise ValueError('nonfinite JSON token: ' + text)
    return json.loads(body.decode('utf-8'), object_pairs_hook=pairs, parse_constant=invalid)


def verified_body(path, expected):
    require(file_pin(path) == expected, 'file identity differs: ' + str(path))
    body = Path(path).read_bytes()
    require(identity(body) == expected, 'file body changed after identity check')
    return body


def verify_sources(manifest):
    observed = []
    for item in manifest['sources']:
        for field in ('original', 'copy'):
            path = Path(item[field])
            require(path == path.resolve(), 'source path resolves elsewhere: ' + str(path))
            actual = file_pin(path)
            require(actual == item['pin'], 'source drift: ' + str(path))
            observed.append({'path': str(path), **actual})
    for item in manifest['helpers']:
        path = Path(item['path'])
        require(path == path.resolve(), 'helper path resolves elsewhere')
        actual = file_pin(path)
        require(actual == item['pin'], 'helper source drift: ' + str(path))
        observed.append({'path': str(path), **actual})
    return observed


def runtime_tree(roots, files):
    paths = set(files)
    for directory in roots:
        root = Path(directory)
        require(root.is_dir() and root == root.resolve(), 'runtime root changed')
        for parent, directories, names in os.walk(root):
            for name in directories:
                require(not (Path(parent) / name).is_symlink(), 'unexpected runtime directory symlink')
            paths.update(str(Path(parent) / name) for name in names)
    return [{'path': name, **file_pin(name)} for name in sorted(paths)]


def verify_runtime(manifest):
    inventory = parse_json(verified_body(manifest['runtime_inventory']['path'], manifest['runtime_inventory']['pin']))
    actual_binding = binding(manifest['interpreter']['named_path'])
    require(actual_binding == manifest['interpreter'], 'interpreter symlink/target binding changed')
    actual_files = runtime_tree(inventory['roots'], inventory['extra_files'])
    require(actual_files == inventory['files'], 'runtime package or interpreter support bytes changed')
    return {'interpreter': actual_binding, 'runtime_files_count': len(actual_files),
            'runtime_files_identity': identity(canonical(actual_files)),
            'inventory_pin': manifest['runtime_inventory']['pin']}


def write_exclusive(path, value):
    with Path(path).open('xb') as stream:
        stream.write(canonical(value))
        stream.flush()
        os.fsync(stream.fileno())
