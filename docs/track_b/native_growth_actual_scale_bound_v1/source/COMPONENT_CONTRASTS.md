# RI147 — actual component contrasts and correlated sensitivity ratios

30 September 2026. Manual analytic author work. The literal accepted source
definitions were read as text; no source, helper, scientific body, symbolic
engine, numerical engine, fixture or native calculation was executed. This
contribution is not an independent adjudication.

## 1. Outcome

The C4 singleton probability and the C5 singleton correction are products
of the **actual, fixed ratio-component coefficients**, not independently
selectable positive quantities. Their two root records occupy distinct
components at each layer. An intrinsic terminal-root invariant proves this
separation without determining or enumerating component indices.

Keeping that correlation gives an exact factorization of the singleton
part of q into two positive factors multiplying the actual C4 probability
contrast and actual C5 canonical-component contrast. Complete four-slot
expansion then expresses v/D3 and q(x)/D3 in two signed relative C4
contrasts and that retained canonical contrast. All signs and zero cases
are kept; the empty slot is removed from these contrast sums only because
its contrast is exactly zero, not from the complete held rows.

No positive quantitative ratio lower bound sufficient for actual
rho<=delta0 or W<=0 is proved. The remaining premise is a specific
dominance comparison among these actual component terms, stated below,
not permission to substitute free coefficients, fit a scale, or execute
the historical certificate.

## 2. Literal source meaning of the component symbols

Write C4=(0,1,3,7) and C5=(0,1,3,7,15) in the accepted predecessor-mask
notation. Let i=0,1 denote the transported root record; all other retained
representative bits are zero. The four C3 ideals S=0,1,3,7 have the same
complete record-blind row A(S), with A(0)=A(1)=A(3)=1/44 and positive
full entry a=A(7). These are inherited fixed-prefix definitions, not new
operands extracted from a scientific object.

Let c4(S,i) denote the accepted ratio-graph component containing
`node(C4,S,i)`, and c5(1,i) the accepted parent-five component containing
`node(C5,1,i)`. The component symbols stand for the actual assignments;
no new indices are calculated here. Define

\[
 \alpha^{(4)}_{S,i}
 :=\alpha^{(4)}_{c4(S,i)}>0,\qquad
 \kappa_i:=\frac{35}{36}\alpha^{\min,(5)}_{c5(1,i)}\ge0.
 \tag{1}
\]

In RI41 `check.py`, `layer()` constructs every node before its full marked
diamond adjacency and orders components by their minimum local key;
`load_certificate()` supplies the fixed positive component vector. The
direct row in `main()` is component coefficient times `potential()`.

RI63 `check.py` independently expresses the same prefix in `layout()`,
`node()`, `potential()`, `Components`, and `reconstruct_prefix()`.
The latter binds `COEFFICIENTS4[key]` to the fixed `OVERRIDES4` lookup or
default at the reconstructed component. `pin_prefix_certificate()` binds
those literal tables to the actual RI41 certificate. The size-four branch
of `row()` multiplies that coefficient by the deletion potential.

At size five, `build_problem()` supplies the fixed component assignment
and complete row caps. `check_certificate_core()` verifies the canonical
alpha vector and all sequential face-dual stages, separately retaining an
alternative primary optimum rather than substituting it. Finally,
`certificate_reports()` forms the actual mixed coefficient as
`(1-eta)*alpha + eta*interior_c`, with eta=1/36. These definitions give
theta=c5/36=1/[72(1+M5)] and the coefficient theta+kappa_i at the C5
singleton. Reading these definitions does not run any of those functions,
reconstruct their graph, or retrieve a selected numerical coefficient.

For a chain, the unique maximal deletion in the literal potential formula
leaves the complete preceding chain row. Therefore, for every stem ideal,

\[
 B_i(S)=A(S)\alpha^{(4)}_{S,i},\qquad
 B_i(1)=A(1)\alpha^{(4)}_{1,i},
 \tag{2}
\]

and for the singleton specifically,

