# Complete five maxima bound for the unchanged native law

30 September 2026, Honolulu. Manual theorem submitted for independent review.

Every actual marked six-event parent with exactly five maxima satisfies

    U6 < 5+10K+80K^2+11/256
       < 462,080,760,006 < 463,000,000,000
       < 465,000,000,000 < T,       K=681472/9.                 (1)

The proof retains all five omission sizes. The triple-omission estimate
uses selected-ideal coverage: both retained caps already belong to the
selected ideal, so only the single old event can need covering. Four-
and five-omission sectors use the accepted finite canonical-support
lemma, while keeping every extra old maximum in their exact potentials.

The result is conditional on the explicitly named unchanged finite-prefix
facts. It is neither a new certificate verification nor a derivation of
the chosen law from DET axioms. One through four maxima were previously
accepted; this submission adds five. SIX maxima, global M6, actual W,
both individual margins, H30 and physical correspondence remain open.

## 1. Inherited premises and target

Keep the exact selected seed and canonical completion, all binary marks,
every labeled ideal, strict positive complete rows, marked equivariance,
precursor-record locality and ordinary marked diamonds.

The accepted four-parent bounds, with their distinct domains, are

    q4(S)>=epsilon=9/681472                   for ALL ideals,
    q4(S)>=u4(S)/8                          for PROPER ideals. (2)

A full four-parent slot uses its actual positive complement and the
all-ideal floor, never a proper-slot coefficient formula. Let K=1/epsilon.

The actual proper parent-five probabilities remain

    q_Q(S)=u5(Q,S)[theta+(35/36)alpha_c(Q,S,r)^(min,5)],
    theta=1/[72(1+M5)].                                        (3)

The canonical vector and its shared coordinates are fixed. RI63's
accepted finite theorem says that every positive canonical component
is everywhere defect-neutral. The accepted RI205 consequence is:
a proper parent-five birth whose six-terminal has at least four
maxima has zero canonical boundary coefficient, hence q_Q(S)=theta*u5(Q,S).
This does not erase its positive restoration term or give an all-size law.

The accepted native antichain witness and unchanged target give

    M5>(3/4)^5*11^10>5,000,000,000,
    T>(468/5)(1+M5)-1/2>465,000,000,000.                         (4)

The same hand witness also gives

    theta < 2^(-38),                                           (5)

since 2^38=274,877,906,944<360,000,000,000=72*5,000,000,000.
No printed numerical M5, full canonical vector or actual theta is
evaluated. Source identities and reading limits are retained in
[SOURCE_REFERENCES.json](SOURCE_REFERENCES.json).

## 2. Entire marked domain

Let C={1,2,3,4,5} be the maxima of P and R=P minus C={x}.
Each precursor E_i is either empty or R, and their union is R.
At least one cap therefore lies above x. Conversely, every such choice
gives exactly five maxima. The domain includes all compatible repeated,
empty and full precursors, all original/cap marks and every labeling.
All five precursors empty is excluded: it would give six maxima.
That class is not being folded into this proof.

For each proper J subset C, let Q_J be R with caps J appended above
their original E_i. Let q_J be its actual complete probability row
with original restricted marks, and B=q_empty the singleton row.
Concatenated subscripts denote unions of cap sets, not products.

For a proper ideal S of P, set I=S intersect C and O=C minus I.
Then O is nonempty and

    S=A union I,  A in J(R)={empty,R},  union_(i in I)E_i subset A.
                                                                    (6)

This is a bijection with the proper ideals, including multiplicities
of distinct labeled ideals even when canonical component keys repeat.
In particular every A=R choice occurs. The complete maximal-deletion
potential is

    u6(P,S)=product_(nonempty H subset O)
                   q_(C minus H)(S)^((-1)^(|H|+1)).             (7)

All old vertices of P lie below some cap, so its maxima are exactly C.
Extra old maxima may reappear inside the deleted parents and are retained
in the later expansions of their own potentials.

## 3. Exact five-sector identity

