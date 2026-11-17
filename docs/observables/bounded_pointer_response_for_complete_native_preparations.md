# Bounded pointer response for complete native preparations

**Accepted conditional finite result.** Appending the same
accepted terminal pointer instrument to both complete native preparations gives
two normalized, unselected record laws. For the prospectively fixed statistic
g(X)=sin(X/128), the source-one-minus-source-zero expectation contrast satisfies

\[
\boxed{\quad
\frac{2645093527}{2834678415360}
\ \leq\ \mathbb E_1g(X)-\mathbb E_0g(X)
\ \leq\ \frac{977776931}{944892805120}.
\quad}
\]

The interval is approximately [0.000933119437, 0.001034801965] and is strictly
positive. Every one of the 60 marked histories in each preparation, and every
real pointer outcome, is retained. This is a rigorous bound on one mathematical
expectation contrast, not its exact value, a per-trial source classifier or an
empirical discrimination claim.

## 1. Registered preparations and supplied field

The [prepared native law](native_source_readout_response.md) starts at
$a\prec b$ with immutable marks $(i,0)$, counters $(1,0)$ and conditional mass
one, for $i=0,1$. A birth adds a new maximal vertex above its actual downward-closed
ideal. Exactly two births, $x,y$, are retained. The 15 structural ideal sequences
each carry all four fair suffix-mark pairs: 60 marked histories per preparation,
120 in total. Each marked weight is one quarter of its structural weight. No
isomorphic endpoints are merged, no history is removed and no earlier preparation
probability is multiplied in. Counter updates and field variables do not feed back
into the native law. Birth count and scheduling are not physical time.

The [Gaussian attachment](gaussian_field_transport_on_native_histories.md) uses
$R=(Q_0,P_0,Q_x,P_x,Q_y,P_y)^T$ on $L^2(\mathbb R^3)$ with common Schwartz core,
$[R_j,R_k]=iJ_{jk}$ and $J=\operatorname{diag}(J_2,J_2,J_2)$,
$J_2=\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)$.
The normalized vector
$\psi(q)=\pi^{-3/4}\exp[-(q_0^2+q_x^2+q_y^2)/2]$ has zero means,
symmetric covariance $I_6/2$ and ordered second moments $(I_6+iJ)/2$.
For $c_{rs}=\mathbf1_{\{s\prec r\}}$, the fixed chronological fields are
\[
\phi_a/\sqrt\beta=Q_0,\qquad \phi_b/\sqrt\beta=-P_0,
\]
\[
\phi_x/\sqrt\beta=Q_x-c_{xb}Q_0-c_{xa}P_0,
\qquad
\phi_y/\sqrt\beta=Q_y-c_{yb}Q_0-c_{ya}P_0-\rho P_x,
\]
\[
\rho=c_{yx}-c_{yb}c_{xa}+c_{ya}c_{xb}.
\]
Older rows are retained as the same operators. The canonical resources, Gaussian,
field assignment and $\beta>0$ are supplied mathematical premises. Factoring out
$\beta$ gives the chosen dimensionless normalization, not a native physical unit.
The [PIM001 baseline](../../research/provisional_integrated_model/PIM001/README.md)
implements these accepted finite ingredients; its known-answer reproduction is
separate from the result below.

The [accepted terminal pointer construction](complete_pointer_laws_on_native_histories.md)
supplies the finite-cover Friedrichs realization, spectral interaction and normalized
Gaussian-convolution kernel. The [mean ledger](native_cover_mean_ledger_and_operator_reserve.md)
supplies inherited mean anchors, not a positive reservoir or a detector calibration.
The oscillator-flow result is not an input to this calculation. The present
question concerns both complete source preparations with histories unread;
the earlier named-history pointer comparison concerned two histories at one endpoint.

The frequency $1/128$ was fixed in the prospective PIM004 control at
2026-11-17 00:01:07.774696 UTC, before the new moment calculation. It is a declared
mathematical choice informed by accepted mean results, not an empirical holdout,
fitted parameter or frequency optimized after computation.

The complete structural weights below make the mixture explicit. The notation
$ab,ax,abx$ denotes the corresponding ideal as a set. Each row represents all
four suffix-mark pairs, individually weighted by one quarter of the listed mass.

