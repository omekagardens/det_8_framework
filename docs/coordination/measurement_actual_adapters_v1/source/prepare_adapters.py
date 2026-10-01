"""UNEXECUTED RI204 proposal. Root review must precede use; prepares one adapters admission only. Never loads a subject."""
import hashlib, importlib.util, json, os, shlex, subprocess, time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri204-root-adapters-f04k2tg9'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
S=B/'ri160-white-fixture-custody-repair-ufok1zpo';P=B/'ri172-root-review-fkjv3v0z';R=B/'ri170-current-e-root-records-proposed-gikj2giy'
pins={
 'source_manifest':(S/'SOURCE_SET.json',147447,'3c01d5825ce66ccf0b071329c46341ea01e28ef4cb76320e5776dd3ae6b53a4f'),
 'source_review':(B/'ri160-root-fixture-adjudication-0rmgmo7y/RI160_ROOT_ADJUDICATION.json',2582,'667e157b07b210952b819f9b9e4907abb4eb3dddb1c7bdcce4d3d6d04ad873b4'),
 'qualification':(P/'RI162_CONSUMER_QUALIFICATION.json',4041,'0e27e1393c949a24a244ef2e2367ed8c72a10df1d3e3a6057cee8a4d20c9e0d7'),
 'profiles':(R/'PROFILES_ACCEPTANCE.json',2208,'d498ccd200b054e8759a37c1cdf0d6014c3e49982e3e944697682266ecf30798'),
 'monitor':(B/'ri141-white-bootstrap-source-h58ls076/prepare.py',45721,'8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe'),
 'template':(B/'ri170-measurement-current-e-preflight-gikj2giy/COPY_BOOTSTRAP.proposal.txt',2440,'c1f5394d34341775d060194c034b570c6551d37ceb3a017f9f0860bb188fb9bf')}
refs={k:dict(path=str(p),bytes=n,sha256=sha) for k,(p,n,sha) in pins.items()}
sources={}
def keep(r):
 row=m.verify(r['path'],r);previous=sources.get(row['path']);assert previous is None or previous==row;sources[row['path']]=row;return row
def load(r):keep(r);return m.load(r['path'])
# Root authenticates the sealed proposal before running this administrative
# preparation. These source captures extend custody, not self-authentication.
W=Path(__file__).resolve().parent
for name in ('prepare_adapters.py','predispatch.py','check_adapters.py','CLOSURE_SEEDS.json','PROPOSAL_NOTES.md'):
 keep(m.ref(W/name))
seeds=load(dict(path=str(W/'CLOSURE_SEEDS.json'),bytes=11142,sha256='bd796aae39a7984fe4fb4c6d57f6741bbe141fcd155af8f7c7e7f3093ef1824b'))
assert seeds['status']=='PROPOSAL_NOT_ADMISSION'
refs['request']=seeds['request']
assert refs['request']==dict(path=str(B/'ri202-root-two-maxima-review-kw07pwnj/ADAPTERS_REQUEST.json'),bytes=3021,sha256='d74665367f305626d445534f1591098e541d1c7b0836bc7ebdd096886b50ee11')
for row in seeds['administrative_records']:keep(row)
prior_sources=m.load(B/'ri200-root-sidecars-ofv27lvp/SOURCES_BEFORE.json')
prior_supplement=m.load(B/'ri200-root-sidecars-ofv27lvp/CLOSURE_SUPPLEMENT.json')
# Preserve every old role, but freshly observe all immutable body references.
assert len(prior_sources['sources'])==659 and len(prior_supplement['current_additional_identities'])==9
assert len(prior_supplement['prior_role_rows'])==810
for row in prior_sources['sources']+prior_supplement['current_additional_identities']+prior_supplement['prior_role_rows']:
 keep(row)
# Traverse FilePins only in explicitly administrative records. Referenced bodies
# remain opaque unless explicitly selected below; no scientific operand decoding.
def keep_refs(value):
 if type(value) is dict:
  if {'path','bytes','sha256'}<=set(value):keep({k:value[k] for k in ('path','bytes','sha256')});return
  if set(value)=={'path','pin'} and type(value['pin']) is dict and set(value['pin'])=={'bytes','sha256'}:keep(dict(path=value['path'],**value['pin']));return
  for item in value.values():keep_refs(item)
 elif type(value) is list:
  for item in value:keep_refs(item)
