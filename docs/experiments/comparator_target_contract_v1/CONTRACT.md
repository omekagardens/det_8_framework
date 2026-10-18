# RI-30 — comparator target precision when the model changes

23 September 2026. **Bounded synthetic inference contract; independently
accepted by the coordinator.** Four-file, standard-library-only bundle. No RET, core or accepted
experiment source is imported or changed. This is conventional exact interval
inference applied to one declared calibration question, not new physics,
measured calibration, policy superiority or an operational deployment.

## 1. Question and supplied premises

Can the mean response at zero normalized reference input be estimated to
absolute error at most a declared tolerance `T` from the selected training
records, under the declared model and error bounds?

Fix

\[
 f(x)=gx+b+cx^2,\qquad x\in\{-1,0,1\},\qquad g,b\in\mathbb R.
\]

The question is `b = f(0)`, not a future individual noisy reading, gain,
curvature, an intervention or a causal mechanism. The input coordinate is
dimensionless and exactly normalized; the responses, `g`, `b`, `c`, observation
errors, curvature bound and tolerance all use the declared response unit.
No conversion from uncertain physical reference voltages is supplied.

Three declared families share this target:

| Family | Domain of `c` |
|---|---|
| `affine` | `c = 0`; no curvature-bound argument |
| `bounded_curvature` | `-K <= c <= K`, supplied exact finite `K >= 0` |
| `unbounded_curvature` | all real `c`; no curvature-bound argument |

`bounded_curvature` with `K=0` has the affine mathematical domain, but remains
a separately named input declaration. No data-driven model-family selection
is performed. Enlarging the family does not inherit a certificate proved
only for the smaller family.

For each selected training reading `i`, supply exact normalized location `x_i`,
response `y_i` and simultaneous deterministic absolute bound `epsilon_i >= 0`:

\[
 y_i=f(x_i)+e_i,\qquad |e_i|\le\epsilon_i.
\tag{1}
\]

All selected readings are assumed to concern the same stable response law,
normalization, units and calibration context. These are premises. Labels do
not establish actual apparatus stability, physical acquisition, reference
accuracy or calibration. Error bounds may include justified measurement,
calibration and other contributions, but this contract does not derive them.

The allowed error set is the Cartesian box in (1). This is **not statistical
independence**. Arbitrarily correlated actual errors satisfying all the bounds
are covered. If extra joint constraints are known, the box can be conservative;
sharpness below is for this expressly declared box, not every narrower physical
error model. There is no probability, confidence allocation, prior, sampling
law, repeated-look guarantee or automatic `1/sqrt(N)` improvement.

## 2. Records, selection and compatibility

Every supplied record has a unique nominal `record_id`, one normalized
reference location and an explicit role:

| Role | Allowed content and inference use |
|---|---|
| `actual` | An observed value and nonnegative error bound. Eligible for training only if its ID is explicitly selected. |
| `held_out` | An observed value and nonnegative error bound, never selected for training. |
| `prospective` | No observed value. May carry a planned error bound; neither the action nor that bound is an observation. |
| `missing` | No value or error interval; a nonblank reason is required. |

An observed numeric zero is a response, not missingness. A missing declaration
does not distinguish failed formation from inaccessible data without additional
evidence. A proposed reference does not become an executed measurement.
All records, including unselected actual readings and held-out values, remain
in the input identity. They do not all become evidence for this training fit.

Let `S` be the explicitly selected IDs; only `actual` records may belong to
`S`. Choosing a held-out, missing or prospective ID is an input error, not
silent filtering. Define the full mathematical compatibility set

\[
\mathcal C=\{(g,b,c):\ c\text{ is in the declared family},\quad
 |gx_i+b+cx_i^2-y_i|\le\epsilon_i\ (i\in S)\}.
\tag{2}
\]

Selection is a supplied declaration, not a policy learned here or a proof that
exclusions were justified. No held-out discrepancy or model-selection score
is computed. To use a formerly held-out reading as training would require an
explicit role/selection change and a new input identity; the result cannot
still be described as evaluated against that same untouched holdout.

For each observed selected location `x`, intersect **all** its intervals:

\[
 I_x=[l_x,u_x]=\bigcap_{i\in S:\,x_i=x}
 [y_i-\epsilon_i,y_i+\epsilon_i].
\tag{3}
\]

