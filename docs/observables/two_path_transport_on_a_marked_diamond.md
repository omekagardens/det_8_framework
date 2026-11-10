# A four-preparation test of endpoint-mark transport

With the path through middle mark 0 taken first, the shared two-mark link rule produces exactly the signed tables
$$
(H_{ij})_{i,j=0,1}=
\begin{pmatrix}m+k&m\\m&m-k\end{pmatrix},
\qquad m,k\in\mathbb R .
$$
Rows give the source mark and columns the final mark. Two independent calibrated readings determine the table. Measuring all four tests two independent equalities. The original growth law supplies the marked diamonds on which to perform this comparison. A separate operation supplies each link's real log-transfer.

## The four preparations exist under the native law

Use the accepted prefix $a\prec b$, with marks $(i,0)$ and consistent descendant counters $(1,0)$. Select the realized branch $I_x=\{a\},\ I_y=\{a,b,x\}$. Its four cover links are $a\to b,\ b\to y,\ a\to x,\ x\to y$; $b,x$ are incomparable. Under the two registered prefix preparations $P_0,P_1$ the structural probabilities are $172/1320$ and $392/1320$. On this branch each specified ordered pair of newborn marks has one quarter of its structural probability. In particular the selected pair $(\mathrm{mark}(x),\mathrm{mark}(y))=(1,j)$ has probability

| Source $i$ | $j=0$ | $j=1$ |
|---|---:|---:|
| 0 | $172/5280$ | $172/5280$ |
| 1 | $392/5280$ | $392/5280$ |

Each entry is conditional on its prepared prefix. The terminal mark $j$ is a registered fair outcome on the selected branch. Collecting each case requires recognizing the full diamond and its marks. These probabilities establish availability; they do not multiply the individual path readings. The two paths lie inside **one** realized order. Neither path is an alternative chronological order for the births.

## Image, realization and coefficient ambiguity

Supply four real numbers $t_{kl}$, with the source mark first and target mark second, and reuse them on every future cover link in every preparation. Suppose path readings add their link tags. Both paths can also carry a common endpoint convention, such as a receiver log gain minus a source log gain. It cancels in the registered difference
$$
H_{ij}=(t_{i0}+t_{0j})-(t_{i1}+t_{1j}).
$$
Write $(A,B,C,D)=(t_{00},t_{01},t_{10},t_{11})$. Direct substitution gives
$$
H_{00}=2A-B-C,\quad H_{01}=H_{10}=A-D,\quad H_{11}=B+C-2D .
$$
Thus $m=A-D$ and $k=A+D-B-C$. The necessary conditions are
$$
H_{01}=H_{10},\qquad H_{00}+H_{11}=2H_{01}.
$$
They suffice. For any compatible table take $m=H_{01}$, $k=(H_{00}-H_{11})/2$ and choose
$$
t_{00}=m,\qquad t_{11}=0,\qquad t_{01}=t_{10}=(m-k)/2 .
$$
Substitution returns every entry, including either sign or zero. Equality of the mixed-mark readings does not require symmetric microscopic link coefficients.

Two coefficient assignments yield the same entire table precisely when their differences satisfy $\Delta A=\Delta D=\alpha$ and $\Delta B+\Delta C=2\alpha$. In matrix form the full ambiguity is
$$
\Delta t=
\begin{pmatrix}\alpha&\alpha+\beta\\\alpha-\beta&\alpha\end{pmatrix},
\qquad \alpha,\beta\in\mathbb R .
$$
The common per-link shift adds $2\alpha$ to both two-link paths. The remaining shift has the form $\phi_l-\phi_k$, with $\phi_1-\phi_0=\beta$; it sums to the same endpoint difference along either path. These account for the whole kernel *within the four shared coefficients*. A separate device convention attached to actual vertices also cancels if it telescopes between the same two tips. Raw individual-link or absolute path readings would be a different observation.

## What the signed readings can test

