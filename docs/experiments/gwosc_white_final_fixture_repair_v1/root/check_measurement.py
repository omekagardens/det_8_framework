"""RI160 independent administrative identities/text only; never imports subject code."""
import difflib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re

R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri160-root-fixture-adjudication-0rmgmo7y')
Q=R.parent/'ri160-white-fixture-custody-repair-ufok1zpo'
P=R.parent/'ri158-white-custody-repair-68cdvzn6'
V=R.parent/'ri158-independent-repair-review-nxij3eju'
D=R.parent/'ri158-root-fixture-review-tupyksou'
A=R.parent/'ri159-root-grid-source-review-aligxun8'/'MEASUREMENT_REVIEW_ASSIGNMENT.json'
HELPER=R.parent/'ri122-root-execution-review-6whn_vky'/'metadata.py'
b=HELPER.read_bytes()
if len(b)!=3144 or hashlib.sha256(b).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('administrative helper differs')
spec=importlib.util.spec_from_file_location('ri160_trusted_metadata',HELPER)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.D=R
predicates=[];observed={}
def need(ok,label):
 if not ok:raise ValueError(label)
 predicates.append(label)
def same(a,b):return json.dumps(a,sort_keys=True,allow_nan=False)==json.dumps(b,sort_keys=True,allow_nan=False)
def observe(p):
 p=str(p)
 need(os.path.normpath(p)==p and (p.startswith(str(R.parent)+'/') or p.startswith('/Volumes/AI_DATA/development/det_8_framework-ret/')),'bounded source/evidence path: '+p)
 if p not in observed:observed[p]=m.identity(p)
 x=observed[p];need(x['resolved_path']==p and x['symlink_chain']==[] and x['bytes']<=67108864,'bounded literal opaque identity: '+p)
 return x
def pin(row,label):
 need(type(row) is dict and set(row)=={'path','bytes','sha256'} and type(row['path']) is str and type(row['bytes']) is int and row['bytes']>=0 and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'closed typed FilePin: '+label)
 need(m.pure(observe(row['path']))==m.pure(row),'whole pin: '+label)
def load(p):
 before=observe(p);raw=Path(p).read_bytes();need(m.pin(raw)==m.pure(before),'administrative body linked: '+str(p))
 def pairs(items):
  out={}
  for k,v in items:
   if k in out:raise ValueError('duplicate metadata key: '+str(p))
   out[k]=v
  return out
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError('nonfinite metadata')))
def seal(directory,expected_count):
 h=load(directory/'HANDOFF.json');names=sorted(x.name for x in directory.iterdir())
 need(names==sorted(h['namespace']) and len(names)==expected_count,'whole exact namespace: '+str(directory))
 need(sorted(Path(x['path']).name for x in h['payloads'])==[n for n in names if n!='HANDOFF.json'],'complete payload coverage: '+str(directory))
 for x in h['payloads']:
  need(Path(x['path']).parent==directory,'payload own directory: '+x['path']);pin(x,'sealed payload')
 return h,names
pin({'path':str(Q/'HANDOFF.json'),'bytes':14881,'sha256':'a0067b9dbacf3ae293260cae242ee646c67c53a0c32ed25d0f47ab3c4056b00f'},'current handoff')
pin({'path':str(A),'bytes':2233,'sha256':'ca2da6c561cc14586ba60a797494f76983078a515a2a484b07b0766c8682a5a1'},'root review assignment')
h,names=seal(Q,31);ph,pnames=seal(P,27);vh,vnames=seal(V,10)
for k in ('assignment','predecessor_source','predecessor_independent_review','root_predecessor_adjudication'):pin(h[k],k)
old=load(P/'SOURCE_SET.json');s=load(Q/'SOURCE_SET.json');d=load(Q/'DEPENDENCIES.json')
need(set(s)=={'schema','status','adapter','modules','dependencies','bootstrap_binding','bootstrap_provenance'},'closed source declaration')
need(s['schema']==old['schema']=='ri156-complete-source-set-v1' and s['status']==old['status']=='UNEXECUTED_SOURCE_NOT_ADMISSION','source-only schema retained')
need(len(old['dependencies'])==525 and len(s['dependencies'])==567 and s['dependencies']==d['files'] and d['inherited_ri158']==525 and d['total']==567,'567 exact shared dependency declarations')
by={x['path']:x for x in s['dependencies']};oldby={x['path']:x for x in old['dependencies']}
need(len(by)==567 and list(by)==sorted(by) and len(oldby)==525,'unique ordered dependencies')
for row in s['dependencies']:pin(row,'dependency')
for path,row in oldby.items():need(path in by and same(row,by[path]),'whole inherited dependency: '+path)
expected={str(P/n) for n in pnames}|{str(V/n) for n in vnames}|{str(D/n) for n in ('RI158_ROOT_ADJUDICATION.json','MEASUREMENT_ROOT_REVIEW.md','MEASUREMENT_REPAIR_ASSIGNMENT.json','MEASUREMENT_METADATA_REPLAY.json')}|{str(R.parent/'ri157-root-adjudication-q_wj4pny'/'MEASUREMENT_PRELIMINARY_FINDING.md')}
need(set(by)-set(oldby)==expected and len(expected)==42,'exact complete42 added predecessor/review/root files')
need(same(s['bootstrap_binding'],old['bootstrap_binding']) and same(s['bootstrap_provenance'],old['bootstrap_provenance']) and s['bootstrap_provenance'] in s['dependencies'],'historical bootstrap selection/provenance retained without runtime observation')
need(set(s['modules'])==set(old['modules']) and len(s['modules'])==11,'same eleven non-main captured modules')
roles={'adapter':s['adapter'],**s['modules']}
for role,row in roles.items():
 need(row['path']==str(Q/(role+'.py')),'exact current source path: '+role);pin(row,'current executable '+role)
