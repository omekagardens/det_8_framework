"""Read-only RI224 installation failure evidence review; no subject execution.
Only fixed saved administrative metadata and opaque bytes are read. Result is
written exclusively in this new reviewer reservation. No candidate JSON decode.
"""
from pathlib import Path
import hashlib,json,os,stat
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri222-freeze-cwd-repair-ypiy2jqw';W=D/'worker_proposal';O=B/'ri222-freeze-install-operation-ypiy2jqw';E=B/'ri154-white-execution-proposed-42_uvw15';R=Path(__file__).resolve().parent
checks=0;identities={}
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def require(ok,msg):
 global checks
 checks+=1
 if not ok:raise ValueError(msg)
def equal(a,b,msg):require(canonical(a)==canonical(b),msg)
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def identity(path):
 p=Path(path);before=p.lstat();require(p.is_absolute() and p.resolve()==p and stat.S_ISREG(before.st_mode),'literal regular file')
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  equal(state(os.fstat(f.fileno())),state(before),'open selection')
  for block in iter(lambda:f.read(1048576),b''):h.update(block);n+=len(block)
  equal(state(os.fstat(f.fileno())),state(before),'descriptor unchanged')
 equal(state(p.lstat()),state(before),'read selection retained');require(n==before.st_size,'whole file')
 row=dict(path=str(p),resolved_path=str(p),symlink_chain=[],bytes=n,sha256=h.hexdigest(),state=state(before))
 if str(p) in identities:equal(identities[str(p)],row,'repeat selection retained')
 identities[str(p)]=row;return row
def ref(p):return {k:identity(p)[k] for k in ('path','bytes','sha256')}
def pure(row):return {k:row[k] for k in ('bytes','sha256')}
def verify(row):v=identity(row['path']);equal(pure(v),pure(row),'whole pin');return v
def load(p):
 def pairs(rows):
  obj={}
  for k,v in rows:require(k not in obj,'duplicate administrative key');obj[k]=v
  return obj
 def bad(x):raise ValueError('nonfinite metadata')
 identity(p);return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=bad)
hand=load(W/'HANDOFF.json');equal(pure(identity(W/'HANDOFF.json')),dict(bytes=9023,sha256='5762caec4ca89f2687de17da71671ec82e1066e81854b9d45364ea3ed59c1330'),'whole unchanged source seal')
equal(sorted(p.name for p in W.iterdir()),sorted(hand['namespace']),'source namespace')
for row in hand['files']:verify(row)
install=(W/'install_freeze.py').read_text();checker=(W/'check_installation.py').read_text()
require("same(z['state'][:4],r['state'][:4],'root device inode mode links')" in install,'literal failing predicate')
require("eq(now[name]['state'][:4],r['state'][:4],'root persistent identity')" in checker,'same checker premise')
require("need(Path.cwd()==literal(D/'monitor') and literal(OUT)==OUT and literal(W)==W,'fixed operation paths')" in install,'unchanged corrected cwd guard')
c=load(O/'COMPLETE.json');before=load(O/'BEFORE.json');obs=load(O/'OBSERVATIONS.json');attempt=load(O/'ATTEMPT.json');pre=load(D/'INSTALL_PREFLIGHT.json');admission=load(D/'ADMIT_INSTALL.json');dispatch=load(D/'DISPATCH.json')
expected_error=dict(type='ValueError',message='RI209: root device inode mode links',secondary=[])
equal(sorted(c),sorted('schema status admission candidate destination first_error independent_tails produced_outputs elapsed_seconds_before_complete_write timing complete_not_self_hashed scientific_execution mode_admission_issued ret_paused'.split()),'closed failure completion')
equal([c['schema'],c['status'],c['first_error'],c['complete_not_self_hashed'],c['scientific_execution'],c['mode_admission_issued'],c['ret_paused']],['ri213-installation-completion-v1','REFUSED_RETAIN_ALL_PARTIALS',expected_error,True,False,False,True],'actual refused completion and scope')
equal(c['admission'],ref(D/'ADMIT_INSTALL.json'),'actual issued admission');equal(dispatch['admission'],c['admission'],'dispatch/admission binding');equal(admission['preflight'],ref(D/'INSTALL_PREFLIGHT.json'),'actual admitted preflight')
equal(attempt,dict(schema='ri209-exclusive-install-attempt-v1',admission=c['admission'],candidate=c['candidate'],destination=str(E/'AUTHORIZED_FREEZE.json'),no_retry=True,scientific_execution=False),'entire actual attempt')
equal(obs['installation_write'],dict(error=None,cleanup_errors=[]),'write and descriptor closes completed before refusal')
equal(sorted(obs),sorted(['E_after','binding_actual','installation_write','sources_actual','supplier_actual']),'only actual saved prefix fields; no invented frozen record')
equal(before['E'],load(pre['E_before']['path']),'entire initial E baseline')
a={r['relative']:r for r in before['E']};z={r['relative']:r for r in obs['E_after']}
require(len(a)==57 and len(z)==58,'complete57 to58 E domain');equal(set(z).__len__(),len(a)+1,'one domain addition')
equal(sorted(z),sorted(list(a)+['AUTHORIZED_FREEZE.json']),'only named freeze added')
equal(a['.']['kind'],z['.']['kind'],'same root kind');equal(z['.']['state'][:3],a['.']['state'][:3],'same actual device/inode/mode')
equal([a['.']['state'][3],z['.']['state'][3]],[23,24],'observed root nlink23 to24')
equal([a['.']['state'][4],z['.']['state'][4]],[736,768],'observed root size736 to768')
equal(z['.']['entries'],sorted(a['.']['entries']+['AUTHORIZED_FREEZE.json']),'complete root membership only named addition')
for name,row in a.items():
 if name!='.':equal(z[name],row,'entire old member unchanged '+name)
