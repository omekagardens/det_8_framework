# RI147 — individual-parent bounds for the unchanged actual scale

30 September 2026. Author-side analytic contribution: literal source reading
and manual algebra only. This is not independent acceptance, an executed
scientific check, or a decision of the actual connected margins.

## 1. Result and scope

The accepted five six-parent shapes supply a new explicit lower bound for
the global proper-potential maximum. In particular, the complete row at
`P4=C4 ordinal-sum A2` has the exact sum

\[
 F_i=1+\ell_i^2+N_i^2\left(\frac1{B_i(1)}-1\right)>1.
 \tag{1}
\]

This retains the actual singleton component correction `N_i`; it does not
replace the size-four component law or the size-five mixture by a common
scale. Together with the already held `E_0,E_1`, (1) gives an actual-containing
scale cap `Z` below. A second deduction is the unevaluated strict bound
`E_i>71/24`, hence `rho<12/95`.

The stronger cap and monotonicity of both reference sums give a two-endpoint
upper bound for the weighted margin which retains its negative full-factor
terms. It improves the earlier positive-term-only envelope. Its remaining
coefficient comparisons are stated exactly; none is established numerically
or promoted to a conclusion about actual H30 feasibility.

## 2. Fixed notation and the direction of the scale inequality

Keep the complete positive held rows `A_i,B_i,G_i,D_i` of RI117/RI128 and
the same records `i=0,1`. The four C3 ideals are `0,1,3,7`; the five C4
ideals are `0,1,3,7,15`. In particular `B_i(15)=c_i`, and `A_i` includes
its full probability at `7`. The retained identities are

\[
 \begin{gathered}
 \theta=c_5/36>0,\quad
 D_i(S)=\theta B_i(S)\quad(S=0,3,7,15),\\
 D_i(1)=\theta B_i(1)+N_i,\quad N_i\ge0,\quad
 \ell_i=1-\theta-N_i>0,\\
 G_i(S)=\theta B_i(S)^2/A_i(S)\quad(S=0,1,3,7),\\
 h_i=\theta c_i,\quad m_i=\theta^2c_i.
 \end{gathered}
 \tag{2}
\]

Here the `S=15` instance of `D_i` denotes the held `e_i`, not a C5 full
slot. The C5 full slot is `ell_i`. Their distinction is needed below.

The actual global law, not a selected-row substitute, is

\[
 \rho=\frac1{2(1+M_6)},\qquad
 M_6=\max_{\text{all marked six-parents}}U(P,r).
 \tag{3}
\]

Every complete individual-parent sum `U_*` therefore implies
`M6>=U_*` and `rho<=1/[2(1+U_*)]`. A lower bound on the maximum gives an
upper bound on the actual scale. No maximum or scale is evaluated here.

## 3. Complete individual-parent lower bounds

RI85's five parent shapes have the following proper-potential sums. These
are complete individual-ideal sums, not the supported portion of a harmonic
row. No newborn-bit conditioning or automorphism division occurs.

| Existing parent | Complete sum |
|---|---|
| `P1=C3 ordinal-sum A3` | `E_i=sum_S A_i(S)G_i(S)^3/B_i(S)^3+3m_i+3j_i` |
| `P2=C3 ordinal-sum (C2 disjoint A1)` | `E2_i=sum_S D_i(S)G_i(S)/B_i(S)+e_i h_i/c_i+h_i+j_i+ell_i` |
| `P3=F(H5)` | `1` |
| `P4=C4 ordinal-sum A2` | `F_i=sum_(S ideal C4) D_i(S)^2/B_i(S)+2ell_i` |
| `P5=C6=F(C5)` | `1` |

The first two complete sums are explicitly derived in RI117. For P3 and
P5, the proper ideals are exactly all ideals of the smaller parent. The
unique-maximal deletion potential is the corresponding complete smaller
row probability, so normalization gives one, including its full ideal.

