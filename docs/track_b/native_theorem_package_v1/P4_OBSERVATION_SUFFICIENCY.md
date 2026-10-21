# Width versus the complete P4 one-birth row

20 October 2026. Conditional manual finite-prefix theorem.

**Result.** Conditional on \(\Xi>1\), width retains the complete row's
total-variation distinguishing power at \(\lambda_*=1/\Xi\) and immediately
to its left. Immediately to its right, width strictly loses distinguishing
power: the \(T_4\) correction becomes negative while the \(T_9\) correction
remains positive, and width pools them. The exact loss divided by the common
scale has a positive first-order right-hand term and is zero on the left.
For the selected half-scale family, the absolute loss is also first order
on the right. Arbitrary positive common scales need not give that lower rate.

Here “no loss” means equality of total variation for this fixed pair of
one-birth laws. It does **not** mean that width is a statistically sufficient
summary of the entire pair; §6 gives an explicit obstruction even where
the total-variation loss is zero.

## 1. Fixed family, neighborhood and notation

Keep the original law, eleven-class regular section, fixed scalar amplitude
and compact neighborhood of the [regular observable family](REGULAR_OBSERVABLE_FAMILY.md).
No coefficient or new amplitude is selected.
Condition on
\[
 \Xi=\theta+360\mu_1-359\mu_0>1,\qquad
 \lambda_*=\Xi^{-1}\in(0,1),\qquad
 t=\lambda-\lambda_*,\qquad g=\frac{\theta c_0\Xi}{360}>0.
\]
For the original root record \(i=0,1\), use
\[
 D_i=\theta b_i>0,\quad H_i=\theta c_i>0,\quad
 F_i(\lambda)=1-\lambda(\theta+\mu_i)>\frac12,\quad
 \Delta=[D,H]<0,\quad \chi=[H,F]=-gt.
\]
The bracket is \([X,Y]=X_0Y_1-X_1Y_0\).
The constants are the fixed admitted ones:
\[
 (b_0,b_1)=(8077/8800,40303/44000),\quad
 (c_0,c_1)=(81/1100,3231/44000),\quad
 0<\theta<10^{-10},\quad0\le\mu_i<1/26.
\]
The needed coordinates of the accepted section \(v_{11}=1\) are
\[
 v_{10}=-\frac{[D,F]}{\lambda\Delta},\qquad
 v_4=\frac{2\chi v_{10}}{\lambda^2\theta\Delta},\qquad
 v_9=-\frac{2[D,F]v_{10}}{\lambda^2\theta\Delta}
     =\frac{2[D,F]^2}{\lambda^3\theta\Delta^2}.               \tag{1}
\]
All denominators are nonzero on the admitted interval. At the exception,
\[
 F(\lambda_*)=\kappa_*\lambda_*H,\quad
 \kappa_*=\frac{F_0(\lambda_*)}{\lambda_*H_0}>0,\quad
 v_{10}(\lambda_*)=-\kappa_*,\quad v_4(\lambda_*)=0.
\]
The fixed amplitude is \(\eta_*=(2\kappa_*)^{-1}>0\).
The regular-family theorem supplies a compact neighborhood \(\mathcal I_*\subset(0,1)\) of
\(\lambda_*\) on which all eleven multipliers
\(h_j=1+\eta_*v_j\) are at least \(1/4\), with
\[
             -\frac34\le\eta_*v_{10}(\lambda)\le-\frac14. \tag{2}
\]
The same amplitude and neighborhood apply in both root sectors. No numerical
radius is supplied, and the entire interval \(0<\lambda\le1\) is not claimed
as an admissible perturbation neighborhood.

Let \(\rho_\lambda>0\) be any admitted common six-parent scale for this
fixed changed prefix. The harmonic equations are unchanged by its choice.
Superscript \(H\), used in §5, means the specifically selected full-layer
half-scale rule. No regularity of an arbitrary \(\rho_\lambda\) is presumed.

## 2. All eight ideals and sixteen marked outcomes

Fix a full old marking of
\(P_4=C_4\oplus A_2\), whose root record is \(i\).
Write its chain as \(r_1<r_2<r_3<r_4\) and its two incomparable caps as
\(a,b\), both above \(r_4\). Let \(I=\{r_1,r_2,r_3\}\).
An outcome is \((S,\beta)\), where \(S\) is an individual precursor ideal
and \(\beta\in\{0,1\}\) is the fair newborn record. Denote baseline and
perturbed probabilities by \(p_i(S,\beta)\) and \(\widetilde p_i(S,\beta)\)
at the **same** \(\lambda\), parent and old marking.

The exact full-row inventory is:

