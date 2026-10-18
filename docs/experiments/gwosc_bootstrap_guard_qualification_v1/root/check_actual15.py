"""Root saved-record arithmetic and custody check; no subject execution."""
import importlib.util, copy, math
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
same=lambda a,b:m.canonical(a)==m.canonical(b)
record=m.load(m.D/'ACTUAL15_REVIEW_INPUT.json');op=Path(record['operation']);out=op/'output';cr=out/'controls'
S=m.B/'ri144-bootstrap-guard-source-oaj1jvyt';deps=m.load(S/'DEPENDENCIES.source-only.json');baseline=deps['selected_bootstrap_binding']
for row in record['operation_tree']:
 p=op/row['relative'];assert not p.is_symlink()
 if row['kind']=='file':assert m.identity(p)==row['identity']
 else:assert p.is_dir()
assert {str(p.relative_to(op)) for p in op.rglob('*')}=={x['relative'] for x in record['operation_tree']}
for row in m.load(m.D/'ROOT_MEASUREMENT_SOURCE_CHECK.json')['observations']:assert m.identity(row['path'])==row
for row in deps['opaque_files']:m.verify(row['path'],row)
assert (m.D/'BOOTSTRAP_PRE.json').read_bytes()==(m.D/'BOOTSTRAP_POST.json').read_bytes()
for name in ('BOOTSTRAP_PRE_TOOL.json','BOOTSTRAP_POST_TOOL.json','GENUINE_TOOL_COMPLETE.json'):
 tool=m.load(m.D/name);assert tool['result']['exit_code']==0 and 'session_id' not in tool['result']
actual=m.load(m.D/'GENUINE_TOOL_COMPLETE.json');dispatch=m.load(m.D/'ROOT_DISPATCH.json');assert actual['invocation']==dispatch['invocation'] and actual['result']['output']==''
for row in dispatch['cards']:m.verify(row['path'],row)
for row in dispatch['copies']:assert Path(row['original']['path']).read_bytes()==Path(row['operational']['path']).read_bytes()
ids=['B01','B02','B03','B04','B05','B06']+['B07_'+k for k in ('path','resolved_path','symlink_chain','bytes','sha256','state')]+['B08','B09','B10']
report=m.load(cr/'REPORT.json');assert report['order']==ids and [r['id'] for r in report['controls']]==ids
assert report['counts']==dict(total=15,passed=15,failed=0) and report['first_error'] is None and report['independent_tail_errors']==[]
assert report['status']=='FIFTEEN_EXPECTATIONS_PASSED'
assert all(report[k] is False for k in ('actual_supplier_observed','current_runtime_qualified','old25_rerun','production_authenticate_called','scientific_execution'))
messages=[None,'bootstrap selection provenance absent from closure','metadata reference drift','accepted direct bootstrap selection provenance','closed selected interpreter binding','closed selected interpreter binding']+['genuine preflight selected interpreter identity']*6+['opaque evidence reference drift','selected interpreter state drift','direct interpreter descriptor']
lengths=[28,1,9,19,20,20]+[21]*6+[24,26,28]
names=['bootstrap selection provenance absent from closure','private_provenance_read','closed metadata FilePin','literal source/metadata path','bounded regular source/metadata','metadata opened drift','metadata descriptor drift','metadata read drift','metadata reference drift']+['duplicate metadata key']*8+['canonical metadata framing','accepted direct bootstrap selection provenance','closed selected interpreter binding','genuine preflight selected interpreter identity','literal direct bootstrap selection','supplier_bytes','opaque evidence reference drift','supplier_lstat','selected interpreter state drift','interpreter_descriptor','direct interpreter descriptor']
observers={1,22,24,26};summary=[]
for row,message,length in zip(report['controls'],messages,lengths):
 i=row['id'];e=row['evidence'];assert row['passed'] is True and row['error'] is None
 assert same(e['baseline_binding'],baseline) and e['complete_loaded_module']==deps['target_module'] and e['captured_loaded_bytes']==m.pure(deps['target_module'])
 expected=[]
 for j in range(length):
  expected.append(dict(kind='observer',name=names[j]) if j in observers else dict(kind='gate',name=names[j],passed=not(message is not None and j==length-1)))
 assert same(e['trace'],expected) and same(e['expected_trace'],expected)
 refusal=None if message is None else dict(type='ValueError',message=message)
 assert same(e['first_refusal'],refusal) and same(e['expected_first_refusal'],refusal)
 returned=baseline if i=='B01' else None
 assert same(e['returned_binding'],returned) and same(e['expected_returned_binding'],returned)
 assert e['inputs_unchanged'] is True and e['real_private_reader_parser_and_comparisons'] is True
 assert e['actual_supplier_observed'] is False and e['production_authenticate_called'] is False
 private=cr/i/'PROVENANCE_DOUBLE.json';selected=copy.deepcopy(baseline)
 if i in ('B03','B04'):selected['bytes']+=1
 assert private.read_bytes()==m.canonical(dict(schema='ri144-private-provenance-double-v1',selected_bootstrap_binding=selected))
 assert e['private_provenance_actual']==m.ref(private)
 declared=dict(path=str(private),**m.pin(m.canonical(dict(schema='ri144-private-provenance-double-v1',selected_bootstrap_binding=selected if i=='B04' else baseline))))
 assert e['private_provenance_declared']==declared
 assert same(e['dependency_operand'],dict(bootstrap_selection_provenance=declared,opaque_files=[] if i=='B02' else [declared],selected_bootstrap_binding=baseline))
 pre=copy.deepcopy(baseline)
 if i=='B05':del pre['state']
 elif i=='B06':pre['extra']=True
 elif i.startswith('B07_'):
  k=i[4:]
  if k in ('path','resolved_path'):pre[k]+='.changed'
  elif k=='bytes':pre[k]+=1
  elif k=='sha256':pre[k]='0'*64
  elif k=='state':pre[k][1]+=1
  else:pre[k]=[dict(path=baseline['path']+'.alias',target=baseline['path'])]
 assert same(e['preflight_operand'],dict(selected_interpreter_binding=pre))
 obs=dict(bytes={k:baseline[k] for k in ('path','bytes','sha256')},state=list(baseline['state']),descriptor=baseline['path'])
 if i=='B08':obs['bytes']['bytes']+=1
 if i=='B09':obs['state'][1]+=1
 if i=='B10':obs['descriptor']+='.changed'
 assert same(e['observer_doubles'],obs)
 summary.append(dict(id=i,trace_length=length,first_refusal=refusal,private_bytes=m.ref(private)))
