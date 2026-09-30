"""Fresh root preparation for one reviewed metadata copy; no subject invocation."""
import hashlib, importlib.util, os, shlex, subprocess, time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=Path(__file__).parent
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=D
S=B/'ri170-measurement-current-e-preflight-gikj2giy';P=B/'ri172-root-review-fkjv3v0z'
m.verify(S/'SOURCE_ONLY_HANDOFF.json',dict(bytes=8755,sha256='8d3cfce3b18ac346a0dab3449de3eee686c5965957e4188933604dd392d66fce'))
q=m.load(S/'PREFLIGHT_PROPOSAL.json');c=m.load(S/'COMMAND_PROPOSALS.json')['commands']['copy']
m.verify(S/'PREFLIGHT_PROPOSAL.json',dict(bytes=13152,sha256='483b9862e18959646cc0518daf8a21b6b2f4d5240f59416a2829fe7474566585'))
m.verify(S/'COMMAND_PROPOSALS.json',dict(bytes=22588,sha256='7ea3f44ceb02a4532dfc32554cff418f60b2dfd468641876212f50bf7d29a9ad'))
paths=q['paths_proposed_not_created'];assert len(paths)==8 and all(not os.path.lexists(p) for p in paths.values())
sources=[m.verify(r['path'],r) for r in q['source_bindings'].values()]
source=m.load(q['source_bindings']['source_manifest']['path'])
sources.extend(m.verify(r['path'],r) for r in [source['adapter'],*source['modules'].values(),*source['dependencies']])
qualification=m.load(P/'RI162_CONSUMER_QUALIFICATION.json')
assert qualification['schema']=='ri156-root-inert-controls-review-v1' and qualification['status']=='ACCEPT_EXACT_INERT_ADAPTER_CONTROLS'
assert qualification['source_manifest']==q['source_bindings']['source_manifest'] and qualification['all_passed'] is True and qualification['scientific_execution'] is False and len(qualification['controls'])==106
for name in ('report','genuine_outer','independent_review'):sources.append(m.verify(qualification[name]['path'],qualification[name]))
for name in ('RI170_ROOT_ADJUDICATION.json','RI162_CONSUMER_QUALIFICATION.json','RI170_CONSUMER_INTERFACE_CHECK.json'):
 sources.append(m.identity(P/name))
assert m.load(P/'RI170_ROOT_ADJUDICATION.json')['status']=='ACCEPT_SOURCE_PROPOSAL_WITH_EXPLICIT_FIELD_COUNT_CORRECTION'
graph=m.load(q['source_bindings']['binding_graph']['path'])
assert graph['prospective_root']==paths['current_E'] and len(graph['copied_files'])==48 and len(graph['sources'])==30 and len(graph['helpers'])==11 and len(graph['history_originals'])==124
for row in graph['copied_files']:sources.append(m.verify(row['source']['path'],row['source']))
for row in graph['history_originals']:sources.append(m.verify(row['path'],row))
for row in graph['sources']:sources.append(m.verify(row['original'],row['pin']))
oldpath=B/'ri163-root-preflight-review-u80slv0b/NATIVE_METADATA_CHECK.json'
m.verify(oldpath,dict(bytes=1443183,sha256='e9400ffb11b976fe80070a87fe5d4fe3e2feb86adb3fea9beeb868ee3bb9a757'));old=m.load(oldpath)
prefix='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9';vendor=[]
for row in old['fresh_identities']:
 if row['path'].startswith(prefix+'/'):
  now=m.identity(row['path']);assert now==row;vendor.append(now)
assert len(vendor)==1810 and sum(r['bytes'] for r in vendor)==48024515
state=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
namespace=[]
for row in old['namespace']:
 p=Path(row['path']);before=p.lstat();assert state(before)==row['state']
 if row['kind']=='directory':assert sorted(x.name for x in p.iterdir())==row['entries']
 else:assert p.is_symlink() and os.readlink(p)==row['target']
 assert state(p.lstat())==state(before);namespace.append(row)
