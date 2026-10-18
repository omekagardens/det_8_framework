"""Root read-only concrete preparation and full custody review; no subject import."""
import hashlib,importlib.util,json,os,shlex,stat
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri224-root-cwd-review-nyvru347';D=B/'ri222-freeze-cwd-repair-ypiy2jqw';W=D/'worker_proposal';E=B/'ri154-white-execution-proposed-42_uvw15'
H=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=H.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',H);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def load(p):return json.loads(Path(p).read_bytes())
def bound(row):m.verify(row['path'],row);return load(row['path'])
def eq(a,b):assert m.canonical(a)==m.canonical(b)
files=['ROOT_SOURCE_REVIEW.json','HOST_GENUINE_TOOL.json','HOST_BEFORE.json','INSTALL_BOOTSTRAP.py','SOURCES_BEFORE.json','SUPPLIER_BEFORE.json','E_BEFORE.json','INSTALL_PREFLIGHT.json','INSTALLATION_PROPOSAL.json','PREPARATION_CUSTODY.json']
eq(sorted(p.name for p in D.iterdir()),sorted(files+['worker_proposal','tmp','monitor']))
assert list((D/'tmp').iterdir())==list((D/'monitor').iterdir())==[]
for p in [B/'ri222-freeze-install-operation-ypiy2jqw',E/'AUTHORIZED_FREEZE.json',E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json',D/'ADMIT_INSTALL.json',D/'DISPATCH.json']:assert not os.path.lexists(p)
observed=[m.identity(D/n) for n in files]
c=load(D/'PREPARATION_CUSTODY.json');p=load(D/'INSTALLATION_PROPOSAL.json');pre=load(D/'INSTALL_PREFLIGHT.json');manifest=load(W/'SOURCE_PINS.json')
m.verify(D/'PREPARATION_CUSTODY.json',dict(bytes=16080,sha256='b165ed2229cf07c61b138fdca0fdde53ddd25ccecdfb8273c6155fc9f552be52'))
m.verify(D/'INSTALLATION_PROPOSAL.json',dict(bytes=4509,sha256='ca1dd21438eaff45880fae5699177f2ef29a0d5e0b2103648ee4de8704e6361b'))
assert c['status']=='PREPARED_NOT_ADMITTED_OR_DISPATCHED' and c['source_domain']==904 and not c['installation_admitted'] and not c['installation_dispatched']
for k in ('original_genuine_host','canonical_genuine_host','preparation_source','preflight','unissued_proposal','source_observations','supplier_observation','E_observation','monitor_template'):m.verify(c[k]['path'],c[k])
for row in c['sealed_source_packet']+c['root_review_support']:eq(m.identity(row['path']),row)
card=p['proposed_admission'];dispatch=p['proposed_dispatch'];assert p['active_card_created'] is p['dispatch_created'] is False
assert set(card)==set(['schema','status','source_manifest','source_review','preflight','output','environment','limits','genuine_outer_required'])
eq(m.pure(p['prospective_admission_pin']),m.pin(m.canonical(card)));eq(dispatch['admission'],p['prospective_admission_pin'])
eq(card['preflight'],m.ref(D/'INSTALL_PREFLIGHT.json'));eq(card['source_review'],m.ref(D/'ROOT_SOURCE_REVIEW.json'));eq(card['source_manifest'],m.ref(W/'SOURCE_PINS.json'))
assert card['status']=='AUTHORIZE_ONE_EXACT_FREEZE_INSTALLATION' and card['output']==str(B/'ri222-freeze-install-operation-ypiy2jqw') and card['genuine_outer_required'] is True
env=dict(LC_ALL='C',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PATH='/usr/bin:/bin',TMPDIR=str(D/'tmp'),TZ='UTC',VECLIB_MAXIMUM_THREADS='1',__CF_USER_TEXT_ENCODING='0x1F5:0x0:0x0')
eq(card['environment'],env);eq(pre['environment'],env)
eq(card['limits'],dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=.025,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05,file_bytes=67108864))
vendor='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
outer=['/usr/bin/env','-i',*[k+'='+v for k,v in env.items()],'/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',vendor,'-I','-B',str(D/'INSTALL_BOOTSTRAP.py')]
eq(dispatch['outer_argv'],outer);assert dispatch['shell_command']==shlex.join(outer) and dispatch['cwd']==str(D) and dispatch['login'] is False and dispatch['external_timeout_seconds']==960 and dispatch['single_attempt'] is True
template=Path(c['monitor_template']['path']).read_text()
for old,new in c['bootstrap_replacements']:assert template.count(old)==1;template=template.replace(old,new)
assert template.encode()==(D/'INSTALL_BOOTSTRAP.py').read_bytes()
m.verify(D/'INSTALL_BOOTSTRAP.py',dict(bytes=2413,sha256='8fbc916c29a874d93f2a1b0543e86870f26a6dc2ce01c57104dcd725c092d853'))
contract=c['cwd_contract'];assert contract['outer_cwd']==str(D) and contract['child_cwd']==str(D/'monitor')
m.verify(contract['monitor']['path'],contract['monitor']);m.verify(contract['installer']['path'],contract['installer'])
monitor=Path(contract['monitor']['path']).read_text();span=monitor[monitor.index('def child_run(command, out, label, seconds, env):'):monitor.index('def dyld_attempts(')]
assert span.count(contract['exact_popen'])==1 and 'chdir' not in span
assert template.count(contract['generated_child_call'])==1 and "Path('"+str(D/'monitor')+"')" in contract['generated_child_call']
assert Path(contract['installer']['path']).read_text().count(contract['installer_guard'])==1
inputs=bound(manifest['files'][0]);repair=bound(manifest['files'][2]);expected={}
for row in inputs['files']+repair['files']+manifest['files']+[m.ref(W/'SOURCE_PINS.json'),m.ref(D/'ROOT_SOURCE_REVIEW.json'),m.ref(D/'INSTALL_BOOTSTRAP.py')]:
 if row['path'] in expected:eq(m.pure(expected[row['path']]),m.pure(row))
 expected[row['path']]=row
