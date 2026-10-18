# Shared affine compatibility and an explicit small amplitude continuation

30 September 2026, Honolulu. Conditional manual theorem for independent review.

The exact shared affine equations admit a simple symbolic solution:

    t0=t2=t3=0,    w_j=z_j,    v_j=0,    d_i=0.              (S1)

Its only nonzero eight-child directions are y_Jj=z_j/e_j on the
eleven empty-birth children. All disconnected equations vanish because
their complete sums are precisely the accepted lower seed harmonic
equations. This checks the global shared system, not merely its two
local intervals.

Define the distinct prospective family's empty-child amplitude ceiling

    a_empty = min_{j:z_j<0} e_j/(-z_j).                      (S2)

Then

    0<a_empty<a_star<1/4,                                  (S3)

and (S1) is a strictly positive H30 continuation through eight births
for every 0<a<a_empty, conditional on the accepted finite baseline,
seed and complete H30 iff. No numerical amplitude is selected.

The original amplitude 1/4 rejection remains unchanged. The exact full
H30 feasible range above a_empty is not settled here. Neither an
all-size record-blind continuation nor quantum, geometric or physical
dynamics is established.

## 1. Original variables and the complete shared equations

Use the same e_j, beta_j, Gamma_j and direction variables as
[AMPLITUDE_RANGE.md](AMPLITUDE_RANGE.md). The amplitude a enters strict
positivity, not the signed affine equations after division by a>0.

The free tuple in RI127 RESULT sections 3 and 5 is

    x=(t0,t2,t3,w4,w5,w6,w7,w8,w9,w10,w11).                 (S4)

The reference and full correction recovery at T1 is

    v1=beta_10*t0+beta_12*t2+beta_13*t3,
    w1=1-Gamma_10*t0-Gamma_12*t2-Gamma_13*t3,                (S5)
    t0>-1/a,    v1>-1/a,    w1>-e_1/a.

Here beta_1m=-Delta_1 k_1m/Delta_1 f1 and
Gamma_1m=k_1m(0)+f1(0)*beta_1m. The accepted nonzero T1
pivot and all-record contrast identities justify this recovery.
No new signs for beta_1m or Gamma_1m are presumed.

For T2 and T3, retain the whole open intervals (A8), with exactly the
same shared t2,t3 and w2,w3 recovered by (A6), not per-parent copies.
For each of the eight other connected parents j=4,...,11,

    (z_j-w_j)*(f_j(r)-f_j(0))=0  for every record r,
    -e_j/a < w_j < z_j+f_j(0)/a,
    v_j=(z_j-w_j)/f_j(0).                                   (S6)

A nonconstant full profile forces w_j=z_j; a constant profile leaves
its intercept free within the strict interval. No division by a zero
contrast occurs, and no additional record quotient is assumed.

For clarity, write a_C3,b,c,d,e_held,g,h_held,j_held,ell for the
held symbols in RI127 RESULT equation 12. They are lower-row
probabilities, not the amplitude a, split h or private corrections d_i.
The complete disconnected sums are

    L1=rho[(a_C3*g^3/b^3)*w1
                      +3*(h_held^2/c)*w2+3*j_held*w3],
    L2=rho[(d*g/b)*w2+(e_held*h_held/c)*w4
                      +h_held*w5+j_held*w6+ell*w7],
    L3=rho[g*w3+2*h_held*w6+j_held*w8],
    L4=rho[(d^2/b)*w4+(e_held^2/c)*w9+2*ell*w10],
    L5=rho[d*w7+e_held*w10+ell*w11].                         (S7)

All records and individual supported ideals remain. The factors 3
and 2 count distinct slots. L1/L3 carry the original xi restrictions;
the other rows carry eta. This is not a new reduction of g_i(r),
the full disconnected-parent profile.

For i=1,...,5 the exact remaining equations and recovery are

    g_i(0)*L_i(r;w)-g_i(r)*L_i(0;w)=0  for every record r,
    d_i=-L_i(0;w)/(e_Ci*g_i(0)),
    L_i(0;w)<e_Ci*g_i(0)/a.                                (S8)

The denominator e_Ci*g_i(0) is strictly positive. The last line is
exactly d_i>-1/a, with its direction checked after multiplying by
positive factors. The source's original factor 4 has been replaced
by 1/a only for this separately labelled family.

In particular the old amplitude-specific D1 consequence
w1<W_star<4/41 is not carried over as an unchanged restriction.
Its derivation used the original positivity bounds. The governing
condition for the prospective family is (S8).

Together, (S5)-(S8), the T2/T3 intervals, and the recovered child
variables are the original complete H30 iff with symbolic amplitude.
No parent or child is omitted: there are eleven J directions, eleven
F directions, three Y directions and five private D directions.
All unsupported child directions remain zero.

## 2. The amplitude independent affine consistency question

After all reference recoveries, the remaining equalities are exactly

    (z_j-w_j)*(f_j(r)-f_j(0))=0,    j=4,...,11,
    g_i(0)*L_i(r;w)-g_i(r)*L_i(0;w)=0,    i=1,...,5,         (S9)

where w1,w2,w3 are their affine expressions in t0,t2,t3 and
w4,...,w11 are retained as shared variables. Thus (S9) is a finite
affine system in x with fixed coefficients and no amplitude.

Shrinking a can relax its positivity inequalities but cannot cure an
inconsistent affine equality. It would be insufficient to know only
that each local T2/T3 interval is nonempty. Here, however, the admitted
seed equations supply a solution of the complete equality system.

## 3. Exact identification with every lower seed equation

