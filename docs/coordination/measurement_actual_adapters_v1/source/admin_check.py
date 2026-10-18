"""Author administrative pin/literal comparison only. Never imports proposal or subject."""
import difflib,hashlib,json,os
from pathlib import Path
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'ri200-root-sidecars-ofv27lvp';N=B/'ri202-root-two-maxima-review-kw07pwnj';checks=0

def check(ok,label):
 global checks
 checks+=1
 if not ok:raise ValueError(label)
def load(p):return json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
rows={}
def keep(r):
 r={k:r[k] for k in ('path','bytes','sha256')};p=Path(r['path']);check(pin(p)==r,'whole pinned bytes '+str(p));check(not p.is_symlink() and p.resolve()==p,'literal source '+str(p));check(r['path'] not in rows or rows[r['path']]==r,'duplicate identity');rows[r['path']]=r

def refs(v):
 if type(v) is dict:
  if {'path','bytes','sha256'}<=set(v):keep(v);return
  if set(v)=={'path','pin'} and type(v['pin']) is dict and set(v['pin'])=={'bytes','sha256'}:keep(dict(path=v['path'],**v['pin']));return
  for item in v.values():refs(item)
 elif type(v) is list:
  for item in v:refs(item)
seeds=load(W/'CLOSURE_SEEDS.json');check(len(seeds['administrative_records'])==33,'33 seeds')
for row in seeds['administrative_records']:keep(row)
prior=load(O/'SOURCES_BEFORE.json');sup=load(O/'CLOSURE_SUPPLEMENT.json')
check(len(prior['sources'])==659 and len(sup['current_additional_identities'])==9 and len(sup['prior_role_rows'])==810,'original closure counts')
for row in prior['sources']+sup['current_additional_identities']+sup['prior_role_rows']:keep(row)
for row in seeds['administrative_records']:
 if Path(row['path']).name in ('SIDECARS_ADJUDICATION.json','INDEPENDENT_SIDECARS_REVIEW.json','ACTUAL_SIDECARS_ROOT_REVIEW.json','GENUINE_TERMINAL_ARGUMENTS.json','ADAPTERS_REQUEST.json','RELOCATED_SOURCE_DECISION.json','INDEPENDENT_MEASUREMENT_INPUT_REVIEW.json','MEASUREMENT_NEXT_ACTION.json'):refs(load(row['path']))
q=load(N/'ADAPTERS_REQUEST.json');check(pin(N/'ADAPTERS_REQUEST.json')==seeds['request'],'exact request');check(set(q)=={'root_decisions','profiles_acceptance','sidecars'},'three requestkeys')
for key in ('source_review','guard_path_review','runtime_applicability'):refs(load(q['root_decisions'][key]['path']))
g=load(B/'ri154-white-mode-preparation-42_uvw15/BINDING_GRAPH.source-only.json');check(q['root_decisions']['packet_handoff']==g['evidence']['ri130_handoff'],'original caller handoff')
# All exact consumer FilePins must be covered; no referenced scientific body is parsed.
required=[]
def needpin(row):required.append(row);check(row['path'] in rows,'required consumer read is in declared closure '+row['path']);check(rows[row['path']]=={k:row[k] for k in ('path','bytes','sha256')},'consumer read exact pin')
for r in q['root_decisions'].values():needpin(r)
for r in q['sidecars'].values():needpin(r)
needpin(q['profiles_acceptance']);a=load(q['profiles_acceptance']['path']);needpin(a['independent_review']);needpin(g['evidence']['profiles_acceptance'])
for mode in ('profile_normal','profile_optimized'):
 needpin(a['completions'][mode]);needpin(a['genuine_outer'][mode]);c=load(a['completions'][mode]['path']);outer=load(a['genuine_outer'][mode]['path']);needpin(outer['raw_tool_receipt'])
 for r in c['artifacts'].values():needpin(r)
app=load(q['root_decisions']['runtime_applicability']['path']);needpin(app['independent_review']);guard=load(q['root_decisions']['guard_path_review']['path'])
for k in ('source_review','independent_review'):needpin(guard[k])
needpin(g['evidence']['guard_acceptance']);oldguard=load(g['evidence']['guard_acceptance']['path'])
for k in ('report','genuine_outer','independent_review'):needpin(oldguard[k])
texts={name:(W/name).read_text() for name in ('prepare_adapters.py','predispatch.py','check_adapters.py')}
check("action='adapters'" in texts['prepare_adapters.py'],'adapter action');check("operation=B/'ri156-operation-ri204-adapters-f04k2tg9'" in texts['prepare_adapters.py'],'exact fresh operation');check('alarm 960; exec @ARGV; die $!;' in texts['prepare_adapters.py'],'outer960');check("'ADAPTERS', 180, expected_environment)" in texts['prepare_adapters.py'],'child180');check("produced_names=['ATTEMPT.json','RESULT.json']" in texts['check_adapters.py'],'two produced plus COMPLETE');check("all_seven_independent_tails_passed=True" in texts['check_adapters.py'],'seven tails');check("len(caller)==11 and len(runtime_candidate)==23" in texts['check_adapters.py'],'closed candidate counts');check("(out/'RESULT.json').read_bytes()==m.canonical(expected)" in texts['check_adapters.py'],'whole canonical result');check("source_supplement=m.ref(D/'CLOSURE_SUPPLEMENT.json')" in texts['prepare_adapters.py'],'supplement pinned preflight')
for name in ('predispatch.py','check_adapters.py'):check("preflight['source_supplement']==m.ref(D/'CLOSURE_SUPPLEMENT.json')" in texts[name],'supplement reconciliation '+name)
patch=''.join(''.join(difflib.unified_diff((O/original).read_text().splitlines(True),texts[new].splitlines(True),fromfile=str(O/original),tofile=str(W/new))) for new,original in [('prepare_adapters.py','prepare_sidecars.py'),('predispatch.py','predispatch.py'),('check_adapters.py','check_sidecars.py')]);check(patch==(W/'SOURCE_DIFF.patch').read_text(),'entire exact delta')
check(not os.path.lexists(B/'ri156-operation-ri204-adapters-f04k2tg9'),'no actual operation');check(all(not os.path.lexists(W.parent/n) for n in ('ADMIT_ADAPTERS.json','DISPATCH.json','ADAPTERS_BOOTSTRAP.py','BOOTSTRAP_PREFLIGHT.json','monitor','tmp')),'no issued active artifacts')
report=dict(schema='ri204-author-administrative-check-v1',status='PASS_SOURCE_PIN_AND_LITERAL_CHECKS_ONLY',checks=checks,distinct_pinned_inputs_checked=len(rows),consumer_read_pins_covered=len(required),seeds=33,prior_source_rows=659,prior_supplement_rows=9,older_role_rows=810,generated_sources_imported_compiled_or_run=False,subject_execution=False,scientific_body_decoding=False,fresh_operational_vendor_host_observation=False,active_admission_created=False,E_mutated=False,source_pins=[pin(W/n) for n in texts],request=seeds['request'])
with (W/'AUTHOR_ADMIN_CHECK.json').open('x') as f:f.write(json.dumps(report,sort_keys=True,indent=2)+'\n')
print(json.dumps(report,sort_keys=True,indent=2))
