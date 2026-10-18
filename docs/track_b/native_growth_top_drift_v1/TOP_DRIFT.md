# RI-69 — universal-top geometry and an amortized full-birth charge

24 September 2026 UTC. **Exact all-size identities and conditional drift bound;
independently accepted after coordinator adjudication.**
This packet retains the same RI-59 candidate, strict prefix, objective,
canonical tie-break and mixture schedule. Only this note, `check.py` and
`CERTIFICATE.json` in this directory are assigned. Accepted sources, ledgers,
measurement, RET and git/index operations are out of worker scope.

## Predeclared computation envelope

Each attempt is limited to 900 seconds and 2 GiB resident memory, enforced
by a wall-time alarm and sampled/checkpoint RSS checks, not by a hard operating
system allocator limit. Unobserved instantaneous overshoot is not excluded.
No threshold will be weakened after a failure. Computation uses exact standard
library arithmetic, byte-pinned accepted helpers and only concrete orders of
size at most six. No size-six-parent optimizer, probability law beyond the
accepted parent-five layer, or blanket seven-event atlas is permitted.

## 1. Intrinsic diagnostics and unchanged premises

Keep the full [RI-59 candidate](../native_growth_expected_defect_v1/EXPECTED_DEFECT.md),
including every ideal, strictly positive inherited prefix, complete binary
marks, precursor-record locality, marked equivariance and full scalar-passive
maps `q(S) D/2` on the entire unnormalized payload. No new law, objective,
canonical order, mixture coefficient or informative quantum coupling is added.

For a finite unmarked order P define:

- `F(P)`: largest cardinality of an arbitrary **induced** Ferrers suborder;
- `h(P)`: longest-chain cardinality, with `h(empty)=0`;
- `R(P)`: largest cardinality of an induced rectangle-minus-greatest suborder.

A rectangle means a product of two nonempty finite chains. Deleting its
greatest vertex gives a Ferrers down-set. The punctured `1 x 1` rectangle is
empty, and punctured one-dimensional rectangles include every finite chain.
These conventions make R defined even for the empty order and give

\[
 0\le h(P)\le R(P)\le F(P),\qquad
 \delta(P)=|P|-F(P),\qquad V(P)=F(P)-h(P)\ge0. \tag{1}
\]

R here is a combinatorial diagnostic, not the record variable. No vertices
or records are removed from the actual process. All subsets in these maxima
are arbitrary induced subsets, not just ideals or maximal deletions. Ferrers
coordinates describe isomorphism types; they are not supplied metric inputs.

Write `P+top` for adding a new greatest vertex, and `P+chain_k` for adding k
successive universal tops. The old P is an ideal of the result. No birth
probability is inferred from this counterfactual sequence.

## 2. Exact universal-top geometry

**Theorem.** For every finite P and every integer k>=1,

\[
 F(P+\mathrm{top})=\max\{F(P),1+R(P)\}, \tag{2}
\]
\[
 \boxed{F(P+\mathrm{chain}_k)
 =\max\{F(P),1+R(P),h(P)+k\}.} \tag{3}
\]

For (2), a retained Ferrers subset omitting the new top has at most F(P)
vertices. If it contains that top, its Ferrers diagram has a greatest element
and is therefore a rectangle: downward closure fills the rectangle below
that greatest cell. Removing the new top leaves an induced punctured rectangle
in P, of size at most R(P). Both bounds are attained by their defining
maximizers, respectively without and with the top.

For (3), classify an arbitrary retained Ferrers subset by how many added tops
it contains. None gives the F(P) bound; exactly one gives the `1+R(P)` bound.
If it contains at least two, its greatest vertex has a **unique coatom**, the
second-highest retained added vertex, above all remaining retained vertices.
A nonchain rectangle has two coatoms, one in each coordinate direction.
The retained rectangle must therefore be a chain, of size at most `h(P)+k`.
Conversely an old longest chain plus all k new tops attains this last bound.
This proof permits skipped old vertices and skipped added tops throughout.

Also, for k>=1,

\[
 R(P+\mathrm{chain}_k)=\max\{R(P),h(P)+k\}. \tag{4}
\]

Indeed, a retained punctured nonchain rectangle has two maximal vertices,
so cannot contain an added top: the highest retained added vertex would be
greatest in that subset.
A retained punctured rectangle containing an added top must instead be a
chain. The same old-subset and longest-chain constructions attain the bounds.
The empty-parent cases in (2)–(4) are included.

## 3. Raising, total streak charge, and permanent quenching

