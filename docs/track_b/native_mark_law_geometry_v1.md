# Mark-law choice and unmarked finite geometry

RI1491 consolidates the independently reviewed QR-LD006 result. The original model uses fair newborn marks. Replacing that prescription by a declared constant bias, while keeping its structural rule fixed, changes two of the four tested unmarked height tails. Consistency alone therefore does not select a unique height law within this changed family.

This note includes the complete structural prefix and the finite derivation. Part A states the original fair model; Part B explicitly replaces its fair-mark prescription for this comparison. Only parent sizes zero through three and four births are used. The [native theorem package](native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model) supplies the admitted structural identities; its later coefficient certificates are not needed here. The [precursor-local payload note](native_precursor_payloads_v1.md) concerns a separate optional coupling and is not used by this passive-payload calculation.

The exact table first derived in CE-RF002 is attributed and independently reconstructed below. That calculation's proposed backward-method advantage remains closed; no performance, novelty, physical prediction or law-selection principle transfers.

## A. Original model and the fixed four-birth structural prefix

A state consists of a finite order \(P\), immutable binary marks \(r:P\to\{0,1\}\), and an arbitrary complex positive-semidefinite payload \(\mathfrak D\) on a fixed carrier. An ideal \(S\subseteq P\) is a downward-closed subset, including the empty and full ideals. A birth appends one maximal vertex with strict past exactly \(S\); write the resulting order \(P+S\). The newborn mark \(b\) is independently fair. The branch map is

\[
 \mathcal B^{P,r}_{S,b}(\mathfrak D)
       =\frac{q(P,r,S)}2\,\mathfrak D .
 \tag{1}
\]

The admitted model requires:

- Every ideal is eligible, \(q(P,r,S)>0\), and the complete ideal sum is one.
- A proper-slot probability may read the whole unmarked order \(P\), but only the marks in \(S\). A full slot may read all old marks.
- Relabeling transports order, ideal and marks together; probabilities are equivariant.
- Two incomparable births commute as complete unnormalized marked maps. Both newborn bits, equal-precursor pairs and all inherited marks are included.
- There is one committed birth at a step. This bookkeeping step is not a physical clock and is not a claim that every present relational activity creates a record.

For two ideals \(S,T\) of a base \(C\), with the new vertices excluded from the second precursors, the diamond identity is

\[
 q(C,r,S)q(C+S,r+b,T)
   =q(C,r,T)q(C+T,r+c,S).
 \tag{2}
\]

Both sides multiply the same transported terminal payload by \(1/4\). Equation (2) is not merely agreement of normalized probabilities or diagonal payloads.

For a proper ideal in a nonempty parent, let \(M=\operatorname{Max}(P)\setminus S\). Its fixed maximal-deletion potential is

\[
 u(P,r,S)=
 \prod_{\varnothing\ne A\subseteq M}
 q(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}} .
 \tag{3}
\]

These are evaluations of smaller mathematical inputs, not erasure of committed history. Full smaller-parent slots retain their full induced marks.

The admitted ratio-component theorem says that (3) satisfies all inherited ratio equations and that every positive solution at the next layer has the form
\(q(P,r,S)=\alpha_{\mathcal C(P,S,r|S)}u(P,r,S)\) on proper slots. The component key keeps the whole unmarked parent and selected marks. All labeled ideal occurrences contribute separately to row sums. Full slots are normalization complements.

### The fixed instance, not a uniquely selected law

The smaller seed is prescribed:

\[
 a_{\rm seed}=2/3,\quad c_{\rm seed}=1/5,\quad d_{\rm seed}=1/4,
 \quad f_{\rm seed}(0)=1/6,\quad f_{\rm seed}(1)=1/3,
\]
\[
 g_{\rm seed}=1/10,\quad k_{\rm seed}=11/20,\quad
 h_{\rm seed}(0)=19/30,\quad h_{\rm seed}(1)=7/15,\quad e=1/44 .
\]

The singleton, two-chain and two-antichain ideal rows are
\((a_{\rm seed},1-a_{\rm seed})\),
\((c_{\rm seed},f_{\rm seed}(i),h_{\rm seed}(i))\), and
\((d_{\rm seed},g_{\rm seed},g_{\rm seed},k_{\rm seed})\).
The parent-three proper rows are:

