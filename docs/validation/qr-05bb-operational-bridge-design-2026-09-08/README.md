# QR-05BB: operational bridge-design checkpoint

8 September 2026 (Pacific/Honolulu). Design and analytical review only.
No fixed numerical study, apparatus experiment or RET integration is performed
by this checkpoint. No DET ontology is required to read or use this model.

## 1. Decision and missing bridge

Select **four labeled local qubit-polarization measurements, followed by a
supplied-geometry weighted response estimator**. The positive question is
whether registered outcomes identify one functional of a declared bilinear
response model. The negative question is whether the same records identify
that functional for a larger continuous response-profile class.

The distinction is important: earlier field-bank production and receiver
application were arithmetic interfaces, not physical detectors. Calling their
inputs measurements did not establish how those inputs could be observed.
Here the proposed chain is explicitly:

```text
fresh local preparations → labeled Z outcomes → estimated corner responses
                         → bilinear model → fixed geometric functional
supplied chart, measure and causal kernel ──→ geometric weights
```

The weights are compiled without using the unknown profile or its target
integral. No control phase is set equal to the desired answer and then read
back as a purported discovery. This remains a conditional observation model,
not an already calibrated apparatus interface.

## 2. Supplied geometry and response-profile domain

Work in one declared flat 1+1 laboratory chart with signature (+,−), units
c = 1 and a fixed length reference. Set

\[
u=t+x,\quad v=t-x,\quad ds^2=du\,dv,\quad d\mu=\tfrac12du\,dv.
\]

Supply the rectangle Q = [u₀,u₁] × [v₀,v₁], positive side lengths Δu, Δv,
and its volume V = Δu Δv/2. Set ξ = (u−u₀)/Δu and ζ = (v−v₀)/Δv.
The four nominal stations have the fixed order **(00, 10, 01, 11)** and
coordinates (ξ,ζ) equal to those labels. Neither coordinates nor V are
inferred from the number of detection events.

Let I₂ be the 2×2 identity and Z = diag(1,−1) the Pauli Z matrix on a qubit.
Declare a continuous local preparation/response map

\[
z\longmapsto\rho(z)=\frac{I_2+f(z)Z}{2},\qquad
f:Q\longrightarrow[-1,1],\qquad f(z)=\operatorname{Tr}(\rho(z)Z).
\]

This is a model of possible local qubit preparations and their calibrated
Z responses. It is not a joint continuum quantum-field state, a stress-energy
field, or a derived gravitational source. The response is scalar-valued in
the declared chart and common calibrated local axis; its transformation as
a physical Lorentz scalar is not assumed or demonstrated.

Only the four corner preparations are sampled in this design. An addressable
map on Q is a separate premise needed to discuss the true profile between
those samples. Four isolated qubit states alone would define only an
interpolated constructed target, not a preexisting interior response.
Continuity and ideal localization are also explicit premises: an unrestricted
L∞ equivalence class specified only almost everywhere has no well-defined
corner values. Earlier almost-everywhere field-error bounds do not themselves
authorize point sampling. Finite aperture, finite duration, axis alignment
and drift would require later apparatus modeling.

Repeated trials mean fresh preparations at repeated nominal settings, not
several independent measurements at the identical spacetime event. The
sampling schedule/dependency graph and the supplied spacetime order are
different objects.

## 3. One target, fixed before choosing the response

Write fₐ = f(zₐ) and use the bilinear basis

\[
\begin{aligned}
\phi_{00}&=(1-\xi)(1-\zeta),&\phi_{10}&=\xi(1-\zeta),\\
\phi_{01}&=(1-\xi)\zeta,&\phi_{11}&=\xi\zeta,\\
If&=\sum_a f_a\phi_a,&F_0&=V^2If,\qquad F=V^2f.
\end{aligned}
\]

The V² factor is a chosen normalization compatible with the preceding
mathematical lineage, not an inferred physical coupling. If the coordinates
carry length units, F formally carries length to the fourth power; f is
dimensionless. The basis is nonnegative and sums to one, so admissible corner
responses give an admissible interpolated response.

Use the conventional future-volume kernel

\[
R_Q(z)=\int_Q\mathbf1[z\prec w]\,d\mu(w)
      =\frac{(u_1-u)(v_1-v)}2\quad(z\in Q).
\]

