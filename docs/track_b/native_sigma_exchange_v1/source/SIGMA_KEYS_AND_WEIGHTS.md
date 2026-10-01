# Sigma component order and exact companion weights

1 October 2026, Honolulu. RI252 manual author derivation pending review.

The sigma coordinate lies between kappa and tau in the original
canonical component order. The fixed seed also makes all carrying
P_tau records equally weighted within a root sector, by an exact
history calculation. These facts settle the equality case of the
sigma-compensated exchange. They do not evaluate any canonical
allocation or prove the lower full-slot coefficient s is constant.

## Exhaust the sigma terminal and its canonical key

The two accepted sigma presentations are

    P_tau: r<a, r,o<x<y, selected {r,o,x,y};
    V5: r,o<x<y<z,       selected {r}.

Their common terminal is

    r,o<x<y<z, r<a,

with exactly two maximal vertices a,z. Deleting z gives P_tau;
deleting a gives V5. These deletions exhaust all parent presentations:
every component transport preserves the terminal. The two maximal
pasts intersect in {r}; its mark i is compulsory. The terminal
distinguishes r by its extra a branch, so its bit cannot be replaced
with the other minimum's bit.

The accepted eight-by-one sigma incidence connects all optional
(o,x,y) assignments in P_tau to the V5 singleton at fixed i.
Both newborn bits and every outside record remain. No mark is removed
before this transport is established.

Use the original five-carrier key: relation bits, then selected-ideal
mask, then selected-record mask, minimized over all nodes/permutations
in the component. RI248's accepted topological-minimum argument and
complete seven-order P_tau calculation give minimum relation code
8604 at order(r,o,x,y,a). In that order the sigma ideal has mask

    1+2+4+8=15.

Its record mask is i+2l+4m+8t. The accepted optional-mark incidence
permits l=m=t=0 within the same component, giving minimum record mask i.

V5 has only the two topological orders obtained by swapping its two
minima. In either, the final chain edge has source label 3 and target
label 4, contributing 2^19 by itself. Hence its relation code exceeds
8604. The topological-minimum lemma excludes a lower non-topological
permutation, so no V5 presentation can precede the stated P_tau node.

It follows, without an original vector-rank lookup, that

    root(sigma_i)=(8604,15,i).                            (K1)

Together with accepted RI248 roots,

    (8590,17,i) < (8604,15,i) < (8604,17,i),
      kappa_i       sigma_i       tau_i.                 (K2)

Only these three coordinates change in the exchange. Other coordinates
may occur between these keys, but remain fixed; they cannot become the
earliest change. A positive epsilon decreases kappa_i, so an exact
zero-primary-cost feasible step is lexicographically improving, whether
c>0 or c=0. No numerical value is inferred from any key or adjacency.

## Derive the actual history weights

Keep the prescribed singleton empty probability a_seed=2/3, the
two-antichain singleton probability g=1/10, and the accepted three-event
edge-plus-isolate probability q_E({r,o})=1/8. All newborn marks are fair.

For the rigid four-event parent

    N: r<a, r<x, o<x,

choose the linear extension(r,o,a,x). For any whole marking
(i,j,l,m), its exact marked-history probability is

    (1/2)(a_seed/2)(g/2)((1/8)/2)
        =a_seed g/128.

The first factor is the first newborn mark. The next birth is an
unrelated o; the third selects only r from the two-antichain; the fourth
selects {r,o} from E. None of these three chosen q values reads a
remaining mark. No record has been dropped.

RI248 established five linear extensions for N and equality of their
marked path products by the complete prefix diamonds. N has no
automorphism divisor: r has two strict descendants and o only one;
its two maxima have different past sizes. Therefore

    w_N(i,j,l,m)=5 a_seed g/128=1/384                    (H1)

for every full marking, derived directly from the admitted seed. This
is an exact special property of this law/shape, not a uniform-history
substitution or an acquired coefficient.

Use the accepted last-birth identity, with BOTH y bits retained,

    Pi_tau(i,j,l,m,t)=(7/5)(v_i/2)w_N(i,j,l,m)
                    =7 v_i/3840.                       (H2)

For a fixed i each of the four (l,m) rows carries four (j,t) assignments,
so its total weight is 7v_i/960, and the full sector weight is

    W_i=Pi_tau,i=7v_i/240>0.                             (H3)

