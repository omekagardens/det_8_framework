# Strict endpoint improvement and active coordinate obstruction

30 September 2026, Honolulu. Manual conditional reduction for independent review.

This note proves the exact endpoint implication needed by RI223. It does
not by itself decide whether the actual native ceiling is improvable.
The separate native note must supply an actual shared direction, an
actual active-coordinate obstruction, or the precise missing witness.

Keep the accepted RI220 child direction y0, whose only nonzero entries
are y0_Jj=z_j/e_j. Write

    c=a_empty=min_{z_j<0} e_j/(-z_j),
    I={j : z_j/e_j=-1/c}.                                  (E1)

The finite set I is nonempty, contains only negative-seed indices,
and excludes j=1 because z1=1. All ties in (E1) are retained.
Accepted RI220 gives 0<c<a_star<1/4. At amplitude c the only zero
child multipliers of y0 are exactly the J coordinates in I. All
other child multipliers and all seven-parent multipliers are positive.

Let H be the homogeneous solution space of the COMPLETE shared signed
system, with all original records and child identifications. Its
vectors delta are directions in the original thirty child variables.
Every affine solution is exactly y0+delta with delta in H.

## 1. A direction positive on every active coordinate is sufficient

Suppose a particular delta in H satisfies

    delta_Jj>0 for every j in I.                            (E2)

For each inactive child C put b_C=1+c*y0_C>0. Choose a symbolic
tau>0 small enough that

    tau < b_C/(2c*abs(delta_C))

for each inactive child with delta_C<0. There are finitely many
such strictly positive bounds; if there are none they impose no
restriction. A further bound tau<1 may be included. This proves
existence of tau without selecting a numerical value.

Set ybar=y0+tau*delta. All signed equations still hold because H
is homogeneous. At each active J coordinate,

    1+c*ybar_Jj=c*tau*delta_Jj>0.

At each inactive coordinate with negative delta the multiplier
exceeds b_C/2, and at the other inactive coordinates it is at least
b_C. Thus every child is strictly positive at the exact amplitude c.
Every seven-parent multiplier is already greater than 3/4 there.

This also gives a strictly larger admissible amplitude. Let
bbar_C=1+c*ybar_C>0. Choose eta>0 below (a_star-c)/2 and below

    bbar_C/(2*abs(ybar_C))

for every child with ybar_C<0. The finitely many bounds are positive.
For c<=a<c+eta each child remains positive. Parent multipliers remain
positive because a<a_star<1/4 and |z_j|<=1. The complete H30 iff
therefore supplies positive extensions at c and on a nonempty interval
above c, using this SAME fixed ybar.

No endpoint zero has been accepted, no record constraint discarded,
and no numerical amplitude, solver or direction has been selected by
this conditional proof.

## 2. The active positivity condition is also necessary

Suppose a full strictly positive solution y exists at some a>=c.
Both y and y0 solve the same affine equations, so delta=y-y0 is in H.
For each active j,

    delta_Jj = y_Jj+1/c > 1/c-1/a >= 0.                    (E3)

The first inequality is strict. Thus delta_Jj>0 for every active j,
including when a=c. Consequently the following are equivalent:

- A homogeneous shared direction satisfying (E2) exists.
- A full strictly positive H30 solution exists at a=c.
- A full strictly positive H30 solution exists at some a>c.
- A full solution exists throughout some interval immediately above c.

These are equivalences about the SAME complete shared system. Knowing
that T2/T3 local intervals are nonempty is not a substitute for (E2).

## 3. An exact nonnegative active-coordinate obstruction

Suppose actual weights mu_j, j in I, satisfy

    mu_j>=0,    sum_I mu_j>0,
    sum_I mu_j*delta_Jj=0 for every delta in H.              (E4)

For every affine solution y=y0+delta,

    sum_I mu_j*y_Jj=-(sum_I mu_j)/c.                        (E5)

If y were strictly positive at a>=c, its active child inequalities
would instead give

    sum_I mu_j*y_Jj > -(sum_I mu_j)/a
                    >= -(sum_I mu_j)/c,

a contradiction. Hence no full positive solution exists at or above c.
The accepted solutions below c then make the full feasible set exactly

    F=(0,c).                                               (E6)

Weights at tied active indices may be zero; at least one must be positive.
Normalization sum mu=1 is optional, not a change of the criterion.
The word active is load-bearing: arbitrary inactive coordinates cannot
be inserted into (E5), because their y0 values are not -1/c.

## 4. Why these are exhaustive without an automatic solver

Let V be the image of H on its I coordinates. It is a finite-dimensional
linear subspace of R^I. The alternative is either V contains a vector
strictly positive in every coordinate or its orthogonal complement
contains a nonzero coordinatewise nonnegative vector.

For a self-contained existence proof, consider the probability simplex
of vectors mu>=0 with sum mu=1 and minimize the squared norm of the
orthogonal projection P_V mu. A minimum exists by compactness and
continuity. This is a mathematical existence argument, not an executed
optimization or a proposed numerical procedure. This auxiliary Euclidean
inner product is a proof device, not a quantum state space or a supplied
physical geometry.

If the minimum is zero, the minimizing mu satisfies (E4). Otherwise
let v=P_V mu at a minimizer. For each coordinate unit vector e_j,
the one-sided variation toward e_j inside the simplex gives

    v_j >= inner_product(v,mu)=norm(v)^2>0.

Here orthogonal projection gives inner_product(v,mu)=norm(v)^2.
Thus v is strictly positive on all active coordinates and has a
preimage delta in H, proving (E2). The two outcomes cannot both hold,
since the inner product of their positive/nonnegative vectors would
be strictly positive rather than zero.

This establishes an alternative, NOT the native branch. No minimizer,
projection, matrix rank, numerical coefficient or actual witness was
computed, inferred from existence, or silently supplied.

## 5. The full feasible amplitude set has one open upper boundary

If one fixed finite direction y is strictly positive at a>0, then it
is strictly positive at every smaller positive amplitude: each
multiplier is a convex combination of its value at a and one.
All signed equations are unchanged. The same argument applies to the
parent multipliers.

Strict positivity of finitely many child and parent multipliers is
also open in a for that fixed y. Thus the full feasible amplitude
set is downward closed and open. RI220 gives a nonempty initial
interval and the necessary upper bound a_star, so

    F=(0,a_full),    c<=a_full<=a_star.                     (E7)

No maximal-amplitude solution at its endpoint is asserted. If (E4)
holds, a_full=c; if (E2) holds, a_full>c. The actual alternative is
the bounded native question, not a reason to restart affine consistency.

[NATIVE_REDUCTION.md](NATIVE_REDUCTION.md) keeps the exact shared
constraints and identifies what the admitted native facts establish.
No new gate, execution contract, empirical or all-size claim follows.
