"""Root source repair disposition and narrow successor; no target execution."""
import hashlib,importlib.util,tempfile
from pathlib import Path
D=Path(__file__).resolve().parent;B=D.parent;H=B/'ri122-root-execution-review-6whn_vky/metadata.py'
assert len(H.read_bytes())==3144 and hashlib.sha256(H.read_bytes()).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',H);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
R=B/'ri158-independent-repair-review-nxij3eju';S=B/'ri158-white-custody-repair-68cdvzn6'
m.verify(R/'HANDOFF.json',dict(bytes=5894,sha256='02f3ef205a747dfdc096f849c1ff64a58984b10a4c3eb635e292b284a1314619'))
m.verify(S/'HANDOFF.json',dict(bytes=12934,sha256='69638eb05897dc2e72c4a29f84d27593dff5e83b98e102c1efccc67f9ded4fa2'))
for P,count in [(S,27),(R,10)]:
 h=m.load(P/'HANDOFF.json');assert sorted(p.name for p in P.iterdir())==sorted(h['namespace']) and len(h['namespace'])==count
 for row in h['payloads']:m.verify(row['path'],row)
a=m.load(D/'METADATA_CHECK.json');b=m.load(R/'METADATA_CHECK.json')
assert {k:v for k,v in a.items() if k!='schema'}=={k:v for k,v in b.items() if k!='schema'}
assert a['predicates']==3888 and a['final_fresh_identity_count']==553
for row in a['observed_identities']:assert m.identity(row['path'])==row
for row in m.load(R/'FINAL_PIN_CHECK.json')['review_preseal_files']:m.verify(row['path'],row)
assert (D/'CHECK.stderr').read_bytes()==b''
summary=m.save('MEASUREMENT_METADATA_REPLAY.json',dict(schema='ri158-root-replay-summary-v1',status='FULL_REPORT_EQUAL_EXCEPT_SCHEMA',replay=dict(chunk='1e4e42',exit_code=0),report=m.ref(D/'METADATA_CHECK.json'),independent_report=m.ref(R/'METADATA_CHECK.json'),checker=m.ref(D/'check_measurement.py'),source_checker=m.ref(R/'check_metadata.py'),adaptations=['output directory R','report schema'],predicates=3888,dependencies=525,inherited=481,additions=44,dependency_bytes=30301774,fresh_complete_identities=553,review_preseal_files_rechecked=8,unchanged_modules=9,changed_modules=2,added_modules=1,unchanged_saved_mode_functions=8,source_namespace=27,review_namespace=10,full_patch_reconstructed=True,controls_defined=84,controls_executed=0,source_acceptance=False,scientific_or_subject_execution=False))
text='''# RI158 root source-repair adjudication

30 September 2026 UTC. Require F02-R final fixture-namespace reconciliation
before source acceptance or qualification. The full nonauthor review is sealed.
Root independently confirms its concrete source trace, using the actual adapter,
control implementation, complete tree format and independent-tail mechanism.

Root read the full RI158 adapter in600bd6 in the previous turn and freshly read
its complete post-authentication runner in34ecda. Root read all integration
controls and custody_io in84e377, with the clipped control-tail assertions fully
recovered in34ecda. The changed saved-mode wrapper was also read in34ecda.
The complete independent narrative/verdict was read in421419; the checker,
sealer and actual administrative records were read in full ind539b8. Independent
reviewer earlier WHITE/caller/bootstrap authorship is disclosed. Nine unchanged
module bodies and eight unchanged saved-mode functions are inherited premises,
not new self-acceptance or a claim that root freshly read every retained module.

The real controls action returns complete expected trees for inert-fixtures and
integration-fixtures. Each separate fixture tail compares its freshly observed
tree with that expected value. Both tails precede namespace_tail. That final
tail makes a new I.tree(out), stores it, admits descendants under either prefix,
and compares only the ordinary produced-file pins. For controls those pins are
ATTEMPT and RESULT. Its success presence test also omits both fixture roots.
A bounded late change to file bytes, membership, type or a link target can thus
be observed in the final namespace without causing an error. A whole fixture
root removed after its successful individual tail also escapes the final
presence test. No runtime attack or control has been executed to make this
finding; it follows from the code's predicates on the existing final observation.

custody_io.tree sorts complete rows by relative path. Direct subtree rows use
'.' for the root; the whole-output observation uses the fixture directory name.
Only this prefix normalization is needed. Compare the complete ordered normalized
subset from that same final observation against the captured expected tree,
retaining all kind/bytes/sha256/target fields and membership. Do not substitute
a later independent rescan or demand unrecorded inode fields. Compare both
eligible trees even after an earlier first error; retain all observed evidence,
partial output and independently eligible tail outcomes. Where no complete
expectation exists, record partial observations without inventing one.

C02 mutates its fixture after RESULT write, before either fixture-tail comparison.
It does not test this late window. O13 mutates RESULT at the final namespace tree
entry, after its ordinary output tail succeeded. The repair needs that timing
for both fixture trees, with exact checks of earlier successful fixture tails,
changed final records, intended refusal and first-error preservation. It must
cover complete membership/root presence and recorded link/file fields, rather
than happen to fail at an earlier unrelated guard. Original84 controls remain
unexecuted and must be preserved alongside the new discriminating definitions.

F01's prior-pin comparison now binds the post-authentication baseline before
ownership. Ordinary produced files are compared both individually and within the
final observation. The saved-mode wrapper compares its final root to a genuinely
verified post-copy object and retains later observations after earlier failures.
These source-level fixes address the reported gaps; F02-R prevents overall source
acceptance or qualification. All resource thresholds and genuine external/runtime
prerequisites remain unchanged. Metadata/source review grants no control pass,
scientific result, calibration, native forward map or physical acceptance.

Independent administrative checkd5b033 and seal9a7c64 exited0. Root replay1e4e42
exit0 matches every report field except schema:3888 predicates,525 dependencies
(481 inherited plus44 additions),553 fresh whole identities, the two-file patch,
9 unchanged/2 changed/1 new source roles and55+29 control definitions. This script
rechecks all553 observations and eight review preseal pins. Historical failures
and current display recoveries are retained. Bookkeeping does not cure F02-R.

RI160 is the narrow repair in a fresh external reservation, followed by fresh
independent source/control review. R01 path applicability, current environment
capture/profiles, qualification, actual WHITE modes, complete independent custody
and separate saved arithmetic remain required. Full32/periodic/mean/join and
selected public GWOSC conventional reproduction remain separate. Native RI157 is
published and RI159 source is independently under review. RET alone stays paused.
'''
with (D/'MEASUREMENT_ROOT_REVIEW.md').open('x') as f:f.write(text)
verdict=m.save('RI158_ROOT_ADJUDICATION.json',dict(schema='ri158-root-source-repair-adjudication-v1',status='REQUIRE_F02_FIXTURE_NAMESPACE_RECONCILIATION_BEFORE_QUALIFICATION',subject=m.ref(S/'HANDOFF.json'),independent_review=m.ref(R/'HANDOFF.json'),verdict=m.ref(R/'VERDICT.json'),root_review=m.ref(D/'MEASUREMENT_ROOT_REVIEW.md'),metadata_replay=summary,preliminary_trace=m.ref(B/'ri157-root-adjudication-q_wj4pny/MEASUREMENT_PRELIMINARY_FINDING.md'),confirmed_findings=['F02-R'],resolved_source_traces=['F01 prior-pin baseline binding','ordinary produced-file final comparisons','verified saved-mode post/final-root comparison'],qualification_or_whole_source_acceptance=False,controls_defined=84,controls_executed=0,scientific_decode_or_execution=False,resource_thresholds_unchanged=True,RET='paused'))
T=Path(tempfile.mkdtemp(prefix='ri160-white-fixture-custody-repair-',dir=B))
assignment=m.save('MEASUREMENT_REPAIR_ASSIGNMENT.json',dict(schema='ri160-fixture-namespace-repair-assignment-v1',owner='/root/ri116_complete_caller_review',reservation=str(T),predecessor_source=m.ref(S/'HANDOFF.json'),independent_review=m.ref(R/'HANDOFF.json'),root_adjudication=verdict,problem='F02-R: final observed fixture subtrees can differ after successful individual fixture tails, without failure; missing whole roots also escape.',required=['Repair only the actual adapter final-namespace integration and necessary integration-control/contracts/identity closure. Keep RI158 and all predecessors immutable.','From the same final whole namespace observation, extract both fixture roots and every descendant; normalize only the prefix/root label, then compare complete ordered records and all actual kind/bytes/sha256/target fields with available captured expected trees.','Require roots and complete membership when success has valid captured expectations. Cover changed bytes, added/deleted members, missing whole root, type and link-target differences. Do not invent inode expectations or use a later independent scan as the comparison.','Preserve earliest error, every independently eligible tail, complete earlier/final observations and partial evidence. Collect all applicable ordinary-output and fixture mismatch evidence before raising the first; a prior ordinary mismatch must not suppress available fixture comparisons.','When a prior failure returned no complete expectation, retain actual partial namespace, never fabricate expected trees or grant success.','Add meaningful inert O13-style final-tree-entry controls for each fixture tree, after both individual fixture comparisons succeed. Assert the intended late refusal, retained successful earlier observations and changed final records; include simultaneous/earlier-primary-error cases and full membership/root/type/link record coverage.','Preserve existing84 control IDs, order and intent; explicit changes to assertions only when demanded by intended additional final comparison. Keep earlier mode verifier and other unchanged modules byte-identical. Update exact source declarations and closure truthfully.','Fresh nonauthor complete source/control review and root adjudication required before separate actual qualification.'],boundaries=['Only external reservation writes and bounded administrative opaque pin/text checks. No subject/control import,compile,AST,probe,run, scientific/body decode, fixtures, runtime inventories/cards/freezes/admissions, engines or Git/index/repository writes. No new agents.','Do not relax any bounds or original15 WHITE cases,both179-control reports,57 artifacts,74 postchecks,three trees,R01 actual path applicability,current-environment capture/profiles,normal-before-optimized,independent custody and separate saved arithmetic.','Record actual admin checks and all failures/clipped displays; exact handoff namespace/pins. Seal then return to root. Worker handoff does not pause programme.'],RET='paused',native='RI159 under separate source review; do not duplicate'))
print(verdict);print(assignment);print('RESERVATION',T)
