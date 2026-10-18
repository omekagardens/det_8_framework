# RI-79 — does delaying the first cutoff preserve record locality?

24 September 2026 UTC. **Exact delayed-cutoff locality counterexample;
independently accepted by the coordinator.** This is one test of
persistence through the next baseline layer, not authorization for an
iterative cutoff-by-cutoff programme.

## 1. Question and held law

[RI-77](../native_growth_random_cutoff_locality_v1/LOCALITY.md) rejects its
specified latent-cutoff mixture at parent size seven. The present question
is whether postponing the **first** possible cutoff to seven removes that
obstruction. It does not change the baseline, held prefix or locality rule.

Use B exactly as in RI-77: the actual accepted strict marked rows at
parents n<6, including RI-63's actual strictly mixed q5, followed at n≥6
by the [RI-38](../native_joint_growth_extension_criterion_v1/CRITERION.md)
common half-scale continuation
\[
 u^B_{P,r}(S)=
 \prod_{\varnothing\ne A\subseteq\operatorname{Max}(P)\setminus S}
 q^B_{P-A,r|_{P-A}}(S)^{(-1)^{|A|+1}},\qquad S\subsetneq P,
\]
\[
 U_n(P,r)=\sum_{S\subsetneq P}u^B_{P,r}(S),\quad
 M_n=\max_{|P|=n,r}U_n(P,r),\quad
 a_n=\frac1{2(1+M_n)},
\]
\[
 q^B_{P,r}(S)=a_nu^B_{P,r}(S)\ (S\subsetneq P),\qquad
 q^B_{P,r}(P)=1-a_nU_n(P,r).
 \tag{1}
\]
Every sum retains individual labeled ideals. Global maxima in this
definition range over complete finite marked tables, not the observed
record or selected rows. No such new table or maximum is computed here.
The baseline is strictly positive, normalized, equivariant and
precursor-record-local by the inherited construction. At parent sizes n≥6,
full probabilities are greater than 1/2. Newborn records remain fair
immutable bits, with full passive maps
\(\mathcal B_{S,b}(D)=q_{P,r}(S)D/2\).

For each cutoff R, use the
[RI-74](../native_growth_plancherel_graft_v1/PLANCHEREL_GRAFT.md) intrinsic
R-core graft: B at parents n<R, full-only bridge at n=R, then the
R-core Ferrers/Plancherel rule with full-only fallback off-family. The
cutoff remains latent and is marginalized, not retained in the local state.
The prior and this graft target are choices, not uniquely derived DET laws.

## 2. General first-atom posterior criterion

Let an independent integer-valued cutoff prior have first positive atom
at m≥6. Write
\[
 w_m>0,\quad w_R=0\ (R<m),\quad
 w_R\geq0,\quad\sum_Rw_R=1,\quad
 s_j=\sum_{R\geq j}w_R,
 \qquad s_{m+2}>0.
 \tag{2}
\]
Neither rational weights nor unbounded support are assumed. Normalization
and finite-prefix consistency follow by mixing component histories.
Inherited path-weight diamonds and marked-order equivariance survive
through the terminal-history weight construction of RI-77. On histories
of positive mixture weight the conditional full-map products telescope.
No conditional rule at zero-weight histories is supplied by a weight ratio.
These facts do not establish precursor-record locality. Without unbounded
cutoff support, this note does not assert positivity of *every* finite
mixture cylinder.

Fix a naturally labeled m-event order K with marking r and a particular
baseline history ending there. Put Q=K⊕1 and append the same newborn bit c
in every comparison. Write \(r\mathbin{\|}c\) for record extension, and let
\[
 b_r=q^B_{K,r}(K)=1-a_mU_m(K,r),\qquad
 g=q^B_{Q,r\mathbin{\|}c}(\varnothing)>0.
 \tag{3}
\]
At fixed unmarked Q, baseline locality makes g independent of every
record bit. The common positive scale a_m likewise does not change when
r changes. Every component shares the same B history through m births,
whose probability is \(\mu_m^B(K,r)>0\).

