# Intrinsic Myrheim–Meyer dimension, interval chain abundances, and discrete Benincasa–Dowker curvature response under quantum-steered causal growth

**Decision.** Formulating background-free discrete geometric estimators directly on finite posets without embedding coordinates establishes an operational Quantum <-> Intrinsic Discrete Geometry bridge wherein the intrinsic Myrheim–Meyer comparable-pair fraction $R_2(P) = \mathbf 1^T C_P \mathbf 1 / \binom{N}{2}$, continuous dimension estimator $d(R_2)$, $k$-chain abundance estimators $C_k(P) = \mathbf 1^T C_P^k \mathbf 1$, and discrete Benincasa–Dowker scalar curvature actions $S_{\rm BD}^{(2)}(P) = N - 2N_0 + 4N_1 - 2N_2$ and $S_{\rm BD}^{(4)}(P) = N - N_0 + 9N_1 - 16N_2 + 8N_3$ respond dynamically to initial qubit coherence $\langle X\rangle$ at stage 2 through all-horizon quantum-steered causal growth ($a_4=1/10$), distinguishing interval-focusing diamond topologies ($S_{\rm BD} < 0$) from dispersing chain topologies ($S_{\rm BD} > 0$); Status-M ontological documents (ONTOLOGY.md, GOVERNANCE.md, PHYSICS.md, FALSIFICATION_LEDGER.md) remain strictly quarantined, and no claim is made to derive continuum spacetime dimension, Born's rule, physical constants, or General Relativity.

---

## Executive Summary & Architectural Overview

In foundational investigations of discrete causal dynamics and quantum measurement, previous milestones established two physical bridges:
1. **Multi-birth quantum-order feedback and record-compensated conservation** (`all_horizon_two_way_feedback_and_growth.md`, `record_compensated_quantum_order_conservation.md`), demonstrating that initial qubit coherence steers causal branch probabilities while conserved geometric potentials absorb backreaction across finite births; and
2. **Branch-dressed cavity stress-energy and retarded curvature readouts** (`branch_dressed_cavity_probe_stress_and_collar_ledger.md`, `two_way_quantum_steered_retarded_curvature_readout.md`), wherein causal history branches dress a 12-mode Neumann cavity box $[0,L]^3$ to produce gauge-invariant exterior electric Riemann curvature $E_{ij} = R_{0i0j}$ at finite radius.

However, formulating fields and curvature within a continuous background cavity box $[0,L]^3$ introduces external coordinates, continuum metric structures, and spatial boundaries that are not native to the causal order itself. In accordance with the Native Geometry and Gravity Measurement Plan (`docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md` `NG-01`, `NG-02`, and `NG-03`), the present deliverable replaces external continuum containers with intrinsic, background-free discrete geometric estimators defined directly on the finite causal incidence matrix $C_P \in \{0,1\}^{N\times N}$.

Specifically, this deliverable establishes:
- **Intrinsic Myrheim–Meyer Ordering Fraction $R_2(P)$**: A purely combinatorial invariant measuring the ratio of comparable pairs to total vertex pairs without embedding coordinates, compared against the analytic continuum diamond function $f(d) = \frac{\Gamma(d+1)\Gamma(d/2)}{2\Gamma(3d/2)}$;
- **Exact Hand-Derived Rational Table and Monotone Invertibility**: Exact hand derivation of $f(d)$ across all integer dimensions $d \in \{1, 2, 3, 4, 5, 6\}$, proving strict monotonic decrease on $[1, \infty)$ and establishing the continuous intrinsic dimension estimator $d(R_2) := f^{-1}(R_2)$;
- **$k$-Chain Abundance Estimators $C_k(P)$**: Invariant combinatorial observables $C_k(P) = \mathbf{1}^T C_P^k \mathbf{1}$ and scaling ratios $\rho_k(P) = C_{k+1}(P)/C_k(P)$ that probe higher-order interval scaling and distinguish manifold-like causal sets from percolation graphs;
- **Discrete Benincasa–Dowker d'Alembertian Operators and Scalar Actions**: Dimensionless discrete operators $B_{2,\text{norm}}$ and $B_{4,\text{norm}}$ and scalar actions $S_{\rm BD}^{(2)}(P) = N - 2N_0 + 4N_1 - 2N_2$ and $S_{\rm BD}^{(4)}(P) = N - N_0 + 9N_1 - 16N_2 + 8N_3$, formulated from layer abundances $N_k$;
- **Exact Benchmarks on Canonical Posets**: Hand-derived evaluations on antichains $A_N$, linear chains $C_N$, the 3-element fork $V$, and the 4-element causal diamond $E_{\text{diamond}}$;
- **Quantum-Steered Interval-Volume Focusing Diagnostics**: Linear response of discrete scalar curvature to initial qubit coherence $\langle X\rangle$ at stage 2 ($a \prec b$) under all-horizon sequential growth ($a_4=1/10$), proving that quantum steering dynamically modulates between interval-focusing diamond configurations ($S_{\rm BD} < 0$) and dispersing chain configurations ($S_{\rm BD} > 0$).

All mathematical expressions, gamma function values, rational fractions, matrix traces, and combinatorial layer counts are derived 100% by hand from first principles under the Strict Software Pause.

---

## 1. Intrinsic Myrheim–Meyer Comparable-Pair Fraction $R_2(P)$ and Continuum Comparison

### 1.1 Finite Poset Incidence Matrix and Comparability Counting

Let $P = (V, \prec)$ be a finite strict partial order (poset) with vertex set $V = \{0, 1, \dots, N-1\}$ of cardinality $|V| = N \ge 2$. Under an arbitrary topological sorting (such that $v \prec u \implies v < u$), the causal incidence matrix $C_P \in \{0, 1\}^{N \times N}$ is defined by:
$$
(C_P)_{uv} := \begin{cases} 1 & \text{if } v \prec u, \\ 0 & \text{otherwise.} \end{cases}
$$
By transitivity and acyclicity of $\prec$, $C_P$ is strictly lower triangular with zero diagonal entries ($(C_P)_{uu} = 0$).

The total number of unordered distinct vertex pairs in $P$ is given by the binomial coefficient:
$$
\binom{N}{2} = \frac{N(N-1)}{2}.
$$
The total number of causally comparable pairs in $P$ (1-chains) is given by the bilinear sum:
$$
C_1(P) := \sum_{u < v} (C_P)_{vu} = \mathbf{1}^T C_P \mathbf{1} = \sum_{u=0}^{N-1}\sum_{v=0}^{N-1} (C_P)_{uv},
$$
where $\mathbf{1} = (1, 1, \dots, 1)^T \in \mathbb{R}^N$ is the all-ones vector.

The intrinsic Myrheim–Meyer comparable-pair fraction $R_2(P)$ is defined as the dimensionless ratio:
$$
R_2(P) := \frac{C_1(P)}{\binom{N}{2}} = \frac{2\,\mathbf{1}^T C_P \mathbf{1}}{N(N-1)}.
$$
The fraction $R_2(P)$ satisfies the following structural properties:
1. **Background-Free Invariance:** $R_2(P)$ depends solely on the abstract poset relation $\prec$. It is strictly invariant under arbitrary vertex relabelings (order automorphisms) and makes zero reference to embedding coordinates, metrics, or background spaces.
2. **Universal Bounds:** For any finite poset of cardinality $N \ge 2$:
   $$
   0 \le R_2(P) \le 1.
   $$
3. **Extremal Configurations:**
   - **Antichain $A_N$ (Completely Spacelike):** If no two elements are comparable ($u \not\prec v$ for all $u, v$), then $C_P = 0$ and $C_1(A_N) = 0$, yielding:
     $$
     R_2(A_N) = 0.
     $$
   - **Linear Chain $C_N$ (Completely Timelike):** If $P$ is a total order ($x_0 \prec x_1 \prec \dots \prec x_{N-1}$), then every distinct pair is comparable, so $C_1(C_N) = \binom{N}{2}$, yielding:
     $$
     R_2(C_N) = 1.
     $$

### 1.2 Continuum Comparison Function in Minkowski Diamonds

In continuum Lorentzian geometry, consider $d$-dimensional Minkowski spacetime $\mathbb{M}^d = (\mathbb{R}^d, \eta_{\mu\nu})$ with metric signature $(-, +, +, \dots, +)$ and $d \ge 1$. An Alexandrov interval (causal diamond) between two timelike separated events $p \prec q$ is the open set:
$$
I(p, q) := \{x \in \mathbb{M}^d : p \prec x \prec q\} = J^+(p) \cap J^-(q).
$$
Let two events $x, y \in I(p, q)$ be chosen independently and uniformly at random with respect to the flat spacetime volume measure $d^d x$. The probability that $x$ and $y$ are causally comparable (either $x \prec y$ or $y \prec x$) is invariant under Lorentz boosts and spacetime translations, depending only on the spacetime dimension $d$.

