# Positive stationary dynamics for the four-chain field

The accepted two-event covariance cannot be preserved by any finite positive oscillator generator in the supplied class while realizing the four-chain commutator. Its saturated adjacent-time correlation forces a common phase advance on every occupied mode, and the commutator at separation two then vanishes. Releasing only that covariance permits an exact two-mode stationary realization. This is a decision about the stipulated oscillator dynamics, not a derivation of physical energy, time or rest mass.

The supported structural history is $a<b<x<y$, indexed by supplied dimensionless ticks $n=0,1,2,3$. Its source-conditioned probabilities are $779/1320$ and $574/1320$ for the two original prepared sources. For each source, each of the four fair suffix-mark pairs contributes one quarter of that probability: $779/5280$ and $574/5280$, respectively. These weights and the rest of the native law are retained. The chain is a necessary test for an all-branch construction; selecting it for this proof does not turn its native probability into one. The [finite interval and source specification](finite_interval_action_and_source_preparation.md) supplies those bookkeeping premises.

The accepted [field-transport construction](gaussian_field_transport_on_native_histories.md) supplies the prior kinematic attachment and accepted prefix. Its validity is not disputed here. The new, explicitly supplied premises are a single stationary oscillator state, one time-translated observable and a positive quadratic generator. None is inferred from the native growth law.

Take any finite number $N$ of canonical pairs with
$$
[Q_j,P_k]=i\delta_{jk}I,\qquad
K=\frac12\sum_{j=1}^N\theta_j(Q_j^2+P_j^2),\quad\theta_j>0,
$$
and the centered product ground state, whose canonical variances are $1/2$. Let
$$
\phi_0=\sum_j(a_jQ_j+b_jP_j),\quad a_j,b_j\in\mathbb R,
\qquad
\phi_n=e^{inK}\phi_0e^{-inK}.
$$
The required commutator is
$$
[\phi_n,\phi_m]=i\beta\,\operatorname{sign}(n-m)I,\quad n\ne m,\quad \beta>0.
$$
The unsymmetrized covariance is $W_{nm}=\langle\phi_n\phi_m\rangle$, with times in increasing order. Its fixed prefix is
$$
W_2=\frac{\beta}{2}\begin{pmatrix}1&-i\\i&1\end{pmatrix}.
$$
All later covariances are free. We do not use unequal variances in a particular previous four-time covariance as an impossibility argument.

The standard Heisenberg convention gives
$$
Q_j(n)=Q_j\cos(n\theta_j)+P_j\sin(n\theta_j),\qquad
P_j(n)=P_j\cos(n\theta_j)-Q_j\sin(n\theta_j).
$$
In particular, the sign follows directly from $i[K,Q_j]=\theta_jP_j$. Put
$c_j=a_j^2+b_j^2$ and $w_j=c_j/2\ge0$. Ground-state contraction, including $\langle Q_jP_j\rangle=i/2$, gives the complete formulas
$$
W_{nm}=\sum_jw_j e^{-i(n-m)\theta_j},\qquad
[\phi_n,\phi_m]=-2i\sum_jw_j\sin((n-m)\theta_j)I. \tag{1}
$$
The state is stationary because its density operator commutes with $K$. Equation (1) includes arbitrary real initial quadratures, repeated frequencies and unused modes; no special choice of $a_j,b_j$ was imposed.

The fixed prefix requires
$$
\sum_jw_j=\frac{\beta}{2},\qquad
\sum_jw_j e^{-i\theta_j}=\frac{i\beta}{2}. \tag{2}
$$
Normalize the nonzero weights by their positive sum. A convex combination of unit-circle points in (2) equals the extreme unit-circle point $i$. Equality in the triangle inequality therefore forces
$$
e^{-i\theta_j}=i
$$
for every occupied mode. Equivalently $\theta_j=3\pi/2$ modulo $2\pi$; all positive aliases are covered. Zero-weight modes have no effect. At lag two every occupied phase is $-1$, so
$$
W_{20}=-\frac{\beta}{2}\in\mathbb R,\qquad
[\phi_2,\phi_0]=0.
$$
This contradicts the required $i\beta I$. Indeed $\phi_2=-\phi_0$ on the occupied canonical modes. The contradiction already uses the first three times, so no fourth-time covariance choice repairs it. It covers the entire finite class in the control. The excluded degenerate case $\beta=0$ does not support the normalization in (2) and is not part of the result.

