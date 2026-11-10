# Registering the scalar mass zero with three interval-probe rates

**Decision.** Retain all three tagged link rates when joining the two observations. Together with the eight scalar readings they determine the hidden offset $d$, the model length $\ell$, and the common gain $g$ on every feasible mixture of the 15 supported four-vertex orders. The mean interval action alone suffices when it differs from four. At mean action four it can discard exactly the information that distinguishes two lengths.

## What each observation supplies

Both arms sample independent draws from the same distribution over the 15 supported four-vertex structural rows. In the link arm the addressed pair is uniform, the two other vertices are omitted independently with probability $t$, and every zero is retained. Let $n_j$ count comparable endpoint pairs with $j$ strict intermediates and write $x=\mathbb E[n_0]$, $y=\mathbb E[n_1]$, $z=\mathbb E[n_2]$. The three recorded rates at $t=0,1/2,1$ determine these three numbers by interpolation of $6p(t)=x+yt+zt^2$. Thus the mean action is $4-2x+4y-2z$. The observer receives population records in each arm and need not match individual orders across trials. [Accepted link readout](one_bit_probe_for_mean_interval_action.md)

In the scalar arm the **increments** $u>0$ have calibrated inverse-length-squared units. The actual mass term is $u+d$ with one unknown common $d\ge0$. Electronic blank subtraction is a separate operation. Let $N=2L_1-4L_2+2L_3$ be the strictly retarded layer matrix on each realized order, $D=-I+N$, $h=2/\ell^2>0$, and $a=d+h$. Here $L_j$ joins endpoints with $j-1$ strict intermediates. Define $m_j=\mathbb E[\mathbf1^\mathsf{T}N^j\mathbf1]$, with the power taken within each order. Since $N^4=0$, the uniform-source, uniform-readout response is
$$
Y(u)=g\left[\frac4{u+a}+\frac{b_1}{(u+a)^2}
                 +\frac{b_2}{(u+a)^3}+\frac{b_3}{(u+a)^4}\right],
\qquad b_j=h^j m_j .
$$
Eight exact readings at the declared distinct positive increments determine $a,g,b_1,b_2,b_3$. Indeed two such rational functions agree identically if they match there: after cross multiplication the difference numerator has degree at most seven. The simple-pole coefficient $4g>0$ preserves the pole location $-a$ even when higher terms vanish. The residue fixes $g$, then the other coefficients give the $b_j$. The pole alone locates the sum $d+h$. [Accepted scalar response](scalar_response_length_and_interval_action.md)

## How the layer counts separate $h$ from $d$

Let $T$ be the probability of a four-element total chain in the common mixture. The moment identities on this support are
$$
 m_1=2x-4y+2z=4-\mathbb E[S],\qquad
 m_2=4y+8z-24T,\qquad
 m_3=8T .
$$

For $m_2$, count two-step paths between a fixed ordered pair of endpoints. One intermediate gives a pair of links with product $2\cdot2=4$. Two incomparable intermediates give a diamond with two such paths, contributing $8$. Two comparable intermediates give a four-chain: the outer endpoints have two paths with products $2(-4)$ and $(-4)2$, totaling $-16$. Relative to counting all two-intermediate pairs at $8$, this subtracts $24$ per four-chain. Interior one-intermediate pairs of that chain are already counted in $4n_1$. For $m_3$, three steps use all four vertices in a single chain of links, with product $2^3$. Consequently $T$ is the four-chain fraction and $z-T$ the diamond fraction. The argument uses only the stipulated four-vertex supports. [Four-vertex order table](finite_interval_action_and_source_preparation.md)

- **When $\mathbb E[S]\ne4$**, $h=b_1/m_1$. Thus even a record compressed to the mean action recovers $h$ on this branch.
- **When $\mathbb E[S]=4$**, $b_1=0$. The retained rates still give $K=4y+8z=m_2+3m_3$. Every supported order has a link, so $x\ge1$. From $m_1=0$ follows $y=(x+z)/2>0$, hence $K>0$. The value $h$ is the unique positive solution on feasible data of
$$
 K h^2=b_2+3b_3/h .