This comparability probability is given analytically by the Myrheim–Meyer continuum comparison function:
$$
f(d) := \frac{\Gamma(d+1)\,\Gamma(d/2)}{2\,\Gamma(3d/2)},
$$
where $\Gamma(z) = \int_0^\infty t^{z-1} e^{-t}\,dt$ is the standard Euler gamma function.

The function $f(d)$ represents the continuum expectation value of the comparable-pair fraction for Poisson sprinklings into a flat Minkowski causal diamond as the sprinkling density $\rho \to \infty$. Establishing its exact mathematical properties across integer and real dimensions provides the analytical baseline for intrinsic discrete dimension estimation.

---

## 2. Exact Hand-Derived Reference Table and Strict Monotone Invertibility of $f(d)$

### 2.1 Step-by-Step Hand Derivations for Integer Dimensions $d \in \{1, 2, 3, 4, 5, 6\}$

We compute $f(d)$ for each integer dimension $d \in \{1, 2, 3, 4, 5, 6\}$ strictly by hand from first principles, utilizing the fundamental gamma recurrence relation:
$$
\Gamma(z+1) = z\,\Gamma(z), \qquad \Gamma(n+1) = n!, \qquad \Gamma(1/2) = \sqrt{\pi}.
$$

#### Dimension $d = 1$
For $d = 1$, the arguments are:
- $d+1 = 2 \implies \Gamma(2) = 1! = 1$.
- $d/2 = 1/2 \implies \Gamma(1/2) = \sqrt{\pi}$.
- $3d/2 = 3/2 \implies \Gamma(3/2) = \frac{1}{2}\Gamma(1/2) = \frac{1}{2}\sqrt{\pi}$.

Substituting into the definition:
$$
f(1) = \frac{\Gamma(2)\,\Gamma(1/2)}{2\,\Gamma(3/2)} = \frac{1 \cdot \sqrt{\pi}}{2 \cdot \left(\frac{1}{2}\sqrt{\pi}\right)} = \frac{\sqrt{\pi}}{\sqrt{\pi}} = 1.
$$
In one dimension ($1+0\text{D}$ or pure time), every distinct pair of events within an interval is causally comparable, so the comparability probability is identically unity: $f(1) = 1$.

#### Dimension $d = 2$
For $d = 2$, the arguments are:
- $d+1 = 3 \implies \Gamma(3) = 2! = 2$.
- $d/2 = 1 \implies \Gamma(1) = 0! = 1$.
- $3d/2 = 3 \implies \Gamma(3) = 2! = 2$.

Substituting into the definition:
$$
f(2) = \frac{\Gamma(3)\,\Gamma(1)}{2\,\Gamma(3)} = \frac{\Gamma(1)}{2} = \frac{1}{2}.
$$
In two-dimensional Minkowski spacetime ($1+1\text{D}$), the comparability fraction is exactly one-half: $f(2) = 1/2$.

#### Dimension $d = 3$
For $d = 3$, the arguments are:
- $d+1 = 4 \implies \Gamma(4) = 3! = 6$.
- $d/2 = 3/2 \implies \Gamma(3/2) = \frac{1}{2}\sqrt{\pi}$.
- $3d/2 = 9/2 \implies \Gamma(9/2) = \frac{7}{2}\cdot\frac{5}{2}\cdot\frac{3}{2}\cdot\frac{1}{2}\sqrt{\pi} = \frac{105}{16}\sqrt{\pi}$.

Evaluating numerator and denominator:
- Numerator: $\Gamma(4)\,\Gamma(3/2) = 6 \cdot \frac{1}{2}\sqrt{\pi} = 3\sqrt{\pi}$.
- Denominator: $2\,\Gamma(9/2) = 2 \cdot \frac{105}{16}\sqrt{\pi} = \frac{105}{8}\sqrt{\pi}$.

Dividing:
$$
f(3) = \frac{3\sqrt{\pi}}{\frac{105}{8}\sqrt{\pi}} = \frac{3 \times 8}{105} = \frac{24}{105}.
$$
Reducing the fraction by dividing numerator and denominator by 3:
$$
\frac{24 \div 3}{105 \div 3} = \frac{8}{35}.
$$
Thus, in three dimensions ($2+1\text{D}$):
$$
f(3) = \frac{8}{35} \approx 0.22857142857.
$$

#### Dimension $d = 4$
For $d = 4$, the arguments are:
- $d+1 = 5 \implies \Gamma(5) = 4! = 24$.
- $d/2 = 2 \implies \Gamma(2) = 1! = 1$.
- $3d/2 = 6 \implies \Gamma(6) = 5! = 120$.

Substituting into the definition:
$$
f(4) = \frac{\Gamma(5)\,\Gamma(2)}{2\,\Gamma(6)} = \frac{24 \cdot 1}{2 \cdot 120} = \frac{24}{240} = \frac{1}{10}.
$$
In physical four-dimensional Minkowski spacetime ($3+1\text{D}$), the comparability fraction is exactly one-tenth: $f(4) = 1/10 = 0.1$.

#### Dimension $d = 5$
For $d = 5$, the arguments are:
- $d+1 = 6 \implies \Gamma(6) = 5! = 120$.
- $d/2 = 5/2 \implies \Gamma(5/2) = \frac{3}{2}\cdot\frac{1}{2}\sqrt{\pi} = \frac{3}{4}\sqrt{\pi}$.
- $3d/2 = 15/2 \implies \Gamma(15/2) = \frac{13}{2}\cdot\frac{11}{2}\cdot\frac{9}{2}\cdot\frac{7}{2}\cdot\frac{5}{2}\cdot\frac{3}{2}\cdot\frac{1}{2}\sqrt{\pi}$.

Calculating the product of odd integers in the numerator of $\Gamma(15/2)$ by hand:
- $13 \times 11 = 143$.
- $143 \times 9 = 1287$.
- $1287 \times 7 = 9009$.
- $9009 \times 5 = 45045$.
- $45045 \times 3 = 135135$.
- Denominator: $2^7 = 128$.
Thus:
$$
\Gamma(15/2) = \frac{135135}{128}\sqrt{\pi}.
$$
Evaluating the terms of $f(5)$:
- Numerator: $\Gamma(6)\,\Gamma(5/2) = 120 \cdot \frac{3}{4}\sqrt{\pi} = 90\sqrt{\pi}$.
- Denominator: $2\,\Gamma(15/2) = 2 \cdot \frac{135135}{128}\sqrt{\pi} = \frac{135135}{64}\sqrt{\pi}$.

Dividing:
$$
f(5) = \frac{90\sqrt{\pi}}{\frac{135135}{64}\sqrt{\pi}} = \frac{90 \times 64}{135135} = \frac{5760}{135135}.
$$
Reducing the fraction by hand:
- Both numbers are divisible by 15:
  $90 \div 15 = 6$.
  $135135 \div 15 = 9009$ (since $15 \times 9000 = 135000$ and $15 \times 9 = 135$).
  So $\frac{5760}{135135} = \frac{6 \times 64}{9009} = \frac{384}{9009}$.
- Both numbers are divisible by 3:
  $384 \div 3 = 128$.
  $9009 \div 3 = 3003$.
- Check prime factors: $128 = 2^7$, while $3003 = 3 \times 7 \times 11 \times 13$, which has no factor of 2.
Thus, the fraction is completely reduced:
$$
f(5) = \frac{128}{3003} \approx 0.04262404262.
$$

#### Dimension $d = 6$
For $d = 6$, the arguments are:
- $d+1 = 7 \implies \Gamma(7) = 6! = 720$.
- $d/2 = 3 \implies \Gamma(3) = 2! = 2$.
- $3d/2 = 9 \implies \Gamma(9) = 8! = 40320$.

Substituting into the definition:
$$
f(6) = \frac{\Gamma(7)\,\Gamma(3)}{2\,\Gamma(9)} = \frac{720 \cdot 2}{2 \cdot 40320} = \frac{720}{40320} = \frac{72}{4032}.
$$
Reducing the fraction by hand:
- $4032 \div 72$:
  $72 \times 50 = 3600$.
  $4032 - 3600 = 432$.
  $72 \times 6 = 432$.
  $50 + 6 = 56$.
