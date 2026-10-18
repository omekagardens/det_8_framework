"""Root RI157 provenance reconciliation and recorded manual proof disposition."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
D=Path(__file__).resolve().parent
B=D.parent
HLP=B/'ri122-root-execution-review-6whn_vky/metadata.py'
assert len(HLP.read_bytes())==3144 and hashlib.sha256(HLP.read_bytes()).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',HLP);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
S=B/'ri157-correlated-capacity-proof-tusjyk77';R=B/'ri157-independent-cap-review-wt1tl1ip';P=B/'ri157-root-review-jco7p6tf'
m.verify(S/'HANDOFF.json',dict(bytes=10114,sha256='968e3c853ce107aceff080126b8ca22f8ba846bbba914ff0b13a32360c660b8c'))
m.verify(R/'HANDOFF.json',dict(bytes=5929,sha256='daccfac1950db64177f5ad6d4fbb2a30fe329ae88efc6bd4b01fe6f9786a36f1'))
for base in (S,R):
 h=m.load(base/'HANDOFF.json');assert sorted(p.name for p in base.iterdir())==sorted(h['namespace'])
 assert len(h['namespace'])==10 and len(h['payloads'])==9
 for row in h['payloads']:m.verify(row['path'],row)
a=m.load(D/'METADATA_CHECK.json');b=m.load(R/'METADATA_CHECK.json')
assert {k:v for k,v in a.items() if k!='schema'}=={k:v for k,v in b.items() if k!='schema'}
assert a['predicates']==15407 and a['final_fresh_identities']==234
for row in a['observed_identities']:assert m.identity(row['path'])==row
fin=m.load(R/'FINAL_PIN_CHECK.json')
for row in fin['reviewer_preseal_payloads']:m.verify(row['path'],row)
assert m.load(R/'VERDICT.json')['repairs_required']==[]
assert (D/'NATIVE_CHECK.stderr').read_bytes()==b''
summary=m.save('ROOT_METADATA_REPLAY.json',dict(schema='ri157-root-replay-summary-v1',status='MATCH_EXCEPT_SCHEMA',actual_replay=dict(chunk='025829',exit_code=0),report=m.ref(D/'METADATA_CHECK.json'),independent_report=m.ref(R/'METADATA_CHECK.json'),checker=m.ref(D/'check_native.py'),reviewed_checker=m.ref(R/'check_metadata.py'),adaptations=['output directory R','report schema'],predicates=15407,dependencies=223,inherited=193,additions=30,selected_bytes=9791698,administrative_bodies=77,historical_typed_refs=1616,current_typed_refs=89,historical_states=17,historical_state_compared_to_current=False,fresh_identity_rechecks=234,review_preseal_pins_rechecked=8,mathematical_acceptance='separate manual adjudication',scientific_or_subject_execution=False))
text='''# RI157 final root proof review

30 September 2026 UTC. Accept the canonical-cap and signed-contrast increment
with the actual-capacity gap preserved. This is manual finite mathematics under
the unchanged accepted RI36/RI41/RI63 law, not a newly executed certificate or
physical result. The preliminary note remains unchanged at its original path;
this final disposition follows the complete sealed nonauthor review.

Root read all three RI157 manuscripts, the full dependency note, RI36 section4,
RI41 retention/proper table and the RI151 hook/fork incidence passage. The
independent reviewer additionally traced the RI63 law/deletion correspondence.
Root has reviewed the full independent narrative, verdict, administrative checker,
actual checks and sealing source. Earlier native reviewer and separate WHITE
roles are disclosed; neither author/coauthor agreement nor bookkeeping is
substituted for independent proof review.

The height-row subtraction retains two distinct arm occurrences and the positive
full complement: w,p<P=113/11480 and s<P/2. Component lower bounds act on each
deletion potential: w,p,s>=1/352. The complete chain row gives
1/2<b_i<2267/2464<a. RI41 explicitly retains RI36's proper-slot bound1/8.
With the same fork arm e_i in both contributions, f_i/2+min g_i,u>=135/1408;
this lower bound does not combine incompatible independent extrema.

For N_i>0, delta=135/57728>1/440 yields N_i<14(p_i-1/440), p_i<1/100.
The full-complement condition N_i<a_theta<1 makes
F_i-[2-2N_i+N_i^2/p_i]=(1-a_theta)(2N_i-1-a_theta)<0.
The two successive convex endpoint bounds yield F_i<35743/12100. The N_i=0
branch separately gives F_i<2, including the positive-part boundary. Hence
F_i<35743/12100<71/24<E_0,E_1 for both orientations. The retained cap is
Mcap=max(E0,E1), and Z=R lies strictly between1/8 and12/95. This neither
identifies globalM6 with Mcap nor actualrho with R; no root-order branch is chosen.

The normalized marked ratios lie in(0,1), so T<(3/2)P and each contrast
bracket H is greater than-2. The individual upper bounds are -71/72,-107/72,
and -235/20664; all are strictly negative. Positive d7 and v therefore force
p1>p0 or s1>s0, with no particular disjunct selected. Dropping only negative
contributions for an upper bound yields v<2theta Dminus and
Dminus<1147/126280, hence0<v<1147/9092160.

B=12lambda*j0/(1+2Mcap), j0>71/72 and Mcap<3. A strict pass v>B would require
lambda<1147/15370080<1/13000. The factor J/b0^3>7/4 follows from b1>1/2,b0<1,
so the same pass requires Dminus>213d7, or the corresponding component bound
with factor8733. A proved reverse weak bound Dminus<=213d7 would instead yield
strict v<B and reject this sufficient envelope. Neither actual inequality is
established by this packet. A1/1000 grid for the complete final109-vector would
supply a separate conditional rejection, but discovery rounding supplies no such
premise. No coefficient body, scale, scientific target or control was evaluated.

Actual capacity sign, marked separation/lambda magnitude, adequate joint q/v
budget, W/C2/C3 and sharedH30 remain open. P2/P3, numericalY=1/4,31 focused
(23F01+8F02),139 policy(77native+62audit),20native/42audit deeper obligations,
other eight parents, fiveDi, sharedT1, strict endpoints and ideal multiplicities
are unchanged. The result says nothing about all-size existence, QM or gravity.
Measurement qualification and conventional public GWOSC reproduction remain
separate, with calibration and the native forward map open. RET stays paused.

Root administrative replay025829 exit0 matches every independent report field
except schema:15407 predicates,223 dependencies and234 fresh identities. This
script rechecks the same current identities and eight review preseal pins.
Source/review namespaces remain10/9 each. Full diagnostic reports are retained
externally; compact records never claim a self-contained runtime archive.

The next native question is whether the entire unchanged final RI41 witness is
on the asserted grid. RI159 prepares the smallest exact checker, independently
structured saved auditor and qualification contract. This source-only handoff
requires fresh source/control review and a bounded actual admission before any
certificate-body read or numerical conclusion. It does not restart global growth
enumeration, change the witness, or add another q-floor reduction.
'''
with (D/'ROOT_MANUAL_REVIEW.md').open('x') as f:f.write(text)
verdict=m.save('RI157_ROOT_ADJUDICATION.json',dict(schema='ri157-root-proof-adjudication-v1',status='ACCEPT_ACTUAL_CANONICAL_CAP_AND_SIGNED_CONTRAST_BOUNDS_WITH_CAPACITY_GAP',source=m.ref(S/'HANDOFF.json'),independent_review=m.ref(R/'HANDOFF.json'),independent_verdict=m.ref(R/'VERDICT.json'),root_review=m.ref(D/'ROOT_MANUAL_REVIEW.md'),preliminary_review=m.ref(P/'NATIVE_PRELIMINARY_REVIEW.md'),metadata_replay=summary,accepted=['F_i<35743/12100<71/24<E_i','retained Mcap=max(E0,E1); Z=R','0<v<1147/9092160','pass requires lambda<1147/15370080<1/13000 and Dminus>213d7'],repairs_required=[],actual_capacity_decided=False,grid_premise_accepted=False,global_M6_or_actual_rho_identified=False,adequate_q_v_budget_proved=False,W_C2_C3_H30_decided=False,scientific_body_decode=False,target_or_control_execution=False,physical_claim=False,RET='paused',next_native_question='Exact whole-final-witness grid premise; source and qualification preparation before bounded actual audit',measurement='RI158 source/output repairs sealed and assigned fresh independent source/control review;84 controls defined,0 executed'))
# Assignment follows the acceptance above; this creates only an empty external reservation.
Q=Path(tempfile.mkdtemp(prefix='ri159-final-witness-grid-source-',dir=B))
cert=m.REPO/'docs/track_b/native_growth_height_normalization_v1/CERTIFICATE.json'
c=m.ref(cert);assert c['sha256']=='3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969'
assignment=m.save('NATIVE_SUCCESSOR_ASSIGNMENT.json',dict(schema='ri159-final-witness-grid-source-assignment-v1',status='ASSIGNED_AFTER_RI157_ROOT_ACCEPTANCE',owner_thread='01a074c4-4b09-76a3-8cb2-0caf116f6b9c',reservation=str(Q),predecessor_adjudication=verdict,predecessor_source=m.ref(S/'HANDOFF.json'),question='Does the entire unchanged final109-component RI41 witness, including default and every override, lie on the1/1000 grid required by the conditional envelope rejection?',deliverables=['Minimal source-only exact grid checker and independently structured saved-result auditor.','Complete intended result and bounded future input/output contract, with whole original certificate/source/accepted-law linkage.','Meaningful inert qualification cases for all109 coverage, default/overrides, reduced rational divisibility, malformed/duplicate keys and labels, missing/extra component indices, off-grid terms, identity drift and exact result disagreement; do not execute.','Analytic consequence ledger for grid PASS/FAIL/refusal: a grid pass may justify only the already proved conditional envelope rejection, never W/H30 or physical acceptance.','Exact handoff namespace, whole pins and actual administrative check outcomes; seal then return for independent review.'],original_certificate=c,original_source=m.ref(cert.with_name('check.py')),original_manuscript=m.ref(cert.with_name('NORMALIZATION.md')),grid_clarification=m.ref(B/'ri155-root-capacity-review-0f1typdz/RI157_GRID_PREMISE_CLARIFICATION.json'),constraints=['Source-only text reading and bounded administrative opaque pin checks. No actual certificate body or coefficient decode now.','Use complete final109-vector defined by default_alpha and every override under the literal ri41-height-primal-v1 contract, seed interior_a,parent_size4,potential RI-38 maximal-deletion,component order increasing minimum canonical-local-key. Preserve exact original byte pin and accepted root-order/law linkage.','Do not mistake selected free-coefficient rounding for the complete final witness. Do not reconstruct graphs, global masses, normalization scales or original heavy verifier. Accepted finite-law/root ordering premises remain explicit.','Require strict duplicate-key rejection and bounded exact rational parsing; independent auditor must separately reconstruct full vector and compare every declared scientific result field, not just a digest or producer booleans.','Fixed pin and historical acceptance may supply original domain/order linkage; a shape-only root check must not be relabeled an independent reconstruction of root order.','Do not change thresholds, seed, amplitude, support, historical evidence or any existing source.','No subject/control import,compile,AST,probe,run; no fixtures created or executed; no scientific engines, active runtime inventories, cards, freezes, admissions or Git/index/repository writes. No new agents.','Root owns independent adjudication and any subsequent bounded qualification/actual admission. A source seal is a worker return boundary, not programme completion.'],retained_open=['actual grid premise until admitted exact audit','actual v>B comparison unless a separately accepted implication decides envelope rejection','adequate joint q/v budget','W/C2/C3/sharedH30','global M6 and actual rho','other eight parents/fiveDi/strict endpoints/marked multiplicity/P2/P3/Y1/4 and31/139/20/42 obligations','calibration/native forward map/physical claims'],RET='paused'))
print(verdict);print(assignment);print('RESERVATION',Q)
