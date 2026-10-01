# RI189 fixed component contrast: exact routing and a two-entry gap

30 September 2026. Manual source-author proof for independent review.
The actual record-contrast comparison remains undecided. No coefficient
value is instantiated or scientific vector decoded in this sitting.

## 1. Result

The six C4 roles in the RI187 obstruction can be addressed by exact
canonical component-root keys, without determining their ordinal indices
or reading their assigned numerical values. The companion
[COMPONENT_ROUTING.md](COMPONENT_ROUTING.md) supplies the complete manual
marked-diamond and canonical-key proof. Write alpha(k) for the coefficient
already assigned to component root k in the unchanged RI41 vector. Then

    pi_i=alpha((78,7,i)),
    sigma_i=alpha((206,7,i)),
    beta_i=alpha((2254,7,i)),       i=0,1,
    p_i=pi_i/44,       s_i=sigma_i/44,
    b_i=41beta_i/44.                                (1)

These sigma_i are size-four component coefficients, not the canonical
positive-part sigma_i in RI187. That older canonical quantity is written
sigma_i^(5) below. Keys label components, not coefficient magnitudes.

Define epsilon=beta_0-beta_1>0. The accepted row bounds and RI187 theorem
give the new necessary window

    v>B6 implies 0<epsilon<epsilon_*<1/10000,

    epsilon_*=44*1147*3875/(41*126280*508644).         (2)

Conversely the single two-entry premise epsilon>=epsilon_* suffices to
prove v<B6 strictly. In particular epsilon>=1/10000 suffices. This does
not assert either lower bound at the actual fixed vector. It identifies
an exact, smaller unresolved coefficient premise, with a bounded proof
design in section 6. Routing has been addressed; the remaining missing
fact is an actual magnitude comparison, not an undiscovered diamond
joining these two coefficients.

## 2. Structural identities versus fixed-value equalities

RI168 already proved the complete terminal incidence: the singleton,
initial-pair and initial-triple families have respectively 2,4,8
components. The compulsory ordered trunk has length 1,2,3. Every trunk
bit survives every proper presentation and marked diamond. The six
roles here are only the representatives with other trunk bits zero.
They are not the entire component inventory.

The complete root families, now with their minimum local keys, are

    P_i:       (78,7,i),
    S_(i,u):   (206,7,i+2u),
    B_(i,u,v): (2254,7,i+2u+4v).                     (3)

The new routing proof checks the original key convention, all possible
maximal-deletion parent roles and optional selected marks. It does not
globally enumerate the 109 components. Terminal type prevents paths
between the three families; compulsory trunk marks prevent the indicated
components within a family from merging.

Separately, the accepted RI127 finite transport theorem and complete C4
normalization give root-only actual values b_i,c_i,s_i. Since their
potentials are record-blind positive constants, actual coefficients in
S_(i,0),S_(i,1), and in all four B_(i,u,v) at fixed i agree in value.
These are inherited facts about the selected vector, not identities of
its graph components, record-flip symmetries or general DET consequences.
The six representative roots in(1) therefore name the needed actual
values without erasing the other components or marked rows.

## 3. What the coupled normalization and completion actually prescribe

The complete C4 row remains

    w+p_i+s_i+b_i+c_i=1,
    c_i=1-w-(pi_i+sigma_i+41beta_i)/44.              (4)

The common empty slot w is canceled only after both rows are retained.
Subtracting gives

    c_1-c_0=(41/44)epsilon
                     -(pi_1-pi_0)/44-(sigma_1-sigma_0)/44. (5)

The opposite parent rows from the same complete diamonds are also
binding. RI168 uses V for the four-event hook and T for the four-event
stem-fork. Their complete proper masks and probabilities are

    V: 0,1,3,7,9,11 : E_V,L_i,z_i,41p_i,f_i,g_(i,u),
    T: 0,1,3,7,11   : E_T,z_i,t_(i,u),41s_i,41s_i.  (6)

Each full complement is one minus its entire displayed sum. E_V and E_T
are their respective empty probabilities; matching potential formulas
alone do not identify their components. L_i and t_(i,u) name the V-root
and T-initial-pair probabilities. The shared z_i is a genuine component
identity from the (1,3)/(3,1) diamonds, not a separate variable for each
row. Both T arm occurrences remain in the sum, even when their component
and value coincide. Every other row containing any of these global
coordinates remains binding. Nothing is varied independently in(4)--(6).

