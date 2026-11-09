# Finite endpoint relaxation separates the paired strengths on a certified subset

**Independently reviewed conditional result.** The stipulated two terminal samples and ideal equilibrium reference can distinguish lambda=3 from lambda=5 on a nonempty observable subset, despite each candidate fitting its own positive common gain and dwell scale. The test uses a ratio of finite two-time deficits; a normalized observed reading certifies the small dimensionless dwell needed in BOTH candidate worlds. No derivative measurement or assumed small sampling time is used. This is not a claim of global separation.

## 1. Fixed native domain, access and supplied response

Keep the root-zero two-chain prefix, marks (0,0), counters (1,0), and all 60 fair-mark/all-ideal continuations. The accepted eligibility gate leaves only the chain C and diamond D active, with probabilities

    p_C=779/1320,  p_D=172/1320,  p_perp=369/1320.

The terminal count-to-actual-handle selector supplies the already accepted source s, grounded return t and pair placement under its explicitly supplied binding and actuation services. No shape, interior field value, history, order or handle label is exposed to the scalar observer. The new storage and common timer are separate premises, not consequences of that selector or the native growth law.

Write the supplied positive storage coefficient as C_store to distinguish it from the chain symbol. It is identical on all three non-ground nodes and common across shapes. The signal is switched on from a fully discharged state:

    C_store dv/dt + k L_lambda v = Q e_s,   v(0)=0,   v_ground=0,

with Q,k,C_store>0. Each free-node storage is shunted to the grounded return. Use the same conditions, initial reset, common positive zeroed gain b, and nondestructive source-to-ground measurement at tau,2tau. The 1:2 timing ratio and common tau>0 across carriers are supplied, not physical seconds. The ideal equilibrium coordinate is the prior steady reference under these conditions; it is NOT claimed to be attained after a finite waiting time.

Introduce dimensionless time x=k*tau/C_store>0, common to both shapes within a world, and amplitude A=bQ/k>0. The two candidates may use different A_3,x_3 and A_5,x_5. No absolute amplitude or time calibration is imposed to compare them.

## 2. Exact finite responses, return balance and covariance

Order the three free vertices as (s,p,q), solely for this proof. The dimensionless grounded matrices of the accepted conductance graphs are

    L_C(lambda) =
      [1+2lambda,  -1,         -lambda]
      [-1,         2+lambda,  -1     ]
      [-lambda,   -1,          2+lambda],

    L_D(lambda) =
      [2+lambda,  -1,  -1]
      [-1,         2,   0]
      [-1,         0,   2].

The chain has cover edges sp,pq,qt and non-cover edges sq,st,pt. The diamond has covers sp,sq,pt,qt, sole non-cover st, and p,q incomparable. Both matrices are symmetric positive definite: extending a vector by zero at the ground gives its quadratic form as the sum of weighted squared edge differences, and the positive cover graph connects every vertex to the ground. This includes both candidate strengths without a singular mode.

Let e=(1,0,0)^T and define the exact dimensionless source response

    g_T,lambda(x) = e^T L_T(lambda)^(-1)
                         [I-exp(-x L_T(lambda))] e,   T=C,D.

The unique solution of the specified linear initial-value equation is
v(t)=(Q/k)L^(-1)[I-exp(-(kt/C_store)L)]e. This follows by direct differentiation and v(0)=0; positive definiteness also gives convergence to the unique accepted steady state. Thus one active observed triple is

    T_T(lambda,A,x)
      = A [g_T,lambda(x), g_T,lambda(2x), R_T(lambda)],

where the previously accepted steady drops are

    R_C(lambda)=(lambda+3)/(lambda^2+6lambda+1),
    R_D(lambda)=1/(1+lambda).

Only these two finite times are sampled. The matrix exponential is an exact expression for the assumed law, not a numerical solver or a time-series observation.

Storage displacement is essential to the return balance. Summing the three free-node equations cancels their internal edge currents and gives

    C_store sum_i dv_i/dt + k sum_i w_it v_i = Q.

The grounded terminal therefore receives the sum of storage displacement and conductive current, equal to Q; its external return has sign -Q. At switch-on the conductive term is zero, with the source current accounted for by storage. At equilibrium the storage term vanishes and the accepted conductive return is recovered. Ignoring storage current would not implement the stipulated balanced terminal model. For the matched blank Q=0, the fully discharged initial state has the unique zero solution.

Simultaneous handle transport permutes the free coordinates, ground, L and e together. Homogeneous storage is invariant under that permutation, so the transported solution is the solution on the transported carrier and the source-to-ground scalar is unchanged. Diamond middle-handle exchange introduces no extra observed coordinate. Growth probabilities, marks and the eligibility gate are unaffected by this post-growth attachment.

## 3. Complete normalized finite observation laws

For each native history h use the deterministic triple above on its active shape and perp otherwise. All four newborn-bit assignments per structural row retain their original weights w(h). Consequently the separate setting-conditional laws are

    P_sig^(lambda,A,x)
      =(369/1320)delta_perp
       +(779/1320)delta_(T_C(lambda,A,x))
       +(172/1320)delta_(T_D(lambda,A,x)),

    P_blank
      =(369/1320)delta_perp+(951/1320)delta_(0,0,0).

