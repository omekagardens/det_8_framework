# Canonical cap and marked contrast bounds

RI157 proves which rows control the retained cap at the unchanged actual
prefix. The two canonical singleton rows are strictly below the other
retained parent sums:

\[
 F_i<\frac{35743}{12100}<\frac{71}{24}<E_0,E_1.
 \tag{1}
\]

Thus \(M_{\rm cap}=\max(E_0,E_1)\) and \(Z=R>1/8\). This
settles the actual cap branch left open by RI155; it does not evaluate a
probability table or identify the global six-parent maximum.

The same fixed prefix also satisfies the new bounds

\[
 0<v<\frac{1147}{9092160},\qquad
 p_1>p_0\ \text{or}\ s_1>s_0.
 \tag{2}
\]

Consequently a strict capacity pass \(v>B\) would require both

\[
 \lambda<\frac{1147}{15370080}<\frac1{13000},\qquad
 (p_1-p_0)_++(s_1-s_0)_+>213(b_0-b_1).
 \tag{3}
\]

Neither actual comparison in (3) is decided here. The result is a proved
actual canonical-cap branch, a stronger actual contrast bound and a precise
remaining marked-row comparison. It is not an actual rejection or pass of
the envelope, nor a W/H30 sign. No additional q floor is constructed.

## What is inherited and what is proved here

The accepted RI155 result is \(0<YE<1/25\) and exact equivalence of both
strict capacities to \(v>B\). Equality \(v=B\) fails the first capacity.
RI155 also supplies \(71/24<E_i<3\), \(71/72<j_i<V_i<1\),
\(0<\theta<1/144\), the canonical threshold formula and the complete
signed contrast. These results are not reproved by administrative hashing.

Three earlier uniform results are now load-bearing:

- RI41's accepted parent-four finite witness has all component coefficients
  \(\alpha_c\ge1/8\), every full complement at least
  \(33901019/474368400>1/14\), and every marked row's total
  height-raising probability below \(19/40\).
- RI36's analytic extension construction bounds **each** size-three proper
  probability by \(1/8\). RI41 explicitly retains that same construction
  at scale \(e=1/44\); it is not an arbitrary later size-three law.
- The accepted RI151 canonical formula retains the actual hook probabilities
  and is not a free choice of a singleton correction.

The RI41 margins are inherited finite-certificate consequences, not new
axiomatic deductions or new certificate executions. The RI36 bound follows
from its displayed construction and complete row forms. The literal source
notes, acceptance records and scope clarification are pinned in the current
dependency files. Discovery rounding is **not** an accepted global
coefficient-grid theorem; no grid is used in (1)–(3).

## Complete rows and sharpened height transports

Write the unchanged C3 row as \((e,e,e,a)\) on ideals \(0,1,3,7\),
where \(e=1/44\) and \(a=41/44\). In each retained root sector,
the complete C4 row is

\[
 (w,p_i,s_i,b_i,c_i),\qquad
 w+p_i+s_i+b_i+c_i=1.
 \tag{4}
\]

Here \(s_i\) is the initial-pair probability, not the size-seven scale.
All entries are positive, \(w\) is record-blind and \(b_0>b_1\) is
accepted. Neither non-core root ordering is assumed.

The complete RI155 diamonds give probabilities \(41w\), \(41p_i\)
and two separate occurrences of \(41s_i\) in the respective opposite
height-raising rows. In each such parent-four row the genuine full
complement also raises height and exceeds \(1/14\). Subtracting that
positive contribution from the total bound \(19/40\), while retaining
all other ideal occurrences, gives

\[
 w,p_i<P:=\frac{19/40-1/14}{41}=\frac{113}{11480}<\frac1{100},
 \qquad s_i<P/2,\qquad c_i<19/40.
 \tag{5}
\]

The two arm occurrences remain separate even for equal marks. These are
complete marked-row inequalities, not a restriction to selected newborn
outcomes. At a chain parent, the deletion potential is its complete preceding
chain row, so \(\alpha_c\ge1/8\) separately gives

\[
 w,p_i,s_i\ge m:=1/352.
\]

Complete normalization now yields both

\[
 \frac{11489}{22960}<b_i<\frac{2267}{2464}<a,
 \qquad b_i>1/2.
 \tag{6}
\]

The lower bound uses (5); the upper bound uses the three proper lower
bounds and \(c_i>1/14\). These are bounds, not substituted actual values.

## The canonical singleton correction is quantitatively limited

For root \(i\), let \(e_i^{\rm fork}\) be either proper root-plus-leaf
probability of the size-three fork, and let \(v_i^{\rm fork}\) be its full
complement. RI36's bound and the complete fork row give

