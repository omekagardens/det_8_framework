"""Root metadata-only preservation and custody after the actual refused child."""
from pathlib import Path
import hashlib,importlib.util,json,os
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri221-root-installation-ru2v15ie';D=B/'ri218-freeze-byte-repair-x62withm';E=B/'ri154-white-execution-proposed-42_uvw15'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
def loadref(r):m.verify(r['path'],r);return m.load(r['path'])
def st(p):
 a=p.lstat();return [a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns]
tool=m.load('/private/tmp/ri221_installation_tool_transcript.json');assert tool['initial_result']['chunk_id']=='685f23' and tool['initial_result']['exit_code']==1 and 'session_id' not in tool['initial_result'];assert tool['terminal_result'] is None
toolref=m.save('GENUINE_INSTALLATION_TOOL.json',tool)
host=m.load('/private/tmp/ri221_host_post.json');assert host['result']['chunk_id']=='bb4da0' and host['result']['exit_code']==0 and json.loads(host['result']['output'])==host['observation'];hostref=m.save('GENUINE_POST_HOST_TOOL.json',host)
pre=m.load(D/'INSTALL_PREFLIGHT.json');sources=loadref(pre['sources']);supplier=loadref(pre['supplier']);tree=loadref(pre['E_before'])
for r in sources+supplier['vendor']+supplier['tools']:assert m.identity(r['path'])==r
for r in supplier['namespace']:
 p=Path(r['path']);assert st(p)==r['state']
 if r['kind']=='directory':assert sorted(x.name for x in p.iterdir())==r['entries']
 else:assert os.readlink(p)==r['target']
assert all(not os.path.lexists(p) for p in supplier['absent'])
assert host['observation']==dict(command=supplier['host']['argv'],environment={'PATH':'/usr/bin:/bin','LC_ALL':'C'},returncode=0,stdout=supplier['host']['stdout'],stderr='',uname=supplier['host']['uname'])
assert list(os.uname())==host['observation']['uname']
for r in tree:
 p=E/r['relative'];assert st(p)==r['state']
 if r['kind']=='directory':assert sorted(x.name for x in p.iterdir())==r['entries']
 else:assert r['kind']=='file' and m.identity(p)==r['identity']
assert len(tree)==57 and sum(r['kind']=='file' for r in tree)==48
proposal=m.load(D/'INSTALLATION_PROPOSAL.json');assert m.load(D/'ADMIT_INSTALL.json')==proposal['proposed_admission'];assert m.load(D/'DISPATCH.json')==proposal['proposed_dispatch']
dispatch=m.load(D/'DISPATCH.json');assert tool['execution_arguments']==dict(cmd=dispatch['shell_command'],workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=4000)
monitor=D/'monitor';assert sorted(x.name for x in monitor.iterdir())==['INSTALL.ATTEMPT.json','INSTALL.COMPLETION.json','INSTALL.stderr','INSTALL.stdout']
saved=[m.identity(p) for p in sorted(monitor.iterdir())];completion=m.load(monitor/'INSTALL.COMPLETION.json');attempt=m.load(monitor/'INSTALL.ATTEMPT.json')
assert completion['passed'] is False and completion['child_exit_code']==1 and completion['first_error'] is None and completion['tail_errors']==[] and completion['stop_reason'] is None
assert completion['command']==attempt['command']==dispatch['child_command'] if 'child_command' in dispatch else completion['command']==attempt['command']
assert completion['environment']==attempt['environment']==pre['environment'] and completion['wall_seconds']==attempt['wall_seconds']==180
for k in ('stdout','stderr'):m.verify(completion[k]['path'],completion[k])
assert completion['stdout']['bytes']==0 and completion['stderr']['bytes']==701 and completion['stderr']['sha256']=='9e0fb84869c9df052f636d2446611f8bc901785725f482e49df1eaacc794cd4e'
assert 'fixed operation paths' in (monitor/'INSTALL.stderr').read_text()
assert list((D/'tmp').iterdir())==[]
absences=[proposal['proposed_admission']['output'],str(E/'AUTHORIZED_FREEZE.json'),str(E/'ADMIT_NORMAL.json'),str(E/'ADMIT_OPTIMIZED.json')]
assert all(not os.path.lexists(p) for p in absences)
expected=['HOST_GENUINE_TOOL.json','HOST_BEFORE.json','INSTALL_BOOTSTRAP.py','SOURCES_BEFORE.json','SUPPLIER_BEFORE.json','E_BEFORE.json','INSTALL_PREFLIGHT.json','INSTALLATION_PROPOSAL.json','PREPARATION_CUSTODY.json','ROOT_SOURCE_REVIEW.json','tmp','monitor','worker_proposal','ADMIT_INSTALL.json','DISPATCH.json']
assert sorted(x.name for x in D.iterdir())==sorted(expected)
old=B/'ri213-freeze-clock-repair-2xc_b29x';assert sorted(x.name for x in old.iterdir())==['HOST_GENUINE_TOOL.json','monitor','tmp','worker_proposal'];assert list((old/'monitor').iterdir())==list((old/'tmp').iterdir())==[]
m.verify(old/'HOST_GENUINE_TOOL.json',dict(bytes=1891,sha256='07cbac05498fb9329338592a1dea8255d09145bee24598491722d494509b4305'))
oldseal=m.load(old/'worker_proposal/HANDOFF.json');assert sorted(x.name for x in (old/'worker_proposal').iterdir())==oldseal['namespace']
for r in oldseal['files']:m.verify(r['path'],r)
current=m.snapshot();entry=m.load(R/'REPO_ENTRY.json');assert current==entry
result=dict(schema='ri221-post-refusal-custody-v1',status='REFUSED_BEFORE_OUTPUT_OWNERSHIP_E_UNCHANGED',genuine_installation=toolref,genuine_post_host=hostref,sources=len(sources),vendor_files=len(supplier['vendor']),vendor_bytes=sum(r['bytes'] for r in supplier['vendor']),tools=len(supplier['tools']),supplier_namespace_rows=len(supplier['namespace']),supplier_absences=supplier['absent'],E_observation=pre['E_before'],E_files=48,E_directories=9,full_identity_state_and_membership_unchanged=True,monitor_files=saved,admission=m.identity(D/'ADMIT_INSTALL.json'),dispatch=m.identity(D/'DISPATCH.json'),operation_and_mode_absences=absences,old_D213_partials_preserved=True,repository_entry=m.ref(R/'REPO_ENTRY.json'),repository_whole_snapshot_unchanged=True,no_retry=True,qualification_credit=0,ret_paused=True)
print(json.dumps(m.save('POST_FAILURE_CUSTODY.json',result)))
