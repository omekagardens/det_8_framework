# RI-85 — complete four-vertex cap first-departure design

25 September 2026 UTC. **Analytic design; coefficient feasibility unevaluated.**
This packet specifies one complete, bounded intrinsic support and one exact
width target. It creates no executor and authorizes no inherited helper,
coefficient, solver or order-enumeration execution. Coordinator review of the
frozen domain is required before implementation or calculation.

## 1. Question, baseline and restrictions

[RI-84](../native_growth_first_departure_check_v1/RESULT_REVIEW.md) rejected
the preceding three-class, record-blind perturbation: its exact simultaneous
harmonic matrix has rank three. That result does not reject a larger support.
The present explicitly assigned enlargement is **all** orders

\[
 T=C_3\oplus Q,\qquad |Q|=4,\quad |\operatorname{Max}(Q)|\geq2.
 \tag{1}
\]

C_k is a k-chain, A_k a k-antichain; an ordinal sum places every element of
its first argument below every element of its second. Disjoint union is
written \(\sqcup\). These are unmarked isomorphism classes, not selected
labeled realizations or fitted geometric shapes.

Keep the actual accepted strictly positive marked prefix at parent sizes
below six, including the actual RI-63 strictly mixed q5. The baseline B uses
the common RI-38 half-scale continuation at six and above. In particular,
for every proper ideal of a six-parent,

\[
 q_B(P,r,S)=a_6u(P,r,S),\qquad
 a_6=\frac1{2(1+M_6)}>0.
 \tag{2}
\]

M6 is the complete marked proper-potential row maximum. Neither M6 nor a
numerical a6 is requested or evaluated. No selected-row maximum substitutes
for it. The held law, fair newborn bits and scalar-passive full payload maps
are unchanged; none is newly derived from DET here.

Set h=1 on every order of size at most six and, at size seven, set

\[
 h_7(T_j)=1+\epsilon z_j\quad(1\leq j\leq11),\qquad
 h_7(H)=1\quad([H]\notin\{T_1,\ldots,T_{11}\}).
 \tag{3}
\]

The z variables are record-blind class values shared across all occurrences.
**No h at size eight or above is prescribed.** In particular, silently
resetting h to one above seven is not an admissible continuation argument.
The question is simultaneous harmonicity on every record row, strict positive
amplitudes, and positive width gain on the single complete row in section 7.

## 2. Exhaustive support and fixed variable order

A predecessor tuple records all strict predecessors; bit i denotes vertex i.
Use the lexicographically least tuple over natural labelings as canonical
key. The following four-vertex tuples fix the variable order. The full
seven-vertex representative is

\[
 T_j=(0,1,3,\ 7+8q_0,7+8q_1,7+8q_2,7+8q_3)
 \quad\text{for }Q_j=(q_0,q_1,q_2,q_3).
 \tag{4}
\]

| j | Q_j | Intrinsic cap | Width |
|---:|---|---|---:|
| 1 | (0,0,0,0) | A4 | 4 |
| 2 | (0,0,0,1) | C2 disjoint A2 | 3 |
| 3 | (0,0,0,3) | (A2 ordinal-sum A1) disjoint A1 | 3 |
| 4 | (0,0,1,1) | (A1 ordinal-sum A2) disjoint A1 | 3 |
| 5 | (0,0,1,2) | C2 disjoint C2 | 2 |
| 6 | (0,0,1,3) | 0<2, 0<3, 1<3 (N) | 2 |
| 7 | (0,0,1,5) | C3 disjoint A1 | 2 |
| 8 | (0,0,3,3) | A2 ordinal-sum A2 | 2 |
| 9 | (0,1,1,1) | A1 ordinal-sum A3 | 3 |
| 10 | (0,1,1,3) | A1 ordinal-sum (C2 disjoint A1) | 2 |
| 11 | (0,1,3,3) | C2 ordinal-sum A2 | 2 |

Here width means maximum antichain size, unchanged by the lower C3 stem.
Q1 has width four; Q2,Q3,Q4,Q9 have an explicit three-antichain and a
comparable pair, hence width three. Each remaining cap has two incomparable
maxima and can be partitioned into two chains, hence width two. In particular
Q3 has width three despite having only two maxima.

