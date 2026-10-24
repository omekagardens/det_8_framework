# RI1468: Fair records and passive payloads are different assumptions

Accepted RI1467 gives a conditional finite result. Fair outcome probabilities can preserve every original marked record probability while changing the payload. Under completely positive outcome maps, the stronger requirement that their nonselective sum be the identity superoperator forces scalar passivity. Universal complete growth diamonds impose a separate commutation condition.

These conclusions concern a supplied matrix/instrument model. They neither derive that model from DET nor replace the accepted scalar law.

## 1. Original law and explicit alternative

A committed record C=(P,r) consists of a finite naturally labeled order and immutable binary marks. A birth appends a maximal vertex above an actual downward-closed ideal S, including empty and full ideals. Fix an admitted scalar law q(C,S) through a declared finite horizon N. Its rows are positive and sum to one; it is equivariant when order, ideals and marks are transported together, and satisfies every complete marked scalar diamond. A proper q slot reads only the selected marks, although it may read the whole unmarked parent.

The original branch is q(C,S)D/2: a fair bit and a passive positive-semidefinite payload D. The relevant model premises are supplied in [Native theorem package](../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md), lines 64–104; line 141 distinguishes admitted coefficient inputs from reconstructed tables. No new q table or continuation is supplied here.

For the alternative, supply a finite matrix algebra M_d(C), common payload identifications under relabeling, and fixed complex-linear completely positive (CP) maps I_0,I_1. They are independent of parent, precursor and marks. Assume their sum Phi=I_0+I_1 is trace preserving and define

    B_(S,b)^C(D) = q(C,S) I_b(D),       b in {0,1}.

The full state includes C and D. For nonzero PSD D, set rho=D/Tr(D) and use the supplied trace rule

    Pr(S,b | C,rho) = q(C,S) Tr[I_b(rho)],
    sum_(S,b) B_(S,b)^C = Phi.

Thus normalization on every input requires trace preservation, not Phi=id. CP makes branch weights nonnegative. Writing E_b=I_b^*(1) for the trace-dual effects, trace preservation gives E_0+E_1=1 and hence 0<=E_b<=1. Each branch is trace nonincreasing. The ideal marginal is q, while the mark distribution may depend on the current payload and is independent of S at fixed rho.

Positive q does not guarantee a positive CP branch. Zero outputs remain in complete sums and identities and are never selected or normalized. D=0 is a map input, not a preparation. Both explicit examples below have positive branches for every nonzero PSD input.

## 2. Complete diamonds and all later suffixes

At C take any ideals S,T. Let x with bit b be born above S and y with bit c above T; each second precursor excludes the other newborn. Transport all marks with their vertices. The scalar premise gives

    alpha = q(C,S) q(C+x_S with bit b,T),
    beta  = q(C,T) q(C+y_T with bit c,S),
    alpha = beta > 0.

Under the common terminal payload identification the complete route maps are

    alpha I_c composed with I_b,
    beta  I_b composed with I_c.

Therefore pairwise commutation of the outcome superoperators suffices for every contained diamond on arbitrary PSD inputs. This includes b=c, equal precursors, and full first precursors. Even when S=T=P, each second precursor is proper in the enlarged parent because it excludes the other new vertex.

Conversely, suppose complete marked diamonds hold universally on every PSD input and N>=2. At the empty base take S=T=empty and both bits. Cancelling the positive scalar coefficient gives I_c I_b(D)=I_b I_c(D) for every PSD D. Every Hermitian matrix is a difference of PSD matrices; complex linearity then extends equality to all M_d(C). Hence universal complete diamonds are equivalent to superoperator commutation in this family. For N<2 the diamond condition is vacuous. Vanishing q, a single preparation, trace-only equality or normalized-state equality would not justify this necessity proof. No particular commuting Kraus representation is required.

For a complete natural marked history h=(S_1,b_1,...,S_n,b_n), n<=N, let C_j be its actual marked prefixes. Linearity gives, even without commutation,

    w_q(h) = product_(j=1..n) q(C_(j-1),S_j),
    B_h(D) = w_q(h) I_(b_n) ... I_(b_1)(D),
    Pr(h | rho) = Tr[B_h(rho)].

