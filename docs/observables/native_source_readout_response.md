# A prepared source record changes two finite outputs

This conditional finite-model result compares two initial source records under one unchanged growth law. All continuation histories and later marks are retained. It supplies a source-record-to-order/readout connection, with no physical mass, energy, time or gravity identification.

## Admitted model and observation assumptions

Use the original fair-mark law through four births in [Native mark-law geometry, Part A](../track_b/native_mark_law_geometry_v1.md), with the optional [incidence register and prepared classical realization](finite_incidence_register.md). At each birth every actual downward-closed ideal is eligible, a fresh maximal vertex is added above exactly that ideal, and its new binary mark is fair. Records are immutable. Positivity, complete-row normalization, marked relabeling covariance and complete marked-diamond identities are inherited properties of that declared law; no uniqueness from DET principles is asserted.

Each selected ancestor counter increments modulo five and the new vertex receives zero. The supplied prepared prefix has no wrap through the four-vertex horizon. Memory, actual-ancestor addressing, preparation and readout are chosen capabilities. The classical realization concerns this prepared history distribution, not arbitrary-input quantum-channel equivalence.

For each prepared root value i, let P_i denote its complete continuation probability law, normalized to one at that prefix. At the terminal four-vertex state, D=1 exactly when the unmarked order is a total chain; Y=1 exactly when at least one counter equals two. D is a formal order diagnostic with no assumed physical access. The joint law is mathematical, not an assertion of a jointly available apparatus.

**Result.** In cell order (00,01,10,11), the exact joint laws are (246,295,0,779)/1320 and (456,290,0,574)/1320 for root values zero and one. The fixed P1-minus-P0 contrasts are −41/264 for D and −7/44 for Y. Both are nonzero, and the events differ on positive-probability histories under both preparations. Distinct events do not imply independent physical channels.

## 1. Prepared prefix and complete branch ledger

Write c=1/5,e=1/44,f_i=f(i),h_i=h(i), with (f_0,h_0)=(1/6,19/30) and (f_1,h_1)=(1/3,7/15). Here c,e are structural constants, not the GDM speed or energy. Both preparations start from a<b, marks(i,0), counters(1,0), with total conditional continuation mass one. The source embedding remains a and its bit is immutable.

Name the two new vertices x,y. The first precursor has exactly three possibilities:

| S3 | Incoming structural weight | Three-parent | Counters(a,b,x) |
|---|---:|---|---|
| empty | c | Edge a<b, isolate x | (1,0,0) |
| {a} | f_i | Fork a<b,a<x | (2,0,0) |
| {a,b} | h_i | Chain a<b<x | (2,1,0) |

For each row below, every ordered pair of newborn bits(b3,b4) in{0,1}² is retained. Its individual weight is the incoming structural weight times q4/4. The q4 values depend only on the inherited root bit i for edge/fork parents, and on no marks for chain parents. Neither the counter update nor D/Y reads newborn bits. Thus all four bit assignments have the same weight and output in each row; summing them gives incoming weight times q4, without deleting any histories.

The following is the entire structural continuation ledger. Counter tuples are in the order(a,b,x,y).

| S3 | S4 | q4 | Terminal counters | (D,Y) |
|---|---|---:|---|---|
| empty | empty | e | (1,0,0,0) | (0,0) |
| empty | {x} | e | (1,0,1,0) | (0,0) |
| empty | {a} | e f_i/c | (2,0,0,0) | (0,1) |
| empty | {a,b} | e h_i/c | (2,1,0,0) | (0,1) |
| empty | {a,x} | 1/8 | (2,0,1,0) | (0,1) |
| empty | {a,b,x} | 65/88 | (2,1,1,0) | (0,1) |
| {a} | empty | e | (2,0,0,0) | (0,1) |
| {a} | {a} | e | (3,0,0,0) | (0,0) |
| {a} | {a,b} | e h_i/f_i | (3,1,0,0) | (0,0) |
| {a} | {a,x} | e h_i/f_i | (3,0,1,0) | (0,0) |
| {a} | {a,b,x} | 1−2e−2e h_i/f_i | (3,1,1,0) | (0,0) |
| {a,b} | empty | e | (2,1,0,0) | (0,1) |
| {a,b} | {a} | e | (3,1,0,0) | (0,0) |
| {a,b} | {a,b} | e | (3,2,0,0) | (0,1) |
| {a,b} | {a,b,x} | 41/44 | (3,2,1,0) | (1,1) |

There are six actual ideals in the edge parent, five in the fork and four in the chain: fifteen structural sequences, each with four bit assignments, hence sixty marked continuation encodings per preparation. Distinct sequences remain distinct even if their terminal orders are isomorphic. There is no further automorphism division or name-permutation multiplier.

Old incomparabilities persist, so an edge-plus-isolate or fork parent cannot become a total chain by appending y. In the chain parent only the full precursor places y above every old vertex. These facts give the D column. Direct equality-to-two tests of the displayed counters give Y. In particular, Y is not a cumulative “ever equalled two” event: the fork's root can increase from two to three, eliminating its positive readout.

## 2. Row checks and complete joint laws

