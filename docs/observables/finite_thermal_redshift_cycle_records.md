# Finite thermal-redshift cycle records

The supplied three-state process gives the two exact record laws

$$
 (P_+,P_-,P_*)_A=(I_A/2,I_A,1-3I_A/2),\qquad
 (P_+,P_-,P_*)_B=(I_B/2,I_B/2,1-I_B),
$$

where

$$
 I_A=\frac{16}{9}e^{-2}-\frac{16}{49}e^{-3}
       -\frac{304}{441}e^{-5/4},\qquad
 I_B=\frac{16}{25}e^{-2}-\frac{16}{81}e^{-3}
       -\frac{176}{2025}e^{-3/4}.
$$

Both cycle probabilities and both remainder probabilities are strictly positive. Thus the finite laws differ: the oriented ratio is 1/2 for A and 1 for B. This statement concerns complete, exactly-three-jump events at the specified finite horizon. It neither assumes nor proves equilibrium. The heat ledger below is an independent consequence of the supplied energy/bath assignment, not an inference of heat from a probability ratio.

## 1. Fixed premises and provenance

The public abstract of Tolman and Ehrenfest, *Temperature Equilibrium in a Static Gravitational Field*, Physical Review 36, 1791 (1930), [DOI 10.1103/PhysRev.36.1791](https://journals.aps.org/pr/abstract/10.1103/PhysRev.36.1791). Its sole role here is the established static equilibrium comparator that lapse times local proper temperature is constant. Only the public abstract is used; the finite process, gaps, rates and physical interpretation are supplied assumptions.

Take positive finite E, k_B and gamma. The prescribed dimensionless lapses are N_L=1 and N_U=2, with dτ_i=N_i dt. The states are 0, L and U, initially 0. Their Killing charges are H(0)=0 and H(L)=H(U)=E. The local occupied gaps are epsilon_L=E and epsilon_U=E/2. Each bath's proper-time downward rate is gamma and upward rate is gamma exp[-epsilon_i/(k_B T_i)]. The reciprocal L/U channel has independently supplied common-time rate gamma in both directions and zero net Killing-energy change. These are classical effective test-system assignments, not native DET dynamics or a derived transport mechanism.

The only preparations are A, with T_L=T_U=T_0=E/(k_B ln4), and B, with T_L=T_0 and T_U=T_0/2. B has N_L T_L=N_U T_U=T_0; A does not. In both preparations the only observation horizon is t_f=1/gamma. The outcomes + and - require exactly three jumps in the prescribed orders; * contains every other trajectory. There is no conditional selection on a final or thermalized state.

## 2. Common-time generators and existence of the path law

Multiplication of a proper-time bath rate by N_i converts it to common time. For L, the Boltzmann factor is 1/4 in both preparations, so q_0L=gamma/4 and q_L0=gamma. For U, the factor is 1/2 in A and 1/4 in B, giving q_0U=gamma in A and gamma/2 in B, while q_U0=2 gamma in both. The reciprocal channel rates are q_LU=q_UL=gamma, already in common time.

In row convention and order (0,L,U),

$$
 Q_A=\gamma\begin{pmatrix}
 -5/4&1/4&1\\
 1&-2&1\\
 2&1&-3
 \end{pmatrix},\qquad
 Q_B=\gamma\begin{pmatrix}
 -3/4&1/4&1/2\\
 1&-2&1\\
 2&1&-3
 \end{pmatrix}.
$$

Every off-diagonal entry is positive, each row sums to zero, and the exit rates in state order are gamma(5/4,2,3) for A and gamma(3/4,2,3) for B. The local up/down rate ratios retain their Boltzmann values after clock conversion, because the same lapse multiplies both rates at each bath. This is the supplied local detailed-balance interpretation; no microscopic derivation is claimed.

For either displayed generator, R=I+Q/(3 gamma) is a stochastic matrix. A Poisson clock of rate 3 gamma with transition matrix R constructs the same CTMC after ignoring self marks. There are almost surely finitely many such marks before t_f, so the process is nonexplosive and has a normalized complete path law. This is an existence and normalization argument, not an additional preparation, simulation or numerical programme.

## 3. Ordered-time laws with every survival interval

Write u_j=gamma t_j and let

$$
 D=\{0<u_1<u_2<u_3<1\},\qquad
 (d_0,d_1,d_2,d_3)=(u_1,u_2-u_1,u_3-u_2,1-u_3).
$$

All four dwell intervals are nonnegative and sum to 1; boundary events have measure zero. For compact notation only, let (a_A,b_A)=(5/4,1) and (a_B,b_B)=(3/4,1/2). These denote the fixed empty exit rate divided by gamma and fixed 0→U rate divided by gamma for the two preparations, not additional cases or variable controls.

For s=A or B, the complete density of the + event on D is

$$
 f_{s,+}(u)=\tfrac12
   \exp[-a_s d_0-2d_1-3d_2-a_s d_3],
$$

and the complete density of the - event is

$$
 f_{s,-}(u)=b_s
   \exp[-a_s d_0-3d_1-2d_2-a_s d_3].
$$

The factors 1/2 and b_s are the respective products of the three dimensionless jump rates. The three powers of gamma from dimensional rates cancel the three inverse powers from dt_1 dt_2 dt_3. The first and last exponent terms include survival before the first and after the third jump. The middle exit rates include all competing exits, including exits that would defeat the requested order. Consequently these are exactly-three-jump probabilities, not products of jump-order branching probabilities or endpoint probabilities.

Define the two, and only two, integrals

$$
 I_s=\int_D
  e^{-a_s(d_0+d_3)-2d_1-3d_2}\,du_1du_2du_3,
 \qquad s=A,B.
$$

Then P_{s,+}=I_s/2. The reversal in section 4 proves P_{s,-}=b_s I_s with the waiting factors included.

For an explicit evaluation, put x=d_1, y=d_2 and z=d_0+d_3=1-x-y. At fixed x,y, integration over the allowed d_0 has length z. Thus, for each of these two fixed a_s,

$$
 I_s=\int_{x,y\ge0,\ x+y\le1}
 (1-x-y)e^{-a_s(1-x-y)-2x-3y}\,dxdy
 =\int_0^1 z e^{-a_s z}
       [e^{-2(1-z)}-e^{-3(1-z)}]\,dz.
$$

The bracket follows by integrating x from 0 to 1-z with y=1-z-x. In particular, no waiting factor was discarded when combining the two empty-state intervals. With the elementary integral

$$
 J(c)=\int_0^1 z e^{cz}\,dz
     =\frac{e^c(c-1)+1}{c^2},
$$

the fixed evaluations are

$$
 I_A=e^{-2}J(3/4)-e^{-3}J(7/4)
 =\frac{16}{9}e^{-2}-\frac{16}{49}e^{-3}
   -\frac{304}{441}e^{-5/4},
$$

$$
 I_B=e^{-2}J(5/4)-e^{-3}J(9/4)
 =\frac{16}{25}e^{-2}-\frac{16}{81}e^{-3}
   -\frac{176}{2025}e^{-3/4}.
$$

These positive integral representations, rather than subtraction of the exponential terms, establish I_A,I_B>0. The three disjoint events +, - and * partition the normalized path space. Therefore their complete laws are precisely the two laws stated at the start, with P_*=1-P_+-P_-≥0. More strongly, the no-jump event belongs to *, has probability e^{-5/4} in A and e^{-3/4} in B, and hence makes each P_* strictly positive. Normalization is inherited from the actual CTMC, not imposed on weights that omit a rate or survival factor.

## 4. Explicit reversal and finite discrimination

Map the + trajectory with jump times u to the - trajectory with

$$
 \mathcal R(u_1,u_2,u_3)=(1-u_3,1-u_2,1-u_1).
$$

This is a bijective involution of D, has absolute Jacobian 1 and reverses the entire dwell list: (d_0,d_1,d_2,d_3) maps to (d_3,d_2,d_1,d_0). The reversed state sequence is 0→U→L→0. Initial and final empty-state dwell intervals exchange places. Direct substitution, separately within each preparation, gives

$$
 f_{s,-}(\mathcal R u)
 =b_s e^{-a_s d_3-3d_2-2d_1-a_s d_0}
 =2b_s f_{s,+}(u).
$$

Thus P_{s,-}=2b_s P_{s,+}=b_s I_s after integration over the full simplex. The equal exponential is an equality of all dwell/survival factors under this specific bijection. Merely multiplying rates without that equality would not establish an integrated finite-time ratio. The preparation starts empty on both sides because these two selected paths close at 0; this does not define a physical time-reversed apparatus for arbitrary trajectories.

It follows that P_{A,+}/P_{A,-}=1/2 and P_{B,+}/P_{B,-}=1. Since both denominator probabilities are positive, the record laws cannot coincide. The cycle symmetry in B is exact at the declared transient horizon even though the initial state is empty. A single cycle outcome does not identify the preparation with certainty because both laws have the same three-outcome support; the statement is that their probability laws differ. No stationary distribution, long-run current, relaxation result or generalized equilibrium theorem is needed or claimed.

Both selected cycles end in state 0. A terminal-state-only reading assigns these two path events the same endpoint and therefore cannot label their orientations. This establishes only that specific loss of distinction. The remainder also includes returns to 0 and nonreturns, and its contribution must be included in any actual terminal marginal. No equality of the complete A/B terminal laws is asserted, nor is a terminal sensor asserted to be universally useless. Dropping a jump-rate or waiting factor is not the summation/integration over paths that defines a terminal marginal.

## 5. Whole-history local and Killing heat ledger

Heat is positive INTO the test system. At bath i, assign +epsilon_i on 0→i and -epsilon_i on i→0; its Killing heat is N_i times that local heat. Channel jumps have no bath heat and zero net Killing-energy change. The assigned H is constant during every dwell interval, with no supplied Killing work from the stationary supports or the reciprocal channel.

For any finite path at the specified horizon, let n_i^+ count 0→i and n_i^- count i→0. The local totals and common conserved-energy accounting are

$$
 Q_L^{\mathrm{loc}}=E(n_L^+-n_L^-),\qquad
 Q_U^{\mathrm{loc}}=\tfrac E2(n_U^+-n_U^-),
$$

$$
 Q^{K}=Q_L^{\mathrm{loc}}+2Q_U^{\mathrm{loc}}
 =\sum_{\text{all jumps}}[H(X_{\mathrm{after}})-H(X_{\mathrm{before}})]
 =H(X_{t_f})-H(X_0)
 =E\,\mathbf1_{\{X_{t_f}\in\{L,U\}\}}.
$$

The jumpwise equality holds for either bath transition and for each channel transition, whose endpoints both have charge E. The sum telescopes for every finite history, regardless of jump count or order. Since the CTMC is nonexplosive, it covers almost every underlying path in +, - and *, including the no-jump path. Paths assigned to * need not have a single heat value: their individual histories obey this identity, and their common net Killing heat is determined by their final occupancy. The observed three-valued record alone need not resolve that occupancy within * or its separate bath totals.

The cycle ledgers, identical in A and B, are:

| Cycle | Jump | Local bath heat into system | Killing heat into system |
|---|---|---:|---:|
| + | 0→L | +E at L | +E |
| + | L→U | 0 (channel) | 0 |
| + | U→0 | -E/2 at U | -E |
| - | 0→U | +E/2 at U | +E |
| - | U→L | 0 (channel) | 0 |
| - | L→0 | -E at L | -E |

Each cycle has zero total Killing heat and returns H to 0. The signed local bath totals are (+E,-E/2) for + and (-E,+E/2) for -, in site order (L,U). Adding the two local numbers without the lapse conversion would give ±E/2; that is not a common conserved energy or extracted work. The occupied local gap changes when comparing L with U, while their assigned Killing charge agrees. A dynamical spatial mechanism implementing that comparison is outside this three-state model.

## 6. Units, limits and closure

E and all local/Killing heats have energy units; k_B has energy/temperature units; T_i are local proper temperatures. gamma has inverse time units using the declared common clock units for both proper and common time; N_i are dimensionless conversion factors. u and all probabilities are dimensionless. The only experimental-time interval considered is the common [0,1/gamma]; the proper elapsed times between its stationary slices are 1/gamma at L and 2/gamma at U. Each dwell in site i of common duration dt corresponds to local proper duration N_i dt. The separate common-time channel rates are stipulated, not converted bath rates.

The result is a conditional finite classical stochastic comparison and an exactly telescoping supplied energy ledger. It does not derive temperature, energy, time units, geometry, gravity, native mass or native thermalization from DET. In particular a prescribed lapse ratio alone does not establish curvature. Maintaining the baths, fixed gaps, stationary supports and reciprocal channel is idealized. No microscopic bath or channel dynamics, propagation delay, support-stress/source-energy accounting, gravitational-mass closure, preparation or measurement cost, reset cost, material realization or empirical permission is supplied. No heat follows from information alone, and no work extraction, engine efficiency or full-device balance is established.

The result is limited to the two declared finite record laws, their reversal comparison and the whole-history heat/time ledger.

## Scientific review

Classical derived both complete finite laws and the pathwise heat ledger. Its distinct reviewer checked the integrals by an independent convolution method and verified all survival intervals. Independent recipient review confirms the registered-clock/energy scope and incomplete calorimetric meaning of the remainder. Author report SHA-256 4d49f5dbc77865dc3d0b54ad6d126c4bf3dbf3075fec38817d9bef176be6e982; scientific review c1149bece33ef1f47ef150d1e83daaeaadd050a2059dad9564980014717915cb; recipient review 760307821c9f2547cf0b67e562ecba11db215d2d6c6cc92b0a3a0e1349293bae.
