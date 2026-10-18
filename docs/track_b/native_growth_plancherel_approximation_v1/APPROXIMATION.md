# RI-75 — strict-positive finite-depth approximation of the Plancherel graft

24 September 2026 UTC. **Independently accepted by the coordinator.**
This packet proves a conditional approximation theorem for the accepted
RI-74 zero-allowed graft. It does not adopt a new law, change the held prefix,
or derive Plancherel dynamics from DET. Finite exact tests below corroborate
a small, explicitly different cutoff-zero toy; they do not enumerate the
actual parent-six layer or prove the all-size theorem.

## 1. Fixed premises and scope

Use [RI-38](../native_joint_growth_extension_criterion_v1/CRITERION.md)'s
scalar-passive, one-birth family: finite committed orders, immutable binary
records, every ideal eligible, and fair newborn marks. A proper slot may
inspect the whole unmarked parent but read only records inside its precursor.
The maps act on the entire unnormalized residual:
\[
 \mathcal B_{S,b}(D)=\tfrac12 q_{P,r}(S)D,\qquad b\in\{0,1\}.
 \tag{1}
\]
Thus two-birth scalar identities multiply the whole \(D/4\), not just a
diagonal or trace summary. The residual is passive; there is no informative
quantum coupling or quantum reconstruction here.

Let \(q^G\) be exactly [RI-74](../native_growth_plancherel_graft_v1/PLANCHEREL_GRAFT.md):
all actual accepted marked rows at parent sizes \(n<k=6\) are held,
including the actual strictly mixed RI-63 \(q_5\). At size six the graft is
full-only. At larger sizes a family parent has the intrinsic form
\(K\oplus F\), \(|K|=6\), with nonempty Ferrers suffix F; its lifted ideal
weights are \(w(F+x_S)/w(F)\). All other proper slots have weight zero;
off-family parents are full-only. The core is the unique six-element ideal,
not the first six labels. The chosen Ferrers weight is
\[
 w(F)=\frac{b(F)e(F)}{|F|!},
 \tag{2}
\]
where b counts all isomorphisms to all matching oriented Young diagrams and
e counts linear extensions. Set \(w(\varnothing)=1\).
RI-74 proves normalization and complete diamonds, including zero products
and the cutoff. Its Plancherel input remains a mathematical borrow.

**Question.** Is this complete boundary law a finite-depth limit of
globally compatible strictly positive laws with exactly the same held rows,
record-read locality, equivariance and fair passive marks?

**Answer.** Yes, within these premises. Sections 2–6 give one explicit
rational construction for every rational \(0<\epsilon\leq1\).
The limits are at fixed finite depth as \(\epsilon\downarrow0\).
No fixed-\(\epsilon\) large-size or infinite-history total-variation
conclusion is proved or claimed here.

## 2. Use the complete structural graph

At each new parent size n, take every local proper node
\[
 i=[P,S,r|_S],\qquad |P|=n,\quad S\subsetneq P\text{ an ideal},
\]
quotiented by full parent isomorphisms carrying precursor and internal marks.
Normalization still sums every individual labeled ideal, not one term
per quotient node. Include every raw diamond edge from size \(n-1\),
all old markings, both newborn marks, equal precursors, loops and parallel
edges. **Do not delete edges with zero boundary coefficients.**

An edge between the two second-birth nodes has the common unmarked terminal
\(H=C+x_S+y_T\). Node isomorphisms also preserve terminal type, so each
complete component c has one terminal type H
([RI-66, §2](../native_growth_terminal_cost_v1/FACTORIZATION.md)).
Different marked components can share H; they remain distinct components.

Call c **active** iff its terminal has the intrinsic form
\[
 H=K\oplus Z,\qquad |K|=6,\qquad Z\ne\varnothing\text{ Ferrers}.
 \tag{3}
\]
Here H comes from a proper slot and therefore has at least two maxima.
Terminal invariance makes this a property of the entire structural
component, not of a selected positive-edge subgraph. All other components
are inactive.

### Positive-factor lemma at the zero boundary

