# Native cover mean ledger and operator reserve

**Accepted conditional finite result.** The accepted native-growth
and Gaussian attachment admit an exact additive cover-diagnostic ledger. A uniform
initial reserve of **2** keeps its fixed-Gaussian **mean** account nonnegative on
all 120 registered histories. The prospectively specified stronger same-space
operator completion fails for **every finite scalar reserve**, already at the
third birth. These are different mathematical demands; neither gives a native
physical energy or a source dynamics.

## Registered law and field resources

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

## 1. What is supplied and what is being tested

Retain both prepared prefixes a<b with marks (i,0), counters (1,0), conditional
mass one, and exactly two additional births. Every actual ideal and all four fair
suffix-mark pairs keep their original probabilities. Retain the accepted
chronological field map on three canonical pairs R=(Q0,P0,Qx,Px,Qy,Py), its common
Schwartz domain, and centered Gaussian covariance I6/2. Positive beta is factored
out, without a physical calibration.

Write $\phi_v=\sqrt\beta L_vR$ with coefficient row $L_v$, and use
coefficient columns $d_{uv}=(L_v-L_u)^T$ for cover differences. At each
registered stage $n=2,3,4$, use the same cover form

\[
\mathcal Q_n=\frac{1}{2\beta}\sum_{u\lessdot v}(\phi_v-\phi_u)^2
             =R^T H_n R,\qquad
H_n=\tfrac12\sum_{u\lessdot v}d_{uv}d_{uv}^T,
\quad d_{uv}=(L_v-L_u)^T.
\]

All statements of form positivity below are on the common Schwartz core.
Symmetric H gives the displayed sum of squares; no operator-order approximation
or commutator-kernel quotient is used. Its fixed-Gaussian mean is
$q_n=\omega(\mathcal Q_n)=\operatorname{tr}(H_n)/2$. The form is a supplied mathematical diagnostic, not a
Hamiltonian or a measured physical energy.

Two **chosen audit completions** were fixed prospectively:

1. A scalar mean reserve r_n=b−(q_n−q_2), requiring r_n≥0 at every registered
   prefix, with one uniform b≥0 for both preparations.
2. A same-space operator identity B_n+Q_n=b I+Q_2, with B_2=b I, requiring
   B_n≥0 on all normalized Schwartz states, for one finite scalar b.

The second is a deliberately stronger proposal. It is not inferred from the
first and is not asserted to encompass arbitrary reservoir constructions.

## 2. Exact birthwise balance identity

Let z be a new maximal vertex above ideal S. A new maximal vertex cannot become
an intermediate point of an old interval u<v: that would require z<v for an old
v. Every old cover therefore persists. The new covers are exactly (u,z) for the
maximal elements u of S. Indeed, a nonmaximal u has an intermediate point of S,
while any intermediate point between maximal u and z would itself lie in S.

The supplied attachment leaves all earlier field operators fixed. Consequently,
on every admitted branch,

\[
\Delta_n:=\mathcal Q_{n+1}-\mathcal Q_n
 =\frac{1}{2\beta}\sum_{u\in\operatorname{Max}(S)}(\phi_z-\phi_u)^2\ge0,
\]
\[
H_{n+1}-H_n=\tfrac12\sum_{u\in\operatorname{Max}(S)}d_{uz}d_{uz}^T,
\qquad q_{n+1}-q_n=\tfrac14\sum\|d_{uz}\|^2.
\]

Empty S gives zero increment. Every nonempty S has a maximal element; the new
field's unique new Q coefficient is one, so its cover difference is nonzero and
the stipulated Gaussian mean increment is strictly positive. Thus growth adds
diagnostic content, even though old observables and their state remain unchanged.
This is inclusion of new terms, not a dynamical energy flux derived from motion.

The accepted research computation verified the exact matrix identity, old-cover inclusion and
unchanged earlier L rows at both births for all 120 histories. It does not
replace the analytic positivity argument with floating-point eigenvalue tests.

## 3. Complete finite mean ledger

$q_2=1/2$ in every row. Here $\Delta_2=q_3-q_2$ and $\Delta_3=q_4-q_3$
denote mean increments in the table. The strings $ab,ax,abx$ denote ideals
as sets of the named vertices. Each structural row
represents four marked histories, each with one quarter of its listed structural
mass. All rows are retained. In particular, the root mark changes weights, not
the field coefficient or diagnostic value at a fixed ideal sequence.

