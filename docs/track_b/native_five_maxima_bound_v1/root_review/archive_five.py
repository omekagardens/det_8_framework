import importlib.util,hashlib
from pathlib import Path
D=Path('/Volumes/AI_DATA/development/det-review-evidence/ri207-root-four-maxima-review-rrel_hre');B=D.parent;Q=B/'ri208-native-five-maxima-po8tjwlh'
h=D/'publication_helpers.py';assert hashlib.sha256(h.read_bytes()).hexdigest()=='8b04758d4e19988f67d0d96e86c93a8eb5405704f5b2a3e3d0b401f33afa4277'
s=importlib.util.spec_from_file_location('p',h);p=importlib.util.module_from_spec(s);s.loader.exec_module(p);m=p.m
assert m.load(D/'RI208_ROOT_ADJUDICATION.json')['status']=='ACCEPT_COMPLETE_FIVE_MAXIMA_CLASS_CONDITIONAL_THEOREM'
origins=p.packet(Q,'source',key='payloads')
names=['RI208_ROOT_PROOF_REVIEW.md','RI208_ROOT_ADJUDICATION.json','RI208_ROOT_METADATA_CHECK.json','RI208_NONAUTHOR_REVIEW.json','review_ri208.py','adjudicate_ri208.py','RI210_NATIVE_ASSIGNMENT.json','RI210_DISPATCH.json','archive_five.py']
origins += [(D/n,'root_review/'+n) for n in names]
refs=m.load(Q/'SOURCE_REFERENCES.json');rows=[r['identity'] for r in refs['direct_sources']]+[m.ref(x) for x,_ in origins]+m.load(D/'RI210_NATIVE_ASSIGNMENT.json')['accepted_analytic_references']+[m.ref(h),m.ref(B/'ri122-root-execution-review-6whn_vky/metadata.py')]
unique={}
for row in rows:
 r={k:row[k] for k in ('path','bytes','sha256')};assert r['path'] not in unique or r==unique[r['path']];unique[r['path']]=r
readme='''# Complete native five-maxima bound

RI208 is independently accepted as a conditional theorem of the unchanged finite prefix. Every marked six-parent with exactly five maxima has U6<5+10K+80K^2+11/256<462080760006<463 billion<465 billion<T, K=681472/9. All empty/full precursor choices covering the singleton remainder, marked records and proper ideals are retained.

The selected-pair lemma yields epsilon^2/8, without requiring omitted precursors to cover selected caps. Full four-parent entries use only the all-ideal floor. Higher sectors apply the accepted finite canonical-support theorem precisely where the resulting terminal has at least four maxima. Positive theta restoration remains. All eight/sixteen old-maximum correction factors, the empty-parent factor and exact cancellation multiplicities are included. Both old-base ideals remain in the five-omission sum. Target and theta bounds use the accepted native witness, without evaluating the printed maximum or canonical vector.

Root full proof/source/checker reads4f3be7,4bb57c,9d5374 and metadata75e78f exit0 are distinct from the independent nonauthor reads and author checks. Metadata covers14 direct sources/537440bytes,20fresh identities,28 selected references,both six-file namespaces and15 preserved boundaries. Author preseal500385 and externally reported final56764b are reconciled against its complete checker, not replayed. The inherited423/26/18 collections remain references. Original failed lookup, recovered display and both wording phases remain; root combined metadata displayfd2bd4 was recovered by complete separate read4bb57c.

One through five maxima are settled against T. RI210 was separately assigned after this adjudication to reuse accepted RI185 classification for the remaining six-maxima upper bound and, only if justified, the exhaustive global target and exact RI199 weighted-W implication. Its explicit accepted analytic references are preserved; no active RI210 source is archived or accepted. Actual W, both margins,H30 and physical correspondence remain open in this checkpoint. All original executable obligations stay uncredited; RET alone is paused.

Exact original source and review copies are authenticated by PUBLICATION_MANIFEST. DEPENDENCY_MAP binds direct sources, required root evidence and assignment premises to original or already committed bytes. The RI205 predecessor is also published in the sibling native_four_maxima_bound_v1 bundle. This is not complete transitive runtime custody, and archived code is not authorized for relocated execution.
'''
print(m.save('FIVE_MAXIMA_PUBLICATION.json',p.archive('docs/track_b/native_five_maxima_bound_v1',origins,list(unique.values()),readme,True)))
