# How accurately must the second sampling time be known to identify mass?

**Theorem.** Put $r=\sqrt2$. A single timing ratio $\alpha$, fixed over the whole ensemble, is certified only to belong to $[r-\varepsilon,r+\varepsilon]$, where $0\le\varepsilon\le1/5$. On the phase band $0<x=\omega T\le4\pi$, every compatible full CL071 population covariance record identifies one inertial mass if and only if
$$
                         0\le\varepsilon<\sqrt2-\frac43 .
$$
This is a strict tolerance on the **half-width** of the time ratio. In time units the second sampling time is certified within $\varepsilon T$ of $\sqrt2 T$. At the threshold the full record can already admit masses differing by a factor of four. Wider intervals still permit a finite decision for each individual record.

## Observation law and finite inverse for any given record

Retain the calibrated one-dimensional canonical harmonic preparation with known $\Theta,T>0$, known displacement scale and trap center, and positive finite stiffness $k$ and inertia $m$. Three ordered, nondisturbing reads at $0,T,\alpha T$ follow the same isolated trajectory in each draw. In CL071 the position is $q(t)=U\cos(\omega t)+V\sin(\omega t)$, with independent centered Gaussian $U,V$ of variance $S=\Theta/k$ and $\omega^2=k/m$. The four exact population numbers are
$$
 (S,A,B,D)=S\big(1,\cos x,\cos(\alpha x),\cos(\alpha x-x)\big),\qquad
 k=\Theta/S,\quad m=\Theta T^2/(Sx^2).
$$
The last entry is the covariance between the two later positions. The three normalized unit vectors at angles $0,x,\alpha x$ give the complete covariance matrix by their pairwise dot products and the common variance. This matrix determines the centered Gaussian law, including at deficient rank. The qualified Classical author result, independent review and disposition are used together. Their physical time and preparation energy are externally supplied. The six earlier spring-work calibration settings contribute no observation here.

For any proposed finite tuple, the following test returns *all* feasible phases and hence all masses.

1. Require $S>0$ and $|A|,|B|,|D|\le S$. Put $a=A/S,\ b=B/S,\ d=D/S$ and $\theta=\arccos a\in[0,\pi]$.
2. Take the distinct members of $\{\theta,2\pi-\theta,2\pi+\theta,4\pi-\theta\}$ in $(0,4\pi]$. At $a=1$ these are $2\pi,4\pi$. At $a=-1$ they are $\pi,3\pi$.
3. For each candidate $x$, form $y=2\pi h\pm\arccos b$ for $h=0,1,2,3$. Retain $x$ if at least one $y$ satisfies
$$
                 (r-\varepsilon)x\le y\le(r+\varepsilon)x,\qquad
                 \cos(y-x)=d .
$$
   The timing endpoints are closed. The list exhausts the possibilities because $0<y\le(r+1/5)4\pi<7\pi$, and $\arccos b\le\pi$. Repeated roots may be discarded.
4. Each retained $x$ returns $m=\Theta T^2/(Sx^2)$, with $k=\Theta/S$. Its timing witness is $\alpha=y/x$. An empty set means the tuple is incompatible. Multiple timing witnesses for the same phase count as one mass.

Necessity follows by solving the first two cosines and checking the later-pair entry. Conversely a retained pair $x,y$ and its positive parameters realize the entire record through the specified Gaussian preparation. Thus the test also rejects invalid Gram matrices without a separate rank or positivity shortcut.

## Which timing errors can give two masses?

For two compatible worlds with the same $S,\Theta,T$, unequal masses correspond exactly to unequal positive phases $x,x'$. Normalize their phases to cycles $u=x/(2\pi)$, $v=x'/(2\pi)$, ordering them $0<u<v\le2$. Write their respective admissible timing ratios as $\alpha,\beta$. The two augmented records agree if and only if there are a single sign $\sigma\in\{+1,-1\}$ and integers $n,j$ such that
$$
                  v-\sigma u=n,\qquad \beta v-\sigma\alpha u=j.             \tag{1}
$$
Indeed equality of the two dot products with the initial unit vector fixes each of the other angles up to reversal and full periods. The remaining dot product fixes the product of their sine components, so if both components are nonzero the two reversals must have the same sign. If either sine vanishes, its angle admits both signs modulo $2\pi$, and can take the sign used by the other angle. If both vanish either common sign works. Rank one can occur at a rational ratio in the interval. No division by a sine or nonsingularity assumption enters (1). Conversely a common rotation by whole periods or simultaneous reflection as in (1) preserves all three dot products. The first vector remains fixed.

