"""RI158 independent administrative/text check; never executes subject code."""
import difflib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re

R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri158-independent-repair-review-nxij3eju')
Q=R.parent/'ri158-white-custody-repair-68cdvzn6'
P=R.parent/'ri156-white-external-adapter-source-1plzn4nm'
V=R.parent/'ri156-independent-adapter-review-dko2kzl_'
D=R.parent/'ri157-root-review-jco7p6tf'
A=R.parent/'ri157-root-adjudication-q_wj4pny'/'MEASUREMENT_REVIEW_ASSIGNMENT.json'
HELPER=R.parent/'ri122-root-execution-review-6whn_vky'/'metadata.py'
b=HELPER.read_bytes()
if len(b)!=3144 or hashlib.sha256(b).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted administrative helper differs')
spec=importlib.util.spec_from_file_location('ri158_trusted_metadata',HELPER)
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
 # Called only for explicitly selected current/admin predecessor files.
 before=observe(p);raw=Path(p).read_bytes();need(m.pin(raw)==m.pure(before),'administrative body linked: '+str(p))
 def pairs(items):
  out={}
  for k,v in items:
   if k in out:raise ValueError('duplicate metadata key: '+str(p))
   out[k]=v
  return out
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError('nonfinite metadata')))
def seal(directory,key,expected_count):
 h=load(directory/'HANDOFF.json');names=sorted(x.name for x in directory.iterdir())
 need(names==sorted(h[key]) and len(names)==expected_count,'whole exact namespace: '+str(directory))
 need(sorted(Path(x['path']).name for x in h['payloads'])==[n for n in names if n!='HANDOFF.json'],'complete payload coverage: '+str(directory))
 for x in h['payloads']:
  need(Path(x['path']).parent==directory,'payload own directory: '+x['path']);pin(x,'sealed payload')
 return h,names
pin({'path':str(Q/'HANDOFF.json'),'bytes':12934,'sha256':'69638eb05897dc2e72c4a29f84d27593dff5e83b98e102c1efccc67f9ded4fa2'},'current handoff')
pin({'path':str(A),'bytes':2109,'sha256':'2f7a97b527a88d7a2dd16e69c7b01dde2e3a3e2f81c57fea4424e80765491206'},'root review assignment')
h,names=seal(Q,'namespace',27);ph,pnames=seal(P,'exact_namespace',26);vh,vnames=seal(V,'namespace',14)
for k in ('assignment','predecessor_source','predecessor_independent_review','root_predecessor_disposition'):pin(h[k],k)
a=load(A);need(a['controls_defined']==84 and a['controls_executed']==0,'review assignment control scope')
old=load(P/'SOURCE_SET.json');s=load(Q/'SOURCE_SET.json');d=load(Q/'DEPENDENCIES.json')
need(set(s)=={'schema','status','adapter','modules','dependencies','bootstrap_binding','bootstrap_provenance'},'closed source declaration')
need(s['schema']==old['schema']=='ri156-complete-source-set-v1' and s['status']==old['status']=='UNEXECUTED_SOURCE_NOT_ADMISSION','source-only schema retained')
need(len(old['dependencies'])==481 and len(s['dependencies'])==525 and s['dependencies']==d['files'] and d['inherited_ri156']==481 and d['total']==525,'525 exact shared dependency declarations')
by={x['path']:x for x in s['dependencies']};oldby={x['path']:x for x in old['dependencies']}
need(len(by)==525 and list(by)==sorted(by) and len(oldby)==481,'unique ordered dependencies')
for row in s['dependencies']:pin(row,'dependency')
for path,row in oldby.items():need(path in by and same(row,by[path]),'whole inherited dependency: '+path)
expected={str(P/n) for n in pnames}|{str(V/n) for n in vnames}|{str(D/n) for n in ('RI156_ROOT_ADJUDICATION.json','MEASUREMENT_ROOT_REVIEW.md','MEASUREMENT_REPAIR_ASSIGNMENT.json','MEASUREMENT_METADATA_REPLAY.json')}
need(set(by)-set(oldby)==expected and len(expected)==44,'exact complete 44 added predecessor/review/root files')
need(same(s['bootstrap_binding'],old['bootstrap_binding']) and same(s['bootstrap_provenance'],old['bootstrap_provenance']) and s['bootstrap_provenance'] in s['dependencies'],'historical bootstrap selection/provenance retained without runtime observation')
need(set(s['modules'])==set(old['modules'])|{'integration_controls'} and len(s['modules'])==11,'eleven non-main captured modules')
for role,row in {'adapter':s['adapter'],**s['modules']}.items():
 need(row['path']==str(Q/(role+'.py')),'exact current source path: '+role);pin(row,'current executable '+role)
c=load(Q/'SOURCE_CORRESPONDENCE.json');correspondence=[];patch=[]
need(len(c['files'])==11,'all eleven predecessor source roles')
for entry in c['files']:
 role=entry['role'];left=P/(role+'.py');right=Q/(role+'.py')
 need(entry['original']['path']==str(left) and entry['successor']['path']==str(right),'correspondence literal paths: '+role)
 pin(entry['original'],'original '+role);pin(entry['successor'],'successor '+role)
 one=left.read_bytes();two=right.read_bytes();equal=one==two
 need(equal==entry['whole_byte_identity']==(role not in ('adapter','mode_verify')),'whole byte status: '+role)
 correspondence.append({'role':role,'unchanged':equal})
 if not equal:patch.extend(difflib.unified_diff(one.decode().splitlines(True),two.decode().splitlines(True),fromfile=str(left),tofile=str(right)))
