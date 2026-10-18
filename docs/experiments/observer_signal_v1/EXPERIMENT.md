# RI-26 — local observers and signals in a supplied geometry

14 September 2026 UTC. **Supplied-geometry kinematic model and synthetic records;
not an actualization-to-geometry derivation or physical measurement.** This is
the separately authorized secondary exploration after the published
[RI-25 qubit experiment](../qubit_record_v1/EXPERIMENT.md). It imports or changes
none of that accepted bundle. Review/publication status belongs to the
[QR handoff](../../coordination/QR_HANDOFF.md).

## 1. Frozen scope, units and observer premises

Supply the radial kinematic slice of spatially flat FLRW on a noncompact line:

\[
ds^2=-c^2dt^2+a(t)^2d\chi^2,\qquad
a(t)=a_*e^{H(t-t_*)},\quad c>0,\ a_*>0.
\]

The general API can use seconds for t, metres for χ, dimensionless a, inverse
seconds for H, and the corresponding metres/second value of c. Frequencies
are cycles/second. The worked fixtures instead choose **one light-second as
the length unit**, retaining seconds as the time unit; c=1 length-unit/second
and a*=1 are then unambiguous. Both signs of H and H=0 are included. There
is no supplied matter model, Einstein equation, perturbation, backreaction,
spatial curvature, finite topology, moving observer or detector-selection law.
Ordinary null propagation and geometric-optics frequency transport are adopted.
Standard FLRW kinematics and its separation from field equations are described
in [Carroll's GR notes §8](https://preposterousuniverse.com/wp-content/uploads/grnotes-eight.pdf),
especially (8.1), (8.66–67) and (8.71–72). The integration and record contract
below are explicit calculations for this stipulated exponential fixture.

Two ideal comoving observers have distinct nominal identities, fixed χi and
unit-rate proper clocks τi=t+bi. Offsets bi are supplied to the **producer**,
not known by a receiver. Equal coordinate locations are allowed while keeping
the two identities distinct. Local durations cancel a constant offset; a
transmitted timestamp alone does not synchronize clocks. Unit rates, common
units, ideal frequency calibration, truthful reference payloads and complete
modeled detection before cutoff are premises. There is no empirical claim
that a real clock or receiver satisfies them.

The present model predicts observer consequences of **given** geometry. It
does not determine a(t) from records, supply native F/L, couple RI-25 qubits to
curvature or derive quantum physics, physical mass or gravity. The existing
primitive-input test therefore cannot be passed by this fixture: its metric
and coordinates are inputs. The model/audit may know them; an observer record
does not acquire them merely because the producer uses them.

## 2. Exact arrival, uniqueness and finite cutoff

For an actual directed emission at te, the other observer is at absolute
comoving separation ℓ=|χr−χe|. A future radial null ray must satisfy

\[
\ell=\int_{t_e}^{t_r}\frac{c}{a(t)}dt.
\]

The integrand is positive at every finite time. The integral is continuous,
zero at te and strictly increasing for tr>te. Any finite solution is unique.
For ℓ=0 the unique nonnegative delay is zero; emission and reception are still
distinct identified records. It is a degenerate colocated transfer, not a
positive-length null trajectory. Signal direction is the sign of χr−χe;
spatial homogeneity makes the arrival calculation depend only on ℓ.

For H≠0 define q(t)=exp[−H(t−t*)]>0. The exact interface uses rational q and
rational H,a*,c,ℓ; time is the audit expression t=t*−ln(q)/H. Integration gives

\[
\ell=\frac{c}{H a_*}(q_e-q_r),\qquad
q_r=q_e-\frac{H a_*\ell}{c}.
\]

Only qr>0 is a finite reception. Write ae=a*/qe and u=H aeℓ/c. Then

\[
\Delta t=-\frac{\ln(1-u)}{H},\qquad
\frac{\nu_r}{\nu_e}=\frac{q_r}{q_e}=1-u,\qquad
z=\frac{\nu_e}{\nu_r}-1=\frac1{1-u}-1.
\]

The frequency formula is the adopted geometric-optics law νr/νe=ae/ar,
with the displayed rational simplification. It gives arνr=aeνe; it does not
assert constant locally measured photon energy or establish a new global
energy-conservation law.

For H>0, qr=0 is an asymptote at future infinity and qr<0 lies beyond the
future reach of this forever-exponential model. Neither has a finite receipt,
received frequency, redshift or timestamp in the executable result. These
fields are null, not zero frequency or a fabricated infinity event. The
available future integral is c qe/(H a*), corresponding to physical separation
aeℓ=c/H at emission. This is a result about this specific exponential model,
not a general identification of Hubble radius with a cosmological horizon;
see [Davis and Lineweaver](https://arxiv.org/abs/astro-ph/0310808) for those distinctions.

For H<0, qr=qe+|H|a*ℓ/c>0 for every finite ℓ. Positive separation gives a
blueshift; a→0 only as t→+∞, not at a finite collapse time. In the static H=0
case q≡1 cannot encode time, so the interface uses a separate rational time:
tr=te+a*ℓ/c, νr/νe=1, z=0.

### Inclusive finite observation window

The producer accepts one finite cutoff not earlier than **any actual
emission**. An input schedule containing an emission after the cutoff is
refused, not silently dropped or promoted to an actual event. Actual emissions
remain recorded even when their signals will not be received. The cutoff
restricts reception visibility as follows:

| Geometry | Valid future cutoff | Receipt by cutoff, including equality |
|---|---|---|
| H>0 | 0<qc≤qe | finite qr≥qc |
| H<0 | qc≥qe>0 | finite qr≤qc |
| H=0 | tc≥te | tr≤tc |

All signs, comparisons and ties are rational. No logarithm display decides
arrival, chronology or cutoff validity. Events at equal exact time are ordered
for export with emission before its reception and window closure last;
tie-breaking among unrelated simultaneous events is bookkeeping, not a new
physical causal relation. Rounded clock ties preserve all actual records.

The observer can report **not received by cutoff** for a preannounced signal
ID absent from its local history. That is not an observed horizon or a claim
of eternal nonarrival. A preannounced ID does not itself prove an emission
occurred. A finite modeled receipt after cutoff, an asymptotic-only forecast
and a beyond-horizon forecast all produce the same kind of finite absence
report. Their distinct forecasts stay in the separate audit. There is no
infinite cutoff or hypothetical receipt stored as an observed event.

## 3. Invariants, static limit and a rejected redshift summary

**Order.** For fixed separation, differentiating the null integral yields
F′(te)=a(F(te))/a(te)>0, where F is the finite-arrival map. Thus later emissions
arrive later when both are finite; the integral's positivity gives tr≥te.
Exact coordinate order becomes order along each unit-rate local clock. Across
different clocks,

\[
\tau_r-\tau_e=\Delta t+b_r-b_e.
\]

This cross-clock difference can be negative without acausality. The receiver
does not report it as flight time. Its frequency ratio is independent of both
offsets, while same-clock ideal durations are exactly offset-invariant.

**Coordinate rescaling.** For λ>0, changing a*→λa* and χi→χi/λ preserves a*ℓ,
aeℓ, the null-arrival map, ratios, symbolic times and local-clock outputs at
the same offsets. a* or ℓ alone is not a coordinate-invariant observable.

**Static limit.** Put θH=aeℓ/c, R=1−HθH>0. The exact delay can be written
Δ=∫(0→θH)dx/(1−Hx). Consequently

\[
\min(\theta_H,\theta_H/R)\le\Delta\le
\max(\theta_H,\theta_H/R).
\]

At fixed te,t*,a*,c,ℓ, H→0 implies qe→1, θH→a*ℓ/c and R→1; these bounds
prove Δ→a*ℓ/c, with frequency ratio→1 and z→0. Holding an arbitrary qe≠1
fixed while changing H is **not** the fixed-emission-time limit. Executable
finite rational families at te=t* corroborate these analytic bounds; numerical
samples do not replace the limit proof.

**One redshift is not a geometry.** At te=t*=0, c=a*=1, the pairs
(H,de/c)=(1,1/2) and (2,1/4) both give νr/νe=1/2 and z=1. Their delays are
ln2 and (ln2)/2, respectively. Thus a summary containing one redshift alone
cannot determine H and physical emission separation. We do not claim their
full records or calibrated timing experiments are indistinguishable. Extra
timing/multiple-pulse data can distinguish possibilities left by that summary.

## 4. Instantaneous frequency versus finite pulse spacing

The instantaneous stretch is

\[
F'(t_e)=\frac{a(F(t_e))}{a(t_e)}=\frac{q_e}{q_r}=1+z.
\]

Two separated crest/packet emissions instead have spacing ratio
[F(t2)−F(t1)]/(t2−t1), a secant of F. A crest label is an identified packet
marker, not an assumption that these finitely separated packets are adjacent
cycles of the carrier whose local frequency is measured. With H≠0, ℓ>0,

\[
F''(t_e)=\frac{H^2(a_*\ell/c)q_e}{q_r^2}>0.
\]

Hence any positive finite secant between finite arrivals is strictly between
its endpoint instantaneous stretches. This holds for contraction as well as
expansion; static/coincident limits have constant stretch. Coincident emission
times give no defined spacing ratio and are not repaired into a positive gap.

For H=a*=c=1, ℓ=1/2, emit at qe1=1 and qe2=3/4. Receipts are qr1=1/2 and
qr2=1/4. The ideal local gaps are ln(4/3) at the emitter and ln2 at the
receiver. Their ratio is ln2/ln(4/3), strictly between 2 and 3 because
(4/3)²=16/9<2<(4/3)³=64/27. Endpoint frequency ratios are 1/2 and 1/3;
endpoint stretches are 2 and 3. The finite spacing is not either endpoint.

## 5. Observable clock displays with proved numerical error

Global model times remain exact logarithmic expressions in audit data. Local
records contain only a displayed rational number d of seconds and an error
ε≥0 with |d−τ|≤ε. Neither H,q,χ,offset, symbolic generator expression nor a
forecast is a clock-reading field. A transmitted emitter reading is a payload,
not the receiver's own time or a synchronization certificate.

The producer proves its numerical enclosure in rational arithmetic. For x>0
set y=(x−1)/(x+1), so |y|<1. With M≥1,

\[
\ln x=2\sum_{j=0}^{M-1}\frac{y^{2j+1}}{2j+1}+\mathcal R_M,
\quad |\mathcal R_M|\le
\frac{2|y|^{2M+1}}{(2M+1)(1-y^2)}.
\]

The bound follows by taking absolute values in the remaining series and
replacing all its denominators by the first. For c0+k ln x, multiply the
radius by |k| and add c0 to the center. The implementation uses M=48, rounds
the center exactly to a 10⁻p grid (default p=9, ties to even), and adds the
exact rounding displacement to the radius. It then rounds that error **up**
to a 10⁻(p+3) grid. No floating logarithm or unstated precision guarantee is
used. Large error remains large; finite precision is not silently promoted to
exact timing. This numerical theorem is distinct from the adopted physical
premise τi=t+bi and ideal frequency/clock calibration.

For two readings from one clock, the ideal duration is enclosed by
[d2−d1−(ε1+ε2),d2−d1+(ε1+ε2)]. For positive emission/reception duration
intervals E=[E−,E+] and R=[R−,R+], the finite spacing ratio is enclosed by
[R−/E+,R+/E−]. If either lower duration bound is not strictly positive, the
observer reports `unresolved_display_precision_or_order`, with no ratio.
Clock displays never decide whether the events exist.

Exact offset cancellation does not imply invariant **rounded** differences:
at 0.1-second precision, times 0.04 and 0.06 display 0.0 and 0.1. Add offset
0.05 and their displayed values are both 0.1. The ideal gap is still 0.02;
the displayed gap becomes unresolved. Tests keep both events and refuse an
unsupported ratio. Frequencies are unchanged by this display issue.

## 6. Record format and receiver access contract

[local_records.py](local_records.py) defines strict JSON round trips with
duplicate/unknown fields and nonfinite JSON refused. Rational values are
canonical strings such as `"1/2"`, not float tokens. A `ClockReading` contains
`kind=bounded_local_clock_display`, `value_seconds`, and `error_seconds`.
The reading constructor accepts any canonical rational value, such as 1/3,
with a declared bound; only `display_log` guarantees decimal-grid production
and the numerical enclosure just proved. An externally supplied reading's
error bound is a premise, not certified merely by schema validation.

Every `LocalRecord` has exactly schema_version=1, event_id, observer_id, kind,
timestamp, precursor_id, payload, measured_frequency, calibration_id and
provenance. The local precursor starts at `start:<observer_id>` and thereafter
names the preceding actual local event; event IDs cannot self-link or reuse
that anchor. The three kinds are:

| Kind | Required contents | What it does not mean |
|---|---|---|
| emission | Actual emitter-local timestamp and complete transmitted payload; no receiver measurement | A scheduled-but-unexecuted future emission |
| reception | Receiver-local timestamp, unchanged received payload and positive locally measured frequency | An expected or infinitely late event |
| window_closed | Actual local cutoff reading; no signal payload or frequency | A receipt, horizon observation or proof that an unreceived signal was emitted |

The payload has exactly emission_id, signal_id, emitter_id, target_id,
crest_id, reference_frequency, emitter_timestamp and bounded message text.
Emission and reception have distinct event IDs, and signal IDs match across
the actual transmission. Emission timestamp/identity must agree with its
payload. The producer checks complete reception payloads against retained
emissions. The receiver validates only what is locally available; it does
not consult the remote emission history or authenticate payload truth.

Local history is an immutable tuple; reversed/duplicate precursors, foreign
observers and calibration/provenance changes are refused. Window closure is
last. For clock intervals [li,ui], maintain Li=max(j≤i)lj and require Li≤ui.
This is necessary and sufficient for some nondecreasing actual times to fit
the intervals: choose time Li. Pairwise checks alone would wrongly admit
[2,2]→[0,3]→[1,1]. Feasibility does not prove actual acquisition order or
completeness; producer exact chronology and retained causal IDs provide the
fixture's declared history. Overlapping intervals and displayed ties remain.

[observer.py](observer.py) imports neither [kinematics.py](kinematics.py) nor
[sim.py](sim.py). `infer(observer_id,local_records,expected_signals,calibration_id)`
uses a preannounced nominal-ID catalogue, the complete supplied local history,
and the explicit calibration premise. It computes frequency ratio and z only
from actual received reference payloads/local frequency measurements. Its
flight-time field is null because cross-observer offsets are unknown. Missing
catalogue IDs receive only a cutoff absence status. Empty/unfinished windows
cannot support that report. Extra actual receipts are retained and reported,
not silently removed for failing to appear in the expected catalogue.

`pulse_spacing(first,second)` uses two actual receipts from the same emitter,
receiver, declared pulse train and calibration/provenance, with distinct
event/emission/signal/crest identities. Full validated-history membership and
ordering remain a caller obligation; a two-row helper cannot prove an omitted
prefix complete. A common emitter clock/epoch and pulse train are explicitly
supplied premises; matching payload message strings alone do not establish
them. It computes finite-duration bounds, never an instantaneous
redshift or inferred flight time. Nominal IDs, calibration labels and frozen
objects are trusted workflow/audit data, not authenticated provenance or a
security boundary. Existing records are not changed by reinterpretation.

## 7. Worked fixtures, execution and outputs

The independent [kinematic tests](test_kinematics.py),
[clock/record tests](test_records.py) and [worked tests](test_worked.py) cover
the specified cases and refusal boundaries. The ten worked fixtures include:

| Fixture | Exact supplied outcome | Observed receipt policy |
|---|---|---|
| Static, H=0, ℓ=1/2 | Δ=1/2, νr/νe=1, z=0 | Finite receipt |
| Expanding, H=1, ℓ=1/2 | Δ=ln2, ratio=1/2, z=1 | Finite receipt |
| Contracting, H=−1, ℓ=1/2 | Δ=ln(3/2), ratio=3/2, z=−1/3 | Finite receipt |
| Expansion horizon, ℓ=1 | Asymptotic future only | Emission retained; no receipt |
| Beyond horizon, ℓ=3/2 | No finite arrival in this model | Emission retained; no receipt |
| Early cutoff, ℓ=1/2, qc=3/4 | Finite arrival qr=1/2, after cutoff | Emission retained; no receipt yet |
| Colocated, ℓ=0 | Zero delay, ratio=1 | Distinct emission/receipt at the same exact time |
| Reverse direction | Same arrival/ratio for equal ℓ | Correct observer/target histories |
| H=2, ℓ=1/4 | Same z=1, different delay (ln2)/2 | One-redshift nonidentifiability only |
| Two finite pulses | Secant ln2/ln(4/3), endpoint stretches 2 and 3 | Two receipts, second exactly at cutoff |

Here c=a*=1, te=t*=0 except the second pulse. The default clock offsets are
bA=7 seconds and bB=−3 seconds; they deliberately prevent interpreting a
cross-clock subtraction as a positive flight time. Both observers' local
closure records are stored. The producer contains no RNG or real dataset.

All files use only the Python standard library and the isolated bundle. No
accepted bundle, core/RET source, research registry or predecessor executor is
imported. With an existing Python 3.11+ interpreter (compatible `python3` may
replace `.venv/bin/python`), run from the repository root:

```sh
.venv/bin/python -I -S -B docs/experiments/observer_signal_v1/run_checks.py
.venv/bin/python -I -S -B -O docs/experiments/observer_signal_v1/run_checks.py
.venv/bin/python -I -S -B docs/experiments/observer_signal_v1/worked_example.py
.venv/bin/python -I -S -B -O docs/experiments/observer_signal_v1/worked_example.py
```

Each worked command prints its new external temporary output directory.
Optional `--output /absolute/new-or-empty-directory` is refused inside the
checkout or if it would overwrite existing data. Generated traces stay outside
the repository. Each fixture has two observer JSONL histories, an observer
plan, receiver reports and a separate model audit. The pulse fixture also has
a finite-spacing report; a top-level summary labels observer results and
producer forecasts separately. None of the model audit is passed to inference.
The summary is an analyst report containing both layers, not an observer feed.

Main executed all **51 focused tests** on Python **3.11.6**, passing normally
in 0.046 s and with optimization in 0.045 s. These comprise 25 exact kinematics,
14 clock/record and 12 simulator/worked tests. Separate direct normal/optimized
worked runs retained 11 emissions, eight receptions and 20 local closures,
and all **52 exported files were byte-identical**. The exported summary SHA256
is `80a646f5dd007ba6a9d64f9ffd6dec7c3c4bb5a1a8d4974fa31c335545ac28a8`.
Full mathematical/specification and source/dataflow reviews passed after the
whole-prefix chronology and direct pulse-helper guards were corrected.
Final source identities accompany the source-quiet handoff. These are focused
implementation tests, not newly registered mathematical witness totals or
physical measurements. No runtime installation, UI, provider contact, data
download, hardware/cloud job or git operation is part of this bundle.

## 8. Completed result and the missing additional rule

The yield is an explicit conditional definition, its arrival/invariance/error
theorems, a counterexample to redshift-only geometry identification, and a
record-producing simulator that preserves finite observer limitations. The
usual kinematics is not novel. Agreement of this deterministic program with
its supplied generator is verification of the fixture, not empirical
correspondence or emergence.

**No actualization→geometry equation has been supplied.** A future additional
rule must name its variables, equations, parameters and an observer-accessible
difference from this baseline before there is another consequence to calculate.
This sitting invents none. It does not promote metric-as-record from Status M,
change Option B, reopen retired kappa-gravity or old clock work, or launch a
QR-05 lettered/coverage/noncollapse gate. Measured-W acquisition and the RET
voltage comparator remain separate prerequisites in the coordinator's
[data/follow-up note](../../coordination/QUBIT_DATA_AND_FOLLOWUP.md).
Stop after independent reviewed handoff; no automatic successor is assigned.