At the next full birth, the R=m component uses its bridge; every R≥m+1
uses baseline full probability b_r. At the following empty-precursor
birth, the R=m graft cannot omit its core, and R=m+1 is itself at its
full-only bridge. Only the R≥m+2 tail contributes. For a specified next
newborn bit d,
\[
 \mu_{m+1}^{mix}(Q,r\mathbin{\|}c)
 =\frac{\mu_m^B(K,r)}2(w_m+s_{m+1}b_r),
\]
\[
 \mu_{m+2}^{mix}(Q+x_\varnothing,r\mathbin{\|}c\mathbin{\|}d)
 =\frac{\mu_m^B(K,r)}4s_{m+2}b_rg.
 \tag{4}
\]
All factors needed for these tested cylinders are positive. Dividing and
summing over the two fair next bits gives
\[
 q^{mix}_{Q,r\mathbin{\|}c}(\varnothing)
 =\frac{s_{m+2}b_rg}{w_m+s_{m+1}b_r}.
 \tag{5}
\]
Using s_(m+1) instead of s_(m+2) in the numerator would incorrectly count
the next bridge. Different markings may have different baseline history
likelihoods; those cancel separately in each conditional probability.

For two markings of the same K, define \(\Delta U_m=U_m(K,r_1)-U_m(K,r_0)\).
Exact subtraction in (5) gives
\[
 \Delta q^{mix}(\varnothing)
 =-\frac{s_{m+2}g w_m a_m\,\Delta U_m}
 {(w_m+s_{m+1}b_{r_1})(w_m+s_{m+1}b_{r_0})}.
 \tag{6}
\]
Consequently **any record variation in U_m obstructs locality for every
prior satisfying (2)**. Every changed record is outside the empty
precursor. Specifying the newborn bit multiplies (6) by 1/2; the full
passive maps still differ on every nonzero D.

Parents n<m remain B. At n=m, the components' likelihoods are still
identical, so the current row is the fixed prior-weighted combination
\(w_m\,\mathbf1_{S=K}+s_{m+1}q^B_{K,r}(S)\), which is local. Thus n=m+1
is the earliest possible failing layer. If s_(m+2)=0 this empty-precursor
test says nothing about other transitions or locality of that prior.

## 3. The only new coefficient domain

Fix, in predecessor-bit notation,
\[
 A=(0,1,1,0),\quad P_5=A\oplus1=(0,1,1,0,15),
\]
\[
 K_6=A\oplus\{x,y\}=(0,1,1,0,15,15),\qquad
 K_7=A\oplus\{x,y,z\}=(0,1,1,0,15,15,15).
 \tag{7}
\]
The appended tops are pairwise incomparable and above all of A. Only
record assignments r0=0 and r1=1 are used: they differ at vertex 0, and
every other bit, including the appended top bits, is zero. K6 data are
inherited from RI-77; K7 is used symbolically, not enumerated as a new
probability row or a seven-parent inventory.

For every individual base ideal S, define the actual held quantities
\[
 q_r(S)=q^{actual}_{A,r}(S),\quad
 p_r(S)=q^{actual}_{P_5,r}(S),\quad
 v_r=q^{actual}_{P_5,r}(P_5)=1-\sum_{S\text{ ideal }A}p_r(S).
 \tag{8}
\]
All q and p are strictly positive; \(\sum_Sq_r(S)=1\). The unique top's
record cannot change any proper p_r(S), because it lies outside every
proper ideal; the normalized full complement is therefore independent
of that top record too. This establishes the top-record invariance used
in the deletion identities without evaluating additional markings.

RI-77's twin-top identity is
\[
 U_{6,r}=\sum_S\frac{p_r(S)^2}{q_r(S)}+2v_r.
 \tag{9}
\]
Its retained records 0 and 1 establish
\[
 \Delta U_6
 =\frac{33685055514151347365383342865}
 {19206178020939013358718419748}>0,\qquad
 v_0=v_1=
 \frac{3654565503014415437810979130563691429}
 {131564358116892863863128623607792891444}.
 \tag{10}
\]
The equality of v is specific to this selected pair; it is not a general
record-independence claim. The new calculation must independently
reconstruct (8), reconcile (9)–(10) with the pinned RI-77 certificate, and
then calculate only
\[
 T_{3,r}=\sum_S\frac{p_r(S)^3}{q_r(S)^2},\qquad
 \Delta T_3=T_{3,1}-T_{3,0}.
 \tag{11}
\]

## 4. Triple-top deletion identity, with no selected numerical scale

