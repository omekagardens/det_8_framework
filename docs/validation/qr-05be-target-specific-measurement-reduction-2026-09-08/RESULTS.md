# QR-05BE results

8 September 2026 (Pacific/Honolulu). **The bounded investigative gate is
complete.** A new four-site plan preserves the original repaired target
estimator's complete probability law while using one fewer fresh shot.
It does not preserve full-profile information or reconstruct the omitted
qubit. Reassigning the saved shot to the center improves the old repaired
plan in the stipulated model, but does not uniformly beat the corner plan.

These are exact finite synthetic results on supplied geometry, not a
physical experiment, quantum advantage, ontology test or gravity law.
See the [standalone model and fixed protocol](README.md),
[machine-readable input](protocol.json) and [full evidence](results.json).

## Target sufficiency with a lost profile direction

The recomputed five-site target weights are
(1/12,1/36,1/36,0,1/9) in (00,10,01,11,cc) order. target4 retains
(00,10,01,cc), with weights (1/12,1/36,1/36,1/9). If A is the full
evaluation matrix, D its inverse, S the row-selection map and q the
geometric integral row, the complete exact certificates give

\[
AD=DA=I_5,\qquad \operatorname{rank}(SA)=4,\qquad
d=De_{11}=(0,0,0,1,-4)^\mathsf T,
\]

\[
SAd=0,\qquad qd=0,\qquad v_{\rm retained}SA=q.
\]

The lost coefficient direction changes f by φ₁₁−4b but leaves this
target unchanged. These linear-map identities cover the specified model
family, not only the twelve fixtures. They establish population-level
target identification under the supplied geometry and physical-domain
premises; they do not imply exact finite-shot answers or minimum possible
measurement count.

For each retained outcome y, the calculation keeps both repair5 outcome
branches over the omitted 11 outcome. Each full estimate equals the
target4 estimate before summation, including on zero-probability branches.
The sum of their probabilities equals the direct four-site probability.
For quantum output, the verified relation is

\[
\rho^{(4)}_y
=\operatorname{Tr}_{11}\!\left(\sum_{x_{11}=\pm1}
\rho^{(5)}_{y,x_{11}}\right).
\]

All states here are unnormalized. The 32-dimensional summed state and its
16-dimensional reduction are both retained; they are not called the same
state. Across the twelve main fixtures there are 384 full-branch pathwise
checks and 192 retained-outcome state comparisons. The off-model control
adds 32 and 16, respectively. target4 and repair5 have identical mean,
variance and MSE in every one of these cases.

Tracing cc instead of 11 produces a different retained-state diagonal in
122 of the 192 main rows and all 16 off-model rows. This negative control
uses a different subsystem order; it diagnoses tracing the wrong factor,
not a physical discrepancy between two legitimate descriptions of the
same labeled subsystem.

## What cannot be recovered

The admitted profiles

\[
f_-=-\tfrac12(\phi_{11}-4b),\qquad
f_+=\tfrac12(\phi_{11}-4b)
\]

both have sufficient admission bound 5/8 and target zero. Their four
retained means are zero and their complete target4 branch reports agree.
Nevertheless the omitted site's means are −1/2 and +1/2; its density
diagonals are (1/4,3/4) and (3/4,1/4). Full five-site record laws have
total variation 1/2, while the retained laws have total variation zero.
The two full outcome-averaged state diagonals also differ and remain in
the capture. Thus the useful target reduction genuinely loses information
about the profile and full quantum output. More shots at retained sites
cannot distinguish this pair; their target happens to be the same.

The larger-domain obstruction is separate. The continuous profile
h = b[(u−1/2)²+(v−1/2)²], bounded by 1/32, has the zero profile's complete
record laws and branch states for all three target plans. Its target is
1/1440, however. Each plan's mean is zero and bias is −1/1440.

| Off-model plan | Variance | MSE |
|---|---:|---:|
| repair5 | 1/48 | 43201/2073600 |
| target4 | 1/48 | 43201/2073600 |
| repeatcc5 | 19/1296 | 30401/2073600 |

