# Absolute sector masses from a spring record, one store line and a finite named test

**Conditional result.** One observed gain fixes all three absolute masses. If every trial is silent, every pretest candidate remains possible. Equal adjacent gaps give a single candidate before any trials. Unequal gaps give ten or eleven. In each candidate world only two trials can click, irrespective of how many other settings are tested.

## 1. Exact inputs and physical registration

The spring input is the complete ideal population record in the three labelled settings $01,02,12$. Each pair consists of two independent carriers, prepared in sectors $0,1,2$ by selecting respectively $A=00,B=10,D=11$. The other middle state is $C=01$. Both middle states have mass $M_1$. Each carrier undergoes two native births and its marked history is $h=(z,b_1,b_2)$, $z\in\{E,F\}$, $b_i\in\{0,1\}$. Write
$$
(q_E,q_F)=(2/3,1/3),\qquad
(\eta_E,\eta_F)=(1/8448,-1/4224),\qquad
p_i(h)=\frac{q_z}{4}\left(1+\frac{\eta_z}{2}\mathbf1_{\{i=1\}}\right).
$$
Each of the 192 labelled cells must have the prescribed probability and a deterministic extension reading. The input must satisfy
$$
P((i,j),h,h',y\in B)=\tfrac13 p_i(h)p_j(h')\mathbf1_{\{y_{ij}\in B\}} .
$$
Here $B$ is any set of readings. There are four bit pairs for each mark. The identities $\sum_z q_z=1$ and $\sum_z q_z\eta_z=0$ normalize each $p_i$, hence the full record. Every history pair appears with its original weight in every setting. A missing setting, a wrong label or weight, or variation of the reading within a setting rejects a proposed exact input.

Use the registered spring with a stable signed extension ratio, rest release, positive common stiffness $K$, common positive tick $T$, and $0<\omega_{ij}T<\pi$ in each admissible world. Neither $K$ nor $T$ has an absolute calibration. The store input is a *single certified detection* at physical spacing $W$, finite and strictly positive. It certifies membership in the set of positive store lines. Its cause, rank, multiplicity, and other line positions or absences are unavailable. Condition the design on this datum. There is no seed likelihood to multiply into the experiment's law.

Use the same fixed, labelled, strictly ordered masses $0<M_0<M_1<M_2$ in all settings and trials. The sector inertias in the spring are the very masses assigning rest energies $M_0c^2,M_1c^2,M_1c^2,M_2c^2$ to the four store-arm labels in a common rest frame. The conversion $c>0$ is known. This identification, the carrier and slot registrations, stable preparations and the independent energy standard for $W$ and each store setting are physical premises. Native count conservation alone supplies none of these calibrations.

## 2. Inverting the population spring record and the seed

Require finite $-1<y_{ij}<1$. In the specified phase domain the equations for $d_{ij}=(\arccos y_{ij})^2$ are $d_{ij}=u_i+u_j$, where $u_i=KT^2/M_i$. Inverting gives
$$
u_0=(d_{01}+d_{02}-d_{12})/2,\quad
u_1=(d_{01}+d_{12}-d_{02})/2,\quad
u_2=(d_{02}+d_{12}-d_{01})/2 .
$$
Require $u_0>u_1>u_2>0$. This enforces positive finite, strictly ordered masses, including the strict squared-phase triangle conditions. Equality of two $u_i$, a zero $u_i$, or an endpoint $y_{ij}=\pm1$ is outside the domain. Write $r_i=u_0/u_i$. The spring allows exactly
$$
(M_0,M_1,M_2)=m(1,r_1,r_2),\qquad m>0 .
$$
For each $m$, taking any $T>0$ and $K=m u_0/T^2$ gives exactly the three input readings and their full history law. This is common $K,T$ across settings within one world. Unknown calibration permits the product to differ between candidate worlds.

