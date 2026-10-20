# D4-P: native width does not identify a physical readout

20 October 2026. A bounded conditional theorem and its operational limitation.
No simulation, experiment, detector proposal or empirical correspondence claim.

## 1. What the admitted law determines

Use the fixed original law, not an arbitrary DET growth law: baseline \(B\),
its admitted harmonic perturbation \(Q\), \(\lambda=1\), and
\(\epsilon=1/4\). Each trial starts at
\(P_*=C_3\oplus A_3\) with all six old marks zero. The complete birth row
includes eleven ideals and both fair newborn bits. The arbitrary
positive-semidefinite payload is retained through scalar maps
\(\mathcal B^i_{S,b}(\mathfrak D)=q_i(P_*,0,S)\mathfrak D/2\).
It does not select a physical measurement channel.

For the complete resulting order, let \(W\) be its width and \(Y=W-3\).
Then \(Y\in\{0,1\}\) and the admitted identity is

\[
 \delta=\mathbb E_QY-\mathbb E_BY
       =\rho U_0/4>0,\qquad U_0=ag_0^3/b_0^3>0.
\]

Consequently the probability of width four increases by exactly \(\delta\).
This is a dimensionless statement about a specified mathematical distribution,
not merely an informal trend. Computing \(Y\) from the exact emitted order
requires three cap-comparability queries when the initial-parent embedding
is supplied. Physical access to that order and embedding is not supplied.

The theorem package supplies conditional model premises; the law-dependence
supplement prevents treating the prescribed law as uniquely selected by DET.
The diagnostic and its independent review establish the exact-order channel
and statistical design, not an observed result. Their operational status
remains **ABSTAIN / NOT RUN**, lacking a certified numerical effect lower
bound and a validated exact sampler. Supplying these two simulation inputs
alone would still not establish a physical preparation or readout.

## 2. Explicit underdetermination theorem

Let \(X=(S,b)\) range over the complete native birth outcomes and let
\(\mu_i(x)=q_i(P_*,0,S)/2\), \(i\in\{B,Q\}\).
The terminal order, marks and \(Y(x)\) are determined by \(x\).
An additional readout \(O\) needs a normalized conditional channel
\(K(do\mid x)\). Use the **same channel for both arms**, with no feedback
into their native transitions. Define

\[
 \nu_i(dx,do)=\mu_i(dx)K(do\mid x).
\]

**Claim.** If the admitted premises put no further restriction on this
external channel, they do not identify its output law.

**Proof.** Normalization gives
\(\int\nu_i(dx,do)=\mu_i(dx)\), integrating over \(o\).
Hence every native outcome probability and every native order-law identity
is unchanged. The result also preserves the full payload map, not just its
trace: multiplying \(\mathcal B^i_x(\mathfrak D)\) by \(K(do\mid x)\)
and integrating over \(o\) returns exactly
\(\mathcal B^i_x(\mathfrak D)\) for every allowed \(\mathfrak D\).
The following channels nevertheless have different readout laws. \(\square\)

1. **Unfixed dimensional scale.** Fix one external output unit \(U\).
   For any positive gain \(\gamma\), measured in that same unit, take the
   deterministic readout \(O_\gamma=\gamma Y\). Its mean arm contrast is
   \(\gamma\delta\); the equally normalized choice
   \(O_{2\gamma}=2\gamma Y\) gives \(2\gamma\delta\).
   Both recover \(Y\) exactly when their gain is known. Thus native
   identifiability of \(Y\) does not supply its proposed dimensional gain.
   These are different gains in the same unit, not a change of units.

2. **Unfixed response.** Let
   \(O_\eta=Y\mathbin{\mathrm{xor}}N_\eta\), where
   \(N_\eta\) is independent of \(X\) and
   \(\Pr(N_\eta=1)=\eta\), \(0\le\eta\le1/2\). Then
   \[
    \Pr_i(O_\eta=1)=\eta+(1-2\eta)\Pr_i(Y=1),\qquad
    \mathbb E_QO_\eta-\mathbb E_BO_\eta=(1-2\eta)\delta .
   \]
   Two informative choices, \(\eta=0\) and \(\eta=1/4\), give contrasts
   \(\delta\) and \(\delta/2\). At \(\eta=1/2\), both arm outputs are
   exactly fair: the contrast disappears while the native gain remains.
   The added output is **not** the native newborn record bit. Its response
   does not replace or violate that bit's admitted fairness.