Let **a=a6**, the single global baseline scale at parent size six. This
is not a7, which appears later in b for the first-atom-seven posterior.
The proper ideals of K7 split into exactly three types:

| Precursor | Separate labeled slots | Potential from maximal deletions |
|---|---:|---|
| S, an ideal of A (including A) | Every individual base ideal | \((a p_r(S)^2/q_r(S))^3 q_r(S)/p_r(S)^3=a^3p_r(S)^3/q_r(S)^2\) |
| A plus one top | 3 | \((a v_r)^2/v_r=a^2v_r\) |
| A plus two tops | 3 | \(q^B_{K_6,r}(K_6)=1-aU_{6,r}\) |

For a base ideal, deleting each of the three singleton top sets supplies
a six-parent proper factor; deleting the three pairs supplies the
five-parent denominators; deleting all three supplies the four-parent
factor. For a one-top ideal the two omitted maxima give two six-parent
proper factors divided by the five-parent full value. For a two-top
ideal only one maximum is omitted. The remaining twin-top orders are
isomorphic with the same transported base records. No top-subset or
isomorphism multiplicity is divided out.

Summing these contributions proves
\[
 U_{7,r}(a)=3-3aU_{6,r}+3a^2v_r+a^3T_{3,r}.
 \tag{12}
\]
This is a symbolic identity for the actual baseline, not an exact inverse
of an inserted numerical operator. The admissible global scale satisfies
\[
 0<a=\frac1{2(1+M_6)}\leq
 a_\star:=\frac1{2(1+\max(U_{6,0},U_{6,1}))},
 \tag{13}
\]
because both selected marked six-parent rows occur in the complete table
defining M6. The upper bound does not substitute a selected maximum for
the actual global maximum.

Using the *verified pair-specific* \(\Delta v=0\), subtract (12):
\[
 \Delta U_7(a)=a[-3\Delta U_6+a^2\Delta T_3].
 \tag{14}
\]
If \(\Delta T_3\leq0\), this is negative for every a>0. Otherwise it is
negative throughout \(0<a\leq a_\star\) whenever the exact rational
margin
\[
 C:=3\Delta U_6-a_\star^2\Delta T_3>0.
 \tag{15}
\]
These are sufficient tests, not an assumption that the margin will pass.
If \(\Delta T_3>0\) and C=0, the upper-bound endpoint is a possible zero.
If C<0, the zero \(\sqrt{3\Delta U_6/\Delta T_3}\) lies inside the bounded
interval. Either failure leaves the actual global scale unresolved;
neither permits a locality acceptance or an enlarged search. No M6, a6,
M7, a7, g or q6/q7 probability value is evaluated.

## 5. Frozen execution and stopping contract

The permitted new arithmetic is (8)–(15) for the two specified records
only. Use actual inherited q4/q5, never a half-scale replacement of q5.
RI-74's pinned `rebuild_prefix()` and `prefix_row()` reconstruct the
canonical strict prefix; its cached row function must be unwrapped to
access the live helper namespace. The inherited terminal-six catalogue
replay verifies that already accepted prefix; it is not a new search.
An independent check may reconstruct the same two rows directly from
RI-63's accepted alpha and strict mixture.

The checker must pin these accepted inputs before loading helpers:

- RI-74 checker:
  `edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c`.
- RI-63 checker:
  `39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b`.
- RI-63 certificate:
  `f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b`.
- RI-41 certificate:
  `3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969`.
- RI-77 certificate:
  `b959c82edb9233b71647e7cf09534f607da10cb2f1cefeb6b86e2ed36eb297a0`.

Freeze the exact new domain, source/helper identities, copied source
destinations, normal/optimized commands and resource envelope before
coefficient execution. Every execution uses copied standard-library
CPython, explicit checks retained under `-O`, a 120-second wall limit and
512-MiB sampled-RSS limit, with durable external receipts under
`/Volumes/AI_DATA/development/det-review-evidence/ri79-qr/`.
Both original and copied sources must retain their frozen identities.

If the sign test succeeds, apply (6) with m=7 and the same eighth bit to
reject all these first-atom-seven priors with s9>0 at parent size eight.
If it does not, report the precise remaining scale/sign question and stop.
No optimizer, new global six-parent inventory, q6/q7 probability table,
other core, other record pair or iterative cutoff search is authorized.
No accepted source, RET, measurement, ledger, coordinator record or git
operation belongs to this worker's reservation.

