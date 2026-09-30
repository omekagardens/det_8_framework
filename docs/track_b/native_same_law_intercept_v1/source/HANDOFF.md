# RI175 monotone intercept handoff

30 September 2026. Author submission for independent root review.

## New theorem and inherited premise

At the unchanged actual prefix, the normalized intercept

    I(x)=a(x)/Q(x)
        =-1+12lambda*[G_*x^2/q(x)+j_0*x/((1-x)*v)]

is strictly increasing on0<x<=R. Its derivative satisfies

    I'(x)>12lambda*j_0/[v(1-x)^2]>0.

This uses a historically certified fixed-prefix premise: RI122 finally
accepted a monic quadratic g with g(1)>0 and g'(1)<0. The accepted
RI127 sign review and RI145 definition identify q=k*g with k>0 at the
unchanged baseline. Hence q'<0 and2q-xq'>0. No coefficient or scientific
certificate was decoded or recalculated. The new monotonicity conclusion
is an analytic consequence of that accepted finite premise, not a fresh
axiom-only derivation of its sign.

The current root scope explicitly permits a narrow literal read of RI122's
final administrative decision; its inherited opaque routing remains intact.
No operational references were recursively followed. The earlier provisional
interpretations are not standalone final acceptance.

## Complete dependence and degenerate cases

The proof expands q_0,q_1,q_2 with the full canonical positive-part N_i
and all three signed products. The q_2 contribution cancels only from
2q-xq', not from q^2 or the underlying correlated data. Zero/positive
canonical branches and tied minima remain.

The general q_0=0 cases are checked without division by zero. Both yield
strictly increasing I through its positive j_0 term. In the double-zero
case q_0=q_1=0, the lower limit is -1+12lambda*G_*/q_2, not -1.
The actual accepted prefix has q_0>0, so its lower limit is -1.

## Endpoint consequence and remaining gap

The intercept condition over the full x interval is now exactly I(R)<=0.
If RI173's separately conditional v<=T_R slope regime also holds, then
full-domain W<=0 is equivalent to that single endpoint condition. Equality
I(R)=0 still gives W<0 at every allowed positive-y point.

Writing B=12lambda*j_0*R/(1-R), the endpoint condition is precisely

    v>B and q(R)>=12lambda*G_*R^2*v/(v-B).

Actual membership in the slope regime and this joint endpoint comparison
remain unresolved. Without the slope hypothesis, the other y endpoint
still requires its own test. No actual W,C2,C3,H30, full continuation,
QM, geometry, mass/gravity or physical conclusion is established.

## Review material and stopping boundary

- [INTERCEPT_REGION.md](INTERCEPT_REGION.md): derivative proof and zero-safe
  lower-end analysis.
- [CANONICAL_INTERCEPT.md](CANONICAL_INTERCEPT.md): full canonical dependence,
  historical same-law linkage and endpoint equivalences.
- [DEPENDENCY_NOTES.md](DEPENDENCY_NOTES.md):313 selected paths, narrow
  historical-read exception and preserved diagnostic phases.

HANDOFF.json binds exactly eight current files. AUTHOR_CHECKS.json retains
the actual preseal checks and the bounded reproduction recipe; the final
seal check is reported externally to avoid a hash cycle. Author-peer
verification is not independent acceptance. No scientific execution, new
agent, repository/index/Git mutation or predecessor edit occurred.

RET stays paused. Measurement and supervisor repair remain separately owned.
All P2/P3,Y=1/4,31/139/20/42,shared T1,other eight parents,five Di and
strict labeled-occurrence obligations remain. Root owns independent review,
successor selection and publication. Stop at this sealed bounded handoff.
