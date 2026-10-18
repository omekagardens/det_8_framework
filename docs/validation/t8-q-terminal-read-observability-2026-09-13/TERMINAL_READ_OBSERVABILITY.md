# RI-08i — minimal terminal internal-read observability

13 September 2026. **CONDITIONAL_BACKWARD_EFFECT_SPAN_CLASSIFICATION;
MINIMAL_MASS_RETAINING_LINEAR_PREDICTIVE_DIMENSIONS;
EXACT_THREE_SETTING_STATE_RECONSTRUCTION.**
One explicitly calibrated available terminal read closes the state
observation gap for the specified known commands. Its calibration and
availability are additional premises, not a DET-derived readout law.
No postmeasurement instrument, unknown Hamiltonian or physical time is
identified.

## 1. Retained native object and known command catalogue

Use the enlarged return cone L_t of
[RI-08g](../t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md),
and the declared common-X commands of
[RI-08h](../t8-q-reversible-generator-2026-09-13/REVERSIBLE_GENERATOR.md).
The theorem allows any fixed known \(|t|<1\). The executable fixture
fixes \(t=3/5\); it does not implement all interior parameters.

For completeness, the native labels are \((a,i,b,j)\), with index
\(8a+4i+2b+j\). The fixed signed permutation and image map are
\[
P_{8a+4b+2i+j,\;8a+4i+2b+j}=(-1)^{ai+bj},\qquad
B_t=(I+tZ)/4,\qquad U=(I\otimes H_{\rm Had}){\rm CNOT},
\]
\[
M_t(\rho)=U((\rho^T/2)\otimes B_t)U^\dagger,\quad
\mathcal I_t((\rho_\alpha))
=P^\dagger\operatorname{diag}(M_t(\rho_{00}),M_t(\rho_{01}),
M_t(\rho_{10}),M_t(\rho_{11}))P,
\]
\[
L_t=\{\mathcal I_t((\rho_\alpha)):\rho_\alpha\succeq0
\text{ independently}\},\qquad \alpha=(a,b).
\]
Its actual real span has dimension sixteen. The reference, frame,
composition and coupler are retained supplied structure, not new native
DET derivations. Complex transpose conventions, all sixteen native labels,
and every entry of the 16×16 kernel remain explicit.

For each cell let
\[
E_{ab}=(I+(-1)^btZ)/4,\qquad
\sigma_\alpha=E_\alpha^{1/2}\rho_\alpha E_\alpha^{1/2}
=\tfrac12(q_\alpha I+x_\alpha X+y_\alpha Y+z_\alpha Z).
\]
Here \(q_\alpha=\operatorname{Tr}\sigma_\alpha\),
\[
m=\sum_\alpha q_\alpha,\qquad
\tau=\operatorname{Tr}N=\tfrac14\sum_\alpha\operatorname{Tr}\rho_\alpha,
\qquad
\sigma_\alpha\succeq0
\Longleftrightarrow q_\alpha\ge\sqrt{x_\alpha^2+y_\alpha^2+z_\alpha^2}.
\]
Native normalization uses m, not generally raw trace \(\tau\), and m
does not mean physical rest mass. Interior filtering is invertible.

The named commands use
\[
U_A=\tfrac35 I-\tfrac45 iX,\qquad
U_B=\tfrac5{13}I-\tfrac{12}{13}iX,
\]
their named product AB and named inverses. On every block they act by
\(\sigma\mapsto U_w\sigma U_w^\dagger\), equivalently the accepted
weighted congruence on \(\rho\). Words retain their actual ordered
nominal labels. They are group elements, not additive clock readings.
Literal cuts keep just one full cell and remain available on L_t.

## 2. Exactly one new terminal observation premise

For a fixed known unit vector n define
\[
Q_{n,\pm}=\tfrac12(I\pm n\cdot(X,Y,Z)),\qquad
\boxed{p_{\alpha,\pm}
=\operatorname{Tr}(Q_{n,\pm}\sigma_\alpha)
=\tfrac12(q_\alpha\pm n\cdot r_\alpha)},
\quad r_\alpha=(x_\alpha,y_\alpha,z_\alpha).
\]
**Added premise:** this read is available and exactly calibrated to the
boxed effects. Positivity alone does not supply that availability or
calibration. In particular the displayed probability law is not derived
from DET here.

