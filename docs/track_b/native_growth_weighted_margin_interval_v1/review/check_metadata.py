"""Independent administrative identities only; no scientific decoding or evaluation."""
from pathlib import Path
import collections
import hashlib
import json
import os
import re
import stat
import traceback

R = Path('/Volumes/AI_DATA/development/det-review-evidence/ri145-independent-proof-review-y6dp5ojt')
Q = Path('/Volumes/AI_DATA/development/det-review-evidence/ri145-native-weighted-margin-proof-zo96x_ci')
CAP = 67108864

def need(ok, message):
    if not ok:
        raise ValueError(message)

def signature(s):
    return (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns)

def identity(path, retain=False):
    path = Path(path)
    need(path.is_absolute() and path.resolve(strict=True) == path, 'literal path: '+str(path))
    prefix = Path('/')
    for component in path.parts[1:]:
        prefix /= component
        need(not prefix.is_symlink(), 'symlink component: '+str(prefix))
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_size <= CAP, 'bounded regular')
    digest, size, pieces = hashlib.sha256(), 0, []
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as source:
        need(signature(os.fstat(source.fileno())) == signature(before), 'open drift')
        while True:
            block = source.read(65536)
            if not block:
                break
            size += len(block)
            need(size <= CAP, 'read cap')
            digest.update(block)
            if retain:
                pieces.append(block)
        need(signature(os.fstat(source.fileno())) == signature(before), 'descriptor drift')
    need(signature(path.lstat()) == signature(before) and size == before.st_size, 'path drift')
    return {'path': str(path), 'resolved_path': str(path), 'bytes': size,
            'sha256': digest.hexdigest(), 'symlinks': []}, b''.join(pieces) if retain else None

def simple(row):
    return {k: row[k] for k in ('path', 'bytes', 'sha256')}

def parse(body):
    def pairs(items):
        value = {}
        for key, val in items:
            need(key not in value, 'duplicate administrative key')
            value[key] = val
        return value
    def bad(value):
        raise ValueError('nonfinite administrative number: '+value)
    return json.loads(body, object_pairs_hook=pairs, parse_constant=bad)

def load(path):
    pin, raw = identity(path, True)
    return pin, parse(raw)

