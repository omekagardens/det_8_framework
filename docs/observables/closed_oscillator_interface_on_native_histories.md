# Closed oscillator interface on native histories

**Accepted conditional finite result.** The accepted retained
fields close as a first-order real linear Heisenberg system at stage two. At
stages three and four they do not. Adding **one observable Px** at stage three,
and **two observables Px, Py** at stage four, gives a closed system. These counts
are minimal in the registered canonical representation, for every supported
history. The resulting explicit equations preserve the commutator and the supplied
Gaussian covariance and are compatible with birth inclusion under one common
ambient flow.

## Registered inputs

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

## 1. Fixed premises and the meaning of closure

Keep accepted PIM001's two preparations, all 120 terminal marked histories and
their registered stages, original growth probabilities, immutable records,
counters, chronological field coefficients and common Gaussian. Reserve the
same three canonical pairs, R=(Q0,P0,Qx,Px,Qy,Py), with [Rj,Rk]=iJjk and
J=diag(J2,J2,J2), J2=[[0,1],[-1,0]]. No new birth or vertex is added by the
companion observables below.

The additional supplied choice is

\[
K_0=\tfrac12\sum_{j=0,x,y}(Q_j^2+P_j^2),\qquad
\frac{dR}{d\tau}=i[K_0,R]=JR.
\]

Use the standard oscillator realization on L2(R3): the Hermite product basis
diagonalizes its self-adjoint closure with eigenvalues n0+nx+ny+3/2. The unitary
flow is well defined and preserves the common Schwartz domain used for the
linear fields. The supplied Gaussian is its ground state. Neither this generator
nor dimensionless tau is derived from DET ontology or calibrated as physical
energy or time. Tau is independent of birth count and never identifies a
physical global present.

Write f=phi/sqrt(beta)=LR. The question is specifically whether a real matrix A
satisfies LJ=AL, so the existing finite field list alone obeys df/dtau=Af.
This is first-order **real linear observable closure**, not an unrestricted
operator-algebra classification or a claim about physical observation resources.
The underlying Hilbert space remains infinite dimensional.

The original fields always have the global evolution L exp(tau J)R. They also
obey the second-order equation f''=−f. Neither fact supplies their omitted
first-derivative initial data, so neither contradicts failure of a closed
first-order system using only f.

## 2. Analytic closure and minimality proof

For any real row space S, first-order closure means SJ is contained in S. Since
J²=−I, the space S+SJ is J-invariant. Every J-invariant extension of S contains
SJ, so S+SJ is the unique smallest such space. The required number of independent
added real linear observables is therefore dim(S+SJ)−dim(S).

Coefficient equality is genuine operator equality here: a nonzero real row r
gives a field rR with Gaussian variance ||r||²/2>0. There is no kernel-as-zero
quotient that could discard a required canonical direction.

Let

\[
\alpha=c_{xa},\quad b=c_{xb},\quad
\gamma=c_{ya},\quad d=c_{yb},\quad e=c_{yx},\qquad
\rho=e-d\alpha+\gamma b.
\]

The normalized accepted fields are

\[
f_a=Q_0,\quad f_b=-P_0,\quad
f_x=Q_x-bQ_0-\alpha P_0,\quad
f_y=Q_y-dQ_0-\gamma P_0-\rho P_x.
\]

At stage two, S2 spans Q0,P0 and is already invariant. At stage three, S3 spans
Q0,P0,Qx. Closure forces Px, and these four canonical directions suffice.
At stage four, S4 spans Q0,P0,Qx,Qy−rho Px. Its closure first contains Px because
it contains Qx, then Qy, and then Py. It is the entire six-dimensional canonical
coefficient space. These arguments hold for every admitted bit pattern,
including rho=0; no exceptional ideal or suffix mark is excluded.

The original stage-three and stage-four fields are linearly independent: unique
Qy and Qx coefficients remove the suffix rows in any vanishing combination,
then Q0 and P0 remove the prefix rows. The proposed Px and Py are independent
modulo S4 by the same unique-coefficient argument. Thus the minimal counts are:

| Stage | Retained span | Smallest invariant span | Extra observables |
| --- | ---: | ---: | --- |
| 2 | 2 | 2 | none |
| 3 | 3 | 4 | Px |
| 4 | 4 | 6 | Px, Py |

There is also a direct closure obstruction: df_x/dtau=Px+alpha f_a+b f_b.
Px lies outside both S3 and S4. At stage four, for example, a coefficient-space
displacement (0,0,0,1,rho,0) annihilates every retained row L but gives value 1
for the x row of LJ. No combination of the retained fields can reproduce that
derivative. The accepted tests checked this witness for every registered history without
calling a rank algorithm.

These are minimal **counts within this linear representation and generator**.
The particular added basis is convenient, not unique. No claim of minimal memory,
energy, apparatus, native degrees of freedom or other possible generators follows.

## 3. Explicit completed equations and decoder

Use

\[
Z_2=(f_a,f_b)^T,\quad Z_3=(f_a,f_b,f_x,P_x)^T,\quad
Z_4=(f_a,f_b,f_x,f_y,P_x,P_y)^T.
\]

At every applicable stage,

\[
\dot f_a=-f_b,\qquad \dot f_b=f_a,
\]
\[
\dot f_x=\alpha f_a+b f_b+P_x,\qquad
\dot P_x=-b f_a+\alpha f_b-f_x.
\]

At stage four add

\[
\dot f_y=(\gamma+\rho b)f_a+(d-\rho\alpha)f_b+\rho f_x+P_y,
\]
\[
\dot P_y=-d f_a+\gamma f_b-f_y-\rho P_x.
\]

These define the matrices A2, A3 and A4 explicitly. In the displayed Z4 order,

\[
A_4=\begin{pmatrix}
0&-1&0&0&0&0\\
1&0&0&0&0&0\\
\alpha&b&0&0&1&0\\
\gamma+\rho b&d-\rho\alpha&\rho&0&0&1\\
-b&\alpha&-1&0&0&0\\
-d&\gamma&0&-1&-\rho&0
\end{pmatrix}.
\]

For a transparent inverse interface, decode the active canonical coordinates as

\[
Q_0=f_a,\quad P_0=-f_b,\quad
Q_x=f_x+b f_a-\alpha f_b,\quad P_x=P_x,
\]
\[
Q_y=f_y+d f_a-\gamma f_b+\rho P_x,\quad P_y=P_y.
\]

At stage two use only the first pair; at stage three use the first two pairs.
Let Z=BR, where B contains the retained field rows followed by the selected
canonical momentum rows. Let D be the decoder, with unused canonical rows zero.
Then BD=I, DB is the projector onto the active pairs, and the explicit equations
satisfy AB=BJ. Since B has independent rows and the active pairs form a
J-invariant space, A²=−I. Therefore the complete finite solution is

\[
Z(\tau)=T(\tau)Z(0),\qquad
T(\tau)=I\cos\tau+A\sin\tau,\qquad T(\tau)B=B E(\tau),
\]
\[
E(\tau)=I_6\cos\tau+J\sin\tau.
\]

A is generally not Euclidean-antisymmetric in these noncanonical coordinates.
Its exact covariance metric, rather than an assumed Euclidean norm, is preserved.

## 4. State preservation and compatibility across a birth

E(tau) is both orthogonal and symplectic. Thus

\[
E E^T=I,\quad E J E^T=J,\quad
E(I+iJ)E^T=I+iJ.
\]

For normalized completed variables, the commutator matrix and symmetric
covariance are Omega=BJB^T and V=BB^T/2. Their ordered second moment is
W=V+i Omega/2. The completed flow preserves all three:

\[
A V+V A^T=0,\qquad A\Omega+\Omega A^T=0,
\quad T V T^T=V,\quad T\Omega T^T=\Omega.
\]

The full centered Gaussian Weyl state is stationary, because its real quadratic
form and commutator phase are unchanged; alternatively the ambient Gaussian is
an eigenstate of K0. Multiplying field rows back by sqrt(beta) restores the
original field normalization and target-first causal commutator. Additional
momentum observables are not assigned new causal-set vertex labels.

