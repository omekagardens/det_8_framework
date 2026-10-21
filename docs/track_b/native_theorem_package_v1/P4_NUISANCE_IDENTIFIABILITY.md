# P4 nuisance-parameter identifiability from child shapes

21 October 2026. Conditional manual finite-prefix theorem.

**Result.** With the original prefix, parent and full old marking fixed,
no unperturbed law at any admitted \((\lambda_0,\rho_0)\) can exactly
reproduce the accepted fixed-amplitude perturbed child-shape law at
\((\lambda_1,\rho_1)\) in the conditional neighborhood.
Two observable shape probabilities already obstruct equality:
their baseline ratio is independent of both nuisance parameters,
whereas the perturbation strictly increases it.

This identifies the **baseline-versus-perturbation model label** in the
stated family. It does not identify \(\lambda\) and \(\rho\) individually,
establish finite-sample stability, or extend to an unknown original prefix,
parent or sector mixture.

## 1. Fixed experiment and the two model families

Keep the same admitted positive normalized original prefix \(q^0\)
through parent size five. Its actual entries are fixed, not refitted
when nuisance parameters change. The declared family leaves every
parent of size at most four unchanged and uses
\[
 q_\lambda(P,r,S)=
 \begin{cases}
  \lambda q^0(P,r,S),&|P|=5,\ S\subsetneq P,\\
  1-\lambda+\lambda q^0(P,r,P),&|P|=5,\ S=P,
 \end{cases}
 \qquad 0<\lambda\le1.                                      \tag{1}
\]
This is the complete parent-five change, including full complements.

At parent six, proper probabilities are
\[
 q^B_{\lambda,\rho}(P,r,S)=\rho\,u_\lambda(P,r,S),\qquad
 u_\lambda(P,r,S)=
 \prod_{\varnothing\ne A\subseteq\operatorname{Max}(P)\setminus S}
 q_\lambda(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}}.
                                                               \tag{2}
\]
Full probabilities are the complete normalization complements.
The nuisance scale \(\rho>0\) must be an **admitted common scale for
the entire marked six-parent layer**, not separately fitted scales for
individual shapes or selected rows. No regularity in \(\lambda\) and
no particular half-scale prescription is assumed.

Fix the same parent \(P_4=C_4\oplus A_2\), with caps \(a,b\) above
\(C_4=\{r_1<r_2<r_3<r_4\}\), and one declared full old marking \(r\).
Its root sector is fixed at \(i=0\) or \(i=1\). Both hypotheses use
that same \(r\). The theorem holds separately in either sector;
no sector or old-marking mixture is part of the primary comparison.

Let \(B_{\lambda,\rho;r}\) denote the complete unmarked child-shape law.
The accepted perturbation is
\[
 Q_{\lambda,\rho;r}(H)=h_\lambda(H)B_{\lambda,\rho;r}(H),       \tag{3}
\]
with the same regular section and fixed amplitude
\(\eta_*=(2\kappa_*)^{-1}>0\) as the [P4 observation comparison](P4_OBSERVATION_SUFFICIENCY.md) and [child-shape theorem](P4_CHILD_SHAPE_OBSERVATION.md).
It is admitted for \(\lambda\in\mathcal I_*\), the accepted compact
neighborhood of the conditional exception
\(\lambda_*=\Xi^{-1}\in(0,1)\), conditional on \(\Xi>1\).
Changing the common scale does not change its harmonic section or
positivity neighborhood. The full row has eight individual ideals
and sixteen fair-bit outcomes before taking child shapes.

## 2. Two shape probabilities from complete maximal deletion

Only two proper ideals are needed:
\[
                         S_0=\varnothing,\qquad S_9=C_4.
\]
Their child shapes are \(K_0\) and \(K_4=T_9\), respectively, in
[the child-shape theorem](P4_CHILD_SHAPE_OBSERVATION.md)'s notation. They are distinct and each is produced by exactly
one ideal in the complete row. Intrinsically, the multisets of
maximal-element principal-downset sizes are
\[
                 \mathcal J(K_0)=\{1,5,5\},\qquad
                 \mathcal J(K_4)=\{5,5,5\}.
\]
These identify the shapes within this seven-shape family without
observing the newborn or an embedded parent.

