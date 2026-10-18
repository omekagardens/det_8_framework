"""RI151 independent metadata-only review check. No scientific source is loaded."""
from pathlib import Path
import collections
import hashlib
import importlib.util
import json
import re
import traceback

R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri151-independent-face-review-uvQfBh5q')
Q=Path('/Volumes/AI_DATA/development/det-review-evidence/ri151-canonical-q-equalities-_546ie2h')
HELPER=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')

def need(ok,message):
    if not ok:
        raise ValueError(message)

raw=HELPER.read_bytes()
need(len(raw)==3144 and hashlib.sha256(raw).hexdigest()==
    'd2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7','authorized administrative helper pin')
spec=importlib.util.spec_from_file_location('m',HELPER)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.D=R

def simple(r):
    return {k:r[k] for k in ('path','bytes','sha256')}

def declared(r):
    return dict(path=r['path'],resolved_path=r['resolved_path'],bytes=r['bytes'],
                sha256=r['sha256'],symlinks=r['symlink_chain'])

def run():
    hp=m.verify(Q/'HANDOFF.json',dict(bytes=6054,sha256='8b41c6467b47de9bb30b310a2f8cf6b3020a01bafcfa317d8276f6f77811eee6'))
    h=m.load(Q/'HANDOFF.json')
    names=sorted(p.name for p in Q.iterdir())
    need(names==sorted(h['namespace']) and len(names)==10,'current exact10 namespace')
    need(len(h['payloads'])==9,'nine payloads')
    current=[hp]
    for ref in h['payloads']:
        need(Path(ref['path']).parent==Q,'payload path')
        obs=m.verify(ref['path'],ref)
        need(simple(obs)==ref,'payload exact named path')
        current.append(obs)
    need(sorted(Path(r['path']).name for r in current)==names,'payload namespace closure')
    deps=m.load(Q/'SOURCE_DEPENDENCIES.json')
    src=m.load(Q/'SOURCE_IDENTITIES.json')
    rows=deps['protected_files']
    need(len(rows)==150 and len({r['path'] for r in rows})==150,'150 unique dependencies')
    need([r['path'] for r in rows]==sorted(r['path'] for r in rows),'path order')
    observations=[]; classes=collections.Counter(); admins=[]
    known={r['path']:simple(r) for r in current}
    for n,row in enumerate(rows,1):
        need(row['role']=='dep_'+str(n).zfill(4),'role order')
        need(not row['path'].startswith(str(Q)+'/'),'no current subject dependency cycle')
        obs=m.verify(row['path'],row['identity'])
        need(declared(obs)==row['identity'] and obs['path']==row['path'],'full dependency identity')
        need(obs['bytes']<=67108864 and obs['symlink_chain']==[],'dependency cap/no symlinks')
        observations.append(obs); known[row['path']]=simple(obs)
        classes[row['classification']]+=1
        if row['classification']=='selected-administrative-proof-provenance': admins.append(row['path'])
    need(sum(x['bytes'] for x in observations)==4347537,'dependency bytes')
    need(dict(classes)=={'selected-administrative-proof-provenance':45,
        'analytic-source-text-or-review':62,'opaque-historical-acceptance-or-source-support':42,
        'opaque-scientific-historical-premise':1},'classification counts')
    predecessor=Q.parent/'ri149-singleton-hook-incidence-yfjac93v'
    old=m.load(predecessor/'SOURCE_DEPENDENCIES.json')['protected_files']
    new={r['path']:r for r in rows}
    strip=lambda r:{k:v for k,v in r.items() if k!='role'}
    need(len(old)==129,'129 predecessor rows')
    for r in old: need(strip(r)==strip(new[r['path']]),'retained row except role')
    def refs(value,out):
        if isinstance(value,dict):
            if type(value.get('path')) is str and type(value.get('bytes')) is int and type(value.get('sha256')) is str:
                ref=simple(value)
                need(ref['path'] in known and known[ref['path']]==ref,'typed reference: '+ref['path'])
                out.append(ref)
            for item in value.values(): refs(item,out)
        elif isinstance(value,list):
            for item in value: refs(item,out)
    historic=[]
    for path in admins:
        m.verify(path,known[path]); refs(m.load(path),historic)
    current_refs=[]; refs(src,current_refs)
    need(len(historic)==734 and len(current_refs)==66,'734 historical and66 current references')
    namespaces=[]
    for dirname,count in [('ri127-connected-compensation-nMyz57P5',8),('ri128-connected-sign-dvgWLqqv',11),
      ('ri127-independent-proof-review-F2Esp0RB',6),('ri128-independent-proof-source-review-Q4vXBzjt',6),
      ('ri143-independent-feasibility-review-f68n6324',7),('ri145-native-weighted-margin-proof-zo96x_ci',10),
      ('ri145-independent-proof-review-y6dp5ojt',7),('ri147-native-scale-membership-q4lxbpke',10),
      ('ri147-independent-scale-review-5qddsve3',7),
      ('ri149-singleton-hook-incidence-yfjac93v',10),('ri149-independent-canonical-review-4hzpisvg',7)]:
        directory=Q.parent/dirname
        expected=sorted(Path(r['path']).name for r in observations if Path(r['path']).parent==directory)
        need(len(expected)==count and sorted(p.name for p in directory.iterdir())==expected,'historical namespace '+dirname)
        namespaces.append(dict(path=str(directory),namespace=expected,count=count))
    pairs=[]
    for key,pub in src['source_text_counterparts']['published'].items():
        ext=src['premise_texts'][key]
        need(pub['path']!=ext['path'] and m.pure(pub)==m.pure(ext),'counterpart literal pins')
        need(Path(pub['path']).read_bytes()==Path(ext['path']).read_bytes(),'whole-byte counterpart')
        pairs.append(dict(external=ext,published=pub,whole_bytes_equal=True))
    need(len(pairs)==4,'four counterpart pairs')
    literals={}
    for name in ('NEUTRAL_COMPONENT_INCIDENCE.md','COUPLED_EQUALITY_REDUCTION.md','CANONICAL_EQUALITY_SYNTHESIS.md'):
        text=(Q/name).read_text()
        paths=re.findall(r'`(/Volumes/[^` \n]+\.(?:md|json|py))`',text)
        need(all(p in known for p in paths),'manuscript absolute literal references')
        need(not re.search(r'^(<{7}|={7}|>{7})( |$)',text,re.M),'conflict marker')
        literals[name]=paths
    need(sum(len(x) for x in literals.values())==7,'seven absolute manuscript references')
    original=src['immutable_numerical_certificate']
    need(original['fixed_targets']==['P2','P3'] and original['numerical_retry_or_retune_authorized'] is False,'original numerical targets')
    need(original['fixed_domain']=='0 < rho <= min(R,1/4), 0 < s <= 1/4; optional B14 is not a certificate-domain replacement','original domain')
    need(all(h['result'][k] is False for k in ('fixed_prefix_values_evaluated','actual_branch_or_root_order_decided','q_v_joint_budget_proved','full_H30_decided')),'actual result gaps retained')
    for observed in observations+current: need(m.identity(observed['path'])==observed,'final identity drift')
    need(sorted(p.name for p in Q.iterdir())==names,'final source namespace')
    report=dict(schema='ri151-independent-administrative-check-v1',status='PASS_METADATA_ONLY_NOT_PROOF_ACCEPTANCE',
      helper=simple(m.identity(HELPER)),subject_handoff=simple(hp),source_namespace=names,
      current_payloads=[simple(r) for r in current[1:]],dependencies=observations,
      dependency_count=150,dependency_bytes=4347537,retained129_except_role=True,addition_count=21,
      classifications=dict(classes),administrative_bodies=admins,historical_reference_occurrences=734,
      current_reference_occurrences=66,historical_namespaces=namespaces,counterparts=pairs,
      absolute_manuscript_references=literals,final_stable_identity_rechecks=160,
      original_numerical_domain_unchanged=True,scientific_body_decode=False,subject_execution=False,
      actual_coefficient_probability_history_maximum_scale_H_z_evaluation=False,symbolic_numerical_engine=False,
      runtime_controller_card_admission=False,repository_index_Git_write=False,proof_validation_by_counts_or_hashes=False)
    print(json.dumps(m.save('METADATA_CHECK.json',report),sort_keys=True))
    print(json.dumps(dict(status=report['status'],dependencies=150,bytes=4347537,historical_refs=734,current_refs=66,subject_files=10),sort_keys=True))

if __name__=='__main__':
    try: run()
    except BaseException:
        with (R/'CHECK_FAILURE.txt').open('x') as f: f.write(traceback.format_exc())
        raise
