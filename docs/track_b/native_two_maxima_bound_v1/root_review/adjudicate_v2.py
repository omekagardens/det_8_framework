import hashlib,importlib.util,tempfile
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri202-root-two-maxima-review-kw07pwnj';Q=B/'ri201-native-two-maxima-09928c97';hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes();assert hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
review='''# Independent root review of the complete two-maxima class

30 September 2026, Honolulu. Accept RI201 conditionally on the explicit
unchanged finite-prefix theorems. This is a manual native-law result; no
certificate, canonical vector, maximum or scientific target was evaluated.

Root read the complete proof (3b3b0a), handoff (1dbdda), accepted RI41
seed/height/ideal-floor statements (e9674a and prior677332), the accepted
RI63 potential/mixture definitions (prior4b9d36), and the complete final
author administrative checker plus both retained premise clarifications
(c4834f). The printed numerical M5 appears in inherited text but is not
an operand. Prior root authorization explicitly admitted the named finite
scalar facts, not a new scientific-body read or certificate verification.

For a six-parent with exactly two maxima, deleting both leaves a four-parent
R. Every vertex lies below at least one maximum, so the two precursor ideals
cover R. The converse construction preserves exactly two maxima. Hence
all parents and all compatible E,D, including full/equal precursors and all
records, are covered. Ideals omitting both maxima are exactly J(R), with
full R retained. The single-omission sectors are the remaining probabilities
of each complete deletion row. With x,y the positive subrow sums, the full
positive complements give 0<x,y<1, U6=2-x-y+sum p*q/B. Expanding the centered
cross-moment uses sum B=1, so its constant is exactly one.

The marked diamond identities transport both ratios to H_S=R+z_S. Every
second slot is proper, so its local record excludes the auxiliary bit.
The same arbitrary auxiliary bit is therefore valid for both identities,
without erasing the original cap bits. If E=D the shared entry is one
entry; its repeated factor must not be treated as two independent entries.
All canonical factors, positive parts, minima, ties and corrections remain.

The inherited RI41 floor is for all ideal probabilities, including the
full ideal, not the q/2 newborn-mark probability. Put K=681472/9. Then
C<=K sum p*q<=Kxy. The four interpolation coefficients (1-x)(1-y),
x(1-y),(1-x)y,xy are positive and sum to one. Their values are 2,1,1,K;
K>2 makes U6<=2-x-y+Kxy<K strict even with identical deletion rows and a
nonstrict floor. This independently establishes the entire-class estimate.

For A4 only the empty birth preserves height one, so the same accepted
height theorem gives z4>1/2. In u5(A5,empty), the complete subset sizes
1,2,3,4,5 have multiplicities5,10,10,5,1 and alternating numerator/denominator
signs. With seed a=2/3,d=1/4,e=1/44, the product is
z4^5*d^10/(e^10*a^5)=(3z4/2)^5*11^10. The empty-parent factor is one.
All other proper A5 slots are positive, so M5>=U5(A5)>u5>10^9.
Manually, (3/4)^5=243/1024>1/8, 11^10>10^10, and10^10/8>10^9.
There is no assertion that A5 maximizes the sum. RI199's same-law target
and theta definition give T>(468/5)(1+M5)-1/2>10^9.
Finally681472<9*76000=684000 and76000<10^9, hence U6<K<76000<T.

Independent nonauthor reviewer /root/qr_opportunities agrees on every
step, including all-record/full-ideal scope and strictness. Its complete
reads/pins20ffdf,5961c0,2a551c,119425 all exited zero. The author reports
actual final5 a3e46e exit0 externally; root treats this as author evidence,
not its own execution. Root's separate administrative check415d8d exit0
freshly verifies18direct sources/617021bytes plusfive packet files,
23selected references, complete current/predecessor five-file namespaces,
fifteen preserved boundary objects and unchanged executable obligations.
Inherited423 and predecessor26 remain by exact reference, not new replays.
All six author diagnostic records and three checker revisions stay intact:
locale/code-unit ordering and JSON insertion-order failures were corrected
administratively; none was a mathematical or scientific test failure.

One- and two-maxima rows are now below T. The global maximum still includes
three through six maxima. Thus actual W, both margins, shared H30, other
connected-parent obligations and physical correspondence remain undecided.
The next native question is the complete three-maxima class, with an exact
triple-omission sector and common-row transport. Publication/qualification/
actual measurement claims stay separate. RET remains paused.
'''
with (D/'RI201_ROOT_PROOF_REVIEW.md').open('x') as f:f.write(review)
decision=m.save('RI201_ROOT_ADJUDICATION.json',dict(schema='ri202-root-ri201-adjudication-v1',status='ACCEPT_COMPLETE_TWO_MAXIMA_CLASS_CONDITIONAL_THEOREM',handoff=m.ref(Q/'HANDOFF.json'),proof=m.ref(Q/'TWO_MAXIMA.md'),root_review=m.ref(D/'RI201_ROOT_PROOF_REVIEW.md'),metadata=m.ref(D/'RI201_ROOT_METADATA_CHECK.json'),root_check=dict(chunk_id='415d8d',exit_code=0),nonauthor_review=dict(agent='/root/qr_opportunities',receipts=['20ffdf','5961c0','2a551c','119425'],result='no mathematical blocker'),author_final_receipt=dict(chunk_id='a3e46e',exit_code=0,reported_by_author=True),theorem='Every actual marked six-parent with exactly two maxima has U6<681472/9<76000<T.',native_witness='M5>U5 empty-slot lower bound>10^9 from the full A5 deletion product and accepted A4 height theorem; printed numerical M5 unused.',premises=['unchanged RI41 all-four-parent ideal floor and height bound','strict fixed-prefix positivity, normalization, locality and all marked diamonds','complete canonical strict-mixture law','accepted RI199 target relation and theta definition'],global_M6_bound=False,actual_W_decided=False,both_margins_or_H30=False,new_finite_verification=False,scientific_body_read_or_execution=False,new_qualification_credit=0,ret_paused=True))
reservation=Path(tempfile.mkdtemp(prefix='ri203-native-three-maxima-',dir=B))
assignment=m.save('RI203_NATIVE_ASSIGNMENT.json',dict(schema='ri203-root-native-three-maxima-assignment-v1',status='ASSIGNED_AFTER_RI201_INDEPENDENT_ADJUDICATION',thread_id='01a074c4-4b09-76a3-8cb2-0caf116f6b9c',predecessor=decision,reservation=str(reservation),question='Settle the entire three-maxima marked six-parent class against the unchanged sufficient target T, focusing on its exact triple-omission product.',domain='R=P-{1,2,3} has three events; maximal-event precursor ideals E1,E2,E3 cover R. All three-event bases, all compatible ideal triples, every original/cap mark and every proper ideal of P remain.',starting_partition='Independently derive U6=3-L+sum_i C2_i+C3. q_J is the actual row on R plus the maxima indexed by J. C2_i=sum over A ideals R with Ei subset A of q_ij(A+i)*q_ik(A+i)/q_i(A+i). C3=sum over ALL A ideals R q_empty(A)*q_12(A)*q_13(A)*q_23(A)/(q_1(A)*q_2(A)*q_3(A)). Include full R and all multiplicities.',available_bounds='Inherited RI41 ideal floor gives each C2_i<K=681472/9 using complete subrow sums. RI201 gives T>(468/5)(1+M5)-1/2 with native M5>10^9. These are available but do not by themselves settle C3. Retain exact L and compare C3<=T-3+L-sum C2_i.',candidate_transport='With H_A=R+z_A, check q_empty(Ei)q_i(A)=q_empty(A)q_H_A(Ei) and q_i(Ej)q_ij(A)=q_i(A)q_(H_A+i)(Ej), preserving every auxiliary/original bit and canonical shared factor. Seek a native joint product bound, or a specific actual violating parent.',successful_return='Complete-class proof or concrete admitted violating parent; if unresolved, substantive structural reduction and the precise smaller remaining native inequality. An auxiliary estimate that fails is not a counterexample and a coarse cubed independent floor alone is not a result.',scope='Manual analytic proof. Existing accepted analytic finite theorems, including named RI41 floor/height and native RI201 witness, allowed as explicit inherited premises. No new certificate/vector/table/scientific-body reads, automated proof arithmetic, graph/LP/subject runs, fixtures/runtime/cards, repository/Git operations or RET work. Do not expand printed numeric M5 use unless mathematically necessary and explicitly explained; native witness preferred. Compact exact references; earlier423/26 remain inherited, not fresh replays.',remaining_classes='Four through six maxima remain separate; global M6 and actual W/H30 are not presumed.',return_instruction='Seal source and actual administrative-check receipts for root independent review. Root owns publication and further assignments.'))
print(decision);print(assignment);print(reservation)