Here z ≺ w uses increasing u and v; including or excluding null boundaries
does not change these volume integrals. In the conventional flat 1+1
massless scalar comparison, the retarded Green function is
G⁰_R(w,z) = ½ 1[z ≺ w], up to this null-boundary convention, so
R_Q(z) = 2 ∫_Q G⁰_R(w,z) dμ(w). This is an adopted geometric comparison,
not a new propagation law. See [Johnston, Eq. (3.23), massless limit](https://arxiv.org/pdf/0806.3083).
R_Q is not a Born probability, completely positive map or qubit transport rule.

Fix σ = V⁴ > 0, corresponding to the preceding normalization with both
comparison regions equal to Q. Define the dimensionless target and its
bilinear-model version:

\[
T(F)=\frac1\sigma\int_Q F R_Q\,d\mu,\qquad
T_0=T(F_0)=\sum_a w_a f_a,\qquad
w_a=\frac{V^2}{\sigma}\int_Q\phi_a R_Q\,d\mu.
\]

Weights depend only on supplied geometry and kernel. Their exact numerical
values are deliberately left to the separately specified next study.
Sampling the kernel at the four corners is not a replacement for integrating
these products. This target is a classical functional of a response profile;
no device in this design measures the nonlocal integral directly.

## 4. Local quantum instrument and accessible records

For each station a and fresh shot r, prepare ρₐ and apply the fixed projective
instrument with x ∈ {−1,+1}:

\[
\Pi_x=\frac{I_2+xZ}{2},\qquad
\mathcal I_x(\rho)=\Pi_x\rho\Pi_x,\qquad
p_a(x)=\operatorname{Tr}(\rho_a\Pi_x)=\frac{1+x f_a}{2}.
\]

The branch state is unnormalized. The full classical–quantum record map is
ρ ↦ ∑ₓ |x⟩⟨x| ⊗ 𝓘ₓ(ρ), with distinct event labels retained. These are
standard quantum measurement constructions, adopted rather than derived
from the record notation. See [Preskill, Chapter 3, §§3.1–3.2](https://www.preskill.caltech.edu/ph219/chap3_15.pdf).
Polarization expectations and projection counts provide a conventional
qubit-readout interpretation; that does not make four Z measurements full
state tomography. See [James et al., §II](https://arxiv.org/pdf/quant-ph/0103121).

Assume independent product preparations across stations and fresh independent
copies across shots. One four-station trial then has

\[
P(x_{00},x_{10},x_{01},x_{11})=\prod_a p_a(x_a).
\]

All 16 ideal outcome vectors, including zero-probability branches, belong to
the prospective comparison domain. This is a declared cardinality, not a
reported numerical test result. Local instruments on distinct tensor factors
commute under permitted schedule swaps; this does not establish physical
Lorentz covariance. A repeated Z measurement on the same unreset qubit does
not satisfy the fresh-copy independence premise.

The observer may retain the following record fields (a proposed schema,
not a production SDK):

- Run, trial/shot and station identifiers; setting and preparation-protocol
  identifiers; readout-calibration and frame identifiers.
- Raw registration reference, attempted-shot status and registered outcome.
- Declared shot quotas and record-availability/collector provenance.

The observer receives compiled weights and declared calibration metadata,
but not private f values, exact states or likelihoods, true moments, target
integrals, or fixture identifiers/seeds that reveal those quantities.
Identifiers must not encode the hidden answer. Preparation controls are
documented separately from the unknown response; a controller secretly
encoding T(F) is outside this model.

Classical aggregation occurs only where the relevant records are lawfully
available after collection. An analysis table is not an instantly accessible
remote record. In the ideal model every attempted shot has one ±1 outcome.
A missing file or absent station is not detector nondetection or outcome zero.
Duplicates, quota failures and setting/frame/calibration mismatches require
an explicit refusal/status, not silent postselection or renormalization.
A physical nondetection outcome would need an expanded POVM and selection
law; an ideal no-loss assumption does not license discarding such outcomes.

For Nₐ positive integer fresh shots per station, define

\[
\widehat f_a=\frac1{N_a}\sum_{r=1}^{N_a}X_{ar},\qquad
\widehat T=\sum_a w_a\widehat f_a,\qquad
\mathbb E[\widehat T]=T_0,\qquad
\operatorname{Var}(\widehat T)=\sum_a\frac{w_a^2(1-f_a^2)}{N_a}.
\]

The variance formula is conditional on the ideal independent preparation
model. Its private fₐ values are not observed uncertainty certificates.
Dependent preparations require covariance terms. Population-law
identifiability and unbiasedness do not give exact reconstruction from a
finite record or a confidence-coverage guarantee.

These diagonal product states and Z-only measurements have the same outcome
law as classical Bernoulli variables. Classical probability is therefore a
required independent comparator, and no quantum advantage is claimed.

## 5. Analytical identifiability boundary

Within the declared bilinear class, corner expectations determine If and
therefore T₀. Now enlarge the admissible profile class to continuous f and
compare

\[
f^{(0)}=0,\qquad f^{(1)}=\delta b,\qquad
b(\xi,\zeta)=\xi(1-\xi)\zeta(1-\zeta),\qquad 0<\delta\le1.
\]

Hold fixed the public settings, geometry, calibration, quotas and opaque
record identifiers; the two alternatives differ only in the hidden response
map. Both profiles are admissible. The bubble b vanishes at every corner and is
strictly positive in the interior. Thus all four sampled density matrices,
and hence the complete accessible record laws for any number of fresh shots
at these stations, are identical. Nevertheless,

\[
T(V^2f^{(1)})-T(V^2f^{(0)})
=\delta\frac{V^2}{\sigma}\int_Q bR_Q\,d\mu>0.
\]

The strict inequality follows because the integrand is nonnegative and
positive on the interior. Equal observation laws give equal expectations
for every integrable statistic of those observations, so no such estimator
can be unbiased for both unequal true targets.

This is a model-expansion obstruction, not a failure of interpolation within
the bilinear class. More repetitions at the same four sites cannot remove
it. A justified profile restriction or new interior measurement access is
needed. One added interior site can separate this particular pair, but does
not establish recovery of arbitrary continuous profiles. The discrepancy is
structural information loss, not evidence of noise, apparatus error, modified
physics or a conflict with established observables.

## 6. Keep three uncertainty sources separate

Let δF = F−F₀ be profile-model error and let eₐ = f̃ₐ−fₐ be error in an
estimated/calibrated corner response. With T̃ = ∑ₐwₐf̃ₐ,

\[
\widetilde T-T(F)=\sum_a w_a e_a-\frac1\sigma\int_Q\delta F R_Q\,d\mu.
\]

If an external justification supplies |δF| ≤ εV² almost everywhere and
|eₐ| ≤ rₐ, then the triangle inequality gives the conditional envelope

\[
|\widetilde T-T(F)|\le\epsilon S_R+\sum_a|w_a|r_a,
\qquad S_R=\frac{V^2}{\sigma}\int_Q|R_Q|\,d\mu.
\]

- **Interpolation/model error:** ε is not certified by the four corner
  records; the bubble shows why. Continuity alone does not give a small ε.
- **Finite-shot variation:** contributes to e once, not again to δF. IID
  assumptions or unbiasedness alone do not supply small deterministic rₐ.
  Statistical confidence bounds need a separately declared protocol.
- **Readout calibration:** outcome-assignment bias and contrast are distinct
  from finite-shot variation. Geometry, weights and localization uncertainty
  are additional modeling terms, not covered by assuming these are exact.

For example, with assignment errors α = P(Y=−1 | X=+1) and
β = P(Y=+1 | X=−1), the observed mean is

\[
\mathbb E[Y]=\beta-\alpha+(1-\alpha-\beta)f.
\]

Known offset β−α and known nonzero contrast 1−α−β allow inversion.
Unknown α and β can be confounded with f; small contrast amplifies error
and zero contrast removes identifiability. A registered ±1 label also
presupposes a calibrated mapping from the actual detector signal. The
conventional distinction between
projection noise and imperfect readout is discussed by
[Degen, Reinhard and Cappellaro, §V.A.4 on classical readout noise](https://web.mit.edu/pcappell/www/pubs/Degen17.pdf).

This envelope is BA-style error composition, **not a transfer of BA's
37-receiver certificate**. Its unit radii, raw-moment bank, exact sharpness,
source-independence results and fixed counts do not apply automatically to
this new point-sampling interface. Corner evaluations are not unrestricted
raw-moment functionals. Any later bank/decoder representation must prove its
own domain-specific map. Coupled error sets can satisfy an enclosing bound
without attaining Cartesian sharpness. The stochastic fresh-preparation
assumption here is also different from BA's deterministic Cartesian-set
assumption.

## 7. Next gate: QR-05BC, separately bounded numerical verification

**Not executed in BB.** Before computing fixed results, freeze a small
standalone protocol, source identity, rational fixture list and independent
comparison routes. Proposed question: do local quantum records recover the
supplied bilinear geometric-response functional in the precise population
sense above, while preserving the off-model obstruction?

| Component | Required prospective check |
|---|---|
| Domain | One supplied unit null-coordinate rectangle; four labeled corner stations; fixed Z settings; fresh independent product preparations |
| Positive fixtures | Zero, deterministic ±1 and asymmetric rational corner responses; no profile-dependent weights or target-dependent controls |
| Quantum route | Tensor-product instruments, all 16 one-trial branches, probabilities and unnormalized branch states; zero branches retained |
| Probability route | Independently constructed classical Bernoulli product law; compare full laws, estimator means and variances |
| Geometry route | Independent direct polynomial integration of the profile, kernel and basis weights, not a copy of a decoded target table |
| Identifiability control | Same full corner-record law but different continuous-profile target for the interior bubble |
| Information controls | Correct joint relabeling versus mismatched station labels or histogram-only loss; fixed geometry while profiles vary |
| Preparation control | Fresh copies versus repeated unreset measurement; do not infer joint independence from correct one-shot marginals |
| Interface controls | Missing/duplicate station or shot; quota, setting, frame and calibration mismatch; refuse unrecorded selection |
| Domain control | Point sampling/interpolation is not the old unrestricted full-moment bank; corner-only kernel quadrature is not the stated integral |
| Calibration boundary | Unknown bias/contrast cannot be presented as known response; no unearned finite-shot confidence or detector claim |

If a tiny repeated-shot extension is included, give it a fixed independent
quota before enumeration. If schedule invariance is claimed, compare full
event-labeled maps, not just scalar probabilities. Any coordinate transport
check is a mathematical change-of-variables comparison under stated response
transport, not proof of spin/measurement covariance in a laboratory.

Failures and zero-support cases must remain visible. A positive result would
verify a bounded conditional model correspondence, not unrestricted field
recovery, a general quantum-to-geometry theorem or physical metric inference.
Disagreement between independently computed exact routes requires a repair
or narrower premise; it cannot be attributed to experimental noise.

No optimizer, RET adapter, empirical thresholds, hardware acquisition or
clock experiment belongs to BC. A later apparatus proposal would need local
preparation and registration calibration, localization/axis/drift checks,
independent interior holdouts to challenge interpolation, a conventional
baseline and an explicit uncertainty protocol. RET integration remains
separately gated.

## 8. Lineage and limits of this checkpoint

The supplied flat measure/kernel comes from the preceding geometry work;
the field-functional and error distinctions come from AO through BA:
[AF supplied local geometry](../qr-05af-local-geometry-2026-09-07/README.md),
[AO field interfaces](../qr-05ao-field-measurements-2026-09-08/README.md),
[AU source-independent receiver](../qr-05au-source-independent-receiver-2026-09-08/README.md),
and [BA error composition](../qr-05ba-field-acquisition-errors-2026-09-08/README.md).
Their fixed numerical captures are not rerun or enlarged here.

The conventional comparator is standard projective measurement plus classical
interpolation and a supplied retarded-volume kernel. The useful structure is
an explicit record-to-question contract, including an observational
indistinguishability witness and separated assumptions. It does not derive
quantum theory, infer geometry from detection counts, propose gravitational
dynamics, validate DET ontology, or establish experimental advantage.

See the [decision record](RESULTS.md), [owned research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md)
and [quantum–record research charter](../../QUANTUM_RECORD_STRUCTURE_RESEARCH.md).
Main project priorities remain RET hardening, materials monitoring and anomaly
triage; book work stays archival and clock/later gravitational couplings
remain deferred.
