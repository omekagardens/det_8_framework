> Public redacted derivative. The prose below records historical research and review; local paths, private file fingerprints and execution identifiers have been obscured. Raw custody, host/runtime logs and administrative scripts are withheld. Claims about exact copies, complete transcripts, byte identities, manifests or execution permissions describe the private original archive, not this derivative. Only the new PUBLICATION_MANIFEST.json hashes verify the redacted payloads. This copy grants no execution authority and cannot replay original custody checks.

# Projected value and original full vector selection

1 October 2026, OBSCURED-LOCATION. RI266 manual author result pending independent
adjudication. Use the complete same-rest constraints, constants and
unique eliminated coordinates in JOINT_CONSTRAINTS_AND_ELIMINATION.md.

The eleven-coordinate problem is exactly a compact four-variable
projected optimization with a concave continuous piecewise-affine
primary value. Every retained tuple has a unique primary-best
seven-coordinate completion. The original canonical choice is the
full-vector lex minimum of the reconstructed PRIMARY-OPTIMAL image,
not an invented ordering of the four retained variables.

All formulas are symbolic conditional identities. Neither the
actual rest, lower coefficients, active caps nor maximizing face
is acquired or evaluated.

## Full feasible polytope and exact projection

Let P_i be the set of eleven-coordinate vectors satisfying all
original nonnegativity constraints and J2–J8, with all other
original coordinates fixed as specified. The fixed-rest rows with
no changed coordinate remain prerequisite inequalities. They have
not been replaced by freely assigned capacities.

P_i is nonempty because the original feasible canonical point lies
in it. Its constraints are finitely many linear closed inequalities.
It is bounded: J13 gives kappa<=1/a0; J5 gives tau<=1/p; J6 and
B_nu>=0 give nu_j<=1/p and xi_lm<=1/v on every compatible row;
Q gives eta_l<=E_l<=1/v; all carrying V5 rows together give sigma<=S.
Every coordinate has a finite upper bound. Thus P_i is a compact
polytope, including any lower-dimensional or singleton cases.

Let pi retain exactly

    w=(tau,nu_0,nu_1,sigma).                            (V1)

J12–J14 prove, in BOTH directions,

    pi(P_i)=D.                                        (V2)

D can be written without minima as the following finite linear system:

    tau,nu_0,nu_1,sigma>=0, sigma<=S,

    p*tau+s_lm*sigma<=1                     for all l,m,

    p*nu_j<=1-B_nu(i,j,l,m,k)               for all j,l,m,k,

    v*tau+n_l*nu_j<=R_lj                   for all l,j. (V3)

The U>=0 condition is equivalent to EVERY displayed P_nu residual
inequality, not just one selected j. R_lj already retains all
P(k,m) minima, and the sigma cap retains all carrying V5 rows.
E_l>=0 and all fixed-rest constraints remain part of the same-point
premises. No dependency on a free coordinate is buried in a constant.

Therefore D is nonempty, convex, closed and bounded; tau,nu_j<=1/p
and sigma<=S bound it directly. The origin also lies in D under the
same feasible-rest residual conditions, but nonemptiness did not
require an invented baseline. Vanishing capacities can give faces
or a singleton; none is discarded.

## Exact value and unique image

Denote the eleven-coordinate reconstruction from J22, INCLUDING
the unchanged retained entries, by E(w). The letter E(w) is a
map; E_l remains the Q cap. This notation is symbolic and does
not instantiate an original vector or acquire an index.

Put

    A_l(w)=min{h_l*E_l,c_l0(w),c_l1(w)},
    H_lm(w)=min{n_l*U_lm(w),c_lm(w)-A_l(w)}.            (V4)

Then kappa=rho/a0, eta_l=A_l/h_l and xi_lm=H_lm/n_l
in E(w). For the original reward W of J18, the exact partial
maximum is

    V(w)=max{W(z):z in P_i, pi(z)=w}

        =(3p/80)*rho(w)+(p*v/15)*tau
          +c_nu*(nu_0+nu_1)
          +(v/32)*sum_l A_l(w)
          +(v/80)*sum_(l,m) H_lm(w)
          +c_sigma*sigma.                             (V5)

For EVERY feasible fiber vector z,

    W(z)<=V(pi(z)),
    equality iff z=E(pi(z)).                          (V6)

This is J19–J22's strict uniqueness result, not merely a proposed
substitution. E(w) is feasible for every w in D. All zero endpoints
and ties in the minima remain. The finite minima of affine or
continuous piecewise-affine functions in V4–V5 also show E and V
are continuous on D.

Consequently both the original restricted and reduced problems
attain the same primary value,

    Vmax=max_(w in D)V(w)=max_(z in P_i)W(z).           (V7)