# Independently reconstruct the whole live tree against the saved failed-tail E_after.
current=[]
for name in sorted(z):
 p=E/name;st=p.lstat();row=dict(relative=name,kind=z[name]['kind'],state=state(st));require(not p.is_symlink(),'no E links')
 if row['kind']=='directory':require(stat.S_ISDIR(st.st_mode),'directory type');row['entries']=sorted(x.name for x in p.iterdir())
 else:require(row['kind']=='file','file type');row['identity']=identity(p)
 current.append(row)
equal(current,obs['E_after'],'whole live E equals captured after tree');equal(sorted(str(p.relative_to(E)) for p in E.rglob('*')),sorted(n for n in z if n!='.'),'full live E namespace')
equal([sum(v['kind']=='file' for v in a.values()),sum(v['kind']=='directory' for v in a.values()),sum(v['kind']=='file' for v in z.values()),sum(v['kind']=='directory' for v in z.values())],[48,9,49,9],'full48+1/nine directory counts')
candidate=Path(c['candidate']['path']);verify(c['candidate']);installed=identity(E/'AUTHORIZED_FREEZE.json');equal(pure(installed),pure(c['candidate']),'whole candidate hash and length')
require(candidate.read_bytes()==(E/'AUTHORIZED_FREEZE.json').read_bytes(),'entire opaque candidate bytes match');require(installed['state'][3]==1 and installed['bytes']==26214,'single-link complete candidate')
# Source/role observations are saved administrative evidence; root supplies its separate complete postflight.
sources=load(pre['sources']['path']);require(len(sources)==904,'complete admitted source rows');equal(before['source_observations'],sources,'captured whole initial source domain');equal(obs['sources_actual'],sources,'saved whole source tail')
equal(obs['binding_actual'],before['bindings'],'saved whole binding tail')
for row in before['bindings'].values():equal(identity(row['path']),row,'all live exact root binding states')
selection=before['source_states'];equal([len(selection['copies']),len(selection['history']),len(selection['target_originals'])],[48,124,30],'complete role lists')
for pair in selection['copies']:
 for key in ('original','copy'):
  live=identity(pair[key]['path']);equal({k:live[k] for k in ('path','bytes','sha256','state')},pair[key],'full retained original/copy role')
for key in ('history','target_originals'):
 for row in selection[key]:live=identity(row['path']);equal({k:live[k] for k in ('path','bytes','sha256','state')},row,'full retained history/target role')
supplier=load(pre['supplier']['path']);equal(obs['supplier_actual'],dict(files=supplier['vendor']+supplier['tools'],namespace=supplier['namespace'],absent=[dict(path=p,absent=True) for p in supplier['absent']],uname=supplier['host']['uname']),'entire saved supplier tail versus admitted baseline, no new host command')
t=c['independent_tails'];tail_names=['source_inputs','root_bindings','supplier','E_and_frozen','save_observations','ordinary_outputs','final_E','output_namespace'];equal(sorted(t),sorted(tail_names),'all eight tails retained')
for name in tail_names:
 equal(sorted(t[name]),['error','value'],'closed tail record')
 equal(t[name]['error'],expected_error if name in ('E_and_frozen','final_E') else None,'actual distinct tail outcome')
 if name in ('E_and_frozen','final_E'):equal(t[name]['value'],None,'failed tail supplies no false value')