For either \(S=S_0\) or \(S=S_9\), the omitted maxima in (2) are exactly
\(\{a,b\}\). Its complete inclusion-exclusion product is therefore
\[
 u_\lambda(P_4,r,S)=
 \frac{
 q_\lambda(P_4\setminus\{a\},r|_{P_4\setminus\{a\}},S)
 q_\lambda(P_4\setminus\{b\},r|_{P_4\setminus\{b\}},S)}
 {q^0(C_4,r|_{C_4},S)}.                                    \tag{4}
\]
Both numerator parents are five-chains, and **both chosen ideals
are proper in those five-parents**. Consequently each numerator
gets exactly one factor \(\lambda\) from (1). The denominator
belongs to the unchanged four-parent prefix. For \(S=C_4\) it is
a full-slot probability, not a proper one; it is nevertheless fixed
and strictly positive. No parent-five full-complement factor is
inserted into either numerator.

Define the two fixed positive constants
\[
 U_{S,r}:=
 \frac{
 q^0(P_4\setminus\{a\},r|_{P_4\setminus\{a\}},S)
 q^0(P_4\setminus\{b\},r|_{P_4\setminus\{b\}},S)}
 {q^0(C_4,r|_{C_4},S)},\qquad
 U_{0,r}=U_{S_0,r},\quad U_{9,r}=U_{S_9,r}.                  \tag{5}
\]
These are definitions using the already admitted prefix, not acquired
or numerically evaluated coefficients. The two numerator factors
retain their actual induced markings. No equality of marked probabilities
under a cap swap is assumed or needed.

Equations (2)–(5) give exactly
\[
 \boxed{\quad
 B_{\lambda,\rho;r}(K_0)=\rho\lambda^2U_{0,r},\qquad
 B_{\lambda,\rho;r}(K_4)=\rho\lambda^2U_{9,r}.
 \quad}                                                      \tag{6}
\]
Each shape has one individual ideal and two fair newborn bits; summing
the two \(q/2\) branches gives \(q\), not \(q/2\) or \(2q\).
The other six ideals and their bits remain in the normalized law.
Checking two of its coordinates is a necessary condition for equality
of whole laws, not filtering or conditioning on those coordinates.

## 3. Nuisance-invariant ratio and the exact non-mimicry theorem

Every admitted baseline in this fixed-prefix, fixed-marking family obeys
\[
 \frac{B_{\lambda,\rho;r}(K_4)}
      {B_{\lambda,\rho;r}(K_0)}
          =R_r:=\frac{U_{9,r}}{U_{0,r}}>0.                    \tag{7}
\]
Both nuisance parameters cancel. The denominator is strictly positive
because \(\lambda,\rho,U_{0,r}>0\).

The accepted perturbation leaves \(K_0\) unchanged and multiplies \(K_4\)
by \(h_9(\lambda)=1+\eta_*v_9(\lambda)>1\) throughout \(\mathcal I_*\).
In the accepted section,
\[
 v_9(\lambda)=\frac{2[D,F(\lambda)]^2}
                    {\lambda^3\theta\Delta^2}>0.
\]
Here \(\lambda,\theta>0\), \(\Delta\ne0\), and
\(v_{10}=-[D,F]/(\lambda\Delta)<0\) on \(\mathcal I_*\) ensures that
the squared numerator is nonzero. Thus the strict inequality does
not fail at the exception or on either side. In particular
\(h_9(\lambda_*)=1+\kappa_*/(\lambda_*\theta)>1\).