Each law sums to one. The 52 inactive histories are never discarded or eligibility-renormalized. The zero triple is distinct from perp. These are correlated finite-time coordinates on one trial; the blank is a separate setting with the same unconditional native preparation, not a paired potential outcome on the same history.

For lambda=3 and 5 the steady constants are respectively

    (R_C(3),R_D(3))=(3/14,1/4),
    (R_C(5),R_D(5))=(1/7,1/6).

Their steady ratio is 6/7 in both worlds. A_5=(3/2)A_3 matches both steady atoms, so their static equivalence is retained.

In each candidate the two active TRIPLES are distinct, since their positive equilibrium coordinates differ. The unequal exact masses 779/1320 and172/1320 therefore identify which observed triple is C and D; no hidden shape tag is supplied. Write their coordinates as z_T,1,z_T,2,z_T,infty. This is identification from an ideal law, not a finite-sample shape classifier.

## 4. Finite observables and a common spectral bound

From those two observed triples form

    y_D = z_D,1/z_D,infty,
    H_C = 2 z_C,1 - z_C,2,
    H_D = 2 z_D,1 - z_D,2,
    J = H_C/H_D.

These are finite recorded combinations. In particular J uses both terminal samples, not a slope at t=0. A cancels from J and from y_D; common dwell x is retained as an unknown candidate-specific nuisance.

For either graph and lambda in {3,5}, the maximum weighted vertex degree is at most 11. For a free vector extended by zero at the ground,

    z^T L z = sum_edges w_ij(z_i-z_j)^2 <=22 ||z||^2.

Thus every eigenvalue r lies in (0,22]. In an orthonormal spectral basis let a_j be the squared source component. Then a_j>=0, sum_j a_j=1, and

    g_T(x)=sum_j a_j(1-exp(-r_j x))/r_j,
    h_T(x):=2g_T(x)-g_T(2x)
          =sum_j a_j(1-exp(-r_j x))^2/r_j >0.

Also sum_j a_j r_j=(L_T)_ss=:d_T. The needed source diagonals are

    (d_C,d_D)=(7,5) for lambda=3,
    (d_C,d_D)=(11,7) for lambda=5.

The measured H_T equals A h_T(x), so H_D is strictly positive in the stipulated signal model for every finite x>0. A zero or negative observed H_D is not divided by; it is incompatible with this exact law.

These identities prove strict increase of g_T from 0 to R_T. Its integral form has positive integrand:
g_T(x)=integral_0^x sum_j a_j exp(-r_j u) du. No derivative is measured or used as an observation.

## 5. The dwell bound is certified by readings in BOTH worlds

Set the proof constants

    epsilon=1/1000,   alpha=1-22epsilon=489/500.

For u in [0,epsilon], exp(-r_j u)>=1-r_j u>=alpha. Hence

    g_D(epsilon)>=epsilon*alpha.

Both candidate steady values obey R_D<=1/4. If a candidate dwell x>=epsilon, monotonicity implies

    y_D=g_D(x)/R_D
       >=4epsilon*alpha
       =489/125000
       >1/400.

Therefore the entirely observable condition

    0<y_D<=1/400

forces x<1/1000 for EACH compatible candidate separately, regardless of its fitted positive A or its own time scale. The same observed y_D tests both worlds; there is no premise that x_3=x_5 and no unverified claim that a numerical tau is small. The bound22 is derived from the two stipulated matrices, not an extra physical calibration. The only extra timing/storage assumptions are those explicitly supplied in Section 1.

## 6. Exact finite separation on that certified subset

For 0<=u<=22x<22epsilon, the elementary inequalities

    1-u/2 <= (1-exp(-u))/u <=1

hold with a positive lower bound (and the quotient is defined by continuity at0). Squaring gives a lower bound at least1-u, hence at least alpha. Applying the finite spectral formula for h_T yields

    alpha*d_T*x^2 <= h_T(x) <= d_T*x^2.

Consequently any compatible record with 0<y_D<=1/400 must have

    (d_C/d_D)*alpha <= J <= (d_C/d_D)/alpha.

For the two candidates the closed conservative intervals are

    lambda=3: 3423/2500 <= J <=700/489,
    lambda=5: 5379/3500 <= J <=5500/3423.

They are disjoint, with the simple rational threshold

    700/489 <3/2 <5379/3500.

The first inequality is 1400<1467; the second is 5250<5379 after positive cross multiplication. These are finite inequalities on actual sampled coordinates. No limiting derivative is the discriminating record.

Define the observable subset W of candidate-format ideal laws by: the complete native atom/inactive probabilities and matched blank of Section 3; positive equilibrium values with steady ratio6/7; two positive deficits H_C,H_D; and 0<y_D<=1/400. Then:

- On W, a record compatible with lambda=3 has J<3/2 and cannot be compatible with lambda=5 for ANY A_5,x_5>0.
- On W, a record compatible with lambda=5 has J>3/2 and cannot be compatible with lambda=3 for ANY A_3,x_3>0.

