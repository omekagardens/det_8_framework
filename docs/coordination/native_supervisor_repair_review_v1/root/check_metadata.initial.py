"""Independent literal-source and opaque metadata checks, no subject execution."""
from pathlib import Path
import hashlib,importlib.util,re,json
D=Path(__file__).resolve().parent;H=D.parent/'ri122-root-execution-review-6whn_vky/metadata.py';b=H.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',H);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
S=m.B/'ri167-native-supervisor-repair-79xn8tjz';h=m.load(S/'HANDOFF.json');current=[m.verify(r['path'],r) for r in m.load(D/'SUBJECT_AUTHENTICATION.json')['files']];assert len(current)==18
bindings=m.load(S/'DEPENDENCY_BINDINGS.json');fresh=[m.verify(r['path'],r) for r in bindings['freshly_rechecked_originals']];assert len(fresh)==33
# Flat reference maps only, not recursive scientific/admin body decoding.
ref=bindings['inherited_reference_manifest'];print('inherited manifest',ref)
x=m.load(ref['path']);refs=[]
def walk(o):
 if isinstance(o,dict):
  if {'path','bytes','sha256'}<=set(o) and isinstance(o['path'],str) and o['path'].startswith('/'):refs.append({k:o[k] for k in ('path','bytes','sha256')})
  else:
   for v in o.values():walk(v)
 elif isinstance(o,list):
  for v in o:walk(v)
walk(x);by={}
for r in refs:
 if r['path'] in by:assert by[r['path']]==r
 by[r['path']]=r
inherited=[m.verify(r['path'],r) for r in by.values()]
c=m.load(S/'SOURCE_CORRESPONDENCE.json');old=Path(c['old_source']['path']).read_text();new=Path(c['new_source']['path']).read_text();m.verify(c['old_source']['path'],c['old_source']);m.verify(c['new_source']['path'],c['new_source'])
def parts(t):
 starts=list(re.finditer(r'^def ([a-z_]+)\(',t,re.M));tail=t.index("if __name__ == '__main__':")
 return {r.group(1):t[r.start():(starts[i+1].start() if i+1<len(starts) else tail)] for i,r in enumerate(starts)}
a,z=parts(old),parts(new);assert len(a)==13 and len(z)==15
assert sorted(set(z)-set(a))==['readable_names','stop_pipe']
assert sorted(k for k in a if a[k]!=z[k])==['process_snapshot','supervise']
for r in c['function_spans']:assert m.pin(z[r['name']].encode())==m.pure(r)
restored=new.replace('RI167 repaired fixed RI161','RI165 fixed RI161',1)
for k in ('stop_pipe','readable_names'):restored=restored.replace(z[k],'',1)
for k in ('process_snapshot','supervise'):restored=restored.replace(z[k],a[k],1)
assert restored==old
assert old[old.index('        for name, fd in fds.items():'):]==new[new.index('        for name, fd in fds.items():'):]
proposal=m.load(S/'COMMAND_PROPOSAL.json');assert m.pin(proposal['command_utf8'].encode())==proposal['command_pin']
assert proposal['tool_fields']['cmd']==proposal['command_utf8'] and proposal['environment']=={'LANG':'C','LC_ALL':'C','PATH':'/usr/bin:/bin'}
for r in proposal['unchanged_five_sources'].values():m.verify(r['path'],r)
variants=m.load(S/'FOCUSED_VARIANTS.json');assert len(variants['variants'])==28 and len({r['id'] for r in variants['variants']})==28 and all(r['executed'] is False for r in variants['variants']);assert variants['retained_groups']==['S%02d'%i for i in range(1,14)]
# An exact source span grounds the manual error path; this is not a test execution.
span=new[new.index('    def drain(failed):',new.index('def supervise():')):new.index('\n    try:\n        for name, suffix',new.index('def supervise():'))]
assert span.index('chunk = os.read')<span.index('write_all(fds[name], kept)')<span.index('except BlockingIOError:')<span.index('except Exception as exc:')
print(m.save('INDEPENDENT_METADATA_CHECK.json',dict(status='PASS_IDENTITY_AND_LITERAL_CORRESPONDENCE_ONLY',current=current,original33=fresh,inherited_reference_files=inherited,inherited_ref_occurrences=len(refs),inherited_distinct_paths=len(inherited),unchanged_original_functions=11,changed_original_functions=['process_snapshot','supervise'],added_helpers=['stop_pipe','readable_names'],whole_reverse_projection=True,original_native_roles_unchanged=5,retained_groups=13,unexecuted_variants=28,reviewed_drain_literal=span,source_executed=False,source_AST_or_compile=False,scientific_body_decoded=False)))
