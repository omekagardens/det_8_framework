# A regular observable family through the exceptional law

20 October 2026. Independently reviewed conditional finite-prefix theorem.

**Result.** Conditional on \(\Xi>1\), the fixed eleven-class kernel has a
regular section with \(v_{11}=1\) through \(\lambda_*=\Xi^{-1}\). Its
recovery never divides by \(\chi\). One fixed nonzero scalar amplitude
makes every multiplier positive on a whole neighborhood of \(\lambda_*\),
and the complete \(P_4\) width contrast is positive in both root sectors
throughout that neighborhood. A uniform lower bound is proved for the
contrast **divided by \(\rho_\lambda\)**, not for the absolute contrast.
No regularity or uniform lower bound of \(\rho_\lambda\) is assumed.

## 1. Fixed object and inherited premises

Let \(I=C_3\), with \(C_k,A_k\) a chain and antichain and
\(\oplus,\sqcup\) ordinal sum and disjoint union. Set \(T_j=I\oplus Q_j\),
where the fixed ordered cap list is
\[
\begin{split}
(Q_1,\ldots,Q_{11})={}&(A_4,\ C_2\sqcup A_2,\
 (A_2\oplus A_1)\sqcup A_1,\ (A_1\oplus A_2)\sqcup A_1,\
 C_2\sqcup C_2,\ N,\ C_3\sqcup A_1,\\
 &A_2\oplus A_2,\ A_1\oplus A_3,\
 A_1\oplus(C_2\sqcup A_1),\ C_2\oplus A_2).
\end{split}
\]
The strict relations in \(N\) are exactly \(0<2,0<3,1<3\).
The five incoming parents are \(P_p=I\oplus R_p\), where
\[
(R_1,\ldots,R_5)=(A_3,C_2\sqcup A_1,A_2\oplus A_1,A_1\oplus A_2,C_3).
\]
The inherited complete 320 marked rows reduce exactly to two root sectors
per displayed parent; all other parent corrections vanish. No sampled
row reduction or new incoming catalogue is asserted.

Keep the original coefficients fixed and unselected:
\[
\begin{gathered}
 a=41/44,\quad (b_0,b_1)=(8077/8800,40303/44000),\\
 (c_0,c_1)=(81/1100,3231/44000),\quad
 0<\theta<10^{-10},\quad 0\le\mu_i<1/26,\\
 G_i=\theta b_i^2/a,\quad H_i=\theta c_i,\quad D_i=\theta b_i,\quad
 U_i=\theta^3 b_i^3/a^2,\\
 J_i(\lambda)=1-\lambda+\lambda j_i,\qquad
 F_i(\lambda)=1-\lambda(\theta+\mu_i),\qquad 0<\lambda\le1.
\end{gathered}
\]
Here \(i=0,1\) is the original root record. The fixed original \(j_i\)
obey the held-law premises of the [singular-law theorem](SINGULAR_LAW_WIDTH.md), including \(j_1>j_0>0\) and
\(j_i=1-\theta\tau_i\), \(0<\tau_i<2\).
For two-sector columns define
\[
 [A,B]=A_0B_1-A_1B_0,\qquad K=[H,J]>0,\qquad
 \Delta=[D,H]<0,\qquad \chi=[H,F].
\]
The complete harmonic equations are
\[
\begin{aligned}
 \lambda^3Uv_1+3\lambda^2\theta Hv_2+3Jv_3&=0,\\
 \lambda^2\theta Gv_2+\lambda^2\theta Hv_4+\lambda Hv_5+Jv_6+Fv_7&=0,\\
 \lambda Gv_3+2\lambda Hv_6+Jv_8&=0,\\
 \lambda^2\theta Dv_4+\lambda^2\theta Hv_9+2Fv_{10}&=0,\\
 \lambda Dv_7+\lambda Hv_{10}+Fv_{11}&=0.                 \tag{1}
\end{aligned}
\]
Every line is a two-component equation. In this note \(v\) is a kernel
section, **not the actual multiplier deviation**; that deviation will
be \(\eta_*v\).

At each \(\lambda\), the admitted compatible baseline \(B_\lambda\)
has positive common parent-six scale \(\rho_\lambda\), which cancels
from (1). Its finite-prefix positivity, record locality and shared-terminal
construction are inherited premises. Both fair newborn bits and the
complete unnormalized scalar-passive payload maps \(q\mathfrak D/2\)
remain in the object. No continuity of this baseline family is assumed.

## 2. Explicit regular section and verification of all rows