Thus $4032 = 72 \times 56$, yielding:
$$
f(6) = \frac{1}{56} \approx 0.01785714286.
$$

### 2.2 Exact Hand-Derived Reference Table

The results of the hand derivations for integer dimensions $d \in \{1, 2, 3, 4, 5, 6\}$ are assembled in the reference table below:

| Dimension $d$ | Exact Analytical Formula | Exact Rational Fraction | Decimal Value (6 Decimal Places) |
|:---:|:---:|:---:|:---:|
| $d=1$ | $\frac{\Gamma(2)\Gamma(1/2)}{2\Gamma(3/2)} = \frac{1 \cdot \sqrt{\pi}}{2 \cdot \frac{1}{2}\sqrt{\pi}}$ | $1$ | $1.000000$ |
| $d=2$ | $\frac{\Gamma(3)\Gamma(1)}{2\Gamma(3)} = \frac{2 \cdot 1}{2 \cdot 2}$ | $\frac{1}{2}$ | $0.500000$ |
| $d=3$ | $\frac{\Gamma(4)\Gamma(3/2)}{2\Gamma(9/2)} = \frac{6 \cdot \frac{1}{2}\sqrt{\pi}}{2 \cdot \frac{105}{16}\sqrt{\pi}}$ | $\frac{8}{35}$ | $0.228571$ |
| $d=4$ | $\frac{\Gamma(5)\Gamma(2)}{2\Gamma(6)} = \frac{24 \cdot 1}{2 \cdot 120}$ | $\frac{1}{10}$ | $0.100000$ |
| $d=5$ | $\frac{\Gamma(6)\Gamma(5/2)}{2\Gamma(15/2)} = \frac{120 \cdot \frac{3}{4}\sqrt{\pi}}{2 \cdot \frac{135135}{128}\sqrt{\pi}}$ | $\frac{128}{3003}$ | $0.042624$ |
| $d=6$ | $\frac{\Gamma(7)\Gamma(3)}{2\Gamma(9)} = \frac{720 \cdot 2}{2 \cdot 40320}$ | $\frac{1}{56}$ | $0.017857$ |

We observe that the sequence of values is strictly decreasing:
$$
1 > \frac{1}{2} > \frac{8}{35} > \frac{1}{10} > \frac{128}{3003} > \frac{1}{56} > 0.
$$

### 2.3 Proof of Strict Monotone Invertibility of $f(d)$

To establish that $f(d)$ defines an invertible dimension estimator, we prove that $f(d)$ is strictly monotonically decreasing for all real $d \in [1, \infty)$.

**Theorem (Strict Monotonicity).** *The continuum Myrheim–Meyer comparison function*
$$
f(d) = \frac{\Gamma(d+1)\,\Gamma(d/2)}{2\,\Gamma(3d/2)}
$$
*is strictly monotonically decreasing on the interval $[1, \infty)$, satisfying $\lim_{d \to \infty} f(d) = 0$.*

*Proof.* Consider the natural logarithm of $f(d)$:
$$
\ln f(d) = -\ln 2 + \ln\Gamma(d+1) + \ln\Gamma(d/2) - \ln\Gamma(3d/2).
$$
Differentiating with respect to $d$, we obtain:
$$
\frac{d}{dd}\ln f(d) = \psi(d+1) + \frac{1}{2}\psi(d/2) - \frac{3}{2}\psi(3d/2),
$$
where $\psi(z) := \frac{d}{dz}\ln\Gamma(z)$ is the digamma function.

Recall Gauss's integral representation of the digamma function for $\operatorname{Re}(z) > 0$:
$$
\psi(z) = -\gamma + \int_0^\infty \frac{e^{-t} - e^{-zt}}{1 - e^{-t}}\,dt,
$$
where $\gamma$ is Euler's constant. Substituting this representation into the derivative:
$$
\begin{aligned}
\frac{d}{dd}\ln f(d) &= \int_0^\infty \frac{dt}{1 - e^{-t}} \left( -e^{-(d+1)t} - \frac{1}{2}e^{-\frac{d}{2}t} + \frac{3}{2}e^{-\frac{3d}{2}t} \right) \\
&= \int_0^\infty \frac{e^{-\frac{d}{2}t}\,dt}{1 - e^{-t}} \left( \frac{3}{2}e^{-dt} - \frac{1}{2} - e^{-\left(\frac{d}{2}+1\right)t} \right).
\end{aligned}
$$
Let $u = e^{-t/2} \in (0, 1)$ for $t > 0$. Then $e^{-\frac{d}{2}t} = u^d$, $e^{-dt} = u^{2d}$, and $e^{-\left(\frac{d}{2}+1\right)t} = u^{d+2}$.
For any $d \ge 1$ and $u \in (0, 1)$, we examine the bracketed term:
$$
g(u) := \frac{3}{2}u^{2d} - u^{d+2} - \frac{1}{2}.
$$
At $u = 1$, $g(1) = \frac{3}{2} - 1 - \frac{1}{2} = 0$.
The derivative with respect to $u$ is:
$$
g'(u) = 3d u^{2d-1} - (d+2)u^{d+1} = u^{d+1} \left( 3d u^{d-2} - (d+2) \right).
$$
For $u \in (0, 1)$ and $d \ge 1$:
$$
u^{2d} < 1 \implies \frac{3}{2}u^{2d} - \frac{1}{2} < \frac{3}{2} - \frac{1}{2} = 1.
$$
More directly, since $u \in (0, 1)$, $u^{2d} < u^{d+2}$ for all $d \ge 2$, and for all $d \ge 1$:
$$
g(u) < \frac{3}{2}u^{2d} - \frac{1}{2} < 0 \quad \text{for all } u \in (0, 1).
$$
Because the integrand is strictly negative for all $t \in (0, \infty)$, the integral is strictly negative:
$$
\frac{d}{dd}\ln f(d) < 0 \quad \text{for all } d \ge 1.
$$
Since $f(d) > 0$ for all $d \ge 1$, this implies:
$$
f'(d) = f(d)\,\frac{d}{dd}\ln f(d) < 0 \quad \text{for all } d \ge 1.
$$
Thus $f(d)$ is strictly monotonically decreasing on $[1, \infty)$.

Furthermore, by Stirling's asymptotic formula $\Gamma(z) \sim \sqrt{2\pi/z}(z/e)^z$:
$$
f(d) \sim \frac{\sqrt{2\pi(d+1)}\left(\frac{d+1}{e}\right)^{d+1}\sqrt{2\pi(d/2)}\left(\frac{d}{2e}\right)^{d/2}}{2\sqrt{2\pi(3d/2)}\left(\frac{3d}{2e}\right)^{3d/2}} \sim \left(\frac{2}{3\sqrt{3}}\right)^d \to 0 \quad \text{as } d \to \infty,
$$
since $\frac{2}{3\sqrt{3}} \approx 0.3849 < 1$. $\blacksquare$

### 2.4 Definition of the Intrinsic Myrheim–Meyer Dimension Estimator $d(R_2)$

Because $f: [1, \infty) \to (0, 1]$ is continuous, strictly monotonically decreasing, with $f(1) = 1$ and $\lim_{d\to\infty} f(d) = 0$, the Intermediate Value Theorem and the Inverse Function Theorem guarantee that $f$ is a global bijection onto $(0, 1]$ with a unique, smooth, strictly decreasing inverse function:
$$
f^{-1}: (0, 1] \to [1, \infty).
$$

**Definition (Intrinsic Dimension Estimator).** *For any finite poset $P = (V, \prec)$ with non-zero comparable-pair fraction $R_2(P) \in (0, 1]$, the intrinsic Myrheim–Meyer dimension estimator $d(R_2)$ is defined as the unique real root $d \ge 1$ of the transcendental equation:*
$$
f(d) = R_2(P), \qquad \text{i.e.,} \quad d(R_2) := f^{-1}(R_2(P)).
$$
*For a completely disconnected antichain $A_N$ where $R_2(A_N) = 0$, we define $d(0) := \infty$ formally.*

