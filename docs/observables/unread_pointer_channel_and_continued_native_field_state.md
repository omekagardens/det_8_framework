# Unread pointer channel and continued native field state

**Accepted conditional result.** The accepted pointer
interaction and supplied oscillator evolution can be composed, but the field
cannot silently retain its original vacuum state. A normalized reduced-state
channel supplies the missing interface. It closes on first and second moments,
while a prospectively chosen native history proves that the output need not be
Gaussian. Thus a Gaussian covariance alone is not a complete state description.

For both complete original preparations, with all histories and all pointer
outcomes retained, the post-readout oscillator diagnostic obeys

\[
\boxed{\quad \langle K_0\rangle_{i,\mathrm{out}}
\geq \frac32+\frac1{440}=\frac{661}{440}>\frac32,
\qquad i=0,1.\quad}
\]

This is a strict failure to preserve the stipulated vacuum, not a physical
energy-injection, conservation or detector-performance claim. The lower bound
is not the exact complete-mixture expectation. Subsequent supplied oscillator
evolution preserves this excess and therefore cannot restore that vacuum.

## 1. Registered ingredients and composition

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

The [closed oscillator interface](closed_oscillator_interface_on_native_histories.md)
supplies the generator and common formal evolution,

\[
R=(Q_0,P_0,Q_x,P_x,Q_y,P_y)^T,\quad [R_j,R_k]=iJ_{jk},\quad
K_0=\tfrac12 R^TR,\quad E(\tau)=I\cos\tau+J\sin\tau.
\]

The initial field is its stipulated pure vacuum, with mean zero, symmetric
covariance $I_6/2$ and $K_0$ expectation $3/2$. Both $K_0$ and $\tau$ remain
supplied dimensionless choices. The
[complete pointer construction](complete_pointer_laws_on_native_histories.md)
supplies the independent pointer, spectral unitary and position measurement;
the [bounded response for both complete preparations](bounded_pointer_response_for_complete_native_preparations.md)
supplies the complete history/record interface and original probability ledger.

The declared composition is one terminal interaction, a complete pointer position
measurement whose outcome is ignored for the subsequent field marginal, then the
supplied common oscillator flow. It introduces no feedback, field reset, repeated
instrument, new birth, waiting-time law or additional measurement. The state
conditioned on a retained outcome is displayed below, but continuation uses the
unread marginal. The empty/empty witness was fixed prospectively before the
state-update calculation; it does not replace either complete preparation.

## 2. The normalized field channel

For each actual terminal history H, keep its accepted nonnegative Friedrichs
operator Q=Q_H, the pointer g(x)=pi^(-1/4)exp(-x²/2), and the spectrally defined
unitary U=exp(-i Q tensor Pp). In the pointer-position representation the Kraus
density is the bounded spectral function

\[
M_x=g(x-Q)=\pi^{-1/4}\exp[-(x-Q)^2/2].
\]

For a field density operator rho, the joint instrument is
M_x rho M_x dx. Its trace is the accepted pointer density. Where that density is
positive, division by the trace gives the outcome-conditioned field state.
Spectral calculus and the normalized Gaussian give
integral M_x² dx=I in the strong sense, so

\[
\Phi_H(\rho)=\int_{\mathbb R}M_x\rho M_x\,dx
\]

is completely positive and trace preserving on trace-class states. One can take
the integral first on positive trace-class states, where trace one and monotone
integration fix it, then extend linearly. No finite-dimensional Hilbert-space
truncation or simultaneous classical cover-field assignment is involved.

Equivalently, the normalized pointer momentum density is
h(s)=pi^(-1/2)exp(-s²), with mean zero and variance 1/2. Tracing in that basis gives

\[
\boxed{\quad
\Phi_H(\rho)=\frac1{\sqrt\pi}\int_{\mathbb R}
e^{-s^2}e^{-isQ_H}\rho e^{isQ_H}\,ds.\quad}
\tag{1}
\]