def run():
    assigned, handoff = load(Q/'HANDOFF.json')
    need(assigned['bytes'] == 6015 and assigned['sha256'] == 'f53a0e1c49069a1e9057ad69169facca556b77e7cfb2534eba440b7eaa91db19', 'assigned source pin')
    namespace = sorted(p.name for p in Q.iterdir())
    need(namespace == sorted(handoff['namespace']) and len(namespace) == 10, 'current namespace')
    need(len(handoff['payloads']) == 9, 'payload count')
    actuals = [assigned]
    for expected in handoff['payloads']:
        got, _ = identity(expected['path'])
        need(simple(got) == expected and Path(got['path']).parent == Q, 'current payload pin')
        actuals.append(got)
    need(sorted(Path(x['path']).name for x in actuals) == namespace, 'payload domain')
    dpin, deps = load(Q/'SOURCE_DEPENDENCIES.json')
    spin, subject = load(Q/'SOURCE_IDENTITIES.json')
    rows = deps['protected_files']
    need(len(rows) == 86 and len({row['path'] for row in rows}) == 86, '86 unique dependencies')
    need([row['path'] for row in rows] == sorted(row['path'] for row in rows), 'dependency order')
    known = {str(Q/'SOURCE_DEPENDENCIES.json'): simple(dpin)}
    classes, pins, administrative = collections.Counter(), [], []
    for index, row in enumerate(rows, 1):
        need(row['role'] == 'dep_'+str(index).zfill(4), 'ordered roles')
        need(not row['path'].startswith(str(Q)+'/'), 'acyclic dependency selection')
        got, _ = identity(row['path'])
        need(got == row['identity'] and got['path'] == row['path'], 'dependency identity')
        pins.append(got)
        known[row['path']] = simple(got)
        classes[row['classification']] += 1
        if row['classification'] == 'selected-administrative-proof-provenance':
            administrative.append(row['path'])
    need(sum(row['bytes'] for row in pins) == 3098788, 'dependency bytes')
    need(dict(classes) == {'analytic-source-text-or-review': 42,
                         'opaque-historical-acceptance-or-source-support': 27,
                         'opaque-scientific-historical-premise': 1,
                         'selected-administrative-proof-provenance': 16}, 'classification counts')
    def refs(value, output):
        if isinstance(value, dict):
            if (type(value.get('path')) is str and type(value.get('bytes')) is int
                    and type(value.get('sha256')) is str):
                expected = {k: value[k] for k in ('path', 'bytes', 'sha256')}
                need(expected['path'] in known and known[expected['path']] == expected,
                     'typed reference: '+expected['path'])
                output.append(expected)
            for child in value.values():
                refs(child, output)
        elif isinstance(value, list):
            for child in value:
                refs(child, output)
    historic_refs = []
    administrative_pins = []
    for path in administrative:
        pin, value = load(path)
        need(simple(pin) == known[path], 'admin pin before decode')
        administrative_pins.append(simple(pin))
        refs(value, historic_refs)
    need(len(historic_refs) == 132, '132 historical typed references')
    current_refs = []
    refs(subject, current_refs)
    need(len(current_refs) == 45, '45 current premise references')
    directories = [('ri127-connected-compensation-nMyz57P5',8),
                   ('ri128-connected-sign-dvgWLqqv',11),
                   ('ri127-independent-proof-review-F2Esp0RB',6),
                   ('ri128-independent-proof-source-review-Q4vXBzjt',6),
                   ('ri143-independent-feasibility-review-f68n6324',7)]
    namespaces = []
    for name, count in directories:
        path = Q.parent/name
        expected = sorted(Path(x['path']).name for x in pins if Path(x['path']).parent == path)
        need(len(expected) == count and sorted(p.name for p in path.iterdir()) == expected,
             'historical namespace: '+str(path))
        namespaces.append({'path':str(path),'namespace':expected,'count':count})
    counterparts = []
    for key, published in subject['source_text_counterparts']['published'].items():
        external = subject['premise_texts'][key]
        need(external['path'] != published['path'], 'distinct actual/published paths')
        ep, eb = identity(external['path'], True)
        pp, pb = identity(published['path'], True)
        need(simple(ep) == external and simple(pp) == published and eb == pb, 'whole-byte counterpart')
        counterparts.append({'actual_read':external, 'published':published, 'whole_bytes_equal':True})
    need(len(counterparts) == 4, 'four counterparts')
    literal_references = {}
    for name in ('WEIGHTED_MARGIN_PROOF.md','ENDPOINT_REDUCTION.md','PROOF_CROSSCHECK.md'):
        _, raw = identity(Q/name, True)
        paths = re.findall(r'/Volumes/[^\s`\)]+?\.md', raw.decode('utf-8'))
        need(all(path in known for path in paths), 'literal manuscript path closure')
        literal_references[name] = paths
    need([len(literal_references[name]) for name in literal_references] == [0,12,7], 'literal reference counts')
    original = subject['immutable_numerical_certificate']
    need(original['fixed_targets'] == ['P2','P3'] and original['numerical_retry_or_retune_authorized'] is False,
         'old targets unchanged')
    need(original['fixed_domain'] == '0 < rho <= min(R,1/4), 0 < s <= 1/4; optional B14 is not a certificate-domain replacement', 'old domain')
    _, result = load(Q/'ANALYTIC_RESULT.json')
    need(result['scope']['scientific_body_decode'] is False
         and result['scope']['subject_helper_import_compile_AST_probe_run'] is False
         and result['review']['independent_acceptance'] is False, 'author scope only')
    need(all(result['not_established'].values()), 'actual result gaps retained')
    # Check selected identities again at end; this is not runtime custody.
    for expected in pins+actuals:
        got, _ = identity(expected['path'])
        need(got == expected, 'final identity drift')
    need(sorted(p.name for p in Q.iterdir()) == namespace, 'final source namespace')
    report = {'schema':'ri145-independent-proof-metadata-check-v1',
      'status':'PASS_ADMINISTRATIVE_IDENTITIES_ONLY',
      'subject_handoff':simple(assigned),'source_namespace':namespace,
      'source_payloads':[simple(x) for x in actuals if x['path'] != str(Q/'HANDOFF.json')],
      'dependencies':pins,'dependency_count':86,'dependency_bytes':3098788,
      'classifications':dict(classes),'administrative_bodies':administrative_pins,
      'administrative_reference_occurrences':132,'current_premise_reference_occurrences':45,
      'historical_namespaces':namespaces,'counterparts':counterparts,
      'literal_references':literal_references,
      'original_numerical_targets_domain_unchanged':True,
      'science_object_access':'Only opaque byte identity; no scientific body decoded, searched or displayed.',
      'scientific_evaluation':False,'symbolic_engine':False,'subject_execution':False,
      'current_runtime_observed':False,'execution_admitted':False,'proof_accepted_by_checker':False}
    with (R/'METADATA_CHECK.json').open('x') as out:
        json.dump(report,out,sort_keys=True,indent=2)
        out.write('\n')
    print(json.dumps({'status':report['status'],'dependencies':86,'bytes':3098788,
                     'reference_occurrences':177,'subject_files':10,'proof_execution':False},sort_keys=True))

if __name__ == '__main__':
    try:
        run()
    except BaseException:
        with (R/'CHECK_FAILURE.txt').open('x') as output:
            output.write(traceback.format_exc())
        raise
