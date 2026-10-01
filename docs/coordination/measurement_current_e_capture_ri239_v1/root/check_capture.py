"""Independent root metadata/monitor outcome review; never imports the collector."""
from pathlib import Path
import hashlib,importlib.util,json,os,shlex
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=Path(__file__).resolve().parent;D=B/'ri236-current-e-normal-preparation-3geu_r1s';O=B/'ri236-current-e-capture-3geu_r1s'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=hp.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
n=0
def eq(a,b):
 global n
 assert m.canonical(a)==m.canonical(b),(a,b);n+=1
recipe=m.load(D/'worker_proposal/CAPTURE_RECIPE.json');contract=m.load(D/'worker_proposal/CURRENT_E_AND_MODE_CONTRACT.json')
m.verify(D/'worker_proposal/CAPTURE_RECIPE.json',dict(bytes=12114,sha256='3f46d182e4adedf6b6e346ebd5e5dd6eae60cf42b4e77b073a957531e4c68195'))
m.verify(D/'worker_proposal/CURRENT_E_AND_MODE_CONTRACT.json',dict(bytes=9569,sha256='b8794cbdb514dc79453b24c2cf55760a889d8e4569c807e1ab678389b0901354'))
eq(sorted(x.name for x in O.iterdir()),sorted(contract['capture_outputs']))
identities=[m.identity(O/name) for name in sorted(contract['capture_outputs'])]
for r in identities:assert r['state'][3]==1 and not r['symlink_chain'] and r['bytes']<=67108864
complete=m.load(O/'COMPLETE.json');eq(sorted(complete),sorted(contract['capture_completion_fields']))
eq(complete['status'],'CAPTURED_FOR_INDEPENDENT_REVIEW');eq(complete['phase'],'capture');eq(complete['first_error'],None);eq(complete['independent_tail_errors'],[])
eq(complete['command'],recipe['parent_command']);eq(complete['environment'],recipe['environment']);eq(complete['sources'],recipe['source_roles']);eq(complete['admission'],m.ref(D/'ADMIT_CAPTURE.json'))
assert 0<=complete['elapsed_seconds']<=900
for k in ['scientific_targets_executed','actual_data_admitted','full32_qualified','runtime_acceptance_created','genuine_outer_created']:eq(complete[k],False)
eq(complete['ret_paused'],True)
eq(sorted(complete['artifacts']),sorted(contract['capture_artifact_roles']))
for k,name in contract['capture_artifact_roles'].items():eq(complete['artifacts'][k],m.ref(O/name))
ns=m.load(O/'NAMESPACE.json');eq(ns['excluded_not_yet_written'],['NAMESPACE.json','COMPLETE.json']);eq(ns['root'],str(O))
eq(ns['entries'],[dict(relative=r['path'].split('/')[-1],kind='file',**m.pure(r)) for r in identities if r['path'].split('/')[-1] not in ns['excluded_not_yet_written']])
eq(m.load(O/'CHECKS.json'),dict(post_metadata='PASS',source_and_admission_postcheck='PASS'))
attempt=m.load(O/'ATTEMPT.json');eq(attempt,dict(schema='ri133-preparation-attempt-v1',admission=complete['admission'],sources=complete['sources'],phase='capture',environment=complete['environment'],scientific_execution=False))
baseline=contract['baseline'];m.verify(baseline['path'],baseline)
stats={}
for label in ['PRE','POST']:
 child=m.load(O/(label+'.COMPLETION.json'));a=m.load(O/(label+'.ATTEMPT.json'))
 eq(child['command'],recipe['snapshot_child_command']);eq(child['environment'],recipe['environment']);eq(child['wall_seconds'],180)
 for k in ['first_error','stop_reason']:eq(child[k],None)
 eq(child['tail_errors'],[]);eq(child['passed'],True);eq(child['child_exit_code'],0);eq(child['final_sample_gap_passed'],True)
 eq(sorted(a),sorted(['command','environment','wall_seconds','pid_owner','scientific_target_entry']))
 eq(a['command'],child['command']);eq(a['environment'],child['environment']);eq(a['wall_seconds'],180);eq(a['scientific_target_entry'],False);assert type(a['pid_owner']) is int and a['pid_owner']>0
 for stream in ['stdout','stderr']:eq(child[stream],m.ref(O/(label+'.'+stream)))
 eq(child['stderr']['bytes'],0)
 eq(m.pure(child['stdout']),m.pure(baseline));assert (O/(label+'.stdout')).read_bytes()==Path(baseline['path']).read_bytes()
 samples=child['samples'];mon=child['monitor_attempts'];assert samples and len(samples)==len(mon)
 previous=0
 for sample,obs in zip(samples,mon):
  eq(sorted(sample),['elapsed_seconds','gap_seconds','rss_kib']);eq(sorted(obs),['elapsed_seconds','returncode','stderr','stdout'])
  eq(obs['returncode'],0);eq(obs['stderr'],'');assert obs['stdout'].strip().isdigit()
  eq(sample['rss_kib'],int(obs['stdout'].strip()));eq(sample['elapsed_seconds'],obs['elapsed_seconds'])
  assert type(sample['rss_kib']) is int and 0<=sample['rss_kib']<=524288
  assert 0<=sample['gap_seconds']<=.1 and abs(sample['elapsed_seconds']-previous-sample['gap_seconds'])<1e-9
  previous=sample['elapsed_seconds']
 eq(child['peak_sampled_rss_kib'],max(x['rss_kib'] for x in samples))
 assert 0<=child['elapsed_seconds']<=180 and 0<=child['final_sample_to_reap_gap_seconds']<=.1
 assert abs(child['elapsed_seconds']-previous-child['final_sample_to_reap_gap_seconds'])<1e-9
 stats[label]=dict(elapsed=child['elapsed_seconds'],samples=len(samples),monitor_attempts=len(mon),max_sample_gap=max(x['gap_seconds'] for x in samples),final_gap=child['final_sample_to_reap_gap_seconds'],peak_rss_kib=child['peak_sampled_rss_kib'])
