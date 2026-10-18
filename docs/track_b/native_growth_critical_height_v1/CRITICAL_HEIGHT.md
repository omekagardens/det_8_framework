# RI-72 — minimum height with critical-child suppression retained

24 September 2026 UTC. **Independently accepted after coordinator adjudication.**
This is a bounded secondary-objective calculation on the original RI-63
primary-optimal face, followed by a conditional all-size existence and
suppression argument. It does not adopt a selector or change the actual
RI-59/61/63 canonical law, its first-free transition layer, or its histories.

## 1. The slice, not a new primary problem

Retain every original cap, all 798 components and the actual inherited
parent-five marked-history weights. With the existing exact matrix and
coefficients, the primary-optimal face is

\[
 K_* = \{\alpha\geq0:A\alpha\leq\mathbf1,\quad
              \beta\cdot\alpha=b\},\qquad
 b=-\frac{1512652301}{37480960000}.
 \tag{1}
\]

There are 1,490 canonical marked-row caps; they retain the multiplicities of
11,424 raw marked histories and 142,944 labeled proper ideal occurrences.
The primary defect optimum is unchanged:
`m_5=6650803/108900000`. A component's zero primary coefficient does not
make its transition probability or its height effect zero.

For a finite order Q, call it **critical** when it has at least two maxima
and

\[
 \delta(Q-v)=\delta(Q)-1
       \quad\hbox{for every maximal }v.
 \tag{2}
\]

Here δ is the existing arbitrary-vertex-deletion Ferrers defect, not an
ideal-only diagnostic. A proper component has one intrinsic terminal
order type, while marks can split one terminal type into several components.
Let S be precisely the set of components with critical terminal order. The
new slice is

\[
 K_*^{\mathrm{crit}}
       =K_*\cap\{\alpha_c=0:c\in S\}.
 \tag{3}
\]

These are the only added coordinate equalities. There is **no** extra zero
or positivity requirement on noncritical components: they may be zero or
positive. In particular, imposing zero on every β=0 component would solve
a different problem. Criticality in (2) concerns the **child/terminal**,
not a stored flag saying its parent is critical.

All critical-terminal proper births raise defect; their full alternatives
raise it by either zero or one. Therefore

\[
 \beta_c=\sum_{j,S':c(j,S')=c}
       \pi_j u_j(S')\,[1-f_j]\geq0
       \quad(c\in S).
 \tag{4}
\]

The retained canonical vector zeros all β≥0 coordinates and is already in
(3), proving nonemptiness without a feasibility search. At this layer S
has **347 components**, covering **78 terminal types**: 285 have β>0 and
62 have β=0. There are 32,032 critical-terminal labeled proper occurrences
in the raw marked domain; all 200 noncritical β=0 components remain legal.
Their critical component-list digest is
`524a108094d29dc3ff5beee6104eafcece1a54154958ac89b001b1493b29b33d`.

The existing height objective is the expected **one-birth height increment**
at these fixed parent-five weights, not total height or an asymptotic rate:
write P+S' for adjoining one new maximal vertex whose strict past is the
ideal S' (not the union of P with its already-present subset S').

\[
 H(\alpha)=1+\kappa\cdot\alpha,\qquad
 \kappa_c=\sum_{j,S':c(j,S')=c}
        \pi_j u_j(S')\,[h(P_j+S')-h(P_j)-1].
 \tag{5}
\]

The full birth supplies the unit baseline. All 798 existing κ are retained.
Minimize (5) on (3); do not impose the old canonical tie-break on that face.

## 2. Exact bounded outcome

The restricted minimum is

\[
 \boxed{H_{\min}^{\mathrm{crit}}
        =\frac{2982979886099966479}{3173270486335488000}
        \simeq0.940033287091366.}
 \tag{6}
\]

The following comparisons use the **same** original inherited distribution:

