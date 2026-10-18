"""Independent root administrative result reconstruction; no subject execution."""
from pathlib import Path
import hashlib,importlib.util,math,shlex
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri249-root-premode-operation-hcybjv4k';D=B/'ri244-current-normal-premode-2kfsmiea';O=B/'ri156-operation-ri244-premode-2kfsmiea';Q=B/'ri248-native-canonical-companion-of3isoc8'
p=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=p.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7';sp=importlib.util.spec_from_file_location('meta',p);m=importlib.util.module_from_spec(sp);exec(compile(raw,str(p),'exec'),m.__dict__);m.D=R
seen={}
def verify(row):
 v=m.identity(row['path']);assert all(v[k]==x for k,x in row.items()),row['path'];assert not v['symlink_chain'] and v['resolved_path']==v['path'];seen[v['path']]=v;return v
def read(p):
 verify(m.ref(p));return m.load(p)
card=read(D/'ADMIT_PRE_MODE.json');request=read(card['request']['path']);runtime=read(request['actual_runtime']['path']);manifest=read(card['source_manifest']['path']);completion=read(O/'COMPLETE.json');result=read(O/'RESULT.json');attempt=read(O/'ATTEMPT.json')
assert set(x.name for x in O.iterdir())=={'ATTEMPT.json','RESULT.json','COMPLETE.json'}
expected=dict(schema='ri130-root-pre-mode-runtime-custody-v1',mode='normal',freeze=m.pure(request['freeze']),runtime_acceptance=runtime['runtime_acceptance'],selection_unchanged=True,optional_namespaces_unchanged=True,host_identity_unchanged=True,observed_dyld_routes=runtime['observed_dyld_routes'],metadata_record=request['actual_runtime'])
assert result==expected and len(result)==9
assert attempt==dict(action='pre_mode',admission=m.ref(D/'ADMIT_PRE_MODE.json'),no_retry=True,schema='ri156-exclusive-metadata-attempt-v1',scientific_execution=False)
assert len(completion)==14 and completion['schema']=='ri156-adapter-completion-v1' and completion['status']=='COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW' and completion['action']=='pre_mode'
assert completion['admission']==m.ref(D/'ADMIT_PRE_MODE.json') and completion['first_error'] is None and completion['scientific_execution'] is False and completion['root_acceptance_created'] is False and completion['ret_paused'] is True
assert 0<=completion['elapsed_seconds_before_complete_write']<=180
pins={n:m.ref(O/n) for n in ['ATTEMPT.json','RESULT.json']}
assert completion['produced_output_pins']==pins and completion['artifacts']==dict(attempt=pins['ATTEMPT.json'],result=pins['RESULT.json'])
tails=completion['independent_tails'];assert set(tails)=={'sources','admission','request','dependencies','output:ATTEMPT.json','output:RESULT.json','namespace'} and all(x['error'] is None and set(x)=={'error','value'} for x in tails.values())
sources={**manifest['modules'],'adapter':manifest['adapter'],'manifest':card['source_manifest']};assert set(sources)==set(completion['authenticated_source_before']) and len(sources)==13
for k,pin in sources.items():
 v=verify(pin);row=completion['authenticated_source_before'][k];assert all(v[a]==b for a,b in row.items())
