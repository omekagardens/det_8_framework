**Applied-comparison repairs and a bounded application design**

13 September 2026. Coordinator-owned RI-11/RI-12 successor to the
[independent review](../../indep%20ndent_review.md) and
[implementation plan](../../REVIEW_IMPLEMENTATION_PLAN.md). This is an audited
work specification and implementation record, not an executed pilot. No RET
source, calibration bank, external data or historical validation results were
changed for this design.

Publication is tracked separately in the
[publication backlog](PUBLICATION_BACKLOG.md). The exact identifiability module
and its 108 tests are published in verified checkpoint `38be4c0`. RI-11's
chronology dependencies and the synthetic comparator's RET import closure
remain unpublished prerequisites; local acceptance below does not imply that
those complete consumers are available from the remote branch yet.

**RI-11: accepted statistical repair batch**

RI-11 is accepted for its scoped arithmetic and reporting contract. It changed
`det8/applied_physics/adversarial.py`, `applied_tests.py` and
`discriminator.py`, the directly affected `run_tests.py:test_applied_physics`
group, and new `det8/tests/test_applied_comparison_contracts.py`. The audited
direct consumers `scripts/full_year_aging.py` and `scripts/g11_quadratic.py`
received narrow chronology/reporting changes, preserving configured paths and
validated single-pass ingestion; their affected operational assertion was
updated. Source reservations are released. Coordinator verification passed
54 focused tests and 12 legacy checks, with separate independent numerical
and chronology review. The retained specification below records the repair's
mathematical basis. Historical reports remain historical; no real-data
reanalysis or calibrated application benefit is established.

Current interfaces intentionally change: `bic()` returns `None` unless the
caller explicitly confirms its regularity/sampling premises, and also at
zero RSS under unknown variance. Causal winner/count fields are `None`;
fit-family labels and descriptive RSS replace mechanism claims. Clock reports
retain dated source records and actual elapsed days. Missing legacy `.clk.Z`
chronology is refused. Interval averaging and clock-error covariance remain
unmodeled; descriptive errors do not cure these scientific limitations.
Detected positive-square underflow and nonfinite results refuse explicitly;
an arithmetic refusal cannot silently remove a candidate from a grid search.
These are bounded numerical guards, not general floating-point certification.

The current RSS-based BIC assumes independent Gaussian errors with an unknown
common variance. Distinguish it from known-noise likelihoods and descriptive
roughness. The two Gaussian arithmetic contracts are:

| Noise declaration | Negative twice log likelihood | Parameter accounting |
|---|---|---|
| Known positive-definite covariance `R` | `rᵀR⁻¹r + log det R + n log(2π)` | Count fitted identifiable mean parameters; fixed independent calibration constants are excluded. |
| Unknown common iid variance, `RSS > 0` | `n[log(2π) + 1 + log(RSS/n)]` | Count identifiable mean parameters plus the estimated variance. |

An ordinary BIC approximation also needs its regularity and sampling
assumptions. A correct Gaussian likelihood by itself does not justify that
approximation at a degeneracy, clipping boundary or arbitrary finite search
bank. Common constants and the extra variance parameter cancel between
comparable same-data iid models; those omissions alone do not explain every
old ranking defect. Correlated data need an actual covariance/time-series
likelihood, not an improvised effective sample count.

For the unknown-variance path, `RSS=0` makes the likelihood unbounded at zero
variance. Return comparison unavailable with that reason; do not award an
automatic winning score or introduce a post hoc residual floor. A known
positive noise variance gives a finite likelihood at zero residual. Reject
negative/nonfinite RSS, mismatched lengths and invalid sample/parameter counts.

Parameter corrections must follow identifiability:

- The DDD baseline fits slope and intercept: two mean parameters, not one.
- The log-linear model has three mean parameters when its design has rank
  three. `a log(1+t)+bt+c` is not necessarily monotonic: its derivative
  `a/(1+t)+b` can change sign.
- Exponential plus offset has three mean parameters where identifiable;
  vanishing amplitude or very large time constant can create degeneracy.
- The offset-free stretched exponential has three mean parameters; fixing
  its stretch exponent at one leaves two. Boundary/grid qualification remains.
- Do **not** mechanically change the κ model's count from four to five.
  With `y=sκ`, fixed activation energy and no clipping, its equation is
  `y′=−(y−sκ_eq)/τ + saΦ`. At most `(sκ₀,sκ_eq,sa,τ₀)` are identifiable under
  sufficiently varied forcing. Constant/no forcing may lower rank further.
  Saturation can expose scale but changes regularity. Prefer explicit output
  coordinates or independently calibrated scale; report degeneracy rather
  than counting named search quantities or grid points.

For roughness `Q=Σᵢ(yᵢ₊₁−yᵢ)²=yᵀLy` on a path, Gaussian data with mean `μ`
and covariance `Σ` satisfy

