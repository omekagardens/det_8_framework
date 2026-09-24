# RI-77 — record locality of a latent random-cutoff graft mixture

24 September 2026 UTC. **Exact locality counterexample independently accepted
by the coordinator.** This packet tests membership in the existing
precursor-record-local class before any asymptotic or geometric promotion.
It proposes no adopted law and changes no accepted row.

## 1. Candidate and held inputs

Let B be the [RI-38](../native_joint_growth_extension_criterion_v1/CRITERION.md)
strict common half-scale continuation of the **actual** held marked prefix
at parent sizes below six, including the actual RI-63 strictly mixed q5.
At parent sizes n≥6 use exactly
\[
 u^B_{P,r}(S)=
 \prod_{\varnothing\ne A\subseteq\operatorname{Max}(P)\setminus S}
 (q^B_{P-A,r|_{P-A}}(S))^{(-1)^{|A|+1}},
 \qquad
 a_n=\frac1{2(1+M_n^B)},
\]
\[
 M_n^B=\max_{|P|=n,r}\sum_{S\subsetneq P}u^B_{P,r}(S),\qquad
 q^B_{P,r}(S)=a_nu^B_{P,r}(S)\ (S\subsetneq P),
 \quad q^B_{P,r}(P)=1-\sum_{S\subsetneq P}q^B_{P,r}(S).
 \tag{1}
\]
Sums are over individual labeled ideals. Complete-table constants are
chosen before evaluating the current marking. This specifies a new
*baseline for this candidate question*, not a replacement for any accepted
continuation. It is not the RI-75 approximation law.

Independently sample one latent integer cutoff \(R\geq6\) with
\[
 w_R=\mathbb P(R)=2^{-(R-5)},\qquad
 \sum_{R=6}^\infty w_R=1,\qquad
 s_j:=\mathbb P(R\geq j)=2^{-(j-6)}\quad(j\geq6).
 \tag{2}
\]
For each fixed R, define \(G^R\) by the
[RI-74](../native_growth_plancherel_graft_v1/PLANCHEREL_GRAFT.md) construction
with core size R: follow B at parents n<R; use the full-only bridge at n=R;
then use the intrinsic R-core Plancherel/Ferrers graft, with full-only
fallback off that family. Its core is recognized as the unique R-element
ideal, not as a history label or an arbitrary supplied subset.

All records remain fair immutable bits, and maps remain
\(\mathcal B_{S,b}(D)=q_{P,r}(S)D/2\) on the whole unnormalized passive D.
The cutoff is an additional latent mathematical choice; its prior and the
Plancherel target are not justified as uniquely DET-derived dynamics.

## 2. What mixing does preserve

For fixed R, the RI-74 normalization and covariance proof applies to the
complete strictly positive B-prefix ending at size R. The same cases cover
the R−1/R bridge boundary, lifted suffix transitions, zero products and
off-family fallback. Thus each \(G^R\) is a normalized, equivariant,
precursor-record-local, zero-allowed law with complete full-payload diamonds.
This argument does not require the six-event prefix to be the only possible
cutoff prefix; the proof uses its completeness and inherited covariance.

For a complete naturally labeled marked history \(h_N\) through N births,
let \(\mu_N^R(h_N)\) be its probability under \(G^R\). Define
\[
 \mu_N^{mix}(h_N)=\sum_{R=6}^\infty w_R\mu_N^R(h_N).
 \tag{3}
\]
Nonnegative sums preserve normalization and prefix marginalization.
For N≥6 all \(R\geq N\) follow B throughout those N births, so the infinite
sum is exactly the finite expression
\[
 \mu_N^{mix}
 =\sum_{R=6}^{N-1}w_R\mu_N^R+s_N\mu_N^B .
 \tag{4}
\]
It is rational on every finite history. Every such history has positive
baseline probability; in particular the positive-weight tail R>N proves
\(\mu_N^{mix}(h_N)>0\). All histories through size six retain the held
prefix exactly. These are ordinary finite-cylinder statements, not a
geometry result.

### Covariance is not locality

