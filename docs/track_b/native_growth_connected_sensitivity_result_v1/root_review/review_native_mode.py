from metadata import *
import sys
mode=sys.argv[1];N=B/'ri122-native-caller-source-jgehvvxx';prefix=mode.upper();A=N/(mode+'-01')
def full(path):
 z=identity(path);return dict(path=z['path'],resolved_path=z['resolved_path'],symlinks=z['symlink_chain'],bytes=z['bytes'],sha256=z['sha256'])
catalogue=load(N/'PROSPECTIVE_STAGE_INVENTORY.json'); by_key={r['key']:{k:r[k]for k in ('role','path')}for r in catalogue['catalogue']}
f=load(N/(prefix+'_EXECUTION_FREEZE.json'));au=load(N/(prefix+'_AUTHORIZATION.json'));ra=load(N/(prefix+'_ROOT_ADMISSION.json'));r=load(A/'receipt.json');outer=load(N/(prefix+'_OUTER_TOOL_RESULT.json'))
assert outer['invocation']==ra['outer_invocation'] and type(outer['result']['exit_code']) is int and outer['result']['exit_code']==0 and 'session_id' not in outer['result']
assert json.loads(outer['result']['output'])==dict(mode=mode,success=True,receipt=str(A/'receipt.json'),receipt_sha256=full(A/'receipt.json')['sha256'])
assert r['success'] is True and type(r['exit_code']) is int and r['exit_code']==0 and r['error'] is None and r['cleanup_errors']==[] and r['received_signals']==[] and r['input_stability'] is True
expected={z['role']:{'ok':True,'identity':full(z['path'])} for z in f['inputs']}
for k,p in dict(interpreter=f['interpreter']['path'],supervisor=f['supervisor']['path'],freeze=str(N/(prefix+'_EXECUTION_FREEZE.json')),authorization=str(N/(prefix+'_AUTHORIZATION.json'))).items():expected[k]=dict(ok=True,identity=full(p))
assert r['inputs_before']==r['inputs_after']==expected
assert [{k:r[k]for k in ('role','path')}for r in f['inputs']]==[by_key[k]for k in catalogue['stages'][mode]['input_order']]
assert list(expected)==[by_key[k]['role']for k in catalogue['stages'][mode]['complete_protected_order']]
runtime=load(N/'RUNTIME_CLOSURE.json');host=runtime['host_platform']
namespace={'directories':{row['path']:{'ok':True,'identity':row}for row in runtime['directories']},'absences':{path:{'ok':True,'absent':True}for path in runtime['absences']},'host_platform':{'uname':{'ok':True,'identity':host['expected_uname']},'system_version':{'ok':True,'identity':host['system_version_plist']['expected_values']},'system_dependencies':[{'ok':True,'identity':{k:row[k]for k in ('install_name','location_status','shared_cache_status')}}for row in host['system_dependencies']],'trust_boundary':host['trust_boundary']}}
assert r['runtime_namespace_before']==r['runtime_namespace_after']==namespace

