# Paired photon counts and the calibration of a gravitational mass measurement

**Decision.** Under the stipulated pure-pair source and fixed independent Bernoulli losses, the two means, two variances and covariance determine both efficiencies uniquely whenever an exact integer-brightness feasibility test passes. No individual photon-pair matching is needed. With independently registered transfer of the signal efficiency to the burst population measure, this removes the accepted common efficiency ambiguity in the recoil/fixture inverse. Source purity cannot be certified by these moments: the pump-associated background family below admits different efficiencies with the same full joint count law, so absolute mass and fixture calibration remain conditional.

Paired optical counts are an established absolute-calibration context. Peřina Jr. et al. discuss count statistics, source noise and a specified source-family histogram model. Here every conclusion follows from the model specified below; no empirical parameter, precision claim or novelty claim transfers. The Poisson counterexample below is evaluated on the source family specified below, without asserting failure of that paper's inverse on its model. [Peřina Jr. et al., arXiv:1205.1969v1](https://arxiv.org/pdf/1205.1969v1)

The v1 landing page and primary PDF text were inspected, particularly the first two pages and source/detection moment relations. No public-PDF binary digest or visual-figure inspection is claimed. No empirical data from the paper are used.

Each calibration exposure has an unknown nonnegative integer pair count $N$, with positive finite mean $n$ and finite variance $v$. Exactly one photon of each pair reaches each declared arm input plane. Conditional on $N$, all photon detections are independent Bernoulli trials, with constant signal efficiency $p\in(0,1]$ and idler efficiency $q\in(0,1]$. The counters resolve photon numbers in count units without saturation. Both arm totals belong to the same exposures, and every exposure, including double zero, is retained. There are no individual-pair labels.

This is an exact population-moment inverse. It supplies neither an apparatus nor independently verified source purity, calibration transfer, repeated-exposure independence, uncertainty intervals, acquisition permission or measured efficiency.

## Forward moments with arbitrary brightness fluctuations

Let $X,Y$ be the detected signal and idler counts and write the five recorded quantities as
$$
 m_s=\mathbb E X,\quad m_i=\mathbb E Y,\quad
 V_s=\operatorname{Var}X,\quad V_i=\operatorname{Var}Y,\quad
 C=\operatorname{Cov}(X,Y).
$$
Conditional on $N$, $X$ and $Y$ are independent binomial counts with parameters $(N,p)$ and $(N,q)$. Total expectation, variance and covariance give
$$
 \begin{aligned}
 m_s&=pn,& m_i&=qn,\\
 V_s&=p(1-p)n+p^2v
     =m_s+p^2(v-n),\\
 V_i&=q(1-q)n+q^2v
     =m_i+q^2(v-n),\\
 C&=pqv. &&
 \end{aligned}                                                   \tag{1}
$$
In particular $C$ is not generally $pqn$. Replacing $v$ by $n$ would impose Poisson brightness and would fail for constant or other sub-/super-Poisson pair counts. In the constant-$N$ case the covariance is zero, although both efficiencies are positive.

Define
$$
 e_s=\frac{V_s-m_s}{m_s^2},\qquad
 e_i=\frac{V_i-m_i}{m_i^2},\qquad
 r=\frac{C}{m_s m_i}.
$$
The model requires
$$
 e_s=e_i=e=\frac{v-n}{n^2},\qquad
 r=\frac{v}{n^2},\qquad h:=r-e=\frac1n>0.          \tag{2}
$$
The difference removes the unknown brightness fluctuations exactly. Therefore the only possible efficiencies are
$$
 \boxed{
 p_*=m_s h=1-\frac{V_s}{m_s}+\frac{C}{m_i},\qquad
 q_*=m_i h=1-\frac{V_i}{m_i}+\frac{C}{m_s}.}       \tag{3}
$$
Both expressions use the equality of normalized excess variances in (2). The brightness moment candidates are
$$
 \boxed{n_*=\frac1h,\qquad v_*=\frac{r}{h^2}.}     \tag{4}
$$
The idler need not be independently calibrated: $q$ is inferred jointly. Matching the two totals to the same exposure remains essential for the covariance even though photon-pair matching is absent. The full brightness distribution is not determined by five moments.