Now make the one permitted change: release $W_2$, retaining the same $\beta$, causal commutator, time orientation, single stationary product ground state and positive generator. Choose two modes with
$$
\theta_1=\frac{5\pi}{4},\quad\theta_2=\frac{7\pi}{4},\qquad
a_1=\sqrt{\frac{\beta}{2}(\sqrt2-1)},\quad
a_2=\sqrt{\frac{\beta}{2}(\sqrt2+1)},\qquad b_1=b_2=0. \tag{3}
$$
Use $\phi_0=a_1Q_1+a_2Q_2$ and the stated Heisenberg evolution. Both coefficients squared and frequencies are strictly positive. On $L^2(\mathbb R^2)$, $K$ is the usual positive self-adjoint oscillator operator, with ground eigenvalue $(\theta_1+\theta_2)/2=3\pi/2$ and positive excitation gaps $\theta_1,\theta_2$. The Schwartz domain is a common invariant domain for the displayed polynomial identities. Finite mode count here does not mean finite Hilbert-space dimension. The normalized product Gaussian is stationary up to the ground-state phase.

For a positive lag $\ell=n-m$, equation (1) yields
$$
W_0=\frac{\beta}{\sqrt2},\quad
W_1=\frac{\beta}{2\sqrt2}+\frac{i\beta}{2},\quad
W_2^{\rm lag}=\frac{i\beta}{2},\quad
W_3=-\frac{\beta}{2\sqrt2}+\frac{i\beta}{2}. \tag{4}
$$
Negative lags are complex conjugates. The symbol $W_2^{\rm lag}$ in (4) means lag two, not the prefix matrix. The full four-time covariance, in order $0,1,2,3$, is
$$
W=\frac{\beta}{2}
\begin{pmatrix}
\sqrt2&1/\sqrt2-i&-i&-1/\sqrt2-i\\
1/\sqrt2+i&\sqrt2&1/\sqrt2-i&-i\\
i&1/\sqrt2+i&\sqrt2&1/\sqrt2-i\\
-1/\sqrt2+i&i&1/\sqrt2+i&\sqrt2
\end{pmatrix}. \tag{5}
$$
All means vanish. Its real part is the symmetrized covariance; its lower off-diagonal imaginary parts are all $+\beta/2$. Thus (1) or direct subtraction gives
$$
W_{nm}-W_{mn}=i\beta\,\operatorname{sign}(n-m),\quad n\ne m,
$$
with the required operator commutators, not merely matching expectations: linear canonical-field commutators are scalars times $I$. Equation (5) is Toeplitz, so it has the stipulated stationarity.

For an exact positivity check, set $u_{j,n}=e^{-in\theta_j}$, $n=0,\ldots,3$. Then
$$
W=\sum_{j=1}^2w_j u_ju_j^\dagger,\qquad w_j=\frac{a_j^2}{2}>0.
$$
The two vectors are orthogonal, since their phase difference is $\pi/2$ and four successive powers sum to zero, and each has squared norm four. The covariance eigenvalues are exactly
$$
\beta(\sqrt2-1),\quad\beta(\sqrt2+1),\quad0,\quad0.
$$
Hence $W$ is positive semidefinite; it is explicitly realized in the canonical ground state, not just posited as a positive matrix.

