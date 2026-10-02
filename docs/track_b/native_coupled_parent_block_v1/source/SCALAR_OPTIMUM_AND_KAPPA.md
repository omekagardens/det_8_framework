> Public redacted derivative. The prose below records historical research and review; local paths, private file fingerprints and execution identifiers have been obscured. Raw custody, host/runtime logs and administrative scripts are withheld. Claims about exact copies, complete transcripts, byte identities, manifests or execution permissions describe the private original archive, not this derivative. Only the new PUBLICATION_MANIFEST.json hashes verify the redacted payloads. This copy grants no execution authority and cannot replay original custody checks.

# Attained scalar optimum and the canonical kappa condition

1 October 2026, OBSCURED-LOCATION. RI264 manual author result pending independent
adjudication. Use the same actual fixed rest, residual caps and notation
as FIXED_REST_BLOCK.md. No cap, active line, breakpoint or canonical
coordinate is numerically evaluated in this note.

The proposed scalar reduction is correct. Its maximum is attained
among at most nine endpoint/intersection candidates. The ORIGINAL
lexicographic selector chooses the smallest maximizing r, including
flat intervals. This gives an exact conditional formula for kappa
and a strict right-derivative test when the tau cap lies inside
the scalar domain. These are necessary conditional identities at
the global canonical point, not sufficient global certificates.

## Concavity and exact finite attainment

Put A=3p/80>0, B=7p/240>0 and c=7p*(n_0+n_1)/480>0.
For each j define three affine functions

    f_Cj(r)=N_j,   f_0j(r)=(R_0j-r)/n_0,
    f_1j(r)=(R_1j-r)/n_1,

    g_j(r)=min{f_Cj(r),f_0j(r),f_1j(r)}.                (S1)

With b=v*T>=0 and D=[0,Rmin],

    F(r)=A*r+B*min(r,b)+c*(g_0(r)+g_1(r)).              (S2)

A minimum of finitely many affine functions is concave: for any
u,w in D and 0<=theta<=1, each affine value at theta*u+(1-theta)*w
is at least theta*min f(u)+(1-theta)*min f(w); taking their minimum
preserves that lower bound. The same argument applies to min(r,b).
Thus F is concave. It is continuous and piecewise affine because
its finitely many affine branches can change their order only at
pair intersections. No optimizing engine is needed for this claim.

Form the following exact set C of DOMAIN-VALID candidate values:

    0 and Rmin;

    b, if 0<=b<=Rmin;

    R_0j-n_0*N_j and R_1j-n_1*N_j, for j=0,1,
       each only if it belongs to D;

    (n_1*R_0j-n_0*R_1j)/(n_1-n_0), for j=0,1,
       only if n_1!=n_0 and the value belongs to D.      (S3)

Remove duplicate VALUES, not record constraints. There are at most
nine values before duplicates: two endpoints, one tau hinge and
three pair intersections per j. Each constant-line intersection
is obtained by solving N_j=(R_lj-r)/n_l. The nonparallel line
intersection comes from

    n_1*R_0j-n_0*R_1j=(n_1-n_0)*r.

If n_0=n_1, the two sloping lines are parallel. Unequal R values
make the smaller intercept the lower line everywhere; equal R
values make the lines coincident everywhere. In neither case is
division by n_1-n_0 allowed or needed. Constant lines cannot be
parallel to either sloping line because n_l is finite and positive.

A pair intersection can be dominated by the third line and therefore
not be a true hinge of g_j. Keeping it in C is harmless: it is a
feasible domain point, and it only subdivides an affine interval.
Likewise different intersections can coincide with one another,
b or either endpoint. Domain filtering uses exact inequalities
and includes equality. No estimated crossing or grid is used.

Between consecutive distinct values of C, no noncoincident branch
order can change and the min(r,b) choice cannot change. Therefore
F is affine on each such open interval and, by continuity, on its
closed endpoints. Its maximum on that segment is at an endpoint,
unless the segment is flat, in which case every point has the
same endpoint value. For a singleton domain C={0}, evaluation
at that one symbolic point is the entire assertion. Hence

    Fmax=max_(q in C) F(q),                            (S4)

and this is an EXACT attained maximum, not a sampled approximation.
Compactness also guarantees existence directly. The formula does
not evaluate the actual value of any F(q).

