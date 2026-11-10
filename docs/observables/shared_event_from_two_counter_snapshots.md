# Recognizing a shared event from two counter snapshots and one registered bit

Two snapshots of descendant counters can agree even when two seven-event histories give different interval actions. The missing information can be supplied by one yes-or-no reading tied to the fourth birth. Under the following growth and readout assumptions, this reading and the snapshots identify every chain or diamond junction and reject every ineligible history.

## What the observer receives

Start from the two-event chain $a<b$ with both marks zero. At each of the next five births, every downward-closed precursor set in the actual parent has positive conditional probability, and the newborn mark is conditionally fair. Choosing a precursor set makes the newcomer a descendant of precisely the events in that set. Its own counter starts at zero, and the selected precursors each increment their counters modulo five. The observer reads the unlabelled counter multisets $H_4,H_7$ after births four and seven, and the terminal bit $B=\mathbf1\{c_7(r)=3\}$ for the registered fourth birth $r$. The marks and individual precursor choices are hidden. Extending the register to seven births and retaining the identity of $r$ are supplied readout assumptions. [Four-event incidence register](finite_incidence_register.md)

The target is a chain or diamond on the first four events, with $r$ at its top, and a chain or diamond on $r$ and the following three, with $r$ at its bottom. A four-event diamond has one bottom, two incomparable middle events and one top. Write C for chain and D for diamond, with the earlier shape first.

## How to classify the join

Induction on births gives $c_n(v)=|\{w:v<w\}|\bmod 5$ for the history at birth $n$. At the fourth birth no counter has wrapped. The multiset $H_C=\{0,1,2,3\}$ forces a chain, and $H_D=\{0,1,1,3\}$ forces a diamond. In both, the count of three identifies a common bottom. In the diamond the two count-one events must be incomparable and below the sole count-zero event. The newborn $r$ is maximal and thus the unique top in either shape. Reject any other $H_4$.

Only three births follow $r$, so its own count cannot wrap. Consequently $B=1$ exactly when all three later events descend from $r$. Reject if $B=0$. When $B=1$, every earlier event gains three descendants by transitivity. Add three modulo five to each cell of $H_4$. This gives the old contribution $K_C=\{0,1,3,4\}$ or $K_D=\{1,3,4,4\}$. Subtract that multiset from $H_7$, preserving multiplicities.

The three remaining counters all count at most two descendants. The remainder $\{0,1,2\}$ gives a future chain. The remainder $\{0,1,1\}$ gives two incomparable newcomers below a common top, completing a future diamond with $r$ at its bottom. Every other remainder is ineligible.

| Earlier and later shapes | $H_4$ | $H_7$ when $B=1$ | Joined action |
| --- | --- | --- | ---: |
| CC | $H_C$ | $\{0,0,1,1,2,3,4\}$ | 7 |
| CD | $H_C$ | $\{0,0,1,1,1,3,4\}$ | 1 |
| DC | $H_D$ | $\{0,1,1,2,3,4,4\}$ | 1 |
| DD | $H_D$ | $\{0,1,1,1,3,4,4\}$ | 3 |

## Which histories the snapshots confuse

Call the third birth $x$, the three newcomers $p,q,s$, and the first four events $P$. To realize each table row, attach $x$ to $\{a,b\}$ for a chain past or $\{a\}$ for a diamond past, then attach $r$ to $\{a,b,x\}$. Attach $p$ to $P$, attach $q$ to $P\cup\{p\}$ for a chain future or to $P$ for a diamond future, and attach $s$ to $P\cup\{p,q\}$. Every choice is downward closed in its actual parent. The chain rule therefore gives positive support to each complete history, including the choice of all-zero marks.

Keep the chain past $a<b<x<r$. Compare the eligible CD history above with one in which $p,q,s$ instead choose $\{a\},\{a,b,x\},\{a,b,x,p,q\}$. These are again possible precursor sets, and now $r$ has no descendants. In birth order the true terminal counts are respectively
$$
(6,5,4,3,1,1,0),\qquad (6,4,3,0,1,1,0).
$$
Both give $H_4=H_C$ and $H_7=\{0,0,1,1,1,3,4\}$. In the eligible history the terminal three belongs to $r$. In the other it belongs to $x$. Even an extra indication that *some* counter equals three leaves this pair indistinguishable.

## What the action contrast measures

Use the prescribed dimensionless action $S(X)=|X|-2n_0+4n_1-2n_2$, where $n_k$ counts comparable endpoint pairs with exactly $k$ events strictly between them. The ineligible history above has $(n_0,n_1,n_2)=(7,4,3)$ and action 3. Its snapshot twin has action 1. For the four eligible classes the shared-event formula gives the table values and hence
$$
S_{CC}+S_{DD}-S_{CD}-S_{DC}=7+3-1-1=8.
$$
Separate additive contributions from the earlier and later shapes would cancel in this contrast. The result compares values of the specified action on four supported classes. Their numerical probabilities, the response of a physical seven-event register and a calibration to gravitational action remain open. [Interval action at a shared event](interval_action_at_a_shared_event.md)