Let an active node restore the maximal vertex y of H, so
\[
 P=H-y,\qquad S=\operatorname{past}_H(y),\qquad
 U=\operatorname{Max}(P)\setminus S.
\]
A nonempty Ferrers order has a unique minimum \(z_0\). Since H has at least
two maxima, Z has at least three vertices; \(z_0\ne y\), and
\(K\cup\{z_0\}\subseteq S\). All core vertices are below the suffix.
A maximum of P outside S stays maximal after y is restored; conversely
each maximum of H other than y is such a vertex. Consequently
\[
 U=\operatorname{Max}(Z)\setminus\{y\}.
\]
For every nonempty \(B\subseteq U\), both \(Z-B\) and
\(Z-(B\cup\{y\})\) are nonempty Ferrers ideals containing \(z_0\).
Deleting several maximal cells leaves an ideal of the original diagram.
The smaller parent \(P-B\) therefore retains K and a nonempty Ferrers
suffix, and restoring y gives another such family member. Hence
\[
 q^G_{P-B}(S)
   =\frac{w(Z-B)}{w(Z-(B\cup\{y\}))}>0.
 \tag{4}
\]
All these parents have size at least seven. No factor reaches the
size-six full-only bridge or an off-family fallback. Marks do not change
(4). Define the strictly positive, finite boundary potential **only on
active nodes**:
\[
 u_i^G=\prod_{\varnothing\ne B\subseteq U}
       q^G_{P-B}(S)^{(-1)^{|B|+1}}.
 \tag{5}
\]
No boundary potential is asserted on inactive nodes. This is not a
wholesale application of RI-38's positive theorem to a law with zeros.

### Full-component constancy, without division by a zero history

For the Ferrers terminal suffix define
\[
 \Psi(Z)=\prod_{\varnothing\ne A\subseteq\operatorname{Max}(Z)}
                w(Z-A)^{(-1)^{|A|+1}}>0.
 \tag{6}
\]
All weights are positive: the minimum survives even deletion of every
maximum. Pair A=B with \(A=B\cup\{y\}\) for every nonempty \(B\subseteq U\).
Their exponents have opposite signs; the unpaired \(A=\{y\}\) contributes
\(w(Z-y)\). Equations (4)–(5) give
\[
 \Psi(Z)=w(Z-y)u_i^G,\qquad
 \frac{q_i^G}{u_i^G}=\frac{w(Z)}{\Psi(Z)}.
 \tag{7}
\]
The last expression depends only on the intrinsic unmarked terminal suffix,
not the deletion role, core records or a preferred diagram embedding.
It is constant on the **full** active component. Distinct marked
components are not merged merely because these constants coincide.

For completeness, every edge in such a component has old base
\(K\oplus(Z-\{x,y\})\), still containing \(z_0\). Its first-birth graft
weights are positive as well. No hidden zero edge is divided out.
Set once for each complete component
\[
 a_c^0=\begin{cases}w(Z)/\Psi(Z),&c\text{ active},\\0,&c\text{ inactive}.
              \end{cases}
 \tag{8}
\]
The positive proper slots of \(q^G\) are exactly the active nodes. Indeed,
a positive proper graft birth must be a lifted birth with Ferrers child;
conversely (3) and the positive-factor lemma give such a parent and birth.
At parent sizes six and seven there are no active nodes: their possible
Ferrers terminal suffixes have respectively one or two vertices, hence only
one maximum. Thus every proper graft weight at those layers is zero.

## 3. Recursive strict approximation

Fix rational \(0<\epsilon\leq1\). Put \(q^\epsilon=q^G=q^{actual}\) on
**every** marked row with parent size below six. Inductively suppose all
smaller rows are defined, positive and compatible. On the complete
size-n proper table define RI-38's directly local potential
\[
 u_i^\epsilon=
 \prod_{\varnothing\ne B\subseteq\operatorname{Max}(P)\setminus S}
       q^\epsilon_{P-B,r|_{P-B}}(S)^{(-1)^{|B|+1}}>0,\qquad
 h_i^\epsilon=a_c^0u_i^\epsilon .
 \tag{9}
\]
Only smaller-parent rows occur. Inactive h is exactly zero; no \(u^G\)
or \(0/0\) is evaluated there. Define the two finite complete-table maxima
\[
 B_n^\epsilon=\max_{P,r}\sum_{S\subsetneq P}h_{P,r}^\epsilon(S),
 \qquad
 M_n^\epsilon=\max_{P,r}\sum_{S\subsetneq P}u_{P,r}^\epsilon(S),
 \tag{10}
\]
summing individual labeled ideals. The maxima include all counterfactual
marked parents on a fixed n-vertex carrier. Then set
\[
 t_n=\frac{\epsilon}{(n+1)^2},\qquad
 \lambda_n=\frac{1-t_n}{\max(1,B_n^\epsilon)},\qquad
 \tau_n=\frac{t_n}{2(1+M_n^\epsilon)},
 \tag{11}
\]
\[
 q^\epsilon_i=\lambda_n h_i^\epsilon+\tau_nu_i^\epsilon
             =(\lambda_n a_c^0+\tau_n)u_i^\epsilon
       \quad(S\subsetneq P),\qquad
 q^\epsilon_{P,r}(P)=1-\sum_{S\subsetneq P}q^\epsilon_{P,r}(S).
 \tag{12}
\]
There is no mixture of completed histories, no row-dependent mixing
coefficient, and no conditioning on surviving in the target support.
The common component scales in (12), not a mixture shortcut, enforce
compatibility.

