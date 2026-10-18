"""Author administrative source/pin check. No proposal/subject imports or evaluation."""
from pathlib import Path
import hashlib,json,difflib,os
W=Path(__file__).resolve().parent;B=W.parents[1];O=B/'ri204-root-adapters-f04k2tg9';P=O/'worker_proposal';checks=0

def check(x,label):
 global checks
 checks+=1
 if not x:raise ValueError(label)
def ld(p):return json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
rows={}
def keep(r):
 r={k:r[k] for k in ('path','bytes','sha256')};p=Path(r['path']);check(pin(p)==r,'opaque identity '+str(p));check(not p.is_symlink() and p.resolve()==p,'literal path');check(r['path'] not in rows or rows[r['path']]==r,'duplicate reference');rows[r['path']]=r

def refs(v):
 if type(v) is dict:
  if {'path','bytes','sha256'}<=set(v):keep(v);return
  if set(v)=={'path','pin'} and type(v['pin']) is dict and set(v['pin'])=={'bytes','sha256'}:keep(dict(path=v['path'],**v['pin']));return
  for item in v.values():refs(item)
 elif type(v) is list:
  for item in v:refs(item)
seeds=ld(W/'CLOSURE_SEEDS.json');check(len(seeds['administrative_records'])==39,'39 seeds')
for r in seeds['administrative_records']:keep(r)
prior=ld(O/'SOURCES_BEFORE.json');sup=ld(O/'CLOSURE_SUPPLEMENT.json');check(len(prior['sources'])==722 and len(sup['prior_role_rows'])==810,'722/810')
for r in prior['sources']+sup['prior_role_rows']:keep(r)
for r in seeds['administrative_records']:
 if Path(r['path']).name in ('ADAPTERS_ACCEPTANCE.json','FREEZE_REQUEST.json','RI206_MEASUREMENT_ASSIGNMENT.json','ROOT_PREPARATION_DECISION.json','INDEPENDENT_PREPARATION_REVIEW.json','INDEPENDENT_CONCRETE_PREFLIGHT_REVIEW.json','INDEPENDENT_ACTUAL_ADAPTERS_REVIEW.json','ACTUAL_ADAPTERS_POSTCHECK.json','GENUINE_TERMINAL_ARGUMENTS.json','MEASUREMENT_NEXT_ACTION.json'):refs(ld(r['path']))
request=ld(seeds['request']['path']);accepted=ld(seeds['adapters_acceptance']['path']);check(request['accepted_adapters']==accepted['accepted_adapters'],'accepted exact three refs');check(set(request)=={'accepted_adapters'} and set(request['accepted_adapters'])=={'caller','guards','runtime'},'closed request');cards={}
for key,r in request['accepted_adapters'].items():keep(r);cards[key]=ld(r['path']);refs(cards[key])
g=ld(B/'ri154-white-mode-preparation-42_uvw15/BINDING_GRAPH.source-only.json');E=Path(g['prospective_root'])
required=[]
def needpin(r):
 required.append(r);check(r['path'] in rows,'consumer reference in proposed closure '+r['path']);check(rows[r['path']]=={k:r[k] for k in ('path','bytes','sha256')},'consumer exact pin')
for r in request['accepted_adapters'].values():needpin(r)
needpin(g['integrated_root'])
for n in ('TARGET_CLOSURE.source-only.json','HISTORY_CLOSURE.source-only.json'):needpin(pin(E/n))
t=ld(E/'TARGET_CLOSURE.source-only.json');h=ld(E/'HISTORY_CLOSURE.source-only.json');check(len(h)==124 and len(t['sources'])==30,'source declaration domains')
for r in h:needpin(r)
for k in ('source_review','packet_handoff'):needpin(cards['caller'][k])
for k in ('report','genuine_outer','independent_review'):needpin(cards['guards'][k])
for k in ('profile_normal','profile_optimized','profile_review','selection','optional_namespaces','observed_dyld_routes','host_scope'):needpin(cards['runtime'][k])
for r in g['helpers']:needpin(dict(path=r['path'],**r['pin']))
check(len(g['copied_files'])==48 and len(g['helpers'])==11 and len(g['sources'])==30 and len(g['stage_bindings'])==17,'graph domains')
# Source text only; no compile, AST, eval or candidate construction.
texts={n:(W/n).read_text() for n in ('prepare_freeze.py','predispatch.py','check_freeze.py')}
consumer=(B/'ri160-white-fixture-custody-repair-ufok1zpo/retained_contract.py').read_text()
for literal in ["PHASE = 'fabricated_white_qualification'","CONTEXT = 'RI125_FABRICATED_ONLY_NOT_HISTORICAL'","CLAIM = 'Fixed fabricated WHITE qualification only; full32 application, actual data and physical claims remain unqualified; RET paused.'"]:check(literal in consumer,'literal retained constant')
for label,needle in [('closed17','assert len(expected)==17'),('run9',"len(r)==9"),('wholecanonical',"(out/'RESULT.json').read_bytes()==m.canonical(expected)"),('history124','assert len(history)==124'),('allguard65','assert len(guard_ids)==65'),('freezeabsent',"assert not os.path.lexists(root/'AUTHORIZED_FREEZE.json')"),('correctenvironment',"'TMPDIR':str(root/'tmp')"),('normaloptimized',"(['-O'] if mode=='optimized' else [])")]:check(needle in texts['check_freeze.py'],label)
for needle in ["action='freeze'","ADMIT_FREEZE_CANDIDATE.json","ri156-operation-ri206-freeze-5e_n5lj_","alarm 960; exec @ARGV; die $!;","'FREEZE', 180, expected_environment)","len(prior_sources['sources'])==722","len(prior_supplement['prior_role_rows'])==810"]:check(needle in texts['prepare_freeze.py'],'preparation literal '+needle)
patch=''.join(''.join(difflib.unified_diff((P/orig).read_text().splitlines(True),texts[new].splitlines(True),fromfile=str(P/orig),tofile=str(W/new))) for new,orig in [('prepare_freeze.py','prepare_adapters.py'),('predispatch.py','predispatch.py'),('check_freeze.py','check_adapters.py')]);check(patch==(W/'SOURCE_DIFF.patch').read_text(),'complete exact source delta')
check(not os.path.lexists(B/'ri156-operation-ri206-freeze-5e_n5lj_'),'no RI206 operation');check(all(not os.path.lexists(W.parent/n) for n in ('ADMIT_FREEZE_CANDIDATE.json','FREEZE_BOOTSTRAP.py','DISPATCH.json','BOOTSTRAP_PREFLIGHT.json','monitor','tmp')),'no active root artifacts');check(all(not os.path.lexists(E/n) for n in ('AUTHORIZED_FREEZE.json','ADMIT_NORMAL.json','ADMIT_OPTIMIZED.json')),'E admission paths absent')
value=dict(schema='ri206-author-administrative-source-check-v1',status='PASS_SOURCE_PINS_AND_LITERALS_ONLY',checks=checks,distinct_pinned_inputs=len(rows),required_consumer_read_pins=len(required),seed_count=39,current_prior_source_rows=722,historical_role_rows=810,source_declaration_history_rows=124,proposal_import_compile_AST_or_execution=False,subject_or_vendor_execution=False,scientific_body_decoding=False,fixture_generation=False,fresh_operational_runtime_or_host_observation=False,admissions_created=False,E_modified=False,source_pins=[pin(W/n) for n in texts])
with (W/'AUTHOR_ADMIN_CHECK.json').open('x') as f:f.write(json.dumps(value,sort_keys=True,indent=2)+'\n')
print(json.dumps(value,sort_keys=True,indent=2))
