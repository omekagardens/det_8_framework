# P4 observation by unlabelled, unmarked child shape

21 October 2026. Conditional manual finite-prefix theorem.

**Result.** For the accepted fixed baseline/perturbation pair, the complete
unlabelled, unmarked child order alone preserves full-row total variation
and is a statistically sufficient observation. Neither the newborn's identity
nor a supplied parent embedding is required. The eight individual ideals
produce exactly seven child shapes: the two single-cap births collide,
and no others do. Every collision has the same likelihood multiplier.

On a possibly smaller existence-defined neighborhood of the conditional
exception, the coarsest deterministic sufficient partition of these seven
shapes has four blocks off the exception and three at it. This is
fixed-pair sufficiency at each fixed \(\lambda\), not sufficiency for an
unknown-parameter family or for arbitrary parents.

## 1. Fixed experiment and inherited premises

Condition on \(\Xi>1\) and \(\lambda_*=\Xi^{-1}\in(0,1)\).
Use the [P4 observation-sufficiency manuscript](P4_OBSERVATION_SUFFICIENCY.md)'s accepted regular section \(v(\lambda)\), the same fixed
amplitude \(\eta_*=(2\kappa_*)^{-1}>0\), and its compact neighborhood
\(\mathcal I_*\subset(0,1)\). The parent is the fixed mathematical input
\[
 P_4=C_4\oplus A_2:
 \quad r_1<r_2<r_3<r_4<a,b,\qquad a\parallel b.
\]
Fix a complete old marking \(r\), with root record \(i=0\) or \(1\).
The comparison is at the same parameter, parent and old marking.
It does not average sectors or histories silently.

An ideal \(S\) produces a child by adding one maximal vertex \(x\) with
strict past \(S\). Both fair newborn records \(\beta=0,1\) are retained
in the complete outcome space
\(\Omega_r=\{(S,\beta):S\text{ an individual ideal of }P_4\}\).
Write its strictly positive baseline and perturbed probabilities as
\(p_r(\omega)\) and \(\widetilde p_r(\omega)\).
The accepted record-blind multiplier identity is
\[
 \widetilde p_r(S,\beta)
   =h_\lambda([P_4+S])\,p_r(S,\beta),\qquad
 h_\lambda(T_j)=1+\eta_*v_j(\lambda),                         \tag{1}
\]
with \(h_\lambda=1\) outside the eleven-class support.
All rows normalize, all multipliers are positive, and both newborn bits
have the same fair conditional law under the two hypotheses.
The arbitrary scalar-passive payload is unchanged by this observation question.

The needed inherited signs and values are
\[
 v_{10}<0,\quad v_9>0,\quad
 \operatorname{sgn}v_4=-\operatorname{sgn}(\lambda-\lambda_*).
                                                               \tag{2}
\]
For completeness these follow from the accepted formulas
\[
 v_{10}=-\frac{[D,F]}{\lambda\Delta},\qquad
 v_4=\frac{2\chi v_{10}}{\lambda^2\theta\Delta},\qquad
 v_9=\frac{2[D,F]^2}{\lambda^3\theta\Delta^2},
\]
where \(\Delta=[D,H]<0\), \(\theta>0\),
\(\chi=-g(\lambda-\lambda_*)\), \(g>0\), and
\(F_i=1-\lambda(\theta+\mu_i)>1/2\).
The fixed neighborhood has
\(-3/4\le\eta_*v_{10}\le-1/4\), so its numerator never vanishes.
At the exception,
\[
 h_4=1,\qquad h_{10}=\frac12,\qquad
 h_9=1+\frac{\kappa_*}{\lambda_*\theta}>1.                     \tag{3}
\]
Here \(h_j\) abbreviates \(1+\eta_*v_j\).
All three functions are continuous (indeed rational with nonzero
denominators) near \(\lambda_*\).

The parent class remains specified by the statistical experiment.
What is removed is the observation of an inclusion \(P_4\hookrightarrow
P_4+S\), old vertex labels, marks, and a distinguished newborn.
No claim of identifying an arbitrary unknown parent from a child is made.

## 2. Exhaustive shape collisions and noncollisions

