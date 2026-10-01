"""Opaque metadata and literal source checks only; no source load/compile/AST,
monitor/installer execution, fixtures, vendor or scientific observations."""
from pathlib import Path
import hashlib,json,difflib,os,stat
B=Path('/Volumes/AI_DATA/development/det-review-evidence');W=Path(__file__).resolve().parent;D=W.parent
OLD=B/'ri218-freeze-byte-repair-x62withm/worker_proposal';R=B/'ri221-root-installation-ru2v15ie';checks=0
def need(v,msg):
 global checks
 checks+=1
 if not v:raise ValueError(msg)
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(p):return json.loads(Path(p).read_bytes())
def state(a):return [a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns]
def pin(p):
 p=Path(p);a=p.lstat();need(stat.S_ISREG(a.st_mode) and not p.is_symlink(),'regular opaque object');h=hashlib.sha256();n=0
 with p.open('rb') as f:
  need(state(os.fstat(f.fileno()))==state(a),'opened selection')
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
  need(state(os.fstat(f.fileno()))==state(a),'end selection')
 need(state(p.lstat())==state(a) and n==a.st_size,'complete stable opaque read')
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def verify(r):q={k:r[k] for k in ('path','bytes','sha256')};need(pin(q['path'])==q,'whole pin '+q['path']);return q
def save(n,v):
 b=canonical(v)
 with (W/n).open('xb') as f:need(f.write(b)==len(b),'complete metadata output')
assignment=load(R/'RI222_REPAIR_ASSIGNMENT.json');need(pin(R/'RI222_REPAIR_ASSIGNMENT.json')['sha256']=='bae3531b2bc3e50f3685beca009610bf7356d36ba7e7ad0cfc3a10f2b5a162b8','exact assignment')
for k in ('predecessor','supersession','review','genuine_failure','custody'):verify(assignment[k])
manifest=load(W/'SOURCE_PINS.json');need(set(manifest)=={'schema','status','files'} and manifest['schema']=='ri209-proposal-source-pins-v1' and manifest['status']=='SOURCE_ONLY_NOT_ADMISSION','closed exact source manifest')
need([Path(r['path']).name for r in manifest['files']]==['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_installation.py','install_freeze.py'],'five ordered source payloads')
for r in manifest['files']:need(Path(r['path']).parent==W,'literal current source path');verify(r)
oldhand=load(OLD/'HANDOFF.json');need(sorted(x.name for x in OLD.iterdir())==sorted(oldhand['namespace']),'old complete sealed namespace')
for r in oldhand['files']:verify(r)
inputs=load(W/'INPUT_PINS.json');repair=load(W/'REPAIR_PROVENANCE.json');oldrepair=load(OLD/'REPAIR_PROVENANCE.json')
need((W/'INPUT_PINS.json').read_bytes()==(OLD/'INPUT_PINS.json').read_bytes(),'all original input bytes');need(len(inputs['files'])==806 and inputs['prior_role_count']==810,'806 original inputs and810 historical roles')
need(len(repair['files'])==90 and len(oldrepair['files'])==43,'90-row union retains43')
need({k:len(v) for k,v in repair['groups'].items()}==dict(inherited43=43,predecessor15=15,failed_root12=12,failed_monitor4=4,root_adjudication11=11,support5=5),'exact provenance groups')
combined={}
for rows in repair['groups'].values():
 for r in rows:need(r['path'] not in combined or combined[r['path']]==r,'no conflicting provenance');combined[r['path']]=r
need(sorted(combined.values(),key=lambda r:r['path'])==repair['files'],'whole grouped union, no omitted role')
for r in oldrepair['files']+oldhand['files']+[assignment['predecessor']]:need(combined[r['path']]==r,'all predecessor pins retained')
expected={}
for r in inputs['files']+repair['files']:
 q={k:r[k] for k in ('path','bytes','sha256')};need(q['path'] not in expected or expected[q['path']]==q,'consistent full declared source');expected[q['path']]=q