**Exhaustion proof.** With four maxima there is just A4. With three maxima
the only nonmaximal element lies below exactly one, two or three maxima,
giving Q2,Q4,Q9. With two maxima the two remaining elements are either
comparable or incomparable. In the comparable case the upper nonmaximal
element lies below both maxima (Q11), or one; in the latter case the lower
element either also lies below the other maximum (Q10), or not (Q7).
In the incomparable case each nonmaximal element has a nonempty subset of
the two maxima above it. Up to permutations of each pair, the possibilities
are identical singleton subsets (Q3), distinct singletons (Q5), a singleton
and the pair (Q6), or two pairs (Q8). This gives 1+3+3+4=11 classes.
Their stated incidence patterns distinguish them. Sorting eligible minimal
vertices gives the displayed lexicographically least natural tuples.

The original RI-82 variables T1,T2,T3 are respectively the present
T9,T11,T10. This is a strict support enlargement, not a silent reordering
of the prior certificate or reuse of its three-variable matrix.

## 3. Complete parent closure and individual transition inventory

The five affected parents are P_i=C3 ordinal-sum R_i, in this fixed order:

| i | Three-cap R_i | Six-parent P_i | Complete individual ideal masks |
|---:|---|---|---|
| 1 | (0,0,0), A3 | (0,1,3,7,7,7) | 0,1,3,7,15,23,31,39,47,55,63 |
| 2 | (0,0,1), C2 disjoint A1 | (0,1,3,7,7,15) | 0,1,3,7,15,23,31,47,63 |
| 3 | (0,0,3), A2 ordinal-sum A1 | (0,1,3,7,7,31) | 0,1,3,7,15,23,31,63 |
| 4 | (0,1,1), A1 ordinal-sum A2 | (0,1,3,7,15,15) | 0,1,3,7,15,31,47,63 |
| 5 | (0,1,3), C3 | (0,1,3,7,15,31) | 0,1,3,7,15,31,63 |

Delete every maximal cap vertex in each supported child. In the next table
the deleted labels are **local cap labels 0..3**; full labels are three larger.
Every slash-separated label is a separate deletion role.

| Child | Deleted cap vertex -> parent |
|---|---|
| T1 | 0/1/2/3 -> P1 |
| T2 | 1/2 -> P2; 3 -> P1 |
| T3 | 2 -> P3; 3 -> P1 |
| T4 | 1 -> P4; 2/3 -> P2 |
| T5 | 2/3 -> P2 |
| T6 | 2 -> P3; 3 -> P2 |
| T7 | 1 -> P5; 3 -> P2 |
| T8 | 2/3 -> P3 |
| T9 | 1/2/3 -> P4 |
| T10 | 2 -> P5; 3 -> P4 |
| T11 | 2/3 -> P5 |

These are 27 deletion roles and exactly five parent classes. Any parent of
a supported birth is obtained by deleting its newborn, which an isomorphism
must send to a maximum of the supported child. Thus no other six-parent
can have a nonzero perturbation coefficient.

For a listed parent, a supported precursor contains the entire C3 stem and
a proper ideal of its three-cap. The three stem vertices form the forced
initial three-element chain in every supported child. A maximal newborn
cannot occupy any of those positions. Conversely every proper cap ideal
produces a four-cap with at least two maxima. A full birth has a unique
maximum and is excluded. This proves both directions of the forward list:

| Parent | Individual supported ideal -> child |
|---|---|
| P1 | 7 -> T1; 15/23/39 -> T2; 31/47/55 -> T3 |
| P2 | 7 -> T2; 15 -> T4; 23 -> T5; 31 -> T6; 47 -> T7 |
| P3 | 7 -> T3; 15/23 -> T6; 31 -> T8 |
| P4 | 7 -> T4; 15 -> T9; 31/47 -> T10 |
| P5 | 7 -> T7; 15 -> T10; 31 -> T11 |

