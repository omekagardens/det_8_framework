"""Root retained post-operation custody; does not import or rerun subjects."""
import hashlib,importlib.util,json,os,stat,time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri162-inert106-root-records-proposed-wb69vu5s'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=R
source=m.load(R/'SOURCES_BEFORE.json');runtime=m.load(R/'RUNTIME_BEFORE.json');dispatch=m.load(R/'DISPATCH.json')
for name in ('admission','request','preflight'):m.verify(dispatch[name]['path'],dispatch[name])
for r in source['sources']+runtime['vendor']+runtime['tools']:assert m.identity(r['path'])==r
state=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
for r in runtime['namespace']:
 p=Path(r['path']);assert state(p.lstat())==r['state']
 if r['kind']=='directory':assert sorted(x.name for x in p.iterdir())==r['entries']
 else:assert p.is_symlink() and os.readlink(p)==r['target']
assert all(not os.path.lexists(p) for p in runtime['absent'])
assert list(os.uname())==runtime['host']['uname']
def tree(root):
 result=[]
 def walk(p):
  a=p.lstat();r=dict(path=str(p),relative=str(p.relative_to(root)),state=state(a))
  if stat.S_ISLNK(a.st_mode):r.update(kind='symlink',target=os.readlink(p))
  elif stat.S_ISDIR(a.st_mode):
   names=sorted(x.name for x in p.iterdir());r.update(kind='directory',entries=names);result.append(r)
   for name in names:walk(p/name)
   assert sorted(x.name for x in p.iterdir())==names and state(p.lstat())==state(a)
   return
  elif stat.S_ISREG(a.st_mode):r.update(kind='file',identity=m.identity(p))
  else:raise ValueError('unexpected output entry '+str(p))
  assert state(p.lstat())==state(a);result.append(r)
 walk(root);return result
out=B/'ri156-operation-ri162-inert106-wb69vu5s';mon=B/'ri162-inert106-monitor-proposed-wb69vu5s';env=B/'ri162-inert106-environment-proposed-wb69vu5s'
trees={k:tree(p) for k,p in [('operation',out),('monitor',mon),('environment',env)]}
assert sorted(p.name for p in out.iterdir())==['ATTEMPT.json','COMPLETE.json','RESULT.json','inert-fixtures','integration-fixtures']
assert sorted(p.name for p in mon.iterdir())==['CONTROLS.ATTEMPT.json','CONTROLS.COMPLETION.json','CONTROLS.stderr','CONTROLS.stdout']
assert list((env/'tmp').iterdir())==[]
c=m.load(mon/'CONTROLS.COMPLETION.json');result=m.load(out/'RESULT.json');complete=m.load(out/'COMPLETE.json')
assert c['child_exit_code']==0 and c['first_error'] is None and c['tail_errors']==[] and c['stop_reason'] is None and c['passed'] is True
assert 0<c['elapsed_seconds']<180 and c['peak_sampled_rss_kib']<=524288 and c['final_sample_gap_passed'] is True
assert len(c['samples'])==len(c['monitor_attempts'])==130
last=0
for a,s in zip(c['monitor_attempts'],c['samples']):
 assert a['returncode']==0 and a['stderr']=='' and int(a['stdout'].strip())==s['rss_kib']
 assert a['elapsed_seconds']==s['elapsed_seconds'] and abs(s['gap_seconds']-(s['elapsed_seconds']-last))<1e-12
 assert 0<=s['gap_seconds']<=0.1 and s['rss_kib']<=524288;last=s['elapsed_seconds']
assert abs(c['final_sample_to_reap_gap_seconds']-(c['elapsed_seconds']-last))<1e-12 and c['final_sample_to_reap_gap_seconds']<=0.1
assert c['peak_sampled_rss_kib']==max(s['rss_kib'] for s in c['samples'])
for key in ('stdout','stderr'):m.verify(c[key]['path'],c[key]);assert c[key]['bytes']==0
assert len(result['controls'])==len(result['order'])==106 and result['scientific_execution'] is False
assert complete['first_error'] is None and complete['scientific_execution'] is False
terminal=m.load(R/'GENUINE_TERMINAL_TOOL.json');assert terminal['actual']['exit_code']==0 and terminal['actual']['output']=='' and terminal['initial']['session_id']==66856
summary=dict(schema='ri162-root-actual-inert106-tail-v1',status='GENUINE_OPERATION_FINISHED_PENDING_FULL_INDEPENDENT_CONTROL_REVIEW',genuine_initial=m.ref(R/'GENUINE_INITIAL_TOOL.json'),genuine_terminal=m.ref(R/'GENUINE_TERMINAL_TOOL.json'),preflight=m.ref(R/'BOOTSTRAP_PREFLIGHT.json'),sources_before=m.ref(R/'SOURCES_BEFORE.json'),runtime_before=m.ref(R/'RUNTIME_BEFORE.json'),sources_rechecked=len(source['sources']),vendor_files_rechecked=len(runtime['vendor']),namespace_entries_rechecked=len(runtime['namespace']),primitives_rechecked=len(runtime['tools']),host_uname_unchanged=True,operation_files=sum(r['kind']=='file' for r in trees['operation']),complete_file_externally_included=True,result=m.ref(out/'RESULT.json'),complete=m.ref(out/'COMPLETE.json'),monitor=m.ref(mon/'CONTROLS.COMPLETION.json'),records=len(result['controls']),elapsed_seconds=c['elapsed_seconds'],peak_sampled_rss_kib=c['peak_sampled_rss_kib'],samples=len(c['samples']),maximum_sample_gap_seconds=max(s['gap_seconds'] for s in c['samples']),final_gap_seconds=c['final_sample_to_reap_gap_seconds'],fixture_genuine_credentials=False,scientific_execution=False,ret_paused=True,observed_at_unix_ns=time.time_ns())
print(m.save('POST_CUSTODY.json',dict(summary=summary,trees=trees)))
print(m.save('ACTUAL_RUN_SUMMARY.json',summary))
