"""RI222 nonauthor administrative review only. No reviewed-source loading/execution.
Reads fixed metadata, source text, opaque file bytes, and E namespace. Writes only
an exclusive result in the reviewer reservation (or a fresh --output directory).
"""
from pathlib import Path
import argparse, difflib, hashlib, json, os, stat
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri222-freeze-cwd-repair-ypiy2jqw'; W=D/'worker_proposal'
OLD=B/'ri218-freeze-byte-repair-x62withm/worker_proposal'
F=B/'ri221-root-installation-ru2v15ie'; E=B/'ri154-white-execution-proposed-42_uvw15'
R=B/'ri222-independent-cwd-review-15d9v2ym'
checks=0; observed={}; claims=[]
def require(ok,label):
 global checks
 checks+=1
 if not ok: raise ValueError(label)
def canonical(v): return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def equal(a,b,label): require(canonical(a)==canonical(b),label)
def state(a): return [a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns]
def ref(v): return {k:v[k] for k in ('path','bytes','sha256')}
def identity(p):
 p=Path(p); a=p.lstat()
 require(p.is_absolute() and p.resolve()==p and stat.S_ISREG(a.st_mode),'literal regular '+str(p))
 h=hashlib.sha256(); n=0
 with p.open('rb') as stream:
  equal(state(os.fstat(stream.fileno())),state(a),'opened selection')
  for block in iter(lambda:stream.read(1048576),b''): h.update(block); n+=len(block)
  equal(state(os.fstat(stream.fileno())),state(a),'closed read selection')
 equal(state(p.lstat()),state(a),'postread selection'); require(n==a.st_size,'full length')
 row=dict(path=str(p),resolved_path=str(p),symlink_chain=[],bytes=n,sha256=h.hexdigest(),state=state(a))
 if str(p) in observed: equal(row,observed[str(p)],'repeat unchanged selection')
 observed[str(p)]=row
 return row
def verify(v):
 row=identity(v['path']); equal(ref(row),ref(v),'declared exact FilePin'); return row
def load(p):
 def pairs(rows):
  out={}
  for k,v in rows: require(k not in out,'duplicate administrative key');out[k]=v
  return out
 def bad(x): raise ValueError('nonfinite administrative JSON')
 return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=bad)
def pinned(p,n,sha):
 v=identity(p); equal([v['bytes'],v['sha256']],[n,sha],'trusted root pin');return v
def seal(w,expected_count):
 h=load(w/'HANDOFF.json'); names=sorted(x.name for x in w.iterdir())
 equal(names,sorted(h['namespace']),'complete sealed namespace')
 require(len(names)==expected_count and len(h['files'])==expected_count-1,'exact seal count')
 equal(sorted(Path(x['path']).name for x in h['files']),sorted(n for n in names if n!='HANDOFF.json'),'whole payload domain')
 for v in h['files']: require(Path(v['path']).parent==w,'bound payload parent'); verify(v)
 return h
