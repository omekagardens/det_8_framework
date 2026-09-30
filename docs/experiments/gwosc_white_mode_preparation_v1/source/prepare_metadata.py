"""RI154 author-owned administrative text/opaque-byte preparation; not a driver.
No target imports, AST, compile, scientific decode, runtime inventory or cards.
"""
import hashlib,json,pathlib,stat
B=pathlib.Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri154-white-mode-preparation-42_uvw15'
S=B/'ri130-white-qualification-caller-source-Q4Aq7hZg'
Q=B/'ri141-white-bootstrap-source-h58ls076'
E=B/'ri154-white-execution-proposed-42_uvw15'
seen={}; checks=[]
def check(ok,label):
 checks.append({'check':label,'passed':bool(ok)})
 if not ok:raise ValueError(label)
def raw(p):
 p=pathlib.Path(p)
 check(str(p).startswith(str(B)+'/') or str(p).startswith('/Volumes/AI_DATA/development/det_8_framework-ret/'),'permitted source/evidence domain '+str(p))
 check('/env/' not in str(p),'not installed runtime '+str(p))
 a=p.lstat();check(stat.S_ISREG(a.st_mode),'regular opaque input '+str(p));data=p.read_bytes();z=p.lstat()
 state=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
 check(state(a)==state(z) and len(data)==a.st_size,'stable opaque read '+str(p))
 pin={'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
 if str(p) in seen:check(seen[str(p)]==pin,'repeat input unchanged '+str(p))
 seen[str(p)]=pin;return data
def ref(p):raw(p);return seen[str(p)]
def identity(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def admin(p):return json.loads(raw(p))
def verify(row):
 check(ref(row['path'])=={k:row[k] for k in ('path','bytes','sha256')},'opaque expected pin '+row['path'])
def write(name,value):
 with (R/name).open('x') as f:f.write(json.dumps(value,sort_keys=True,indent=2)+'\n')
check(not E.exists() and not E.is_symlink(),'prospective root absent; never created')
sh=admin(S/'HANDOFF.json'); check(len(sh['artifacts'])==47,'all47 sealed RI130 payloads')
for row in sh['artifacts']:verify(row)
actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
check(actual==sorted([x['relative'] for x in sh['artifacts']]+['HANDOFF.json']),'exact48 original source regular namespace')
check(not any(p.is_symlink() for p in S.rglob('*')),'sealed source namespace has no links')
t=admin(S/'TARGET_CLOSURE.source-only.json');h=admin(S/'HISTORY_CLOSURE.source-only.json');deps=admin(Q/'DEPENDENCIES.source-only.json')
check(len(t['sources'])==30 and len({x['relative'] for x in t['sources']})==30,'complete30 target records')
check(len(h)==124,'complete124 historical roles')
check(len(deps['opaque_files'])==442,'complete442 inherited preparation dependencies')
for row in deps['opaque_files']:verify(row)
for row in h:verify(row)
new_sources=[]
for row in t['sources']:
 for p in [pathlib.Path(row['original']),S/row['relative']]:check(identity(raw(p))==row['pin'],'original/copy body '+str(p))
 new_sources.append({'relative':row['relative'],'original':row['original'],'copy':str(E/row['relative']),'pin':row['pin']})
helper_names=['control.py','runtime_support.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py','profile_observe.source-only.py','guard_controls.source-only.py','TARGET_CLOSURE.source-only.json','HISTORY_CLOSURE.source-only.json']
helpers=[{'path':str(E/n),'pin':identity(raw(S/n))} for n in helper_names]
roles={'white_kernel':'science/primary/white_kernel.py','white_path':'science/primary/white_path.py','wrapper_controls':'science/primary/white_controls.py','white_contract':'science/primary/CONTRACT.md','cases':'science/primary/CASES.md','kernel_refusals':'science/primary/KERNEL_REFUSALS.md','fabricated_interfaces':'science/primary/FABRICATED_INTERFACES.md','white_refusals_text':'science/primary/WHITE_REFUSALS.md','white_source_handoff':'science/primary/HANDOFF.json','fixtures':'science/qualifier/white_fixtures.py','kernel_controls':'science/qualifier/kernel_controls.py','orchestrator':'science/qualifier/qualify_white_only.py','stage_contract':'science/qualifier/STAGE_CONTRACT.md','control_expectations':'science/qualifier/CONTROL_EXPECTATIONS.json','validator':'science/validator/white_validator.py','validator_controls':'science/validator/validator_controls.py'}
by_name={x['relative']:x for x in t['sources']}
stage={k:{'path':str(E/v),'pin':by_name[v]['pin']} for k,v in roles.items()}
stage['white_root_disposition']={'path':t['white_root']['path'],'pin':{k:t['white_root'][k] for k in ('bytes','sha256')}}
check(len(stage)==17 and len({x['path'] for x in stage.values()})==17,'all17 distinct prospective roles')
verify(t['white_root']);verify(t['integrated_root'])
guard_path=B/'ri152-root-guard-qualification-pd116byo/GUARD_ACCEPTANCE.json';guard=admin(guard_path)
profiles_path=B/'ri150-root-optimized-profile-0ydjxad3/PROFILES_ACCEPTANCE.json';profiles=admin(profiles_path)
for old,new in zip(guard['helpers'],helpers):
 check(old['path']==str(S/pathlib.Path(new['path']).name) and old['pin']==new['pin'],'old guard bytes equal proposed helper '+new['path'])
check(guard['helpers']!=helpers,'old guard card cannot satisfy new literal helper paths')
check(profiles['environment_root']!=str(E),'old environment root differs from prospective WHITE root')
check(profiles['packet']==str(S),'actual profiles bind original packet only')
known={
 'measurement_assignment':B/'ri152-root-guard-qualification-pd116byo/MEASUREMENT_NEXT_ACTION.json',
 'caller_source_acceptance':B/'ri130-root-caller-adjudication-ijhv5s6r/RI130_ROOT_ADJUDICATION.json',
 'guard_acceptance':guard_path,
 'guard_root_actual':B/'ri152-root-guard-qualification-pd116byo/RI152_ROOT_ACTUAL_ADJUDICATION.json',
 'guard_independent_handoff':B/'ri152-independent-actual65-review-ssaGIKOi/HANDOFF.json',
 'guard_independent_narrative':B/'ri152-independent-actual65-review-ssaGIKOi/INDEPENDENT_ACTUAL_REVIEW.md',
 'guard_preflight':B/'ri152-independent-guard-preflight-qvsy2hmk/HANDOFF.json',
 'guard_source_read_coverage':B/'ri152-independent-guard-preflight-qvsy2hmk/INDEPENDENT_PREFLIGHT_REVIEW.md',
 'profiles_acceptance':profiles_path,
 'normal_profile_independent':B/'ri148-independent-normal-review-fbnud7fq/HANDOFF.json',
 'optimized_profile_independent':B/'ri150-independent-optimized-review-zlcd4ret/HANDOFF.json',
 'ri141_prepare':Q/'prepare.py','ri141_runtime_metadata':Q/'runtime_metadata.py','ri141_protocol':Q/'PROTOCOL.md','ri141_handoff':Q/'HANDOFF.json','ri141_dependencies':Q/'DEPENDENCIES.source-only.json',
 'ri130_protocol':S/'PROTOCOL.md','ri130_complete_mode_contract':S/'MODE_CUSTODY_CONTRACT.md','ri130_handoff':S/'HANDOFF.json'}
known_refs={k:ref(p) for k,p in known.items()}
# Actual report bodies read here are guard/preparation metadata only; no WHITE numerical body.
for r in profiles['completions'].values():verify(r)
for r in profiles['genuine_outer'].values():verify(r)
for k in ('report','genuine_outer','independent_review'):verify(guard[k])
all_copies=[{'relative':n,'source':ref(S/n),'destination':str(E/n)} for n in actual]
source_only={'schema':'ri154-prospective-relocation-bindings-v1','status':'SOURCE_PREPARATION_ONLY_NOT_AUTHORIZATION','prospective_root':str(E),'root_created':False,'copied_file_count':48,'copied_files':all_copies,'helper_count':11,'helpers':helpers,'target_count':30,'sources':new_sources,'stage_role_count':17,'stage_bindings':stage,'history_count':124,'history_originals':h,'integrated_root':t['integrated_root'],'prior_original_guard_helpers':guard['helpers'],'old_environment_root':profiles['environment_root'],'proposed_environment':{'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','TMPDIR':str(E/'tmp'),'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'},'source_changes':[],'all_proposed_copies_uncreated':True,'dynamic_root_note':'This literal proposed root is not reserved or created as an operation. Root may adopt it only after review, or explicitly regenerate this entire path map for a different fresh root and review the deterministic map. Never partially edit or repoint accepted records.','evidence':known_refs}
write('BINDING_GRAPH.source-only.json',source_only)
write('DEPENDENCIES.json',{'schema':'ri154-source-preparation-dependencies-v1','status':'OPAQUE_CURRENT_SOURCE_AND_SAVED_EVIDENCE_ONLY','inherited_ri141_count':442,'inherited_ri141':deps['opaque_files'],'direct_premises':known_refs,'complete_read_files':sorted(seen.values(),key=lambda x:x['path']),'runtime_installed_files_read':0,'scientific_body_decode':False})
write('PREPARATION_CHECK.json',{'schema':'ri154-administrative-preparation-check-v1','status':'PASS','checks':checks,'counts':{'ri130_files':48,'prospective_copies':48,'target_pairs':30,'helpers':11,'history_roles':124,'stage_roles':17,'inherited_dependencies':442,'unique_opaque_inputs':len(seen)},'prohibited_actions_performed':[],'qualification_claim':False,'driver_implemented':False,'proposed_root_created':False})
print(json.dumps({'status':'PASS','checks':len(checks),'unique_inputs':len(seen),'prospective_root_absent':True,'outputs':['BINDING_GRAPH.source-only.json','DEPENDENCIES.json','PREPARATION_CHECK.json']},sort_keys=True))
