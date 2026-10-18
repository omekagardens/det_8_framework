# RI120: bounded analytic check of the T2 sensitivity condition

26 September 2026. Source reading and manual algebra only. No scientific
certificate was decoded; no native coefficient, probability, polynomial,
H/z value, scale, solver or fixture was evaluated. No target code was
imported, parsed, compiled, probed or run.

## Result

The actual size-five strict-mixture rule proves a useful record-domain
identity: T2's complete full probability is independent of its first cap
bit. In RI117's notation, all sixteen profiles are paired,

    f2(xi+8)=f2(xi),        Q2_8=0,
    Q2_(xi+8)(x)=Q2_xi(x)  for xi=1,...,7,

as polynomial identities, not merely equality at the actual rho.

This is not a sensitivity theorem. The remaining seven complete stem
contrasts are not proved zero or nonzero by this note. Their simultaneous
vanishing at the actual rho remains the exact gap. The requested complete
all-fifteen-Q2 contract must retain and reconcile every profile, including
these analytically justified duplicates. No numerical campaign is begun.

## 1. Authority and unchanged premises

Read in full:

- /Volumes/AI_DATA/development/det-review-evidence/ri117-root-proof-review-lyl4b3a6/ROOT_ADJUDICATION.json
  (tool chunk 5d5759).
- /Volumes/AI_DATA/development/det-review-evidence/ri117-root-proof-review-lyl4b3a6/RI120_ASSIGNMENT.json
  (tool chunk 394fbe).

The accepted RI117 proof, its complete connected-parent lemma and RI111
remain fixed. The eleven-class seed, amplitude 1/4, 28-child support and
sixteen parent obligations are unchanged. The task permits only the
already retained forty-row/224-slot C3/C4/C5/H5 domain, without new
disconnected D1 data or actual execution.

Use the accepted strictly positive marked baseline, precursor locality,
equivariance, complete marked diamonds, and the RI38 deletion potential.
At parent size five the actual law is RI63's strict mixture, not a
later common half-scale. Set

    tau=c5/36>0,
    alpha_actual,c=(35/36) alpha_boundary,c+tau.

The boundary coefficients are nonnegative. RI63's accepted finite result
says every active boundary component is everywhere defect-neutral.
Consequently a component containing a defect-raising role has boundary
coefficient zero; its actual coefficient is exactly tau. This implication
does not say every neutral role has coefficient tau, or that every
size-five row is a common-scale row.

The other source texts consulted are:

- docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md,
  sections 1 and 4, including its explicit distinction between boundary
  and actual strict laws.
- docs/track_b/native_growth_ferrers_defect_v1/DEFECT.md, sections 1--2.
- docs/track_b/native_growth_four_vertex_cap_v1/DESIGN.md, sections 4--5.
- docs/track_b/native_growth_fixed_amplitude_lift_v1/AMPLITUDE.md,
  its accepted unique-minimum/unique-atom Ferrers argument and strict
  restoration of the H5 core slot.
- docs/track_b/native_joint_growth_extension_criterion_v1/CRITERION.md,
  the whole-map diamond and deletion-potential definitions.

All these repository paths are under
/Volumes/AI_DATA/development/det_8_framework-ret/.
Only text was read. Printed large constants in the source were not
recomputed or used to choose a scale.

## 2. Complete C5 proper-birth classification

Let C5 be a five-chain with ideals 0,1,3,7,15,31. Its defect is zero.
Every proper birth has one of the first five masks.

A nonempty Ferrers order has a unique minimum. If a Ferrers order is
nonchain, its down-set contains both axis-neighbour cells (1,0),(0,1);
they give two distinct atoms above its minimum. Therefore a nonchain
order with a unique atom is not Ferrers.

- Mask0 adds an isolated vertex, hence raises the defect from zero to one.
- Masks3,7,15 add a branch above respectively the first two, three or four
  chain vertices. The child is nonchain, but its sole atom is the old
  second chain vertex. It is not Ferrers. Deleting the newborn restores
  C5, so its defect is exactly one.
- Mask1 adds a short arm above the root. The child is a Ferrers hook,
  represented by the down-set with cells
  (0,0),(1,0),(2,0),(3,0),(4,0),(0,1).
  This role is defect-neutral.

This exhausts every proper ideal. Full mask31 is treated by normalization,
not by the proper ratio-component formula.

The first four raising roles therefore have coefficient tau for every
allowed marking. The neutral mask1 may have a different actual component
coefficient. Its being neutral alone does not prove its boundary
coefficient is positive or zero.

## 3. Exact held-row identities and cap-bit removal

Retain RI117's notation: xi=0,...,7 is the full three-chain marking;
eta=xi+8 sigma, sigma in {0,1}, records the next chain vertex. Write

    B_xi(S)=q_B(C4,xi,S),
    D_eta(S)=q_B(C5,eta,S),       S=0,1,3,7,
    c_xi=q_B(C4,xi,15),
    e_eta=q_B(C5,eta,15),
    ell_eta=q_B(C5,eta,31).

C5 has a unique maximum. Each proper ideal excludes it, and its
maximal-deletion potential is exactly the corresponding complete C4
probability. C4's maximal bit is irrelevant to that complete row by
the accepted unique-top lemma. Thus section 2 proves

    D_eta(0)=tau B_xi(0),
    D_eta(3)=tau B_xi(3),
    D_eta(7)=tau B_xi(7),
    e_eta=tau c_xi.                                              (1)

