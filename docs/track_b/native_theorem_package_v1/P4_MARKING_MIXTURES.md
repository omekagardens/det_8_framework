# P4 model-label separation under hidden old-marking mixtures

21 October 2026. Conditional manual finite-prefix theorem.

**Result.** [The nuisance-identifiability theorem](P4_NUISANCE_IDENTIFIABILITY.md)'s baseline-versus-perturbation separation survives
arbitrary hidden old-marking distributions, even when the two hypotheses
use different distributions and different nuisance parameters.
The original prefix and parent remain fixed. One common positive
six-parent scale is used within each hypothesis.

The accepted all-mark held identities reduce the two relevant constants to
\[
 U_{0,r}=U_0>0,\qquad U_{9,r}=\theta^2c_{r(r_1)},\qquad
             c_1=\frac{359}{360}c_0>0.
\]
The accepted fixed-amplitude perturbation obeys
\(h_9(\lambda)c_1>c_0\) on the **whole inherited neighborhood**
\(\mathcal I_*\). Consequently even its smallest mixture ratio exceeds
the largest baseline mixture ratio. No further neighborhood shrink,
coefficient selection or full-row overlap construction is needed.

This removes the known-full-old-marking and matching-mixture premises
from this exact model-label theorem. It does not remove the fixed-prefix,
fixed-parent, conditional-occurrence, prescribed-law or exact-order-access
premises. It is not a theorem of bare DET or an empirical observation claim.

## 1. Fixed laws and precisely what is mixed

Keep the admitted positive original prefix \(q^0\) through parent five.
Its parent-four witness, canonical parent-five construction and all actual
coefficients remain fixed. For \(0<\lambda\le1\), all parents of size
at most four are unchanged; parent-five proper slots become
\(\lambda q^0(P,r,S)\), and full slots become
\(1-\lambda+\lambda q^0(P,r,P)\).

At parent six the baseline uses the admitted maximal-deletion potential
and a common scale \(\rho>0\):
\[
 q^B_{\lambda,\rho}(P,r,S)=\rho u_\lambda(P,r,S)
                    \quad(S\subsetneq P).
\]
Every full slot is its complete normalization complement.
The scale is admitted for the entire marked six-parent layer, not
chosen separately by old marking, selected shape or ideal.

Fix
\[
 P_4=C_4\oplus A_2,\qquad
 C_4=\{r_1<r_2<r_3<r_4\},\qquad a\parallel b
\]
with both caps above the chain. An old marking is a binary map \(r\)
on all six vertices; let \(i(r)=r(r_1)\). There are finitely many such
markings. No independence, fairness or full support is imposed on their
mixing distribution.

Let \(B_{\lambda,\rho;r}\) be the complete unmarked child-shape law.
For \(\lambda\in\mathcal I_*\), the accepted perturbation is
\[
 Q_{\lambda,\rho;r}(H)
       =h_\lambda(H)B_{\lambda,\rho;r}(H).
\]
It retains the same regular section, fixed nonzero amplitude
\(\eta_*=(2\kappa_*)^{-1}\), and conditional premise
\(\Xi>1,\ \lambda_*=\Xi^{-1}\in(0,1)\).
The multiplier is record-blind. Every complete marked row is positive
and normalized; both fair newborn bits are retained before taking shapes.

For any probability distribution \(\pi\) on old markings define
\[
 B_{\lambda,\rho;\pi}=\sum_r\pi(r)B_{\lambda,\rho;r},\qquad
 Q_{\lambda,\rho;\pi}=\sum_r\pi(r)Q_{\lambda,\rho;r}.       \tag{1}
\]
Within each sum, \(\lambda,\rho\), the original prefix and parent are
fixed. They are not mixed. Baseline parameters \((\lambda_0,\rho_0)\)
may differ from perturbed parameters \((\lambda_1,\rho_1)\).
Case (a) uses one distribution \(\pi\) under both hypotheses.
Case (b) permits independent choices \(\pi_0,\pi_1\).
These are conditional mathematical mixture laws, not a prescribed
history sampler or a physical preparation procedure.

## 2. Mark dependence derived from locality and the admitted held rows

