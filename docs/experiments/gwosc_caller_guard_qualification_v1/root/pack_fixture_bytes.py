"""Lossless data-only representation of retained nonscientific guard fixtures.

No extraction, subject import, numerical reconstruction or path rewriting.
"""
import base64, importlib.util, os, stat
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
op=Path(m.load(m.D/'OPERATION_LAYOUT.json')['operation']);out=op/'output'
report=m.load(out/'GUARD_REPORT.json');root=Path(report['fixture_root'])
assert root.parent==out and root.name.startswith('ri130-nonscientific-guards-')
saved=m.load(out/'CHECKS.json')['guards']['all_tree_entries']
actual=[];payload=[];file_bytes=0
for p in sorted(root.rglob('*')):
    row=dict(relative=p.relative_to(root).as_posix());st=p.lstat()
    if stat.S_ISLNK(st.st_mode):row.update(kind='symlink',target=os.readlink(p));encoded=dict(row)
    elif stat.S_ISDIR(st.st_mode):row['kind']='directory';encoded=dict(row)
    else:
        assert stat.S_ISREG(st.st_mode)
        ref=m.ref(p);body=p.read_bytes();assert m.pin(body)==m.pure(ref)
        row.update(kind='file',**m.pure(ref));encoded=dict(row,body_base64=base64.b64encode(body).decode('ascii'));file_bytes+=len(body)
        assert base64.b64decode(encoded['body_base64'],validate=True)==body
    actual.append(row);payload.append(encoded)
assert actual==saved
value=dict(schema='ri152-nonscientific-fixture-bytes-v1',original_root=str(root),source_report=m.ref(out/'GUARD_REPORT.json'),source_namespace=m.ref(out/'NAMESPACE.json'),entries=payload,scope='Complete retained nonscientific guard metadata and inert fixture bytes. Link targets retained literally as data; no symlinks created or followed and no extraction/execution authorized.',scientific_results=False,relocated_execution_authorized=False)
ref=m.save('FIXTURE_BYTES.json',value)
decoded=m.load(m.D/'FIXTURE_BYTES.json');assert len(decoded['entries'])==len(saved)
for row,want in zip(decoded['entries'],saved):
    assert {k:v for k,v in row.items() if k!='body_base64'}==want
    p=root/row['relative']
    if row['kind']=='file':
        b=base64.b64decode(row['body_base64'],validate=True);assert b==p.read_bytes() and m.pin(b)==m.pure(want)
    elif row['kind']=='symlink':assert p.is_symlink() and os.readlink(p)==row['target']
    else:assert p.is_dir() and not p.is_symlink()
print(ref)
print(m.save('FIXTURE_PACK_CHECK.json',dict(schema='ri152-fixture-byte-bijection-check-v1',status='PASS_COMPLETE_BYTE_AND_NAMESPACE_BIJECTION',package=ref,entries=len(saved),file_bytes=file_bytes,files=sum(r['kind']=='file' for r in saved),directories=sum(r['kind']=='directory' for r in saved),symlinks=sum(r['kind']=='symlink' for r in saved),every_decoded_body_equals_saved_original=True,all_link_targets_retained_as_data=True,subject_execution=False,scientific_results=False)))
