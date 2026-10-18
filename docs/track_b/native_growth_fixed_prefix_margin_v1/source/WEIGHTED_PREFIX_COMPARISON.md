# RI153 — correlated singleton floors and a two-endpoint theorem

30 September 2026. Manual author-side analytic contribution. No actual
prefix coefficient, probability, scale, minimum value or scientific sign
is evaluated. The uniform q/W comparison remains undecided; this note
proves sharper sufficient comparisons and an exact endpoint reduction
for every nonnegative floor of the singleton weighted term.

## 1. Fixed expressions and the correlated interval

Retain the accepted RI151 formula and all its fixed-prefix correlations:

\[
 H_i=41p_i-f_i/2-\min(g_{i0},g_{i1}),\qquad
 \sigma_i=[H_i]_+/c_i\ge0,
 \qquad \gamma=35/1476.
\]

Here p,c,f,g are the unchanged size-four probabilities, not independent
variables to fit. The actual target corrections are
`N_i=gamma sigma_i` and `kappa_i=(35/36)sigma_i/(41p_i)`.
Keep the same actual-containing cap `Z` from RI147, with the same
substituted N_i in all of its defining expressions. Put

\[
 \omega_i=44\theta p_i>0,\quad
 k_i(x)=2-x-2\omega_i+\theta x^2\omega_i^2,
 \quad S(x)=\sigma_0k_0(x)-\sigma_1k_1(x).
 \tag{1}
\]

The inherited exact identity is

\[
 q(x)=T_{\rm core}(x)+\gamma S(x)
 \qquad(0\le x\le Z).
 \tag{2}
\]

Z remains positive and no greater than 1/4. Zero is an analytic endpoint,
not an actual allowed scale. Neither ordering sigma nor ordering the
target component indices determines the correction contrast. No actual
branch of H_i is selected in this note.

## 2. A stronger kernel bound from complete prefix normalization

The accepted stage-four component identity is `J7=41p_i`, at the
four-element hook Q4=(3,1). It is one strictly positive proper probability
in a complete strictly positive row. Therefore

\[
 0<p_i<1/41,\qquad
 0<\omega_i<44\theta/41<11/1476,
 \tag{3}
\]

using the already proved `theta<1/144`. The inequality does not discard
any other Q4 ideal; their positivity is what makes it strict.

Since `k_i'(x)=-1+2theta x omega_i^2<0` on `[0,Z]`,

\[
 0<k_i(Z)\le k_i(x)\le k_i(0)=2-2\omega_i<2.
\]

In particular,

\[
 k_i(x)>2-Z-88\theta/41>2561/1476>41/36.
 \tag{4}
\]

The middle strict comparison follows from `Z<=1/4`, `theta<1/144`;
these are inequalities from fixed definitions, not evaluations of the
actual theta or Z. They improve the earlier universal lower factor.

## 3. The kernel ratio has an exact monotonic direction

Let `R(x)=k1(x)/k0(x)>0`. Direct differentiation and factorization give

\[
 R'(x)=\frac{\omega_0-\omega_1}{k_0(x)^2}
 \left[2-\theta x(4-x)(\omega_0+\omega_1)
              +4\theta x\omega_0\omega_1\right].
 \tag{5}
\]

For example, expansion of the opposite numerator gives
`k0' k1-k0 k1'=(omega0-omega1)[-2+theta x(4-x)(omega0+omega1)
-4theta x omega0 omega1]`, verifying the sign in (5).
The bracket in (5) is strictly positive: on this interval
`x(4-x)<=1`, `omega0+omega1<1` and `theta<1`, while the final term
is nonnegative. Thus its value is greater than one.

Consequently R increases if `p0>p1`, decreases if `p0<p1`, and is
constant if they agree. Define its exact symbolic maximum by

\[
 R_*=
 \begin{cases}
 k_1(Z)/k_0(Z),&p_0\ge p_1,\\
 k_1(0)/k_0(0),&p_0<p_1.
 \end{cases}
 \tag{6}
\]

No root comparison is asserted; both cases are retained. Since sigma1
is nonnegative, the following criterion is exact, including zero sigmas:

\[
 S(x)\ge0\ \text{on }[0,Z]
 \quad\Longleftrightarrow\quad
 C:=\sigma_0-R_*\sigma_1\ge0.
 \tag{7}
\]

Necessity holds at the maximizing endpoint; sufficiency follows from
`S(x)=k0(x)[sigma0-sigma1 R(x)]`. Nothing is divided by either sigma
or their difference. If only positive x are considered and the maximum
is at zero, a negative endpoint value still implies negative values for
sufficiently small positive x by continuity.