| Ix | Iy | q3 | q4 | Delta2 | Delta3 | r4 at b=2 | P0 structural | P1 structural |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ∅ | ∅ | 1/2 | 1/2 | 0 | 0 | 2 | 1/220 | 1/220 |
| ∅ | a | 1/2 | 5/4 | 0 | 3/4 | 5/4 | 1/264 | 1/132 |
| ∅ | x | 1/2 | 5/4 | 0 | 3/4 | 5/4 | 1/220 | 1/220 |
| ∅ | ab | 1/2 | 1 | 0 | 1/2 | 3/2 | 19/1320 | 7/660 |
| ∅ | ax | 1/2 | 5/2 | 0 | 2 | 0 | 1/40 | 1/40 |
| ∅ | abx | 1/2 | 5/2 | 0 | 2 | 0 | 13/88 | 13/88 |
| a | ∅ | 5/4 | 5/4 | 3/4 | 0 | 5/4 | 1/264 | 1/132 |
| a | a | 5/4 | 2 | 3/4 | 3/4 | 1/2 | 1/264 | 1/132 |
| a | ab | 5/4 | 2 | 3/4 | 3/4 | 1/2 | 19/1320 | 7/660 |
| a | ax | 5/4 | 2 | 3/4 | 3/4 | 1/2 | 19/1320 | 7/660 |
| a | abx | 5/4 | 5/2 | 3/4 | 5/4 | 0 | 43/330 | 49/165 |
| ab | ∅ | 1 | 1 | 1/2 | 0 | 3/2 | 19/1320 | 7/660 |
| ab | a | 1 | 2 | 1/2 | 1 | 1/2 | 19/1320 | 7/660 |
| ab | ab | 1 | 3/2 | 1/2 | 1/2 | 1 | 19/1320 | 7/660 |
| ab | abx | 1 | 7/4 | 1/2 | 3/4 | 3/4 | 779/1320 | 287/660 |

Since q_n is nondecreasing along each branch and max q_4=5/2, the sharp uniform
mean reserve is

\[
b_* =\max_H(q_4(H)-q_2)=2.
\]

At b=2 the identity r_n+q_n=5/2 holds at every stage of every history, with
r_n≥0. Sharpness is witnessed, for example, by Ix=∅, Iy={a,x}: its structural
mass is 1/40 under either preparation, each marked mass is 1/160, and its mean
demand is exactly 2. The other attaining rows are (∅,abx) and (a,abx). No
postselection or restriction to these witnesses is made.

The exact ensemble means, using the original complete masses, are:

| Quantity | i=0 | i=1 |
| --- | --- | --- |
| E q2 | 1/2 | 1/2 |
| E q3 | 113/120 | 59/60 |
| E q4 | 937/480 | 2743/1320 |
| E Delta2 | 53/120 | 29/60 |
| E Delta3 | 97/96 | 289/264 |
| E(q4−q2) | 697/480 | 2083/1320 |
| E r4 at b=2 | 263/480 | 557/1320 |

The source-one minus source-zero terminal contrast is **133/1056**. It is a
conditional dimensionless diagnostic-response computation, not an energy
calibration. The minimal uniform reserve is the same for both source bits despite
the different mean draw. The underlying field-state schedule dependence remains.

## 4. Failure of the specified positive operator completion

Take the supported third-birth ideal $S=\{a\}$. Its structural probabilities
are $f_0=1/6$ and $f_1=1/3$, both positive, with probability $f_i/2$ for
each newborn mark. The accepted
field formula gives

\[
\Delta_2=\tfrac12(Q_x-P_0-Q_0)^2,
\qquad B_3=bI-\Delta_2.
\]

Use the normalized real Schwartz function

\[
\psi_t(q_0,q_x,q_y)=\pi^{-3/4}
\exp[-(q_0^2+(q_x-t)^2+q_y^2)/2].
\]

It shifts only ancillary Qx, leaving the prepared pair's state exactly unchanged.
The three contributing quadratures have centered squared sum mean 3/2, so

\[
\langle\Delta_2\rangle_t=\tfrac34+\tfrac12t^2,
\qquad \langle B_3\rangle_t=b-\tfrac34-\tfrac12t^2\longrightarrow-\infty.
\]

