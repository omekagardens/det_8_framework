"""Root reads actual administrative refusal; no subject execution or retry."""
import importlib.util, json, os
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
d=m.load(m.D/'ROOT_DISPATCH.json');t=m.load(m.D/'GENUINE_TOOL_INITIAL.json');op=Path(d['operation'])
assert t['invocation']==d['invocation'] and t['result']['exit_code']==1 and 'session_id' not in t['result']
assert 'ValueError: actual complete environment' in t['result']['output']
assert sorted(p.name for p in op.iterdir())==['cards','environment'] and not os.path.lexists(op/'output')
assert sorted(p.name for p in (op/'environment').iterdir())==['tmp'] and list((op/'environment/tmp').iterdir())==[]
assert sorted(p.name for p in (op/'cards').iterdir())==sorted(Path(x['path']).name for x in d['cards'])
for row in d['cards']:m.verify(row['path'],row)
for row in d['copies']:
 m.verify(row['original']['path'],row['original']);m.verify(row['operational']['path'],row['operational'])
source=m.load(m.D/'ROOT_PRE_ADMISSION_SOURCE_CHECK.json')
for row in source['observations']:assert m.identity(row['path'])==row
assert (m.D/'BOOTSTRAP_PRE.json').read_bytes()==(m.D/'BOOTSTRAP_POST.json').read_bytes()
probe=m.load(m.D/'BOOTSTRAP_ENV_DIAGNOSTIC.json');assert probe['result']['exit_code']==0
actual=json.loads(probe['result']['output']);expected=m.load(op/'cards/launcher.json')['environment']
assert all(actual[k]==v for k,v in expected.items())
extras={k:actual[k] for k in actual.keys()-expected.keys()};assert set(extras)=={'CPATH','LIBRARY_PATH','MANPATH','SDKROOT'}
finding=dict(id='RI137-F01-BOOTSTRAP-ENVIRONMENT',scope='Operational bootstrap applicability failure, not an F01/F02 control outcome',actual_first_error='ValueError: actual complete environment',actual_terminal_exit=1,tool_chunk='feff2a',failure_before_control_module_load=True,controls_executed=0,owned_output_created=False,actual_monitor_called=False,post_refusal_diagnostic_extra_environment=extras,diagnostic_causality_scope='Observed through the same /usr/bin/python3 vendor entry; not a full internal xcrun trace',source_and_cards_unchanged=True,bootstrap_pre_post_exact=True,retry=False,source_review_did_not_establish_operational_applicability=True)
print(m.save('RI137_ACTUAL_REFUSAL_REVIEW.json',dict(schema='ri137-root-actual-refusal-review-v1',status='REJECT_ACTUAL_ATTEMPT_ENVIRONMENT_MISMATCH',dispatch=m.ref(m.D/'ROOT_DISPATCH.json'),genuine_tool=m.ref(m.D/'GENUINE_TOOL_INITIAL.json'),diagnostic=m.ref(m.D/'BOOTSTRAP_ENV_DIAGNOSTIC.json'),bootstrap_pre=m.ref(m.D/'BOOTSTRAP_PRE.json'),bootstrap_post=m.ref(m.D/'BOOTSTRAP_POST.json'),source_pre=m.ref(m.D/'ROOT_PRE_ADMISSION_SOURCE_CHECK.json'),finding=finding,source_repair_next='Select and bind the actual authenticated vendor interpreter entry consistently in both commands, retain exact environment equality, fresh nonauthor source review then genuine root admission before another operation.',current_runtime_qualified=False,scientific_execution=False,RET_paused=True)))