| Boundary vector or value | Exact expected height increment | Critical-child entry mass |
|---|---|---|
| RI-70 unrestricted minimum | 69729502462340410231/79331762158387200000 | 6650803/108900000 |
| RI-72 restricted minimum | 2982979886099966479/3173270486335488000 | 0 |
| Retained canonical vector | 25799901101980099/26711031029760000 | 0 |
| Retained alternative vector | 10372327938670249993/10639712319160320000 | 0 |
| RI-70 unrestricted maximum | 330159038233/337328640000 | 0 |

Thus the cost of enforcing critical-child suppression at this one layer is

\[
 H_{\min}^{\mathrm{crit}}-H_{\min}
       =\frac{6650803}{108900000}=m_5,
 \quad
 H_{\mathrm{canonical}}-H_{\min}^{\mathrm{crit}}
       =\frac{410241824076346411}{15866352431677440000}>0.
 \tag{7}
\]

The numerical equality to m_5 is a certified finite-layer identity, not a
general height/defect formula. Height can be reduced relative to the
canonical completion while preserving both its primary optimum and its
zero boundary critical-entry mass.

The RI-70 minimum's six positive critical-terminal coordinates are 566–571.
All have β=0 and terminal type 241, represented by
`(0,1,1,7,7,7)`, of defect two. The other 64 positive β=0 coordinates of
that witness are noncritical. The restricted height-minimizing vector is
nonunique, as shown below. The displayed vector is not claimed to be the
hypothetical lexicographically selected minimizer.

There is also a direct attaining construction, without another search:
erase those six coordinates from the old minimum. All caps relax, the
primary objective is unchanged, and all critical coordinates become zero.
For that terminal type κ/U=-1: its height is three and every maximal
deletion preserves that height. Erasure therefore raises H by precisely
the removed probability mass, giving (6). It reroutes those
height-preserving, defect-raising proper births into full complements.
The new exact dual proves that this price is unavoidable on (3); erasure
alone would prove only a feasible upper bound. The erased vector differs
from the new numerical witness. Two distinct attaining vectors therefore
prove nonuniqueness, without identifying the final lexicographic selection.

Critical entry is computed as the complete raw marked-row probability,
equivalently \(\sum_{c\in S}U_c\alpha_c\). Both newborn bits are included;
there is no extra orbit or deletion multiplicity. This is not the primary
objective contribution \(\sum_{c\in S}\beta_c\alpha_c\), which is zero for
the six critical zero-cost coordinates even when their entry mass is positive.

Strict mixing reintroduces critical-child probability. At the common fixed
prefix, every vector in (3) has the same strictly mixed critical-entry mass

\[
 \Gamma_5=\frac{
 3972146365710155348353002408889790040486116794799475977}{
 143814339078313825258549631166275054109317991394923931238400}.
 \tag{8}
\]

It is \(\eta_5c_5\sum_{c\in S}U_c\), with \(\eta_5=1/36\).
For the unrestricted minimum the corresponding counterfactual mass is
\(\Gamma_5+(35/36)m_5\). Counterfactual fixed-prefix mixtures are comparisons,
not changes to the actual transition law.

## 3. Exact certificate on the original constraints

[CERTIFICATE.json](CERTIFICATE.json) records a rational primal α, nonnegative
row multipliers y, a free primary-face multiplier λ and free coordinate
multipliers μ supported only on S. [check.py](check.py) requires

\[
 \begin{aligned}
 &\alpha\geq0,\quad A\alpha\leq\mathbf1,\quad
       \beta\cdot\alpha=b,\quad \alpha_S=0,\\
 &y\geq0,\quad
       g:=\kappa+A^Ty-\lambda\beta-\mu_S\geq0,\\
 &\kappa\cdot\alpha=-\sum_jy_j+\lambda b.
 \end{aligned}
 \tag{9}
\]

All 1,490 original row inequalities and all 798 original dual columns are
checked with exact fractions. The new zero equalities have zero right-hand
side, hence do not add to the dual objective. Their multipliers can have
either sign; imposing μ≥0 would be unjustified.

For any feasible γ in (3),