\[
 D_i(1)=(\theta+\kappa_i)B_i(1),\qquad
 N_i:=D_i(1)-\theta B_i(1)=\kappa_i B_i(1).
 \tag{3}
\]

Thus N_i contains the actual C4 singleton as a factor. C4 and C5 are
different layers with different component vectors; no equality between
their coefficients follows from the common deletion-potential formula.

## 3. Why the two singleton records cannot be identified

Each proper node (P,S,r|S) has an intrinsic unmarked terminal: append the
newborn above S. Each ratio edge in both literal graph constructions is
an ordinary two-birth diamond from a fixed smaller base. Its two endpoint
nodes have the **same terminal up to the newborn swap**. Quotienting a node
by an isomorphism of its entire parent, precursor and precursor marks also
preserves that terminal isomorphism class. Hence a path of such edges
cannot leave its unmarked terminal class.

For C4 singleton birth the terminal is the Ferrers hook with row lengths
(4,1); for C5 singleton birth it is the hook with row lengths (5,1).
In each, the root is the unique minimum and lies strictly below every
maximal vertex. In any presentation as a proper birth, the newborn is a
maximal vertex. Its entire past, the precursor, therefore contains the
intrinsic root. The root is not a removable newborn or an excluded old
mark in any incident role. Its bit remains in the selected precursor at
both endpoints of every incident diamond and under every transported
isomorphism. Changing the unrelated newborn bits cannot change that bit.

In particular, there is no path through an empty-precursor node that could
erase the root bit: an empty birth creates an isolated newborn, whereas
these terminal hooks are connected and have a unique minimum. The two
root bits cannot be interchanged by an automorphism either, since the
root is intrinsic and its binary mark is transported, not complemented.

Consequently

\[
 c4(1,0)\ne c4(1,1),\qquad c5(1,0)\ne c5(1,1).
 \tag{4}
\]

This is a graph-invariant argument, not a new graph enumeration. It does
not assert that different components must receive different numerical
coefficients. Equal coefficient values remain possible, as does a zero
canonical C5 coefficient; their actual values are not calculated here.

Both a hook and either parent obtained by deleting one of its maximal
vertices are Ferrers. Every corresponding birth role is defect-neutral.
Thus the accepted rule forcing a component with a raising role to have
zero canonical coefficient does not supply such a conclusion for this
singleton hook component. Conversely, neutrality does not force it to be
active. The actual canonical optimization, including its tie-break,
remains the premise controlling kappa0 and kappa1. Neither root-bit order
nor minimum-key/component-index order is a proved coefficient monotonicity.

## 4. Complete actual C4 contrast factorization

For S in {0,1,3,7}, define fixed held expressions

\[
 \begin{split}
 d_S&:=B_0(S)-B_1(S),\\
 p_S&:=\frac{B_0(S)+B_1(S)}{A(S)}
      =\alpha^{(4)}_{S,0}+\alpha^{(4)}_{S,1}>0,\\
 t_S&:=\frac{B_0(S)^2+B_0(S)B_1(S)+B_1(S)^2}{A(S)^2}\\
    &=(\alpha^{(4)}_{S,0})^2
      +\alpha^{(4)}_{S,0}\alpha^{(4)}_{S,1}
      +(\alpha^{(4)}_{S,1})^2>0.
 \end{split}
 \tag{5}
\]

In particular d_S=A(S)(alpha^(4)_{S,0}-alpha^(4)_{S,1}). Strict locality
gives d0=0. The accepted RI127 core theorem gives d7>0, because b0>b1.
No sign for d1 or d3 is assumed. Here d3 refers to the initial-pair ideal
mask3; it is not the positive core difference D3.

Use Delta=record1-record0. Complete row normalization and the accepted
actual H5 formulas give, with all four stem ideals still present,