## Necessary and sufficient pure-pair moment feasibility

For a finite real record, the following conditions are necessary and sufficient for some allowed integer-valued brightness law and efficiencies to reproduce exactly these five moments:

1. $m_s,m_i>0$, $V_s,V_i\ge0$, and $C\ge0$.
2. The normalized excess variances agree: $e_s=e_i=e$.
3. $h=r-e>0$, and $0<p_*=m_sh\le1,\ 0<q_*=m_ih\le1$.
4. With $n_*,v_*$ from (4), put $j=\lfloor n_*\rfloor$ and $f=n_*-j$. Require
$$
                 v_*\ge f(1-f).                \tag{5}
$$

The quantities must be finite. A zero covariance is allowed. Zero efficiencies or infinite brightness are not admitted limiting solutions. There is no additional upper bound on brightness variance because $N$ has no finite upper support. The covariance-matrix positivity restrictions follow from the construction below; they need not be treated as an independent sufficient certificate.

**Necessity of the integer boundary.** Every nonnegative integer $N$ satisfies
$$
 (N-j)(N-j-1)\ge0.
$$
At mean $n_*=j+f$, taking expectations yields (5). If $v_*=0$, this forces integer $n_*$, and $N=n_*$ almost surely. Thus a constant brightness is permitted exactly at its integer mean, not at an arbitrary real mean.

**Attainability.** The adjacent-integer law on $j,j+1$, with probabilities $1-f,f$, has mean $n_*$ and variance $v_{\min}=f(1-f)$. It attains equality in (5), including a deterministic integer at $f=0$. For any larger target $v_*$, choose a finite integer $L>n_*+v_*/n_*$. The law on $0,L$ with mass $n_*/L$ at $L$ has the same mean and variance
$$
 v_{\rm high}=n_*(L-n_*)>v_*.
$$
Mix these two mean-matched laws with weight
$$
 \tau=\frac{v_*-v_{\min}}{v_{\rm high}-v_{\min}}
$$
on the high-variance law. The result is supported on at most $0,j,j+1,L$, has positive finite mean, finite variance exactly $v_*$, and is nonnegative integer-valued. No asymptotic or noninteger population is needed.

Apply the independent Bernoulli losses at $p_*,q_*$. Its means and covariance agree by (2)–(4). Its signal variance is
$$
 m_s+p_*^2(v_*-n_*)
 =m_s+m_s^2(r-h)=m_s+m_s^2e=V_s,
$$
and similarly for the idler. This proves sufficiency for the recorded five moments and sharpness of (5).

Hence the set of efficiencies compatible with the pure-pair moment record is exactly the singleton $\{(p_*,q_*)\}$ when these checks pass, and empty otherwise. Feasibility certifies existence within the conditional model, not the physical truth of that model or compatibility with any unrecorded higher count statistics.

Two boundaries illustrate the cancellation. For Poisson brightness $v=n$, both marginal variances equal their means and (3) reduces to $p=C/m_i,\ q=C/m_s$. For constant positive integer brightness, $C=0$ and (3) instead gives $p=1-V_s/m_s,\ q=1-V_i/m_i$. Unit efficiencies are permitted. No Poisson brightness restriction is needed for the general inverse.

## Transfer to the accepted gravitational recoil inverse

The accepted registered recoil experiment determines
$\delta=J_c/(M_0cR)>0$ from two opposite free elastic backscatters with common incident frequency and common initial target rapidity, together with $H=R/(cT)$. It does so independently of burst counting efficiency. The full-rank two-burst record with one common unknown counting efficiency determines the effective channel action
$\widehat\gamma=\gamma/\epsilon$, where
$\gamma=GJ_c/(c^3R^2)$. Retain all accepted spectral-rank, positive-solution, geometry, tick, same-channel and baseline-registration checks.

Use the registered ratios $F=R_f/R$, $L=R/\ell$, scalar action $j=J_s/(M_0c\ell)>0$, and positive fixture slope $a_f$. Define
$$
 \widehat\mu=\widehat\gamma/\delta,\quad
 \widehat\kappa=\frac{a_fF}{2\widehat\mu},\quad
 \widehat\alpha_s=\frac{\widehat\mu L}{j}.
