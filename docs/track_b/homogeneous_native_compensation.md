# Homogeneous native branches and local compensation

This independently reviewed conditional theorem classifies one optional homogeneous two-state family through four births. Native admissibility requires commuting branch matrices. Every admissible member whose total residual map is nonidentity has input-independent bit effects and cannot compensate any nonconstant residual row locally. Identity members have the complete local freedoms stated below.

## Fixed structural law and changed carrier family

Use exactly the binary-marked orders and structural probabilities q(P,r,S) in [Part A of the fixed four-birth prefix](native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix). Each birth appends a maximal vertex with strict past the chosen downward ideal S; existing order and marks are immutable. All actual ideals, including empty/full and distinct labeled occurrences, remain. Parent sizes are 0–3; there is no fifth-birth equation. Full slots are complete normalization complements.

The inherited structural premises are q>0, sum_S q=1, equivariance, proper-slot access to the whole unmarked parent and only selected marks, and the transported identity

    q(P,r,S) q(P_x,r_x,T) = q(P,r,T) q(P_y,r_y,S).             (1)

Here S,T are any ideals, including S=T; x and y have arbitrary newborn bits and are incomparable. Second precursors are the transported old subsets, excluding the other newborn. The fixed prefix has q_empty=1 and singleton empty-slot probability 2/3 for either mark.

Choose fixed finite nonnegative real 2-by-2 matrices C_0,C_1, independent of parent, ideal, birth number, old marks and history. Let K=C_0+C_1 be column-stochastic and e_b=1^T C_b have two strictly positive components, with 1^T=(1,1). The common residual cone is R_+^2, vertex relabeling acts trivially, and each local test includes every rho=(x,1-x)^T, 0<=x<=1. Define

    B_(S,b)=q(P,r,S) C_b.                                    (2)

This replaces the original fair passive carrier prescription; no extra factor 1/2 is present. Matrix entries may vanish. Homogeneity is optional, not a universal native principle.

## Admissibility exactly equals commutation

Summing all ideal/bit branches in (2) gives K, hence total probability one. Each branch mass q_S e_b rho is strictly positive, and its normalized child is C_b rho/(e_b rho). Nonnegativity and strict effects retain every continuation, including boundary inputs. Fixed C adds no old-data dependence, so full-map locality and equivariance follow from q, including full-to-proper precursor transport.

For any required diamond based at size at most two, the two complete maps are

    q(P_x,r_x,T) q(P,r,S) C_c C_b,
    q(P_y,r_y,S) q(P,r,T) C_b C_c.                            (3)

Equation (1) equates their positive scalar factors. Necessity is witnessed by the actual empty-base diamond with S=T=empty and unequal newborn bits: its maps are (2/3)C_1 C_0 and (2/3)C_0 C_1. Equality on the full carrier therefore forces C_0 C_1=C_1 C_0.

Conversely, commutation equates (3) for unequal bits; equal bits already agree. The structural identity covers every inherited marking, ideal pair and full-to-proper slot. After transport the marked endpoint is identical, so corresponding suffix maps are identical, even when a suffix precursor contains either newborn. Left multiplication by a suffix and right multiplication by a preceding history preserve equality.

Any two natural birth orders of one final marked order are connected by adjacent incomparable swaps: move the next desired vertex leftward; crossed vertices must be incomparable since both orders respect the order. Repeat. Through four births every such pair has base size at most two. Thus the proved diamonds and suffixes give complete finite history consistency. Together these arguments prove full admissibility exactly when the matrices commute, within the declared premises.

## Nonidentity maps exclude local compensation

At a parent with n actual ideals, the complete effect matrix E_P has 2n rows eta_(S,b)=q_S e_b, and its total map is K. Positive q gives rowspan(E_P)=span{e_0,e_1}, without dropping any ideal record.

Commutation implies C_b K=K C_b and hence

    e_b K=1^T C_b K=1^T K C_b=e_b.

Write K=[[1-alpha,beta],[alpha,1-beta]], alpha,beta in [0,1]. For e_b=(u_b,v_b), invariance says alpha(v_b-u_b)=0 and beta(u_b-v_b)=0. If K!=I, at least one coefficient is nonzero, so e_b=p_b(1,1), with p_b>0 and p_0+p_1=1. This includes reducible, periodic, singular and other permitted boundary matrices; no inverse, irreducibility or mixing is used.

Allow arbitrary finite real, source-independent child values U_(S,b), parent value zero, and a prescribed fixed row ell with unequal components. The full-input conditional-mean target is

    sum_(S,b) U_(S,b) eta_(S,b) rho + ell K rho = ell rho.    (4)

The two basis inputs make (4) equivalent to the row equation E_P^T U=(ell(I-K))^T, as in the [local compensation theorem](local_record_compensation.md). Put v_b=sum_S q_S U_(S,b). The record row v_0 e_0+v_1 e_1 is constant across coordinates. For s=ell_0-ell_1!=0 the required drift is (s alpha,-s beta); it is constant only if alpha=-beta, forcing both zero. Thus no nonidentity admissible member permits any nonconstant row at any parent, even with ideal-dependent values.

Nonidentity admissible members exist: for any nonnegative column-stochastic K and 0<p<1, C_0=pK and C_1=(1-p)K commute and have positive effects. The obstruction is not vacuous.

## Identity members and every local freedom

If K=I, nonnegative off-diagonal entries must vanish separately. The complete family is

    C_0=diag(a,d), C_1=diag(1-a,1-d), 0<a,d<1.               (5)

Conversely every such pair is admissible. Every prescribed nonconstant ell has zero drift, so U=0 works. All solutions are ker(E_P^T), equivalently

    v_0(a,d)+v_1(1-a,1-d)=0.                                (6)

If a!=d, determinant a-d!=0 gives v_0=v_1=0. If a=d=p, the sole constraint is p v_0+(1-p)v_1=0. Each bit's q-weighted averaging map is onto and has n-1 free ideal coefficients: choose all but one value and solve using a positive q. Therefore all solution spaces have dimensions 2n-2 and 2n-1 respectively. At empty, n=1 gives zero and one. All ideal values remain distinct.

Constant residual rows are excluded from nonconstant success. Adding a constant mass row leaves drift unchanged; fixed nonzero scaling relates prescribed-row questions without replacing their inputs. A common parent-and-child offset is a gauge. Shifting children alone at fixed parent zero adds that constant, unlike zero-mean record freedom.

## Scope

Optional same-C factorization and retained native identities jointly force this result. The accepted [context-dependent active law](native_active_residual_v1.md) lies outside that restriction and remains intact, as do the [fixed-law obstruction](native_additive_balance_obstruction.md) and local classification. Separate-parent solutions do not construct a global marked-prefix potential across shared records, merged histories or the horizon. Full-input conclusions cannot silently replace a restricted reachable-domain question.

No universal native-energy obstruction, physical energy/mass/action/time/units, source coupling, preparation/readout, environmental closure, calibration, gravity, empirical, finite-sample, novelty or efficiency claim follows. No global scalar-energy necessity on arbitrary curved geometry is imposed. Option B, Status M and all scientific, review, custody, calibration and execution gates remain.