\[
 \begin{split}
 \Delta c&=\sum_Sd_S,\\
 \Delta h&=\theta\sum_Sd_S,\qquad
 \Delta m=\theta^2\sum_Sd_S,\\
 \Delta j&=\theta\sum_Sd_S(p_S-2),\\
 v=\Delta V&=\theta\sum_Sd_S
                   [p_S+2\theta-2-\theta^2t_S],\\
 D_3&=\theta^3d_7t_7>0.
 \end{split}
 \tag{6}
\]

For clarity, j_i=1-theta sum B_i(S)^2/A(S)-2theta c_i and
V_i=theta^3 sum B_i(S)^3/A(S)^2+2theta^2 c_i+j_i. Factoring each square
and cube difference yields (6); no numerical difference or coefficient
has been formed. All four C3 entries are needed for the identities before
the exactly zero empty contrast is recognized.

Substitute (6) into RI145's accepted q residual. Define

\[
 \begin{split}
 \mathcal H_S&:=p_S+2\theta-2-\theta^2t_S,\\
 \mathcal F_S(x)&:=(4-2\theta-2x)p_S
   -\theta^2(1-\theta x^2)t_S\\
 &\hspace{12mm}+5\theta-6+(4-2\theta)x-\theta^2x^2.
 \end{split}
 \tag{7}
\]

Then the exact full contrast is

\[
 q(x)=\theta\sum_Sd_S\mathcal F_S(x)
                +N_0k_0(x)-N_1k_1(x),
 \qquad
 k_i(x):=2-x-2\omega_i+\theta x^2\omega_i^2,
 \tag{8}
\]

where omega_i=G_i(1)/B_i(1)=theta B_i(1)/A(1). The sign in the last
term is record0 minus record1: RI145's original expression is
(x-2)Delta N+2Delta(N omega)-theta x^2 Delta(N omega^2).
This convention is consistent with d_S, not with Delta.

As a manual coefficient check, the coefficient of p_S in the sum is
(1-theta x^2)+(3-2theta-2x+theta x^2)=4-2theta-2x. The remaining
constant part collects to 5theta-6+(4-2theta)x-theta^2x^2; the cubic
difference contributes -theta^2(1-theta x^2)t_S. This independently
reconciles (8) with the previously accepted residual formula.

## 5. Positive singleton factors without dropping their correlation

The complete unique-maximum C5 proper-potential sum is the complete C4
row sum1. Thus M5>=1 and theta<=1/144. Strict B_i(1)<1 with A(1)=1/44
gives

\[
 0<\omega_i<11/36.
 \tag{9}
\]

The main synthesis strengthens theta to a strict inequality using a
different complete parent; this section only needs the weaker bound
just proved. Neither calculation evaluates M5 or a coefficient.

Put beta_i=B_i(1)>0 and delta_kappa=kappa0-kappa1. The symbol beta_i in
this section is a held singleton probability, not RI127's local pivot.
Difference-of-squares and difference-of-cubes factorization gives

\[
 \begin{split}
 N_0k_0-N_1k_1
   &=\kappa_0d_1 h_*(x)
        +\delta_\kappa\beta_1 k_1(x),\\
 h_*(x)&:=2-x-2\theta p_1+\theta^3x^2t_1.
 \end{split}
 \tag{10}
\]

This identity keeps the joint occurrence of beta_i in N_i and omega_i.
It does not replace DeltaN by an unrelated nonnegative parameter. It is
also valid when either kappa is zero or when beta0=beta1; no such quantity
was divided by to obtain it.

For every 0<=x<=1/4, the bounds in (9) give

\[
 \frac{41}{36}<k_i(x)<2,\qquad
 \frac{19}{36}<h_*(x)<2.
 \tag{11}
\]

For the lower bounds, retain the nonnegative quadratic terms, use
2-x>=7/4, and use theta p1=omega0+omega1<11/18. For the upper bounds,
k_i'(x)=-1+2theta x omega_i^2<0 and
h_*'(x)=-1+2theta^3x t1<0; both values at x=0 are strictly below2.
The last derivative uses theta^3t1=theta(omega0^2+omega0omega1+omega1^2)<1.

