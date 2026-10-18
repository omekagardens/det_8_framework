# RI-32 — one record-weighted ideal-growth candidate

23 September 2026. **Cycle-1 dossier; candidate family rejected for NG-01;
coordinator accepted as a family-scoped rejection.** No implementation or simulation
was performed. This is one fully specified ansatz and its small analytic
counterexample, not a new QR-05 study or a claim of native geometry.

The controlling scope is [RI-31, NG-01 and cycle 1](../../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md).
The family below uses finite orders, committed marks and an admitted pair-kernel,
plus explicit new law choices. Its weights normalize, its residual maps close,
and its one-step law is equivariant under relabeling. For positive coupling,
records affect an unlabeled order question. Nevertheless, **every member fails
the required adjacent-incomparable-birth identity**. Positive coupling also
violates the declared strict precursor-record read permission. Neither a larger
run nor more residual dimensions can repair these identities for this family.

## 1. Primitive, domain and cheap width audit — first

### Primitive boundary

The candidate reads only a present finite committed order, its retained binary
marks and a fixed law parameter. It retains a finite residual pair-kernel.
No metric, spacetime coordinates, supplied mesh, target sprinkling, Johnston
kernel, Rideout–Sorkin parameter/growth kernel, physical Hilbert space or
preparation amplitudes generate the object. Residual matrix indices are
alternative labels in the admitted pair-kernel calculus, not supplied positions
or physical quantum basis states. No future events are preallocated.

This establishes only **primitive-form compatibility under the listed candidate
premises**, not entailment by DET. The affine propensity formula, its global
normalization, fair binary records, residual domain and passive update are
chosen here. A diagonal rewriting of the chosen probabilities later in this
dossier does not turn them into a derivation from the residual kernel.

### Domain audit

The admitted normalized residual states are complex Hermitian positive kernels
on a fixed nonempty finite alternative carrier, with total-entry mass one.
Unnormalized branches are scalar multiples of the entire input kernel. They
are not asserted to remain normalized until positive-branch conditioning.
This avoids confusing total-entry normalization with ordinary quantum trace
normalization. It adds no physical preparation/operation availability premise
by implication.

The [full-cone operation obstruction](../../validation/t8-q-operation-domain-2026-09-13/OPERATION_DOMAIN.md)
does not obstruct these scalar branch maps: they deliberately extract no
information from the residual. It would be wrong to describe this passive
payload as a quantum-to-geometry coupling or a solution of that obstruction.

### Cheap structural-width audit

Every order ideal, including the empty and full ideals, has strictly positive
weight for every finite parent. There is no fixed chain/port bound. Repeated
empty-ideal births put an antichain of any finite size in the support. Repeated
full-ideal births also permit chains; ideals joining several prior branches
are not excluded. Thus the specific two-port width obstruction does not apply
to this family.

This is **support**, not typicality or a manifoldlike regime. In particular,
the path making an all-zero-mark antichain of size `n` has probability
`2^(-n(n+1)/2)`: at its size-`k` parent there are `2^k` ideals, all with weight
one, and the selected empty/zero branch has probability `2^(-(k+1))`.
Its positive but small probability proves no asymptotic width law, volume
law, dimension, local geometry or continuum limit. The covariance obstruction
below stops this candidate before any such screen is warranted.

## 2. Complete state, initial conditions and fixed law

Write a state as

\[
 X=(C,R;\Omega,D,\gamma),\qquad C=(V,\prec).
\]

- `V` is a finite set of already committed event labels; `prec` is a strict
  transitive partial order. `#` is its counting measure, not a physical volume.
- `R:V -> {0,1}` retains one immutable outcome mark per event. Together with
  `C`, it retains each event's complete strict precursor and outcome. There is
  one fixed declared setting, encoded in the context `gamma`; no other record
  payload is suppressed by this particular state definition.
- `Omega` is a nonempty finite alternative carrier fixed along a history.
  `D` is a complex Hermitian pair-kernel on that carrier satisfying

  \[
  D\succeq0,\qquad m(D)=\sum_{\alpha,\beta\in\Omega}D_{\alpha\beta}=1.
  \tag{1}
  \]

  Every entry, including off-diagonal complex entries, is retained. There is
  no physical Hilbert-space input or replacement of `D` by its diagonal.
- `gamma` is a fixed type/setting/controller/context declaration. Its
  controller has a single state; it has no hidden clock, stage schedule,
  latent parameter posterior or operation-selection channel.

