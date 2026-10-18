# Six prescribed coefficients and the normalized witness gap

30 September 2026, Honolulu. RI231 manual conditional result for independent
review. Six admitted RI41 roots now have traced prescribed values. They
reduce the accepted lower combinations, but do not yet decide the complete
normalized H30 improvement-versus-optimality problem.

## 1. Exact source and bounded inspection

The separate RI231 six-root literal admission permits complete literal
display of the unchanged original RI41 CERTIFICATE.json solely to resolve

    (2,3,0), (6,3,0), (70,3,0),
    (70,7,0), (70,9,0), (70,9,1).

Its exact identity is 2845 bytes, SHA256
3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969.
The complete literal display and before/after identity checks are recorded
at6d68fc exit0. No scientific JSON parsing, full resolved vector, other
coordinate extraction or descendant execution was used. The old exception
remains historical; this read uses the new separate authority only.

RI41 NORMALIZATION section5 specifies zero-based indices in the original
increasing-minimum-key root list. The literal certificate prescribes
default_alpha="1/8"; an explicit override, when present at the original
index, supersedes that default.

The six matches are:

| Root | Original zero-based index | Exact provenance | Prescribed lambda |
| --- | ---: | --- | --- |
| (2,3,0) | 5 | no override at5; default | 1/8 |
| (6,3,0) | 13 | no override at13; default | 1/8 |
| (70,3,0) | 33 | explicit override "33":"203153/1000" | 203153/1000 |
| (70,7,0) | 34 | no override at34; default | 1/8 |
| (70,9,0) | 36 | no override at36; default | 1/8 |
| (70,9,1) | 37 | no override at37; default | 1/8 |

These indices were counted manually in the original list, without sorting,
filtering or reindexing it. The list's first four roots occupy0..3.
The block with first entry2 occupies4..11; (2,3,0) is its second
root. The block with first entry6 occupies12..19; (6,3,0) is its
second root. The next two blocks occupy20..25 and26..32.
The six consecutive roots beginning at33 are

    (70,3,0), (70,7,0), (70,8,0),
    (70,9,0), (70,9,1), (70,11,0).

The two unrequested neighboring roots are ordinal landmarks only; their
values are not resolved. A complete manual inspection of the override
object verifies absence at5,13,34,36,37 and the exact entry at33.
No absence was guessed from numerical key order or from an excerpt.

The accepted RI228 routing proof, not this textual lookup, establishes
that these roots are the required complete marked components. The
certificate chooses this finite law; resolving its entries is not a
derivation of their values from DET primitives.

## 2. Actual ratios and equal gamma sectors

Apply the accepted potential multipliers to the prescribed values:

    alpha_empty=alpha_singleton=5/352,
    alpha_pair=203153/8800,
    alpha_I=1/8,
    gamma_0=gamma_1=1/64.                                  (W1)

The pair calculation cancels the factor5 in
(5/44)*(203153/1000). For gamma the multiplier is1/8,
so multiplying the default1/8 gives1/64. These are manual
substitutions at the six admitted roots, not newly chosen parameters.
The preexisting alpha_I=w/e_I is now also resolved by this admitted
root. No further empty probability table is instantiated.

Retain beta_S=theta*alpha_S for all four stem ideals, with the actual
theta unchanged and unevaluated. All actual canonical coefficients,
rho and s also remain unchanged. In particular equal gamma sectors do
not imply equal kappa sectors; the coupled canonical problem still
has its actual record-dependent rows and history weights.

For any four-term held family X define the fixed linear combination

    Acal[X]=(5/352)*(X_empty+X_singleton)
                  +(203153/8800)*X_pair+(1/8)*X_I.          (W2)

This abbreviation retains all four separate ideal occurrences.
It is not a new averaging measure or a fitted set of weights.

The fixed three-chain row has A_empty=A_singleton=A_pair=1/44
and A_I=41/44. Consequently the complete K mass on ideals containing
its isolate is

    T=1-Acal[A]
     =1-(203403/387200+45100/387200)
     =138697/387200.                                       (W3)

For a manual arithmetic trace, the first two ratios sum to5/176
=250/8800. Adding alpha_pair gives203403/8800 and multiplying
by1/44 gives203403/387200. The last stem contribution is
41/352=45100/387200. This evaluates only the admitted alpha
combination T, not the other individual K probabilities.

## 3. Substitution into every accepted lower combination

Let t0=138697/387200 and chi_i=(35/36)*kappa_i. The complete
RI228 L8-L9 combinations now read

    V_H=theta^2*Acal[G]+2m+j,
    V_C=theta*Acal[D]+theta*e+ell,

    R1=theta^3*Acal[A*G^3/B^3],
    R2=theta^2*(Acal[D*G/B]+e),
    R4=theta*(Acal[D^2/B]+e^2/c),

    P_Y=1-theta*(Acal[B]+c),       T=t0,

    M2=theta^2*t0+(2theta*chi_i+chi_i^2)/64,
    M3=theta^3*t0+(3theta^2*chi_i
                           +3theta*chi_i^2+chi_i^3)/64,
    F_Y=1-theta*(Acal[B]+c+t0)-chi_i/64.                    (W4)

