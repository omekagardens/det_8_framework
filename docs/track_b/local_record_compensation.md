# Local record compensation for a finite two-state instrument

**Independently reviewed local mathematical result.** This conditional classification concerns one supplied instrument at one parent. It supplies no new native growth law or physical conservation law.

## Inputs and target

Fix finitely many observed labels b=1,...,m, m>=1, and supplied nonnegative real 2-by-2 matrices B_b. Their sum K is column-stochastic: 1^T K=1^T, with 1^T=(1,1). Use the full input interval Delta={rho=(x,1-x)^T:0<=x<=1}. The actual effects are e_b=1^T B_b; E is the m-by-2 matrix with these rows. Effects and K come from the same instrument.

Fix a real row ell=(ell_0,ell_1) with ell_0!=ell_1. Child record values V_b are finite real constants depending only on b; the parent record value is zero. They may be signed, with no additional coefficient bound. For every rho in Delta the required conditional-mean balance is

    sum_b V_b e_b rho + ell K rho = ell rho.                 (1)

This is not pathwise balance. Actual outcome probabilities p_b=e_b rho are nonnegative and sum to one. For p_b>0 the child is B_b rho/p_b. For p_b=0 nonnegativity implies B_b rho=0, so the unnormalized contribution vanishes; no normalized child is invented or outcome discarded.

## Criterion and complete solution

Put d=ell(I-K). Then (1) holds exactly when

    V^T E=d.                                               (2)

Indeed the target is (V^T E-d)rho=0; the two basis inputs in Delta force both row components to vanish. The converse is immediate. Consequently feasibility is equivalent to d belonging to rowspan(E), and every solution is V_*+ker(E^T) for any particular solution V_*. The kernel is precisely the record vectors with zero probability-weighted mean for every input. Since sum_b e_b=(1,1), rank(E) is 1 or 2.

**Rank two.** Every prescribed ell is feasible. Write e_b=(u_b,v_b), choose independent rows i,j and D=u_i v_j-u_j v_i!=0. Choose arbitrary finite V_b outside {i,j}, and set

    (r_0,r_1)=d-sum_(b outside {i,j}) V_b e_b,
    V_i=(r_0 v_j-u_j r_1)/D,
    V_j=(u_i r_1-r_0 v_i)/D.                                (3)

Substitution gives the required remaining row; independence makes these two coefficients unique. Thus (3) gives every solution, with m-2 free coefficients.

**Rank one.** Each effect is e_b=q_b(1,1), where q_b>=0 and sum_b q_b=1. Actual probabilities are q_b, not necessarily equal across labels. Parameterize

    K=[[1-alpha,beta],[alpha,1-beta]], alpha,beta in [0,1].

Writing s=ell_0-ell_1!=0 gives d=(s alpha,-s beta). Membership in span{(1,1)} requires alpha=-beta, hence alpha=beta=0 by nonnegativity. Therefore feasibility requires and is ensured by K=I. Every solution then satisfies sum_b q_b V_b=0: choose any q_i>0, choose all other coefficients freely, and set V_i=-sum_(b!=i)q_b V_b/q_i. There are m-1 free coefficients.

Thus, for any prescribed nonconstant ell, feasibility is equivalent to **rank(E)=2 or K=I**. The same criterion decides existence of any nonconstant ell: in feasible cases every nonconstant row works, otherwise none does. Rank two is equivalent to some effect having unequal coordinates; this concerns complete probability functions, not perfect inference from one outcome.

## Degeneracies and gauges

Constant residual rows always give d=0 and exactly ker(E^T), a trivial case excluded from nonconstant success. Modulo span{(1,1)}, all nonzero residual-row classes are feasible under the criterion, otherwise none are.

For m=1, feasibility requires K=I and V_1=0. Duplicate or proportional effects are covered by the ranks. A zero effect forces B_b=0 and leaves V_b free. Boundary-only zero probabilities require no division and give no extra freedom because (1) holds on all Delta. No branch is removed.

Adding c1^T to ell leaves d unchanged. A fixed nonzero rescaling ell'=a ell+c1^T transports solutions to aV+ker(E^T); a=0 loses nonconstancy. These relations do not replace a prescribed numeric row. With parent value g, subtracting g from every child value sets the parent to zero. Shifting children alone changes (1) unless the shift is zero; a nonzero constant record vector is not zero-mean freedom. Consistent outcome-label permutations, or joint residual-coordinate relabeling of states, maps, effects and row, preserve the equation.

## Native mapping boundary

The unchanged [first-birth obstruction](native_additive_balance_obstruction.md) has effects (1/2,1/2) for both marks and K=[[3/4,1/4],[1/4,3/4]]. It has rank one and K!=I, retaining its obstruction. This is an inherited check, not a repaired law.

Local feasibility establishes neither globally admissible DET growth nor a consistent potential across parents, shared records, merged histories or diamonds. Restricted reachable domains need their own input-domain check. Nearly dependent effects may require large signed values: no stability, cost, statistical accuracy or efficiency guarantee follows.

Physical energy/mass, units, time/symmetry, source coupling, environment closure, preparation/readout and calibration remain external to the [native mapping programme](../coordination/NATIVE_MASS_MAPPING.md). No geometry, gravity, GWOSC, empirical, novelty or universal conservation claim follows, and no global scalar-energy necessity on arbitrary curved geometry is imposed. Option B, Status M and all scientific, review, custody, calibration and execution gates remain.