\[
 \kappa\cdot\gamma
  =g\cdot\gamma-y\cdot A\gamma+\lambda b
  \geq-\sum_jy_j+\lambda b.
 \tag{10}
\]

Equality at the supplied α certifies (6), independently of numerical solver
status. Exact complementarity and the claimed height are checked as well.
The witness has 134 positive primal coordinates (63 with β=0), 160
positive row multipliers, 346 nonzero critical-equality multipliers
(318 positive and 28 negative), and λ=-19/4. There are 808 tight original
caps and 532 zero reduced columns after adding the coordinate multipliers.

Accepted dependency bytes and the entire derived problem are pinned.
The new critical classification uses intrinsic orders and all maximal
deletions, not parent flags. The verifier also preserves the raw marked
history and labeled slot multiplicities and compares the retained witnesses.
It is a certificate checker, not a new optimization executor.

### Declared discovery envelope and one search

Before discovery, this packet declared at most **one** numerical endpoint
search: 1,800 seconds, 2 GiB resident memory, one solver worker, existing
packages, no second objective, Pareto sweep or higher-layer optimizer.
Enforcement is by a wall alarm and resident-memory checkpoints/sampling,
not a hard OS allocation cap; instantaneous unsampled overshoot is not
excluded. Existing helper bounds remain in force.

Exactly one HiGHS dual-simplex call ran through the already available
SciPy 1.16.3 / NumPy 2.3.5 under CPython 3.12.14. The existing primary
complementarity reduction left 216 columns, including 104 with β=0, and
76 forced cap rows. Of the unrestricted reduced face's 256 columns, only
the 40 critical-terminal columns were removed; no noncritical zero-cost
column was removed by the new restriction.

The solver used 115 iterations. Exact rational active-system recovery had
full ranks 134/134 for the primal and 149/149 for the reduced dual;
backlifting, including the free critical-equality multipliers, produced
(9). The discovery body took 6.347 seconds with checkpoint peak
183,386,112 bytes; the outer process took 8.006 seconds with sampled peak
183,140,352 bytes. No second numerical search was performed.

Predeclared refusal cases include changed inputs, wrong terminal-critical
classification, confusion with parent flags, forbidden coordinates,
original cap or face violations, malformed dual signs, original-column
infeasibility, nonzero exact gap, wrong height and dropped marked/labeled
multiplicity. The final checker has 17 reason-specific refusal controls;
it also replays the 14 accepted RI-70 controls and inherited RI-63 checks.

### Verification evidence and identities

The final standard-library checker passes under both normal and optimized
CPython 3.14.0; correctness does not depend on removable Python assertions.
The root's normal/-O replays took 18.343/18.296 seconds, with sampled
resident peaks 129,662,976/130,383,872 bytes. Their stdout is identical:
3,870 bytes, SHA-256
`030b7776031c48b6b5c079b2aff5a560330ca61bb79782c42f3892b93f92c4b9`.
Their progress stderr is also identical: 1,484 bytes, SHA-256
`350ab3783d4d1905c6ef38a9f7b126b84438cd6721fd136e17e3b1645f8419ed`.

Final machine-readable identities:

- Checker: 507 lines, 27,648 bytes, SHA-256
  `4b26bbd7e56c87aff939cf562ac5b11febe0a5402e7b3f5dd3734a4e2df96ef4`.
- Certificate: 663 lines, 24,074 bytes, SHA-256
  `31e485b31163bf1b42e7149f32e0249d160c527e85bb93d2cb083059ea6b1a76`.
- Reconstructed problem:
  `5d93b2d8bc05873a83d7161ecc1fca3a9e8f55ca3d6de07519bff2b1776e423c`.

Coordinator publication removed one extra final newline from the handoff
certificate (24075 bytes, SHA-256
`1d5a67f9926d4136569fc790bf57dd47a3f8040fe39d5363fc0508f9084d8956`).
Parsed certificate data are identical; the identities above describe the
publication bytes. Coordinator replay evidence is in the progress record.