This is a binary **internal** read with the actual cell retained, hence
eight full outcomes \((a,b,\pm)\), not a global binary read that erases
a and b. Every weight is nonnegative and
\(\sum_{\alpha,\pm}p_{\alpha,\pm}=m\). The effects on \(\rho_\alpha\)
are \(E_\alpha^{1/2}Q_{n,\pm}E_\alpha^{1/2}\), between 0 and E_alpha.
This proves mathematical positivity/completeness of the proposed read,
not its physical availability.

The executable admits exactly the one tilted read
\[
n=(3/5,0,4/5),\qquad
Q_+=\tfrac1{10}\begin{pmatrix}9&3\\3&1\end{pmatrix},\qquad Q_-=I-Q_+ .
\]
Z and X below classify alternative mathematical catalogues and provide
counterexamples. They are not extra primary available reads in this
fixture. Neither an arbitrary extra control nor another measurement
family is added.

Commands, literal cuts and finite stopping may precede at most one
terminal read. No operation follows that read. Effect calibration
specifies probabilities, not a state-update map.

## 3. Backward effect span

Let \(v_w\) be the axis defined by
\(U_w^\dagger(n\cdot{\rm Pauli})U_w=v_w\cdot{\rm Pauli}\).
The backward effects on a source block are
\((q_\alpha\pm v_w\cdot r_\alpha)/2\).
Every common-X word fixes the X line and rotates the YZ plane.
For one A, the backward-axis rule is
\[
(v_x,v_y,v_z)\longmapsto
(v_x,Cv_y+Sv_z,-Sv_y+Cv_z),\qquad C=-7/25,\quad S=24/25.
\]
Therefore the span of all available axes is contained in the X line
when \(n_x\ne0\), together with the YZ plane when
\(n_\perp=(n_y,n_z)\ne0\), with absent components omitted.

These bounds are attained using A alone. If \(n_x=0\), axes n and
its A image span the YZ plane since S is nonzero. If \(n_\perp=0\),
the X line alone is obtained. If both components are nonzero, rotate
the transverse coordinate basis so n becomes \((n_x,0,\|n_\perp\|)\).
This coordinate calculation does not add an available control. The
three axes for empty word, A and AA have row determinant
\[
2n_x\|n_\perp\|^2S(C-1)\ne0.
\]
Thus they span all three Bloch directions. B and other finite words
cannot enlarge the already specified invariant space.

**Effect-span theorem.** Per cell, the homogeneous real-linear span of
all backward effects, including cut weights, has rank
\[
\boxed{1+\mathbf1_{\{n_x\ne0\}}+
2\mathbf1_{\{n_\perp\ne0\}}.}
\]
The extra 1 is q, obtained by adding the two internal outcomes.
Because the four cell blocks are independent and full cell outcomes
are resolved, their effect spaces form a direct sum.

| Fixed read axis | Per-cell summary | Full-span rank | Normalized affine dimension |
| --- | --- | ---: | ---: |
| Z, or any axis wholly in YZ | (q,y,z) | 12 | 11 |
| X or minus X | (q,x) | 8 | 7 |
| Both X and transverse components | (q,x,y,z) | 16 | 15 |

This is a theorem on the full native span via the invertible map
\(\mathcal I_t\) and faithful filtering, not a finite sample rank claim
or replacement of the native state by a chosen matrix quotient.

## 4. Exact finite-experiment equivalence and positive quotients

Fix the same known context/read calibration, full earlier committed
prefix, initial pending word and retained nominal-command metadata.
Policies may inspect those retained labels and outcomes, not the unknown
raw kernel. Keeping a raw source for audit does not add a physical
observation of its entries. Stop retains the payload and pending word
but is not an oracle reading them.

**Finite-experiment theorem.** Two normalized L_t sources have equal
conditional future outcome laws for every allowed finite common
command/cut/stop policy, with at most one terminal read, iff their
summaries in the table agree.

**Sufficiency.** Commands descend to X-fixed/YZ-rotation maps on the
appropriate summary. Literal cuts descend to coordinate block
projections, with weights determined by q. Positive selected cuts
normalize by those same weights. Terminal effects depend only on the
summary. Induction over the finite retained-history tree therefore
gives the same branch probabilities and observed nominal histories,
including stopping. This does not infer a postterminal state.

**Necessity and separating experiments.** A difference in q is detected
by an immediate full cut or a terminal outcome sum. If q agrees but a
retained Bloch coordinate differs, one of the spanning axes above has
nonzero dot product with that difference. Performing its finite A word
and then the terminal read gives different full outcome probabilities.
This is an explicit finite separator: for a YZ-axis read, empty/A
suffice; for an X-axis read, empty suffices; for the tilted read,
empty/A/AA suffice.

