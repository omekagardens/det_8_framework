"""Root review reconciliation. Opaque files and administrative metadata only."""
import importlib.util
from pathlib import Path
import re
from collections import Counter

spec=importlib.util.spec_from_file_location('metadata','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.D=Path(__file__).resolve().parent
S=m.B/'ri129-native-sign-caller-source-8TksBLo0';R=m.B/'ri129-native-caller-independent-review-Z0SqaY10';A=m.B/'ri122-native-caller-source-jgehvvxx'
def full(path):
    row=m.identity(path)
    return dict(path=row['path'],resolved_path=row['resolved_path'],bytes=row['bytes'],sha256=row['sha256'],symlinks=row['symlink_chain'])
def ref(v):return {k:v[k] for k in ('path','bytes','sha256')}
packet_checks=[]
for folder,expected in [(S,dict(bytes=10184,sha256='b3839ba2f81e791321e2549107ce5f1b84ffdbbcc635396ab4e72002386feac0')),(R,dict(bytes=3082,sha256='6cd215563c660948188a73c6d3d0ccc6fe6f583b4d1bc2cc981654abcc223ac0'))]:
    m.verify(folder/'HANDOFF.json',expected);h=m.load(folder/'HANDOFF.json')
    for row in h['files']:m.verify(row['path'],row)
    assert {p.name for p in folder.iterdir()}=={'HANDOFF.json'}|{Path(r['path']).name for r in h['files']}
    packet_checks.append(dict(handoff=m.ref(folder/'HANDOFF.json'),payload_count=len(h['files']),exact_namespace=True))
review=m.load(R/'INDEPENDENT_SOURCE_REVIEW.json')
assert review['status']=='PASS_COMPLETE_SOURCE_REVIEW_ONLY' and review['blocking_findings']==[]
assert review['authorship']['authored_RI129_or_RI128_components'] is False
assert not review['execution_authorized'] and not review['scientific_execution']
for row in review['sources'].values():assert full(row['path'])==row
assert set(review['sources'])=={'native_supervisor','audit_caller','caller_contract','history_manifest','runtime_manifest','dependency_manifest'}
dep=m.load(S/'SOURCE_DEPENDENCIES.json');hist=m.load(A/'HISTORY_RECONCILIATION.json');runtime=m.load(A/'RUNTIME_CLOSURE.json')
assert len(dep['protected_files'])==299
known={}
for row in hist['protected_files']+runtime['files']+dep['protected_files']:
    r=ref(row['identity']);p=row['path'];assert p==r['path']
    assert p not in known or known[p]==r
    known[p]=r
for folder in (S,):
    for p in folder.iterdir():known[str(p)]=m.ref(p)
for name in ('HISTORY_RECONCILIATION.json','RUNTIME_CLOSURE.json'):known[str(A/name)]=m.ref(A/name)
counts=Counter();occurrences=0;reference_sources=Counter();dep_rows=[]
def refs(v):
    if type(v) is dict:
        if {'path','bytes','sha256'}<=set(v) and type(v['path']) is str and type(v['bytes']) is int and type(v['sha256']) is str:yield ref(v)
        for x in v.values():yield from refs(x)
    elif type(v) is list:
        for x in v:yield from refs(x)
previous=''
for i,row in enumerate(dep['protected_files'],1):
    assert row['role']==f'dep_{i:04d}' and previous<row['path'];previous=row['path']
    assert full(row['path'])==row['identity']
    counts[row['classification']]+=1
    dep_rows.append(dict(role=row['role'],**ref(row['identity'])))
    if row['classification']=='existing-administrative-source-custody-metadata':
        for value in refs(m.load(row['path'])):
            assert known[value['path']]==value
            occurrences+=1;reference_sources[row['path']]+=1
assert occurrences==114488 and len(reference_sources)==111
assert counts['existing-administrative-source-custody-metadata']==126

# Reconcile the reviewer's complete audit coverage map without evaluating code.
native=(S/'supervise.py').read_bytes().splitlines(keepends=True)
audit=(S/'launch_audit.py').read_bytes().splitlines(keepends=True)
spans=m.load(R/'TEXT_SPAN_MAP.json');position=1;equal_lines=0
assert len(native)==1452 and len(audit)==1623
for row in spans['audit_spans']:
    assert row['start']==position
    body=b''.join(audit[row['start']-1:row['end']]);assert m.pin(body)['sha256']==row['sha256']
    if row['identical_native_span']:
        r=row['identical_native_span'];other=b''.join(native[r['start']-1:r['end']])
        assert body==other and m.pin(other)['sha256']==r['sha256'];equal_lines+=row['end']-row['start']+1
    position=row['end']+1
assert position==1624 and equal_lines==571

# Apply the exact saved unified patches to immutable originals as raw lines.
def patch_lines(old,patch):
    p=patch.splitlines(keepends=True);out=[];cursor=0;i=2;hunks=0
    while i<len(p):
        h=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@[^\n]*\n',p[i]);assert h
        start,n,new,k=int(h[1]),int(h[2] or 1),int(h[3]),int(h[4] or 1)
        oldpos=start-1 if n else start;assert oldpos>=cursor
        out.extend(old[cursor:oldpos]);cursor=oldpos;i+=1;a=b=0
        while i<len(p) and not p[i].startswith('@@ '):
            tag=p[i][0];line=p[i][1:];assert tag in ' +-'
            if tag in ' -':assert old[cursor]==line;cursor+=1;a+=1
            if tag in ' +':out.append(line);b+=1
            i+=1
        assert (a,b)==(n,k) and len(out)==new-1+k;hunks+=1
    out.extend(old[cursor:]);return ''.join(out),hunks
patch_checks=[]
for name,patch in [('supervise.py','SUPERVISE_SOURCE_DELTA.patch'),('launch_audit.py','AUDIT_CALLER_SOURCE_DELTA.patch')]:
    rebuilt,hunks=patch_lines((A/name).read_text().splitlines(keepends=True),(S/patch).read_text())
    assert rebuilt==(S/name).read_text()
    patch_checks.append(dict(source=name,hunks=hunks,exact=True))
corrected=m.load(R/'CORRECTED_METADATA_SUMMARY.json')
assert corrected['status']=='PASS' and corrected['references_outside_closed_map']==[] and corrected['reference_identity_mismatches']==[]
for r in corrected['retained']:
    old=(A/r['name']).read_text();new=(S/r['name']).read_text()
    if r.get('end')=='EOF':
        old=old[old.index(r['start']):];new=new[new.index(r['start']):]
        assert new.count('    pre_attempt_prerequisites(mode)\n')==1
        new=new.replace('    pre_attempt_prerequisites(mode)\n','',1)
    else:
        old=old[old.index(r['start']):old.index(r['old_end'])]
        new=new[new.index(r['start']):new.index(r['new_end'])]
        assert m.pin(new.encode())==dict(bytes=r['bytes'],sha256=r['sha256'])
    assert old==new
for row in packet_checks:
    m.verify(row['handoff']['path'],row['handoff'])
    for f in m.load(row['handoff']['path'])['files']:m.verify(f['path'],f)
print(m.save('ROOT_SOURCE_REVIEW_RECONCILIATION.json',dict(schema='ri129-root-source-review-reconciliation-v1',status='PASS_SOURCE_AND_ADMINISTRATIVE_METADATA_ONLY',packets=packet_checks,six_review_source_identities_match=True,dependency_count=299,dependencies=dep_rows,administrative_records=126,metadata_reference_sources=111,closed_typed_reference_occurrences=occurrences,unresolved_or_conflicting_references=0,audit_coverage_lines=1623,audit_exact_native_equivalence_lines=571,complete_source_patches=patch_checks,retained_text_comparisons=5,reviewer_initial_false_text_mismatches_preserved=True,scientific_json_decode=False,target_import_compile_ast_probe_run=False,current_runtime_scanned=False,execution_admitted=False)))