An ideal omitting \(r_4\) is a chain prefix of length \(0,1,2\), or \(3\).
An ideal containing \(r_4\) consists of all \(C_4\) plus any subset of
the two caps. Thus there are exactly eight individual ideals.

Let \(K_k\), \(0\le k\le4\), be the unlabelled unmarked child shape
from the chain prefix of length \(k\); let \(K_c\) be the shape from a
single-cap ideal, and \(K_f\) the shape from the full ideal.
To prove the complete collision classification, use the intrinsic invariant
\[
 \mathcal J(H)=
 \{\!\{\,|\downarrow_H m|:m\in\operatorname{Max}(H)\,\}\!\},
 \qquad \downarrow_H m=\{y:y\le_H m\}.                        \tag{4}
\]
This is a multiset with multiplicity. It needs only the child's order
relation, not labels, marks, a newborn designation or a parent embedding.
An order isomorphism preserves maximality and principal-downset sizes.

| Ideal | Individual ideals | Fair-bit outcomes | Child shape | \(\mathcal J\) | Likelihood ratio |
| --- | ---: | ---: | --- | --- | --- |
| Empty prefix | 1 | 2 | \(K_0\) | \(\{\!\{1,5,5\}\!\}\) | \(1\) |
| Prefix length 1 | 1 | 2 | \(K_1\) | \(\{\!\{2,5,5\}\!\}\) | \(1\) |
| Prefix length 2 | 1 | 2 | \(K_2\) | \(\{\!\{3,5,5\}\!\}\) | \(1\) |
| Prefix length 3 | 1 | 2 | \(K_3=T_4\) | \(\{\!\{4,5,5\}\!\}\) | \(h_4\) |
| Entire \(C_4\) | 1 | 2 | \(K_4=T_9\) | \(\{\!\{5,5,5\}\!\}\) | \(h_9\) |
| \(C_4\cup\{a\}\), \(C_4\cup\{b\}\) | 2 | 4 | \(K_c=T_{10}\) | \(\{\!\{5,6\}\!\}\) | \(h_{10}\) |
| Full \(P_4\) | 1 | 2 | \(K_f\) | \(\{\!\{7\}\!\}\) | \(1\) |

For a prefix child \(K_k\), the three maximal vertices are \(a,b,x\).
Each cap has its four chain ancestors, hence downset size five.
The newborn's downset has size \(k+1\). This proves the first five
invariants, including the disconnected \(K_0\).

For a single-cap birth, the newborn and the other cap are the two maxima.
Their downsets have sizes six and five. The two single-cap children
are explicitly isomorphic: swap \(a\) and \(b\), fix the chain and \(x\).
This is an unmarked isomorphism; it need not preserve unequal old cap marks.

For the full birth, \(x\) is the unique greatest vertex and has downset
size seven. All seven displayed multisets are distinct. Therefore
the exhibited single-cap collision is the only collision among the eight
ideal outcomes, and the two bit outcomes of each ideal add no new shape.
This proves every collision and noncollision without a global order census.

The invariant (4) is injective on these seven possible shapes, although
no such injectivity is claimed for arbitrary finite orders. In particular
the \(T_9\) newborn can be indistinguishable from the old caps as a vertex
of the unmarked child; recognizing its shape does not identify that vertex,
and the proof never requires doing so.

## 3. Shape sufficiency and exact preservation of total variation

Let \(\Phi:\Omega_r\to\{K_0,\ldots,K_4,K_c,K_f\}\) forget labels,
marks and the newborn designation and return the child isomorphism class.
Every fiber has positive baseline mass. Equation (1) is constant on each
fiber, including all four marked atoms producing \(K_c\).
Consequently
\[
 \widetilde p_r^\Phi(H)=h_\lambda(H)p_r^\Phi(H),\qquad
 \widetilde p_r(\omega\mid\Phi=H)=p_r(\omega\mid\Phi=H).        \tag{5}
\]
This is pairwise statistical sufficiency. Explicitly the common conditional
kernel is \(p_r(\omega)/p_r^\Phi(H)\) on the fiber of \(H\).
It is a mathematical conditional distribution, not an implemented sampler
or physical reconstruction of vertex identities.