Admit every such finite `(C,R)` and every kernel in (1) as mathematical inputs.
This full preparation domain is an additional candidate assumption, not a DET
theorem or a claim that laboratory sources realize it. The designated starting
class is the empty order/record map with any fixed allowed `Omega,D_0,gamma`.
The same `D_0` and context can be used in all contrasting histories below.

Fix once and for all a **finite** real parameter `lambda >= 0`. It is a
dimensionless free law parameter, not inferred from data or a gravitational
constant. No update changes it. Rational choices would permit rational
probability arithmetic, but no executor or finite parameter grid is supplied.

Let `J(C)` be the finite set of order ideals of `C`. For each `S in J(C)`, set

\[
 h_R(S)=\sum_{a\in S}R(a),\qquad
 w_\lambda(C,R;S)=1+\lambda h_R(S),\qquad
 Z_\lambda(C,R)=\sum_{I\in J(C)}w_\lambda(C,R;I).
\tag{2}
\]

`Z_lambda` is a normalization factor, not the live residual state. Every ideal
has weight at least one, so `Z_lambda >= |J(C)| >= 1` and is finite. The fixed
law supplies alternatives `(S,b)` for `b in {0,1}` with joint probability

\[
 \pi_\lambda(S,b\mid C,R)=\frac{w_\lambda(C,R;S)}{2Z_\lambda(C,R)}.
\tag{3}
\]

The marginal ideal probability is `q_lambda(S|C,R)=w_lambda/Z_lambda`;
the new record is a fair bit conditional on that ideal. Neither probability
depends on `D`. Equation (3) is an explicit extra law, not a kernel sampling
mechanism deduced from existing DET principles. Sampling it introduces no
extra agent, will variable or state-dependent choice outside the rule.

Only after selecting `(S,b)` is a fresh event `e` appended:

\[
 V^+=V\cup\{e\},\qquad
 \prec^+=\prec\ \cup\ \{(s,e):s\in S\},\qquad
 R^+|_V=R,\quad R^+(e)=b.
\tag{4}
\]

The ideal condition makes this transitive; freshness and maximality prevent
cycles. Existing records and relations are never rewritten. Birth labels are
bookkeeping names, not physical times, coordinates or a selected foliation.
An algorithmic step means one use of (3)–(4), not a derived elapsed duration.

## 3. Full payload maps, closure and mass scope

For each recorded branch use the unnormalized map

\[
 \mathcal B^{C,R}_{S,b}(D)
   =\pi_\lambda(S,b\mid C,R)D,
\tag{5}
\]

with output order/records given by (4), the same carrier `Omega`, and the same
type/context `gamma`. These are the complete branch maps, not scalar payload
summaries. They extend linearly and positively to the unnormalized PSD cone;
linearity is part of this chosen construction, not inferred from biadditivity
of a pair-kernel in its event arguments.

For every admitted normalized input, the branch mass is `pi_lambda > 0`, and
conditioning yields the **entire unchanged kernel**:

\[
 m(\mathcal B^{C,R}_{S,b}(D))=\pi_\lambda(S,b\mid C,R),\qquad
 \frac{\mathcal B^{C,R}_{S,b}(D)}{
       m(\mathcal B^{C,R}_{S,b}(D))}=D.
\tag{6}
\]

The sum of branch masses is one by (2)–(3); the sum of the unnormalized residual
maps is the identity when the separate classical labels are forgotten.
All PSD entries survive conditionally, including possible zero-mass directions
of the ambient cone. This does not give those directions their own normalized
states. Kernel positivity and normalized-domain closure follow directly from
scalar multiplication and (6).

There are no zero-probability `(S,b)` branches at finite `lambda` in this
admitted domain. Ineligible non-ideal precursors are not alternatives; if
represented in an enlarged audit alphabet they have the zero map and cannot
be selected or normalized. No silent, halt or absorption branch is admitted:
one algorithmic step commits one record with total mass one. In particular,
`b=0` is a committed outcome, not missing data, an unrecorded transition or a
physical no-click declaration. No claim about absence of silent activity or
never-commit behavior in DET generally follows. No physical clock or infinite
history measure is constructed here.

For clarity, an optional alternative-index kernel can re-encode (3): on the
finite alphabet `A_C={(S,b)}`, set

\[
 G_{C,R}(u,v)=\mathbf1_{u=v}\,\pi_\lambda(u\mid C,R).
\tag{7}
\]

It is positive with total mass one and exactly decoherent singleton alternatives.
It describes potential next outcomes, not pre-existing future events. **This
is only a diagonal classical re-encoding of the already chosen law.** It is
not a derivation of (3) from `D`, a replacement for the full map (5), an
apparatus construction or a proof of quantum record formation. The retained
residual is passive; this family makes no phase-sensitive or full-QM claim.