Put $\alpha=r_1-1>0$, $\beta=r_2-r_1>0$. The two ordered energy gaps are $a=mc^2\alpha$ and $b=mc^2\beta$. On three carriers with occupation $j$ and number $d$ of $D$'s, the rest energy is $3mc^2+aj+(b-a)d$. A positive line is an attainable positive energy drop per lost count $\Delta j>0$. Use the admitted eleven distinct $\Delta d/\Delta j$ positions
$$
\mathcal T=\{-1,0,1/4,1/3,2/5,1/2,3/5,2/3,3/4,1,2\}.
$$
For each $t$, the putative line is $mc^2[\alpha+(\beta-\alpha)t]$. Each positive position has a joint transposition witness in the full-permutation class. The seed says only that one such position equals $W$. Form the set of distinct positive numbers
$$
D=\{\alpha+(\beta-\alpha)t:t\in\mathcal T\}\cap(0,\infty).
$$
The exact pretest **baseline mass set in physical units** and triplets are
$$
\mathcal M=\{W/(c^2 d_*):d_*\in D\},\qquad
\{m(1,r_1,r_2):m\in\mathcal M\}.
$$
Necessity follows from the seed equation. Conversely, for each retained $d_*$ a witnessing pair makes $W$ an attainable line for that mass, and the choice of $K,T$ above realizes the spring record. Both arms use the same masses. Candidate count does not count multiple witnesses or repeated positions. A common additive mass shift would leave store energy differences unchanged, but preserving $M_1/M_0=r_1>1$ under a shift $h$ requires $(r_1-1)h=0$. Thus there is no further free offset. The unknown absolute spring scale is restricted to the discrete choices $m u_0$.

Let $l=\min(\alpha,\beta)$, $v=\max(\alpha,\beta)$. Equal gaps $l=v>0$ give $D=\{l\}$, so the spring ratios and seed alone determine $m=W/(c^2l)$. For unequal gaps the affine map on $\mathcal T$ is injective. Each of the nine $t$ in $[0,1]$ gives a positive position. The two outer positions are $2v-l>0$ and $2l-v$, irrespective of gap orientation. Hence $N=|\mathcal M|=11$ for $l<v<2l$, and $N=10$ for $v=2l$ or $v>2l$, where the low outer value is zero or negative, respectively. Strict positivity applies to the computed energy position, so an outer coefficient of $-1$ can still supply a valid seed. For valid spring data $D$ contains $\alpha,\beta$. Every finite $W>0$ therefore has an explanation. Invalid pretest data have an empty compatible set.

## 3. A preset finite experiment and its normalized law

For every $m\in\mathcal M$ schedule the physical setting $w_m=mc^2\alpha$. These settings are distinct because $\alpha>0$. Order them increasingly as $w_1,\ldots,w_N$. Preset two fresh, independent trials at each setting, in that order, and take the entire schedule. Each uses three independent carriers, each with its original two marked births, the stationary preparation $\rho(A,B,C,D)=(5,4,4,1)/14$, and an independent fresh store at level 6 of $0,\ldots,12$ with $E_{\rm store}=e_0+sw_k$. Counts are $J(A,B,C,D)=(0,1,1,2)$ per label, added over the three slots.

The additional actuator premise extends the admitted named diagnostic at a certified second-largest line. At **each** calibrated candidate setting it effects the full transposition $(BAA,6)\leftrightarrow(AAA,7)$ exactly when conservation permits, and otherwise acts as identity. It fixes the other 830 joint states and never uses a measured history or hidden label to choose a control. Count totals coincide, $1+6=0+7$. Carrier rest energy drops by exactly $a$ forward and the store gains $w_k$. The reverse changes both signs. The carrier and store energy zeros cancel, and other material, motion, interaction, support and actuator energies stay fixed. Thus equality of total energy is precisely $w_k=a$. The reverse endpoint belongs to the joint bijection despite its zero preparation probability. On the level-6 slice a carrier-only map can send both $BAA$ and $AAA$ to $AAA$, with distinct final store levels. The physical ability to implement this sharp selective response and register the level without false positives, missed events or hidden energy is supplied independently of the mathematical conservation test.