All old-mark dependence remains in w_q. Summing child traces gives the parent trace at every step, so induction normalizes the complete finite law and its prefixes, retaining zero atoms without postselection.

With commutation, exchange adjacent incomparable birth labels, carry their marks, and reconstruct prefixes and ideals by restriction. This is an invertible map of structurally allowed complete histories: the reverse exchange is its inverse. Before the pair the maps agree; at the pair the full diamond equates them. Every later parent and ideal is the transported copy of its original, so equivariance equates each actual q factor and the fixed instrument supplies the same later outcome map. Composing that entire suffix with the equal pair and common prefix proves equality of complete B_h(D) for every D. Every suffix within N is included. Equal maps preserve both positive and zero weights, restricting the transport to a probability-preserving bijection on each fixed source's positive histories.

Commutation on one shared matrix carrier is algebraic. It is not spacetime locality.

## 3. All-input fairness preserves the record law

Fairness means trace halving for every current PSD input:

    Tr[I_b(D)] = Tr(D)/2    iff    E_b = 1/2.

Here 1 denotes the matrix identity. The reverse implication follows from the trace pairing. For the forward implication, every rank-one PSD test has zero pairing with the Hermitian difference E_b-1/2, so that difference has zero quadratic form and vanishes. Fairness on a restricted preparation set is weaker.

Apply trace halving successively to the positive intermediate outputs in the history factorization:

    Pr(h | rho) = 2^(-n) w_q(h),       Tr(rho)=1.

This is exactly the full original natural marked law and every prefix law for the fixed q, instrument and initial committed record. The calculation itself needs no commutation; commutation separately supplies growth diamonds and transport. Records are independent of the initial payload, so common processing of those records cannot reveal it. This says nothing about a newly supplied payload readout or the payload remaining unchanged.

For a counterexample supply a qubit, Z=diag(1,-1), and

    I_0(D)=D/2,       I_1(D)=ZDZ/2.

Kraus operators 1/sqrt(2) and Z/sqrt(2) prove CP. These maps commute and have effects 1/2. Yet their nonselective channel is

    Phi(D)=(D+ZDZ)/2=diag(D_00,D_11).

It is trace preserving but not id: it sends the projector onto |+>=(|0>+|1>)/sqrt(2) to the maximally mixed state. Every selected branch has probability q/2>0. Conditioned on the bit, the normalized payload is rho or Zrho Z; after m outcome-one marks it is Z^m rho Z^m. The record still has probability 2^(-n)w_q(h). It identifies the known transformation that occurred, not the unknown initial state. Fairness therefore does not force scalar-passive outcome maps.

## 4. Identity of the nonselective channel is stronger

Assume now I_0+I_1=id on the whole matrix algebra, not merely equality of traces. Under CP this forces

    I_b=p_b id,       p_b>=0,       p_0+p_1=1.

For a finite proof use the unnormalized vector Omega=sum_j |j,j> and Choi convention J(T)=(id tensor T)(|Omega><Omega|). CP gives positive J(I_b), with

    J(I_0)+J(I_1)=|Omega><Omega|.

For any v perpendicular to Omega, both nonnegative quadratic forms sum to zero, so each is zero. Positivity, via the positive square root, implies J(I_b)v=0. Each Choi matrix is therefore supported on the one-dimensional span of Omega and equals p_b|Omega><Omega|. Their sum fixes p_0+p_1=1. The matrix-unit blocks of the Choi matrix determine T, proving the asserted maps without an extra dimension factor.

Without fairness the scalar probabilities may be biased or zero. Positive branches leave normalized payloads unchanged and have history law w_q(h) product_j p_(b_j). All-input fairness fixes p_0=p_1=1/2, recovering exactly qD/2. Scalar maps commute.

This proof uses CP and identity on the entire supplied matrix domain; it makes no unchecked merely-positive-map or restricted-cone extension. Trace preservation constrains traces, not the rank-one Choi sum above. Normalization, fairness, scalar passivity and identity nonselective channel must not be conflated.

## 5. Informative commuting filters when fairness is relaxed

