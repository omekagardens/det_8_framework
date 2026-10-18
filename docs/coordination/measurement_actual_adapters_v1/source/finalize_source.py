"""Author-only text refinements and exact diff generation, no proposed script execution."""
from pathlib import Path
import difflib
W=Path(__file__).resolve().parent;O=W.parents[1]/'ri200-root-sidecars-ofv27lvp'
def update(name,old,new):
 p=W/name;s=p.read_text();assert s.count(old)==1,(name,old,s.count(old));p.write_text(s.replace(old,new))
update('prepare_adapters.py',"source_observation=m.ref(D/'SOURCES_BEFORE.json'),runtime_observation=runtime", "source_observation=m.ref(D/'SOURCES_BEFORE.json'),source_supplement=m.ref(D/'CLOSURE_SUPPLEMENT.json'),runtime_observation=runtime")
for name in ('predispatch.py','check_adapters.py'):
 update(name,"supplement=m.load(D/'CLOSURE_SUPPLEMENT.json')", """supplement=m.load(D/'CLOSURE_SUPPLEMENT.json')
preflight=m.load(dispatch['preflight']['path'])
assert preflight['source_observation']==m.ref(D/'SOURCES_BEFORE.json')
assert preflight['source_supplement']==m.ref(D/'CLOSURE_SUPPLEMENT.json')
assert preflight['runtime_observation']==m.ref(D/'RUNTIME_BEFORE.json')
assert preflight['E_observation']==m.ref(D/'E_BEFORE.json')""")
update('check_adapters.py',"assert complete['schema']=='ri156-adapter-completion-v1'", """assert set(complete)=={'schema','action','status','admission','artifacts','first_error','independent_tails','elapsed_seconds_before_complete_write','authenticated_source_before','produced_output_pins','tail_observations','scientific_execution','root_acceptance_created','ret_paused'}
assert complete['schema']=='ri156-adapter-completion-v1'""")
update('check_adapters.py',"and all(v['error'] is None for v in ct.values())", "and all(set(v)=={'value','error'} and v['error'] is None for v in ct.values())")
update('check_adapters.py',"for key in ('namespace_fixture_mismatches','namespace_member_mismatches','namespace_output_mismatches'):assert complete['tail_observations'][key]==[]", """assert set(complete['tail_observations'])=={'sources','outputs','namespace','namespace_fixture_mismatches','namespace_member_mismatches','namespace_output_mismatches'}
for key in ('namespace_fixture_mismatches','namespace_member_mismatches','namespace_output_mismatches'):assert complete['tail_observations'][key]==[]""")
update('check_adapters.py',"assert trees['E']==m.load(D/'E_BEFORE.json') and list((D/'tmp').iterdir())==[]", """assert trees['E']==m.load(D/'E_BEFORE.json') and list((D/'tmp').iterdir())==[]
assert all(row['identity']['bytes']<=67108864 for key in ('operation','monitor') for row in trees[key] if row['kind']=='file')""")
patch=[]
for name,old in [('prepare_adapters.py','prepare_sidecars.py'),('predispatch.py','predispatch.py'),('check_adapters.py','check_sidecars.py')]:
 patch.extend(difflib.unified_diff((O/old).read_text().splitlines(True),(W/name).read_text().splitlines(True),fromfile=str(O/old),tofile=str(W/name)))
(W/'SOURCE_DIFF.patch').write_text(''.join(patch))
print('Final text refinements written; three proposal scripts remain unexecuted.')