\[
 0<e_i^{\rm fork}\le1/8,\qquad
 v_i^{\rm fork}=1-2e-2e_i^{\rm fork}.
 \tag{7}
\]

There are two distinct fork arm ideals. No numerical comparison of the two
seed-root declarations is used.

Use RI151's actual hook quantities \(L_i=41p_i\), \(f_i\) and
\(g_{i,u}\), where \(u\) ranges over both retained atom marks. The
single omitted maximum in each relevant hook ideal leaves respectively
the fork proper arm and the fork full row. Therefore their deletion
potentials are \(e_i^{\rm fork}\) and \(v_i^{\rm fork}\). The actual
parent-four coefficient bound gives, with both atom choices retained,

\[
 f_i\ge e_i^{\rm fork}/8,\qquad
 \min_u g_{i,u}\ge v_i^{\rm fork}/8.
\]

Combining these **correlated** fork terms before bounding them proves

\[
 \frac{f_i}{2}+\min_u g_{i,u}
 \ge\frac{1-2e}{8}-\frac{3e_i^{\rm fork}}{16}
 \ge\frac{135}{1408}.
 \tag{8}
\]

It is not legitimate to minimize the fork full and proper entries
independently. The canonical formula is

\[
 N_i=\frac{35}{1476c_i}
       [41p_i-f_i/2-\min_u g_{i,u}]_+.
\]

Hence, for \(\delta=135/57728>1/440\),

\[
 0\le N_i\le\frac{35}{36c_i}[p_i-\delta]_+.
 \tag{9}
\]

The weak inequality is important when the positive part vanishes. If
\(N_i=0\), then \(F_i=1+(1-\theta)^2<2\), already enough for (1).
If \(N_i>0\), then \(p_i>\delta\), and \(c_i>1/14\) implies

\[
 0<N_i<14(p_i-r),\qquad r=1/440<p_i<1/100.
 \tag{10}
\]

Let \(a_\theta=1-\theta\) and keep the strict full complement
\(0\le N_i<a_\theta<1\). The exact complete-parent expression is

\[
 F_i=1+a_\theta^2-2a_\theta N_i+N_i^2/p_i
     <2-2N_i+N_i^2/p_i.
 \tag{11}
\]

The difference of the first expression and the second is
\((1-a_\theta)(2N_i-1-a_\theta)<0\). The second expression is convex
in \(N_i\). On the containing interval from zero to \(14(p_i-r)\),
its maximum is at an endpoint. The nonzero endpoint is

\[
 G(p)=2-28(p-r)+196(p-r)^2/p
     =2+168p-364r+196r^2/p.
\]

This is convex for \(p>0\), so on \([r,1/100]\) its maximum is one
of \(G(r)=2\) and \(G(1/100)=35743/12100\). The latter is larger
than two and strictly below \(71/24\), since
\(24\cdot35743=857832<859100=71\cdot12100\). This proves (1)
with the zero case included. The formal interval endpoints establish a
bound; they are not admitted actual laws with a zero full complement.

Thus the two \(F_i\) cannot control this retained cap. The exact new
conclusion is \(Z=R\), not \(\rho=R\): the actual global maximum may
involve other parents. No original parent equation is removed.

## The sign of every contrast bracket is controlled

Retain the complete RI147 identity

\[
 v=\theta\sum_{S=1,3,7}d_S\mathcal H_S,\quad
 d_S=B_0(S)-B_1(S),\quad
 \mathcal H_S=P_S+2\theta-2-\theta^2T_S,
\]
\[
 P_S=\frac{B_0(S)+B_1(S)}{A(S)},\qquad
 T_S=\frac{B_0(S)^2+B_0(S)B_1(S)+B_1(S)^2}{A(S)^2}.
 \tag{12}
\]

The empty contrast vanishes by locality, not because its row probability
is discarded. Bounds (5)–(6) imply both individual component ratios
\(B_i(S)/A(S)<1\) for each of these three ideals. Thus
\(T_S<(3/2)P_S\), proving \(\mathcal H_S>-2\). For \(S=1,3\),
(5) gives \(P_S<1\), so \(\mathcal H_S<0\). For the core,

\[
 P_7<2267/1148,\qquad
 \mathcal H_7<2267/1148+1/72-2=-235/20664<0.
 \tag{13}
\]

Consequently every bracket lies strictly in \((-2,0)\). Because
\(d_7=b_0-b_1>0\), the core term is strictly negative. Accepted \(v>0\)
therefore forces at least one non-core contrast to be negative:
\(p_1>p_0\) or \(s_1>s_0\). This is a proved disjunction, not selection
of either root ordering.