The maximizing set is a nonempty closed interval [r_-,r_+],
possibly a singleton: concavity makes the set convex, and continuity
makes it closed. Its left endpoint is a candidate. Otherwise it
would lie in the interior of one of the affine segments above:
nonzero slope would contradict maximality, and zero slope would
make the preceding endpoint a still smaller maximizer. Thus

    r_-=min{q in C:F(q)=Fmax}.                          (S5)

This finite formula retains an entire flat maximizing interval;
it does not claim that every maximizing r is one of nine points.
Dominated candidates inside a flat interval remain harmless.
Both endpoints are retained even when b lies outside D.

## The actual original lexicographic endpoint

The fixed-r primary-best block is unique by B17–B18. All other
original coordinates are fixed, including any coordinates whose
keys interleave with the changed ones. The actual order satisfies

    kappa_i precedes tau_i,
    tau_i precedes BOTH nu_(i,0) and nu_(i,1).           (S6)

Here is the complete structural justification needed for this use.
RI248 CANONICAL_BINDING gives the component roots

    root(kappa_i)=(8590,17,i),
    root(tau_i)=(8604,17,i).

RI231 exhausts each nu component through P and P_nu. The minimum
relation code of P is 8730. P_nu has a unique top above all other
vertices, so in every topological five-carrier labeling, vertex 3
precedes top vertex 4; that relation alone contributes 2^19. The
accepted topological-minimum lemma prevents a nontopological
permutation from lowering the minimum. Both parent minima exceed
8604, whatever the selected-ideal and record masks. Thus S6 holds
for both compulsory a marks without an original index lookup.

For any two primary-maximizing values u<w, consider B18.
If w>b, then kappa(w)>kappa(u): the function (r-b)_+ is strictly
increasing beyond b and is zero at and below b. Kappa is the first
of the four changed coordinates, so the u block is lexicographically
smaller. If w<=b, both kappas vanish, but tau(u)=u/v<w/v=tau(w).
Tau precedes both nu, so again the u block is lexicographically
smaller, regardless of the later nu changes.

These cases exhaust u<w, including u<b=w. They prove the unique
conditional primary-plus-original-lex block is B18 at

    r*=r_-,
    kappa*=(r*-b)_+/a0,
    tau*=min(r*,b)/v,
    nu_j*=min{N_j,(R_0j-r*)/n_0,(R_1j-r*)/n_1}.         (S7)

It would be invalid to choose the largest maximizing r, an arbitrary
plateau point or merely an arbitrary primary optimizer. S6 compares
every coordinate that may increase or decrease, not just kappa/tau.

## Exact right slopes from all active lines

For any q<Rmin, let E_j(q) be the nonempty set of lines in S1
whose value equals g_j(q). Keep every tied active line. Define

    d_j(q)=max(
        {0 if C is active}
        union {1/n_0 if 0 is active}
        union {1/n_1 if 1 is active}
    ).                                                  (S8)

An inactive line has a strictly positive gap at q. Because there
are finitely many finite affine lines, for a sufficiently small
positive step no such line can replace the tied active minimum.
Among active lines the one with the smallest slope wins to the
right. Thus the exact right derivative is

    g_j,+ '(q)=-d_j(q).                                 (S9)

This argument also treats parallel or coincident lines. For example,
a constant tied with a decreasing line does NOT give a zero right
slope; the negative slope wins. S8 is defined only through actual
active equalities, not by selecting a preferred cap in a tie.

For q<Rmin the complete right derivative is therefore

    F_+'(q)=A+B*1_(q<b)-c*(d_0(q)+d_1(q)).               (S10)

At q=b the min(r,b) term has zero right slope. It is not assigned
its left slope B. At q=Rmin there is no required right derivative
inside D; endpoint cases are handled separately below.

## Sharp positivity test for the lex chosen kappa

First, if b>=Rmin, every feasible r is at most b. Formula S7 gives

    b>=Rmin => kappa*=0.                                (S11)

This includes b=Rmin, Rmin=0 and the singleton domain. No derivative
outside D is used.

Now suppose 0<=b<Rmin. The right derivative at b exists by S10.
The exact conditional test is

    kappa*>0  iff  F_+'(b)>0
              iff  A>c*(d_0(b)+d_1(b))
              iff  d_0(b)+d_1(b)<18/[7*(n_0+n_1)].      (S12)