For P4, let its two new maxima be `a,b`. A proper ideal contained in the
C4 stem omits both maxima. The two singleton deletions give the same C5
entry `D_i(S)` with transported records; the double deletion gives the
C4 entry `B_i(S)`. Its potential is therefore `D_i(S)^2/B_i(S)`.
All five stem ideals occur once, including the whole C4 stem. The other
two proper ideals are `C4+a` and `C4+b`. Each omits exactly one maximum,
so each has potential equal to the C5 **full** probability `ell_i`.
The full six-parent ideal is excluded. This accounts for all seven
proper ideals in RI85's eight-ideal P4 row.

Using (2) and the complete C4 row sum, without assigning a value to any
entry, gives

\[
 \begin{aligned}
 F_i
 &=\theta^2+2\theta N_i+\frac{N_i^2}{B_i(1)}+2\ell_i\\
 &=1+\ell_i^2+N_i^2\left(\frac1{B_i(1)}-1\right)>1.
 \end{aligned}
 \tag{4}
\]

Strictness uses `ell_i>0` and `0<B_i(1)<1`; it does not require `N_i>0`.
Thus zero canonical singleton correction remains covered. Every bound
holds on the transported record domain; the two fixed representatives
used here do not assert that they maximize the row sum.

## 4. A stronger explicit constant bound, without a new scale

The same complete two-maximum argument at the size-five parent H5 gives
its unscaled proper-potential sum

\[
 K_i=\sum_{S=0,1,3,7}\frac{B_i(S)^2}{A_i(S)}+2c_i.
\]

The RI63 row sum `sum_c A_jc` is the sum of all proper potentials in
that row, partitioned by their ratio components. Thus its defining maximum
`M5` includes this sum: `M5>=K_i`. Complete C3 normalization and
`sum_S B_i(S)=1-c_i` give the exact positive decomposition

\[
 K_i=1+c_i^2+
 \sum_S A_i(S)
 \left(\frac{B_i(S)}{A_i(S)}-(1-c_i)\right)^2>1.
 \tag{5}
\]

RI63 fixes `theta=1/[72(1+M5)]`, so

\[
 0<\theta\le\frac1{72(1+K_i)}<\frac1{144},
 \qquad \theta K_i<\frac1{72}.
 \tag{6}
\]

The actual H5 mixture is used only through the accepted special identities
(2): all four stem probabilities and both one-cap probabilities have the
restoration coefficient. Its full complement is therefore
`j_i=1-theta K_i>71/72`. This statement is not extended to an arbitrary
size-five row or its singleton component. Consequently

\[
 M_6\ge E_i>3j_i>\frac{71}{24},
 \qquad 0<\rho<\frac{12}{95}.
 \tag{7}
\]

The stronger symbolic `E_i` bounds are retained; (7) is only a convenient
constant consequence. In particular the already proved `E2_i<2` makes the
P2 and unique-maximum bounds redundant relative to `E_0` for the selected
comparison, not missing from the complete-parent derivation.

## 5. A fixed actual-containing cap using the retained parents

Retain RI145's definitions of `R`, `X`, and `d`. Define

\[
 Z=\min\left\{X,\frac1{2(1+F_0)},\frac1{2(1+F_1)}\right\},
 \quad X=\min(R,1/4),\quad
 R=\frac1{2(1+\max(E_0,E_1))}.
 \tag{8}
\]

All these expressions are fixed, positive, and unevaluated. Equations
(3)–(4) prove `rho<=Z`. Equation (7) also gives `X=R<12/95<1/4`, hence
`Z<12/95`. Formula (8) neither asserts `Z<X` for the unknown coefficients
nor identifies the maximizing six-parent. It defines a new analytic
containing cap authorized for this proof, not a change to the old numerical
certificate or its fixed input domain.

For `d(x)=2(3-2x+x^2)`, decreasing on `[0,Z]`, set `Y=1/d(Z)`.
The accepted B14 bound gives `s<=1/d(rho)<=Y<=8/41`. The actual pair
therefore belongs to `0<x<=Z, 0<y<=1/d(x)`, and also to its containing
rectangle `0<x<=Z, 0<y<=Y`.

## 6. Monotonicity keeps the negative full-factor contributions

