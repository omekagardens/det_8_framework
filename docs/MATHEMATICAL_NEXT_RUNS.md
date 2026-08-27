# Validated Riemann and checkpointed Collatz next runs

**Status:** Completed bounded extensions. The Riemann run adds a numerical
zero-count gate and Decimal reevaluation before admitting higher windows. The
Collatz run extends the exact frontier in hash-chained checkpoints and compares
odd residue classes at three moduli.

**Implementations:**

- `det8/models/examples/riemann_validated_extension.py`
- `det8/models/examples/collatz_frontier_extension.py`
- `det8/models/mathematical_next_runs.py`

Run both:

```bash
python3 -m det8.models.mathematical_next_runs
```

## 1. Riemann validation gate

The extension raises the bounded critical-line record from 128 to 512 zeros.
It does not accept the new spacing windows immediately. First it applies three
checks.

### Continuous-argument count

The code continues \(\arg\zeta(s)\) along the conventional path

\[
2\longrightarrow 2+iT\longrightarrow \tfrac12+iT
\]

and evaluates the numerical Riemann--von Mangoldt relation

\[
N(T)=1+\frac{\vartheta(T)}{\pi}
       +\frac{\arg\zeta(\tfrac12+iT)}{\pi}.
\]

The audit height \(T=827.6229926273\) lies between the 512th and 513th
sign-changing critical-line roots. Both argument-continuation resolutions
return exactly 512:

| Audit | Path steps | Continuous count | Largest phase increment |
|---|---|---:|---:|
| Coarse | 0.25 vertical, 0.01 horizontal | 512.000000 | 0.1376 rad |
| Fine | 0.125 vertical, 0.005 horizontal | 512.000000 | 0.0706 rad |

The decreasing phase increment and unchanged integer count guard against a
branch-unwrapping error in this bounded run.

### Decimal root reevaluation

The 1st, 128th, 256th, 384th, and 512th roots are reevaluated with a
50-digit Decimal Euler--Maclaurin implementation. Every \(\pm10^{-8}\)
bracket retains a sign change. The largest direct Decimal zeta residual is

\[
1.96\times10^{-11}.
\]

The 512th zero is at height

\[
\gamma_{512}=826.9058109541.
\]

These checks produce strong numerical agreement between sign-change scanning,
high-precision reevaluation, and total zero counting. They are not directed-
rounding interval enclosures and therefore are not a proof of RH.

## 2. Higher-window RET result

Only after the validation gate passes does the scheduler assimilate three new
24-zero windows:

| Starting zero | Spacing variance | Fraction below 0.5 mean spacing |
|---:|---:|---:|
| 245 | 0.14064 | 0.04348 |
| 129 | 0.12490 | 0.04348 |
| 489 | 0.14975 | 0.04348 |

The posterior changes from the original 128-zero run as follows:

| Declared family | First run | Validated extension |
|---|---:|---:|
| GUE-limit spacing | 0.55377 | 0.59751 |
| Finite-height correction | 0.33019 | 0.32991 |
| Over-rigid spacing | 0.11604 | 0.07258 |
| Poisson spacing | \(5.60\times10^{-16}\) | \(3.37\times10^{-17}\) |
| `M_bottom` | \(6.02\times10^{-10}\) | \(2.00\times10^{-16}\) |

The additional record strengthens the GUE-like description and weakens the
over-rigid alternative. It does not remove the finite-height ambiguity. The
defensible finding remains that the sampled spacings are strongly non-Poisson,
not that RH has been established.

## 3. Checkpointed Collatz frontier

The exact verification frontier is extended from 65,536 to 262,144 in three
blocks. Each block hashes every tuple

```text
(start, status, steps, peak, terminal, repeated value)
```

and chains its digest to the preceding checkpoint. The final chain digest is
the resume token for a subsequent run.

| Checkpoint | Maximum stopping time | Largest peak | New records |
|---|---:|---:|---|
| 65,537--131,072 | 353 at 106,239 | 2,482,111,348 at 113,383 | time and peak |
| 131,073--196,608 | 382 at 156,159 | 17,202,377,752 at 159,487 | time and peak |
| 196,609--262,144 | 442 at 230,631 | 17,202,377,752 at 212,649 | time only |

All 262,144 starting values reached 1. There are zero resource-limited
trajectories and zero verified nontrivial cycles. The cumulative records are:

\[
\text{maximum stopping time}=442\quad(n=230631),
\]

\[
\text{maximum peak}=17{,}202{,}377{,}752\quad(n=159487).
\]

The second occurrence of the peak in the third block does not replace the
earlier cumulative record holder.

## 4. Multi-modulus residue structure

Even residue classes are excluded because their first halving step creates a
trivial comparison. Across the extended range, the odd-class mean spreads are:

| Modulus | Lowest mean class | Highest mean class | Mean spread |
|---:|---:|---:|---:|
| 8 | 5 | 7 | 25.45 steps |
| 16 | 5 | 15 | 37.50 steps |
| 32 | 21 | 31 | 49.04 steps |

For modulus 8 specifically:

| Residue | Mean total stopping time |
|---:|---:|
| 1 | 128.93 |
| 3 | 128.61 |
| 5 | 115.59 |
| 7 | 141.04 |

Thus the original residue-7 minus residue-5 contrast persists and increases
from 20.75 steps in the earlier range to 25.45 steps in the frontier range.
The increasing spread under finer partitions is evidence that the deterministic
residue tree carries predictive workload structure. It is not evidence of a
nonconvergent orbit.

## 5. What the next runs changed

The Riemann result is now protected against the most immediate failure mode of
a sign-change-only scanner: the independently continued argument count agrees
with the number of located critical-line roots through the audit height. A
future proof-grade step still requires directed-rounding interval bounds or an
established Turing-method implementation.

The Collatz search is now resumable by deterministic checkpoint digest and
has a clear escalation rule. A resource-limited trajectory would be rerun with
expanded limits; only an exact repeated nontrivial state would enter the cycle
branch. The next computational frontier can therefore extend without changing
the meaning of prior results.