need(len(expected)==896,'896 distinct opaque inputs')
for p in sorted(expected):verify(expected[p])
# Entire prior operational/source preflight domain is retained as opaque files.
prior_sources=load(OLD.parent/'SOURCES_BEFORE.json');need(len(prior_sources)==857,'previous operational source857')
for r in prior_sources:need(expected[r['path']]=={k:r[k] for k in ('path','bytes','sha256')},'every old857 source remains declared')
# Check immutable saved failure records, not a replay of operational observers.
custody=load(assignment['custody']['path']);event=load(assignment['genuine_failure']['path'])
need(event['initial_result']['chunk_id']=='685f23' and event['initial_result']['exit_code']==1 and event['terminal_result'] is None,'retained genuine failed one-event attribution')
need(custody['status']=='REFUSED_BEFORE_OUTPUT_OWNERSHIP_E_UNCHANGED' and custody['qualification_credit']==0,'failure scope')
for r in [custody['admission'],custody['dispatch']]+custody['monitor_files']:verify(r);need(state(Path(r['path']).lstat())==r['state'],'complete failed file selection retained')
need(sorted(p.name for p in (OLD.parent/'monitor').iterdir())==['INSTALL.ATTEMPT.json','INSTALL.COMPLETION.json','INSTALL.stderr','INSTALL.stdout'],'entire old monitor namespace retained')
new=(W/'install_freeze.py').read_text();old=(OLD/'install_freeze.py').read_text();checktext=(W/'check_installation.py').read_text()
change=("Path.cwd()==D and literal(OUT)==OUT and literal(W)==W","Path.cwd()==literal(D/'monitor') and literal(OUT)==OUT and literal(W)==W")
correspondence=[]
for n in ('install_freeze.py','check_installation.py'):
 a=(OLD/n).read_text();z=(W/n).read_text();projected=z
 oldline=[x for x in a.splitlines() if x.startswith('REPAIR=')];newline=[x for x in z.splitlines() if x.startswith('REPAIR=')]
 need(len(oldline)==len(newline)==1 and newline[0]=='REPAIR='+repr(pin(W/'REPAIR_PROVENANCE.json')),'exact complete repair constant')
 if n=='install_freeze.py':need(z.count(change[1])==1 and change[0] not in z,'one corrected guard');projected=projected.replace(change[1],change[0])
 projected=projected.replace(newline[0],oldline[0]).replace('ri222-freeze-cwd-repair-ypiy2jqw','ri218-freeze-byte-repair-x62withm').replace('ri222-freeze-install-operation-ypiy2jqw','ri218-freeze-install-operation-x62withm')
 need(projected==a,'entire inverse projection '+n);need(len(a.splitlines())==len(z.splitlines()),'line-count correspondence')
 correspondence.append(dict(source=n,old=pin(OLD/n),new=pin(W/n),lines=len(z.splitlines()),entire_inverse_projection=True))
for start,end in [(' # RI213: all safe receipt/error state',' OUT.mkdir(mode=0o700)'),('  # All eight ordinary tails above','  save(OUT/\'COMPLETE.json\',completion)'),('  def sources_tail():','  # All eight ordinary tails above')]:need(old[old.index(start):old.index(end)]==new[new.index(start):new.index(end)],'complete retained clock/tail block')
for text in ("need(Path(path).read_bytes()==data,'written exact bytes')","need(DEST.read_bytes()==candidate,'exact accepted byte copy')","def same(a,b,msg):need(m.canonical(a)==m.canonical(b),msg)","schema='ri213-installation-completion-v1'"):
 need(new.count(text)==old.count(text)==1,'retained byte/JSON/schema semantics')