A separate root audit did not call the new checker or an optimizer. It
reconstructed RI-63, used direct arbitrary-subset height and defect tests
on 4,824 orders, independently classified all raw terminal occurrences,
and checked every original cap/dual column, the signed multipliers, exact
gap and complementarity. It confirmed the full 11,424/142,944 raw marked
row/slot coverage, critical mass and the direct erased witness. It took
8.871 seconds with checkpoint peak 205,570,048 bytes. The two attaining
primal vectors differ in 64 coordinates. No numerical search was used in
any of these replay/audit checks.

The checker author's independent normal/-O replays passed in
18.427/18.216 seconds, sampled peaks 128,499,712/130,973,696 bytes.
A separate reviewer's normal/-O replays passed in 18.184/18.479 seconds;
those used checker resource checkpoints and an outer timeout, not a separate
RSS sampler. All six final runs produced the same stdout identity above
with unchanged source/certificate pins. That reviewer also performed a
separate exact candidate audit in 6.172 seconds, checkpoint peak
115,834,880 bytes, reproducing all constraints, raw multiplicities, signed
multipliers, the erased comparison and the strict entry bound Γ_5<1/72.

Two independent proof/source reviewers found no substantive blocker.
Their clarifications made the birth notation, nonuniqueness, weaker
zero-cost suppression and prospective own-history recursion explicit.
These are exact finite certificates and human-readable mathematical
proof reviews, not theorem-prover formalization. Scoped links, whitespace
and conflict-marker checks are clean; the directory contains only the
three assigned files.

Reproduce the complete certificate check from the repository root with
`python3 -I -S -B docs/track_b/native_growth_critical_height_v1/check.py`,
and add `-O` before the file path for the optimized replay. `--problem`
exports the pinned reconstructed metadata instead of checking the endpoint.

## 4. Prospective all-size existence under its own history law

This is a **conditional alternative construction**, not an adopted law or
a DET-native derivation. Retain the existing chosen finite-order/mark
architecture, complete scalar-diamond solution, rational fixed prefix,
component ordering and strict mixing rule. Suppose inductively that the
prospective prefix is strict, rational and covariant. Rebuild the complete
history distribution π_n, potentials u_n, caps, β_n and κ_n from **that
prospective prefix**, including every marked counterfactual history.

First find the original primary optimum b_n of that layer. Add the
critical-terminal zero equalities only on its primary-optimal face; then
minimize its height increment and finally minimize successive coordinates
in the existing complete canonical component order. This defines the
prospective boundary vector \(\widehat\alpha_n\).

Existence does not require accepting the actual old law's later tables.
Every coordinate occurs in a positive row cap, so the feasible polytope
is nonempty, bounded and rational. A critical-terminal component has
β≥0 by (4). Every primary minimizer already zeros β>0 coordinates:
reducing a positive such coordinate would relax caps and strictly lower
the primary objective. Its critical β=0 coordinates can also be zeroed
without changing that objective or violating caps. Therefore the
restricted primary-optimal slice is nonempty.

The secondary linear minimum is attained on a nonempty compact rational
face. Successively minimizing all finitely many canonically ordered
coordinates leaves a unique rational vector. This proves existence of a
lex-completed selector, not efficient computation at arbitrary size.
The finite certificate (9) proves an optimal value and an attaining
vector; it does **not** prove the supplied vector is the lex-selected one.
Any lex-completed secondary minimizer at the shared first-free prefix
has height (6), but its coordinates need separate certification. No such
lexicographic solver ladder was run.

Use precisely the existing mixture

\[
 \eta_n=(n+1)^{-2},\quad
 M_n=\max_j\sum_{S'\subsetneq P_j}u_j(S'),\quad
 c_n=\frac1{2(1+M_n)},\quad
 \alpha_n=(1-\eta_n)\widehat\alpha_n+\eta_nc_n\mathbf1.
 \tag{11}
\]