Let `F=F(P)`, `h=h(P)`, `V=F-h` and `a=1_{R(P)=F(P)}`. Since R<=F and
both are integers, (2) yields

\[
 \delta(P+\mathrm{top})-\delta(P)=1-a,
 \quad\text{so a full birth raises defect iff }R(P)<F(P). \tag{5}
\]

For k>=1, equations (2)–(3) give

\[
 F(P+\mathrm{chain}_k)=\max\{F+a,h+k\},
\]
\[
 \boxed{\delta(P+\mathrm{chain}_k)-\delta(P)
            =\min\{k-a,V\}.} \tag{6}
\]

For k=0 the increment is zero; a single formula for all k>=0 replaces
`k-a` in (6) by `max(0,k-a)`. An uninterrupted infinite full-top streak
therefore adds exactly V defect in total. Equivalently its remaining V is
`V-min(V,max(0,k-a))`.

The precise pattern is:

- If R<F, then V>=1: births 1 through V raise; all later tops are neutral.
- If R=F and V>0: birth 1 is neutral, births 2 through V+1 raise, and all
  later tops are neutral.
- If V=0, every full birth is neutral from the start.

Thus the **minimal** number of added tops after which every future full birth
is neutral is `V+a` when V>0 and zero when V=0. The first neutral top need
not be permanent quenching. For k>=1 this also follows by comparing (3) and
(4): future quenching occurs exactly when `h+k>=F+a`.

The three-cell punctured `2 x 2` rectangle is the fork `(0,1,1)`. It has
`F=R=3`, `h=2` and V=1. Its next three full births give:

| Added tops | Size | F | h | Defect | V | New defect increment |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 3 | 3 | 2 | 0 | 1 | — |
| 1 | 4 | 4 | 3 | 0 | 1 | 0 |
| 2 | 5 | 4 | 4 | 1 | 0 | 1 |
| 3 | 6 | 5 | 5 | 1 | 0 | 0 |

This is a neutral → raising → permanently neutral counterexample to the
claim that the first neutral full birth guarantees all later ones are neutral.

## 4. A pathwise accounting identity for arbitrary births

For any eligible maximal birth, RI-56 gives `d=Delta delta in {0,1}`.
Likewise `z=Delta h in {0,1}`: a longest chain gains at most the newborn,
and all old chains remain. Since F is size minus defect,

\[
 \Delta V=1-d-z\in\{-1,0,1\}. \tag{7}
\]

A full birth always has z=1, hence `Delta V=-d`. Positive change in V occurs
only at a **proper**, defect-neutral birth with no height increase. Call this
one unit of recharge; it is accounting terminology, not a physical energy.

Along an actual history let Y_n indicate a defect-raising full birth, G_n
indicate a proper birth with `(d,z)=(0,0)`, and K_n indicate a proper birth
with `(d,z)=(1,1)`. Every birth satisfies

\[
 V_{n+1}-V_n=G_n-K_n-Y_n.
\]

Consequently, for every finite N>=5, pathwise,

\[
 \boxed{\sum_{n=5}^{N-1}Y_n
 =V_5+\sum_{n=5}^{N-1}G_n-\sum_{n=5}^{N-1}K_n-V_N
 \le V_5+\sum_{n=5}^{N-1}G_n.} \tag{8}
\]

The proper negative increments and nonnegative terminal balance are retained
in the identity, not assumed absent. The bound concerns **defect-raising full
births**, not all full births. Raising proper births with no height increase
do not consume V and are not bounded by this argument.

## 5. Boundary expectations under the actual strict prefix

At layer n use the actual strict-prefix history distribution pi_n, exactly
as in RI-59. Its boundary and interior row kernels are `q_n^0` and `q_n^I`;
the actual row kernel is

\[
 q_n=(1-\eta_n)q_n^0+\eta_n q_n^I,
 \qquad\eta_n=(n+1)^{-2}. \tag{9}
\]

No separate boundary-history process replaces pi_n. Define the deterministic
boundary averages `L_n^0`, `G_n^0`, `K_n^0` as the pi_n-weighted probabilities
of the three indicators Y, G, K, evaluated with `q_n^0`. In particular

\[
 L_n^0=\sum_j\pi_j q_j^0(P_j)
               [\delta(P_j+\mathrm{top})-\delta(P_j)]. \tag{10}
\]

Superscript-zero averages are distinct from the realized indicators in (8).
The boundary V drift is `b_n=G_n^0-K_n^0-L_n^0`. Let `a_n=E[V_{n+1}-V_n]`
under the actual law, and let `i_n` be the interior drift averaged under the
same pi_n. By affinity and (7),