Define
\[
\begin{gathered}
 a_2=-\frac{\lambda[U,J]}{3\theta K},\qquad
 a_3=-\frac{\lambda^3[H,U]}{3K},\qquad
 a_6=-\frac{a_3[G,J]}{2K},\qquad
 a_8=-\frac{\lambda a_3[H,G]}K,\\
 Y=\lambda H,\qquad Q=-\lambda^2\theta G a_2-Ja_6,\\
 C=[Y,Q]=\frac{\lambda^4}{6K}
       \bigl(2[H,G][U,J]-[H,U][G,J]\bigr).
\end{gathered}                                                    \tag{2}
\]
The [singular-law theorem](SINGULAR_LAW_WIDTH.md) proves \(C(\lambda)<0\) throughout \(0<\lambda\le1\) from the
fixed coefficient identities and held-law bounds. This is a load-bearing
inherited sign theorem, not an additional coefficient selection.

The following recovery gives all eleven coordinates:
\[
\begin{gathered}
 t=\frac{\chi^2}{\Delta C},\qquad v_1=t,\qquad v_{11}=1,\\
 (v_2,v_3,v_6,v_8)=t(a_2,a_3,a_6,a_8),\\
 v_7=\frac{\chi}{\lambda\Delta},\qquad
 v_{10}=-\frac{[D,F]}{\lambda\Delta},\\
 v_4=\frac{2\chi v_{10}}{\lambda^2\theta\Delta},\qquad
 v_9=-\frac{2[D,F]v_{10}}{\lambda^2\theta\Delta},\\
 v_5=\frac{tQ_0-F_0v_7}{\lambda H_0}-\lambda\theta v_4.
\end{gathered}                                                    \tag{3}
\]
The only nonconstant denominators in (2)–(3) are products of
\(a,\lambda,\theta,H_0,K,\Delta,C\). They are all nonzero on the stated
interval. In particular there is **no division by \(\chi\)**, \(t\),
\(v_{10}\), or \([D,F]\). All coordinates are rational and continuous on
\(0<\lambda\le1\); boundedness as \(\lambda\downarrow0\) is not claimed.

The first and third rows of (1) follow directly from the four front
coefficients in (2), using \(K\ne0\). For the fifth row, the two equations
\[
 Dv_7+Hv_{10}=-F/\lambda
\]
have determinant \(\Delta\), and Cramer's rule gives (3). The fourth row
likewise solves
\[
 Dv_4+Hv_9=-2Fv_{10}/(\lambda^2\theta)
\]
with the same determinant. Finally the second row becomes
\[
 Y(\lambda\theta v_4+v_5)=tQ-Fv_7.
\]
Its right-hand side has zero bracket with \(Y\):
\[
 [Y,tQ-Fv_7]=tC-\lambda\chi v_7
            =\chi^2/\Delta-\chi^2/\Delta=0.              \tag{4}
\]
Since \(Y_0=\lambda H_0>0\), the definition of \(v_5\) supplies the
root-zero component and the vanishing bracket supplies the root-one
component. This checks every row, including at \(\chi=0\).

The section also spans the entire kernel. Indeed, any kernel vector
with coordinate 11 zero has coordinates 7 and 10 zero by the fifth
row and \(\Delta\ne0\). Front elimination followed by the bracket of
the second row with \(Y\) gives \(Cv_1=0\). Thus coordinate 1 and all
four front coordinates vanish. The fourth row then forces coordinates
4 and 9 to vanish, and the second forces coordinate 5 to vanish.
Subtracting a vector's coordinate 11 times (3) therefore leaves zero.
This establishes a one-dimensional kernel with the displayed global
normalization; it does not restore a nonzero coordinate 1 at the exception.

## 3. Exceptional specialization and one fixed positive amplitude

Condition, without selecting actual coefficients, on
\[
 \Xi=\theta+360\mu_1-359\mu_0>1,\qquad
 \lambda_*=\Xi^{-1}\in(0,1).
\]
The accepted exact identity is
\[
 \chi(\lambda)=\frac{\theta c_0}{360}(1-\lambda\Xi).
\]
At the exception set
\[
 \kappa_*=\frac{F_0(\lambda_*)}{\lambda_*H_0}>0,\qquad
 F(\lambda_*)=\kappa_*\lambda_*H.
\]
In fact \(\kappa_*>1\), since \(F_0>1-\theta-1/26>1/2\) and
\(\lambda_*H_0<1/2\). Substituting
\([D,F(\lambda_*)]=\kappa_*\lambda_*\Delta\) in (3) gives exactly
\[
 v(\lambda_*)=w=
 (0,0,0,0,0,0,0,0,\ 2\kappa_*^2/(\lambda_*\theta),-\kappa_*,1). \tag{5}
\]
This is the accepted [exceptional-law width direction](SINGULAR_OBSERVABLE_WITNESS.md) with its coordinate 11 equal to one.