| Parent | Proper ideal probabilities |
| --- | --- |
| Three-antichain | Empty \(e\); each singleton \(eg_{\rm seed}/d_{\rm seed}\); each pair \(ek_{\rm seed}/d_{\rm seed}\) |
| Edge \(u<v\), isolate \(w\) | Empty and \(w\): \(e\); \(u\): \(ef_{\rm seed}(r_u)/c_{\rm seed}\); \(uv\): \(eh_{\rm seed}(r_u)/c_{\rm seed}\); \(uw\): \(ek_{\rm seed}/g_{\rm seed}\) |
| Fork | Empty and root: \(e\); each root-plus-leaf ideal \(eh_{\rm seed}(i)/f_{\rm seed}(i)\) |
| Join | Empty, each root singleton and root pair: \(e\) |
| Three-chain | Empty, root and initial pair: \(e\) |

Every full slot is the complete complement.

## B. A separately declared constant-bias family

### 1. Declared family and consistency

Retain the printed parent-zero-through-three \(q\), complete ideal support, immutable binary marks and original scalar-passive payload. For \(0<t<1\), declare
\[
 \pi_t(0)=t,\quad \pi_t(1)=1-t,\qquad
 \mathcal B^{P,r;t}_{S,b}(X)=q(P,r,S)\pi_t(b)X.
\]
No optional precursor-local unitary coupling is used here.

Every branch coefficient is positive. Since all ideals remain included,
\[
 \sum_{S,b}q(P,r,S)\pi_t(b)=1.
\]
Thus the complete nonselective payload map remains identity and the row is normalized. Constant newborn probabilities add no dependence on outside marks or labels; the original locality and equivariance of \(q\) are preserved.

For any supported incomparable-birth diamond, including equal precursors and every old/new marking, the two structural products agree by the actual \(q\) identity. Multiplying them by the same positive \(\pi_t(b)\pi_t(c)\) proves equality of the complete unnormalized marked maps. This is stronger than merely matching normalized endpoint probabilities. These checks establish a consistent changed finite family under the retained conditions, not compliance with the original explicit fair-mark postulate when \(t\ne1/2\).

### 2. History-level change of measure

Let \(\gamma\) be a naturally encoded four-birth history, \(z(\gamma)\) its number of zero marks, and \(W(\gamma)\) the product of its actual structural factors. Then
\[
 L_{1/2}(\gamma)=W(\gamma)/16,\qquad
 L_t(\gamma)=W(\gamma)t^{z(\gamma)}(1-t)^{4-z(\gamma)},
\]
so
\[
 \frac{L_t(\gamma)}{L_{1/2}(\gamma)}
 =16t^{z(\gamma)}(1-t)^{4-z(\gamma)}.
\]
Both laws have the same complete support. No factorization of geometry from marks is assumed: \(W\) may read the inherited marks. The change-of-measure factor is constant within a fixed zero-count class, so summing over histories preserves every natural-encoding multiplicity.

Consequently, for the four-birth height \(H\) and zero count \(Z\),
\[
 P_t(H\ge h,Z=z)
 =16t^z(1-t)^{4-z}P_{1/2}(H\ge h,Z=z).
\]
The mark sequence itself is independent Bernoulli under this family because each next bit has the same conditional probability after every parent/ideal choice. Geometry and marks need not be independent. In particular, conditional geometry given \(Z=z\) is unchanged, but its mixture weights change.

### 3. Independent applicability and table check

The accepted Comp-Sci CE-RF002 calculation concerns exactly this original fair passive prefix, four births and all ideal occurrences. Its twenty finite probabilities are reusable at that scope; its backward-method advantage candidate remains closed. No performance or physical validation transfers.

I independently reconstructed the fair generating polynomials from the printed smaller-parent rows. Write \(c=1/5,\ g=1/10,\ k=11/20,\ e=1/44\), with \(f_0=1/6,\ f_1=1/3,\ h_0=19/30,\ h_1=7/15\). Let \(x\) count zero marks. The five size-three shape contributions are
\[
 B_A=(1+x)^3/48,\quad B_E=(1+x)^3/40,\quad
 B_F=(2+x)(1+x)^2/144,
\]
\[
 B_J=11(1+x)^3/240,\qquad
 B_C=(14+19x)(1+x)^2/720.
\]
Here \(A,E,F,J,C\) are antichain, edge plus isolate, fork, join and chain. Their natural-encoding factors are \(1,3,1,1,1\). The structural products are respectively \(1/6,1/15,f_i/3,11/30,h_i/3\), with the edge product counted three times. Summing role-specific mark assignments and the fair three-bit factor \(1/8\) gives these polynomials without extra automorphism multiplicities. Their sum is \((1+x)^3/8\).

