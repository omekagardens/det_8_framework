# RI178 upper boundary and single endpoint handoff

30 September 2026. Sealed author submission for independent root review.

## New results

Both complete reference factors 1-U20/d and 1-U30/d strictly increase.
Their exact quotient numerators exceed127/128 and67/24 respectively on
the assigned interval. The full canonical correction and every occurrence
remain; positivity alone was not used as a monotonicity argument.

Combining those derivatives with RI175's accepted q>0,q'<0,q(0)>0
proves that J(x)=W(x,1/d(x))/r strictly increases on0<x<=R, without
assuming v<=T_R. Every product and varying-denominator derivative is
retained. Both I and J tend to-1 at the excluded lower x limit.

The affine-y interpolation first gives the requested two-endpoint iff:
full curved-domain W<=0 exactly when I(R)<=0 and J(R)<=0.
An additional same-domain bound makes the second condition redundant:

    I(x)<=0 implies J(x)<-1/(2d(x))<=-1/12<0.

Indeed I=-1+u+t with u,t>0; I<=0 gives u+t<=1. The positive reference
factors then bound J by (E_add-min(U20,U30))/d, while the accepted
same-law inequalities give E_add<99/128<1 and min(U20,U30)>3/2.
No y-slope sign is needed or inferred.

Consequently the strengthened exact result is

    W<=0 on the whole curved domain iff I(R)<=0,

without the RI173 slope-regime premise. When it holds, W is strictly
negative at every allowed positive-y point, including when I(R)=0.
In that equality case the supremum is0 but is not attained because y=0
is excluded. If I(R)>0, formal sufficiently small positive y at x=R
violates full-domain nonpositivity; this does not locate actual rho,s.

## Remaining comparison

The sole endpoint condition is still undecided at the actual prefix:

    v>B_cap and q(R)>=12lambda*G_*R^2*v/(v-B_cap),
    B_cap=12lambda*j_0*R/(1-R).

Equality in the second comparison is retained. The strict v>B_cap branch
is required before division. No actual W/C2/C3, capacity, H30 feasibility,
full continuation or physical claim is settled merely by this reduction.

## Proofs and checks

- [REFERENCE_COMPLEMENTS.md](REFERENCE_COMPLEMENTS.md): full canonical
  coefficient bounds and both quotient derivative proofs.
- [UPPER_BOUNDARY.md](UPPER_BOUNDARY.md): exact J derivative, two-endpoint
  reduction, stronger domination lemma and all equality/limit cases.
- [DEPENDENCY_NOTES.md](DEPENDENCY_NOTES.md):325 selected source identities,
  unchanged historical scope and preserved diagnostics.

The inherited finite-sign premise is used through accepted RI175, not
recomputed. The author-peer check identified one normalization wording
ambiguity in the supremum statement; it was corrected to distinguish W/r
from W before sealing. Independent root acceptance remains pending.

HANDOFF.json binds exactly eight files. AUTHOR_CHECKS.json records the actual
preseal checks and inline administrative reproduction recipe. Final8 is
reported externally after the seal, not preclaimed in a self-hashed file.
No scientific decoding or execution, new agent, repository/index/Git change
or predecessor edit occurred. RET stays paused; measurement and RI176 remain
separate. Preserve P2/P3,Y=1/4,31/139/20/42,shared T1,other eight
parents,five Di,strict endpoints and every labeled occurrence. Root owns
independent review, publication and successor selection. Stop at this handoff.