Choose once and for all
\[
                         \eta_*=\frac1{2\kappa_*}>0.    \tag{6}
\]
At \(\lambda_*\) the multipliers \(1+\eta_*w_j\) are one on the
first eight coordinates and, on coordinates 9–11, are respectively
\[
 1+\frac{\kappa_*}{\lambda_*\theta},\qquad
 \frac12,\qquad 1+\frac1{2\kappa_*}.
\]
Their minimum is \(1/2\). By continuity of the finite eleven coordinates,
there is \(\varepsilon>0\) such that
\[
 \mathcal I_*=[\lambda_*-\varepsilon,\lambda_*+\varepsilon]\subset(0,1),
 \qquad
 \max_{\lambda\in\mathcal I_*,\,1\le j\le11}
 |\eta_*(v_j(\lambda)-w_j)|\le\frac14.                  \tag{7}
\]
This existence-defined neighborhood may depend on the fixed original
coefficients. No numerical radius or coefficient-independent radius is
claimed.

Use the **same** amplitude (6) at every parameter in (7):
\[
 h_7(T_j;\lambda)=1+\eta_*v_j(\lambda)\ge\frac14,\qquad
 h_7=1\text{ off support},\qquad h_n=1\ (n\le6).          \tag{8}
\]
The complete new parent-six probabilities are
\(q_\lambda(P,r,S)=q_{B_\lambda}(P,r,S)h_7(P+S;\lambda)\).
Equation (1) gives normalization of every complete marked row; (8)
gives strict positivity. The inherited record-local/shared-terminal
construction therefore gives an admissible finite prefix through seven
births for each \(\lambda\in\mathcal I_*\). Both newborn bits have
probability \(q_\lambda/2\), and the full payload convention is unchanged.

This is a family of fixed-parameter laws, not a protocol that changes
\(\lambda\) during a trajectory. The multiplier floor is uniform;
a uniform lower bound on all baseline or perturbed probabilities does
not follow from it.

## 4. Complete \(P_4\) contrast in both root sectors

Use \(P_4=C_4\oplus A_2\), with two incomparable caps \(a,b\).
The independently reviewed [complete inventory](SINGULAR_OBSERVABLE_WITNESS.md) remains valid at every parameter:

| Precursor ideal | Occurrences | Child | Width |
| --- | ---: | --- | ---: |
| Chain prefix of length 0, 1 or 2 | 3 | Outside support | 3 |
| Chain prefix of length 3 | 1 | \(T_4\) | 3 |
| Entire \(C_4\) | 1 | \(T_9\) | 3 |
| \(C_4\) and one cap | 2 | \(T_{10}\) | 2 |
| Full \(P_4\) | 1 | Outside support | 2 |

There are eight individual ideals and sixteen marked newborn outcomes.
The observation takes the complete child order and known parent embedding.
Its statistic is
\(W=2+\mathbf1\{x\text{ incomparable with both }a,b\}\).
Two cap-comparability queries suffice. No missing relations, unknown
embeddings, thinning, noisy readout or physical detector is supplied.
Neither records nor outcomes are filtered; both newborn bits are summed.

For root sector \(i=0,1\), compare against the baseline at the **same**
\(\lambda\). Importantly, \(v_4\) is generally nonzero away from the
exception and must be included:
\[
\begin{split}
 \delta_{4,i}(\lambda)
 &:=\mathbb E_{q_\lambda}W-\mathbb E_{B_\lambda}W\\
 &=\eta_*\rho_\lambda
   (3\lambda^2\theta D_i v_4+
    3\lambda^2\theta H_i v_9+4F_i v_{10})\\
 &=\eta_*\rho_\lambda\lambda^2\theta(D_i v_4+H_i v_9)\\
 &=-2\eta_*\rho_\lambda F_i v_{10}.                     \tag{9}
\end{split}
\]
The last two identities use the full fourth harmonic row in (1).
The factor four retains both distinct \(T_{10}\) ideals of width two.
This is equally the contrast in \(\Pr(W=3)\).

At \(\lambda_*\), (9) gives \(\delta_{4,i}=\rho_{\lambda_*}F_i(\lambda_*)>0\),
as in the [exceptional-law width witness](SINGULAR_OBSERVABLE_WITNESS.md). On the entire neighborhood (7),
\[
 -\frac34\le\eta_*v_{10}(\lambda)\le-\frac14,
\]
so the same fixed amplitude gives, simultaneously in both sectors,
\[
 \boxed{\quad
 \frac{F_i(\lambda)}2
 \le\frac{\delta_{4,i}(\lambda)}{\rho_\lambda}
 \le\frac{3F_i(\lambda)}2,\qquad
 \frac{\delta_{4,i}(\lambda)}{\rho_\lambda}>\frac14.
 \quad}                                                \tag{10}
\]
Here \(F_i>1-\theta-1/26>1/2\). Thus the contrast is positive on both
sides and at the exception, including all admitted transported markings.

