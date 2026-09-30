"""Reviewer-owned administrative opaque/text check. Never imports any subject."""
import hashlib,json,os,re,stat
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri152-independent-guard-preflight-qvsy2hmk'
S=B/'ri130-white-qualification-caller-source-Q4Aq7hZg'
Q=B/'ri141-white-bootstrap-source-h58ls076'
REPO=Path('/Volumes/AI_DATA/development/det_8_framework-ret')
reads={}; checks=[]
def need(v,label):
    if not v: raise ValueError(label)
    checks.append(label)
def raw(path):
    p=Path(path)
    need(p.is_relative_to(B) or p.is_relative_to(REPO/'docs'), 'read boundary '+str(p))
    before=p.lstat(); need(stat.S_ISREG(before.st_mode) and not p.is_symlink(), 'regular '+str(p))
    data=p.read_bytes(); after=p.lstat()
    need(before==after, 'stable opaque read '+str(p))
    row={'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    if str(p) in reads: need(reads[str(p)]==row, 'same repeated identity '+str(p))
    reads[str(p)]=row
    return data
def pin(path): raw(path); return reads[str(path)]
def obj(path): return json.loads(raw(path))
def verify(row):
    got=pin(row['path']); need(got=={k:row[k] for k in ('path','bytes','sha256')}, 'whole pin '+row['path'])
    return got
def save(name,v):
    data=(json.dumps(v,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
    with (R/name).open('xb') as f:f.write(data)
    return {'path':str(R/name),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def tree(root):
    rows=[]
    for parent,dirs,files in os.walk(root,followlinks=False):
        for n in dirs+files:
            p=Path(parent)/n; st=p.lstat(); rel=str(p.relative_to(root))
            if stat.S_ISLNK(st.st_mode): row={'relative':rel,'kind':'symlink','target':os.readlink(p)}
            elif stat.S_ISDIR(st.st_mode):row={'relative':rel,'kind':'directory'}
            else:
                got=pin(p);row={'relative':rel,'kind':'file','bytes':got['bytes'],'sha256':got['sha256']}
            rows.append(row)
    return sorted(rows,key=lambda x:x['relative'])
sh=obj(S/'HANDOFF.json'); qh=obj(Q/'HANDOFF.json'); d=obj(Q/'DEPENDENCIES.source-only.json')
need(len(sh['artifacts'])==47,'47 original RI130 payloads')
for r in sh['artifacts']:verify(r)
actual_tree=tree(S);need(actual_tree==d['packet_namespace'],'entire RI130 files/directories namespace')
need(len([r for r in actual_tree if r['kind']=='file'])==48,'48 RI130 files including HANDOFF')
need(len(qh['files'])==14,'14 original RI141 payloads')
for r in qh['files']:verify(r)
need(sorted(p.name for p in Q.iterdir())==qh['exact_namespace'],'exact15 RI141 namespace')
need(len(d['opaque_files'])==442 and len({r['path'] for r in d['opaque_files']})==442,'442 distinct opaque dependencies')
for r in d['opaque_files']:verify(r)
need(sum(r['bytes'] for r in d['opaque_files'])==25947539,'25947539 dependency bytes')
target=obj(S/'TARGET_CLOSURE.source-only.json'); history=obj(S/'HISTORY_CLOSURE.source-only.json')
need(len(target['sources'])==30 and len(history)==124,'30 source pairs and124 history rows')
for r in target['sources']:
    old=pin(r['original']);new=pin(S/r['relative'])
    need({k:old[k] for k in ('bytes','sha256')}==r['pin']=={k:new[k] for k in ('bytes','sha256')},'exact original/copy '+r['relative'])
for r in history:verify(r)
need(sum(r['bytes'] for r in history)==10625600,'124 historical bytes sum')
family=[('parent',['source','caller','runtime_acceptance','mode','late','late_postcheck']),('worker',['source','caller','runtime_acceptance','mode','late','late_postcheck']),('capture',['positive','changed_copy','buffer_drift','occupied']),('monitor',['positive','no_sample','wall','initial_gap','sample_gap','rss','nonzero','malformed','timeout','final_gap']),('runtime',['positive','absent_file','absent_dangling_link','missing_loader','changed_loader_declaration','changed_loader_path','missing_config']),('static',['positive','actual','extra','bool_limit','source_omitted','source_copy','helper_omitted','mode_command']),('acceptance',['positive','source_execution','caller_binding','caller_history','caller_ret','guards_absent','runtime_binding','runtime_loader','runtime_profile']),('mode',['normal_positive','optimized_positive','wrong_command','pre_missing','normal_incomplete','normal_drift']),('relation',['positive','science_file','wrong_link','extra_envelope','missing_artifact','postcheck','extra_namespace','control_message','tail_dropped'])]
ids=[a+'_'+b for a,bs in family for b in bs]
need(len(ids)==len(set(ids))==65,'65 unique literal reviewed IDs')
need(sh['caller_guard_declarations']['ordered_ids']==ids,'source handoff exact65 order')
kt=raw(S/'caller_contract.py').decode();qt=raw(Q/'prepare.py').decode();ht=raw(S/'guard_controls.source-only.py').decode()
def ids_text(t):return t[t.index('GUARD_IDS = tuple('):].split('])',1)[0]+'])'
need(ids_text(kt)==ids_text(qt),'verbatim RI130/RI141 GUARD_IDS expressions; no eval')
# Literal dispatch tuples checked against hand-read family lists, without subject evaluation.
for a,bs in family:
    if a in ('parent','worker'):continue
    literal='('+','.join(repr(x) for x in bs)+')'
    need(literal in ht, 'harness literal dispatch tuple '+a)
need("for side in ('parent','worker')" in ht and "('source','caller','runtime_acceptance','mode','late','late_postcheck')" in ht,'harness ordered failure side/kind tuples')
coverage={}
for p in [S/x for x in ('guard_controls.source-only.py','control.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py','runtime_support.py')]+[Q/'prepare.py',Q/'runtime_metadata.py']:
    data=raw(p);coverage[str(p)]={'lines':len(data.splitlines()),'pin':reads[str(p)],'fresh_manual_complete_read':True}
need(sum(x['lines'] for x in coverage.values())==2820,'2820 complete fresh subject lines')
for p in [S/'PROTOCOL.md',Q/'PROTOCOL.md',B/'ri130-root-caller-adjudication-ijhv5s6r/ROOT_SOURCE_REVIEW.md',B/'ri130-root-caller-adjudication-ijhv5s6r/RI130_ROOT_ADJUDICATION.json',B/'ri140-root-source-adjudication-8796wh9l/RI141_ROOT_ADJUDICATION.json',B/'ri130-caller-independent-review-GpeTxmLW/INDEPENDENT_SOURCE_REVIEW.md',B/'ri141-bootstrap-independent-review-k5bss5xp/INDEPENDENT_SOURCE_REVIEW.md',B/'ri148-independent-normal-review-fbnud7fq/HANDOFF.json',B/'ri150-independent-optimized-review-zlcd4ret/HANDOFF.json']:
    pin(p)
a=obj(B/'ri150-root-optimized-profile-0ydjxad3/PROFILES_ACCEPTANCE.json')
need(reads[str(B/'ri150-root-optimized-profile-0ydjxad3/PROFILES_ACCEPTANCE.json')]['sha256']=='4bf521e8e8cceafce449b0e8620c515df53a2cb2b2d1c0ff612cbb4934c91716','specified current profiles acceptance pin')
need(a['stage']=='profiles' and a['status']=='ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE' and a['scientific_execution'] is False,'bounded both-profile acceptance scope')
need(a['packet']==str(S),'profiles original packet binding')
for name,value in a['sources'].items():
    got=pin(Q/name);need({k:got[k] for k in ('bytes','sha256')}==value,'profiles preparation source '+name)
need(set(a['completions'])==set(a['genuine_outer'])=={'profile_normal','profile_optimized'},'both exact predecessor modes')
for r in list(a['completions'].values())+list(a['genuine_outer'].values())+[a['independent_review']]:verify(r)
spec=obj(S/'science/qualifier/CONTROL_EXPECTATIONS.json')
need(len(spec['order'])==179 and len(spec['refusals'])==176,'authentic admin first-refusal inventory')
need(spec['order'][-3:]==['WT01','WT02','WT03'],'three complete tail schemas remain distinct')
# No numerical fixture/certificate/result body is decoded. No current vendor/runtime file observed.
result={'schema':'ri152-independent-source-preflight-check-v1','status':'PASS_SOURCE_AND_OPAQUE_PREREQUISITES_ONLY','check_count':len(checks),'checks':checks,'read_inputs':sorted(reads.values(),key=lambda x:x['path']),'counts':{'ri130_files':48,'ri130_directories':len([r for r in actual_tree if r['kind']=='directory']),'ri141_files':15,'opaque_dependencies':442,'opaque_dependency_bytes':25947539,'source_pairs':30,'history':124,'history_bytes':10625600,'fresh_source_lines':2820,'guard_cases_declared':65,'guard_cases_executed':0},'read_coverage':coverage,'ordered_guard_ids':ids,'controls':{'target_import_compile_ast_probe_execution':False,'scientific_body_decode':False,'runtime_capture':False,'active_card_or_admission':False,'repository_or_git_write':False}}
r=save('OPAQUE_PREFLIGHT_CHECK.json',result)
print(json.dumps({'status':'PASS','checks':len(checks),'read_inputs':len(reads),'result':r},sort_keys=True))