An absent location has no constraint, not the interval `[0,0]`. If any retained
location has `l_x > u_x`, (2) is empty immediately. This check precedes all
other rules, including unbounded curvature or a zero-input reading. Equal
repeated intervals do not narrow (3). Distinct justified intervals can narrow
it by intersection; they can also contradict it. There is no averaging-based
precision gain from counting records.

## 3. Exact target interval and continuous-domain proof

Assume first that every selected-location intersection is nonempty.
If **both** endpoint locations are selected, write

\[
 M=\tfrac12(I_{-1}+I_{+1})
  =[(l_{-1}+l_{+1})/2,(u_{-1}+u_{+1})/2].
\tag{4}
\]

Here `M` contains exactly the possible values of `b+c`. The complete projected
target set `B = {b : (g,b,c) in C}` is:

- With both endpoints and finite effective bound `K` (affine means `K=0`),
  start with `B = M + [-K,K]`.
- With unbounded curvature, or fewer than both endpoints, start with
  `B = R`. In the missing-endpoint case unrestricted gain absorbs the
  nonzero-location constraint even when `c=0`.
- If an actual selected zero-reference interval `I_0` exists, intersect the
  starting set with `I_0`. No other role contributes this interval.

An empty final intersection means `C` is empty, not that every target claim
is vacuously certified. Otherwise the answer is either a finite nonempty
closed interval or all of `R`; no half-infinite case occurs for this model.

**Attainability for every real target, not a finite grid.** For both endpoints,
let `b` be any member of the stated projected set. Let `s` be `b` clamped to
the interval `M`, and choose

\[
\begin{split}
 c&=s-b,\\
 \mu_-&=\max(l_{-1},\,2s-u_{+1}),\\
 \mu_+&=2s-\mu_-,\\
 g&=(\mu_+-\mu_-)/2.
\end{split}
\tag{5}
\]

Since `2s` lies between the sums of the lower and upper endpoint bounds,
`mu_-` belongs to `I_-1` and `mu_+` belongs to `I_+1`. More explicitly,
`mu_- <= u_-1` follows from both terms in the maximum being at most `u_-1`;
`mu_- <= 2s-l_+1` follows in the same way from the lower sum inequality.
The latter gives `mu_+ >= l_+1`, while the definition gives
`mu_+ <= u_+1`. The resulting endpoint responses are exactly `mu_-` and
`mu_+`. For finite `K`, distance from `b` to `M` is at most `K`, so
`|c| <= K`; for affine, `b` is in `M` and `c=0`. A selected zero interval
is satisfied because `b` was required to belong to it.

With only one endpoint `x=+1` or `-1`, choose any `mu` in its nonempty
intersection, set `c=0`, and set `g=(mu-b)/x`. With neither endpoint choose
`g=c=0`. Any required zero interval still constrains `b`. These constructions
also work in every bounded-curvature family. They prove there are no hidden
gain constraints and that the missing-endpoint rule is exact.

Conversely, every compatible parameter triple obeys the interval rules by
adding its endpoint responses and using its zero response. Together these
arguments prove equality, nonemptiness when reported, and continuous real-
domain attainability. Rational inputs and a rational target give a rational
witness through (5); the proof does not restrict physical parameters to
rational values.

With just one record at each endpoint, finite `K` gives the simpler formula

\[
 B=[s-h-K,s+h+K],\qquad
 s=(y_-+y_+)/2,\quad h=(\epsilon_-+\epsilon_+)/2,
\tag{6}
\]

before any selected zero reading. Repetition uses (3), not the average of
all raw readings or a sample-size correction to (6).

## 4. Precision and structural identification are different

For a compatible bounded target interval `[L,U]`, return

\[
 \widehat b=(L+U)/2,\qquad r=(U-L)/2.
\tag{7}
\]

Every compatible target is within `r` of this estimate. For any competing
point estimate `a`, the two attainable endpoints imply
`max(|a-L|,|a-U|) >= (U-L)/2` by the triangle inequality. Thus (7) gives
the exact deterministic minimax absolute error for the supplied observations
and allowed uncertainty set. It is not a worst-case sampling-risk theorem.
The estimate meets the requested precision **iff `r <= T`**, inclusively.
At `r=T=0` a compatible singleton meets precision.

