# RI-82 — one frozen first-departure support and width-bias design

25 September 2026 UTC. **Design independently accepted by the coordinator.
Actual coefficient feasibility not evaluated.** This note freezes one
support, its complete affected-parent closure and one intrinsic width
target. No checker, coefficient/probability execution, solver, numerical
search or adopted-law change is authorized by the note itself.

## 1. Baseline and the finite first-departure question

Use the actual [RI-77](../native_growth_random_cutoff_locality_v1/LOCALITY.md)
and [RI-79](../native_growth_delayed_cutoff_locality_v1/LOCALITY.md) baseline
B: the accepted strictly positive marked rows at parent sizes n<6,
including the actual RI-63 strictly mixed q5, and the common half-scale
continuation at n≥6. In particular, for every six-parent proper ideal,
\[
 q_B(P,r,S)=a_6u(P,r,S),\qquad
 a_6=\frac1{2(1+M_6)}>0.
 \tag{1}
\]
M6 is the complete marked proper-potential row maximum, not a selected-row
maximum. Neither it nor a numerical a6 is evaluated in this design or
required for the proposed bounded test. The deletion potentials u use the
actual inherited q4/q5 law, not a replacement boundary or generic mix.

Apply the simultaneous harmonic equations of
[RI-81](../native_growth_local_mixture_criterion_v1/MIXTURES.md) for the
first layer allowed to change. Set h(P)=1 for every order with |P|≤6.
At size seven, set
\[
 h_7(T_j)=1+\epsilon z_j\quad(j=1,2,3),\qquad
 h_7(H)=1\quad([H]\notin\mathcal T),
 \tag{2}
\]
where the fixed support \(\mathcal T\) is specified below. The values are
unmarked isomorphism-class values, not values only on the displayed
labelings. **No h at sizes eight or greater is prescribed.** Setting all
those future values back to one would generally fail harmonicity at a
modified seven-event parent and is not an implicit continuation.

The required six-parent equations are, for every complete record row,
\[
 \sum_{S\text{ individual ideal of }P}
 q_B(P,r,S)h_7(P+S)=1.
 \tag{3}
\]
The question is whether this one support has a nonzero direction satisfying
all of (3), with positive h7 and a specified positive width bias. A signed
null vector alone is not success.

## 2. One fixed, intrinsic three-class support

C_k denotes the k-chain, A_k a k-antichain, and the ordinal sum X⊕Y places
every element of X below every element of Y. The disjoint union symbol
means no cross relations. Freeze the **ordered variable list**
\(\mathcal T=(T_1,T_2,T_3)\):

| Variable | Intrinsic class | Natural predecessor-bit representative | Width |
|---|---|---|---:|
| T1 | C4⊕A3 | (0,1,3,7,15,15,15) | 3 |
| T2 | C5⊕A2 | (0,1,3,7,15,31,31) | 2 |
| T3 | C4⊕(C2 disjoint A1) | (0,1,3,7,15,15,31) | 2 |

Bit i denotes vertex i in a predecessor mask. Each support member has at
least two maximal vertices. The classes are pairwise distinct: width
separates T1, while the maximal-vertex past-size multisets of T2 and T3
are {5,5} and {4,5}. The variable order is T1,T2,T3 even though their
canonical tuples have a different lexicographic order.

These are the three non-chain suffix orders on three vertices above a
fixed four-chain that have at least two maxima. This freezes a small
coupled comparison between a three-way antichain suffix and narrower
two-maximal suffixes. Width is an intrinsic maximum-antichain statistic;
there is no supplied metric, coordinate mesh or manifold target.

Canonicalization here means the lexicographically least predecessor tuple
over all natural labelings of the same finite order. The representatives
above use that convention. For T3 the possible suffix tuples, after its
forced four-chain, are (15,15,31), (15,15,47) and (15,31,15), so its listed
tuple is the least one. **Every isomorphic realization belongs to the
support**, not only a literal tuple match. No later support enlargement
or adaptive family sweep is part of this design.

## 3. Complete affected six-parent closure and labeled multiplicities

Deleting the new maximal vertex from any supported child must recover its
parent. Delete **every** maximal vertex of each support representative,
then quotient only the resulting unmarked parent classes:

