# Coupling observability in a two-constituent Hamiltonian model

Scientific status: **accepted scoped conditional mathematics** (GDM011 and GDM012).
Publication status: **approved public edition following distinct editorial-equivalence review and coordinator disposition**.
See [review attribution](REVIEW.md) and [adoption boundaries](ADOPTION.md).

Two calibrated preparations identify constituent and interaction-energy coupling parameters inside the first supplied family. They do not distinguish that family from the second supplied family at the original readout. One prescribed additional time does distinguish the two families, except on their common constituent-only subfamily.

This document contains the hypotheses and substantive proofs. It assumes no DET ontology and establishes no physical gravity law. Both families, canonical mechanics, preparation and controls are supplied mathematical hypotheses. Exact derivatives are assumed; experimental precision is not proved.

## Part I — parameter identification inside interaction-energy coupling

In this part mu denotes the parameter called mu_I in Part II. Equations are numbered separately within each part.

### I.1. Full canonical equations, including relative field forces

Let e,c,ell>0, d=4ell, k=e/ell², q=X2−X1−d, R=(X1+X2)/2, K(P)=sqrt(e²+c²P²) and V(q)=kq²/2. The supplied candidate is

H=K(P1)+K(P2)+V(q)−2FR−g R[2mu+beta V(q)/c²].

F is calibrated force on each constituent; g is calibrated acceleration-dimension control. Mu and beta are finite constants, common across preparations, with mass and dimensionless units respectively. Canonical brackets have {X_i,P_j}=delta_ij, with Xdot_i=partial_Pi H and Pdot_i=−partial_Xi H. Dots denote t derivatives; primes on y,b denote tau derivatives, while primes on V,K,f denote derivatives of their arguments.

Define Q(q)=mu+beta V(q)/(2c²). Exact differentiation gives

Xdot_i=c²P_i/K_i,
Pdot1=V'(q)+F+g Q(q)−g beta R V'(q)/c²,
Pdot2=−V'(q)+F+g Q(q)+g beta R V'(q)/c².       (1)

Thus

Ptotal_dot=2F+g[2mu+beta V(q)/c²],
(P2−P1)_dot=−2[1−g beta R/c²]V'(q).           (2)

The opposite-sign R V' forces are retained. They cannot in general be replaced by a common constituent force. All terms in (1) have force units; g beta R/c² is dimensionless.

The two preparations are outward, denoted o: P1=−e/(10c),P2=e/(10c); and equilibrium, denoted e: P1=P2=0. Both have q=R=0, with X1=−d/2,X2=d/2, independent of both controls. Fix h=ell/(4c).

Bounded kinetic velocities keep R and q bounded on finite intervals. For finite fixed controls and parameters, the polynomial position-dependent forces in (1) are then bounded, so momenta remain finite. Smooth unique flow and parameter derivatives exist. In particular |q(t)|<2ct≤ell/2 for 0<t≤h. This supplies separation support and a common neighborhood of zero controls, not stability or a physical preparation claim.

### I.2. Exact zero-control baselines

At F=g=0, total momentum stays zero and oddness of K' gives R_j(t)=0 in both preparations. Put tau=ct/ell, y=q/ell, b=c(P2−P1)/(2e), f(b)=b/sqrt(1+b²). Both baselines obey

y'=2f(b), b'=−y.                              (3)

The outward initial data are y=0,b=1/10. Before a possible first exit from 0<b<1/10, the equations give y>0, y'<1/5 and b'≤0. Integration gives y<tau/5 and b≥1/10−tau²/10≥3/32>0 through tau=1/4. These bounds exclude a first zero of b, while positive y excludes a return to b=1/10. Consequently, for positive tau≤1/4, y>0, 3/32≤b<1/10 and y<1/20. The equilibrium initial data y=b=0 give the identically zero solution.

Let V_j(t)=V(q_j(t)) and

D_j(t)=K''(P1_j^0(t))=K''(P2_j^0(t))
      =(c²/e)[1+b_j(ct/ell)²]^(-3/2)>0.         (4)

The baselines do not depend on mu or beta because their field terms vanish at zero controls.