$$
If $b_3>0$, the left side increases from zero to infinity and the right side decreases from infinity to $b_2$, even when $b_2<0$. If $b_3=0$, then $T=0$ and $b_2=K h^2>0$, giving $h=\sqrt{b_2/K}$.

On both branches require $0<h\le a$. Then $d=a-h$ and $\ell=\sqrt{2/h}$. Equality $h=a$ is the allowed zero-offset endpoint. All three $m_j=b_j/h^j$ are determined, including $T=m_3/8$. The tagged native rates can therefore register the zero without an independently known gain, known preparation label, or additional mass setting.

## A collision when only the action is transmitted

Use the following two preparations from the published four-vertex order table. In each world its own two arms sample the same preparation; the marks within each structural row may keep their fair conditional law.

| World | Structural rows $(I_x,I_y)$ and probabilities | $(x,y,z)$ | $(m_1,m_2,m_3)$ |
| --- | --- | --- | --- |
| A | $(\varnothing,ab)$, probability one | $(2,1,0)$ | $(0,4,0)$ |
| B | $(\varnothing,abx)$ and $(ab,ab)$, probability one half each | $(3,3/2,0)$ | $(0,6,0)$ |

Both transmit exactly $\mathbb E[S]=4$. Choose any positive $H$ in the calibrated inverse-length-squared units and the same positive gain. Set
$$
 h_A=\sqrt{3/2}\,H,\quad h_B=H,\qquad
 d_A=2H-h_A,\quad d_B=2H-h_B .
$$
Both offsets are nonnegative, both pole locations are $-2H$, and $h_A^2 m_{2,A}=h_B^2 m_{2,B}=6H^2$. Both worlds therefore give
$$
 Y(u)=g\left[\frac4{u+2H}+\frac{6H^2}{(u+2H)^3}\right]
$$
at **all eight common settings**, indeed at every positive $u$. Their lengths $\sqrt{2/h_A}$ and $\sqrt{2/h_B}$ differ. The full records immediately distinguish them, since $p_A(0)=1/3$ and $p_B(0)=1/2$. This witnesses loss of identifiability for the mean-action compression; it does not require changing the setting scale.

## Finite common-mixture test

For proposed exact records, interpolate the three click rates and require rates in $[0,1]$. In the scalar arm interpolate a polynomial of degree at most three through $Y_i(u_i+a)^4$ at the first four abscissas and require agreement at the remaining four, solving for $a>0$ as in the scalar-response derivation linked above. Reject all-zero data, absence of a solution $a>0$ with pole at $-a$, or a nonpositive simple-pole coefficient. Expand in powers of $u+a$ to obtain the scalar coefficients. Apply the appropriate recovery above, requiring $b_1=0$ on the exceptional branch, $b_3\ge0$, and $0<h\le a$.

Finally form one vector per published structural row, $(n_0,n_1,n_2,\mathbf1_{\rm four\text{-}chain})$. Require **one** nonnegative set of 15 weights summing to one whose weighted vector is $(x,y,z,b_3/(8h^3))$. Also require the resulting three moment identities above to reproduce **all** $b_j=h^jm_j$. These are finite necessary and sufficient conditions: any physical mixture gives these equalities, and any such weights, gain, length and offset reproduce both observation laws. The weights describe an admissible preparation, without asserting unique order probabilities. For a compressed record the same forward feasibility conditions can be used with only the reported action equation in place of the three layer means, leaving $h$ and the weights existential; the example supplies two solutions.

The dimensional information still comes from the calibrated increments. The calculation identifies a length parameter of the supplied operator under common gain, drive, offset and ensemble registration. It supplies no physical zero-setting observation, calibrated apparatus, or independent evidence for a spacetime spacing or gravity law.