All inequalities are STRICT. The final expression cancels the
strictly positive p using A=3p/80 and c=7p*(n_0+n_1)/480.
No n contrast is divided by. This is a test on the actual active
caps at b, not a determination of those caps or their outcome.

To prove the first equivalence, let Dplus=F_+'(b). Concavity implies
that secant slopes to the right are at most Dplus, and secant slopes
ending at b from the left are at least Dplus.

If Dplus>0, a sufficiently short positive step improves F because
F is affine immediately to the right until the next distinct
breakpoint. Every point r<b has strictly smaller value than F(b)
by the left secant bound (vacuous when b=0). Hence no maximizer
lies at or below b, so r*>b and kappa*>0.

If Dplus<0, every point r>b has F(r)<F(b) by the right secant bound.
A maximizer can occur at b or to its left, but never to its right.
Thus r*<=b and kappa*=0.

If Dplus=0, every point r>b has F(r)<=F(b), and the left secant
bound gives F(r)<=F(b) also for r<b. Therefore b is a global
maximizer, and its smallest maximizing endpoint satisfies r*<=b.
Again kappa*=0. Since b<Rmin and there are finitely many branches,
F is in fact flat on a short interval immediately to the right.
Some PRIMARY optima there have positive kappa, but the ORIGINAL
lexicographic optimum does not. This is why replacing the strict
test in S12 by a nonnegative one is wrong.

The proof works at b=0: if the derivative is nonpositive, r*=0;
if positive, r*>0. If a positive derivative leads to a maximum
only at Rmin, S12 still applies and S7 retains that closed endpoint.
An interior kink can also be the maximum. No assumption about a
smooth or unique primary maximum is made.

## Conditional necessity at the global canonical point

Let the fixed rest in FIXED_REST_BLOCK be the actual original
canonical rest. If its four actual coordinates were not primary
optimal within this restricted block, a better feasible block
would preserve every unchanged row and strictly lower the original
primary objective, contradiction. If they were primary optimal
but not S7, the smaller original lex block proved above would
preserve that primary objective and every fixed coordinate,
contradicting the original sequential selector.

Consequently S7 and S11–S12 are NECESSARY identities/tests at the
same global canonical point. In particular positive canonical
kappa requires b<Rmin, r*>b, tau*=T and the strict active-slope
condition. Tau saturation agrees with the accepted original
companion-cap consequence; it was not assumed in the derivation.

This is not a sufficient global optimum theorem. A block fixed
point can fail directions changing mu, eta, xi, sigma, other sectors
or any other original coordinate. Nothing proves that freely supplied
R,N,T values arise from the same feasible rest, much less from the
actual primary and sequential canonical optimum. No full dual is
constructed and no original dual row or reduced cost is waived.

Remaining actual premises include the full feasible fixed rest,
the lower coefficients and marked t_K*mu values entering each R,
all other P_nu contributions entering each N, the companion
allocations entering T, their simultaneous compatibility with every
unchanged original constraint, the active cap lines and exact
maximizing endpoint. The symbolic formulas do not acquire any of
these values. They do not decide the cross-sector kappa gap, C_b,
a full normalized witness or a signed inconsistency.

## Stop and preserved original system

RI262 already closed every support pattern in its circulation
family. This result addresses a different, complete four-coordinate
block with coupled residual capacities; it does not reopen or extend
that support enumeration. Stop at this proof for independent root
adjudication. No successor or source acquisition is assigned.

Retain all original equations, recovery, actual offsets/selector,
u2=-1, hook d=0!=d7 and full normalized existence iff actual C_b=0,
as referenced in FIXED_REST_BLOCK. All records, ideals, newborns,
strict endpoints, fifteen typed/raw boundaries and the 423-source
manifest remain unchanged. All original literal exceptions including
RI250 remain closed. No scientific body/hash/checker or JSON route,
mathematical engine, new coefficient/support/cap acquisition,
graph/vector/H/z reconstruction, subject execution, measurement/RET,
repository/Git/index or publication operation is used. Administrative
identity checks are not theorem execution or independent acceptance.
Option B and Status M remain unchanged; no full-QM or gravity claim.

