# Proof-governed Riemann and Collatz searches

**Status:** Bounded computational search plus adaptive finite-record model
comparison. These runs do not prove either conjecture.

**Implementations:**

- `det8/models/examples/riemann_zero_search.py`
- `det8/models/examples/collatz_search.py`
- `det8/models/mathematical_searches.py`

Run:

```bash
python3 -m det8.models.examples.riemann_zero_search
python3 -m det8.models.examples.collatz_search
python3 -m det8.models.mathematical_searches
python3 run_tests.py
```

## 1. Proof boundary

The mathematical adapters split exact computation from statistical
description:

1. an exact bounded layer records what was computed;
2. RET compares declared models for summaries of that finite record;
3. the result retains the unsearched domain and resource limits.

Posterior weights are conditional predictive support for the finite summaries.
They are not probabilities that a universal conjecture is true or false.

## 2. Riemann critical-line search

The standard-library numerical layer evaluates the analytically continued
zeta function using Euler--Maclaurin summation and scans sign changes of

\[
Z(t)=\Re\!\left[e^{i\vartheta(t)}
\zeta\!\left(\tfrac12+it\right)\right].
\]

It locates 128 sign-changing roots on the critical line, beginning at

\[
\gamma_1=14.134725141734702.
\]

The maximum direct zeta residual among the 128 roots is
\(2.82\times10^{-12}\). For each 24-zero window, the adapter forms locally
unfolded spacings

\[
d_n=(\gamma_{n+1}-\gamma_n)
\frac{\log(\gamma_n/2\pi)}{2\pi}
\]

and normalizes them to unit sample mean. RET then compares four finite-record
families: GUE-limit spacing, Poisson spacing, a finite-height correction, and
an over-rigid alternative. Summary variance and small-gap fraction use a
correlated covariance rather than independent scalar errors.

### Adaptive result

The scheduler sampled windows beginning at zero indices 49, 25, 1, and 97.
The final conditional weights are:

| Declared family | Posterior support |
|---|---:|
| GUE-limit spacing | 0.55377 |
| Finite-height correction | 0.33019 |
| Over-rigid spacing | 0.11604 |
| Poisson spacing | \(5.60\times10^{-16}\) |
| `M_bottom` | \(6.02\times10^{-10}\) |

The finite finding is therefore stronger than “GUE wins”: the sampled record
is sharply inconsistent with Poisson spacing, while the limited height and
small 24-zero windows leave meaningful ambiguity between an asymptotic
GUE-like description and finite-height/over-rigid descriptions.

This is not an RH test. The scanner:

- searches only \(\Re(s)=1/2\), so it cannot find an off-line zero;
- locates sign-changing roots and does not certify even-multiplicity roots;
- does not compare its count with a rigorous interval zero-counting method;
- uses double precision rather than proof-grade interval arithmetic.

## 3. Collatz bounded search

For positive integers the exact layer iterates

\[
T(n)=
\begin{cases}
n/2,&n\equiv0\pmod2,\\
3n+1,&n\equiv1\pmod2.
\end{cases}
\]

Every trajectory has one of three explicit statuses:

- `reached_one`;
- `resource_limit`;
- `verified_cycle`, requiring an actually repeated state before reaching one.

A resource-limited trajectory is unresolved and is never reported as a
counterexample.

### Exact bounded result

All 65,536 starting values in \([1,65536]\) reached 1 within the declared
10,000-step limit. There were no resource-limited starts and no verified
nontrivial cycles.

| Finite-range record | Result |
|---|---:|
| Longest total stopping time | 339 steps |
| Starting value for longest time | 52,527 |
| Largest trajectory peak | 593,279,152 |
| Starting value for largest peak | 60,975 |

This verifies convergence only for that finite range.

### Adaptive workload result

RET models the mean and standard deviation of total stopping time across
finite blocks. Its full covariance is a declared block-to-block predictive
tolerance, not numerical error: the integer trajectories themselves are
computed exactly.

After two calibration blocks, the scheduler first selected the high-range
block \([32769,65536]\), then mod-8 residue blocks over \([8193,32768]\).
The residue means were:

| Residue class | Mean stopping time |
|---:|---:|
| \(1\pmod8\) | 106.84 |
| \(3\pmod8\) | 106.06 |
| \(5\pmod8\) | 96.00 |
| \(7\pmod8\) | 116.75 |

The final selected description is residue-sensitive log-affine growth with
support 0.80397, compared with 0.17271 for log-affine growth without the
residue term and 0.02331 for the log-quadratic family. The fitted signed
mod-8 contrast is

\[
b_8=9.41\pm3.40\ \text{steps}\quad(1\sigma),
\]

where the declared feature assigns \(-b_8\) to residue 5, \(+b_8\) to residue
7, and zero to residues 1 and 3. This is a finite-range modular workload
structure, not a new nonconvergent orbit and not a proof-relevant anomaly by
itself.

## 4. Completed next runs

The next suggested Riemann and Collatz runs are implemented and reported in
`docs/MATHEMATICAL_NEXT_RUNS.md`.

The Riemann record now reaches 512 zeros and is gated by a two-resolution
continuous-argument count plus 50-digit Decimal root checks. The Collatz
frontier now reaches 262,144 in hash-chained checkpoints and reports mod-8,
mod-16, and mod-32 profiles. Their remaining proof boundaries are retained.
