"""Independent finite metadata/text review only; no subject module is loaded.
Source/history inputs are opaque hash reads. JSON loads below name saved
administrative manifests/custody only. No new runtime or E inventory.
"""
from pathlib import Path
import hashlib,json,stat,re,difflib,os
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
W=B/'ri226-directory-custody-recovery-yvfg_p1b/worker_proposal'
OLD=B/'ri222-freeze-cwd-repair-ypiy2jqw/worker_proposal'
R=B/'ri226-independent-recovery-review-_vv8hup3'
labels=[]; identities={}
def require(value,label):
 labels.append(label)
 if not value: raise ValueError(label)
def canon(value): return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def equal(a,b,label): require(canon(a)==canon(b),label)
def pin(path):
 p=Path(path);a=p.lstat();require(stat.S_ISREG(a.st_mode) and not p.is_symlink(),'regular opaque input '+str(p))
 data=p.read_bytes();z=p.lstat();require((a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns),'stable opaque read '+str(p))
 row=dict(path=str(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest());identities[str(p)]=row;return row
def verify(row):
 v=pin(row['path']);equal(v,{k:row[k] for k in ('path','bytes','sha256')},'complete opaque pin '+row['path'])
def load(path):
 def pairs(items):
  value={}
  for k,v in items:require(k not in value,'no duplicate metadata key '+k);value[k]=v
  return value
 return json.loads(Path(path).read_bytes(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def span(src,name):
 match=re.search(r'^def '+re.escape(name)+r'\(',src,re.M);require(match is not None,'function starts '+name)
 end=re.search(r'^def |^if __name__',src[match.end():],re.M)
 return src[match.start():match.end()+end.start() if end else len(src)].rstrip()
verify(dict(path=str(W/'HANDOFF.json'),bytes=9657,sha256='bead93928f1f1af37379f4d8add4c5e254b31633fa8d00acb274a2739d237fdc'))
h=load(W/'HANDOFF.json');equal(sorted(p.name for p in W.iterdir()),sorted(h['namespace']),'exact sealed19 namespace');equal([len(h['files']),len(h['namespace'])],[18,19],'seal counts')
for row in h['files']:require(Path(row['path']).parent==W,'payload parent');verify(row)
base=load(W/'INPUT_PINS.json');repair=load(W/'REPAIR_PROVENANCE.json');manifest=load(W/'SOURCE_PINS.json');cor=load(W/'CORRESPONDENCE.json');admin=load(W/'ADMIN_CHECK.json')
require((W/'INPUT_PINS.json').read_bytes()==(OLD/'INPUT_PINS.json').read_bytes(),'base entire bytes unchanged')
prior=load(OLD/'REPAIR_PROVENANCE.json');equal(repair['groups']['inherited_repair'],prior['files'],'entire90 inherited repair rows')
expected_groups={'inherited_repair':90,'ri222_seal':16,'retained_root_operation':12,'retained_monitor':4,'retained_operation':4,'actual_failure_and_diagnostics':31}
equal({k:len(v) for k,v in repair['groups'].items()},expected_groups,'all six complete group counts')
union={}
for rows in repair['groups'].values():
 for row in rows:
  require(row['path'] not in union or union[row['path']]==row,'compatible grouped pin');union[row['path']]=row
equal([union[k] for k in sorted(union)],repair['files'],'157 complete grouped dependency rows')
inputs={}
for row in base['files']+repair['files']:
 require(row['path'] not in inputs or inputs[row['path']]==row,'compatible input pin');inputs[row['path']]=row
equal([len(base['files']),len(repair['files']),len(inputs),len(base['prior_role_rows']),base['prior_role_count']],[806,157,963,810,810],'input and prior role counts')
for row in inputs.values():verify(row)
for family in [base['roles'],repair['roles']]:
 for key,row in family.items():equal(inputs[row['path']],row,'role in complete input domain '+key)
for row in base['prior_role_rows']:
 # Historical role wrapper may include metadata; every embedded FilePin is reconciled.
 def refs(value):
  if isinstance(value,dict):
   if {'path','bytes','sha256'}<=set(value):
    pure={k:value[k] for k in ('path','bytes','sha256')};equal(inputs[pure['path']],pure,'all historical role pins retained')
   for v in value.values():refs(v)
  elif isinstance(value,list):
   for v in value:refs(v)
 refs(row)
require(set(manifest)=={'schema','status','files'},'manifest fields')
equal([manifest['schema'],manifest['status']],['ri226-proposal-source-pins-v1','SOURCE_ONLY_NOT_ADMISSION'],'source manifest status')
equal([Path(row['path']).name for row in manifest['files']],['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_reconciliation.py','reconcile_freeze.py'],'five ordered source payloads')
prospective=dict(inputs)
for row in manifest['files']:require(row['path'] not in prospective,'new manifest payload distinct');prospective[row['path']]=row;verify(row)
equal([len(prospective),len(prospective)+3],[968,971],'concrete closure and prospective manifest decision bootstrap slots')
refs=repair['roles'];before=load(refs['original_before']['path']);obs=load(refs['original_observations']['path']);c=load(refs['original_complete']['path']);post=load(refs['postflight']['path']);old_sources=load(refs['original_sources']['path'])
equal(len(old_sources),904,'all original904 source rows')
for row in old_sources:equal({k:row[k] for k in ('path','bytes','sha256')},inputs[row['path']],'original source full pin retained')
equal(before['source_observations'],old_sources,'whole original before sources');equal(obs['sources_actual'],old_sources,'whole original after sources');equal(obs['binding_actual'],before['bindings'],'whole original binding tail')
equal(c['status'],'REFUSED_RETAIN_ALL_PARTIALS','retained refused outcome');err=dict(type='ValueError',message='RI209: root device inode mode links',secondary=[]);equal(c['first_error'],err,'retained first error')
equal(obs['installation_write'],dict(error=None,cleanup_errors=[]),'original write close only successful')
old={row['relative']:row for row in before['E']};new={row['relative']:row for row in obs['E_after']}
require(len(old)==57 and len(new)==58 and set(new)==set(old)|{'AUTHORIZED_FREEZE.json'},'saved sole new member')
equal(old['.'],post['root_before'],'exact historical before root');equal({k:new['.'][k] for k in ('state','entries')},post['root_after'],'exact historical after root')
equal(old['.']['state'][:3],new['.']['state'][:3],'historical root dev inode mode');equal([old['.']['state'][3],new['.']['state'][3]],[23,24],'exact historical nlink transition');equal(new['.']['entries'],sorted(old['.']['entries']+['AUTHORIZED_FREEZE.json']),'historical exact root membership')
for key,row in old.items():
 if key!='.':equal(new[key],row,'entire saved unchanged old member '+key)
for row in new.values():
 if row['kind']=='file':require(stat.S_ISREG(row['identity']['state'][2]) and row['identity']['state'][3]==1 and row['identity']['symlink_chain']==[],'saved regular single-link member')
equal(new['AUTHORIZED_FREEZE.json']['identity'],post['installed_partial'],'whole saved installed partial');equal([sum(r['kind']=='file' for r in new.values()),sum(r['kind']=='directory' for r in new.values())],[49,9],'saved tree counts')
require(set(c['independent_tails'])=={'source_inputs','root_bindings','supplier','E_and_frozen','save_observations','ordinary_outputs','final_E','output_namespace'},'all old eight tails')
for k in ('E_and_frozen','final_E'):equal(c['independent_tails'][k],dict(value=None,error=err),'whole original failed tail '+k)
for k in ('source_inputs','root_bindings','supplier','save_observations','ordinary_outputs','output_namespace'):equal(c['independent_tails'][k]['error'],None,'original passed tail '+k)
equal(c['independent_tails']['source_inputs']['value'],old_sources,'original full source tail');equal(c['independent_tails']['root_bindings']['value'],before['bindings'],'original full binding value');equal(c['independent_tails']['supplier']['value'],obs['supplier_actual'],'original full supplier value')
primary=(W/'reconcile_freeze.py').read_text();checker=(W/'check_reconciliation.py').read_text();oldp=(OLD/'install_freeze.py').read_text();oldc=(OLD/'check_installation.py').read_text()
for key,newtext,oldtext in [('unchanged_primary_function_spans',primary,oldp),('unchanged_checker_function_spans',checker,oldc)]:
 for name in cor[key]:equal(span(newtext,name),span(oldtext,name),'entire unchanged function '+name)
for original,newtext,oldname,newname,patch in [(oldp,primary,'install_freeze.py','reconcile_freeze.py','RECONCILER_DIFF.patch'),(oldc,checker,'check_installation.py','check_reconciliation.py','CHECKER_DIFF.patch')]:
 delta=''.join(difflib.unified_diff(original.splitlines(True),newtext.splitlines(True),fromfile=str(OLD/oldname),tofile=str(W/newname)));require((W/patch).read_text()==delta,'complete literal delta '+patch)
for prefix in ('CAP=','LIMITS=','ENV=','VENDOR='):
 line=next(x for x in oldp.splitlines() if x.startswith(prefix));require(line in primary,'unchanged primary literal '+prefix)
for prefix in ('LIMITS=','ENV=','VENDOR='):
 line=next(x for x in oldc.splitlines() if x.startswith(prefix));require(line in checker,'unchanged checker literal '+prefix)
start='  # The first fallible post-mkdir operation is protected.';end="  same(m.ref(args.admission),a_ref,'admission after ownership')"
equal(primary[primary.index(start):primary.index(end)],oldp[oldp.index(start):oldp.index(end)],'complete protected initial clock block')
start='  # All eight ordinary tails above were attempted before final timing.';end='  completion=dict('
equal(primary[primary.index(start):primary.index(end)],oldp[oldp.index(start):oldp.index(end)].replace('installation soft wall exceeded','reconciliation soft wall exceeded'),'complete protected final clock block')
require(primary.count('os.open(')==1 and "need(Path(path).parent==OUT,'only fresh external output writes')" in primary,'sole generic confined write primitive')
for text in ("os.open(E,",'dir_fd=',"os.open('AUTHORIZED_FREEZE.json'",'.unlink(','.replace(','.chmod(','subprocess.','Popen('):require(text not in primary,'no mutation or new child primitive '+text)
require("Path.cwd()==literal(D/'monitor')" in primary and "eq(dispatch['cwd'],str(D),'outer cwd')" in checker,'separate exact child and outer cwd')
monitor=next(r for r in inputs.values() if r['path']==str(B/'ri141-white-bootstrap-source-h58ls076/prepare.py'))
equal({k:monitor[k] for k in ('bytes','sha256')},dict(bytes=45721,sha256='8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe'),'unchanged whole monitor pin');require('cwd=out, env=env, start_new_session=True)' in Path(monitor['path']).read_text(),'actual monitor child cwd')
equal([admin['checks'],len(admin['predicate_labels']),admin['opaque_files'],len(admin['opaque_identities'])],[4064,4064,968,968],'serialized author check counts')
for row in admin['opaque_identities']:equal(row,identities[row['path']],'every author observed pin independently matched')
result=dict(schema='ri226-independent-source-metadata-check-v1',status='PASS_SOURCE_TEXT_AND_SAVED_ADMINISTRATIVE_METADATA_ONLY',checks=len(labels),opaque_identities=[identities[k] for k in sorted(identities)],predicate_labels=labels,source_inputs=963,prospective_source_count=971,preserved_original_source_paths=904,prior_roles=810,subject_import_compile_AST_probe_execution=False,scientific_body_decode=False,current_runtime_or_E_inventory=False,fixture_or_clock_evaluation=False,qualification_credit=0)
out=R/'CHECK_RESULT.json';data=canon(result)
with out.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
print(json.dumps(dict(report=dict(path=str(out),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()),checks=len(labels),opaque_files=len(identities),status=result['status'])))
