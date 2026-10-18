"""RI160 author administrative identity/text check. No target import or AST.
Writes source declarations and check results only; no control/fixture execution.
"""
from pathlib import Path
import hashlib,json,re,difflib
D=Path(__file__).resolve().parent;B=D.parent
P=B/'ri158-white-custody-repair-68cdvzn6';V=B/'ri158-independent-repair-review-nxij3eju';R=B/'ri158-root-fixture-review-tupyksou'
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def pin(p):
 assert p.is_absolute() and p.resolve()==p and p.is_file() and not p.is_symlink(),str(p)
 before=p.stat();h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for part in iter(lambda:f.read(1048576),b''):n+=len(part);h.update(part)
 state=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
 assert state(before)==state(p.stat()) and n==before.st_size
 return {'path':str(p),'bytes':n,'sha256':h.hexdigest()}
def read(p):return json.loads(p.read_bytes())
def write(name,v):
 with (D/name).open('xb') as f:f.write(canonical(v))
def verify(row):assert pin(Path(row['path']))==row,row['path']
for name,n,h in [('MEASUREMENT_REPAIR_ASSIGNMENT.json',3860,'1cb89c7279761a3b892d9d8c440d97db3e0b5f5aecb4b43792b2bac19eff64e8'),('RI158_ROOT_ADJUDICATION.json',2058,'d4b636f90564a7eba586de4bbb5f8bbb82f50a63d02c51c1b91f37471c57f7a9')]:
 verify({'path':str(R/name),'bytes':n,'sha256':h})
for root,n,h in [(P,12934,'69638eb05897dc2e72c4a29f84d27593dff5e83b98e102c1efccc67f9ded4fa2'),(V,5894,'02f3ef205a747dfdc096f849c1ff64a58984b10a4c3eb635e292b284a1314619')]:
 verify({'path':str(root/'HANDOFF.json'),'bytes':n,'sha256':h});handoff=read(root/'HANDOFF.json')
 assert sorted(p.name for p in root.iterdir())==sorted(handoff['namespace'])
 for row in handoff['payloads']:verify(row)
old=read(P/'SOURCE_SET.json');deps={}
for row in old['dependencies']:
 assert row['path'].startswith(str(B)+'/') or row['path'].startswith('/Volumes/AI_DATA/development/det_8_framework-ret/'),'no installed runtime observation'
 verify(row);deps[row['path']]=row
assert len(deps)==525
for root in (P,V):
 for p in root.iterdir():deps[str(p)]=pin(p)
for name in ('MEASUREMENT_REPAIR_ASSIGNMENT.json','RI158_ROOT_ADJUDICATION.json','MEASUREMENT_ROOT_REVIEW.md','MEASUREMENT_METADATA_REPLAY.json'):
 p=R/name;deps[str(p)]=pin(p)
p=B/'ri157-root-adjudication-q_wj4pny'/'MEASUREMENT_PRELIMINARY_FINDING.md';deps[str(p)]=pin(p)
files=[deps[k] for k in sorted(deps)];correspondence=[];delta=[]
roles=['adapter']+sorted(old['modules']);assert len(roles)==12
for role in roles:
 a=(P/(role+'.py')).read_bytes();b=(D/(role+'.py')).read_bytes();same=a==b
 assert same==(role not in ('adapter','integration_controls')),role
 correspondence.append({'role':role,'original':pin(P/(role+'.py')),'successor':pin(D/(role+'.py')),'whole_byte_identity':same})
 if not same:delta.extend(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile=str(P/(role+'.py')),tofile=str(D/(role+'.py'))))
with (D/'SOURCE_DIFF.patch').open('x') as f:f.write(''.join(delta))
def functions(path):
 text=path.read_text();marks=list(re.finditer(r'^def ([A-Za-z_][A-Za-z_0-9]*)\(',text,re.M));out={}
 for i,m in enumerate(marks):out[m.group(1)]=text[m.start():marks[i+1].start() if i+1<len(marks) else len(text)]
 return out
ap=functions(P/'adapter.py');an=functions(D/'adapter.py');unchanged_adapter=[]
assert set(ap)==set(an)
for k in ap:
 if k!='run_authenticated':assert ap[k]==an[k],k;unchanged_adapter.append(k)
a=ap['run_authenticated'];b=an['run_authenticated']
assert a.split('    def namespace_tail():',1)[0]==b.split('    def namespace_tail():',1)[0]
assert a.split('    actions=[',1)[1]==b.split('    actions=[',1)[1]
ip=functions(P/'integration_controls.py');inew=functions(D/'integration_controls.py');unchanged_controls=[]
for k in ('need','exact','integration_case','mode_case'):
 assert ip[k]==inew[k],k;unchanged_controls.append(k)
# The prior run_all_controls was the last function, so its old trailing spacing
# is excluded only in this explicitly changed wrapper's textual diff.
def literal_ids(path,label):
 found=re.findall('^'+re.escape(label)+r'=([^\n]+)$',path.read_text(),re.M);assert len(found)==1,label
 return re.findall(r"'([^']+)'",found[0])