### Admissibility at every finite size

For n≥6 we have \(0<t_n<1\), \(\lambda_n>0\), \(\tau_n>0\).
Every proper slot is positive, and every row satisfies
\[
 \lambda_n\sum h_i^\epsilon\leq1-t_n,\qquad
 \tau_n\sum u_i^\epsilon
 \leq\frac{t_nM_n^\epsilon}{2(1+M_n^\epsilon)}<\frac{t_n}{2}.
 \tag{13}
\]
Its full complement is therefore **strictly greater than \(t_n/2\)**.
All probabilities are rational by finite rational induction.

Each factor of (9) reads only \(r|_S\), directly, with no forbidden
intermediate record read. Isomorphisms preserve deletion subsets and factors.
The a constants use only terminal unmarked structure. Crucially, (10)–(11)
are fixed once from the complete counterfactual marked table during the
construction of the law, **before any current marking is supplied for
evaluation**. They are not adaptive current-row parameters. This preserves
precursor-record locality and marked-parent equivariance. Full slots are
entitled to read all parent records.

RI-38's positive-prefix theorem gives the exact raw-edge identities for
\(u^\epsilon\). The two second-birth nodes of each edge belong to the same
complete component and therefore have the same positive multiplier
\(\lambda_n a_c^0+\tau_n\). Multiplying the potential identity by it proves
every new diamond. A second birth in an incomparable-birth diamond omits
the other newborn, so that second precursor is always proper; a new full
complement imposes no extra same-layer diamond condition. It participates
as an inherited first factor at the next induction stage.

Together with the unchanged valid prefix this proves all sizes, all marks,
equal/reversed precursor pairs and all full-payload maps (1). The finite
maxima make the construction well-defined, not computationally efficient.
Normalized kernels also define consistent finite-history distributions
and the ordinary path measure on the finitely branching history tree.
No covariant event-algebra classification is claimed.

## 4. Uniform convergence on each finite layer

Induct on n. Convergence below six is exact equality. For every active node,
all factors in (9) have strictly positive graft limits by (4).
Finite products and reciprocals are continuous there, so
\(u_i^\epsilon\to u_i^G\), and (7) gives
\(h_i^\epsilon\to q_i^G\). On every inactive node both h and the target
proper weight are identically zero. Each fixed complete marked table is
finite; convergence is therefore uniform on that table.

It follows that
\[
 B_n^\epsilon\longrightarrow
 B_n^G:=\max_{P,r}\sum_{S\subsetneq P}q^G_{P,r}(S)\leq1,\qquad
 \lambda_n\longrightarrow1.
\]
Do **not** assume that inactive \(u_i^\epsilon\) converge or remain bounded.
Their contribution is controlled by the total row bound (13), which
vanishes as \(\epsilon\downarrow0\), even if \(M_n^\epsilon\to\infty\).
Every proper probability in (12) thus tends uniformly to its graft weight;
full complements converge by finite normalization. This completes the
induction.

In particular at n=6,7, h=0 and the proper total is \(<t_n/2\),
converging to the full-only graft. No actual parent-six inventory is needed
for this argument.

## 5. Explicit finite-depth marked-history bound

