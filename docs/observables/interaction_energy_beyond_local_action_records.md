# Interaction energy beyond local action records

The two registered preparations give exactly the same six action readings, and indeed the same full action histories on the specified interval, but distinct complete-carrier kinetic masses and terminal velocities. The missing datum is the classical relative correlation in the interaction energy. One initial real correlation reading resolves this ambiguity within the fixed two-preparation family. This conclusion uses the explicitly supplied total square-root Hamiltonian; it does not derive that Hamiltonian from the accepted boost theorem or DET.

## 1. Finite construction and source roles

The construction fixes one translation pair, two internal pairs, exactly two preparations, one smooth finite force pulse, six retained cells, one target response and one added initial-correlation reading. No extra mode, force experiment, sweep or cycle is used.

The [local boost relation](conditional_boost_mass_relation.md) proves a local quantum-matrix coefficient condition under supplied canonical and boost premises. It does not supply the all-orders classical dispersion used below. [Six casing positions and total inertial mass](six_casing_positions_and_total_inertial_mass.md) concerns Newtonian total-inertia inference from finite casing trajectories; [boundary displacements and vibrational energy](boundary_displacements_and_vibrational_energy.md) concerns graph-mode energy invisible to endpoint displacements. These motivate and delimit the question, rather than supplying its answer. The calculations below derive the result from the stipulated Hamiltonian.

## 2. Supplied state, positive energy and exact equations

Use real canonical pairs (X,P), (q1,p1), (q2,p2), with bracket {X,P}=1, {qj,pk}=delta_jk and all cross brackets zero. Define

```text
zj=(qj+i pj)/sqrt(2),    {zj,zk*}=-i delta_jk,
Nj=|zj|²,    N=N1+N2,    C=z1* z2+z2* z1=2 Re(z1* z2).
```

Internal qj,pj have sqrt(action) units and are not physical spatial positions or momenta. The supplied constants M0,c,omega,I,J are positive and finite, and 0<g<omega. Define

```text
E_star=M0 c²+omega N+g C,
H0(P,z)=sqrt(c² P²+E_star²).
```

The inequality |C|<=2|z1||z2|<=N gives, throughout the complete real state domain,

```text
E_star >= M0 c²+(omega-g)N >= M0 c² > 0,
H0 >= E_star > 0.
```

Thus both are smooth finite functions at every finite state and H0 has a strictly positive global lower bound. The interaction term gC need not be separately positive; the full internal quadratic term omega N+gC is nonnegative. No positivity of every bookkeeping component is required or asserted.

Set T=1/omega, s=t/T, h(s)=10s³-15s⁴+6s⁵ and

```text
F(t)=(J/T)h'(t/T),    Hdrive(t)=H0-F(t)X,    0<=t<=T.
```

This time-dependent linear potential implements a prescribed external force. It is not a closed actuator Hamiltonian and is not bounded below in X when F is nonzero. The positive carrier energy is H0, not Hdrive.

By differentiating H0 at fixed P or fixed internal state, Hamilton's equations are

```text
Xdot=c²P/H0,    Pdot=F(t),
z1dot=-i alpha(omega z1+g z2),
z2dot=-i alpha(omega z2+g z1),
alpha=E_star/H0.
```

The factor alpha multiplies both internal equations. Dropping it during the pulse would give the wrong phase evolution. These equations follow from {zj,Hdrive}=-i partial(H0)/partial(zj*) and the stipulated canonical normalization; no physical proper-time interpretation of alpha is needed.

E_star depends only on the internal variables. Since H0 is a function of P and E_star, and {E_star,P}={E_star,X}=0,

```text
dE_star/dt={E_star,H0-FX}=0.
```

This is conservation of the internal-plus-base scalar E_star under this translation drive, not conservation of H0 or Hdrive. Equivalently, {N,C}=0, so N and C are separately conserved under the stipulated H0 and external force. Individual Nj need not be conserved at a general state: direct differentiation gives