For example, between spectral values lambda and lambda-prime the two forms have
the same multiplier exp[-(lambda-lambda-prime)²/4]: it follows either by integrating
g(x-lambda)g(x-lambda-prime) or by the characteristic function of h. Equation (1)
is the full reduced quantum state map. The random scalar s describes a mixture
of quantum unitaries, not classical joint values of noncommuting cover fields.

The complete history/field output is the classical-quantum state with blocks
P_i(H) Phi_H(rho_vac), and its unread field marginal is

\[
\rho_{i,\mathrm{out}}=\sum_H P_i(H)\Phi_H(\rho_{\rm vac}).
\tag{2}
\]

All 60 positive marked histories under each preparation remain; each conditional
channel has trace one, so every native history marginal is unchanged. This also
retains all real pointer outcomes. Reading the pointer and then forgetting its
outcome gives the same field marginal as simply tracing it out.

The already-recorded complete-preparation pointer marginal, including its exact rational contrast
interval [2645093527/2834678415360, 977776931/944892805120], is unchanged. A subsequent
field-only unitary cannot alter that pointer marginal. This does not license
reusing the initial-vacuum pointer law for a second measurement.

## 3. Closed moment interface, without a Gaussian-state assumption

Let A_H contain the actual normalized cover rows and B_H=A_H^T A_H. Then
Q_H=R^T B_H R/2, with Weyl ordering automatic because B_H is symmetric. Put
F_H=J B_H. The CCR give i[Q_H,R]=F_H R, and hence

\[
e^{isQ_H}R e^{-isQ_H}=S_H(s)R,\qquad S_H(s)=e^{sF_H}.
\tag{3}
\]

This identity can be interpreted on the bounded Weyl operators, avoiding an
unbounded-operator product assertion. The quadratic canonical flow solves the
linear coefficient equation with initial identity and is symplectic because
F_H J+J F_H^T=0. Its unitary lift differentiates to the same real quadratic on
the canonical polynomial core. To identify its generator with the accepted
realization, finite Hermite vectors form a dense analytic set: each quadratic
application changes total occupation by at most two and its norm on an occupation
cutoff grows at most linearly in that cutoff. Repeated application is therefore
bounded by a constant to the k-th power times k! times a fixed polynomial in k,
which has a positive analytic-vector radius. The quadratic is essentially
self-adjoint there; its nonnegative closure is the specified Friedrichs operator.
Thus the lift and spectral unitary agree. The shear below also verifies (3)
directly without needing this general construction.

For arbitrary finite first and second moments define m=Tr(rho R) and the raw
symmetric matrix T_jk=Tr(rho {R_j,R_k}/2). The map on centered covariance must
subtract the updated m m^T if m is nonzero. From (1) and (3),

\[
m'=\mathbb E_s[S_H(s)]m=\exp(F_H^2/4)m,
\]
\[
T'=\mathbb E_s[S_H(s)T S_H(s)^T]
       =\exp(\mathcal L_H^2/4)T,\qquad
\mathcal L_H(T)=F_H T+T F_H^T.
\tag{4}
\]

The last exponential is an ordinary linear operator on the 21-dimensional space
of real symmetric six-by-six matrices. Its square means composition of that
operator, not elementwise squaring. The Gaussian identity follows from the
even-moment series, E s^(2k)=(2k)!/(4^k k!). It is valid for these finite matrices:
the exponential series and integral are absolutely dominated by exp(C|s|).
In particular, ||S_H(s)||≤exp(||F_H|| |s|), so all the second moments in this
finite family are finite after Gaussian averaging. Higher fixed moments of the
initial Gaussian are finite by the same estimate. No infinite-energy exception
is being used in the complete-preparation bound.

Afterward the supplied common flow gives exactly

\[
m(\tau)=E(\tau)m',\qquad
T(\tau)=E(\tau)T'E(\tau)^T.
\tag{5}
\]