c=load(Q/'SOURCE_CORRESPONDENCE.json');correspondence=[];patch=[]
need([x['role'] for x in c['files']]==['adapter']+sorted(s['modules']),'all twelve ordered executable roles')
for entry in c['files']:
 role=entry['role'];left=P/(role+'.py');right=Q/(role+'.py')
 need(entry['original']['path']==str(left) and entry['successor']['path']==str(right),'correspondence literal paths: '+role)
 pin(entry['original'],'original '+role);pin(entry['successor'],'successor '+role)
 one=left.read_bytes();two=right.read_bytes();equal=one==two
 need(equal==entry['whole_byte_identity']==(role not in ('adapter','integration_controls')),'whole byte status: '+role)
 correspondence.append({'role':role,'unchanged':equal})
 if not equal:patch.extend(difflib.unified_diff(one.decode().splitlines(True),two.decode().splitlines(True),fromfile=str(left),tofile=str(right)))
need(sum(x['unchanged'] for x in correspondence)==10,'ten whole unchanged executable files')
need(''.join(patch)==(Q/'SOURCE_DIFF.patch').read_text(),'entire two-file patch independently reconstructed')
pin(c['patch'],'complete patch');pin(c['predecessor'],'correspondence predecessor')
def function(text,name):
 starts=list(re.finditer(r'^def ([A-Za-z_][A-Za-z_0-9]*)\(',text,re.M));matches=[i for i,x in enumerate(starts) if x.group(1)==name]
 need(len(matches)==1,'unique top-level source function '+name)
 i=matches[0];return text[starts[i].start():starts[i+1].start() if i+1<len(starts) else len(text)]
for role,key,expected_names in [('adapter','unchanged_adapter_functions',['need','canonical','identity','initial_read','authenticate','execute_action','run','main']),('integration_controls','unchanged_integration_function_bodies',['need','exact','integration_case','mode_case'])]:
 need(c[key]==expected_names,'exact unchanged function declaration: '+role)
 one=(P/(role+'.py')).read_text();two=(Q/(role+'.py')).read_text()
 for name in expected_names:need(function(one,name)==function(two,name),'complete unchanged function text: '+role+'.'+name)
one=function((P/'adapter.py').read_text(),'run_authenticated');two=function((Q/'adapter.py').read_text(),'run_authenticated')
need(one.split('    def namespace_tail():')[0]==two.split('    def namespace_tail():')[0],'run_authenticated entire preceding source unchanged')
need(one.split('    actions=[')[1]==two.split('    actions=[')[1],'run_authenticated entire following source unchanged')
def ids(path,labels):
 text=Path(path).read_text();out=[]
 for label in labels:
  found=re.findall('^'+re.escape(label)+r'=([^\n]+)$',text,re.M)
  need(len(found)==1,'literal control tuple: '+label)
  out.extend(re.findall(r"'([^']+)'",found[0]))
 return out