```text
N1dot=2g alpha Im(z1* z2),    N2dot=-2g alpha Im(z1* z2).
```

Their constancy for the two chosen preparations will be a result of their real relative correlation.

## 3. Exactly two finite trajectories

Let sigma be +1 or -1. Initially X=P=0 and

```text
z1(0)=sqrt(I/2),    z2(0)=sigma sqrt(I/2).
```

Therefore N(0)=I, C(0)=sigma I and the conserved scalar is

```text
E_sigma=M0 c²+(omega+sigma g)I.
```

Both E_sigma are positive, and E_+-E_-=2gI>0. These distinct initial total energies are compatible with identical initial bare actions; no identical complete preparation or identical preparation work has been asserted.

For w=z2-sigma z1, the full driven equations give

```text
wdot=-i alpha(omega-sigma g)w.
```

The initial value w(0)=0 implies w(t)=0. This establishes preservation of the normal-mode relation under the drive, rather than assuming the unforced normal-mode solution remains valid. Integrating Pdot gives

```text
P(t)=J h(t/T),
H_sigma(t)=sqrt(E_sigma²+c² J² h(t/T)²),
alpha_sigma(t)=E_sigma/H_sigma(t).
```

Define the finite phase integral

```text
phi_sigma(t)=(omega+sigma g) integral_0^t alpha_sigma(u) du.
```

An exact solution of the full internal equations is

```text
z1_sigma(t)=sqrt(I/2) exp[-i phi_sigma(t)],
z2_sigma(t)=sigma z1_sigma(t).
```

In real coordinates, q1=sqrt(I) cos(phi_sigma), p1=-sqrt(I) sin(phi_sigma), and (q2,p2)=sigma(q1,p1). The translational trajectory is exactly

```text
X_sigma(t)=integral_0^t c² J h(u/T)/sqrt(E_sigma²+c² J² h(u/T)²) du.
```

These integrals are a closed exact specification on the registered interval; no numerical approximation is needed for the observation or response decision.

Finite-domain checks are explicit. The polynomial satisfies h(0)=0, h(1)=1,

```text
h'(s)=30s²(1-s)²>=0,
h''(s)=60s(1-s)(1-2s),
```

so 0<=h<=1, 0<=P<=J and 0<=F<=15J/(8T). The force and its first time derivative vanish at both endpoints. On the finite interval all displayed trajectories are smooth, every internal real coordinate is bounded in magnitude by sqrt(I), and 0<=Xdot<c, hence 0<=X<cT for positive t<=T. If the force is extended by zero outside this interval, it is C1; no higher join smoothness is needed or claimed.

For both preparations and all t in [0,T],

```text
0 < a_min := E_-/sqrt(E_-²+c²J²) <= alpha_sigma(t) <= 1.
```

Here E/sqrt(E²+c²J²) is strictly increasing for positive E, so the lower bound covers both energies. Thus no internal time-factor singularity or stalled internal evolution occurs for these fixed positive finite parameters. In particular, phi_sigma and its derivatives on the finite interval are bounded, and H_sigma<=sqrt(E_+²+c²J²). This is a finite bound for the registered experiment, not a parameter-uniform resource bound for arbitrarily large I or J.

## 4. Complete retained record and response contrast

The exact solution gives N1_sigma(t)=N2_sigma(t)=I/2 throughout [0,T]. All six retained cells are therefore:

| Preparation | N1(0) | N2(0) | N1(T/2) | N2(T/2) | N1(T) | N2(T) |
|---|---:|---:|---:|---:|---:|---:|
| sigma=+1 | I/2 | I/2 | I/2 | I/2 | I/2 | I/2 |
| sigma=-1 | I/2 | I/2 | I/2 | I/2 | I/2 | I/2 |

Indeed retaining either bare-action history at every time in this interval would not distinguish these two preparations. The two internal phase histories, their initial relative sign, complete states and translation histories are not identical; those were expressly excluded from the reduced record. There is no assertion of equality of all observations or of physical preparations.