The accepted uniform full-complement and height margins applied to these
complete rows give the already established bounds used below. They do
not in the present source derivation fix the cross-root difference of
the two entries beta_0,beta_1. No claim is made that the complete fixed
law logically fails to determine it: the vector is prescribed and its
difference is a definite number. The missing item is a permitted proof
of its magnitude from the selected analytic premises.

The original RI41 construction makes the distinction explicit:

- `local_key` defines the whole-parent/precursor/selected-mark quotient;
  `layer` seeds all proper nodes, retains the complete raw diamonds and
  orders components by their minimum keys.
- `load_certificate` checks the declared ordered root list and supplies
  the fixed positive coefficient vector through its default and overrides.
  It does not calculate the vector from lexicographic key order.
- Complete proper rows multiply each potential by that fixed component
  coefficient; full probabilities are then set by normalization.

These are literal source definitions, read without calling any function
or opening its scientific input. RI41 supplies an exact feasible witness,
not a theorem that its 109-vector is an optimizer or is uniquely selected
by the half-height constraints. Its discovery-rounding narrative is not
a proved spacing property of these two accepted entries.

RI63 explicitly keeps the RI41 prefix unchanged and reconciles its pinned
coefficients before defining the next layer. Its canonical optimization
is at parent size five. It does not retroactively choose or optimize the
size-four pi_i,sigma_i,beta_i. The later canonical N_i terms and theta/M5
remain coupled to this same prefix; they cannot supply an invented
cross-root coefficient order or an arbitrary spacing assumption here.

## 4. Necessary small-gap window and conditional exclusion

Use the accepted RI157/187 same-law quantities

    delta=b_0-b_1=(41/44)epsilon>0,
    D_-=(p_1-p_0)_++(s_1-s_0)_+,
    U=1147/126280,
    tau=508644/3875,
    0<D_-<U,       v>B6 implies D_-/delta>tau.        (7)

The strict U bound retains both selected proper-slot lower margins and
their separate upper bounds, including the two T arm occurrences.
It is inherited as an analytic enclosure, not reevaluated on the vector.

All quantities divided by below are positive. If v>B6, then

    delta<D_-/tau<U/tau,
    0<epsilon<(44/41)*U/tau=epsilon_*.              (8)

Conversely epsilon>=epsilon_* implies delta>=U/tau, so

    D_-/delta<U/delta<=tau.                         (9)

RI187's strict reverse-premise theorem then yields v<B6. Equality at
epsilon=epsilon_* still gives strict exclusion because D_-<U. No lower
bound on epsilon was assumed before its conditional branch was stated.

For a simpler sufficient premise, U<1/100 since114700<126280. Also
tau>131>1000/9 and41/44>9/10. Thus

    epsilon_* = U/[(41/44)tau] < (1/100)/100=1/10000. (10)

Equivalently, if epsilon>=1/10000, then

    delta>=41/440000>9/100000,
    D_-/delta<1000/9<131<tau,
    v<B6.                                          (11)

These are hand rational comparisons of analytic bounds, not evaluations
of the selected coefficient difference. The required pairwise premise is

    alpha((2254,7,0))-alpha((2254,7,1))>=1/10000,     (12)

or the weaker sufficient threshold epsilon_* in(8). A universal grid
theorem for all109 coefficients is unnecessary for this route.

The threshold epsilon_* is the exact cutoff obtained from the particular
uniform bound U and RI187's tau. It is not claimed to be an optimal native
threshold. A gap smaller than epsilon_* neither proves v>B6 nor refutes
the endpoint: the actual numerator D_- would still have to be compared.

## 5. The remaining six-entry comparison, now unambiguously routed

Without any extra spacing premise, the exact obstruction can be written
using only the six specified component roots:

    D_-/delta =
      [(pi_1-pi_0)_++(sigma_1-sigma_0)_+]/(41epsilon).

Therefore the direct rejection predicate is

    (pi_1-pi_0)_++(sigma_1-sigma_0)_+
                         <=(20854404/3875)epsilon.   (13)

Satisfaction would imply v<B6 strictly by RI187. Its strict opposite is
only a necessary test for the capacity branch, not sufficient for v>B6
and certainly not for the full H6 comparison. All actual values in(13)
remain coupled, not independently chosen variables. Equations(8)--(12)
reduce one sufficient rejection route from six entries to two; they are
not merely a relabeling of(13) or of the endpoint equivalence.

Even an eventual rejection of v>B6 would exclude only the full-domain
endpoint certificate at Z6. It would not decide actual W(rho,s), since
rho<Z6 and the actual s remains fixed. Conversely success of the strict
branch would still leave the full canonical q comparison.