pinned(W/'HANDOFF.json',9023,'5762caec4ca89f2687de17da71671ec82e1066e81854b9d45364ea3ed59c1330')
pinned(W/'SOURCE_PINS.json',1363,'65696e7ab9e4b78c52c8c815dd79917fd7ed6b822074501b9f6393859cb4f535')
handoff=seal(W,16); oldhand=seal(OLD,15)
pinned(F/'RI222_REPAIR_ASSIGNMENT.json',2264,'bae3531b2bc3e50f3685beca009610bf7356d36ba7e7ad0cfc3a10f2b5a162b8')
a=load(F/'RI222_REPAIR_ASSIGNMENT.json')
equal([a['reservation'],a['worker'],a['output']],[str(D),str(W),str(B/'ri222-freeze-install-operation-ypiy2jqw')],'exact assigned paths')
for k in ('predecessor','supersession','review','genuine_failure','custody'): verify(a[k])
man=load(W/'SOURCE_PINS.json'); equal(sorted(man),['files','schema','status'],'closed source manifest')
equal([man['schema'],man['status']],['ri209-proposal-source-pins-v1','SOURCE_ONLY_NOT_ADMISSION'],'source-only manifest')
equal([Path(x['path']).name for x in man['files']],['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_installation.py','install_freeze.py'],'five ordered complete source bindings')
for x in man['files']: require(Path(x['path']).parent==W,'manifest parent');verify(x)
inputs=load(W/'INPUT_PINS.json'); rep=load(W/'REPAIR_PROVENANCE.json'); oldrep=load(OLD/'REPAIR_PROVENANCE.json')
require((W/'INPUT_PINS.json').read_bytes()==(OLD/'INPUT_PINS.json').read_bytes(),'entire input bytes retained')
equal([len(inputs['files']),len(inputs['prior_role_rows']),inputs['prior_role_count']],[806,810,810],'base identities/full roles')
oldreview=load(OLD.parent/'ROOT_SOURCE_REVIEW.json'); prep=load(OLD.parent/'PREPARATION_CUSTODY.json'); supersession=load(a['supersession']['path'])
root_names=['CALLER_FAILURE_REVIEW.json','FRESH_PREDISPATCH_CHECK.json','GENUINE_INSTALLATION_TOOL.json','GENUINE_POST_HOST_TOOL.json','POST_FAILURE_CUSTODY.json','REPO_ENTRY.json','RI218_OPERATIONAL_SUPERSESSION.json','RI222_REPAIR_ASSIGNMENT.json','ROOT_INSTALLATION_ADMISSION_DECISION.json','postfailure_failed.py','postfailure_v2.py']
failed_names=['ADMIT_INSTALL.json','DISPATCH.json','E_BEFORE.json','HOST_BEFORE.json','HOST_GENUINE_TOOL.json','INSTALLATION_PROPOSAL.json','INSTALL_BOOTSTRAP.py','INSTALL_PREFLIGHT.json','PREPARATION_CUSTODY.json','ROOT_SOURCE_REVIEW.json','SOURCES_BEFORE.json','SUPPLIER_BEFORE.json']
monitor_names=['INSTALL.ATTEMPT.json','INSTALL.COMPLETION.json','INSTALL.stderr','INSTALL.stdout']
groups=dict(inherited43=oldrep['files'],predecessor15=oldhand['files']+[a['predecessor']],failed_root12=[ref(identity(OLD.parent/n)) for n in failed_names],failed_monitor4=[ref(identity(OLD.parent/'monitor'/n)) for n in monitor_names],root_adjudication11=[ref(identity(F/n)) for n in root_names],support5=[oldreview['independent_review'],oldreview['root_metadata'],supersession['concrete_review'],prep['preparation_source'],prep['original_genuine_host']])
equal(rep['groups'],groups,'every provenance member independently reconstructed')
union={}
for rows in groups.values():
 for row in rows:
  if row['path'] in union:equal(union[row['path']],row,'consistent group overlap')
  union[row['path']]=row
require(len(union)==90,'90 exact repair identities'); equal(rep['files'],[union[k] for k in sorted(union)],'complete grouped repair domain')
full={}
for row in inputs['files']+rep['files']:
 if row['path'] in full:equal(full[row['path']],ref(row),'consistent union')
 full[row['path']]=ref(row)
require(len(full)==896,'896 actual input identities')
for row in full.values():verify(row)
prior=load(OLD.parent/'SOURCES_BEFORE.json');require(len(prior)==857,'original857')
for row in prior:equal(full[row['path']],ref(row),'each original operational source retained')
for row in inputs['roles'].values(): equal(full[row['path']],ref(row),'all direct old roles retained')
future=set(full)|{x['path'] for x in man['files']}|{str(W/'SOURCE_PINS.json'),str(D/'ROOT_SOURCE_REVIEW.json'),str(D/'INSTALL_BOOTSTRAP.py')}
require(len(future)==904,'904 prospective source domain, not observation')
new=(W/'install_freeze.py').read_text();old=(OLD/'install_freeze.py').read_text();checker=(W/'check_installation.py').read_text()
oldguard="Path.cwd()==D and literal(OUT)==OUT and literal(W)==W";newguard="Path.cwd()==literal(D/'monitor') and literal(OUT)==OUT and literal(W)==W"
projection=[]
for name in ('install_freeze.py','check_installation.py'):
 left=(OLD/name).read_text();right=(W/name).read_text();target=right
 ol=[s for s in left.splitlines() if s.startswith('REPAIR=')];nl=[s for s in right.splitlines() if s.startswith('REPAIR=')]
 require(len(ol)==len(nl)==1,'one repair declaration');equal(nl[0],'REPAIR='+repr(ref(identity(W/'REPAIR_PROVENANCE.json'))),'whole literal repair ref')
 if name=='install_freeze.py': require(right.count(newguard)==1 and oldguard not in right,'one actual guard correction');target=target.replace(newguard,oldguard)
 target=target.replace(nl[0],ol[0]).replace(D.name,OLD.parent.name).replace('ri222-freeze-install-operation-ypiy2jqw','ri218-freeze-install-operation-x62withm')
 require(target==left,'whole executable inverse projection '+name)
 projection.append(dict(name=name,lines=len(right.splitlines()),old=ref(identity(OLD/name)),new=ref(identity(W/name)),complete_projection=True))
