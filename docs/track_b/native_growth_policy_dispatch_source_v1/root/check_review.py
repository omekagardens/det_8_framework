"""Root opaque identities and ordinary-text correspondence only."""
import importlib.util, re
from pathlib import Path
from collections import Counter
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
Q=m.B/'ri136-native-policy-dispatch-source-g_z472z7';R=m.B/'ri136-dispatch-independent-review-s5t7rk5z';A=m.B/'ri134-native-validator-extraction-source-y8kwkcde'
def packet(p,size,digest):
 h=m.verify(p/'HANDOFF.json',dict(bytes=size,sha256=digest));rows=[m.verify(x['path'],x) for x in m.load(p/'HANDOFF.json')['files']]+[h]
 assert sorted(str(x) for x in p.iterdir())==sorted(x['path'] for x in rows)
 assert all(not x['symlink_chain'] for x in rows)
 return rows
source=packet(Q,11534,'748b0e5e7b309705d5a6daf0aaaf6b89dce071f95af4fe3f4b9cb572a6f9ae18')
review=packet(R,3086,'e64a15ac7f69e027e09d3e7f7fa99dfcfd21fe58fbe242ebf82a398e33b9f244')
d=m.load(Q/'SOURCE_DEPENDENCIES.json');old=m.load(A/'SOURCE_DEPENDENCIES.json');entries=d['protected_files'];prior=old['protected_files']
assert len(entries)==373 and len(prior)==343
index={x['path']:x for x in entries};assert list(index)==sorted(index) and len(index)==373
observations=[m.verify(x['identity']['path'],x['identity']) for x in entries]
for n,x in enumerate(entries,1):assert x['path']==x['identity']['path'] and x['role']=='dep_%04d'%n
for x in prior:assert {k:v for k,v in x.items() if k!='role'}=={k:v for k,v in index[x['path']].items() if k!='role'}
adds=[x for x in entries if x['path'] not in {y['path'] for y in prior}];assert len(adds)==30
def refs(v):
 if type(v) is dict:
  if {'path','bytes','sha256'}<=v.keys() and type(v['path']) is str and type(v['bytes']) is int and type(v['sha256']) is str:yield v
  for x in v.values():yield from refs(x)
 elif type(v) is list:
  for x in v:yield from refs(x)
refcounts=[]
for row in adds:
 if row['access_policy']=='metadata-identities-only-no-scientific-body-decoding':
  rr=list(refs(m.load(row['path'])))
  for x in rr:assert all(x[k]==index[x['path']]['identity'][k] for k in ('path','bytes','sha256'))
  refcounts.append(dict(path=row['path'],count=len(rr)))
assert len(refcounts)==11 and sum(x['count'] for x in refcounts)==785
manifest=m.load(Q/'SOURCE_IDENTITIES.json');manifest_refs=[m.verify(x['path'],x) for x in refs(manifest)];assert len(manifest_refs)==14
cases={}
for side,count in [('native',77),('audit',62)]:
 t=Path(manifest['subjects'][side]['controls']['path']).read_text()
 triples=[dict(zip(('id','family','mutation'),x)) for x in re.findall(r"^    _case\('([^']+)', '([^']+)', '([^']+)'",t,re.M)]
 assert len(triples)==len({x['id'] for x in triples})==count and triples==manifest['subjects'][side]['ordered_cases']
 cases[side]=triples
cor=m.load(Q/'SOURCE_CORRESPONDENCE.json');a=Path(cor['old_source']['path']).read_text();b=Path(cor['new_source']['path']).read_text()
for key in ('old_source','new_source','complete_delta'):m.verify(cor[key]['path'],cor[key])
def span(text,name):
 hit=re.search(r'^def '+re.escape(name)+r'\(',text,re.M)
 if hit is None:return None
 tail=text[hit.start():];nxt=re.search(r'\n(?=def |class |if __name__)',tail);chunk=tail[:nxt.start()+1] if nxt else tail
 return dict(start_line=text[:hit.start()].count('\n')+1,**m.pin(chunk.encode()))
for row in cor['functions']:
 aa=span(a,row['name']);bb=span(b,row['name']);assert aa==row['old'] and bb==row['new']
 cls='NEW_FUNCTION' if aa is None else 'EXACT_RETAINED_TEXT' if aa['sha256']==bb['sha256'] else 'ADAPTED_FUNCTION'
 assert row['classification']==cls
classes=dict(Counter(x['classification'] for x in cor['functions']));assert classes==dict(EXACT_RETAINED_TEXT=6,ADAPTED_FUNCTION=5,NEW_FUNCTION=5)
patch=(Q/'DISPATCHER_DELTA.patch').read_text().splitlines(keepends=True);oldlines=a.splitlines(keepends=True);out=[];cursor=0;i=2;hunks=0
while i<len(patch):
 h=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n',patch[i]);assert h
 start=int(h[1])-1;out.extend(oldlines[cursor:start]);cursor=start;i+=1;before=after=0
 while i<len(patch) and not patch[i].startswith('@@ '):
  line=patch[i];assert line[0] in ' +-'
  if line[0] in ' -':assert oldlines[cursor]==line[1:];cursor+=1;before+=1
  if line[0] in ' +':out.append(line[1:]);after+=1
  i+=1
 assert before==int(h[2] or 1) and after==int(h[4] or 1);hunks+=1
out.extend(oldlines[cursor:]);assert ''.join(out)==b and hunks==7
assert b.count('helper.run_case(caller, case_id)')==1
assert b.index("'authorized case triple differs'")<b.index('helper, control_id = load_exact_module')<b.index('caller, caller_id = load_exact_module')<b.index('helper.run_case(caller, case_id)')
for row in source+review+observations+manifest_refs:assert m.identity(row['path'])==row
print(m.save('ROOT_REVIEW_RECONCILIATION.json',dict(schema='ri136-root-opaque-text-reconciliation-v1',status='PASS',checker=m.ref(__file__),source=source,review=review,dependencies=observations,dependency_count=373,unchanged_inherited=343,additions=30,new_admin_reference_counts=refcounts,new_refs=785,manifest_references=manifest_refs,literal_cases=cases,whole_delta_reconstructed=True,patch_hunks=7,function_classes=classes,single_real_call_after_exact_selection=True,final_identity_state_unchanged=True,old145_body_traversal_repeated=False,source_execution=False,controls_executed=0,current_runtime_observed=False,scientific_body_decode=False)))