At the end of the same pulse P(T)=J for both. The signed terminal velocities are

```text
V_sigma=Xdot_sigma(T)=c²J/sqrt(c²J²+E_sigma²).
```

For J>0 and E>0,

```text
partial/partial E [c²J/sqrt(c²J²+E²)]
 =-c²J E/(c²J²+E²)^(3/2)<0.
```

Consequently 0<V_+<V_-<c for every stated choice of parameters. The same retained action record and same registered force thus admit two different target velocities.

At a fixed internal state, Taylor expansion at P=0 gives

```text
H0=E_star+c²P²/(2E_star)-c⁴P⁴/(8E_star³)+O(P⁶).
```

The defined zero-momentum kinetic mass is therefore

```text
Mkin=E_star/c²,
Mkin_sigma=M0+(omega+sigma g)I/c²,
Mkin_+-Mkin_-=2gI/c²>0.
```

This coefficient follows algebraically from the added full dispersion. It is not a derivation of that dispersion or a native mass relation. At nonzero terminal momentum J, the ratio J/V_sigma is H_sigma(T)/c², not the zero-momentum coefficient Mkin_sigma. No terminal impulse-over-speed identification of the latter is silently made.

The separation is strict for each fixed admitted parameter tuple. No finite-precision guarantee or uniform separation margin over all positive parameters is claimed; the record contract is exact.

## 5. Complete carrier force-work ledger

The internal contribution is fully retained. For each preparation, all entries in this table remain constant throughout the pulse:

| Component | sigma=+1 | sigma=-1 |
|---|---:|---:|
| Base scalar energy | M0 c² | M0 c² |
| Bare mode 1 contribution | omega I/2 | omega I/2 |
| Bare mode 2 contribution | omega I/2 | omega I/2 |
| Interaction contribution | +gI | -gI |
| Complete E_star | E_+ | E_- |

The negative interaction entry in the minus preparation leaves E_->M0 c² because omega>g. The full carrier energy is H_sigma(t), with translational excess K_sigma(t):=H_sigma(t)-E_sigma>=0. This is an exact bookkeeping split under the specified square root; it is not Newtonian P²/(2M) at finite momentum. There is no exchange between the bare mode actions in these normal-mode preparations, so this packet is not a closed excitation-transfer experiment.

Along the controlled trajectory, using the constant E_sigma and Pdot=F,

```text
dH0/dt=(c²P/H0)Pdot=F Xdot.
```

Thus the external force does complete carrier work

```text
W_sigma=integral_0^T F(t) Xdot_sigma(t) dt
 =sqrt(E_sigma²+c²J²)-E_sigma >0.
```

Endpoint accounting is

```text
H0(0)=E_sigma,
H0(T)=sqrt(E_sigma²+c²J²),
Delta(base)=Delta(bare1)=Delta(bare2)=Delta(interaction)=0,
Delta K_sigma=W_sigma.
```

The two drives have the same force waveform and impulse J, but their works differ because their translation histories differ. In fact d[sqrt(E²+c²J²)-E]/dE=E/sqrt(E²+c²J²)-1<0, so W_+<W_-. Equal impulse does not imply equal work. Both initial energy difference 2gI and the different delivered work must be retained when comparing final complete energies; no energy is created by comparing the two preparations.

For completeness, Hdrive has explicit time dependence. Its Hamiltonian derivative is

```text
dHdrive/dt=partial Hdrive/partial t=-Fdot(t) X(t).
```

There is no contradiction with dH0/dt=F Xdot: differentiating Hdrive=H0-FX gives exactly the same equation. Since F(0)=F(T)=0, endpoint Hdrive equals endpoint H0, and integration by parts gives

```text
-integral_0^T Fdot X dt = integral_0^T F Xdot dt = W_sigma.
```

This ledger concerns the specified carrier and the work entering through the prescribed external force. No total energy, momentum, material mechanism or thermodynamic cost of the force source is supplied. Nor are the work and resources of preparing the two distinct initial states given. The result neither closes those systems nor infers an engine, efficiency, heat law or empirical isolation.