sources=bound(pre['sources']);assert len(sources)==len(expected)==904 and {r['path'] for r in sources}==set(expected)
for row in sources:eq(m.pure(row),m.pure(expected[row['path']]))
supplier=bound(pre['supplier']);assert len(supplier['vendor'])==1810 and sum(r['bytes'] for r in supplier['vendor'])==48024515 and len(supplier['tools'])==4 and len(supplier['namespace'])==195 and len(supplier['absent'])==2
host=bound(pre['host_tool_receipts']);genuine=bound(host['genuine_tool']);eq(json.loads(genuine['result']['output']),genuine['observation']);assert genuine['result']['chunk_id']=='343dae' and genuine['result']['exit_code']==0
eq(genuine,load(R/'GENUINE_PREPARATION_HOST_TOOL.json'));eq(supplier['host'],dict(argv=host['command'],exit_code=host['returncode'],stdout=host['stdout'],stderr=host['stderr'],uname=host['uname']));eq(list(os.uname()),host['uname'])
old=bound(inputs['roles']['historical_supplier']);eq({k:v for k,v in supplier.items() if k not in ('environment','observed_at_unix_ns')},{k:v for k,v in old.items() if k not in ('environment','observed_at_unix_ns')})
estate=bound(pre['E_before']);eq(estate,sorted(bound(inputs['roles']['historical_E']),key=lambda r:r['relative']));assert len(estate)==57 and sum(r['kind']=='file' for r in estate)==48
state=lambda a:[a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns]
for repeat in range(2):
 for row in sources+supplier['vendor']+supplier['tools']+observed:eq(m.identity(row['path']),row)
 for row in supplier['namespace']:
  q=Path(row['path']);eq(state(q.lstat()),row['state'])
  if row['kind']=='directory':eq(sorted(x.name for x in q.iterdir()),row['entries'])
  else:assert row['kind']=='symlink';eq(os.readlink(q),row['target'])
 assert all(not os.path.lexists(q) for q in supplier['absent'])
 for row in estate:
  q=E/row['relative'];eq(state(q.lstat()),row['state'])
  if row['kind']=='directory':eq(sorted(x.name for x in q.iterdir()),row['entries'])
  else:eq(m.identity(q),row['identity'])
entry=load(R/'REPO_ENTRY.json');eq(m.snapshot(),entry)
print(json.dumps(dict(status='PASS_ROOT_CONCRETE_PREPARATION_NOT_ADMISSION',source_rows=904,vendor_files=1810,vendor_bytes=48024515,tools=4,namespace=195,absences=2,E_files=48,E_directories=9,exact_prepared_files=observed,bootstrap_cwd_contract=contract,repository_unchanged=True,scientific_execution=False)))
