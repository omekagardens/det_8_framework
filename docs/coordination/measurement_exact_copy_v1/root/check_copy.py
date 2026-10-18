"""Independent root metadata replay of actual copy and custody, no helper import."""
import hashlib,importlib.util,os,stat,time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=Path(__file__).parent
R=B/'ri170-current-e-root-records-proposed-gikj2giy'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=R
source=m.load(R/'SOURCES_BEFORE.json');runtime=m.load(R/'RUNTIME_BEFORE.json');dispatch=m.load(R/'DISPATCH.json');genuine=m.load(R/'GENUINE_TOOL.json')
for name in ('admission','request','preflight','copy_authority'):m.verify(dispatch[name]['path'],dispatch[name])
for r in source['sources']+runtime['vendor']+runtime['tools']:assert m.identity(r['path'])==r
state=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
for r in runtime['namespace']:
 p=Path(r['path']);assert state(p.lstat())==r['state']
 if r['kind']=='directory':assert sorted(x.name for x in p.iterdir())==r['entries']
 else:assert p.is_symlink() and os.readlink(p)==r['target']
assert all(not os.path.lexists(p) for p in runtime['absent']) and list(os.uname())==runtime['host']['uname']
def tree(root):
 result=[]
 def walk(p):
  a=p.lstat();r=dict(path=str(p),relative=str(p.relative_to(root)),state=state(a))
  if stat.S_ISDIR(a.st_mode):
   names=sorted(x.name for x in p.iterdir());r.update(kind='directory',entries=names);result.append(r)
   for name in names:walk(p/name)
   assert sorted(x.name for x in p.iterdir())==names and state(p.lstat())==state(a);return
  assert stat.S_ISREG(a.st_mode) and a.st_nlink==1
  r.update(kind='file',identity=m.identity(p));assert state(p.lstat())==state(a);result.append(r)
 walk(root);return result
def compact(rows):
 return sorted([dict(relative=r['relative'],kind=r['kind'],**(m.pure(r['identity']) if r['kind']=='file' else {})) for r in rows],key=lambda r:r['relative'])
def observe(path):return {k:m.identity(path)[k] for k in ('path','bytes','sha256','state')}
out=B/'ri156-operation-ri170-copy-proposed-gikj2giy';mon=B/'ri170-copy-monitor-proposed-gikj2giy';env=B/'ri170-copy-environment-proposed-gikj2giy';E=B/'ri154-white-execution-proposed-42_uvw15'
trees={k:tree(p) for k,p in [('operation',out),('monitor',mon),('environment',env),('copied_root',E)]}
assert sorted(p.name for p in out.iterdir())==['ATTEMPT.json','COMPLETE.json','RESULT.json']
assert sorted(p.name for p in mon.iterdir())==['COPY.ATTEMPT.json','COPY.COMPLETION.json','COPY.stderr','COPY.stdout']
assert sorted(p.name for p in env.iterdir())==['tmp'] and list((env/'tmp').iterdir())==[]
c=m.load(mon/'COPY.COMPLETION.json');result=m.load(out/'RESULT.json');complete=m.load(out/'COMPLETE.json');attempt=m.load(out/'ATTEMPT.json')
assert genuine['actual_arguments']==dispatch['exec_command'] and genuine['actual_result']['exit_code']==0 and genuine['actual_result']['output']=='' and genuine['actual_result']['chunk_id']=='d49fc5' and 'session_id' not in genuine['actual_result']
commands=m.load(B/'ri170-measurement-current-e-preflight-gikj2giy/COMMAND_PROPOSALS.json')['commands']['copy']
assert c['command']==commands['monitored_child_argv'] and c['environment']==runtime['environment']==commands['exact_environment'] and c['wall_seconds']==180
assert c['child_exit_code']==0 and c['first_error'] is None and c['tail_errors']==[] and c['stop_reason'] is None and c['passed'] is True
assert 0<c['elapsed_seconds']<180 and c['peak_sampled_rss_kib']<=524288 and c['final_sample_gap_passed'] is True
assert 0<len(c['samples'])==len(c['monitor_attempts'])
last=0
for a,s in zip(c['monitor_attempts'],c['samples']):
 assert a['returncode']==0 and a['stderr']=='' and int(a['stdout'].strip())==s['rss_kib']
 assert a['elapsed_seconds']==s['elapsed_seconds'] and abs(s['gap_seconds']-(s['elapsed_seconds']-last))<1e-12
 assert 0<=s['gap_seconds']<=0.1 and 0<=s['rss_kib']<=524288;last=s['elapsed_seconds']