## 6. The single added correlation reading

For the specified two preparations, the proposed extra initial scalar is exactly

```text
C(0)=+I or -I.
```

With I>0, it distinguishes the two allowed initial signs. Combining it with N(0)=N1(0)+N2(0)=I and the registered parameters gives

```text
E_star=M0 c²+omega I+g C(0),
Mkin=E_star/c²,
V(T)=c²J/sqrt(c²J²+E_star²).
```

Hence this one added scalar resolves the energy and response ambiguity in the fixed two-preparation family. A value other than +I or -I is incompatible with that family; this is not a classification of arbitrary internal states or a general tomography theorem. The task does not need to observe the evolving common internal phase to predict this target under the stated model.

A bare action reading is not the entire interacting internal energy. The missing term here is an ordinary classical cross correlation at fixed observed actions. Its role is not evidence for quantum coherence, a quantum/classical divergence, a new regime law or the DET ontology.

The registered M0 is essential to the absolute total-energy/mass inference. Without a registered base energy, the action and correlation data alone leave that contribution unknown. Unknown omega, g or action calibration also obstruct the numerical energy assignment; unknown c or impulse J obstruct the quoted mass or velocity conversion. This packet derives none of those standards. It does not infer actual energy from an uncalibrated display.

## 7. Units, distinct yield and limitations

Conventional dimensions are [X]=L, [P]=[J]=M L/T, [c]=L/T, [M0]=M, [qj]=[pj]=sqrt(M L²/T), [Nj]=[N]=[C]=[I]=M L²/T, [omega]=[g]=1/T, and [E_star]=[H0]=[Hdrive]=M L²/T². F has force units, F X has energy units, alpha is dimensionless and phi_sigma is dimensionless. The same supplied canonical action normalization is used in both preparations. No native action, time, mass, energy, propagation speed or force unit is calibrated by this construction.

The finite yield is an explicit failure of the retained six-action-cell record to determine whole-carrier response, together with one exact correlation augmentation for this pair. Both subsystem actions are observed, so the omission is not an entirely unobserved oscillator's energy as in the boundary-displacement graph-mode example. The response change comes from an interaction term and the added total translation law, not the casing example's visible-displacement aliasing or an unknown Newtonian constituent mass. There is no partner elimination, noise law or friction inference, and no extension of the distinct force-work-loop obstruction.

Spatial quantum scalar/native-sample/source-tensor constructions and initial Einstein-constraint matching are not inputs here. This model has no spatial internal scalar field, native growth or sample attachment, local relativistic stress tensor, source/support closure or gravitational equations. Its full square-root carrier dispersion is a supplied effective mechanical law, and no general relativity or physical particle realization is asserted. Use as a conventional mass-attribution benchmark requires complete interaction-energy/record registration before interpreting differing responses.

No finite construction here validates mass or gravity physically, establishes native DET units, authorizes empirical execution, derives the chosen law from ontology, or revives retired kappa-gravity. Physical preparation, a realizable actuator and measurement, calibration, finite error, and any gravitational interpretation remain additional questions rather than hidden premises.

For a native application, the native state, observables, energy/momentum and translation dynamics still need a justified identification with this model, together with physical scale calibration. A local relativistic or gravity application also needs a justified field/stress realization and source coupling. Empirical use needs preparation, actuation, measurement, uncertainty and the relevant complete-apparatus energy/momentum accounting. The finite observation result neither supplies nor refutes those further constructions. Neither the kinetic coefficient nor finite impulse-over-speed ratio is a measured gravitational mass.

## Reviewed basis

DET Classical supplied the finite derivation and a distinct nonblind scientific review. The reviewer's prospective control-design exposure was disclosed; the review independently checked the canonical normal coordinates, full driven equations, finite bounds, observation cells, kinetic coefficient and work ledger. DET Quantum Relativity reviewed the restricted recipient use as a classical observation benchmark, preserving the supplied total dispersion and physical-accounting limits.