All quantities here refer to the complete mathematical table, not estimates
from the toy. Define the computable finite-layer discrepancy
\[
 E_n(\epsilon)=\max_{P,r}
          \sum_{S\subsetneq P}|h_{P,r}^\epsilon(S)-q^G_{P,r}(S)|.
 \tag{14}
\]
It is rational for rational epsilon and tends to zero at each fixed n.
Let \(d_n\) be the maximum total variation between full row distributions
of ideal plus fair newborn bit. The fair split leaves TV unchanged.
The full-complement error is bounded by the sum of proper-slot errors,
and consequently
\[
 d_n\leq E_n+(1-\lambda_n)B_n^\epsilon+\frac{t_n}{2}.
 \tag{15}
\]
Since \(\lambda_n\leq1\), there is no sign ambiguity. In fact
\[
 (1-\lambda_n)B_n^\epsilon
    =(B_n^\epsilon-1)_++t_n\min(B_n^\epsilon,1).
\]
Also \(|B_n^\epsilon-B_n^G|\leq E_n\) and \(B_n^G\leq1\).
Hence the explicit bound
\[
 d_n\leq\bar d_n:=
 \min\left(1,\ E_n+(B_n^\epsilon-1)_+
       +t_n\min(B_n^\epsilon,1)+t_n/2\right)
 \leq \min(1,\,2E_n+3t_n/2).
 \tag{16}
\]
These are proved error bounds, not a claimed epsilon-only convergence rate:
(14) still depends on the recursively constructed tables.

Let \(\mu_N^\epsilon,\mu_N^G\) be distributions on entire naturally labeled
marked histories through N births. Their histories through six births
coincide exactly. At each subsequent step, maximally couple the two ideal/bit
rows whenever their histories still agree. The conditional disagreement
probability at that step is at most \(\bar d_n\). Thus
\[
 \|\mu_N^\epsilon-\mu_N^G\|_{\rm TV}
 \leq 1-\prod_{n=6}^{N-1}(1-\bar d_n)
 \leq \min\left(1,\sum_{n=6}^{N-1}\bar d_n\right)
 \xrightarrow[\epsilon\downarrow0]{}0
 \quad\text{for every fixed finite }N.
 \tag{17}
\]
For N≤6 the bound is zero (empty product convention).
Every function or coarse-graining of these histories obeys the same bound.
For example, at a fixed N≥7 the probability under this candidate that
\(\delta(P_N)>6\) is at most (17), since that event is impossible for the
graft. This is a finite-horizon statement only.

## 6. Limits deliberately not taken

Although \(\sum_n t_n<\infty\), this does not bound total leakage from the
graft's Ferrers-suffix support. The floor in (13) controls only added
**proper** mass. The full complement can itself create a non-Ferrers child
from a Ferrers parent; active rescaling and accumulated earlier perturbations
also enter (14)–(16). No size-uniform or summable bound on \(E_n\) has been
proved. A summable exploration schedule alone therefore does not transfer
RI-74's pathwise \(\delta\leq6\) conclusion to any fixed positive epsilon.

For an explicit full-slot leak, take the suffix to be the four-cell
\(2\times2\) Ferrers diamond. A full birth appends a universal top, producing
a nonchain five-vertex order with a unique maximum. A Ferrers diagram with
a unique maximum is rectangular (all row lengths equal); at size five such
a rectangle is a chain. The new suffix is therefore not Ferrers. The graft
assigns this full slot zero, but every strict approximant assigns it positive
mass. This leak is in the full complement, not the proper exploration floor.

No interchange of \(N\to\infty\) and \(\epsilon\downarrow0\), infinite-path
TV convergence, or fixed-epsilon almost-sure/expected \(\delta/N\to0\)
theorem is established here. Selecting epsilon for each fixed finite horizon
does not construct one strict law with the asserted infinite-horizon
property. No claim of balanced shape, manifold, Lorentzian metric, mass,
source response or gravity is made.

The actual law and prefix selection are not changed. The chosen
Plancherel/Ferrers target is not justified by DET uniqueness or native
dynamics. Passive D is retained, not promoted to a derived quantum
instrument. Option B, metric-as-record Status M, RET's separate scope and
measurement work remain unchanged.

## 7. Predeclared bounded exact corroboration

Only the three files in this directory are new work. Accepted sources,
coordinator/navigation/ledger files, RET, measurement and git/index remain
outside this worker's edit scope.