For a store trial let $H=(h_1,h_2,h_3)$, $h_i=(z_i,b_{i1},b_{i2})$, and let $x$ be the carrier string at the end of the native births, *before* the control. The accepted stationary law is
$$
Q(H)=\prod_{i=1}^3(q_{z_i}/4),\qquad
P(H,x)=Q(H)\prod_{i=1}^3\rho(x_i).
$$
This sums to one across all $8^3$ complete histories and all $4^3$ strings. Appending the deterministic indicator for the joint output of the selected permutation sends each old $(H,x)$ term to a unique output. If microscopic native paths are retained, the same indicator multiplies their original path weights. Every originally forbidden native path remains zero. In particular, a terminal $B$-to-$A$ change under the actuator occurs *after* both births.

Write $p=4\cdot5\cdot5/14^3=25/686$, the conditional probability of the one ordered string $BAA$ for every $H$. Its value includes neither permutations of slots nor an extra $C$ label. In the world of baseline $m$, put $I_k=\mathbf1_{\{w_k=mc^2\alpha\}}$. For terminal store level $s'$ the full fixed-setting law is
$$
P_m(H,s'\mid w_k)=Q(H)\,f_{m,k}(s'),\qquad
f_{m,k}(s')=
\begin{cases}
p I_k & s'=7,\\
1-p I_k & s'=6,\\
0 & \text{otherwise}.
\end{cases}
$$
Hence $f$ also gives the conditional level law for each particular history. Level 6 includes the $1-p=661/686$ on-resonance probability and unit off-resonance probability. Other positive *unlabelled* lines can exist at off-resonance settings while this named control is silent. For the entire labelled log $\mathcal L=((H_{kn},s'_{kn}))_{k=1,\ldots,N;\ n=1,2}$,
$$
P_m(\mathcal L\mid\text{spring input},W,\text{preset settings})=
\prod_{k=1}^N\prod_{n=1}^2 Q(H_{kn}) f_{m,k}(s'_{kn}).
$$
Every factor is normalized. This uses independence between repetitions and settings conditional on the fixed mass world. The settings are deterministic and there is no probability distribution on the mass alternatives.

## 4. Sharp inverse for every complete log

Check the pretest, the exact ordered preset list and its two labelled trials per setting. Each trial must contain three correctly formed complete marked histories and a store level. Missing, duplicate or extra trial slots, wrong settings, incomplete or invalid marks, or a level outside $\{6,7\}$ fail the full-record contract. Identical *outcomes* in two correctly labelled trials are allowed. Malformed full records have no explanation under this contract. For valid format let $G$ be the set of distinct settings with at least one level-7 observation.

| Observed gain settings | Compatible baseline mass set |
| --- | --- |
| $G=\varnothing$ | All of $\mathcal M$ |
| $G=\{w\}$ | $\{w/(c^2\alpha)\}$ |
| $\lvert G\rvert\ge2$ | Empty |

Multiply each returned mass by $(1,r_1,r_2)$ to recover the corresponding absolute triplet. Only one setting resonates in any world. At that setting both levels have strictly positive probability for every valid $H$. Every other setting gives level 6 with certainty for every valid $H$. These facts prove both exclusions and attainability in the table by the displayed product law, including a double click at one spacing. For the entirely silent log the joint probability is $(1-p)^2\prod Q(H_{kn})>0$ in *each* world. Even the individual silent-history likelihoods agree across all candidates.

Conditional on any admissible world, the chance of at least one click over the **whole** schedule is
$$
1-(1-p)^2=1-(661/686)^2=33675/470596 .
$$
With unequal gaps this is also the probability of unique mass certification, and the ambiguity probability is $436921/470596$. With equal gaps, $\mathcal M$ is a singleton before probing. Certification then has probability one, although a click still has probability $33675/470596$ and both trials still run. Inconsistent records have probability zero in every admitted world. If instead the exact normalized response laws at the same settings were supplied, exactly one setting would have level-7 probability $p$ and all others zero. That exact vector determines $m$ in every world. A putative population vector must match the full law of a returned world, including its history factors and independence where the joint schedule law is claimed. Two silent trials at a setting supply no exact zero-probability certificate.

## 5. Forward and inverse check at the zero outer line

Let $m_*>0$ be a fixture mass. Generate $M=m_*(1,2,4)$ and take $KT^2=m_*$ *only in this forward check*. The squared phases are $(3/2,5/4,3/4)$ in settings $01,02,12$, all strictly in $(0,\pi^2)$. Give the observer the three $y_{ij}=\cos\sqrt{d_{ij}}$ in the specified spring cells and only a certified $W=3m_*c^2$. No source or rank is attached to $W$.

Inversion gives $u=(1,1/2,1/4)$, $(\alpha,\beta)=(1,2)$. The eleven coefficients yield one zero outer value and the ten distinct positives
$$
D=\{1,5/4,4/3,7/5,3/2,8/5,5/3,7/4,2,3\}.
$$
Each candidate is $m=W/(c^2 d_*)$. For example $d_*=3,2,1$ give $m=m_*,3m_*/2,3m_*$, respectively. The three worlds all reproduce the same seed and all 192 spring cells by taking $KT^2=m$. In the first world $W$ is the high outer line, in the second it is the second adjacent gap, and in the third it is the first adjacent gap. These possible sources are part of the verification only.

Write $U=W/3$ in energy units. The ordered settings are $U$ times
$$
1,\ 3/2,\ 12/7,\ 9/5,\ 15/8,\ 2,\ 15/7,\ 9/4,\ 12/5,\ 3 .
$$
There are 20 trials. For a concrete positive log take every single-carrier history to be $(E,0,0)$, and record level 7 on the first trial at $U$ and level 6 on every other trial. Each of the 60 individual histories has probability $1/6$. This log has probability $6^{-60}p(1-p)$ in the generating world and zero elsewhere. Its mass triplet is $(U/c^2)(1,2,4)$. Keeping those histories and replacing that one level 7 by 6 produces a log of probability $6^{-60}(1-p)^2$ in every one of the ten worlds. The fixture therefore exhibits ambiguity on a supported complete native record at the strict zero-line boundary $v=2l$.

**Scope.** This is a fixed budget of $2N\le22$ post-seed store trials, with one fresh store and three two-birth carriers in every trial. It bounds neither acquisition of the exact spring input and certified seed nor calibration, selective tuning, restoration, laboratory time or waiting for a click. The stipulated experiment ends after its preset observations, including all silent ones. Its conclusions concern exact data and ideal registration. No implementation, general line-search capability, empirical outcome or efficiency has been established.

**Source basis.** The labelled spring inversion supplies the mass ray. The accepted store catalogue supplies the eleven coefficients and the earlier single-setting diagnostic. The full joint-store criterion and CL073 supply the conserved ledger and conditional native label law.

## Use in a gravitational mass comparison

A finite store log can supply an absolute inertial mass if its mass labels and energy calibration carry over to the receiving experiment. The [three-sector spectroscopy test](sector_spectroscopy_and_endpoint_weighing.md) already decides proportionality from ratios under its held-level model. An absolute mass certificate alone cannot remove a middle-level shift caused by the holder.

## Scientific review

Classical supplied the proof. Its independent scientific reviewer verified the finite log, including all silent trials. DET Quantum Relativity independently checked how the certificate transfers to a mass comparison. The coordinator accepted the conditional result on 9 November 2026 HST.

- Classical control SHA-256: `2c942596bf64126293affd32594c7258d1b69e03bc8c407df351400fced24c2a`.
- Author report SHA-256: `bfa499901e9f417127e0f17217c92543d81434ecc6cae04f0fd57dbf1dbee530`.
- Author freeze SHA-256: `bb0c9aa50c7dfdecc7d7fce7d23ed726d722c09ce4880acd45e2a341dec273a5`.
- Independent scientific review SHA-256: `59fbb4dbea09d3dff38dd5187b854dc2fbf49bb1ce85933605dd7f36b4309be0`.
- Donor disposition SHA-256: `2c641fc28f5ae82397843fa82d96c88a67edd97741c6ddf5a304556bc75d318d`.
- QR recipient assessment SHA-256: `9715928fcd9500b04cc47f9216d6f77bc4cd95b28fbd20368dc7820374e08670`.