All four stem slots D_eta(S) exclude the first cap vertex carrying
sigma, so they also ignore sigma by precursor locality. Define

    N_xi=D_eta(1)-tau B_xi(1).

Both terms depend only on the root record because their precursor is
mask1. Therefore N_xi depends only on xi modulo 2. Its nonnegativity
follows from the actual mixture:

    N_xi=(35/36) alpha_boundary,c(xi) B_xi(1) >= 0.                (2)

This is a formal equality, not a calculation of a boundary coefficient.

The complete C4 row is the four stem slots plus c_xi. Using its sum
one and all five C5 proper slots gives the exact full complement

    ell_eta=1-tau-N_xi.                                          (3)

Hence e and ell ignore sigma as well. No blanket permission to remove
an internal mark has been used: e's independence is a specific consequence
of the actual mixture and Ferrers classification; ell's follows only after
complete normalization.

For the accepted H5 values b=q_C4(7), d=q_C5(7) and h=q_H5(15),
the inherited twin-top diamond gives h=c d/b. Since d=tau b by (1),

    h_xi=tau c_xi,     m_xi=h_xi^2/c_xi=tau h_xi.                 (4)

Every division has a strictly positive denominator. This does not evaluate
tau, c, d, h or m.

## 4. A simplified but still unevaluated T2 profile

Let A_xi(S)=q_C3,xi(S) and G_xi(S)=q_H5,xi(S), on the four stem ideals.
Use the accepted H5 full value j and RI117's

    E=sum_S A G^3/B^3+3m+3j.

Define, solely as held symbolic ratios,

    r_xi=G_xi(1)/B_xi(1),
    H_xi=A_xi(1)G_xi(1)^3/B_xi(1)^4.

The label H here is not a new seed multiplier. Both ratios use positive
denominators; neither is evaluated. Since every term has precursor1,
r and H depend only on the root bit.

RI117 gives the complete size-six proper sum

    E2=sum_S D G/B + e h/c + h+j+ell.

Substitute (1)--(4), retaining the entire H5 row identity
sum_S G=1-2h-j. This yields

    E2_xi=1+(1-tau)(h_xi+j_xi)+N_xi(r_xi-1).                     (5)

Likewise its cubic T2 expression is

    C2=sum_S A G^3 D/B^4+e h^2/c^2
      =tau(E-2m-3j)+N H.                                        (6)

Thus define the complete polynomial coefficients

    A2_xi=E_xi+2+2(1-tau)h_xi+(1-2tau)j_xi
               +2N_xi(r_xi-1),
    B2_xi=2m_xi+2j_xi+1-tau-N_xi,
    C2_xi=tau(E_xi-2m_xi-3j_xi)+N_xi H_xi.                      (7)

They are precisely RI117's coefficients after justified symbolic
substitution, not new fitted coefficients. The full profile remains

    f2(xi)=1-s[3-rho A2_xi+rho^2 B2_xi+rho^3 C2_xi].              (8)

All right-hand sides ignore sigma. Therefore the complete sixteen-row
polynomial family obeys the identities stated under Result, including
the exactly zero eta=8 reference contrast.

No record at a different stem vertex is erased by (7) without an
additional proof about E,h,j. The root-only dependence of N,r,H does not
by itself imply root-only dependence of the whole expression.

## 5. What remains unproved

For xi=1,...,7 define the unchanged reference contrasts

    Q2_xi(x)=-(A2_xi-A2_0)
                 +x(B2_xi-B2_0)+x^2(C2_xi-C2_0).                (9)

Then

    f2(xi)-f2(0)=-s rho Q2_xi(rho).

Consequently f2 is constant exactly when all seven expressions (9)
vanish at the fixed actual rho. Combined with the proved duplicate
identities, this is equivalent to all fifteen conditions in the
assigned complete contract.

The following invalid shortcuts are specifically excluded:

- Nonconstant E, j, h or a different T1 profile does not establish a
  nonzero value of their new linear/quadratic combination.
- An identically nonzero Q2 polynomial can still vanish at the actual
  rho. Nonzero coefficients alone do not prove sensitivity.
- Actual tau is the size-five strict restoration coefficient c5/36.
  Replacing it by rho, or assigning every q5 proper slot the same
  coefficient, changes the baseline.
- N>=0 does not prove N differs between records or vanishes. Nor does
  it determine cancellations with the other held terms.
- A selected root cannot be substituted for the fixed actual rho.
- Cap-bit independence does not prove complete record constancy.

No published identity read for this bounded examination settles all
the remaining contrasts or provides a required nonzero actual value.
This is an exact identified gap, not a proof that no stronger analytic
argument could exist.

The existing forty complete held rows/224 slots already contain all
arguments of (9). No new disconnected shape or native query is necessary
to define the complete assigned source-only certificate if root chooses
that fallback. Such source work must still retain all sixteen profiles,
all fifteen quadratics including zeros, and every complete held row.
This note does not create that source, an executor, active admission,
freeze, candidate, scientific report or new gate.

## 6. Work boundary

Only this fresh external note is authored. Accepted RI117 files and
earlier evidence remain unchanged. No repository, index or Git action
occurs. The note neither rejects the fixed 28-child support nor establishes
a positive extension, because actual connected sensitivity remains open.

The positive T1 family and all sixteen parent conditions, including
shared-variable D1 compatibility and the other twelve parent systems,
remain exactly as accepted. No full QM, geometry, gravity or empirical
conclusion follows. Independent analytic review is required before any
new conditional identity in this note is accepted.

