# Coherent inertia from opposite-kick position means

**Decision.** In the registered two-level quadratic-band carrier model, the two finite-dwell phase contrasts vanish exactly when the mechanical inverse-inertia coefficient commutes with the independently registered rest generator. Their magnitude bounds the off-diagonal coefficient. When they vanish, two diagonal readings give a separate rest-gap compatibility test. A positive diagonal/noncommuting pair shares the stationary gap and the leading separate kinetic curvatures but separates under the phase test. A scalar-inertia carrier with tag-dependent kicks matches the projected twelve means if the kick registration is removed.

## Field registration and motion domain

Use the accepted E90 stationary two-mode realization on $a<b<x<y$ with its changed prefix covariance. Its dimensionless ground-state generator is $K=\sum_{\ell=1}^2\theta_\ell(N_\ell+1/2)$ with $\theta_1=5\pi/4,\theta_2=7\pi/4$. The stationary reference is a separate ground-state arm. The moving arm uses the mode tags $|0\rangle=|1,0\rangle$, $|1\rangle=|0,1\rangle$ in the same oscillator representation. Their span $\mathcal E$ is the invariant internal subspace supplied for the moving carrier. The oscillator field algebra acts in its full representation. The moving Hamiltonian can be taken block diagonal on $\mathcal E$ and its orthogonal complement, with one common choice on the complement. [Accepted stationary construction](stationary_dynamics_for_four_chain_fields.md)

On $\mathcal E$, use $H_0=\operatorname{diag}(\varepsilon_0,\varepsilon_1)>0$ and independently register $\Delta=\varepsilon_1-\varepsilon_0>0$. Identifying $\Delta=A_*(\theta_2-\theta_1)/\tau$ requires an independently calibrated physical tick $\tau>0$, action scale $A_*>0$, and an unaliased frequency identification for these same carrier modes. The E90 integer-time covariances alone allow positive frequency aliases. A calibrated rest reference with independent spectral and timing registration supplies the gap. The absolute total rest-energy offset may be supplied or left free as distinguished below. The stationary and moving preparations need a verified common carrier and mode correspondence.

Take the translation space $L^2(\mathbb R,dp)$, $P=p$, $X=iA_*\partial_p$, and a common physical axis and position baseline. In the admitted symmetric open momentum band containing the initial and both shifted packet supports, the supplied free Hamiltonian is exactly
$$
 H(p)=H_0+\tfrac12p^2 A,\qquad A=A^\dagger>0.
 \tag{1}
$$
It acts by matrix multiplication. The pulse and drift preserve $\mathcal E$, and there is no external force during the drift. The commutator calculations apply on smooth compactly supported $\mathcal E$-valued functions in the band. $X$ is the ordinary self-adjoint position operator on the full translation space, with this domain available for the calculation. A self-adjoint matrix multiplication dynamics can be defined by extending (1) outside the band. Every state used in the free dwell has support inside the band, so its evolution is independent of that extension.

For each tag, start from a fresh copy of the same real, smooth, even, normalized $g$ supported in $[-\sigma,\sigma]$, times a pure internal state $\xi$ of norm one. Set $0<\sigma<p_0$, where $p_0>0$ is a calibrated impulse magnitude. The common product packet has initial means $\langle P\rangle=\langle X\rangle=0$. Use the kick $e^{is p_0X/A_*}$ times the internal identity for $s=\pm1$. The sign follows from $is p_0X/A_*=-s p_0\partial_p$. The post-kick state is $g(p-sp_0)\xi$ with the same position mean and momentum mean $sp_0$. The kicks and packet shape are matched independently of the phase and level tags, by supplied momentum transfer registration. The six internal preparations are
$$
 |0\rangle,\ |1\rangle,\quad
 \psi_\varphi=(|0\rangle+e^{i\varphi}|1\rangle)/\sqrt2,\quad
 \varphi=0,\pi/2,\pi,3\pi/2 .
$$
Use both signs for each preparation, for twelve moving tags $z=(\xi,s)$. All use one dwell $T>0$ with $q=\Delta T/(2A_*)<1$. The phase preparations are specified relative to one stable phase reference at the beginning of the dwell.

## Complete joint observation law

For preparation bit $i$, the fixed prefix is $a\prec b$ with marks $(i,0)$ and counters $(1,0)$. A history $H$ consists of $I_x,I_y$ and the ordered pair of suffix marks. The original structural numerators over 1320 can be kept in three groups, with $ab=\{a,b\}$ and analogous set concatenation.

