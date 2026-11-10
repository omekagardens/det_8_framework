# Spectral field covariance under unread native growth

The proposed covariance consistency equation fails for both prepared bits. For the fixed old-field test vector $f=(1,-i)^T$, its prefix quadratic form is zero. Every continuation contributes a nonnegative value to the unread average, and the supported three-chain with an isolated fourth event contributes $\beta(2/\sqrt3-1)$. The full continuation weights therefore give a strict failure of the old marginal.

## Supplied spectral construction

Johnston v2, §II, Eqs. (18)–(23), supplies the positive spectral construction and the field relations on commutator zero modes. Equation (29) identifies its vacuum two-point function. The indexing check uses Eq. (35), where the paper uses the entry $12$ for the retarded response from its first point to its second. Our matrices use target row and source column, so the retarded matrix is transposed relative to that convention. With the control's sign $i(K_R-K_R^T)$, this transposes the paper's commutator matrix and its positive spectral part. The real symmetric part is preserved by this transpose. This inspection concerns the specified primary text and version. [Johnston, arXiv:0909.0944v2, §II and indexing in §III](https://arxiv.org/pdf/0909.0944v2)

## Prefix, continuation weights and covariance contract

Fix the prepared prefix $a\prec b$ with marks $(i,0)$ and consistent descendant counters $(1,0)$, for $i=0$ or $1$. Use the original conditional continuation law $P_i$ at this prefix. The 15 structural rows specify the ideals of the births $x,y$, and their four fair mark continuations give 60 histories of total mass one for each $i$. Each ordered suffix-mark pair carries one quarter of its structural row probability. The proof keeps these weights and the fixed labels $a,b$ in each row.

The supplied zero-mass kernel is $K_R=\beta C$, with one common $\beta>0$ and $C_{rs}=1$ exactly when $s\prec r$. Put $K_A=K_R^T$, $A=i(K_R-K_A)$ and
$$
 W=A_+=\frac{|A|+A}{2},\qquad |A|=\sqrt{A^2}.
$$
Use the standard counting inner product in the labelled vertex basis at both stages. In particular, the old basis vectors carry the same norm when included at stage four. The state rule supplies a centered two-point function in that field normalization. The history probabilities come from growth, while $K_R,A,W$ are supplied or calculated on each realized order.

For history $H$, write $B_H=W_4(H)[a,b;a,b]$ for the principal block in the fixed old labels. The prescribed field identification and unread marginal requirement give the equation
$$
                W_2=\overline B_i,\qquad
       \overline B_i:=\sum_{H=1}^{60}P_i(H) B_H.      \tag{1}
$$
Equality of the old-field marginal would require (1) because the quadratic moments of the same old fields are linear in the state. The equation concerns the unread mixture. The conditional field covariance may depend on the observed suffix. Old mark permanence is a property of the given growth records. Equation (1) is an additional premise for the field attachment.

## Positivity and the fixed commutator

The real matrix $K_R-K_R^T$ is antisymmetric, so $A$ is Hermitian and $A^T=-A$. Spectrally, $W$ acts by $\max(\lambda,0)$ on an $A$-eigenvector with eigenvalue $\lambda$. Thus $W$ is positive semidefinite, including when $A$ has zero modes. The matrix $A^2$ is real symmetric and positive semidefinite, and its positive square root is real symmetric. Consequently
$$
                            W-W^T=A.                \tag{2}
$$
In the target-first convention, the prefix matrices are
$$
 A_2=\beta\begin{pmatrix}0&-i\\ i&0\end{pmatrix},
 \qquad
 W_2=\frac{\beta}{2}\begin{pmatrix}1&-i\\ i&1\end{pmatrix}.
$$
Here the commutator of the old fields in the order $(a,b)$ is $-i\beta$. Each continuation preserves the induced order on those labels, hence $A_4(H)[a,b;a,b]=A_2$. Each $B_H$ is positive semidefinite and $B_H-B_H^T=A_2$. The unread mean has the same commutator since the weights sum to one.

For the fixed $f=(1,-i)^T$, $A_2 f=-\beta f$ and $W_2 f=0$. For every continuation, (2) gives
$$
    f^\dagger B_H f
       = \operatorname{tr}B_H+i\big((B_H)_{ba}-(B_H)_{ab}\big)
       = \operatorname{tr}B_H-\beta\ \ge0.            \tag{3}
$$
The last inequality follows from positivity of the principal block. Thus every continuation contributes at least the prefix value for this same old quadratic test. Equation (3) also compares the sum of the two old field variances, with prefix trace $\beta$.

Under the field interpretation, the quadratic form is the expectation of $F^\dagger F$ for $F=\phi_a-i\phi_b$. The old commutator gives $[F,F^\dagger]=2\beta$, and $F^\dagger F=\phi_a^2+\phi_b^2-\beta I$. The zero of the prefix quadratic form is a vacuum condition for this complex smearing. The commutator remains the same in the unread mixture.

## One supported strict contribution

Use the structural row $I_x=\{a,b\}$, $I_y=\varnothing$. Its terminal order is $a\prec b\prec x$ with $y$ isolated. The incoming third-birth probability is $19/30$ for $P_0$ and $7/15$ for $P_1$. The fourth-birth empty-ideal probability is $1/44$ in both. The row therefore has weights $19/1320$ and $14/1320$, respectively. All four suffix-mark pairs are included at one quarter of their row weight.

In this row $A_4=A_3\oplus0$. On $a,b,x$, let $v=(1,-1,1)^T$. Multiplying the skew matrix for the three-chain gives
$$
 A_3=i\beta\begin{pmatrix}0&-1&-1\\1&0&-1\\1&1&0\end{pmatrix},
 \qquad A_3^2=\beta^2(3I-vv^T).
$$
Since $v^T v=3$, $A_3^2$ vanishes on $v$ and is $3\beta^2 I$ on its orthogonal complement. Hence
$$
                   |A_3|=\frac{\beta}{\sqrt3}(3I-vv^T).
$$
Its diagonal entries are $2\beta/\sqrt3$. The zero diagonal of $A_3$ then gives $(B_H)_{aa}=(B_H)_{bb}=\beta/\sqrt3$ throughout the row. Therefore
$$
                f^\dagger B_H f=\beta(2/\sqrt3-1)>0. \tag{4}
$$
The strict sign follows from $4>3$. This calculation concerns the block of the four-event covariance on the declared continuation, including the isolated zero block.

## Failure after the suffix is unread

The prefix quadratic form is zero. Combining (3) and (4) with the complete original weights yields
$$
\begin{aligned}
 f^\dagger(\overline B_0-W_2)f
   &=\operatorname{tr}\overline B_0-\beta
     \ \ge\ \frac{19}{1320}\,\beta(2/\sqrt3-1)>0,\\
 f^\dagger(\overline B_1-W_2)f
   &=\operatorname{tr}\overline B_1-\beta
     \ \ge\ \frac{14}{1320}\,\beta(2/\sqrt3-1)>0 .
\end{aligned}
$$
These are exact positive lower bounds on the two full-law gaps. They use one strict row and the nonnegative contributions of every remaining marked history. The mixture includes the entire suffix law, so the violation concerns an unread marginal. Its commutator is still $A_2$, and the discrepancy lies in the symmetric covariance. A common positive normalization rescales both the covariances and the gap.

If the proposed marginal were preserved at each birth, applying the two successive restrictions and averaging with the complete continuation law would give (1) by total expectation. The violation therefore rejects the assignment as a projectively consistent interface at every birth under this identification.

## Zero modes and inherited field labels

The two-event commutator $A_2$ is invertible. On the witness row the commutator zero modes are the isolated $y$ direction and the embedded vector $(1,-1,1,0)^T$. Both also lie in the kernel of $W_4$. With Johnston's Eq. (23) quotient imposed, the corresponding field relations are $\phi_y=0$ and $\phi_a-\phi_b+\phi_x=0$. The covariance formula itself assigns zero second moment along these modes.

For any continuation, include an old coefficient vector $g$ as $\iota g=(g_a,g_b,0,0)^T$. If $A_4(H)\iota g=0$, restricting that vector equation to the old coordinates gives $A_2 g=0$, hence $g=0$. Thus the commutator quotient introduces no old-only linear field relation. The inherited old labels and their commutator remain available for the same test in every branch. The vector $f$ used in (3) lies in the negative spectral subspace of $A_2$, and its vanishing $W_2$ moment is a property of the prefix state rather than a commutator zero-mode relation.

## Decision and physical scope

Reject the joint prescription of fresh positive spectral assignment at every stage, fixed old-field transport, and the proposed unread marginal. Keeping the fixed labels and the unread requirement would call for a different state-selection premise, such as restrictions from a common completed-region state. Keeping the stagewise spectral choice would require a different field transport or marginal requirement. The calculation supplies the finite consistency test for this attachment.

The growth law supplies the original prepared histories and their weights. The benchmark, counting inner product, field normalization and marginal identification are inputs to the test. The derived quantities are covariance differences in the supplied $\beta$ normalization and dimensionless bounds after division by $\beta$. A physical field implementation and an action scale, clock, rest inertia or spacetime calibration require separate registration. The result is analytic and conditional on the exact finite model.


Accepted inputs: [Point-source propagation](point_source_propagation_on_finite_orders.md), [contact placement](contact_placement_in_finite_mass_propagation.md), [complete four-event law](finite_interval_action_and_source_preparation.md) and [prepared-source response](native_source_readout_response.md).