diff=''.join(''.join(difflib.unified_diff((OLD/n).read_text().splitlines(keepends=True),(W/n).read_text().splitlines(keepends=True),fromfile=str(OLD/n),tofile=str(W/n))) for n in ('install_freeze.py','check_installation.py','PROTOCOL.md'))
require((W/'SOURCE_DIFF.patch').read_text()==diff,'whole source/protocol diff exact')
spans=[]
for start,end in [(' # RI213: all safe receipt/error state',' OUT.mkdir(mode=0o700)'),(' try:\n  # The first fallible post-mkdir',' return 0 if first is None else 1'),('  def sources_tail():','  # All eight ordinary tails above')]:
 x=old[old.index(start):old.index(end)];y=new[new.index(start):new.index(end)];require(x==y,'exact complete ownership/clock/tail block')
 spans.append(dict(start=start,end=end,bytes=len(y.encode()),sha256=hashlib.sha256(y.encode()).hexdigest()))
for text in ("need(Path(path).read_bytes()==data,'written exact bytes')","need(DEST.read_bytes()==candidate,'exact accepted byte copy')","def same(a,b,msg):need(m.canonical(a)==m.canonical(b),msg)","schema='ri213-installation-completion-v1'"):
 require(old.count(text)==new.count(text)==1,'retained exact bytes/JSON/schema semantics')
require(new.index(newguard)<new.index(' OUT.mkdir(mode=0o700)'),'cwd refusal preownership')
require('chdir(' not in new and new.count('Path.cwd()')==1,'no path relaxation or chdir')
mon=B/'ri141-white-bootstrap-source-h58ls076/prepare.py';pinned(mon,45721,'8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe')
boot=OLD.parent/'INSTALL_BOOTSTRAP.py';pinned(boot,2417,'76779aeb180fc09ef2c90a2c1341ff3f5285640645ac15e1d90b27014422a00a')
ms=mon.read_text();child=ms[ms.index('def child_run(command, out, label, seconds, env):'):ms.index('def dyld_attempts(')]
popen="child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=output, stderr=errors,\n                                     cwd=out, env=env, start_new_session=True)"
require(child.count(popen)==1 and 'chdir(' not in child,'actual monitor cwd argument')
bs=boot.read_text();call=[s for s in bs.splitlines() if s.startswith('module.child_run(')];require(len(call)==1,'one retained call')
vendor='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
def expected_call(d):return 'module.child_run('+repr([vendor,'-I','-B',str(d/'worker_proposal/install_freeze.py'),'--admission',str(d/'ADMIT_INSTALL.json')])+', Path('+repr(str(d/'monitor'))+"), 'INSTALL', 180, expected_environment)"
equal(call[0],expected_call(OLD.parent),'retained exact cwd/entry/argument vector')
contract=load(W/'CWD_CONTRACT_CHECK.json')
equal(contract,dict(schema='ri222-static-source-cwd-contract-v1',status='PASS_LITERAL_INTERFACE_NOT_EXECUTION',monitor=ref(identity(mon)),monitor_function='child_run(command, out, label, seconds, env)',exact_popen=popen,retained_actual_bootstrap=ref(identity(boot)),retained_actual_call=call[0],prospective_call_text=expected_call(D),prospective_call_executed=False,outer_cwd=str(D),child_cwd=str(D/'monitor'),installer=ref(identity(W/'install_freeze.py')),installer_guard=newguard,guard_precedes_ownership=True,postchecker=ref(identity(W/'check_installation.py')),outer_cwd_assertion="eq(dispatch['cwd'],str(D),'outer cwd')",monitor_implementation_unchanged=True,limits_unchanged=True,new_bootstrap_created=False,new_runtime_observation=False),'entire static cwd contract independently reconstructed')
require("eq(dispatch['cwd'],str(D),'outer cwd')" in checker and 'workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=4000' in checker,'outer command scope retained')
c=load(a['custody']['path']);equal(c['status'],'REFUSED_BEFORE_OUTPUT_OWNERSHIP_E_UNCHANGED','historical actual refusal status');equal(c['qualification_credit'],0,'no qualification from failure')
event=load(a['genuine_failure']['path']);equal([event['initial_result']['chunk_id'],event['initial_result']['exit_code'],event['terminal_result']],['685f23',1,None],'saved genuine actual failure attribution')
for row in [c['admission'],c['dispatch']]+c['monitor_files']:equal(identity(row['path']),row,'entire preserved failed selection')
equal(sorted(x.name for x in (OLD.parent/'monitor').iterdir()),monitor_names,'exact failed monitor namespace')
require("Path.cwd()==D and literal(OUT)==OUT and literal(W)==W" in (OLD.parent/'monitor/INSTALL.stderr').read_text(),'actual observed old cwd refusal')
# E is opaque: only complete prior selected file identities and directory memberships.
ebefore=load(c['E_observation']['path']);require(len(ebefore)==57,'complete saved E57')
for row in ebefore:
 p=E/row['relative'];equal(state(p.lstat()),row['state'],'E selection unchanged')
 if row['kind']=='directory':require(p.is_dir() and not p.is_symlink(),'E directory kind');equal(sorted(x.name for x in p.iterdir()),row['entries'],'whole E membership')
 else:equal(identity(p),row['identity'],'whole opaque unchanged E file')