| Precursor \(S\) | Ideal occurrences | Marked outcomes | Child | Width \(W\) | Signed change per ideal, both bits summed |
| --- | ---: | ---: | --- | ---: | --- |
| Chain prefix of length 0, 1 or 2 | 3 | 6 | Outside support | 3 | \(0\) each |
| \(I\), chain prefix of length 3 | 1 | 2 | \(T_4\) | 3 | \(A_i\) |
| Entire \(C_4\) | 1 | 2 | \(T_9\) | 3 | \(B_i\) |
| \(C_4\cup\{a\}\) or \(C_4\cup\{b\}\) | 2 | 4 | \(T_{10}\) | 2 | \(C_i\) each |
| Full \(P_4\) | 1 | 2 | Outside support | 2 | \(0\) |

Here \(C_i\) is a signed probability change, not a chain or a kernel pivot.
The three quantities are
\[
 \begin{split}
 A_i&=\eta_*\rho_\lambda\lambda^2\theta D_i v_4,\\
 B_i&=\eta_*\rho_\lambda\lambda^2\theta H_i v_9,\\
 C_i&=\eta_*\rho_\lambda F_i v_{10}.
 \end{split}                                                \tag{3}
\]
Each marked atom has **half** the tabulated ideal correction.
Unsupported outcomes have positive baseline probability and zero correction;
none is removed. The complete harmonic row gives
\[
                         A_i+B_i+2C_i=0.                    \tag{4}
\]
The factor two counts the two distinct \(T_{10}\) precursors.

The observation assumption is complete child-order access with the known
parent embedding, so \(S\) can be recovered as the old vertices below the
newborn. Width is
\[
 W=2+\mathbf1\{x\text{ is incomparable with both }a,b\}.
\]
The old marking is retained in the native object. Ignoring the newborn bit
does not lose distinguishing information for this pair: both laws assign
the same fair conditional bit distribution at every \(S\). Summing the
two half-corrections gives exactly the same total variation as retaining
all sixteen atoms. No conditioning on a selected event or root mixture
is used. Statements for \(i=0,1\) hold separately for all admitted
transported old markings.

## 3. Exact total variation and maximizing events

Define full-row total variation by
\[
 \operatorname{TV}_i
 =\frac12\sum_{S,\beta}
       |\widetilde p_i(S,\beta)-p_i(S,\beta)|
 =\sup_E|\widetilde p_i(E)-p_i(E)|.
\]
A zero-sum signed row has total variation equal to its total positive
mass. A positive maximizing event includes every positive atom, excludes
every negative atom, and may include any zero-correction atom. Its
complement maximizes the absolute difference with the opposite sign.

On \(\mathcal I_*\), (1)–(2) imply
\[
 B_i>0,\qquad C_i<0,\qquad
 \operatorname{sgn}A_i=\operatorname{sgn}\chi=-\operatorname{sgn}t.
                                                               \tag{5}
\]
For \(B_i\), the square in (1) is nonzero because \(v_{10}<0\).
For \(A_i\), both \(v_{10}\) and \(\Delta\) are negative.

The width-three event has contrast
\[
 \delta_i:=\widetilde p_i(W=3)-p_i(W=3)
          =A_i+B_i=-2C_i>0.                                  \tag{6}
\]
Since \(W\) only takes values two and three, this is also the expected-width
contrast and the total variation between the two width distributions.
Accounting for both bits and both \(T_{10}\) ideals,
\[
 \boxed{\quad
 \operatorname{TV}_i
 =\frac12(|A_i|+B_i+2|C_i|)
 =\delta_i+(-A_i)_+,\qquad
 L_i:=\operatorname{TV}_i-\delta_i=(-A_i)_+.
 \quad}                                                       \tag{7}
\]

Write \(E_4=\{(I,0),(I,1)\}\),
\(E_9=\{(C_4,0),(C_4,1)\}\), and let \(E_{10}\) contain both bits
of both single-cap ideals. The maximizers and loss are:

| Parameter position | Positive maximizing event, up to zero-correction atoms | Full-row TV | Width TV-loss \(L_i\) |
| --- | --- | --- | --- |
| \(\lambda<\lambda_*\), in \(\mathcal I_*\) | \(E_4\cup E_9\) | \(A_i+B_i=\delta_i\) | \(0\) |
| \(\lambda=\lambda_*\) | \(E_9\) | \(B_i=\delta_i=\rho_{\lambda_*}F_i(\lambda_*)\) | \(0\) |
| \(\lambda>\lambda_*\), in \(\mathcal I_*\) | \(E_9\) | \(B_i=\delta_i-A_i\) | \(-A_i>0\) |

