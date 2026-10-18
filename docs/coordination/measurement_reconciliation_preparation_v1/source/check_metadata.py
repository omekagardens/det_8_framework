"""Administrative source-text/opaque-reference checker only.
No target/helper import/compile/AST/probe/run, current E walk or supplier
inventory. Only declared source/history files are hashed; only manifests,
root/source reviews and recorded administrative custody JSON are decoded.
"""
from pathlib import Path
import json,hashlib,re,difflib
B=Path('/Volumes/AI_DATA/development/det-review-evidence');W=B/'ri229-reconciliation-preparation-t93t1607/worker_proposal';D=B/'ri226-directory-custody-recovery-yvfg_p1b';S=D/'worker_proposal'
labels=[];observed={}
def canon(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def ck(ok,label):
 labels.append(label)
 if not ok:raise ValueError(label)
def eq(a,b,label):ck(canon(a)==canon(b),label)
def filepin(p):
 p=Path(p);a=p.stat();raw=p.read_bytes();z=p.stat();ck(a==z,'stable opaque read '+str(p));r=dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());observed[str(p)]=r;return r

def verify(r):eq(filepin(r['path']),{k:r[k] for k in ('path','bytes','sha256')},'complete declared pin '+r['path'])
def load(p):return json.loads(Path(p).read_bytes())
def fieldnames(line):return re.findall(r'(?:\(|,)\s*([A-Za-z_][A-Za-z_0-9]*)=',line)
def span(text,name):
 a=re.search(r'^def '+re.escape(name)+r'\(.*$',text,re.M);ck(a is not None,'function '+name);start=a.end()+1;b=re.search(r'^\S',text[start:],re.M);return text[a.start():start+b.start() if b else len(text)].rstrip()
deps=load(W/'DEPENDENCIES.json');build=load(W/'BUILD_METADATA.json');manifest=load(W/'SOURCE_PINS.json')
eq(len(deps['files']),992,'exact declared992');ck(len({r['path'] for r in deps['files']})==992,'unique dependency domain')
for r in deps['files']+list(deps['roles'].values())+manifest['files']:verify(r)
hand=load(S/'HANDOFF.json');eq(sorted(p.name for p in S.iterdir()),sorted(hand['namespace']),'entire immutable19 source namespace')
for r in hand['files']:verify(r)
review=load(D/'ROOT_SOURCE_REVIEW.json');eq(review['status'],'ACCEPT_RI226_READ_ONLY_RECONCILIATION_SOURCE_ONLY','actual source acceptance');eq(review['source_manifest'],deps['roles']['recovery_manifest'],'actual manifest binding');eq(review['packet'],deps['roles']['recovery_handoff'],'actual full packet binding');ck(review['preparation_or_execution_admitted'] is False and review['frozen_custody_accepted'] is False,'no operative acceptance inferred')
base=load(S/'INPUT_PINS.json');repair=load(S/'REPAIR_PROVENANCE.json');source_manifest=load(S/'SOURCE_PINS.json');inputs={r['path']:r for r in base['files']+repair['files']};eq(len(inputs),963,'all fixed963 input paths');eq(base['prior_role_count'],810,'all810 role rows retained')
all_deps={r['path']:r for r in deps['files']}
for path,r in inputs.items():eq(all_deps[path],r,'entire fixed input declaration preserved')
actual_rows=load(repair['roles']['original_sources']['path']);eq(len(actual_rows),904,'whole904 original source rows')
for row in actual_rows:eq(all_deps[row['path']],{k:row[k] for k in ['path','bytes','sha256']},'original source whole byte pin preserved')
prospective=set(inputs)|{r['path'] for r in source_manifest['files']}|{str(S/'SOURCE_PINS.json'),str(D/'ROOT_SOURCE_REVIEW.json'),str(D/'RECONCILE_BOOTSTRAP.py')}
eq(len(prospective),971,'closed971 future source domain by paths only');ck(str(D/'RECONCILE_BOOTSTRAP.py') not in observed,'future bootstrap not read as actual')
p=(W/'prepare_reconciliation.py').read_text();b=(W/'RECONCILE_BOOTSTRAP.source-only.py').read_text();old=Path(deps['roles']['predecessor_preparation']['path']).read_text();template=Path(deps['roles']['bootstrap_template']['path']).read_text();replaced=template
for original,new in build['bootstrap_replacements']:eq(replaced.count(original),1,'single bootstrap literal replacement');replaced=replaced.replace(original,new)
eq(replaced,b,'complete bootstrap correspondence');eq(len(build['bootstrap_replacements']),7,'exact seven replacements')
for old_text,new_text,old_path,new_path,out in [(template,b,deps['roles']['bootstrap_template']['path'],str(W/'RECONCILE_BOOTSTRAP.source-only.py'),'BOOTSTRAP_DIFF.patch'),(old,p,deps['roles']['predecessor_preparation']['path'],str(W/'prepare_reconciliation.py'),'PREPARATION_DIFF.patch')]:
 expect=''.join(difflib.unified_diff(old_text.splitlines(True),new_text.splitlines(True),fromfile=old_path,tofile=new_path));eq((W/out).read_text(),expect,'whole exact delta '+out)