Meeting this precision does **not** mean `|b| <= T`, that the device meets a
zero-offset acceptance specification, or that applying a correction is safe.
For example, `[9/100,11/100]` has radius `1/100` but is not near zero to
tolerance `1/20`. No actuation decision is returned.

When `B=R`, every finite estimate has unbounded worst-case absolute error;
`precision_met=False`, with no invented infinite timestamp, numeric infinity
or finite radius. Empty compatibility gives no estimate or precision verdict.

The separate `structurally_identified` flag asks about the **noiseless selected
design and declared parameter family**, not the realized intervals:

- A selected actual zero location identifies `b` in every family.
- Both endpoints identify `b` in the affine or effective `K=0` family.
- Otherwise `b` is not structurally identified. With `K>0`, the endpoints
  admit changes `(delta_g,delta_b,delta_c)=(0,d,-d)` for suitable nonzero
  `d` inside the domain. With a missing endpoint, free gain gives the
  alternative directly. Positive `K` is not an extra exact observation.

This flag remains defined for an incompatible dataset as a property of its
design; it does not assert that any parameters fit that dataset. Structural
nonidentification may coexist with a sufficiently narrow partial interval;
structural identification may coexist with an unacceptably wide noisy interval.

## 5. Small implementation and declared-content identity

[contract.py](contract.py) supplies frozen `Model`, `Record`, `Request` and
`Report` dataclasses plus four functions:

- `assess(request)` computes (3)–(7), status and structural flag.
- `canonical_payload(request)` returns detached identity content.
- `verify_report(request, report)` recomputes the digest and every conclusion,
  checking exact field types as well as values.
- `compatible_parameters(request, target_value)` constructs one compatible
  rational `(g,b,c)` or refuses an outside/empty target. This is a mathematical
  witness, not measured ground truth or an estimate of the full parameter vector.

`Request` includes the model, tuple of all records, tuple of selected IDs,
tolerance, response unit, session and calibration IDs, model/error premise
descriptions, fixed target `mean_at_zero` and fixed reference unit `normalized`.
The named global context is asserted for these records; there is no per-record
acquisition verification or cross-session transport operation. The caller must
not silently combine incomparable physical records under one session label.

Numeric inputs are exactly built-in `int` or `fractions.Fraction`; booleans,
floats, strings and subclasses are refused. Reduced numerator/denominator bit
length is at most 256 each. Derived results are exact and are not rounded or
truncated to that input limit. The optional witness target obeys the same input
limit; this implementation limit does not weaken the real-domain proof.
There may be zero through 64 supplied records and selected IDs, in tuples.
IDs are unique and selections must refer to present eligible records. Unsupported
references, negative bounds, contradictory role payloads and malformed selections
are input errors. Valid but mutually inconsistent selected intervals are instead
reported as incompatibility.

All text is nonblank built-in `str` without edge whitespace or ASCII control
characters. Record IDs have at most 96 characters, nominal context/unit/role/
target strings at most 128, and premise descriptions/missing reasons at most
512. These limits bound the fixed calculation; no performance claim is made.

The SHA-256 input identity covers the contract-version tag, all model/K
declarations, parameter order, reference catalogue/units, response unit, target,
tolerance, session/calibration labels, model/error basis, **every supplied record
and role/value/error/reason**, retained tuple order, and selected-ID tuple order.
Rationals are reduced strings; the detached payload is encoded using UTF-8 JSON
with sorted keys, compact separators and ASCII escaping. Equivalent rational
inputs have the same encoding. Reordering records can change identity without
changing the mathematical answer.

A changed model, bound, unit, target, tolerance, reading, role or selection
invalidates the old report through `verify_report`, subject to the usual
SHA-256 collision-resistance assumption rather than an injectivity theorem.
Unsupported targets are
refused, not silently mapped to `b`. The identity binds declarations, not
authenticity, physical calibration, a code signature or an immutable acquisition.
The frozen Python objects are not a hostile-code security boundary; arbitrary
runtime monkey-patching or bypassing constructors is outside the API contract.
Source hashes and runtime identity belong to the separate review handoff.

## 6. Fixed worked cases and acceptance obligations

