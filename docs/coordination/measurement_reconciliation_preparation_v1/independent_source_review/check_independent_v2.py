"""Read-only finite source/metadata checks; only this review's output is written.
No subject/helper import, AST, compile, execution, current E or vendor inventory.
"""
from pathlib import Path
import hashlib,json,stat,os,re
B=Path('/Volumes/AI_DATA/development/det-review-evidence');W=B/'ri229-reconciliation-preparation-t93t1607/worker_proposal';S=B/'ri226-directory-custody-recovery-yvfg_p1b/worker_proposal';R=B/'ri229-independent-preparation-review-ajsf_qna'
checks=[];observed={}
def need(ok,label):
 checks.append(label)
 if not ok:raise ValueError(label)
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def eq(a,b,label):need(canonical(a)==canonical(b),label)
def pin(path):
 p=Path(path);a=p.lstat();need(stat.S_ISREG(a.st_mode) and not p.is_symlink(),'ordinary opaque file '+str(p));raw=p.read_bytes();z=p.lstat();need((a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns),'opaque stable '+str(p));v=dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());observed[str(p)]=v;return v
def verify(v):eq(pin(v['path']),{k:v[k] for k in ('path','bytes','sha256')},'whole opaque pin '+v['path'])
def load(p):return json.loads(Path(p).read_bytes())
verify(dict(path=str(W/'HANDOFF.json'),bytes=9292,sha256='7efdb57c59ce7a5f2834bbdb335ff4b2c0afe4e3849e15970fc3aa2c20c321e0'))
h=load(W/'HANDOFF.json');eq(sorted(p.name for p in W.iterdir()),sorted(h['namespace']),'whole18 namespace');eq([len(h['namespace']),len(h['files'])],[18,17],'whole17 payloads')
for v in h['files']:need(Path(v['path']).parent==W,'payload parent');verify(v)
deps=load(W/'DEPENDENCIES.json');declared={v['path']:v for v in deps['files']};eq(len(declared),992,'unique992 dependencies')
base=load(S/'INPUT_PINS.json');repair=load(S/'REPAIR_PROVENANCE.json');oldhand=load(S/'HANDOFF.json');accepted=load(deps['roles']['recovery_decision']['path']);ih=load(deps['roles']['independent_recovery_review']['path'])
expected={}
def add(v):
 need(v['path'] not in expected or expected[v['path']]==v,'compatible closure reference');expected[v['path']]=v
for v in base['files']+repair['files']+oldhand['files']+[deps['roles']['recovery_handoff'],deps['roles']['recovery_decision'],deps['roles']['assignment']]+ih['payloads']+[deps['roles']['independent_recovery_review'],accepted['root_manual_review'],accepted['root_metadata_check']]:add(v)
eq(declared,expected,'complete independently derived992 dependency closure')
for v in declared.values():verify(v)
for k,v in deps['roles'].items():eq(v,declared[v['path']],'every selecting role in declared closure '+k)
old_sources=load(repair['roles']['original_sources']['path']);eq(len(old_sources),904,'904 original rows')
for v in old_sources:eq({k:v[k] for k in ('path','bytes','sha256')},declared[v['path']],'entire original byte pin in new closure')
source_manifest=load(S/'SOURCE_PINS.json');domain={v['path'] for v in base['files']+repair['files']+source_manifest['files']}|{str(S/'SOURCE_PINS.json'),str(S.parent/'ROOT_SOURCE_REVIEW.json'),str(S.parent/'RECONCILE_BOOTSTRAP.py')};eq(len(domain),971,'complete prospective971 by literal paths only');eq([len(base['files']),len(repair['files']),len(base['prior_role_rows']),base['prior_role_count']],[806,157,810,810],'base repair and complete role counts')
need(str(S.parent/'RECONCILE_BOOTSTRAP.py') not in declared,'no future bootstrap pin presented as actual dependency')
writer=(W/'prepare_reconciliation.py').read_text();bootstrap=(W/'RECONCILE_BOOTSTRAP.source-only.py').read_text();eq([len(writer.splitlines()),len(bootstrap.splitlines())],[222,18],'complete operational text line counts')
for name,v in [('MANIFEST',deps['roles']['recovery_manifest']),('HANDOFF',deps['roles']['recovery_handoff']),('REVIEW',deps['roles']['recovery_decision'])]:
 for value in (str(v['bytes']),v['path'],v['sha256']):need(value in next(l for l in writer.splitlines() if l.startswith(name+'=')),'literal correct '+name+' field')