| $I_x$ | $I_y$ | $P_0$ structural | $P_1$ structural |
| --- | --- | ---: | ---: |
| ∅ | ∅ | 1/220 | 1/220 |
| ∅ | a | 1/264 | 1/132 |
| ∅ | x | 1/220 | 1/220 |
| ∅ | ab | 19/1320 | 7/660 |
| ∅ | ax | 1/40 | 1/40 |
| ∅ | abx | 13/88 | 13/88 |
| a | ∅ | 1/264 | 1/132 |
| a | a | 1/264 | 1/132 |
| a | ab | 19/1320 | 7/660 |
| a | ax | 19/1320 | 7/660 |
| a | abx | 43/330 | 49/165 |
| ab | ∅ | 19/1320 | 7/660 |
| ab | a | 19/1320 | 7/660 |
| ab | ab | 19/1320 | 7/660 |
| ab | abx | 779/1320 | 287/660 |

## 2. Complete probability interface

Use the two registered prefixes a<b, marks (i,0), counters (1,0), with i=0,1.
Retain their original conditional probabilities P_i(H), exactly two additional
births, all actual ideals and all four suffix-mark pairs. Every P_i(H) is positive
and each complete sum is one. Distinct histories are not merged merely because
their endpoints are isomorphic.

For each terminal history H, let d_e=(phi_v−phi_u)/sqrt(beta) be its actual cover
differences. Keep the specified dimensionless form and its accepted realization

\[
Q_H=\tfrac12\sum_{e\in\mathrm{covers}(H)}d_e^2\geq0,
\qquad \nu_H(B)=\langle\psi,E_{Q_H}(B)\psi\rangle.
\]

The canonical field state has symmetric quadrature covariance I6/2. Beta>0
cancels from this fixed diagnostic; no physical unit is thereby determined.
The accepted form argument works for every finite cover list, so nu_H is a
normalized spectral measure on [0,infinity), with all Gaussian moments used
below finite.

Keep the independent pointer g(x)=pi^(−1/4)exp(−x²/2), its variance 1/2, unit
coupling exp(−i Q_H tensor Pp) defined by the joint spectral calculus, and complete
position PVM. The normalized kernel is

\[
\mu_H(dx)=\left[\int_{[0,\infty)}
 \pi^{-1/2}e^{-(x-\lambda)^2}\,\nu_H(d\lambda)\right]dx.
\]

The same kernel rule is used for both prepared bits. At fixed ideal sequence,
the field coefficients and instrument do not depend on either the source bit or
suffix marks; the source bit changes the native history weights. Therefore

\[
\Pr_i(H,dx)=P_i(H)\mu_H(dx),\qquad
M_i(dx)=\sum_H P_i(H)\mu_H(dx).
\]

Each summand is a nonnegative measure. Tonelli and the normalized Gaussian and
spectral measure give mu_H(R)=1. Hence Pr_i(H,R)=P_i(H) and M_i(R)=1. This is
the full-measure normalization argument; verifying moment zero alone would not
prove positivity or define a probability law.

Negative readings, tails and all histories remain in M_i. The observer's statistic
uses only recorded X, without a history label or endpoint selection. No coupling,
support, probability or native growth update is modified. No claim is made that
the field state is preserved after its interaction with the pointer.

The complete measures are specified mathematically by this spectral convolution
and mixture. The accepted research computation gives exact moments and the certificate;
it is not a sampler, a numerical density implementation or a claim that four
moments determine an arbitrary probability law.

## 3. Exact moments without classicalizing the cover fields

Let A contain the real cover coefficient rows, so d=AR. Define

\[
W_{rs}=\omega(d_r d_s)
       =\tfrac12(G_{rs}+iK_{rs}),\qquad
G=AA^T,\quad K=AJA^T.
\]

These are **ordered** second moments. Noncommuting cover fields cannot be assigned
simultaneous classical Gaussian values with covariance G/2. That substitution
would lose K and give wrong higher moments.

For a centered canonical Gaussian, the expectation of an even ordered word is
the sum over pairings of ordered contractions. One direct derivation expands the
Gaussian expectation of an ordered product of linear-field exponentials: its
quadratic exponent contains W_rs for r preceding s; differentiating once in each
formal parameter gives all pairings. Equivalently, repeatedly commute annihilation
operators to the vacuum. The recurrence pairs the first factor with every later
factor, deletes that pair and preserves the order of the remaining word. There
is no fermionic sign.

