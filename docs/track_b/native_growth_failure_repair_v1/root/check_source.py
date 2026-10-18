"""Opaque pins and literal text reconstruction only; no subject parsing/execution."""
import importlib.util
from pathlib import Path
import re
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
B=m.D.parent;S=B/'ri140-native-failure-repair-source-l_a4mna0';O=B/'ri138-native-external-launch-source-92pbd52w'
h=m.load(S/'HANDOFF.json');m.verify(S/'HANDOFF.json',dict(bytes=6044,sha256='8726a3d8be2d62b2326a6ad45d5e1f497fda521d4a1e4a9c92e04101c16f2141'))
for row in h['files']:m.verify(row['path'],row)
assert {p.name for p in S.iterdir()}=={'HANDOFF.json'}|{Path(x['path']).name for x in h['files']}
deps=m.load(S/'SOURCE_DEPENDENCIES.json')['protected_files'];old=m.load(O/'SOURCE_DEPENDENCIES.json')['protected_files']
assert len(deps)==423 and len(old)==396
current={r['path']:r for r in deps};assert len(current)==423
total=0
for i,row in enumerate(deps,1):
 assert row['role']=='dep_'+str(i).zfill(4) and row['path']==row['identity']['path']
 observed=m.verify(row['path'],row['identity']);total+=observed['bytes']
 assert observed['resolved_path']==row['identity']['resolved_path']
 assert observed['symlink_chain']==row['identity']['symlinks']
for row in old:assert {k:v for k,v in row.items() if k!='role'}=={k:v for k,v in current[row['path']].items() if k!='role'}
assert total==169620097
c=m.load(S/'SOURCE_CORRESPONDENCE.json');delta=[]
for diffname,rows in [('SOURCE_CODE.diff',c['complete_source_delta_checks']),('METADATA_CONTRACT.diff',c['complete_shared_metadata_contract_delta_checks'])]:
 lines=(S/diffname).read_text().splitlines(keepends=True);sections={};i=0
 while i<len(lines):
  assert lines[i].startswith('--- RI138/');name=lines[i].rstrip('\n').split('/',1)[1];i+=1
  assert lines[i]=='+++ RI140/'+name+'\n';i+=1;start=i
  while i<len(lines) and not lines[i].startswith('--- RI138/'):i+=1
  sections[name]=lines[start:i]
 for row in rows:
  m.verify(row['old']['path'],row['old']);m.verify(row['current']['path'],row['current'])
  original=Path(row['old']['path']).read_text().splitlines(keepends=True);target=Path(row['current']['path']).read_text()
  body=sections.get(row['name'],[]);out=[];cursor=0;i=0;hunks=0
  while i<len(body):
   match=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n',body[i]);assert match
   oldstart=int(match[1])-1;oldcount=int(match[2] or '1');newcount=int(match[4] or '1');i+=1;hunks+=1
   assert oldstart>=cursor;out+=original[cursor:oldstart];cursor=oldstart;removed=added=0
   while i<len(body) and not body[i].startswith('@@ '):
    line=body[i];assert line[0] in ' +-'
    if line[0] in ' -':assert original[cursor]==line[1:];cursor+=1;removed+=1
    if line[0] in ' +':out.append(line[1:]);added+=1
    i+=1
   assert (removed,added)==(oldcount,newcount)
  out+=original[cursor:];assert ''.join(out)==target and hunks==row['hunks']
  delta.append(dict(name=row['name'],hunks=hunks,identical_reconstruction=True))
 assert set(sections)=={r['name'] for r in rows if r['hunks']}
slices=[]
for module in c['modules']:
 oldlines=Path(module['old']['path']).read_bytes().splitlines(keepends=True);newlines=Path(module['current']['path']).read_bytes().splitlines(keepends=True)
 assert len(oldlines)==module['old_lines'] and len(newlines)==module['current_lines']
 for row in module['unchanged_definitions']:
  a=b''.join(oldlines[row['old_start']-1:row['old_end']]);b=b''.join(newlines[row['current_start']-1:row['current_end']])
  assert a==b and m.pin(a)==m.pure(row)
  slices.append(dict(module=module['name'],name=row['name'],**m.pure(row)))
assert len(slices)==96
print(m.save('ROOT_SOURCE_CHECK.json',dict(status='PASS_LITERAL_METADATA_CHECKS_ONLY',source_handoff=m.ref(S/'HANDOFF.json'),payloads=16,namespace_files=17,dependencies=423,dependency_bytes=total,inherited_rows_unchanged_except_role=396,added_rows=27,delta_reconstruction=delta,unchanged_slices=slices,overlapping_class_slices_not_semantic_proof=True,subject_import_compile_ast_execution=False,source_acceptance=False,independent_review_pending=True)))
