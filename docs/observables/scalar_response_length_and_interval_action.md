# Eight scalar-response readings on the four-birth orders

Under the stipulated retarded scalar law, eight exact population readings at distinct, calibrated positive settings determine the length parameter $\ell$ and the mean dimensionless interval action. The observer needs only the aggregate response at each setting. If the settings share an unknown scale $k$, the same design determines $\ell\sqrt{k}$ and the mean action. An absolute length then needs an independent standard.

## What is driven and read

In an order-compatible listing of the four vertices, define $L_j[x,y]=1$ when $y\prec x$ and the open interval from $y$ to $x$ has $j-1$ elements, and zero otherwise. The source vertex is the column and its later target the row. Set
$$
 N=2L_1-4L_2+2L_3,\qquad D=-I+N,\qquad h=2/\ell^2 .
$$
The conventional two-dimensional operator is $hD$. The factor two follows from the normalization in equation (1). The growth law supplies orders, while this choice of operator and its coefficients enters from outside the growth law. [Dowker and Glaser, arXiv:1305.2588v2, equation (1)](https://arxiv.org/pdf/1305.2588v2)

At each calibrated mass-term setting $u>0$ in inverse-length-squared units, apply the uniform source to each realized order after growth. Solve $(uI-hD)\phi=\mathbf1$ and sum all four components. The reading $Y(u)=g\,\mathbb E[\mathbf1^\mathsf T\phi]$ uses the same unknown positive gain $g$, the same $\ell>0$, the same preparation mixture, and exact blank subtraction at all eight settings. The observer receives no order or pair labels. A physical use would require implementing this uniform drive and sum. The earlier symmetric terminal field and the one-bit link probe use different observations. [Terminal field comparison](./finite_native_order_field_coupling.md) · [One-bit population readout](./one_bit_probe_for_mean_interval_action.md)

## Why the pole remains identifiable

The strictly lower triangular matrix $N$ satisfies $N^4=0$. On each order $O$, let $c_j(O)=\mathbf1^\mathsf T N_O^j\mathbf1$; write $m_j=\mathbb E[c_j(O)]$, so $m_0=4$. The inverse of $(u+h)I-hN_O$ is its finite geometric series. Summing the field and then averaging gives
$$
 Y(u)=g\sum_{j=0}^3\frac{h^j m_j}{(u+h)^{j+1}} .
$$
In particular, each $m_j$ comes from powers on the **same** order before averaging. Raising a mean matrix to a power would mix vertices and products from different realizations.

Every feasible response can be written $P(u)/(u+h)^4$ for $\deg P\le3$. Suppose two candidate responses agree at the eight distinct positive settings. Cross multiplication gives a polynomial of degree at most seven with eight zeros. The two rational functions therefore agree identically. Each has coefficient $4g>0$ on its simple-pole term in the expansion about $-h$. Higher negative powers can vanish; they cannot cancel this coefficient. Thus the reduced rational function has exactly one finite pole location, $-h$, whether its order is one, two, three or four as a matter of algebra. The support test below decides which orders of pole are realized by the allowed mixtures. No four-chain weight is required. For example, the supported order with just $a\prec b$ has $N^2=0$ yet its response has a pole at the same $-h$.

## Finite reconstruction and support check

1. For a trial $t>0$, interpolate the unique degree-at-most-three polynomial $P_t$ through the first four values $(u_i,\,Y_i(u_i+t)^4)$. Require $P_t(u_i)=Y_i(u_i+t)^4$ at each of the other four settings. These are polynomial equations of degree at most four in $t$, since the interpolation weights use the fixed $u_i$. An all-zero data vector is infeasible because the preceding uniqueness argument would force the rational function to vanish. For any other vector, two successful positive values of $t$ would give identical nonzero proper rational functions with different sole pole locations. Hence there is at most one positive common root, and feasible data have exactly one. Set $h=t$, giving $\ell=\sqrt{2/h}$.
2. Expand $P_h(u)=a_0(u+h)^3+a_1(u+h)^2+a_2(u+h)+a_3$, allowing zero coefficients. Require $a_0>0$. Then $g=a_0/4$ and $m_j=a_j/(g h^j)$ for $j=1,2,3$. The common gain is determined by the known count of four driven vertices.
3. For a full consistency decision, construct $N_i$ as above for each of the **15 structural rows** $(I_x,I_y)$ of the accepted E63 table. These ideals specify the full relation for that row. Form $v_i=(\mathbf1^\mathsf TN_i\mathbf1,\mathbf1^\mathsf TN_i^2\mathbf1,\mathbf1^\mathsf TN_i^3\mathbf1)$. Require a solution of the finite linear system $p_i\ge0,\ \sum_i p_i=1,\ \sum_i p_i v_i=(m_1,m_2,m_3)$. This is necessary by averaging. It is sufficient because the resulting mixture reproduces the entire response with the reconstructed $g,h$. The fair marked continuations within a row can retain their original conditional probabilities. Failure of any step rejects the readings for this model. The weights themselves need not be unique. [E63 structural rows and actions](./finite_interval_action_and_source_preparation.md)

## Which action enters the response

At vertex $x$, the local dimensionless contribution is
$$
 -(D\mathbf1)_x=1-2|L_1(x)|+4|L_2(x)|-2|L_3(x)|.
$$
Summing over targets counts each comparable endpoint pair once in its layer. Thus the individual action is $S(O)=-\mathbf1^\mathsf T D_O\mathbf1=4-c_1(O)$, and the population reading determines $\mathbb E[S]=4-m_1$. Equivalently, the reconstructed function expands at large $u$ as $Y(u)=4g/u-gh\,\mathbb E[S]/u^2+O(u^{-3})$. This is an algebraic check on the finite inverse; it uses no ninth reading.

The accepted one-bit comparison tabulates mean layer counts times 1320 as $(4066,1886,951)$ and $(4286,1441,966)$ for $P_0,P_1$. Applying the weights $(2,-4,2)$ and dividing by 1320 gives $m_1=2490/1320=83/44$ and $m_1=4740/1320=79/22$, respectively. The response formula returns $93/44,9/22$ for the mean actions, and a source-one minus source-zero contrast of $-75/44$. This checks the sign and normalization against the published finite law. All $D_O$ have four eigenvalues equal to $-1$; even the supported single-link and two-disjoint-link orders have different actions (2 and 0). Order information here enters through the driven and observed matrix elements of the inverse. The aggregate identifies the mean across preparations and does not recover the realized action on each trial. [Accepted source comparison](./finite_interval_action_and_source_preparation.md)

## What the external setting standard supplies

If the display supplies only $v$ with $u=kv$, write $H=h/k$ and $G=g/k$. Then $Y(kv)=G\sum_{j=0}^3 H^j m_j/(v+H)^{j+1}$. Applying the same inverse in $v$ gives exactly $H,G$ and the three moments. For each $\lambda>0$, the simultaneous change
$$
 (k,h,g,\ell)\longmapsto(\lambda k,\lambda h,\lambda g,\ell/\sqrt\lambda)
$$
preserves every displayed response with the same mixture. Conversely equality of the displayed curves fixes $h/k,g/k,m_1,m_2,m_3$ by the pole and coefficient proof. The overall scale freedom therefore accounts for the entire ambiguity in $k,h,g,\ell$ under the stated convention. In particular $\ell\sqrt{k}=\sqrt{2/H}$, $g/h=G/H$, and the dimensionless action survive.

The calibrated result transfers the units of the **external mass-term standard** to the model parameter $\ell$. Interpreting that parameter as an actual spacetime spacing would also require an independently validated field response and a relation between these finite orders and physical spacetime sampling. This study gives an exact conditional inverse with eight settings. Measurement precision, curvature and a native gravitational scale remain unestablished.