RI145 proved `U20=3-x mathcal K(x)` with

\[
 \begin{aligned}
 \mathcal K(x)={}&(1-\theta x^2)T_0
 +(3-2x-\theta x^2)m_0+(2-2x)j_0+2J_0\\
 &+(2-x)\ell_0+N_0\omega_0(2-\theta x^2\omega_0),
 \end{aligned}
\]

where `T0,J0,ell0,m0,j0>0`, `N0>=0`, and `0<omega0<1`.
Differentiating this displayed polynomial by hand gives

\[
 \begin{aligned}
 -U20'(x)={}&(1-3\theta x^2)T_0
 +(3-4x-3\theta x^2)m_0+(2-4x)j_0+2J_0\\
 &+(2-2x)\ell_0+N_0\omega_0(2-3\theta x^2\omega_0)>0
 \end{aligned}
 \tag{9}
\]

on `[0,X]`: every bracket is strictly positive for `x<=1/4` and
`theta<1/144`; the last entire term may vanish. Also
`U30'(x)=-1-(1-2x)V0<0`. Set

\[
 u_2=U20(Z),\qquad u_3=U30(Z).
\]

Then `Uj0(x)>=u_j` for `0<x<=Z`. The accepted bounds give
`7/4<u2<3`, `3/2<u3<2`; thus `1-y u_j>0` for all `0<y<=Y`.

For the positive quadratic `q=q0+q1 x+q2 x^2`, let

\[
 t_Z=\min\{Z,\max\{0,-q_1/(2q_2)\}\},\qquad
 \mu_Z=q(t_Z)>0.
 \tag{10}
\]

RI145's accepted `q2>0`, `q(0)>0` and positivity on `(0,R]` prove by
completing the square that this is its exact symbolic minimum on `[0,Z]`.
No root, coefficient or minimum value is computed. The closed endpoints,
including a vertex at an endpoint, are retained.

## 7. Improved sufficient test at the actual-containing cap

Use RI145's positive fixed scalars
`r=r3_0`, `lambda=D3/r`, `eta=epsilon3/r`, `g=theta^3 c0`, and `v=V1-V0`.
Here `g` is an aggregate, not the held probability `g_i`. Define the
following unevaluated envelope coefficients, distinguished from the held
row and local-margin notation:

\[
 a_2=\frac{12\lambda gZ^2}{\mu_Z},\qquad
 a_3=\frac{12\lambda j_0Z}{(1-Z)v},\qquad
 b=12Z^2(1+\eta)(j_0+gZ).
 \tag{11}
\]

For `0<x<=Z`, `0<y<=1/d(x)`, the exact normalized identity and (9) give

\[
 \begin{aligned}
 W(x,y)/r
 &\le-1+a_2(1-yu_2)+a_3(1-yu_3)+yb\\
 &=-1+a_2+a_3+y(b-u_2a_2-u_3a_3).
 \end{aligned}
 \tag{12}
\]

To check the inequality directions, first replace `Uj0(x)` by its lower
bound `u_j`. The resulting full factors are positive. Then use
`x^2/q(x)<=Z^2/mu_Z`, `x/(1-x)<=Z/(1-Z)`, and monotonicity of
`x^2(j0+gx)`. Thus the positive coefficient substitutions do not multiply
an uncontrolled negative factor.

Maximizing only this affine upper bound over `0<y<=Y` yields

\[
 \boxed{\quad W/r\le-1+\mathcal S_Z,\qquad
 \mathcal S_Z=a_2+a_3+Y\max\{b-u_2a_2-u_3a_3,0\}.\quad}
 \tag{13}
\]

The lower endpoint may be a supremum as `y` tends to zero; it is not an
admitted actual scale. The sufficient condition `mathcal S_Z<=1` is
equivalent to the two explicit envelope comparisons

\[
 a_2+a_3\le1,\qquad
 (1-Yu_2)a_2+(1-Yu_3)a_3+Yb\le1.
 \tag{14}
\]

