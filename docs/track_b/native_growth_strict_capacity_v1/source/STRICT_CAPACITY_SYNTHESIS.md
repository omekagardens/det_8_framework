# Strict capacity from the accepted height bound

RI155 resolves one of the two actual capacity questions for the unchanged
fixed prefix and removes the extra multiplier from the other. Manual source
reasoning gives

\[
 0<YE<\frac{14256}{370025}<\frac1{25},\qquad Yu_3>\frac14.
 \tag{1}
\]

Consequently the two strict capacities of the accepted sufficient envelope
hold **if and only if**

\[
 v>\frac{12\lambda j_0 Z}{1-Z}.
 \tag{2}
\]

The sign of (2) at the fixed prefix is not established here. This is a
completed partial analytic resolution, not a claim that the envelope passes,
that the weighted margin has a sign, or that H30 is feasible or obstructed.
The first inequality in (1) is new proof for the actual fixed prefix, not
an arbitrary positive-coefficient example or a rephrasing of RI153.

The load-bearing additional premise is RI41's already accepted **all-row
height bound at parent size four**. Its original proof is a finite exact
certificate. We reuse its printed theorem and prove new consequences; we
do not rerun that certificate or claim a first-principles derivation of its
witness. The result is conditional on this fixed accepted finite law, not
every DET-compatible law or a later-layer height bound.

## Accepted objects and notation

The full premise identities and bounded administrative closure are in
SOURCE_IDENTITIES.json and SOURCE_DEPENDENCIES.json. The companion
CAPACITY_STRUCTURE.md proves the event incidence and complete-row bounds;
CAPACITY_COMPARISON.md proves the capacity comparison. These are author
contributions, not independent acceptance.

Let \(e=A(0)=A(1)=A(3)=1/44\) and \(a=A(7)=41/44\) be the unchanged
complete C3 row. In each retained C4 root sector \(i=0,1\), write its
**complete** row as

\[
 (w,p_i,s_i,b_i,c_i)
   =(B_i(0),B_i(1),B_i(3),B_i(7),B_i(15)),\qquad
 w+p_i+s_i+b_i+c_i=1.
 \tag{3}
\]

Here \(s_i\) names the C4 initial-pair probability, not the later size-seven
scale. Every term is strictly positive; \(w\) is record-independent by
strict empty-precursor locality. The accepted contrast is \(b_0>b_1>0\).
No order for \(p_0,p_1\) or \(s_0,s_1\) is assumed.

Retain

\[
 \theta=\frac1{72(1+M_5)}<\frac1{144},\quad
 K_i=\sum_S\frac{B_i(S)^2}{A(S)}+2c_i,\quad j_i=1-\theta K_i,
\]
\[
 T_i=\sum_S\frac{B_i(S)^3}{A(S)^2},\quad
 E_i=\theta^3T_i+3\theta^2c_i+3j_i,\quad
 g=\theta^3c_0,
 \tag{4}
\]

where all four C3 ideals occur in both sums. In this note \(E_i\) are
parent sums; the unindexed envelope coefficient \(E\) below is different.
The singleton correction remains the actual canonical one:

\[
 N_i=\frac{35}{1476}\sigma_i\ge0,\quad
 \ell_i=1-\theta-N_i>0,\quad
 F_i=1+\ell_i^2+N_i^2(1/p_i-1).
 \tag{5}
\]

No branch of \(\sigma_i=[H_i]_+/c_i\) is selected. Define, without
evaluating a maximum,

\[
 R=\frac1{2(1+\max(E_0,E_1))},\qquad
 Z=\min\left\{R,\frac1{2(1+F_0)},\frac1{2(1+F_1)}\right\}.
 \tag{6}
\]

RI147 proves \(0<\rho\le Z<12/95<1/4\). This is the same
actual-containing cap, not a substituted generating scale. Retain

\[
 d(x)=2(3-2x+x^2),\quad Y=1/d(Z),\quad
 u_3=U_{30}(Z)>3/2,\quad Y\le8/41,
\]
\[
 r=\theta^3b_0^3/a^2>0,\quad
 \lambda=1-(b_1/b_0)^3\in(0,1),\quad
 v=V_1-V_0>0,\quad \eta=\epsilon_3/r>0,
\]
\[
 B=\frac{12\lambda j_0Z}{1-Z},\qquad
 E=12Z^2(1+\eta)(j_0+gZ).
 \tag{7}
\]

The analytic \(Y=1/d(Z)\) never replaces numerical certificate \(Y=1/4\).

## Transport the height theorem before bounding the row

RI41 NORMALIZATION.md equations (1) and (6) state that the sum of **all**
height-raising ideal probabilities in every marked four-parent row is below
one half. Proper longest-chain ideals count, as does the genuine full ideal.
This is not merely a bound on full births.

Three C3 diamonds transfer that theorem to (3). The ratio of the C3 full
probability to each proper probability is \(a/e=41\).

