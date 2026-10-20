# Singular-law kernel and target-width theorem

20 October 2026. Conditional finite mathematics for the declared
parent-five scaling family.

**Result.** At an exceptional law, loss of the normalization \(z_1=1\)
is an invariant loss of the target-width-changing direction in this
eleven-class harmonic space. The full kernel still has dimension one.
The formal compatible singular alternative would have dimension two and
allow width change, but the published coefficient identities and bounds
exclude it throughout this family. Whether the actual family encounters
an exceptional law still depends on one unselected coefficient comparison.

## 1. Object, complete equations and premises

Let \(C_k,A_k\) denote a chain and antichain; \(\oplus,\sqcup\) are ordinal
sum and disjoint union. Put \(I=C_3\) and \(T_j=I\oplus Q_j\), where
the ordered cap list is
\[
\begin{split}
(Q_1,\ldots,Q_{11})={}&(A_4,\ C_2\sqcup A_2,\
 (A_2\oplus A_1)\sqcup A_1,\ (A_1\oplus A_2)\sqcup A_1,\
 C_2\sqcup C_2,\ N,\ C_3\sqcup A_1,\\
 &A_2\oplus A_2,\ A_1\oplus A_3,\
 A_1\oplus(C_2\sqcup A_1),\ C_2\oplus A_2).
\end{split}
\]
Here \(N\) has exactly the strict relations \(0<2,0<3,1<3\).
A real vector \(z\in\mathbb R^{11}\) defines \(Z(T_j)=z_j\), zero on
every other seven-order class. The multiplier is \(h_7=1+\epsilon Z\),
with \(h_n=1\) for \(n\le6\). All marks and fair newborn outcomes remain;
the payload maps are the admitted unnormalized scalar maps \(q\mathfrak D/2\).

The family preserves the original prefix through parent four, multiplies
parent-five proper probabilities by \(0<\lambda\le1\), and replaces each
full probability \(q\) there by \(1-\lambda+\lambda q\). Parent six is
rebuilt with its positive common scale \(\rho_\lambda\), not the old scale.

The admitted complete incoming parents are \(I\oplus R_p\), with
\[
(R_1,\ldots,R_5)=(A_3,\ C_2\sqcup A_1,\ A_2\oplus A_1,\
 A_1\oplus A_2,\ C_3).
\]
All 320 marked rows reduce exactly to the two root sectors of each row
below. This is an inherited all-record identity, not a sampled reduction.

Use two-component columns indexed by root bit \(i=0,1\):
\[
\begin{gathered}
 a=41/44,\quad
 (b_0,b_1)=(8077/8800,40303/44000),\quad
 (c_0,c_1)=(81/1100,3231/44000),\\
 G_i=\theta b_i^2/a,\quad H_i=\theta c_i,\quad
 D_i=\theta b_i,\quad U_i=\theta^3b_i^3/a^2,\\
 J_i=1-\lambda+\lambda j_i,\qquad
 F_i=1-\lambda+\lambda f_i,\qquad f_i=1-\theta-\mu_i.
\end{gathered}
\]
The admitted bounds include \(0<\theta<10^{-10}\),
\(0\le\mu_i<1/26\), and \(j_1>j_0>0\). The full homogeneous system
\(M_\lambda z=0\), with **no normalization imposed on \(z_1\)**, is
\[
\begin{aligned}
 \lambda^3Uz_1+3\lambda^2\theta Hz_2+3Jz_3&=0,\\
 \lambda^2\theta Gz_2+\lambda^2\theta Hz_4+\lambda Hz_5+Jz_6+Fz_7&=0,\\
 \lambda Gz_3+2\lambda Hz_6+Jz_8&=0,\\
 \lambda^2\theta Dz_4+\lambda^2\theta Hz_9+2Fz_{10}&=0,\\
 \lambda Dz_7+\lambda Hz_{10}+Fz_{11}&=0. \tag{1}
\end{aligned}
\]
Each line is a two-component equation. The common positive
\(\rho_\lambda\) cancels from harmonicity. All other parent rows have
zero correction. Thus the rank of this ten-row matrix is also the rank
of the complete marked eleven-column system.

Write \([A,B]=A_0B_1-A_1B_0\),
\(K=[H,J]>0\), \(\Delta=[D,H]<0\), and \(\chi=[H,F]\).
These nonzero first two pivots follow from the admitted coefficients.
The additional held-row identity needed below is
\[
 j_i=1-\theta\tau_i,\qquad
 \tau_i=Q_{2,i}+2c_i,\qquad
 Q_{2,i}=\sum_S B_S(i)^2/A_S.
\]
There are four stem slots, \(A_S>0\), \(\sum_S A_S=1\), and
\(0<B_S(i)/A_S<1\). Hence \(0<Q_{2,i}<1\); since \(0<c_i<1/2\),
\[
                     0<\tau_i<2.                       \tag{2}
\]
These are fixed-law premises; the original coefficients are not free choices.

## 2. Full kernel at \(\chi=0\): both algebraic cases