need(new.index(change[1])<new.index(' OUT.mkdir(mode=0o700)'),'guard remains before ownership')
diff=''.join(''.join(difflib.unified_diff((OLD/n).read_text().splitlines(keepends=True),(W/n).read_text().splitlines(keepends=True),fromfile=str(OLD/n),tofile=str(W/n))) for n in ('install_freeze.py','check_installation.py','PROTOCOL.md'))
need((W/'SOURCE_DIFF.patch').read_text()==diff,'entire disclosed source/protocol delta')
# Explicit source interface check: these are literal texts, not compiled code.
monitor=B/'ri141-white-bootstrap-source-h58ls076/prepare.py';mp=pin(monitor)
need(mp['bytes']==45721 and mp['sha256']=='8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe','complete unchanged monitor source')
ms=monitor.read_text();child=ms[ms.index('def child_run(command, out, label, seconds, env):'):ms.index('def dyld_attempts(')]
popen="child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=output, stderr=errors,\n                                     cwd=out, env=env, start_new_session=True)"
need(child.count(popen)==1 and 'chdir' not in child,'real unchanged Popen forwards cwd=out')
bootstrap=OLD.parent/'INSTALL_BOOTSTRAP.py';bp=pin(bootstrap);need(bp['bytes']==2417 and bp['sha256']=='76779aeb180fc09ef2c90a2c1341ff3f5285640645ac15e1d90b27014422a00a','whole retained actual bootstrap')
bs=bootstrap.read_text();calls=[x for x in bs.splitlines() if x.startswith('module.child_run(')];need(len(calls)==1,'one actual monitor invocation');actual_call=calls[0]
vendor='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
def call(d):return "module.child_run("+repr([vendor,'-I','-B',str(d/'worker_proposal/install_freeze.py'),'--admission',str(d/'ADMIT_INSTALL.json')])+", Path("+repr(str(d/'monitor'))+"), 'INSTALL', 180, expected_environment)"
need(actual_call==call(OLD.parent),'actual out is literal previous D/monitor')
prospective_call=actual_call.replace(str(OLD.parent),str(D));need(prospective_call==call(D),'fresh prospective call changes paths only')
need(new.count("Path.cwd()==literal(D/'monitor')")==1 and 'os.chdir' not in new,'exact literal child guard, no chdir')
need("eq(dispatch['cwd'],str(D),'outer cwd')" in checktext and "workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=4000" in checktext,'retained outer/tool cwd D and exact arguments')
need('child_run(command,D/monitor' in (W/'PROTOCOL.md').read_text() and 'Popen(cwd=out)' in (W/'PROTOCOL.md').read_text(),'explicit two-cwd contract')
cwd=dict(schema='ri222-static-source-cwd-contract-v1',status='PASS_LITERAL_INTERFACE_NOT_EXECUTION',monitor=mp,monitor_function='child_run(command, out, label, seconds, env)',exact_popen=popen,retained_actual_bootstrap=bp,retained_actual_call=actual_call,prospective_call_text=prospective_call,prospective_call_executed=False,outer_cwd=str(D),child_cwd=str(D/'monitor'),installer=pin(W/'install_freeze.py'),installer_guard=change[1],guard_precedes_ownership=True,postchecker=pin(W/'check_installation.py'),outer_cwd_assertion="eq(dispatch['cwd'],str(D),'outer cwd')",monitor_implementation_unchanged=True,limits_unchanged=True,new_bootstrap_created=False,new_runtime_observation=False)
save('CWD_CONTRACT_CHECK.json',cwd)
future=set(expected)
for r in manifest['files']+[pin(W/'SOURCE_PINS.json')]:need(r['path'] not in future,'distinct new source file');future.add(r['path'])
for p in (D/'ROOT_SOURCE_REVIEW.json',D/'INSTALL_BOOTSTRAP.py'):need(str(p) not in future,'distinct future root binding');future.add(str(p))
need(len(future)==904,'prospective exact904 source count')
for p in (D/'ADMIT_INSTALL.json',D/'DISPATCH.json',D/'INSTALL_BOOTSTRAP.py',D/'tmp',D/'monitor',Path(assignment['output'])):need(not os.path.lexists(p),'no new operational object')
result=dict(schema='ri222-administrative-source-check-v1',status='PASS_LITERAL_SOURCE_AND_OPAQUE_CUSTODY_NOT_EXECUTION',checks=checks,assignment=pin(R/'RI222_REPAIR_ASSIGNMENT.json'),source_manifest=pin(W/'SOURCE_PINS.json'),source_contract=pin(W/'CWD_CONTRACT_CHECK.json'),base_inputs=806,repair_rows=90,distinct_opaque_inputs=896,prior_historical_roles=810,complete_prior_source_domain=857,prospective_source_count=904,correspondence=correspondence,whole_clock_and_eight_tail_spans_unchanged=True,byte_and_JSON_comparisons_unchanged=True,retained_clock_schema='ri213-installation-completion-v1',actual_predecessor_failure='685f23 exit1 before ownership',old_monitor_files_and_states_preserved=True,subject_execution=False,fixture_execution=False,current_runtime_observation=False,scientific_decode=False,qualification_credit=0)
save('ADMIN_CHECK.json',result)
print(json.dumps(dict(report=pin(W/'ADMIN_CHECK.json'),cwd_contract=pin(W/'CWD_CONTRACT_CHECK.json'),checks=result['checks'],status=result['status'])))
