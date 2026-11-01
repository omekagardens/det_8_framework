# GDM020 prospective candidate model

All choices below are supplied hypotheses for one formal comparison. They are frozen before derivation. They are not an accepted quantization of a complete physical atom.

## Space, symbols and ordering

Use L2(R3_Q) tensor L2(R3_q) tensor C4_spin, with Q,P and q,p the canonical position/momentum pairs, [Q_i,P_j]=[q_i,p_j]=i*hbar*delta_ij, all other cross-pair commutators zero. Let M=2m>0, mu=M/4, C>0 and epsilon=c^-2. Write q=|q| and P2=P dot P, p2=p dot p for commuting symbol arguments before quantization.

Define the real classical symbols

e=p2/(2mu)-C/q,
w=3p2/(2mu)-2C/q,
a2=-(p2)^2/(32mu^3)-C/(2mu M)[p2/q+(p dot q)^2/q^3],
b_i=[(q dot P)p_i+(P dot p)q_i]/(2M^2).

OpW is Weyl quantization in both canonical sectors. Products in the following displayed symbol are quantized as the displayed classical monomials, including rational position coefficients. For those coefficients use their ordinary locally integrable distributions and distributional derivatives, without adding contact terms. A convenient initial formal test space has smooth compact support away from q=0 and Schwartz central dependence. Extension of the matrix elements actually required on the high-angular-momentum packet must be justified in the result. We do not assert a nonperturbative self-adjoint evolution for the p4 truncation.

The leading operator is the conventional Coulomb-plus-free-center Hamiltonian

H0=H_C+P2/(2M),  H_C=p2/(2mu)-C/q.

The candidate operators through the retained formal order are

H_A(f,g)=H0-(f+Mg)Q_x
 +epsilon*OpW{a2-P2*e/(2M^2)-(P2)^2/(8M^3)
             -g Q_x[w+3P2/(2M)]+Mg b_x+Mg^2 Q_x^2/2},

H_B(f,g)=H_A(f,g)-(3epsilon*g/M)OpW{q_x(P dot p)}.

This is GDM015's canonical expressions5/6 with a supplied Weyl convention. Nothing else is restored. The observable is R_x=Q_x-epsilon*OpW{b_x}; the force is still -fQ_x, not -fR_x. Spin is acted on by the identity throughout.

## Fixed preparation and clock

Use normalized conventional relative Coulomb circular states |n>_c=|n,l=n-1,m_z=n-1>, n=140,...,160. Fix their phases by the usual real-positive radial hydrogenic functions and Condon-Shortley spherical harmonics in a single laboratory xyz frame. Their energies are E_n=-mu*C^2/(2hbar^2 n^2).

Set c_n=N exp[-(n-150)^2/100], with N positive and sum c_n^2=1. For fixed varphi,

|psi_varphi>=sum_n c_n exp[-i(n-1)varphi]|n>_c.

The full relative Hilbert space remains available to all operators and propagation. The finite set specifies only initial support; it is not a truncation of dynamics. Across blocks varphi is uniform modulo2pi; for each derivative and its matched denominator it is held fixed by the stipulated retained preparation setting. No physical synthesis or model-to-model phase pairing is assumed.

Declare a=hbar^2*150^2/(mu*C), omega=sqrt[C/(mu*a^3)], t*=pi/(4omega). This a is a comparison radius, not an equality of the packet's radius or energy with a classical point. All these quantities and the preparation remain fixed as f,g and epsilon are varied. There is no fitting to responses.

Let sigma=a/10. The CM pure state is

Phi_CM(Q)=(2pi*sigma^2)^(-3/4) exp[-|Q|^2/(4sigma^2)].

It has zero means, per-coordinate position standard deviation sigma, momentum standard deviation hbar/(2sigma), and zero symmetrized Q-P covariance. These specify a minimum-uncertainty isotropic Gaussian, not Q=P=0. Choose the fixed normalized spectator spin state (|up,down>+|down,up>)/sqrt2. The initial state is the tensor product of this spin state, Phi_CM and psi_varphi.

## Formal response definition

For each j=A,B define <R_x(t)>_j by coefficientwise perturbation about the conventional leading dynamics, retaining terms through epsilon and first order in each separately varied control. Mixed derivatives needed to isolate epsilon*g or epsilon*f are interpreted by the formal interaction-picture expansion; no exact finite-epsilon dynamics or remainder bound is asserted.

At the same fixed initial state and clock define

T_R^j(t,varphi)=partial_g <R_x(t)>_j evaluated at f=g=0,
S_R^j(t,varphi)=partial_f <R_x(t)>_j evaluated at f=g=0,
Z_R^j=T_R^j/S_R^j whenever formal division has a nonzero leading denominator.

The sole target is the coefficient of epsilon in Z_R^B(t*,varphi)-Z_R^A(t*,varphi). A common denominator and its leading value must be derived, not borrowed from the classical point preparation. Q and R raw responses must not be identified. The accepted classical contrast for comparison is [24C/(pi^2 a)]*[cos(2varphi)+sin(2varphi)]; reproducing that contrast would not establish either individual law.

Unproved preparation, physical matched controls/readout, calibration, response completeness and omitted spin/radiation/annihilation/gravitational contributions remain. No physical record, measured derivative, empirical success or native DET derivation is specified by these operators.
