# Positive harmonic width contrasts vanish at the exceptional law

20 October 2026. Conditional finite theorem for the fixed eleven-class,
record-blind parent-five family.

**Result.** Conditional on \(\Xi>1\) and
\(\lambda_*=1/\Xi\), the absolute target-width contrast tends to zero
uniformly over **every** strictly positive harmonic perturbation on the
declared support. Normalization and amplitude may depend arbitrarily on
\(\lambda\). In fact a local quadratic upper bound follows; no sharpness
or matching lower rate is claimed. No continuity or uniform positive lower
bound of \(\rho_\lambda\) is needed for this conclusion.

## 1. All admissible amplitudes in one variable

Retain the fixed original coefficients, eleven classes \(T_1,\ldots,T_{11}\),
and complete marked harmonic system \(M_\lambda\) specified in the
[singular-law kernel and width theorem](SINGULAR_LAW_WIDTH.md).
For any permitted multiplier write
\[
 h_7(T_j)=1+v_j>0,\qquad h_7=1\text{ off the support},\qquad
 h_n=1\quad(n\le6).
\]
Thus the complete conditions are
\[
          M_\lambda v=0,\qquad v_j>-1\quad(1\le j\le11).       \tag{1}
\]
If one starts with \(h_7=1+\epsilon(\lambda)Z_\lambda\), simply set
\(v=\epsilon(\lambda)z(\lambda)\). Equation (1) also describes the
multipliers directly, without selecting a normalization or an amplitude
recipe. All original record rows, ideal occurrences, full branches and
both newborn bits are retained.

A common positive scaling of the entire harmonic h sequence, including
the lower layers and unsupported values, cancels in transition ratios.
Dividing out that constant gives the stated baseline-relative convention.
No value of v1 or normalization of a factorization v=epsilon*z is imposed.
Scaling v itself generally changes the perturbation and must still
preserve v_j>-1.

For the complete target parent \(P_1=C_3\oplus A_3\), root bit \(i\),
let \(\delta_i(\lambda,v)\) be the perturbed-minus-baseline expected width
**at the same \(\lambda\)**. The accepted full-row identity is
\[
 \delta_i(\lambda,v)=p_i(\lambda)v_1,\qquad
 p_i(\lambda)=\rho_\lambda\lambda^3U_i,\qquad
 U_i=\theta^3b_i^3/a^2>0.                                  \tag{2}
\]
Here \(a=41/44\), \(b_0=8077/8800\), \(b_1=40303/44000\).
The coefficient \(p_i\) is the baseline probability of the single
precursor \(C_3\) in that complete row, with both newborn bits summed.
Consequently
\[
                         0<p_i(\lambda)\le1.              \tag{3}
\]
This uses probability normalization, not any regularity of \(\rho_\lambda\).

## 2. Two harmonic identities, with no division by \(\chi\)

Use the same two-root-sector columns
\[
\begin{gathered}
 H_i=\theta c_i,\quad D_i=\theta b_i,\quad
 (c_0,c_1)=(81/1100,3231/44000),\\
 F_i=1-\lambda(\theta+\mu_i),\quad X=\lambda D,\quad Y=\lambda H,\\
 [A,B]=A_0B_1-A_1B_0,\quad
 \Delta=[D,H]<0,\quad\chi(\lambda)=[H,F].
\end{gathered}
\]
The admitted bounds are \(0<\theta<10^{-10}\) and \(0\le\mu_i<1/26\).

The complete P1/P3 front elimination is linear in \(v_1\); write its
remaining P2 right-hand side as \(v_1Q(\lambda)\). This defines a
coefficient column, **not** a normalization of the perturbation.
Two of the remaining complete vector equations are
\[
\begin{aligned}
 Y(\lambda\theta v_4+v_5)+Fv_7&=v_1Q,\\
 Xv_7+Yv_{10}+Fv_{11}&=0.                                 \tag{4}
\end{aligned}
\]
Let \(C(\lambda)=[Y,Q]\). The [singular-law theorem](SINGULAR_LAW_WIDTH.md)
establishes \(C(\lambda)<0\) on \(0<\lambda\le1\).
It is continuous there: explicitly,
\[
 C(\lambda)=\frac{\lambda^4}{6K}
 \bigl(2[H,G][U,J]-[H,U][G,J]\bigr),\quad
 K=[H,J]>0,\quad J_i=1-\lambda+\lambda j_i,\quad
 G_i=\theta b_i^2/a.                                      \tag{5}
\]
The original \(j_i,\theta,\mu_i\) remain fixed and unselected.

Taking the bracket of each equation (4) with \(Y\) gives
\[
       C(\lambda)v_1=\lambda\chi v_7,\qquad
       \lambda\Delta v_7=\chi v_{11}.                     \tag{6}
\]
The second sign follows from
\([Y,X]=-\lambda^2\Delta\) and \([Y,F]=\lambda\chi\).
Multiplying the first relation by \(\Delta\) and using the second,
\[
                  \boxed{\Delta C(\lambda)v_1
                              =\chi(\lambda)^2v_{11}.}  \tag{7}
\]
No division by \(\chi\) occurred. Equation (7) therefore holds at the
exception as well as on both sides. Since \(\Delta C(\lambda)>0\),
it binds the width-changing coordinate to \(v_{11}\) for every vector
in the full homogeneous kernel.

## 3. Positivity bounds the coordinate on the right