**Same orientation, $\sigma=+1$.** The only positive integral difference is $v-u=1$. A difference of 2 would require the excluded $u=0$. Write $\alpha=r+e,\ \beta=r+f$, $|e|,|f|\le\varepsilon$. Then
$$
                \beta v-\alpha u=r+fv-eu .
$$
At these fixed $u,v$, the attainable values form the closed interval centered at $r$ of radius $\varepsilon(v+u)$. The errors in two competing worlds may differ. Since $v+u=2v-1\le3$, reaching an integer requires $\varepsilon\ge\operatorname{dist}(r,\mathbb Z)/3=(r-1)/3$. This bound for the positive-sign branch is attained with $u=1,v=2$ and opposite endpoint errors chosen to lower the expression to 1.

**Reflected orientation, $\sigma=-1$.** Now $u+v=n\in\{1,2,3\}$. The value 4 would force $u=v=2$, hence the same mass. For fixed $n$,
$$
                     \frac{\beta v+\alpha u}{n}
                     =\frac{v}{n}\beta+\frac{u}{n}\alpha
                     \ \in [r-\varepsilon,r+\varepsilon] .
$$
Every point of this closed interval is attainable, by taking both timings equal to it. Therefore (1) is possible for that $n$ exactly when the certified interval contains some $j/n$, provided the unequal phases exist. Each $n=1,2,3$ splits into two unequal positive numbers at most 2 (for example $1/4+3/4,\ 1/2+3/2,\ 1+2$, respectively). The least half-widths for these three denominators are
$$
 \begin{array}{c|ccc}
 n&1&2&3\\ \hline
 \text{nearest }j/n & 1 & 3/2 & 4/3\\
 \text{required half-width} & r-1 & 3/2-r & r-4/3 .
 \end{array}
$$
The smallest of the four branch thresholds is $r-4/3$. In particular it is smaller than $3/2-r$ since $r<17/12$, and smaller than $(r-1)/3$ since $r<3/2$. It lies strictly between 0 and $1/5$. This exhausts the congruences for distinct phases, including competitors whose actual timings differ. Below the threshold each compatible record therefore has exactly one mass.

## Boundary record and loss of the uniform guarantee

At $\varepsilon=r-4/3$ the lower timing endpoint is $\alpha=4/3$. Take this **same** timing in both worlds, with $x=2\pi$ in the first and $x'=4\pi$ in the second. The reflected phases have cycle sum 3, and their timed cycle sum is 4. Both are allowed by the half-open band. They give the identical tuple
$$
                           (S,A,B,D)=S(1,1,-1/2,-1/2)
$$
for any chosen $S>0$. Both worlds have $k=\Theta/S$, while their respective masses are $\Theta T^2/(4\pi^2 S)$ and $\Theta T^2/(16\pi^2 S)$. Here the reading at $T$ repeats the initial position. The third projection and the full singular joint Gaussian law are consistent with the tuple. Because the same timing remains admitted in every wider certified interval, the example proves failure of the uniform guarantee at and above the threshold. It need not make all records ambiguous.

## Calibration and accepted scope

The certified interval describes one unknown constant of the acquisition schedule. It is neither an independent timing deviation on each draw nor a bound on sampling error in the covariances. The result uses exact matched population statistics. It gives no finite-sample resolution guarantee for nearby records.

With unknown $\Theta$, the phase test still holds, and the data give $k/\Theta=1/S$ and $m/\Theta=T^2/(Sx^2)$ on each surviving branch. Scaling $\Theta,k,m$ together by any positive factor preserves the complete position law. An absolute mass uses the supplied preparation energy, displacement calibration and physical first time. The native phase/action interface leaves the physical rate and time per birth external. The independent spring-work/echo study uses its own stiffness transfer, paths, work gains and timing references. No common carrier, clock or work-to-thermal energy calibration is established by this comparison.

## Reviewed sources

The preparation and trajectory model come from Classical CL071/v1, including its independent review and the qualification on physical time. DET Quantum Relativity derived the timing bound. DET Relational State Research independently verified both phase orientations, the boundary collision and the finite inverse. The related [native phase and action interface](native_phase_action_interface.md) and [spring work scale](spring_mass_scale_in_displayed_work.md) give the calibration assumptions for those separate models.