Strip the common fair-bit factor from a component history probability,
writing \(W_R(P,r)=2^{|P|}\mu_{|P|}^R(P,r)\).
Inherited diamonds make each \(W_R\) invariant under the choice of natural
construction of the same marked order: adjacent swaps of incomparable
births preserve the product. This also holds for zero products.
Let \(W_{mix}=\sum_Rw_RW_R>0\).
The induced next-ideal probability, after marginalizing R, is
\[
 q^{mix}_{P,r}(S)
  =\frac{\sum_Rw_RW_R(P,r)q^R_{P,r}(S)}
         {W_{mix}(P,r)}
  =\frac{W_{mix}(P+x_S,r+b)}{W_{mix}(P,r)}.
 \tag{5}
\]
The ratio does not depend on the newborn bit b: no component's current
probability reads that newborn record. A specified bit still contributes
its separate factor \(1/2\).

Both routes around any incomparable-birth diamond telescope to the same
terminal \(W_{mix}/W_{mix}(P,r)\), multiplying the entire \(D/4\).
Marked-order equivariance likewise survives. The posterior depends on the
complete marked order, not on a preferred natural labeling.

But (5) reweights components by their **record-dependent likelihoods**.
It need not read only \(r|_S\). In particular, an empty-precursor transition
must be independent of **all** existing record bits to satisfy the required
locality. Neither positive cylinders nor covariant path weights prove that
constraint. This is not a simple prior-weighted mixture of the current rows.

At parents n<6 the rule is held unchanged. At n=6 the common prior has
not yet been updated differently by the components, so the current row is
\(\tfrac12(\text{full-only})+\tfrac12 q^B_6\); locality still holds there.
Parent size seven is the earliest possible failing layer.

## 3. Exact posterior at the earliest test

Fix a six-event order K and a complete marking r. Let Q=K⊕1 be the
seven-event order reached by a full seventh birth, with its newborn bit c.
Here r+c denotes extension by that bit, not integer addition.
Use
\[
 b_r=q^B_{K,r}(K)=1-a_6U_6(K,r),\qquad
 U_6(K,r)=\sum_{S\subsetneq K}u^B_{K,r}(S),\qquad
 g=q^B_{Q,r+c}(\varnothing)>0.
 \tag{6}
\]
Baseline locality makes g independent of **every** bit of Q at fixed
unmarked Q. Its value and the global positive constant a6 can remain
symbolic; neither a complete M6 calculation nor a q7 table is required.
RI-38 gives \(0<b_r<1\) (indeed \(b_r>1/2\)).

Let \(\mu_6(K,r)>0\) be the held probability of the chosen complete
six-birth marked history. At the seventh birth, R=6 uses its full bridge
with weight one, whereas every R≥7 still uses baseline full weight b_r.
Thus
\[
 \mu_7^{mix}(Q,r+c)
   =\frac{\mu_6(K,r)}2\bigl(w_6+s_7b_r\bigr).
 \tag{7}
\]
For the next empty-ideal birth, R=6 gives zero because the precursor
omits the six-core. Crucially, **R=7 is now at its own full-only bridge**,
so it also gives zero. Only R≥8, with total prior \(s_8=1/4\), contributes.
For a specified eighth newborn bit d, the joint cylinder has mass
\[
 \mu_8^{mix}(Q+x_{\varnothing},r+c+d)
   =\frac{\mu_6(K,r)}4\,s_8b_rg.
 \tag{8}
\]
Dividing (8) by (7) and summing the two fair eighth bits gives
\[
 q^{mix}_{Q,r+c}(\varnothing)
    =\frac{s_8b_rg}{w_6+s_7b_r}
    =\frac{b_rg}{2(1+b_r)} .
 \tag{9}
\]
Using s7 instead of s8 in the numerator would incorrectly include the
R=7 bridge and double the answer. Different r can have different
\(\mu_6(K,r)\); these factors cancel separately in each conditional
probability. No uniform-record assumption is made.

