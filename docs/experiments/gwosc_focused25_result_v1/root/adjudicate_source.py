"""Root source text/opaque metadata adjudication, never subject execution."""
import importlib.util,difflib,re
from pathlib import Path
sp=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=Path(__file__).resolve().parent
S=m.B/'ri139-focused-bootstrap-repair-source-XP8iNwMw';R=m.B/'ri139-bootstrap-independent-review-VMq4RmI9';P=m.B/'ri137-focused-control-launcher-source-nykv2tsg'
observations=[]
for base,n,h in [(S,7035,'24e6815b31bd47b543211f4f51156d1c0c67d96dac88db65db48f85d3be898d0'),(R,4113,'83103b433a7caa1763c2bea9a2565bede26b35a60da1383d8674b661ae37b613')]:
 observations.append(m.verify(base/'HANDOFF.json',dict(bytes=n,sha256=h)));v=m.load(base/'HANDOFF.json');assert sorted(p.name for p in base.iterdir())==v['closed_namespace']
 for row in v['files']:observations.append(m.verify(row['path'],row))
deps=m.load(S/'DEPENDENCIES.source-only.json');olddeps=m.load(P/'DEPENDENCIES.source-only.json');assert len(deps['opaque_files'])==310
old={x['path']:x for x in olddeps['opaque_files']};new={x['path']:x for x in deps['opaque_files']};assert len(old)==276 and all(new[k]==v for k,v in old.items()) and len(new.keys()-old.keys())==34
for row in deps['opaque_files']:observations.append(m.verify(row['path'],row))
oldpath=P/'launch_controls.source-only.py';newpath=S/'launch_controls.source-only.py';a=oldpath.read_text();b=newpath.read_text()
patch=''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=str(oldpath),tofile=str(newpath)))
assert patch==(S/'REPAIR.diff').read_text()
def functions(text):
 matches=list(re.finditer(r'^def (\w+)\(',text,re.M));out={}
 for i,x in enumerate(matches):
  end=matches[i+1].start() if i+1<len(matches) else text.index("\nif __name__ == '__main__':")
  out[x.group(1)]=text[x.start():end].rstrip()+'\n'
 return out
af=functions(a);bf=functions(b);same=[k for k in af if af[k]==bf[k]];changed=[k for k in af if af[k]!=bf[k]];added=sorted(bf.keys()-af.keys())
assert len(same)==17 and changed==['prepare_launch','run'] and added==['selected_bootstrap']
assert a[a.index('F01 ='):a.index('\n\ndef need')]==b[b.index('F01 ='):b.index('\n\ndef need')]
hist=m.load(m.B/'ri137-root-launch-adjudication-ie1m0jc_/BOOTSTRAP_PRE.json');selected=deps['selected_bootstrap_binding']
row=next(x['identity'] for x in hist['framework_namespace'] if x['path']==selected['path']);assert row==selected
assert b.count("child = P.child_run(card['child_command'], out, 'FOCUSED25', 180, env)")==1
assert b.count("selected_bootstrap(read(card['bootstrap_host_preflight']), deps)")==2
assert b.index("selected_bootstrap(read(card['bootstrap_host_preflight']), deps)")<b.index('module_bytes = captured')<b.index('out.mkdir')
for row in observations:assert m.identity(row['path'])==row
check=m.save('ROOT_SOURCE_RECONCILIATION.json',dict(schema='ri139-root-source-reconciliation-v1',source=m.ref(S/'HANDOFF.json'),review=m.ref(R/'HANDOFF.json'),observations=observations,dependencies=310,inherited=276,added_dependencies=34,source_names=8,review_names=7,complete_delta_exact=True,unchanged_functions=same,changed_functions=changed,new_functions=added,author_grouped_spans=15,independently_counted_unchanged_functions=17,case_limit_environment_blocks_unchanged=True,selected_binding_from_saved_metadata=True,subject_execution=False))
text='''# RI139 root source adjudication

Accept the exact narrow unexecuted bootstrap repair after complete fresh nonauthor review. Root read the complete repair diff, new selected_bootstrap function, both complete changed functions, authoring record and full independent review. Root's prior complete RI137 wrapper review remains inherited, not a newly claimed whole390-line reread. Root independently reconciled all8 source and7 review names, all310 dependency identities/276 retained+34added, the exact full old-to-new diff, complete control/resource/premise block and 17 actual unchanged functions. Author's15 grouped unchanged spans include17 actual functions; this nonblocking attribution issue needs no source mutation. The chosen direct binding exactly matches the genuine saved PRE row.

The added guard requires the closed complete direct binding in genuine root preflight, compares fixed historical identity/state, stable current bytes/state and actual sys.executable before module loading and again in the independent card tail. Both command vectors use that same direct entry. Exact environment equality, one unchanged monitor, all25 controls, resource bounds, protected ownership/partial retention/independent groups remain unchanged. Group-internal failures can skip later statements in that group and must not be reported as a complete PASS.

This source result alone admits no execution. Fresh external vendor-bootstrap/framework/host/environment observation and authentic selected binding must precede new cards. The original RI137 attempt remains rejected, zero25, with its later diagnostics retained as corroboration rather than a reconstruction of that process. No candidate science runtime is accepted by the vendor observation. Kernel/Apple loader/shared cache, stable supplier/no descendants, source/cache equivalence and genuine tool-origin are explicit premises. The960-second Perl parent alarm is not a process-group memory/cleanup guarantee; unchanged child180s/sample512MiB/25ms/100ms/50ms requirements must be observed in the actual run. Root will reject a missing sample, overrun or late failure without retry or relaxation.

After this source adjudication, root may separately admit one fresh existing25-control operation with complete actual evidence review. Current preparation/capture, normal-before-optimized profiles,65guards, WHITE/full32/public GWOSC and native physical claims remain separate. RI138 is under independent source review. RET remains paused.
'''
(m.D/'ROOT_SOURCE_REVIEW.md').write_text(text)
print(m.save('RI139_ROOT_ADJUDICATION.json',dict(schema='ri139-root-source-adjudication-v1',status='ACCEPT_NARROW_UNEXECUTED_DIRECT_BOOTSTRAP_REPAIR',source=m.ref(S/'HANDOFF.json'),independent_review=m.ref(R/'HANDOFF.json'),root_review=m.ref(m.D/'ROOT_SOURCE_REVIEW.md'),reconciliation=check,source_accepted=True,execution_admitted=False,controls_executed=0,N01='15 grouped unchanged spans contain17 actual unchanged functions; all bytes unchanged',RI137_attempt_remains_rejected=True)))