| Child | Maximal vertices | Deleted vertex | Resulting parent class |
|---|---|---|---|
| T1 | 4,5,6 | Any of 4,5,6 | P_A=C4⊕A2=(0,1,3,7,15,15) |
| T2 | 5,6 | Either of 5,6 | P_B=C6=(0,1,3,7,15,31) |
| T3 | 5,6 | 5 | P_B |
| T3 | 5,6 | 6 | P_A |

These seven deletion roles give exactly two affected parent isomorphism
classes. If any other parent could produce a supported child, an
isomorphism to that child would send the newborn to one of its maxima,
and deleting it would put the parent in this list: a contradiction.
Thus **all other six-parent equations are unchanged**. Earlier parents
are unchanged because both their parent and child h values are one.

Backward deletion counts are not forward transition multiplicities.
The complete individual-ideal lists are
\[
 \mathcal I(P_A)=(0,1,3,7,15,31,47,63),\qquad
 \mathcal I(P_B)=(0,1,3,7,15,31,63).
 \tag{4}
\]
Their entire supported forward sublists are:

| Parent | Individual precursor mask | Child variable |
|---|---:|---|
| P_A | 15 | T1 |
| P_A | 31 | T3 |
| P_A | 47 | T3 |
| P_B | 31 | T2 |
| P_B | 15 | T3 |

In particular the two T3 slots of P_A must be added, not merged into one
transition or divided by an automorphism factor. Conversely T1 has three
backward deletion roles but only one forward ideal of P_A. The two listed
P_A births of T3 are isomorphic children even though one natural tuple
uses the alternative suffix (15,15,47).

All remaining ideals in (4), including each full ideal 63, have h7=1 and
zero perturbation coefficient. A full birth is above every old vertex
and gives a unique maximal vertex; hence **no support child is full-birth**.
Subtracting the baseline normalization from (3), taking epsilon nonzero
and using (1), therefore gives exactly
\[
 \sum_{S:\,[P+S]\in\mathcal T}u(P,r,S)z_{[P+S]}=0.
 \tag{5}
\]
The same positive global a6 cancels. No row-specific scale, numerical M6
or full-birth complement evaluation is substituted in this argument.

## 4. All marked rows reduce to two balances for each base marking

Use the fixed lower chains
\[
 C_4=(0,1,3,7),\qquad C_5=(0,1,3,7,15).
\]
For each of the **16** complete four-bit assignments xi=0,…,15, let
\[
 q_\xi=q^{actual}_{C_4,\xi}(15),\qquad
 p_\xi=q^{actual}_{C_5,\xi}(15),\qquad
 v_\xi=q^{actual}_{C_5,\xi}(31),\qquad
 \alpha_\xi=\frac{p_\xi^2}{q_\xi}.
 \tag{6}
\]
The unique fifth vertex has record zero in these evaluation representatives.
Every proper ideal of C5 excludes that top; precursor-record locality
makes each proper probability independent of its record. Its normalized
full complement v therefore also ignores that record. This is a proof of
top-bit irrelevance, not a test on only a few top assignments.

For P_A, deleting either omitted maximum at S=15 supplies p_xi, and
deleting both supplies the denominator q_xi. At S=31 or47 only the other
maximum is omitted, supplying the five-parent full value v_xi. For the
unique-maximum parent P_B, one maximal deletion supplies its full C5 row.
Thus the full list of supported potentials is
\[
 u_A(15)=\alpha_\xi,\qquad u_A(31)=u_A(47)=v_\xi,
 \qquad u_B(31)=v_\xi,\quad u_B(15)=p_\xi.
 \tag{7}
\]
In either six-parent the two bits beyond C4 have no effect on these
coefficients: a deleted bit is absent; a retained C5 top bit is irrelevant
by the preceding argument. For every full r=0,…,63, use xi=r&15, with
the ordinary induced-suborder record transport. Therefore (5) for **all
128 complete affected marked rows** is exactly
\[
 \alpha_\xi z_1+2v_\xi z_3=0,\qquad
 v_\xi z_2+p_\xi z_3=0
 \quad(\xi=0,\ldots,15).
 \tag{8}
\]
No record is averaged or discarded without this invariance proof. The
compact 32 equations represent the full rows; the factor two is a labeled
ideal multiplicity, not two different child variables.