$$
Here $\mu=GM_0/(Rc^2)$ is a mass conversion, distinct from the calibration brightness $n$. The accepted ambiguity is
$$
 (\gamma,\mu,\kappa,\alpha_s)
 =(\epsilon\widehat\gamma,\epsilon\widehat\mu,
       \widehat\kappa/\epsilon,\epsilon\widehat\alpha_s),
 \qquad0<\epsilon\le1.                          \tag{6}
$$

If the pure-pair feasibility test passes **and** independent transfer registration establishes $\epsilon=p_*$ for the whole included burst population measure, then (6) becomes the unique tuple
$$
 \boxed{
 \gamma=p_*\widehat\gamma,\quad
 \mu=p_*\widehat\mu,\quad
 \kappa=\widehat\kappa/p_*,\quad
 \alpha_s=p_*\widehat\alpha_s.}                 \tag{7}
$$
It separates the tested fixture response from the mass conversion and scalar gravity strength without assuming $J_c=J_s$. The already efficiency-independent ratios
$$
 \kappa\mu=a_fF/2,\quad
 \kappa\alpha_s=a_fFL/(2j),\quad
 \gamma/\mu=\delta,\quad J_c/J_s=\delta L/j
$$
remain fixed. The scalar gravitational-length conversion is
$GJ_s/(c^3\ell^2)=\mu jL$. Blank and loaded fixture masses in baseline units retain the donor formulas with this same $\mu$.

This is absolute population registration, not an absolute length standard. Mass is obtained in units $Rc^2/G$ and actions in units $c^3R^2/G$; dimensional values still require absolute $R$, or an absolute tick and registered radius/tick transfer, with physical $c,G$. The common length/time, mass and action scaling of the donor remains when only dimensionless registrations are supplied. This calculation neither imports a universal photon action nor proves a universal fixture response.

Identifying $p_*$ with $\epsilon$ is not supplied by the count inverse. It requires independently registered spectrum, frequency weighting, direction and full angular/temporal coverage, collection modes, path, dead time, count response and applied settings. A scalar efficiency for exposure totals is insufficient if spectral loss changes the burst's frequency-weighted population moments. The reference-plane-to-count efficiency includes all losses after the reference plane; without separate path-transmission registration it is not an intrinsic detector efficiency.

## Pump-associated unpaired Poisson photons: full-law obstruction

Now make exactly the authorized source-purity relaxation. Let
$$
 M\sim{\rm Pois}(\lambda),\quad U\sim{\rm Pois}(u),\quad
 V\sim{\rm Pois}(v_b)
$$
be independent numbers of pairs, unpaired signal photons and unpaired idler photons, with all three rates positive in the example below. Every photon experiences the same arm loss $p$ or $q$. These unpaired photons are source/pump associated, not a separately known additive detector dark-count distribution.

Poisson splitting of pair outcomes and thinning of unpaired photons give independent latent detected counts
$$
 A_s\sim{\rm Pois}(p u+\lambda p(1-q)),\quad
 A_i\sim{\rm Pois}(qv_b+\lambda(1-p)q),\quad
 Z\sim{\rm Pois}(\lambda pq),
$$
with observed totals $X=A_s+Z,\ Y=A_i+Z$. These latent categories are a proof of the law; no individual pairs or categories become recorded features.

Set
$$
 A=\mathbb E X=p(\lambda+u),\quad
 B=\mathbb E Y=q(\lambda+v_b),\quad
 C=\lambda pq.
$$
For one generated pair the detection factor is $(1-p+pz)(1-q+qw)$. Compounding its Poisson count and the two unpaired Poisson counts gives the entire per-exposure probability generating function
$$
 \boxed{\mathbb E[z^Xw^Y]
 =\exp[(A-C)(z-1)+(B-C)(w-1)+C(zw-1)].}        \tag{8}
$$
In particular $V_s=A,\ V_i=B,\ \operatorname{Cov}(X,Y)=C$, and the complete observed count law depends only on $A,B,C$.

For fixed $0<C<\min(A,B)$, every efficiency pair satisfying
$$
 C/B\le p\le1,\qquad C/A\le q\le1
$$
is realized with nonnegative rates
$$
 \lambda=\frac{C}{pq},\quad
 u=\frac{Aq-C}{pq},\quad
 v_b=\frac{Bp-C}{pq}.                           \tag{9}
