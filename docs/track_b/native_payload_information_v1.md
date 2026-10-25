# Record probabilities and residual payload information

RI1486 — Conditional finite-instrument theorem and counterexample

This note extends the mathematical observation question in [Statistical information in complete marked endpoints](native_endpoint_experiment_v1.md). The actual [admitted model](native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model) retains its passive scalar branches. General matrix instruments below are explicit additional conditional premises; they are not new accepted native dynamics or physical instruments. The complete proof and finite counterexample were independently reviewed as RI1485.

## 1. Explicit mathematical premises

Keep the native finite law, support, marks and horizon unchanged. The following possible extension is a **new conditional matrix-instrument premise**, not admitted native dynamics.

Let H be a finite set of distinct history encodings and pi:H->E a fixed endpoint map. Each fibre F_e has t_e>0 members; count encodings, not automorphism permutations. On one common carrier M_d, suppose parameter theta specifies completely positive trace-nonincreasing linear maps Phi_(theta,h), whose sum is trace preserving. Payload coordinates are identified across histories before comparing maps. Inputs are all density matrices on M_d.

Define Psi_(theta,e)=sum_(h in F_e) Phi_(theta,h), and the classical-record/residual-payload outputs
\[
 \mathcal I_\theta(X)=\sum_h |h\rangle\langle h|\otimes\Phi_{\theta,h}(X),
 \qquad
 \mathcal J_\theta(X)=\sum_e |e\rangle\langle e|\otimes\Psi_{\theta,e}(X).
 \tag{1}
\]
These are mathematical instruments with classical record labels. Joint access to the stated record and residual payload is an assumed observation contract.

Optionally admit an arbitrary finite reference R, correlated with the input and retained unchanged. Then use Phi_(theta,h) tensor id_R on every input density matrix rho_AR. The result below includes that reference without assuming product inputs. No reference system is required for the counterexample.

## 2. Sufficient map condition, and its precise necessity

Assume, for every theta and e,
\[
 \Phi_{\theta,h}=\Phi_{\theta,k}\quad(h,k\in F_e)
 \quad\text{as linear maps on }M_d. \tag{2}
\]
Let D forget the history label while retaining the payload. Let U choose a uniform history from the observed endpoint's fibre, independently of the payload, and retain that payload unchanged:
\[
 U\left(\sum_e|e\rangle\langle e|\otimes Y_e\right)
 =\sum_h|h\rangle\langle h|\otimes Y_{\pi(h)}/t_{\pi(h)}.
 \tag{3}
\]
Both channels are parameter-independent and completely positive trace preserving. Kraus operators are |pi(h)><h| tensor I for D and |h><pi(h)| tensor I/sqrt(t_pi(h)) for U; their adjoint-products each sum to the appropriate identity.

Always D I_theta=J_theta. Under (2), Psi_(theta,e)=t_e Phi_(theta,h), so
\[
 U\mathcal J_\theta=\mathcal I_\theta. \tag{4}
\]
Map equality also gives
\[
 (U\otimes\mathrm{id}_R)(\mathcal J_\theta\otimes\mathrm{id}_R)(\rho_{AR})
 =(\mathcal I_\theta\otimes\mathrm{id}_R)(\rho_{AR})
\]
for every admitted reference and joint input.

Conversely, if this particular uniform-label, unchanged-payload U satisfies (4) on all input density matrices, comparing each history block gives Phi_(theta,h)=Psi_(theta,e)/t_e on those states. Density matrices span the Hermitian matrices, and complex linearity extends equality to M_d. Thus (2) is necessary and sufficient for **this U**. This is not a necessity classification for arbitrary channels that may process the payload.

The two mathematical output experiments consequently simulate each other on the stated input/parameter family. Any admitted subsequent joint decision procedure has the same action probabilities after composition. This is an equality of instruments, stronger than equality of classical record laws. It supplies neither acquisition access nor efficient implementation.

## 3. Two-dimensional counterexample to trace-only sufficiency

Declare an independent toy instrument with d=2, two abstract histories h=0,1, and one endpoint e=pi(0)=pi(1). This toy does not replace native branches or claim to satisfy native marked diamonds.

Put Z=diag(1,-1), and
\[
 \Phi_0(X)=X/2,\qquad \Phi_1(X)=ZXZ/2. \tag{5}
\]
Kraus operators I/sqrt(2), Z/sqrt(2) prove complete positivity. Each branch has trace Tr(X)/2 on positive X, and their sum is trace preserving. Hence the two branch probabilities agree for **every input state**, not just a selected preparation. Nevertheless the maps differ.

Specify the observer/input family: the unknown input is one of
\[
 \rho_\pm=|\pm\rangle\langle\pm|,\qquad
 |\pm\rangle=(|0\rangle\pm|1\rangle)/\sqrt2.
\]
The observer receives only the specified output, has no retained input copy or supplied input label, and may make arbitrary mathematical joint output measurements. The reference is trivial.

Endpoint aggregation gives
\[
 \Psi(\rho_+)=\Psi(\rho_-)=I/2. \tag{6}
\]
History-labelled outputs instead are
\[
 \mathcal I(\rho_+)=\tfrac12|0\rangle\langle0|\otimes\rho_+
                  +\tfrac12|1\rangle\langle1|\otimes\rho_-,
\]
\[
 \mathcal I(\rho_-)=\tfrac12|0\rangle\langle0|\otimes\rho_-
                  +\tfrac12|1\rangle\langle1|\otimes\rho_+.
 \tag{7}
\]
Their supports are orthogonal. The projector
\[
 T=|0\rangle\langle0|\otimes\rho_+
   +|1\rangle\langle1|\otimes\rho_-
\]
has outcome probability one on the first output and zero on the second. Thus history plus residual payload distinguishes these inputs perfectly; endpoint plus residual payload cannot distinguish their identical outputs. With equal priors its minimum error is one half.

No single input-independent reconstruction channel, even one allowed to process the entire endpoint payload, can map the same state |e><e| tensor I/2 to both distinct states in (7). This finite witness proves genuine loss of recoverable joint information, not merely unequal matrix representatives. Knowledge of the fixed toy instrument does not supply the unknown input label.

Trace equality specifies only equal effects Phi_h^*(I). It does not specify the output maps or their correlations with history. The toy rejects trace-only sufficiency; it is not a counterexample to the accepted full-map diamonds.

## 4. Native scope and future selection criterion

In the existing passive scalar family, each complete history map is
\[
 \Phi_{p,h}(X)=L_p(h)X.
\]
The accepted marked diamonds, equivariance and suffix transport give equal L_p(h) within each complete marked endpoint fibre. On the common carrier, the entire maps therefore agree, including their action on off-diagonal matrices and retained references. The uniform reconstruction already preserves the passive payload at that proved finite scope.

This adds no non-scalar dynamics or derivation of QM. For a proposed non-scalar law/readout contract, checking record probabilities alone is insufficient. One must justify full history-map equality on a common identified carrier, or supply a separate recovery proof for the declared input and output access. Reference-system guarantees require the stated map-level control. These are criteria, not an opened successor task.

Only manual reasoning and inert text/hash/JSON administration were used. All scientific/custody, protected validation, ABSTAIN, Status M, zero qualification and RET-only pause gates persist. No physical preparation, novelty, efficient algorithm, quantum/gravity achievement or Boundary claim follows.
