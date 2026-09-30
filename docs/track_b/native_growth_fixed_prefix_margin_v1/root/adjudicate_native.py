"""Adjudicate the sealed RI153 manual proof and independent review."""
import importlib.util
import tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
Q=m.B/'ri153-fixed-prefix-weighted-margin-7_73jtl5';R=m.B/'ri153-independent-margin-review-FciZqSiY'
m.verify(Q/'HANDOFF.json',dict(bytes=6422,sha256='4058c2a9545211d2e845661a86516a69b94d15833c3ebbccb9657dc8de61beb7'))
m.verify(R/'HANDOFF.json',dict(bytes=8463,sha256='1b4546dcab2214e93869eeb236f3da4898dcb5ce767e8eb96f08d671fb267588'))
seals=[]
for d in (Q,R):
 h=m.load(d/'HANDOFF.json');assert sorted(p.name for p in d.iterdir())==sorted(h['namespace'])
 assert sorted(h['namespace'])==sorted(['HANDOFF.json']+[Path(x['path']).name for x in h['payloads']])
 seals.append(m.identity(d/'HANDOFF.json'))
 for row in h['payloads']:
  assert Path(row['path']).parent==d;seals.append(m.verify(row['path'],row))
root=m.load(m.D/'METADATA_CHECK.json');ind=m.load(R/'METADATA_CHECK.json')
assert {k:v for k,v in root.items() if k!='schema'}=={k:v for k,v in ind.items() if k!='schema'}
for row in root['dependencies']:assert m.identity(row['path'])==row
v=m.load(R/'INDEPENDENT_MARGIN_REVIEW.json')
assert v['required_repairs']==[] and v['status']=='ACCEPT_EXACT_PREFIX_IDENTITIES_AND_CONDITIONAL_JOINT_BUDGET_REDUCTION'
assert m.load(R/'REVIEW_DIAGNOSTICS.json')['author_diagnostics_verbatim']==m.load(Q/'AUTHOR_CHECKS.json')['diagnostics']
assert m.snapshot()==m.load(m.D/'REPO_ENTRY.json')
decision=m.save('RI153_ROOT_ADJUDICATION.json',dict(schema='ri153-root-proof-adjudication-v1',status=v['status'],subject=m.ref(Q/'HANDOFF.json'),independent_review=m.ref(R/'HANDOFF.json'),manual_review=m.ref(m.D/'ROOT_MANUAL_REVIEW.md'),root_check=m.ref(m.D/'METADATA_CHECK.json'),root_check_tool='58ede7 exit0',fresh_seal_identities=seals,accepted_results=v['accepted_manual_results'],clarifications=v['clarifications'],excluded_inference=v['excluded_inference'],remaining=v['remaining'],preserved=v['preserved'],conditional_implication=v['conditional_implication'],scientific_execution=False,physical_claim=False,ret_paused=True))
print(decision)
nextdir=Path(tempfile.mkdtemp(prefix='ri155-strict-capacity-proof-',dir=m.B))
print(m.save('NATIVE_SUCCESSOR_RESERVATION.json',dict(schema='ri155-native-strict-capacity-assignment-v1',owner='Quantum Relativity 01a074c4-4b09-76a3-8cb2-0caf116f6b9c',status='ASSIGNED_AFTER_RI153_ADJUDICATION',reservation=str(nextdir),predecessor=decision,question='Resolve the strict-capacity prerequisite of the accepted joint envelope for the same fixed prefix: YE<1 and v>B max(1,(1-Yu3)/(1-YE)). Prioritize an actual structural proof or structural obstruction of these capacities before spending more work on q floors. Use the retained complete normalization, component incidence, actual-containing Z, and exact v/D3 contrast; expose cancellations or a quantitatively adequate correlated bound. If neither sign can be settled analytically, give the precise remaining fixed-prefix comparison plus a substantive new derivation or a source-justified blocked premise; do not merely restate RI153 or provide arbitrary positive-coefficient examples. A failed envelope is not a W or H30 sign; a pass still leaves the q threshold unless separately proved. Keep all zero/strict-boundary cases.',scope='Manual source-only native-law proof/candidate analysis. No numerical scientific-body decode, actual coefficient/probability/history/maximum/scale/H/z evaluation, source/helper import/compile/AST/probe/run, CAS/numerical engine, global enumeration, fixture/runtime/controller/card/admission, repository/index/Git or sealed predecessor mutation. Preserve withdrawn seed inference as excluded; no premise from it. Exact source text/admin identity checking allowed. Seal concrete source and actual administrative checks for fresh nonauthor review and root adjudication.',preserved=v['preserved'],measurement_separate=True,ret_paused=True)))