Supply 0<eta<1, a_+=(1+eta)/2 and a_-=(1-eta)/2, and set

    K_0=diag(sqrt(a_+),sqrt(a_-)),
    K_1=diag(sqrt(a_-),sqrt(a_+)),
    I_b(D)=K_b D K_b^dagger.

The diagonal Kraus operators commute, so their outcome superoperators commute. Their effects (1+eta Z)/2 and (1-eta Z)/2 sum to 1. Normalization, all complete diamonds and the full transport proof apply. For normalized rho,

    Pr(b | rho) = [1+(-1)^b eta Tr(Zrho)]/2,
    Pr(S,b | C,rho) = q(C,S) Pr(b | rho).

The mark probabilities lie in [(1-eta)/2,(1+eta)/2], strictly inside (0,1). Invertible K_b preserve nonzero PSD payloads, so every allowed finite history is positive. Eta=1 can lose positivity and is excluded; eta=0 recovers id/2.

The nonselective channel preserves diagonal entries and multiplies off-diagonal entries by sqrt(1-eta^2), so is not id for eta>0. Different Z populations can be distinguished statistically already by the first mark. This is not perfect state identification or informational completeness. For a particular full history with n_0 zero marks and n_1 one marks,

    Pr(h | rho) = w_q(h) [
        rho_00 a_+^(n_0) a_-^(n_1)
      + rho_11 a_-^(n_0) a_+^(n_1) ].

Its effect is diagonal. The actual marked-history q weight is independent of initial rho, so different coherences with the same diagonal remain indistinguishable by the entire record. The contrast changes an explicit assumption; it supplies no native or empirical measurement advantage.

## 6. Prior credit and remaining boundaries

The supplied [QR-05A excerpt](../validation/qr-05a-quantum-births-2026-09-05/README.md), lines 7–105, already uses q times CP instruments, universal full maps and complete-history transport, with borrowed unmarked percolation and qubit operations. The present scope is the fairness/identity split for arbitrary admitted marked q and fixed outcome maps. CP/Choi facts and the supplied qubit operations are standard mathematics, not new DET derivations.

The [QR05 adjudication excerpt](../track_b/QR05_ADJUDICATION.md), lines 53–75, identifies native-growth, quantum/growth and geometry gaps. The [QR-MAP scope excerpt](../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md), lines 1–50, permits broader mass/gravity research without deriving the missing inputs. The [QR_MAP RI-08c excerpt](../track_b/QR_MAP.md), lines 413–431, instead assumes prescribed effects, same-source-cone range and repeatability, with restricted preparation reachability. Those distinct operational premises neither imply this full matrix/CP identity premise nor become proved here. Only the supplied excerpts were read; linked full originals remain attribution.

A DET-native carrier/instrument/trace-rule selection or derivation, physical preparation/readout, accessible record labels/marks, and independently justified observation and rival contracts remain absent. The enlarged state includes D; the original proper-mark restriction on q alone does not guarantee physical measurement locality. [RI1466](RI1466_RECORD_OBSERVABILITY.md)'s record-only equality does not cover a changed generating instrument or new payload access.

No additional q table, horizon or continuation, physical clock/action/work store, native discriminator, full QM, geometry/gravity, agency, empirical advantage or RI1451 escape is supplied. The original scalar model remains unchanged. The pending stronger full-branch record-locality question has no accepted answer here; its proposed condition is neither the original q-only restriction nor physical locality.

Scientific scope is separate from custody. The retained author history includes an unwritten 14,036-byte report-cap failure, first written 12,264-byte report and final 12,258-byte report/6,064-byte premises. Attributed author completion 15:09:20 UTC is distinct from preparation 15:08:57; the original complete receipt and subsequent clock are absent from this grant. Reviewer completion 15:26:06 is likewise attributed. Recovered root display clipping and cursor error, and inherited cap/patch/display/schema/missing/late/manifest-basis qualifications remain. Current hashes do not reconstruct historical completion.

Measurement/E/NE/CE actual operational inputs remain missing. Protected validation/custody, ABSTAIN, Option B/Status M, zero qualification, shared 10% stop/reset, RET-only pause and all physical/execution gates remain.
