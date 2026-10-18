"""Publish exact accepted RI210 sources and review, preserving other work."""
from pathlib import Path
import hashlib,importlib.util
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri211-root-global-W-review-xh6eetn1';old=B/'ri207-root-four-maxima-review-rrel_hre';Q=B/'ri210-native-six-maxima-leicoenm'
p=old/'publication_helpers.py';b=p.read_bytes();assert len(b)==3490 and hashlib.sha256(b).hexdigest()=='8b04758d4e19988f67d0d96e86c93a8eb5405704f5b2a3e3d0b401f33afa4277'
with (D/'publication_helpers.py').open('xb') as f:f.write(b)
s=importlib.util.spec_from_file_location('pub',D/'publication_helpers.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);m=h.m
for src,name in [(Path('/private/tmp/ri211_checkpoint.md'),'CURRENT_CHECKPOINT.md'),(Path(__file__),'publish.py')]:
    with (D/name).open('xb') as f:f.write(src.read_bytes())
origins=h.packet(Q,'source',key='payloads')
root_names=['RI210_ROOT_PROOF_REVIEW.md','RI210_ROOT_METADATA_CHECK.json','RI210_NONAUTHOR_REVIEW.json','RI210_ROOT_ADJUDICATION.json','RI212_NATIVE_ASSIGNMENT.json','RI212_DISPATCH.json','review_metadata.py','adjudicate.py','publish.py']
origins.extend((D/name,'root_review/'+name) for name in root_names)
origins.extend([(old/'VERIFIED_REMOTE_CHECKPOINT.json','prior_checkpoint/VERIFIED_REMOTE_CHECKPOINT.json'),(old/'PUBLICATION_WHITESPACE_DIAGNOSTIC.json','prior_checkpoint/PUBLICATION_WHITESPACE_DIAGNOSTIC.json'),(old/'repair_archive_encoding.py','prior_checkpoint/repair_archive_encoding.py'),(B/'ri122-root-execution-review-6whn_vky/metadata.py','root_review/metadata.py')])
source=m.load(Q/'SOURCE_REFERENCES.json');rows=[r['identity'] for r in source['direct_sources']]
rows.extend(m.ref(p) for p,_ in origins)
rows.extend([m.ref(old/'publication_helpers.py'),m.ref(D/'CURRENT_CHECKPOINT.md')])
for row in m.load(D/'RI212_NATIVE_ASSIGNMENT.json')['source_admission']:rows.append(row['identity'])
unique={}
for r in rows:
    if r['path'] in unique:assert m.pure(unique[r['path']])==m.pure(r)
    unique[r['path']]=r
bundle='docs/track_b/native_global_maximum_weighted_sign_v1'
readme='''# Global maximum bound and strict weighted sign

Root and a separate nonauthor accept RI210 on its named inherited finite-law premises. Every marked six-antichain satisfies U6<2^36+7<69 billion. Combining all six maxima-count classes gives the actual same-law global M6<463 billion<465 billion<T. The exact RI199 implication then gives W(rho,s)>0 at the original correlated pair, strictly even at equality in its sufficient target.

The proof reuses the complete marked RI185 antichain classification and all-proper A5 restoration theorem, retains all 63 ideals and 64 records, actual full complements, seed probabilities and canonical corrections. No maximum, scale, scientific vector or coefficient was evaluated. Conditional mathematics and metadata authentication remain distinct. The original source-author wording is preserved as submitted; root acceptance is in root_review/RI210_ROOT_ADJUDICATION.json.

Both individual margins, shared T1, eight other connected parents, five Di, H30 and physical correspondence remain open. RI212 is assigned to the original individual-margin question. Measurement RI209 continues separately toward an independently reviewed freeze installation. RET remains paused; all original executable qualifications remain uncredited.

SOURCE_REFERENCES and the root metadata result distinguish 26 direct sources, 48 selected references, 32 fresh identities and 15 preserved boundary objects from the inherited 423-source collection. Author checks retain their attribution. Root and independent manual reviews record the actual reads, recovered display clipping and limits. Archived code is evidence and is not authorized for execution at relocated paths.

PUBLICATION_MANIFEST pins every exact archive payload. DEPENDENCY_MAP records same-bundle copies, existing committed equivalents and external originals. This is not a complete transitive or runtime archive. The prior checkpoint remote receipt and its lossless-encoding diagnostic are retained without rewriting their original evidence.
'''
check=h.archive(bundle,origins,list(unique.values()),readme,True)
fronts=['REVIEW_IMPLEMENTATION_PLAN.md','docs/coordination/REVIEW_PROGRESS.md','docs/coordination/QR_HANDOFF.md','docs/coordination/PUBLICATION_BACKLOG.md']
block=(D/'CURRENT_CHECKPOINT.md').read_text()
for name in fronts:
    p=m.REPO/name;t=p.read_text();oldheading='**Current checkpoint — complete four/five-maxima theorems and actual freeze candidate.**'
    assert t.count(oldheading)==1;t=t.replace(oldheading,'**Prior checkpoint — complete four/five-maxima theorems and actual freeze candidate.**',1)
    first,rest=t.split('\n',1)
    if name.endswith('QR_HANDOFF.md'):first='# Current QR coordination — RI210 global bound accepted; RI212 individual margins active'
    p.write_text(first+'\n\n'+block+rest.lstrip('\n'))
dest=m.REPO/bundle;dm=m.load(dest/'DEPENDENCY_MAP.json')
files=fronts+[p.relative_to(m.REPO).as_posix() for p in sorted(dest.rglob('*')) if p.is_file()]
scope=dict(schema='ri211-publication-scope-v1',parent=h.entry['head'],bundles=[bundle],checks=[check],files=sorted(files),copies=[dict(path=bundle+'/'+r['path'],original=r['original']) for r in dm['copies']],scientific_execution=False,excluded='All unrelated tracked/nonignored work, active RI209/RI212 files, protected scientific bodies and paused RET edits.')
print(m.save('PUBLICATION_SCOPE_FINAL.json',scope))
checker=(old/'check_final_checkpoint_v2.py').read_text().replace('ri207-','ri211-')
with (D/'check_final_checkpoint.py').open('x') as f:f.write(checker)
checker=(old/'check_dependencies_v2.py').read_text().replace('ri207-','ri211-')
with (D/'check_dependencies.py').open('x') as f:f.write(checker)
print(check)
