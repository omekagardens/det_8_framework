"""Root administrative review reconciliation; no archived target execution."""
import importlib.util
import os
from pathlib import Path
import stat

s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
D=m.D;R=D/'review'
m.verify(R/'HANDOFF.json',dict(bytes=7582,sha256='bb20f9a2072725038cd5630a46120f5a9ced6e99e267ade5f7079451edb82647'))
h=m.load(R/'HANDOFF.json');v=m.load(R/'VERDICT.json');t=m.load(R/'TEST_RESULTS.json');sub=m.load(R/'PUBLICATION_SUBSET.json')
assert len(h['files'])==22 and len({x['path'] for x in h['files']})==22
for row in h['files']+[h['source'],h['readme']]:m.verify(row['path'],row)
assert {x['path'] for x in sub['review_files']}=={x['path'] for x in h['files']} - {str(R/'PUBLICATION_SUBSET.json')}
assert h['tests']==v['tests']==t['counts']==dict(total=17,passed=17,positive=3,negative=14)
assert h['verdict']==v['verdict']=='PASS_NARROW_READ_ONLY_ARCHIVE_UTILITY' and v['blocking_findings']==[]
assert len(t['results'])==len(t['result_records'])==17
positive=[];negative=[]
for row,result in zip(t['result_records'],t['results']):
 m.verify(row['path'],row);assert m.load(row['path'])==result
 assert result['passed'] is True and result['exit_code']==result['expected_exit'] and result['timeout_seconds']==30
 assert result['command'][:3]==['/usr/bin/python3','-I','-B']
 assert result['command'][3]==result['checker']['path']
 m.verify(result['checker']['path'],h['source'])
 if result['exit_code']==0:
  assert result['stderr']=='';out=__import__('json').loads(result['stdout'])
  assert out['status']=='PUBLISHED_BYTES_AND_SAVED_AGREEMENT_PASS'
  assert (out['archived_files'],out['exact_copies'],out['operation_files'],out['saved_control_outcomes'],out['saved_monitor_samples'])==(135,132,89,25,30)
  assert all(out[x] is False for x in ['archived_code_executed','external_paths_opened','current_runtime_qualified','historical_tool_origin_independently_authenticated','scientific_claim_established'])
  positive.append(result['case'])
 else:
  assert result['exit_code']==1 and result['stdout']=='';out=__import__('json').loads(result['stderr'])
  assert out['status']=='REFUSED' and result['expected_refusal_substring'] in out['error'];negative.append(result['case'])
A=Path(t['original_archive']);inventory=[]
for directory,dirs,files in os.walk(A,followlinks=False):
 for name in dirs+files:
  p=Path(directory)/name;st=p.lstat();row=dict(relative=p.relative_to(A).as_posix())
  if stat.S_ISDIR(st.st_mode):row['kind']='directory'
  else:
   assert stat.S_ISREG(st.st_mode);row.update(kind='file',**m.pure(m.ref(p)))
  inventory.append(row)
assert sorted(inventory,key=lambda x:x['relative'])==t['archive_before_and_after']
assert len(positive)==3 and len(negative)==14
assert len(t['zero_and_partial_bytes'])==10
for row in t['zero_and_partial_bytes']:m.verify(A/row['relative'],row)
base=m.load(D/'AUTHOR_BASE_CHECK.json');manifest=m.ref(A/'PUBLICATION_MANIFEST.json')
assert m.pure(manifest)==m.pure(base['original_published_manifest'])
assert m.pin(m.git('show',base['published_commit']+':docs/experiments/gwosc_focused25_result_v1/PUBLICATION_MANIFEST.json'))==m.pure(manifest)
result=dict(schema='ri142-root-archive-utility-adjudication-v1',status='ACCEPT_NARROW_READ_ONLY_ARCHIVE_UTILITY',root_is_source_author=True,
 independent_nonauthor_review=m.ref(R/'HANDOFF.json'),review=m.ref(R/'INDEPENDENT_REVIEW.md'),verdict=m.ref(R/'VERDICT.json'),tests=m.ref(R/'TEST_RESULTS.json'),
 source=h['source'],readme=h['readme'],publication_subset=m.ref(R/'PUBLICATION_SUBSET.json'),base_check=m.ref(D/'AUTHOR_BASE_CHECK.json'),
 root_review='Complete 223-line source, README, independent review and test driver read; all 17 saved records reconciled against complete result, observed reviewer tool c0fe42 exit 0 and exact immutable source.',
 original_manifest=manifest,original_archive_files=135,original_archive_namespace_entries=len(inventory),original_archive_preserved=True,
 compact_review_files_including_handoff=23,counts=t['counts'],positive_cases=positive,negative_cases=negative,zero_streams=2,partial_receipts=8,
 limits=['Stable reader-controlled filesystem and reader Python/standard library premise; no adversarial containment or atomic whole-tree snapshot.',
 'Manifest and outcome mutations refuse at fixed hashes; deeper parsing and semantic guards received source review, not dynamic mutation coverage.',
 'Pinned published bytes and selected saved agreements only; not a full fresh semantic replay of all control envelopes.',
 'Historical tool origin, external dependency completeness, current runtime, calibrated science and native forward map are not established.'],
 actual_control_rerun=False,archived_subject_execution=False,runtime_capture_or_admission=False,
 active_native='RI140 source repair remains active and unaccepted, including related startup ownership path.',
 active_measurement='RI141 sealed source assigned for complete independent review; no current capture admitted.',
 programme_complete=False,ret_paused=True)
print(m.save('ROOT_ADJUDICATION.json',result))