| $I_x$ | $I_y$ in the displayed order | Numerators for $i=0$ | Numerators for $i=1$ |
| --- | --- | --- | --- |
| $\varnothing$ | $\varnothing,x,a,ab,ax,abx$ | $6,6,5,19,33,195$ | $6,6,10,14,33,195$ |
| $a$ | $\varnothing,a,ab,ax,abx$ | $5,5,19,19,172$ | $10,10,14,14,392$ |
| $ab$ | $\varnothing,a,ab,abx$ | $19,19,19,779$ | $14,14,14,574$ |

Each row entry splits into four equally weighted marked histories. The numerators in each preparation sum to 1320, so $P_i(H)$ sums to one over the 60 histories. Let $\mathcal C$ be the four marked instances of $I_x=ab,I_y=abx$. Its original mass is $779/1320$ for $i=0$ and $574/1320$ for $i=1$. Draw each of the twelve moving tags with conditional probability $1/12$ on every history. The stationary reference and kick/position standards are established on separate runs. The moving law below is conditional on those registered standards. [Accepted native continuation ledger](finite_interval_action_and_source_preparation.md)

Supply an ideal complete position measurement on $\mathcal C$, with the internal degree unread, no disturbance before the end of the dwell, and success probability one. Use the momentum wavefunction and its position transform
$$
 \eta_z(p)=U_p(T)g(p-sp_0)\xi,\qquad U_p(t)=e^{-itH(p)/A_*},
 \qquad
 f_z(x)=\frac1{\sqrt{2\pi A_*}}\int e^{ipx/A_*}\eta_z(p)\,dp .
$$
The output probability on a Borel set $D_x\subseteq\mathbb R$ is $\int_{D_x}\|f_z(x)\|_{\mathcal E}^2dx$. Unitarity and the Fourier norm identity give total probability one. Smooth compact momentum support and (1) give a finite first moment, since the transform is rapidly decreasing. The measured mean is relative to the known common zero baseline, established independently of the final measurement. The reference kick value $k=sp_0$ is an independently certified transfer for that tag. Transfer calibration uses separate reference trials.

For $H\in\mathcal C$ the joint law of $H,z$, availability, failure flag $F$, reference transfer $k$ and position $x$ is
$$
 {\Pr}_i(H,z,\mathrm{available},F=0,k=sp_0,x\in D_x)
       =\frac{P_i(H)}{12}\int_{D_x}\|f_z(x)\|^2dx.
 \tag{2}
$$
For $H\notin\mathcal C$ it is the atom
$$
 {\Pr}_i(H,z,\mathrm{unavailable},F=\bot,k=\bot,x=\bot)
       =\frac{P_i(H)}{12}.
 \tag{3}
$$
The marker $\bot$ denotes an inapplicable motion arm. Other outcomes, including $F=1$ on $\mathcal C$ in this ideal law, have zero weight. Equations (2)–(3) sum to one and preserve the history marginal. They retain every suffix mark, tag and unavailable branch. The mechanical decision conditions on an available chain. Equations (2)–(3) retain each original chain probability in the full law. With a nonideal detector, retaining a failure symbol alone cannot establish the full population means. The theorem uses the stipulated ideal readout and exact means, with no finite-sample precision claim.

## Finite-dwell mechanical response

On the packet domain $[H,X]=-iA_*\partial_p H=-iA_*p A$. The Heisenberg velocity at time $t$ in a fixed momentum fiber is $p\,U_p(t)^\dagger A U_p(t)$. The matrix multiplier $U_p(t)$ preserves smooth compact support. Integrating the Heisenberg velocity on the common domain yields the exact mean displacement
$$
 d_{\xi,s}=\int dp\,|g(p-sp_0)|^2\,p
      \int_0^T dt\,\langle\xi|U_p(t)^\dagger A U_p(t)|\xi\rangle .
 \tag{4}
$$
Even $H(p)$ and the reflected densities give $d_{\xi,-}=-d_{\xi,+}$. Hence
$$
 r_\xi=\frac{d_{\xi,+}-d_{\xi,-}}{2p_0T}=\langle\xi|B|\xi\rangle,
 \qquad
 B=\frac1{p_0T}\int dp\,|g(p-p_0)|^2p
                \int_0^T U_p(t)^\dagger A U_p(t)\,dt .
 \tag{5}
