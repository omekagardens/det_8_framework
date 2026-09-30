# RI145 — author-peer crosscheck of the weighted-margin bound

This is a symbolic, source-only author-peer derivation, not independent
adjudication or an executed scientific check. It uses the unchanged held
relations and accepted interval of RI127/RI128. No probability table,
scientific JSON body, seed, native scale, polynomial coefficient, maximum,
or numerical sign is evaluated. In particular it does not assume a stronger
bound on the actual size-six scale than the accepted one.

## 1. Premises and notation

Write `theta=c5/36`, and retain RI128's held row values, proper-potential
sums, and positive scalars. The polynomial coefficient `C2_i` is not the
local margin `C_2`. Set

\[
 X=\min(R,1/4),\qquad
 R=\frac1{2(1+\max(E_0,E_1))},\qquad
 d(x)=2(3-2x+x^2).
\]

The formal domain used in this proof is

\[
 0<x\le X,\qquad 0<y\le 1/d(x).
 \tag{1}
\]

RI128's accepted scale bound and B14 show that (1) contains the actual
pair `(rho,s)`. This analytic use of B14 does not modify a predecessor
certificate, its selected method, or its executor. The interval is fixed
before this derivation; no native scale is chosen or retuned.

The following literal source relations are the load-bearing premises:

- [RI120 prefix lemmas](/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn/ANALYTIC_PREFIX_LEMMAS.md),
  A1/A3/A4: `D_i(0)=theta B_i(0)`,
  `G_i(S)=theta B_i(S)^2/A_i(S)` on all four stem ideals, and
  `h_i=theta c_i`, `m_i=theta^2 c_i`.
- [RI120 F2 analytic check](/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn/F2_ANALYTIC_CHECK.md:132),
  equations (2), (4), (5): `N_i>=0` and
  `E2_i=1+(1-theta)(h_i+j_i)+N_i(r_i^root-1)`, where
  `r_i^root=G_i(1)/B_i(1)`.
- [RI41 normalization](/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md:56),
  section 1: the three-chain proper slots, including `A_i(1)`, are `1/44`.
- [RI63 strict restoration](/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md:164),
  equation (6): `c5=1/[2(1+M5)]`, with `M5>0` because a proper potential
  is strictly positive. Only this definition and positivity are used,
  not the later displayed numerical value of `M5` or `c5`.
- [RI128 input formulas](/Volumes/AI_DATA/development/det-review-evidence/ri128-connected-sign-dvgWLqqv/INPUT_FORMULAS.md:147),
  equations (2)–(10): complete positive held sums, the native radius,
  `q=-Q2_1`, the empty coefficients, and the two pivot ratios.
- [RI127 local positivity](/Volumes/AI_DATA/development/det-review-evidence/ri127-connected-compensation-nMyz57P5/LOCAL_POSITIVITY.md:161),
  section 4 and the paragraph beginning at line 357: `q(x)>0` on
  `0<x<=R`, `q(0)>0`, and `Q2_1` is a strictly negative scalar times
  its monic quadratic. Consequently the quadratic coefficient `q2` of
  `q(x)=q0+q1 x+q2 x^2` is strictly positive.
- [RI128 analytic bounds](/Volumes/AI_DATA/development/det-review-evidence/ri128-connected-sign-dvgWLqqv/ANALYTIC_BOUNDS.md:342),
  B14/B15: the curved upper bound for `s` and the seed-free harmonic
  identity for `W=3m0 C_2+3j0 C_3`.

## 2. Full-domain positivity of the proper-potential sums

The RI63 definition gives `0<theta<1/72<1`. Positive complete-row
normalization gives `0<B_i(1)<1`. The stem identity and RI41 proper slot
therefore imply

\[
 r_i^{\rm root}
 =\theta\frac{B_i(1)}{A_i(1)}
 =44\theta B_i(1)<\frac{11}{18}<1.
\]

The complete H5 row has four strictly positive stem slots together with
`2h_i+j_i`, so `0<h_i+j_i<1`. As `N_i>=0`, RI120 equation (5) yields

\[
 E2_i
 =1+(1-\theta)(h_i+j_i)+N_i(r_i^{\rm root}-1)
 \le1+(1-\theta)(h_i+j_i)<2.
 \tag{2}
\]

This retains `N_i=0`; strict negativity of its contribution is unnecessary.
The original complete-sum formulas also give `B2_0>0`, `C2_0>0` and
`0<V0<E0`. In particular

\[
 A2_0=E0+2E2_0-j0<E0+4.
\]

For `0<x<=X<=R`, the radius definition gives
`x E0<=1/2-x`. Hence, throughout (1),

\[
 \begin{aligned}
 U20(x)
 &=3-A2_0x+B2_0x^2+C2_0x^3\\
 &>3-x(E0+4)
 \ge\frac52-3x
 \ge\frac74,\\[2mm]
 U30(x)
 &=2-x-x(1-x)V0\\
 &>2-x-xE0
 \ge\frac32.
 \end{aligned}
 \tag{3}
\]

