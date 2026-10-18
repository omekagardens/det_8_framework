"""Root administrative identities and source-text evidence only; no target load."""
import importlib.util
from pathlib import Path
sp=importlib.util.spec_from_file_location('metadata','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=Path(__file__).resolve().parent
S=m.B/'ri133-white-runtime-preparation-source-lrck33ys';R=m.B/'ri133-runtime-preparation-independent-review-ipnnpdq6'
source_pin=dict(bytes=5719,sha256='480188c24c2b4a0062e7a1b882d8a11eb1f7786c987224d23d22ece22927be59')
review_pin=dict(bytes=3228,sha256='b4b567c416e4879d1a4e67a9400a3641a1e7b7924454d82dcacade88fc7a8178')
packets=[]
for base,pin,count in [(S,source_pin,10),(R,review_pin,9)]:
 identities=[m.verify(base/'HANDOFF.json',pin)];h=m.load(base/'HANDOFF.json');names={'HANDOFF.json'}
 for row in h['artifacts']:
  p=Path(row['path']);assert p.parent==base;names.add(p.name);identities.append(m.verify(p,row))
 assert len(names)==count and {p.name for p in base.iterdir()}==names
 assert all(p.is_file() and not p.is_symlink() for p in base.iterdir())
 packets.append(dict(root=str(base),files=identities,exact_namespace=True))
deps=m.load(S/'DEPENDENCIES.source-only.json');rows=deps['opaque_files'];assert len(rows)==len({x['path'] for x in rows})==228
identities=[m.verify(x['path'],x) for x in rows];assert sum(x['bytes'] for x in identities)==15474401
findings=m.load(R/'FINDING_EVIDENCE.json');history={k:m.verify(findings[k]['path'],findings[k]) for k in ('historical_checker','historical_handoff','historical_interpreter')}
hpin=m.pure(history['historical_interpreter']);hpath=history['historical_interpreter']['path'];assert hpath not in {x['path'] for x in rows}
def refs(x):
 if isinstance(x,dict):
  if {'path','bytes','sha256'}<=x.keys():yield x
  for v in x.values():yield from refs(v)
 elif isinstance(x,list):
  for v in x:yield from refs(v)
assert any(x['path']==hpath and m.pure(x)==hpin for x in refs(m.load(history['historical_handoff']['path'])))
p=(S/'prepare.py').read_text();rt=(S/'runtime_metadata.py').read_text();old=Path(history['historical_checker']['path']).read_text()
assert len(p.splitlines())==653 and len(rt.splitlines())==391
run=p[p.index('def run(path):'):p.index('\ndef main():')];lines=run.splitlines()
pos={k:next(i for i,line in enumerate(lines) if line.startswith(prefix)) for k,prefix in [('ownership','    out.mkdir('),('admission_read','    admission_ref = ref('),('attempt','    save(out/\'ATTEMPT.json\''),('try','    try:'),('finally','    finally:')]}
assert pos['ownership']<pos['admission_read']<pos['attempt']<pos['try']<pos['finally'];assert "'sources': source_set()" in lines[pos['attempt']]
assert not any(line.startswith(('    try:', '    except', '    finally:')) for line in lines[pos['ownership']:pos['try']])
snapshot=rt[rt.index('def snapshot(dependencies):'):];assert snapshot.count('interpreter = binding(')==1
assert "same(binding(VENV + '/bin/python'), interpreter, 'interpreter binding drift')" in snapshot
assert 'INTERPRETER_BINDING' not in rt and 'historical_interpreter' not in rt
assert "ROOTS = [STDLIB, VENV + '/lib/python3.11/site-packages', '/opt/homebrew/lib/python3.11/site-packages']" in rt
assert "interpreter = m.load(C/'INTERPRETER_BINDING.candidate.json')" in old and "require(binding(interpreter['named_path']) == interpreter, 'interpreter changed')" in old
binding=m.load(hpath);assert set(binding)=={'named_path','resolved_path','symlink_chain','target'} and len(binding['symlink_chain'])==4
review=m.load(R/'INDEPENDENT_SOURCE_REVIEW.json');assert review['status']=='REPAIR_REQUIRED_BEFORE_PREPARATION_ADMISSION'
assert [x['id'] for x in review['findings']]==['F01','F02'];assert review['coverage']['independent_metadata_predicates']==465
report=dict(schema='ri133-root-source-findings-reconciliation-v1',status='TWO_SOURCE_BLOCKERS_CONFIRMED',packets=packets,dependencies=identities,dependency_count=228,dependency_bytes=15474401,historical_finding_evidence=history,historical_interpreter_pin_in_authentic_handoff=True,historical_interpreter_absent_from_source_dependency_closure=True,source_control_flow_offsets=pos,complete_nonauthor_review_lines=1044,reviewer_reported_metadata_predicates=465,root_read_scope='Entire independent review, metadata disposition, complete run/failure-tail and snapshot functions, historical checker and authentic binding; root does not claim a second full 1044-line review.',source_runtime_or_scientific_execution=False,current_runtime_observed=False,bootstrap_helper=m.ref(m.B/'ri122-root-execution-review-6whn_vky/metadata.py'))
print(m.save('ROOT_REVIEW_RECONCILIATION.json',report))