## 4. Locality and meaningful record feedback

The target locality permission is the strict one in the
[licensed-birth contract](../../validation/t8-q-licensed-growth-2026-09-12/BIRTH_F.md):
the probability/update for a proposed precursor `S` may read records only in
`S`. The numerator in (2) is precursor-local. Its normalizer need not be.

Take the singleton parent `V={a}` with mark `R(a)=r`. Its ideals are the empty
set and `{a}`, so

\[
 Z_\lambda=2+\lambda r,\qquad
 P(S=\varnothing\mid r)=\frac1{2+\lambda r},\qquad
 P(S=\{a\}\mid r)=\frac{1+\lambda r}{2+\lambda r}.
\tag{8}
\]

For `lambda>0`, even the empty-precursor probability changes when `r` changes.
The marked empty branch has probability `1/[2(2+lambda r)]` and has the same
defect. Normalizing local propensities has introduced a forbidden record read.
Thus **strict precursor-record locality fails for every positive lambda**.
This is a statement about the specified read permission, not superluminal
physics or a rejection of every weaker, relative-odds or globally conditioned
notion of locality.

There is nevertheless genuine direct feedback in this stipulated law. For the
unlabeled question “is the next two-event order a chain?”, the probabilities
from `r=0` and `r=1` differ by

\[
 \frac{1+\lambda}{2+\lambda}-\frac12
   =\frac{\lambda}{2(2+\lambda)}>0.
\tag{9}
\]

Both singleton marks arise from the empty starting state with probability
one half, with exactly the same residual `D_0` and context. These are lawful
alternative histories, not an intervention overwriting a committed record.
No static hidden-seed posterior is being updated: (3) directly reads `R`.
This establishes chosen record-to-order dependence, not a measured causal
mechanism, matter backreaction or a gravity source. At `lambda=0`, that
dependence vanishes.

## 5. Equivariance passes; full birth covariance fails

### One-step relabeling

An isomorphism of marked parents transports `V,prec,R,S` together. It bijects
their ideal sets and preserves each mark sum in (2), so it preserves `Z_lambda`
and (3). A relabeling `tau` of the separate alternative carrier transports
both kernel indices by `D'_(tau(alpha),tau(beta))=D_(alpha,beta)`; scalar
multiplication in (5) commutes with this transport. New event labels do not
add residual coordinates or change `gamma`. Thus the complete one-step map
has the declared marked-parent and residual-coordinate equivariance.

Equivariance is not the adjacent-birth identity. The local T8b/T8c reference,
`docs/track_b/covariant_record_growth.md`, already distinguishes
these obligations and supplies the uniform-over-ideals negative control.
That local reference is used for attribution, not imported or asserted to be
a published executable dependency. The following counterexample is
self-contained and applies that known obstruction to this entire family.

### One reachable full-payload counterexample for every lambda

Begin with the singleton `a` marked zero, and any allowed normalized `D`.
Specify two births `x,y` with old-parent precursors `S={a}`, `T=empty`, and
outcomes `R(x)=R(y)=0`. The final order has `a prec x`, with `y` incomparable
to both; the two newborns are incomparable. Both birth orders are permitted.

Along these paths every mark is zero. Hence every weight in (2) is one,
**for every finite lambda >= 0**. The marked branch weights are:

| Path | First branch | Intermediate parent's ideals | Second branch | Complete unnormalized residual |
|---|---:|---|---:|---:|
| Add `x` at `{a}`, then `y` at `empty` | `1/4` | Chain `a prec x`: `empty,{a},{a,x}` | `1/6` | `D/24` |
| Add `y` at `empty`, then `x` at `{a}` | `1/4` | Antichain `{a,y}`: `empty,{a},{y},{a,y}` | `1/8` | `D/32` |

After canonical newborn-coordinate identification, the complete final marked
order, setting/type/context and residual carrier are the same. But

\[
 \mathcal B^{C+S,R+0}_{T,0}\,
 \mathcal B^{C,R}_{S,0}(D)=D/24
 \quad\ne\quad
 D/32=\mathcal B^{C+T,R+0}_{S,0}\,
 \mathcal B^{C,R}_{T,0}(D).
\tag{10}
\]

The comparison includes all entries of the unnormalized residual; normalized
conditional residuals alone would both be `D` and conceal the failure.
Mass one guarantees `D` is nonzero, so (10) fails for **every** admitted
normalized residual, not only a chosen starting state. Every displayed branch
has positive probability. There is no zero-weight or unreachable-state escape.
If the paths are compared from the designated empty starting class, the common
initial zero-mark birth contributes a factor `1/2`: the weights are `D/48`
and `D/64`, still unequal.

