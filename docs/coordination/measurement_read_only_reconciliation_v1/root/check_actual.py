from pathlib import Path
import hashlib,importlib.util,json,os,shlex
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri234-root-reconciliation-tzop5ais';D=B/'ri226-directory-custody-recovery-yvfg_p1b';O=B/'ri226-freeze-reconciliation-operation-yvfg_p1b';E=B/'ri154-white-execution-proposed-42_uvw15'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7';s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
count=0
identities={}
def eq(a,b):
 global count
 assert m.canonical(a)==m.canonical(b);count+=1
def current(row):
 obs=m.identity(row['path']);eq(obs,row);identities[row['path']]=obs
posttool=m.load('/private/tmp/ri234_postcheck_tool.json');assert posttool['initial']['chunk_id']=='cfb84c' and posttool['initial']['exit_code']==0
postref=m.save('GENUINE_POSTCHECK_TOOL.json',posttool);result=json.loads(posttool['initial']['output']);m.verify(result['report']['path'],result['report']);report=m.load(result['report']['path']);assert report['status']=='PASS_READ_ONLY_RECONCILIATION_PENDING_ROOT_ACCEPTANCE' and report['checks']==161124
transcript=m.load(R/'GENUINE_RECONCILIATION_TOOL.json');assert transcript['initial_result']['chunk_id']=='5709fd' and transcript['initial_result']['session_id']==77528 and transcript['initial_result'].get('exit_code') is None and transcript['initial_result']['output']==''
assert transcript['terminal_result']['chunk_id']=='d0b911' and transcript['terminal_result']['exit_code']==0 and transcript['terminal_result']['output']=='' and transcript['terminal_result'].get('session_id') is None
eq(transcript['terminal_arguments'],dict(session_id=77528,chars='',yield_time_ms=1000,max_output_tokens=4000));eq(transcript['intermediate_calls'],[])
dispatch=m.load(D/'DISPATCH.json');eq(shlex.split(transcript['initial_arguments']['cmd']),dispatch['outer_argv']);eq(transcript['initial_arguments'],dict(cmd=dispatch['shell_command'],workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=4000))
for n in ['GENUINE_PREDISPATCH_HOST.json','GENUINE_POST_HOST.json']:
 host=m.load(R/n);obs=json.loads(host['result']['output']);eq(obs,host['observation']);assert host['result']['exit_code']==0 and obs['returncode']==0 and obs['stderr']=='';old=m.load(D/'HOST_BEFORE.json');eq(obs,{k:v for k,v in old.items() if k not in ('schema','genuine_tool')})
for row in m.load(R/'ISSUED_CONTROLS.json').values():
 if isinstance(row,dict) and 'state' in row:current(row)
for row in m.load(R/'FRESH_PREDISPATCH_CHECK.json')['outputs']:current(row)
for row in m.load(D/'SOURCES_BEFORE.json'):current(row)
before=m.load(O/'BEFORE.json');obs=m.load(O/'OBSERVATIONS.json');complete=m.load(O/'COMPLETE.json');eq(complete['status'],'RECONCILED_PENDING_INDEPENDENT_ROOT_REVIEW');eq(complete['first_error'],None);eq(complete['original_status'],'REFUSED_RETAIN_ALL_PARTIALS')
assert len(complete['independent_tails'])==8 and all(x['error'] is None for x in complete['independent_tails'].values())
eq(sorted(p.name for p in O.iterdir()),['ATTEMPT.json','BEFORE.json','COMPLETE.json','FROZEN.json','OBSERVATIONS.json']);eq(before['E'],obs['E_after']);eq(before['E'],report['whole_E']);eq(before['E'],m.load(D/'E_BEFORE.json'))
for row in before['E']:
 p=E/row['relative'];st=p.lstat();eq([st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns],row['state'])
 if row['kind']=='directory':eq(sorted(x.name for x in p.iterdir()),row['entries'])
 else:current(row['identity'])
for row in before['bindings'].values():current(row)
supplier=m.load(R/'POST_SUPPLIER.json');old=m.load(D/'SUPPLIER_BEFORE.json');eq({k:v for k,v in supplier.items() if k!='observed_at_unix_ns'},{k:v for k,v in old.items() if k!='observed_at_unix_ns'})
for row in supplier['vendor']+supplier['tools']:current(row)
for row in supplier['namespace']:
 p=Path(row['path']);st=p.lstat();eq([st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns],row['state'])
 if row['kind']=='directory':eq(sorted(x.name for x in p.iterdir()),row['entries'])
 else:eq(os.readlink(p),row['target'])
for p in supplier['absent']:assert not os.path.lexists(p)
monitor=m.load(D/'monitor/RECONCILE.COMPLETION.json');assert monitor['passed'] and monitor['child_exit_code']==0 and monitor['first_error'] is None and monitor['tail_errors']==[] and monitor['stop_reason'] is None
samples=monitor['samples'];attempts=monitor['monitor_attempts'];assert len(attempts) in (len(samples),len(samples)+1);previous=0
for raw,row in zip(attempts,samples):
 assert raw['returncode']==0 and raw['stderr']=='' and raw['stdout'].strip().isdigit();eq(int(raw['stdout']),row['rss_kib']);eq(raw['elapsed_seconds'],row['elapsed_seconds']);assert abs(row['gap_seconds']-(row['elapsed_seconds']-previous))<1e-12 and 0<=row['gap_seconds']<=.1 and row['rss_kib']<=524288;previous=row['elapsed_seconds']
if len(attempts)>len(samples):
 raw=attempts[-1];assert raw['returncode']==1 and raw['stdout'].strip()=='' and raw['stderr']=='' and previous<=raw['elapsed_seconds']<=monitor['elapsed_seconds']
assert 0<monitor['elapsed_seconds']<=180 and monitor['final_sample_gap_passed'] and 0<=monitor['elapsed_seconds']-previous<=.1;assert abs(monitor['elapsed_seconds']-previous-monitor['final_sample_to_reap_gap_seconds'])<1e-12
eq(max(x['rss_kib'] for x in samples),monitor['peak_sampled_rss_kib']);assert all(m.ref(D/'monitor'/('RECONCILE.'+k))['bytes']==0 for k in ('stdout','stderr'))
eq(m.snapshot(),m.load(R/'REPO_ENTRY.json'))
record=m.save('ROOT_ACTUAL_RECONCILIATION_CHECK.json',dict(schema='ri234-root-actual-reconciliation-review-v1',status='PASS_ACTUAL_EVIDENCE_PENDING_NONAUTHOR_REVIEW',canonical_comparisons=count,distinct_current_whole_identities=len(identities),identities=list(identities.values()),sameauthor_postcheck=result['report'],sameauthor_predicates=161124,genuine_postcheck=postref,monitor_samples=len(samples),monitor_attempts=len(attempts),elapsed_seconds=monitor['elapsed_seconds'],peak_sampled_child_rss_kib=monitor['peak_sampled_rss_kib'],maximum_sample_gap_seconds=max(x['gap_seconds'] for x in samples),final_sample_to_reap_gap_seconds=monitor['final_sample_to_reap_gap_seconds'],E_unchanged=True,original_failed_operation_remains_refused=True,repository_unchanged=True,scientific_execution=False,mode_admission=False,RET_paused=True,checker=m.ref(Path(__file__).resolve())))
print(json.dumps(dict(record=record,comparisons=count,identities=len(identities),samples=len(samples),maximum_gap=max(x['gap_seconds'] for x in samples))))
