# A sufficient separation margin for complete population rows

**Accepted conditional result.** For the fixed model below, every pair of legal opposite-relative-sign population tuples is separated by at least \(m=3/320\) in maximum-word total variation. Their closed population-error neighborhoods are disjoint whenever \(2\eta<m\). This is a sufficient margin, not a sharp-distance or sampling claim. The proof received distinct review and coordinator acceptance.

## Complete model and target

The stipulated source has four equally weighted cells, a target block with Bloch vector \(X/2\), and mixed other blocks. The axis is common \(Z\), commands are positive half-commands, and the planar effects are \([I\pm(3X+4Z)/5]/2\). These are supplied model premises. The labelled words \(A\) and \(B\) are separate standalone commands; \(AB\) is their coherent composition without intermediate readout or reset. Signs remain fixed across words within each explanation. Only their product \(\sigma\in\{+1,-1\}\), the relative sign, is targeted; simultaneous sign reversal remains ambiguous.

Fix magnitude tolerance \(\epsilon=1/2\) and drift allowance \(\kappa=1/4\). Independently for each sign class choose
\[
q_\sigma=(r_A^\sigma,r_B^\sigma,a_\sigma,b_\sigma),
\quad r_A^\sigma,r_B^\sigma,a_\sigma,b_\sigma\in[1/2,3/2],
\]
\[
|a_\sigma-r_A^\sigma|\le1/4,
\qquad |b_\sigma-r_B^\sigma|\le1/4.
\]
The standalone centers of the two explanations need not coincide.

The complete ordered outcome alphabet is
\[
(00,+),(00,-),(01,+),(01,-),(10,+),(10,-),(11,+),(11,-),
\text{failure},\text{loss},\text{no-click},\text{timeout}.
\]
For \(t\in[-1,1]\), define the normalized twelve-entry row
\[
R(t)=\frac1{80}(10+3t,10-3t,10,10,10,10,10,10,0,0,0,0).
\]
The first two numerators are at least seven; all numerators sum to eighty. The exact population tuple is
\[
F_\sigma(q_\sigma)=\left(
R(\cos(\pi r_A^\sigma/2)),
R(\cos(\pi r_B^\sigma/2)),
R(\cos(\pi(a_\sigma+\sigma b_\sigma)/2))\right).
\]
Let \(\mathcal T_\sigma\) be its image over the legal parameter range. For complete normalized triples use
\[
d_\infty(P,Q)=\max_{w\in\{A,B,AB\}}\operatorname{TV}(P_w,Q_w),
\qquad \operatorname{TV}(p,q)=\tfrac12\sum_{j=1}^{12}|p_j-q_j|.
\]
Word positions and outcome labels are fixed. No target-only conditioning, renormalization or label permutation is used.

## Short proof of the uniform margin

Exactly two entries vary between ideal rows, so
\[
\operatorname{TV}(R(t),R(u))=3|t-u|/80.
\]
Set
\[
\Delta=\max\{|r_A^+-r_A^-|,|r_B^+-r_B^-|\}.
\]
On \([1/2,3/2]\), \(f(r)=\cos(\pi r/2)\) decreases with
\(|f'(r)|\ge\pi/(2\sqrt2)>1\). Integration gives
\(|f(r)-f(s)|\ge|r-s|\), including endpoints. Some standalone scalar difference is therefore at least \(\Delta\).

The two separate linkage constraints give
\[
|a_+-a_-|\le1/2+\Delta,
\qquad |b_+-b_-|\le1/2+\Delta.
\]
Let \(S=a_++b_+\in[1,3]\), \(D=a_--b_-\in[-1,1]\),
\(x=\min(S,4-S)\in[1,2]\) and \(y=|D|\in[0,1]\).
All four branches satisfy
\[
\begin{aligned}
S-D&=(a_+-a_-)+(b_++b_-)\ge1/2-\Delta,\\
S+D&=(a_++a_-)+(b_+-b_-)\ge1/2-\Delta,\\
4-S-D&=4-(a_++a_-)-(b_+-b_-)\ge1/2-\Delta,\\
4-S+D&=4-(b_++b_-)-(a_+-a_-)\ge1/2-\Delta.
\end{aligned}
\]
The first two inequalities use pair sums at least one; the last two use pair sums at most three, together with the displayed difference bounds. Their minimum is \(x-y\), hence \(x-y\ge1/2-\Delta\).

The folds cover both halves of \(S\) and both signs of \(D\); the ranges allow no further periodic branches. With \(u=x-1\), \(v=1-y\) in \([0,1]\), the sine chord inequality \(\sin(\pi z/2)\ge z\) yields
\[
\begin{aligned}
|\cos(\pi S/2)-\cos(\pi D/2)|
&=\sin(\pi u/2)+\sin(\pi v/2)\\
&\ge u+v=x-y\ge1/2-\Delta.
\end{aligned}
\]
If \(\Delta\ge1/4\), a standalone word has scalar difference at least \(1/4\); otherwise the coherent word has difference greater than \(1/4\). Applying the exact TV factor proves
\[
d_\infty(F_+(q_+),F_-(q_-))\ge3/320.
\]
This includes magnitude endpoints, saturated drift constraints and \(\Delta=1/4\), without identifying the two center pairs or assuming an optimizer. It bounds every pair and therefore their infimum; equality with that infimum is not asserted.

## Population-error interface and limits

For external \(\eta\ge0\), let \(B_\eta(\mathcal T_\sigma)\) contain complete normalized triples within distance \(\eta\) of some \(Q_\sigma\in\mathcal T_\sigma\). Perturbed rows may have positive failure, loss, no-click or timeout mass.

If \(P\) belonged to both neighborhoods, the full-row triangle inequality would give
\[
3/320\le d_\infty(Q_+,Q_-)
\le d_\infty(Q_+,P)+d_\infty(P,Q_-)\le2\eta.
\]
Thus \(2\eta<3/320\) makes them disjoint. At equality or above, this sufficient certificate proves neither overlap nor impossibility.

Return the sole compatible relative-sign class when exactly one neighborhood contains \(P\); otherwise **ABSTAIN**, including zero compatible classes. Correct identification additionally requires actual containment in the true class's neighborhood. The margin does not certify that premise or supply an efficient membership procedure.

This is deterministic population geometry. It supplies no sample size, confidence level, reporting probability, empirical calibration, physical implementation or efficiency benefit. A matched conventional block quantum model has the same conclusion. Preparation, drift certification, complete registration, restoration and physical costs remain external. The corrected twelve-label alphabet is retained; earlier omission and custody qualifications are not repaired. All scientific, review, calibration, protected-validation, custody, resource and execution gates remain.