The complete future audit domain is consequently:

- 2 affected six-parent classes ×64 complete markings =128 rows;
- (8+7) ideals ×64 markings =960 labeled row/ideal occurrences;
- (3+2) supported ideals ×64 markings =320 nonzero coefficient occurrences;
- 640 zero-correction occurrences, including all 128 full births;
- 16 C4 rows with 5 ideals and 16 C5 rows with 6 ideals =32 held marked
  rows and 176 actual held-probability slots, sufficient to supply (6);
- 16 triples (q,p,v) and 32 compact balance equations.

The 960 entries are perturbation/child-membership entries, **not** a new
q6 probability table. Unsupported slots need no numerical baseline q6.

## 5. Exact analytical rank dichotomy — feasibility still unknown

All q,p,v and alpha in (6) are positive. Choose the reference base marking
xi=0 and define, symbolically from its actual inherited quantities,
\[
 k=\frac{\alpha_0}{2v_0}>0,\qquad
 \ell=\frac{p_0}{v_0}>0.
 \tag{9}
\]
The two reference rows \((\alpha_0,0,2v_0)\) and
\((0,v_0,p_0)\) are linearly independent. Their kernel is one-dimensional;
any nonzero vector in it has z1≠0. Normalize its orientation to z1=1:
\[
 z=(1,k\ell,-k).
 \tag{10}
\]
This candidate is not yet declared feasible. It satisfies the full system
if and only if the following exact identities hold for **every** xi:
\[
 \alpha_\xi=2v_\xi k,\qquad p_\xi=v_\xi\ell.
 \tag{11}
\]
If they hold, the full supported matrix has rank two and kernel spanned
by (10). If any fails, its rank is three and its only solution is zero.
Explicit three-row minors certify the latter outcome:
\[
 \det(A_0,B_0,A_\xi)
 =2v_0(\alpha_0v_\xi-v_0\alpha_\xi),
\]
\[
 \det(A_0,B_0,B_\xi)
 =\alpha_0(v_0p_\xi-p_0v_\xi).
 \tag{12}
\]
Use the first failed compact row in the fixed order xi=0,…,15, A before
B, for a deterministic certificate. This is exact equality/rank checking,
not optimization or a search over supports. **No value in (6) has been
newly evaluated for this design, so neither rank outcome is claimed.**

A rank-three result would reject nonconstant h7 on this frozen support
only, with h7=1 on all other seven-event classes. It would not exclude a
larger/different support, a later first departure or all nonconstant
all-size harmonic transforms. Such alternatives are not started here.

## 6. Positivity and one named complete-row geometric target

Conditional on (11), take (10) and
\[
 0<\epsilon<1/k.
 \tag{13}
\]
Then the only decreasing supported h value, h7(T3)=1−epsilon k, stays
strictly positive; T1 and T2 increase and all other classes remain one.
A deterministic interior choice for a future feasible certificate is
\[
 \epsilon=\frac1{2k},\qquad
 h_7(T_1)=1+\frac1{2k},\quad
 h_7(T_2)=1+\frac\ell2,\quad h_7(T_3)=\frac12.
 \tag{14}
\]
No epsilon or vector with a zero/negative supported h passes admission.

The named target is the complete parent
\(P_*=P_A=(0,1,3,7,15,15)\), with **all six record bits zero**.
For the intrinsic child width w(H), compare the complete conditional
expectation, summing all ideals and both fair newborn bits. There is no
conditioning on a proper birth or on reaching the support. The exact
linear functional after canceling only the common positive scale is
\[
 \mathcal L(z)=
 \sum_{S:\,[P_*+S]\in\mathcal T}
 u(P_*,0,S)z_{[P_*+S]}w(P_*+S)
 =3\alpha_0z_1+4v_0z_3.
 \tag{15}
\]
The coefficient 4 counts **two** width-two T3 slots. Using the complete
normalization balance \(\alpha_0z_1+2v_0z_3=0\),
\[
 \mathbb E_h[w(\text{child})\mid P_*,0]
 -\mathbb E_B[w(\text{child})\mid P_*,0]
 =\epsilon a_6\mathcal L(z)
 =\epsilon a_6\alpha_0>0.
 \tag{16}
\]
At (14) the gain is exactly a6 v0>0. Neither the absolute baseline expected
width nor a numerical a6 is needed. This is a strictly positive one-birth
conditional width bias, not an asymptotic or manifoldlike geometry theorem.

