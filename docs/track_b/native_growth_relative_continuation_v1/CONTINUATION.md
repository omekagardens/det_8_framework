# RI-89 — first-continuation record-independence criterion

25 September 2026 UTC. **Proof and bounded successor design only.**
The accepted [RI-88 construction](../native_growth_four_vertex_cap_check_v1/RESULT_REVIEW.md)
admits a strictly positive seven-birth prefix. This note asks whether its
record-independent relative history weight survives one specified class of
continuations. It does not ask again whether some admissible continuation
exists: [RI-38](../native_joint_growth_extension_criterion_v1/CRITERION.md)
already answers that question affirmatively.

The result here is an exact necessary-and-sufficient criterion for the
common-level-scale continuation. An existing, unchanged RI-79 contrast
additionally forces the two new scales to coincide if the relative weight
is to remain record-blind. That restriction does **not** yet decide the
common half-scale selector. Its remaining obstruction can be tested on one
explicit parent and two records using only already accepted held data.
No such new coefficient calculation is performed here.

## 1. Fixed seed, two scales and complete domain

Keep the actual strictly positive held rows through parent size five and
the baseline B of [RI-85](../native_growth_four_vertex_cap_v1/DESIGN.md).
At parent size six its proper probabilities are
q6^B(P,r,S)=rho*u6^B(P,r,S), with the unknown common rho=a6>0; full
probabilities are normalized complements. The actual rho is the RI-38
half-scale of the complete marked layer, not a selected-row normalization.

Write h7 for the accepted unmarked multiplier. It is one outside the
eleven classes C3 ordinal-sum Q with four cap vertices and at least two
maxima, and on the supported classes T_j it equals

\[
 h_7(T_j)=1+z_j/4,
 \qquad 3/4\leq h_7(T_j)\leq5/4.
 \tag{1}
\]

The fixed z is the RI-88 canonical vector, not a newly chosen direction.
Set h=1 through six births. The modified seed has

\[
 q^h_6(P,r,S)=q^B_6(P,r,S)h_7(P+S),
 \qquad W_h(P,r)/W_B(P,r)=h_7(P)\quad(|P|=7).
 \tag{2}
\]

Here P+S appends a fresh maximal event with past S. W is the weight of one
natural construction with common fair-bit factors stripped, not an
unlabeled probability. Earlier seed rows are unchanged. Full six-parent
births have unique-maximal children and therefore multiplier one.
For a more general positive RI-88 amplitude the following argument has
the same form, but the present packet fixes the accepted amplitude 1/4.

For every seven-parent P and every complete binary marking r, define the
two RI-38 proper-ideal potentials from their respective complete seeds:

\[
 u^i(P,r,S)=
 \prod_{\varnothing\ne A\subseteq\operatorname{Max}(P)\setminus S}
 q^i(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}},
 \quad i\in\{B,h\},\quad S\subsetneq P.
 \tag{3}
\]

Induced orders, ideals and retained marks are transported together in each
factor. Deletion evaluates a smaller mathematical input; it does not erase
committed records. All factors are positive. Put

\[
 U(P,r)=\sum_{S\subsetneq P}u^B(P,r,S),\qquad
 V(P,r)=\sum_{S\subsetneq P}u^h(P,r,S).
 \tag{4}
\]

Every separate labeled ideal contributes, including repeated isomorphism
classes. Let s=a7^B be the fixed, unknown baseline level-seven scale, and
let t be the new common level-seven scale for the modified seed. Assume

\[
 s,t>0,\qquad 1-sU(P,r)>0,\qquad1-tV(P,r)>0
 \quad\text{for every }P,r.
 \tag{5}
\]

Thus the two proposed extensions are

\[
 q^B_7(P,r,S)=s u^B(P,r,S),\quad
 q^h_7(P,r,S)=t u^h(P,r,S)\quad(S\subsetneq P),
\]
\[
 q^B_7(P,r,P)=1-sU(P,r),\quad
 q^h_7(P,r,P)=1-tV(P,r).
 \tag{6}
\]