Products and divisions inside Acal are slotwise in the same four
stem ideals. Every denominator is inherited positive. The held
m=theta^2*c, j,e,ell and all other held rows are the actual law.
Neither the canonical term nor its zero branch is dropped.

All five original disconnected profiles become, with exactly these
substitutions,

    X=V_H+2F_Y+M2,             Z=V_C+P_Y,

    B1=4-rho*(E1+3X)+3rho^2*(j+F_Y)
                                +rho^3*(3nu+M3)+rho^4*R1,
    B2=3-rho*(E2+X+Z-F_Y)
                     +rho^2*(m+j+ell+F_Y+M2)+rho^3*R2,
    B3=2-rho-rho*(1-rho)*V_H,
    B4=3-rho*(E4+2Z)+rho^2*(2ell+P_Y)+rho^3*R4,
    B5=2-rho-rho*(1-rho)*V_C,
    g_i=1-s*B_i.                                           (W5)

E1,E2,E4,nu and every original ideal occurrence are as accepted in
RI225. This substitution preserves81 proper and5 full occurrences,
every record, every transported precursor and both newborn bits.
It does not infer that all five profiles are functions only of i.

For every original record, the five relative-row families remain

    (1-s*B_i(0))*Delta l_i(W)
                         +s*Delta B_i*l_i(0;W)=0,           (W6)

where l_i=L_i/rho are the original complete shared linear forms.
Keep the normalized recovery

    u2=-1,
    W1=-Gamma_10*u0+Gamma_12-Gamma_13*u3,
    W2=Gamma2>0,   W3=-Gamma3*u3,   Wj=Uj for j=4,...,11,

and every connected condition

    Uj*Delta f_j=0        for every record, j=4,...,11.      (W7)

The original N12 recovers the full-child corrections with positive
reference denominators. None becomes an independently selected fit.
The unchanged ten unknowns are u0,u3,U4,...,U11. The constant f8,f11
profiles leave their original freedoms subject to all(W6), not free
solutions of the whole problem.

Equivalently, using the symbolic original
H_ij=g_i(0)*Q_ij(r)-g_i(r)*Q_ij(0), every row still has the form

    -H_i1*Gamma_10*u0
    -(H_i1*Gamma_13+H_i3*Gamma3)*u3
    +sum_(j=4..11) H_ij*Uj
       =-H_i1*Gamma_12-H_i2*Gamma2.                         (W8)

Here H is not instantiated or reconstructed. Equations(W4)-(W5)
are substitutions for its inherited g factors, not an automated
matrix calculation or a change to Q, Gamma or the fixed scales.

## 4. What the six values settle and what remains

The six values settle all previously named RI41 alpha/gamma roles.
They prove gamma has no root-record contrast and make T explicit.
They do not settle chi_0,chi_1. In particular the complete actual
mixture and not just its boundary law enters M2,M3,F_Y.

[CANONICAL_CAPACITY.md](CANONICAL_CAPACITY.md) now derives the full
exceptional P row, including all four possibly active components.
It proves kappa_i<=352/41 and at least one tight P row in each root
sector at the canonical optimum. That narrows the missing allocation
question without inferring positivity or equality of the two kappas.

No complete normalized solution of(W6)-(W8), or finite signed row
combination with zero unknown coefficients and nonzero right side,
has been supplied. Actual improvement, ceiling optimality and
maximal amplitude remain open. Knowing two kappa values is a
specified remaining lower-profile premise, not a theorem that those
values alone automatically solve every connected contrast.

All inherited finite premises, shared T1/T2/T3 constraints, the other
eight connected parents, five disconnected families, q/N corrections
and strict endpoints remain. The original1/4 rejection and positive
small-amplitude family are unchanged. No all-size, full QM, geometry,
mass or gravity conclusion follows.

## 5. Source boundary

[SOURCE_REFERENCES.json](SOURCE_REFERENCES.json) preserves all inherited
boundaries and records the new exact exception separately. The two
construction texts and accepted RI228 notes/root decision supply the
analytic premises; the RI231 exception supplies only the bounded
literal coefficient read. Source authority was not expanded by links
in any manuscript.

The remaining packet is [HANDOFF.md](HANDOFF.md),
[AUTHOR_VERIFICATION.json](AUTHOR_VERIFICATION.json) and
[HANDOFF.json](HANDOFF.json). All new deductions await independent
adjudication. No automatic scientific parsing/arithmetic, full vector,
other certificate/body, graph/LP/runtime/card/fixture, H/z reconstruction,
new numerical amplitude, repository/Git/index, measurement, RET or
successor work was performed.