In particular, the unchanged canonical correction is retained as

    N_i=(35/1476)*sigma_i^(5),
    sigma_i^(5)=[41p_i-f_i/2-min(g_(i,0),g_(i,1))]_+/c_i,
    omega_i=44theta*p_i,

    q(z)=(1-theta*z^2)v
      +(2-theta-2theta*z+theta^2*z^2)Delta h
      +(3-2theta-2z+theta*z^2)Delta j
      +(z-2)Delta N+2Delta(N*omega)-theta*z^2 Delta(N*omega^2). (14)

Delta means record1 minus record0. All minima, zero/positive branches,
tied minima and differences of full products remain. No favorable
canonical term is assumed while testing the necessary capacity branch.

## 6. Bounded review design for the unresolved pair premise

The minimal remaining target for the sufficient route is a proof of
the two-key separation(12), or the exact epsilon_* version. It is a
specific mathematical predicate, not a request to enumerate another
parent family, rerun the scientific checker or evaluate a full vector.
The following is a proof design only; none of its scientific-input
steps is admitted or performed by this sitting.

1. Retain the unchanged prefix identity and the original coefficient
   selector defined in the already selected RI41/RI63 sources. Obtain
   root authorization before any new historical path, scientific body
   read, selected-table instantiation or new execution. A path being
   known or inherited does not itself authorize numerical extraction.
2. Use the companion's complete canonical routing proof to bind the
   two components to exactly (2254,7,0) and (2254,7,1). No global component
   index is guessed from terminal shape or from adjacency in key order.
3. Require a same-source mathematical witness for their difference.
   This may be an independently accepted analytic separation lemma or
   a separately authorized exact two-entry bound, explicitly linked to
   the prescribed default/override selection and original root ordering.
   It cannot be obtained by assigning convenient new coefficients.
4. For the simple threshold, an exact rational witness beta_i=n_i/d_i,
   with d_i>0, would need the integer inequality

       10000*(n_0*d_1-n_1*d_0)>=d_0*d_1.             (15)

   This is a specification, not instantiated arithmetic. Alternatively
   certified intervals beta_0>=L0, beta_1<=U1 with L0-U1>=epsilon_*
   would suffice. Their provenance and actual fixed-law binding are
   load-bearing, not just the interval subtraction.
5. If such a witness is unavailable or below the threshold, report that
   this sufficient route is unresolved/inapplicable. Do not infer the
   strict opposite of(13). A direct six-entry proof of(13), if later
   authorized, must retain both positive parts and all six exact key
   bindings; that is a distinct possible check, not a started successor.

The pair alone is a bounded target. Proving an unrelated denominator
grid, treating consecutive root keys as monotone values, or citing that
discovery once rounded candidates is not a substitute for the specified
same-law witness. No such witness is supplied in this packet.

## 7. Evidence boundary and conclusion

Complete main source reads cover the current assignment, root decision
and manual review; the complete RI187 endpoint manuscript; RI41
NORMALIZATION and its standalone checker as literal text; RI168 INCIDENCE;
and RI63 COMPLETION. Complete RI187 LOWER_LAW_TRACE and DEPENDENCY_NOTES
reads from the immediately preceding author work are retained, not
misreported as new executions. RI157's accepted contrast bound remains
an inherited theorem. The companion and provenance records supply exact
pins, full manual routing details and actual author-peer check receipts.

The new result is an explicit canonical-key routing proof and a
conditional two-entry separation theorem with a concrete bounded review
design. The actual inequality D_-<=tau*delta, its strict opposite, v>B6,
H6 and actual W/H30 remain undecided. This is neither a fixed-law
counterexample nor a proof that further structural reasoning is impossible.

No scientific JSON/vector/certificate decode or evaluation, selected
coefficient-table instantiation, numerical/symbolic/graph engine,
target/helper/vendor import, compile, AST, probe or run occurred. No
new mathematical path, agent/thread, fixture, runtime/profile/card,
admission, repository/index/Git or predecessor change was made. Preserve
P2/P3,Y=1/4,31/139/20/42,shared T1,other eight parents,five Di,theta/M5
and all labeled occurrences and canonical terms. RET is paused;
measurement and qualification are separately owned. Root owns independent
acceptance, publication, execution admission and successor selection.
No QM, geometry, mass/gravity, physical or ontological promotion follows.
Stop at the sealed handoff.