The unsupported ideals of **each** parent are exactly 0,1,3,63. These have
zero correction, not zero baseline probability. The 43 individual ideals
include 23 supported slots and 20 unsupported slots. Backward deletion
counts are not forward multiplicities; no automorphism division or merging
of same-child ideal occurrences is allowed.

For each parent and all r=0,...,63, subtract baseline normalization from
the complete harmonic equation. Every supported birth is proper, so (2)
and nonzero epsilon give exactly

\[
 \sum_{S:[P_i+S]=T_j}u(P_i,r,S)z_j=0,
 \tag{5}
\]

with the sum including every individual supported S and its j. The same
positive global a6 cancels in every equation. No full-birth complement,
numerical q6/q7 or new global six/seven-order inventory is needed.

## 4. Held factor closure, transport and justified record reduction

For every supported proper S define U=Max(P) minus S. The inherited
[RI-38 deletion identity](../native_joint_growth_extension_criterion_v1/CRITERION.md)
gives

\[
 u(P,r,S)=\prod_{\varnothing\ne B\subseteq U}
 q^{actual}_{P\setminus B,\,r|_{P\setminus B}}(S)
 ^{(-1)^{|B|+1}}.
 \tag{6}
\]

Each factor is evaluated on a smaller mathematical input, not by deleting
an actual committed record. Transport the order, precursor and record
together under restriction: list surviving vertices in increasing old label
order and assign their bits consecutively. If any canonical relabeling is
then used, transport all three by that same map. For a proper factor erase
only record bits outside its induced precursor by precursor locality; a full
factor must initially retain the entire induced record. Apply further record
projections only using the lemmas below, recording the raw and reduced forms.

Deleting nonempty subsets of cap maxima leaves zero, one or two cap vertices.
The only possible factor orders, including full-precursor factors, are

\[
 C_3=(0,1,3),\quad C_4=(0,1,3,7),\quad
 C_5=(0,1,3,7,15),\quad H_5=C_3\oplus A_2=(0,1,3,7,7).
 \tag{7}
\]

All queries have size at most five. **The exact extra held classes beyond
RI-82 are C3 and H5.** No other held class is needed for these coefficients.

### Unique-top and twin-top lemmas

For C4 and C5, every proper ideal excludes the unique top. Proper locality
therefore removes its record from every proper probability; full normalization
removes it from the full complement as well. Thus complete C4 rows ignore
bit3, and complete C5 rows ignore bit4. This does **not** remove C5 bit3.

For H5, proper ideals 0,1,3,7 directly ignore both top marks. The remaining
proper ideals are 15 and23, each retaining one top. Use an inherited diamond
based at K=C4, with the two precursors C3 and K. The first intermediate
order is H5; the other is C5. For arbitrary old/newborn marks, its scalar
coefficient identity is

\[
 q_{C_4}(7)\,q_{H_5}(15)
 =q_{C_4}(15)\,q_{C_5}(7).
 \tag{8}
\]

All three other factors ignore cap marks: the C4 factors by unique-top
invariance, and q_C5(7) by proper locality. Strict positivity permits
division. Thus the H5 probability at15 ignores both top marks; swapping
the two tops transports records and gives the same conclusion at23.
Its full complement therefore ignores both top marks too. This is an
inherited full-record-cube identity, not a numerical equality at top-zero
samples or an assumption that all maximal records are irrelevant.

### Parameter definitions and frozen held-row queries

Let xi=0,...,7 be the complete C3 marking and eta=xi+8 sigma, sigma in
{0,1}. Define positive actual held quantities as follows; any omitted top
bits in evaluation representatives are zero:

\[
\begin{aligned}
 a_\xi&=q_{C_3,\xi}(7),&
 b_\xi&=q_{C_4,\xi}(7),&c_\xi&=q_{C_4,\xi}(15),\\
 d_\xi&=q_{C_5,\xi}(7),&
 e_\eta&=q_{C_5,\eta}(15),&f_\eta&=q_{C_5,\eta}(31),\\
 g_\xi&=q_{H_5,\xi}(7),&
 h_\xi&=q_{H_5,\xi}(15)=q_{H_5,\xi}(23)
          =c_\xi d_\xi/b_\xi,&
 j_\xi&=q_{H_5,\xi}(31).
\end{aligned}
 \tag{9}
\]

