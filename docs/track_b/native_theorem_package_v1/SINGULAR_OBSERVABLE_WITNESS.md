# A surviving width observable at the exceptional law

20 October 2026. Independently reviewed conditional finite-prefix theorem.

**Result.** The proposed \(P_4\) width statistic is not blind. The
exceptional harmonic direction changes the full-row expected width of
its child for every nonzero admissible scalar amplitude. Thus blindness
of width at \(P_1\) does not imply blindness of width at every admitted
parent. No alternative statistic or enlarged support is needed.

## 1. Fixed conditional law and its complete surviving direction

Condition on
\[
 \Xi=\theta+360\mu_1-359\mu_0>1,\qquad
 \lambda_*=\Xi^{-1}\in(0,1).
\]
No actual coefficient comparison is selected. Let \(B_*=B_{\lambda_*}\)
be the admitted baseline, with its positive parent-six common scale
\(\rho_*=\rho_{\lambda_*}\). The fixed coefficients satisfy
\(0<\theta<10^{-10}\) and \(0\le\mu_i<1/26\). Put
\[
 H_i=\theta c_i,\quad D_i=\theta b_i,\quad
 F_i=1-\lambda_*(\theta+\mu_i),\qquad
 (c_0,c_1)=(81/1100,3231/44000),\quad
 (b_0,b_1)=(8077/8800,40303/44000).
\]
Here \(i=0,1\) denotes the original root record.
At the exception the accepted identity is
\[
 F=\kappa\lambda_*H,\qquad
 \kappa=\frac{F_0}{\lambda_*H_0}>0.
\]

The [singular-law kernel theorem](SINGULAR_LAW_WIDTH.md) gives the **entire** eleven-column homogeneous kernel as
\[
 \operatorname{span}\{w\},\qquad
 w=(0,0,0,0,0,0,0,0,A,-\kappa,1),\qquad
 A=\frac{2\kappa^2}{\lambda_*\theta}>0.                   \tag{1}
\]
The three nonzero entries name actual unmarked children. With \(I=C_3\),
\(C_k,A_k\) a chain and antichain, and \(\oplus,\sqcup\) ordinal sum
and disjoint union, they are
\[
 T_9=I\oplus(A_1\oplus A_3),\quad
 T_{10}=I\oplus(A_1\oplus(C_2\sqcup A_1)),\quad
 T_{11}=I\oplus(C_2\oplus A_2).
\]
For a real scalar \(\eta\), define the actual multiplier by
\[
 h_7(T_j)=1+\eta w_j,\qquad
 h_7=1\text{ on all other seven-order classes},\qquad
 h_n=1\quad(n\le6).
\]
Thus \(\eta\) is the actual coefficient of \(w\), not an additional
fixed-amplitude convention. Any factorization \(v=\epsilon z\) on this
one-dimensional kernel is included by absorbing its scalar into \(\eta\).

The new complete one-birth probabilities at any six-parent are
\[
 q_\eta(P,r,S)=q_{B_*}(P,r,S)\,h_7(P+S).
\]
They sum to one by the inherited complete harmonic equations. When all
multipliers are positive, the entire finite prefix through seven births
is admissible by the accepted record-local/shared-terminal construction.
For this vector the first three incoming parent equations vanish termwise;
the fourth cancels as in (6) below, and the fifth is
\(-\kappa\lambda_*H+F=0\). The admitted complete incoming catalogue
has no other nonzero correction rows, including across all markings.
Both newborn bits retain branch weights \(q_\eta(P,r,S)/2\); the
scalar-passive payload convention is unchanged.

## 2. Exact positivity interval on all eleven coordinates

The only nonconstant multipliers are
\[
 h_7(T_9)=1+\eta A,\qquad
 h_7(T_{10})=1-\eta\kappa,\qquad
 h_7(T_{11})=1+\eta.
\]
Before simplifying, strict positivity is exactly
\[
          \max\{-1,-1/A\}<\eta<1/\kappa.                \tag{2}
\]
No coordinate is omitted just because it is absent from the target row.

