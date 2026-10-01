from pathlib import Path
import importlib.util,hashlib,json,os,time
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri234-root-reconciliation-tzop5ais';D=B/'ri226-directory-custody-recovery-yvfg_p1b';O=B/'ri226-freeze-reconciliation-operation-yvfg_p1b'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
host=m.load('/private/tmp/ri234_post_host_record.json');assert host['result']['exit_code']==0
obs=json.loads(host['result']['output']);host['observation']=obs;hp=m.save('GENUINE_POST_HOST.json',host);hr=m.save('POST_HOST.json',dict(schema='ri209-root-host-command-record-v1',**obs,genuine_tool=hp))
old=m.load(D/'SUPPLIER_BEFORE.json')
def state(p):
 z=p.lstat();return [z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]
post=dict(absent=[],environment=old['environment'],host=dict(argv=obs['command'],exit_code=obs['returncode'],stderr=obs['stderr'],stdout=obs['stdout'],uname=list(os.uname())),namespace=[],observed_at_unix_ns=time.time_ns(),tools=[m.identity(r['path']) for r in old['tools']],vendor=[m.identity(r['path']) for r in old['vendor']])
assert obs['returncode']==0 and obs['stderr']=='' and obs['environment']==dict(PATH='/usr/bin:/bin',LC_ALL='C')
for r in old['namespace']:
 p=Path(r['path']);a=state(p);row=dict(path=str(p),kind=r['kind'],state=a)
 if r['kind']=='directory':row['entries']=sorted(x.name for x in p.iterdir())
 else:row['target']=os.readlink(p)
 assert state(p)==a;post['namespace'].append(row)
for path in old['absent']:
 assert not os.path.lexists(path);post['absent'].append(path)
assert m.canonical({k:v for k,v in post.items() if k!='observed_at_unix_ns'})==m.canonical({k:v for k,v in old.items() if k!='observed_at_unix_ns'})
sp=m.save('POST_SUPPLIER.json',post)
transcript=m.load('/private/tmp/ri234_operation_transcript.json');tp=m.save('GENUINE_RECONCILIATION_TOOL.json',transcript)
transport=m.load('/private/tmp/ri234_operation_transport.json');m.save('GENUINE_RECONCILIATION_TRANSPORT.json',transport)
outer=m.save('GENUINE_OUTER.json',dict(schema='ri226-root-genuine-reconciliation-v1',dispatch=m.ref(D/'DISPATCH.json'),tool_transcript=tp,monitor=m.ref(D/'monitor/RECONCILE.COMPLETION.json'),post_supplier=sp,post_host_tools=hr))
assert m.canonical(m.snapshot())==m.canonical(m.load(R/'REPO_ENTRY.json'))
print(json.dumps(dict(outer=outer,monitor={k:v for k,v in m.load(D/'monitor/RECONCILE.COMPLETION.json').items() if k in ('passed','elapsed_seconds','peak_sampled_rss_kib','first_error','tail_errors','child_exit_code','final_sample_to_reap_gap_seconds')},completion={k:v for k,v in m.load(O/'COMPLETE.json').items() if k in ('status','first_error','elapsed_seconds_before_complete_write')})))