for z in f['inputs']:assert z['identity']==expected[z['role']]['identity']
for k in ('argv','cwd','environment','limits'):assert r[k]==f[k]
compact=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True)
payload=hashlib.sha256(compact({k:v for k,v in f.items() if k!='authorization'}).encode()).hexdigest()
assert au['freeze_payload_sha256']==r['freeze_payload_sha256']==payload
assert au['authorized'] is True and au['mode']==mode and au['supervisor_sha256']==f['supervisor_sha256']
assert f['authorization']['sha256']==full(N/(prefix+'_AUTHORIZATION.json'))['sha256']
prepared=load(A/'prepared.json');admitted=load(A/'admission.json')
assert prepared['observed_runtime_namespace']==admitted['observed_runtime_namespace']==namespace
assert prepared['observed_inputs']==admitted['observed_inputs']==expected and admitted['admitted'] is True and prepared['authorization_granted'] is False
assert admitted['freeze_payload_sha256']==payload
for k in ('argv','cwd','environment','limits'):assert prepared[k]==admitted[k]==f[k]
assert prepared['supervisor_argv']==[str(N/('launch_audit.py' if mode=='audit' else 'supervise.py')),mode] and prepared['supervisor_cwd']==f['cwd']
assert prepared['paths']=={k:z['identity']['path'] for k,z in expected.items()}
assert admitted['freeze_identity']==expected['freeze']['identity'] and admitted['authorization_identity']==expected['authorization']['identity']
for role,name in [('stdout','stdout.log'),('stderr','stderr.log'),('samples','samples.jsonl'),('prepared','prepared.json'),('admission','admission.json')]:assert r['outputs'][role]==full(A/name)
assert (A/'stderr.log').read_bytes()==b''
events=[json.loads(line) for line in (A/'samples.jsonl').read_text().splitlines()]
assert events[0]['event']=='launch' and events[0]['pid']==events[0]['pgid']==r['pid']==r['pgid']
mon=[z for z in events if z['event']=='monitor_attempt'];assert len(mon)==r['monitor_attempts']
live=0;peak=0
for i,z in enumerate(mon,1):
 assert z['index']==i and z['returncode']==0 and z['stderr']=='' and 'error' not in z
 assert z['argv']==['/bin/ps','-axo','pid=,pgid=,rss=']
 assert 0<z['effective_timeout_seconds']<=min(.25,120-z['elapsed_before'])+1e-12 and z['elapsed_after']<120
 rows=[];seen=set()
 for line in z['stdout'].splitlines():
  cells=line.split();assert len(cells)==3 and all(x.isdecimal() for x in cells);pid,pgid,rss=map(int,cells)
  assert pid not in seen;seen.add(pid)
  if pid==r['pid']:assert pgid==r['pid']
  if pgid==r['pid']:rows.append(dict(pid=pid,pgid=pgid,rss_kib=rss))
 assert rows==z['owned_rows'] and sum(x['rss_kib'] for x in rows)*1024==z['owned_rss_bytes']
 present=any(x['pid']==r['pid'] for x in rows);assert z['owned_leader_present'] is present
 assert present or z['child_poll'] is not None
 assert z['terminal_absence']==(not present and z['child_poll'] is not None)
 if z['child_poll_before'] is not None:assert rows==[]
 live+=int(present);peak=max(peak,z['owned_rss_bytes'])
assert live==r['live_rss_samples']>0 and peak==r['sampled_peak_rss_bytes']<=536870912
assert mon[-1]['terminal_absence'] is True and mon[-1]['owned_rows']==[] and type(mon[-1]['child_poll']) is int and mon[-1]['child_poll']==0
assert events[-1]['event']=='terminal_poll' and events[-1]['returncode']==0 and events[-1]['terminal_absence'] is True
assert not any(z['event']=='owned_group_cleanup' for z in events)
assert r['child_end_observed'] is True and r['child_elapsed_seconds']<120
if mode=='witness':
 for k in ('witness_certificate_absence_before','witness_certificate_absence_after'):assert r[k]==dict(original=True,copy=True,audit_copy=True)
 for p in (N/'CERTIFICATE.json',N/'closure/native_growth_connected_sensitivity_v1/CERTIFICATE.json',N/'AUDIT_CANDIDATE.json'):assert not p.exists()
if mode=='optimized':assert (N/'normal-01/stdout.log').read_bytes()==(A/'stdout.log').read_bytes()
refs=dict(source_adjudication=N/'ROOT_SOURCE_ADJUDICATION.json',applicability=N/(prefix+'_APPLICABILITY.json'),genuine_outer=N/(prefix+'_OUTER_TOOL_RESULT.json'),root_admission=N/(prefix+'_ROOT_ADMISSION.json'),freeze=N/(prefix+'_EXECUTION_FREEZE.json'),authorization=N/(prefix+'_AUTHORIZATION.json'),receipt=A/'receipt.json')
output_names=['receipt.json','stdout.log','stderr.log','samples.jsonl','prepared.json','admission.json']
if mode=='audit':
 assert (A/'REPORT.json').read_bytes()==(A/'stdout.log').read_bytes()
 assert r['outputs']['audit_report']==full(A/'REPORT.json')
 output_names.append('REPORT.json')
review=dict(schema='ri122-root-completed-mode-review-v1',status='PASS_COMPLETED_'+prefix+'_CUSTODY_PENDING_INDEPENDENT_REVIEW',mode=mode,blocking_findings=[],**{k:full(p) for k,p in refs.items()},outputs={name:full(A/name) for name in output_names},before_after_current_identities_match=True,terminal_owned_group_absent=True,native_arithmetic_recomputed=False,native_mathematics_accepted=False,programme_complete=False,raw_census_reconstruction=dict(attempts=len(mon),live=live,peak_rss_bytes=peak,child_seconds=r['child_elapsed_seconds']))
path=N/(prefix+'_ROOT_COMPLETE_REVIEW.json')
with path.open('xb') as out:out.write(canonical(review));out.flush();os.fsync(out.fileno())
print(json.dumps(ref(path)))