The strict inequalities remain strict at `x=X`. Thus `1-y U20<=1` and
`1-y U30<=1` everywhere in (1). The proof does not require either formal
full complement to be positive away from the actual pair. Multiplication
by the positive pivot factors preserves these upper bounds even if a
formal complement is negative.

## 3. Independently normalized weighted identity

Put

\[
 r=r_{3,0},\qquad
 \lambda=\frac{D3}{r}=1-(b_1/b_0)^3,\qquad
 \eta=\frac{\epsilon3}{r},\qquad
 g=\theta^3c_0.
\]

Here `r,g,eta>0` and `0<lambda<1`. The lowercase `g` in this note denotes
only this aggregate; it is not the source's held slot `g_i=G_i(7)`.
The accepted core identities give `r2_0=theta r`, `D2=theta D3` and
`m0 theta=g`. The empty-stem identity gives
`epsilon2=theta epsilon3`. Substituting these identities, the pivot ratios,
and the empty/core/full formulas into B15 gives exactly

\[
 \frac Wr=-1+
 12\lambda\left[
  \frac{j_0x(1-yU30(x))}{(1-x)v}
  +\frac{g x^2(1-yU20(x))}{q(x)}
 \right]
 +12y x^2(1+\eta)(j_0+gx).
 \tag{4}
\]

For example the T2 empty/core contribution is
`m0 y x^3(epsilon2+r2_0)/r = g y x^3(1+eta)`; the T3
contribution is `j0 y x^2(1+eta)`. This checks the power of `theta`
and the extra power of `x` in (4). B15 eliminates the seed coordinates
exactly by the accepted harmonic row; none is evaluated or selected.

## 4. A strictly positive symbolic denominator floor

Define, without evaluating any coefficient,

\[
 x_* =\max\!\left(0,\min\!\left(X,-\frac{q_1}{2q_2}\right)\right),
 \qquad \mu=q(x_*).
\]

Since `q2>0`, completing the square shows that this is the minimum of
`q` on `[0,X]`. Accepted positivity on `(0,X]` and `q(0)>0` give `mu>0`.
This includes both endpoint minima and a vertex at an endpoint; no degree
drop or unsupported leading-coefficient sign is assumed. It is a symbolic
description of a proven positive floor, not numerical optimization or a
new choice of scientific scale.

Let `Y*=1/d(X)`. For `0<=x<=X<=1/4`,
`d(x)-d(X)=2(x-X)(x+X-2)>=0`, so `y<=Y*<=8/41`. Define

\[
 L=\frac{12\lambda j_0}{(1-X)v}>0,\qquad
 K=\frac{12\lambda g}{\mu}
      +12Y_*(1+\eta)(j_0+gX)>0.
 \tag{5}
\]

Apply (3) to the two full factors in (4), then use
`1/(1-x)<=1/(1-X)`, `q(x)>=mu`, `y<=Y*`, and `j0+gx<=j0+gX`.
All remaining multipliers are positive. The result is the uniform bound

\[
 \boxed{\quad W/r\le-1+Lx+Kx^2\quad}
 \qquad\text{on (1).}
 \tag{6}
\]

## 5. Explicit obstruction interval and unresolved native membership

For a formal margin fraction `0<=zeta<1`, set

\[
 t_\zeta=
 \frac{2(1-\zeta)}{L+\sqrt{L^2+4K(1-\zeta)}},
 \qquad \delta_\zeta=\min(X,t_\zeta)>0.
 \tag{7}
\]

Rationalizing the positive quadratic root gives
`L t_zeta+K t_zeta^2=1-zeta`. Because `Lx+Kx^2` is strictly increasing
for `x>=0`, (6) proves

\[
 0<x\le\delta_\zeta,\quad 0<y\le1/d(x)
 \quad\Longrightarrow\quad W\le-\zeta r.
 \tag{8}
\]

In particular `zeta=1/2` gives the strict, seed-free obstruction
`W<=-r/2<0` on an explicitly defined nonempty subdomain. At `zeta=0`
the endpoint conclusion is only `W<=0`; strict negativity follows for
`x<t_0`. Since `m0,j0>0`, either nonpositive conclusion excludes
simultaneous strict positivity of both local margins at that same point.

The sufficient condition `LX+KX^2<=1` would extend nonpositivity to all
of (1), including the actual pair. It is equivalent to nonpositivity of
the bounding polynomial throughout `[0,X]`, not equivalent to a sign
criterion for `W` itself. This note establishes neither that condition
nor `rho<=delta_(1/2)`. A failure of this sufficient bound would not prove
positive feasibility. The actual connected H30 sign decision therefore
remains open; no stronger actual-scale premise, parameter tuning,
support change, new scientific evaluation, or executor is introduced.