## 6. Exact result: delaying to seven does not remove the obstruction

The frozen two-record calculation found \(\Delta T_3>0\), exactly
\[
 \Delta T_3=
 \frac{22200459560303236956690380575518249944678574035909267006030927620375905653359765}
 {1727823478280625677043847888839039892542722676306757007278067053440791675997786}.
 \tag{16}
\]
The [certificate](CERTIFICATE.json) retains both complete q4/q5 row pairs,
every labeled quadratic/cubic term, both U7 coefficient vectors, the
selected-row upper bound a_star, and the resulting margin (15). Its exact
positive margin is \(C=N_C/D_C\), with

```text
N_C = 17028308207156976815469767925177258129467622898393383694125836628921317703238651364412789510794722667353913052426035213513438463956666478012780755273855140775127209833684826930943453558335088621263901524629191562825
D_C = 3288381299815858873415829209944872248101120668461097303310045427869075294509792042967290369515877839282506667319293705543312879512617245980783116838036168591814061620173085562764701757632042715986920143287054196868
```

The independent calculation, reconstructing actual strict q5 directly from
RI-63 rather than importing the RI-74 wrapper or this checker, agrees on
the rows and coefficients. Its exact integer cross-product also confirms
the sign of C. Consequently, for the unknown actual global a=a6,
\[
 \Delta U_7(a)
 =-a[3\Delta U_6-a^2\Delta T_3]
 \leq-aC<0
 \qquad(0<a\leq a_\star).
 \tag{17}
\]
No global maximum or selected numerical a was needed. This is a uniform
strict sign on the whole allowed interval, not an observation at a fitted
scale.

Apply (6) with **m=7**, K=K7, and the same eighth newborn bit c=0.
The two eight-record orders Q=K7⊕1 differ only at old vertex 0. Now
b_r=1-a7 U7,r(a6), with a7 positive and separate from a6. Since
\(\Delta U_7<0\), the empty-precursor probability has
\(\Delta q^{mix}(\varnothing)>0\) for **every independent cutoff prior
whose first positive atom is seven and whose tail s9 is positive**.

**Disposition: rejected in the required precursor-record-local class,
with an exact parent-eight counterexample.** Delaying the first cutoff
from six to seven does not repair locality for this fixed baseline and
graft construction. The failure is at the earliest possible layer for
that prior class. Both test histories have positive probability.

This does not decide first atoms beyond seven, priors with s9=0,
state-dependent cutoff choices, an explicitly retained latent cutoff,
different baselines, or other graft laws. It does not refute normalization
or covariant history weights. No successive-cutoff search or alternative
repair is started here.

## 7. Verification and handoff

The domain, complete proof/source review, original/copied input pins,
commands and resource envelope were frozen before the first coefficient
execution. Both proof reviewers approved the symbolic triple-top and
general-prior posterior derivations and the full bounded source. One
prospective wording correction restricted the greater-than-one-half
full-probability claim to n≥6, rather than the held prefix.

The final machine artifacts are frozen at these SHA-256 identities:

- `check.py`, 359 lines / 17,574 bytes:
  `2f394aedf1c9c9c4952eda7c826eb4faf19b83b57c5f8236b8b44ac1e8be8a48`.
- `CERTIFICATE.json`, 14,652 bytes:
  `d06001c27ac1ed12a6ba7c5af7970524be825ce70eac50e8b34ef34603906143`.

The checker author and QR worker each replayed the saved certificate in
standard-library CPython 3.14.0, normal and optimized. Exact supervised
commands were frozen beforehand, invoking the copied checker with
`/opt/homebrew/bin/python3 -I -S -B` and adding `-O` for optimized mode.
Every replay verified four held marked rows, 42 labeled probability slots,
20 labeled base-ideal term pairs (40 moment values) and two symbolic
coefficient vectors. There were
**24 new intended-reason refusal controls**, separately from **15 inherited
prefix controls** and 69 inherited canonical lexicographic stages.

| Saved-certificate replay | Seconds | Peak sampled RSS |
|---|---:|---:|
| Author normal | 9.179 | 126,877,696 bytes |
| Author optimized | 9.072 | 124,485,632 bytes |
| QR worker normal | 9.136 | 123,840 KiB |
| QR worker optimized | 9.083 | 122,208 KiB |