The checker independently re-expresses a **cutoff-zero toy**: pure
Ferrers target rows on Ferrers parents, full-only fallback elsewhere.
Its natural parents have sizes zero through three and terminals at most
four. Epsilon is restricted to \(\{1,1/2,1/4\}\).
All binary markings, both newborn bits, labeled ideals and structural
components in that domain are retained; no zero-target edge is removed.
The same deletion-potential and complete-layer scaling formulas are used.
The toy has no actual six-event core and is **not** a numerical validation
of the held RI-63 prefix or actual parent-six layer.
Starting from its neutral empty seed makes the toy's numerical rows
mark-independent, although distinct marked components and all record cubes
are retained. Preservation of actual prefix feedback is a theorem premise
and exact construction rule, not an empirical feature tested by this toy.

A separate explicitly **synthetic algebraic** row with
\(u=(1,1/\epsilon)\), \(a^0=(1/2,0)\) tests the floor bound in the presence
of a divergent inactive potential. It is not asserted to be a realizable
RI-38 poset component; it isolates the inequality that handles such
divergence in the proof. A second cap-stress row uses \(u=(3,1/\epsilon)\)
with the same a constants, to exercise the \(B>1\) branch. That second row
is not a convergence fixture: its active h does not tend to the target
proper mass \(1/2\). Both rows use only the same three declared epsilons.
Exact checks and refusal controls include
target-zero slots, strict normalization, all bounded diamonds,
equivariance/locality, finite-history TV, malformed receipts and over-scope
requests. Checking several epsilons is not proof of a limiting rate.

Execution is standard-library-only CPython 3.14, normal and optimized
modes, explicit conditions rather than removable assertions; declared
per-run limits are **120 seconds / 512 MiB**. No optimizer, network,
sampling, larger-domain search or actual parent-six exhaustive inventory
is authorized. Fresh evidence is retained durably below
`/Volumes/AI_DATA/development/det-review-evidence/ri75-qr/`.
No lost temporary receipt is re-created as recovered evidence.

## 8. Completed corroboration and source-stable handoff

The [checker](check.py) is standalone and imports no predecessor or project
code. It independently checks the natural-order inventory against all
transitive subsets of forward edges. Diagram weights count every oriented
partition and every isomorphism; labeled ideals remain separate row terms.
The [certificate](CERTIFICATE.json) stores exact rational results plus
deterministic manifests, not sampled or floating-point estimates.

The complete structural toy graph has the following inventory:

| New parent size | Local nodes | Marked components | Active components | Raw edges | Zero target edges |
|---|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 4 | 4 |
| 2 | 6 | 4 | 2 | 32 | 24 |
| 3 | 39 | 19 | 2 | 400 | 368 |

These are **436 retained raw edges**, not only positive target edges.
For each of the three epsilons the checker validates 66 new marked rows
with 352 individual labeled ideal slots, in addition to the fixed origin
row. It makes 1,198 record-locality and 1,980 marked-equivariance comparisons.
The target and each strict approximation pass all 436 scalar diamonds and
436 full complex-payload comparisons, including terminal/newborn-mark
transport. The payload has diagonal entries 2,3 and off-diagonal entries
\(1/3\pm2i/5\); one such payload is corroboration, while (1) supplies the
arbitrary-D proof.

Complete marked-history inventories at sizes 0–4 are 1,2,8,56,640. At size
four all 640 histories have positive approximating probability, versus 80
positive target histories. Exact TV is checked against both row-envelope
bounds and the sharper product bound in (17). The six synthetic rows test
the divergent inactive coordinate and both cap branches, with no asserted
poset realization and no convergence claim for the cap-stress rows.
Thirteen refusal controls
cover invalid epsilon/node/activity, a zero target denominator, an omitted
floor denominator, a wrong error bound, overscope inventory, duplicate JSON
keys, a dropped labeled ideal, altered source/maxima and unknown fields.

Fresh saved-certificate runs used CPython **3.14.0**, standard library only:

```sh
/opt/homebrew/bin/python3 -I -S -B docs/track_b/native_growth_plancherel_approximation_v1/check.py
/opt/homebrew/bin/python3 -I -S -B -O docs/track_b/native_growth_plancherel_approximation_v1/check.py
```

