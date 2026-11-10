# What a negative position covariance says about time reversal

The exact stationary position pair excludes every finite, time-homogeneous continuous-time jump model satisfying conventional detailed balance on its stationary support with this deterministic readout. Its covariance is $-2z$ for the contrast below. The specified six-state process nevertheless reproduces the pair and triple and is microscopically reversible when direction changes sign under path reversal. The three-state circulating source reproduces the same record with conventional microscopic irreversibility. The interpretation therefore depends on the physical assignment of time-reversal parity, which the three position readings do not determine.

## Fixed position record and circulating source

At $0,\tau,2\tau$, read the chronological position $i\in\mathbb Z_3$ with the same labels and deterministic map. Prepare the stationary law and make no intermediate reset or selection. Use outgoing rows, so the transition matrix acts on column observables. Let $C_{i,i+1}=1$ modulo three, $\Pi=(I+C+C^2)/3$, $r=\pi/(\sqrt3\,\tau)>0$, and $z=e^{-6r\tau}=e^{-2\sqrt3\pi}$. Rates are inverse supplied model time. Position labels, the contrast, $z$, and probabilities are dimensionless.

The circulating model has $L_+=r(3C+C^2-4I)$. Uniform stationarity follows from zero column sums. The two orientations on the edge $i\leftrightarrow i+1$ carry stationary flows $3r/3$ and $r/3$, giving current $2r/3$ in the fixed positive orientation. All three positions are even. Conventional path reversal thus fails. As a check on the reported clock, the two centered eigenvalues of $L_+$ are $-6r\pm i\sqrt3 r$. Their exponentials at $\tau$ both equal $-z$. The constant mode is preserved, hence
$$
 Q=\Pi-z(I-\Pi),\qquad Q_{ii}=(1-2z)/3,\qquad Q_{ij}=(1+z)/3\quad(i\ne j).
$$
The stationary Markov source gives pair probability $Q_{ij}/3$ and triple probability $Q_{ij}Q_{jk}/3$.

## Obstruction for every all-even completion in the registered class

Let $G$ generate any candidate hidden process on its finite stationary support with stationary weights $\mu_x>0$. Write $g$ for its position map and $H(x)=h(g(x))$, with $h=(2,-1,-1)$. Any candidate matching the pair has uniform position marginal, so $E_\mu H=0$ and $\|H\|_\mu^2=2$. Conventional detailed balance $\mu_xG_{xy}=\mu_yG_{yx}$ makes $G$, and hence $P_t=e^{tG}$, self-adjoint for $\langle a,b\rangle_\mu=\sum_x\mu_x a(x)b(x)$. Stationarity and the semigroup law give
$$
 \operatorname{Cov}(h(g(X_0)),h(g(X_\tau)))=
 \langle H,P_\tau H\rangle_\mu
 =\|P_{\tau/2}H\|_\mu^2>0 .
$$
The exponential of a finite matrix is invertible at finite time, so the nonzero lift cannot have zero norm after this operator acts. The half-time factor is an algebraic identity inside the candidate model and requires no intermediate reading or preparation. No Markov assumption on the observed position enters. The target has $Qh=-zh$ and therefore covariance $\sum_i h_i(Qh)_i/3=-2z<0$. This contradiction already rules out a matching pair, and marginalizing a matching triple would produce that same impossible pair.

## Six-state sampling calculation

Order the states by sign and then by position. The off-diagonal block from sign $s$ to $-s$ is $r\Pi$, including its same-position entry $r/3$. The block that preserves the sign is
$$
 B_s=(8r/3)C^s+(2r/3)C^{-s}-(13r/3)I .
$$
Every row and column of the full generator sums to zero. In particular each exit rate is $13r/3$, including flips that keep the position. All jump rates are nonnegative and the uniform probability $1/6$ per state is stationary.

For the centered position mode $f_m(i)=e^{2\pi \mathrm{i} m i/3}$, $m=1,-1$, the flip block vanishes because $\Pi f_m=0$. Thus position modes supported in one sign block remain there under the generator. On that block their eigenvalues are
$$
 \lambda_{s,m}=(8r/3)e^{2\pi\mathrm{i}ms/3}
             +(2r/3)e^{-2\pi\mathrm{i}ms/3}-13r/3
             =-6r+\mathrm{i}\,ms\sqrt3 r .