\[
 \varepsilon_n=a_n-b_n=\eta_n(i_n-b_n),
 \qquad |\varepsilon_n|\le2\eta_n. \tag{11}
\]

Telescoping the actual, not boundary, V expectation now gives the exact
finite-horizon identity

\[
 \boxed{\sum_{n=5}^{N-1}L_n^0
 =E V_5-E V_N+\sum_{n=5}^{N-1}G_n^0
       -\sum_{n=5}^{N-1}K_n^0+\sum_{n=5}^{N-1}\varepsilon_n.} \tag{12}
\]

Since V and K are nonnegative and
`sum_(n>=5)(n+1)^(-2)<=integral_5^infinity x^(-2)dx=1/5`,

\[
 \boxed{\sum_{n=5}^{N-1}L_n^0
 \le E V_5+\sum_{n=5}^{N-1}G_n^0+2\sum_{n=5}^{N-1}\eta_n
 \le E V_5+\sum_{n=5}^{N-1}G_n^0+\frac25.} \tag{13}
\]

This is an expectation bound, not a pathwise numerical bound on a sum of
boundary hazards. Equation (8) is the separate realized-count statement.

## 6. Intrinsic recharge coefficients and the remaining charged mass

For a proper component c let Q_c be its unmarked terminal type, while retaining
its distinct marked fiber and mass U_c from
[RI-66](../native_growth_terminal_cost_v1/FACTORIZATION.md). For every maximal
v of Q put `P_v=Q-v`, and define

\[
 J_+(Q)=\frac1{e(Q)}\sum_v e(P_v)
      \mathbf1_{\{\delta(Q)=\delta(P_v),\ h(Q)=h(P_v)\}},
\]
\[
 J_-(Q)=\frac1{e(Q)}\sum_v e(P_v)
      \mathbf1_{\{\delta(Q)=\delta(P_v)+1,\ h(Q)=h(P_v)+1\}}. \tag{14}
\]

RI-66's general unmarked role-statistic identity applies to both indicators.
Writing `p_c^0=alpha_c^min U_c`, it gives

\[
 G_n^0=\sum_c p_c^0J_+(Q_c),\qquad
 K_n^0=\sum_c p_c^0J_-(Q_c). \tag{15}
\]

Every labeled maximal-deletion role is counted with e(P_v). No component is
merged because it shares Q with another; no division by a zero allocation
alpha is made. The marked-fiber constants and actual history multiplicities
remain in U_c. The identities also hold for any feasible auxiliary boundary
allocation, though only the unchanged canonical choice is used here.

Let `A={P:delta(P)>0 and P noncritical}` as in
[RI-65](../native_growth_residual_reentry_v1/OBSTRUCTION.md), and let h_A(Q)
be RI-66's whole-component-normalized raising role sum on this parent sector.
Then `T_n^+=A_n^++F_n^+`, where

\[
 A_n^+=\sum_c p_c^0h_A(Q_c),\qquad 0\le F_n^+\le L_n^0.
\]

F_n^+ is only the selected sector's full contribution, not all of L_n^0.
In particular whole recharge cannot simply be restricted to A: an earlier
zero-defect parent can accumulate V used by later positive-defect full births.
Define the nonnegative proper charged mass

\[
 C_n^0=A_n^++G_n^0
       =\sum_c p_c^0[\,h_A(Q_c)+J_+(Q_c)\,]. \tag{16}
\]

The raising and recharge indicators are disjoint, so `0<=h_A+J_+<=1`.
For canonical allocations RI-66 confines the support to D(Q)<0; (16) still
retains each marked component's actual allocation. Combining with (13),

\[
 \boxed{\sum_{n=5}^{N-1}T_n^+
      \le E V_5+\sum_{n=5}^{N-1}C_n^0+\frac25.} \tag{17}
\]

The sharper version retains `-E V_N-sum K_n^0` and the actual signed mixing
error from (12). The remaining sufficient premise is concrete:
`N^(-1) sum_(n=5)^(N-1) C_n^0 -> 0`. Together with RI-65's already summable
zero-defect and critical sectors, this would give normalized defect tending
to zero in expectation, L1 and probability under this same candidate.
It is **not proved here**, is not asserted necessary, and is not a new
selection objective. This packet reduces the full-birth part to a proper
charged-mass obligation; it does not solve that obligation.

**This sufficient premise also forces height density one.** The actual
expected recharge differs from G_n^0 by at most eta_n, since its indicator
lies in [0,1]. The actual V identity, dropping only nonnegative consumption,
therefore gives

