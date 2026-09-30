"""Independent root saved-evidence arithmetic and opaque identity check only."""
import importlib.util, os, stat
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
layout=m.load(m.D/'OPERATION_LAYOUT.json');op=Path(layout['operation']);out=op/'output'
def tree(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  row=dict(relative=p.relative_to(root).as_posix()); st=p.lstat()
  if stat.S_ISLNK(st.st_mode):row.update(kind='symlink',target=os.readlink(p))
  elif stat.S_ISDIR(st.st_mode):row['kind']='directory'
  else:assert stat.S_ISREG(st.st_mode); row.update(kind='file',**m.pure(m.ref(p)))
  rows.append(row)
 return rows
before=m.load(m.D/'SOURCE_PRE.json');after=[m.identity(r['path']) for r in before['identities']];assert after==before['identities']
print(m.save('SOURCE_POST.json',dict(identities=after,unchanged=True)))
for key in ['card','source_review']:
 row=m.load(m.D/'ADMISSION_CUSTODY.json')[key];assert m.identity(row['path'])==row
assert (m.D/'BOOTSTRAP_PRE.json').read_bytes()==(m.D/'BOOTSTRAP_POST.json').read_bytes()
assert m.load(m.D/'BOOTSTRAP_POST_TOOL.json')['result']['exit_code']==0
genuine=m.load(m.D/'GENUINE_TOOL_COMPLETE.json');assert genuine['initial']['session_id']==81040 and genuine['terminal']['exit_code']==0
assert genuine['initial']['output']==genuine['terminal']['output']==''
complete=m.load(out/'COMPLETE.json');card=m.load(op/'CAPTURE_ADMISSION.json')
assert complete['status']=='CAPTURED_FOR_INDEPENDENT_REVIEW' and complete['first_error'] is None and complete['independent_tail_errors']==[]
assert complete['sources']==card['sources'] and complete['admission']==m.ref(op/'CAPTURE_ADMISSION.json')
assert complete['environment']==layout['environment'] and complete['phase']=='capture'
assert complete['ret_paused'] is True and all(complete[k] is False for k in ['scientific_targets_executed','actual_data_admitted','full32_qualified','runtime_acceptance_created','genuine_outer_created'])
assert 0<complete['elapsed_seconds']<900
assert all(card[k] is None for k in ['baseline_acceptance','normal_acceptance','profiles_acceptance','guard_admission'])
for row in complete['artifacts'].values():m.verify(row['path'],row)
namespace=m.load(out/'NAMESPACE.json');assert namespace['excluded_not_yet_written']==['NAMESPACE.json','COMPLETE.json']
expected=namespace['entries']+[dict(relative=n,kind='file',**m.pure(m.ref(out/n))) for n in ['NAMESPACE.json','COMPLETE.json']]
assert tree(out)==sorted(expected,key=lambda r:r['relative']) and len(expected)==12
assert m.load(out/'CHECKS.json')==dict(post_metadata='PASS',source_and_admission_postcheck='PASS')
summaries=[]
for label in ['PRE','POST']:
 child=m.load(out/(label+'.COMPLETION.json'));attempt=m.load(out/(label+'.ATTEMPT.json'))
 assert child['passed'] and child['child_exit_code']==0 and child['first_error'] is None and child['stop_reason'] is None and child['tail_errors']==[]
 assert child['wall_seconds']==attempt['wall_seconds']==180 and 0<child['elapsed_seconds']<=180
 assert child['command']==attempt['command']==[layout['selected_interpreter_binding']['path'],'-I','-B',str(m.B/'ri141-white-bootstrap-source-h58ls076/prepare.py'),'--snapshot',str(op/'CAPTURE_ADMISSION.json')]
 assert child['environment']==attempt['environment']==layout['environment'] and attempt['scientific_target_entry'] is False and type(attempt['pid_owner']) is int and attempt['pid_owner']>0
 assert len(child['samples'])==len(child['monitor_attempts'])>0
 previous=0
 for sample,raw in zip(child['samples'],child['monitor_attempts']):
  assert raw['returncode']==0 and raw['stderr']=='' and raw['stdout'].strip().isdigit()
  assert sample['rss_kib']==int(raw['stdout']) and sample['elapsed_seconds']==raw['elapsed_seconds']
  assert 0<=sample['rss_kib']<=524288 and 0<=sample['gap_seconds']<=.1
  assert abs(sample['elapsed_seconds']-previous-sample['gap_seconds'])<1e-9
  previous=sample['elapsed_seconds']
 assert child['peak_sampled_rss_kib']==max(x['rss_kib'] for x in child['samples'])
 assert abs(child['elapsed_seconds']-previous-child['final_sample_to_reap_gap_seconds'])<1e-9
 assert child['final_sample_gap_passed'] and 0<=child['final_sample_to_reap_gap_seconds']<=.1
 for stream in ['stdout','stderr']:m.verify(child[stream]['path'],child[stream]);assert child[stream]['bytes']<=67108864
 assert child['stderr']['bytes']==0
 summaries.append(dict(label=label,samples=len(child['samples']),elapsed=child['elapsed_seconds'],peak_rss_kib=child['peak_sampled_rss_kib'],maximum_gap=max(x['gap_seconds'] for x in child['samples']),final_gap=child['final_sample_to_reap_gap_seconds']))
assert (out/'PRE.stdout').read_bytes()==(out/'POST.stdout').read_bytes()
snap=m.load(out/'PRE.stdout');deps=m.load(m.B/'ri141-white-bootstrap-source-h58ls076/DEPENDENCIES.source-only.json')
assert snap['runtime_inventory']==m.load(deps['historical_runtime']['path'])
assert snap['interpreter']==m.load(deps['historical_interpreter']['path'])
assert snap['optional_namespaces']==m.load(deps['historical_optional_namespaces']['path'])
assert snap['sources']['opaque_files']==deps['opaque_files'] and snap['sources']['packet_namespace']==deps['packet_namespace']
assert snap['host_bootstrap']['bootstrap']['named']==card['bootstrap']
assert dict(uname=snap['host_bootstrap']['uname'],system_version=snap['host_bootstrap']['system_version'])==card['host']
assert snap['scientific_execution'] is False and snap['actual_data_admission'] is False
runtime=snap['runtime_inventory'];selections={r['path']:r for r in snap['selection']['files']};runtime_rows=[]
for r in runtime['files']:
 fresh=m.verify(r['path'],r);runtime_rows.append(fresh);sel=selections[r['path']];st=fresh['state']
 for k,v in zip(['device','inode','mode','nlink','bytes','mtime_ns','ctime_ns'],st):
  if k!='nlink':assert sel[k]==v
 if Path(r['path']).suffix=='.pyc':
  with open(r['path'],'rb') as f:assert f.read(16).hex()==sel['pyc_first16_hex']
  assert sel['pyc_payload_not_parsed_or_executed'] is True
assert len(selections)==len(runtime_rows)
for p in runtime['absent_paths']+snap['preobserved_dyld_routes']['absent_paths']:assert not os.path.lexists(p)
for row in runtime['symlinks']+snap['preobserved_dyld_routes']['symlinks']:assert os.readlink(row['path'])==row['target']
for row in runtime['loader_bindings']+[snap['interpreter']]:
 fresh=m.identity(row['named_path']);assert fresh['resolved_path']==row['resolved_path'] and fresh['symlink_chain']==row['symlink_chain'] and m.pure(fresh)==row['target']
print(m.save('RUNTIME_POST_IDENTITIES.json',dict(identities=runtime_rows,scientific_body_decode=False,subject_execution=False)))
print(m.save('OPERATION_FINAL_IDENTITIES.json',dict(root=str(op),entries=tree(op),identities=[m.identity(p) for p in sorted(op.rglob('*')) if p.is_file()])))
outer=dict(schema='ri133-root-genuine-outer-v1',status='ACTUAL_TOOL_COMPLETION',command=complete['command'],environment=layout['environment'],exit_code=0,completion=m.ref(out/'COMPLETE.json'),raw_tool_receipt=m.ref(m.D/'GENUINE_TOOL_COMPLETE.json'),external_timeout_seconds=960)
print(m.save('GENUINE_OUTER.json',outer))
print(m.save('ROOT_CAPTURE_CHECK.json',dict(schema='ri146-root-saved-capture-check-v1',status='PASS_PENDING_INDEPENDENT_REVIEW',source_files=len(after),runtime_files=len(runtime_rows),runtime_bytes=sum(x['bytes'] for x in runtime_rows),snapshots=m.ref(out/'PRE.stdout'),snapshots_byte_equal=True,monitors=summaries,parent_seconds=complete['elapsed_seconds'],output_entries=len(expected),operation_entries=len(tree(op)),source_admission_and_vendor_unchanged=True,scientific_credit=False,scope='Saved complete snapshot comparison, every runtime file fresh opaque identity/selection, actual monitor arithmetic, full output namespace; independent actual review remains separate')))