The final height-three tail kernels are \(0,21/22,10/11,1\) for \(A,F,J,C\). For \(E\), the non-height-three slots sum to
\[
 e(2+f_i/c+k/g),
\]
so its tail is \(214/264\) for edge-root zero and \(209/264\) for edge-root one. The resulting edge contribution is
\((209+214x)(1+x)^2/10560\).
After factoring \((1+x)^2\), the chain, fork, join and edge terms over denominator \(31680\) are
\[
 (616+836x)+(420+210x)+(1320+1320x)+(627+642x)
 =2983+3008x.
\]
The final fair bit multiplies by \((1+x)/2\).

Height one is automatic. Height exactly one requires the all-antichain path, with structural product
\((2/3)(1/4)(1/44)=1/264\), independent of marks. Height four requires the three-chain full slot \(1-3e=41/44\). Thus
\[
 T_h(x):=\sum_z P_{1/2}(H\ge h,Z=z)x^z
 =\frac{(A_h+B_hx)(1+x)^3}{63360},
\]
with the following independently checked coefficients and entries. Every joint entry is a numerator over \(63360\).

| \(h\) | \((A_h,B_h)\) | \(z=0\) | \(1\) | \(2\) | \(3\) | \(4\) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | \((3960,3960)\) | 3960 | 15840 | 23760 | 15840 | 3960 |
| 2 | \((3945,3945)\) | 3945 | 15780 | 23670 | 15780 | 3945 |
| 3 | \((2983,3008)\) | 2983 | 11957 | 17973 | 12007 | 3008 |
| 4 | \((574,779)\) | 574 | 2501 | 4059 | 2911 | 779 |

The expansion is \(A,3A+B,3A+3B,A+3B,B\), which verifies all twenty entries manually. These are overlapping tail queries, not twenty disjoint outcomes.

### 4. Unmarked tails and direct four-chain check

Summing the reweighted table gives, for interior \(t\),
\[
 P_t(H\ge h)=16(1-t)^4T_h\!\left(\frac{t}{1-t}\right)
 =\frac{A_h(1-t)+B_ht}{3960}.
\]

| Event | Exact probability | Dependence in this family |
| --- | --- | --- |
| \(H\ge1\) | \(1\) | invariant |
| \(H\ge2\) | \(263/264\) | invariant |
| \(H\ge3\) | \((2983+25t)/3960\) | strictly increasing |
| \(H\ge4\) | \(41(14+5t)/3960\) | strictly increasing |

A separate direct check does not rely on table reweighting. Four-chain formation requires a full singleton birth, then the two-chain full slot, then the three-chain full slot. Conditional on the first mark \(i\), the product is
\[
 \frac13 h_i\frac{41}{44},
 \qquad h_0=19/30,\quad h_1=7/15.
\]
The other three marks sum out because these chain-path factors do not depend on them. Averaging the first mark yields
\[
 P_t(H=4)=\frac{41}{132}
 \left(t\frac{19}{30}+(1-t)\frac7{15}\right)
 =\frac{41(14+5t)}{3960},
\]
confirming the transformed table directly.

For two strictly interior instances,
\[
 P_{1/3}(H=4)=1927/11880,\qquad
 P_{2/3}(H=4)=2132/11880.
\]
The exact positive contrast is \(41/2376\). The height-three-tail contrast is \(5/2376\). At \(t=1/2\), the tails recover \(1,263/264,1997/2640,41/240\), preserving the original fair results. The exact-height probabilities, obtained by adjacent tail differences, are positive throughout \(0<t<1\) and sum to one. Polynomial values at \(t=0,1\) are limits only; those parameters lose positive mark support.

### 5. Law choice versus coordinates

Renaming every mark by \(r'=1-r\) transports the whole law:
\[
 t'=1-t,\qquad q'(P,r',S)=q(P,1-r',S).
\]
Height is unchanged under this coordinate operation, so the transported pair \((q',1-t)\) has the same unmarked height law as \((q,t)\). The present comparison holds \(q\) fixed instead. That is different: the printed \(f_0=1/6,f_1=1/3\) and \(h_0=19/30,h_1=7/15\) are not mark-flip symmetric. The interior height contrast therefore demonstrates a changed probability law, not a coordinate artifact.

This result is confined to constant bias, the fixed structural prefix and four births. It classifies neither arbitrary intrinsic kernels, alternative \(q\) seeds nor later horizons.

### 6. Remaining premise and stop

The retained formal constraints do not uniquely fix this finite unmarked height law once the fair-mark prescription is released. A principle selecting \(t\), or justification for retaining fair marks, is still a separate premise. Physical interpretation also requires a justified preparation/record/detector correspondence and calibration. A finite order-height probability is not a metric, physical gravity result, calibrated GWOSC forward map or observation.

The original fair model and the closed QR-LD005 local-access result remain intact at their scopes. No optional payload coupling, physical selection, Boundary influence or new implementation follows.