\[
 E V_N\le E V_5+\sum_{n=5}^{N-1}G_n^0+\frac15. \tag{17a}
\]

Because `0<=G_n^0<=C_n^0`, vanishing Cesaro C_n^0 implies `E[V_N/N]->0`.
Together with the defect conclusion above and the exact identity
`h(P_N)=N-delta(P_N)-V(P_N)`, it follows that

\[
 E\left[1-\frac{h(P_N)}N\right]
 =E\left[\frac{\delta(P_N)+V(P_N)}N\right]\longrightarrow0. \tag{17b}
\]

Thus `h(P_N)/N->1` in expectation, L1 and probability under that premise.
This is a near-chain, height-density-one regime, not balanced square-Ferrers
scaling `h~sqrt(N)`, and it assigns no physical dimension. Discarding the
terminal balance in (12) is consequently restrictive for geometry: recharge
can be stored in extensive V_N without becoming defect. The unsigned C_n^0
budget is not a general route to balanced geometry; the exact signed identity
retains cancellations that this sufficient bound deliberately loses.

There is no automatic coefficient-one recharge/improvement inequality. The
bounded six-event diagnostic `Q=(0,1,1,3,5,7)` has recharge numerator 16 and
D(Q)=-6, hence `J_+(Q)/[-D(Q)/e(Q)]=8/3`. This rejects coefficient 1 only,
not every size-independent coefficient, and says nothing by itself about
allocation or occupation. No extra universal-family search is made here.

## 7. Why recharge need not be small, and why modes of convergence differ

An explicit allowed deterministic growth path visits square Ferrers diagrams.
From `m x m`, add the new column cells `(i,m+1)` for i=1,...,m, then the new
row cells `(m+1,j)` for j=1,...,m+1. Every intermediate order remains a Ferrers
down-set. Exactly two of these 2m+1 births increase height: the two rectangle
completion corners. All other 2m-1 births are proper, neutral and preserve
height, and therefore recharge V. At square times,

\[
 |P|=m^2,\qquad\delta(P)=0,\qquad h(P)=2m-1,
 \qquad V(P)=(m-1)^2. \tag{18}
\]

Thus cumulative recharge can be extensive with defect identically zero and
no defect-raising full births. The endpoint V_N in (8) stores that recharge.
A sublinear recharge budget is sufficient for sublinear full-raising counts,
not necessary. This path is a structural example, not a claim that it has
positive infinite-path probability or appreciable occupation under RI-59.
It proves no lower bound on the candidate's expected recharge.

Deterministic Cesaro decay of the expected budgets above does not by itself
give almost-sure decay. An almost-sure variant needs a separate assumption
on conditional rates along the **actual** path. For example, if
`N^(-1) sum g_n^0(P_n,r_n) -> 0` almost surely, summable mixing errors and
the bounded-increment martingale law used in RI-56 make the actual recharge
count divided by N vanish almost surely. Equation (8) then does the same
for defect-raising full births. An analogous pathwise charged-rate premise
handles the proper positive-defect/noncritical contribution as well.
No such premise is established here. Stronger summability of the expected
recharge budget would imply finitely many actual recharges and full defect
increments almost surely, not finitely many full births.

## 8. Bounded exact corroboration and disposition

The [checker](check.py) fully replays byte-pinned accepted RI-66 and its
[certificate](../native_growth_terminal_cost_v1/CERTIFICATE.json), including
the accepted RI-63 canonical/strict-law checks and their controls. It then
explicitly reconstructs RI-63 once more to obtain its row interface, which
RI-66 does not return. No accepted helper globals are patched. All five
source/certificate dependency pins are verified before loading and again
after reconstruction. This is disclosed accepted-source reuse, not an
independent replacement of the growth-law implementation.

New geometry independently enumerates Ferrers and punctured-rectangle cell
types and every arbitrary retained subset. A punctured rectangle with six
vertices is constructed directly: its removed seventh cell is never placed
in an order. Height recurrence is cross-checked against chain subsets.

| Exact finite coverage | Count |
| --- | ---: |
| Natural orders, sizes zero through six | 5,232 |
| Arbitrary retained subsets | 320,867 |
| Eligible last-birth cases | 5,231 |
| One-top cases / positive-length bounded top streaks | 408 / 477 |
| Available streak cases reaching quenching | 351 |
| Natural-history/cutoff charge identities | 36,147 |
| Recharge / proper negative-V / full-raising birth cases | 1,225 / 58 / 95 |
| Raw marked parent-five histories / labeled proper slots | 11,424 / 142,944 |
| Proper components / terminal types / maximal roles | 798 / 255 / 671 |