$$
On the positive arm $p>0$ and $\int dp\,p|g(p-p_0)|^2=p_0$. Thus $B$ is an average of unitary conjugates with positive normalized weight. Writing $\lambda_-$ and $\lambda_+$ for the two extremal eigenvalues of $A$, it follows that $0<\lambda_- I\le B\le\lambda_+I$. The units of $B$ are inverse mass.

Let $u=(r_{\psi_0}-r_{\psi_\pi})/2$ and $v=(r_{\psi_{\pi/2}}-r_{\psi_{3\pi/2}})/2$. With the stated phase convention,
$$
 \langle\psi_\varphi|B|\psi_\varphi\rangle
 = (B_{00}+B_{11})/2+\operatorname{Re}(e^{i\varphi}B_{01}),
 \qquad (u,v)=(\operatorname{Re}B_{01},-\operatorname{Im}B_{01}).
 \tag{6}
$$
Their magnitude $R=\sqrt{u^2+v^2}=|B_{01}|$ is invariant under relative rephasing of the rest eigenbasis with the phase reference transformed consistently. The two eigenstate tags give $B_{00},B_{11}$. In a qualified mean record the opposite-sign means reflect, and the two sums over opposite phases both equal $r_{|0\rangle}+r_{|1\rangle}$. These are necessary model checks.

For each fiber,
$$
 \frac{d}{dt}(U_p^\dagger A U_p)
     =\frac{i}{A_*}U_p^\dagger[H_0,A]U_p,
$$
because the kinetic part of (1) commutes with $A$. Thus
$\|U_p(t)^\dagger A U_p(t)-A\|\le(t/A_*)\|[H_0,A]\|$.
Averaging (5) over $0\le t\le T$ gives
$$
 |B_{01}-A_{01}|\le\|B-A\|
 \le\frac{T}{2A_*}\|[H_0,A]\|
 =q|A_{01}|.
 \tag{7}
$$
The last equality follows by taking the operator norm of the two-by-two matrix with off-diagonal entries $-\Delta A_{01}$ and $\Delta\overline{A_{01}}$ and zero diagonal. In particular
$$
   \frac{R}{1+q}\ \le\ |A_{01}|\ \le\ \frac{R}{1-q}.
 \tag{8}
$$
For $R=0$, $q<1$ forces $A_{01}=0$. Conversely $A_{01}=0$ implies $[H_0,A]=0$, giving $B=A$ and $R=0$. Because the gap is nonzero this is exactly the commutation decision in the registered basis. The readings determine $B_{01}$ and constrain $A_{01}$ by (7)–(8). The theorem provides this decision and bound at finite dwell.

## Diagonal mass and the common energy offset

For a qualified nonzero $R$, $[H_0,A]\ne0$ excludes the GDM030 benchmark $A=c^2H_0^{-1}$ for any common energy offset. For a qualified zero $R$, $B=A=\operatorname{diag}(r_{|0\rangle},r_{|1\rangle})>0$, so
$$
       m_j=1/r_{|j\rangle},\qquad j=0,1 .
$$
The $m_j$ are inferred through displacement, signed impulse and lab time. Introduce a candidate total rest matrix $\operatorname{diag}(e,e+\Delta)$, $e>0$. GDM030 supplies the conditional benchmark, with an independent $c>0$. Its diagonal compatibility conditions are as follows.

- For a free common offset, compatibility is exactly $c^2(m_1-m_0)=\Delta$. Necessity follows by subtracting $c^2m_0=e$ from $c^2m_1=e+\Delta$. For sufficiency choose $e=c^2m_0>0$, which is unique within the benchmark.
- For known $e$, require both $c^2m_0=e$ and $c^2m_1=e+\Delta$. The gap test alone leaves the absolute equality open.
- A failed equality after a qualified diagonal result excludes the corresponding benchmark. A failed kick, time, calibration or full-mean observation model leaves the comparison unqualified. A passing mean comparison is conditional on the observation model.

In the zero-contrast case the known $g$, $T$ and inferred diagonal $A$ also specify the full law (2), with each internal component evolved by its scalar momentum phase and then traced over. This permits a full-law check on a claimed diagonal record. The mean identities alone do not certify an arbitrary full distribution. The inferred $e$ in the free-offset case is conditional on the benchmark and does not supply an independent energy measurement. [Local boost coefficient and offset theorem](conditional_boost_mass_relation.md)