$$
Both exponents $e^{\tau\lambda_{s,m}}$ are $-z$ in either sign. The observable constant across all six states is preserved. Decomposing the position indicator for terminal label $j$, lifted identically to both signs, into its mean $1/3$ and centered part yields, for each of the six starting states,
$$
 \sum_{u=\pm1}(e^{\tau G_6})_{(i,s),(j,u)}
 =\tfrac13-z(\mathbf1_{i=j}-\tfrac13)=Q_{ij}.
$$
Here $G_6$ denotes the full block generator just defined. This conditional equality holds before averaging over a starting sign.

Write $Y_t$ for position and $S_t$ for direction. At stationarity $P(Y_0=i,Y_\tau=j)=Q_{ij}/3$. For any such pair, the hidden Markov property gives
$$
 P(Y_{2\tau}=k\mid Y_0=i,Y_\tau=j)
 =\sum_{u=\pm1}P(S_\tau=u\mid Y_0=i,Y_\tau=j)
     P(Y_{2\tau}=k\mid Y_\tau=j,S_\tau=u)=Q_{jk}.
$$
The posterior weights sum to one and each last factor is the same from either direction. Hence the triple is $Q_{ij}Q_{jk}/3$ for every $i,j,k$, as in the circulating source. Since $Q$ is symmetric and the marginal uniform, this triple equals the time-reversed position triple $Q_{kj}Q_{ji}/3$.

## Time-order reversal and both parity conventions

Use the same stationary six-state dynamics in the reverse comparison and align states in reverse chronological order with $\Theta(i,s)=(i,-s)$. For a fixed-sign jump $(i,s)\to(i+d s,s)$, $d=\pm1$, the aligned reverse jump starts at $(i+d s,-s)$ and displaces by $d(-s)$. It has the same coefficient $8r/3$ for $d=1$ and $2r/3$ for $d=-1$. For a flip $(i,s)\to(j,-s)$, the aligned reverse jump $(j,s)\to(i,-s)$ also has rate $r/3$, including $j=i$. Thus each $G_{6,xy}=G_{6,\Theta y,\Theta x}$ off the diagonal. Stationary endpoint weights are all $1/6$, and the survival factor for each residence of duration $u$ is $e^{-13ru/3}$ in either parity partner. Reversing the order of the residence intervals and jump factors preserves their product, including the terminal residence. This proves equality of the aligned stationary microscopic path laws.

Under identity parity the edge $(0,+)\to(1,+)$ has rate $8r/3$ and its ordinary reverse has rate $2r/3$. The equal endpoint weights and holding rates leave the forward stationary flow four times the reverse flow. The parity change alone accounts for the difference between the two microscopic reversal tests on this fixed generator.

## Discrete-time control and scope

As a discrete-time kernel $Q$ has unit row sums, strictly positive entries because $0<z<1/2$, and $Q_{ij}/3=Q_{ji}/3$. It is conventionally reversible with the uniform law despite the centered eigenvalue $-z$. Discrete-time detailed balance gives self-adjointness but allows a negative eigenvalue. Continuous-time detailed balance at stationarity supplies the additional self-adjoint semigroup square in the obstruction. The circulating model above provides a continuous-time embedding that violates conventional detailed balance.

Position is even under reversal in both models. The lag, rates, stationary preparation, labels and readout are supplied. The position record leaves the physical parity of a hidden variable and any thermodynamic interpretation undetermined. [Ford and Spinney on reversal in discrete phase space](https://arxiv.org/abs/1204.4822v2)

## Applicability to the DET position and source records

The birth-indexed transport experiment starts at a fixed site. An interval counted in births supplies neither the stationary ring preparation nor a common elapsed duration. Its position triple tests a position-only Markov model with a noninvasive reader. The separate source-channel experiment rules out its proposed equilibrium model because the channel changes the supplied equilibrium distribution. Neither record establishes a negative stationary lag covariance for the same repeatedly observed even position. [Position-triple experiment](three_position_reads_and_timed_projection.md) · [Source-channel stationarity test](source_channel_reversible_markov_obstruction.md)