If only cap i is omitted, (7) is q_(C minus i)(S). Let L_i be the
mass in that complete five-parent row of ideals not containing every
other cap. Empty supplies positive omitted mass, and its positive
full ideal supplies mass in the retained sector. Thus 0<L_i<1.
All five such sectors sum to 5-L, where L=sum_i L_i and 0<L<5.

For omission of two caps j,k, let I=C minus {j,k}, with |I|=3.
There are ten sectors, each equal to

    C2_I = sum_A q_(I+j)(S)q_(I+k)(S)/q_I(S),  S=A union I.    (8)

For omission of three caps O, retain a pair I=C minus O. There are
ten sectors. The seven deletion factors give

    C3_I = sum_A q_I(S)
           [product_(H subset O, |H|=2)q_(I+H)(S)]
                  /[product_(h in O)q_(I+h)(S)].               (9)

Each sum in (8)-(9) uses exactly the A permitted by (6).

For omission of four caps O=C minus {i}, retain only i. There are
five sectors, with S=A+i and E_i subset A. All fifteen factors give

    C4_i = sum_A
        [product_(H subset O, |H|=3)q_(i+H)(S)]
        [product_(h in O)q_(i+h)(S)]
        /[q_i(S) product_(H subset O, |H|=2)q_(i+H)(S)].        (10)

Finally, omission of all five caps leaves A in J(R). Its thirty-one
nonempty deletion subsets give

    C5 = sum_(A in J(R)) B(A)
           [product_(|J|=4)q_J(A)] [product_(|J|=2)q_J(A)]
            /[product_(|J|=3)q_J(A) product_(|J|=1)q_J(A)].     (11)

In (11) single through quintuple deletions have multiplicities
5,10,10,5,1 and signs +,-,+,-,+. Their parent sizes are respectively
5,4,3,2,1. Thus the exact independent partition is

    U6 = 5-L + sum_(|I|=3)C2_I + sum_(|I|=2)C3_I
                    + sum_i C4_i + C5.                        (12)

No sectors overlap or lose full base ideals. In (8) q_I(R+I) is
FULL in its four-parent denominator. In (9) all four-parent
denominators are proper, because they exclude their additional cap.
This remains true when A=R and q_I(S) itself is a full three-parent
probability.

## 4. Ten double omission sectors

Each numerator in (8) is a strict subrow of a complete five-parent
row, excluding at least its positive full ideal. The all-ideal
four-parent floor applies to every denominator, including full.
Therefore

    C2_I <= K sum_A q_(I+j)(S)q_(I+k)(S)
          <= K [sum_A q_(I+j)(S)] [sum_A q_(I+k)(S)] < K.       (13)

Expanding the product of subrow sums adds nonnegative off-diagonal
terms. It does not assume statistical independence or independently
adjust shared canonical coordinates.

## 5. Selected-ideal lemma for ten triple sectors

Fix a retained pair I and let S=A union I satisfy (6). The common
three-parent base is Q_I=R+I. We prove

    product_(h in O)q_(I+h)(S) >= q_I(S)epsilon^2/8,
    O=C minus I.                                               (14)

The three omitted precursors do NOT cover the retained caps. That
all-ideal premise is neither assumed nor needed.

If A=R, every event of Q_I is in S. In any Q_(I+h), h is the sole
omitted maximum, and its potential is q_I(S), with S full only in
the smaller Q_I.

If A is empty, each retained cap has empty precursor by (6).
Both caps are selected in S. Original coverage forces at least one
omitted cap h to have E_h=R, covering the only old vertex x outside S.
In Q_(I+h), h is again the sole omitted maximum. The other maxima,
the retained caps, are already selected. Thus once again

    u4(Q_(I+h),S)=q_I(S).

This four-parent slot is proper, so (2) gives its probability at least
q_I(S)/8. The other two four-parent factors are each at least epsilon,
proving (14) in every allowed case and for every original record.
The proof is restricted to these selected ideals, not a new general
covering-precursor statement.

