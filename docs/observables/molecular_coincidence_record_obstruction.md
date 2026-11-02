# A complete coincidence record need not preserve a molecular sector

For the fixed supplied interacting quantum walk below, the normalized molecular preparation u₊ has two positive-weight record outcomes, each with a nonzero component outside the stipulated two-branch molecular sector. This independently reviewed counterexample refutes universal preservation for this instrument. It does not assert leakage for every preparation, complete loss of all molecular components or later dissociation.

The Hilbert space consists of square-summable four-coin-component sequences ψ(r), r ∈ 2ℤ, satisfying ψ(−r) = −Swap ψ(r), with norm squared Σr‖ψ(r)‖². The coincidence subspace at r=0 is the singlet. Odd separations are excluded, or the molecular projector is extended by zero on that block. The full relative Fourier zone is [−π,π), with measure dk/(2π); even-support sequences give π-periodic Fourier functions. These conventions retain the sequence norm. The one-particle symbol is WH(k)=diag(exp(ik),exp(−ik)) H, where H is the normalized Hadamard matrix; W0(k)=WH(k)⊗WH(−k). The total-momentum label p=0 defines a relative fiber, not a normalizable global plane wave. No finite ring is substituted.

The allowed preparations are ψ=c₊u₊+c₋u₋ with |c₊|²+|c₋|²=1. Apply the complete Lüders instrument N and I−N immediately, before another walk step. Every outcome label remains recorded; zero-weight outcomes have no assigned normalized conditional state. A numerical survival fraction is unnecessary for this test.

## Fixed model, molecular space and normalization

Use the supplied p=0 even-relative Fermi fiber, full relative Fourier zone[-pi,pi) with dk/(2pi), Hadamard order WH=S H, collision phase-1 and W=W0(I-2N). The relative coordinate is r=x1-x2 in2Z; coin basis is up/down. Let

    s_-=(|up,down>-|down,up>)/sqrt(2),
    e=|r=0> tensor s_-,  ||e||=1,
    z_±=(1±2sqrt(2)i)/3,
    f_±(k)=2(W0(k)-z_±I)^(-1)W0(k)s_-,
    A_±=||f_±||>0,  u_±=f_±/A_±,
    Pi=|u_+><u_+|+|u_-><u_-|.

The versioned primary eigenstate construction supplies these two admissible eigenbranches, bounded resolvents and orthogonality. They are imported model premises; this note proves a record obstruction, not a new bound-state theorem. A_± is the actual fiber norm; no capture probability or evaluated norm is substituted. Fixed p is a fiber, not a normalized global plane wave. No odd-separation or other point/flat-band state is added to Pi.

The source's eigenvector consistency condition is N f_±=e: equation4 fixes the origin component psi, and equations5–6 require N f=psi. Here psi=s_-, 1-Gamma=2, and the constant Fourier component represents e. Thus N u_+=e/A_+ is nonzero. This uses the already admitted source construction, without an approximate normalization. [Ahlbrecht et al., arXiv1105.1051v1, equations4–7](https://arxiv.org/pdf/1105.1051v1).

## A finite support witness that e is not molecular

Fix the Fourier convention phi(k)=sum_r exp(ikr)psi(r), compatible with the stated symbol. Then in the p=0 relative fiber the free shift sends coin up/down from r to r+2, down/up to r-2, and equal coins leave r unchanged. Changing Fourier sign would reflect the witness; it does not change the conclusion.

The Hadamard tensor maps s_- to -s_-. The contact multiplier first maps e to -e, so after one full step

    W e=(|2,up,down>-|-2,down,up>)/sqrt(2).

Both resulting components are noncoincident; the second contact multiplier acts as identity on them. The up/down coefficient of (H tensor H)|up,down> is -1/2. Only the r=2 component can reach r=4 at the next step. Therefore

    (W² e)_(r=4,up,down)=-1/(2sqrt(2)) !=0.

Neither e nor W e has any r=4 component. Meanwhile z_++z_-=2/3 and z_+z_-=1. Consequently the polynomial

    P(t)=(t-z_+)(t-z_-)=t²-(2/3)t+1

annihilates ran(Pi), since its two generators are W-eigenvectors at those roots. But

    (P(W)e)_(r=4,up,down)=-1/(2sqrt(2)) !=0.

Thus e is not in ran(Pi). Equivalently L=(I-Pi)e is nonzero. This is a two-step algebraic diagnostic of the specified operator, not a simulated trajectory or an extra time evolution in the record instrument. All vectors are in the fixed even Fermi fiber and W is bounded/unitary, so this polynomial has no unbounded-domain issue. The reflected r=-4 component is retained by Fermi symmetry; a single nonzero component suffices for the contradiction.

## One allowed preparation, both record outcomes

Choose the exact allowed preparation psi=u_+, corresponding to coefficients(c_+,c_-)=(1,0), hence ||psi||=1. Use the immediate supplied complete instrument K_c=N, K_o=I-N, before another walk step. Write A=A_+.

For coincidence,

    v_c=N psi=e/A,
    q_c=||v_c||²=1/A²>0,
    psi_c=v_c/sqrt(q_c)=e,
    (I-Pi)v_c=L/A !=0.

In particular the normalized recorded branch is outside the molecular sector. The weight expression is used only to establish positivity; no numerical survival fraction is calculated.

For noncoincidence,

    v_o=(I-N)psi=psi-e/A,
    (I-Pi)v_o=-L/A !=0.

Therefore v_o is nonzero and q_o=||v_o||²>0. Orthogonality of N and I-N gives q_c+q_o=1, so0<q_c<1 as well. The conditional noncoincidence state is psi_o=v_o/sqrt(q_o), with nonzero complementary component. This explicitly accounts for the other outcome rather than retaining a favorable branch or asserting all preparations behave alike.

The complete retained state is

    |c><c| tensor |v_c><v_c| + |o><o| tensor |v_o><v_o|,

of traceone. Opposite signs in the two complementary amplitude vectors cannot cancel across distinct classical record labels; neither branch is erased. For other allowed preparations, a zero-weight branch remains unnormalized/undefined under the same convention. No universal claim that every preparation leaks is needed or proved.

It follows that both tested block operators are nonzero: their action on u_+ is respectively L/A and -L/A. This one normalized preparation with positive-weight nonmolecular outcomes refutes the admitted all-preparations/all-positive-outcomes preservation statement. It does not assert that the record unbinds the system at every later time, supplies a dissociation rate or changes the underlying unitary's bound spectrum.

## Scope

The Hilbert carrier, Hadamard walk, collision phase, eigenstate construction and Lüders instrument are supplied conventional premises. Derived here are the finite polynomial obstruction and one exact complete-record counterexample. Binding is not identified with physical or native mass. No inertial/rest-energy interpretation, native units, gravity coupling, calibration or empirical evidence follows. A different instrument or preparation contract is a separate question; the fixed negative result is unchanged.

The model source is [Ahlbrecht et al., *Bound Molecules in an Interacting Quantum Walk*, arXiv:1105.1051v1](https://arxiv.org/pdf/1105.1051v1), equations 1–7 and the normalization discussion. The proof uses its eigenstate consistency condition explicitly and retains both classical record branches.