The admitted bounds imply
\(F_0>1-\theta-1/26>1/2\), while
\(\lambda_*H_0=\lambda_*\theta c_0<1/2\).
Hence \(\kappa>1\). Also \(0<\lambda_*\theta<1\), so \(A>1\).
Equation (2) therefore simplifies to the exact interval
\[
 \boxed{\displaystyle
       -\frac{\lambda_*\theta}{2\kappa^2}
             <\eta<\frac1\kappa.}                      \tag{3}
\]
Within (3), the \(T_{11}\) condition is redundant because
\(\eta>-1/A>-1\), not because \(T_{11}\) was discarded.
The lower endpoint makes \(h_7(T_9)=0\), and the upper endpoint
makes \(h_7(T_{10})=0\); both are excluded by strict positivity.
Outside this interval at least one required multiplier is nonpositive.
All other multipliers equal one.

Consequently (3) is necessary and sufficient for this finite-prefix
positive family. No artificial upper bound \(h_7\le1\) is imposed:
normalized transition probabilities are bounded by one because the
complete positive row sums to one.

## 3. Parent, observation and complete outcome accounting

Take
\[
 P_4=C_3\oplus(A_1\oplus A_2)=C_4\oplus A_2.
\]
Write its four-chain as \(r_1<r_2<r_3<r_4\), with incomparable caps
\(a,b\) above \(r_4\). Its width is two. The old root mark is \(i\);
other old marks may be fixed identically in the baseline and perturbed
comparison. The contrast below holds across their admitted transported
markings.

Append the new maximal vertex \(x\) with precursor an ideal \(S\).
There are exactly eight individual ideals, including the full one.
Each has both newborn bits, so the complete marked row has sixteen
outcomes. Let \(I=\{r_1,r_2,r_3\}\). The full ideal inventory is:

| Precursor \(S\) | Individual occurrences | Child class | Child width | Multiplier |
| --- | ---: | --- | ---: | --- |
| Chain prefix of length 0, 1 or 2 | 3 | Outside the eleven-class support | 3 | 1 |
| \(I\), chain prefix of length 3 | 1 | \(T_4=I\oplus((A_1\oplus A_2)\sqcup A_1)\) | 3 | 1 |
| Entire \(C_4\) | 1 | \(T_9=I\oplus(A_1\oplus A_3)\) | 3 | \(1+\eta A\) |
| \(C_4\cup\{a\}\) or \(C_4\cup\{b\}\) | 2 | \(T_{10}=I\oplus(A_1\oplus(C_2\sqcup A_1))\) | 2 | \(1-\eta\kappa\) |
| Full \(P_4\) | 1 | Outside the support; unique greatest vertex | 2 | 1 |

Here \(\oplus\) and \(\sqcup\) denote ordinal sum and disjoint union.
The original caps are the only old two-antichain. Any child antichain
larger than two must contain \(x\) and both caps. Thus width is exactly
two or three, and
\[
 W=2+\mathbf1\{x\text{ is incomparable with both }a,b\}.   \tag{4}
\]
This proves the table's widths without selecting favorable births.

The observation channel takes the **complete child order** and the known
initial-parent embedding, then reports \(W\), or the bounded binary
statistic \(Y=W-2\). Two cap-comparability queries suffice. Missing order
relations, unknown embeddings, thinning or noisy readout are not included.
This is exact mathematical order access, not a proposed physical detector
or an assertion that a sampling implementation exists.

No outcome or record is filtered. The newborn bit is ignored by this
order statistic but both values are summed; old records remain in the
native object. The comparison is at the same \(\lambda_*\), parent and
old marking, not between different baseline parameters or a selected
subset of visits to the parent.

## 4. Full-row contrast in both root sectors

The accepted complete P4 harmonic row has supported coefficients
\[
 \rho_*\bigl(
   \lambda_*^2\theta D_i z_4+
   \lambda_*^2\theta H_i z_9+2F_i z_{10}\bigr)=0.         \tag{5}
\]
In particular, \(T_9\) has one precursor of baseline probability
\[
 p_{9,i}=\rho_*\lambda_*^2\theta H_i,
\]
and each of the two \(T_{10}\) precursors has probability
\(p_{10,i}=\rho_*F_i\). Their multiplicity is retained.

