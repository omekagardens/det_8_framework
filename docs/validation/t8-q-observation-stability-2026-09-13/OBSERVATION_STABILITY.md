# RI-08j — observation stability and deterministic error budgets

13 September 2026. **SHARP_FILTERED_OBSERVATION_STABILITY;
SINGULAR_AND_RARE_CELL_BOUNDARIES;
EXACT_SUPPLIED_CANDIDATE_BUDGET_CERTIFICATE.**
This capstone gives conditional mathematical bounds for the accepted
finite cone and calibrated read. It does not infer confidence levels,
calibration, preparation availability or a physical law.

## 1. Fixed setting, two distances and probability scope

Retain the interior L_t, native map \(\mathcal I_t\), known common-X
commands and sole calibrated tilted terminal read of
[RI-08i](../t8-q-terminal-read-observability-2026-09-13/TERMINAL_READ_OBSERVABILITY.md).
For each cell \(\alpha=(a,b)\),
\[
N=\mathcal I_t((\rho_\alpha)),\quad
E_{ab}=(I+(-1)^btZ)/4,\quad |t|<1,\quad
\sigma_\alpha=E_\alpha^{1/2}\rho_\alpha E_\alpha^{1/2}
=\tfrac12(q_\alpha I+r_\alpha\cdot{\rm Pauli}).
\]
The four blocks are independently positive and normalized by
\(m(N)=\sum_\alpha q_\alpha=1\), not by the ordinary native trace.
All sixteen native labels and every entry of the 16-by-16 kernel are
retained. The reference, frame and existing command/read premises
are unchanged. No additional primary control or read is introduced.