The two selected shapes are [the child-shape theorem](P4_CHILD_SHAPE_OBSERVATION.md)'s
\(K_0\), from \(S=\varnothing\), and \(K_4=T_9\), from \(S=C_4\).
Their intrinsic maximal-principal-downset multisets are
\(\{1,5,5\}\) and \(\{5,5,5\}\). Each arises from exactly one ideal
among the complete eight-ideal row. Summing its two fair-bit branches
gives the ideal probability, with no extra factor of two.

For both selected ideals, the omitted maximal elements are exactly
\(a,b\). The complete deletion product is
\[
 u_\lambda(P_4,r,S)=
 \frac{q_\lambda(P_4-a,r|_{P_4-a},S)
       q_\lambda(P_4-b,r|_{P_4-b},S)}
      {q^0(C_4,r|_{C_4},S)}.                              \tag{2}
\]
Both singleton-deletion parents are five-chains and both selected
ideals are proper in them. Their numerator factors therefore each
acquire one \(\lambda\). The denominator is a fixed four-parent
probability; for \(S=C_4\) it is a full slot, not a scaled proper slot.

### Empty ideal: locality removes every old mark

Proper-slot record locality permits dependence only on marks in the
precursor. There are no marks in the empty precursor. Thus
\[
 e_5:=q^0(C_5,\varnothing)>0,\qquad
 e_4:=q^0(C_4,\varnothing)>0
\]
are independent of all markings. Equivariance identifies the two
unmarked five-chain representatives in (2). Therefore
\[
                       U_{0,r}=\frac{e_5^2}{e_4}=:U_0>0    \tag{3}
\]
for every full old marking. This does not infer mark independence
from a root-sector summary. It follows from empty-precursor locality
itself. No numerical evaluation of \(e_4,e_5,U_0\) is required.

### Entire chain: a specific held-law identity is essential

Locality alone only removes the marks of the excluded cap in each
five-chain numerator. It would still allow dependence on all four
marks in \(C_4\), and the full four-chain denominator may read them all.
A further accepted fixed-instance fact is needed.

