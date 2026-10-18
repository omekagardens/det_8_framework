"""Root fresh metadata-only preflight/admission for the already installed E."""
from pathlib import Path
import hashlib, importlib.util, os, shlex, stat, subprocess, sys, time
D=Path(__file__).parent;B=D.parent
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=hp.read_bytes()
assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=D
phase=sys.argv[1];assert phase in ('PRE','POST')
P=B/'ri170-measurement-current-e-preflight-gikj2giy';S=B/'ri141-white-bootstrap-source-h58ls076'
m.verify(P/'PREFLIGHT_PROPOSAL.json',dict(bytes=13152,sha256='483b9862e18959646cc0518daf8a21b6b2f4d5240f59416a2829fe7474566585'))
m.verify(P/'COMMAND_PROPOSALS.json',dict(bytes=22588,sha256='7ea3f44ceb02a4532dfc32554cff418f60b2dfd468641876212f50bf7d29a9ad'))
q=m.load(P/'PREFLIGHT_PROPOSAL.json');c=m.load(P/'COMMAND_PROPOSALS.json')['commands']['profile_optimized']
R=Path(q['paths_proposed_not_created']['root_records']);E=Path(q['next_runtime_stage']['environment_root']);out=Path(c['output_proposal'])
baseline_ref=m.verify(R/'BASELINE_ACCEPTANCE.json',dict(bytes=1657,sha256='75d30bdc2d03621867ce5a64c229eb619b6183f29b6434dbc04b4a2792e5e06e'))
baseline_ref=m.ref(R/'BASELINE_ACCEPTANCE.json')
normal_root=B/'ri188-root-endpoint-profile-review-1jg_i948'
normal_ref=m.ref(R/'NORMAL_ACCEPTANCE.json')
assert m.pure(normal_ref)==dict(bytes=1680,sha256='5470ddd468cba8a5168042ceb73d1ce5204971233f3b26ecbbe657d617da95d2')
normal=m.load(normal_ref['path'])
assert normal['stage']=='normal' and normal['status']=='ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE' and normal['scientific_execution'] is False
assert normal['environment_root']==str(E)
m.verify(normal_root/'RI190_ROOT_ADJUDICATION.json',dict(bytes=2745,sha256='de11a7189504ff777f3145c8566d4e10ae0cb455d5eba2bc9aead327661fc576'))
baseline=m.load(baseline_ref['path'])
assert baseline['status']=='ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE' and baseline['stage']=='baseline'
assert baseline['scientific_execution'] is False and baseline['environment_root']==str(E)
old_root=B/'ri183-root-parent-capture-review-2mnanskj'
m.verify(old_root/'RI186_ROOT_ADJUDICATION.json',dict(bytes=2455,sha256='ac8ffe54952e49ad9534c4b8da612e8c2371213ff32d1232244a133a2492e4ef'))
copy=m.load(R/'ACTUAL_COPY_ROOT_REVIEW.json')
assert copy['status']=='ACCEPT_ONE_EXACT_METADATA_COPY_ONLY' and copy['copied_files']==48 and copy['all_ten_independent_tails_passed'] is True
assert copy['copy_root']==str(E)
sources={}
def keep(row):
    now=m.verify(row['path'],row)
    if row['path'] in sources:assert sources[row['path']]==now
    sources[row['path']]=now
for row in m.load(R/'SOURCES_BEFORE.json')['sources']:keep(row)
keep(baseline_ref);keep(m.ref(old_root/'RI186_ROOT_ADJUDICATION.json'))
keep(normal_ref);keep(m.ref(normal_root/'RI190_ROOT_ADJUDICATION.json'));keep(normal['independent_review'])
for group in ('completions','genuine_outer'):
    for row in normal[group].values():keep(row)
m.verify(normal_root/'OPERATION_FINAL_IDENTITIES.json',dict(bytes=12102,sha256='861957727359066a538f3a3e67304b26408c4f1797131b9b11e280e99a031298'))
keep(m.ref(normal_root/'OPERATION_FINAL_IDENTITIES.json'))
normal_inventory=m.load(normal_root/'OPERATION_FINAL_IDENTITIES.json')
for row in normal_inventory['identities']:
    assert m.identity(row['path'])==row;keep(row)
assert len(normal_inventory['identities'])==16
assert {x.name for x in Path(normal_inventory['root']).iterdir()}=={Path(x['path']).name for x in normal_inventory['identities']}
assert normal['sources']==baseline['sources'] and normal['packet']==baseline['packet']
keep(baseline['independent_review'])
for group in ('completions','genuine_outer'):
    for row in baseline[group].values():keep(row)