$$
Both unpaired rates are strictly positive when the corresponding lower bounds on $q,p$ are strict. Thus even the full histogram need not identify the efficiencies in this particular allowed source family. These are sharp ranges within this Poisson relaxation, not an analysis of arbitrary backgrounds.

Here is one exact same-law example, with $A=B=1,\ C=1/4$:

| Model | $p$ | $q$ | pair rate $\lambda$ | unpaired signal rate $u$ | unpaired idler rate $v_b$ |
|---|---:|---:|---:|---:|---:|
| Positive-background world A | $1/2$ | $1/2$ | $1$ | $1$ | $1$ |
| Positive-background world B | $3/4$ | $1/2$ | $2/3$ | $2/3$ | $4/3$ |
| Pure-pair interpretation | $1/4$ | $1/4$ | $4$ | $0$ | $0$ |

In both positive-background worlds the observed latent rates are
$(A-C,B-C,C)=(3/4,3/4,1/4)$, so (8) agrees at every count outcome. In particular the double-zero probability is
$$
 \Pr(X=0,Y=0)=e^{-7/4},
$$
with no discarded empty exposures. All losses and all three source rates in worlds A and B are strictly positive. The pure-pair interpretation also has exactly this full law. Its five moments pass the pure-pair feasibility test: $h=1/4,\ n_*=v_*=4,\ p_*=q_*=1/4$. Passing the test therefore does not certify pure-pair input.

The components may all vanish with the pump blocked in both worlds, so a pump-off dark-count measurement alone need not reveal this contamination. No measured background subtraction or source characterization is invented here. The construction establishes nonidentifiability for the authorized family, not a claim about every optical source or the cited paper's additional source model.

## Consequence of the same-law example for mass and fixture response

Register each world's actual signal efficiency as the common burst efficiency within that world. Use the accepted same-record rescaling (6) at $\epsilon_A=1/2$ and $\epsilon_B=3/4$, preserving the donor's recoil, burst, scalar and fixture records. The calibration exposure laws also agree by (8). Nevertheless
$$
 \frac{\mu_B}{\mu_A}=\frac32,\qquad
 \frac{\kappa_B}{\kappa_A}=\frac23,\qquad
 \frac{\alpha_{s,B}}{\alpha_{s,A}}=\frac32.
$$
The action scales change by the same factor as mass in this fixed-radius donor family, while recoil ratios and the registered native scalar ratios persist. The calibration record therefore does not remove the gravitational scale ambiguity once this source-purity relaxation is admitted.

For this particular record and restricted Poisson-background family, the sharp nonnegative-background range is $p\in[1/4,1]$. With verified transfer to the burst it would give
$$
 \mu\in[\widehat\mu/4,\widehat\mu],\quad
 \kappa\in[\widehat\kappa,4\widehat\kappa],\quad
 \alpha_s\in[\widehat\alpha_s/4,\widehat\alpha_s],
$$
with all values linked by the same $p$. Requiring both backgrounds strictly positive removes the $p=1/4$ endpoint. These conditional bounds are not a unique calibration; dropping even this source-family restriction would require a different argument.

## Observation registration

The older incomplete-counter donor uses matched detections of the same spatial event and a Poisson location process. Its overlap intensity is a recorded matched coincidence. Here the photons are distinct partners, brightness may be arbitrary, and only same-exposure totals and their moments are recorded. Neither spatial-Poisson assumptions nor same-event coincidence labels have been imported. The mean/variance subtraction in (2) is what removes arbitrary brightness fluctuations.

All exposures and failure/zero records remain in the denominator. Missing readout or unresolved preparation cannot be silently recoded as zero. Any independent corrections for dark counts or gain would require their own supplied uncertainty and applicability contract. Source purity, fixed independent losses, number resolution, absence of saturation and matched exposure boundaries require external evidence; the desired gravitational calibration cannot verify them from its own result.


The [free-recoil fixture inverse](fixture_mass_response_from_two_free_recoils.md) uses the [gravitating two-burst action](radiation_action_from_two_gravitating_bursts.md). The [incomplete spatial counter analysis](event_density_from_two_incomplete_counters.md) uses matched observations of the same event.