# Persisted RI213 partial is a metadata file, not an installer invocation.
oldpartial=B/'ri213-freeze-clock-repair-2xc_b29x'
require((oldpartial/'tmp').is_dir() and not list((oldpartial/'tmp').iterdir()),'old RI213 tmp still empty')
require((oldpartial/'monitor').is_dir() and not list((oldpartial/'monitor').iterdir()),'old RI213 monitor still empty')
pinned(oldpartial/'HOST_GENUINE_TOOL.json',1891,'07cbac05498fb9329338592a1dea8255d09145bee24598491722d494509b4305')
absences=c['operation_and_mode_absences']+[str(D/n) for n in ('ADMIT_INSTALL.json','DISPATCH.json','INSTALL_BOOTSTRAP.py','tmp','monitor')]+[a['output']]
for p in absences:require(not os.path.lexists(p),'retained fresh absent '+p)
actual=load(W/'ACTUAL_ADMIN_RECEIPTS.json');equal(actual['current_author_admin_failures'],[],'author reports no new administrative failure')
byid={x['chunk_id']:x for x in actual['receipts']};equal([byid['c774a3']['exit_code'],byid['ad048f']['exit_code'],byid['ad048f']['predicates']],[0,0,6645],'author saved actual administrative attribution only')
for row in actual['receipts']:
 for key in ('result','source','contract'):
  if key in row:verify(row[key])
# Rehash current seal at end; no current packet write can hide behind the opening read.
seal(W,16)
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=R);args=parser.parse_args()
result=dict(schema='ri222-independent-metadata-review-v1',status='PASS_SOURCE_LITERAL_AND_OPAQUE_METADATA_ONLY',checks=checks,source_handoff=ref(observed[str(W/'HANDOFF.json')]),source_manifest=ref(observed[str(W/'SOURCE_PINS.json')]),base_inputs=806,repair_inputs=90,distinct_inputs=896,prior_source_rows_retained=857,prior_role_rows=810,prospective_source_rows=904,exact_namespace=16,payloads=15,projection=projection,unchanged_spans=spans,cwd_contract=contract,E_files=48,E_directories=9,actual_predecessor_failure_preserved=True,absences=absences,observed_identity_count=len(observed),observed_identities=[observed[k] for k in sorted(observed)],subject_execution=False,qualification_credit=0,ret_paused=True)
p=args.output/'CHECK_RESULT.json';data=canonical(result)
with p.open('xb') as f:require(f.write(data)==len(data),'complete own result');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(result=dict(path=str(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()),checks=result['checks'],observed_identity_count=len(observed),status=result['status'])))