### I.3. Complete first variations and response matrix

For z=F or g, write xi_i^z=partial_z X_i|0 and pi_i^z=partial_z P_i|0; their initial data are zero. Let eta^z=xi2^z−xi1^z. Linearizing (1) gives

xidot_i^z=D_j pi_i^z,
pidot1^z=k eta^z+delta_zF
 +delta_zg[Q_j−beta R_j^0 V'_j/c²],
pidot2^z=−k eta^z+delta_zF
 +delta_zg[Q_j+beta R_j^0 V'_j/c²],             (5)

where Q_j=mu+beta V_j/(2c²). The deltas select the differentiated control. Terms proportional to g times a state variation vanish at the evaluation point g=0.

Here R_j^0=0, so the relative direct field source in (5) vanishes for the stated preparations. This follows from their baseline symmetry; it is not omission of the relative force in (1). With rho^z=pi2^z−pi1^z, the difference IVP is eta_dot=D_j rho, rho_dot=−2k eta with zero data. Therefore eta=rho=0 and

pi_i^F(t)=t,
pi_i^g(t)=mu t+[beta/(2c²)] integral_0^t V_j(s) ds.

Define S_j=partial_F R_j(h)|F=g=0 and T_j=partial_g R_j(h)|F=g=0, at the fixed preparation. The exact responses are consequently

S_j=integral_0^h t D_j(t) dt,
T_j=mu S_j+beta B_j,                           (6)

B_j=[1/(2c²)] integral_0^h D_j(t)
                       [integral_0^t V_j(s) ds] dt.       (7)

S has length/force units; T and B have time-squared units. These are full finite-readout integrals for the linear responses, not small-time extrapolations.

For these two prescribed symmetric preparations the identification condition is

Delta=S_e B_o−S_o B_e != 0.                    (8)

The mechanical responses are independent of mu,beta; the parameter Jacobian of the four-response vector has the same rank as the two-by-two matrix with rows (S_e,B_e),(S_o,B_o). Thus calibrated mechanical response by itself does not supply a second parameter equation; the two independent field responses do.

### I.4. Strict finite-h rank and explicit reconstruction

For the equilibrium baseline, V_e=0 and D_e=c²/e, hence

S_e=c²h²/(2e)=ell²/(32e)>0, B_e=0.             (9)

For the outward baseline, V_o(s)=e y_o(cs/ell)²/2>0 for every positive s≤h. The continuous positive D_o and (7) give B_o>0. More explicitly,

B_o=(ell²/(4c²)) integral_0^(1/4) f'(b_o(tau))
                        [integral_0^tau y_o(u)² du] d tau.

Therefore, with equilibrium row first,

Delta=S_e B_o
 =(ell^4/(128e c²)) integral_0^(1/4) f'(b_o(tau))
                        [integral_0^tau y_o(u)² du] d tau >0.     (10)

The sign is established at exactly the prescribed h. No candidate or preparation was changed to obtain rank.

In the stipulated V(0)=0 convention the unique reconstruction is

mu=T_e/S_e,
beta=[T_o−(T_e/S_e)S_o]/B_o
    =[T_o/S_o−T_e/S_e]/(B_o/S_o).              (11)

B_o is the exact coefficient determined by the declared calibrated model and baseline IVP. It is not an additional supplied measurement, nor can it be inferred from S_o alone if arbitrary dynamics or couplings are admitted. Equations (10)–(11) establish noiseless structural identifiability, not a bound on experimental conditioning, error or attainable sensitivity.

### I.5. Additive energy zero and invariant charge

Change the interaction-energy convention to V_C=V+C, where C is constant. Derivatives V' and the zero-control dynamics are unchanged. To preserve the same field coupling, transform

beta_C=beta, mu_C=mu−beta C/(2c²).             (12)

Then 2mu_C+beta_C V_C/c²=2mu+beta V/c² and H_C=H+C. The complete canonical flow and all four responses are identical. Changing V without (12) instead changes the hypothetical coupling; it is not merely a change of notation.

The response coefficient changes as

B_j,C=B_j+[C/(2c²)]S_j,

so the second response-matrix column receives a multiple of the first. Delta is unchanged. A convention-independent reconstruction uses

mu_eq:=mu+beta V(0)/(2c²)=T_e/S_e,
beta=[T_o/S_o−T_e/S_e]/
      [B_o/S_o−B_e/S_e].                      (13)

The denominator is invariant under the shift and positive here. Beta, mu_eq, and the effective pair charge 2mu+beta V(q)/c² are convention-invariant. Bare mu is identified only after choosing the energy zero. In the originally prescribed zero, mu_eq=mu.

### I.6. Negative controls and remaining observation premises

With only one preparation j, S_j>0 and T_j=mu S_j+beta B_j identify one combination. For any real a,

(mu,beta) -> (mu−a B_j/S_j, beta+a)

preserves both responses. In equilibrium B_e=0 leaves beta entirely unconstrained. The outward preparation alone also cannot separate the two parameters.

If g is not calibrated, let the actual field be g=kappa u for a measured control knob u with unknown nonzero gain kappa. Then the measured field response is

partial_u R_j=kappa(mu S_j+beta B_j).

The two preparations identify kappa*mu and kappa*beta, not their absolute normalization. The change (kappa,mu,beta)->(a kappa,mu/a,beta/a), a nonzero, preserves every response. Ratios may survive when defined, but absolute charge and interaction-coupling scale do not. Unknown zero gain loses all field information. This degeneracy already holds with the mechanical force independently calibrated.

Retain the two-preparation protocol as a conditional constituent/interaction-coupling identification design. Physical use requires independently calibrated F and g; a common calibrated displacement/time readout realizing the stipulated R and h; field-independent preparation; validated e,c,ell and baseline V; justified persistence of the same mu,beta across preparations; and evidence that the proposed coupling, including the R V' relative force, actually represents the physical interaction without omitted channels. Unknown readout gain, additional coupling functions or model uncertainty are not excluded by this finite rank proof.

The calculation does not determine that g is gravitational, set mu=e/c², establish physical inertial/rest mass, identify a physical energy center, complete a physical boost/worldline construction, or violate an equivalence principle. No fitted data, new coefficient chain, experiment, runtime or native-law claim is introduced. The result changes the observation-design decision: the declared calibrated two-preparation candidate separates two coupling parameters modulo energy-zero convention; the specified reduced controls do not. The accepted scope is conditional identification within this supplied model.

## Part II — discrimination from total-internal-energy coupling

### II.1. Fixed protocol and full Family E equations

Let e,c,ell>0, d=4ell, k=e/ell², q=X2−X1−d, R=(X1+X2)/2,
K(P)=sqrt(e²+c²P²), V(q)=kq²/2 and H0=K(P1)+K(P2)+V(q).
Use ordinary canonical brackets and constant calibrated controls F,g. F is force per constituent; g has acceleration units. The competing supplied families are

H_I=H0−2FR−gR[2mu_I+beta V/c²],
H_E=H0−2FR−gR[2mu_E+alpha(H0−2e)/c²].

Each family has its own finite constant parameters, shared across its preparations and times. Mu has mass units; alpha,beta are dimensionless. Neither family is asserted native, conventional, gravitational or relativistically complete.

Both preparations have X1=−d/2,X2=d/2, independently of controls. Equilibrium has P1=P2=0; outward has P1=−e/(10c),P2=e/(10c). Set h=ell/(4c). The extension uses equilibrium at h and outward at h/2 and h. Separate identically prepared trials may supply the two outward readouts; no harmless intermediate-measurement assumption is made.

For Family E define

A=1−g alpha R/c²,
Q_E=mu_E+alpha(H0−2e)/(2c²),
v_i=K'(P_i)=c²P_i/K_i.

Direct canonical differentiation gives

Xdot_i=A v_i,
Pdot1=A V'+F+g Q_E,
Pdot2=−A V'+F+g Q_E.                         (1)

Consequently Ptotal_dot=2F+2g Q_E and (P2−P1)_dot=−2A V'. The momentum-dependent coupling changes velocities as well as forces. In particular, a global bound |Xdot_i|<c at nonzero g is not inherited from the kinetic term.

At zero controls, both families reduce to H0. Their two baseline trajectories exist through h, with R=0, opposite momenta and |q|<ell/20 for the outward state; equilibrium is stationary. For any fixed finite coupling parameters, (1) is smooth in state and controls. Choose a compact tube with positive margin around each baseline, contained in |q|<ell and with finite momenta. Bounded derivatives on a slightly larger tube, continuous parameter dependence and the usual continuation estimate ensure that sufficiently small |F|,|g| keep the solution in that tube through h. Taking the smaller neighborhood covers both preparations and families. This local argument supplies differentiability and separation support; it asserts neither global bounded speed nor stability.

### II.2. Baselines and complete first variations

Write tau=ct/ell, y=q/ell, b=c(P2−P1)/(2e), f(b)=b/sqrt(1+b²). The zero-control relative equations are

y'=2f(b), b'=−y.

For the outward state, the exact finite-interval bounds proved in Part I give y>0, 3/32<=b<1/10 and y<1/20 for 0<tau<=1/4. In particular y is strictly increasing. Equilibrium has y=b=0. Set

D_j(t)=K''(P1_j^0)=K''(P2_j^0)
      =(c²/e)[1+b_j(ct/ell)²]^(-3/2)>0.

Along each zero-control trajectory H0 is conserved. Therefore

epsilon_j=(H0_j−2e)/(2c²),
epsilon_e=0,
epsilon_o=(e/c²)[sqrt(101)/10−1]>0.           (2)

These constants are baseline excitation energies divided by 2c², not measured masses.

For z=F or g define xi_i=partial_z X_i|0, pi_i=partial_z P_i|0, eta=xi2−xi1. All initial variations vanish. Differentiating the full Family E equations, before using R_j^0=0, gives

xidot_i=D_j pi_i−delta_zg alpha R_j^0 v_i^0/c²,
pidot1=k eta+delta_zF
       +delta_zg[mu_E+alpha epsilon_j−alpha R_j^0 V'_j/c²],
pidot2=−k eta+delta_zF
       +delta_zg[mu_E+alpha epsilon_j+alpha R_j^0 V'_j/c²]. (3)

State-variation terms multiplied by g vanish at g=0. The displayed direct velocity and relative-force sources vanish specifically because R_j^0=0. They were not discarded from the Hamiltonian.

With rho=pi2−pi1, the resulting homogeneous difference system is eta_dot=D_j rho, rho_dot=−2k eta. Zero initial data imply eta=rho=0. Thus

pi_i^F(t)=t,
pi_i^g(t)=(mu_E+alpha epsilon_j)t.

For either family define S_j(t)=partial_F R_j(t)|0 and T_j(t)=partial_g R_j(t)|0. For every 0<t<=h the same positive mechanical response is

S_j(t)=integral_0^t s D_j(s) ds.

Family E consequently has the exact normalized response

Z_j^E(t):=T_j^E(t)/S_j(t)=mu_E+alpha epsilon_j. (4)

For the two prescribed preparations, Part I gives

Z_j^I(t)=mu_I+beta w_j(t),
w_j(t)=B_j(t)/S_j(t),
B_j(t)=[1/(2c²)] integral_0^t D_j(s)
                         [integral_0^s V_j(u)du]ds.      (5)

The same variational proof holds on each prefix [0,t] of the established interval; it is not transferred to other preparations. Here w_e=0, while w_o(t)>0. S has length/force units, T and B have time-squared units, and Z,w,epsilon have mass units.

### II.3. Original readout: exact family ambiguity

At h, abbreviate w_h=w_o(h)>0 and epsilon=epsilon_o>0. The normalized equilibrium/outward pairs are

I: (mu_I, mu_I+beta w_h),
E: (mu_E, mu_E+alpha epsilon).

Both describe every real pair as their two parameters vary. The parameter correspondence

mu_E=mu_I, alpha=beta w_h/epsilon             (6)

matches all four original force/field responses; conversely beta=alpha epsilon/w_h. The mechanical responses add no family distinction because they are identical. Parameter identification within Family I therefore does not identify that family against E. This statement concerns the assigned derivatives, not all nonlinear finite-control observations.

### II.4. Strict finite-time variation of w_o

Suppress the outward subscript and define, for s>0,

m(s)=[1/(2c²s)] integral_0^s V(u)du,
a(s)=s D(s)>0.

Since y>0 and y'>0 through h, V(t)=e y(ct/ell)²/2 is strictly increasing. Hence

m'(s)=[s V(s)−integral_0^s V(u)du]/(2c²s²)>0.

Equation (5) expresses w(t) as the weighted mean

w(t)=[integral_0^t a(s)m(s)ds]/[integral_0^t a(s)ds].

The integrals extend continuously to zero. For every positive t, strict increase of m gives 0<w(t)<m(t), and differentiation yields

w'(t)=[a(t)/S_o(t)][m(t)−w(t)]>0.             (7)

In particular 0<w_o(h/2)<w_o(h). This uses positivity on the full prescribed finite interval, with no series expansion or fitted time.

### II.5. Prescribed extension and exact residual degeneracy

Put w_1=w_o(h/2), w_2=w_o(h), and form the ordered normalized response triple (equilibrium at h, outward at h/2, outward at h). Its possible values are

I: (mu_I, mu_I+beta w_1, mu_I+beta w_2),
E: (mu_E, mu_E+alpha epsilon, mu_E+alpha epsilon). (8)

If the triples coincide, their first components give mu_E=mu_I. Subtracting the outward components gives beta(w_2−w_1)=0, hence beta=0. Equation (8) then forces alpha=0. Conversely alpha=beta=0 with equal mu makes the entire Hamiltonians identical. This common constituent-only subfamily is intrinsically indistinguishable; if mu also vanishes, every field response vanishes.

For an observed triple (z_e,z_1,z_2), let a=z_1−z_e and b=z_2−z_e. Exact membership tests are

Family I: w_2 a−w_1 b=0;
Family E: b−a=0.

Both hold exactly only when a=b=0. A nonzero Family I interaction coefficient produces unequal outward normalized responses; a nonzero Family E excitation coefficient produces equal outward responses shifted from equilibrium. Data satisfying neither relation reject both declared families. The extra readout therefore distinguishes these two model families away from their intersection, not every possible coupling law.

### II.6. Conventions and physical obligations

Under V_C=V+C and H0_C=H0+C, holding the reference 2e fixed, preserve the same Hamiltonian flow by

mu_I,C=mu_I−beta C/(2c²),
mu_E,C=mu_E−alpha C/(2c²),

with alpha,beta unchanged. Each Hamiltonian changes only by C. Correspondingly w_j,C=w_j+C/(2c²) and epsilon_j,C=epsilon_j+C/(2c²). The equilibrium normalized response is the invariant effective constituent charge. The differences w_o(t)−w_e(t) and epsilon_o−epsilon_e are invariant. In a shifted convention, use these differences in place of w_1,w_2,w_h and epsilon in sections II.3–II.5, and use the equilibrium effective charge in place of bare mu. The comparison and membership tests then retain exactly their stated form; using shifted raw w coefficients would not. Bare mu requires the declared energy-zero/reference convention.

Absolute parameter inference requires calibrated F,g and common position/time units. An unknown common nonzero gain g=kappa*u scales all Z equally: it preserves these homogeneous family-membership tests but loses absolute coupling normalization. Zero gain erases field information. Preparation- or time-dependent gains are not covered and can invalidate the comparison.

Physical use additionally requires validated kinetic/potential parameters, faithful control and readout realization, preparation independent of controls, parameters stable across trials, exclusion of omitted channels, and a justified choice of candidate coupling families. Exact derivatives are not finitely noisy samples; no precision, conditioning or experimental feasibility bound is proved. Neither family has been established physical, gravitational, DET-derived, or a completed relativistic model. The result resolves only the assigned family-discrimination question. No further family, preparation or readout time is included in this result.