Every proper slot is positive; each full complement is greater than
η_n/2. These rational probabilities generate the next prospective
positive rational history distribution, closing the finite-layer
induction. These normalized consistent finite-history kernels define the
ordinary infinite-history probability measure. Shared parent-five histories justify (6) for that first
alternative completion. Later π_n, u_n, b_n and objectives generally
differ from those of the retained actual law and must not be interchanged.

### Locality and covariance are retained conditionally

Selection uses the complete counterfactual row table once per layer,
not a new optimization conditioned on an actual unread marking. Runtime
proper probabilities remain functions of the allowed quotient node
`[P,S',r|S']`: the whole unmarked parent and the precursor's marks,
with one common scale per complete scalar-diamond component. The full
complement may read the full parent record. Intrinsic terminal criticality,
height and defect are invariant under relabeling; the existing canonical
component order is likewise transported consistently. Equal-precursor
and loop constraints and complete marked diamonds remain included.

Consequently this selection and its common-component strict mixture
preserve the inherited locality/covariance identities. The existing fair
newborn marking and passive quantum payload are unchanged; no informative
quantum coupling or new Hilbert-space derivation is introduced.

## 5. Critical suppression, and exactly what does not transfer

Let C denote class (2), and consider the prospective probability space
just constructed. A full birth has a unique maximum, so cannot enter C.
All proper components ending in C have boundary scale zero. For every
complete parent history of size n≥5,

\[
 \Pr(P_{n+1}\in C\mid\mathcal F_n)
   =\eta_nc_n
       \sum_{S':P_n+S'\in C}u_n(S')
   \leq\frac{\eta_nM_n}{2(1+M_n)}
   <\frac{\eta_n}{2}.
 \tag{12}
\]

The sum is over labeled proper ideals in that parent; both newborn bits
are already included. Thus

\[
 \mathbb E\sum_{n=5}^{\infty}\mathbf1_{P_{n+1}\in C}
     \leq\frac1{10},
 \qquad
 \mathbb E\!\left[
  \sum_{n=m}^{\infty}\mathbf1_{P_{n+1}\in C}
          \mid\mathcal F_m\right]\leq\frac1{2m}
          \quad(m\geq5).
 \tag{13}
\]

The conditional probability of any such future entry has the same upper
bound. The predictable sum of entry rates has the deterministic
pathwise bound obtained from (12). The **realized integer count** does
not have a pathwise bound of 1/10: it is finite almost surely and has
expectation at most 1/10. No independence assumption is needed.

Occupation of critical parents at sizes ≥6 is the preceding entry
event, so its expected total is at most 1/10 and it is finite almost
surely. Any nonnegative boundary/actual row drift bounded by one and
supported on those parents inherits this summability. Including parent
size five adds the separate fixed-prefix term \(\Pr(P_5\in C)\);
it is not controlled by the new tail schedule.

Primary optimality still suppresses β>0 coordinates. After the height
objective is added, noncritical β=0 coordinates are **not generally forced
to vanish**; individual such coordinates may still be zero.
Therefore RI-61's stronger suppression theorem for **all** β≥0 components
does not transfer wholesale. No claim here removes the noncritical
raising-role or full-complement drift. Critical suppression alone does
not establish sublinear defect, balanced height or any geometric limit.

## 6. Scope and handoff

Only this note, the exact checker and its certificate belong to this
packet. There is no change to accepted sources, RET, measurement,
coordinator ledgers, the actual canonical law or its quantum payload.
No higher-layer optimization, second endpoint search, Pareto sweep or
lexicographic search is authorized by this calculation.

The results are a stricter finite minimum and a conditional all-size
existence/suppression theorem for an unadopted selector. They do not
establish a DET-native quantum reconstruction, manifoldlike geometry,
mass, clocks, gravitational dynamics or an empirical discriminator.
Option B and metric-as-record Status M are unchanged.

Exact verification and independent source/proof review have passed.
This is the stable three-file handoff; the worker stops here. Coordinator
adjudication, publication and any successor assignment remain separate.