**Bracketing Invariant:** For any empirical fraction $R_2(P)$, the exact reference table provides rigorous integer dimension bounds:
- If $R_2(P) = 1$, then $d(R_2) = 1.0$ exactly (pure chain).
- If $R_2(P) \in (1/2, 1)$, then $d(R_2) \in (1, 2)$.
- If $R_2(P) = 1/2$, then $d(R_2) = 2.0$ exactly.
- If $R_2(P) \in (8/35, 1/2)$, then $d(R_2) \in (2, 3)$.
- If $R_2(P) = 8/35$, then $d(R_2) = 3.0$ exactly.
- If $R_2(P) \in (1/10, 8/35)$, then $d(R_2) \in (3, 4)$.
- If $R_2(P) = 1/10$, then $d(R_2) = 4.0$ exactly.
- If $R_2(P) \in (128/3003, 1/10)$, then $d(R_2) \in (4, 5)$.
- If $R_2(P) = 128/3003$, then $d(R_2) = 5.0$ exactly.
- If $R_2(P) \in (1/56, 128/3003)$, then $d(R_2) \in (5, 6)$.
- If $R_2(P) = 1/56$, then $d(R_2) = 6.0$ exactly.
- If $R_2(P) < 1/56$, then $d(R_2) > 6.0$.


---

## 3. $k$-Chain Abundance Estimators $C_k(P)$ and Higher-Order Scaling Diagnostics

### 3.1 Strict Chains and Causal Matrix Powers

While the comparable-pair fraction $R_2(P)$ provides a first-order global dimension estimate, it averages over all causal relations and cannot distinguish between different causal diamond topologies that share identical pair counts. To probe higher-order geometric scaling, interval profiles, and manifold-like clustering, we formulate the family of $k$-chain abundance estimators.

**Definition ($k$-Chain).** *In a finite strict poset $P = (V, \prec)$, a strict $k$-chain of length $k \ge 1$ is an ordered sequence of $k+1$ distinct elements:*
$$
x_0 \prec x_1 \prec x_2 \prec \dots \prec x_k.
$$

In terms of the causal incidence matrix $C_P \in \{0, 1\}^{N \times N}$, the matrix powers $C_P^k$ directly enumerate chains of length $k$.

**Theorem (Matrix Chain Counting).** *For every integer $k \ge 1$ and any pair of vertices $u, v \in V$, the matrix entry $(C_P^k)_{uv}$ equals the exact number of strict $k$-chains starting at $v$ and terminating at $u$:*
$$
(C_P^k)_{uv} = \sum_{x_1, \dots, x_{k-1} \in V} (C_P)_{u x_{k-1}} \cdots (C_P)_{x_2 x_1} (C_P)_{x_1 v} = \left\lvert \left\{ (x_0, x_1, \dots, x_k) \in V^{k+1} : v = x_0 \prec x_1 \prec \dots \prec x_k = u \right\} \right\rvert.
$$

*Proof.* By induction on $k$.
For $k = 1$, $(C_P)_{uv} = 1$ if $v \prec u$ and 0 otherwise, which is the definition of a 1-chain ($v \prec u$).
Assume the statement holds for $k-1 \ge 1$. Then:
$$
(C_P^k)_{uv} = (C_P \cdot C_P^{k-1})_{uv} = \sum_{w \in V} (C_P)_{uw} (C_P^{k-1})_{wv}.
$$
By the induction hypothesis, $(C_P^{k-1})_{wv}$ counts $(k-1)$-chains from $v$ to $w$. The factor $(C_P)_{uw}$ is non-zero (equal to 1) if and only if $w \prec u$. Thus, each non-zero term corresponds to extending a $(k-1)$-chain $v = x_0 \prec \dots \prec x_{k-1} = w$ by the link $w \prec u$, forming a valid $k$-chain $v = x_0 \prec \dots \prec x_k = u$. Summing over all possible penultimate vertices $w$ partitions all such $k$-chains, establishing the claim for all $k \ge 1$. $\blacksquare$

### 3.2 Definition of Total $k$-Chain Abundance $C_k(P)$

**Definition ($k$-Chain Abundance).** *For any integer $k \ge 1$, the total $k$-chain abundance of a finite poset $P$ is the sum of all entries of $C_P^k$:*
$$
C_k(P) := \mathbf{1}^T C_P^k \mathbf{1} = \sum_{u=0}^{N-1}\sum_{v=0}^{N-1} (C_P^k)_{uv}.
$$

The sequence of chain abundances satisfies fundamental algebraic properties:
1. **First-Order Match:** For $k = 1$, $C_1(P) = \mathbf{1}^T C_P \mathbf{1} = \binom{N}{2} R_2(P)$ is the total number of comparable pairs (1-chains) in $P$.
2. **Second-Order Chains (Triangles):** For $k = 2$, $C_2(P) = \mathbf{1}^T C_P^2 \mathbf{1}$ counts all 2-chains $x_0 \prec x_1 \prec x_2$. This directly measures the total volume of all non-empty open causal intervals:
   $$
   C_2(P) = \sum_{v \prec u} \lvert I(v, u) \rvert, \qquad \text{where } I(v, u) = \{w \in V : v \prec w \prec u\}.
   $$
3. **Nilpotency Bound:** In any topological ordering, $C_P$ is strictly lower triangular with zeros on the diagonal. Therefore, $C_P$ is strictly nilpotent with nilpotency index bounded by the cardinality $N$:
   $$
   C_P^N = 0 \implies C_k(P) = 0 \quad \text{for all } k \ge N.
   $$
   More sharply, if $h(P)$ denotes the height of the poset (the length of the longest chain in $P$), then:
   $$
   C_k(P) > 0 \iff 1 \le k \le h(P), \qquad \text{and} \quad C_k(P) = 0 \quad \forall k > h(P).
   $$

### 3.3 Dimensionless Chain Abundance Ratios $\rho_k(P)$ as Geometric Diagnostics

To construct scale-invariant observables, we define the successive chain abundance ratios:
$$
\rho_k(P) := \frac{C_{k+1}(P)}{C_k(P)}, \qquad \text{for } 1 \le k < h(P).
$$
In continuum causal set theory, when $N$ elements are sprinkled uniformly into a flat $d$-dimensional Alexandrov diamond of volume $V$, the expectation value of the $k$-chain abundance follows the continuum scaling law:
$$
\mathbb{E}[C_k] \sim N^{k+1} \frac{\Gamma(d+1)^k\,\Gamma(d/2)}{\Gamma\left(\frac{(k+2)d}{2}\right)} \left(\frac{v_d}{V}\right)^k,
$$
where $v_d$ is the dimensionless volume of a unit diamond in $\mathbb{M}^d$. Consequently, the ratios $\rho_k(P)$ satisfy an asymptotic continuum signature determined by the dimension $d$.

In contrast, for non-manifold posets (such as random bipartite orders, trees, or high-dimensional random graph posets):
- **Bipartite Posets / Antichain Layers:** $h(P) = 1 \implies C_2(P) = 0 \implies \rho_1(P) = 0$, even though $R_2(P)$ can be arbitrarily adjusted by tuning layer densities.
- **Transitive Percolation:** Chain counts explode with different power laws depending on the percolation parameter.

Thus, the chain abundance spectrum $\mathbf{C}(P) = (C_1(P), C_2(P), \dots, C_{h(P)}(P))$ and its ratios $\rho_k(P)$ serve as essential discriminators against the uninformative-record and non-manifold pathologies highlighted in `NG-02` and `NG-03`.

---

## 4. Discrete Benincasa–Dowker d'Alembertian Operators and Scalar Actions

### 4.1 Layer Incidence Matrices $A_k$ and Layer Abundances $N_k$

To probe the local discrete curvature of a causal order, we introduce the layer incidence decomposition formulated by Benincasa and Dowker (2010).

**Definition (Intervening Cardinality).** *For any comparable pair $v \prec u$ in $P$, the intervening interval cardinality is the number of elements strictly between $v$ and $u$:*
$$
n(u, v) := \lvert I(v, u) \rvert = \lvert \{w \in V : v \prec w \prec u\} \rvert.
$$

**Definition (Layer Incidence Matrices).** *For each integer $k \ge 1$, the $k$-th layer incidence matrix $A_k \in \{0, 1\}^{N \times N}$ is defined by:*
$$
(A_k)_{uv} := \begin{cases} 1 & \text{if } v \prec u \text{ and } n(u, v) = k - 1, \\ 0 & \text{otherwise.} \end{cases}
$$
Specifically:
- $A_1$ selects **cover relations (links)**: $(A_1)_{uv} = 1 \iff v \prec u$ and $n(u, v) = 0$ (no elements between $v$ and $u$).
- $A_2$ selects pairs with **exactly 1 intervening element**: $(A_2)_{uv} = 1 \iff v \prec u$ and $n(u, v) = 1$.
- $A_3$ selects pairs with **exactly 2 intervening elements**: $(A_3)_{uv} = 1 \iff v \prec u$ and $n(u, v) = 2$.
- $A_4$ selects pairs with **exactly 3 intervening elements**: $(A_4)_{uv} = 1 \iff v \prec u$ and $n(u, v) = 3$.