There is also a useful exact order implication. At fixed theta, A(1),x,
write omega=theta beta/A(1). Differentiating the polynomial beta k(omega)
with respect to this formal beta argument gives

\[
 (2-x)-4\omega+3\theta x^2\omega^2>19/36
 \quad(0<\omega<11/36,\ 0\le x\le1/4).
 \tag{12}
\]

This derivative is a polynomial identity and sign proof, not parameter
fitting or a variation of the actual law. Thus for fixed kappa>0 the
function kappa beta k is strictly increasing in beta, and for kappa=0 it
is identically zero. Equation (10) consequently gives a nonnegative
singleton residual if both actual inequalities beta0>=beta1 and
kappa0>=kappa1 hold; the opposite pair gives a nonpositive residual.
These are conditional implications only. Neither pair of orderings is
established for the unchanged actual coefficients by this note.

The main synthesis records a valid signed-part lower bound using (11),
including all zero cases. It does not assert that this lower bound is
positive. Nothing here permits replacing a negative d1 or delta_kappa by
zero or reversing its multiplication inequality.

## 6. Exact sensitivity ratios and the remaining actual premise

Since d7>0, define only the two signed relative contrasts

\[
 \gamma_1:=d_1/d_7,\qquad \gamma_3:=d_3/d_7.
 \tag{13}
\]

For example gamma1=A(1)(alpha^(4)_{1,0}-alpha^(4)_{1,1}) /
[a(alpha^(4)_{7,0}-alpha^(4)_{7,1})]. This is a fixed relation among
the actual component entries, not permission to choose gamma freely.

Equations (6)--(10) give

\[
 \boxed{\frac v{D_3}
  =\frac{\mathcal H_7+\gamma_1\mathcal H_1
                       +\gamma_3\mathcal H_3}{\theta^2t_7}},
 \tag{14}
\]

\[
 \boxed{\begin{split}
 \frac{q(x)}{D_3}
  =\frac1{\theta^2t_7}\left[
   \mathcal F_7(x)+\gamma_3\mathcal F_3(x)
   +\gamma_1\left(\mathcal F_1(x)
                         +\frac{\kappa_0}{\theta}h_*(x)\right)
   +\frac{\delta_\kappa\beta_1}{\theta d_7}k_1(x)\right].
 \end{split}}
 \tag{15}
\]

All denominators in these identities are named positive quantities.
Gamma1, gamma3 and delta_kappa can be zero or signed; no division by any
of them is used. Positivity of the underlying probabilities does not make
their contrasts positive. The accepted signs v>0 and q>0 ensure that the
respective complete numerators are positive on their accepted domain,
but by themselves do not prove a specified positive lower magnitude.

Specifically, a proposed positive lower bound v/D3>=a_v is equivalent to
the actual component dominance comparison

\[
 \mathcal H_7+\gamma_1\mathcal H_1+\gamma_3\mathcal H_3
                   \ge a_v\theta^2t_7.
 \tag{16}
\]

A uniform bound q(x)/D3>=a_q on an actual-containing interval is the
corresponding comparison of the full bracket in (15) with a_q theta^2t7
for every x in that interval. The main synthesis isolates this equivalently
as an inequality on the actual delta_kappa, dividing only by beta1 k1>0;
the scale-side note states the joint compensation budget these bounds
would have to meet. No fitted a_v or a_q is supplied here.

This pinpoints what remains to be proved from the fixed C4 component
vector and fixed C5 canonical solution. Nonnegativity of the canonical
coordinates, distinct component identities, the lexicographic definition,
and the accepted positive sign of the entire expression are not themselves
proofs of (16) or its quantitative q counterpart. This statement concerns
the present derivation; it is not a theorem that no further analytic proof
from those fixed objects exists.

No freely chosen coefficient example is offered as a counterexample to
the actual law. No formal x is selected as actual rho. The new parent-wise
M6 bounds and actual-scale enclosure in the companion proof must still be
combined with a proved adequate sensitivity budget; this note does not
close that comparison or rerun RI145's small-x theorem.