Equality is conditional on identical initial metadata and the same
retained nominal policy. For example A followed by B and a single AB
can give equal raw outputs while their pending words and subsequent
records differ. Their known labels are never merged. A policy
conditioned on unequal initial pending words can choose different
stop/read actions even for equal raw states.

On the full unnormalized cone, replace conditional laws by
outcome-weight measures including total mass. The same summaries
characterize equivalence. Their positive images and sections are:

- Z: four copies of \(q\ge\sqrt{y^2+z^2}\), with section
  \(\sigma=(qI+yY+zZ)/2\), setting x=0;
- X: four copies of \(q\ge|x|\), with section
  \(\sigma=(qI+xX)/2\), setting y=z=0;
- tilted: the full product \(q\ge\sqrt{x^2+y^2+z^2}\), with its
  exact inverse rather than a discarded direction.

Necessity of each inequality follows from positivity of sigma;
sufficiency follows from the displayed positive section. Pull back
by \(E^{-1/2}\) and \(\mathcal I_t\) to obtain positive real-linear
sections in native coordinates. They retain mass and commute with the
declared commands and cuts in the respective summary coordinates.
These are closed pointed generating cones with faithful mass and
compact normalized bases. The existence of a section is not an
available physical reset or preparation, and no original residual
or known preparation selector is erased.

**Minimality convention.** Ranks 12/8/16 are the attained minimum for
homogeneous, mass-retaining real-linear predictive summaries on the
full unnormalized native span. Any such summary has kernel contained
in the common kernel of the available backward effects. To see this
even if prediction is not postulated linear in the summary, perturb
an interior positive source by a sufficiently small signed kernel
direction; equal summaries must give equal effect weights. Thus the
summary rank is at least the effect-span rank, and the displayed
summaries attain it. On the normalized mass-one affine slice the
dimensions are 11/7/15; one known mass coordinate can be omitted
there. No nonlinear encoding bound, physical preparation-richness
claim or minimum over a smaller available preparation set is inferred.

## 5. Hidden direction and a failed additional-control criterion

In one cell set \(\sigma=Q_{X+}\) or \(Q_{X-}\), all other blocks zero,
where \(Q_{X\pm}=(I\pm X)/2\). Both native sources have mass one after
pullback by the faithful filter. They have the same q,y,z but different
x. Every common-X word fixes them. Every Z terminal read and all finite
preceding cuts/stops therefore give the same outcome law under a common
metadata policy, despite distinct full raw kernels.

For the specified tilted read their plus weights instead are
\[
p_+(Q_{X+})=4/5,\qquad p_+(Q_{X-})=1/5 .
\]
These are full outcome weights in the occupied cell; no cell-weight
division is used. The states are mathematical witnesses, not established
available preparations.

The criterion “add any nonparallel control” is insufficient to repair
Z-read blindness. Conjugation by a pi Z rotation maps
\((x,y,z)\mapsto(-x,-y,z)\). Along with every X rotation it still
preserves the X line and YZ observation plane. Every word of this
enlarged diagnostic control group keeps backward Z axes in YZ, so
the same missing X directions survive. This is an all-word invariant
subspace counterexample, not merely one unsuccessful control sample.
No extra control is needed for the primary tilted read.

## 6. Exact three-setting reconstruction

For the tilted read use the three distinct resolved command settings
empty, A and AA. Their backward axes are
\[
v_0=(3/5,0,4/5),\quad
v_1=(3/5,96/125,-28/125),\quad
v_2=(3/5,-1344/3125,-2108/3125),
\]
\[
\det\begin{pmatrix}v_0\\v_1\\v_2\end{pmatrix}
=-73728/78125 .
\]
Each table supplies all eight full outcome weights for the same
normalized source snapshot under its known word. It is not a table
of probabilities conditioned on an already selected cell.
For each cell define
\[
q_\alpha=p^{(k)}_{\alpha,+}+p^{(k)}_{\alpha,-},\qquad
d_k=p^{(k)}_{\alpha,+}-p^{(k)}_{\alpha,-}=v_k\cdot r_\alpha.
\]
The q values must agree across the three settings. Direct inversion gives
\[
\boxed{
x=\frac{125d_0+70d_1+125d_2}{192},\quad
y=\frac{-55d_0+180d_1-125d_2}{192},\quad
z=\frac{195d_0-70d_1-125d_2}{256}.}
\]
Recover sigma from q,x,y,z. At the executable \(t=3/5\),
\[
D_0=\operatorname{diag}(2,1),\quad D_1=\operatorname{diag}(1,2),
\quad E_{ab}=D_b^2/10,\qquad
\boxed{\rho_\alpha=10D_b^{-1}\sigma_\alpha D_b^{-1}} .
\]
Finally apply the full native \(\mathcal I_{3/5}\), reproducing every
native entry, not just diagonal weights or a real-amplitude truncation.