The signs and these maximizing events are the same in both root sectors;
no separate choice of amplitude or event by root is needed.
On the left, \(W=3\) is a maximizing event because it adds only
zero-correction prefixes to \(E_4\cup E_9\). At the exception, \(E_4\)
also has zero correction, so \(W=3\) still maximizes.
On the right, \(W=3\) wrongly includes the negative \(E_4\) correction.

The right-hand maximizing event \(S=C_4\) is determined by the assumed
complete order and embedding: the newborn is above \(r_4\) and incomparable
with both caps, so its old ancestors are exactly the four chain vertices.
This refines width by the newborn's relation to \(r_4\).
Reporting any such event as a binary statistic maps every outcome to
zero or one; it does not filter or renormalize a selected subset.
No physical measurement implementation is supplied.

## 4. Exact loss formula and local order without scale regularity

Combining (1), (3) and \(\chi=-gt\), define
\[
 k_i(\lambda)=\frac{2\eta_*D_i g\,v_{10}(\lambda)}{\Delta}>0,\qquad
 k_i^*:=k_i(\lambda_*)=\frac{D_i g}{|\Delta|}>0.
\]
The exact loss on the entire admitted neighborhood is
\[
 \boxed{\qquad
 L_i(\lambda)=\rho_\lambda k_i(\lambda)t_+,\qquad
 \frac{L_i(\lambda)}{\rho_\lambda}=k_i(\lambda)t_+ .
 \qquad}                                                       \tag{8}
\]
Here \(t_+=\max\{t,0\}\). The coefficient \(k_i\) is a smooth rational
function near the exception, using only nonzero \(\lambda,\Delta\).
For \(t\downarrow0\) from the right,
\[
 \frac{L_i(\lambda_*+t)}{\rho_{\lambda_*+t}}
       =\frac{D_i g}{|\Delta|}\,t+O(t^2).                     \tag{9}
\]
Thus normalized loss is exactly zero on the left and has positive
first-order right-hand behavior in both root sectors, without any
assumption on the scale.

The same distinction is visible without dividing by a possibly irregular
scale. Relative to the positive width contrast,
\[
 \frac{L_i}{\delta_i}
   =\beta_i(\lambda)t_+,\qquad
 \beta_i(\lambda)=\frac{D_i g}{|\Delta|F_i(\lambda)}>0,\qquad
 \frac{L_i}{\operatorname{TV}_i}
   =\frac{\beta_i(\lambda)t_+}{1+\beta_i(\lambda)t_+}.           \tag{10}
\]
Both ratios are independent of \(\rho_\lambda\), zero on the left and
first order on the right. These are specified total-variation losses,
not a claim about every information measure or every statistical decision.

For arbitrary admitted common scales, the two individual \(T_{10}\)
baseline probabilities are each \(\rho_\lambda F_i\). Every other ideal
also has positive probability, so full-row normalization forces
\[
                  2\rho_\lambda F_i<1,\qquad \rho_\lambda<1.
\]
Since \(k_i\) is bounded on a compact neighborhood, (8) yields the
absolute upper bound \(L_i=O(t_+)\), and \(L_i\to0\) at the exception
even when the scale is discontinuous. This does not make the full-row TV
or the width contrast continuous; both can inherit scale discontinuities.
Nor does it force a nonzero first-order absolute coefficient or a
first-order lower bound.

For example, the admitted alternative from the [baseline-scale theorem](BASELINE_SCALE_THEOREM.md) uses
\(\rho^{\rm bad}_\lambda=|t|\rho^H_\lambda\) when \(t\ne0\), with
\(\rho^{\rm bad}_{\lambda_*}=\rho^H_{\lambda_*}>0\).
Every fixed-parameter law remains admissible. On the right its loss is
\(t\) times the half-scale loss, hence second order rather than first order.
This is an optional-scale counterexample, not the selected half-scale law.

## 5. Absolute first-order loss under the full-layer half-scale rule

For the explicitly selected construction,
\[
 \rho^H_\lambda=\frac1{2(1+\mathcal M_6(\lambda))},
\]
where \(\mathcal M_6\) is the maximum of the complete proper-potential sums
over **all** marked six-parents and all individual ideal occurrences.
The independently reviewed [baseline-scale theorem](BASELINE_SCALE_THEOREM.md)
proves its positive continuity and a uniform positive lower bound on the admitted neighborhood.

It also proves that each six-parent deletion potential is a polynomial
in \(\lambda\), because its reciprocal factors use only fixed smaller
prefix probabilities. Thus each complete row sum is a polynomial, and
their finite maximum is locally Lipschitz: on a compact neighborhood,
bound all polynomial derivatives and apply the maximum inequality.
Composing with \(x\mapsto1/[2(1+x)]\), whose derivative is bounded for
\(x\ge0\), shows that \(\rho^H\) is locally Lipschitz.
No unique maximizing row or differentiability at a switch is needed.