Its completed terminal coordinates Z=C_H R are invertible linear coordinates;
transform these moments by C_H and its transpose to reuse the accepted explicit
completed equations. The letter C_H here distinguishes that decoder interface
from the quadratic matrix B_H above. Finite sums with the original P_i(H) give
the complete-preparation moments. Means remain zero for the specified vacuum
input, so T is then the covariance.

Equations (1), (4) and (5) are a constructive continuation interface. Equations
(4)-(5) close the first/second-moment problem; they do not determine every
observable or make the output Gaussian. The accepted finite computation evaluated
the fixed witness and complete-preparation bound; it did not implement general
matrix exponentials or a full density-operator simulator.

## 4. Fixed witness: exact field disturbance and non-Gaussianity

The control prospectively fixed Ix=empty, Iy=empty. The only cover is a<b and
d=−Q0−P0, so Q=(Q0+P0)²/2. Both suffix pairs are untouched. On the first pair,

\[
F=N=\begin{pmatrix}1&1\\-1&-1\end{pmatrix},\quad N^2=0,
\qquad S(s)=I+sN=
\begin{pmatrix}1+s&s\\-s&1-s\end{pmatrix}.
\]

The conditional state at fixed s is a centered Gaussian, with first-pair
covariance

\[
V_s=\tfrac12 S(s)S(s)^T=
\begin{pmatrix}
1/2+s+s^2&-s^2\\-s^2&1/2-s+s^2
\end{pmatrix}.
\]

Averaging s with E s²=1/2 gives the exact unread covariance

\[
\boxed{\quad V_{\rm out}=
\begin{pmatrix}1&-1/2\\-1/2&1\end{pmatrix}\oplus I_4/2.\quad}
\tag{6}
\]

This is a valid mixed-state covariance: the first block has eigenvalues 1/2 and
3/2 and determinant 3/4. It is not the original covariance I6/2. Its first means
are still zero. For Q0 at fixed s, the variance v_s=1/2+s+s² and the fourth
moment is 3v_s². Using E s⁴=3/4 and vanishing odd moments,

\[
\langle Q_0^2\rangle=1,\qquad
\langle Q_0^4\rangle=3\mathbb E v_s^2=6,\qquad
\kappa_4(Q_0)=6-3(1)^2=3.
\tag{7}
\]

The positive fourth cumulant proves the witness output is non-Gaussian. A
Gaussian with the same covariance would incorrectly predict Q0 fourth moment 3.
As a full-state check, rotate coordinates to A=(Q0+P0)/sqrt(2),
B=(−Q0+P0)/sqrt(2). Here Q=A² and the initial first-pair wavefunction is
psi(a)=pi^(-1/4)exp(-a²/2). The exact unread density kernel is