All four runs exited zero with no 120-second / 512-MiB resource stop.
Their stdout was byte-identical: 5,283 bytes, SHA-256
`8b81a6332a708a0049d56ab14517eb67553937aa0837cc16c501d1b926fd9705`.
Their stderr was likewise identical: 816 bytes, SHA-256
`482acd90a5bac8aeebaf8eed07e8239525cfc8f304aa3e5ffa2880043b4bdc3d`.
All seven original/copied executable and certificate inputs retained their
frozen identities. Sampled RSS is not a continuous measurement or an OS
allocator hard-cap guarantee.

The independent RI-63-direct calculation also passed in normal and optimized
modes: 9.029 / 8.985 seconds, with sampled peaks 121,792 / 121,088 KiB.
Its outputs were identical: stdout 6,358 bytes, SHA-256
`c6c3c369c277176208541e3f7454c95b3c8060093466dc5b1ac76519294d9ec4`;
stderr 503 bytes, SHA-256
`116be90d3a1910a36d726a40605a9bbf8ac0274864c10801247891649c2ea571`.
Both exited zero without a resource stop and retained their input pins.
This independently checks the new arithmetic using the same accepted
prefix; it does not independently derive that prefix.

A separate exact saved-data reconciliation compared all four held rows
and both coefficient vectors, recomputed all 20 labeled quadratic/cubic
term pairs and the scale bound/margin, and confirmed the strict sign. Both
mathematical reviewers read the full result-bearing proof and independently
checked its saved coefficients without rerunning helpers. The verification is exact
rational arithmetic and source/proof review, not a proof-assistant proof.

Durable evidence is retained under:

- `/Volumes/AI_DATA/development/det-review-evidence/ri79-qr/author-Q9bcLx/`:
  prospective source/command freezes, copied seven-file closure, witness
  generation, saved-certificate receipts and output/pin comparisons.
- `/Volumes/AI_DATA/development/det-review-evidence/ri79-qr/worker-svKfqO/`:
  prospective proof snapshot and execution freezes, independent source and
  receipts, saved-certificate receipts, exact reconciliation, source-hygiene
  check, review record and handoff manifest.

The worker handed off this three-file packet for adjudication. No new core,
record pair, global table, numerical baseline scale, q6/q7 probability row,
optimizer or successor was introduced. No geometry, gravity, informative
quantum dynamics or empirical correspondence conclusion is made. Worker
verification is distinct from the coordinator adjudication below and publication.

## 8. Coordinator adjudication

Root reviewed the complete proof, checker and independent direct-alpha source,
verified all 38 worker evidence entries and seven machine dependencies, and
replayed copied sources in both modes under a prospective 120-second/512-MiB
sampled-RSS freeze. Normal/optimized runs exited zero in 9.162/9.214 seconds,
with sampled peaks 122912/122832 KiB and no resource stop. Their complete
stdout/stderr exactly match the worker identities above. Original/copied source
pins remained unchanged before and after each run.

Root separately re-summed the certificate's 42 probabilities, 20 moment pairs
and two coefficient vectors, and checked the exact endpoint margin and printed
integers without importing worker code. An independent coordinator reviewer
read the complete proof/source, independently reconciled this saved arithmetic,
and verified the worker and root evidence bindings. The general-prior posterior,
labeled multiplicities, positive witness histories and distinct a6/a7 scales
pass review. The counterexample is accepted for exactly the stated prior and
baseline/graft class; later first atoms and constructive geometric laws remain
open.

Fresh evidence is retained under
`/Volumes/AI_DATA/development/det-review-evidence/ri79-root-20260924T230503Z/`.
The prospective `replay/ROOT_REPLAY_FREEZE.json` is 3290 bytes, SHA-256
`6324499d17e7c1f0f2e4fdebc07f6b9e7e9c8078d192fc8b6fb59937d25f4c3a`.
`INDEPENDENT_RI79_MATHEMATICAL_REVIEW.json` is 5832 bytes, SHA-256
`dbe51e01a04e57a46b0c00a72c5422838cfdf6997c150eb44dda8f16adc789b5`.
The machine files remain exactly those pinned in section 7. The coordinator
records govern publication and any separately reviewed successor assignment.