## 7. Finite-prefix admission and the distinct continuation question

If the actual coefficients pass (11), define the changed rows only at
parent size six by
\[
 q_h(P,r,S)=q_B(P,r,S)h_7(P+S),
 \tag{17}
\]
leaving all rows at smaller parents unchanged. For affected parents,
(8) gives normalization of the entire row; for all others the closure
proof gives h7=1 for every child. Every ideal remains strictly positive
under (13). In particular every full probability is unchanged, not
replaced by a different row-normalizing scale.

The multiplier in (17) is unmarked and isomorphism-invariant. Thus strict
record locality and marked-parent equivariance remain valid. Earlier
diamonds, based at parents of size at most four, are unchanged. For every
diamond based at a five-parent, both baseline full-D/4 routes multiply by
the same h7 of their common unmarked seven-event terminal. Therefore all
new required full-payload diamonds hold, including every record assignment,
newborn mark, equal-precursor pair and relabeling. The fair record law,
carrier, context and scalar passivity are unchanged.

Such a passing witness is a **complete admissible strictly positive prefix
through seven births**, not merely two selected normalized rows. Under
the established hypotheses of
[RI-38](../native_joint_growth_extension_criterion_v1/CRITERION.md), it can
serve as the seed for a subsequent positive compatible all-size continuation,
preserving this finite modification. That theorem does not promise that
the continued weights remain W_B(P,r)h(P) with record-independent h
relative to the original baseline. It solves a different, less restricted
continuation problem.

No harmonic equations above parent size six are solved here. Neither a
finite-prefix success nor a chosen RI-38 continuation establishes lasting
width improvement, sublinear height, a nonconstant positive all-size
record-blind h, informative quantum dynamics, mass or gravity.
Even a passing result is a construction in the stated conditional family,
not proof that DET uniquely selects the baseline or this perturbation.

## 8. Prospective exact verification strategy — execution not authorized

The analytical work reduces the open question to a fixed finite calculation.
No checker is created in this sitting. A coordinator-approved later executor
must use the following domain and strategy without changing the support.

### Canonicalization, closure and multiplicity

Use a deterministic unmarked canonical key: the lexicographically least
natural predecessor tuple, checking every topological relabeling of each
specified object. Every such object has at most seven vertices; at most
7! permutations per object suffice. The only new combinatorial inputs are
the three supported children, their seven maximal-deletion roles, the two
affected parents and their 15 labeled forward extensions. C4/C5 are the
two held-row sources. Outside the explicitly identified inherited prefix
replay below, no global six- or seven-order inventory is generated.

Retain both the labeled object and its canonical key. Reconstruct all
maximal deletions and all individual ideals of the two parents, compare
the complete closure/forward table to sections 2–3, and transport records
and precursor masks together under any induced deletion or relabeling.
Do not identify a transition with its child class: child variables are
shared only by summing all the labeled contributions.

### Actual inherited source closure

Use published RI-74 `rebuild_prefix()` and `prefix_row()` for C4 and C5,
at exactly the 16 base assignments xi and top bit zero for C5. The cached
row helper must be unwrapped to access the live initialized namespace.
RI-63's ordinary `row()` stops at four; it must not replace actual q5.
Byte-pin these accepted inputs before loading any helper:

- RI-74 `check.py`:
  `edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c`.
- RI-63 `check.py`:
  `39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b`.
- RI-63 `CERTIFICATE.json`:
  `f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b`.
- RI-41 `CERTIFICATE.json`:
  `3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969`.

The actual-q5 probability manifest is
`7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378`;
the inherited problem identity is
`dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c`.
The unchanged prefix proof has 69 canonical stages and 15 inherited refusal
controls. Its existing terminal-six catalogue replay, if approved with
the helper closure, is prefix verification only; it is not a new global
six-parent law or normalization table. No RI-77/79 executor or certificate
is needed for these new coefficients.

