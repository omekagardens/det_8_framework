"""RI161 independent administrative replay; no subject code or scientific JSON."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re

B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri161-root-qualification-review-0dyyjyuy';Q=B/'ri161-grid-qualification-source-679wwadg'
P=B/'ri159-final-witness-grid-source-47ofu03n';V=B/'ri159-independent-grid-review-p1uvnluc'
ROOT=B/'ri159-root-grid-source-review-aligxun8';EARLIER=B/'ri158-root-fixture-review-tupyksou'
ASSIGN=B/'ri160-root-fixture-adjudication-0rmgmo7y'/'NATIVE_REVIEW_ASSIGNMENT.json'
HELPER=B/'ri122-root-execution-review-6whn_vky'/'metadata.py'
raw=HELPER.read_bytes()
if len(raw)!=3144 or hashlib.sha256(raw).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted helper identity')
spec=importlib.util.spec_from_file_location('ri161_trusted_admin',HELPER)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.D=R
checks=[];observed={};refs=[];extended=[]
def need(ok,label):
 if not ok:raise ValueError(label)
 checks.append(label)
def same(x,y):return json.dumps(x,sort_keys=True,allow_nan=False)==json.dumps(y,sort_keys=True,allow_nan=False)
def identity(path):
 path=str(path)
 need(Path(path).is_absolute() and os.path.normpath(path)==path,'literal absolute path: '+path)
 need(path.startswith(str(B)+'/') or path.startswith('/Volumes/AI_DATA/development/det_8_framework-ret/'),'selected evidence/source path: '+path)
 if path not in observed:observed[path]=m.identity(path)
 row=observed[path]
 need(row['bytes']<=67108864 and row['resolved_path']==path and row['symlink_chain']==[],'bounded regular resolved opaque identity: '+path)
 return row
def pin(row,label):
 need(type(row) is dict and type(row.get('path')) is str and type(row.get('bytes')) is int and row['bytes']>=0 and type(row.get('sha256')) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'typed FilePin: '+label)
 actual=identity(row['path']);need(m.pure(actual)==m.pure(row),'whole byte pin: '+label)
 for key in ('resolved_path','symlinks','symlink_chain'):
  if key in row:need(same(row[key],actual['symlink_chain'] if key=='symlinks' else actual[key]),'identity '+key+': '+label)
 return actual
def admin(path):
 before=identity(path);data=Path(path).read_bytes();need(m.pin(data)==m.pure(before),'administrative read binding: '+str(path))
 def pairs(items):
  out={}
  for key,value in items:
   if key in out:raise ValueError('duplicate administrative key: '+str(path))
   out[key]=value
  return out
 return json.loads(data,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError('nonfinite administrative metadata')))
pin({'path':str(ASSIGN),'bytes':2626,'sha256':'6e4182b5463b207f8b7d5974e78889ff7caa531210906441466828d691464843'},'review assignment')
pin({'path':str(Q/'HANDOFF.json'),'bytes':9989,'sha256':'32a5bab9518259f379f1893e56a45f7eec28dab682995b29ce6cc9ae697b9760'},'subject handoff')
H=admin(Q/'HANDOFF.json');A=admin(ASSIGN)
names=['AUTHOR_CHECKS.json','CONTRACT.md','COVERAGE.md','DEPENDENCY_NOTES.md','HANDOFF.json','HANDOFF.md','SOURCE_DEPENDENCIES.json','SOURCE_IDENTITIES.json','caller.py','fault_cases.py','qualify_grid.py']
need(sorted(H['namespace'])==names and sorted(p.name for p in Q.iterdir())==names,'exact eleven-file subject namespace')
need(len(H['payloads'])==10 and sorted(Path(r['path']).name for r in H['payloads'])==[n for n in names if n!='HANDOFF.json'],'complete ten subject payloads')
for row in H['payloads']:
 need(Path(row['path']).parent==Q,'subject payload directory');pin(row,'subject payload')
D=admin(Q/'SOURCE_DEPENDENCIES.json');S=admin(Q/'SOURCE_IDENTITIES.json')
rows=D['protected_files'];index={r['path']:r for r in rows}
need(len(rows)==len(index)==280 and list(index)==sorted(index),'280 unique sorted dependencies')
policies={'analytic-source-text-or-review':'text-reading-and-opaque-identity-no-execution','selected-administrative-proof-provenance':'metadata-identities-only-no-scientific-body-decoding','opaque-historical-acceptance-or-source-support':'opaque-bytes-only-no-recursive-reference-expansion','opaque-scientific-historical-premise':'opaque-bytes-only-no-scientific-body-decoding'}
classes={}
for n,row in enumerate(rows,1):
 need(set(row)=={'role','path','identity','classification','access_policy','reference_provenance'},'closed dependency row: '+row['path'])
 need(row['role']=='dep_%04d'%n and row['identity']['path']==row['path'],'ordered role/path: '+row['path'])
 need(set(row['identity'])=={'path','resolved_path','bytes','sha256','symlinks'},'closed manifest identity: '+row['path'])
 need(row['classification'] in policies and row['access_policy']==policies[row['classification']],'classification/access: '+row['path'])
 classes[row['classification']]=classes.get(row['classification'],0)+1;pin(row['identity'],row['path'])
need(classes=={'analytic-source-text-or-review':101,'selected-administrative-proof-provenance':98,'opaque-historical-acceptance-or-source-support':79,'opaque-scientific-historical-premise':2},'all four access classes')
need(sum(r['identity']['bytes'] for r in rows)==24169856,'bounded total selected bytes')
old=admin(P/'SOURCE_DEPENDENCIES.json')['protected_files'];need(len(old)==252,'252 predecessor rows')
omit=lambda row:{k:v for k,v in row.items() if k!='role'}
for row in old:need(row['path'] in index and same(omit(row),omit(index[row['path']])),'whole inherited row except role: '+row['path'])
additions=set()
for directory in (P,V):
 h=admin(directory/'HANDOFF.json');actual=sorted(x.name for x in directory.iterdir())
 need(actual==sorted(h['namespace']) and len(actual)==(11 if directory==P else 10),'complete predecessor namespace: '+str(directory))
 need(sorted(Path(x['path']).name for x in h['payloads'])==[n for n in actual if n!='HANDOFF.json'],'complete predecessor payload coverage: '+str(directory))
 for row in h['payloads']:
  need(Path(row['path']).parent==directory,'predecessor payload path');pin(row,'predecessor payload')
 additions.update(str(directory/n) for n in actual)
additions.update(str(ROOT/n) for n in ('NATIVE_SUCCESSOR_ASSIGNMENT.json','RI159_ROOT_ADJUDICATION.json','ROOT_MANUAL_REVIEW.md','ROOT_METADATA_REPLAY.json','METADATA_CHECK.json'))
additions.update(str(EARLIER/n) for n in ('NATIVE_REVIEW_ASSIGNMENT.json','NATIVE_PRELIMINARY_REVIEW.md'))
need(len(additions)==28 and set(index)-{r['path'] for r in old}==additions,'complete exact28 additions')
def scan(value,origin,where='$'):
 if type(value) is dict:
  if all(key in value for key in ('path','bytes','sha256')):
   need(type(value['path']) is str and (value['path'] in index or value['path']==str(Q/'SOURCE_DEPENDENCIES.json')),'closed typed reference: '+origin+where)
   pin(value,origin+where);refs.append({'origin':origin,'pointer':where,'path':value['path']})
   if 'state' in value and 'symlink_chain' in value:
    need(type(value['state']) is list and len(value['state'])==7 and all(type(v) is int for v in value['state']),'historical seven-field selection: '+origin+where)
    extended.append({'origin':origin,'pointer':where,'path':value['path'],'historical_state_not_compared_to_current':True})
  for key,v in value.items():scan(v,origin,where+'/'+key)
 elif type(value) is list:
  for n,v in enumerate(value):scan(v,origin,where+'/'+str(n))
allowed=[r['path'] for r in rows if r['classification']=='selected-administrative-proof-provenance']
for path in allowed:scan(admin(path),path)
need(len(refs)==2335 and len(extended)==17,'2335 historical typed references /17 preserved historical states')
historical=len(refs);scan(S,str(Q/'SOURCE_IDENTITIES.json'))
need(len(refs)-historical==49 and len(extended)==17,'49 complete current typed references')
pairs=[]
for role,left in S['source_text_counterparts']['published'].items():
 right=S['premise_texts'][role]
 need(left['path']!=right['path'] and left['path'] in index and right['path'] in index,'separate selected pair paths: '+role)
 need(Path(left['path']).read_bytes()==Path(right['path']).read_bytes(),'whole byte source counterpart: '+role)
 pairs.append({'role':role,'published':left,'external':right})
need(len(pairs)==4,'four source counterpart pairs')
roles=['certificate','original_source','original_manuscript','assignment','accepted_predecessor','accepted_manual_review']
need(list(S['actual_input_roles_qp04_only'])==roles,'six original QP04-only role order')
oldS=admin(P/'SOURCE_IDENTITIES.json')
need(same(S['actual_input_roles_qp04_only'],oldS['runtime_inputs']),'unchanged complete original fixed-six input map')
for role,row in S['actual_input_roles_qp04_only'].items():
 need(row['path'] in index and set(row)=={'path','bytes','sha256'},'fixed input selected closed pin: '+role);pin(row,'fixed input '+role)
need(set(S['subject_sources'])=={'checker','auditor'} and same(S['subject_sources'],H['subject_sources']),'unchanged checker/auditor declared pins')
for row in S['subject_sources'].values():pin(row,'accepted whole source')
texts={name:(Q/name).read_text() for name in ('caller.py','fault_cases.py','qualify_grid.py')}
for name,n in [('caller.py',909),('fault_cases.py',591),('qualify_grid.py',666)]:
 need(len(texts[name].splitlines())==n,'complete literal source length: '+name)
 need(re.search(r'^\s*assert\b',texts[name],re.M) is None,'no removable source assert: '+name)
# Literal pin extraction only. No AST parsing, eval, subject calls or fixture construction.
t=texts['qualify_grid.py'];span=t.split('INPUTS = {',1)[1].split('\n}',1)[0]
found=re.findall(r'"([a-z_]+)": \{\s*"path": "([^"\n]+)",\s*"bytes": ([0-9]+), "sha256": "([0-9a-f]{64})"\}',span)
qpins={role:{'path':path,'bytes':int(n),'sha256':sha} for role,path,n,sha in found}
need(len(found)==6 and same(qpins,S['actual_input_roles_qp04_only']),'qualification independent-oracle literal fixed-six references')
ct=texts['caller.py']
for role,row in S['subject_sources'].items():
 need(row['sha256'] in ct and '"bytes": '+str(row['bytes']) in ct,'caller immutable subject pin literal: '+role)
need(str(Q) in ct and str(P) in ct,'exact current and accepted source path literals')
for marker in ['for index in range(109):','for coordinate in range(3):','for key in RATIONAL_FIELDS:','for parent, keys in _dictionary_paths():']:
 need(marker in t,'complete sweep structural marker: '+marker)
need('type(error) is refusal_type' in t and 'expected_error is None and _equal(value, expected_value)' in t,'Q/R class identity and full independent result comparison')
need('type(error) is not refusal_type' in texts['fault_cases.py'] and 'passed = _same(expected, observed)' in texts['fault_cases.py'],'P class identity and full observation comparison')
need('raw = b"x" * (pins[role]["bytes"] + (1 if variation == "length" else 0))' in texts['fault_cases.py'],'same-size hash versus distinct-size pin faults')
need('report = validate_report(bytes(buffers["stdout"]), req, sha, mode)' in ct and 'result["terminal_group_empty"] = not group_exists(process.pid)' in ct,'actual report and group terminal source guards')
# Count only reviewed literal family multiplicities; no catalogue function is executed
# and no descriptor or scientific synthetic object is created.
q_counts=[1,1,1,1,109,1,1,1,1,2,1,1,1,2,1,4,5,3,9,6,8,9,9,2,2,2,6,9,11,5,8,6,5,2,1]
r_counts=[1,1,4,25,8,4,109*5,109*4,3,11,5,1,(5+6+109)+(11+7+6+4+5+6*3+109*7),9,5,2]
p_counts=[24,14,8,8,2,8,2,1,6,2,2,2]
need(len(q_counts)==35 and sum(q_counts)==237,'237 manually traced Q variant counts')
need(len(r_counts)==16 and sum(r_counts)==1994 and r_counts[12]==934,'1994 manually traced R counts including934 R13')
need(len(p_counts)==12 and sum(p_counts)==79 and sum(p_counts)-4==75,'79 manually traced P counts including4 genuine caller observations')
counts={'source_inspected_not_executed':True,'families':63,'q_variants':237,'q_records_per_mode':474,'r_records_per_mode':1994,'fault_records_per_mode':75,'caller_records_per_mode':4,'total_per_mode':2547,'total_two_modes':5094,'q05_indices_per_implementation':109,'r07_records':545,'r08_records':436,'r13_dictionary_locations':120,'r13_removals':814,'r13_extras':120}
need(sum(q_counts)*2+sum(r_counts)+sum(p_counts)==2547 and same(counts,H['planned_case_counts']),'entire prospective counts match manual review and handoff')
C=admin(Q/'AUTHOR_CHECKS.json');need(same(counts,C['manual_review']['prospective_counts']),'author counts match manually reviewed multiplicities')
need(C['administrative_check']['tool_receipt']['chunk_id']=='f4d604' and C['administrative_check']['tool_receipt']['exit_code']==0,'author actual preseal receipt retained')
expectedpre=C['administrative_check']['outcome'];need(expectedpre['stage']=='preseal9' and len(expectedpre['current_payloads'])==9 and expectedpre['final_fresh_identity_rechecks']==289,'author preseal nine-file boundary')
for row in expectedpre['current_payloads']:pin(row,'author preseal payload')
need([x for x in C['diagnostics'] if x['exit_code']==1][0]['receipts']==['eb3d76'],'author failed search retained')
need(C['scope']['qualification_cases_executed']==0 and C['scope']['actual_grid_result'] is None and H['actual']['cases_executed']==0,'source preparation has zero executed cases and no actual grid')
for name in ('CONTRACT.md','COVERAGE.md','DEPENDENCY_NOTES.md','HANDOFF.md'):
 txt=(Q/name).read_text();need(re.search(r'^(<{7}|={7}|>{7})( |$)',txt,re.M) is None,'no conflict markers: '+name)
need(admin(B/'ri155-root-capacity-review-0f1typdz'/'RI157_GRID_PREMISE_CLARIFICATION.json')['reading']['exit_code']==1,'inherited failed diagnostic preserved')
for path,before in list(observed.items()):need(same(m.identity(path),before),'complete fresh identity unchanged: '+path)
need(len(observed)==292,'292 complete identities:280dependencies11subject1reviewassignment')
report={'schema':'ri161-root-source-admin-review-v1','status':'PASS_ADMINISTRATIVE_IDENTITY_AND_LITERAL_BINDING_NOT_QUALIFICATION','predicates':len(checks),'dependencies':280,'selected_bytes':24169856,'inherited_rows':252,'exact_additions':sorted(additions),'classifications':classes,'administrative_bodies':98,'historical_typed_references':2335,'current_typed_references':49,'historical_extended_identities':extended,'historical_state_compared_to_current':False,'source_pairs':pairs,'literal_fixed_six':qpins,'literal_family_counts':{'Q_variants':q_counts,'R_records':r_counts,'P_records':p_counts},'prospective_counts':counts,'source_lines':{'caller.py':909,'fault_cases.py':591,'qualify_grid.py':666},'cases_executed':0,'subject_namespace':names,'subject':m.ref(Q/'HANDOFF.json'),'assignment':m.ref(ASSIGN),'trusted_helper':m.ref(HELPER),'final_fresh_identities':292,'observed_identities':list(observed.values()),'typed_reference_occurrences':refs,'predicates_completed':checks,'scope':{'scientific_decode':False,'source_import_compile_AST_probe_run':False,'fixture_created':False,'scientific_or_numerical_engine':False,'runtime_card_admission':False,'repo_Git_write':False,'source_acceptance_by_metadata':False}}
ref=m.save('METADATA_CHECK.json',report)
print(json.dumps({key:report[key] for key in ('status','predicates','dependencies','selected_bytes','inherited_rows','administrative_bodies','historical_typed_references','current_typed_references','final_fresh_identities','cases_executed')},sort_keys=True))
print(json.dumps(ref,sort_keys=True))