To compare a parent and child completed system, select the old coordinates from
the new vector. The stage-two-to-three selector picks coordinates (1,2), and the
stage-three-to-four selector picks (1,2,3,5), in one-based indexing. Calling it P,

\[
B_{old}=P B_{new},\qquad P A_{new}=A_{old}P,
\qquad P T_{new}(\tau)=T_{old}(\tau)P.
\]

Old coefficient rows, commutators, covariances and the entire old Gaussian state
therefore persist under birth inclusion and common evolution.

The identification is essential: a birth at parameter tau uses the new
coefficient rows against the same ambient R(tau), including the pairs reserved
before birth. It does not reset the new pair or start an independent “age since
birth” clock. Under this chosen convention, constructing the extended field list
and applying the same ambient flow commute as linear observable maps. Original
q and the fair marks do not depend on tau or the fields. No waiting-time law,
continuous-time stochastic growth generator, state-transfer channel or physical
birth dynamics is thereby supplied.

The unaugmented field restrictions are stationary as well, although their
first-order equations are not autonomous at stages three and four. Stationarity
does not make endpoint registration schedule-independent. On the [accepted u/v
swap](native_field_state_across_a_causal_diamond.md), both branch covariances are individually unchanged, so their difference
remains (beta/2)diag(0,0,−1,1). **The known endpoint field-state covariance FAIL
persists at every common tau.**

## Scope of the interface

The generator $K_0$ and common dimensionless parameter $\tau$ are additional
supplied choices. The minimality, equations, decoder and preservation identities
are derived under them. This finite linear interface uses an infinite-dimensional
Schrödinger carrier. It does not establish unrestricted operator-algebra closure,
minimal memory or apparatus, a physical clock or energy scale, native dynamics,
source or reservoir coupling, conservation of physical energy/stress, a pointer
instrument, gravity, a continuum theory or empirical prediction. In particular,
a parent restriction does not reconstruct the child's new independent directions
from the old outputs. PIM002's reserve result and the pointer-law result were not
inputs; no reservoir repair or instrument law is inferred from oscillator closure.

## Scientific provenance and evidence level

DET Provisional Integrated Model authored PIM003. DET Relational State Research completed the distinct
nonblind scientific review; the coordinator accepted the result with scope on
17 November 2026 (UTC). This article reuses that accepted proof and validation. Publication
assembly does not rerun the model or constitute another scientific review.

The distinct review checked the minimal-span proof, omitted-derivative witness,
ODE signs, decoder, stationary Gaussian and both birth selectors. All five declared
test groups passed without skips. The existing probe checked 360 stage occurrences
and 240 birth inclusions across the same 120 histories; repeated prefixes are
occurrences, not new preparations. Exact rational rotations are finite regression
checks, while the analytic argument proves the identities for every real $\tau$.
The original rank checkpoint was preserved without restarting enumeration:
105,425 bytes, SHA-256
`b3496e590122c515a53b5f2217ec5c79f475c15ca72d4fab1002b1d37e89b508`.
The final 884-byte dynamics summary was reproduced byte for byte, SHA-256
`c811865d756a26410816f0c0049f695d44ec00a93bdd13cfc152db0b58cf7ea8`.
The test guard disables the original rank routines during completed-interface
checks. No new histories or generator scan underlie this acceptance.

The exact source identities are recorded here without treating private archive
locations as public reproduction links:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| PIM003 accepted author report | 12,777 | `9cfbfe2d492c622f964b05a64ef44d1c4aad05ab46302ed50aa0c37732431420` |
| PIM003 distinct scientific review | 7,901 | `a822a32accd9f208391e9095854b2c2869386196429701b94c0fe0dc2dc45ebe` |

Runs were verified in the accepted scientific record. Reproduction means exact
mathematical fixtures and accepted component checks. The result is conditional
mathematics under the stated supplied choices; it adds no ontology derivation
of the growth law or canonical resources. Agreement with observations is
**NOT TESTED**: no empirical dataset, calibration or holdout was used. This
publication adds no executable for PIM003; the linked public PIM001 package has
its own narrower scope. Option B and Status M remain unchanged.