Replication reduces shot variance here without repairing the missing
spatial information. The obstruction is not presumed noise or an apparatus
artifact. Neither fewer records nor repetition at the same sites recovers
arbitrary continuous profiles.

## Frozen cost comparisons

target4 uses four shots versus repair5's five with the same target-estimate
law: a saving of one of five preparations/readouts in this declared model.
That is not a calibrated hardware time/energy saving, and it only preserves
the specified target question and retained output.

repeatcc5 uses five fresh shots, reallocating the otherwise unused 11 shot
to a second center copy. The two center outcomes are averaged. With center
mean m_cc, direct enumeration and the independent-copy formula agree:

\[
\operatorname{Var}(\widehat T_{\rm target4})
-\operatorname{Var}(\widehat T_{\rm repeatcc5})
=\frac{v_{cc}^2(1-m_{cc}^2)}2
=\frac{1-m_{cc}^2}{162}\ge0.
\]

Both estimators have the same mean, so their MSE difference is the same
quantity. Compared with the old repair5 plan at equal five-shot count,
repeatcc5 improves nine fixtures, ties three and worsens none. The ties
are plus, minus and peak_bubble, whose center outcomes are deterministic.
This conditional identity follows stipulated fresh-copy independence;
it is not an optimal-allocation or quantum-advantage result.

Below, Δ4 = target4 minus corner4 MSE; Δ5 = repeatcc5 minus corner5 MSE;
ΔR = repeatcc5 minus repair5 MSE. Negative is better. The first comparison
uses equal four-shot cost, the latter two equal five-shot cost. All signed
comparisons are retained, not only improvements.

| Profile | target4 MSE | repeatcc5 MSE | Δ4 | Δ5 | ΔR |
|---|---:|---:|---:|---:|---:|
| zero | 1/48 | 19/1296 | 1/648 | 1/648 | −1/162 |
| plus | 0 | 0 | 0 | 0 | 0 |
| minus | 0 | 0 | 0 | 0 | 0 |
| asymmetric | 289/15552 | 581/46656 | 25/5832 | 65/23328 | −143/23328 |
| corner00 | 1/108 | 1/216 | 1/108 | 1/216 | −1/216 |
| corner11 | 1/108 | 1/216 | 1/108 | 1/216 | −1/216 |
| bubble | 431/20736 | 607/41472 | 5/3456 | 61/41472 | −85/13824 |
| peak_bubble | 11/1296 | 11/1296 | −5/216 | −11/648 | 0 |
| asymmetric_bubble | 269/15552 | 551/46656 | 13/5832 | 1/729 | −4/729 |
| negative_boundary | 109/6912 | 77/6912 | −13/5184 | −13/5184 | −1/216 |
| collision_minus | 1/48 | 19/1296 | 1/648 | 1/648 | −1/162 |
| collision_plus | 1/48 | 19/1296 | 1/648 | 1/648 | −1/162 |

Against their respective equal-cost corner baselines, target4 and repeatcc5
each improve two fixtures, tie two and worsen eight. This fixture census
is not a prevalence estimate for applications. All three target plans are
unbiased on the admitted model, while the corner plans retain bias −θ/144.
Unknown response-dependent variances mean that the largest geometric weight
alone does not establish the best site to replicate. The likelihoods here
remain exactly classical Bernoulli-equivalent.

## Verification and source history

The quantum/monomial and independently authored Bernoulli/beta routes agree
on the complete mathematical report. The capture retains all 1,536 main
branches: 1,006 positive-probability and 530 zero-probability rows. The
off-model control adds 80 positive rows. Exact operator banks retain all
16/32 outcomes for four/five copies and compare all 24/120 station orders.
An independent tensor-Boole test oracle verifies its one-dimensional
moments through degree five before checking the geometric integrals; its
synthetic integration nodes are not additional observer measurements.

The public observer computes 1,616 estimates, checks 3,232 forward/reverse
record orders and retains 170 named refusals (34 for each of five plans).
All slots remain mandatory for the selected plan, including repair5's
zero-weight 11 slot. repeatcc5 requires distinct cc#1 and cc#2 records and
averages them; dropping or duplicating a record is not replication. The
observer receives the declared public record/weight context, not private
profile coefficients, target, state or likelihood. Strict native types,
plan identity and record provenance remain part of the contract.