The captured theorem package §2 and §4, and law-family supplement §2,
supply the **complete all-mark held identities**
\[
 q^0(C_4,r|_{C_4},C_4)=c_i,\qquad
 q^0(C_5,r',C_4)=e_i=h_i=\theta c_i,\qquad i=r(r_1),       \tag{4}
\]
where \(r'\) is any induced five-chain marking with the same chain root.
Here \(e_i\) is the supplement's \(e\), or the package's \(e'\);
it is not the smaller-seed \(e=1/44\).
The held rows, including full complements, are root-only by the admitted
all-mark proofs of this particular prefix. They are not inferred here
from ten sampled harmonic rows, nor asserted for all record-local laws.

Applying (4) separately to the two actual induced numerator markings
and the denominator in (2) gives
\[
             U_{9,r}=\frac{(\theta c_i)(\theta c_i)}{c_i}
                         =\theta^2c_i.                    \tag{5}
\]
No cap-swap symmetry of a marked state is assumed. The cap records may
differ: locality removes them from the selected numerator slots, and
the held identities remove the non-root chain-mark dependence.

The constants are already admitted:
\[
 c_0=\frac{81}{1100},\qquad c_1=\frac{3231}{44000}
                       =\frac{359}{360}c_0<c_0.             \tag{6}
\]
Only these printed identities are substituted. No original coefficient
archive, optimization, certificate reduction or additional coefficient
table is reconstructed.

Combining (2)–(5), for every marking,
\[
 \boxed{\quad
 B_{\lambda,\rho;r}(K_0)=\rho\lambda^2U_0,\qquad
 B_{\lambda,\rho;r}(K_4)=\rho\lambda^2\theta^2c_{i(r)}.
 \quad}                                                    \tag{7}
\]
The perturbation leaves \(K_0\) unchanged and multiplies \(K_4\) by
\(h_9(\lambda)>1\). Equation (7) concerns two coordinates of the
complete normalized law; it does not filter or condition on those shapes.

## 3. The finite mixture ratio

Put
\[
 \alpha_\pi=\sum_{r:i(r)=0}\pi(r),\qquad
 \bar c_\pi=\alpha_\pi c_0+(1-\alpha_\pi)c_1.
\]
Every distribution on all six marks induces some
\(\alpha_\pi\in[0,1]\), and every such value is realizable.
Correlations between the root, chain and cap marks have no further
effect on these two coordinates, by (3) and (5). We do not need to
assert that every other shape probability is mark-independent.

Equation (1) now gives exactly
\[
 \begin{array}{ll}
 B_{\lambda,\rho;\pi}(K_0)=\rho\lambda^2U_0,&
 B_{\lambda,\rho;\pi}(K_4)=\rho\lambda^2\theta^2\bar c_\pi,\\
 Q_{\lambda,\rho;\pi}(K_0)=\rho\lambda^2U_0,&
 Q_{\lambda,\rho;\pi}(K_4)=
       \rho\lambda^2\theta^2h_9(\lambda)\bar c_\pi .
 \end{array}                                               \tag{8}
\]
Denominators below are strictly positive. Define
\[
 R_{\min}=\frac{\theta^2c_1}{U_0},\qquad
 R_{\max}=\frac{\theta^2c_0}{U_0}.
\]
The complete possible baseline ratios, independently of nuisance
parameters, form the interval
\[
 \frac{B(K_4)}{B(K_0)}\in[R_{\min},R_{\max}].
                                                               \tag{9}
\]
At a fixed perturbed \(\lambda_1\), the complete mixture-ratio interval is
\[
 \frac{Q(K_4)}{Q(K_0)}
       \in h_9(\lambda_1)[R_{\min},R_{\max}].                 \tag{10}
\]

### (a) The same arbitrary distribution under both hypotheses

For the same \(\pi\), the baseline ratio is
\(\theta^2\bar c_\pi/U_0>0\) even if \(\lambda_0,\rho_0\) differ
from \(\lambda_1,\rho_1\). The perturbed ratio is precisely that
number multiplied by \(h_9(\lambda_1)>1\).
Thus the two full shape laws cannot agree.

This conclusion covers every common \(\pi\), not only a known or uniform
mixture, throughout the inherited \(\mathcal I_*\). It is a
model-label separation statement. Across different nuisance parameters,
it does not assert the original fixed-pair likelihood factorization
for every shape, TV preservation from a joint old-mark experiment,
or statistical sufficiency of a compressed partition.

## 4. (b) Different distributions: separation on the whole inherited interval

For independent mixtures, pointwise \(h_9>1\) alone would not be enough:
the baseline could increase its root-zero weight.
The exact two-coordinate separation condition in the present ordering is
\[
                  h_9(\lambda_1)c_1>c_0
 \quad\Longleftrightarrow\quad
                  h_9(\lambda_1)>\frac{360}{359}.           \tag{11}
\]
The accepted family supplies more than merely \(h_9>1\).

[The regular-family theorem](REGULAR_OBSERVABLE_FAMILY.md) §3 defines its compact neighborhood by
\[
 \left|\eta_*(v_j(\lambda)-w_j)\right|\le\frac14
       \quad(\lambda\in\mathcal I_*,\ 1\le j\le11),
\]
with
\[
 w_9=\frac{2\kappa_*^2}{\lambda_*\theta},\qquad
 \eta_*=\frac1{2\kappa_*}.
\]
Hence, on the whole inherited interval,
\[
 h_9(\lambda)\ge
       \frac34+\frac{\kappa_*}{\lambda_*\theta}
       >\frac74>\frac{360}{359}.                           \tag{12}
\]
The strict middle step uses the already admitted
\(\kappa_*>1,\ 0<\lambda_*<1,\ 0<\theta<10^{-10}<1\).
These are symbolic comparisons with existing rational bounds, not an
evaluation of the actual multiplier, coefficients, radius or
probability effect. [The observation-comparison](P4_OBSERVATION_SUFFICIENCY.md) and [child-shape](P4_CHILD_SHAPE_OBSERVATION.md) manuscripts retain this [regular-family](REGULAR_OBSERVABLE_FAMILY.md) neighborhood;
any smaller inherited neighborhood also satisfies (12).
No new radius is chosen and no extra continuity assumption on \(\rho\)
is used.

**Mixture-robust non-mimicry theorem.** For any two distributions
\(\pi_0,\pi_1\) on the full old-marking space, every admitted baseline
\(\lambda_0\in(0,1],\rho_0>0\), and every admitted perturbed
\(\lambda_1\in\mathcal I_*,\rho_1>0\),
\[
                  B_{\lambda_0,\rho_0;\pi_0}
                        \ne Q_{\lambda_1,\rho_1;\pi_1}.      \tag{13}
\]

**Proof.** By (9) the baseline ratio is at most \(R_{\max}\).
By (10)–(12) the perturbed ratio is at least
\(h_9(\lambda_1)R_{\min}>R_{\max}\).
Equality of complete laws would require equality of these ratios,
a contradiction. Equivalently, equality at \(K_0\) forces
\(\rho_0\lambda_0^2=\rho_1\lambda_1^2\); equality at \(K_4\)
would then require
\(\bar c_{\pi_0}=h_9(\lambda_1)\bar c_{\pi_1}\), impossible because
\(\bar c_{\pi_0}\le c_0<h_9(\lambda_1)c_1
 \le h_9(\lambda_1)\bar c_{\pi_1}\). \(\square\)

One nuisance- and mixture-independent law functional is
\[
                 \mathcal G(p)=p(K_4)-R_{\max}p(K_0).
                                                               \tag{14}
\]
For every baseline mixture,
\[
 \mathcal G(B)=\rho_0\lambda_0^2\theta^2(\bar c_{\pi_0}-c_0)
                                                          \le0.
\]
For every admitted perturbed mixture,
\[
 \mathcal G(Q)=\rho_1\lambda_1^2\theta^2
        \bigl(h_9(\lambda_1)\bar c_{\pi_1}-c_0\bigr)>0.
\]
The equality boundary on the baseline side is allowed.
The fixed coefficient \(R_{\max}\) is defined by the original prefix;
it is not numerically calibrated here. This is a separator of exact
laws, not a claim that a single observed shape reveals the hypothesis,
nor a uniform-family sufficiency theorem.

## 5. What a failed ratio criterion would and would not mean

For any fixed pair of admitted parameter values with positive \(h_9\),
the exact two-coordinate mixture criterion is interval intersection:
\[
 [c_1,c_0]\cap h_9[c_1,c_0]\ne\varnothing
       \quad\Longleftrightarrow\quad
       \frac{c_1}{c_0}\le h_9\le\frac{c_0}{c_1}.             \tag{15}
\]
This is an algebraic diagnostic, not an extension of perturbation
admissibility beyond \(\mathcal I_*\).

Necessity for matching the two coordinates follows from (8).
For sufficiency at the level of these two coordinates only, select
\(\bar c_{\pi_0},\bar c_{\pi_1}\) in the two-point convex hull with
\(\bar c_{\pi_0}=h_9\bar c_{\pi_1}\). Choose one sufficiently small
\(s>0\), and set \(\rho_j=s/\lambda_j^2\).
Both scales can be admitted for their entire marked layers because
the positive common-scale construction allows downward scaling.
Equation (8) then matches \(K_0\) and \(K_4\).
All other probabilities remain those of their complete admitted rows;
nothing in this argument makes them equal.

Thus (15), if it held, would establish overlap only of the
two-coordinate projections after choosing scales and mixtures.
It would not be a full-law overlap construction or a loss-of-identifiability
theorem. No full-law overlap is claimed. In the present accepted
neighborhood, (12) excludes (15) altogether, so (13) needs no
calculation of the remaining five shape coordinates.

## 6. Removed premise, scale-zero boundary and physical-access limit

The old full marking, root bit and mixture weights need not be known,
observed, equal between hypotheses, independent or uniform for (13).
This is stronger than simply forgetting the old marking at the output
of a fixed-input experiment.

The following premises remain load-bearing:

- The same original admitted prefix, including the particular canonical
  all-mark held identities (4) and the fixed values (6).
- The same specified \(P_4\) parent class and the declared parent-five
  scaling family.
- One admitted positive common six-parent scale within each hypothesis.
- The same fixed-amplitude regular perturbation, conditional
  \(\Xi>1\), on its accepted neighborhood.
- Complete, exact unlabelled and unmarked child-order access, sufficient
  to distinguish \(K_0\) and \(K_4\).

No mixture over \(\lambda\), original prefixes or parents is included.
No per-mark scale is substituted for the common scale. No actual
occurrence decision for \(\Xi\) is made.
The theorem neither recovers the hidden marking distribution nor
identifies nuisance parameters individually.

Exact model-label separation still does not yield uniform absolute
finite-sample stability. Fix the same admitted \(\lambda\in\mathcal I_*\)
under both hypotheses and any two old-marking distributions. Send their
common-layer scales \(\rho\) toward zero while keeping that \(\lambda\) fixed.
Then all proper probabilities
in each complete marked row are \(O(\rho)\).
There are finitely many markings, so the same conclusion holds for
arbitrary marking mixtures. The unchanged full-birth shape \(K_f\)
has probability tending to one under either hypothesis.
Both families therefore have the point mass at \(K_f\) in their
closures, even though their positive-scale laws cannot coincide by (13).
The two diagnostic shapes become rare. No confidence bound, sample size,
numerical effect, calibrated threshold or uniform positive absolute
margin is supplied.

[The child-shape theorem](P4_CHILD_SHAPE_OBSERVATION.md)'s intrinsic shape recognition removes labels, marks, newborn
identity and the supplied parent embedding from the output requirement.
It does not construct a physical readout of the complete order.
Missing/delayed records, noisy order relations and unknown parent mixtures
remain outside the theorem. Hidden old-mark robustness is not a physical
observation channel, QM reconstruction, geometry or gravity result.

## Public premises and evidence scope

The [nuisance-identifiability theorem](P4_NUISANCE_IDENTIFIABILITY.md)
supplies the fixed-old-marking separation and common-scale comparison.
The [child-shape theorem](P4_CHILD_SHAPE_OBSERVATION.md) supplies intrinsic
shape identification, with the [P4 observation comparison](P4_OBSERVATION_SUFFICIENCY.md)
retaining the accepted fixed-amplitude row and neighborhood.
The [regular-family theorem](REGULAR_OBSERVABLE_FAMILY.md), §3, supplies
the coordinate-deviation bound on the whole inherited neighborhood from
which the multiplier estimate is derived here.
The [baseline-scale theorem](BASELINE_SCALE_THEOREM.md) supplies the complete
scaling, maximal-deletion and admitted common-scale construction.
The [theorem package](THEOREM_PACKAGE.md), §§2 and 4, and
[law-family supplement](LAW_FAMILY_SUPPLEMENT.md), §2, state the complete
all-mark held identities of the fixed instance. Those identities remain
inherited premises, not consequences of locality alone.

References in §2 to captured expositions concern retained private originals.
The captured package and supplement are accepted
expositions of the fixed instance, not newly authenticated original
coefficient certificates.

The locality argument, two held-identity substitutions, mixture intervals,
non-mimicry proof and projection-overlap criterion are manual deductions.

The comparison retains the same original prefix and parent, one admitted
common scale within each hypothesis, and the whole inherited perturbation
neighborhood. Equal and different hidden old-marking distributions are both
covered. No mixture over law parameters, prefixes or parents and no per-mark
scale is added. Projection overlap would not establish full-law overlap.
The zero-scale closure limit does not supply a uniform absolute margin or
finite-sample guarantee. Complete exact order access remains a mathematical
premise, with no physical observation channel supplied.

Private source labels, exact source/check correspondence, source fingerprints,
review/freeze records, raw administrative receipts and reader/checker scripts
are intentionally withheld. These public relative dependencies identify
mathematical premises; they do not supply private custody records or original
coefficient authentication. This edition is conditional mathematical exposition,
not an executable installation or an independently replayable custody package.
See the [publication note](PUBLICATION_NOTE.md) and
[public evidence policy](../../coordination/REDACTED_PUBLICATION.md).

## A common separator for a constrained prefix family

The [prefix-family manuscript](P4_PREFIX_FAMILY_SEPARATOR.md) replaces equality
of the entire original prefix by shared held calibration and explicit validity
conditions on actual complete prefixes. The common law-functional coefficient
is 648/25; each perturbable member keeps its own neighborhood and fixed
amplitude. The class may be a singleton, and no second distinct member is
established. The measurable-mixture corollary concerns admitted complete laws.
Exact calibration supplies no numerical probability effect, uniform
finite-sample guarantee or physical observation channel.