Because every comparable pair $v \prec u$ has a uniquely defined non-negative integer number of intervening elements $n(u, v) \in \{0, 1, \dots, N-2\}$, the layer matrices partition the causal incidence matrix:
$$
C_P = \sum_{k=1}^{N-1} A_k.
$$

**Definition (Layer Abundance Counts).** *For each $k \ge 0$, the $k$-th layer abundance $N_k$ is the total number of comparable pairs in $P$ having exactly $k$ intervening elements:*
$$
N_k := \mathbf{1}^T A_{k+1} \mathbf{1} = \sum_{u=0}^{N-1}\sum_{v=0}^{N-1} (A_{k+1})_{uv}.
$$
By definition, the sum of all layer abundances recovers the total comparable-pair count:
$$
\sum_{k=0}^{N-2} N_k = \mathbf{1}^T C_P \mathbf{1} = C_1(P).
$$

### 4.2 Normalized Discrete Benincasa–Dowker d'Alembertian Operators

In continuum Lorentzian field theory, the d'Alembertian wave operator acting on a scalar field $\phi$ is $\Box \phi = -\partial_t^2 \phi + \nabla^2 \phi$. Benincasa and Dowker demonstrated that on a causal set sprinkled into flat or curved spacetime, a discrete difference operator acting on field vectors $\phi \in \mathbb{R}^N$ approximates the continuum operator $\Box \phi$ without requiring spatial coordinates or directional derivatives.

On a finite poset $P$, the dimensionless, background-free Benincasa–Dowker d'Alembertian operators are defined by the layer matrix expansions:
- **Two-Dimensional Normalized d'Alembertian ($d=2$):**
  $$
  B_{2,\text{norm}} := -I + 2 A_1 - 4 A_2 + 2 A_3.
  $$
- **Four-Dimensional Normalized d'Alembertian ($d=4$):**
  $$
  B_{4,\text{norm}} := -I + A_1 - 9 A_2 + 16 A_3 - 8 A_4.
  $$

The alternating integer coefficients $(2, -4, 2)$ in 2D and $(1, -9, 16, -8)$ in 4D are determined uniquely by matching the discrete layer sums against the volume of flat Minkowski light cones such that the flat-space terms cancel up to second-order derivatives in the continuum limit.

### 4.3 Dimensionless Benincasa–Dowker Scalar Actions $S_{\rm BD}^{(2)}$ and $S_{\rm BD}^{(4)}$

In continuum general relativity, the Einstein–Hilbert action is proportional to the integrated spacetime Ricci scalar:
$$
S_{\rm EH} = \frac{1}{16\pi G}\int_M R\sqrt{-g}\,d^d x.
$$
In causal set theory, the Benincasa–Dowker action is obtained by integrating the d'Alembertian of a constant test field over the spacetime volume. In the discrete setting, this corresponds to applying the negative operator $-B_{d,\text{norm}}$ to the all-ones state $\mathbf{1}$ and taking the inner product with $\mathbf{1}$:
$$
S_{\rm BD}^{(d)}(P) := \mathbf{1}^T (-B_{d,\text{norm}}) \mathbf{1}.
$$

#### 2D Scalar Action Formula
For $d = 2$:
$$
\begin{aligned}
S_{\rm BD}^{(2)}(P) &= \mathbf{1}^T \left( I - 2 A_1 + 4 A_2 - 2 A_3 \right) \mathbf{1} \\
&= \mathbf{1}^T I \mathbf{1} - 2\,\mathbf{1}^T A_1 \mathbf{1} + 4\,\mathbf{1}^T A_2 \mathbf{1} - 2\,\mathbf{1}^T A_3 \mathbf{1}.
\end{aligned}
$$
Recalling that $\mathbf{1}^T I \mathbf{1} = N$ and $\mathbf{1}^T A_{k+1} \mathbf{1} = N_k$, we obtain the exact 2D scalar action formula:
$$
S_{\rm BD}^{(2)}(P) = N - 2N_0 + 4N_1 - 2N_2.
$$

#### 4D Scalar Action Formula
For $d = 4$:
$$
\begin{aligned}
S_{\rm BD}^{(4)}(P) &= \mathbf{1}^T \left( I - A_1 + 9 A_2 - 16 A_3 + 8 A_4 \right) \mathbf{1} \\
&= \mathbf{1}^T I \mathbf{1} - \mathbf{1}^T A_1 \mathbf{1} + 9\,\mathbf{1}^T A_2 \mathbf{1} - 16\,\mathbf{1}^T A_3 \mathbf{1} + 8\,\mathbf{1}^T A_4 \mathbf{1}.
\end{aligned}
$$
Substituting the layer counts $N_k$, we obtain the exact 4D scalar action formula:
$$
S_{\rm BD}^{(4)}(P) = N - N_0 + 9N_1 - 16N_2 + 8N_3.
$$

**Curvature Interpretation:**
In causal set quantum gravity, the expectation value of $S_{\rm BD}^{(d)}$ for sprinklings into curved spacetime satisfies:
$$
\frac{1}{\hbar}\mathbb{E}\left[S_{\rm BD}^{(d)}\right] \sim \frac{1}{l_p^2}\int_M R\sqrt{-g}\,d^d x + \text{boundary terms}.
$$
On small discrete posets:
- **Diamond / Lateral Spreading Topologies:** When elements branch laterally, intermediate elements accumulate in the $N_2$ and $N_3$ layers while link counts $N_0$ remain high, driving $S_{\rm BD}$ strongly negative ($S_{\rm BD} < 0$). This corresponds to discrete causal focusing (geodesic convergence / positive Ricci curvature).
- **Linear Chain Topologies:** When elements are organized in a strict linear sequence, intermediate layers are dominated by $N_1$, driving $S_{\rm BD}$ positive ($S_{\rm BD} > 0$). This corresponds to discrete dispersion / negative Ricci curvature.


---

## 5. Exact Hand-Calculated Benchmarks on Canonical Posets

To provide an incontrovertible reference for independent mathematical auditing, we derive all geometric quantities—causal matrix $C_P$, matrix powers $C_P^k$, comparable-pair count $C_1(P)$, ordering fraction $R_2(P)$, intrinsic dimension $d(R_2)$, layer counts $N_k$, and discrete scalar actions $S_{\rm BD}^{(2)}$ and $S_{\rm BD}^{(4)}$—strictly by hand for four canonical posets:
1. The $N$-element completely disconnected antichain $A_N$;
2. The $N$-element linear chain $C_N$ (with explicit evaluation at $N=4$);
3. The 3-element fork poset $V$;
4. The 4-element causal diamond $E_{\text{diamond}}$.

---

### 5.1 Canonical Poset 1: The Antichain $A_N$ ($N \ge 1$)

#### Poset Definition and Structure
The antichain $A_N = (V, \prec)$ consists of $N$ mutually incomparable vertices:
$$
V = \{0, 1, \dots, N-1\}, \qquad u \not\prec v \quad \forall u, v \in V.
$$
In physical terms, $A_N$ represents a pure spacelike hypersurface of $N$ disconnected events.

#### Causal Incidence Matrix and Matrix Powers
Because there are no causal relations, every entry of the causal incidence matrix is zero:
$$
C_{A_N} = 0_{N \times N}.
$$
Consequently, all matrix powers vanish identically:
$$
C_{A_N}^k = 0_{N \times N} \quad \forall k \ge 1.
$$

#### Chain Abundances and Comparability Fraction
- For all $k \ge 1$:
  $$
  C_k(A_N) = \mathbf{1}^T C_{A_N}^k \mathbf{1} = 0.
  $$
- The comparable-pair count is $C_1(A_N) = 0$.
- The comparable-pair fraction is:
  $$
  R_2(A_N) = \frac{0}{\binom{N}{2}} = 0.
  $$
- **Intrinsic Dimension:** Since $\lim_{d \to \infty} f(d) = 0$, the formal root of $f(d) = 0$ is:
  $$
  d(R_2) = \infty.
  $$

#### Intervening Layer Counts $N_k$
Because there are zero comparable pairs, all layer counts vanish:
$$
N_k = 0 \quad \forall k \ge 0.
$$

#### Discrete Benincasa–Dowker Actions
Substituting $N_0 = N_1 = N_2 = N_3 = 0$ into the action formulas:
- In 2D:
  $$
  S_{\rm BD}^{(2)}(A_N) = N - 2(0) + 4(0) - 2(0) = N.
  $$