### Exact certificate, with either outcome admitted

Use canonical reduced rational strings, explicit integer domains and a
strict schema. Preserve:

1. Source/dependency identities, the ordered support, canonical keys,
   all maximal-deletion roles and the entire labeled forward table.
2. All 32 complete held rows /176 probability slots, with strict positivity
   and exact normalization, and all 16 q,p,v,alpha quadruples.
3. All 128 affected complete record rows and all 960 ideal occurrences,
   distinguishing the 320 supported coefficients from the 640 zero
   corrections. Record the proven four-to-one top-bit equivalence and
   verify each expanded row against the 32 compact balances.
4. The two independent reference rows, k and ell, and every exact residual
   of (11), in the frozen xi/A-before-B order.
5. If every residual is zero: the normalized z, the interval (13), the
   interior epsilon (14), all positive h values, every normalization
   residual and the strictly positive scaled width gain in (16).
6. Otherwise: the first failing compact row, the corresponding explicit
   three-row minor (12), and its nonzero exact determinant. The disposition
   is **no nonzero perturbation on this support**, not global nonexistence.

Do not require a positive result as a verifier assertion. Recompute the
entire bounded witness from the pinned held rows and compare all saved
fields, not just a claimed pass flag or digest. No optimizer is needed.
A separate source review should re-derive the two balance identities and
an independent exact certificate-only audit should check every residual,
rank witness, positive amplitude and width functional as applicable.

### Intended-reason refusals

The future executor must fail for the intended reason on mutated inputs
that: introduce another support class/parent/record domain; perform a q6/q7
probability lookup or numerical global-scale calculation; omit a maximal
deletion; confuse a representative tuple with its whole class; reorder
the T1,T2,T3 variables; merge the two P_A→T3 ideal slots; use backward
deletion counts as forward multiplicities; omit a complete marked row;
corrupt induced record/ideal transport; leak a top bit into a reduced
coefficient; substitute a non-actual q5 prefix; change a dependency pin;
confuse C4-full mask15 with C5-full mask31; use noncanonical/nonfinite
rationals, boolean indices or duplicate/extra JSON fields; corrupt a
residual, minor or
disposition; admit epsilon=0 or the zero-h endpoint epsilon=1/k; reverse
the width-gain sign; or present only a proper-birth-conditioned target.

These are design requirements, not tests claimed to have run. New
intended-reason controls must be reported separately from inherited ones.
Validate exact integer types and domain membership before any cached
lookup, so booleans cannot reuse cached integer keys. The exact mutations
and reasons require source review before execution. A top-bit control must
mutate the expanded coefficient or reject a forbidden held-row query before
helper lookup, not numerically probe C5 top-bit one outside the frozen
new-row query domain.

### Prospective commands, resource envelope and stop rule

After separate coordinator authorization to implement an executor, freeze
its complete reviewed source hash, this design's final identity, copied
dependency closure, schema, exact command arrays and durable destinations
**before any new coefficient run**. Let E denote that later approved
evidence directory and C=E/closure the copied track_b root; neither a future
executor nor those execution artifacts is created by this note.

The prospective child command forms are:

```text
/opt/homebrew/bin/python3 -I -S -B C/native_growth_first_departure_v1/check.py --witness
/opt/homebrew/bin/python3 -I -S -B C/native_growth_first_departure_v1/check.py
/opt/homebrew/bin/python3 -I -S -B -O C/native_growth_first_departure_v1/check.py
```

C must be replaced by the frozen absolute copied path, not left to shell
environment expansion. Use standard-library CPython 3.14, exact Fraction/
integer arithmetic and checks retained under `-O`. Every attempt gets
**120 seconds /512 MiB sampled RSS**, with internal elapsed/peak checkpoints
and an external owned-process watchdog. This is not an allocator-hard-cap
claim. Preserve exclusive stdout/stderr and pre/post input pins and receipts
under `/Volumes/AI_DATA/development/det-review-evidence/`; never temporary
or overwritten logs. Freeze the generated certificate and replay normal
and optimized modes only under a separately recorded saved-certificate
command/input addendum.