The scales are fixed from the laws before a current record is observed;
they cannot vary with P, r, S or the residual payload. Equation (5) is
equivalent to s<1/M_B and t<1/M_h, where M_B=max U and M_h=max V range
over the **complete** finite marked seven-parent layer. These maxima are
definitions and are not evaluated. The actual baseline has
s=1/[2(1+M_B)]; choosing the same RI-38 rule for the modified seed gives
t=1/[2(1+M_h)]. No numerical s, t, rho, M_B or M_h is supplied here.

All claims quantify over every seven-parent, its full 128-record cube,
and every individual ideal, or equivalently all representatives with
complete marked transports. This proof quantifier does not authorize a
new seven-parent catalogue. The five affected six-parents of RI-88 are
not a replacement for this larger logical quantifier.

Retain one committed birth, complete ideal eligibility, strict positivity,
fair independent immutable newborn bits, fixed context/carrier, and the
whole unnormalized scalar-passive maps q(P,r,S)D/2. Neither probability
reads D. These are the conditional model premises, not DET-derived
informative quantum dynamics.

## 2. Proper births: a forced terminal product

Let K=Max(P)\S. It is nonempty for a proper ideal. In the ratio of the two
products (3), only singleton deletions reach a six-parent, where the seed
changed. All deletions of two or more maxima reach unchanged earlier rows.
The singleton exponent is +1. Consequently

\[
 \frac{u^h(P,r,S)}{u^B(P,r,S)}=J(P,S),\qquad
 J(P,S)=\prod_{x\in K}h_7((P\setminus\{x\})+S).
 \tag{7}
\]

S remains an ideal after every deletion. If it is full in a singleton-
deleted parent, that child's h7 is one; the factor is not dropped by an
unsupported proper-only assumption. J is independent of all records and
is intrinsic under simultaneous order/ideal isomorphisms.

Now H=P+y_S is the unmarked eight-event terminal of a proper birth. Its
maxima are exactly K union {y}. Moreover H\y=P and
H\x=(P\x)+S for x in K. Equation (2) and the last-birth identity give

\[
 \frac{W_h(H,r\mathbin{\|}b)}{W_B(H,r\mathbin{\|}b)}
 =h_7(P)\frac{t}{s}J(P,S)
 =\frac{t}{s}\prod_{v\in\operatorname{Max}(H)}h_7(H\setminus\{v\}).
 \tag{8}
\]

Both fair-bit factors cancel separately for either b. Every maximal vertex
is a factor, even if several deletions yield isomorphic seven-orders; do
not divide by automorphisms or replace the product by distinct classes.
The final expression is independent of which maximum is the last-born
vertex, of its bit, and of all inherited marks.

Every eight-order with at least two maxima can be obtained this way by
deleting any chosen maximum: at least one other maximum is outside the
newborn's past, so that past is proper. Hence (8) supplies and uniquely
forces the record-blind relative weight on all such terminals, with no
unmatched proper-birth case.

## 3. Full births: the exact missing condition

An eight-order H with a unique maximum y is exactly P plus a full birth;
every element lies below y in a finite poset with a unique maximum.
Its deletion parent P=H\y is unique. Its relative weight is

\[
 h_7(P)\,k_P(r),\qquad
 k_P(r)=\frac{1-tV(P,r)}{1-sU(P,r)}.
 \tag{9}
\]

The denominator and numerator are strictly positive by (5). The newborn
bit is irrelevant, but the full ideal is permitted to read every old
record. There is therefore no locality rule that makes k_P record-blind.
Unique-maximal and multiple-maximal terminals are disjoint; there is no
additional equation matching (8) and (9) on an overlap.

**Theorem.** For fixed seed and scales satisfying (5), a positive function
h8 on unmarked eight-order classes with