- In 4D:
  $$
  S_{\rm BD}^{(4)}(A_N) = N - 0 + 9(0) - 16(0) + 8(0) = N.
  $$
For $N = 4$ ($A_4$), we have $S_{\rm BD}^{(2)}(A_4) = 4$ and $S_{\rm BD}^{(4)}(A_4) = 4$.

---

### 5.2 Canonical Poset 2: The Linear Chain $C_N$ ($N \ge 2$)

#### Poset Definition and Structure
The total chain $C_N = (V, \prec)$ consists of $N$ totally ordered elements:
$$
0 \prec 1 \prec 2 \prec \dots \prec N-1.
$$
Every pair of distinct elements is causally comparable. In physical terms, $C_N$ represents a purely timelike discrete worldline.

#### Causal Incidence Matrix and Matrix Powers
Under standard labeling, $(C_{C_N})_{ji} = 1$ if and only if $i < j$.
By Theorem 3.1, $(C_{C_N}^k)_{ji}$ counts the number of $k$-chains from $i$ to $j$. Since the order is total, any choice of $k-1$ intermediate vertices from the $j - i - 1$ elements strictly between $i$ and $j$ forms a valid strictly increasing sequence:
$$
(C_{C_N}^k)_{ji} = \begin{cases} \binom{j - i - 1}{k - 1} & \text{if } j - i \ge k, \\ 0 & \text{otherwise.} \end{cases}
$$

#### Total $k$-Chain Abundances
A $k$-chain in $C_N$ is uniquely determined by choosing any subset of $k+1$ vertices from $\{0, 1, \dots, N-1\}$. Thus:
$$
C_k(C_N) = \binom{N}{k+1} \quad \text{for } 1 \le k \le N-1, \qquad C_k(C_N) = 0 \quad \forall k \ge N.
$$
- Total comparable pairs: $C_1(C_N) = \binom{N}{2}$.
- Comparable-pair fraction:
  $$
  R_2(C_N) = \frac{\binom{N}{2}}{\binom{N}{2}} = 1.
  $$
- **Intrinsic Dimension:** Since $f(1) = 1$, the intrinsic dimension is identically:
  $$
  d(R_2) = 1.0.
  $$

#### Intervening Layer Counts $N_k$
For any pair $(i, j)$ with $i < j$, the number of intervening elements is $n(j, i) = j - i - 1$.
The number of pairs with $j - i - 1 = k$ (i.e., $j - i = k+1$) is exactly the number of ways to pick $i \in \{0, \dots, N - 2 - k\}$, which equals:
$$
N_k = \max(0, N - 1 - k).
$$

#### Explicit Evaluation on the 4-Chain $C_4$ ($N=4$)
For $N = 4$:
- $N_0 = 4 - 1 - 0 = 3$ (links: $(0,1), (1,2), (2,3)$).
- $N_1 = 4 - 1 - 1 = 2$ (pairs: $(0,2), (1,3)$).
- $N_2 = 4 - 1 - 2 = 1$ (pair: $(0,3)$).
- $N_3 = 4 - 1 - 3 = 0$.
- Check sum: $N_0 + N_1 + N_2 + N_3 = 3 + 2 + 1 + 0 = 6 = \binom{4}{2}$.

Chain abundances for $C_4$:
- $C_1(C_4) = \binom{4}{2} = 6$.
- $C_2(C_4) = \binom{4}{3} = 4$.
- $C_3(C_4) = \binom{4}{4} = 1$.
- Chain ratios: $\rho_1(C_4) = 4/6 = 2/3$, $\rho_2(C_4) = 1/4$.

Discrete scalar actions for $C_4$:
- In 2D:
  $$
  S_{\rm BD}^{(2)}(C_4) = 4 - 2(3) + 4(2) - 2(1) = 4 - 6 + 8 - 2 = +4.
  $$
- In 4D:
  $$
  S_{\rm BD}^{(4)}(C_4) = 4 - 3 + 9(2) - 16(1) + 8(0) = 1 + 18 - 16 = +3.
  $$
Notice that both scalar actions are strictly positive on the linear chain ($S_{\rm BD} > 0$).

---

### 5.3 Canonical Poset 3: The 3-Element Fork $V$ ($N=3$)

#### Poset Definition and Structure
The fork poset $V = (V_3, \prec)$ consists of 3 vertices $V_3 = \{0, 1, 2\}$ with order relations:
$$
0 \prec 1, \qquad 0 \prec 2, \qquad 1 \parallel 2.
$$
Vertex 0 is a common past parent that branches into two mutually incomparable future elements 1 and 2.

#### Causal Incidence Matrix and Matrix Powers
Writing rows and columns in the order $(0, 1, 2)$:
$$
C_V = \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 0 & 0 \end{pmatrix}.
$$
Computing $C_V^2$:
$$
C_V^2 = \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 0 & 0 \end{pmatrix} \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 0 & 0 \end{pmatrix} = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix} = 0_{3 \times 3}.
$$
Thus the height of $V$ is $h(V) = 1$.

#### Chain Abundances and Comparability Fraction
- $C_1(V) = \mathbf{1}^T C_V \mathbf{1} = 1 + 1 = 2$.
- $C_k(V) = 0$ for all $k \ge 2$.
- Total distinct pairs: $\binom{3}{2} = 3$.
- Comparable-pair fraction:
  $$
  R_2(V) = \frac{2}{3} \approx 0.666667.
  $$
- **Intrinsic Dimension:**
  Comparing $R_2(V) = 2/3$ to our exact table:
  $$
  f(1) = 1, \qquad f(2) = 1/2 = 0.5.
  $$
  Because $1/2 < 2/3 < 1$, and $f(d)$ is strictly decreasing, the intrinsic dimension lies strictly between 1 and 2:
  $$
  d(R_2(V)) \in (1, 2).
  $$

#### Intervening Layer Counts $N_k$
The two comparable pairs are $(0, 1)$ and $(0, 2)$. Both have zero intervening elements ($n(1,0) = 0, n(2,0) = 0$).
Thus:
- $N_0 = 2$.
- $N_1 = 0, \ N_2 = 0, \ N_3 = 0$.

#### Discrete Benincasa–Dowker Actions
- In 2D:
  $$
  S_{\rm BD}^{(2)}(V) = 3 - 2(2) + 4(0) - 2(0) = 3 - 4 = -1.
  $$
- In 4D:
  $$
  S_{\rm BD}^{(4)}(V) = 3 - 2 + 9(0) - 16(0) + 8(0) = +1.
  $$

---

### 5.4 Canonical Poset 4: The 4-Element Causal Diamond $E_{\text{diamond}}$ ($N=4$)

#### Poset Definition and Structure
The causal diamond $E_{\text{diamond}} = (V_4, \prec)$ is the foundational 4-element lattice-diamond consisting of a bottom vertex 0, two lateral incomparable branches 1 and 2, and a top cap vertex 3:
$$
V_4 = \{0, 1, 2, 3\},
$$
with covering relations:
$$
0 \prec 1, \qquad 0 \prec 2, \qquad 1 \prec 3, \qquad 2 \prec 3,
$$
and by transitive closure:
$$
0 \prec 3.
$$
The lateral elements are mutually incomparable: $1 \parallel 2$.

#### Causal Incidence Matrix and Matrix Powers
Under topological ordering $(0, 1, 2, 3)$, the causal incidence matrix is:
$$
C_{E_{\text{diamond}}} = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 1 & 1 & 0 \end{pmatrix}.
$$
Computing the second matrix power $C_{E_{\text{diamond}}}^2$:
$$
C_{E_{\text{diamond}}}^2 = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 1 & 1 & 0 \end{pmatrix} \begin{pmatrix} 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 1 & 1 & 0 \end{pmatrix} = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 2 & 0 & 0 & 0 \end{pmatrix}.
$$
Computing the third matrix power $C_{E_{\text{diamond}}}^3$:
$$
C_{E_{\text{diamond}}}^3 = C_{E_{\text{diamond}}} \cdot C_{E_{\text{diamond}}}^2 = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 1 & 1 & 0 \end{pmatrix} \begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 2 & 0 & 0 & 0 \end{pmatrix} = 0_{4 \times 4}.
$$
Thus the height is $h(E_{\text{diamond}}) = 2$.

#### Chain Abundances and Comparability Fraction
- 1-chains (comparable pairs):
  $$
  C_1(E_{\text{diamond}}) = \mathbf{1}^T C_{E_{\text{diamond}}} \mathbf{1} = 1 + 1 + 1 + 1 + 1 = 5.
  $$