`E(Q)=μᵀLμ+tr(LΣ)` and
`Var(Q)=2tr[(LΣ)²]+4μᵀLΣLμ`.

For constant mean and iid variance `σ²` on `n` nodes, these reduce to
`E(Q)=2(n−1)σ²` and `Var(Q)=(12n−16)σ⁴`. The existing `n=20, σ=0.1`
generator therefore has mean **0.38**, variance **0.0224**. The other
generator's `σ=0.01` contributes **0.0038** even before its deterministic
roughness. Adjacent differences share errors. The hundredfold difference in
the generators' noise variances can explain classification without identifying
a diffusion mechanism.

The first repair should return a named descriptive roughness diagnostic and
its declared null moments, remove BIC labeling from squared discrepancies and
replace physical mechanism labels with descriptive fit-family labels. A later
mechanism comparison requires common observation-noise treatment and an
ordinary correlated-noise/diffusion alternative.

`run_aging_adversarial` currently uses observation index as elapsed days.
Preserve actual chronology from ingestion or refuse unsupported gaps; missing
days cannot silently shorten a days-valued time constant.

Meaningful acceptance checks: independent Gaussian likelihood arithmetic;
parameter-penalty differences at equal likelihood; scale-confounded κ pairs
with identical unclipped output; fitted baseline intercept recovery; analytic
roughness moments and shared-error covariance; a nonmonotonic log-linear
example; and a missing-day fixture. Replace legacy assertions requiring
`RSS=0 → −∞`, DET/defect classifications and 10/10 synthetic identification.
Do not tune thresholds to retain those old success counts.

**RI-12: offline voltage-comparator calibration adviser**

The proposed task is to decide whether an offset correction is useful and
which reference level to measure next within a short, stable session.
The model `y=gx+b+ε` compares gain-only and gain-plus-offset explanations.
It fits the present static linear-Gaussian RET API and does not require a
general drift, mixture, change-point or quantum likelihood extension.

| Design component | Initial specification for feasibility review |
|---|---|
| Estimand | Response relative to the chosen reference standard, including prediction at a declared operating input; no separate device mechanism is inferred. |
| Actions | Three fixed reference levels, such as −1, 0 and +1 V, with measured reset/settling/acquisition costs. |
| Episode | At most two parameters per model, six selected training records and four terminal held-out records. |
| Inference | Frozen Gaussian priors, declared noise/covariance and a named public Objective version; use public experiment, ingestion, prediction, ranking, decision, closure and replay contracts. |
| Noise limits | Independently characterized covariance; no unexplained drift, carryover or significant errors in the input reference. Shared reference uncertainty cannot be treated as independent observation noise. |
| Evidence status | Design only. G2 completion does not calibrate this additional apparatus scenario or validate measured application benefit. |

Require raw readings, actual reference/input values, timestamps, device and
session identity, calibration identity, temperature/stability conditions,
reset history, measured action costs and raw-source hashes. Preserve missing
and rejected readings with reasons. Use earlier sessions to select priors,
noise declarations and feasibility limits; freeze them before evaluating
later sessions. Terminal checks remain unseen during fitting/action choice.

If comparing policies by offline replay, precollect a complete action-by-slot
bank inside each demonstrably stable episode. Reveal only the selected
action's next unused observation. Preserve timestamps and source slices.
Report actual collection cost separately from replay-estimated policy cost.
If unselected measurements change later observations through heating, drift
or carryover, this bank does not support the proposed counterfactual replay.
Refuse that comparison or redesign it. Offline replay is not an executed
adaptive laboratory trial.

Use identical inputs, priors/noise assumptions, training budgets and terminal
checks for a fixed calibration design including zero and nonzero references,
a conventional greedy uncertainty-per-cost design and RET's information/cost
policy. Full gain-plus-offset regression is a conventional prediction
baseline. A weak random policy must not be the sole comparator.

Set the operational prediction tolerance from the actual instrument task
before evaluation. One percent of full scale is only a candidate for feasibility
review. Report held-out predictive score/error/coverage; cost to the declared
precision or decision target; wrong correction decisions; refusals and model
inadequacy; and replay/source-accounting integrity.

A possible pilot benefit target is ten percent lower restricted mean
measurement cost than the strongest frozen conventional design without
worsening a prespecified prediction/error margin. This is a proposed pilot
criterion, not an amendment to G2. Failed/refused episodes receive full-budget
cost in that restricted endpoint; actual cost is reported separately.
Evaluation size follows the desired uncertainty, not convenience: for example,
zero failures in about 300 independent episodes gives a one-sided 95% upper
error bound near one percent. Correlated or few sessions support a weaker,
explicitly bounded claim.

**QR contribution: answerability before confidence**