Here a_xi is a size-three held probability, **not the global a6**; h_xi
is a held probability, not the perturbation h7. The actual H5 slots must be
retained and compared to (8), not replaced by an unverified derived value.
Proper locality gives q_C5,eta(7)=d_xi for both sigma. No assertion reduces
e_eta or f_eta to xi, to bit0, or to a single representative record.

| Held order | Complete rows queried | Ideals per row | Probability slots |
|---|---:|---:|---:|
| C3 | records 0..7 (8) | 4 | 32 |
| C4 | records 0..7, unique top zero (8) | 5 | 40 |
| C5 | records 0..15, unique top zero (16) | 6 | 96 |
| H5 | records 0..7, both tops zero (8) | 7 | 56 |
| Total | 40 | | 224 |

Every held row includes all its individual ideals and its positive full
complement. These are source-query counts, not counts of independent numbers.
C3 conservatively retains all eight markings; minimal record compression is
not a goal. The initial 64-mark cube remains the required expanded domain.

## 5. Complete symbolic coefficient matrix

For each supported slot, (6) yields the following table. Parameters without
an explicit subscript use xi=r&7; e,f use eta=r&15 where applicable.

| Parent | Individual ideal masks | Potential per individual slot |
|---|---|---|
| P1 | 7 | a g^3 / b^3 |
| P1 | 15,23,39 | h^2 / c |
| P1 | 31,47,55 | j |
| P2 | 7 | d g / b |
| P2 | 15 | e h / c |
| P2 | 23 | h |
| P2 | 31 | j |
| P2 | 47 | f |
| P3 | 7 | g |
| P3 | 15,23 | h |
| P3 | 31 | j |
| P4 | 7 | d^2 / b |
| P4 | 15 | e^2 / c |
| P4 | 31,47 | f |
| P5 | 7 | d |
| P5 | 15 | e |
| P5 | 31 | f |

For example, P1 at7 omits all three cap maxima: its three singleton deletions
give g^3, its three double deletions give b^3 in the denominator, and its
triple deletion gives a. At a one-top ideal its two singleton deletions give
h^2 and its double deletion gives c in the denominator. In P2 at15, deleting
the isolated maximum gives C5 at15 (e); deleting the chain tip gives H5 at15
(h); deleting both gives C4 full (c). These checks illustrate why all deleted
subsets and transported records must be retained, even when factors coincide.

Thus the full harmonic system is equivalent to Mz=0, with these rows:

\[
\begin{aligned}
 P_1:\;&(a g^3/b^3)z_1+3(h^2/c)z_2+3jz_3=0,\\
 P_2:\;&(dg/b)z_2+(eh/c)z_4+hz_5+jz_6+fz_7=0,\\
 P_3:\;&gz_3+2hz_6+jz_8=0,\\
 P_4:\;&(d^2/b)z_4+(e^2/c)z_9+2fz_{10}=0,\\
 P_5:\;&dz_7+ez_{10}+fz_{11}=0.
\end{aligned}
 \tag{10}
\]

P1 and P3 use xi=0..7. P2,P4,P5 use eta=0..15 with xi=eta&7.
Order compact rows by parent index, then increasing xi or eta, giving a
**64 by 11** matrix. The record at vertex3 is retained for the latter three
parents; it is their first cap vertex, not necessarily the only physically
read record. Coefficients may still depend on all three stem bits.

For each parent expand r=0..63 in increasing order. P1/P3 use r&7, so each
compact row represents eight full markings. The other parents use r&15, so
each represents four. Equations (6), (8) and locality prove these equalities
for the complete cube. A later verifier must reconcile every expanded row
and every factor, rather than use compact-row agreement as its sole evidence.
The representative expanded row for each compact row is the same parent
with r=xi or r=eta respectively (all omitted bits zero). Retain this explicit
row-ID mapping, including when lifting any compact dual certificate to the
320-row matrix; the other expanded records must still be checked.

