"""Root independent source correspondence and opaque custody; never loads targets."""
import importlib.util,re
from pathlib import Path
sp=importlib.util.spec_from_file_location('metadata','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=Path(__file__).resolve().parent
S=m.B/'ri134-native-validator-extraction-source-y8kwkcde';R=m.B/'ri134-native-extraction-independent-review-mcwy0ya3';P=m.B/'ri129-native-sign-caller-source-8TksBLo0'
packets=[]
for base,count,pin in [(S,17,dict(bytes=14101,sha256='3dd25f629fffe6bf23491bfb98987df75870f180ccd2733d5011fde6abf882ac')),(R,8,dict(bytes=3009,sha256='ea6e42b1a61c990eede360b649491dfff3de88aca2cdb7599246e148971086f1'))]:
 files=[m.verify(base/'HANDOFF.json',pin)];h=m.load(base/'HANDOFF.json')
 for row in h['files']:
  assert Path(row['path']).parent==base;files.append(m.verify(row['path'],row))
 assert {x.name for x in base.iterdir()}=={Path(x['path']).name for x in files} and len(files)==count
 assert all(x['symlink_chain']==[] and x['resolved_path']==x['path'] for x in files)
 packets.append(dict(path=str(base),files=files,exact_namespace=True))
d=m.load(S/'SOURCE_DEPENDENCIES.json');old=m.load(P/'SOURCE_DEPENDENCIES.json');rows=d['protected_files'];oldrows=old['protected_files'];assert len(rows)==343 and len(oldrows)==299
index={x['path']:x for x in rows};assert len(index)==343
identities=[m.verify(x['path'],x['identity']) for x in rows]
assert all(not x['symlink_chain'] and x['resolved_path']==x['path'] for x in identities)
for row in oldrows:assert {k:v for k,v in row.items() if k!='role'}=={k:v for k,v in index[row['path']].items() if k!='role'}
assert {k:v for k,v in d.items() if k!='protected_files'}=={k:v for k,v in old.items() if k!='protected_files'}
assert [x['path'] for x in rows]==sorted(index) and [x['role'] for x in rows]==['dep_%04d'%i for i in range(1,344)]
meta=m.load(R/'OPAQUE_TEXT_REVIEW.json');namespaces=[]
for ns in meta['predecessor_namespaces']:
 names=sorted(str(p) for p in Path(ns['path']).iterdir());assert names==ns['members'] and len(names)==ns['count'];assert set(names)<=set(index);namespaces.append(ns)
assert [x['count'] for x in namespaces]==[13,9,11,6]
projections=[]
for c in m.load(S/'SOURCE_CORRESPONDENCE.json')['callers']:
 for key in ['old_source','new_source']:m.verify(c[key]['path'],c[key])
 oldlines=Path(c['old_source']['path']).read_text().splitlines(keepends=True);newlines=Path(c['new_source']['path']).read_text().splitlines(keepends=True);replaced={};removed=set()
 for item in c['four_moved_blocks']:
  oldblock=item['old_block'];newblock=item['new_function'];ob=oldlines[oldblock['start_line']-1:oldblock['end_line']];nb=newlines[newblock['start_line']-1:newblock['end_line']]
  assert m.pin(''.join(ob).encode())==m.pure(oldblock) and m.pin(''.join(nb).encode())==m.pure(newblock)
  assert nb[0].startswith('def '+item['function']+'(');body=nb[1:]
  if item['one_line_docstring_excluded'] is not None:assert body[0].rstrip('\n')==item['one_line_docstring_excluded'];body=body[1:]
  while body and not body[-1].strip():body.pop()
  if item['dependency_return_entries_added']:assert body.pop()=='    return entries\n'
  expected=[x[item['common_indent_removed_from_old']:] if x.strip() else x for x in ob]
  while expected and not expected[-1].strip():expected.pop()
  assert body==expected,'moved body differs'
  lineno=item['production_call_line'];assert newlines[lineno-1].strip()==item['production_call'];replaced[lineno]=''.join(ob);removed.update(range(newblock['start_line'],newblock['end_line']+1))
 projected=''.join(replaced.get(i,line) for i,line in enumerate(newlines,1) if i not in removed).splitlines(keepends=True)
 for i,line in enumerate(projected):
  if i==1:projected[i]=oldlines[1]
  elif line.startswith(('E = Path(', 'DEPENDENCIES_BYTES = ', 'DEPENDENCIES_SHA256 = ')):
   prefix=line.split('=')[0]+'=';matching=[x for x in oldlines if x.startswith(prefix)];assert len(matching)==1;projected[i]=matching[0]
 assert projected==oldlines,'whole source reconstruction differs'
 projections.append(dict(caller=c['caller'],old_source=c['old_source'],new_source=c['new_source'],moved_bodies_and_calls=4,full_projection=m.pin(''.join(projected).encode())))
coverage=[]
for who,fn,rowskey,caseskey,expected_decl,expected_case in [('native','supervise.py','declarations','direct_case_inventory',52,77),('audit','launch_audit.py','rows','ordered_case_inventory',69,62)]:
 v=m.load(S/(who+'_coverage.json'));text=(S/fn).read_text();oldtext=(P/fn).read_text();block=text.split('CONTROL_DECLARATIONS = (\n',1)[1].split('\n)\n',1)[0];assert block==oldtext.split('CONTROL_DECLARATIONS = (\n',1)[1].split('\n)\n',1)[0]
 r=v[rowskey];assert len(r)==len(block.splitlines())==expected_decl
 for line,row in zip(block.splitlines(),r):assert line=='    ('+', '.join(repr(row['declaration'][k]) for k in ['name','function','code','condition'])+'),'
 triples=re.findall(r"^    _case\('([^']*)', '([^']*)', '([^']*)'",(S/(who+'_policy_controls.py')).read_text(),re.M)
 assert [dict(zip(['id','family','mutation'],t)) for t in triples]==v[caseskey] and len(triples)==expected_case
 coverage.append(dict(caller=who,declarations=expected_decl,prospective_cases=expected_case))
review=m.load(R/'INDEPENDENT_SOURCE_REVIEW.json');assert review['status']=='PASS_BOUNDED_UNEXECUTED_SOURCE_ONLY' and review['blocking_findings']==[] and review['prospective_controls']['executed']==0
assert meta['administrative_closure']['reference_occurrences']==115670 and meta['administrative_closure']['bodies']==145 and meta['administrative_closure']['failures']==[]
print(m.save('ROOT_REVIEW_RECONCILIATION.json',dict(schema='ri134-root-source-reconciliation-v1',status='PASS_BOUNDED_SOURCE_CORRESPONDENCE_AND_CUSTODY',packets=packets,dependencies=identities,inherited_unchanged=299,added=44,namespaces=namespaces,projections=projections,coverage=coverage,independent_reviewer_admin_closure=dict(bodies=145,references=115670,root_reexecuted_this_traversal=False,reviewer_helper_read=True,reviewer_report=m.ref(R/'OPAQUE_TEXT_REVIEW.json')),root_scope='Complete independent review and metadata-checker source; extraction bodies, call contexts, complete native delta, supplied audit delta and both control dispatch tails; full prior RI132 runner. Root separately rechecked all343 dependencies, namespaces, eight bodies/calls, whole reverse projections and literal declaration/case inventories. Complete3708-line nonauthor review and manual139-case trace belong to the separate reviewer.',current_runtime_observed=False,target_import_compile_ast_probe_execution=False,scientific_body_decode=False)))