\[
 q^h_7(P,r,S)=q^B_7(P,r,S)\frac{h_8(P+S)}{h_7(P)}
 \tag{10}
\]

for every complete marked row exists if and only if, for every P and
every record pair r,r',

\[
 s(U_r-U_{r'})-t(V_r-V_{r'})
       +st(V_rU_{r'}-V_{r'}U_r)=0.
 \tag{11}
\]

Here all four quantities have the same whole parent P. Equation (11) is
obtained by cross-multiplying the two positive ratios (9); no zero-mass
division or averaging over records is allowed.

**Proof.** Necessity follows from (10) on the full ideal, whose unmarked
child is fixed as r varies. Conversely (11) makes k_P(r)=k_P>0 constant.
Define h8 by (8) on multiple-maximal terminals and by h7(P)k_P on unique-
maximal terminals. These exhaust all terminals and satisfy (10) on every
transition. Marked equivariance of U and V implies that isomorphic parents
have the same constant k_P, so the definition is unmarked and intrinsic.
Normalization of q7^h then yields the full harmonic identity

\[
 \sum_{S\text{ ideal }P}q^B_7(P,r,S)h_8(P+S)=h_7(P).
 \tag{12}
\]

All h8 are finite and positive. They are unique, because every terminal
has a maximal-deletion birth and all its transition probabilities are
positive. This proves the theorem. It is a through-eight-birth result,
not a theorem supplying h at all later sizes.

### Affine form, including constant rows

Equivalently, for each P there must be a constant k_P>0 with

\[
 1-tV_r=k_P(1-sU_r)\quad\text{for all }r.
 \tag{13}
\]

If U_r is constant on its complete cube, V_r must also be constant;
then any scales already satisfying (5) meet this parent's condition.
If U varies, its values and V must lie on one affine line

\[
 V_r=\alpha_P U_r+\beta_P,\qquad
 \alpha_P>0,\qquad\alpha_P+s\beta_P=s/t.
 \tag{14}
\]

The slope and intercept are uniquely determined by any two distinct U
values, and must fit all remaining records. Indeed
alpha_P=s*k_P/t and beta_P=(1-k_P)/t. Conversely (14) gives
k_P=t*alpha_P/s>0 and (13). A collinearity test alone is insufficient:
the positive slope and shared-scale relation are essential. Nor is one
record pair sufficient for the universal condition.

For the particular pair of half-scale selectors, (11) is equivalent to

\[
 2(1+M_h)\Delta U-2(1+M_B)\Delta V
       +V_rU_{r'}-V_{r'}U_r=0,
 \tag{15}
\]

where Delta denotes r minus r'. For varying U, (14) becomes
2(1+M_B)alpha_P+beta_P=2(1+M_h). This is symbolic: equality of the two
maxima is not assumed, and their definitions are not an execution plan.

## 4. Locality, equivariance and full-map covariance

Each potential factor in (3) reads only marks in S. Strict proper-ideal
locality therefore holds directly, not by cancellation of forbidden reads.
The full complement may read the whole marked parent. A common scale fixed
once per level preserves both this locality and marked equivariance.
The RI-38 argument supplies every new natural-label diamond for each
extension independently; (11) is not needed to make either law valid.

If (11) passes, the ratios (10) telescope through a diamond based at a
six-parent: both paths gain the same h8(terminal), since h=1 on its base
and the intermediate h7 cancels. The entire unnormalized D/4 agrees,
including every inherited record, both newborn bits and equal precursors.
The first birth may use the full six-parent precursor. Each second
precursor in the incomparable-birth diamond is nevertheless proper in
its intermediate parent because it excludes the other newborn. In
particular a full seven-parent probability is not a new diamond's
second-leg variable. Equal precursors still describe two distinct births
and are not removed from this argument.

