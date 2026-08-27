# Exodus/DET8 adaptive relational scheduler

**Status:** Synthetic Bayesian experiment-design layer over the relational
tomography model. It schedules discriminator measurements; it does not predict
an Exodus force or supply evidence for a novel DET channel.

Implementation: `det8/models/exodus_adaptive_scheduler.py`

Run:

```bash
python3 -m det8.models.exodus_adaptive_scheduler
python3 run_tests.py
```

The first command emits the complete adaptive study as JSON. The second runs
the 260-test DET8 suite.

---

## 1. Objective

The relational tomography run defined 144 possible interventions. Exhausting
that entire grid would be expensive in a physical experiment. The scheduler
therefore asks

\[
\boxed{
x_{n+1}=\arg\max_x I(M;Y_x\mid D_n),
}
\]

where (M) is the endpoint hypothesis, (Y_x) is the next three-vector force
observation under intervention (x), and (D_n) is the accumulated record.

The available controls are:

- wall distance;
- terminal common mode;
- lead routing;
- device rotation;
- chamber rotation;
- preparation path.

After each simulated observation, Gaussian likelihoods update the posterior
probability of every endpoint model.

---

## 2. Declared hypotheses

| Hypothesis | Predicted relation |
|---|---|
| Null | No force |
| Device internal | Constant device-axis force |
| Common mode only | Electrical-state-dependent device-axis force |
| Boundary electrode | Common mode plus wall-distance dependence |
| Lead only | Lead route coupled to chamber normal |
| Full relational | Boundary-electrode plus lead/chamber components |
| Full plus Earth | Full model plus a (50\ \mu\mathrm N) Earth-fixed vector |
| Full plus history | Full model plus a (10\ \mu\mathrm N) matched-state path difference |

The two novel-channel amplitudes are deliberately declared sensitivity scales.
Scheduler performance changes if those scales or the measurement noise change.

---

## 3. Information calculation

Evaluating full Monte Carlo information gain for all 144 candidates after
every observation is unnecessarily expensive. The implemented hybrid uses:

1. a moment-matched Gaussian predictive covariance to rank all candidates;
2. an uncapped predictive-disagreement score to avoid ties when several
   candidates approach the three-bit prior-entropy limit;
3. direct Monte Carlo expected-posterior entropy on the 12 best candidates;
4. Bayesian updating with the selected vector observation.

This reduces a full scheduler run from roughly two minutes to a few seconds
while retaining an explicit Monte Carlo audit at the final selection step.

---

## 4. Two-stage stopping rule

The scheduler distinguishes two questions that should not be collapsed.

### Stage 1: Which endpoint family?

The target family is

\[
\{\text{full relational},\text{full+Earth},\text{full+history}\}.
\]

Crossing 95% family probability establishes that boundary and lead relations
are required. It does **not** establish which, if any, novel extension is
present.

### Stage 2: Is a particular novel channel required?

Earth and history hypotheses must independently cross a 95% exact-model
threshold. If no exact model reaches that threshold, the result remains
inconclusive even when Stage 1 succeeds.

This prevents endpoint discovery from being reported as discovery of a novel
DET interaction.

---

## 5. Example adaptive choice

At (50\ \mu\mathrm N) per-component noise, the hybrid scheduler chooses:

| Control | Selected value |
|---|---:|
| Wall distance | (0.08\ \mathrm m) |
| Common mode | (+4\ \mathrm{kV}) |
| Lead routing | Same end |
| Device rotation | (90^\circ) |
| Chamber rotation | (0^\circ) |
| Preparation sign | (-1) |

One vector observation raises the relational-family probability from 37.5%
to 97.79%. The individual posterior probabilities remain distributed:

| Surviving model | Probability |
|---|---:|
| Full relational | (29.10\%) |
| Full plus Earth | (41.96\%) |
| Full plus history | (26.72\%) |
| Lead only | (2.21\%) |

Thus the observation locates the endpoint family but does not justify a novel
submodel. The scheduler stops Stage 1 and requests targeted Stage-2 controls.

---

## 6. Adaptive versus random scheduling

Thirty trials were run with the full-relational model as truth,
(50\ \mu\mathrm N) component noise, a 95% family threshold, and a 20-step
budget:

| Strategy | Success | Median measurements | Mean measurements |
|---|---:|---:|---:|
| Adaptive information gain | (100\%) | (1.0) | (1.07) |
| Random without replacement | (100\%) | (3.5) | (3.87) |

The adaptive policy saves a median 2.5 vector-force measurements. This is a
small synthetic design, so the numerical efficiency gain is conditional on
the declared hypotheses. The main result is that intervention choice contains
more information than repetition count alone.

---

## 7. Control ablation

| Available control set | Candidate states | Family threshold | Final family probability |
|---|---:|---:|---:|
| All controls | 144 | Reached in 1 | (99.996\%) |
| No chamber rotation | 72 | Reached in 1 | (99.895\%) |
| No lead rerouting | 48 | Reached in 1 | (99.899\%) |
| No preparation reversal | 72 | Reached in 1 | (99.997\%) |
| One static geometry | 3 | Not reached | (71.49\%) |

For broad endpoint-family identification, several alternative high-contrast
controls remain sufficient. A single static geometry is not. Exact Earth or
history claims still require the corresponding rotation or preparation
contrasts; the Stage-1 ablation should not be read as making those controls
unnecessary.

---

## 8. Positive and negative novel-channel controls

With (10\ \mu\mathrm N) component noise and a 40-step exact-model budget:

| Synthetic truth | Selected model | Steps to 95% | Final truth probability |
|---|---|---:|---:|
| Full relational; no novel channel | Full relational | Not reached | (88.60\%) |
| Injected (50\ \mu\mathrm N) Earth-fixed term | Full plus Earth | (1) | (99.9998\%) |
| Injected (10\ \mu\mathrm N) matched-history term | Full plus history | (11) | (97.07\%) |

The positive controls are recovered. The no-novel-channel case selects the
correct model but does not reach 95%, so the scheduler reports an inconclusive
exact-model verdict rather than overstating absence. Confirming that a small
extra term is zero can require more information than detecting a large
positive term.

---

## 9. What this adds to DET

The adaptive scheduler turns relational governance into a sequential research
procedure:

1. declare conventional and novel endpoint hypotheses;
2. choose the intervention with maximum expected discrimination;
3. update the relational record with the full vector observation;
4. stop when the endpoint family is identified;
5. open a stricter second stage for any proposed Earth/history extension;
6. retain “inconclusive” when the exact posterior threshold is not crossed.

What emerged is not a new force. It is a disciplined way for DET to decide
which experiment should happen next while minimizing both wasted trials and
novel-channel overclaiming.

---

## 10. Limits and next implementation

The scheduler currently uses point hypotheses with calibrated amplitudes,
independent Gaussian noise, equal model priors, equal experimental cost, and
synthetic observations generated by one of its own models. A laboratory
scheduler needs hierarchical amplitude priors, correlated sensor drift,
mechanical cross-axis calibration, switching costs, voltage and safety limits,
and the ability to ingest real measurements.

The next implementation path is therefore a cost-aware live-data scheduler:
update nuisance parameters and endpoint probabilities from measured force,
voltage, charge, temperature, and chamber-reaction records, then rank only
interventions that are physically safe and available.