| Frozen audit domain | Count |
|---|---:|
| Support classes / maximal-deletion roles | 11 / 27 |
| Affected parent classes / complete marked rows | 5 / 320 |
| Individual ideals over parent representatives | 43 |
| Expanded labeled ideal occurrences | 2752 |
| Supported occurrences | 1472 |
| Zero-correction occurrences | 1280 |
| Of these: full births / strict-stem-prefix births | 320 / 960 |
| Held complete rows / probability slots | 40 / 224 |
| Compact harmonic rows / variables | 64 / 11 |
| Raw deletion factors over all supported expanded slots | 2752 |

The last number is independent of the ideal-occurrence count despite being
equal to it. Per complete record, the five parents contribute respectively
19,9,4,8,3 deletion factors, since a slot omitting k maxima has 2^k-1 factors.
All factors are counted before cancellations or reuse; their total is
(19+9+4+8+3)*64=2752. No unsupported coefficient requires a q6 lookup.

## 6. Frozen exact finite decision, including a width-only obstruction

The rational matrix is not evaluated in this design. Once the actual held
rows are separately authorized and checked, use deterministic exact rational
row reduction: scan columns left-to-right, choose the first available
nonzero pivot row, normalize the pivot, and eliminate that column in every
other row. No approximate tolerance, optimization, fitting, support sweep
or adaptive record selection is allowed.

Retain rank, pivot columns and the complete reduced row-echelon form. Build
the standard null basis in increasing free-column order by setting that free
coordinate to one, all other free coordinates to zero, and solving pivot
coordinates. This fixes the decision without choosing a favorable row:

1. If some basis vector has nonzero first coordinate, choose the first such
   vector and divide by that coordinate. The resulting exact rational vector
   obeys Mz=0 and z1=1. Verify every compact and expanded residual separately.
2. Otherwise the first coordinate vanishes on the entire kernel. Compute a
   rational row-span certificate y by solving M^T y=e1 with the same pivot
   convention and all free variables zero. Retain and check all eleven
   identities y^T M=e1^T. This proves z1=0 for every harmonic vector.

The dual coordinates y are unrestricted signed rationals, not nonnegative
optimization multipliers. Lift them only through the explicit representative
row IDs above; do not divide by expanded-record multiplicities.

The alternatives are exhaustive by finite-dimensional linear algebra over
the rationals: the annihilator of ker(M) is the row space of M. They are
also the exact real-feasibility alternatives, since rational elimination
describes the same homogeneous kernel over the reals. An implementation
error, bad dependency or resource stop is neither alternative.

If rank(M)=11, the whole supported perturbation kernel is zero. If rank<11
but alternative 2 holds, **only the named width target is rejected**;
nonzero harmonic directions may exist with zero gain on this row. Report
these dispositions separately. Merely finding a nonzero null vector does
not meet the success condition.

## 7. Strict positivity and the complete-row width functional

Freeze the target to P*=P1=C3 ordinal-sum A3, with all six records zero.
Let w be intrinsic child width. Its complete conditional expectation sums
**all eleven ideals**, supported and unsupported, and both fair newborn
bits. Unsupported terms have zero difference, not zero probability. The
two fair factors sum to one. Define the scale-free difference functional

\[
 \mathcal L(z)=4(a_0g_0^3/b_0^3)z_1
       +9(h_0^2/c_0)z_2+9j_0z_3.
 \tag{11}
\]

The coefficients nine are three separate ideals times width three. Subtract
three times the P1 zero-record harmonic row in (10) to obtain, on ker(M),

\[
 \mathcal L(z)=(a_0g_0^3/b_0^3)z_1.
 \tag{12}
\]

Its multiplier is strictly positive. Therefore a harmonic perturbation
with positive gain exists exactly when the first decision branch gives
z1=1 (orientation and scale can always be absorbed into z and epsilon).
This equivalence rules out the whole fixed-row target under the dual
certificate, not just the canonical basis vector tested first.

For a feasible z define Zmax=max_j |z_j|, a finite maximum over eleven
coordinates, not a baseline normalization maximum. A deterministic interior
amplitude is

\[
 \epsilon_* =\frac1{2(1+Z_{\max})}>0.
 \tag{13}
\]