## 4. Correlation-aware constant floors, without a sign assumption

Set `z^+=max(z,0)`, `z^-=max(-z,0)` for the fixed expression C. Three
valid uniform floors are

\[
 \begin{aligned}
 K_{\rm box}&=k_0(Z)\sigma_0-k_1(0)\sigma_1,\\
 K_0&=k_0(Z)C^+-k_0(0)C^-,\\
 K_1&=\frac{k_1(Z)}{R_*}C^+
                   -\frac{k_1(0)}{R_*}C^-.
 \end{aligned}
 \tag{8}
\]

The first uses monotonicity of each positive kernel with the negative
root-one term bounded in the opposite direction. For the second, use
`S>=k0(x)C` and distinguish the sign of C. For the third, use
`1/R(x)>=1/R_*` to get `S>=k1(x)C/R_*`, again with the sign retained.
All multipliers and all divisors have proved positive signs.

It follows that

\[
 S(x)\ge K_{\rm corr}:=\max\{K_{\rm box},K_0,K_1\}.
 \tag{9}
\]

This is not a claim that Kcorr is nonnegative. It is, however, provably
no weaker than the earlier RI151 floor `Kold=(41/36)sigma0-2sigma1`.
Indeed

\[
 K_{\rm box}-K_{\rm old}
 =[k_0(Z)-41/36]\sigma_0+[2-k_1(0)]\sigma_1\ge0.
 \tag{10}
\]

Each bracket is strictly positive, so (10) is strict whenever at least
one sigma is positive. If both vanish, S is identically zero and all
these floors equal zero. This is strict improvement of a justified bound,
not a claim that the actual sufficient margin test now passes.

## 5. Exact endpoint theorem for every nonnegative singleton floor

For every fixed `m>=0`,

\[
 \boxed{\quad S(x)\ge m\ \text{for all }x\in[0,Z]
 \quad\Longleftrightarrow\quad
 S(0)\ge m\ \text{and }S(Z)\ge m.\quad}
 \tag{11}
\]

Necessity is immediate. For sufficiency first suppose `p0>=p1`. R is
nondecreasing, and `S(Z)>=m>=0` gives `C>=0`. Both factors in
`S(x)=k0(x)[sigma0-sigma1 R(x)]` are then nonnegative and no smaller
than their values at Z. Thus `S(x)>=S(Z)>=m`.

Suppose instead `p0<=p1`, so `omega0<=omega1`. Write

\[
 S(x)=S(0)-(\sigma_0-\sigma_1)x
       +\theta(\sigma_0\omega_0^2-\sigma_1\omega_1^2)x^2.
 \tag{12}
\]

If `sigma0<=sigma1`, its quadratic coefficient is nonpositive. The
function is concave (including an affine or constant case), hence
bounded below by the smaller endpoint on this interval. If
`sigma0>sigma1`, set `Delta=sigma0-sigma1>0`. Then
`sigma0 omega0^2-sigma1 omega1^2<=omega0^2 Delta`, so

\[
 S'(x)\le-\Delta(1-2\theta x\omega_0^2)<0.
\]

Its minimum is therefore at Z. This proves (11), including equal p,
equal sigma, zero sigma, zero floor, and endpoint equalities.

More precisely, if `m_end=min(S(0),S(Z))>=0`, it is the **exact**
minimum of S on `[0,Z]`. The two endpoint expressions are

\[
 \begin{aligned}
 S(0)&=2\sigma_0(1-\omega_0)-2\sigma_1(1-\omega_1),\\
 S(Z)&=\sigma_0(2-Z-2\omega_0+\theta Z^2\omega_0^2)
       -\sigma_1(2-Z-2\omega_1+\theta Z^2\omega_1^2).
 \end{aligned}
 \tag{13}
\]

Nonnegativity of the requested floor is load-bearing. When an endpoint
is negative, this note does not claim that endpoint values alone give
the minimum of S. The full q may still have an adequate positive floor
because Tcore compensates for a negative singleton contribution. That
possibility is not rejected by a failure of (11)'s sufficient application.

## 6. A precise sufficient prefix comparison for the q floor

Tcore is the accepted degree-at-most-two polynomial in x. Let mT be any
proved uniform lower bound for it on the **same** `[0,Z]`, or its exact
unevaluated symbolic minimum. For the latter, use both endpoints if the
quadratic coefficient is nonpositive; if it is positive, evaluate the
symbolic expression at its vertex clipped to `[0,Z]`. This is a manual
definition with all zero and endpoint cases, not a numerical minimization
or an assumption that the core is positive.