for row in seeds['administrative_records']:
 name=Path(row['path']).name
 if name in ('SIDECARS_ADJUDICATION.json','INDEPENDENT_SIDECARS_REVIEW.json','ACTUAL_SIDECARS_ROOT_REVIEW.json','GENUINE_TERMINAL_ARGUMENTS.json','ADAPTERS_REQUEST.json','RELOCATED_SOURCE_DECISION.json','INDEPENDENT_MEASUREMENT_INPUT_REVIEW.json','MEASUREMENT_NEXT_ACTION.json'):
  keep_refs(m.load(row['path']))
request=refs['request'];request_value=load(request)
assert set(request_value)=={'root_decisions','profiles_acceptance','sidecars'}
assert set(request_value['root_decisions'])=={'source_review','independent_source_review','packet_handoff','guard_path_review','runtime_applicability'}
assert set(request_value['sidecars'])=={'runtime_inventory','selection','optional_namespaces','observed_dyld_routes','host_scope'}
assert request_value['profiles_acceptance']==refs['profiles']
for key in ('source_review','guard_path_review','runtime_applicability'):
 value=load(request_value['root_decisions'][key]);keep_refs(value)
prior_sidecars=m.load(B/'ri200-root-sidecars-ofv27lvp/ACTUAL_SIDECARS_ROOT_REVIEW.json')
assert request_value['sidecars']==prior_sidecars['sidecars']
assert m.load(B/'ri200-root-sidecars-ofv27lvp/SIDECARS_ADJUDICATION.json')['status']=='ACCEPT_FIVE_WHOLE_FIELD_ADMINISTRATIVE_SIDECARS'

for row in refs.values():keep(row)
manifest=load(refs['source_manifest']);assert len(manifest['modules'])==11 and len(manifest['dependencies'])==567
for row in [manifest['adapter'],*manifest['modules'].values(),*manifest['dependencies']]:keep(row)
q=load(refs['qualification']);assert q['schema']=='ri156-root-inert-controls-review-v1' and q['status']=='ACCEPT_EXACT_INERT_ADAPTER_CONTROLS'
assert q['source_manifest']==refs['source_manifest'] and q['all_passed'] is True and q['scientific_execution'] is False and len(q['controls'])==106
for name in ('report','genuine_outer','independent_review'):keep(q[name])
gpath=B/'ri154-white-mode-preparation-42_uvw15/BINDING_GRAPH.source-only.json'
g=load(dict(path=str(gpath),bytes=86813,sha256='7be820c27d7a7b5f5b1661a49e5119b7922a1c49f4f24fa2d4567d1f2e5942bf'))
profiles=load(refs['profiles']);assert profiles['stage']=='profiles' and profiles['scientific_execution'] is False and profiles['environment_root']==g['prospective_root']
keep(profiles['independent_review']);snapshots=[]
for mode in ('profile_normal','profile_optimized'):
 c=load(profiles['completions'][mode]);outer=load(profiles['genuine_outer'][mode]);keep(outer['raw_tool_receipt'])
 assert c['status']=='CAPTURED_FOR_INDEPENDENT_REVIEW' and c['first_error'] is None and c['independent_tail_errors']==[]
 assert outer['exit_code']==0 and outer['completion']==profiles['completions'][mode] and outer['environment']==c['environment'] and outer['command']==c['command']
 for row in c['artifacts'].values():keep(row)
 pre=load(c['artifacts']['PRE']);post=load(c['artifacts']['POST']);assert pre==post;snapshots.append(pre)
assert snapshots[0]==snapshots[1]
for key,field in {'runtime_inventory':'runtime_inventory','selection':'selection','optional_namespaces':'optional_namespaces','observed_dyld_routes':'preobserved_dyld_routes','host_scope':'host_bootstrap'}.items():
 assert Path(request_value['sidecars'][key]['path']).read_bytes()==m.canonical(snapshots[0][field])
# Native static and prior preflight are read as administrative premises, now pinned
# and included before the source observation is finalized.
static=B/'ri164-root-static-review-xr1qffz8/RI164_ROOT_ADJUDICATION.json'
load(dict(path=str(static),bytes=2910,sha256='001baa675b4bcc7a514537bdaaad9811f79b3170d85e3615368bf8320188ffb7'))
oldpre=load(m.ref(R/'BOOTSTRAP_PREFLIGHT.json'))
# Closed existing E namespace; body pins only, no scientific JSON decoding.
E=Path(g['prospective_root']);names={'.':'directory','science':'directory','science/primary':'directory','science/qualifier':'directory','science/validator':'directory','tmp':'directory','runs':'directory','runs/normal':'directory','runs/optimized':'directory'}
for r in g['copied_files']:
 keep(r['source']);keep(dict(path=r['destination'],**m.pure(r['source'])));names[r['relative']]='file'