The same factorization gives
\[
 \begin{split}
 \operatorname{TV}(p_r^\Phi,\widetilde p_r^\Phi)
 &=\frac12\sum_H |h_\lambda(H)-1|\,p_r^\Phi(H)\\
 &=\frac12\sum_{\omega\in\Omega_r}
               |\widetilde p_r(\omega)-p_r(\omega)|\\
 &=\operatorname{TV}(p_r,\widetilde p_r).                    \tag{6}
 \end{split}
\]
All sixteen original atoms are used; no event is filtered or renormalized.
Even if baseline probabilities in a shape fiber differed, their shared
likelihood multiplier would still prove (5)–(6). Unmarked isomorphism alone
is not being used to assume equality of marked probabilities.

To connect directly with the accepted complete-row contrast, set
\[
 A_i=\eta_*\rho_\lambda\lambda^2\theta D_i v_4,\quad
 B_i=\eta_*\rho_\lambda\lambda^2\theta H_i v_9,\quad
 C_i=\eta_*\rho_\lambda F_i v_{10}.
\]
Then \(A_i+B_i+2C_i=0\), \(B_i>0\), \(C_i<0\).
The shape-level signed row, in the table's order, is
\[
                       (0,0,0,A_i,B_i,2C_i,0).
\]
The collision has combined equal-sign contributions, not cancelled them.
Thus for both sectors and every admitted old marking,
\[
 \operatorname{TV}_{\rm shape}
   =\frac12(|A_i|+B_i+2|C_i|)
   =\operatorname{TV}_{\rm full}.                           \tag{7}
\]
A positive TV-maximizing event is recognizable from shape alone:
on the left it is \(\{K_3,K_4\}\), at the exception or on the right
it is \(\{K_4\}\), with any zero-correction shapes optional.
In terms of (4), these are the \(\{4,5,5\}\) and \(\{5,5,5\}\)
cases on the left, and the \(\{5,5,5\}\) case on the right.
The embedding premise is therefore unnecessary for these events.

Forgetting only the fair newborn bit already preserves the conditional
law because that bit has the same conditional distribution under both
hypotheses. The additional loss of labels and embedding also preserves
the pair by (5); no record variable has been silently removed from the
definition of the original complete experiment.

## 4. Coarsest deterministic sufficient partition of shapes

“Smallest” here means **coarsest deterministic partition preserving
statistical sufficiency for the fixed two-law pair at that \(\lambda\)**,
not merely a binary event attaining TV.

A block of shapes is sufficient exactly when its likelihood ratio is
constant. To see necessity, if the two conditional distributions in a block
agree, division by its positive baseline probabilities gives
\(h_\lambda(H)=\widetilde p_r(B)/p_r(B)\) for every shape \(H\) in the block.
Conversely a constant ratio gives the same conditional distribution,
as in (5). Hence the coarsest partition is uniquely the collection of
equal-likelihood-ratio level sets.

Put
\[
                 N=\{K_0,K_1,K_2,K_f\}.
\]
Its likelihood ratio is exactly one. At the exception (3) gives three
distinct ratio levels and the exact three-block partition
\[
                  \boxed{\ \{N\cup\{K_3\},\ \{K_4\},\ \{K_c\}\}\ .\ } \tag{8}
\]

Away from the exception, potential coincidences between \(h_4\) and
\(h_9\), or between \(h_4\) and \(h_{10}\), must not be excluded by
assertion. They can be excluded locally without choosing any coefficients.
At \(\lambda_*\),
\[
 h_4-h_{10}=\frac12,\qquad
 h_9-h_4=\gamma_*:=\frac{\kappa_*}{\lambda_*\theta}>0.
\]
Continuity gives a compact neighborhood
\(\mathcal J_*\subset\mathcal I_*\), with \(\lambda_*\) in its interior,
on which
\[
                 h_4-h_{10}>\frac14,\qquad
                 h_9-h_4>\frac{\gamma_*}{2}.                 \tag{9}
\]
The same fixed amplitude is retained. No numerical radius or
coefficient-independent neighborhood is asserted.

Together with (2), this gives all ratio orderings:

| Position in \(\mathcal J_*\) | Strict ordering | Coarsest sufficient partition |
| --- | --- | --- |
| \(\lambda<\lambda_*\) | \(h_{10}<1<h_4<h_9\) | \(N,\{K_3\},\{K_4\},\{K_c\}\) |
| \(\lambda=\lambda_*\) | \(h_{10}<1=h_4<h_9\) | \(N\cup\{K_3\},\{K_4\},\{K_c\}\) |
| \(\lambda>\lambda_*\) | \(h_{10}<h_4<1<h_9\) | \(N,\{K_3\},\{K_4\},\{K_c\}\) |

Every listed shape has positive probability. Merging two distinct ratio
levels therefore destroys pairwise sufficiency; (8) and the four-block
partitions are minimal. Their blocks and ordering are the same in both
root sectors because the multiplier section is record-blind.

A TV-optimal **binary** event is a weaker reduction: it need only separate
the signs of the corrections, as in §3, and is not generally sufficient
for the full pair. Width's failure to be sufficient, already proved in
[the P4 observation-sufficiency manuscript](P4_OBSERVATION_SUFFICIENCY.md), is therefore not an obstruction to sufficiency of the seven-shape
observation or its three/four ratio-level reduction.
This classification is pointwise in \(\lambda\); no multi-parameter
sufficiency claim is added.

All conclusions (5)–(9) hold for any admitted positive common scale.
The scale cancels from likelihood ratios, and no regularity of
\(\rho_\lambda\) is needed. If the selected half-scale construction is used,
the previously proved absolute-TV bounds and rates transfer unchanged,
because (6) is an exact identity. No new scale selection is made here.

## 5. Forgetting or mixing old markings and root sectors

The preceding theorem is conditional on one fixed full old marking;
it holds separately for both root sectors. Forgetting that marking from
the **output** of this fixed-input experiment is not an assumption that
the input sectors were sampled with particular weights.

If an experiment instead mixes old markings \(r\) (including the root
sector), the direct extension requires a declared probability distribution
\(w_r\), **the same under baseline and perturbation**, at the same
\(\lambda\), fixed parent class, regular section and amplitude.
On the joint space that includes the old marking,
\[
 P(r,\omega)=w_r p_r(\omega),\qquad
 Q(r,\omega)=w_r h_\lambda(\Phi(\omega))p_r(\omega).            \tag{10}
\]
The ratio is still \(h_\lambda(H)\), independently of \(r\).
Thus shape remains sufficient and TV-preserving even relative to this
joint experiment that retains the old marking. Its shape marginal is
\[
 Q^\Phi(H)=h_\lambda(H)\sum_r w_r p_r^\Phi(H)
          =h_\lambda(H)P^\Phi(H).
\]
The same three/four-block classification follows. Weights may depend on
\(\lambda\), but must agree between the two hypotheses at each parameter;
they need not be uniform, and none is selected here.
Such equality would hold if both hypotheses were sampled from the same
unchanged pre-birth input distribution with the same conditioning.
That sampling premise is not silently added to a differently specified
experiment.

There is a precise obstruction if the two input mixtures differ.
Let their normalized weights be \(w_r\) and \(\widetilde w_r\).
In the unchanged shape \(K_0\), every \(p_r^\Phi(K_0)>0\) and the multiplier
equals one. The joint signed mass for a given old marking is therefore
\[
              (\widetilde w_r-w_r)p_r^\Phi(K_0).
\]
Any unequal normalized weights have both a positive and a negative weight
difference. Summing over markings within the same unmarked shape then
strictly contracts the absolute-difference sum. Thus
\[
 \operatorname{TV}(P^\Phi,Q^\Phi)<\operatorname{TV}(P,Q)        \tag{11}
\]
for this unequal-mixture comparison when the benchmark is the joint
experiment retaining old marking. This proof does not need numerical
weights or coefficients. It shows why equality of mixtures is essential
to the stated joint preservation result.

If the old marking has instead already been marginalized **before**
the benchmark is defined, that is a different experiment. Its shape
likelihood ratio, where the denominator is positive, is
\[
 h_\lambda(H)\,
 \frac{\sum_r\widetilde w_r p_r^\Phi(H)}
      {\sum_r w_r p_r^\Phi(H)}.                              \tag{12}
\]
One cannot infer the original three/four ratio-level partition from (12)
without the same-mixture premise or other explicit information.

