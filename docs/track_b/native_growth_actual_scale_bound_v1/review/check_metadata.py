"""RI147 independent administrative check; no scientific decoding or evaluation."""
from pathlib import Path
import collections
import hashlib
import importlib.util
import json
import re
import traceback

R = Path('/Volumes/AI_DATA/development/det-review-evidence/ri147-independent-scale-review-5qddsve3')
Q = Path('/Volumes/AI_DATA/development/det-review-evidence/ri147-native-scale-membership-q4lxbpke')
HP = Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')

def need(value, message):
    if not value:
        raise ValueError(message)

# Authenticate the explicitly root-authorized administrative helper before load.
raw = HP.read_bytes()
need(len(raw) == 3144 and hashlib.sha256(raw).hexdigest() ==
     'd2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7', 'root helper pin')
spec = importlib.util.spec_from_file_location('m', HP)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.D = R

def simple(row):
    return {k: row[k] for k in ('path', 'bytes', 'sha256')}

def manifest_identity(row):
    return dict(path=row['path'], resolved_path=row['resolved_path'],
                bytes=row['bytes'], sha256=row['sha256'], symlinks=row['symlink_chain'])

def run():
    handoff_pin = m.verify(Q/'HANDOFF.json', dict(bytes=6645, sha256=
        'a963f33ba976b9972fe4867bb5790f76e77857971e73f43b0876a4107b97b1e2'))
    handoff = m.load(Q/'HANDOFF.json')
    namespace = sorted(p.name for p in Q.iterdir())
    need(namespace == sorted(handoff['namespace']) and len(namespace) == 10, 'exact10 namespace')
    need(len(handoff['payloads']) == 9, 'nine payloads')
    current = [handoff_pin]
    for row in handoff['payloads']:
        need(Path(row['path']).parent == Q, 'payload path')
        got = m.verify(row['path'], row)
        need(simple(got) == row, 'payload named path')
        current.append(got)
    need(sorted(Path(row['path']).name for row in current) == namespace, 'payload closure')
    deps = m.load(Q/'SOURCE_DEPENDENCIES.json')
    premise = m.load(Q/'SOURCE_IDENTITIES.json')
    rows = deps['protected_files']
    need(len(rows) == 108 and len({r['path'] for r in rows}) == 108, '108 unique dependencies')
    need([r['path'] for r in rows] == sorted(r['path'] for r in rows), 'sorted dependency paths')
    known = {r['path']:simple(r) for r in current}
    observations, administrative, classes = [], [], collections.Counter()
    for n, row in enumerate(rows, 1):
        need(row['role'] == 'dep_'+str(n).zfill(4), 'role order')
        need(not row['path'].startswith(str(Q)+'/'), 'acyclic source dependency')
        observed = m.verify(row['path'], row['identity'])
        need(manifest_identity(observed) == row['identity'] and observed['path'] == row['path'], 'full named resolved link identity')
        observations.append(observed)
        known[row['path']] = simple(observed)
        classes[row['classification']] += 1
        if row['classification'] == 'selected-administrative-proof-provenance':
            administrative.append(row['path'])
    need(sum(r['bytes'] for r in observations) == 3505381, 'selected dependency byte count')
    need(dict(classes) == {'analytic-source-text-or-review':50,
        'selected-administrative-proof-provenance':25,
        'opaque-historical-acceptance-or-source-support':32,
        'opaque-scientific-historical-premise':1}, 'classification counts')
    old_path = Q.parent/'ri145-native-weighted-margin-proof-zo96x_ci'/'SOURCE_DEPENDENCIES.json'
    old = m.load(old_path)['protected_files']
    new_by_path = {r['path']:r for r in rows}
    for row in old:
        new = new_by_path[row['path']]
        need({k:v for k,v in row.items() if k != 'role'} ==
             {k:v for k,v in new.items() if k != 'role'}, 'retained86 row content')
    need(len(old) == 86 and len(rows)-len(old) == 22, '86 retained +22 additions')
    def refs(value, output):
        if isinstance(value, dict):
            if (type(value.get('path')) is str and type(value.get('bytes')) is int
                    and type(value.get('sha256')) is str):
                ref = simple(value)
                need(ref['path'] in known and known[ref['path']] == ref,
                     'typed reference closure: '+ref['path'])
                output.append(ref)
            for child in value.values():
                refs(child, output)
        elif isinstance(value, list):
            for child in value:
                refs(child, output)
    historical_refs = []
    for path in administrative:
        m.verify(path, known[path])
        refs(m.load(path), historical_refs)
    current_refs = []
    refs(premise, current_refs)
    need(len(historical_refs) == 309 and len(current_refs) == 53, '309+53 typed reference occurrences')
    namespaces = []
    for name,count in [('ri127-connected-compensation-nMyz57P5',8),
        ('ri128-connected-sign-dvgWLqqv',11),('ri127-independent-proof-review-F2Esp0RB',6),
        ('ri128-independent-proof-source-review-Q4vXBzjt',6),('ri143-independent-feasibility-review-f68n6324',7),
        ('ri145-native-weighted-margin-proof-zo96x_ci',10),('ri145-independent-proof-review-y6dp5ojt',7)]:
        directory = Q.parent/name
        expected = sorted(Path(r['path']).name for r in observations if Path(r['path']).parent == directory)
        need(len(expected) == count and sorted(p.name for p in directory.iterdir()) == expected, 'selected historical namespace '+name)
        namespaces.append(dict(path=str(directory), namespace=expected, count=count))
    counterparts = []
    for key,published in premise['source_text_counterparts']['published'].items():
        external = premise['premise_texts'][key]
        need(published['path'] != external['path'], 'distinct literal counterpart paths')
        need(m.pure(published) == m.pure(external), 'counterpart pins')
        need(Path(published['path']).read_bytes() == Path(external['path']).read_bytes(), 'counterpart whole bytes')
        counterparts.append(dict(external=external,published=published,whole_bytes_equal=True))
    need(len(counterparts) == 4, 'four counterparts')
    literals = {}
    for name in ('COMPONENT_CONTRASTS.md','ACTUAL_SCALE_BOUND.md','SCALE_MEMBERSHIP_SYNTHESIS.md'):
        paths = re.findall(r'/Volumes/[^\s`\)]+?\.(?:md|json|py)', (Q/name).read_text())
        need(all(p in known for p in paths), 'manuscript literal reference closure')
        literals[name] = paths
    need(sum(len(v) for v in literals.values()) == 25, '25 literal references')
    original = premise['immutable_numerical_certificate']
    need(original['fixed_targets'] == ['P2','P3'] and original['numerical_retry_or_retune_authorized'] is False, 'original numerical target boundary')
    need(original['fixed_domain'] == '0 < rho <= min(R,1/4), 0 < s <= 1/4; optional B14 is not a certificate-domain replacement', 'original numerical domain')
    need(all(v is False for v in handoff['actual_results'].values()), 'remaining actual results')
    for old_observation in observations+current:
        need(m.identity(old_observation['path']) == old_observation, 'end identity drift')
    need(sorted(p.name for p in Q.iterdir()) == namespace, 'end source namespace')
    report = dict(schema='ri147-independent-administrative-check-v1',
        status='PASS_ADMINISTRATIVE_IDENTITIES_ONLY', helper=simple(m.identity(HP)),
        subject_handoff=simple(handoff_pin), source_namespace=namespace,
        current_payloads=[simple(r) for r in current[1:]], dependencies=observations,
        dependency_count=108, dependency_bytes=3505381, retained86_except_role=True,
        added_dependency_count=22, classifications=dict(classes),
        administrative_bodies=administrative, historical_reference_occurrences=309,
        current_reference_occurrences=53, selected_historical_namespaces=namespaces,
        whole_byte_counterparts=counterparts,literal_references=literals,
        final_stable_identity_rechecks=118,original_numerical_domain_retained=True,
        scientific_body_decode=False,scientific_execution=False,symbolic_engine=False,
        actual_coefficient_scale_maximum_seed_H_evaluation=False,
        runtime_card_or_admission=False,proof_acceptance_by_checker=False)
    print(json.dumps(m.save('METADATA_CHECK.json', report),sort_keys=True))
    print(json.dumps(dict(dependencies=108,bytes=3505381,historical_refs=309,current_refs=53,
        source_files=10,status=report['status']),sort_keys=True))

if __name__ == '__main__':
    try:
        run()
    except BaseException:
        with (R/'CHECK_FAILURE.txt').open('x') as f:
            f.write(traceback.format_exc())
        raise
