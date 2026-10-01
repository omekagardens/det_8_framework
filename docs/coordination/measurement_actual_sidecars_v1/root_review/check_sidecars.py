"""Independent root replay of saved administrative sidecars; no subject import."""
import hashlib, importlib.util, os, stat, subprocess, time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri200-root-sidecars-ofv27lvp'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
sources=m.load(D/'SOURCES_BEFORE.json');runtime=m.load(D/'RUNTIME_BEFORE.json');dispatch=m.load(D/'DISPATCH.json');genuine=m.load(D/'GENUINE_TOOL.json')
for name in ('admission','request','preflight','bootstrap','monitor_source'):m.verify(dispatch[name]['path'],dispatch[name])
supplement=m.load(D/'CLOSURE_SUPPLEMENT.json')
for r in sources['sources']+supplement['current_additional_identities']+runtime['vendor']+runtime['tools']:assert m.identity(r['path'])==r
state=lambda st:[st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]
for r in runtime['namespace']:
 p=Path(r['path']);assert state(p.lstat())==r['state']
 if r['kind']=='directory':assert sorted(x.name for x in p.iterdir())==r['entries']
 else:assert p.is_symlink() and os.readlink(p)==r['target']
assert all(not os.path.lexists(p) for p in runtime['absent']) and list(os.uname())==runtime['host']['uname']
host=subprocess.run(runtime['host']['argv'],capture_output=True,timeout=5,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
assert host.returncode==runtime['host']['exit_code']==0 and host.stdout.decode()==runtime['host']['stdout'] and host.stderr.decode()==runtime['host']['stderr']==''
def tree(root):
 rows=[]
 for p in [root,*sorted(root.rglob('*'))]:
  assert not p.is_symlink();kind='directory' if p.is_dir() else 'file';rel='.' if p==root else str(p.relative_to(root))
  row=dict(relative=rel,kind=kind,state=state(p.lstat()))
  if kind=='file':assert p.stat().st_nlink==1;row['identity']=m.identity(p)
  else:row['entries']=sorted(x.name for x in p.iterdir())
  rows.append(row)
 return rows
def compact(rows):return sorted([dict(relative=r['relative'],kind=r['kind'],**(m.pure(r['identity']) if r['kind']=='file' else {})) for r in rows],key=lambda r:r['relative'])
def observe(path):return {k:m.identity(path)[k] for k in ('path','bytes','sha256','state')}
admit=m.load(dispatch['admission']['path']);out=Path(admit['output']);mon=D/'monitor';E=B/'ri154-white-execution-proposed-42_uvw15'
trees={k:tree(p) for k,p in [('operation',out),('monitor',mon),('tmp',D/'tmp'),('E',E)]}
assert trees['E']==m.load(D/'E_BEFORE.json') and list((D/'tmp').iterdir())==[]
names={'runtime_inventory':'runtime_inventory','selection':'selection','optional_namespaces':'optional_namespaces','observed_dyld_routes':'preobserved_dyld_routes','host_scope':'host_bootstrap'}
produced_names=['ATTEMPT.json','RESULT.json',*[k+'.json' for k in names]]
assert sorted(p.name for p in out.iterdir())==sorted(produced_names+['COMPLETE.json'])
assert sorted(p.name for p in mon.iterdir())==['SIDECARS.ATTEMPT.json','SIDECARS.COMPLETION.json','SIDECARS.stderr','SIDECARS.stdout']
assert genuine['actual_arguments']['cmd']==dispatch['shell_command'] and genuine['actual_arguments']['workdir']==str(D) and genuine['actual_arguments']['login'] is False
assert genuine['actual_result']['exit_code']==0 and genuine['actual_result']['output']=='' and 'session_id' not in genuine['actual_result']
c=m.load(mon/'SIDECARS.COMPLETION.json');result=m.load(out/'RESULT.json');complete=m.load(out/'COMPLETE.json');attempt=m.load(out/'ATTEMPT.json')
command=[m.load(sources['inputs']['source_manifest']['path'])['bootstrap_binding']['path'],'-I','-B',str(B/'ri160-white-fixture-custody-repair-ufok1zpo/adapter.py'),'--admission',dispatch['admission']['path']]
assert c['command']==command and c['environment']==runtime['environment']==admit['environment'] and c['wall_seconds']==180
assert c['child_exit_code']==0 and c['first_error'] is None and c['tail_errors']==[] and c['stop_reason'] is None and c['passed'] is True
assert 0<c['elapsed_seconds']<180 and c['peak_sampled_rss_kib']<=524288 and c['final_sample_gap_passed'] is True
assert 0<len(c['samples'])<=len(c['monitor_attempts'])<=len(c['samples'])+1
last=0
for a,sample in zip(c['monitor_attempts'],c['samples']):
 assert a['returncode']==0 and a['stderr']=='' and int(a['stdout'].strip())==sample['rss_kib']
 assert a['elapsed_seconds']==sample['elapsed_seconds'] and abs(sample['gap_seconds']-(sample['elapsed_seconds']-last))<1e-12
 assert 0<=sample['gap_seconds']<=0.1 and 0<=sample['rss_kib']<=524288;last=sample['elapsed_seconds']
if len(c['monitor_attempts'])>len(c['samples']):
 a=c['monitor_attempts'][-1];assert set(a)=={'elapsed_seconds','returncode','stdout','stderr'} and a['returncode']==1 and a['stdout'].strip()=='' and a['stderr']=='' and last<=a['elapsed_seconds']<=c['elapsed_seconds']
assert abs(c['final_sample_to_reap_gap_seconds']-(c['elapsed_seconds']-last))<1e-12 and 0<=c['final_sample_to_reap_gap_seconds']<=0.1
assert c['peak_sampled_rss_kib']==max(s['rss_kib'] for s in c['samples'])
for key in ('stdout','stderr'):m.verify(c[key]['path'],c[key]);assert c[key]['bytes']==0
ma=m.load(mon/'SIDECARS.ATTEMPT.json');assert set(ma)=={'command','environment','wall_seconds','pid_owner','scientific_target_entry'} and ma['command']==command and ma['environment']==c['environment'] and ma['wall_seconds']==180 and type(ma['pid_owner']) is int and ma['pid_owner']>0 and ma['scientific_target_entry'] is False
assert attempt==dict(schema='ri156-exclusive-metadata-attempt-v1',admission=dispatch['admission'],action='sidecars',no_retry=True,scientific_execution=False)
assert complete['schema']=='ri156-adapter-completion-v1' and complete['status']=='COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW'
assert complete['admission']==dispatch['admission'] and complete['action']=='sidecars' and complete['first_error'] is None and complete['scientific_execution'] is False and complete['root_acceptance_created'] is False and complete['ret_paused'] is True and 0<=complete['elapsed_seconds_before_complete_write']<=180
ct=complete['independent_tails'];assert set(ct)=={'admission','dependencies','namespace','request','sources',*('output:'+n for n in produced_names)} and all(v['error'] is None for v in ct.values())
manifest=m.load(sources['inputs']['source_manifest']['path']);all_sources={**manifest['modules'],'adapter':manifest['adapter'],'manifest':sources['inputs']['source_manifest']}
expected_sources={k:observe(row['path']) for k,row in all_sources.items()}
assert complete['authenticated_source_before']==ct['sources']['value']==complete['tail_observations']['sources']==expected_sources
assert ct['dependencies']['value']==manifest['dependencies'] and ct['admission']['value']==dispatch['admission'] and ct['request']['value']==dispatch['request']
outputs={name:m.ref(out/name) for name in produced_names}
assert complete['produced_output_pins']==complete['tail_observations']['outputs']==outputs
for name,pin in outputs.items():assert ct['output:'+name]['value']==pin
assert complete['artifacts']==dict(attempt=outputs['ATTEMPT.json'],result=outputs['RESULT.json'])
namespace=[r for r in compact(trees['operation']) if r['relative']!='COMPLETE.json']
assert ct['namespace']['value']==complete['tail_observations']['namespace']==namespace
for key in ('namespace_fixture_mismatches','namespace_member_mismatches','namespace_output_mismatches'):assert complete['tail_observations'][key]==[]
for key in ('namespace_fixture_trees','namespace_fixture_comparisons'):assert key not in complete['tail_observations']
profiles=m.load(sources['inputs']['profiles']['path']);normal=m.load(profiles['completions']['profile_normal']['path']);pre=m.load(normal['artifacts']['PRE']['path'])
expected={key:m.ref(out/(key+'.json')) for key in names};assert result==expected
for name,field in names.items():assert (out/(name+'.json')).read_bytes()==m.canonical(pre[field])
summary=dict(schema='ri200-root-sidecars-review-v1',status='ACCEPT_FIVE_WHOLE_FIELD_ADMINISTRATIVE_SIDECARS',genuine_tool=m.ref(D/'GENUINE_TOOL.json'),preflight=dispatch['preflight'],sources_before=m.ref(D/'SOURCES_BEFORE.json'),runtime_before=m.ref(D/'RUNTIME_BEFORE.json'),sources_rechecked=len(sources['sources'])+len(supplement['current_additional_identities']),source_supplement=m.ref(D/'CLOSURE_SUPPLEMENT.json'),prior_role_rows_preserved=810,vendor_files_rechecked=len(runtime['vendor']),vendor_bytes_rechecked=sum(r['bytes'] for r in runtime['vendor']),namespace_entries_rechecked=len(runtime['namespace']),primitives_rechecked=len(runtime['tools']),host_uname_unchanged=True,host_version_unchanged=True,complete_file_externally_included=True,result=m.ref(out/'RESULT.json'),complete=m.ref(out/'COMPLETE.json'),monitor=m.ref(mon/'SIDECARS.COMPLETION.json'),sidecars=expected,mappings=names,baseline=normal['artifacts']['PRE'],E_unchanged=True,sidecar_count=5,operation_files=8,all_twelve_independent_tails_passed=True,elapsed_seconds=c['elapsed_seconds'],peak_sampled_rss_kib=c['peak_sampled_rss_kib'],samples=len(c['samples']),maximum_sample_gap_seconds=max(s['gap_seconds'] for s in c['samples']),final_gap_seconds=c['final_sample_to_reap_gap_seconds'],runtime_capture_executed=False,scientific_execution=False,ret_paused=True,observed_at_unix_ns=time.time_ns())
print(m.save('POST_CUSTODY.json',dict(summary=summary,trees=trees)))
print(m.save('ACTUAL_SIDECARS_ROOT_REVIEW.json',summary))