The inherited explicitly admitted RI85 DESIGN equation 10 gives,
for the same accepted normalized eleven-coordinate seed,

    (a_C3*g^3/b^3)*z1+3*(h_held^2/c)*z2+3*j_held*z3=0,
    (d*g/b)*z2+(e_held*h_held/c)*z4
                       +h_held*z5+j_held*z6+ell*z7=0,
    g*z3+2*h_held*z6+j_held*z8=0,
    (d^2/b)*z4+(e_held^2/c)*z9+2*ell*z10=0,
    d*z7+e_held*z10+ell*z11=0.                              (S10)

The RI85 symbol f for the C5 full slot is the RI127 symbol ell.
This is a notation translation, not equality of unrelated profiles.
The five ordered coefficient rows and each repeated ideal occurrence
match (S7) term for term.

The seed's simultaneous harmonicity is an accepted RI88 premise.
The RI85 design alone did not prove existence of that seed; its
historical unevaluated language is not promoted to acceptance here.
The current accepted seed supplies the zero equalities in (S10).

Those equations retain every compact xi/eta representative and their
complete six-parent record cubes. In a disconnected parent the
restriction to its original six-parent is the same record used in
(S10). Thus every original disconnected-parent marking, including
either added-isolate bit, has

    L_i(r;z)=rho*0=0,    i=1,...,5.                          (S11)

No value, constancy, record restriction or numerical determination
of g_i(r) is needed: both terms of its contrast in (S8) multiply zero.
This is not the invalid inference that a nonconstant profile forces a
private correction to vanish. Here d_i=0 follows directly from the
proved L_i(0;z)=0 and its positive denominator.

## 4. Verification of the complete signed solution

Take the free tuple

    x0=(0,0,0,z4,z5,z6,z7,z8,z9,z10,z11).

At T1, (S5) gives v1=0 and w1=1=z1. At T2/T3,
(A6) gives v2=v3=0 and w2=z2,w3=z3. Every j>=4
in (S6) likewise has w_j=z_j and v_j=0, so every connected
reference and contrast equation is satisfied. All five disconnected
reference and contrast equations follow from (S11), with d_i=0.

Hence (S1) is a concrete symbolic solution of every affine equality,
with each occurrence of a shared variable assigned the same value.
It does not reconstruct the seed from a matrix or compute any
coefficient. It substitutes the accepted seed symbols into their
accepted exact equations.

In terms of the original thirty child directions, the solution is

    y_Jj=z_j/e_j,    j=1,...,11,
    y_F(Tj)=0,      j=1,...,11,
    y_Y0=y_Y2=y_Y3=0,
    y_F(Di)=d_i=0,  i=1,...,5.                              (S12)

Some allowed support directions being zero does not enlarge or change
the H30 support. It is permitted by the original interval equations.

## 5. Strict positivity of this global subfamily

The finite negative seed set is nonempty because z2<0. Each e_j is
a strictly positive, record-blind baseline empty probability, and
every negative z_j is a finite fixed number. Therefore (S2) is a
positive finite minimum, attained by at least one seed index.

For the solution (S12),

    1+a*y_Jj=1+a*z_j/e_j.

If z_j<0 this is positive exactly when a<e_j/(-z_j).
If z_j>=0 it is positive for every a>0. Every other eight-child
multiplier is identically one. Thus the exact strict positive
amplitude interval for THIS FIXED CHILD DIRECTION is

    0<a<a_empty.                                           (S13)

At a=a_empty at least one J multiplier is zero, so the endpoint
does not give a positive law. Beyond it, this particular direction
fails. Other directions have not thereby been excluded.

Because z2<0 and Gamma_2>0,

    a_empty<=e_2/(-z2)
             <(e_2+Gamma_2)/(-z2)
             =a_star<1/4.                                 (S14)

Consequently all seven-parent multipliers satisfy
1+a*z_j>=1-a>3/4 for a in (S13). Off the seven-parent seed
support they remain one. All smaller multipliers are unchanged.
The entire proposed finite transform is strictly positive.

The complete H30 iff and the verified harmonic equations therefore
establish a conditional positive extension through eight births for
this distinct small-amplitude subfamily. Equivalently, the standard
baseline transform uses the ratios of these positive parent/child
multipliers; normalization follows from the complete harmonic rows.
The shared terminal multipliers preserve the inherited diamond
identities. Records and the scalar-passive quantum payload are
unchanged, not newly derived.

## 6. Precisely what is and is not left open

Let F be the set of positive amplitudes for which some child direction
on this SAME H30 support and normalized seven-parent seed direction
gives the full positive extension. The two proved inclusions are

    (0,a_empty) subset F subset (0,a_star).                 (S15)

The first follows from the complete signed solution and strict bounds
above. The second follows from the necessary exact T2 interval.
The strict separation a_empty<a_star leaves a genuine undecided
range: another shared direction may or may not work at a_empty or
between it and a_star. We have not found the maximal full amplitude,
and no numerical amplitude or coefficient has been selected.

Any later question about that range must retain the concrete
simultaneous strict system (S5)-(S8) with the same unknowns.
Affine consistency itself is now settled by (S1); it would not be
progress to ask for another rank or generic consistency test.
Optimizing or executing that system is not authorized or begun here.

The accepted amplitude 1/4 obstruction is immutable. This theorem
does not infer an all-size record-blind transform, persistent width
gain, informative quantum dynamics, Lorentzian geometry, gravity,
mass or empirical correspondence. No executable qualification credit
is claimed. RET remains paused; no measurement, repository, Git,
fixture, runtime, scientific-body read or automated proof calculation
is part of this source-only work. Stop for independent adjudication.