complete=m.load(baseline['completions']['capture']['path'])
assert complete['status']=='CAPTURED_FOR_INDEPENDENT_REVIEW' and complete['first_error'] is None and complete['independent_tail_errors']==[]
for row in complete['artifacts'].values():keep(row)
base_post=m.load(complete['artifacts']['POST']['path'])
assert base_post['scientific_execution'] is False
runtime=[]
for row in base_post['runtime_inventory']['files']:runtime.append(m.verify(row['path'],row))
assert len(runtime)==9923 and sum(r['bytes'] for r in runtime)==258862951

for key in ('complete','result','genuine_tool','monitor','preflight','sources_before','runtime_before'):keep(copy[key])
keep(m.ref(R/'ACTUAL_COPY_ROOT_REVIEW.json'))
for row in q['source_bindings'].values():keep(row)
h=m.load(S/'HANDOFF.json');assert sorted(x.name for x in S.iterdir())==sorted(h['exact_namespace'])
keep(m.ref(S/'HANDOFF.json'))
for row in h['files']:keep(row)
deps=m.load(S/'DEPENDENCIES.source-only.json')
for row in deps['opaque_files']:keep(row)
selected=m.identity(deps['selected_bootstrap_binding']['path']);assert selected==deps['selected_bootstrap_binding']
graph=m.load(q['source_bindings']['binding_graph']['path']);assert graph['prospective_root']==str(E)
copies=[]
for row in graph['copied_files']:
    keep(row['source']);actual=m.verify(row['destination'],row['source']);copies.append(actual)
    assert Path(row['destination'])==E/row['relative'] and Path(row['source']['path']).read_bytes()==Path(row['destination']).read_bytes()
expected_dirs={'science','science/validator','science/qualifier','science/primary','tmp','runs','runs/normal','runs/optimized'}
dirs=[];files=[]
for path in sorted(E.rglob('*')):
    mode=path.lstat().st_mode;assert not stat.S_ISLNK(mode)
    if stat.S_ISDIR(mode):dirs.append(path.relative_to(E).as_posix())
    else:assert stat.S_ISREG(mode);files.append(path.relative_to(E).as_posix())
assert set(dirs)==expected_dirs and set(files)=={r['relative'] for r in graph['copied_files']} and len(files)==48
for name in ('tmp','runs/normal','runs/optimized'):assert not list((E/name).iterdir())
old=m.load(R/'RUNTIME_BEFORE.json');vendor=[]
for row in old['vendor']:
    now=m.identity(row['path']);assert now==row;vendor.append(now)
assert len(vendor)==1810
state=lambda st:[st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]
for row in old['namespace']:
    path=Path(row['path']);before=state(path.lstat());assert before==row['state']
    if row['kind']=='directory':assert sorted(x.name for x in path.iterdir())==row['entries']
    else:assert path.is_symlink() and os.readlink(path)==row['target']
    assert state(path.lstat())==before