The pair $H_{00},H_{11}$ determines $m=(H_{00}+H_{11})/2$ and $k=(H_{00}-H_{11})/2$, and hence predicts both mixed-mark readings. One mixed reading and either diagonal also suffice. A single entry leaves a parameter free; the two off-diagonal entries measure the same parameter. Holding out the mixed preparations gives two checks: the readings must agree with each other and with the predicted midpoint. For example the exact table $\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)$ passes the exchange equality but fails the midpoint test. No choice of the four shared coefficients or their invisible shifts fits it. Passing both checks establishes compatibility and identifies $m,k$; it does not uniquely determine the four link tags.

The sign requires an accessible rule for ordering the two arms. Here their distinct immutable marks provide that rule once the instrument can read them. If the middle marks coincide, both paths have the identical ordered mark sequence $i,h,j$, so this link law forces $H=0$, even with external arm labels. If the arms are intrinsically identical and unnamed, their exchange fixes the accessible diamond while reversing a putative signed difference. A nonzero sign cannot be assigned from those records. If separate path values are available only as an unordered pair, one can retain their absolute difference. A choice of drawing orientation or birth index supplies no intrinsic sign.

## What an optical comparison still requires

The accepted continuum calculation uses four directed null links $P\to A,P\to B,A\to F,B\to F$, with $r_{XY}$ the received/emitted frequency ratio on the same photon. With the stipulated two-dimensional geometry and the same local velocity and gain $g_X>0$ for the two tags at each corner, it gives
$$
\mathcal I=\int R\,d\mathcal A=2\log Q-4\log\Gamma,\qquad
Q=\frac{r_{PA}r_{PB}}{r_{AF}r_{BF}},\quad
\Gamma=\frac{g_A g_B}{g_P g_F}.
$$
A shared gain gives $\Gamma=1$. Otherwise this one relative gain product must be established for the curvature inference from the four ratios.

Even identifying $(a,b,x,y)$ with $(P,A,B,F)$ does not equate the two observables. Put $\ell_{XY}=\log r_{XY}$. In the native path ordering $(PA,AF,PB,BF)$, an ordinary difference of the two optical path sums has coefficients $(+,+,-,-)$, while $\log Q$ has coefficients $(+,-,+,-)$. In fact the ordinary path difference of these raw optical log ratios cancels the conformal endpoint factors and gains along each route upon subtraction. Using the optical report's corner rapidities it equals $2(\xi_P-\xi_A-\xi_B+\xi_F)$, which can be nonzero even in a flat diamond. Directly substituting optical log ratios for native link tags would therefore miss the target.

A transfer comparison requires an independently specified and tested map from the native marks, cover links and directed arm readings to the physical rays and calibrated frequency comparisons. It must register the tips and arms, the direction and sign for each transfer, a shared log scale and its normalization, and the relative gain correction. It must justify why the mark-only coefficients are shared over the four matched preparations. Calibrated independent optical observations could then test a prescribed equality or proportionality. Fitting the conversion to those same readings would leave the equality assumed. Both quantities are dimensionless; a dimensional curvature would additionally require a physical length or area and the relevant geometric model.

The separate three-birth phase construction conjugates chronological birth kernels by one source-dependent change of angle coordinates. Transforming states and effects together preserves probabilities, and holding a detector convention fixed can give a contrast. Those kernels act between growth states. They supply neither the four transfers between vertices of this realized order nor the registration to null rays. The accepted point-source calculation likewise supplies a scalar source and response, which does not resolve two signed arm sums. The present proof establishes a finite falsification test conditional on mark access, additive transfer and calibrated readout. It leaves the native birth probabilities, their dynamics and the physical interpretation of the tags as supplied in their respective models.

[Supported four-event diamond](point_source_propagation_on_finite_orders.md) · [Source preparations](finite_interval_action_and_source_preparation.md) · [Chronological phase model](native_phase_action_interface.md) · [Four-link optical curvature](integrated_curvature_from_four_frequency_ratios.md)