Every supported value 1+epsilon_* z_j is strictly greater than one half.
The exact full positive interval for this orientation is

\[
 0<\epsilon<\epsilon_{\max},\qquad
 \epsilon_{\max}=\min_{j:z_j<0}(-1/z_j).
 \tag{14}
\]

The negative set is nonempty: z1=1 and all three nonzero coefficients of
the P1 reference row are positive, so z2 or z3 must be negative. Verify
strictness at every supported coordinate, including those not reached by
P*. Zero amplitude and any zero-h endpoint are excluded.

The actual, unconditional-within-this-parent-row width difference is

\[
 \mathbb E_h[w(\text{child})\mid P_*,0]
 -\mathbb E_B[w(\text{child})\mid P_*,0]
 =\epsilon_* a_6\mathcal L(z)
 =\epsilon_* a_6a_0g_0^3/b_0^3>0.
 \tag{15}
\]

No conditioning on proper birth, support membership or a chosen newborn
mark is used. An absolute numerical baseline expectation or numerical a6
is unnecessary. This is a one-birth width statement, not persistence,
typical geometry, dimension, a manifold or a physical observable claim.

## 8. Finite-prefix admission and distinct all-size questions

On a passing branch define only the changed six-parent rows by
q_h(P,r,S)=q_B(P,r,S)h7(P+S); leave every smaller-parent row unchanged.
For the five affected parents, the complete equations give normalization.
For every other parent, maximal-deletion closure gives h7=1 for every
child. Strict positivity follows from (13); full probabilities are unchanged.

The multiplier is unmarked and class-invariant, so precursor-record locality
and marked-parent equivariance survive. For a diamond based at a five-parent,
both baseline routes acquire the same h7 of the common unmarked terminal.
Thus the full scalar-passive D/4 maps agree for every inherited record,
both newborn marks, every equal-precursor pair and every relabeling. Earlier
diamonds are unchanged. This is a complete admissible prefix through seven
births, not merely a collection of normalized selected rows.

[RI-38](../native_joint_growth_extension_criterion_v1/CRITERION.md) then
permits some strictly positive compatible all-size continuation preserving
this seed. It does not guarantee an all-size record-blind h relative to the
original B, a continuation with persistent width improvement, or any chosen
geometric regime. No continuation is implemented or selected here.

The hypotheses remain those of the conditional scalar-passive fair-record
family, not a unique derivation from DET. No metric, Minkowski coordinates,
Johnston kernel, Rideout-Sorkin parameter, supplied mesh or physical amplitudes
are inputs to this cap calculation. This does not turn the passive quantum
payload into informative dynamics or prove a quantum-to-Lorentzian map.
Mass, gravity, metric-as-record promotion, retired kappa-gravity and empirical
correspondence are not conclusions; Option B and Status M are unchanged.

## 9. Later implementation contract — not execution authority

Before a later checker is implemented or any coefficients are calculated,
the coordinator must accept this source-stable domain. The eventual source,
dependency closure, strict schema, exact command arrays, exclusive evidence
destinations, supervision and resource limits require a separate reviewed
freeze and execution authorization. This note creates none of those artifacts.
No inherited checker/helper import is permitted by the present assignment.

The proposed held-row API is the actual RI-74 rebuild_prefix()/prefix_row()
closure, not RI-63 row() substituted for q5. Access any live helper namespace
through the unwrapped cached function, as in the accepted RI-84 implementation.
The fixed accepted dependencies to pin before any such later loading are:

| Input under docs/track_b | SHA-256 |
|---|---|
| native_growth_plancherel_graft_v1/check.py | edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c |
| native_growth_expected_defect_completion_v1/check.py | 39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b |
| native_growth_expected_defect_completion_v1/CERTIFICATE.json | f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b |
| native_growth_height_normalization_v1/CERTIFICATE.json | 3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969 |

The accepted actual probability manifest is
`7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378`;
the inherited problem identity is
`dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c`.
Its 69 canonical stages and 15 inherited controls remain distinct from any
new controls. Any authorized replay of that unchanged prefix's terminal-six
catalogue is inherited-prefix validation, not permission for a new global
size-six/seven inventory or a q6/q7 probability table.