For nonempty compact P_i its linear reward attains a maximum.
Alternatively the now-proved continuity on compact D gives the
same result. The remaining original objective is its unchanged
fixed constant minus Vmax.

## Concavity follows from partial maximization

The nested expression c_lm-A_l in V4 must NOT be called concave
merely because A_l is a minimum. Instead use the full linear
feasible system and its exact projection.

For u,w in D and 0<=theta<=1, the vector

    z_theta=theta*E(u)+(1-theta)*E(w)

belongs to P_i by convexity, and its retained tuple is
w_theta=theta*u+(1-theta)*w. The linear whole-history reward gives

    W(z_theta)=theta*V(u)+(1-theta)*V(w).

Partial maximality at that SAME w_theta then gives

    V(w_theta)>=theta*V(u)+(1-theta)*V(w).              (V8)

Thus V is concave. Equivalently its hypograph is exactly the
projection of the full linear system with one extra inequality:

    {(w,q):w in D, q<=V(w)}
       ={(pi(z),q):z in P_i, q<=W(z)}.                 (V9)

Existence of each maximizing fiber, already proved, gives equality
in V9. This proof retains the coupled Q/P_nu/V5 constraints and
does not infer concavity from a formally convenient nested minimum.

## Exact finite affine branch description

Piecewise-affine structure can be proved without computing any
cap, sampling w, running an optimizer or guessing a vertex count.
Start from the complete linear domain V3. Form closed branch cells
by choosing, with ties ALLOWED:

1. One minimizing affine expression R_lj-v*tau-n_l*nu_j for rho,
   retaining its comparisons with all four expressions.
2. For each l, one minimizing member of
   {h_l*E_l,c_l0,c_l1} for A_l, with all comparisons.
3. For each l,m, one minimizing member among ALL (j,k) expressions
   [1-B_nu(i,j,l,m,k)-p*nu_j]/v for U_lm, with all comparisons.
4. For each l,m, one minimizing member of
   {n_l*U_lm,c_lm-A_l} for H_lm, substituting the branch expressions
   already selected above and retaining their comparison.

On each such cell, every chosen expression is affine. All cell
conditions are finite linear weak inequalities. Each nonempty
cell is a closed polytope contained in D; empty choices contribute
nothing. The finitely many choices cover D, including lower-dimensional
cells and every active tie. At an overlap the selected minimum
VALUES agree, so E and V agree there.

Hence E and V are affine on each cell and continuous piecewise
affine globally. This is an exact finite branch description of the
linear system's proven partial maximum, not a branch evaluation.
No number of vertices or small candidate count is asserted.
Parallel/coincident expressions require no division and remain
under their weak comparisons.

On any one nonempty cell an affine objective has an exposed maximizing
face, possibly the entire cell. Global maxima are obtained by retaining
the maximizing faces of cells whose maximum equals Vmax. This keeps
flat faces and all their points; selecting an arbitrary representative
or a single grid point would not recover the full optimal set.

## Full primary optimal face and affine recovery there

Define

    M={w in D:V(w)=Vmax},
    P_i^*={z in P_i:W(z)=Vmax}.                         (V10)

M is nonempty and compact. It is convex by concavity of V: the
value on a segment between two maximizers is at least Vmax and
cannot exceed Vmax. P_i^* is the full exposed primary-optimal
face of the original restricted linear problem.

V6 proves the exact set identities

    pi(P_i^*)=M,    P_i^*=E(M).                        (V11)

The inverse is unique, because pi(E(w))=w. There is a further
consequence of uniqueness that helps retain the actual selector.
For u,w in M, the convex combination of E(u) and E(w) is feasible
and has reward Vmax. It therefore has to be the UNIQUE fiber
optimizer at theta*u+(1-theta)*w. Hence

    E(theta*u+(1-theta)*w)
       =theta*E(u)+(1-theta)*E(w),  u,w in M.           (V12)

Thus although E is generally piecewise affine over D, its
restriction to the full primary-maximizing set is affine.
No hidden choice of eliminated coordinates remains on a primary
tie. V11–V12 are proved from the original full feasible problem,
not imposed as a new reconstruction convention.

## Preserve the original full vector lex selector

Let iota(z) mean placing the eleven coordinates back in their
ORIGINAL component positions while every other actual coordinate
is held fixed. This is only a symbolic embedding by the admitted
component identities. It does not reconstruct H, z, an actual
canonical vector or an original index table.

The unique conditional canonical answer is

    alpha_block^*
       =lexmin_original {iota(E(w)):w in M}.           (V13)