old_ids=[]
for label in ('MONITOR_IDS','MODE_IDS','STAGE_IDS','IO_IDS','TAIL_IDS','SHAPE_IDS','BINDING_IDS'):old_ids+=literal_ids(D/'inert_controls.py',label)
retained_ids=[]
for label in ('SOURCE_IDS','OUTPUT_IDS','FIXTURE_IDS','MODE_IDS'):retained_ids+=literal_ids(D/'integration_controls.py',label)
late_ids=literal_ids(D/'integration_controls.py','FINAL_FIXTURE_IDS')
assert len(old_ids)==55 and len(retained_ids)==29 and len(late_ids)==22
assert old_ids+retained_ids==read(P/'CONTROL_INVENTORY.json')['combined_order']
combined=old_ids+retained_ids+late_ids;assert len(set(combined))==106
for name in late_ids:assert '| '+name+' |' in (D/'FINAL_FIXTURE_CONTROL_CONTRACT.md').read_text(),name
adapter=(D/'adapter.py').read_text();integration=(D/'integration_controls.py').read_text()
assert 'CONTROL_IDS=SOURCE_IDS+OUTPUT_IDS+FIXTURE_IDS+MODE_IDS+FINAL_FIXTURE_IDS' in integration
assert "'integration51':new" in integration
assert adapter.count('tree=I.tree(out)')==1
assert adapter.index("observations['namespace_fixture_mismatches']=fixture_mismatches")<adapter.index('if all_mismatches:raise')
assert 'all_mismatches=member_mismatches+mismatches+fixture_mismatches' in adapter
assert "I.same(actual,expected,'final namespace control fixture tree '+name)" in adapter
assert "return run_authenticated(path,a,manifest,mods,q,admission_ref,execute_action)" in adapter
assert [x for x in adapter.splitlines() if x.startswith('BOUNDS=')]==[x for x in (P/'adapter.py').read_text().splitlines() if x.startswith('BOUNDS=')]
write('DEPENDENCIES.json',{'schema':'ri160-opaque-source-dependencies-v1','status':'SOURCE_ONLY','inherited_ri158':525,'total':len(files),'files':files,'installed_runtime_observed':False,'scientific_body_decoded':False})
write('SOURCE_SET.json',{'schema':'ri156-complete-source-set-v1','status':'UNEXECUTED_SOURCE_NOT_ADMISSION','adapter':pin(D/'adapter.py'),'modules':{k:pin(D/(k+'.py')) for k in sorted(old['modules'])},'dependencies':files,'bootstrap_binding':old['bootstrap_binding'],'bootstrap_provenance':old['bootstrap_provenance']})
write('SOURCE_CORRESPONDENCE.json',{'schema':'ri160-source-correspondence-v1','predecessor':pin(P/'HANDOFF.json'),'files':correspondence,'unchanged_adapter_functions':unchanged_adapter,'changed_adapter_span':'only nested namespace_tail within run_authenticated; exact preceding/following spans unchanged','unchanged_integration_function_bodies':unchanged_controls,'added_function':'final_fixture_case','changed_integration_wrappers':['run_controls','run_all_controls'],'patch':pin(D/'SOURCE_DIFF.patch'),'source_execution':False})
write('CONTROL_INVENTORY.json',{'schema':'ri160-literal-control-inventory-v1','retained84_order':old_ids+retained_ids,'new22_order':late_ids,'combined_order':combined,'counts':{'retained':84,'new':22,'total':106,'executed':0},'method':'literal source regular expressions only, no evaluation, AST, import, compilation or fixture'})
write('ADMINISTRATIVE_CHECK.json',{'schema':'ri160-author-administrative-check-v1','status':'PASS_OPAQUE_IDENTITIES_AND_TEXT_ONLY','predecessor_namespace_count':27,'review_namespace_count':10,'inherited_dependency_count':525,'dependency_count':len(files),'complete_verified_dependencies':files,'whole_unchanged_executable_files':10,'changed_executable_files':2,'added_executable_files':0,'unchanged_adapter_functions':unchanged_adapter,'unchanged_integration_function_bodies':unchanged_controls,'control_counts':{'retained':84,'new':22,'total':106,'executed':0},'source_files':[{'file':pin(D/(name+'.py')),'lines':len((D/(name+'.py')).read_text().splitlines())} for name in roles],'source_acceptance':False,'subject_import_compile_AST_probe_execute':False,'fixtures_generated_or_evaluated':False,'scientific_decode':False,'runtime_observed':False})
print(json.dumps({'status':'PASS_OPAQUE_AND_TEXT_ONLY','dependencies':len(files),'unchanged_executable_files':10,'changed_executable_files':2,'controls':[84,22,106,0],'unchanged_adapter_functions':len(unchanged_adapter),'unchanged_integration_functions':len(unchanged_controls)},sort_keys=True))