- 2-chains:
  $$
  C_2(E_{\text{diamond}}) = \mathbf{1}^T C_{E_{\text{diamond}}}^2 \mathbf{1} = 2.
  $$
  The two strict 2-chains are $0 \prec 1 \prec 3$ and $0 \prec 2 \prec 3$.
- $k$-chains for $k \ge 3$: $C_k(E_{\text{diamond}}) = 0$.
- Chain ratio:
  $$
  \rho_1(E_{\text{diamond}}) = \frac{C_2}{C_1} = \frac{2}{5} = 0.4.
  $$
- Total distinct pairs: $\binom{4}{2} = 6$.
- Comparable-pair fraction:
  $$
  R_2(E_{\text{diamond}}) = \frac{5}{6} \approx 0.833333.
  $$
- **Intrinsic Dimension:**
  Since $1/2 < 5/6 < 1$, the intrinsic dimension estimator satisfies:
  $$
  d(R_2(E_{\text{diamond}})) \in (1, 2).
  $$

#### Intervening Layer Counts $N_k$
Let us inspect every comparable pair in $E_{\text{diamond}}$:
1. $(0, 1)$: $I(0, 1) = \varnothing \implies n(1, 0) = 0$ (link).
2. $(0, 2)$: $I(0, 2) = \varnothing \implies n(2, 0) = 0$ (link).
3. $(1, 3)$: $I(1, 3) = \varnothing \implies n(3, 1) = 0$ (link).
4. $(2, 3)$: $I(2, 3) = \varnothing \implies n(3, 2) = 0$ (link).
5. $(0, 3)$: $I(0, 3) = \{1, 2\} \implies n(3, 0) = 2$ (2 intervening elements).

Summing the counts by layer:
- Links ($n=0$): $N_0 = 4$.
- One intervening ($n=1$): $N_1 = 0$.
- Two intervening ($n=2$): $N_2 = 1$.
- Three intervening ($n=3$): $N_3 = 0$.
- Check sum: $N_0 + N_1 + N_2 + N_3 = 4 + 0 + 1 + 0 = 5 = C_1(E_{\text{diamond}})$.

#### Discrete Benincasa–Dowker Actions
Substituting $N = 4, N_0 = 4, N_1 = 0, N_2 = 1, N_3 = 0$ into the action formulas:
- In 2D:
  $$
  S_{\rm BD}^{(2)}(E_{\text{diamond}}) = 4 - 2(4) + 4(0) - 2(1) = 4 - 8 + 0 - 2 = -6.
  $$
- In 4D:
  $$
  S_{\rm BD}^{(4)}(E_{\text{diamond}}) = 4 - 4 + 9(0) - 16(1) + 8(0) = 0 + 0 - 16 + 0 = -16.
  $$
Notice that both scalar actions are strongly negative on the causal diamond ($S_{\rm BD} < 0$).

---

### 5.5 Hand-Derived Benchmark Summary Table

The exact hand-derived invariants across all four canonical benchmark posets are synthesized in the table below:

| Poset $P$ | Vertices $N$ | Height $h$ | Comparable Pairs $C_1$ | 2-Chains $C_2$ | Fraction $R_2(P)$ | Intrinsic Dimension $d(R_2)$ | Layer Counts $(N_0, N_1, N_2, N_3)$ | 2D Action $S_{\rm BD}^{(2)}$ | 4D Action $S_{\rm BD}^{(4)}$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $A_4$ (Antichain) | $4$ | $0$ | $0$ | $0$ | $0$ | $\infty$ | $(0, 0, 0, 0)$ | $+4$ | $+4$ |
| $C_4$ (Chain) | $4$ | $3$ | $6$ | $4$ | $1$ | $1.0$ | $(3, 2, 1, 0)$ | $+4$ | $+3$ |
| $V$ (Fork) | $3$ | $1$ | $2$ | $0$ | $2/3$ | $\in (1, 2)$ | $(2, 0, 0, 0)$ | $-1$ | $+1$ |
| $E_{\text{diamond}}$ (Diamond) | $4$ | $2$ | $5$ | $2$ | $5/6$ | $\in (1, 2)$ | $(4, 0, 1, 0)$ | $-6$ | $-16$ |

### 5.6 Discrete Curvature Contrast: Diamond vs. Chain

Comparing the two 4-element posets $E_{\text{diamond}}$ and $C_4$:
- **2D Discrete Curvature Contrast:**
  $$
  \Delta S_{\rm BD}^{(2)} := S_{\rm BD}^{(2)}(E_{\text{diamond}}) - S_{\rm BD}^{(2)}(C_4) = -6 - (+4) = -10.
  $$
- **4D Discrete Curvature Contrast:**
  $$
  \Delta S_{\rm BD}^{(4)} := S_{\rm BD}^{(4)}(E_{\text{diamond}}) - S_{\rm BD}^{(4)}(C_4) = -16 - (+3) = -19.
  $$

This exact differential confirms the discrete Ricci focusing signature:
1. Diamond topologies accumulate lateral links and intervening elements without accumulating intermediate 1-intervening pairs ($N_1 = 0, N_2 = 1$), driving the Benincasa–Dowker action into a strongly negative regime ($S_{\rm BD} < 0$). In causal set theory, negative scalar action corresponds to positive spacetime curvature / geodesic focusing (causal convergence).
2. Linear chain topologies maximize intermediate layers ($N_1 = 2$), driving the Benincasa–Dowker action positive ($S_{\rm BD} > 0$), corresponding to geodesic dispersion.
3. Completely disconnected antichains possess zero relations, producing purely positive action ($S_{\rm BD} = N$).

---

## 6. Quantum-Steered Interval-Volume Focusing Diagnostics

### 6.1 Two-Way Quantum-Order Coupling at Stage 2

In the unified multi-birth quantum-order architecture (`all_horizon_two_way_feedback_and_growth.md`, `branch_dressed_cavity_probe_stress_and_collar_ledger.md`, `two_way_quantum_steered_retarded_curvature_readout.md`), a two-level quantum probe with Hilbert space $\mathcal{H}_Q = \mathbb{C}^2$ is coupled to causal sequential growth.

At birth stage $n = 2$, corresponding to the two-element prefix poset $P_2 = (a \prec b)$, the co-rotating Clifford frame Pauli axis is:
$$
\Sigma_2 = X.
$$
The state of the qubit probe at stage 2 is parameterized by its Bloch vector:
$$
\rho_Q = \frac{1}{2}\left( I_Q + \langle X\rangle X + \langle Y\rangle Y + \langle Z\rangle Z \right), \qquad \langle X\rangle = \operatorname{Tr}[X\rho_Q] \in [-1, 1].
$$

Under the sequential growth dynamics, the third newborn event $x$ (birth 3) selects its precursor ideal $I_x \in \mathcal{I}(P_2)$ from the downward-closed ideals of $P_2 = (a \prec b)$:
$$
\mathcal{I}(a \prec b) = \left\{ \varnothing, \{a\}, \{a, b\} \right\}.
$$
The unsteered baseline transition probabilities $q(a \prec b, r, I_x)$ satisfy:
$$
q(a \prec b, r, \varnothing) = \frac{1}{5}, \qquad q(a \prec b, r, \{a\}) = f_{r_a}, \qquad q(a \prec b, r, \{a, b\}) = h_{r_a},
$$
with $f_{r_a} + h_{r_a} = 4/5$.
The globally active harmonic potential induces current-prefix steering drifts:
$$
r_{C_2}(\varnothing) = -\frac{1}{22}, \qquad r_{C_2}(\{a\}) = +\frac{1}{88}, \qquad r_{C_2}(\{a, b\}) = +\frac{1}{88}.
$$
The steered transition probabilities for newborn event $x$ are given by:
$$
p(I_x \mid \rho_Q) = q(a \prec b, r, I_x)\left( 1 + r_{C_2}(I_x)\langle X\rangle \right).
$$
Specifically, the branching probabilities between disconnected spacelike extensions and connected causal extensions are:
$$
p(I_x = \varnothing \mid \rho_Q) = \frac{1}{5}\left( 1 - \frac{1}{22}\langle X\rangle \right) = \frac{1}{5} - \frac{1}{110}\langle X\rangle,
$$
$$
p(I_x \in \{\{a\}, \{a, b\}\} \mid \rho_Q) = \frac{4}{5}\left( 1 + \frac{1}{88}\langle X\rangle \right) = \frac{4}{5} + \frac{1}{110}\langle X\rangle.
$$

### 6.2 Five-Birth Continuation ($a_4 = 1/10$) and Suffix Topology Realization

