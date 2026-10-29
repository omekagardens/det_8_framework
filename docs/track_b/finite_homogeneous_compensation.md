# Finite-dimensional homogeneous native compensation

This independently reviewed conditional theorem covers every fixed finite dimension d>=2 in the family below. Native admissibility is equivalent to commuting branches. At every parent, a prescribed residual row admits local conditional-mean balance exactly when it is already invariant under the total map. Records cannot compensate nonzero drift. Nonidentity maps in higher dimensions can nevertheless have nonconstant invariant rows.

## Declared finite family

Keep exactly [Part A's structural probabilities q](native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix) on binary-marked finite orders through four births: parent sizes 0–3, every actual downward ideal, immutable marks and full-slot normalization complements. A birth appends a maximal vertex with strict past its selected ideal. Distinct labeled ideal occurrences count separately.

Inherited premises are q>0, sum_S q_S=1, equivariance, proper-slot access to the whole unmarked parent and only precursor marks, and the transported structural diamond

    q(P,r,S) q(P_x,r_x,T)=q(P,r,T) q(P_y,r_y,S).              (1)

S,T may coincide. Newborn bits are arbitrary; second precursors are old subsets excluding the other newborn. Thus the births are incomparable. The empty factor is 1; the singleton empty-slot factor is 2/3 for either mark.

Fix nonnegative real d-by-d matrices C_0,C_1, independent of parent, ideal, birth number, old marks and history. Their sum K is column-stochastic; each effect e_b=1_d^T C_b is strictly positive in every coordinate. The common cone is R_+^d; vertex relabeling acts trivially. Dimension stays fixed within each history. Each local input domain is the full simplex Delta_d={rho>=0:1_d^T rho=1}. Define

    B_(S,b)=q(P,r,S) C_b.                                    (2)

This optional factorization replaces the original fair passive carrier prescription, without an extra 1/2. Individual matrix entries may vanish. No quantum carrier, irreducibility, invertibility, diagonalization or convergence premise is imposed.

## Full native admissibility

The complete branch sum is K and every mass p_(S,b)=q_S e_b rho is positive, including at simplex boundaries. The child C_b rho/(e_b rho) is nonnegative and normalized, so every allowed continuation remains supported. Fixed C adds no old-data dependence; locality and equivariance follow from q, including full old ideals becoming proper after another birth.

For bases of size at most two, the complete incomparable-birth maps are

    q(P_x,r_x,T) q(P,r,S) C_c C_b,
    q(P_y,r_y,S) q(P,r,T) C_b C_c.                            (3)

Equation (1) equates the positive scalar factors for all inherited markings, ideal pairs and full-to-proper transports. At the actual empty-base, equal-empty-precursor, unequal-bit diamond, these maps are (2/3)C_1 C_0 and (2/3)C_0 C_1. Equality on the full carrier forces commutation by cancelling that positive scalar.

Conversely commutation equates (3) for unequal bits; equal bits already agree. After transport the marked endpoints coincide, so corresponding suffix maps coincide even when their precursors contain either newborn. Left multiplication by suffixes and right multiplication by preceding histories preserve equality.

Two natural birth orders of one final marked order connect by adjacent incomparable swaps: move the next desired vertex leftward, crossing only incomparable vertices because both orders respect the partial order, and repeat. Through four births each swapped pair has base size at most two. The proved diamonds and suffixes therefore cover complete finite history consistency. Admissibility is exactly C_0 C_1=C_1 C_0 at this scope, in every declared dimension.

## Stationary effects and the no-drift theorem

At a parent with n actual ideals, E_P has all 2n rows eta_(S,b)=q_S e_b and total map K. Positivity of q gives W=rowspan(E_P)=span{e_0,e_1}, retaining every record occurrence.

Let ell be any prescribed finite real row, h=ell(I-K), and U_(S,b) arbitrary finite real child values independent of hidden source, posterior state and traversal history. Parent value is zero. The target is

    U^T E_P rho + ell K rho = ell rho   for all rho in Delta_d.

Every coordinate basis input is admitted, so this is equivalent to U^T E_P=h. Feasibility initially means h in W, with all solutions U_*+ker(E_P^T). This row argument is valid in dimension d, without importing a two-state criterion.

Commutation gives C_b K=K C_b, hence

    e_b K=1_d^T C_b K=1_d^T K C_b=e_b.

Thus W lies inside the stationary-row space H={ell:ell K=ell}; any compensable drift h must satisfy hK=h.

Every algebraic power K^m is nonnegative and column-stochastic by induction. Each coordinate of ell K^m is a convex combination of ell's entries, so

    ||ell K^m||_infinity <= ||ell||_infinity.

If h=ell-ell K and hK=h, another induction gives ell K^m=ell-mh: multiplying the m identity by K yields the m+1 identity. Consequently

    m |h_j| <= 2 ||ell||_infinity

for every coordinate j and every positive integer m. A nonzero h_j contradicts this fixed bound for sufficiently large m. Therefore h=0. These are algebraic powers of one supplied stochastic matrix, not extra native births or a convergence assumption.

The complete criterion is therefore

    local balance exists for ell  iff  ell K=ell.            (4)

For invariant ell, U=0 works and all solutions are ker(E_P^T). For noninvariant ell, none exists. Reducible, periodic, singular and all other supported boundaries are included. Nonzero individual null-record values do not compensate nonzero drift.

## All rows, records and gauges

H contains the constant mass row and has dimension d-rank(I-K). Thus a nonconstant feasible row exists for a fixed member exactly when rank(I-K)<=d-2. Feasible row classes modulo span{1_d^T} have dimension d-rank(I-K)-1; their nonzero classes are the nonconstant target. These criteria preserve the prescribed numeric row and are independent of parent.

For an invariant row, put v_b=sum_S q_S U_(S,b). The exact record condition is

    v_0 e_0 + v_1 e_1=0.                                    (5)

Uniquely write U_(S,b)=v_b+w_(S,b), with sum_S q_S w_(S,b)=0 for each bit. Because e_0+e_1=1_d^T, effect rank is one precisely when e_0=p1_d^T, 0<p<1; otherwise it is two. Rank one requires p v_0+(1-p)v_1=0; rank two requires v_0=v_1=0.

The averaging map is onto by choosing constant values within each bit. Each weighted-zero w family has n-1 free values: a positive q fixes the last from the others. Thus every record freedom is accounted for, with total dimensions 2n-1 or 2n-2, respectively. At empty n=1 these give one or zero. Only actual q weights and n vary with parent.

Constant mass offsets in ell leave its drift unchanged. Fixed nonzero scaling relates solution pairs without replacing a prescription; kernel additions change only null records. For ungauged potentials, U=V_child-V_parent. A common parent/child offset leaves U unchanged; shifting children alone by a adds a1_d^T to the record row and preserves balance only for a=0. These are distinct freedoms.

## Identity, two states and three states

For K=I, nonnegativity forces every branch off-diagonal entry to vanish. Exactly the supported identity members are

    C_0=diag(a_1,...,a_d), C_1=diag(1-a_1,...,1-a_d), 0<a_i<1.

They commute and every row is invariant; all record freedoms are those above. For d=2 and K!=I, rank(I-K)=1 because I-K is nonzero and has the mass row in its left kernel. Only constant rows remain, recovering the [two-state theorem](homogeneous_native_compensation.md).

For d=3, choose 0<a,c<1 and

    K=[[1,0,0],[0,0,1],[0,1,0]], D=diag(a,c,c),
    C_0=DK, C_1=(I-D)K.                                     (6)

K fixes coordinate one and swaps two and three; it is nonidentity, reducible, periodic and column-stochastic. D commutes with K and K^2=I, so C_0 C_1=D(I-D)=C_1 C_0. Branches are nonnegative, sum to K, and have strictly positive effects (a,c,c) and (1-a,1-c,1-c). The admissibility proof applies with the unchanged q.

Here H consists exactly of (x,y,y). The nonconstant row (1,0,0) is invariant and U=0 balances it. For a!=c, effects have rank two; for a=c, rank one. The latter has K!=I and a nonconstant feasible row, so the two-state rank-two-or-identity alternative is not necessary in higher dimension. Neither case compensates drift. The row (0,1,0) has nonzero drift (0,1,-1) and is infeasible by (4).

## Scope

The optional fixed finite classical family and full-simplex premise remain essential. The accepted [context-dependent active law](native_active_residual_v1.md) and earlier local results retain their scopes. Local conditional-mean balance establishes neither branchwise conservation nor a global marked-prefix potential across parents, shared records or merged histories. Restricted reachable domains require their own justification.

No quantum derivation, physical energy/mass/action/time/units, source coupling, preparation/readout, environmental closure, calibration, gravity, empirical, finite-sample, novelty or efficiency claim follows. No global scalar-energy necessity on arbitrary curved geometry is imposed. Option B, Status M and all scientific, review, custody, calibration and execution gates remain.