assert all(not os.path.lexists(p) for p in old['absent'])
tools=[m.identity(r['path']) for r in old['tools']];assert tools==old['tools']
host=subprocess.run(['/usr/bin/sw_vers'],capture_output=True,timeout=5,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
assert host.returncode==0 and host.stderr==b'' and host.stdout.decode()==old['host']['stdout'] and list(os.uname())==old['host']['uname']
for row in list(sources.values())+copies+vendor+tools+runtime:assert m.identity(row['path'])==row
observation=dict(accepted_baseline=baseline_ref,accepted_normal=normal_ref,runtime=runtime,sources=list(sources.values()),copies=copies,E=str(E),directories=dirs,files=files,vendor=vendor,vendor_namespace=old['namespace'],tools=tools,absent=old['absent'],host=old['host'],selected_interpreter_binding=selected,environment=c['exact_environment'],scientific_decode=False,subject_execution=False)
if phase=='POST':
    assert observation==m.load(D/'PROFILE_OPTIMIZED_PREFLIGHT_OBSERVATION.json')
    card=m.load(D/'PROFILE_OPTIMIZED_ADMISSION_CUSTODY.json')
    for key in ('admission','source_review','preflight'):assert m.identity(card[key]['path'])==card[key]
    print(m.save('PROFILE_OPTIMIZED_POST_CUSTODY.json',dict(observation=observation,admission_and_source_review_unchanged=True,observed_at_unix_ns=time.time_ns())))
else:
    assert not os.path.lexists(out) and not os.path.lexists(R/'ADMIT_PROFILE_OPTIMIZED.json')
    observation_ref=m.save('PROFILE_OPTIMIZED_PREFLIGHT_OBSERVATION.json',observation)
    preflight=m.save('PROFILE_OPTIMIZED_PREFLIGHT.json',dict(schema='ri192-current-e-optimized-profile-preflight-v1',selected_interpreter_binding=selected,observation=observation_ref,copy_acceptance=m.ref(R/'ACTUAL_COPY_ROOT_REVIEW.json'),proposal_acceptance=m.ref(B/'ri172-root-review-fkjv3v0z/RI170_ROOT_ADJUDICATION.json'),platform_premises=m.load(R/'BOOTSTRAP_PREFLIGHT.json')['platform_premises'],scope='Fresh full opaque 9923-file candidate runtime, vendor, tools, host, original sources, accepted baseline and exact E48 custody for one nonscientific optimized profile. The accepted parent must match full baseline PRE before entering the profile child. Stable host/supplier and Apple kernel/loader remain explicit premises; no continuous filesystem freeze or instruction trace is claimed.'))
    decision=m.save('PROFILE_OPTIMIZED_SOURCE_ADJUDICATION.json',dict(schema='ri192-current-e-optimized-profile-adjudication-v1',status='ACCEPT_EXACT_SOURCE_FOR_ONE_NONSCIENTIFIC_OPTIMIZED_PROFILE',source=q['source_bindings']['ri141_source_handoff'],source_review=q['source_bindings']['ri141_source_adjudication'],prior_actual_capture=q['source_bindings']['ri146_capture_actual'],copy_acceptance=m.ref(R/'ACTUAL_COPY_ROOT_REVIEW.json'),fresh_preflight=preflight,scope='One optimized-profile parent, PRE/POST metadata children and one selected optimized candidate-interpreter profile child. Snapshot180/profile30/524288KiB/25ms/100ms/50ms/genuine960s bounds remain unchanged. Original RI130 fields and separate E custody remain. Baseline and normal stage are independently accepted; profiles/guard predecessors remain null. Complete profile relation differs only by optimize flag; each full module/cache report is separately retained. No scientific target, guards or data analysis. Actual output requires independent review before both-mode acceptance or any guards.',runtime_acceptance_created=False,independent_postreview_required=True,ret_paused=True))
    card=dict(schema='ri141-root-preparation-admission-v1',status='AUTHORIZE_ONE_NONSCIENTIFIC_PREPARATION',phase='profile_optimized',sources={n:m.pure(m.ref(S/n)) for n in ('prepare.py','runtime_metadata.py','DEPENDENCIES.source-only.json')},source_review=decision,packet=str(B/'ri130-white-qualification-caller-source-Q4Aq7hZg'),output=str(out),environment_root=str(E),bootstrap=dict(named_path=selected['path'],resolved_path=selected['resolved_path'],symlink_chain=selected['symlink_chain'],target=m.pure(selected)),bootstrap_host_preflight=preflight,host=dict(uname=list(os.uname()),system_version=m.ref('/System/Library/CoreServices/SystemVersion.plist')),baseline_acceptance=baseline_ref,normal_acceptance=normal_ref,profiles_acceptance=None,guard_admission=None,bounds=dict(snapshot_seconds=180,profile_seconds=30,guard_seconds=180,rss_kib=524288,target_poll_seconds=0.025,maximum_sample_gap_seconds=0.1,ps_timeout_seconds=0.05,file_bytes=67108864,driver_soft_seconds=900,genuine_outer_timeout_seconds=960),genuine_outer_required=True)
    admission=m.save(R/'ADMIT_PROFILE_OPTIMIZED.json',card)
    print(m.save('PROFILE_OPTIMIZED_ADMISSION_CUSTODY.json',dict(admission=m.identity(admission['path']),source_review=m.identity(decision['path']),preflight=m.identity(preflight['path']))))
    assert c['shell_command']==shlex.join(c['outer_argv']) and c['cwd']==str(R) and c['login'] is False
    print(m.save('PROFILE_OPTIMIZED_DISPATCH.json',dict(exec_command=dict(cmd=c['shell_command'],workdir=str(R),login=False,yield_time_ms=1000,max_output_tokens=2000),command_proposal=m.ref(P/'COMMAND_PROPOSALS.json'),admission=admission,environment=c['exact_environment'],outer_argv=c['outer_argv'],single_attempt=True)))
    print('READY_FOR_ONE_CURRENT_E_OPTIMIZED_PROFILE_ONLY')