Summing (H1) over all eight (j,l,m) assignments gives W_N,i=1/48;
RI248's Pi_tau,i=(7/5)v_i W_N,i then gives the same (H3).
As another same-law identity, its P-sector
formula gives Pi_P,i=3p_i/80 and hence
p_i Pi_tau,i=(7/9)v_i Pi_P,i, without a new source value.

Since s_(i,l,m) is independent of j,t, (H2) proves

    bar_s_i =
      [s_(i,0,0)+s_(i,0,1)+s_(i,1,0)+s_(i,1,1)]/4.      (H4)

All sixteen original carrying records contribute; the four-term
average is the result of the original weights, not an assumption.

## What the admitted diamonds do and do not say about s

Use the complete V row, where V is r,o<x<y. Abbreviate only existing
lower probabilities:

    e_V=q_V(empty),
    b_(i,l)=q_V({r,o};i,l),
    t_(i,l,m)=q_V({r,o,x};i,l,m).

These symbols do not introduce new law parameters or acquire values.
Strict record locality makes e_V record-independent. The accepted
join diamond gives q_V({r})=v_i/40 and q_V({o})=v_l/40.
Full normalization then gives exactly

    s_(i,l,m)=1-e_V-v_i/40-v_l/40-b_(i,l)-t_(i,l,m).      (D1)

The old top bit is absent; the lower join-top bit m is NOT silently
removed. Marked equivariance swaps the two minima, giving

    b_(i,l)=b_(l,i),
    t_(i,l,m)=t_(l,i,m),
    s_(i,l,m)=s_(l,i,m).                                 (D2)

This is not a flip of binary records and does not identify 00,01,11.

There is a concrete reason no additional m independence follows by
transport for the last proper slot. Append above {r,o,x} in V.
The terminal is r,o<x<y,z. Its only maxima are y,z, both with exactly
the same past {r,o,x}. Deleting either gives V again. The common
past retains ALL i,l,m; only the two minima can be swapped by an
automorphism. The top-of-join x cannot be exchanged with a minimum.
Thus complete component transport preserves m and the unordered pair
of minimum marks. It does not identify the m=0 and m=1 slot values.

The unique omitted maximum of V is y. The admitted deletion-potential
formula therefore gives potential q_J(J)=10/11 for this slot, where
J is the three-event join. That common potential does not make the
actual slot probabilities equal: they still multiply their existing,
unacquired original component scales. No scale is assigned a default
or read from a closed certificate.

Consequently neither the minimum-swap symmetry nor this diamond
proves a constant-s sector for the prescribed law. This is not a proof
that its actual s-values differ, nor a theorem that no other accepted
same-law argument could establish equality. A constant-s assertion
would require an additional proved identity for the complete expression
(D1), not just a common deletion potential or an assumed record flip.

For precision, define bar_t_i as the average of the four t_(i,l,m).
Combining (H4) and (D1) yields

    bar_s_i=1-e_V-v_i/40-(v_0+v_1)/80
                       -(b_(i,0)+b_(i,1))/2-bar_t_i.     (D3)

Thus the strict obstruction in SIGMA_EXCHANGE.md is equivalent, when
kappa_i and sigma_i are positive, to the existence of a tight row with

    v_l/40+b_(i,l)+t_(i,l,m)
       >(v_0+v_1)/80+(b_(i,0)+b_(i,1))/2+bar_t_i.        (D4)

The common empty and own-root terms cancel. No term involving the
other minimum or the lower join-top record is discarded. None of the
unknown lower probabilities, tight rows or canonical allocations is
evaluated here.

## Limits and retention

These are manual deductions from the exact admitted seed, complete
prefix diamonds, complete sigma incidence and original component
ordering. No new literal acquisition, rank reconstruction, probability
table, mathematical engine or execution is used.

The new strict obstruction and conditional constant-s product-zero
statement are necessary conditions at the unchanged canonical point.
They do not compare kappa0 with kappa1 or resolve C_b. All original
equations, recovery, offsets, strict endpoints, records/ideals/newborns
and source boundaries are retained as specified in SIGMA_EXCHANGE.md.
Stop for independent root review; no successor is selected.