Here "original" means the complete original sequential coordinate
order. It does NOT mean lex(tau,nu_0,nu_1,sigma), minimizing rho
first, or any guessed order among eta,xi and the other changed
coordinates. RI264's four-coordinate comparison is insufficient
when seven more coordinates may change. The admitted relative
kappa/sigma/tau keys do not by themselves order all eleven.

Existence and uniqueness of V13 do not require an invented order.
The set iota(E(M)) is compact by continuity. In the actual original
finite coordinate order, minimize its first coordinate, restrict to
that attained minimum, then minimize the next, and continue.
Each stage leaves a nonempty compact set. Fixed coordinates have
constant value and impose no new choice. After every changed
coordinate is fixed, all eleven entries agree, so there is exactly
one image vector. Retained entries are themselves part of that
image, so exactly one retained tuple w* yields it.

By V12 every coordinate restriction on M is affine. Thus these
are exactly the original sequential optimal-face restrictions,
transported through the one-to-one full image; they are not a
different reduced lex objective. No omitted early coordinate can
reverse a tie decision.

The resulting exact conditional identities are

    w*=(tau_i,nu_(i,0),nu_(i,1),sigma_i) chosen by V13,

    kappa_i=rho(w*)/a0,
    eta_(i,l)=A_l(w*)/h_l,
    xi_(i,l,m)=H_lm(w*)/n_l.                           (V14)

All eleven entries, not only the seven eliminated ones, remain
bound to the same original primary-plus-lex selector.

## What follows for kappa and what remains unresolved

At the selected tuple, J12 and V14 give the exact test

    kappa_i=0 iff some R_lj-v*tau_i-n_l*nu_(i,j)=0,

    kappa_i>0 iff EVERY R_lj-v*tau_i-n_l*nu_(i,j)>0.     (V15)

The finitely many marked minima have not been evaluated. At least
one complete P row is tight after kappa upper-bound elimination;
V15 asks whether that row has any capacity LEFT for kappa.

One can state a selector-independent sufficient dichotomy on the
whole primary face. Define the attained nonnegative values

    rho_min=min_(w in M)rho(w),
    rho_max=max_(w in M)rho(w).                        (V16)

If rho_min>0, every primary-optimal joint block has positive kappa,
so the lex choice does too. If rho_max=0, every such block has
kappa zero. If rho_min=0<rho_max, the primary face contains both
kinds; V13 must settle the canonical choice. No permission to
minimize kappa first follows without all required original order
comparisons. V16 is not an evaluated sign criterion.

RI264's one-dimensional right-derivative test does not automatically
apply to this newly freed joint problem. The sharper actual
lex-sensitive kappa sign remains unresolved unless the actual
maximizing face and original coordinate restrictions are controlled.
This packet does not assign arbitrary numeric examples or caps
to settle that gap.

If the fixed rest is the original global canonical rest, any better
joint primary block would lower the original objective while preserving
all other coordinates and rows. Any equal-primary full-vector
lex-smaller joint block would contradict the original selector.
Therefore V13–V15 are NECESSARY at that same global canonical
point. They are not sufficient for global optimality, feasibility
of independently supplied capacities, or full dual compatibility.
Directions changing mu, other sectors or any unlisted coordinate
remain outside this conditional theorem.

Actual B_Q,B_nu,D_i,R,E,S, lower probabilities, active branches,
maximizing face and full-vector lex restrictions remain unevaluated.
The global rest and all its coupled constraints remain required.
No kappa magnitude/cross-sector gap, C_b decision, normalized
witness or signed inconsistency is established.

## Original system retained and bounded stop

RI262's circulation support family remains closed. RI266 addresses
the distinct eleven-coordinate conditional block and stops at this
complete reduction and selector image. No next gate, acquisition
or successor is proposed or assigned.

Preserve all original 13 equations and 10 coordinates, u2=-1,
the complete forms/recovery and actual offsets/selector in admitted
RI248 CANONICAL_BINDING section 7. Accepted hook d=0!=d7 and
full normalized existence iff actual C_b=0 remain. No forced-zero
consequence deletes a coordinate or equation. All records, labeled
ideals, both newborns and strict-restoration endpoints remain;
the closed canonical optimization is not a substitute for that
unchanged strict law.

All fifteen whole typed/raw boundary objects, their exact 43,739-byte
raw value and the 423-source unexpanded manifest remain by reference.
All original scientific and RI250 routes stay closed. No protected
body/hash/checker or scientific JSON, new coefficient/cap/support
acquisition, mathematical engine, scientific source import/compile/AST
or execution, graph/vector/H/z reconstruction, measurement/RET,
repository/Git/index or publication operation is used. Administrative
custody checks are distinct from manual proof and independent acceptance.
Option B and Status M remain; no full-QM, geometry or gravity claim.
Root alone owns operational decisions, publication and any successor.