Expand

\[
\omega(Q_H^k)=2^{-k}\sum_{e_1,\ldots,e_k}
\omega(d_{e_1}d_{e_1}\cdots d_{e_k}d_{e_k}),\qquad 0\leq k\leq4.
\]

All ordered cover-index tuples are included. The accepted computation represents
2W=G+iK as pairs of exact integers. Each k-th moment has k contraction factors
1/2 and k quadratic factors 1/2, so the final denominator is 4^k before reduction.
It checks that every imaginary sum cancels exactly. There are no floating-point
trigonometric, matrix or oscillator-cutoff errors.

The accepted spectral convolution is equivalent for its scalar record law to
X=Lambda+Z, where Lambda has nu_H and Z is an independent real Gaussian of
variance 1/2. This representation concerns the single measured Q_H spectrum and
pointer noise, not simultaneous classical values of its noncommuting components.
Thus, writing q_k=E Lambda^k,

\[
x_1=q_1,\quad x_2=q_2+\tfrac12,\quad
x_3=q_3+\tfrac32q_1,\quad
x_4=q_4+3q_2+\tfrac34.
\]

Original history weights then give the unselected mixture moments by finite
summation. Mark-independent values may be cached, but the accepted result archive explicitly retains all 120 marked records
and their individual probabilities.

For audit, the complete structural-row Q moments needed beyond the mean are:

| Ix | Iy | E Q² | E Q³ | E Q⁴ |
| --- | --- | --- | --- | --- |
| ∅ | ∅ | 3/4 | 15/8 | 105/16 |
| ∅ | x | 51/16 | 795/64 | 16809/256 |
| ∅ | a | 67/16 | 1515/64 | 48201/256 |
| ∅ | ab | 2 | 7 | 35 |
| ∅ | ax | 14 | 531/4 | 7131/4 |
| ∅ | abx | 57/4 | 1111/8 | 30681/16 |
| a | ∅ | 67/16 | 1515/64 | 48201/256 |
| a | a | 39/4 | 321/4 | 14937/16 |
| a | ab | 8 | 209/4 | 959/2 |
| a | ax | 31/4 | 189/4 | 6341/16 |
| a | abx | 45/4 | 645/8 | 12817/16 |
| ab | ∅ | 2 | 7 | 35 |
| ab | a | 33/4 | 229/4 | 9025/16 |
| ab | ab | 4 | 73/4 | 481/4 |
| ab | abx | 83/16 | 1545/64 | 39561/256 |

These values apply to each of the four suffix marks and to either source bit at
the same ideal sequence. The probabilities remain different where the original
law prescribes. The complete weighted moments are:

| Moment | Source i=0 | Source i=1 |
| --- | --- | --- |
| E Q = E X | 937/480 | 2743/1320 |
| E Q² | 31805/4224 | 9025/1056 |
| E Q³ | 1460249/28160 | 431631/7040 |
| E Q⁴ | 186592627/337920 | 27898609/42240 |
| E X² | 33917/4224 | 9553/1056 |
| E X³ | 308541/5632 | 90715/1408 |
| E X⁴ | 194479267/337920 | 29013289/42240 |

The first row and its difference 133/1056 reproduce the accepted PIM002 mean
ledger. They are inherited checks, not a newly discovered mean response.

## 4. Certificate for the one prescribed bounded statistic

Put t=1/128 and delta_m=E_1 X−E_0 X=133/1056. The global Taylor remainder and
an elementary pointwise inequality give

\[
|\sin(tx)-tx|\leq\frac{t^3|x|^3}{6},\qquad
|x|^3\leq\frac{x^2+x^4}{2},
\]

because (x²+x⁴)/2−|x|³=x²(|x|−1)²/2≥0. Finite fourth moments justify the
expectations. Applying the two inequalities separately under the complete M0
and M1 laws yields

\[
\left|\{\mathbb E_1\sin(tX)-\mathbb E_0\sin(tX)\}-t\delta_m\right|
\leq R,
\quad
R=\frac{t^3}{12}\sum_{i=0}^1(\mathbb E_iX^2+\mathbb E_iX^4).
\]

The exact quantities are

\[
t\delta_m=\frac{133}{135168},\qquad
\sum_i(\mathbb E_iX^2+\mathbb E_iX^4)=\frac{144118633}{112640},
\]
\[
R=\frac{144118633}{2834678415360}.
\]