Equation (10) implies the **pointwise** statement
\(\delta_{4,i}(\lambda)>\rho_\lambda/4>0\).
It does not supply a constant \(d>0\) with
\(\delta_{4,i}(\lambda)\ge d\) for all \(\lambda\in\mathcal I_*\).
The quotient in (10) is continuous; neither raw probability continuity nor
absolute-contrast continuity follows from the premises used here.
A separately admitted \(\rho_\lambda\ge\rho_{\min}>0\) on this
neighborhood would give \(\delta_{4,i}>\rho_{\min}/4\).
Continuity of \(\rho\) at the exception together with its positive value
would be one sufficient way to obtain such a bound on a smaller
neighborhood. **Neither premise is admitted or asserted here.**

## 5. Compatibility with the \(P_1\) quadratic upper bound

The complete \(P_1=C_3\oplus A_3\) width identity gives
\[
 \delta_{1,i}(\lambda)
 =\eta_*\rho_\lambda\lambda^3U_i
       \frac{\chi(\lambda)^2}{\Delta C(\lambda)}\ge0.    \tag{11}
\]
This is zero at the exception and positive off it. Since
\(p_i=\rho_\lambda\lambda^3U_i\) is an actual complete-row precursor
probability, \(0<p_i\le1\). Continuity and negativity of \(C\) give
\(c_*=\min_{\mathcal I_*}|C|>0\), and hence
\[
\begin{split}
 0\le\delta_{1,i}(\lambda)
 &\le\frac{\eta_*}{|\Delta|c_*}\chi(\lambda)^2\\
 &=\frac{\eta_*}{|\Delta|c_*}
   \left(\frac{\theta c_0\Xi}{360}\right)^2
   |\lambda-\lambda_*|^2.                              \tag{12}
\end{split}
\]
No continuity or lower bound of \(\rho_\lambda\) enters this upper bound.
Because \(\eta_*<1\), it also respects the broader [positive-contrast bound](POSITIVE_CONTRAST_LIMIT.md) over
all strictly positive multipliers. No matching lower rate or sharpness
is claimed.

Regularizing kernel coordinates does not undo the invariant \(P_1\)
width blindness. It gives a positive family through that point whose
surviving direction is detected at the different admitted parent \(P_4\).
These two conclusions are compatible; no support enlargement is involved.

## Public premises and scope

The [singular-law theorem](SINGULAR_LAW_WIDTH.md) supplies the complete
eleven-column system, fixed coefficient identities and strict \(C<0\) bound.
The [exceptional-law width witness](SINGULAR_OBSERVABLE_WITNESS.md) supplies
the exceptional kernel, exact positivity interval and complete \(P_4\)
inventory. The [positive-contrast limit theorem](POSITIVE_CONTRAST_LIMIT.md)
states the separate uniform upper bound over all positive multipliers at
\(P_1\). The [theorem package](THEOREM_PACKAGE.md) supplies the admitted
finite law and shared-terminal construction.

The original complete marked-row reduction, held-law coefficient identities,
\(C<0\), positive compatible baseline, and record-local/shared-terminal
payload construction remain inherited premises. Independent manual review
accepted the regular recovery, fixed-amplitude positivity and normalized
two-sector contrast. The regular recovery,
row substitutions, positivity neighborhood and contrast bounds printed here
are conditional finite mathematics, not a coefficient acquisition, sampling
implementation or observed simulation result.

The actual comparison \(\Xi>1\) remains unselected. The neighborhood is
existence-defined, with no numerical or coefficient-independent radius.
The lower bound concerns \(\delta_{4,i}/\rho_\lambda\); no continuity of
\(\rho_\lambda\), uniform positive lower bound for it, or uniform absolute
signal guarantee is admitted. Complete child-order access and the known parent
embedding remain mathematical observation assumptions.

For the explicitly prescribed full-layer half-scale continuation, the separate
[baseline-scale theorem](BASELINE_SCALE_THEOREM.md) proves continuity of
\(\rho^H_\lambda\) and a symbolic positive lower bound. It therefore upgrades
this normalized contrast to a uniform absolute lower bound on the same
conditional neighborhood. That conclusion uses the additional optional law
prescription; the general-family result above requires no such prescription.
An arbitrary positive compatible common-scale continuation need not have
continuity or a uniform absolute contrast. No numerical bound is supplied.

No sharpness, h8/30/33/38 transfer, all-size continuation, other-support
classification, informative quantum dynamics, geometric or physical claim
follows. This result neither changes the existing application protocols nor
establishes benchmark success or historical custody. See the
[publication note](PUBLICATION_NOTE.md) for review and evidence boundaries.