Use normalized endpoint readings `y_-=-1`, `y_+=1`, each with error `1/100`,
and estimate-error tolerance `T=1/20`. All cases are deterministic synthetic
fixtures, not acquired data.

| Declared inputs | Required target result |
|---|---|
| Affine | `[-1/100,1/100]`; precision met. |
| Same readings, bounded curvature `K=1/5` | `[-21/100,21/100]`; precision not met. The affine report does not transfer. |
| Same readings, unbounded curvature | All real targets; no finite precision. |
| Bounded curvature plus selected actual zero `y_0=1/10`, error `1/100` | `[9/100,11/100]`; precision met. With affine instead, compatibility is empty. |
| That zero reading is held out or unselected, or the zero action is prospective/missing | Endpoint-only training result unchanged. |
| Bounded curvature plus selected actual zero `y_0=3/10`, error `1/100` | Empty compatibility; no estimate or precision verdict. |
| Only one selected endpoint and no selected zero, even affine | All real targets; free gain prevents a finite bound. |
| Selected actual zero and fewer than both endpoints | Exactly the zero interval, provided no selected-location contradiction exists. |
| Empty repeated intersection at any selected location | Incompatible in every family, even with an otherwise precise zero reading. |

[test_contract.py](test_contract.py) is independently authored. Required
checks include exact radius/tolerance equality, singleton and zero-error cases,
continuous-domain witness identities at selected rational points, minimax
endpoint separation, nonidentification alternatives, missing endpoints,
repeated intersection and contradiction, structural versus precision status,
role/selection refusal, observed zero versus missing, changed-content identity,
detached canonical payloads and malformed input rejection. Mathematical proof
is (2)–(7); finitely many test points do not replace that proof.

Run from the repository root using Python 3.11 or later:

```sh
.venv/bin/python -I -S -B docs/experiments/comparator_target_contract_v1/run_checks.py
.venv/bin/python -I -S -B -O docs/experiments/comparator_target_contract_v1/run_checks.py
```

The runner adds only this bundle to the isolated interpreter path, discovers
only `test_contract.py`, refuses zero tests and treats skips/expected failures
as unsuccessful completion. It does not import `det8`, accepted model bundles,
the RET comparator or earlier test suites. There is no data acquisition,
network use or result-file writer. `-B` prevents bytecode caches.

**Source-stable author verification, 23 September 2026.** On Python 3.11.6,
the independent test author passed all 48 tests in both modes. The main
handoff replay also passed all 48 normally (0.023 s) and with optimization
(0.022 s), with zero skipped or expected-failure cases. Scoped Ruff lint and
format checks pass; all six local document targets resolve. Independent
mathematical/specification review found no remaining blocker. These are
checks of this four-file bundle only, not a replay of accepted predecessor
suites or coordinator publication acceptance.

## 7. Relation to accepted work and stop boundary

The [RI-12 contract](../../coordination/IDENTIFIABILITY_CONTRACT.md) establishes
unrestricted exact linear identification; its fixed-affine
[synthetic comparator](../../coordination/COMPARATOR_DEMO.md) adds conditional
Gaussian arithmetic. Neither is extended or imported here. The
[application plan](../../coordination/APPLICATION_WORK_PLAN.md) separately
records RI-18's information loss, RI-19's error lower bounds and the remaining
measured evaluation requirements. [RI-23](../../coordination/SCALAR_VALUE_ERROR_CONTRACT.md)
already distinguishes compatibility, uncertainty and positivity for a different
matrix-valued question. This bundle supplies only the missing concrete
comparator **target-precision decision under explicit model change**.

Incompatibility can mean a wrong family, invalid calibration/error bounds,
unstable response, wrong record context or other premise failure. It proves
none of those explanations individually. Passing synthetic checks cannot
validate the declared law, error budgets, selection practice or model adequacy.
Missing errors cannot be supplied from a simulator's truth access. Held-out
observations cannot be invented from endpoint fits.

This assignment stops after four-file source-stable review handoff. No RET
implementation, approximate quantum adapter, full-QM derivation, geometry law,
new lettered gate, dataset/hardware acquisition or automatic successor follows.
A measured application still needs a chosen instrument/problem, justified
reference and error bounds, operational target, costs, conventional baseline,
and a frozen independent evaluation. This contract does not close that gate.