Subtracting and adding R gives the boxed positive interval at the beginning of
this article. This proves M0 and M1 differ and that the declared initial source
record affects a bounded terminal record under the supplied complete instrument.
It does not assert a deterministic identification of the source from one trial,
estimate experimental detection rates, or give a sampling-cost guarantee.
No exact sine expectation, density curve or global characteristic-function branch
was evaluated; none is required for this finite certificate.

## Mathematical fixtures and limits

The commuting one-cover Gaussian and the canonical oscillator vacuum are
independent normalization fixtures; the latter has $Q$ moments $2^{-k}$ and detects
the incorrect replacement of the ordered contraction by its real part. Taylor
expansion of the accepted two named-history Laplace laws gives moment vectors
$(1,2,8,209/4,959/2)$ and $(1,2,33/4,229/4,9025/16)$, including moment zero.
These match the corresponding structural rows above.

An independent creation/annihilation method supplies another exact check. For
$d=u\cdot Q+v\cdot P$, write
\[
\sqrt2\,d=\sum_j[(u_j+iv_j)z_j+(u_j-iv_j)\partial_{z_j}].
\]
Apply $Q=\tfrac14\sum_e(\sqrt2\,d_e)^2$ repeatedly to polynomial $1$; its constant
coefficient is the vacuum expectation. Retaining the complete polynomial through
degree eight reproduces the fourth moments without an oscillator cutoff. This
method is independent of the ordered Wick recurrence used for the reported table.

The full laws are defined by the positive spectral convolution and finite mixture.
Four moments alone do not determine an arbitrary probability measure. No exact
sine expectation, numerical density, sampler, global characteristic-function
branch computation or empirical discrimination was obtained here. The strictly
positive interval proves a difference of complete laws and one bounded expectation
response; it does not identify the source deterministically from one trial or give
a sampling-cost guarantee.

Canonical Gaussian resources, pointer access, unit coupling and normalization
remain supplied. The initial source bit is not identified with energy, and no
physical detector, energy/stress, conservation, clock, gravitational coupling,
native-unit calibration, all-size or continuum result follows. The
[endpoint field-state covariance failure](native_field_state_across_a_causal_diamond.md)
and the [named pointer-law inequality](complete_pointer_laws_on_native_histories.md)
remain unchanged. This result repairs neither and gives no universal readout
obstruction or minimal-register theorem. No physical coefficients from the
separate classical fluid models are transplanted.

## Scientific provenance and evidence level

DET Provisional Integrated Model authored PIM004. DET Energy Research completed the distinct
nonblind scientific review; the coordinator accepted the result with scope on
17 November 2026 (UTC). This article reuses that accepted proof and validation. Publication
assembly does not rerun the model or constitute another scientific review.

The distinct review independently reconstructed all 15 structural moment rows
through fourth order using exact creation/annihilation polynomial arithmetic,
matched every one of the 120 marked records and both full mixture vectors,
and reproduced the rational certificate. It also matched all original masses,
terminal quadratic matrices and inherited means against the accepted PIM002
record. Seven declared test groups passed without skips. The existing CLI output
was byte-identical to the frozen 95,744-byte result, SHA-256
`17966d2b9ac14150da7ab84de09918bc23174cffbd55e8708d8b9f4d6f7748ef`.
The checks retained all histories and all real outcomes, with no retuning,
frequency search, extra case or new normalization over a selected subset.

The exact source identities are recorded here without treating private archive
locations as public reproduction links:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| PIM004 accepted author report | 14,344 | `703aad123a4760e5bd0e2d4776b1b0191abc0a551ca6ea4155eab33c556aeda8` |
| PIM004 distinct scientific review | 13,644 | `30f5956ff59aa956b1dad9b18436fa492ce5f0c39c64dff8ff6401bf6141cf15` |

Runs were verified in the accepted scientific record. Reproduction means exact
mathematical fixtures and accepted component checks. The result is conditional
mathematics under the stated supplied choices; it adds no ontology derivation
of the growth law or canonical resources. Agreement with observations is
**NOT TESTED**: no empirical dataset, calibration or holdout was used. This
publication adds no executable for PIM004; the linked public PIM001 package has
its own narrower scope. Option B and Status M remain unchanged.
