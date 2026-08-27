# Neutron-lifetime RET adapter

**Status:** Published-aggregate inference plus prospective synthetic experiment
design. This adapter does not ingest raw collaboration data and does not claim
to resolve the neutron-lifetime discrepancy.

**Implementation:** `det8/models/examples/neutron_lifetime.py`

Run:

```bash
python3 -m det8.models.examples.neutron_lifetime
python3 run_tests.py
```

## 1. Question

The adapter asks a more specific question than “beam or bottle?”:

\[
\boxed{\text{Which measurement relationship carries the discrepancy?}}
\]

It separates neutron confinement from decay-product readout. This matters
because the J-PARC result is a beam measurement that detects electrons rather
than the protons used by the historical NIST beam result.

The assimilated aggregate records are:

| Record | Method/readout | Lifetime used |
|---|---|---:|
| [NIST BL1](https://arxiv.org/abs/1309.2623) | cold beam/proton | \(887.7\pm2.25\) s |
| [UCNτ](https://arxiv.org/abs/2106.10375) | magnetic bottle/survivor | \(877.75\pm0.36\) s |
| [J-PARC](https://arxiv.org/abs/2412.19519) | pulsed beam/electron | \(877.2\pm4.35\) s |

Statistical and the larger quoted systematic uncertainty are combined in
quadrature for this reduced demonstration. The J-PARC systematic is reported
asymmetric (\(+4.0/-3.6\) s); the adapter uses the larger \(+4.0\) s, so the
asymmetry is presently collapsed rather than modeled. The later UCNτ update is
not also assimilated because its data overlap the earlier result and no
empirical cross-release covariance has been supplied. The core can now ingest
such a covariance when it is available.

## 2. Declared model families

All lifetimes are expressed relative to 880 s. The declared families are:

\[
\begin{aligned}
M_0 &: \tau=880+\delta\tau,\\
M_P &: \tau=880+\delta\tau+b_P I_{\rm proton},\\
M_B &: \tau=880+\delta\tau+b_B I_{\rm bottle},\\
M_S &: \tau=880+\delta\tau+b_S s_x,\\
M_D &: \tau=880+\delta\tau+b_D S_{\rm beam},\\
M_\bot &: \text{declared set inadequate}.
\end{aligned}
\]

Here \(S_{\rm beam}=+1\) for beam records and \(-1\) for bottle records, so
\(b_D\) is a dark-decay shift that lengthens the beam beta-partial lifetime and
shortens the bottle survival lifetime with opposite sign. \(b_P\), \(b_B\), and
\(b_S\) are nuisance relationships. The coordinate \(s_x\) is a declared
synthetic contrast axis for spectrum-sensitive pressure tests; it is not
claimed as a measured physical state variable.

Complexity priors penalize additional parameters, and the dark-decay model
receives the strongest penalty under RG1. Gaussian priors allow every offset
to be inferred rather than fixed to the historical discrepancy.

## 3. Literature-posterior result

Sequential assimilation gives:

| Declared model | Posterior support |
|---|---:|
| Proton-pipeline relationship | 0.8033 |
| Spectrum/state relationship | 0.1267 |
| Bottle-storage relationship | 0.0564 |
| Dark decay channel | 0.0114 |
| Common unshifted lifetime | 0.0004 |
| `M_bottom` | 0.0018 |

Within the proton-pipeline model, the inferred quantities are:

\[
\tau=877.77\pm0.35\ \mathrm{s},
\qquad
b_P=9.45\pm2.22\ \mathrm{s}
\quad(1\sigma).
\]

This is conditional predictive support inside a reduced hypothesis set. In
particular, \(b_P=9.45\) s is an **equivalent model offset**, not a demonstrated
correction to the historical NIST apparatus. It fuses absolute fluence
calibration, proton detection efficiency, and proton backscattering; with only
one proton record these three are collinear, so they are not separated here.

The J-PARC record is the main relational discriminator: it shares the beam
method and beta-decay readout class with beam experiments, but it does not
share proton detection. In this declared model set it raises the
proton-specific model from 0.477 to 0.803 and lowers the dark-decay model
from 0.096 to 0.011. A universal dark-decay channel would lengthen *every*
beam record, so the J-PARC electron-beam value (which agrees with the bottle
value) is precisely the observation that suppresses it.

## 4. Next-action result

The literature state is `CALIBRATE`, because the posterior standard deviation
of the equivalent proton-pipeline offset is still 2.22 s, above the declared
1 s calibration gate.

The scheduler ranks:

```text
absolute_proton_flux_audit
```

above another lifetime measurement. It has both scientific-question
information and nuisance information. The proposed action represents a joint
audit of absolute neutron fluence and proton readout, expressed in equivalent
lifetime seconds. A real adapter would replace this reduced observable with
the audit's raw monitor efficiencies, geometry, acceptance, and covariance.

Under a declared synthetic truth with a 9.5 s proton-specific offset, one such
audit raises the proton-pipeline posterior above 0.999 and advances the state
to `CLOSE`. The `CLOSE` terminal gate is here named `cross-method consistency`
rather than the momentum conservation closure used by the thrust fixtures. That
is a simulation validation of the decision rule, not a forecast of the audit
result.

## 5. Correlation and nonlinear-observation pressure tests

The same three literature records can be assimilated as one vector with a
complete covariance matrix. At zero off-diagonal covariance, the joint update
matches sequential independent assimilation to better than \(10^{-12}\) in
posterior weight.

Because no empirical NIST–J-PARC cross-covariance has been declared, the
adapter reports a sensitivity sweep rather than choosing one:

| Assumed beam-record correlation | Proton-pipeline support |
|---:|---:|
| -0.5 | 0.732 |
| 0.0 | 0.798 |
| +0.5 | 0.890 |

These are assumption sensitivities, not measurements. Their spread shows why
shared-systematic covariance cannot be silently ignored or invented.

The adapter also exposes a raw nonlinear bottle observable at storage times
200 s and 1000 s:

\[
S(t)=\exp\!\left[-\frac{t}{\tau_n}\right].
\]

The two survival fractions accept a correlated counting covariance. Cubature
propagation gives \(E[S(t)]\neq S(t;E[\tau])\) under lifetime uncertainty and
updates the lifetime state while preserving the general RET interface.

## 6. Declared-truth pressure suite

The adapter also starts from the prior and generates six adaptively scheduled
actions under each declared truth:

- common lifetime;
- proton-pipeline offset;
- bottle-storage offset;
- spectrum/state dependence;
- dark-decay channel.

The leading posterior model matches all five generators. The common model is
recovered conservatively at 0.853; all four nonzero-channel cases exceed
0.999. This is a matched-generator test and therefore checks implementation
identifiability, not external validity.

An incompatible 950 s precision electron-beam observation drives
`M_bottom` to 1.0 and enters `MODEL_FAILURE`, demonstrating that the adapter
does not force every observation into the nearest named explanation.

## 7. Interpretation and next data requirements

The present finding is:

> Given these three independent aggregate values, their declared errors, and
> this reduced model set, a proton-specific audit has greater expected value
> than immediately escalating to a dark-decay claim.

The result does not prove that a proton or flux systematic exists. A serious
version needs collaboration-level likelihoods or sufficient statistics for:

- absolute fluence calibration and its shared uncertainties;
- detector efficiency, acceptance, backgrounds, and stability;
- neutron velocity and spectral distributions;
- trap cleaning, depolarization, heating, and loss channels;
- empirically estimated correlations between published analyses;
- asymmetric and non-Gaussian systematic likelihoods.

The first item is now representable as a joint covariance; it remains a data
requirement. Asymmetric and non-Gaussian likelihoods remain a core extension;
the J-PARC record is already a concrete instance (its systematic is
\(+4.0/-3.6\) s, collapsed here to the larger \(+4.0\) s).

## 8. Prior-hyperparameter sensitivity

The proton-pipeline conclusion is prior-driven at \(n=3\), so the adapter now
reports a one-axis sweep of the complexity penalty, the open-model prior, and
the open-model scale around the reference configuration (\(\lambda=0.8\),
\(p(M_\bot)=0.03\), scale \(30\) s). Across the sweep the proton-pipeline
posterior support ranges from 0.771 to 0.845, and the dark-decay support from
0.002 to 0.024. Neither range reverses the ordering, but the proton-pipeline
spread is material: the 0.803 point estimate sits inside a roughly
\(\pm 0.04\) prior-driven band, not a precise number. This sweep is reported
in the fixture output alongside the correlation sweep of Section 5.

## 9. Raw survival-curve and counting observables

The published aggregate records are not the bottle method's raw observable. A
bottle experiment counts surviving neutrons at storage times, and a beam
experiment counts decay products. The adapter now exercises both raw paths and
checks them against the aggregate.

**Survival-curve consistency.** Assimilating a synthetic bottle survival
fraction \(S(t)=\exp(-t/\tau_n)\) at storage times 200 s and 1000 s through the
nonlinear cubature path recovers \(\tau=877.99\) s from the common model,
consistent with the published UCNτ value \(877.75\) s. The raw nonlinear
representation and the aggregate Gaussian record therefore agree; this is a
consistency check on the representation, not new information.

**Binomial/Poisson counting.** `det8/models/examples/neutron_counting_evidence.py`
feeds the evidence layer's Binomial and Poisson families with physically-shaped
counts: a million-neutron bottle surviving count, and proton/electron beam
decay counts at the measured precision scale. The raw counts favor the
proton-pipeline hypothesis at weight above 0.9999, suppress dark decay below
\(10^{-6}\), and reproduce the aggregate direction. The bottle survivor count
alone already rules out a dark-decay channel that shortens the bottle lifetime,
and the NIST proton count is what flips support from a common lifetime to a
proton-specific one. These counts are synthetic roundings of the published
lifetimes; no collaboration raw data is ingested.
