"""RI162 authorized finite read-only facts; never executes any selected Python,
monitor, adapter or control. No recursive supplier/runtime or environment scan.
"""
from pathlib import Path
import os,stat,hashlib,json,subprocess,datetime
D=Path(__file__).resolve().parent;B=D.parent
S=B/'ri160-white-fixture-custody-repair-ufok1zpo';Q=B/'ri141-white-bootstrap-source-h58ls076'
VENDOR='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def observe(name):
 p=Path(name);resolved=p.resolve(strict=True);chain=[];current=p
 # The exact named selection and each symlink selected at its endpoint. Whole
 # path resolution is separately recorded; no runtime namespace is traversed.
 while current.is_symlink():
  before=current.lstat();target=os.readlink(current);assert state(before)==state(current.lstat())
  chain.append({'path':str(current),'target':target,'state':state(before)})
  current=(current.parent/target).absolute() if not os.path.isabs(target) else Path(target)
  assert len(chain)<=16
 before=resolved.lstat();assert stat.S_ISREG(before.st_mode) and before.st_size<=67108864
 h=hashlib.sha256();n=0
 with resolved.open('rb') as f:
  assert state(os.fstat(f.fileno()))==state(before)
  for b in iter(lambda:f.read(65536),b''):h.update(b);n+=len(b);assert n<=67108864
  assert state(os.fstat(f.fileno()))==state(before)
 assert n==before.st_size and state(resolved.lstat())==state(before) and p.resolve(strict=True)==resolved
 return {'path':str(p),'resolved_path':str(resolved),'bytes':n,'sha256':h.hexdigest(),'state':state(before),'symlink_chain':chain}
selected=[VENDOR,str(Q/'prepare.py'),'/usr/bin/env','/usr/bin/perl','/bin/ps','/usr/bin/sw_vers']
rows=[observe(p) for p in selected]
command=['/usr/bin/sw_vers'];host=subprocess.run(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10,check=False)
u=os.uname();historical=json.loads((S/'SOURCE_SET.json').read_bytes())['bootstrap_binding']
record={'schema':'ri162-fixed-read-only-facts-v1','observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selected_file_observations':rows,'historical_selected_binding':historical,'current_selected_binding':rows[0],'current_binding_equals_immutable_expected_binding':rows[0]==historical,'host':{'uname':{'sysname':u.sysname,'release':u.release,'version':u.version,'machine':u.machine},'sw_vers':{'command':command,'timeout_seconds':10,'returncode':host.returncode,'stdout':host.stdout.decode('utf8'),'stderr':host.stderr.decode('utf8')}},'limitations':['Finite fixed-file bytes/selection and OS facts only; no selected interpreter execution, sys.executable/flags/environment observation, runtime import/profile or complete supplier preflight.','Full supplier/cache/loader/host applicability remains a root predispatch responsibility; historical supplier observations are not current.','Path-component symlinks are represented by complete resolved_path; explicit chain lists endpoint symlink traversal. Direct vendor is required to have named path equal resolved path and empty chain.'],'target_or_control_execution':False,'runtime_inventory':False,'active_admission_created':False}
with (D/'FIXED_CURRENT_FACTS.json').open('x') as f:json.dump(record,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({'selected_files':len(rows),'vendor_exact_historical_binding':record['current_binding_equals_immutable_expected_binding'],'vendor':rows[0],'host':record['host'],'execution':'read-only sw_vers only; no selected vendor or subject execution'},sort_keys=True))