The first bounded implementation is accepted in a separate applied
helper: [exact rational design/target certificates](IDENTIFIABILITY_CONTRACT.md),
with an independently written test suite. Coordinator replay passed 162
focused tests (108 identifiability and 54 existing applied/consumer cases);
the independent author also passed the 108 new cases under optimized Python.
This concerns structural identification
under a known linear mean map on unrestricted real parameters, not exact
recovery from finite noisy observations. Each supplied candidate measurement
reports separately whether it distinguishes the displayed alternative
pair and whether its addition identifies the requested target across all
remaining alternatives. Neither result establishes physical feasibility,
precision, cost benefit or a calibrated decision. RET source is not involved
in this first contract.

For a design matrix `H` and requested quantity `qᵀθ`, the data identify that
quantity precisely when `qᵀδ=0` for every `δ` in `ker H`. If all readings use
one input `x₀`, the direction `δ=(1,−x₀)` is invisible to those readings. A
prediction at `x*≠x₀` changes by `x*−x₀` along that direction. A second distinct
reference input separates the alternatives. A proper prior can give finite
posterior uncertainty even when the data alone do not identify the answer.

A bounded consumer should report data identification versus prior dependence,
uncertainty, explicit indistinguishable alternatives and a feasible separating
measurement, or refusal when noise/cost/stability prevents useful separation.
This uses ordinary linear identifiability mathematics and the QR discipline of
declaring questions, legal tests and refusal. Its value needs a measured
decision/cost comparison; it is not a claim of new mathematics or quantum
advantage.

The [synthetic public-API comparator fixture](COMPARATOR_DEMO.md) is also
accepted. Its independently authored 34 tests verify the exact Gaussian
oracle, actual observed-row bindings, candidate versus observed information,
held-out non-assimilation and source-byte replay. Root replay passed all 236
focused application/registry cases, including these 34. Seven deterministic
synthetic capture byte strings are retained in memory across the two branches;
their raw JSON semantics are checked separately from hash identity. Running
the fixture writes no result files and changes no RET source.

With the declared proper prior and noise variance 1/4, another reading at the
same reference reduces the same-level mean variance from 2/9 to 2/17 while
structural rank remains one. A second distinct reference gives rank two;
gain and offset still have positive posterior variance 1/9. This is conditional
Gaussian arithmetic, not sampled calibration or evidence that either policy
works better in an instrument. Four held-out records leave inference unchanged.
There is no Objective, ranking, closure decision or measured-benefit claim.

Next steps: establish the measured target/data and operational tolerance;
then freeze a compatible objective, baseline comparison and evaluation protocol.
The coordinator has asked whether the user has a specific instrument or dataset
in mind; that choice remains open. Coordinate SDK file ownership with RET before
any implementation there. The scientific foundations and premise-consolidation
lanes can continue independently of missing pilot data.

**Current SDK feasibility boundaries from source review**

The existing [apparatus adapter](../../det8/ret/adapters/apparatus.py) observes
two response axes at `x` and `x+0.25` per action. With both axes observed,
one action already provides a rank-two gain/offset design. The proposed
single-channel comparator instead declares one response, feature row `(x,1)`
in the explicit `(gain, offset)` parameter order, and a 1-by-1 observation
covariance. Its same-level ambiguity is not a defect of the existing adapter.

A future sidecar must assemble H from actually assimilated, observed training
axes for a declared model. Missing axes and held-out validation records cannot
enter it. Retain the exact declared design ledger, model/parameter order,
target and record-to-row bindings. A multi-axis action adds its whole observed
block, not just one chosen row. Repeated rows can improve noisy precision
while leaving structural rank unchanged; this certificate is not an action
utility or cost ranking.

[Prediction](../../det8/ret/inference.py) returns future-observation covariance,
including observation noise. It cannot silently be relabeled as uncertainty
in the mean quantity `qᵀθ`. The current [workflow](../../det8/ret/workflow.py)
uses a named question and model-family/nuisance/cost objective; `question_id`
does not make its action ranking optimize arbitrary target precision. A
structural certificate may annotate that workflow. Any stronger target-based
planning claim needs a compatible objective or separately reviewed extension.

Current multi-record held-out closure requires distinct raw-source hashes and
assumes block-diagonal observation noise across records, while retaining
shared parameter uncertainty. Four slices of the same raw-bank hash cannot
be relabeled as independent held-out sources. Use genuinely separate captures
under the justified noise model, or one explicit joint vector record with
the required covariance. Source identity alone does not establish statistical
independence; shared reference error must still be modeled.

The accepted isolated fixture implements the public-API inference, exact ledger,
prospective candidate status, observed-axis/source accounting and verified
replay portions of this integration step. It deliberately leaves workflow
objectives and closure for a separate evaluation contract: a four-record
held-out arithmetic example is not a completed application acceptance test.
Target-optimal action choice, policy superiority, measured calibration and
G2 completion remain unestablished. Coordinate ownership before SDK changes.