need('root_namespace_before=sorted(p.name for p in D.iterdir())' in writer,'initial root membership retained')
need("need(name in output_names and type(data) is bytes and len(data)<=67108864" in writer,'write whitelist and cap')
need("with p.open('xb') as f:" in writer and "need(p.read_bytes()==data" in writer,'exclusive direct byte writes')
need(writer.count('.mkdir(')==2,'two exact preparation directory creations')
need(writer.count('.replace(')==1 and 'original_bootstrap=original_bootstrap.replace(old,new)' in writer,'only bootstrap string replacement, no filesystem replace')
for word in ('.unlink(','.rmdir(','.rename(','os.replace(','.chmod(','.write_bytes(','.write_text(','subprocess.','os.system(','exec(compile('):need(word not in writer,'no mutable or dispatch primitive '+word)
need("produced_before_custody=dict(produced)" in writer,'custody takes preemit copy of eight earlier refs')
need("future_admission_path=str(D/'ADMIT_RECONCILE.json')" in writer,'future path only')
need("proposed_dispatch=dict(outer_argv=" in writer,'unissued dispatch values exist');dispatch_line=next(l for l in writer.splitlines() if l.startswith('proposed_dispatch='));need('admission=' not in dispatch_line,'no fabricated admission pin')
for text in ('HOST_INPUT','PREP_REVIEW','PREP_MANIFEST'):need(text in writer,'external actual input required '+text)
need("eq(json.loads(host_transcript['result']['output']),observation" in writer,'raw genuine stdout whole-object equality')
need("eq(m.identity(HOST_INPUT['path']),host_original_state" in writer,'original host selection retained')
need("eq(tree(),etree,'final entire E unchanged after all preparation outputs')" in writer,'whole final E after output writes')
need("original_sources+list(original_before['bindings'].values())" in writer,'all original source and binding checks')
need("need(not os.path.lexists(O) and not os.path.lexists(D/'ADMIT_RECONCILE.json') and not os.path.lexists(D/'DISPATCH.json')" in writer,'final no operation admission dispatch')
need('exec(compile(captured' in bootstrap and 'module.child_run(' in bootstrap,'captured-only monitor load and selected entry')
need(bootstrap.index('hashlib.sha256(captured)')<bootstrap.index('exec(compile(captured')<bootstrap.index('module.child_run('),'hash-before-load-before-one-call')
need(bootstrap.count('module.child_run(')==1 and 'module.run(' not in bootstrap,'one bounded monitor call only')
need("'RECONCILE', 180, expected_environment)" in bootstrap and "'-I', '-B'" in bootstrap,'exact label limit flags')
protocol=(W/'PROTOCOL.md').read_text();need('not** the reconciler' in protocol,'preparation failure model explicitly separate');need('No future admission FilePin' in (W/'READINESS.md').read_text(),'readiness no future pin claim')
original_checker=(W/'check_metadata.py').read_text();replayed=(R/'replay_metadata.py').read_text();pattern="(W/'METADATA_CHECK.json')";replacement="(Path('/Volumes/AI_DATA/development/det-review-evidence/ri229-independent-preparation-review-ajsf_qna')/'AUTHOR_CHECK_REPLAY.json')"
need(original_checker.count(pattern)==3 and replayed==original_checker.replace(pattern,replacement),'replay exactly three output paths only')
need((R/'AUTHOR_CHECK_REPLAY.json').read_bytes()==(W/'METADATA_CHECK.json').read_bytes(),'full replay report byte-identical to author result')
report=load(R/'AUTHOR_CHECK_REPLAY.json');eq([report['predicates'],len(report['labels']),report['opaque_files'],len(report['opaque_pins'])],[3999,3999,997,997],'entire replay declared counts')
for v in report['opaque_pins']:eq(v,observed[v['path']],'every replay whole pin independently matched')
replay_pin=pin(R/'AUTHOR_CHECK_REPLAY.json')
result=dict(schema='ri229-independent-metadata-reconciliation-v1',status='PASS_SOURCE_AND_ADMINISTRATIVE_METADATA_ONLY',predicates=len(checks),labels=checks,opaque_files=len(observed),opaque_pins=[observed[k] for k in sorted(observed)],dependency_count=992,prospective_recovery_domain=971,old_source_paths=904,historical_roles=810,reviewed_author_checker_replay=replay_pin,subject_or_bootstrap_execution=False,fresh_E_supplier_inventory=False,scientific_decode=False,qualification_credit=0)
raw=canonical(result)
with (R/'INDEPENDENT_CHECK.json').open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
print(json.dumps(dict(report=dict(path=str(R/'INDEPENDENT_CHECK.json'),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),predicates=len(checks),opaque_files=len(observed),status=result['status'])))