All 798 component recharge and negative-V factors are checked both from raw
marked slots and canonical row sums, with RI-66's verified U denominators
and extension multiplicities. There are 301 recharge-positive and 27
negative-V-positive components. Recharge and selected-sector raising obey
the stated disjointness bound; negative-V roles are separately retained.
The certificate also retains the punctured-square streak and the `(3,2,1)`
diagnostic, with extension count 16 and maximal-deletion counts 5,5,6.

The actual starting expectation and current canonical boundary quantities are

\[
 E V_5=\frac{89043192349}{281107200000},\quad
 G_5^0=\frac{911129927779901}{26711031029760000},\quad
 L_5^0=\frac{6650803}{108900000}. \tag{19}
\]

Here `K_5^0=A_5^+=F_5^+=0`. In particular the positive whole full-raising
charge L_5^0 is not the selected-sector full charge F_5^+. The saved
[certificate](CERTIFICATE.json) contains exact actual, boundary and interior
expectations, height/defect/V drifts, signed epsilon, and one-step endpoint
identities. A separately evolved boundary history is never used.

The main independent audit computed height by exhaustive chain-subset
comparison on 766 cached orders, aggregated all 1,490 canonical rows and
15,702 labeled proper-slot occurrences, and checked the mixture and charge
identities. It took 6.484 seconds, with checkpoint peak RSS 112,951,296 bytes.
All 27 overlapping rational fields match the saved certificate exactly.
A further main-worker certificate audit checked all 255 terminal records,
671 roles and 798 pairs of component factors using chain-subset heights and
the accepted RI-66 data.

Ten new in-memory controls reject changed dependency bytes, an incorrect
top-F value, omitting the first neutral step, ideal-only retained subsets,
a wrong path charge, wrong component denominator, corrupt recharge weight,
corrupt strict mixture, an attempted seventh top and duplicate JSON keys.
Default execution also rejects a missing-component certificate: 11 new
saved-certificate controls, in addition to the accepted controls replayed.
Each rejection is checked for its intended reason. Saved-certificate checking
compares the complete reconstructed object; explicit checks stay active under
optimized Python.

From the repository root, with Python's standard library only:

```sh
python3 -I -S -B docs/track_b/native_growth_top_drift_v1/check.py
python3 -I -S -B -O docs/track_b/native_growth_top_drift_v1/check.py
```

The main worker ran both commands under CPython 3.14.0 with the predeclared
sampled parent watchdog. Both exited zero in 22.405/22.334 seconds, with
sampled peak RSS 137,330,688/139,018,240 bytes. Their 2,616-byte stdout was
byte-identical, SHA-256
`71f172797e3215538b2b49715a631e05efce08fb8d7d2dc82108fe1d40996c74`.
The checker author independently replayed default mode in 22.196/22.188
seconds. A separate reviewer independently replayed it in 21.826/21.875
seconds, using the checker's resource checkpoints and an outer timeout,
without separately sampling RSS. Both reviewers' output matches exactly.
Normal/optimized witness generation also matched byte-for-byte.

Stable byte pins:

- `check.py` (29,082 bytes, 582 lines):
  `255180f3b381d1ff7b2d4bc2b0a58731a3ad6426d48964b2017e527e42389885`;
- `CERTIFICATE.json` (175,533 bytes):
  `c070a561145548afdea835ab22bc1a0d33adf935a496c6e1435da470520a23c6`;
- canonical reconstructed witness:
  `e03afea107a133bd4c4ec45caba9c7e677c33099e5e403f49cdef6139a7e3a0d`.

Two independent reviewers read the complete proof and all checker source,
including the final quenching/staircase delta. The complete parsed-certificate
review checked all structured terminal, role, component and expectation data.
The height-density-one implication was separately verified analytically;
it is not an asymptotic conclusion drawn from finite tests.

**Disposition:** the exact top/streak formulas and pathwise charge hold,
and the actual-prefix boundary bound follows within the unchanged candidate.
Recharge or charged-mass decay remains unproved. The unsigned sufficient
budget would force height density one and does not establish balanced geometry.
The all-size proofs are not extrapolations from size-six enumeration. No q6
law, new optimizer, informative QM, geometry reconstruction, mass, gravity or
empirical discriminator is derived. Option B and Status M remain unchanged.
Exactly the three assigned files are authored; accepted sources, ledgers,
measurement, RET and git/index operations remain untouched by the worker.
Stop at stable handoff for coordinator adjudication.