\[
\rho'(a,a')=\psi(a)\overline{\psi(a')}
\exp[-(a^2-a'^2)^2/4].
\]

This displays the changed state without discarding the field coherence by fiat.
It is not a new pointer-distribution calculation.

The distinction between a channel and a canonical observable evolution is also
essential. In this witness Phi-dagger(Q0)=Q0 and Phi-dagger(P0)=P0, but

\[
\Phi^\dagger(Q_0^2)=Q_0^2+\tfrac12(Q_0+P_0)^2
\ne\big(\Phi^\dagger(Q_0)\big)^2.
\tag{8}
\]

Each conditional shear is symplectic; its unread average is not a multiplicative
algebra automorphism. The identity first-moment map must not be mistaken for an
unchanged state or a deterministic symplectic evolution.

## 5. Whole-preparation conclusion and continued evolution

For the witness, (6) gives <K0>=Tr(Vout)/2=2, an excess of 1/2 over the initial
3/2. Each preparation's accepted ledger assigns total witness mass 1/220,
comprising all four suffix marks with individual masses 1/880. The accepted finite computation read
these values from the existing complete-preparation ledger without rerunning growth.

The oscillator inequality K0≥3/2 holds on every normalized field output. Thus
every other history contributes a nonnegative excess. Keeping the complete sum,

\[
\begin{aligned}
\langle K_0\rangle_{i,\mathrm{out}}-3/2
&=\sum_H P_i(H)\operatorname{Tr}
   [(K_0-3/2)\Phi_H(\rho_{\rm vac})]\\
&\geq (1/220)(1/2)=1/440.
\end{aligned}
\]

This proves neither complete output equals the original vacuum. It does not,
by itself, prove either full history mixture is non-Gaussian or nonstationary
under K0. Those stronger statements are not claimed. Non-Gaussianity and
nonstationarity are established for the fixed conditional witness only.

The later oscillator is orthogonal, so (5) preserves Tr(T)/2 and hence this
excess. For example, a quarter-turn flips the off-diagonal entry in the witness's
first covariance block from −1/2 to +1/2; it evolves the changed covariance,
not I6/2. Neither that nor any later oscillator time restores the vacuum.
The accepted oscillator vacuum-stationarity theorem remains correct for its original input;
readout has changed that premise. The supplied moment equations still apply.

## 6. Scope and scientific provenance

The original probabilities and field, canonical vacuum, pointer access and
coupling, $K_0$ and $\tau$ are supplied components. The one unread interaction
followed by the common oscillator is a declared composition. The normalized
channel, moment maps, fixed witness state and complete-preparation lower bound
are derived conditional mathematics. No fit, empirical calibration or holdout
is present.

$K_0$ is not asserted to be physical energy. No total field/pointer/interaction
energy balance, conservation law, physical clock, native unit, gravitational
coupling, reservoir dynamics, physical detector performance or empirical
prediction follows. The
[endpoint field-state covariance failure](native_field_state_across_a_causal_diamond.md)
and [named pointer-law inequality](complete_pointer_laws_on_native_histories.md)
remain unchanged; state disturbance repairs neither. The source bit, growth
probabilities and all history support stay fixed. Option B and Status M remain
unchanged. The fixed conditional witness is non-Gaussian and nonstationary;
the complete mixtures are established only to be non-vacuum. There is no
full-mixture non-Gaussianity or nonstationarity conclusion here.

DET Provisional Integrated Model authored PIM005. DET Energy Research completed
the distinct nonblind scientific review and the coordinator accepted it with
scope on 17 November 2026 (UTC), without author correction. Author-side assistance
was separate from that verdict. Energy checked the full analytic channel and
moment arguments and independently reconstructed the witness generator, shear,
covariance, fourth moment, superoperator update, quarter-turn and lower bound.
The review checked all 120 native masses and all eight marked witness records
across both preparations without rerunning growth enumeration.

Six declared test groups passed without skips or expected failures. The existing
CLI produced 1,969 bytes with exit zero and empty stderr, byte-identical to the
accepted result, SHA-256
`18141e989b25e6df8749b67d1a6824e2ca3a2f4f1a19e68420f854391c8d0ffd`.
These are attributed prior scientific checks; they were not rerun for publication.
The analytic arguments carry the general state/channel claims. Finite witness
checks do not implement a general matrix-exponential or full-state simulator.

| Accepted source | Bytes | SHA-256 |
| --- | ---: | --- |
| PIM005 author report | 15,284 | `9e289c12141e4939576f2a5d0f13d7517f4f23e0d6feac65fb38035a9804895d` |
| Distinct Energy scientific review | 13,450 | `894dc6f02058ae4f6488004d95c07084dae18de42963227322ee1b0f24a98fb8` |

These source identities are not private-path public reproduction links. The
linked PIM001 implementation remains at its existing scope; this publication
adds no PIM005 executable. Runs were verified in the accepted scientific record;
reproduction concerns native weights and exact mathematical fixtures. No new
ontology derivation of the supplied resources, dynamics, interaction or physical
units is claimed. Agreement with observations is **NOT TESTED**.