need(sum(x['unchanged'] for x in correspondence)==9,'nine unchanged modules')
need(''.join(patch)==(Q/'SOURCE_DIFF.patch').read_text(),'entire two-file patch independently reconstructed')
pin(c['new_module'],'added integration module');pin(c['patch'],'complete patch')
oldmode=(P/'mode_verify.py').read_text();newmode=(Q/'mode_verify.py').read_text();unchanged=[]
for marker in c['unchanged_mode_functions']:
 need(oldmode.count(marker)==1 and newmode.count(marker)==1,'unique function text marker: '+marker)
 def span(text):
  start=text.index(marker);end=text.find('\ndef ',start+1)
  return text[start:] if end<0 else text[start:end]
 need(span(oldmode)==span(newmode),'entire unchanged function text: '+marker);unchanged.append(marker)
need(len(unchanged)==8,'eight unchanged saved-mode functions')
def ids(path,labels):
 text=Path(path).read_text();out=[]
 for label in labels:
  found=re.findall('^'+re.escape(label)+r'=([^\n]+)$',text,re.M)
  need(len(found)==1,'literal control tuple: '+label)
  out.extend(re.findall(r"'([^']+)'",found[0]))
 return out
oldids=ids(Q/'inert_controls.py',('MONITOR_IDS','MODE_IDS','STAGE_IDS','IO_IDS','TAIL_IDS','SHAPE_IDS','BINDING_IDS'))
newids=ids(Q/'integration_controls.py',('SOURCE_IDS','OUTPUT_IDS','FIXTURE_IDS','MODE_IDS'))
inv=load(Q/'CONTROL_INVENTORY.json')
need(len(oldids)==55 and len(newids)==29 and len(set(oldids+newids))==84,'55 plus29 unique literal IDs')
need(inv['old_order']==oldids and inv['new_order']==newids and inv['combined_order']==oldids+newids and inv['counts']=={'old':55,'new':29,'total':84,'executed':0},'complete ordered control inventory')
for name in newids:need('| '+name+' |' in (Q/'INTEGRATION_CONTROL_CONTRACT.md').read_text(),'new control contract row: '+name)
for name in oldids:need('| '+name+' |' in (P/'CONTROL_CONTRACT.md').read_text(),'retained control contract row: '+name)
final=load(Q/'FINAL_SOURCE_PIN_CHECK.json');need(final['adapter']==s['adapter'] and final['modules']==s['modules'] and final['controls_executed']==0,'final author source identity declarations')
author=load(Q/'ADMINISTRATIVE_CHECK.json');need(author['complete_verified_dependencies']==s['dependencies'] and author['source_correspondence']==c['files'],'author report exact dependency/source reconciliation')
need(author['controls']=={'retained':55,'new':29,'total':84,'executed':0} and author['whole_unchanged_executable_files']==9 and author['changed_executable_files']==2 and author['added_executable_files']==1,'author declared source/control counts')
for row in author['current_source_files']:
 pin(row['file'],'author current source row');need(row['lines']==len(Path(row['file']['path']).read_text().splitlines()),'actual complete source line count')
tools=load(Q/'ACTUAL_ADMINISTRATIVE_TOOLS.json');need(tools['failed_commands']==[] and tools['metadata_check']['chunk_id']=='4ef446' and tools['metadata_check']['exit_code']==0,'author actual declaration retained, not independent runtime credit')
# Fresh before/after whole-file observations, independent of historical state claims.
for path,before in list(observed.items()):need(m.identity(path)==before,'fresh complete identity unchanged: '+path)
need(len(observed)==553,'553 full identities:525 dependencies27 subject1 review assignment')
report=dict(schema='ri158-independent-metadata-review-v1',status='PASS_ADMINISTRATIVE_IDENTITY_AND_TEXT_NOT_SOURCE_ACCEPTANCE',predicates=len(predicates),dependencies=525,inherited=481,additions=44,
 selected_dependency_bytes=sum(x['bytes'] for x in s['dependencies']),subject_namespace=names,source_payloads=26,prior_namespaces=[26,14],unchanged_modules=9,changed_modules=2,new_modules=1,current_executable_modules=12,
 unchanged_mode_functions=unchanged,full_patch_matches=True,controls={'old':55,'new':29,'total':84,'executed':0},source_correspondence=correspondence,
 subject=m.ref(Q/'HANDOFF.json'),assignment=m.ref(A),trusted_helper=m.ref(HELPER),observed_identities=list(observed.values()),predicates_completed=predicates,final_fresh_identity_count=553,
 scope={'scientific_decode':False,'subject_import_compile_AST_probe_execution':False,'controls_executed':False,'runtime_observed':False,'source_acceptance':False,'repository_Git_write':False})
ref=m.save('METADATA_CHECK.json',report)
print(json.dumps({k:report[k] for k in ('status','predicates','dependencies','inherited','additions','selected_dependency_bytes','unchanged_modules','changed_modules','new_modules','controls','final_fresh_identity_count')},sort_keys=True))
print(json.dumps(ref,sort_keys=True))
