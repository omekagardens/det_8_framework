"""RI171 administrative protocol. UNEXECUTED; external root authenticates bootstrap."""
import hashlib
import json
import os
import stat

BASE = '/Volumes/AI_DATA/development/det-review-evidence'
VENDOR = '/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
ENV = {'LANG': 'C', 'LC_ALL': 'C', 'PATH': '/usr/bin:/bin'}
SUBJECT = BASE + '/ri169-write-would-block-repair-7_868hay/supervise_native.py'
SUBJECT_SHA = '566c5bc4ae52b775a50ea465999b6e50a99067ea6312df38c38d1ba4c8018bc6'
ROLES = ('protocol', 'driver', 'worker', 'payload', 'checker', 'manifest', 'subject')
SOURCE_DIRECTORY = BASE + '/ri182-compound-cleanup-oracle-repair-6835ytb8'
FIXED_FILES = {'protocol':'protocol.py', 'driver':'qualify_supervisor.py', 'worker':'case_worker.py', 'payload':'inert_payload.py', 'checker':'check_saved.py', 'manifest':'CASE_MANIFEST.json'}


def need(value, message):
    if not value:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False, ensure_ascii=True) + '\n').encode('ascii')


def pairs(items):
    out = {}
    for k, v in items:
        need(k not in out, 'duplicate JSON key')
        out[k] = v
    return out


def decode(raw):
    return json.loads(raw.decode('ascii'), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def capture(path, cap):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        a = os.fstat(fd)
        need(stat.S_ISREG(a.st_mode) and a.st_nlink == 1 and 0 <= a.st_size <= cap, 'private regular bounded file')
        chunks, count = [], 0
        while True:
            b = os.read(fd, min(65536, cap + 1 - count))
            if not b:
                break
            chunks.append(b)
            count += len(b)
            need(count <= cap, 'read cap')
        b = os.fstat(fd)
        signature = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        need(signature(a) == signature(b) == signature(os.lstat(path)), 'read custody changed')
        raw = b''.join(chunks)
        return raw, {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}, list(signature(b))
    finally:
        os.close(fd)


def put(path, value):
    raw = value if isinstance(value, bytes) else canonical(value)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        view = memoryview(raw)
        while view:
            n = os.write(fd, view)
            need(n > 0, 'administrative short write')
            view = view[n:]
        os.fsync(fd)
    finally:
        os.close(fd)


def bind_sources(request):
    need(set(request['sources']) == set(ROLES), 'source roles')
    bodies, observations = {}, {}
    for role in ROLES:
        expected = request['sources'][role]
        need(type(expected) is dict and set(expected) == {'path', 'bytes', 'sha256'}, 'source pin shape')
        need(expected['path'] == (SUBJECT if role == 'subject' else SOURCE_DIRECTORY + '/' + FIXED_FILES[role]), 'fixed role pathname')
        raw, got, state = capture(expected['path'], 1048576)
        need(got == expected, 'source pin differs: ' + role)
        bodies[role] = raw
        observations[role] = {'pin': got, 'state': state}
    need(request['sources']['subject']['path'] == SUBJECT and request['sources']['subject']['sha256'] == SUBJECT_SHA, 'fixed subject')
    return bodies, observations


def request(path, digest):
    need(os.path.dirname(path) == BASE and os.path.basename(path).startswith('ri171-supervisor-request-'), 'root request pathname')
    raw, pin, state = capture(path, 262144)
    need(pin['sha256'] == digest, 'external request digest')
    value = decode(raw)
    need(type(value) is dict and set(value) == {'schema', 'case_id', 'operation', 'sources', 'source_admission', 'bootstrap_preflight', 'outer_contract'}, 'closed request')
    need(value['schema'] == 'ri171-one-case-request-v1', 'request schema')
    need(type(value['case_id']) is str, 'case id type')
    op = value['operation']
    need(type(op) is str and os.path.dirname(op) == BASE and os.path.basename(op).startswith('ri171-supervisor-case-') and os.path.realpath(BASE) == BASE, 'fresh operation path shape')
    prerequisites = {}
    for name in ('source_admission', 'bootstrap_preflight', 'outer_contract'):
        item = value[name]
        need(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'}, 'external prerequisite pin')
        _, got, prior = capture(item['path'], 1048576)
        need(got == item, 'external prerequisite bytes')
        prerequisites[name] = {'pin': got, 'state': prior}
    # Their semantics/origin are independently adjudicated by root before dispatch.
    bodies, sources = bind_sources(value)
    manifest = decode(bodies['manifest'])
    matches = [row for row in manifest['cases'] if row['id'] == value['case_id']]
    need(len(matches) == 1 and manifest['subject'] == value['sources']['subject'], 'literal manifest selection')
    return value, matches[0], bodies, {'request': pin, 'request_state': state, 'sources': sources, 'prerequisites': prerequisites}


def tree(directory):
    root = os.lstat(directory)
    need(stat.S_ISDIR(root.st_mode) and not stat.S_ISLNK(root.st_mode), 'fixture root must be a real directory')
    entries, total = [], 0
    for parent, ds, files in os.walk(directory, followlinks=False):
        ds.sort()
        files.sort()
        for name in ds + files:
            p = os.path.join(parent, name)
            st = os.lstat(p)
            rel = os.path.relpath(p, directory)
            need(not stat.S_ISLNK(st.st_mode), 'unexpected fixture symlink')
            if stat.S_ISDIR(st.st_mode):
                entries.append({'path': rel, 'kind': 'directory'})
            else:
                raw, pin, _ = capture(p, 67108864)
                total += len(raw)
                need(total <= 134217728, 'complete fixture tree cap')
                entries.append({'path': rel, 'kind': 'file', 'bytes': pin['bytes'], 'sha256': pin['sha256']})
    return sorted(entries, key=lambda x: x['path'])


def postcheck(request_value, path, digest):
    """Every comparable source/prerequisite reread is attempted after earlier failure."""
    result, errors = {'sources': {}, 'prerequisites': {}}, []
    def failed(stage, exc):
        errors.append({'stage': stage, 'type': type(exc).__name__, 'message': str(exc)})
    try:
        raw, got, state = capture(path, 262144)
        result['request'], result['request_state'] = got, state
        need(got['sha256'] == digest and canonical(decode(raw)) == canonical(request_value), 'request changed')
    except BaseException as exc:
        failed('request', exc)
    for role in ROLES:
        try:
            expected = request_value['sources'][role]
            _, got, state = capture(expected['path'], 1048576)
            result['sources'][role] = {'pin': got, 'state': state}
            need(got == expected, 'source pin changed')
        except BaseException as exc:
            failed('source:'+role, exc)
    for role in ('source_admission', 'bootstrap_preflight', 'outer_contract'):
        try:
            expected = request_value[role]
            _, got, state = capture(expected['path'], 1048576)
            result['prerequisites'][role] = {'pin': got, 'state': state}
            need(got == expected, 'prerequisite pin changed')
        except BaseException as exc:
            failed('prerequisite:'+role, exc)
    return result, errors