In this admitted P4 row, shape does in fact remain sufficient relative
to the already-marginalized **ideal/bit** experiment even for unequal
input mixtures. The accepted baseline gives each single-cap ideal
probability \(\rho_\lambda F_i\), independently of the other old marks.
Each of its two bit atoms therefore has probability
\(\rho_\lambda F_i/2\), and the perturbation multiplies all four such atoms
by \(h_{10}\). Conditional on \(K_c\), these four atoms are uniform under
both laws and in every sector. Each other shape comes from one ideal,
so its two bit atoms are likewise conditionally uniform. This fixed
conditional kernel, independent of the old marking, survives either
mixture. It recovers the already-marginalized ideal/bit distributions
mathematically, not the discarded old-mark label or realized embedding.

Thus unequal mixtures strictly lose information when compared with the
**joint old-mark experiment** in (11), but the subsequent shape quotient
loses none of the information still present in the averaged ideal/bit
experiment. Its coarsest ratio-level partition may differ from (8)–(9)
according to (12). This distinction does not substitute an unmatched
mixture for the accepted fixed pair.

## 6. Removed assumption and remaining observation limit

The mathematical observation now requires only the **complete unmarked
seven-event order up to isomorphism**, with the tested parent class fixed
as \(P_4\). The intrinsic invariant (4) recognizes the seven outcome
shapes and the needed ratio-level blocks. It does not require knowing
which vertex was born, which cap was extended, any old labels or marks,
or an embedded copy of the parent.

This is still a native mathematical access assumption: the entire order
relation is available exactly. Nothing here constructs a physical procedure
that yields that order, proves its empirical observability, or handles
missing/delayed records, unknown parent-class mixtures, noisy relations,
coarse physical readout or quantum measurement implementation.
The result removes the embedding premise for this finite distinguishing
statistic; it does not remove the missing physical observation channel.

## Public premises and evidence scope

The [P4 observation-sufficiency manuscript](P4_OBSERVATION_SUFFICIENCY.md)
supplies the fixed complete-row experiment, multiplier identities, signs and
width comparison. The [regular observable family](REGULAR_OBSERVABLE_FAMILY.md)
supplies the regular section, fixed amplitude and positivity neighborhood.
The [baseline-scale theorem](BASELINE_SCALE_THEOREM.md) supplies the selected
half-scale regularity used only where explicitly stated. The
[theorem package](THEOREM_PACKAGE.md) states the admitted finite-law premises.

The shape inventory, intrinsic-invariant proof, factorization,
minimality and mixture obstruction are manual deductions.
Conditional occurrence,
fixed-law positivity/harmonicity and all other inherited premises remain.
No all-size, physical detector, QM reconstruction or geometry/gravity claim
is made.

This conditional finite manuscript removes the supplied parent embedding and
newborn identity for the fixed-pair observation while retaining exact access
to the complete child order. It supplies no physical observation channel.
The same-mixture and unequal-mixture comparisons have the distinct benchmarks
specified in §5; no unannounced input mixture is selected.

Private source labels, exact source/check correspondence, source fingerprints,
review/freeze records and raw administrative receipts are intentionally
withheld from this public derivative. Public relative dependencies above
identify its mathematical premises; they do not claim to reproduce private
source or check records. This edition supplies a manuscript, not an
executable installation or an independently replayable custody package.
See the [publication note](PUBLICATION_NOTE.md) and
[public evidence policy](../../coordination/REDACTED_PUBLICATION.md).

## Baseline nuisance parameters and the full shape law

The [nuisance-identifiability manuscript](P4_NUISANCE_IDENTIFIABILITY.md)
shows that, for the same fixed prefix, parent and full old marking, no admitted
baseline parameter and common scale reproduce the conditional fixed-amplitude
perturbed shape law. A two-shape probability ratio separates the model labels.
This does not identify the individual nuisance parameters or supply uniform
finite-sample stability. The three/four-block partitions above are not
sufficient for the full nuisance family; whether they distinguish the composite
models is a separate question. Exact complete-order access remains a
mathematical premise, with no physical observation channel supplied.