assert abs(c['final_sample_to_reap_gap_seconds']-(c['elapsed_seconds']-last))<1e-12 and 0<=c['final_sample_to_reap_gap_seconds']<=0.1
assert c['peak_sampled_rss_kib']==max(s['rss_kib'] for s in c['samples'])
for key in ('stdout','stderr'):m.verify(c[key]['path'],c[key]);assert c[key]['bytes']==0
assert attempt==dict(schema='ri156-exclusive-metadata-attempt-v1',admission=dispatch['admission'],action='copy',no_retry=True,scientific_execution=False)
assert complete['schema']=='ri156-adapter-completion-v1' and complete['status']=='COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW'
assert complete['admission']==dispatch['admission'] and complete['action']=='copy' and complete['first_error'] is None and complete['scientific_execution'] is False and complete['root_acceptance_created'] is False and complete['ret_paused'] is True
ct=complete['independent_tails'];assert set(ct)=={'admission','dependencies','namespace','output:ATTEMPT.json','output:RESULT.json','request','sources'} and all(v['error'] is None for v in ct.values())
manifest=m.load(source['source_manifest']['path']);all_sources={**manifest['modules'],'adapter':manifest['adapter'],'manifest':source['source_manifest']}
expected_sources={k:observe(row['path']) for k,row in all_sources.items()}
assert complete['authenticated_source_before']==ct['sources']['value']==complete['tail_observations']['sources']==expected_sources
assert ct['dependencies']['value']==manifest['dependencies'] and ct['admission']['value']==dispatch['admission'] and ct['request']['value']==dispatch['request']
expected_outputs={name:m.ref(out/name) for name in ('ATTEMPT.json','RESULT.json')}
assert complete['produced_output_pins']==complete['tail_observations']['outputs']==expected_outputs
for name,pin in expected_outputs.items():assert ct['output:'+name]['value']==pin
assert complete['artifacts']==dict(attempt=expected_outputs['ATTEMPT.json'],result=expected_outputs['RESULT.json'])
namespace=[r for r in compact(trees['operation']) if r['relative']!='COMPLETE.json']
assert ct['namespace']['value']==complete['tail_observations']['namespace']==namespace
for key in ('namespace_fixture_mismatches','namespace_member_mismatches','namespace_output_mismatches'):assert complete['tail_observations'][key]==[]
assert result['schema']=='ri156-copy-result-v1' and result['status']=='COPIED_PENDING_ROOT_REVIEW' and result['first_error'] is None and result['no_retry'] is True and result['root']==str(E)
rt=result['independent_tails'];assert set(rt)=={'originals','complete_copies','full_namespace'} and all(v['error'] is None for v in rt.values())
authority=m.load(dispatch['copy_authority']['path']);g=m.load(authority['graph']['path']);assert g['prospective_root']==str(E)
copies=[dict(relative=r['relative'],original=observe(r['source']['path']),copy=observe(r['destination'])) for r in g['copied_files']]
for r,decl in zip(copies,g['copied_files']):assert m.pure(r['copy'])==m.pure(r['original'])==m.pure(decl['source'])
expected_states=dict(copies=copies,history=[observe(r['path']) for r in g['history_originals']],target_originals=[observe(r['original']) for r in g['sources']])
expected_tree=[dict(relative=name,kind='directory') for name in ('.','science','science/primary','science/qualifier','science/validator','tmp','runs','runs/normal','runs/optimized')]
expected_tree+= [dict(relative=r['relative'],kind='file',**m.pure(r['source'])) for r in g['copied_files']];expected_tree.sort(key=lambda r:r['relative'])
assert compact(trees['copied_root'])==expected_tree and len(copies)==48 and len(expected_states['history'])==124 and len(expected_states['target_originals'])==30
expected_observation=dict(schema='ri156-complete-copy-card-observation-v1',root=str(E),stage='copied',source_states=expected_states,cards={},tree=expected_tree,tmp_empty=True,scientific_body_decoded=False,source_acceptance_created=False)
assert result['observation']==expected_observation and rt['complete_copies']['value']==expected_states and rt['full_namespace']['value']==expected_tree
assert rt['originals']['value']==[r['source'] for r in g['copied_files']]
for label,p in [('capture','ri170-current-e-capture-proposed-gikj2giy'),('normal','ri170-current-e-profile-normal-proposed-gikj2giy'),('optimized','ri170-current-e-profile-optimized-proposed-gikj2giy')]:assert not os.path.lexists(B/p)
summary=dict(schema='ri174-root-actual-copy-review-v1',status='ACCEPT_ONE_EXACT_METADATA_COPY_ONLY',genuine_tool=m.ref(R/'GENUINE_TOOL.json'),preflight=m.ref(R/'BOOTSTRAP_PREFLIGHT.json'),sources_before=m.ref(R/'SOURCES_BEFORE.json'),runtime_before=m.ref(R/'RUNTIME_BEFORE.json'),sources_rechecked=len(source['sources']),vendor_files_rechecked=len(runtime['vendor']),namespace_entries_rechecked=len(runtime['namespace']),primitives_rechecked=len(runtime['tools']),host_uname_unchanged=True,complete_file_externally_included=True,result=m.ref(out/'RESULT.json'),complete=m.ref(out/'COMPLETE.json'),monitor=m.ref(mon/'COPY.COMPLETION.json'),copy_root=str(E),copied_files=48,history_originals=124,target_originals=30,copied_root_directories=9,all_ten_independent_tails_passed=True,elapsed_seconds=c['elapsed_seconds'],peak_sampled_rss_kib=c['peak_sampled_rss_kib'],samples=len(c['samples']),maximum_sample_gap_seconds=max(s['gap_seconds'] for s in c['samples']),final_gap_seconds=c['final_sample_to_reap_gap_seconds'],runtime_capture_executed=False,scientific_execution=False,ret_paused=True,observed_at_unix_ns=time.time_ns())
print(m.save('POST_CUSTODY.json',dict(summary=summary,trees=trees)))
print(m.save('ACTUAL_COPY_ROOT_REVIEW.json',summary))