An implementation defect, dependency mismatch, incomplete coverage or
resource stop is not a mathematical no-go. Preserve that failure and stop
for root review; do not silently retry, relax the envelope, trim record
rows or substitute approximate arithmetic. A rank-three result stops at
the frozen-support rejection. A feasible positive width-biased result
stops at the complete finite-prefix witness and independent review. Neither
outcome authorizes another support, cutoff search, all-size harmonic solver
or continuation implementation.

## 9. Status and handoff

**Support and analytical reduction specified; actual feasibility open.**
Two complete independent mathematical design reviews and a separate full
prospective-executor audit passed. The reviews checked the exhaustive
maximal-deletion closure, individual forward multiplicities, every complete
marked-row reduction, both rank certificates, positive amplitude interval,
complete-row width target, finite-prefix covariance and RI-38 continuation
scope. They also checked the frozen domain, actual-prefix API/pins,
certificate/refusal design and resource/stopping contract.

The mathematical work was symbolic derivation and hand verification of the
finite combinatorial lists. No actual q,p,v,alpha,k,ell or epsilon values
were newly calculated; no helper, solver, enumeration script or prospective
executor was run. The rank and positivity tests described in section 8 are
future obligations, not completed checks. There is no proof-assistant claim.

Durable worker evidence is retained in
`/Volumes/AI_DATA/development/det-review-evidence/ri82-qr/worker-wuKyIQ/`:
the final design snapshot, `SOURCE_CHECK.json`, `REVIEW_RECORD.json` and
`HANDOFF_MANIFEST.json`. Source hygiene checks byte identity, local references,
declared dependency pins, equation labels and whitespace only; it does not
decide feasibility or mechanically verify the proofs.

The one-file design is ready for coordinator adjudication before any
implementation or coefficient execution. Only this design note is reserved.
Accepted laws/sources, RI-81's handoff source, RET, measurement, coordinator
records and git/index are not edited by this worker. No successor is started,
no law is adopted, and no empirical/gravity conclusion is made. Worker
review is not coordinator acceptance or publication.

## 12. Independent coordinator acceptance and implementation handoff

Root read the complete design and independently reconstructed its deletion
closure, record reduction, exact rank minors, positivity range and complete-row
width functional. A separate full mathematical/API review found no blocker.
The worker manifest and all twelve source/reference/evidence identities match;
all eight accepted references/runtime dependencies are already published.
No coefficient, helper, solver or order-enumeration execution occurred in this
adjudication. The actual rank and feasibility remain unknown.

Original reviewed design: 23466 bytes, SHA-256
`e04ef588e1617befb5e25370c33c25912a9293d9f6e4ac159d73bd9cd2f14168`.
Worker manifest:
`/Volumes/AI_DATA/development/det-review-evidence/ri82-qr/worker-wuKyIQ/HANDOFF_MANIFEST.json`,
10573 bytes, SHA-256
`94ada3bca43dcc85985c55cc1a0efd1d91fafc31ef61f8e980c458bb1ba87058`.
Independent coordinator-side review:
`/Volumes/AI_DATA/development/det-review-evidence/ri82-root-review/INDEPENDENT_DESIGN_REVIEW-20260925T000228Z-60e39003.json`,
14217 bytes, SHA-256
`f8760a192da8a7d659bf89b54e639f6cdefdb7cb737f2186e45c1e994322079b`.
Root adjudication and the original note are retained under
`/Volumes/AI_DATA/development/det-review-evidence/ri80-ri82-publication-20260925T000640Z-63dd51ee/`.
Only the status and this acceptance appendix changed after the reviewed source.

RI-84 is assigned to the existing Quantum Relativity task: implement exactly
this fixed-support checker and certificate schema. Its initial source-only
phase permits `check.py` and `IMPLEMENTATION.md` in the separate
`native_growth_first_departure_check_v1` directory. `CERTIFICATE.json` remains
absent until actual execution. Root will review the stable implementation and
fresh source/input/command freeze before the first coefficient calculation;
then the actual saved certificate needs its own replay addendum and independent
arithmetic audit. Either exact rank outcome is acceptable. No support expansion,
resource relaxation, replacement q5 or global q6 computation is authorized.