Therefore (8) sharpens, for \(t\downarrow0\), to
\[
 \boxed{\quad
 L_i^H(\lambda_*+t)
  =\rho^H_{\lambda_*}\frac{D_i g}{|\Delta|}\,t+O(t^2),
 \qquad L_i^H(\lambda)=0\ \text{for }\lambda\le\lambda_*
                       \text{ in }\mathcal I_* .
 \quad}                                                       \tag{11}
\]
The right-hand coefficient is strictly positive in both sectors. Hence
the absolute loss is \(\Theta(t)\) on the right for this rule (bounded
above and below by positive coefficient-dependent multiples of \(t\)
on a sufficiently small right neighborhood). No numerical constants,
radius or effect size have been evaluated.

At the exception the complete two-sector TV vector is exactly
\[
 (\operatorname{TV}_0,\operatorname{TV}_1)
   =\rho^H_{\lambda_*}\bigl(F_0(\lambda_*),F_1(\lambda_*)\bigr),
\]
and the width distribution has the same TV in each sector.
On the right the complete row has strictly greater TV, while width still
has the previously proved positive absolute contrast. The distinction
between retaining a nonzero signal and retaining all of its TV
distinguishing power is essential.

## 6. TV-optimality is weaker than full statistical sufficiency

For this two-law family, statistical sufficiency of the deterministic
statistic \(W\) would require the conditional distribution of the complete
outcome given \(W\) to be the same under baseline and perturbation.
Since every atom has positive baseline probability, that requires their
likelihood ratio to be constant within each width fiber.

But the likelihood ratio is
\[
 \frac{\widetilde p_i(S,\beta)}{p_i(S,\beta)}
       =h_7(P_4+S)=1+\eta_*v_{[P_4+S]},
\]
with multiplier one outside support. Within \(W=3\), the three short
chain-prefix ideals have ratio one, whereas \(T_9\) has ratio
\(1+\eta_*v_9>1\). Within \(W=2\), the full ideal has ratio one,
whereas each \(T_{10}\) ideal has ratio \(1+\eta_*v_{10}<1\).
All these atoms are present with positive probability throughout
\(\mathcal I_*\), including at \(\lambda_*\).

Thus width is **not** a sufficient statistic for the complete pair at
any parameter in this neighborhood. On the left and at the exception
it nevertheless attains the maximal TV difference because no width
fiber mixes positive and negative corrections. On the right the
width-three fiber does mix them, producing the precise loss (7)–(11).
No claim of zero general information loss is inferred from zero TV loss,
and no separate divergence or decision-theory program is opened.

## Public premises and evidence scope

The [regular observable family](REGULAR_OBSERVABLE_FAMILY.md) supplies the
eleven-coordinate section, fixed amplitude, positivity neighborhood and
complete \(P_4\) inventory. The [baseline-scale theorem](BASELINE_SCALE_THEOREM.md)
supplies the specifically selected scale's continuity, lower bound and
polynomial-potential property. The [theorem package](THEOREM_PACKAGE.md) and
[law-family supplement](LAW_FAMILY_SUPPLEMENT.md) state the admitted finite
law, support and changed-prefix construction.

The complete marked-row reduction, positive prefix, regular section,
fixed-amplitude neighborhood and the ratio-component/common-scale
construction remain inherited premises. The half-scale regularity and
polynomial-potential statements are used only when explicitly stated.
Actual occurrence of the exception remains conditional on \(\Xi>1\).

The printed comparisons concern the complete pair of one-birth laws at the
same parameter, parent and old marking. Equality of total variation after
taking width does not assert statistical sufficiency or preservation of
every information measure. Complete child-order access and the parent
embedding remain mathematical observation assumptions. Reporting a binary
maximizing event retains every outcome; it is not event filtering.

These are conditional manual finite statements, not numerical coefficient
acquisition, simulation, benchmark or sampler results. No numerical effect
or neighborhood radius, physical detector, quantum-dynamics derivation,
geometry/gravity claim, h8/30/33/38 transfer or all-size result is supplied.
The application protocols, historical custody failures, production status
and RET pause are unchanged. See the [publication note](PUBLICATION_NOTE.md)
and [public evidence policy](../../coordination/REDACTED_PUBLICATION.md).

## Child shape without a supplied parent embedding

The [child-shape manuscript](P4_CHILD_SHAPE_OBSERVATION.md) proves that the
complete unlabelled, unmarked child shape is sufficient and preserves full-row
TV for this conditional fixed pair. It removes the supplied parent embedding
and newborn identity, while retaining exact complete-order access. Its
coarsest sufficient partition has four blocks locally off the exception and
three at it; §5 distinguishes equal and unequal input mixtures and their
benchmarks. No physical observation channel is supplied.