assert tails['sources']['value']==completion['authenticated_source_before']==completion['tail_observations']['sources']
assert tails['admission']['value']==m.ref(D/'ADMIT_PRE_MODE.json') and tails['request']['value']==card['request'] and tails['dependencies']['value']==manifest['dependencies'] and len(manifest['dependencies'])==567
for row in manifest['dependencies']:verify(row)
tree=[dict(kind='directory',relative='.')]+[dict(kind='file',relative=n,**m.pure(pins[n])) for n in sorted(pins)]
for n in pins:assert tails['output:'+n]['value']==pins[n]
assert tails['namespace']['value']==tree and completion['tail_observations']==dict(namespace=tree,namespace_fixture_mismatches=[],namespace_member_mismatches=[],namespace_output_mismatches=[],outputs=pins,sources=completion['authenticated_source_before'])
M=D/'monitor';assert set(x.name for x in M.iterdir())=={'PRE_MODE.ATTEMPT.json','PRE_MODE.COMPLETION.json','PRE_MODE.stdout','PRE_MODE.stderr'}
mc=read(M/'PRE_MODE.COMPLETION.json');ma=read(M/'PRE_MODE.ATTEMPT.json');command=['/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9','-I','-B',manifest['adapter']['path'],'--admission',str(D/'ADMIT_PRE_MODE.json')]
assert set(ma)=={'command','environment','pid_owner','scientific_target_entry','wall_seconds'} and ma['command']==command and ma['environment']==card['environment'] and ma['wall_seconds']==180 and type(ma['pid_owner']) is int and ma['pid_owner']>0 and ma['scientific_target_entry'] is False
assert set(mc)=={'child_exit_code','command','elapsed_seconds','environment','final_sample_gap_passed','final_sample_to_reap_gap_seconds','first_error','monitor_attempts','passed','peak_sampled_rss_kib','samples','stderr','stdout','stop_reason','tail_errors','wall_seconds'}
assert mc['command']==command and mc['environment']==card['environment'] and mc['wall_seconds']==180 and mc['passed'] is True and mc['child_exit_code']==0 and mc['first_error'] is None and mc['stop_reason'] is None and mc['tail_errors']==[]
assert 0<mc['elapsed_seconds']<=180 and mc['final_sample_gap_passed'] is True
samples=mc['samples'];attempts=mc['monitor_attempts'];assert len(samples)==len(attempts)>0
last=0
for sample,obs in zip(samples,attempts):
 assert set(sample)=={'elapsed_seconds','gap_seconds','rss_kib'} and set(obs)=={'elapsed_seconds','returncode','stderr','stdout'}
 assert obs['returncode']==0 and obs['stderr']=='' and obs['stdout'].strip().isdigit() and sample['elapsed_seconds']==obs['elapsed_seconds'] and sample['rss_kib']==int(obs['stdout'].strip())
 assert math.isfinite(sample['elapsed_seconds']) and 0<sample['elapsed_seconds']-last<=.1 and abs(sample['gap_seconds']-(sample['elapsed_seconds']-last))<1e-9 and 0<=sample['rss_kib']<=524288
 last=sample['elapsed_seconds']
assert mc['peak_sampled_rss_kib']==max(x['rss_kib'] for x in samples)
gap=mc['elapsed_seconds']-last;assert 0<=gap<=.1 and abs(gap-mc['final_sample_to_reap_gap_seconds'])<1e-9
for name in ['stdout','stderr']:assert mc[name]==m.ref(M/('PRE_MODE.'+name)) and verify(mc[name])['bytes']==0
genuine=read(R/'GENUINE_OPERATION_TOOLS.json')['operation'];tokens=shlex.split(genuine['arguments']['cmd']);env=[k+'='+v for k,v in sorted(card['environment'].items())]
assert tokens==['/usr/bin/env','-i',*env,'/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',command[0],'-I','-B',str(D/'PRE_MODE_BOOTSTRAP.proposal.py')]
assert genuine['arguments']['workdir']==str(D) and genuine['arguments']['login'] is False and genuine['result']['session_id']==78888 and genuine['result']['output']==''
assert len(genuine['polls'])==1 and genuine['polls'][0]['arguments']['session_id']==78888 and genuine['polls'][0]['result']['exit_code']==0 and genuine['polls'][0]['result']['output']==''
post=read(R/'POSTFLIGHT.json');assert post['phase']=='postflight' and post['status']=='PASS_METADATA_CUSTODY' and post['E_unchanged'] is True and post['immutable_preparation_input_rows']==2854
for name,row in post['controls'].items():verify(row)
for row in list(seen.values()):assert m.identity(row['path'])==row
print(m.save('ROOT_PRE_MODE_OUTCOME_CHECK.json',dict(status='PASS_COMPLETE_METADATA_OPERATION_RECONSTRUCTION',full_result=result,adapter_tails=7,dependencies=567,source_objects=13,output_identities=[m.identity(p) for p in sorted(O.iterdir())],monitor_identities=[m.identity(p) for p in sorted(M.iterdir())],samples=len(samples),raw_attempts=len(attempts),peak_sampled_rss_kib=mc['peak_sampled_rss_kib'],elapsed_seconds=mc['elapsed_seconds'],maximum_sample_gap_seconds=max(x['gap_seconds'] for x in samples),final_sample_to_reap_gap_seconds=gap,whole_postflight=m.ref(R/'POSTFLIGHT.json'),genuine_tools=m.ref(R/'GENUINE_OPERATION_TOOLS.json'),reviewed_identities=len(seen),sampled_child_not_group_quota=True,parent_pid_not_child_identity=True,stable_host_supplier_and_no_descendant_premises_retained=True,loader_cache_closure_not_proved=True,scientific_execution=False,mode_card_created=False,RET_paused=True)))
