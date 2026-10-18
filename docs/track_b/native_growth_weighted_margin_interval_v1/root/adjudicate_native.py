"""Root RI145 opaque reconciliation and bounded proof disposition."""
import importlib.util, tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
S=m.B/'ri145-native-weighted-margin-proof-zo96x_ci';R=m.B/'ri145-independent-proof-review-y6dp5ojt'
observed=[]
for base,size,digest in [(S,6015,'f53a0e1c49069a1e9057ad69169facca556b77e7cfb2534eba440b7eaa91db19'),(R,4678,'e30140e00872f1269933db73509f3f066c463b8a98650e171be1b737bb6f2374')]:
 observed.append(m.verify(base/'HANDOFF.json',dict(bytes=size,sha256=digest)))
 h=m.load(base/'HANDOFF.json');assert sorted(x.name for x in base.iterdir())==sorted(h['namespace'])
 for row in h['payloads']:observed.append(m.verify(row['path'],row))
deps=m.load(S/'SOURCE_DEPENDENCIES.json')['protected_files'];known={}
for row in deps:
 e=row['identity'];a=m.verify(row['path'],e);assert a['resolved_path']==e['resolved_path'] and a['symlink_chain']==e['symlinks']
 observed.append(a);known[a['path']]=a
assert len(deps)==86 and sum(known[x]['bytes'] for x in known)==3098788
known[str(S/'SOURCE_DEPENDENCIES.json')]=m.identity(S/'SOURCE_DEPENDENCIES.json')
def walk(v):
 count=0
 if isinstance(v,dict):
  if {'path','bytes','sha256'}<=set(v):assert m.pure(v)==m.pure(known[v['path']]);count+=1
  for x in v.values():count+=walk(x)
 elif isinstance(v,list):
  for x in v:count+=walk(x)
 return count
refs=sum(walk(m.load(x['path'])) for x in deps if x['classification']=='selected-administrative-proof-provenance')
premises=walk(m.load(S/'SOURCE_IDENTITIES.json'));assert (refs,premises)==(132,45)
check=m.save('ROOT_NATIVE_CHECK.json',dict(schema='ri145-root-opaque-reconciliation-v1',identities=observed,dependencies=86,dependency_bytes=3098788,historical_typed_refs=refs,premise_typed_refs=premises,source_namespace=10,review_namespace=7,scientific_body_decode=False,subject_execution=False))
decision=dict(schema='ri145-root-analytic-adjudication-v1',status='ACCEPT_EXACT_CONDITIONAL_ANALYTIC_PROOF_WITH_ACTUAL_SCALE_GAP',source_handoff=m.ref(S/'HANDOFF.json'),independent_handoff=m.ref(R/'HANDOFF.json'),independent_narrative=m.ref(R/'INDEPENDENT_PROOF_REVIEW.md'),root_check=check,
 root_manual_review='Read full main proof, endpoint derivation, author-peer crosscheck, dependency scope and actual author checks; full independent narrative and structured review. Rechecked held-epsilon cancellation, singleton P>0 decomposition, all positive brackets, q clamp and rationalized root, excluded y=0 continuity, q contrast residual. Traced exact RI120 prefix/F2, RI127 q sign and RI128 formulas/B14/B15 plus RI41 singleton/RI63 strict-mixture definitions. Independent full premise review supplies remaining historical lineage; no claim to redo ancestral numerical arithmetic.',
 accepted=['Exact seed-free W and positive clearing','Strict singleton-preserving reference/complement bounds','Positive symbolic quadratic minimum and uniform L/K compensation bound','Explicit positive delta_alpha interval with included upper endpoint','Equivalent two-polynomial endpoint criterion and complete singleton contrast residual'],
 actual_gap=['Actual rho<=delta0 unproved','LX+KX^2<=1 sufficient but unproved and not necessary','Full-domain endpoint signs unproved','Actual W/C2/C3 and full shared H30 unresolved'],
 remaining='Fixed baseline/seed/amplitude/support; shared T1, other eight connected parents and all five Di; immutable P2/P3 Y=1/4; unchanged31/139/20/42 runtime obligations and genuine custody. RET paused.',scientific_execution=False,formal_prover_used=False,blocking_findings=[])
print(check);print(m.save('RI145_ROOT_ADJUDICATION.json',decision))
target=Path(tempfile.mkdtemp(prefix='ri147-native-scale-membership-',dir=m.B))
print(m.save('NATIVE_SUCCESSOR_RESERVATION.json',dict(schema='ri147-root-native-proof-assignment-v1',owner_thread='01a074c4-4b09-76a3-8cb2-0caf116f6b9c',reservation=str(target),predecessor=m.ref(m.D/'RI145_ROOT_ADJUDICATION.json'),status='ASSIGNED_AFTER_PREDECESSOR_ADJUDICATION',
 question='Can the actual half-scale law supply rho<=delta0 (or a sharper actual-containing W<=0 bound) by analytic control of the specific held sensitivity ratios, rather than leaving q and v merely positive?',
 concrete_step='Starting with RI145 exact q residual, derive the actual root-record contrast factorization using accepted C4 and C5 singleton-component definitions. Retain DeltaN and all correlated terms. Seek justified lower bounds for v/D3 and q(x)/D3 and combine them with rho=1/[2(1+M6)] and explicit accepted individual-parent lower bounds on M6. Try to close the actual membership inequality; if not, give the strongest proved comparison and precisely isolate the remaining actual coefficient/component premise. Do not rerun the already accepted small-x theorem or treat freely chosen positive coefficients as a counterexample to the fixed law.',
 scope='Manual analytic proof and new administrative whole-byte/reference checking only; historical scientific bodies opaque. No subject/helper import/compile/AST/probe/run, symbolic/numerical engine, new probability/scales/maxima/H/z evaluation, global enumeration, runtime/controller/card or operational admission. Do not modify predecessor packets or repository/Git. Original numerical certificate/domain and all shared/native obligations unchanged. Measurement and RET excluded.',
 acceptance='Complete source premise closure, explicit inequality directions/zero and endpoint cases, proof or sharply stated remaining premise, author actual checks and sealed handoff for nonauthor review. No self acceptance or automatic execution.')))
print({'next_reservation':str(target)})