Set \(t=z_1\). The first and third rows of (1), using \(K>0\), force
\[
\begin{gathered}
 z_2=t a_2,\quad z_3=t a_3,\quad z_6=t a_6,\quad z_8=t a_8,\\
 a_2=-\frac{\lambda[U,J]}{3\theta K},\qquad
 a_3=-\frac{\lambda^3[H,U]}{3K},\\
 a_6=-\frac{a_3[G,J]}{2K},\qquad
 a_8=-\frac{\lambda a_3[H,G]}K.
\end{gathered}
\]
Define \(X=\lambda D,\ Y=\lambda H\) and
\[
 Q=-\lambda^2\theta G a_2-Ja_6,\qquad C=[Y,Q].
\]
The remaining three rows are exactly
\[
\begin{aligned}
 Y(\lambda\theta z_4+z_5)+Fz_7&=tQ,\\
 Xz_7+Yz_{10}+Fz_{11}&=0,\\
 \lambda\theta(Xz_4+Yz_9)+2Fz_{10}&=0.       \tag{3}
\end{aligned}
\]

At \(\chi=0\), positivity gives \(F=\kappa Y\) with
\(\kappa=F_0/Y_0>0\), while \([X,Y]=\lambda^2\Delta\ne0\).
The second equation of (3) forces \(z_7=0,\ z_{10}=-\kappa z_{11}\).
The third forces \(z_4=0,\ z_9=2\kappa^2z_{11}/(\lambda\theta)\).
The first is now \(Yz_5=tQ\), equivalent to
\[
             tC=0,\qquad z_5=tQ_0/Y_0.                  \tag{4}
\]
These implications are reversible, so no homogeneous directions are lost.

Define
\[
 w=(0,0,0,0,0,0,0,0,\ 2\kappa^2/(\lambda\theta),-\kappa,1).
\]
If \(C=0\), also define
\[
 v=(1,a_2,a_3,0,Q_0/Y_0,a_6,0,a_8,0,0,0).
\]
The complete alternatives are therefore
\[
\begin{array}{c|c|c|c}
\text{singular compatibility}&\ker M_\lambda&\dim\ker M_\lambda&
 \operatorname{rank}M_\lambda\\ \hline
 C\ne0&\operatorname{span}\{w\}&1&10\\
 C=0&\operatorname{span}\{v,w\}&2&9 .
\end{array}                                             \tag{5}
\]
Independence in the second row follows from \(v_1=1,w_1=0,w_{11}=1\).

## 3. Target-width functional and its image

Use the complete one-birth row at \(P_1=I\oplus A_3\), with root sector
\(i\). Its old width is three. Among supported children only \(T_1\)
has width four; \(T_2,T_3\) have width three. All unsupported children
have \(Z=0\), not zero probability. Subtracting three times the first
harmonic row from the width correction gives
\[
 \mathcal W_i(z)
 :=\sum_{S\text{ ideal}}q_{B_\lambda}(P_1,r,S)
                  Z(P_1+S)\operatorname{width}(P_1+S)
 =\rho_\lambda\lambda^3U_i z_1.                         \tag{6}
\]
The actual perturbed-minus-baseline expected width is
\(\epsilon\mathcal W_i(z)\). Both newborn bits are summed, not conditioned on.

Since the factor in (6) is strictly positive, (5) gives
\[
 \mathcal W_i(\ker M_\lambda)=
 \begin{cases}\{0\},&C\ne0,\\ \mathbb R,&C=0.\end{cases}   \tag{7}
\]
For both root sectors jointly the compatible image is the line
\(\{s(U_0,U_1):s\in\mathbb R\}\), and otherwise it is zero.
These are images of a signed linear functional, not claims of arbitrarily
large admissible probability differences.

Thus failure of \(z_1=1\) cannot be repaired by a different normalization
to recover this width contrast: every nonzero-width vector would have
\(z_1\ne0\) and could be rescaled to \(z_1=1\).
The width-blind vector \(w\) nevertheless remains nonzero.
For any finite kernel vector, choosing
\[
 0<\epsilon\le\min\{1/4,\ 1/[2(1+\max_j|z_j|)]\}
\]
makes every multiplier strictly positive. Complete harmonicity and the
admitted shared-terminal telescoping then give an admissible prefix
through seven births. Width blindness is not disappearance of all
admissible perturbations.

## 4. The declared bounds exclude compatible singularity

Eliminating the front coordinates explicitly yields
\[
 C=\frac{\lambda^4}{6K}\,\Omega,\qquad
 \Omega=2[H,G][U,J]-[H,U][G,J].                         \tag{8}
\]
Indeed
\(Q=\lambda^3G[U,J]/(3K)
-\lambda^3J[H,U][G,J]/(6K^2)\); taking its bracket with
\(Y=\lambda H\) proves (8).

Let
\[
 r=b_1/b_0=40303/40385,\qquad s=c_1/c_0=359/360,\qquad
 x=J_1/J_0.
\]
The definitions give \(G_1/G_0=r^2,\ U_1/U_0=r^3,\ H_1/H_0=s\), so
\[
 \Omega=H_0G_0U_0J_0\,\Phi(x),\qquad
 \Phi(x)=2(r^2-s)(x-r^3)-(r^3-s)(x-r^2).              \tag{9}
\]
By (2), \(J_i=1-\lambda\theta\tau_i\). Hence
\(J_0>1-2\theta>1/2\) and
\[
               0<x-1<4\theta.                         \tag{10}
\]
No numerical value of either \(j_i\) has been selected.

