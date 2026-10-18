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
q=m.load(P/'PREFLIGHT_PROPOSAL.json');c=m.load(P/'COMMAND_PROPOSALS.json')['commands']['capture']
R=Path(q['paths_proposed_not_created']['root_records']);E=Path(q['next_runtime_stage']['environment_root']);out=Path(c['output_proposal'])
copy=m.load(R/'ACTUAL_COPY_ROOT_REVIEW.json')
assert copy['status']=='ACCEPT_ONE_EXACT_METADATA_COPY_ONLY' and copy['copied_files']==48 and copy['all_ten_independent_tails_passed'] is True
assert copy['copy_root']==str(E)
sources={}
def keep(row):
    now=m.verify(row['path'],row)
    if row['path'] in sources:assert sources[row['path']]==now
    sources[row['path']]=now
for row in m.load(R/'SOURCES_BEFORE.json')['sources']:keep(row)
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
for row in list(sources.values())+copies+vendor+tools:assert m.identity(row['path'])==row
observation=dict(sources=list(sources.values()),copies=copies,E=str(E),directories=dirs,files=files,vendor=vendor,vendor_namespace=old['namespace'],tools=tools,absent=old['absent'],host=old['host'],selected_interpreter_binding=selected,environment=c['exact_environment'],scientific_decode=False,subject_execution=False)
if phase=='POST':
    assert observation==m.load(D/'CAPTURE_PREFLIGHT_OBSERVATION.json')
    card=m.load(D/'CAPTURE_ADMISSION_CUSTODY.json')
    for key in ('admission','source_review','preflight'):assert m.identity(card[key]['path'])==card[key]
    print(m.save('CAPTURE_POST_CUSTODY.json',dict(observation=observation,admission_and_source_review_unchanged=True,observed_at_unix_ns=time.time_ns())))
else:
    assert not os.path.lexists(out) and not os.path.lexists(R/'ADMIT_CAPTURE.json')
    observation_ref=m.save('CAPTURE_PREFLIGHT_OBSERVATION.json',observation)
    preflight=m.save('CAPTURE_PREFLIGHT.json',dict(schema='ri183-current-e-capture-preflight-v1',selected_interpreter_binding=selected,observation=observation_ref,copy_acceptance=m.ref(R/'ACTUAL_COPY_ROOT_REVIEW.json'),proposal_acceptance=m.ref(B/'ri172-root-review-fkjv3v0z/RI170_ROOT_ADJUDICATION.json'),platform_premises=m.load(R/'BOOTSTRAP_PREFLIGHT.json')['platform_premises'],scope='Fresh full opaque vendor, tools, host, original source and exact E48 custody for one nonscientific current-E capture. Stable host/supplier and Apple kernel/loader remain explicit premises; no continuous filesystem freeze or instruction trace is claimed.'))
    decision=m.save('CAPTURE_SOURCE_ADJUDICATION.json',dict(schema='ri183-current-e-capture-adjudication-v1',status='ACCEPT_EXACT_SOURCE_FOR_ONE_NONSCIENTIFIC_CAPTURE',source=q['source_bindings']['ri141_source_handoff'],source_review=q['source_bindings']['ri141_source_adjudication'],prior_actual_capture=q['source_bindings']['ri146_capture_actual'],copy_acceptance=m.ref(R/'ACTUAL_COPY_ROOT_REVIEW.json'),fresh_preflight=preflight,scope='One capture parent and two PRE/POST metadata children under unchanged180/524288KiB/25ms/100ms/50ms and genuine960s outer bounds. Original RI130 snapshot source fields remain unchanged; E has separate before/after custody. No candidate interpreter/profile/guard/science entry. All four predecessor fields null.',runtime_acceptance_created=False,independent_postreview_required=True,ret_paused=True))
    card=dict(schema='ri141-root-preparation-admission-v1',status='AUTHORIZE_ONE_NONSCIENTIFIC_PREPARATION',phase='capture',sources={n:m.pure(m.ref(S/n)) for n in ('prepare.py','runtime_metadata.py','DEPENDENCIES.source-only.json')},source_review=decision,packet=str(B/'ri130-white-qualification-caller-source-Q4Aq7hZg'),output=str(out),environment_root=str(E),bootstrap=dict(named_path=selected['path'],resolved_path=selected['resolved_path'],symlink_chain=selected['symlink_chain'],target=m.pure(selected)),bootstrap_host_preflight=preflight,host=dict(uname=list(os.uname()),system_version=m.ref('/System/Library/CoreServices/SystemVersion.plist')),baseline_acceptance=None,normal_acceptance=None,profiles_acceptance=None,guard_admission=None,bounds=dict(snapshot_seconds=180,profile_seconds=30,guard_seconds=180,rss_kib=524288,target_poll_seconds=0.025,maximum_sample_gap_seconds=0.1,ps_timeout_seconds=0.05,file_bytes=67108864,driver_soft_seconds=900,genuine_outer_timeout_seconds=960),genuine_outer_required=True)
    admission=m.save(R/'ADMIT_CAPTURE.json',card)
    print(m.save('CAPTURE_ADMISSION_CUSTODY.json',dict(admission=m.identity(admission['path']),source_review=m.identity(decision['path']),preflight=m.identity(preflight['path']))))
    assert c['shell_command']==shlex.join(c['outer_argv']) and c['cwd']==str(R) and c['login'] is False
    print(m.save('CAPTURE_DISPATCH.json',dict(exec_command=dict(cmd=c['shell_command'],workdir=str(R),login=False,yield_time_ms=1000,max_output_tokens=2000),command_proposal=m.ref(P/'COMMAND_PROPOSALS.json'),admission=admission,environment=c['exact_environment'],outer_argv=c['outer_argv'],single_attempt=True)))
    print('READY_FOR_ONE_CURRENT_E_CAPTURE_ONLY')