All **44 tests passed** in isolated normal Python 3.14.0 and again with
optimization enabled (20.280 s and 20.300 s respectively). These are test
durations, not performance benchmarks. Full driver replays passed in both
modes, retaining all eleven frozen source identities and byte-identical
input, freeze and capture. Exactly one separate reference-only audit in
Python 3.11.6 matched the entire encoded mathematical subreport: 438,880
canonical bytes, SHA256
`1bff1a62731598222318dd2174f76590d3f4139ea3cad854f72355168c8315e5`.
It made one reference analysis call (0.86928 s); no primary engine, driver,
observer, test suite or historical executor ran in that audit. This is
not a full-suite Python 3.11 compatibility claim.

The selected BD overlap also matches: ten original profiles, three plans,
800 main branches and 32 repair5 off-model branches, with their common
geometry, operators, schedules and complete selected plan reports. Old
numerical engines were not executed. This checks the declared restriction;
it does not rerun or recertify BD's separate covariance and global-admission
controls. BD files and its mandatory-record contract remain unchanged.

Before the first source freeze or fixed evaluation, the adapted test harness
was brought into line with the five plans and the selected BD evidence
structure. Review caught two additional test-only issues: assigning shot ID
2 is a valid no-op on repeatcc5's last cc#2 record, so malformed-record
generation now skips exact-type/equal-value no-ops; and the historical
mutation guard now compares canonical wire values because native Python
equality hides integer 1 → boolean True changes. Positive cc#2 averaging,
duplicate cc#1 refusal and the malformed native-type cases remain tested.
README schema clarifications likewise preceded freezing. These were not
repairs to observed mathematical outcomes. **The first freeze and first
capture succeeded; there was no post-first source, protocol, mathematical
or test correction.**

The driver uses fresh verified source loading, same-byte protocol hashing
and parsing, type-exact comparisons, input nonmutation checks and final
source/freeze/capture byte brackets. JSON size, duplicate keys, floats,
nonfinite values, symlinks and create-only output handling are exercised
under normal and optimized execution. The 4,000,000-byte JSON cap was fixed
before capture. The frozen source ledger has eleven entries: six current
protocol/source files and five predecessor evidence files.

| Artifact | Bytes | SHA256 |
|---|---:|---|
| source-freeze.json | 2,396 | `b1e64907147c4dab23ffb339e666b7be537881c2763130368b2bc0a226e128f8` |
| results.json | 2,241,522 | `a9c83821f194e03b41958cd5c052920325d973a3263d18b829694a1b9bf09874` |

Reproduction from this directory (capture already exists; do not overwrite):

```sh
python3 -I -B test_qr05be.py
python3 -I -O -B test_qr05be.py
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
```

## Next proposed gate: QR-05BF

The next bounded question is **known geometric-placement sensitivity of
the reduced access**. Keep the profile basis, target kernel and corner
positions fixed, but prospectively vary the supplied strictly interior
station position z. Separate three issues:

1. Does the BE decoder still work unchanged? A residual against the target
   integral row diagnoses a stale compiled map, not by itself insufficient
   measurement access.
2. Can a newly compiled four-site decoder recover the target? With full
   evaluation matrix A_z, integral row q and omitted direction
   d_z = A_z⁻¹e_11, test the exact target-identification condition q d_z = 0
   together with the retained rank. Include equality cases; do not assume
   that every displacement breaks reduced access.
3. Where q d_z is nonzero, construct conservatively admitted profile pairs
   with identical retained laws/states but different targets. Repeated
   retained-site shots cannot repair that ambiguity. Restore 11 access
   and compile q A_z⁻¹ as the full-access comparison.

Choose the bounded placements, admission construction and comparisons
before their evaluation. No BF numerical study has run here. This is a
supplied-position portability question, not an unknown-localization noise
model, inferred metric, apparatus calibration or gravity dynamics. RET
integration, physical measurements and the QR-06 adapter remain separately
gated. This publication began from pushed BD commit
`06845f4906b5b61ff3bb4ed72bacd2ede6a0a3c0`; separate RET/core/application
changes are outside its scope.