Here is a rational sign bound with ample margin. Put
\(e=1-r=82/40385\), so \(1/500<e<1/400\), and put \(d=1-s=1/360\).
Direct polynomial expansion gives
\[
\begin{split}
 \Phi(1)&=eB,\\
 B&=-6e+9e^2-5e^3+e^4+d(4-5e+2e^2)\\
  &<-6/500+1/16000+1/90
    =-119/144000<-1/1250.
\end{split}
\]
For the bound, use \(e^4<e^2\), discard the negative cubic,
and use \(-5e+2e^2<0\). Therefore \(\Phi(1)<-1/625000\).
The coefficient of \(x\) in \(\Phi\) is \(2r^2-r^3-s<2\).
Together with (10),
\[
 \Phi(x)<-1/625000+8\theta
         <-1/625000+8\cdot10^{-10}<0.                  \tag{11}
\]
All factors outside \(\Phi\) in (8)–(9) are positive. Consequently
\[
                  C<0\quad\text{for every }0<\lambda\le1.
\]
In particular the formal \(C=0\) row of (5) is excluded for this
declared family. At any exceptional law, the exact kernel is
\(\operatorname{span}\{w\}\), the system has rank ten, and both target-width
functionals vanish on the entire kernel.

## 5. Family-wide conclusion and the precise remaining premise

Off \(\chi=0\), the published nonzero-pivot elimination gives a unique
\(z_1=1\) solution; its homogeneous kernel has dimension one and rank ten.
For completeness, set \(k=\lambda\theta z_4+z_5\). Solve successively
\(Yk+Fz_7=tQ\), then \(Yz_{10}+Fz_{11}=-Xz_7\), then
\(Xz_4+Yz_9=-2Fz_{10}/(\lambda\theta)\), and recover
\(z_5=k-\lambda\theta z_4\). The respective determinants are
\(\lambda\chi,\lambda\chi,\lambda^2\Delta\), all nonzero.
Together with the four front coordinates, this gives exactly one kernel
vector for each \(t\), including zero when \(t=0\).

Its width-functional image is \(\mathbb R\). Combined with the theorem
above, **the rank is ten throughout the family**, even at a possible
exception: the change there is in the width image, not a rank drop.

The location question can be stated without selecting any original value.
Using \(f_i=1-\theta-\mu_i\) and \(c_1=(359/360)c_0\), define
\[
 \Xi=\theta+360\mu_1-359\mu_0.
\]
Then exactly
\[
                 \chi(\lambda)=\frac{\theta c_0}{360}(1-\lambda\Xi).
                                                               \tag{12}
\]
The admitted original seed at \(\lambda=1\) has \(z_7\ne0\);
the second equation of (3) would force \(z_7=0\) if \(\chi(1)=0\).
Thus \(\Xi\ne1\). If \(\Xi>1\), there is exactly one exceptional
law \(\lambda_*=1/\Xi\in(0,1)\), with the width-blind kernel above.
If \(\Xi<1\), there is none in the declared interval.

**Remaining premise:** which side of \(1\) the actual fixed coefficient
combination \(\Xi\) occupies. This note does not decide that comparison
or assert that both alternatives are realized by admissible original
instances. No such comparison is needed for the singular kernel/width
classification, and no coefficient audit is opened.

The result concerns this eleven-class, record-blind, finite-prefix harmonic
space and this specified one-birth width functional. It is not a statement
about all order observables, all supports, all growth laws, or DET itself.
There is no h8/30/33/38 transfer, full-QM, geometric or physical validation
claim.

The separate [positive-contrast limit theorem](POSITIVE_CONTRAST_LIMIT.md)
addresses approach to a possible exceptional law. Conditional on \(\Xi>1\),
all strictly positive harmonic perturbations on this same support obey a
local uniform quadratic upper bound on target-width contrast against the
baseline at the same parameter. Arbitrary normalization and amplitude choices
cannot evade it. No continuity or uniform positive lower bound of
\(\rho_\lambda\) is needed. Sharpness, a matching lower rate and convergence
of raw widths or entire baseline laws are not established.

## Public sources and scope

The [law-family supplement](LAW_FAMILY_SUPPLEMENT.md) supplies the
fixed-seed obstruction and moving-seed construction. The
[theorem package](THEOREM_PACKAGE.md) states the admitted finite law,
original support and held-row coefficient identities. The
[law-dependence note](LAW_DEPENDENCE.md) distinguishes optional law
choices from coordinate changes and proves the finite-prefix scaling
premise. The complete eleven-column system and argument needed for
this theorem are printed above.

The fixed-law premises remain conditional. The unresolved occurrence
comparison here is distinct from the later thirty-class canonical
coefficient branch. Neither is settled by publication; no later-layer
or fixed-support exclusion is transferred to a changed law. See the
[publication note](PUBLICATION_NOTE.md) for the evidence boundary.