If (11) fails, the modified common-scale law is still a positive local,
equivariant, covariant RI-38 continuation. What fails is its membership
in [RI-81's record-independent relative-weight subclass](../native_growth_local_mixture_criterion_v1/MIXTURES.md).
Failure does not by itself show a locality violation, an invalid growth
law, or universal nonexistence of a different record-blind continuation.

## 5. An existing untouched contrast forces equal new scales

Use the already accepted [RI-79 contrast](../native_growth_delayed_cutoff_locality_v1/LOCALITY.md),
not a newly computed parent row. Its seven-parent is

\[
 K=(0,1,1,0,15,15,15),\qquad r_0=0,\quad r_1=1.
 \tag{16}
\]

It has two minimal vertices, 0 and 3, neither maximal. Deleting any of
its three maxima preserves both minima. Appending a fresh maximal birth
to a resulting six-parent cannot remove either minimum. Every seven-child
in (7) therefore has at least two minima, whereas every supported h7 class
C3 ordinal-sum Q has exactly one. Thus h7(K)=1, all factors J(K,S)=1,
and

\[
 V(K,r)=U(K,r)\quad\text{for every }r.
 \tag{17}
\]

RI-79 used exactly the present baseline below parent size seven and
proved U(K,1)-U(K,0)<0 uniformly over the permitted unknown rho=a6.
Specifically its symbolic difference is
rho[-3 Delta U6+rho^2 Delta T3], with a strictly positive certified
margin 3 Delta U6-rho_star^2 Delta T3. Its rho_star is a rigorous upper
bound from two held rows, not a substitute for the global scale.

Putting V=U into (11) leaves (s-t)(U_r-U_r')=0. The accepted nonzero
contrast therefore proves the following necessary condition:

\[
 \boxed{t=s.}
 \tag{18}
\]

For the actual two half-scale selectors this means M_h=M_B. If their
maxima differ, this selector is already rejected as record-blind. Their
equality or inequality has not been evaluated or proved here; (18) is
not such a result. Equal scales are necessary, not sufficient.

At equal scales put D(P,r)=V(P,r)-U(P,r). The remaining exact condition is

\[
 \frac{D(P,r)}{1-sU(P,r)}\quad\text{independent of }r,
 \tag{19}
\]

or, for a pair 0,1,

\[
 D_1-D_0-s(D_1U_0-D_0U_1)=0.
 \tag{20}
\]

An isolated nonzero Delta U, Delta V or Delta D does not alone decide
(20). The complement denominators cannot be omitted.

A separate simplification eliminates unproductive witness choices.
If a seven-parent P has a unique maximum x, then every proper ideal is
an ideal of A=P\x and u^i(P,r,S)=q^i_6(A,r|_A,S). Their sum includes
the full A slot and is exactly one for each seed. Thus U=V=1 on P and
there is no record contrast there. This does not remove the full-birth
terminals P+top for **multi**-maximal parents from the required test.

## 6. Smallest data-level successor test, not executed

The smallest possible record-dependence witness uses one parent and two
markings. Freeze the following particularly simple affected parent:

\[
 P_\star=C_3\oplus A_4=(0,1,3,7,7,7,7),\quad r=0,1,
 \tag{21}
\]

with all four top marks zero and only vertex 0 changed. This is a
minimal comparison in number of parent/record pairs, not a claim of the
fewest ideals or globally smallest possible counterexample. A nonzero
(20) here would suffice to reject the selector; zero would not accept it.

Only the already retained C3, C4 and H5=C3 ordinal-sum A2 rows at
records 0 and 1 are needed: six complete held rows /32 probability slots,
plus the accepted multipliers H_j=h7(T_j) for j=1,2,3. No C5 query,
new prefix reconstruction, q6/q7 table or new support catalogue is needed.

For each labeled C3 ideal S in {0,1,3,7}, set

\[
 A_r(S)=q_{C_3,r}(S),\quad B_r(S)=q_{C_4,r}(S),\quad
 G_r(S)=q_{H_5,r}(S).
 \tag{22}
\]

Use RI-85's positive held symbols a_r=A_r(7), b_r=B_r(7), g_r=G_r(7),
c_r=q_C4,r(15), h_r=q_H5,r(15)=q_H5,r(23), and j_r=q_H5,r(31).
The lower-case h_r is a held probability, not H_j or h7. The unique-top
and twin-top invariance lemmas of RI-85 justify ignoring removed cap
marks and using these rows after transport; none is an assumed erasure.

Define the following symbolic expressions in those accepted entries:

\[
 E_r=\sum_{S\in\{0,1,3,7\}}\frac{A_r(S)G_r(S)^3}{B_r(S)^3}
             +3h_r^2/c_r+3j_r,
 \qquad
 K_r=\sum_{S\in\{0,1,3,7\}}\frac{A_r(S)^3G_r(S)^6}{B_r(S)^8}.
 \tag{23}
\]

E_r is the baseline proper-potential sum on P1=C3 ordinal-sum A3.
No new numerical value of either expression is evaluated here. The
maximal-deletion formula gives the following complete proper-slot types
for P_star. Each multiplicity counts individual ideals:

| Precursor type | Count | Baseline potential per slot | J multiplier |
|---|---:|---|---|
| S in {0,1,3,7} inside C3 | 4 | rho^4 A_r(S)^3 G_r(S)^6 / B_r(S)^8 | H1^4 for S=7; otherwise 1 |
| C3 plus one cap vertex | 4 | rho^3 h_r^3/c_r^2 | H2^3 |
| C3 plus two cap vertices | 6 | rho^2 j_r | H3^2 |
| C3 plus three cap vertices | 4 | 1-rho E_r | 1 |

For the first type, the omitted-maxima counts are four; singleton
deletions supply q6=rho*A*G^3/B^3, the six double deletions supply G in
the denominator, the four triple deletions supply B, and the final
deletion supplies A in the denominator. Their product is the table's
rho^4 A^3 G^6/B^8. For one included cap vertex, the corresponding counts
are three, three, one, giving (rho*h^2/c)^3*c/h^3. For two included
vertices they give (rho*j)^2/j. With three included vertices only one
maximum is omitted, giving the unchanged full P1 probability. This also
proves every power and includes all four base ideals, not just S=7.

There are 18 proper ideals and one full ideal. The multiplier column
follows the accepted T1/T2/T3 forward inventory; three included cap
vertices produce a unique-maximal seven-child with h7=1. Consequently

\[
 U_r(\rho)=4-4\rho E_r+6\rho^2j_r
                  +4\rho^3h_r^3/c_r^2+\rho^4K_r,
 \tag{24}
\]

\[
 D_r(\rho)=\rho^4\frac{a_r^3g_r^6}{b_r^8}(H_1^4-1)
       +4\rho^3\frac{h_r^3}{c_r^2}(H_2^3-1)
       +6\rho^2j_r(H_3^2-1),\qquad V_r=U_r+D_r.
 \tag{25}
\]

All top-subset multiplicities remain separate in deriving these sums.
The proper potentials and U,V are independent of the cap marks by the
same held invariances and the P1 full complement. The two selected
markings do not replace all possible stem markings in a passing claim.

After the necessary equality t=s, the prospective obstruction is exactly

\[
 F(\rho,s)=D_1(\rho)-D_0(\rho)
       -s\,[D_1(\rho)U_0(\rho)-D_0(\rho)U_1(\rho)].
 \tag{26}
\]

The permitted unknown scale belongs to the rigorous outer domain

\[
 0<\rho\leq\frac1{2(1+\max(E_0,E_1))},\qquad
 0<s\leq\frac1{2(1+\max(U_0(\rho),U_1(\rho)))}.
 \tag{27}
\]

These selected rows belong to the full baseline tables. Hence their
maxima give upper bounds only; neither bound is substituted for the
actual global half-scale. Under (27) all selected baseline denominators
are positive. The actual equal-scale candidate must additionally satisfy
the complete positivity premises (5); rejecting (26) on the larger
outer domain would in particular reject the actual candidate.

**Concrete recommendation for a separately authorized successor:** ingest
only the pinned RI-88 certificate's six held rows and H1,H2,H3, verify
their exact domains/normalization and inherited provenance, and form the
two rational-coefficient polynomials (24)–(25) and (26) symbolically. Seek
a rigorous nonvanishing certificate for F over (27), without choosing
rho or s, computing M6/M7, rerunning the producer or querying another
parent. Retain individual-slot derivations and positive denominators.
This would be a targeted two-record obstruction test, not a q7 evaluator.

A uniform nonzero sign, if proved, would complete a common-scale
record-blindness rejection: t!=s already fails section 5; t=s would fail
here. If F can vanish within the outer domain, distinguish extraneous
bound-admissible scales from the actual unknown global ones and report
the unresolved condition. If F vanishes identically, this pair is blind,
not proof that the universal criterion passes. Do not automatically add
another parent, record pair, interval search or larger support.

The new polynomial coefficients and their signs are **not calculated**
in this note. RI-79's unchanged contrast decides (18), but the accepted
RI-88 harmonic equations alone do not establish (26)'s nonvanishing.
No conclusion is inferred from decimal magnitudes or the signs of the
individual z coordinates.

## 7. What is established, and what remains outside this result

The frozen result is a theorem about a specified continuation class,
a necessary equality of its scales, and one bounded unresolved test.
Passing (11) would produce the unique positive unmarked h8 for that
selector, not a nonconstant all-size harmonic function. Failing it would
reject that selector's record-blind relative weights, not all admissible
growth laws, component-scale choices, or other record-blind continuations.
The existing laws remain local even if their relative weight reads records.

Regardless of this criterion, choosing RI-38's explicit half-scale rule
at every later level retains full-birth probability greater than 1/2.
[RI-39](../native_growth_history_height_v1/HISTORY_HEIGHT.md) applies with
the present finite seed cutoff and yields liminf H(P_N)/N >= 1/2 almost
surely. The accepted finite width increase does not repair the rejected
vanishing-height-density target. That warning concerns this normalization,
not every possible continuation or all geometric regimes.

No informative quantum coupling, physical observable correspondence,
Lorentzian structure, mass, gravity, metric-as-record promotion, or unique
DET choice is established. The passive payload is retained in the full
maps rather than discarded, but has not become a growth driver. Option B,
Status M and the RET pause are unchanged.

## 8. Provenance and source-only handoff

The accepted result dependencies are unchanged:

- RI-88 CERTIFICATE.json: 1,828,149 bytes, SHA-256
  `ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b`.
- RI-79 CERTIFICATE.json: 14,652 bytes, SHA-256
  `d06001c27ac1ed12a6ba7c5af7970524be825ce70eac50e8b34ef34603906143`.
- RI-38 CRITERION.md: 22,701 bytes, SHA-256
  `65c779a8e189adf9a6d5033310b9d1d7521b5051bd371a5112ef3273f3273675`.
- RI-81 MIXTURES.md: 21,800 bytes, SHA-256
  `ed0195b466c67dff9084a4a5284d72507185c0177157934347dc28ff31f1ab05`.
- RI-39 HISTORY_HEIGHT.md: 18,756 bytes, SHA-256
  `8834cd8f14b753d46b5edeb0b94c07cf8167a8ed2d479f734d50ea812b46d07c`.

This is the sole reserved repository artifact. No checker, helper, prefix,
solver, probability enumeration or new coefficient arithmetic is run.
Reading retained JSON values and hashing source bytes are not such runs.
No certificate, source-execution admission, next-level law table or
successor executor is created. The coordinator owns acceptance, publication,
git/index and any later numerical admission. Proof review and stable-source
handoff status are recorded in the external RI-89 evidence packet.
