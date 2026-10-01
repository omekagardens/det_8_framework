"""Losslessly encode two reviewed archive copies; never edit source originals."""
from pathlib import Path
import gzip,hashlib,importlib.util
D=Path('/Volumes/AI_DATA/development/det-review-evidence/ri207-root-four-maxima-review-rrel_hre')
hp=D.parent/'ri122-root-execution-review-6whn_vky/metadata.py'
raw=hp.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
scope=m.load(D/'PUBLICATION_SCOPE_FINAL.json')
assert m.git('diff','--cached','--name-only')==b''
assert m.git('rev-parse','HEAD').decode().strip()==scope['parent']
diagnostic=dict(schema='ri207-publication-whitespace-diagnostic-v1',
    phase='staged',invocation='69a8a8',session_id=39102,terminal='66063e',exit_code=1,
    findings=['source/SOURCE_DIFF.patch:346: trailing whitespace',
              'root_review/publication_helpers.py:47: new blank line at EOF'],
    disposition='Preserve originals byte-for-byte through gzip encoding, update maps and manifests, rerun original acceptance thresholds.',
    source_originals_changed=False,unrelated_work_changed=False)
print(m.save('PUBLICATION_WHITESPACE_DIAGNOSTIC.json',diagnostic))
targets=[('docs/track_b/native_four_maxima_bound_v1','root_review/publication_helpers.py'),
         ('docs/coordination/measurement_actual_freeze_candidate_v1','source/SOURCE_DIFF.patch')]
scope['encoded_copies']=[]
for bundle,rel in targets:
    dest=m.REPO/bundle;old=dest/rel;new=dest/(rel+'.gz')
    rows=[r for r in scope['copies'] if r['path']==bundle+'/'+rel];assert len(rows)==1
    row=rows[0];m.verify(old,row['original']);m.verify(row['original']['path'],row['original'])
    original=Path(row['original']['path']).read_bytes();assert original==old.read_bytes()
    encoded=gzip.compress(original,mtime=0);assert gzip.decompress(encoded)==original
    with new.open('xb') as f:f.write(encoded)
    assert gzip.decompress(new.read_bytes())==original
    old.unlink()
    er=dict(path=bundle+'/'+rel+'.gz',original=row['original'],encoding='gzip',decompressed=m.pin(original))
    scope['copies'].remove(row);scope['encoded_copies'].append(er)
    scope['files'].remove(bundle+'/'+rel);scope['files'].append(er['path'])
    dm=m.load(dest/'DEPENDENCY_MAP.json')
    copied=[x for x in dm['copies'] if x['path']==rel];assert len(copied)==1
    dm['copies'].remove(copied[0]);dm['encoded_copies']=[dict(er,path=rel+'.gz')]
    for dep in dm['dependencies']:
        if dep['location']=='archive' and dep['path']==rel:
            dep.update(location='archive_gzip',path=rel+'.gz',decompressed=m.pin(original))
    counts={}
    for dep in dm['dependencies']:counts[dep['location']]=counts.get(dep['location'],0)+1
    dm['dependency_locations']=counts
    (dest/'DEPENDENCY_MAP.json').write_bytes(m.canonical(dm))
    with (dest/'README.md').open('a') as f:
        f.write('\nThe archive stores `'+rel+'` as `'+rel+'.gz` to retain its original whitespace exactly. Gzip decompression must reproduce the complete original byte count and SHA256 recorded in DEPENDENCY_MAP; the original source remains unchanged. This is archive encoding only and authorizes no execution.\n')
    manifest=m.load(dest/'PUBLICATION_MANIFEST.json')
    manifest['payload']=[dict(path=p.relative_to(dest).as_posix(),**m.pure(m.ref(p))) for p in sorted(dest.rglob('*')) if p.is_file() and p.name!='PUBLICATION_MANIFEST.json']
    manifest['exact_copies']=len(dm['copies']);manifest['losslessly_encoded_copies']=1
    (dest/'PUBLICATION_MANIFEST.json').write_bytes(m.canonical(manifest))
    for check in scope['checks']:
        if check['bundle']==bundle:
            check.update(copies=len(dm['copies']),losslessly_encoded_copies=1,dependency_locations=counts)
scope['files'].sort();scope['archive_encoding_diagnostic']=m.ref(D/'PUBLICATION_WHITESPACE_DIAGNOSTIC.json')
print(m.save('PUBLICATION_SCOPE_REPAIRED.json',scope))
checker=(D/'check_final_checkpoint_v2.py').read_text().replace('PUBLICATION_SCOPE_FINAL.json','PUBLICATION_SCOPE_REPAIRED.json').replace('SCOPED_PATHS_FINAL.nul','SCOPED_PATHS_REPAIRED.nul').replace('CHECKPOINT_FINAL_','CHECKPOINT_REPAIRED_')
with (D/'check_final_checkpoint_v3.py').open('x') as f:f.write(checker)
checker=(D/'check_dependencies_v2.py').read_text().replace('import hashlib,importlib.util','import hashlib,importlib.util,gzip').replace('PUBLICATION_SCOPE_FINAL.json','PUBLICATION_SCOPE_REPAIRED.json').replace('PUBLICATION_DEPENDENCY_CHECK.json','PUBLICATION_DEPENDENCY_REPAIRED_CHECK.json')
checker=checker.replace("  elif kind=='existing_git':", "  elif kind=='archive_gzip':\n   raw=gzip.decompress((d/row['path']).read_bytes());assert m.pin(raw)==m.pure(r)==row['decompressed'] and raw==Path(r['path']).read_bytes()\n  elif kind=='existing_git':")
with (D/'check_dependencies_v3.py').open('x') as f:f.write(checker)
with (D/'repair_archive_encoding.py').open('xb') as f:f.write(Path(__file__).read_bytes())
print('Encoded two exact source copies without altering originals; all acceptance thresholds retained.')