Define only the actual opposing mass

\[
 D_-=(p_1-p_0)_++(s_1-s_0)_+.
\]

Discarding negative contributions only for an upper bound, and retaining
strictness from the core, gives

\[
 0<v<2\theta D_-,\qquad
 D_-<3P/2-2m=\frac{1147}{126280},
\]
\[
 \boxed{0<v<\frac{1147}{9092160}.}
 \tag{14}
\]

The positive-part bounds cover either zero contrast and both choices of
root ordering. No signed contrast was replaced by a favorable positive one
inside an equality.

## What a pass would now demand of the actual marked rows

Put \(J=b_0^2+b_0b_1+b_1^2\), \(d_7=b_0-b_1>0\) and
\(\lambda=d_7J/b_0^3\). The now-proved cap branch gives

\[
 B=\frac{12\lambda j_0}{1+2\max(E_0,E_1)},\qquad
 \max(E_0,E_1)<3,\quad j_0>71/72.
\]

If \(v>B\), equations (14) and these strict bounds imply

\[
 \lambda<\frac{42}{71}v
 <\frac{1147}{15370080}<\frac1{13000}.
 \tag{15}
\]

Since \(b_1>1/2\) and \(b_0<1\), also \(J/b_0^3>7/4\).
Combining the exact \(\lambda\) with \(v<2\theta D_-\) gives

\[
 \frac{D_-}{d_7}
 >\frac{6j_0J}{\theta b_0^3(1+2M_{\rm cap})}>213.
 \tag{16}
\]

In the actual parent-four component coordinates this requires

\[
 (\alpha_{1,1}-\alpha_{1,0})_+
 +(\alpha_{3,1}-\alpha_{3,0})_+
 >8733(\alpha_{7,0}-\alpha_{7,1}),
 \tag{17}
\]

because \(a/e=41\). These are actual component relations, not freely
chosen coefficients. All positive divisions use \(d_7>0\), not a possibly
zero singleton or initial-pair difference.

An actual proof of \(D_-\le213d_7\) would therefore reject the retained
strict capacity. Indeed the bounds give
\(v<426\theta d_7<(71/24)d_7<B\). No such marked-row comparison is
claimed here. Likewise a lower bound on \(\lambda\) at least
\(1/13000\) would reject capacity, but its known positivity alone does
not provide that magnitude. These are precise sufficient rejection
premises, not arbitrary-coefficient counterexamples.

## The grid inference is not admitted

RI41's discovery paragraph describes rounding an exploratory candidate.
The coordinator's RI157 clarification explicitly does not accept a global
final-witness grid theorem from that description. This proof therefore
does not infer any minimum spacing of distinct component coefficients.

Conditionally, if a separately accepted audit established that every final
parent-four coefficient is a multiple of \(1/1000\), then the already
strict core ordering would give
\(d_7\ge a/1000\), and \(\lambda>d_7\ge41/44000>1/13000\),
rejecting this envelope. That audit is **missing**, not authorized or run
here. It would need to establish the grid for the complete final fixed
coefficient vector, including defaults and overrides, with its exact
certificate/source linkage. Discovery history is not a substitute.

The direct marked-row alternative (16) remains the comparison under the
current source-only assignment. No scientific certificate is decoded, no
override is compared, and no grid result is claimed.

## Remaining scope and handoff

The actual canonical cap branch is proved, but actual \(v>B\), adequate
q/v budget, \(W\), individual \(C_2/C_3\), small-scale membership and
shared H30 remain open. Failing the sufficient envelope does not by itself
determine those signs. A genuine full-envelope pass would obstruct this
fixed H30 candidate; no such pass is proved.

Original P2/P3 and numerical \(Y=1/4\), all 31 focused, 139 policy, 20
native and 42 audit obligations, the other eight parents, all five \(D_i\),
shared T1, strict endpoints and individual ideal multiplicities remain.
RET is paused and measurement stays separate. This finite-law result is
not an all-size, DET-entailment, QM, geometry/gravity or empirical claim.

CANONICAL_CAP_BOUND.md and CORRELATED_CONTRAST_BOUND.md provide the detailed
coauthor arguments; AUTHOR_CHECKS records main/peer reads and actual
administrative checks. Coauthors are not independent reviewers. No new
subagent, source executor, scientific engine or decode, global enumeration,
runtime/card/freeze/admission, repository/index/Git operation or sealed
predecessor change is part of this packet. It stops for fresh nonauthor
review and coordinator adjudication, with no successor assigned here.
