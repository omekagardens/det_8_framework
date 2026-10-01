"""Fresh administrative pre-dispatch custody, no target or adapter invocation."""
import hashlib,importlib.util,os,subprocess,time
from pathlib import Path
D=Path('/Volumes/AI_DATA/development/det-review-evidence/ri200-root-sidecars-ofv27lvp');B=D.parent
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=hp.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
sources=m.load(D/'SOURCES_BEFORE.json');runtime=m.load(D/'RUNTIME_BEFORE.json');dispatch=m.load(D/'DISPATCH.json')
supplement=m.load(D/'CLOSURE_SUPPLEMENT.json')
for r in sources['sources']+supplement['current_additional_identities']+runtime['vendor']+runtime['tools']:assert m.identity(r['path'])==r
state=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
for r in runtime['namespace']:
 p=Path(r['path']);assert state(p.lstat())==r['state']
 if r['kind']=='directory':assert sorted(x.name for x in p.iterdir())==r['entries']
 else:assert os.readlink(p)==r['target']
assert all(not os.path.lexists(p) for p in runtime['absent']) and list(os.uname())==runtime['host']['uname']
host=subprocess.run(runtime['host']['argv'],capture_output=True,timeout=5,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
assert host.returncode==0 and host.stdout.decode()==runtime['host']['stdout'] and host.stderr==b''
E=B/'ri154-white-execution-proposed-42_uvw15';before=m.load(D/'E_BEFORE.json');actual=[E,*sorted(E.rglob('*'))]
assert len(actual)==len(before)
for p,r in zip(actual,before):
 assert not p.is_symlink() and state(p.lstat())==r['state']
 if r['kind']=='file':assert m.identity(p)==r['identity']
 else:assert sorted(x.name for x in p.iterdir())==r['entries']
for name in ('admission','request','preflight','bootstrap','monitor_source'):m.verify(dispatch[name]['path'],dispatch[name])
a=m.load(dispatch['admission']['path']);assert a['environment']==runtime['environment'] and not os.path.lexists(a['output']) and list((D/'monitor').iterdir())==list((D/'tmp').iterdir())==[]
print(m.save('PREDISPATCH_CUSTODY.json',dict(schema='ri200-fresh-predispatch-custody-v1',dispatch=m.ref(D/'DISPATCH.json'),sources_before=m.ref(D/'SOURCES_BEFORE.json'),runtime_before=m.ref(D/'RUNTIME_BEFORE.json'),E_before=m.ref(D/'E_BEFORE.json'),all_full_identities_equal=True,source_files=len(sources['sources']),vendor_files=len(runtime['vendor']),namespace_rows=len(runtime['namespace']),tools=len(runtime['tools']),absences=len(runtime['absent']),E_unchanged=True,owned_outputs_fresh=True,host_unchanged=True,observed_at_unix_ns=time.time_ns(),scientific_execution=False)))