A future exact certificate must retain, and an independent consumer must
rederive, at least the following:

1. All source identities, ordered class representatives, widths, 27 deletion
   roles, five complete ideal lists and every forward child membership.
2. All 40 held normalized positive rows /224 slots; all parameter extractions;
   both H5 one-top slots and the exact diamond identity (8) for every xi.
3. Every one of the 320 expanded rows and 2752 ideal occurrences, with raw
   induced order/ideal/record transports for all 2752 deletion factors,
   their signs and actual held values, including repeated identical factors.
4. All 64 compact rows, full expanded-to-compact correspondence and the
   exact rational RREF/rank/null basis, recomputed rather than trusted.
5. Either the canonical z with z1=1, all residuals, the exact interval and
   interior amplitude, every positive h value and complete-row width gain;
   or the exact y row-span witness and separate rank/nullity disposition.

Enumerating natural relabelings of these specified objects is a prospective
verification of class keys and transport, not a global family search. Every
parent marking is retained, and the mathematical equivariance argument
extends representative-row validity to isomorphic parents. A future source
must freeze its explicit relabeling audit domain before execution.

Intended-reason refusals must catch changed support or variable order;
missing maxima/ideals/records; confusion of backward and forward counts;
merging repeated ideal slots; corrupt widths (especially Q3); improper
full-birth inclusion; q6/q7 or global-scale requests; unproved bit0-only or
first-cap-bit erasure; wrong deletion exponents/record transport; replacing
actual q5; dropping full complements; corrupt RREF/rank/null or dual evidence;
calling a nonzero width-blind kernel a success; zero/negative h; an incorrect
width sign or proper-birth-conditioned target; and noncanonical rationals,
boolean indices, duplicate/extra JSON fields or mismatched source pins.
Integer type/domain validation must precede cached lookup. These controls
are specified, not implemented or claimed to have passed.

An eventual checker must validate exact rational identities under normal
and optimized Python modes, with saved output/receipts and independently
checked full certificate arithmetic. The exact command and finite resource
envelope belong to its future coordinator-reviewed execution packet, not an
implicit permission in this design. Preserve any failed attempt and stop
for review; do not relax limits, trim records, change the target or retry
against altered inputs. Either mathematical outcome stops this fixed
candidate. No next support, later departure, optimizer or continuation search
is authorized by a success or obstruction certificate.

## 10. Source-only status and handoff

The complete family, closure, symbolic matrix and exact width decision are
specified. **Actual rank, target feasibility and amplitude values are open.**
The derivations are analytic and hand combinatorial work; no enumeration
script, inherited checker/helper, coefficient calculation or solver has run
for RI-85. There is no proof-assistant claim.

Independent structural and locality reviewers separately derived the support
and transport reduction before drafting. Three complete independent reviews
then passed: structural/width, record-locality/continuation, and adversarial
exact-decision/implementation-domain review. All read the complete source and
checked its equations, multiplicities, record projections and claim limits.
The reviewed mathematical source was 577 lines /27,014 bytes, SHA-256
`5e72f56df587b7a9b669c5f819c719aabf74f5d8dfac1aa675c4a056b9872a3f`.
Only this review-status update and the explicit signed-dual/no-multiplicity-
division clarification were added afterward; no equation or domain changed.
The latter clarification was independently endorsed in the review exchange.
Final source/hash/link/hygiene checks and the four actual dependency-pin
comparisons are read-only checks, not coefficient or proof-assistant execution.

The one-file packet is ready for independent coordinator adjudication.
Worker proof review is not coordinator acceptance, implementation authority
or a positive coefficient result. Source identity is returned with the
handoff; all review messages are retained in this task and its review agents.

Only this new DESIGN.md is reserved. Accepted sources and historical evidence
are preserved. RET remains paused; no measurement, clocks, book, roadmap,
ledger, coordinator files or git/index operations are part of this worker's
scope. Coordinator adjudication, publication and any implementation dispatch
are separate obligations. This note does not open a new lettered QR-05 gate.