for r in g['history_originals']:keep(r)
for r in g['sources']:keep(dict(path=r['original'],**r['pin']))
state=lambda st:[st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]
def tree(root):
 rows=[]
 for p in [root,*sorted(root.rglob('*'))]:
  assert not p.is_symlink();kind='directory' if p.is_dir() else 'file';rel='.' if p==root else str(p.relative_to(root))
  row=dict(relative=rel,kind=kind,state=state(p.lstat()))
  if kind=='file':row['identity']=m.identity(p)
  else:row['entries']=sorted(x.name for x in p.iterdir())
  rows.append(row)
 return rows
etree=tree(E);assert {r['relative']:r['kind'] for r in etree}==names
# Existing accepted vendor/host scope, freshly observed before this operation.
oldpath=B/'ri163-root-preflight-review-u80slv0b/NATIVE_METADATA_CHECK.json'
old=load(dict(path=str(oldpath),bytes=1443183,sha256='e9400ffb11b976fe80070a87fe5d4fe3e2feb86adb3fea9beeb868ee3bb9a757'))
prefix='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9'
vendor=[]
for row in old['fresh_identities']:
 if row['path'].startswith(prefix+'/'):
  now=m.identity(row['path']);assert now==row;vendor.append(now)
assert len(vendor)==1810 and sum(r['bytes'] for r in vendor)==48024515
namespace=[]
for row in old['namespace']:
 p=Path(row['path']);before=p.lstat();assert state(before)==row['state']
 if row['kind']=='directory':assert sorted(x.name for x in p.iterdir())==row['entries']
 else:assert p.is_symlink() and os.readlink(p)==row['target']
 assert state(p.lstat())==state(before);namespace.append(row)