for name in ['ref','eq','opaque','load','save']:eq(span(p,name),span(old,name),'whole retained preparation function '+name)
for prefix in ['ENV=','LIMITS=','VENDOR=']:
 eq(next(l for l in p.splitlines() if l.startswith(prefix)),next(l for l in old.splitlines() if l.startswith(prefix)),'retained literal '+prefix)
monitor=Path(deps['roles']['monitor']['path']).read_text();reconciler=(S/'reconcile_freeze.py').read_text();saved_checker=(S/'check_reconciliation.py').read_text()
real_popen="child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=output, stderr=errors,\n                                     cwd=out, env=env, start_new_session=True)"
ck(real_popen in monitor,'actual monitor Popen cwd=out');ck("Path.cwd()==literal(D/'monitor')" in reconciler,'actual subject exact child cwd');ck("eq(dispatch['cwd'],str(D),'outer cwd')" in saved_checker,'actual checker outer cwd')
vendor='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
expected_call='module.child_run('+repr([vendor,'-I','-B',str(S/'reconcile_freeze.py'),'--admission',str(D/'ADMIT_RECONCILE.json')])+', Path('+repr(str(D/'monitor'))+"), 'RECONCILE', 180, expected_environment)"
eq([l for l in b.splitlines() if l.startswith('module.child_run(')],[expected_call],'one exact full monitor call')
ck(b.index('hashlib.sha256(captured)')<b.index("exec(compile(captured")<b.index('module.child_run('),'whole capture hash then load then child call');ck("(1, 1, 0)" in b and "!= expected_environment" in b,'normal isolated complete environment guard')
for forbidden in ['module.run(',"import reconcile_freeze",'import check_reconciliation','subprocess.run(','m.git(','m.snapshot(','exec(compile(']:ck(forbidden not in p,'preparation has no target/process call '+forbidden)
ck('prospective_admission_pin' not in p and 'admission=card' not in p and "card=ref(" not in p,'no invented future admission pin');ck("'ADMIT_RECONCILE.json','DISPATCH.json'" in p,'no existing active outputs')
output_names=['HOST_GENUINE_TOOL.json','HOST_BEFORE.json','RECONCILE_BOOTSTRAP.py','SOURCES_BEFORE.json','SUPPLIER_BEFORE.json','E_BEFORE.json','RECONCILE_PREFLIGHT.json','RECONCILIATION_PROPOSAL.json','PREPARATION_CUSTODY.json']
eq(next(l for l in p.splitlines() if l.startswith('output_names=')),'output_names='+repr(output_names).replace(', ',','),'literal nine output whitelist')
for n in ['ADMIT_RECONCILE.json','DISPATCH.json','AUTHORIZED_FREEZE.json']:ck("save('"+n+"'" not in p and "emit('"+n+"'" not in p,'no operational writer '+n)
ck("need(p.read_bytes()==data,'saved preparation bytes')" in p,'direct complete byte readback');ck("eq(actual,produced[name],'whole captured preparation output pin')" in p,'whole output pin check');ck("'all nine actual preparation output pins'" in p and "'exact final preparation additions only'" in p,'full final output/namespace checks')
for required in ["len(original_sources)==904", "original_sources+list(original_before['bindings'].values())", "[23,24]", "eq(etree,sorted(old_E", "eq(tree(),etree,'final entire E unchanged after all preparation outputs')", "len(expected)==971", "len(namespace)==195", "len(vendor)==1810", "sum(r['bytes'] for r in vendor)==48024515", "type(observation['returncode']) is int"]:ck(required in p,'complete preparation requirement '+required)
schemas={
'pre=save(':'schema status sources supplier E_before host_tool_receipts monitor_bootstrap source_manifest environment scientific_execution',
'proposed_card=dict(':'schema status source_manifest source_review preflight output environment limits genuine_outer_required',
'proposed_dispatch=dict(':'outer_argv shell_command cwd login bootstrap monitor_source external_timeout_seconds single_attempt actual_execution_not_yet_started',
'proposal=save(':'schema status proposed_admission_fields future_admission_path dispatch_fields_without_admission active_card_created dispatch_created',
'custody=save(':'schema status sealed_source_packet root_review_support preparation_source_manifest preparation_source_review preparation_support preparation_dependency_states retained_failure retained_postflight original_genuine_host canonical_genuine_host monitor_template bootstrap_replacements cwd_contract source_domain original_source_observation original_bindings root_namespace_before root_namespace_expected_after produced_before_custody prior_roles copy_history_targets source_observations supplier_observation E_observation preflight unissued_proposal preparation_source tool_origin_and_startup_are_root_premises scientific_execution reconciliation_admitted reconciliation_dispatched E_read_only ret_paused'}
for start,fields in schemas.items():line=next(l for l in p.splitlines() if l.startswith(start));eq(fieldnames(line),fields.split(),'exact closed field declaration '+start)
eq([len(v.split()) for v in schemas.values()],[10,9,9,7,35],'exact record field counts')
# Named historical administrative observations only, without any current E walk.
oldbefore=load(repair['roles']['original_before']['path']);obs=load(repair['roles']['original_observations']['path']);post=load(repair['roles']['postflight']['path']);eq(oldbefore['E'][0],post['root_before'],'saved historical before');eq({k:obs['E_after'][0][k] for k in ('state','entries')},post['root_after'],'saved entire post root');eq([oldbefore['E'][0]['state'][3],obs['E_after'][0]['state'][3]],[23,24],'actual saved links, no fabricated platform rule')
# Check integer fidelity with actual recorded integers, not fabricated target fixtures.
eq(json.loads(canon(post)),post,'lossless actual administrative JSON integers');ck(type(post['root_after']['state'][-1]) is int and post['root_after']['state'][-1]>2**53,'actual nanosecond integer is preserved beyond float exact range')
report=dict(schema='ri229-administrative-source-check-v1',status='PASS_SOURCE_TEXT_AND_OPAQUE_METADATA_ONLY',predicates=len(labels),opaque_files=len(observed),fixed_dependencies=992,recovery_inputs=963,recovery_prospective_sources=971,original_sources_retained=904,historical_roles=810,complete_bootstrap_replacements=7,field_counts=[10,9,9,7,35],source_lines={'writer':len(p.splitlines()),'bootstrap':len(b.splitlines())},no_subject_import_compile_AST_probe_run=True,no_E_inventory_or_runtime_observation=True,no_preparation_or_admission_execution=True,no_scientific_decode=True,labels=labels,opaque_pins=[observed[k] for k in sorted(observed)])
raw=canon(report)
with (W/'METADATA_CHECK.json').open('xb') as f:f.write(raw)
assert (W/'METADATA_CHECK.json').read_bytes()==raw
print(json.dumps(dict(report=dict(path=str(W/'METADATA_CHECK.json'),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),predicates=report['predicates'],opaque_files=report['opaque_files'],status=report['status'])))