## A worked positive pair and its twelve means

Use independent positive scales $A_*,\tau,c$, $E_*=A_*/\tau$, $M_*=E_*/c^2$, $p_*=E_*/c$. Fix the total rest matrix for the worked pair to the chosen $E_*K$ on $\mathcal E$. The two rest levels are $\varepsilon_0=11\pi E_*/4,\ \varepsilon_1=13\pi E_*/4$, since the stationary ground eigenvalue of $K$ is $3\pi/2$. Thus $\Delta=\pi E_*/2$. Use $T=\tau/2,\ q=\pi/8$, $p_0=p_*/10$, $\sigma=p_0/10$, and band $(-2p_0,2p_0)$. For a concrete envelope take $g(p)=C\exp[-1/(1-(p/\sigma)^2)]$ on $|p|<\sigma$, zero outside, with $C>0$ fixed by $\|g\|_2=1$. All these values are supplied choices for the exact mathematical record.

Set $a_j=c^2/\varepsilon_j>0$, $d=\sqrt{a_0a_1}/2$, and
$$
 A_{\mathrm d}=\begin{pmatrix}a_0&0\\0&a_1\end{pmatrix},
 \qquad A_{\mathrm c}=\begin{pmatrix}a_0&d\\d&a_1\end{pmatrix}.
 \tag{9}
$$
The latter is positive since $a_0>0$ and its determinant is $3a_0a_1/4>0$. The same $H_0$, oscillator reference and mode tags are used in both. In the characteristic polynomial of $H_0+\lambda A_{\mathrm c}$ the off-diagonal contribution enters as $-\lambda^2 d^2$. Nondegeneracy at $\lambda=0$ gives the same first derivatives $a_j$ as for $A_{\mathrm d}$. With $\lambda=p^2/2$, both rest-level eigenvalues start as $\varepsilon_j+(p^2/2)a_j+O(p^4)$. This establishes equality of the leading curvatures.

For the exact record, let $b_0=(B_{\mathrm c})_{00},b_1=(B_{\mathrm c})_{11},b=(b_0+b_1)/2,\ u_{\mathrm c}=\operatorname{Re}(B_{\mathrm c})_{01},\ v_{\mathrm c}=-\operatorname{Im}(B_{\mathrm c})_{01}$, with $B_{\mathrm c}$ the definite integral (5) at (9) and the stated scales and envelope. Thus every entry below is a specified exact population value. Each row supplies both signed means $d_{\xi,+}=p_0T r_\xi,\ d_{\xi,-}=-p_0T r_\xi$. Equation (2) gives the position law for those same settings.

| $\xi$ | $r_\xi$ with $A_{\mathrm d}$ | $r_\xi$ with $A_{\mathrm c}$ |
| --- | --- | --- |
| $\lvert0\rangle$ | $a_0$ | $b_0$ |
| $\lvert1\rangle$ | $a_1$ | $b_1$ |
| $\psi_0$ | $(a_0+a_1)/2$ | $b+u_{\mathrm c}$ |
| $\psi_{\pi/2}$ | $(a_0+a_1)/2$ | $b+v_{\mathrm c}$ |
| $\psi_{\pi}$ | $(a_0+a_1)/2$ | $b-u_{\mathrm c}$ |
| $\psi_{3\pi/2}$ | $(a_0+a_1)/2$ | $b-v_{\mathrm c}$ |

Equation (7) gives $u_{\mathrm c}\ge (1-\pi/8)d>0$. For $A_{\mathrm d}$ both phase contrasts are zero and the independently inferred masses pass the known-offset benchmark. For $A_{\mathrm c}$ the strictly positive first contrast already rejects it. The separation is at positive $T$, for a normalized finite-width packet. The equal curvatures are the leading coefficients at $p=0$. Equations (2) and (5) give the finite-momentum responses.

## One kick-mismatch ambiguity for projected means

Use the $A_{\mathrm c}$ record above as the matched world. Write $r_\xi^{\mathrm c}$ for its six positive response entries. Keep the same rest generator, stationary reference, initial product preparations, baseline, support and tag weights. In a second world choose scalar inverse inertia
$$
   A_{\mathrm s}=\alpha I,\quad \alpha=a_0+a_1,
   \qquad k_{\xi,s}=s p_0\,r_\xi^{\mathrm c}/\alpha .
 \tag{10}