Equations (2) and (9) prove the valid certificate

\[
 q(x)\ge Q_{\rm cert}:=mT+\gamma K_{\rm corr}.
 \tag{14}
\]

If the endpoints in (13) are nonnegative, one may replace Kcorr by the
exact `m_end`, or take the maximum of valid floors. No arbitrary prefix
counterexample or favorable point is introduced by this comparison.

For a specified adequate positive q threshold `Qreq`, put

\[
 M_{\rm req}=\max\{0,(Qreq-mT)/\gamma\}.
\]

The two explicit fixed-prefix comparisons

\[
 S(0)\ge M_{\rm req},\qquad S(Z)\ge M_{\rm req}
 \tag{15}
\]

then suffice for `q(x)>=Qreq` on the entire correlated interval. This
follows from the exact nonnegative-floor theorem, not a generic signed
coefficient envelope. It reduces this sufficient route to two endpoint
relations of the same fixed positive-part prefix expressions. It is
not necessary for adequate q: mT may be conservative or the core may
compensate a negative singleton term in a correlated manner.

For orientation, the companion budget reduction keeps

\[
 \begin{gathered}
 A=12\lambda gZ^2>0,\quad B=12\lambda j_0Z/(1-Z)>0,\\
 E=12Z^2(1+\eta)(j_0+gZ)>0,\quad
 Y=1/d(Z),\quad u_j=Uj0(Z).
 \end{gathered}
\]

Here g is the old positive aggregate `theta^3 c0`, not g_iu. The
original separate sensitivity v remains required. With

\[
 C_0=1-B/v,\qquad C_1=1-(1-Yu_3)B/v-YE,
\]

both RI147 endpoint budgets are equivalent to `C0>0`, `C1>0` and

\[
 \min_{[0,Z]}q\ge Qreq
 :=A\max\{1/C_0,(1-Yu_2)/C_1\}.
 \tag{16}
\]

The positive factor `1-Yu2` is retained. No formula in (14)–(15)
replaces the separate v requirement or either budget. If either C is
nonpositive, no finite positive q floor can satisfy this particular
envelope; that is not a sign conclusion for W. For positive C0,C1,
`Qcert>=Qreq`, or the endpoint route (15), is a concrete sufficient
comparison at the unchanged correlated prefix. None is proved to hold
here.

## 7. Remaining issue and preserved boundaries

The new yield is the sharpened prefix normalization bound, an exact
monotone kernel ratio, correlation-aware floors strictly dominating the
old floor when a sigma is nonzero, and the exact two-endpoint theorem
for every nonnegative singleton floor. The remaining sufficient
prefix relation is explicitly (14) versus (16), or (15), together with
the separate positive budget denominators. This is more specific than
an unspecified ordering of sigma or the original canonical coordinates.

The actual signs of the endpoint contrasts, the adequate v/D3 floor,
the full correlated q floor and both joint budgets have not been
evaluated or proved. A failed sufficient floor is not a positive W
result, a countermodel to the fixed prefix, or a proof of nonderivability.
Actual rho membership in the obstruction interval, individual C2/C3
signs and complete H30 feasibility remain open. All other parents and
the shared-variable constraints remain binding. Boundary zero components
still retain positive actual strict restoration.

## 8. Actual source reading and work scope

The complete new assignment and root decision were read at
`/Volumes/AI_DATA/development/det-review-evidence/ri151-root-formula-review-_rfeb0e3/NATIVE_SUCCESSOR_RESERVATION.json`
and `RI151_ROOT_ADJUDICATION.json`. They accept the unchanged RI151
J7 identity, full fixed-prefix formula and exact q substitution. The
literal RI147 and RI151 manuscripts supplying k, Tcore, the correlated
domain and joint budgets were read in full in the preceding author
contributions; their mathematical definitions are retained here. The
current parent budget derivation and prefix-agent structural refinements
were coordinated by manual author-peer algebra, not treated as
independent acceptance.

Only this assigned Markdown is authored. No scientific body was decoded,
actual numerical prefix/coefficient/probability/history/maximum/scale/H/z
or sign was evaluated, and no symbolic/numerical engine, source/helper
import, compilation, AST, probe, execution, global enumeration, runtime
inventory, controller, card or admission was used. No repository/index/Git
or predecessor edit occurred. The 31/139/20/42 obligations, both joint
budgets, shared T1 recovery, other eight connected parents, all five Di
conditions, strict endpoints and old P2/P3/Y=1/4 remain unchanged. RET
is paused and measurement separate. No QM, geometry, gravity, all-size,
empirical or ontological conclusion is introduced.