Indeed equality of the full laws forces association of the same two triples by their unequal masses, so both y_D and J agree. Section 5 would force both fitted dwells below epsilon; Section 6 would then put the same J in disjoint intervals. This contradiction allows separate common amplitude AND time fits, rather than comparing two worlds at an arbitrarily fixed numerical scale.

Interval membership alone does not prove that a candidate fits every coordinate. A record in the gap, at J=3/2, or outside both intervals rejects both candidate laws on W. The rejection test is conditional on the supplied model; it does not attribute a discrepancy to a physical failure of gravity.

### Explicit attainment with finite readings

For either lambda choose x0=1/10000 and any A>0. The exact record consists of the two triples T_C(lambda,A,x0),T_D(lambda,A,x0), with all probabilities and matched blank of Section 3. Since g_D(x)<=x and 1/R_D<=6,

    0<y_D<=6x0=3/5000<1/400.

Both deficits are strictly positive. Thus this record lies in W and in its candidate's interval and is excluded from the other candidate. Every time in this witness is positive and finite, with second sample at 2x0; all native histories, inactive trials and blank zeros remain. The same bound certifies every 0<x<1/2400 and A>0 against the observable cut. This is a theoretical attainability witness under the supplied response, not a claim that a physical timer can set a known absolute dwell or resolve those deficits.

## 7. Exact candidate compatibility and limits of the result

For completeness the full stipulated record can be tested without classifying all intersections. Require the exact blank/inactive weights and the two distinct positive-equilibrium triples identified by their masses. For a proposed lambda in {3,5}, require the equilibrium values to equal A(R_C,R_D) for one A>0, which determines A=z_D,infty/R_D. Require 0<y_D<1. Strict monotonicity and the limits of g_D/R_D give a UNIQUE finite x>0 solving

    g_D,lambda(x)/R_D(lambda)=y_D.

Then the remaining finite coordinates must equal
A g_D,lambda(2x), A g_C,lambda(x), A g_C,lambda(2x). These checks, together with the equilibrium and weight conditions, are necessary AND sufficient by the exact normalized laws in Section 3. This is a mathematical compatibility condition, not a numerical implementation or sweep.

W provides certified separation, not a proof of global disjointness outside W. Without its observed dwell certificate the conservative intervals are not licensed. As x tends to infinity the transient coordinates approach the statically equivalent steady records; an approach to that limit is not an exact finite collision. As x tends to zero the deficits become small; the proof still uses finite x, but establishes no noise margin, instrument resolution, finite-sample power or practical acquisition precision. Subtraction in H_T may be delicate physically. Actual offsets, gain drift, unequal storage, loading/readout disturbance, timing errors, losses or failures need an independently specified calibrated full law and prospective tolerances; none is fitted away or deleted here.

The record determines or bounds dimensionless information: y_D and J are directly scale-free; W bounds each candidate's k*tau/C_store below epsilon; conditional on a compatible identified strength, the exact finite model determines its dimensionless dwell x and output amplitude A. It does not separately determine Q,b,k,C_store, tau in seconds or an absolute physical potential. A is in the supplied output units. The known 1:2 ratio is not an absolute clock.

## 8. Alternatives, resources and physical boundary

A signed interior measurement could add a static ratio but would require a correctly bound extra probe. It is not used here. Changing the source-mark mixture without changing the conditional static response merely reweights shapes whose statically equivalent responses already match; it cannot replace this added temporal information. No new growth cases or source-to-charge assignment are introduced.

The temporal result depends on the NEW homogeneous storage law, fully discharged switch-on, common positive time scale across shapes, known 1:2 timer, common zeroed gain, nondestructive source/ground probes and exact ideal equilibrium reference. Giving each shape independent timing, storage or gain would change the model and is not controlled by this proof. Storage on all three free carriers is an additional attachment even though no interior field reading is exposed. Nothing derives a native or causal gravitational propagation law from record growth.

Required and unobserved costs include prepared native histories and handle-bound counts; persistent carrier/port identity; eligibility and pair placement; source/return activation and grounding; installing and matching three free-node storage elements; full discharge, switch timing and common timer ratio; holding/control, source work and dissipation; repeated nondestructive endpoint acquisition and retention; obtaining the ideal steady datum under its supplied limit convention; gain/zero calibration, storage/timing stability, failures and all source/register/storage/port reset. Inactive and blank trials remain in the ledger and have preparation/access costs. Identical premises and resources go to conventional comparators. No energy, efficiency, hardware-readiness or quantum-necessity claim follows. No physical length, mass, seconds or absolute native unit has been inferred.

## Reviewed sources

- [Unlabelled terminal field response: exact finite equivalence certificate](finite_native_order_field_coupling.md)
- [Terminal count access selects the actual finite field commands](terminal_counts_and_field_placement.md)
- [A prepared source record changes two finite outputs](native_source_readout_response.md)

Scientific report SHA-256 `ec518844cd0ae2b2d138cdc9ea28f5e60aa2231c0990544b4d6d2a54f86f8cff`. Independent review SHA-256 `8860b80db9ebe9a56c36bd65ac751cb27951ef37620b10f90cbddb7df4528279`.