## 7. Exact read scope and manual checks

New source reads in this contribution were complete, through EOF:

- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/check.py`
  (312 lines): every definition, fixed input load, component construction,
  direct row construction and entry path read as text only.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/check.py`
  (1172 lines): every definition, prefix pin and literal tables, canonical
  component proof, actual mixture, controls and entry path read as text only.
- `/Volumes/AI_DATA/development/det-review-evidence/ri146-root-current-capture-9bfi4u8s/NATIVE_SUCCESSOR_RESERVATION.json`:
  administrative RI147 assignment.
- `/Volumes/AI_DATA/development/det-review-evidence/ri146-root-current-capture-9bfi4u8s/RI145_ROOT_ADJUDICATION.json`:
  administrative acceptance and remaining actual-scale gap.
- `/Volumes/AI_DATA/development/det-review-evidence/ri147-native-scale-membership-q4lxbpke/SCALE_MEMBERSHIP_SYNTHESIS.md`:
  complete current author text read for algebraic integration, not historical
  acceptance or independent review.

Complete reads from this author's immediately preceding RI145 work are
reused as accepted textual premises, without claiming a fresh full read:

- `/Volumes/AI_DATA/development/det-review-evidence/ri145-native-weighted-margin-proof-zo96x_ci/ENDPOINT_REDUCTION.md`:
  accepted complete q residual and held coefficient identities.
- `/Volumes/AI_DATA/development/det-review-evidence/ri127-connected-compensation-nMyz57P5/DECISION_CONTRACT.md`,
  `LOCAL_POSITIVITY.md`, and `RECORD_TRANSPORT.md` in that same directory:
  accepted native signs, full transported records and fixed actual baseline.
- `/Volumes/AI_DATA/development/det-review-evidence/ri128-connected-sign-dvgWLqqv/INPUT_FORMULAS.md`
  and `ANALYTIC_BOUNDS.md` in that same directory: complete formulas, fixed
  scientific domain and actual-containing interval.
- `/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn/ANALYTIC_PREFIX_LEMMAS.md`
  and `F2_ANALYTIC_CHECK.md` in that same directory: all H5 stem entries,
  C5 singleton exception, complete full complements and exact N definition.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md`
  and `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md`:
  fixed component rule, strict canonical mixture and normalized complete rows.

The current RI145 main proof was additionally searched as text for relevant
component passages; that targeted search is not claimed as a fresh complete
read. Its literal path is
`/Volumes/AI_DATA/development/det-review-evidence/ri145-native-weighted-margin-proof-zo96x_ci/WEIGHTED_MARGIN_PROOF.md`.

The displayed literal source tables were not converted to selected actual
coefficient values or newly instantiated probabilities. No scientific
CERTIFICATE.json, ri88.json, saved probability body, canonical alpha body,
maximum, scale, H/z or polynomial coefficient instance was decoded or
evaluated. The published and external paths remain distinct literal
dependencies even if some source bytes match.

Manual checks covered the unique-maximum potential reduction, actual
coefficient correlation, terminal/root-bit invariant and exclusion of an
empty-precursor path, square/cube contrast signs, every coefficient in
(8), zero-safe factorization (10), endpoint-valid factor bounds (11),
monotonicity derivative (12), positive clearing of both ratios, and the
remaining-premise interpretation. The current main synthesis was separately
read in full and its singleton factors, signed-part floor and target
delta_kappa equivalence checked; no concrete algebra or scope defect was
found. This is author-peer integration, not independent acceptance.

Only this Markdown is authored. All 31/139/20/42 runtime obligations, fixed
seed/amplitude/support, shared T1 recovery, eight other connected parents,
all five Di systems and strict inequalities remain. Actual W, C2/C3 and
simultaneous H30 feasibility remain unresolved. Repository/index/Git,
predecessor packets, RET, measurement, controllers, cards and runtimes are
unchanged. No geometry, mass/gravity, physical or full-QM promotion follows.