assert len(namespace)==195
absent=[prefix+'/lib/python39.zip','/Library/Python'];assert all(not os.path.lexists(p) for p in absent)
toolrows=[m.identity(p) for p in ('/usr/bin/env','/usr/bin/perl','/bin/ps','/usr/bin/sw_vers')]
host=subprocess.run(['/usr/bin/sw_vers'],capture_output=True,timeout=5,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
assert host.returncode==0 and host.stderr==b'' and host.stdout==b'ProductName:\t\tmacOS\nProductVersion:\t\t26.5.2\nBuildVersion:\t\t25F84\n'
selected=m.identity(manifest['bootstrap_binding']['path']);assert selected==manifest['bootstrap_binding']
for r in list(sources.values())+vendor+toolrows:assert m.identity(r['path'])==r
assert tree(E)==etree
operation=B/'ri156-operation-ri204-adapters-f04k2tg9';monitor=D/'monitor';tmp=D/'tmp'
assert all(not os.path.lexists(p) for p in (operation,monitor,tmp));monitor.mkdir(mode=0o700);tmp.mkdir(mode=0o700)
env=dict(LC_ALL='C',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PATH='/usr/bin:/bin',TMPDIR=str(tmp),TZ='UTC',VECLIB_MAXIMUM_THREADS='1',__CF_USER_TEXT_ENCODING='0x1F5:0x0:0x0')
m.save('CLOSURE_SUPPLEMENT.json',dict(schema='ri204-prior-role-custody-supplement-v1',
 prior=prior_supplement['prior'],prior_role_rows=prior_supplement['prior_role_rows'],
 ri200_source_record=m.ref(B/'ri200-root-sidecars-ofv27lvp/SOURCES_BEFORE.json'),
 ri200_supplement=m.ref(B/'ri200-root-sidecars-ofv27lvp/CLOSURE_SUPPLEMENT.json'),
 ri200_prior_source_rows=prior_sources['sources'],ri200_prior_additional_identities=prior_supplement['current_additional_identities'],
 prior_roles=810,ri200_distinct_sources=668,current_additional_identities=[],
 total_current=len(sources),all_prior_roles_in_current_source_map=True,
 historical_states_are_not_current_observations=True,scientific_execution=False))
m.save('SOURCES_BEFORE.json',dict(sources=list(sources.values()),inputs=refs,graph=m.ref(gpath)))
runtime=m.save('RUNTIME_BEFORE.json',dict(vendor=vendor,namespace=namespace,absent=absent,tools=toolrows,host=dict(argv=['/usr/bin/sw_vers'],exit_code=host.returncode,stdout=host.stdout.decode(),stderr=host.stderr.decode(),uname=list(os.uname())),environment=env,observed_at_unix_ns=time.time_ns()))
m.save('E_BEFORE.json',etree)
# Static/prior-preflight inputs already pinned in the finalized source closure.
pre=m.save('BOOTSTRAP_PREFLIGHT.json',dict(schema='ri204-root-adapters-preflight-v1',status='FRESH_SOURCE_VENDOR_HOST_CHECKED_FOR_ONE_METADATA_ADAPTERS_ACTION',selected_interpreter_binding=selected,source_observation=m.ref(D/'SOURCES_BEFORE.json'),source_supplement=m.ref(D/'CLOSURE_SUPPLEMENT.json'),runtime_observation=runtime,E_observation=m.ref(D/'E_BEFORE.json'),static_native_adjudication=m.ref(static),platform_premises=m.load(static)['platform_premises_accepted'],operation_premises=oldpre['operation_premises'],source_acceptance=refs['source_review'],scientific_execution_authorized=False,prepared_at_unix_ns=time.time_ns()))
# The exact accepted RI202 request is consumed at its original path; never regenerated.
assert request==refs['request']
card=dict(schema='ri156-root-adapter-admission-v1',status='AUTHORIZE_ONE_BOUNDED_METADATA_ACTION',action='adapters',source_manifest=refs['source_manifest'],source_review=refs['source_review'],qualification=refs['qualification'],request=request,output=str(operation),environment=env,bootstrap_preflight=pre,bounds=dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=0.025,maximum_sample_gap_seconds=0.1,ps_timeout_seconds=0.05,file_bytes=67108864),genuine_outer_required=True)
assert len(card)==12;m.save('ADMIT_ADAPTERS.json',card)
bootstrap=Path(refs['template']['path']).read_text()
oldenv=m.load(B/'ri170-measurement-current-e-preflight-gikj2giy/COMMAND_PROPOSALS.json')['commands']['copy']['exact_environment']
bootstrap=bootstrap.replace('# Prospective text only. Not executed or an admission. Root must review and issue actual cards first.','# One root-admitted administrative adapters action; unchanged RI141 child monitor.')
bootstrap=bootstrap.replace(repr(oldenv),repr(env))
bootstrap=bootstrap.replace('ri170_whole_unchanged_ri141_copy_monitor','ri204_whole_unchanged_ri141_adapters_monitor')
bootstrap=bootstrap.replace(str(R/'ADMIT_COPY_ADAPTER.json'),str(D/'ADMIT_ADAPTERS.json')).replace(str(B/'ri170-copy-monitor-proposed-gikj2giy'),str(monitor)).replace("'COPY', 180, expected_environment)","'ADAPTERS', 180, expected_environment)")
assert repr(env) in bootstrap and 'ADMIT_COPY' not in bootstrap and "'ADAPTERS'" in bootstrap
with (D/'ADAPTERS_BOOTSTRAP.py').open('x') as f:f.write(bootstrap)
outer=['/usr/bin/env','-i',*[k+'='+v for k,v in env.items()],'/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',selected['path'],'-I','-B',str(D/'ADAPTERS_BOOTSTRAP.py')]
m.save('DISPATCH.json',dict(outer_argv=outer,shell_command=shlex.join(outer),cwd=str(D),login=False,admission=m.ref(D/'ADMIT_ADAPTERS.json'),request=request,preflight=pre,bootstrap=m.ref(D/'ADAPTERS_BOOTSTRAP.py'),monitor_source=refs['monitor'],single_attempt=True,actual_execution_not_yet_started=True))
print(json.dumps(dict(status='PREPARED_FOR_INDEPENDENT_PREFLIGHT_REVIEW',root=str(D),sources=len(sources),vendor_files=len(vendor),vendor_bytes=sum(r['bytes'] for r in vendor),namespace=len(namespace),E_files=len(g['copied_files']),dispatch=m.ref(D/'DISPATCH.json'))))