For every finite b≥0, taking t=sqrt(2b) gives expectation −3/4. At the sharp
mean budget b=2, the simple witness t=2 already gives −3/4. Thus **no finite
scalar reserve satisfies the prospectively specified all-state operator
positivity condition**. A positive operator/form cannot have such a negative
expectation on a normalized core state.

The witness is not a replacement preparation for the original 120-history law.
Those histories still use t=0 and the same fixed Gaussian. At b=2, that state's
B3 expectation is +5/4 on this branch. A nonnegative expectation in one state
does not make the observable positive. The supplied oscillator state and every
native probability remain unchanged in the implemented mean ledger.

This obstruction is limited to B_n+Q_n=bI+Q2 on the fixed common representation,
finite scalar B2 and positivity on all states. It proves nothing about arbitrary
correlated reservoirs, state-dependent initial energy operators, physical
transfer dynamics, cutoff models or changed attachments. Such alternatives need
explicit new premises and their own prospective question. No pointer outcome
law, spectral readout distribution or measurement model is derived here.

## 5. Whole-programme use and limits

The [radiation-loaded membrane energy result](radial_energy_of_a_radiation_loaded_membrane.md) supplies a useful **scope comparison**, not
a coefficient for this construction. Its positive quadratic is conserved because
the supplied acoustic and wall equations give opposite pressure-work rates,
−A0(q_wall/3)V and +A0(q_wall/3)V, with the full boundary accounting retained.
Here the mean reserve is defined by subtraction; no reservoir evolution,
coupling or equal-and-opposite physical work law is supplied. The [finite acoustic inertia result](finite_acoustic_inertia_and_energy_ledger.md) likewise
retains its own causal fluid, actuator and boundary ledger. Neither conventional
model's geometry, clocks, material or dimensional coefficients are transplanted.

The actionable consequence for the native matter/source programme is precise:
the cover diagnostic can be recorded with an exact source-conditioned **mean
demand**. Calling the resulting subtraction ledger a positive closed reservoir
requires additional structure; the specified finite-scalar operator completion
is ruled out. This separates a usable accounting interface from an unjustified
conservation claim.

The [accepted endpoint field-state covariance failure](native_field_state_across_a_causal_diamond.md) remains demonstrated
by the earlier u/v swap. Its agreeing mean 2 does not imply equality of full
records. The [complete pointer-law comparison](complete_pointer_laws_on_native_histories.md) is a separate accepted result and was not an input to this mean-ledger proof. Scheduler order
is never a physical global present. Option B / Status M remain unchanged.

Physical energy/stress, persistence, source coupling, clocks, units, conservation
from actual exchange equations, larger-size or continuum models and observations
remain unestablished. No pointer instrument or spectral outcome distribution is
derived by the mean ledger or its operator-positivity test.

## Scientific provenance and evidence level

DET Provisional Integrated Model authored PIM002. DET Relational State Research completed the distinct
nonblind scientific review; the coordinator accepted the result with scope on
16 November 2026. This article reuses that accepted proof and validation. Publication
assembly does not rerun the model or constitute another scientific review.

The distinct reviewer rebuilt all 120 history records with exact arithmetic from
the accepted transition and field formulas, matching all 15 structural rows,
matrices, probabilities and reserves. The five declared test groups passed without
skips, and the existing probe reproduced the frozen 588,810-byte result exactly,
SHA-256 `84616c5c51744c45ad78fefd7a9616985d23c9858aa30e1f5e5363a221892c1f`.
The analytic cover argument establishes positivity, and the normalized displaced
Gaussian establishes the restricted operator obstruction; neither conclusion is
inferred from a numerical eigenvalue check.

The exact source identities are recorded here without treating private archive
locations as public reproduction links:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| PIM002 accepted author report | 12,201 | `2dab2e10a47319b2145a83e0d2c8eb608a6d0f53c0e72ac84ffdc22ae1590cc2` |
| PIM002 distinct scientific review | 9,594 | `a5611c29084f4e8c9c57bf26630708bdd819938d1844342a77a5d795558b3a5e` |

Runs were verified in the accepted scientific record. Reproduction means exact
mathematical fixtures and accepted component checks. The result is conditional
mathematics under the stated supplied choices; it adds no ontology derivation
of the growth law or canonical resources. Agreement with observations is
**NOT TESTED**: no empirical dataset, calibration or holdout was used. This
publication adds no executable for PIM002; the linked public PIM001 package has
its own narrower scope. Option B and Status M remain unchanged.