The changed prefix is
$$
W'_2=\frac{\beta}{2}
\begin{pmatrix}\sqrt2&1/\sqrt2-i\\1/\sqrt2+i&\sqrt2\end{pmatrix},
\qquad \det W'_2=\frac{\beta^2}{8}>0. \tag{6}
$$
Its diagonal variance is $\beta/\sqrt2$, replacing $\beta/2$, and its real nearest-time covariance is $\beta/(2\sqrt2)$, replacing zero. The adjacent-time commutator is unchanged. This is exactly the released premise. We have given one construction and made no minimum-mode claim, no search over further growth cases and no further relaxation.

The sampled sign deserves a separate check. Under the standard Heisenberg convention the commutator of a single positive-frequency position field has the minus-sine sign in (1). The chosen phases exceed $\pi$, and their weighted sine sums at each of the three positive integer lags equal $-\beta/2$. The resulting commutators therefore have the required positive sign. No upper frequency bound was supplied. This does not assert a constant-sign commutator at every positive continuous time: near zero the minus-sine expression has the opposite sign. The question concerns only the four supplied ticks.

The obstruction is consequential for any proposed all-branch dynamics containing this positive-probability chain with the same fixed prefix and oscillator premises. The constructive result is narrower: it realizes this chain conditional on its selection after the allowed prefix change. It does not construct a family on all the other native histories, establish consistency between different branches, or replace their original weights. The fair marks may label the four instances of the same chain construction without modifying those weights. The selected Gaussian and canonical operators remain an external mathematical attachment to the native histories.

The dimensionless $\beta$ is a prescribed field-commutator normalization. In (3), the amplitudes are chosen proportional to $\sqrt\beta$, and the $\theta_j$ are chosen phase advances per supplied tick. The native birth index has supplied no duration. Moreover, replacing a $\theta_j$ by a positive alias $\theta_j+2\pi k_j$ preserves every integer-time field covariance and commutator while changing the oscillator energy gaps. Thus even this complete sampled record does not uniquely identify the generator spectrum. An arbitrary additive identity shift also leaves Heisenberg observables unchanged; the control fixes a particular unshifted positive $K$, without proving an absolute physical energy origin.

If an independent physical clock gives $\tau>0$ per tick and an action reference $A_*>0$ is independently supplied, one may define
$$
t=n\tau,\qquad H_{\rm phys}=\frac{A_*}{\tau}K+C I.
$$
Then evolution with $e^{itH_{\rm phys}/A_*}$ agrees with the prescribed $e^{inK}$, up to an irrelevant scalar phase. Frequencies are $\theta_j/\tau$, energy gaps are $A_*\theta_j/\tau$, and a field unit $F_*$ gives $\Phi_n=F_*\phi_n$ and commutator $iF_*^2\beta\,\operatorname{sign}(n-m)$. Canonical physical units likewise require a declared map from the dimensionless $Q,P$. None of $\tau,A_*,F_*,C$ is determined by this chain calculation.

The [native phase/action interface](native_phase_action_interface.md) separates native transitions from supplied phase dwells and calibrations. The [dispersion comparison](dispersion_from_phase_and_velocity.md) supplies a separate, conditional route involving moving-carrier observations. This oscillator construction has neither a registered translational momentum nor an inertia or dispersion measurement. Calling a positive excitation gap a rest mass would introduce a further physical law and scale. It is not a conclusion here.

Ground-state preparation, maintaining the frequency settings and tick reference, accessing the noncommuting field readings, measurement disturbance, controller energy, reset and readout costs remain unspecified. A Gaussian vector is a mathematical state, not an established preparation procedure. Mathematical mode count does not give an apparatus energy budget or work-extraction protocol. For the supplied autonomous model $K$ is conserved under its own evolution; this does not account for an external preparation or measuring apparatus.

The finite decision is therefore **incompatible with the fixed accepted prefix; compatible on the supported chain after releasing that prefix, within the supplied stationary oscillator model**. This remains a conditional mathematical result. The changed prefix preparation would need separate physical registration before any operational energy or mass interpretation.