equal(t['source_inputs']['value'],sources,'whole passed source tail');equal(t['root_bindings']['value'],before['bindings'],'whole passed binding tail');equal(t['supplier']['value'],obs['supplier_actual'],'whole passed supplier tail')
produced={n:ref(O/n) for n in ('ATTEMPT.json','BEFORE.json','OBSERVATIONS.json')};equal(c['produced_outputs'],produced,'all and only produced saved outputs')
equal(t['save_observations']['value'],produced['OBSERVATIONS.json'],'actual saved observations tail');equal(t['ordinary_outputs']['value'],produced,'whole passed ordinary output tail');equal(t['output_namespace']['value'],[identity(O/n) for n in sorted(produced)],'whole passed output namespace before COMPLETE')
equal(sorted(p.name for p in O.iterdir()),sorted(list(produced)+['COMPLETE.json']),'exact four partial operation files');require(not (O/'FROZEN.json').exists(),'no frozen success record')
for p in O.iterdir():require(p.is_file() and not p.is_symlink() and p.stat().st_nlink==1,'ordinary single-link output')
timing=c['timing'];equal(sorted(timing),['elapsed','final','initial'],'complete timing')
for v in timing.values():equal(v['error'],None,'clock acquisition succeeded');require(type(v['value']) in (int,float),'exact numeric timing')
equal(timing['elapsed']['value'],timing['final']['value']-timing['initial']['value'],'elapsed real arithmetic');equal(c['elapsed_seconds_before_complete_write'],timing['elapsed']['value'],'complete duration binding')
monitor=load(D/'monitor/INSTALL.COMPLETION.json');ma=load(D/'monitor/INSTALL.ATTEMPT.json')
equal(sorted(p.name for p in (D/'monitor').iterdir()),['INSTALL.ATTEMPT.json','INSTALL.COMPLETION.json','INSTALL.stderr','INSTALL.stdout'],'four monitor files')
command=['/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9','-I','-B',str(W/'install_freeze.py'),'--admission',str(D/'ADMIT_INSTALL.json')]
equal([monitor['command'],ma['command']],[command,command],'whole actual child command');equal(monitor['environment'],admission['environment'],'actual exact environment');equal(ma['environment'],monitor['environment'],'attempt environment');equal([ma['wall_seconds'],monitor['wall_seconds']],[180,180],'retained wall limit')
equal([monitor['child_exit_code'],monitor['passed'],monitor['first_error'],monitor['tail_errors'],monitor['stop_reason'],monitor['final_sample_gap_passed']],[1,False,None,[],None,True],'genuine child failure distinct from monitor failure')
equal([len(monitor['samples']),len(monitor['monitor_attempts'])],[42,42],'complete42 samples and raw attempts')
previous=0
for sample,raw in zip(monitor['samples'],monitor['monitor_attempts']):
 equal(sorted(raw),['elapsed_seconds','returncode','stderr','stdout'],'complete raw attempt');equal(sorted(sample),['elapsed_seconds','gap_seconds','rss_kib'],'complete sample')
 require(type(raw['returncode']) is int and raw['returncode']==0 and raw['stderr']=='' and raw['stdout'].strip().isdigit(),'real successful raw ps')
 equal([raw['elapsed_seconds'],int(raw['stdout'].strip())],[sample['elapsed_seconds'],sample['rss_kib']],'raw RSS/time reconstruction')
 require(abs(sample['gap_seconds']-(sample['elapsed_seconds']-previous))<1e-12 and 0<=sample['gap_seconds']<=.1 and type(sample['rss_kib']) is int and 0<=sample['rss_kib']<=524288,'all actual gap/RSS bounds');previous=sample['elapsed_seconds']
require(0<monitor['elapsed_seconds']<180 and abs(monitor['final_sample_to_reap_gap_seconds']-(monitor['elapsed_seconds']-previous))<1e-12 and 0<=monitor['final_sample_to_reap_gap_seconds']<=.1,'wall and final reap interval')
equal(monitor['peak_sampled_rss_kib'],max(s['rss_kib'] for s in monitor['samples']),'peak reconstruction')
for k in ('stdout','stderr'):verify(monitor[k]);require(monitor[k]['bytes']==0,'empty child stream')
require(type(ma['pid_owner']) is int and ma['pid_owner']>0 and ma['scientific_target_entry'] is False,'parent-PID receipt only')
for p in [E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json']:require(not os.path.lexists(p),'no scientific mode authority')
require(not list((D/'tmp').iterdir()),'external tmp empty')
result=dict(schema='ri224-independent-failed-installation-check-v1',status='CONFIRM_FAILURE_AFTER_EXACT_WRITE_NOT_ACCEPTANCE',checks=checks,identities=list(identities.values()),identity_count=len(identities),first_error=expected_error,failed_tails=['E_and_frozen','final_E'],passed_tails=[n for n in tail_names if n not in ('E_and_frozen','final_E')],before_root=a['.'],after_root=z['.'],old_members_unchanged_except_root_metadata=True,exact_new_root_entry_only='AUTHORIZED_FREEZE.json',installed=installed,candidate=ref(candidate),candidate_body_decoded=False,operation_files=4,FROZEN_absent=True,monitor=ref(D/'monitor/INSTALL.COMPLETION.json'),monitor_samples=42,monitor_elapsed=monitor['elapsed_seconds'],peak_sampled_rss_kib=monitor['peak_sampled_rss_kib'],whole_source_and_supplier_postflight_external_to_this_review=True,subject_execution=False,qualification_credit=0,installation_acceptance=False,recovery_authority=False,ret_paused=True)
data=canonical(result)
with (R/'CHECK_RESULT.json').open('xb') as f:require(f.write(data)==len(data),'complete own metadata output');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(result=dict(path=str(R/'CHECK_RESULT.json'),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()),checks=result['checks'],identities=result['identity_count'],status=result['status'])))