A timing version is equally explicit. Let \(h_P(v)\) be the number of
vertices in a longest chain ending at \(v\), minus one. Then \(u\prec v\) implies
\(h_P(u)<h_P(v)\). For a fixed external time unit, all assignments
\(t_\tau(v)=\tau h_P(v)\), \(\tau>0\), preserve that ordering. Replacing
\(\tau\) by \(2\tau\) doubles every comparable-pair duration while leaving
the entire native law unchanged. This is an added mathematical timestamp
assignment, **not** a physical clock or a Lorentzian construction.

These are logical extensions witnessing a missing restriction, not claims
that any particular channel is a realizable apparatus. They introduce no
new native dynamics or record-formation rule. If readout disturbs the
native process, the joint dynamics need specification instead of the
non-feedback factorization above.

## 3. Limitation and the missing premise

The exact-order observation is well-defined; its physical interpretation is
not identified by the four admitted sources. A physical correspondence would
need, independently of fitting the desired result, both a preparation map
from an operational procedure to the native input distribution and an
observation channel from native outcomes to measured outputs. Even granting
the exact native preparation, the constructions above leave readout scale
and contrast unfixed.

This is not a universal no-go for DET. Further justified premises could
restrict those maps. It is also not a new QM or gravity derivation: passive
payload retention supplies no informative quantum measurement, and order
height supplies no dimensional time or metric. Identical native predictions
with different external readouts demonstrate **current channel
underdetermination**, not a contradiction in the native width theorem.

## 4. Minimal future operational channel contract

These are missing requirements, not a completed discriminator or permission
to begin an experiment.

| Item | Required specification |
| --- | --- |
| Units | Output quantity and units; independently justified gain, offset and any time conversion, with calibration bounds. |
| Preparation | Procedure-to-native-state map; what would realize each compared law; initial-state, reset and selection errors without favorable-outcome conditioning. |
| Observation | A fixed channel or joint measurement dynamics; access to the relevant order information; noise, missed/delayed records, selection and backaction; distinction between measured outputs and native marks. |
| Baseline | Operational comparator and named conventional/nuisance explanations; distinguish their output predictions, not just two symbolic laws. |
| Uncertainty | Full preparation/channel/calibration error budget; effect lower bound after the channel; justified sampling assumptions, held-out design, sample size and stopping rule. |
| Falsifier | A preregistered statistic, threshold and PASS/FAIL/ABSTAIN conditions; a stated observation that rejects or downgrades the proposed correspondence. Channel or premise failure must not be relabeled as a universal DET refutation. |

## Sources, review and evidence limits

The [admitted model](THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model),
[law-family result](LAW_FAMILY_SUPPLEMENT.md), and
[width diagnostic](WIDTH_DIAGNOSTIC.md) supply the native premises. The diagnostic
has a separate independent review; this note does not rerun or instantiate it.
Independent manual review checks the counterchannels, payload marginalization,
and timestamp construction. These are mathematical arguments, not a detector
model, proof-assistant verification or an empirical result.

The private record preserves a failed strict file-identity check after one
public source file’s identity changed at the same path during integration. A separate
bounded readback confirmed the source texts were byte-identical to the initial
captures. That establishes content correspondence; it does not turn the earlier
strict-identity failure into a pass or reconstruct historical custody.

Exact private source paths, fingerprints, read captures and administrative
receipts remain local under the [publication policy](../../coordination/REDACTED_PUBLICATION.md).
The original note and failure are preserved. This public edition changes only
provenance and navigation text; the mathematical argument above is retained.

This closes the bounded identifiability question for the declared non-feedback
extension class. It supplies no physical preparation, readout calibration,
coefficient acquisition, simulation, protected validation, production
qualification or RET result. A physical prediction still requires the additional
operational commitments in the table above.
