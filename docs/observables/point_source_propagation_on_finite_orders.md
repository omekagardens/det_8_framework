# Point-source propagation on the supported four-vertex orders

**Decision.** Reject exact pairwise identification of the supplied scalar response with the strict massless two-dimensional causal matrix on this support. Even allowing arbitrary common weights for each interval size, one cannot make the inverse agree on both the four-chain and the diamond. With a nonzero diagonal contact, the additional information needed on this support is exactly whether the two events inside a two-intermediate interval are comparable.

## Comparison and supported witnesses

Use a fixed realized order and index each matrix by target row and source column. The strict causal matrix $C_{ts}$ equals one if $s\prec t$ and zero otherwise. Nomaan X, Dowker and Surya propose $K_0^{(2)}=C/2$ for the massless two-dimensional flat-sprinkling comparison. Here the benchmark is $\beta C$ on distinct endpoints, with one common nonzero gain $\beta$ across all source–target pairs and orders. On-site response is unobserved. Both the comparator and the impulse interface are supplied after growth. [Nomaan X, Dowker and Surya, §2.1, equations (11)–(15)](https://arxiv.org/pdf/1701.07212v5)

The native support contains both required orders. With prefix $a\prec b$, births $x,y$, and predecessor ideals written as in the four-vertex table:

- **Diamond:** $(I_x,I_y)=(a,abx)$. The open interval from $a$ to $y$ contains $b,x$, which are incomparable. The row has probabilities $172/1320$ and $392/1320$ under the two accepted preparations.
- **Four-chain:** $(I_x,I_y)=(ab,abx)$. Now $a\prec b\prec x\prec y$, and the same two intervening vertices are ordered. The row has probabilities $779/1320$ and $574/1320$.

These are the only two rows with a two-intermediate pair. All other comparable pairs have zero or one intermediate. All four fair newborn-mark continuations of each row use its same terminal order. The comparison is per order and per pair, without reweighting any preparation. [Four-vertex structural table](finite_interval_action_and_source_preparation.md)

## What the specified scalar law predicts

Write $D=-I+N$, $N=2L_1-4L_2+2L_3$, where $L_j$ indicates $j-1$ strict intermediates. At *actual* zero mass term the earlier response convention $(uI-hD)^{-1}$, $h=2/\ell^2>0$, gives $G=(-hD)^{-1}$. Since $N^4=0$, $hG=I+N+N^2+N^3$. This is a mathematical comparison at zero mass. The earlier scalar experiment used aggregate readings at positive settings. [Scalar-response convention](scalar_response_length_and_interval_action.md)

| Strict source–target pair | $N_{ts}$ | $(N^2)_{ts}$ | $(N^3)_{ts}$ | $hG_{ts}$ |
| --- | ---: | ---: | ---: | ---: |
| Link | 2 | 0 | 0 | 2 |
| One intermediate | −4 | 4 | 0 | 0 |
| Diamond endpoints | 2 | 8 | 0 | 10 |
| Four-chain endpoints | 2 | −16 | 8 | −6 |

The two diamond routes each contribute $2\cdot2$ to $N^2$. In the chain the two routes with one stop contribute $2(-4)+(-4)2$, while the route with two stops contributes $2^3$. Incomparable and backward pairs give zero by transitivity. For the inverse $D^{-1}$ itself the strict entries in the final column acquire a common minus sign.

**Distinguishing observation.** Apply the same unit impulse at $a$ in each witness and register only the downstream field at $y$ with a common gain. The benchmark predicts equal responses. The supplied scalar law predicts $10/h$ in the diamond and $-6/h$ in the chain, a diamond-minus-chain difference of $16/h$ before readout gain. Even within the four-chain one impulse at $a$ gives different responses at the link target $b$ and the one-intermediate target $x$. Adjusting a common length or normalization cannot remove either discrepancy.

## Why every cardinality-only choice fails

Allow $A=\alpha I+bL_1+cL_2+dL_3$ with $\alpha\ne0$. Its inverse is retarded, has zero entries outside the causal relation and diagonal $\delta=1/\alpha$. Consequently matching every strict entry **forces the complete response** to be $\delta I+\beta C$; the contact is common and unobserved. Write $q=\beta/\delta$. The unique operator for this complete response is
$$
 A_*=(\delta I+\beta C)^{-1}
     =\delta^{-1}(I-q C+q^2 C^2-q^3 C^3).
$$
This follows by finite multiplication since $C^4=0$. On a strict pair $(C^2)_{ts}$ counts individual intervening vertices, while $(C^3)_{ts}$ counts ordered pairs of intervening vertices forming a strict chain from source to target. Thus the entries forced on **the operator** are:

| Interval | $\delta (A_*)_{ts}$ |
| --- | ---: |
| Link | $-q$ |
| One intermediate | $-q+q^2$ |
| Two intermediates, incomparable | $-q+2q^2$ |
| Two intermediates, comparable | $-q+2q^2-q^3$ |

The chain-minus-diamond difference in the forced coefficient of the outer pair is $-q^3/\delta=-\beta^3/\delta^4\ne0$. One coefficient $d$ cannot serve both. Conversely, distinguishing the two kinds of two-intermediate interval and using this table, diagonal $1/\delta$, and zeros off the relation gives $A_*$ on **every** supported row. Thus one endpoint-specific comparability bit is necessary to resolve this size class and sufficient at four vertices. A population fraction of four-chains does not supply the bit for a particular registered pair.

If zero contact is imposed as part of the target, $\beta C$ is strictly triangular and singular. It remains a defined strict kernel, but has no ordinary two-sided matrix inverse. A nonzero contact permits the construction above and has no effect on the downstream comparison. The construction reads its coefficients **from** the target. It cannot establish that the growth law selected that target.

## Implication for the calibration

The accepted scalar calibration identifies a model length under a uniform drive and sum; the earlier terminal-field study uses a symmetric static balance. Neither observation measures the point-to-point retarded response used here. This finite counterexample concerns exact equality on the supported orders. A continuum approximation would require a specified continuum limit, ensemble and convergence test of its own. No physical source, detector, spacetime dimension or native length scale follows from this comparison. [Calibration decision](scalar_length_with_unknown_mass_offset.md) · [Terminal-field interface](finite_native_order_field_coupling.md)