All structural branch weights are positive. For the edge row, f_i+h_i=4/5 and c=1/5 give proper sum

2e+e(f_i+h_i)/c+1/8=6e+1/8=23/88,

so the full complement is65/88. The fork full complement is43/55 for i=0 and49/55 for i=1: h_0/f_0=19/5 and h_1/f_1=7/5 give the stated values directly. The chain proper sum is3e and its full complement41/44. Every row sums to one.

The incoming weights also normalize: (6+5+19)/30=1 for i=0 and(3+5+7)/15=1 for i=1. Keeping the two fair-bit factors in each encoded history therefore gives complete continuation mass one.

Summing the ledger by joint cell gives

p_i(0,0)=2ce+f_i(1−e)+h_i e,
p_i(0,1)=c(1−2e)+f_i e+2h_i e,
p_i(1,0)=0,
p_i(1,1)=h_i(1−3e).

For reconstructible exact arithmetic, over denominator1320 the contributions to p_i(0,0) are12+215+19=246 for i=0 and12+430+14=456 for i=1. Contributions to p_i(0,1) are252+5+38=295 and252+10+28=290. The chain/full products give779 and574 for p_i(1,1).

| Prepared root i | p(0,0) | p(0,1) | p(1,0) | p(1,1) | Total |
|---|---:|---:|---:|---:|---:|
| 0 | 246/1320 | 295/1320 | 0 | 779/1320 | 1 |
| 1 | 456/1320 | 290/1320 | 0 | 574/1320 | 1 |

Indeed246+295+779=1320 and456+290+574=1320. The zero(1,0)cell follows from the complete event accounting, not removal of any structural support.

The D marginals are779/1320 and574/1320. The Y marginals are1074/1320 and864/1320. Therefore

Delta_D=(574−779)/1320=−41/264,
Delta_Y=(864−1074)/1320=−7/44.

As a separate symbolic check, f_1−f_0=1/6 and h_1−h_0=−1/6. The formulas above give Delta_D=−(1−3e)/6 and Delta_Y=(2e−1)/6, reproducing the fractions. Their exact relation is Delta_Y=(42/41)Delta_D, or Delta_Y−Delta_D=−1/264. This relation does not identify either output with a physical variable.

## 3. Event distinction, preparation and transport

D is contained in Y on this complete continuation domain. Their symmetric difference is precisely the(0,1)cell, with positive masses295/1320 and290/1320 under the two preparations.

An explicit common supported witness uses S3=empty, S4={a}, b3=b4=0. Its terminal counters are(2,0,0,0), with D=0,Y=1. The individual marked-history weight is c(e f_i/c)/4=e f_i/4, equal to1/1056 for i=0 and1/528 for i=1. These positive witnesses establish distinction under both laws; they are not postselection of the operational continuation distribution.

The starting counters are consistent with a zero-initialized birth of a followed by b over{a}: only a is incremented. Subsequent counters increment precisely actual ancestors and never modify old records or comparabilities. All displayed counts stay below five, preserving the admitted no-wrap interpretation. The initial embedding singles out the same a even after x or y is born as another root. The source is not reselected from a terminal shape; this embedding is bookkeeping, not an additional input to q.

Transporting all vertex identities simultaneously transports ideals, counters, marks and the initial embedding. Admitted q equivariance preserves branch weights; the fixed counter update commutes with this transport. Total-chain and existence-of-a-two-counter events ignore names. The joint laws therefore do not arise from a numerical-label artifact. This does not assert that flipping bit coordinates while leaving q unchanged is a coordinate transformation.

The classical prepared register suffices. Its mathematical update and inherited optional quantum map obligations remain at their accepted scopes; no coherent sum over histories or arbitrary-input classical quantum simulation is introduced. Counter memory does not feed back into q.

## 4. Scope and remaining mapping obligations

Both prescribed marginal contrasts are nonzero, and the events are distinct on positive support, so the fixed candidate succeeds at its finite conditional criterion. No seed, prefix, upper mark, support, bit law, output, horizon or contrast orientation was changed.

The established ingredient is a concrete map from a prepared immutable source record to a changed continuation order law and a changed fixed optional readout under that same q. It is stronger than merely exhibiting different marks or selecting two endpoint shapes after the fact. It remains a theorem about this chosen finite model, not uniqueness of q from DET principles.

The source bit is not energy/action. D is not acceleration or position. Y is not phase or elapsed time. Birth count is not physical duration. Native constructions corresponding to the current mass/gravity comparison’s X,P,phi,J,e, scales and common-energy coupling remain absent from this map. No sign-fitting hot/cold assignment, calibration or claim of live residual-to-source backreaction is made. Physical preparation, actual-ancestor addressing, memory, readout, acquisition and costs remain supplied premises.

The [native mapping plan](../coordination/NATIVE_MASS_MAPPING.md) retains these additional obligations. The current mass/gravity comparison remains conditional on its imported Hamiltonian, variables and scales. No sign-fitting conversion, scientific execution, calibrated prediction, physical validation, efficiency or novelty claim follows from the finite calculation. All earlier source statements retain their original mathematical scope.