Insert (14) in (9). Each of the three numerator sums is a strict
subrow of its complete five-parent row. Hence

    C3_I <= 8K^2 sum_A product_(H subset O, |H|=2)q_(I+H)(S)
          <= 8K^2 product_(H subset O, |H|=2)[sum_A q_(I+H)(S)]
           < 8K^2.                                             (15)

The ten triple sectors contribute less than 80K^2. The stronger
constant 8 is essential to the available final comparison; it comes
from the proved sole-omitted-maximum case, not a guessed improvement
of RI205's bound.

## 6. Higher omission sectors with exact canonical support

The companion [higher omission proof](HIGH_OMISSION_LEMMA.md) derives

    C4_i <= theta^4*3*110^11 < 2^(-73) < 1/128,
    C5   <= 2*theta^5*3^8*110^24 < 1/256.                       (16)

For a size-five numerator in (10), the selected retained cap i lies
below the newborn, while the three other caps remain maximal.
Together with the newborn there are at least four terminal maxima.
For a size-five numerator in (11), all four caps remain maximal;
the newborn supplies a fifth. The accepted support lemma therefore
gives the EXACT theta*u5 expression at precisely these slots.

The companion does not assume caps alone exhaust the omitted maxima
of those five-parents. The sole old vertex can reappear as an omitted
maximum. Selected-ideal coverage limits this to at most one relevant
deleted parent in each four-omission sector; original coverage gives
the analogous limit among the five four-cap parents in (11).
Every correction factor, including the empty-parent factor when
present, is kept before applying bounds.

The estimates use the inherited all-ideal seed floors q1>=1/3 and
q3>=1/110, ordinary probability upper bounds, exact cancellation of
identical actual factors, and (5). Their complete parity counts are
shown in the companion. No canonical terms are erased in the lower
sectors, where the support condition has not been established.

In particular the higher-sector total obeys

    sum_i C4_i + C5 < 5/128+1/256=11/256<1.                    (17)

## 7. Comparison and unchanged dependencies

Equations (12)-(17), with L>0, prove

    U6 < 5+10K+80K^2+11/256
       < 6+10*76000+80*76000^2
        =462,080,760,006 < 463,000,000,000 < T.                (18)

The hand arithmetic uses K<76000 since 681472<9*76000=684000;
76000^2=5,776,000,000; 80 times this is 462,080,000,000;
and the remaining summands are 760000+6. The strict target comparison
in (4) is unchanged. This proves U6<T, hence the requested U6<=T,
uniformly over the entire five-maxima marked class.

All probabilities remain entries of the same actual canonical law.
Original/cap marks, canonical minima, positive parts, ties, shared
indices, zero branches, the known N_i corrections and their products
are retained unless their zero coefficient is proved by the support
lemma at the specific higher-sector slot. The marked diamonds
transport every original and both newborn bits; no record is fitted
or averaged away. No free-coefficient example is offered as a native
counterexample.

This is a finite conditional theorem, not a new executable verification
or a physical prediction. The native M5 witness remains only a lower
bound; no maximizing-parent or actual-scale claim is made.

## 8. Evidence and stopping boundary

All new arithmetic and proofs are manual. Only administrative identities,
references, namespaces and text hygiene are machine checked. No new
scientific body/vector/certificate, automated proof arithmetic, graph/LP
or subject execution, fixture/runtime/card, new agent/thread, repository
or Git/index write is part of this packet.

The accepted one-through-four-maxima results remain unchanged. Six
maxima and the global M6 comparison are not settled here, so actual W,
both margins, H30 and physical correspondence remain open. Original
P2/P3, Y=1/4, shared T1, the other eight connected parents, all five Di,
and executable obligations 92/34/35 and 31/139/20/42 remain uncredited.
Inherited423 and older source collections stay by exact reference,
not new replays. RET remains paused; Option B and Status M are unchanged.

Stop at the sealed source handoff for root independent adjudication.
Root retains Git/publication and the choice of any successor. This
packet does not start or design the six-maxima obligation.