This is a simple analytic rejection within cycle 1, not a claimed full-domain
positive covariance theorem or an executed finite audit. It rejects the whole
parameter family even if strict precursor-record locality is relaxed. At
`lambda=0` the order law is the previously rejected uniform-over-ideals rule;
positive lambda does not fix it because a reachable all-zero sector retains
that rule unchanged.

The formulas still define a normalized **labeled classical growth process**.
One can form an unlabeled pushforward by summing the distinct labeled
histories with their actual weights. What fails is the required equal full-map
weight across natural labelings, not the existence of every possible unlabeled
probability distribution. Early quotienting, dropping multiplicities, changing
the record rule after seeing this failure or examining only favorable histories
would change the problem; none is done here.

## 6. Premise and result ledger

| Item | Status and exact scope |
|---|---|
| Finite committed order, maximal append, immutable old relations/records | Existing QR-MAP structural vocabulary; equations (4) use it explicitly. |
| Admitted complex positive pair-kernel structure | Conditional DET mathematical vocabulary; not proof of physical preparations or full QM. |
| All normalized PSD total-entry kernels on a fixed carrier as candidate inputs | Additional domain choice; the residual is passive and no informative all-cone effect is claimed. |
| All-ideal eligibility, fair binary new records, singleton controller/context | Additional candidate choices, not derived apparatus or growth principles. |
| Fixed finite `lambda>=0`, weight `1+lambda*h`, global normalization | Entirely chosen law. No empirical calibration or DET entailment. |
| Complete maps `B=pi*D`, unchanged carrier and positive-branch residual | Explicit passive-payload choice; positivity, mass accounting and closure follow by substitution. |
| No silent/stopping branches; one birth per algorithmic step | Scope restriction, not a claim that record growth exhausts present activity. |
| Unbounded finite antichain support | Cheap width screen passes; no typicality, infinite measure or manifold conclusion. |
| Marked-parent equivariance | Direct relabeling argument in section 5; not Lorentz covariance. |
| Nontrivial unlabeled feedback | Equation (9), only for positive lambda, comparing reachable histories with the same residual. |
| Strict precursor-record locality | Fails for every positive lambda by (8); no universal locality no-go follows. |
| Adjacent-birth/full-payload natural-label covariance | Fails for every family member by (10), including zero lambda. |
| Physical geometry, local volume, clocks, mass and gravity | Not constructed or inferred. Option B and metric-as-record Status M are unchanged. |

## 7. Disposition, checks actually made and stop

**Disposition:** reject this one record-weighted-ideal family for NG-01.
Neither records changing an order marginal, one-step equivariance, normalized
rows nor wide supported histories imply full joint covariance. This result
does not establish that all native-input feedback laws are impossible.

The uniform-over-ideals failure is established prior material, credited above.
The bounded result here is that this explicit record-responsive extension
retains it in a reachable sector and also leaks record dependence through
its normalizer. This is not a novelty claim about the underlying mathematics.

**Actually checked:** the accepted plan and relevant existing contracts were
read; finite sums, positivity/closure, the singleton feedback/locality formulas,
the two lists of intermediate ideals and their complete branch products were
checked analytically. Independent reviewers checked the mathematics and
primitive/domain/claim boundaries. No Python/project sources were executed,
no enumeration, random simulation, data acquisition or new theorem-search
campaign was run, and no numerical pass count is claimed. The carrier is finite
but arbitrary; the small counterexample already falsifies an all-size claim.

This document is the entire research artifact. Its equations are self-contained;
the linked accepted plan, structural/activity/domain records and local T8
description provide scope and attribution, not runtime dependencies. See also
the [activity/commit/access contract](../RECORD_PROCESS_CONTRACT.md) and
[existing geometry work order](../QR_MAP_RELATIVITY_GEOMETRY_PLAN.md).
The final document identity is supplied in the handoff rather than embedded
in itself. Root owns coordinator records, git/index and publication.

**One bounded recommendation:** independently adjudicate and retain this
family-scoped rejection; do not implement or simulate this family as an NG-01
success candidate. No cycle-2 executor is warranted to discover a failure
already given by (10). Any future consideration of another law would require
a fresh bounded scope addressing joint normalization, read permissions and
full-payload diamonds from the outset; this dossier specifies and starts none.

Source work stops at this single-document handoff. No existing QR map, handoff,
accepted source, RET implementation, observation-channel work, gravity ledger
or release gate is changed. No replacement family, automatic successor,
coverage/noncollapse programme, QR-05 series, clocks, book or retired
kappa-gravity work is opened.
