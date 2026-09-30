"""RI159 independent administrative replay; no subject code or scientific JSON."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re

B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri159-root-grid-source-review-aligxun8';Q=B/'ri159-final-witness-grid-source-47ofu03n'
P=B/'ri157-correlated-capacity-proof-tusjyk77';V=B/'ri157-independent-cap-review-wt1tl1ip'
ROOT=B/'ri157-root-adjudication-q_wj4pny';EARLIER=B/'ri157-root-review-jco7p6tf'
ASSIGN=B/'ri158-root-fixture-review-tupyksou'/'NATIVE_REVIEW_ASSIGNMENT.json'
HELPER=B/'ri122-root-execution-review-6whn_vky'/'metadata.py'
raw=HELPER.read_bytes()
if len(raw)!=3144 or hashlib.sha256(raw).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted helper identity')
spec=importlib.util.spec_from_file_location('ri159_trusted_admin',HELPER)
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
pin({'path':str(ASSIGN),'bytes':2541,'sha256':'44f7bf8548e07a47702c25ffd9e0fa0f10c5e89e4a67db80a00754f49eb20786'},'review assignment')
pin({'path':str(Q/'HANDOFF.json'),'bytes':8831,'sha256':'424a2b10d6e3eed43c3180f0d462e925396dcba26f5ed97666bccb6be1cda635'},'subject handoff')
H=admin(Q/'HANDOFF.json');A=admin(ASSIGN)
names=['AUTHOR_CHECKS.json','CONSEQUENCE_LEDGER.md','CONTRACT.md','DEPENDENCY_NOTES.md','HANDOFF.json','HANDOFF.md','QUALIFICATION_CASES.md','SOURCE_DEPENDENCIES.json','SOURCE_IDENTITIES.json','grid_audit.py','grid_check.py']
need(sorted(H['namespace'])==names and sorted(p.name for p in Q.iterdir())==names,'exact eleven-file subject namespace')
need(len(H['payloads'])==10 and sorted(Path(r['path']).name for r in H['payloads'])==[n for n in names if n!='HANDOFF.json'],'complete ten subject payloads')
for row in H['payloads']:
 need(Path(row['path']).parent==Q,'subject payload directory');pin(row,'subject payload')
D=admin(Q/'SOURCE_DEPENDENCIES.json');S=admin(Q/'SOURCE_IDENTITIES.json')
rows=D['protected_files'];index={r['path']:r for r in rows}
need(len(rows)==len(index)==252 and list(index)==sorted(index),'252 unique sorted dependencies')
policies={'analytic-source-text-or-review':'text-reading-and-opaque-identity-no-execution','selected-administrative-proof-provenance':'metadata-identities-only-no-scientific-body-decoding','opaque-historical-acceptance-or-source-support':'opaque-bytes-only-no-recursive-reference-expansion','opaque-scientific-historical-premise':'opaque-bytes-only-no-scientific-body-decoding'}
classes={}
for n,row in enumerate(rows,1):
 need(set(row)=={'role','path','identity','classification','access_policy','reference_provenance'},'closed dependency row: '+row['path'])
 need(row['role']=='dep_%04d'%n and row['identity']['path']==row['path'],'ordered role/path: '+row['path'])
 need(set(row['identity'])=={'path','resolved_path','bytes','sha256','symlinks'},'closed manifest identity: '+row['path'])
 need(row['classification'] in policies and row['access_policy']==policies[row['classification']],'classification/access: '+row['path'])
 classes[row['classification']]=classes.get(row['classification'],0)+1;pin(row['identity'],row['path'])
need(classes=={'analytic-source-text-or-review':91,'selected-administrative-proof-provenance':88,'opaque-historical-acceptance-or-source-support':71,'opaque-scientific-historical-premise':2},'all four access classes')
need(sum(r['identity']['bytes'] for r in rows)==16345304,'bounded total selected bytes')
old=admin(P/'SOURCE_DEPENDENCIES.json')['protected_files'];need(len(old)==223,'223 predecessor rows')
omit=lambda row:{k:v for k,v in row.items() if k!='role'}
for row in old:need(row['path'] in index and same(omit(row),omit(index[row['path']])),'whole inherited row except role: '+row['path'])
additions=set()
for directory in (P,V):
 h=admin(directory/'HANDOFF.json');actual=sorted(x.name for x in directory.iterdir())
 need(actual==sorted(h['namespace']) and len(actual)==10,'complete predecessor namespace: '+str(directory))
 need(sorted(Path(x['path']).name for x in h['payloads'])==[n for n in actual if n!='HANDOFF.json'],'complete predecessor payload coverage: '+str(directory))
 for row in h['payloads']:
  need(Path(row['path']).parent==directory,'predecessor payload path');pin(row,'predecessor payload')
 additions.update(str(directory/n) for n in actual)
additions.update(str(ROOT/n) for n in ('NATIVE_SUCCESSOR_ASSIGNMENT.json','RI157_ROOT_ADJUDICATION.json','ROOT_MANUAL_REVIEW.md','ROOT_METADATA_REPLAY.json','check_native.py','METADATA_CHECK.json'))
additions.update(str(EARLIER/n) for n in ('NATIVE_REVIEW_ASSIGNMENT.json','NATIVE_PRELIMINARY_REVIEW.md'))
additions.add(S['runtime_inputs']['certificate']['path'])
need(len(additions)==29 and set(index)-{r['path'] for r in old}==additions,'complete exact29 additions')
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
need(len(refs)==1981 and len(extended)==17,'1981 historical typed references /17 preserved historical states')
historical=len(refs);scan(S,str(Q/'SOURCE_IDENTITIES.json'))
need(len(refs)-historical==48 and len(extended)==17,'48 complete current typed references')
pairs=[]
for role,left in S['source_text_counterparts']['published'].items():
 right=S['premise_texts'][role]
 need(left['path']!=right['path'] and left['path'] in index and right['path'] in index,'separate selected pair paths: '+role)
 need(Path(left['path']).read_bytes()==Path(right['path']).read_bytes(),'whole byte source counterpart: '+role)
 pairs.append({'role':role,'published':left,'external':right})
need(len(pairs)==4,'four source counterpart pairs')
roles=['certificate','original_source','original_manuscript','assignment','accepted_predecessor','accepted_manual_review']
need(list(S['runtime_inputs'])==roles,'ordered six proposed runtime inputs')
for role,row in S['runtime_inputs'].items():
 need(row['path'] in index and set(row)=={'path','bytes','sha256'},'fixed input selected closed pin: '+role);pin(row,'fixed input '+role)
# Literal metadata extraction only: not AST parsing or execution of either source.
check_text=(Q/'grid_check.py').read_text();audit_text=(Q/'grid_audit.py').read_text()
check_span=check_text.split('FIXED_IDENTITIES = (',1)[1].split('\n)\n',1)[0]
check_matches=re.findall(r'\("([a-z_]+)",\s*"([^"\n]+)",\s*([0-9]+),\s*"([0-9a-f]{64})"\)',check_span)
checkpins={role:{'path':path,'bytes':int(size),'sha256':digest} for role,path,size,digest in check_matches}
audit_span=audit_text.split('PINNED_FILES = {',1)[1].split('\n}\n',1)[0]
audit_matches=re.findall(r'"([a-z_]+)": \{\s*"path": "([^"\n]+)",\s*"bytes": ([0-9]+),\s*"sha256": "([0-9a-f]{64})",\s*\}',audit_span)
auditpins={role:{'path':path,'bytes':int(size),'sha256':digest} for role,path,size,digest in audit_matches}
need(len(check_matches)==len(audit_matches)==6 and same(checkpins,S['runtime_inputs']) and same(auditpins,S['runtime_inputs']),'both complete literal fixed-six identity maps equal metadata')
imports={}
for name,text in [('grid_check.py',check_text),('grid_audit.py',audit_text)]:
 need(re.search(r'^\s*assert\b',text,re.M) is None,'no removable assert statement: '+name)
 imports[name]=re.findall(r'^(?:from\s+([a-z_][a-z_0-9]*)\s+import|import\s+([a-z_][a-z_0-9]*))',text,re.M)
 need(len(text.splitlines())==(374 if name=='grid_check.py' else 521),'complete source line count: '+name)
need('from fractions import Fraction' in check_text and '_integer_gcd(numerator, denominator)' in audit_text and not re.search(r'^(?:from|import)\s+(?:grid_check|fractions)\b',audit_text,re.M),'independent arithmetic implementation source declarations')
qual=(Q/'QUALIFICATION_CASES.md').read_text();cases=re.findall(r'^\| ([QRP][0-9]{2}) \|',qual,re.M)
expected=['Q%02d'%n for n in range(1,36)]+['R%02d'%n for n in range(1,17)]+['P%02d'%n for n in range(1,13)]
need(cases==expected and len(set(cases))==63,'all63 ordered case/family identifiers, no execution count')
literals=[]
for name in ('CONTRACT.md','QUALIFICATION_CASES.md','CONSEQUENCE_LEDGER.md','HANDOFF.md'):
 text=(Q/name).read_text()
 need(re.search(r'^(<{7}|={7}|>{7})( |$)',text,re.M) is None,'no conflict markers: '+name)
 need(re.search(r'[ \t]+$',text,re.M) is None,'no trailing whitespace: '+name)
 for path in re.findall(r'`(/Volumes/[^` \n]+\.(?:md|json|py))`',text):
  need(path in index or (Path(path).parent==Q and Path(path).name in names),'literal selected reference: '+path);literals.append({'source':name,'path':path})
need(len(literals)==0,'zero literal absolute manuscript references')
C=admin(Q/'AUTHOR_CHECKS.json');declared=C['preseal_check']
need(declared['command_chunk']=='4333cf' and declared['exit_code']==0 and declared['receipt']['stage']=='preseal9','retained actual-author declaration, not own execution')
need(len(declared['receipt']['current_payloads'])==9 and declared['receipt']['final_fresh_identity_rechecks']==261,'author preseal9 boundary')
for row in declared['receipt']['current_payloads']:pin(row,'author preseal payload')
need(C['diagnostics']['failed_main_commands']==[] and C['diagnostics']['truncated_main_outputs']==[],'author current diagnostic declarations preserved')
need(H['qualification_cases_executed']==0 and H['qualification_fixtures_created']==0 and H['actual_grid_result'] is None,'no claimed subject qualification/grid result')
need(admin(B/'ri155-root-capacity-review-0f1typdz'/'RI157_GRID_PREMISE_CLARIFICATION.json')['reading']['exit_code']==1,'inherited failed diagnostic retained')
for path,before in list(observed.items()):need(same(m.identity(path),before),'complete fresh identity unchanged: '+path)
need(len(observed)==264,'264 full fresh identities:252dependencies11subject1assignment')
report={'schema':'ri159-root-source-admin-replay-v1','status':'PASS_ADMINISTRATIVE_IDENTITY_AND_LITERAL_BINDING_NOT_QUALIFICATION','predicates':len(checks),'dependencies':252,'selected_bytes':16345304,'inherited_rows':223,'exact_additions':sorted(additions),'classifications':classes,'administrative_bodies':88,'historical_typed_references':1981,'current_typed_references':48,'historical_extended_identities':extended,'historical_state_compared_to_current':False,'source_pairs':pairs,'literal_references':literals,'fixed_input_literal_bindings':{'producer':checkpins,'auditor':auditpins},'source_import_text':imports,'case_family_ids':cases,'cases_executed':0,'subject_namespace':names,'subject':m.ref(Q/'HANDOFF.json'),'assignment':m.ref(ASSIGN),'trusted_helper':m.ref(HELPER),'final_fresh_identities':264,'observed_identities':list(observed.values()),'typed_reference_occurrences':refs,'predicates_completed':checks,'scope':{'scientific_decode':False,'source_import_compile_AST_probe_run':False,'fixture_created':False,'scientific_or_numerical_engine':False,'runtime_card_admission':False,'repo_Git_write':False,'source_acceptance_by_metadata':False}}
ref=m.save('METADATA_CHECK.json',report)
print(json.dumps({key:report[key] for key in ('status','predicates','dependencies','selected_bytes','inherited_rows','administrative_bodies','historical_typed_references','current_typed_references','final_fresh_identities','cases_executed')},sort_keys=True))
print(json.dumps(ref,sort_keys=True))