def tree(root,exclude=()):
 result=[]
 for p in sorted(root.rglob('*')):
  rel=p.relative_to(root).as_posix()
  if rel in exclude:continue
  assert not p.is_symlink()
  result.append(dict(relative=rel,kind='directory') if p.is_dir() else dict(relative=rel,kind='file',**m.pure(m.ref(p))))
 return result
childnames={'ATTEMPT.json','REPORT.json','NAMESPACE.json'}|set(ids)|{i+'/PROVENANCE_DOUBLE.json' for i in ids}
parentnames={'ATTEMPT.json','BOOTSTRAP15.ATTEMPT.json','BOOTSTRAP15.stdout','BOOTSTRAP15.stderr','BOOTSTRAP15.COMPLETION.json','ENVELOPE_CHECKS.json','ADMINISTRATIVE_CHECKS.json','NAMESPACE.json','COMPLETE.json','controls'}|{'controls/'+i for i in childnames}
assert {r['relative'] for r in tree(cr)}==childnames and len(childnames)==33
assert {r['relative'] for r in tree(out)}==parentnames and len(parentnames)==43
assert m.load(cr/'NAMESPACE.json')['entries']==tree(cr,('NAMESPACE.json',))
assert m.load(out/'NAMESPACE.json')['entries']==tree(out,('NAMESPACE.json','COMPLETE.json'))
completion=m.load(out/'COMPLETE.json');child=m.load(out/'BOOTSTRAP15.COMPLETION.json');card=m.load(op/'cards/launcher.json')
assert same(completion['child'],child) and completion['status']=='CAPTURED_FOR_ROOT_REVIEW'
assert completion['first_error'] is None and completion['independent_tail_errors']==[] and 0<=completion['elapsed_seconds']<=900
assert child['first_error'] is None and child['tail_errors']==[] and child['stop_reason'] is None and child['child_exit_code']==0
assert child['command']==card['child_command'] and child['environment']==card['environment']
assert 0<=child['elapsed_seconds']<=180 and child['wall_seconds']==180
assert len(child['samples'])==len(child['monitor_attempts'])==10
last=0;peak=0;maxgap=0
for sample,attempt in zip(child['samples'],child['monitor_attempts']):
 assert attempt['returncode']==0 and attempt['stderr']=='' and int(attempt['stdout'])==sample['rss_kib'] and attempt['elapsed_seconds']==sample['elapsed_seconds']
 gap=sample['elapsed_seconds']-last;assert math.isclose(gap,sample['gap_seconds'],abs_tol=1e-12) and 0<=gap<=.1 and 0<=sample['rss_kib']<=524288
 last=sample['elapsed_seconds'];peak=max(peak,sample['rss_kib']);maxgap=max(maxgap,gap)
finalgap=child['elapsed_seconds']-last;assert math.isclose(finalgap,child['final_sample_to_reap_gap_seconds'],abs_tol=1e-12) and 0<=finalgap<=.1
assert child['peak_sampled_rss_kib']==peak and child['final_sample_gap_passed'] is True
for field in ('stdout','stderr'):assert child[field]==m.ref(out/('BOOTSTRAP15.'+field)) and child[field]['bytes']==0
assert all(r.get('bytes',0)<=67108864 for r in tree(out)) and sum(r.get('bytes',0) for r in tree(out))<=536870912
print(m.save('ROOT_ACTUAL15_CHECK.json',dict(schema='ri144-root-saved-actual15-reconciliation-v1',status='PASS_SAVED_RECORD_AND_CUSTODY_CHECK',review_input=m.ref(m.D/'ACTUAL15_REVIEW_INPUT.json'),checker=m.ref(__file__),cases=summary,source_dependencies=472,parent_entries=43,child_entries=33,monitor_attempts=10,peak_sampled_rss_kib=peak,child_seconds=child['elapsed_seconds'],maximum_sample_gap_seconds=maxgap,final_gap_seconds=finalgap,complete_operation_identity_unchanged=True,complete_bootstrap_PRE_POST_equal=True,actual_tool_chunk='32ad3f',actual_exit_code=0,subject_execution_by_this_checker=False,remaining='Separate complete nonauthor actual review, then root actual adjudication; production capture remains separate',scientific_credit=False)))