tools=m.load(R/'GENUINE_CAPTURE_TOOLS.json');args=tools['initial']['arguments']
for k,v in recipe['proposed_exec_command_arguments'].items():eq(args[k],v)
eq(shlex.split(args['cmd']),recipe['outer_argv']);eq(tools['initial']['result']['session_id'],14757);eq(len(tools['polls']),1)
eq(tools['polls'][0]['arguments']['session_id'],14757);eq(tools['polls'][0]['result']['exit_code'],0)
eq(tools['initial']['result']['output'],'');eq(tools['polls'][0]['result']['output'],'');eq(tools['single_attempt'],True)
supp=m.load(R/'BASELINE_AUTHENTICATION_SUPPLEMENT.json');eq(m.identity(supp['historical_E_baseline_identity']['path']),supp['historical_E_baseline_identity'])
eq(m.load(R/'PRE_E.json'),m.load(supp['historical_E_baseline_identity']['path']));eq(m.load(R/'POST_E.json'),m.load(R/'PRE_E.json'))
for phase in ['PRE','POST']:
 c=m.load(R/(phase+'_CUSTODY.json'));eq(c['status'],'PASS_FRESH_'+phase+'_CUSTODY')
 for r in c['refs'].values():m.verify(r['path'],r)
 for r in m.load(R/(phase+'_ROLE_CUSTODY.json'))['observed_identities']:eq(m.identity(r['path']),r)
for name,row in m.load(R/'ISSUED_CAPTURE_CONTROLS.json')['controls'].items():eq(m.identity(D/name),row)
for r in identities:eq(m.identity(r['path']),r)
eq(m.snapshot(),m.load(R/'REPO_ENTRY.json'))
record=dict(schema='ri239-root-actual-capture-check-v1',status='PASS_ACTUAL_CAPTURE_WHOLE_BASELINE_AND_CUSTODY',comparisons=n,artifacts=identities,monitor_statistics=stats,parent_elapsed=complete['elapsed_seconds'],genuine_tools=m.ref(R/'GENUINE_CAPTURE_TOOLS.json'),pre_custody=m.ref(R/'PRE_CUSTODY.json'),post_custody=m.ref(R/'POST_CUSTODY.json'),baseline=baseline,baseline_authentication=m.ref(R/'BASELINE_AUTHENTICATION_SUPPLEMENT.json'),limits_unchanged=recipe['bounds'],premises=['Apple supplier/startup and loader/cache remain external observed-window premises','RSS observes owned child only; no-descendant premise; samples are not hard OS quotas','ps50ms enforced by unchanged collector; raw attempts do not independently timestamp each subprocess start','Genuine outer960sec remains enforced by exact Perl alarm through final metadata writes'],scientific_execution=False,E_unchanged=True,repository_unchanged=True,scope='Metadata capture only; not scientific qualification or actual-data admission',checker=m.ref(Path(__file__).resolve()))
print(json.dumps(dict(record=m.save('ROOT_CAPTURE_CHECK.json',record),comparisons=n,monitor_statistics=stats)))