The QR worker's durable supervisor recorded normal/optimized elapsed times
**0.239/0.232 seconds**, sampled peak RSS **24,208/24,016 KiB**, exit zero,
unchanged source/certificate and no 120-second/512-MiB stop. Internal peak-RSS
checkpoints and wall alarm also passed; sampled RSS is not a hard allocator
cap. Both modes produced identical 5,780-byte stdout, SHA-256
`c4daa669735d44356f77115b7139add810ea962513cedef062e603af3168d04f`,
and identical 132-byte progress stderr, SHA-256
`394c56bb3222aa0f46021a83bf983d94aa0bd43df2514cc2256b9ce7116f4fd9`.
The reconstructed canonical witness digest, excluding its output newline, is
`6ffb590db4c75e03c3002038c91277c5ef3e9c8a0892f1ca74b584147a962656`.

Frozen machine identities, each with exactly one EOF newline:

- check.py: 26,354 bytes, SHA-256
  `f7fe29623524beaca0399af38454080a2244eb478545ec5257cbfcf5e55b21a6`.
- CERTIFICATE.json: 14,784 bytes, SHA-256
  `72f28b26debe5f33846e7720ce029e21a2bd1a78f83490fd06d7d9f099554aed`.

The author independently captured the final witness in 0.227 seconds, sampled
peak 24,821,760 bytes, with the same machine identities. Its final normal/-O
saved-certificate runs from a copied two-file closure also passed, in
0.255/0.226 seconds with sampled peaks 24,477,696/24,559,616 bytes. Their
stdout/stderr match the worker streams exactly; original and copied input
pins stayed unchanged. Author source
snapshots, witness streams and receipts remain at
`/Volumes/AI_DATA/development/det-review-evidence/ri75-qr/author-GWce74/`.
QR-worker normal/optimized raw streams, supervisor, receipts and independent
arithmetic remain at
`/Volumes/AI_DATA/development/det-review-evidence/ri75-qr/worker-eP2DGd/`.
These are worker/author evidence, not coordinator replay or acceptance.

Two independent reviewers read the full mathematical note and checker,
including the final source delta, and reported no blocker at the frozen
checker pin. Separately written worker arithmetic imported no project code:
it used (6) directly for coefficients and brute permutation counts for
linear extensions. Normal/optimized outputs agreed exactly. A separate
comparison passed **1,188** checks against the saved witness, including every
marked-row probability manifest, all layer maxima/scales/errors and every
finite-history TV. Its additional weight-only check of the explicit
five-vertex full-leak example enumerated diagram embeddings through five;
it constructed no parent-four or parent-five probability layer. This extra
check is not part of the terminal-four machine certificate.

The independent arithmetic's first setup attempt failed before mathematical
checks because macOS rejected an RLIMIT_AS request. That failure is recorded
as a retrospective setup record, not fabricated raw output. The unsupported
limit was removed; fresh supervised runs with peak-RSS checkpoints passed.
All successful evidence above is freshly retained, not a reconstruction of
lost temporary receipts.

**Disposition:** an explicit conditional strict-positive family and
finite-depth approximation theorem, with bounded exact corroboration.
Actual held rows remain untouched. The three-file packet is ready for
coordinator adjudication; no successor, adoption, asymptotic defect proof,
physical correspondence or git/index action is started by this handoff.


## 9. Coordinator adjudication

Root read the complete final proof and checker, and a separate coordinator
review reconciled the final note against its earlier independent proof review.
No mathematical or scope blocker remained. Root's fresh copied two-file replay
under CPython 3.14.0 passed normally and with -O in 0.260/0.258 seconds,
exit zero, with byte-identical stdout/stderr matching the identities above.
Both modes retained unchanged machine inputs. The declared 120-second/512-MiB
alarm, internal peak-RSS checkpoints and external watchdog passed; the short
runs make the external RSS samples sparse, not measurements of true peak RSS.
Fresh copies, actual streams, receipts and supervisor are retained in
`/Volumes/AI_DATA/development/det-review-evidence/ri75-root-20260924/`.

The conditional theorem is accepted; the three-file reservation is released
for root publication. RI-76 separately investigates fixed-parameter defect
asymptotics and a positive-probability height obstruction via irreversible
exit from the graft family. Those conclusions are not results of this packet's
finite-history limit or bounded toy. The actual law, physical premises and
RET pause remain unchanged.