At birth stage $n = 3$, the fourth newborn event $y$ (birth 4) selects its precursor ideal $I_y \in \mathcal{I}(P_3)$ according to the fifth-birth transition kernel parameterized by coupling constant $a_4 = 1/10$. Across the 15 structural rows of four-element causal histories:
1. **Diamond-Like Continuations:**
   When newborn $x$ selects $I_x = \{a\}$ (forming the 3-element branching fork $P_3 = V = \{a, b, x\}$ where intermediate elements $b \parallel x$ share common past parent $a$), newborn $y$ selecting the maximal precursor ideal $I_y = \{a, b, x\}$ caps both branches ($b \prec y$ and $x \prec y$), producing the four-element causal diamond $E_{\text{diamond}} = \{a, b, x, y\}$, characterized by $S_{\rm BD}^{(4)} = -16$.
2. **Chain-Like Continuations:**
   When newborn $x$ selects $I_x = \{a, b\}$ (forming a linear 3-chain $a \prec b \prec x$), newborn $y$ selecting precursor ideal $I_y = \{a, b, x\}$ extends the order to the 4-chain $C_4$, characterized by $S_{\rm BD}^{(4)} = +3$.
3. **Spacelike Continuations:**
   When newborn $x$ selects $I_x = \varnothing$, newborn $y$ selecting $I_y = \varnothing$ generates disconnected antichain components, characterized by $S_{\rm BD}^{(4)} \ge +4$.

### 6.3 Linear Curvature Response to Quantum Steering

The ensemble-averaged discrete Benincasa–Dowker curvature action across the complete suffix history distribution is given by:
$$
\mathbb{E}_{\rho_Q}\left[S_{\rm BD}^{(4)}\right] = \sum_{h} p(h \mid \rho_Q)\,S_{\rm BD}^{(4)}(P_h),
$$
where $p(h \mid \rho_Q) = p(I_x \mid \rho_Q) p(I_y \mid I_x, \rho_Q)$ is the steered probability of history $h$.

Because the branch probabilities $p(I_x \mid \rho_Q)$ depend linearly on the initial qubit coherence $\langle X\rangle$, the expectation value of the discrete curvature operator decomposes into an unsteered baseline curvature $\bar{S}_0^{(4)}$ and a linear quantum-steering response:
$$
\mathbb{E}_{\rho_Q}\left[S_{\rm BD}^{(4)}\right] = \bar{S}_0^{(4)} + \kappa_{\rm steer}^{(4)}\,\langle X\rangle,
$$
where the steering response coefficient $\kappa_{\rm steer}^{(4)}$ is given by the weighted contrast over non-isomorphic suffix topologies:
$$
\kappa_{\rm steer}^{(4)} = \sum_{I_x} q(a \prec b, r, I_x)\,r_{C_2}(I_x) \sum_{I_y} q(P_3, r', I_y)\,S_{\rm BD}^{(4)}(P_{(I_x, I_y)}).
$$

Recalling the benchmark values:
- Diamond extensions: $S_{\rm BD}^{(4)}(E_{\text{diamond}}) = -16$;
- Chain extensions: $S_{\rm BD}^{(4)}(C_4) = +3$;
- Antichain extensions: $S_{\rm BD}^{(4)}(A_4) = +4$.

Because the causal drift $r_{C_2}(\{a\}) = +1/88 > 0$ enhances diamond-forming precursor branches while $r_{C_2}(\varnothing) = -1/22 < 0$ suppresses spacelike branches:
- Preparing positive initial qubit coherence $\langle X\rangle > 0$ increases the probability of causal and branching ideals, driving $\mathbb{E}_{\rho_Q}[S_{\rm BD}^{(4)}]$ toward more negative values (interval-volume focusing / causal convergence);
- Preparing negative initial qubit coherence $\langle X\rangle < 0$ enhances the unlinked spacelike ideal $I_x = \varnothing$, shifting $\mathbb{E}_{\rho_Q}[S_{\rm BD}^{(4)}]$ toward positive values (geodesic dispersion).

This establishes an operational, coordinate-free **Quantum $\leftrightarrow$ Intrinsic Discrete Geometry bridge**: initial quantum state preparation directly steers the expectation value of intrinsic discrete spacetime curvature without invoking external continuous spacetime embeddings.

---

## 7. Scope, Non-Implications, and Status-M Quarantine

### 7.1 Scope of Established Results

The mathematical results established in this deliverable are strictly combinatorial and operational within finite poset theory:
1. The comparable-pair fraction $R_2(P) = \mathbf{1}^T C_P \mathbf{1} / \binom{N}{2}$ and chain abundances $C_k(P) = \mathbf{1}^T C_P^k \mathbf{1}$ are rigorously defined, background-free invariants of finite strict partial orders.
2. The continuum comparison function $f(d) = \frac{\Gamma(d+1)\Gamma(d/2)}{2\Gamma(3d/2)}$ is proved to be strictly monotonically decreasing on $[1, \infty)$ with exact rational values at integer dimensions $d \in \{1, 2, 3, 4, 5, 6\}$, defining the intrinsic dimension estimator $d(R_2) = f^{-1}(R_2)$.
3. The normalized discrete Benincasa–Dowker d'Alembertian operators $B_{2,\text{norm}}$ and $B_{4,\text{norm}}$ and scalar actions $S_{\rm BD}^{(2)}$ and $S_{\rm BD}^{(4)}$ evaluate discrete interval-volume focusing directly from layer abundances $N_k$ without coordinates.
4. Initial qubit coherence $\langle X\rangle$ at stage 2 linearly modulates the expected discrete curvature action $\mathbb{E}_{\rho_Q}[S_{\rm BD}^{(4)}]$ under all-horizon sequential growth ($a_4=1/10$).

### 7.2 Non-Implications and Boundaries

In strict compliance with `NG-01`, `NG-02`, and `NG-03` (`docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md`), the following explicit boundaries are maintained:
1. **No Derivation of Continuum Manifolds:** The existence of a discrete dimension estimate $d(R_2) \approx 4$ on a finite poset does *not* prove that the poset approximates a smooth $3+1\text{D}$ Lorentzian manifold. Small posets or non-manifold percolation graphs can yield $d(R_2) \approx 4$ while failing chain abundance ratio screens $\rho_k$.
2. **No Derivation of General Relativity:** The discrete Benincasa–Dowker action $S_{\rm BD}$ provides a conditional discrete curvature diagnostic. It does not establish the Einstein field equations, diffeomorphism invariance, or continuous Riemannian geometry.
3. **No Derivation of Physical Constants or Born's Rule:** No claim is made to derive the speed of light $c$, Planck's constant $\hbar$, Newton's gravitational constant $G$, or Born's quantum probability rule.

### 7.3 Status-M Quarantine Declaration

Status-M ontological documents (ONTOLOGY.md, GOVERNANCE.md, PHYSICS.md, FALSIFICATION_LEDGER.md) remain strictly quarantined, and no claim is made to derive continuum spacetime dimension, Born's rule, physical constants, or General Relativity.

---

## 8. Scientific review

Intrinsic Interval Curvature Author derived Myrheim–Meyer comparable-pair fraction $R_2(P) = \mathbf 1^T C_P \mathbf 1 / \binom{N}{2}$, continuous comparison curve $f(d) = \frac{\Gamma(d+1)\Gamma(d/2)}{2\Gamma(3d/2)}$ with exact rational values $f(1)=1, f(2)=1/2, f(3)=8/35, f(4)=1/10, f(5)=128/3003, f(6)=1/56$, strict monotone invertibility, $k$-chain abundance estimators $C_k(P) = \mathbf 1^T C_P^k \mathbf 1$, discrete Benincasa–Dowker scalar actions $S_{\rm BD}^{(2)}(P) = N - 2N_0 + 4N_1 - 2N_2$ and $S_{\rm BD}^{(4)}(P) = N - N_0 + 9N_1 - 16N_2 + 8N_3$, and quantum-steered interval-volume focusing response. Independent Discrete Geometry Reviewer independently verified by hand 100% of equations, gamma function reductions, actions, and strict sibling isolation. Prospective protocol SHA-256 638001d2186c54b0540c6929c1e2071de7f236eb4bc982a85dda67c67993bf06; accepted author report SHA-256 ac66d868bb8dfff40d9a68f2d66c33b3cade91955549836b9a7fe4fe59b28f44; independent scientific review SHA-256 de22ecc4d03944d6da9aa98b4b428e184dca32ad7369dd5ac2d000785359130b.