For two record assignments r,r′, at the same K and the same seventh bit c,
\[
 q^{mix}_{Q,r'+c}(\varnothing)-q^{mix}_{Q,r+c}(\varnothing)
 =\frac{g(b_{r'}-b_r)}{2(1+b_{r'})(1+b_r)}
 =-\frac{a_6g\,[U_6(K,r')-U_6(K,r)]}
         {2(1+b_{r'})(1+b_r)}.
 \tag{10}
\]
All prefactors and denominators are strictly positive. Thus **any exact
record variation of U6 at fixed K proves a locality violation** at the
empty precursor. Every changed old mark lies outside that precursor.
No numerical value of a6 or g is needed to prove nonzero difference.

## 4. Exclusion/control and independent row identity

### Every unique-maximum core has U6=1

If K has a unique maximum m, every proper ideal excludes m, and
\(\operatorname{Max}(K)\setminus S=\{m\}\).
The deletion product in (1) reduces to
\[
 u^B_{K,r}(S)=q^{actual}_{K-m,r|_{K-m}}(S).
\]
The proper ideals of K are exactly all ideals of K−m. Summing the
normalized actual five-parent row gives
\[
 U_6(K,r)=1
 \tag{11}
\]
for every marking. In particular the six-chain cannot witness (10).
This is an exclusion theorem for all unique-maximum cores, not just
an observed lack of variation in one tested example.

### Twin-top reduction

For \(K=A_4\oplus\{x,y\}\), with two incomparable universal maxima,
let, for all individual ideals S of \(A_4\),
\[
 q(S)=q^{actual}_{A_4,r}(S),\qquad
 p(S)=q^{actual}_{A_4\oplus1,r}(S),\qquad
 v=q^{actual}_{A_4\oplus1,r}(A_4\oplus1)=1-\sum_Sp(S).
\]
The notation p(S) uses the base ideal, not the full five-parent ideal.
The top record is irrelevant: every proper five-parent ideal excludes
the unique top, and its full complement is a sum of those proper weights.

The six-parent proper ideals are the base ideals S and the two ideals
\(A_4\cup\{x\}, A_4\cup\{y\}\). For the former, the deletion product has
two five-parent factors and one four-parent denominator, giving
\(u_6(S)=p(S)^2/q(S)\). For either latter ideal it gives v.
Consequently
\[
 U_6(K,r)=\sum_{S\text{ ideal }A_4}\frac{p(S)^2}{q(S)}+2v
        =1+\sum_S\frac{(q(S)-p(S))^2}{q(S)}.
 \tag{12}
\]
The last equality uses \(\sum_Sq(S)=1\). All q(S) are positive.
This independently checks the deletion-product arithmetic and shows that
the two top bits cannot affect U6. It does **not** by itself establish
variation in the four base bits; that is the bounded exact question.

## 5. Prospective bounded witness domain and execution contract

The only new six-cores whose rows may be evaluated are, in predecessor-bit
notation with labels 0 through 5:
\[
 K_1=(0,1,0,0,15,15),\qquad
 K_2=(0,1,1,0,15,15),
\]
and the unique-maximum control
\[
 K_{chain}=(0,1,3,7,15,31).
\]
Evaluate all 64 record assignments on each: **128 selected search rows**
plus **64 chain control rows**. Record integers use bit i for vertex i.
There is no additional core, adaptive fallback, random sample, optimizer,
global six-parent inventory, M6 value or baseline q7 table.
If both search cores have constant U6, the result is bounded no-witness,
not global acceptance of locality.

The actual held rows are reconstructed through published RI-74
`rebuild_prefix()` and `prefix_row()`. The latter reconstructs q5 from
RI-63's accepted canonical alpha and its actual strict mix; RI-63's
ordinary `row()` stops at parent size four and must not substitute for q5.
The inherited complete terminal-six catalogue replay is allowed solely as
verification of that accepted prefix, **not a newly selected parent-six
search**. Replaying the certificate is not running an optimizer.

Frozen accepted helper identities:

- RI-74 check.py:
  `edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c`.
- RI-63 check.py:
  `39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b`.
- RI-63 CERTIFICATE.json:
  `f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b`.
- RI-41 CERTIFICATE.json:
  `3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969`.

The new checker must pin that closure before helper loading, then reconstruct
only the selected six-parent potentials by the alternating maximal-deletion
formula with correctly transported records. It must compare the independent
twin-top expression (12), verify top-bit irrelevance, the chain identity,
and preserve each labeled ideal. All resulting record rows and any differing
pair must be retained exactly; no float threshold defines a witness.

Before witness execution, freeze source/dependency identities, the stated
domain, exact commands, copied source destinations and resource envelope.
Use standard-library CPython 3.14 normal and optimized modes, **120 seconds /
512 MiB sampled RSS per run**, with explicit checks not removed by -O.
Durable sources, stdout/stderr and receipts belong only under
`/Volumes/AI_DATA/development/det-review-evidence/ri77-qr/`, never temporary
directories. Original and copied inputs must retain their pins.

## 6. Exact counterexample on the prescribed actual-prefix rows

The bounded calculation found **record variation in K2**. K1 has one
constant U6 value over its 64 markings, and the chain has U6=1 throughout.
No other search core was introduced.

| Fixed core | Marked rows | Proper ideals per row | Distinct U6 values |
|---|---:|---:|---:|
| K1=(0,1,0,0,15,15) | 64 | 14 | 1 |
| K2=(0,1,1,0,15,15) | 64 | 12 | 2 |
| Six-chain | 64 | 6 | 1 |

At K2, take r0=0 (all six records zero) and r1=1 (only vertex 0's
record changed to one). Both six-birth histories have strictly positive
held-prefix probability. Write \(U_0=N_0/D_0\), \(U_1=N_1/D_1\), with
these exact integers, also retained in the [certificate](CERTIFICATE.json):

```text
N0 = 1042733828363819872001555378483902662033559831056935412489416465520361605875614708170883481
D0 = 301628639840079740796010667996291572501091864710470127977754143817122579550700613884263908
N1 = 124646651937506512654044130816358037077060592463438674593349339803809842615720438501165217
D1 = 23920471889344787217381332543677521743714313375815649677608549257661280800641808453313466
```

Their exact difference is
\[
 U_1-U_0
   =\frac{33685055514151347365383342865}
           {19206178020939013358718419748}>0.
 \tag{13}
\]
The independent weighted-square calculation, using actual q5 reconstructed
directly from RI-63's canonical alpha and strict mix, agrees with the
deletion-product result on **all 192 declared U6 values**. The two top bits
are irrelevant as predicted by (12). This is not a half-scale replacement
of the held five-parent law.

Now keep the seventh bit c=0 and the unmarked order Q=K2⊕1 fixed.
The two resulting seven-record assignments differ only at old vertex 0,
outside the empty precursor. Because \(a_6>0\), \(g>0\) and all
\(1+b_r>0\), (10) and (13) give
\[
 q^{mix}_{Q,r_1+0}(\varnothing)
       -q^{mix}_{Q,r_0+0}(\varnothing)
 =-\frac{a_6g}{2(1+b_{r_1})(1+b_{r_0})}
       \frac{33685055514151347365383342865}
            {19206178020939013358718419748}<0.
 \tag{14}
\]
This proves the required incompatibility without evaluating M6, a6, g or
any q7 row. Specifying either eighth newborn bit multiplies both
probabilities by the same \(1/2\); the violation persists for the full
scalar-passive maps on every nonzero D.

**Disposition: the specified marginalized random-cutoff mixture fails
strict precursor-record locality, first witnessed at parent size seven.**
Its positive cylinders and covariance remain valid, but do not make it
an admissible law in the required local class. This is a counterexample
for the specified baseline and cutoff prior, not a no-go theorem for
every latent-state extension or every possible mixture.

## 7. Scope of the rejection

The posterior formula (9), exact witness (13)–(14), and unique-maximum
exclusion (11) complete this assigned compatibility question.
No eventual finite-core or other asymptotic conclusion is promoted here.
A covariant history mixture can be a legitimate mathematical law without
belonging to the required local class. Retaining the sampled R as
additional state would be a different object, not an unannounced repair
of the marginalized rule.

No uniqueness, informative quantum dynamics, nondegenerate geometry,
gravity or observation claim is made. Accepted laws, RET, measurement,
coordinator records and git/index remain untouched by this worker.
Only this note and the bounded checker/certificate are reserved for handoff;
no successor is authorized here.

## 8. Verification and handoff

The prospective domain/helper/source/resource/command freeze preceded the
first witness run. Independent source review identified the cached RI-74
helper interface issue before execution:
its decorated row function needed unwrapping to access the live namespace.
That pre-execution defect was corrected, both reviewers reconciled the
final source, and the unexecuted draft freeze was explicitly superseded.
Retained prospective draft copies are not represented as execution evidence.

The final source and saved certificate are frozen at these SHA-256 identities:

- `check.py`, 18,863 bytes:
  `d732d5dcd20bb82af6098ae864598b0492ccd635628ef315c40dfed877454483`.
- `CERTIFICATE.json`, 371,353 bytes:
  `b959c82edb9233b71647e7cf09534f607da10cb2f1cefeb6b86e2ed36eb297a0`.

The checker author and QR worker each replayed the saved certificate in
standard-library CPython 3.14.0, both normal and optimized. The copied checker
was invoked with `/opt/homebrew/bin/python3 -I -S -B`, adding `-O` for the
optimized run; complete supervised command arrays were frozen beforehand.
Each replay verified **192 marked rows, 2,048 proper slots and 4,864 deletion
factors**, with **20 new intended-reason refusal controls** and **15 inherited
prefix controls**. The inherited controls are not counted as new tests.

| Saved-certificate replay | Seconds | Peak sampled RSS |
|---|---:|---:|
| Author normal | 9.197 | 126,156,800 bytes |
| Author optimized | 9.127 | 126,205,952 bytes |
| QR worker normal | 9.193 | 123,072 KiB |
| QR worker optimized | 9.222 | 123,088 KiB |

All four runs exited zero without a resource stop. Their stdout was
byte-identical (3,023 bytes, SHA-256
`79d77255e3316b70bd7dbe5a35c0caffb4b814504c175c04999de25dcaf6e922`),
as was stderr (951 bytes, SHA-256
`803475c36d8bd4c5c4d0e7edce6bd72e43335efae5306127cbd412adf6c9360b`).
The six-file executable/certificate dependency closure retained its original
and copied pins. These are bounded sampled-RSS receipts, not continuous
memory measurements or a theorem about resource use on other inputs.

The worker also ran an independently written weighted-square calculation,
importing RI-63 directly rather than this checker or RI-74's prefix wrapper.
Its normal and optimized runs took 9.115 and 8.882 seconds, with peak sampled
RSS 121,776 and 121,744 KiB. Both exited zero without a resource stop and
produced identical output: stdout 23,286 bytes, SHA-256
`6d1fd36efb708cfc7530caf5e101c35c338569b9a363bd85fecd242125c3c8ca`;
stderr 503 bytes, SHA-256
`116be90d3a1910a36d726a40605a9bbf8ac0274864c10801247891649c2ea571`.
All **192 exact sums** agree with the saved certificate. This independently
checks the new-row arithmetic using the same accepted prefix; it does not
claim an independent derivation of that prefix. A separate reconciliation
re-summed every saved proper-potential row and checked the printed witness
integers and exact difference.

Two mathematical reviewers read the complete proof, reconciled the corrected
checker source, and checked the final witness. This is source/proof review
and exact rational execution, not a proof-assistant formalization.

Durable evidence is retained under:

- `/Volumes/AI_DATA/development/det-review-evidence/ri77-qr/author-wM7dnW/`:
  final prospective freezes, copied six-file closure, witness-generation
  receipt, saved-certificate replay receipts and output comparison.
- `/Volumes/AI_DATA/development/det-review-evidence/ri77-qr/worker-n4ib7q/`:
  prospective command/source freezes, independent arithmetic source and
  normal/optimized receipts, saved-certificate receipts, exact reconciliation,
  source-hygiene check, review record and handoff manifest.

No additional core, six-parent inventory, global M6, q6/q7 probability table,
optimizer or successor was evaluated in this packet.

## 9. Coordinator adjudication

The coordinator read the complete proof and checker, verified all 37 external
handoff evidence identities and the six-file machine dependency closure, and
replayed copied sources in normal and optimized modes under a prospectively
frozen 120-second/512-MiB sampled-RSS envelope. Both runs exited zero without
a resource stop in 9.215/9.293 seconds, with peak sampled RSS 123200/123040 KiB.
Their stdout and stderr exactly match the worker identities above. All original
and copied machine-source pins remained fixed before and after each run.

A separate coordinator reviewer read the proof and both arithmetic sources,
independently re-summed all 192 retained certificate rows without executing
worker code, and reconciled the 2048 slots, 4864 factors and exact positive
record difference. The counterexample is accepted within the stated candidate
class; this does not establish a no-go theorem for every latent construction.

Fresh coordinator evidence is retained under
`/Volumes/AI_DATA/development/det-review-evidence/ri78-root-20260924T2234/ri77-replay/`.
`ROOT_REPLAY_FREEZE.json` is 1631 bytes, SHA-256
`73e40c27f429e6d4b5f8e1caee9c7d1230a713bf1e79e9bc928a5f93389678ef`.
The checker and certificate above remain unchanged. Publication and subsequent
assignments belong to the coordinator records, not this fixed witness.