assert len(namespace)==195
absence=[prefix+'/lib/python39.zip','/Library/Python'];assert all(not os.path.lexists(p) for p in absence)
tools=[m.identity(p) for p in ('/usr/bin/env','/usr/bin/perl','/bin/ps','/usr/bin/sw_vers')]
assert all(r['resolved_path']==r['path'] and r['symlink_chain']==[] for r in tools)
host=subprocess.run(['/usr/bin/sw_vers'],capture_output=True,timeout=5,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
assert host.returncode==0 and host.stderr==b'' and host.stdout==b'ProductName:\t\tmacOS\nProductVersion:\t\t26.5.2\nBuildVersion:\t\t25F84\n'
selected=m.identity(source['bootstrap_binding']['path']);assert selected==source['bootstrap_binding']
for r in sources+vendor+tools:assert m.identity(r['path'])==r
assert all(not os.path.lexists(p) for p in paths.values())
R=Path(paths['root_records']);R.mkdir(mode=0o700);Path(paths['copy_environment']).mkdir(mode=0o700)
Path(c['exact_environment']['TMPDIR']).mkdir(mode=0o700);Path(paths['copy_monitor']).mkdir(mode=0o700);m.D=R
print(m.save('SOURCES_BEFORE.json',dict(sources=sources,source_manifest=q['source_bindings']['source_manifest'],proposal=m.ref(S/'PREFLIGHT_PROPOSAL.json'))))
runtime=m.save('RUNTIME_BEFORE.json',dict(vendor=vendor,namespace=namespace,absent=absence,tools=tools,host=dict(argv=['/usr/bin/sw_vers'],exit_code=host.returncode,stdout=host.stdout.decode(),stderr=host.stderr.decode(),uname=list(os.uname())),environment=c['exact_environment'],observed_at_unix_ns=time.time_ns()))
static=B/'ri164-root-static-review-xr1qffz8/RI164_ROOT_ADJUDICATION.json'
pre=dict(schema='ri174-root-genuine-copy-preflight-v1',status='FRESH_SOURCE_VENDOR_HOST_CHECKED_FOR_ONE_METADATA_COPY',selected_interpreter_binding=selected,source_observation=m.ref(R/'SOURCES_BEFORE.json'),runtime_observation=runtime,static_native_adjudication=m.ref(static),platform_premises=m.load(static)['platform_premises_accepted'],operation_premises=['Unchanged reviewed isolated vendor/stdlib and adapter sources do not introduce undeclared dynamic suppliers or child descendants; explicit source/platform assumptions, not runtime closure proofs.','Root retains before/after hashes, source/card bytes and exact environment. Read-window stability is not an enforced global filesystem freeze.','Fixed 960s outer alarm and reviewed 180s child monitor are operational controls, not continuous/group RSS enforcement. Any missed100ms sampling gap, absent samples, output overflow or genuine nonzero exit refuses this attempt.'],source_acceptance=q['source_bindings']['source_adjudication'],proposal_acceptance=m.ref(P/'RI170_ROOT_ADJUDICATION.json'),scientific_execution_authorized=False,prepared_at_unix_ns=time.time_ns())
print(m.save('BOOTSTRAP_PREFLIGHT.json',pre))
authority=m.save('COPY_AUTHORITY.json',dict(schema='ri156-root-copy-admission-v1',status='AUTHORIZE_ONE_EXACT_SOURCE_COPY_ONLY',graph=q['source_bindings']['binding_graph'],root=paths['current_E'],source_review=q['source_bindings']['relocation_adjudication']))
request=m.save('COPY_REQUEST.json',dict(copy_admission=authority));print(authority);print(request)
card=dict(schema='ri156-root-adapter-admission-v1',status='AUTHORIZE_ONE_BOUNDED_METADATA_ACTION',action='copy',source_manifest=q['source_bindings']['source_manifest'],source_review=q['source_bindings']['source_adjudication'],qualification=m.ref(P/'RI162_CONSUMER_QUALIFICATION.json'),request=request,output=paths['copy_operation'],environment=c['exact_environment'],bootstrap_preflight=m.ref(R/'BOOTSTRAP_PREFLIGHT.json'),bounds=dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=0.025,maximum_sample_gap_seconds=0.1,ps_timeout_seconds=0.05,file_bytes=67108864),genuine_outer_required=True)
assert len(card)==12
print(m.save('ADMIT_COPY_ADAPTER.json',card))
assert c['shell_command']==shlex.join(c['outer_argv']) and c['cwd']==str(R)
print(m.save('DISPATCH.json',dict(exec_command=dict(cmd=c['shell_command'],workdir=str(R),login=False,yield_time_ms=1000,max_output_tokens=2000),admission=m.ref(R/'ADMIT_COPY_ADAPTER.json'),request=request,preflight=m.ref(R/'BOOTSTRAP_PREFLIGHT.json'),copy_authority=authority,command_proposal=m.ref(S/'COMMAND_PROPOSALS.json'),single_attempt=True,actual_execution_not_yet_started=True)))
print('READY_FOR_ONE_GENUINE_METADATA_COPY_INVOCATION')
