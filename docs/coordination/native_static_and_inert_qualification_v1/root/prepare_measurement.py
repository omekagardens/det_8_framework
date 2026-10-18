"""Root fresh source/runtime preflight and one-shot inert measurement admission."""
import hashlib,importlib.util,json,os,stat,subprocess,time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=Path(__file__).parent
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
S=B/'ri162-inert-qualification-preflight-wb69vu5s';m.verify(S/'HANDOFF.json',dict(bytes=8931,sha256='97b16e9424e415dc03d3ff654785ea3bfb691964dbfa7c4c1e1a26db3e1207bf'))
h=m.load(S/'HANDOFF.json')
for r in h['payloads']:m.verify(r['path'],r)
q=m.load(S/'QUALIFICATION_PROPOSAL.json');paths=q['operation_paths_not_created'];assert all(not os.path.lexists(p) for p in paths.values())
source=m.load(q['adapter_admission_field_proposal']['source_manifest']['path'])
sources=[m.verify(r['path'],r) for r in source['dependencies']]
for r in [source['adapter'],*source['modules'].values(),q['monitor_source'],q['monitor_source_acceptance'],q['source_root_acceptance']]:sources.append(m.verify(r['path'],r))
oldpath=B/'ri163-root-preflight-review-u80slv0b/NATIVE_METADATA_CHECK.json';m.verify(oldpath,dict(bytes=1443183,sha256='e9400ffb11b976fe80070a87fe5d4fe3e2feb86adb3fea9beeb868ee3bb9a757'));old=m.load(oldpath)
prefix='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9'
vendor=[]
for r in old['fresh_identities']:
 if r['path'].startswith(prefix+'/'):
  now=m.identity(r['path']);assert now==r;vendor.append(now)
assert len(vendor)==1810 and sum(r['bytes'] for r in vendor)==48024515
state=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
namespace=[]
for r in old['namespace']:
 p=Path(r['path']);before=p.lstat();assert state(before)==r['state']
 if r['kind']=='directory':assert sorted(x.name for x in p.iterdir())==r['entries']
 else:assert p.is_symlink() and os.readlink(p)==r['target']
 assert state(p.lstat())==state(before);namespace.append(r)
assert len(namespace)==195
absence=[prefix+'/lib/python39.zip','/Library/Python']
assert all(not os.path.lexists(p) for p in absence)
toolpaths=['/usr/bin/env','/usr/bin/perl','/bin/ps','/usr/bin/sw_vers']
tools=[m.identity(p) for p in toolpaths]
for r in tools:assert r['resolved_path']==r['path'] and r['symlink_chain']==[]
host=subprocess.run(['/usr/bin/sw_vers'],capture_output=True,timeout=5,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
assert host.returncode==0 and host.stderr==b'' and host.stdout==b'ProductName:\t\tmacOS\nProductVersion:\t\t26.5.2\nBuildVersion:\t\t25F84\n'
selected=m.identity(source['bootstrap_binding']['path']);assert selected==source['bootstrap_binding']
for r in sources+vendor+tools:assert m.identity(r['path'])==r
for key in ('root_records','environment_root','tmp','monitor_output'):Path(paths[key]).mkdir(mode=0o700,exist_ok=False)
m.D=Path(paths['root_records'])
assert list(Path(paths['tmp']).iterdir())==[] and list(Path(paths['monitor_output']).iterdir())==[]
assert not os.path.lexists(paths['adapter_output'])
print(m.save('SOURCES_BEFORE.json',dict(sources=sources,source_manifest=m.ref(q['adapter_admission_field_proposal']['source_manifest']['path']),proposal=m.ref(S/'QUALIFICATION_PROPOSAL.json'))))
runtime=m.save('RUNTIME_BEFORE.json',dict(vendor=vendor,namespace=namespace,absent=absence,tools=tools,host=dict(argv=['/usr/bin/sw_vers'],exit_code=host.returncode,stdout=host.stdout.decode(),stderr=host.stderr.decode(),uname=list(os.uname())),environment=q['monitor_call']['env'],observed_at_unix_ns=time.time_ns()))
pre=dict(schema='ri162-root-genuine-inert106-preflight-v1',status='FRESH_SOURCE_VENDOR_HOST_CHECKED_FOR_ONE_INERT_QUALIFICATION',selected_interpreter_binding=selected,source_observation=m.ref(m.D/'SOURCES_BEFORE.json'),runtime_observation=runtime,static_native_adjudication=m.ref(D/'RI164_ROOT_ADJUDICATION.json'),platform_premises=m.load(D/'RI164_ROOT_ADJUDICATION.json')['platform_premises_accepted'],operation_premises=['Unchanged reviewed isolated vendor/stdlib and adapter sources do not introduce undeclared dynamic suppliers or child descendants; these are explicit source/platform assumptions, not runtime closure proofs.','Root retains before/after hashes, source/card bytes and exact environment. Read-window stability is not an enforced global filesystem freeze.','The fixed 960s outer alarm and reviewed 180s child monitor are operational controls, not continuous/group RSS enforcement. Any missed 100ms sampling gap, absent samples, output overflow or genuine nonzero exit refuses this attempt.'],source_acceptance=q['source_root_acceptance'],proposal_acceptance=m.ref(B/'ri163-root-preflight-review-u80slv0b/RI162_ROOT_ADJUDICATION.json'),scientific_execution_authorized=False,controls=106,prepared_at_unix_ns=time.time_ns())
print(m.save('BOOTSTRAP_PREFLIGHT.json',pre))
print(m.save('CONTROLS_REQUEST.json',q['request_fields']));assert m.ref(paths['request'])==q['request_future_identity']
card=q['adapter_admission_field_proposal'];card['bootstrap_preflight']=m.ref(paths['preflight'])
print(m.save('ADAPTER_ADMISSION.json',card))
print(m.save('DISPATCH.json',dict(exec_command=q['exec_command_arguments_proposal'],admission=m.ref(paths['admission']),request=m.ref(paths['request']),preflight=m.ref(paths['preflight']),single_attempt=True,unchanged_source_manifest=q['adapter_admission_field_proposal']['source_manifest'],actual_execution_not_yet_started=True)))
print('READY_FOR_ONE_GENUINE_TOOL_INVOCATION')