Compare normalized compatible sources N,N' in the same known context,
full earlier prefix, initial pending word and nominal metadata. Let
\[
w_0=(),\quad w_1=(A),\quad w_2=(A,A),\qquad
p_k=(p_{\alpha,\pm}^{(k)})_{\alpha,\pm},\quad
\epsilon_k={\rm TV}(p_k,p'_k)=\tfrac12\sum_{\alpha,\pm}
|p_{\alpha,\pm}^{(k)}-p_{\alpha,\pm}^{\prime(k)}|.
\]
These are full eight-outcome laws conditional on the supplied normalized
snapshot, not probabilities renormalized within a cell. Each word is an
additional resolved setting on that snapshot. Its prior pending word
remains retained; labels are never merged because matrices coincide.
Neither stored preparation history nor these mathematical setting tables
supplies unknown earlier selection probabilities or repeated preparation.

Define
\[
\boxed{d_F(N,N')=\tfrac12\sum_\alpha
\|\sigma_\alpha-\sigma'_\alpha\|_1},\qquad
\boxed{d_N(N,N')=\tfrac12\|N-N'\|_1}.
\]
The filtered direct sum has trace one, so \(0\le d_F\le1\).
Raw kernels are generally not trace-one states: d_N is not a probability
distance and need not be bounded by one.

The general proofs below allow fixed interior t. The primary exact
implementation remains restricted to \(t=3/5\) and the accepted tilt
\(n=(3/5,0,4/5)\). Other axes/polarizations are mathematical diagnostics,
not newly available operations.

## 2. Sharp filtered observation bound

Let V have the three backward axes as rows:
\[
V=\begin{pmatrix}
3/5&0&4/5\\
3/5&96/125&-28/125\\
3/5&-1344/3125&-2108/3125
\end{pmatrix},\qquad B=V^{-1},\quad
b_k=\|B_{\cdot k}\|_2,\quad C=\sum_{k=0}^2b_k .
\]
RI-08i establishes the exact inverse and the full native reconstruction.
Here the inverse controls errors, not just uniqueness.

For one Hermitian difference
\(\Delta\sigma=(\delta q I+\delta r\cdot{\rm Pauli})/2\),
the eigenvalues are \((\delta q\pm\|\delta r\|_2)/2\). Hence
\[
\boxed{\|\Delta\sigma\|_1=\max(|\delta q|,\|\delta r\|_2)}.
\]
Since \(\delta p_\pm=(\delta q\pm v_k\cdot\delta r)/2\), similarly
\[
\boxed{\epsilon_k=\tfrac12\sum_\alpha
\max(|\delta q_\alpha|,|v_k\cdot\delta r_\alpha|)}.
\]
The factors of one half refer to TV/distance, not to the trace norms
in these block identities.

**Stability theorem.**
\[
\boxed{\max_k\epsilon_k\ \le\ d_F\
\le\sum_k b_k\epsilon_k\
\le C\max_k\epsilon_k.}
\]

**Proof.** Every \(v_k\) is a unit vector, so its scalar product with
\(\delta r\) is bounded by \(\|\delta r\|_2\), proving the first bound.
Write \(\delta d_k=v_k\cdot\delta r\) and
\(\delta r=\sum_k B_{\cdot k}\delta d_k\). Then
\(\|\delta r\|_2\le\sum_kb_k|\delta d_k|\).
Moreover \(v_k\cdot B_{\cdot k}=1\), so \(b_k\ge1\) by
Cauchy–Schwarz. Therefore, cell by cell,
\[
\max(|\delta q|,\|\delta r\|_2)
\le\sum_k b_k\max(|\delta q|,|\delta d_k|).
\]
Summing and dividing by two proves the middle bound; the last is
immediate. One may cap a valid d_F upper bound by one, but the local
sharp constants below are unchanged. ∎

**Sharpness on the full mathematical domain.** Assign three distinct
cells to k=0,1,2 and give every cell q=1/4 in both sources. In cell k
choose opposite Bloch vectors
\[
r_k=+\epsilon_k B_{\cdot k},\qquad
r'_k=-\epsilon_k B_{\cdot k},
\]
and leave the fourth cell at the same center. For sufficiently small
nonnegative \(\epsilon_k\), specifically \(\epsilon_kb_k\le1/4\),
both sources are positive and normalized. Their differences obey
\(v_j\cdot\delta r_k=2\epsilon_k\delta_{jk}\), so the three actual
TV errors are exactly the prescribed \(\epsilon_j\) and
\[
d_F=\sum_kb_k\epsilon_k .
\]
This proves sharpness of each weighted coefficient; equal small
positive errors prove sharpness of C. To attain the lower coefficient
one, keep all Bloch vectors zero and transfer a small amount of center
mass between two cells in the two sources. All three TV errors then
equal d_F. These witnesses establish mathematical attainability,
not available preparation procedures.

## 3. Coefficients, axis conditioning and certified enclosures

At the accepted tilt the inverse columns, in units of 1/768, are
\[
(500,-220,585),\quad(280,720,-210),\quad(500,-500,-375).
\]
Consequently
\[
b_0=b_2=\frac{125\sqrt{41}}{768},\qquad
b_1=\frac{5\sqrt{6409}}{384},\qquad
C\approx3.126749168936497 .
\]
The decimal is explanatory only, never a certified upper bound.

For a general unit axis with
\(a=|n_x|>0,\ b=\|n_\perp\|>0,\ a^2+b^2=1\),
rotate transverse coordinates for calculation so the axis is (a,0,b).
This is a change of coordinates, not an extra available control.
The inverse has rows
\[
\left(\frac{25}{64a},\frac7{32a},\frac{25}{64a}\right),\quad
\left(-\frac{11}{48b},\frac3{4b},-\frac{25}{48b}\right),\quad
\left(\frac{39}{64b},-\frac7{32b},-\frac{25}{64b}\right).
\]
Sign changes in n_x and transverse frame rotations do not change
column norms. Thus
\[
b_0=b_2=\frac{25}{192}
\sqrt{\frac9{a^2}+\frac{25}{b^2}},\quad
b_1=\frac1{32}\sqrt{\frac{49}{a^2}+\frac{625}{b^2}},
\]
\[
\boxed{C(a,b)=\frac{25}{96}
\sqrt{\frac9{a^2}+\frac{25}{b^2}}
+\frac1{32}\sqrt{\frac{49}{a^2}+\frac{625}{b^2}}.}
\]
Taking limits along the unit circle gives
\[
\lim_{a\to0}aC=1,\qquad
\lim_{b\to0}bC=25/12 .
\]
For instance, multiplying the first expression by a makes its two
radicals tend to 3 and 7, yielding \(75/96+7/32=1\).
Multiplying by b gives \(125/96+25/32=25/12\).
Interior full rank is therefore compatible with arbitrarily poor
conditioning. At a=0 or b=0 the inverse ceases to exist and RI-08i's
exact rank-loss theorems apply. An inverse determinant alone would not
establish these directional norm bounds.

The exact fixture uses rational upper enclosures, proved by squaring:
\[
\sqrt{41}\le\frac{640313}{100000},\qquad
\sqrt{6409}\le\frac{1000703}{12500}.
\]
The positive square gaps are respectively
\(737969/10^{10}\) and \(244209/156250000\).
Thus certified coefficients may be taken as
\[
\widehat b_0=\widehat b_2=\frac{640313}{614400},\qquad
\widehat b_1=\frac{1000703}{960000},\qquad
\sum_k\widehat b_k=\frac{24013449}{7680000}.
\]
The fixture validates exact inequalities, not rounded decimals.
Sharpness belongs to the radical b values; their slightly larger
rational enclosures are safe executable bounds, not sharp constants.

## 4. Native norm and the singular polarization boundary

For each native image block,
\[
M_t(\Delta\rho)=U((\Delta\rho^T/2)\otimes B_t)U^\dagger,\qquad
B_t\succeq0,\quad\operatorname{Tr}B_t=1/2 .
\]
Diagonalizing the Hermitian first factor shows its tensor trace norm
is \(\|\Delta\rho\|_1/4\). The direct sum and signed native permutation
preserve trace norm. Therefore
\[
\boxed{\|\Delta N\|_1=\tfrac14\sum_\alpha\|\Delta\rho_\alpha\|_1},
\qquad d_N=\tfrac18\sum_\alpha\|\Delta\rho_\alpha\|_1 .
\]
For any invertible S, positive/negative parts and the triangle inequality
give \(\|SAS^\dagger\|_1\le\|S\|_{\rm op}^2\|A\|_1\).
Applying the same bound to the inverse gives the lower bound. The
eigenvalues of E are \((1\pm|t|)/4\), hence
\[
\boxed{\frac{d_F}{1+|t|}\le d_N\le\frac{d_F}{1-|t|}} .
\]
In particular \(d_N\le C\max_k\epsilon_k/(1-|t|)\) is valid.
No joint sharpness of this composed coefficient is claimed.

The endpoint factor is unavoidable even for bounded raw sources.
For \(0<t<1\), write \(\lambda_\pm=(1\pm t)/4\). In one source put
\(\rho_{00}=Q_{Z-}\), in the other put \(\rho_{10}=Q_{Z-}\).
In both put
\[
\rho_{01}=\frac{3+t}{1+t}Q_{Z-},
\]
with other blocks zero. The first two cells are dark in b=0; cell01
is bright in b=1. Each source has mass
\(\lambda_-+\lambda_+(3+t)/(1+t)=1\).
The block coefficients and raw norms stay bounded as t tends to one.
Their distances and full-setting errors are exactly
\[
\boxed{d_N=1/4,\qquad d_F=\epsilon_0=\epsilon_1=\epsilon_2
=(1-t)/4.}
\]
The positive differing filtered blocks occupy distinct retained cells,
so every full law has TV equal to that moved mass, regardless of its
internal split. This attains \(d_N=d_F/(1-t)\).
Moving \(Q_{Z+}\) instead and using common
\(\rho_{01}=(3-t)Q_{Z-}/(1+t)\) similarly attains the lower factor.
The signs of the polarization may be exchanged; these are diagnostics,
not new primary preparations.

At t=1 the raw dark difference persists but has zero mass and is
invisible to every whole-cone mass-dominated effect, as RI-08g proved.
There is no faithful inverse filter or raw-state recovery at the
endpoint. Neither finite errors nor bounded raw inputs repair this
structural failure.

## 5. A supplied-candidate budget certificate, not fitting

Let \(y_k\) be supplied complete, ordered, normalized eight-outcome
tables at the three fixed resolved settings. Each is a probability
law but the three need not be exactly compatible with one L_t source.
Let exact \(\eta_k\ge0\) be deterministic declared budgets. Define
\[
\mathcal F(y,\eta)=
\{N\in L_t:m(N)=1,\ {\rm TV}(p_k(N),y_k)\le\eta_k
\text{ for }k=0,1,2\}.
\]
The comparison retains the same known calibration, context and initial
metadata. When a typed source is supplied, its full source/prefix/pending
metadata are retained and checked. Raw-matrix audits require
`metadata=None` and have only fixed-fixture mathematical scope: attaching
metadata to a raw candidate is rejected through every audit entry point.
A caller requiring matched context/history must supply the typed State;
the audit never promotes a raw matrix into a prepared State. Matching
labels do not independently verify empirical calibration or preparation
history.

The bounded [model](model.py) checks a **supplied** exact positive
normalized candidate N_c, computes its actual TV errors and compares
each with its budget. It does not search for another candidate, fit,
clip, project, silently normalize or relabel tables.

**Success theorem.** A passing candidate proves \(\mathcal F\ne\varnothing\).
For any two feasible sources, triangle TV gives
\(\epsilon_k\le2\eta_k\), and therefore
\[
\boxed{\operatorname{diam}_{d_F}\mathcal F\le2\sum_kb_k\eta_k
\le2\sum_k\widehat b_k\eta_k},
\]
\[
\boxed{\operatorname{diam}_{d_N}\mathcal F
\le\frac{2\sum_k\widehat b_k\eta_k}{1-|t|}.}
\]
At the fixed executable t=3/5 the raw factor is 5/2. These are valid
upper bounds, not claims of sharp diameter for every supplied table.
A failed candidate is inconclusive about nonemptiness. The executor
does not issue an infeasibility certificate or invoke a conic solver.
Malformed data/source rejection is likewise not a proof that a valid
different candidate cannot exist.

The successful and failed audit objects retain exact tables, budgets,
actual errors and candidate data. Typed context/history/pending payloads
remain immutable. They are neither prepared States nor terminal
continuations; no physical read or commitment is performed by the check.
Full zero cells and all native entries survive. Earlier local/reference
selection weights remain unspecified.

**Exact refusal can coexist with budget feasibility.** The center
candidate has \(\sigma_\alpha=I/8\), so q=1/4 in each cell and every
full outcome weight is 1/8. Keep y0 and y2 equal to this table. In y1
add \(0<\delta\le1/8\) to (00,+) and subtract it from (01,+).
Each table is still normalized and nonnegative, but its cell masses
disagree across settings. The unchanged exact RI-08i reconstruction
refuses this family. The center nevertheless has actual errors
\((0,\delta,0)\), so is feasible for those declared budgets.
No “corrected exact table” is silently substituted.

Conversely, for exact center tables and zero budgets the center is
feasible while a different distinguishable candidate fails. Failure
of that candidate plainly cannot establish empty \(\mathcal F\).
No deterministic budget here is a confidence level.

## 6. Rare cells, calibration and a limited target corollary

Full-law precision cannot uniformly control cell-conditioned states
when the cell mass vanishes. In cell00 choose
\(\sigma_{00}=qQ_{X+}\) or \(qQ_{X-}\), \(0<q<1\), and give both
sources the same center remainder of mass \(1-q\) in cell01.
Then \(d_F=q\) and, under every common-X word followed by the fixed
tilted read, \(\epsilon_k=3q/5\). These full-law errors tend to zero.
After conditioning on the occupied rare cell, however, Q_X+ and Q_X-
remain trace distance one. At q=0 that conditional state is undefined,
not a zero-error reconstructed internal state.

A positive lower bound is therefore needed for conditional guarantees.
For cell weights q,q'≥q_min>0, the triangle inequality gives
\[
\tfrac12\|\sigma/q-\sigma'/q'\|_1
\le\frac{\|\sigma-\sigma'\|_1+|q-q'|}{2q_{\min}}
\le\frac{2d_F}{q_{\min}} .
\]
If q=q', the sharper bound \(d_F/q_{\min}\) holds. These are
conditional mathematical bounds, not assumptions that rare events
will be available in a finite experiment.

Unknown calibration/state-frame ambiguity remains separate. For a
unitary W commuting with the known common-X commands, simultaneously
conjugating the filtered source and unknown read projector by W leaves
all three probabilities unchanged. If the read frame is not calibrated,
those tables cannot distinguish that paired change. This diagnostic
symmetry is not a new available control. Deterministic budgets cannot
substitute for justified calibration, sampling or repeated preparation.

There is a limited deterministic linear-target corollary. Suppose
H_i(N) is one specified event probability from setting k(i), and the
linear target on the actual span satisfies \(\ell=\lambda^T H\).
For a feasible source, set \(z_i=y_{k(i)}(\text{that event})\). TV
bounds event probabilities, so
\[
|\ell(N)-\lambda^Tz|\le\sum_i|\lambda_i|\eta_{k(i)} .
\]
This convention matters: a binary expectation difference
\(p_{\alpha,+}-p_{\alpha,-}\) can have error \(2\eta_k\), not
\(\eta_k\). More generally a linear functional of a normalized
setting law is bounded by its coefficient oscillation times TV.
The corollary is algebraic error transfer only; it changes no
application contract and demonstrates no empirical performance.

## 7. Exact witness scope and stop boundary

The independent [checks](check.py) use exact rational/native calculations
and radical identities or proved rational enclosures. Finite witnesses
test the constants, sharp constructions, singular/rare-cell examples
and candidate contract; the full-domain and limiting statements rely
on the written proofs, not a numerical grid or inverse determinant.
The model does not turn signed-span diagnostics into positive
preparations or decimal approximations into certified bounds.

~~~sh
.venv/bin/python -B docs/validation/t8-q-observation-stability-2026-09-13/check.py
.venv/bin/python -B -O docs/validation/t8-q-observation-stability-2026-09-13/check.py
~~~

This is the final bounded refinement of this finite-cone branch before
any separately authorized premise-to-conclusion consolidation. No
automatic successor, generic solver, new hardware/control/preparation,
postmeasurement law, full-QM claim or gravity promotion is started.
Accepted source pins, the registered runner/schema/import contract,
RI-15, claims, coordinator material, core/RET/application source and
protected evidence are not edited. Git integration stays central.
The yield is the stability theorem, explicit boundary counterexamples
and an exact supplied-candidate certificate under declared premises.