**Exact table-consistency theorem.** A real three-setting table is
produced by exactly one normalized source in L_t iff it has shared
per-cell q, \(\sum_\alpha q_\alpha=1\), and for each cell
\[
q_\alpha\ge0,\qquad
q_\alpha^2\ge x_\alpha^2+y_\alpha^2+z_\alpha^2
\]
for the displayed reconstructed coordinates.
Necessity follows from filtering a positive normalized source.
Conversely these inequalities make the reconstructed sigma blocks
positive; inverse filtering gives a positive native source of mass one,
and the inverse-axis identities reproduce every supplied table entry.
They also imply nonnegative supplied weights since the backward axes
are unit vectors. Implementations may reject negative entries earlier.
Uniqueness follows from the nonzero determinant and native inverse.

If q=0 the inequalities force x=y=z=0, and the whole block is zero.
There is no division by q and no zero-cell conditional state to invent.
Failure of the exact compatibility conditions is a rejected model
table, not an instruction to project, renormalize, clip or fit it.
This is exact mathematical model consistency, not a statistical
goodness-of-fit rule for empirical frequencies.

**Three-setting minimum.** With q known, k resolved settings of this
fixed binary internal read contribute at most k Bloch linear
functionals per cell. For k<3 there is a nonzero direction orthogonal
to all those axes; sufficiently small opposite perturbations about
a positive interior block give distinct states with the same table.
Cuts add only q and cannot remove this ambiguity. Therefore three
resolved settings are necessary for full-state observability on the
whole mathematical domain, and the displayed settings attain it.
Randomized settings with their selectors resolved count as those
distinct settings, not one; forgetting a selector cannot add an
independent axis. Adaptive cut branches do not evade the count of
the actual terminal settings resolved in each cell.

## 7. Strictly terminal typed response and probability scope

The [model](model.py) separates source states, prior literal-cut records
and the new terminal response. Selecting a positive terminal outcome
may retain the exact **pre-read** source, full context/calibration,
all preceding records, ordered pending word, declared effect and actual
\((a,b,\pm)\) record. It does not manufacture a separate cell commitment
unless a preceding literal cut actually occurred.

The response leaves the postmeasurement residual unspecified.
The retained pre-read kernel is neither renamed nor normalized as a
postmeasurement state. Commands, cuts, another read or reset on the
terminal response are refused. A zero-weight outcome cannot be selected
and leaves the immutable source unchanged. Raw effect inspection may
still return its zero weight.

Every reported probability is conditional on the explicitly supplied
normalized snapshot and the declared preceding procedure. Its earlier
local/reference preparation or history-selection probabilities are not
recovered from stored provenance. Known record labels and source entries
are retained without making the latter an available policy oracle.
Exact reconstruction returns a mathematical source kernel, not a
postterminal continuation or an available preparation.

## 8. Witness scope, endpoint boundary and stop

The independent [checks](check.py) use exact Gaussian-rational arithmetic,
native-index reconstruction, signed-span/effect-rank certificates,
positive sections, separators and typed negative tests. Finite witnesses
check the written formulas and contracts; the all-finite equivalence
and minimality claims are proved above, not inferred by enumeration.

At \(|t|=1\) filtering is not invertible. The endpoint effect obstruction
in RI-08g still applies: all whole-cone mass-dominated effects factor
through four cell weights. No inverse filter, full native observability
or interior section is extended through singular mass by a limiting
argument. The runtime refuses endpoint primary sources.

Reproduction from the repository root:

~~~sh
.venv/bin/python -B docs/validation/t8-q-terminal-read-observability-2026-09-13/check.py
.venv/bin/python -B -O docs/validation/t8-q-terminal-read-observability-2026-09-13/check.py
~~~

The yield is conditional state observability and exact consistency under
known calibrated commands/read probabilities. It is not identification
of an unknown Hamiltonian/generator, physical time, empirical independence,
repeated-preparation availability, finite-sample tomography accuracy,
a reusable instrument, full QM, native geometry, rest mass or gravity.
The earlier reversible-law and domain premises remain unproved from DET.
Accepted sources and other lanes remain unchanged. This bounded result
is submitted for independent acceptance; no successor is opened here.