For \(z=w\), (5) is the exact cancellation
\[
                  p_{9,i}A=2p_{10,i}\kappa,             \tag{6}
\]
since \(F_i=\kappa\lambda_*H_i\).
Every other ideal has zero correction, not zero baseline probability.
Using its actual width from the table, the full-row contrast is
\[
\begin{split}
 \delta_{4,i}(\eta)
  &:=\mathbb E_{q_\eta}W-\mathbb E_{B_*}W\\
  &=\eta\bigl(3p_{9,i}A-4p_{10,i}\kappa\bigr)\\
  &=\eta p_{9,i}A
    =2\eta\rho_*\kappa F_i
    =2\eta\rho_*\lambda_*\kappa^2 H_i.                  \tag{7}
\end{split}
\]
The factor four in the second line is width two times two separate
precursors. Both fair newborn bits contribute their complete probability
sum. Formula (7) is equally the change in
\(\Pr(W=3)=\mathbb E Y\).

Explicitly, the two-sector contrast is
\[
 \boxed{\displaystyle
 (\delta_{4,0},\delta_{4,1})
 =2\eta\rho_*\lambda_*\theta\kappa^2
       (81/1100,\ 3231/44000).}                         \tag{8}
\]
The same scalar \(\eta\) applies to both sectors. Every factor other
than \(\eta\) is positive. Therefore every nonzero \(\eta\) in (3)
is a nonzero observable witness: positive \(\eta\) increases width,
negative \(\eta\) decreases it.

For example, the explicit symbolic choice \(\eta=1/(2\kappa)\) lies
strictly inside (3), gives \(h_7(T_{10})=1/2\), and produces
\(\delta_{4,i}=\rho_*F_i>0\). It selects only an amplitude in the
conditional family, not any original coefficient value.

For completeness, each scalar contrast ranges over the exact open interval
\[
                 -p_{9,i}<\delta_{4,i}<2p_{10,i}.        \tag{9}
\]
These are not independently adjustable root-sector contrasts.
The excluded endpoints would remove all \(T_9\) mass, or both
\(T_{10}\) masses, respectively.

## Public premises and scope

The kernel remains width-blind at \(P_1=C_3\oplus A_3\), as proved
previously. The present witness is width at a different already admitted
parent \(P_4\); it neither contradicts nor extends the near-exception
\(P_1\) contrast theorem. The result is a finite-prefix mathematical
observable, not an observed experimental signal or a sampling design.
Actual occurrence of \(\lambda_*\) remains conditional on \(\Xi>1\).

The [regular observable family](REGULAR_OBSERVABLE_FAMILY.md) extends this
fixed-exception direction with a kernel section normalized by \(v_{11}=1\),
without dividing by \(\chi\). Conditional on \(\Xi>1\), one fixed amplitude
keeps all multipliers at least \(1/4\) on a neighborhood and gives positive
\(P_4\) width contrast there in both root sectors. Its uniform lower bound is
for \(\delta_{4,i}/\rho_\lambda>1/4\), not for the absolute contrast.
No continuity or uniform lower bound of \(\rho_\lambda\) is assumed.

The [singular-law kernel theorem](SINGULAR_LAW_WIDTH.md) supplies the complete
eleven-column harmonic system, exceptional kernel and admitted coefficient
bounds. The [positive-contrast limit theorem](POSITIVE_CONTRAST_LIMIT.md)
states the distinct near-exception result for width at \(P_1\).
The [theorem package](THEOREM_PACKAGE.md) supplies the admitted finite law,
complete marked-row reduction, positive baseline and scalar-passive
shared-terminal construction. Those premises remain conditional.

Independent review accepted the full ideal inventory, both root-sector
contrasts and the exact positivity interval. This publication supplies their
equations and proof, not an executed simulation, a validated sampler or a
numerical comparison of the original coefficients. Complete child-order access
and the known parent embedding are mathematical observation assumptions.
The actual comparison \(\Xi>1\) remains unselected.

No h8/30/33/38 transfer, other-support classification, all-size geometry,
sharp near-exception rate or physical-channel claim is made. Historical
custody and finite-certificate limitations remain unchanged; see the
[publication note](PUBLICATION_NOTE.md) for review and evidence boundaries.
