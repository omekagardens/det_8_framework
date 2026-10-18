"""Root RI144 metadata and text only, without subject evaluation."""
import importlib.util,re,difflib
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);D=Path(__file__).resolve().parent;m.D=D;B=D.parent
S=B/'ri144-bootstrap-guard-source-oaj1jvyt';h=m.load(S/'HANDOFF.json');deps=m.load(S/'DEPENDENCIES.source-only.json');old=m.load(B/'ri141-white-bootstrap-source-h58ls076/DEPENDENCIES.source-only.json')
assert sorted(x.name for x in S.iterdir())==h['exact_namespace']
observations=[m.verify(r['path'],r) for r in h['files']+deps['opaque_files']]+[m.identity(S/'HANDOFF.json')]
by={r['path']:r for r in deps['opaque_files']};assert len(by)==472
for r in old['opaque_files']:assert by[r['path']]==r
assert len(old['opaque_files'])==442
c=m.load(S/'SOURCE_CORRESPONDENCE.json');pre=Path(c['before']['path']).read_bytes();post=Path(c['after']['path']).read_bytes();control=Path(c['new_control_source']['path']).read_bytes()
for row in c['unchanged_existing_definition_spans']:
 a,z=row['before_lines'];x,y=row['after_lines'];left=b''.join(pre.splitlines(keepends=True)[a-1:z]);right=b''.join(post.splitlines(keepends=True)[x-1:y]);assert left==right and m.pin(right)==m.pure(row)
assert len(c['unchanged_existing_definition_spans'])==14
for key,source in [('qualified_monitor_unchanged_function',Path(c['qualified_monitor_whole_source']['path']).read_bytes()),('exact_target_selected_bootstrap',Path(c['exact_target_module']['path']).read_bytes())]:
 row=c[key];assert m.pin(b''.join(source.splitlines(keepends=True)[row['start']-1:row['end']]))==m.pure(row)
for row in [c['qualified_monitor_whole_source'],c['exact_target_module'],c['new_control_source'],c['before'],c['after']]:m.verify(row['path'],row)
# Independently reconstruct the complete two-part unified patch as ordinary text.
ls=(S/'REPAIR.diff').read_text().splitlines(keepends=True);at=0;patches=[]
while at<len(ls):
 assert ls[at].startswith('--- ');before=ls[at][4:].strip();after=ls[at+1][4:].strip();assert ls[at+1].startswith('+++ ');at+=2
 src=[] if before=='/dev/null' else Path(before).read_text().splitlines(keepends=True);out=[];cursor=0
 while at<len(ls) and not ls[at].startswith('--- '):
  z=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n',ls[at]);assert z
  os,oc,ns,nc=map(int,[z[1],z[2] or '1',z[3],z[4] or '1']);at+=1;start=os-1 if oc else os
  assert start>=cursor;out.extend(src[cursor:start]);cursor=start;oldcount=newcount=0
  while at<len(ls) and not ls[at].startswith(('@@ ','--- ')):
   line=ls[at];at+=1;kind=line[0];body=line[1:];assert kind in ' +-'
   if kind in ' -':assert src[cursor]==body;cursor+=1;oldcount+=1
   if kind in ' +':out.append(body);newcount+=1
  assert (oldcount,newcount)==(oc,nc)
 out.extend(src[cursor:]);assert ''.join(out).encode()==Path(after).read_bytes();patches.append(dict(before=before,after=after))
assert len(patches)==2
def spans(raw):
 lines=raw.splitlines(keepends=True);marks=[(i,re.match(rb'def (\w+)\(',line)[1].decode()) for i,line in enumerate(lines) if re.match(rb'def (\w+)\(',line)]
 terminal=next((i for i,l in enumerate(lines) if l.startswith(b"if __name__")),len(lines));return {n:b''.join(lines[i:(marks[k+1][0] if k+1<len(marks) else terminal)]) for k,(i,n) in enumerate(marks)}
p,q=spans(post),spans(control)
assert p['recipe']==q['recipe']
for name in c['same_13_copied_helper_spans_in_control_and_launcher']:assert p[name]==q[name]
print(m.save('ROOT_MEASUREMENT_SOURCE_CHECK.json',dict(schema='ri144-root-source-check-v1',status='PASS',source_handoff=m.ref(S/'HANDOFF.json'),dependencies=len(by),dependency_bytes=sum(r['bytes'] for r in by.values()),inherited=442,additions=30,unchanged_spans=14,identical_recipe=True,identical_helper_spans=13,full_diff=patches,observations=observations,source_execution=False,current_runtime_observed=False,scientific_body_decoded=False)))