fiftyfive=ids(Q/'inert_controls.py',('MONITOR_IDS','MODE_IDS','STAGE_IDS','IO_IDS','TAIL_IDS','SHAPE_IDS','BINDING_IDS'))
twentynine=ids(Q/'integration_controls.py',('SOURCE_IDS','OUTPUT_IDS','FIXTURE_IDS','MODE_IDS'))
newids=ids(Q/'integration_controls.py',('FINAL_FIXTURE_IDS',))
oldinv=load(P/'CONTROL_INVENTORY.json');inv=load(Q/'CONTROL_INVENTORY.json')
need(len(fiftyfive)==55 and len(twentynine)==29 and len(newids)==22 and len(set(fiftyfive+twentynine+newids))==106,'55plus29plus22 unique literal IDs')
need(oldinv['combined_order']==fiftyfive+twentynine==inv['retained84_order'] and inv['new22_order']==newids and inv['combined_order']==fiftyfive+twentynine+newids and inv['counts']=={'retained':84,'new':22,'total':106,'executed':0},'complete ordered control inventory')
for name in newids:need('| '+name+' |' in (Q/'FINAL_FIXTURE_CONTROL_CONTRACT.md').read_text(),'new control contract row: '+name)
for name in twentynine:need('| '+name+' |' in (P/'INTEGRATION_CONTROL_CONTRACT.md').read_text(),'retained integration contract row: '+name)
source_text=(Q/'integration_controls.py').read_text()
need("FINAL_FIXTURE_IDS=(" in source_text and "for identifier in CONTROL_IDS:" in source_text,'literal declared control source and dispatch retained')
final=load(Q/'FINAL_SOURCE_PIN_CHECK.json');pin(final['source_set'],'final author source set')
need(final['unchanged_exact_source_files']==[roles[x] for x in ['adapter']+sorted(s['modules'])] and final['complete_dependency_count']==567 and final['source_execution'] is False,'final author complete source declarations')
author=load(Q/'ADMINISTRATIVE_CHECK.json')
need(author['complete_verified_dependencies']==s['dependencies'],'author exact dependency reconciliation')
need(author['control_counts']=={'retained':84,'new':22,'total':106,'executed':0} and author['whole_unchanged_executable_files']==10 and author['changed_executable_files']==2 and author['added_executable_files']==0,'author declared source/control counts')
need(author['unchanged_adapter_functions']==c['unchanged_adapter_functions'] and author['unchanged_integration_function_bodies']==c['unchanged_integration_function_bodies'],'author function count reconciliation')
for row in author['source_files']:
 pin(row['file'],'author current source row');need(row['lines']==len(Path(row['file']['path']).read_text().splitlines()),'actual source line count')
tools=load(Q/'ACTUAL_ADMINISTRATIVE_TOOLS.json')
need([(x['chunk_id'],x['exit_code']) for x in tools['successful_administrative_tools']]==[('cef2d2',0),('5023cf',0)],'author declared successful administrative tools retained')
need(len(tools['failed_commands'])==1 and tools['failed_commands'][0]['chunk_id']=='5269bc' and tools['failed_commands'][0]['exit_code']==1 and tools['failed_commands'][0]['stderr_file']=='ADMIN_READ_FAILURE.stderr','author failed lookup preserved')
need((Q/'ADMIN_READ_FAILURE.stderr').read_text()=='cat: /Volumes/AI_DATA/development/det-review-evidence/ri158-independent-repair-review-nxij3eju/INDEPENDENT_REVIEW.md: No such file or directory\n','exact failure diagnostic')
need([x['chunk_id'] for x in tools['recovery']]==['601576','9a93e3'] and tools['clipped_display']=={'chunk_id':'faed7e','exit_code':0,'recovered_by':['c270c3','826c74','3dfefd','193414'],'scope':'Long combined old adapter/integration source display'},'author declared recovery chain preserved')
need(tools['controls_executed']==0 and tools['runtime_observed'] is False and tools['source_acceptance'] is False,'author administrative-only scope')
pub=load(Q/'PUBLICATION_SUBSET.json');need(pub['include_names']==names and pub['external_only_preserved']==[],'subject complete publication subset')
for path,before in list(observed.items()):need(m.identity(path)==before,'fresh complete identity unchanged: '+path)
need(len(observed)==599,'599 identities:567 dependencies31 subject1 review assignment')
report=dict(schema='ri160-root-metadata-replay-v1',status='PASS_ADMINISTRATIVE_IDENTITY_AND_TEXT_NOT_SOURCE_ACCEPTANCE',predicates=len(predicates),dependencies=567,inherited=525,additions=42,
 selected_dependency_bytes=sum(x['bytes'] for x in s['dependencies']),subject_namespace=names,source_payloads=30,prior_namespaces=[27,10],unchanged_modules=10,changed_modules=2,new_modules=0,current_executable_modules=12,
 unchanged_adapter_functions=c['unchanged_adapter_functions'],unchanged_integration_functions=c['unchanged_integration_function_bodies'],full_patch_matches=True,nested_tail_only_adapter_change=True,controls={'retained':84,'new':22,'total':106,'executed':0},source_correspondence=correspondence,
 subject=m.ref(Q/'HANDOFF.json'),assignment=m.ref(A),trusted_helper=m.ref(HELPER),observed_identities=list(observed.values()),predicates_completed=predicates,final_fresh_identity_count=599,
 scope={'scientific_decode':False,'subject_import_compile_AST_probe_execution':False,'controls_executed':False,'runtime_observed':False,'source_acceptance':False,'repository_Git_write':False})
ref=m.save('METADATA_CHECK.json',report)
print(json.dumps({k:report[k] for k in ('status','predicates','dependencies','inherited','additions','selected_dependency_bytes','unchanged_modules','changed_modules','new_modules','controls','final_fresh_identity_count')},sort_keys=True))
print(json.dumps(ref,sort_keys=True))