Hence
\[
 \boxed{\quad
 \frac{Q_{\lambda_1,\rho_1;r}(K_4)}
      {Q_{\lambda_1,\rho_1;r}(K_0)}
      =R_r h_9(\lambda_1)>R_r
 \quad(\lambda_1\in\mathcal I_*).
 \quad}                                                       \tag{8}
\]

**Non-mimicry theorem.** For every \(\lambda_1\in\mathcal I_*\) and
admitted \(\rho_1>0\), and every \(\lambda_0\in(0,1]\) with an admitted
\(\rho_0>0\),
\[
                       Q_{\lambda_1,\rho_1;r}
                             \ne B_{\lambda_0,\rho_0;r}.      \tag{9}
\]
In particular the conclusion holds when both parameter values lie in
the conditional neighborhood.

**Proof.** Equality at \(K_0\), using (6) and its unchanged multiplier,
would force
\(\rho_0\lambda_0^2=\rho_1\lambda_1^2\).
Equality at \(K_4\) would then require
\(h_9(\lambda_1)=1\), contradicting (8).
Equivalently the two complete laws have different observable ratios (7)–(8).
This uses no other probability evaluation. \(\square\)

An equivalent division-free separator of shape laws \(p\) is
\[
 \mathcal G_r(p):=p(K_4)-R_rp(K_0).
\]
It satisfies
\[
 \mathcal G_r(B_{\lambda,\rho;r})=0,\qquad
 \mathcal G_r(Q_{\lambda_1,\rho_1;r})
  =\rho_1\lambda_1^2U_{9,r}\,[h_9(\lambda_1)-1]>0.            \tag{10}
\]
The value \(R_r\) is fixed by the original prefix but is not numerically
calibrated here. This is an algebraic identifiability result for the
stated model, not a numerical decision threshold.

The proof uses the full unmarked child-shape law. Labels appear in (4)–(5)
only to derive its probabilities in a mathematical representative.
They are not reintroduced as required observations.

## 4. Fixed-pair minimal partitions are not uniform-family sufficiency

[The child-shape theorem](P4_CHILD_SHAPE_OBSERVATION.md)'s three/four-block partitions were proved sufficient for one fixed
baseline/perturbation pair. The present proof does not promote that
result to the nuisance family. Indeed those partitions all merge \(K_0\)
with the full-birth shape \(K_f\) in their neutral block (and at the
exception also merge \(K_3\)).

At a fixed admitted \(\lambda\), let
\[
 T_r(\lambda)=\sum_{S\subsetneq P_4}u_\lambda(P_4,r,S)>0
\]
be the **complete** proper-potential sum, with every individual ideal.
The full shape has exactly the full ideal as precursor, so
\[
 B_{\lambda,\rho;r}(K_f)=1-\rho T_r(\lambda)>0.
\]
Within the neutral block, the baseline probability ratio is
\[
 \frac{B_{\lambda,\rho;r}(K_0)}
      {B_{\lambda,\rho;r}(K_f)}
   =\frac{\rho\lambda^2U_{0,r}}{1-\rho T_r(\lambda)}.           \tag{11}
\]
It strictly increases with \(\rho\) on the admitted positive range:
its derivative is
\(\lambda^2U_{0,r}/(1-\rho T_r)^2>0\).
Distinct sufficiently small common scales are admitted by the same
continuation construction (decreasing a common scale increases all full
complements). Therefore the conditional distribution inside that block
changes across baseline nuisance choices.

Those fixed-pair minimal partitions are consequently **not** statistically
sufficient for the whole nuisance family. This obstruction needs no
numerical row sum or additional coefficient selection. It does not impede
(9), which retains the full shape law and its separate \(K_0\) coordinate.
This failure of ordinary full-family sufficiency does not itself prove that
those compressed partitions cannot distinguish the two composite hypotheses.
That weaker question is not settled by (11). No alternative uniform-family
minimal partition is classified here.

## 5. Exact scope versus stability and physical observation

The load-bearing premises for (9) are:

- The same original complete prefix \(q^0\), the declared uniform
  parent-five proper scaling (1), and the admitted deletion-potential
  construction.
- The same \(P_4\) parent and one fixed full old marking under both models.
- A single admitted positive common six-parent scale at each parameter,
  not independently adjustable shape/component scales.
- The accepted fixed nonzero amplitude, positive regular perturbation
  neighborhood, unchanged \(K_0\), and strictly increased \(T_9\).
- Exact access to the complete unlabelled, unmarked child order,
  so the two distinct shapes and their law are well-defined.

No scale continuity, lower bound, or half-scale selection is needed.
The selected half-scale family is a subfamily of the one treated here,
so it also cannot mimic the perturbation by changing its baseline parameter.
No new regularity or numerical-effect claim for that subfamily is added.

This is not a proof that either \(\lambda\) or \(\rho\) can be uniquely
recovered within one model family. It is a proof that the two specified
families of shape laws do not intersect at positive admitted scales.
Changing the original prefix would change \(R_r\); changing marking or
parent, mixing sectors, or allowing component-dependent scales would
change the comparison. Those are outside the primary claim, not excluded
by (9).

Exact separation does not imply uniform finite-sample stability.
At any fixed \(\lambda_1\in\mathcal I_*\), admitted common scales can
decrease toward zero. All proper probabilities are then \(O(\rho)\);
the unchanged full-birth complement tends to one. Baseline and perturbation
both approach the point mass at \(K_f\), and their TV difference at that
same parameter tends to zero, despite (8) holding at every positive scale.
The zero scale itself is not admitted. Thus the two families can have
touching closures without an exact intersection. No error bars, sample
size, numerical neighborhood, lower effect size or ratio-estimation
guarantee is supplied.

The complete order remains a native mathematical access assumption.
The proof neither constructs a physical readout of it nor handles missing
or noisy order relations. Unknown parent/sector mixtures and physical
observation channels are distinct unaddressed questions here.
The result is not QM reconstruction, emergent geometry, or empirical
validation.

## Public premises and evidence scope

The first section of the [baseline-scale theorem](BASELINE_SCALE_THEOREM.md)
supplies the complete parent-five scaling, maximal-deletion potentials,
full normalization complements and admitted common-scale construction.
The [law-family supplement](LAW_FAMILY_SUPPLEMENT.md) distinguishes the
parent-five change from its compatible later-layer continuation; no
particular half-scale prescription is forced in the present comparison.
The [P4 observation comparison](P4_OBSERVATION_SUFFICIENCY.md) and
[regular observable family](REGULAR_OBSERVABLE_FAMILY.md) supply the
accepted section, fixed amplitude, signs and positivity neighborhood.
The [child-shape theorem](P4_CHILD_SHAPE_OBSERVATION.md) supplies exact
shape identification and its fixed-pair sufficiency statements. The
[theorem package](THEOREM_PACKAGE.md) states the inherited finite-law premises.

The two potential reductions, nuisance cancellation, non-mimicry proof,
partition obstruction and closure limit are manual deductions.
No actual \(\Xi\) selection,
new physical premise, later-layer/all-size transfer or successor is supplied.

This manuscript retains the same fixed prefix, parent and full old marking.
Exact model-label separation does not identify the individual nuisance
parameters or supply uniform finite-sample stability. Complete unmarked
order access remains a mathematical premise, and no physical observation
channel is supplied. The whole-family sufficiency obstruction does not
settle whether the compressed partitions can distinguish the composite
hypotheses.

Private source labels, exact source/check correspondence, source fingerprints,
review/freeze records, raw administrative receipts and reader/checker scripts
are intentionally withheld from this public derivative. These public relative
dependencies state mathematical premises; they do not claim to reproduce
private custody records. This edition supplies conditional mathematical
exposition, not an executable installation or an independently replayable
custody package. See the [publication note](PUBLICATION_NOTE.md) and
[public evidence policy](../../coordination/REDACTED_PUBLICATION.md).
