"""Root independent saved-data reconciliation. No subject imports or reruns."""
import importlib.util,os,math,copy,shlex
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
def same(a,b):assert m.canonical(a)==m.canonical(b)
def tree(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  assert not p.is_symlink();row=dict(relative=str(p.relative_to(root)),kind='directory' if p.is_dir() else 'file')
  if p.is_file():row.update(m.pure(m.ref(p)))
  rows.append(row)
 return rows
d=m.load(m.D/'ROOT_DISPATCH.json');initial=m.load(m.D/'GENUINE_TOOL_INITIAL.json');final=m.load(m.D/'GENUINE_TOOL_FINAL.json');same(initial['invocation'],d['invocation']);assert initial['result']['session_id']==12210 and final['exit_code']==0 and final['output']=='' and 'session_id' not in final
O=Path(d['operation']);out=O/'output';card=m.load(O/'cards/launcher.json');control=m.load(O/'cards/controls.json');a=m.load(out/'FOCUSED25.ATTEMPT.json');mon=m.load(out/'FOCUSED25.COMPLETION.json');done=m.load(out/'COMPLETE.json');r=m.load(out/'controls/REPORT.json')
argv=shlex.split(d['invocation']['cmd']);i=argv.index('/usr/bin/perl');same(dict(x.split('=',1) for x in argv[3:i]),card['environment']);same(argv[i+3:],card['launcher_command'])
same(done['child'],mon);same(mon['command'],card['child_command']);same(a['command'],card['child_command']);same(mon['environment'],card['environment']);same(a['environment'],card['environment'])
assert done['status']=='CAPTURED_FOR_ROOT_REVIEW' and done['first_error'] is None and done['independent_tail_errors']==[] and done['elapsed_seconds']<900
assert mon['child_exit_code']==0 and mon['first_error'] is None and mon['stop_reason'] is None and mon['tail_errors']==[] and mon['wall_seconds']==180 and mon['elapsed_seconds']<=180
samples=mon['samples'];attempts=mon['monitor_attempts'];assert len(samples)==len(attempts)==30;last=0
for sample,attempt in zip(samples,attempts):
 assert attempt['returncode']==0 and attempt['stderr']=='' and attempt['stdout'].strip().isdigit()
 assert type(sample['rss_kib']) is int and 0<=sample['rss_kib']<=524288 and sample['rss_kib']==int(attempt['stdout'])
 t=sample['elapsed_seconds'];assert math.isfinite(t) and t>last
 assert abs(sample['gap_seconds']-(t-last))<1e-12 and sample['gap_seconds']<=0.1 and t==attempt['elapsed_seconds'];last=t
gap=mon['elapsed_seconds']-last;assert abs(gap-mon['final_sample_to_reap_gap_seconds'])<1e-12 and 0<=gap<=0.1
assert max(x['rss_kib'] for x in samples)==mon['peak_sampled_rss_kib']==65952
for k in ('stdout','stderr'):m.verify(mon[k]['path'],mon[k]);assert mon[k]['bytes']==0
for row in d['cards']:m.verify(row['path'],row)
for row in d['copies']:m.verify(row['original']['path'],row['original']);m.verify(row['operational']['path'],row['operational'])
same(tree(O/'environment'),[dict(relative='tmp',kind='directory')]);assert sorted(p.name for p in (O/'cards').iterdir())==sorted(Path(x['path']).name for x in d['cards'])
pre=(m.D/'BOOTSTRAP_PRE.json').read_bytes();assert pre==(m.D/'BOOTSTRAP_POST.json').read_bytes()
source=m.load(m.D/'ROOT_SOURCE_RECONCILIATION.json')
for row in source['observations']:assert m.identity(row['path'])==row
for k in ('source','dependency','card'):assert done['checks'][k]=='PASS'
same(m.load(out/'NAMESPACE.json')['entries'],[x for x in tree(out) if x['relative'] not in ('NAMESPACE.json','COMPLETE.json')])
same(m.load(out/'controls/NAMESPACE.json')['entries'],[x for x in tree(out/'controls') if x['relative']!='NAMESPACE.json'])
ids=control['controls'];same(r['order'],ids);same(r['counts'],dict(total=25,passed=25,failed=0));same([x['id'] for x in r['controls']],ids)
same(r['sources_before'],control['sources']);same(r['sources_after'],control['sources']);same(r['admission'],m.ref(O/'cards/controls.json'))
for k in ('actual_current_runtime_qualified','scientific_execution','production_admission_created','runtime_profiles_or_65_caller_guards_executed'):same(r[k],False)
deps=m.load(m.B/'ri139-focused-bootstrap-repair-source-XP8iNwMw/DEPENDENCIES.source-only.json');hist=m.load(deps['historical_interpreter']['path']);checked=[]
pre_errors=dict(pre_admission_read='CONTROL_PRE_ADMISSION_READ',occupied='one fresh root-owned preparation output',mkdir='CONTROL_MKDIR_FAILURE')
for row in r['controls']:
 same(row['passed'],True);same(row['error'],None);kind=row['id'][4:];e=row['evidence']
 if row['id'].startswith('F01_'):
  base=out/'controls'/row['id'];owned=base/'owned-output';same(e['retained_tree'],tree(base));same(e['actual_runtime_or_production_admission'],False)
  counts=dict.fromkeys(('checks','complete','post','pre','source_set','source_tail','tree'),0)
  if kind in pre_errors:
   error=dict(type='ValueError',message=pre_errors[kind]);same(e['first_error'],error);same(e['escaped'],error);same(e['calls'],counts);same(e['attempted_completion'],[]);same(e['returncode'],None)
   if kind=='occupied':assert (owned/'UNRELATED_OCCUPIED').read_bytes()==b'preserve me\n' and sorted(p.name for p in owned.iterdir())==['UNRELATED_OCCUPIED']
   else:assert not os.path.lexists(owned)
  else:
   counts.update(checks=1,complete=1,post=1,pre=int(kind=='positive'),source_set=1 if kind=='post_admission_read' else 2,source_tail=1,tree=1);same(e['calls'],counts)
   error=None if kind=='positive' else dict(type='ValueError',message=dict(post_admission_read='CONTROL_POST_ADMISSION_READ',initial_source_read='CONTROL_INITIAL_SOURCE_READ',attempt_open='CONTROL_ATTEMPT_OPEN').get(kind,'CONTROL_ATTEMPT_PARTIAL'))
   same(e['first_error'],error);assert len(e['attempted_completion'])==1;c=e['attempted_completion'][0];same(c['first_error'],error)
   tails={'secondary_post':[('post_metadata','CONTROL_SECONDARY_POST')],'secondary_source':[('source_admission','CONTROL_SECONDARY_SOURCE')],'secondary_namespace':[('retain_namespace','CONTROL_SECONDARY_NAMESPACE')],'secondary_checks':[('save_checks','CONTROL_SECONDARY_CHECKS')],'three_secondary':[('post_metadata','CONTROL_SECONDARY_POST'),('source_admission','CONTROL_SECONDARY_SOURCE'),('retain_namespace','CONTROL_SECONDARY_NAMESPACE')]}.get(kind,[])
   same(c['independent_tail_errors'],[dict(tail=t,type='ValueError',message=v) for t,v in tails])
   if kind in ('post_admission_read','initial_source_read','attempt_open'):assert not (owned/'ATTEMPT.json').exists()
   elif kind!='positive':assert (owned/'ATTEMPT.json').read_bytes()==b'{"CONTROL_PARTIAL_ATTEMPT":' and e['events'].count('save_ATTEMPT.json')==1
   if kind=='final_partial':assert (owned/'COMPLETE.json').read_bytes()==b'{"CONTROL_PARTIAL_COMPLETE":';same(e['escaped'],dict(type='ValueError',message='CONTROL_FINAL_RECEIPT_WRITE'));same(e['returncode'],None)
   else:same(m.load(owned/'COMPLETE.json'),c);same(e['escaped'],None);same(e['returncode'],int(kind!='positive'))
 else:
  expected=copy.deepcopy(hist)
  if kind in ('named_path','resolved_path'):expected[kind]+='.changed'
  if kind in ('link_literal','snapshot_alias'):expected['symlink_chain'][0]['target']='./python3.11'
  if kind=='link_order':expected['symlink_chain'].reverse()
  if kind=='link_omitted':expected['symlink_chain']=expected['symlink_chain'][1:]
  if kind=='target_bytes':expected['target']['bytes']+=1
  if kind in ('target_sha','snapshot_target'):expected['target']['sha256']='0'*64
  same(e['current_binding_control_operand'],expected);snapshot=kind.startswith('snapshot_')
  same(e['actual_current_interpreter_observed'],False);same(e['snapshot_observers_substituted'],snapshot);same(e['provenance_after_authentication_mutated_in_memory'],kind=='provenance_missing')
  reads=([deps['historical_optional_namespaces']['path']] if snapshot else [])+[deps['historical_interpreter_provenance']['path']]+([] if kind=='provenance_missing' else [deps['historical_interpreter']['path']]);same(e['reads'],reads)
  counts=dict.fromkeys(('absences','host','interpreter','loaders','namespaces','routes','sources','walk'),0)
  if snapshot:counts.update(absences=1,host=1,interpreter=1,loaders=8,namespaces=1,routes=1,sources=1)
  same(e['calls'],counts);same(e['refusal'],None if kind=='positive' else dict(type='RuntimeError',message='historical interpreter handoff identity' if kind=='provenance_missing' else 'candidate interpreter differs from authentic historical binding'))
 checked.append(dict(id=row['id'],checked=True,first_error_or_refusal=e.get('first_error',e.get('refusal'))))
print(m.save('ROOT_ACTUAL_RECONCILIATION.json',dict(schema='ri139-root-actual-focused25-reconciliation-v1',status='PASS_PENDING_INDEPENDENT_ACTUAL_REVIEW',dispatch=m.ref(m.D/'ROOT_DISPATCH.json'),genuine_initial=m.ref(m.D/'GENUINE_TOOL_INITIAL.json'),genuine_final=m.ref(m.D/'GENUINE_TOOL_FINAL.json'),complete=m.ref(out/'COMPLETE.json'),report=m.ref(out/'controls/REPORT.json'),controls=checked,counts=dict(total=25,positives=2,expected_refusals=23),monitor=dict(samples=30,peak_sampled_rss_kib=65952,elapsed_seconds=mon['elapsed_seconds'],maximum_gap_seconds=max(x['gap_seconds'] for x in samples),final_gap_seconds=gap),source_observations_unchanged=len(source['observations']),full_output_namespace=tree(out),complete_operation_namespace=tree(O),bootstrap_pre_post_byte_identical=True,independent_current_science_runtime_qualification=False,no_descendant_and_Apple_loader_cache_premises_retained=True,subject_reexecution=False)))