The root-zero component of the second equation (4) is
\[
             \lambda D_0v_7+\lambda H_0v_{10}+F_0v_{11}=0.
\]
Using \(v_7,v_{10}>-1\) and \(F_0>0\) gives
\[
                    v_{11}<\frac{\lambda(D_0+H_0)}{F_0}. \tag{8}
\]
The fixed coefficient identities give
\[
 D_0+H_0=\theta(b_0+c_0)=349\theta/352<\theta,\qquad
 F_0>1-\theta-1/26>1/2.
\]
Together with \(\lambda\le1\) and the independent positivity condition
\(v_{11}>-1\),
\[
                       -1<v_{11}<2\theta<1,\qquad
                       |v_{11}|<1.                     \tag{9}
\]
This is a consequence of positivity of the complete perturbation,
particularly coordinates 7, 10 and 11. Positivity of the target row
alone would not supply these inequalities. No bound on a chosen
normalized \(z\) or a chosen \(\epsilon\) has been assumed.

Combining (2), (3), (7) and (9) yields the normalization-independent bound
\[
 |\delta_i(\lambda,v)|
 \le \frac{p_i(\lambda)\chi(\lambda)^2}
           {|\Delta|\,|C(\lambda)|}
 \le \frac{\chi(\lambda)^2}
           {|\Delta|\,|C(\lambda)|}.                    \tag{10}
\]

## 4. Uniform collapse near the exceptional law

Condition on the still-unselected comparison
\[
 \Xi=\theta+360\mu_1-359\mu_0>1,\qquad \lambda_*=1/\Xi\in(0,1).
\]
The accepted identity is
\[
 \chi(\lambda)=\frac{\theta c_0}{360}(1-\lambda\Xi)
             =-\frac{\theta c_0\Xi}{360}(\lambda-\lambda_*).
                                                               \tag{11}
\]
Choose a compact interval \(I_*\subset(0,1)\) with \(\lambda_*\) in
its interior. By the continuity and strict negativity in (5),
\[
                  c_*=\min_{\lambda\in I_*}|C(\lambda)|>0.
\]
For both root sectors and every multiplier satisfying (1),
\[
 |\delta_i(\lambda,v)|
 \le A_*|\lambda-\lambda_*|^2,\qquad
 A_*=\frac{(\theta c_0\Xi/360)^2}{|\Delta|c_*}<\infty,
 \quad\lambda\in I_*.                                   \tag{12}
\]
In particular,
\[
 \lim_{\lambda\to\lambda_*}
 \sup_{\substack{M_\lambda v=0\\v_j>-1\ \forall j}}
                  |\delta_i(\lambda,v)|=0.              \tag{13}
\]
At \(\lambda_*\), (7) gives \(v_1=0\) exactly, hence \(\delta_i=0\).
The constants depend on the fixed admitted family; no uniformity over
different choices of original coefficients is claimed.

This is consistent with the signed width-functional image being
\(\mathbb R\) at every nonsingular law. Arbitrarily scaling a signed
kernel vector does not preserve (1). The positive, normalized
probability contrasts form a smaller set, whose diameter is bounded
by \(2A_*|\lambda-\lambda_*|^2\). Nonzero width-blind perturbations
remain at the exception; the theorem does not eliminate all harmonic
perturbations or all order-law changes.

The separate [exceptional-law width witness](SINGULAR_OBSERVABLE_WITNESS.md)
makes one such change observable at \(P_4=C_4\oplus A_2\): conditional on
\(\Xi>1\), its complete-row width contrast is nonzero exactly when the
admissible kernel amplitude is nonzero. This does not change the present
\(P_1\) upper bound or imply its sharpness. Complete child-order access and
the parent embedding are assumed; no physical channel or simulation run follows.

## 5. What is and is not needed from \(\rho_\lambda\)

For (10)–(13), **neither continuity nor a uniform positive lower bound
of \(\rho_\lambda\) is needed**. The only scale-dependent step is
\(p_i\le1\), already forced by the normalized complete baseline row.
Even a varying scale with no assumed limit cannot defeat this upper bound.

A uniform nonzero quadratic lower bound on the supremum in (13), or a
matching two-sided rate for that envelope, would be a stronger claim.
There cannot be such a lower bound for every individual perturbation,
since the unchanged baseline is allowed. An envelope lower bound would
require a matching feasible positive perturbation family and quantitative
control from below of
\(p_i=\rho_\lambda\lambda^3U_i\). On this neighborhood, a positive lower
bound for \(\rho_\lambda\) would supply the latter; continuity at
\(\lambda_*\) together with \(\rho_{\lambda_*}>0\) would be one sufficient
way to obtain it, not a necessary condition. No such stronger conclusion
or sharpness claim is proved here.

Likewise (13) concerns the contrast against the baseline at the same
parameter. It is not a claim that the raw expected widths or entire
probability laws converge to their values at \(\lambda_*\).
Those statements require control of the baseline law itself.
No extra premise about that control has been silently inserted.

## Public premises and limits

The [singular-law theorem](SINGULAR_LAW_WIDTH.md) gives the complete
eleven-class object, full marked equations, front recovery and strict
\(C<0\) proof. The [theorem package](THEOREM_PACKAGE.md) supplies the admitted
finite law, original support and held-row coefficient identities. These
complete marked-row, positive-baseline and target-width premises remain
conditional; this proof does not reauthenticate their historical certificates.

The conclusion concerns the specified one-birth target-width contrast on
this support, against the baseline at the same parameter. It selects no
original coefficients and supplies no h8/30/33/38 transfer, other-support
classification, all-size geometry, physical prediction or empirical
validation. See the [publication note](PUBLICATION_NOTE.md) for review and
evidence boundaries.