Equality in (14) suffices for nonpositivity; a strict upper bound below
one gives a strict negative margin. By construction (13) is no weaker
than discarding the negative full-factor terms, which gives
`W/r<=-1+a2+a3+Yb`. Reducing X to Z also increases the quadratic minimum
and reduces the other positive cap factors. These are symbolic comparison
statements, not proof that any of the sufficient inequalities passes.

## 8. Exact sensitivity-ratio gap and claim boundary

Define only abbreviations of the unchanged sensitivity ratios,

\[
 \sigma_3=v/D3>0,\qquad \sigma_{2,Z}=\mu_Z/D3>0.
\]

Then (11) becomes

\[
 a_3=\frac{12j_0Z}{r(1-Z)\sigma_3},\qquad
 a_2=\frac{12gZ^2}{r\sigma_{2,Z}}.
 \tag{15}
\]

Any proved lower bounds on these ratios may safely replace their
denominators: both coefficients of `a2,a3` in each endpoint of (14)
are strictly positive. Mere positivity of the ratios does not supply
their required magnitudes. In particular the first comparison needs a
joint bound on both contributions, not two separate bounds by one.

This note proves neither (14) nor a lower sensitivity-ratio bound strong
enough to imply it. The residual `Delta N`, `Delta(N omega)`, and
`Delta(N omega^2)` terms in RI145's exact q identity are not discarded.
Any further cancellation must follow from the actual C4/C5 component
definitions, not from freely assigning positive held entries. A failure
of (14) would not prove positive W, still less a positive continuation.

For an exact, less conservative full-domain criterion one may retain the
RI145 cleared polynomials `a(x),b(x)` themselves: `a(x)<=0` and
`d(x)a(x)+b(x)<=0` for all `0<x<=Z` are equivalent to W nonpositive on
that entire curved domain. Neither comparison has been settled here.
The cap and its envelope do not decide the actual connected signs,
actual membership in the earlier small-x interval, or the full shared
H30 system. All other connected parents, the single shared T1 recovery,
the five Di conditions and strict endpoints remain binding.

## 9. Actual reading and work boundary

The following literal sources were read for this contribution:

- `/Volumes/AI_DATA/development/det-review-evidence/ri146-root-current-capture-9bfi4u8s/NATIVE_SUCCESSOR_RESERVATION.json`: complete assignment.
- `/Volumes/AI_DATA/development/det-review-evidence/ri128-connected-sign-dvgWLqqv/ANALYTIC_BOUNDS.md`: sections 1–4 reread; complete document had been read for RI145. B3–B5 fix the maximum domain and complete unique-maximum proof; B14 supplies the correlated scale bound.
- `/Volumes/AI_DATA/development/det-review-evidence/ri117-coupled-positive-family-QrAaK5YQ/CONNECTED_CONSTRAINTS_LEMMA.md`: complete; all individual proper ideals for E/E2 and their retained records.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_four_vertex_cap_v1/DESIGN.md`: complete; five parent shapes, full ideal lists, maximal-deletion transport, and actual-baseline restrictions.
- `/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn/ANALYTIC_PREFIX_LEMMAS.md`: complete; actual restoration identities and H5 full complement.
- `/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn/F2_ANALYTIC_CHECK.md`: complete; singleton correction, ell, complete-row substitution and forbidden common-scale replacement.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md`: section 4's unchanged strict-mixture definition reread; no printed large scientific value used.
- `/Volumes/AI_DATA/development/det-review-evidence/ri145-native-weighted-margin-proof-zo96x_ci/WEIGHTED_MARGIN_PROOF.md`: complete author-peer read in RI145, with relevant definitions searched again in this sitting; the now accepted symbolic identity, positive decomposition, q floor and claim limits are reused as premises.

Only this assigned Markdown is authored. No scientific body was decoded,
source/helper imported or executed, symbolic/numerical engine invoked,
probability queried, actual maximum/scale or H/z evaluated, or global order
family enumerated. No controller, fixture, runtime inventory, card, admission,
repository/index/Git change or predecessor edit occurred. RET and measurement
remain separate; no QM, geometry, gravity or empirical claim is added.