- Precursors \((0,7)\) connect C4 empty birth to the long C3 precursor in
  C3 disjoint A1. That latter probability is \(41w\), raises height, and
  shares its row with other positive probabilities. Thus \(w<1/82\).
- Precursors \((1,7)\) connect the C4 singleton to the long C3 ideal in
  the hook of shape \((3,1)\). Its probability is the accepted
  \(L_i=41p_i\), and it raises height. Thus \(p_i<1/82\).
- Precursors \((3,7)\) connect the C4 initial pair to a full C3 arm in
  the two-tip parent \((0,1,3,3)\). There are **two distinct arms** with
  probability \(41s_i\) each when their transported selected records
  agree. Both raise height, and the positive full complement also raises
  height. Thus \(82s_i<1/2\), or \(s_i<1/164\).

Each use transports the whole parent, selected ideal and retained marks;
the arbitrary excluded tip/newborn marks are not fixed as an extra premise.
The companion incidence proof explains how to choose a common permitted
row for the two arm occurrences. Equivariance identifies their probabilities,
not their occurrences in the row sum. C4's own full birth raises height, so
also \(c_i<1/2\). Complete normalization now gives

\[
 b_i>1-\frac1{82}-\frac1{82}-\frac1{164}-\frac12
       =\frac{77}{164}.
 \tag{8}
\]

Nothing in this argument compares the two numerical seed declarations or
selects an actual component coefficient from the historical table.

## The empty coefficient has the same restoration power

The held empty coefficient is not the C3 proper probability \(e\). The
RI145 definition and accepted H5 empty-slot identity give exactly

\[
 \epsilon_3=A_EG_E^3/B_E^3
   =\theta^3 w^3/e^2,\qquad
 \eta=41^2(w/b_0)^3.
 \tag{9}
\]

Both numerator and denominator in \(\eta\) carry \(\theta^3\); it cancels.
Replacing \(\epsilon_3\) with the historical C3 probability would create a
spurious inverse power of \(\theta\). That exploratory idea is excluded.
Using (8) and the strict bound on \(w\),

\[
 0<\eta<41^2(2/77)^3=\frac{13448}{456533}<\frac1{32}.
 \tag{10}
\]

The last comparison is the exact bound arithmetic
\(32\cdot13448=430336<456533\), not an evaluation of an actual probability.

Since \(K_0>2c_0\), \(\theta^2Z<2\), and \(c_0>0\),

\[
 0<j_0+gZ=1-\theta K_0+\theta^3c_0Z
   <1-\theta c_0(2-\theta^2Z)<1.
 \tag{11}
\]

Consequently

\[
 YE<12(12/95)^2(8/41)(33/32)
    =\frac{14256}{370025}<\frac1{25}.
 \tag{12}
\]

The integer comparison is \(25\cdot14256=356400<370025\).
This proves the actual first capacity with strict slack greater than
\(24/25\). It holds for either zero or positive canonical singleton
correction and for every tied or untied selection in (6).

## The second capacity no longer needs its extra multiplier

Because \(0<Z<1/4\), \(d(Z)<6\) and hence \(Y>1/6\).
Together with \(u_3>3/2\), this yields \(Yu_3>1/4\). Equations
(12) and the inherited \(Yu_3<1\) therefore prove

\[
 0<\frac{1-Yu_3}{1-YE}<1.
 \tag{13}
\]

RI153's unresolved maximum is exactly one, not merely bounded by a
convenient substitute. Equivalently, set

\[
 C_0=1-B/v,\qquad C_1=1-(1-Yu_3)B/v-YE.
\]

If \(C_0\ge0\), then \(B/v\le1\) and

\[
 C_1\ge Y(u_3-E)>\frac14-\frac1{25}=\frac{21}{100}.
 \tag{14}
\]

Thus \(C_0>0,C_1>0\) is exactly (2). At \(v=B\), the second
capacity remains strictly positive, but the first is zero and the envelope
still fails: its first budget contains the strictly positive term \(A/\mu\).
For \(v<B\), the first capacity is negative and the envelope likewise
fails. Neither failure determines the sign of the underlying \(W\).

For \(v>B\), both capacities pass, but the separate adequate \(q\)
threshold remains necessary for the retained envelope. No new \(q\)-floor
construction or claim of an adequate value is made in this sitting.

## What the selected cap can and cannot explain

The complete sums also imply \(E_i<3\). Indeed, every
\(B_i(S)/A(S)<44\), so \(T_i<44K_i\), while \(2c_i<K_i\).
Substitution in (4) gives

\[
 E_i<3+\theta K_i[-3+(3/2)\theta+44\theta^2]<3.
 \tag{15}
\]

The last bracket is negative already from \(\theta<1/144\): its two
positive terms sum to less than one. Combining this with the inherited
\(E_i>71/24\) yields \(1/8<R<12/95\). Consequently