$$
Use the same packet profile translated by the actual transfer $k_{\xi,s}$. This releases state-independent kick matching. It changes the post-kick momentum means, while preserving the sign tag and the internal preparation.

All the kicks lie in the stated band with their shifted packet supports. In detail, $B_{\mathrm c}$ lies between the extremal eigenvalues of $A_{\mathrm c}$. Since $\lambda_+<\alpha$ and $\lambda_-\lambda_+=3a_0a_1/4$,
$$
 \frac{r_\xi^{\mathrm c}}{\alpha}
 \ge\frac{\lambda_-}{\alpha}>
       \frac{3a_0a_1}{4\alpha^2}
       =\frac{143}{768}>\frac1{10},\qquad
 \frac{r_\xi^{\mathrm c}}{\alpha}<1 .
$$
Here $a_0:a_1=13:11$. Thus $\sigma<|k_{\xi,s}|<p_0$, with each full support inside $(-2p_0,2p_0)$. In the scalar world the exact velocity is $\alpha p I$ and the dwell mean is $\alpha k_{\xi,s}T=s p_0T r_\xi^{\mathrm c}$. This equals the first world's mean for every level, phase and sign tag. The strict phase contrast in the first world makes at least two actual same-sign transfers differ in the scalar world.

The projected record retains the native history and tag probabilities, available and unavailable symbols, ideal success flags, common time and position baseline, rest reference, nominal sign labels and all twelve **population means** on the available branch. It drops the independent actual-kick and shifted-packet registration, any transfer/work diagnostics, and the position distributions beyond their means. On this projection the two records coincide. The true kick entries differ from the matched $sp_0$, so the full registered laws are distinguishable. Equality of the position distributions is outside this ambiguity. It illustrates precisely why independent kick matching is part of the commutation test.

## Physical boundary and custody

The E90 record and the native weights are inherited. The moving carrier, positive quadratic-band $A$, canonical translation, coherent preparation, impulse and independent position readout are supplied structure. Evenness and exact quadratic form on the occupied band are load-bearing. Higher momentum terms can contribute off-diagonal velocity at finite $p$, so a response in an extended model would need a separate coefficient attribution. Finite dwell, nonzero independently registered gap and calibrated coherence are required for the exact converse. The dimensional standards are independent. $p_0$ has momentum units, $X$ length, $T,\tau$ time, and $A_*$ action. $B$ and its contrasts have inverse-mass units, or are dimensionless after multiplication by a registered mass reference. $\Delta$ has energy units, and $c$ is needed independently for the diagonal comparison.

In the ideal matched arm the kick changes the carrier energy by $p_0^2\langle\xi|A|\xi\rangle/2$. This follows from the common zero incoming momentum mean, equal packet variance and unchanged internal vector at the pulse. The impulse source must provide the opposite momentum and account for its own recoil and transferred work. During free dwell $P$ and the total $H(P)$ are conserved. The separate internal and quadratic terms can exchange expectation when they do not commute. Separate work accounts are required for preparing the modes and their phase reference, packet production, impulse control and source restoration, readout and failed acquisitions in a nonideal realization, and restoring the carrier and reference for the next trial. The ideal measurement is a stipulated statistical law. A calibrated apparatus and a gravitational response require separate physical premises.

The earlier same-carrier registration concerns active/inertial proportionality under static mixing and successful coverage, while the moving-phase comparison tests scalar dispersions at several speeds. This packet uses a phase-sensitive inertial coefficient within one registered rest doublet. The conventional primary comparison separates rest and inertia operators and discusses a horizontal interferometric test. The signed-kick position law and exact quadratic band are the specific supplied premises here. [Same-carrier registration](same_carrier_mass_registration.md) · [Moving phase and velocity](dispersion_from_phase_and_velocity.md) · [Zych and Brukner, arXiv:1502.00971v1, §§II–IV](https://arxiv.org/pdf/1502.00971v1)

## Scientific review

Relational State derived this finite conditional result. Quantum Relativity independently verified the full law, bound, positive example, offset conditions and projected-mean ambiguity. Author report SHA-256 2c1ea2ce20f22ad24bcda644fc0599de1b6e2bd76dda94a698c25207f3a69812; independent review 40a961747865f9261587857605d1adf72d5d57015e5033b6d5e75e3e2cbf95a2.