\[
 Z<1/8\iff\max(F_0,F_1)>3,\quad
 Z=1/8\iff\max(F_0,F_1)=3,\quad
 Z>1/8\iff\max(F_0,F_1)<3.
 \tag{16}
\]

Only the retained \(F_i\) rows can lower this particular cap below
\(1/8\); this is not a statement about the actual global maximizing
six-parent. CAPACITY_STRUCTURE.md supplies the exact nonnegative \(N_i\)
threshold for these alternatives, including equality and \(N_i=0\),
without selecting an actual canonical branch.

There is also a conditional obstruction with a definite bound. The same
complete sums give

\[
 V_i=j_i+2\theta^2c_i+\theta^3T_i
 <1+\theta K_i[-1+\theta+44\theta^2]<1.
\]

Since \(V_i>j_i>71/72\) and \(v=V_1-V_0>0\),
\(0<v<1/72\). Put \(M_{\rm cap}=\max(E_0,E_1,F_0,F_1)\),
which is not the global \(M_6\). Equation (6) gives exactly
\(Z=1/[2(1+M_{\rm cap})]\) and
\(B=12\lambda j_0/(1+2M_{\rm cap})\). Thus capacity success requires

\[
 \lambda<\frac{1+2M_{\rm cap}}{852}.
 \tag{16a}
\]

In particular, if \(\max(F_0,F_1)\le3\), success requires
\(\lambda<7/852\). If that branch holds and \(\lambda\ge7/852\),
the retained envelope fails its strict capacity, including equality. Neither
the branch nor the actual comparison of \(\lambda\) with this bound is
claimed decided. It is a conditional obstruction, not a counterexample
constructed from independently chosen coefficients.

## Precise remaining correlated comparison

The remaining condition is not positivity of \(v\), which is already
known. It is a quantitative comparison on the same prefix. To expose its
complete dependence, retain the accepted RI147 differences

\[
 d_S=B_0(S)-B_1(S),\quad
 P_S=(B_0(S)+B_1(S))/A(S),\quad
 T_S=(B_0(S)^2+B_0(S)B_1(S)+B_1(S)^2)/A(S)^2,
\]
\[
 \mathcal H_S=P_S+2\theta-2-\theta^2T_S,\quad
 \gamma_1=d_1/d_7,\quad\gamma_3=d_3/d_7,\quad
 \mathcal H=\mathcal H_7+\gamma_1\mathcal H_1+\gamma_3\mathcal H_3.
 \tag{17}
\]

Here \(d_0=0\), \(d_7>0\), but \(d_1,d_3\) and both \(\gamma\)'s
may be signed or zero. Write \(J=b_0^2+b_0b_1+b_1^2>0\) and
\(t=1/Z=2[1+\max(E_0,E_1,F_0,F_1)]\). The exact common-factor
cancellation is

\[
 \frac v\lambda=\frac{\theta b_0^3}{J}\mathcal H.
\]

Hence (2) is exactly

\[
 \boxed{\theta b_0^3(t-1)\mathcal H>12j_0J.}
 \tag{18}
\]

All divisions used here have named positive denominators. No sign of a
gamma, root ordering, or positive-part branch has been selected. The same
actual canonical \(N_i\) must be used inside \(F_i\) and hence \(t\).
Equation (18) is an unevaluated comparison, not a freely tunable parameter
condition. The new rowwise bounds prove (12) and (13), but this manuscript
does not prove a quantitatively adequate lower bound on the signed
contrast \(\mathcal H\). That is the exact unresolved premise. It is
not asserted independent of all fixed-law axioms or impossible to prove.

## Limits and handoff

The actual \(YE\) result and capacity reduction are submitted for fresh
nonauthor review. No actual \(v>B\) result, adequate joint budget,
small-scale membership, \(W\), individual \(C_2/C_3\), or full H30
decision follows yet. No theorem here promotes QM, geometry, gravity,
all-size growth or empirical correspondence.

All other eight connected parents, all five \(D_i\) systems, shared T1
recovery, individual ideal multiplicities, strict endpoints, original
P2/P3 and numerical \(Y=1/4\), and the 31 focused variants, 139 policy
cases, 20 native and 42 audit deeper obligations remain unchanged. RET
stays paused; measurement remains separate.

The withdrawn historical seed-order comparison provides no premise. RI153
clarification N01 is retained: only its box floor and maximum correlated
floor were proved to dominate the older floor, not each ratio anchor.
The RI155 uniform-margin clarification is preserved as an administrative
record; the proof above does not need its optional coefficient bound.

This work reads literal accepted source text and performs manual algebra.
Administrative checks authenticate saved bytes and declared references;
they are not mathematical proof or continuing custody. No scientific body
decode, selected-probability evaluation, source/helper import, compilation,
AST, probe or execution, numerical/symbolic engine, global enumeration,
runtime/controller/card/admission, repository/index/Git operation, or
sealed predecessor mutation is part of this packet. It stops at this
result and the precise comparison (18); it assigns no successor.
