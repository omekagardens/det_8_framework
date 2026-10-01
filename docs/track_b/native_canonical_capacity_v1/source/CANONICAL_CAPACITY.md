# Complete canonical parent capacity and forced tightness

30 September 2026, Honolulu. RI231 manual conditional lemma for independent
review. The exceptional canonical coefficient remains unresolved, but its
complete parent incidence forces a tighter upper bound and a tight row at
the canonical optimum. No allocation is inferred from negative cost alone.

## 1. Parent and every ideal

Use the accepted exceptional five-parent

    P: r<a<b,   r<x,   o<x,

whose maxima are b,x and whose minima are r,o. Its Ferrers-cell
arbitrary-deletion defect is one: deleting o leaves the four-cell
hook, whereas P itself has two minima.

Every ideal excluding x is a chain prefix of r<a<b, with o either
absent or present. Every ideal containing x contains r,o and may
include an initial segment of a<b. This gives exactly eleven ideals:
the following ten proper ideals and the single full ideal P.

| Proper precursor | Terminal defect | Canonical role |
| --- | ---: | --- |
| empty | 2 | zero |
| {r} | 2 | zero |
| {r,a} | 2 | zero |
| {r,a,b} | 1 | kappa |
| {o} | 2 | zero |
| {r,o} | 2 | zero |
| {r,a,o} | 2 | zero |
| {r,a,b,o} | 1 | mu |
| {r,o,x} | 1 | tau |
| {r,a,o,x} | 1 | nu |

Every labeled ideal is listed once. All32 binary records and both
newborn bits remain; these are not orbit-averaged row counts.
The final full slot is the normalized complement, not another free
proper component.

Here is a complete defect check for the six zero roles. In every
terminal both r and o remain minimal; deleting any other original
vertex or the newborn therefore leaves at least two minima, except
that removing an isolated newborn simply restores the non-Ferrers P.
Deleting r leaves at least a and o minimal (and may leave more).
It remains to check deletion of o:

- Empty precursor leaves the four-cell hook disjoint from the
  newborn isolate.
- Precursors {r} and {r,o} leave r with three distinct covers a,x
  and the newborn; a Ferrers cell order has at most two covers
  above its least cell.
- Precursors {r,a} and {r,a,o} leave incomparable b and the
  newborn, each with chain principal ideal, sharing r,a. The
  accepted axis-segment obstruction excludes a Ferrers cell order.
- Precursor {o} leaves the newborn isolated from the hook.

Thus no single deletion makes these terminals Ferrers. Deleting o
and the newborn restores the hook, so their defect is exactly two.
Each role raises defect1to2. The accepted RI63 active-component
neutrality theorem makes its whole canonical coefficient zero;
strict restoration of that role in the actual law is not zero.

For the other four roles, deleting o leaves respectively Ferrers
shapes with row lengths (4,1), (4,1), (3,1,1), (3,2).
The two minima show defect at least one; these witnesses show
exactly one. All four P roles are neutral. Being neutral alone
does not assign them canonical mass.

## 2. Complete presentations and marked components

For each of the four neutral births let y denote the new maximum
when convenient. Its terminal has exactly two maxima. The following
table exhausts its other parent presentation.

| Component family | P precursor | Other parent | Other precursor |
| --- | --- | --- | --- |
| kappa | {r,a,b} | Y=C4 disjoint {o} | {r,o} |
| mu | {r,a,b,o} | P_mu: r<a<b<y, o<y | {r,o} |
| tau | {r,o,x} | P_tau: r<a, r<x<y, o<x<y | {r,a} |
| nu | {r,a,o,x} | P_nu: r<a, r<x, o<x, a<y, x<y | {r,a} |

For kappa the terminal is the accepted Tstar: extending the solo
chain of P gives r<a<b<y with r<x,o<x. For mu the new
y additionally has o in its past. For tau y extends x. For
nu y lies above both a and x. Deleting the two terminal maxima
gives exactly the two displayed presentations in each case.
No longer ratio path can acquire another parent: it preserves
the terminal order, and every possible newborn must be maximal.

The four terminal orders are different. The first two have height
four but have respectively eight and nine strict relations; the
last two have height three and respectively eight and nine strict
relations. This is a manual shape comparison, not an automated
canonical-key or certificate-index calculation.

In each case delete both terminal maxima to obtain the common
four-event base, and use their two full past ideals as the ordered
birth precursors. The intersection of those pasts is compulsory
in both local nodes. At fixed compulsory marks, independently
varying all other base marks gives the complete bipartite incidence:

| Family | Compulsory vertices | P optional bits | Other-parent optional bits | Components |
| --- | --- | --- | --- | --- |
| kappa | r | a,b | o | kappa_i |
| mu | r,o | a,b | none | mu_(i,l) |
| tau | r | o,x | a | tau_i |
| nu | r,a | o,x | none | nu_(i,j) |

Thus the incidences are4-by2,4-by1,4-by2,4-by1 at each fixed
compulsory assignment. Both newborn bits and both ordered precursor
pairs are retained. The common vertices are intrinsically
distinguished: r has the long-chain branch in mu, and in nu a
lies above r and supplies the solo terminal tip. No terminal
automorphism exchanges compulsory roles or flips their marks.
Every optional selected mark is joined by the full diamond, and
no compulsory mark changes along an edge. These are complete
component descriptions, not assertions from local coefficient equality.

Write i=r_r, j=r_a, k=r_b, l=r_o, m=r_x for a P marking.
The canonical coordinates are nonnegative; none of mu,tau,nu
is presumed positive or assigned a numerical value. They are
distinct families of the original canonical problem, not new
free parameters that may be refitted.

## 3. Complete canonical P row

The P precursor for kappa omits only maximum x. Its potential is

    a0=q(K,{r,a,b})=alpha_I*A_I=41/352,                     (C1)

where K=C3 disjoint {o}, A_I=41/44, and the separately admitted
six-root witness gives alpha_I=1/8.

The other three potentials are unchanged strictly positive lower
probabilities. Define, retaining the indicated restrictions,

    t(r)=q(K,r|K,K),
    v(r)=q(N,r|N,{r,o,x}),
    n(r)=q(N,r|N,N),
    N: r<a, r<x, o<x.                                     (C2)

For mu omit maximum x, leaving K and its full ideal.
For tau and nu omit maximum b, leaving N with the selected
three-ideal or full ideal. Thus unique omitted-maximum deletion
proves(C2), without reading any additional RI41 coordinate.

Every complete canonical P row is consequently

    C_P(r)=a0*kappa_i
                +t(r)*mu_(i,l)+v(r)*tau_i+n(r)*nu_(i,j) <=1,
    q_can(P,P)=1-C_P(r)>=0.                                (C3)

All six other proper terms are zero by section1, not silently
omitted. Formula(C3) holds on the full32-record cube, with every
labeling transported equivariantly. No maximal-record or root-only
shortcut is needed for its quantifier; no missing bits have been
set to zero. The potentials remain the actual fixed-prefix ones.

The complete two-parent incidence also gives every affected row
outside P when one changes only these four families:

    Y:     kappa_i has potential gamma_i=1/64,
    P_mu:  mu_(i,l) has potential gamma_i=1/64,
    P_tau: tau_i has potential p(r)=q(N,{r,a}),
    P_nu:  nu_(i,j) has potential p(r)=q(N,{r,a}).            (C4)

For P_mu and P_nu the sole maximum is y; deleting it leaves K
or N. For P_tau its maxima are a,y; the precursor contains a,
so deleting y leaves N. All these p potentials are strictly
positive. Their actual values need not be resolved for this lemma.

Each listed family has exactly one proper ideal in each of its
two parent presentations for the given compatible markings.
Other canonical components on the other parents remain in their
rows as fixed, possibly nonzero contributions. They are not
discarded when checking feasibility or exchanges.

## 4. Full increments and the exact objective change

Full P raises defect1to2, as accepted in RI228. A direct check
removes any ambiguity: all single deletions except r,o retain
both minima; removing r leaves a,o minimal; removing o leaves a
five-cell unique-maximum nonchain, impossible for a Ferrers
rectangle. Removing o,x leaves a chain, proving exact defect2.

Full Y and full P_mu are neutral: deleting o leaves respectively
a chain, while the two minima rule out defect zero. The proper
roles in their displayed components are neutral as well.

P_tau and P_nu each have defect one: deleting o leaves respectively
a four-cell hook and a four-cell rectangle. Their full births
have defect exactly two. After deleting o, each leaves a five-cell
unique-maximum nonchain; deleting r instead leaves at least a,o
minimal; all other single deletions keep r,o. Deleting o and a
leaves a chain in both cases. These are complete single-deletion
obstructions plus explicit two-deletion witnesses.

It follows that a variation supported only on kappa,mu,tau,nu
has exact primary objective change

    Delta Phi =
      -sum_(marked P rows) pi_P*Delta C_P
      -sum_(marked P_tau rows) pi_tau*p*Delta tau
      -sum_(marked P_nu rows) pi_nu*p*Delta nu.              (C5)

All weights are the actual strictly positive fixed-prefix marked
history masses, with the original natural-history multiplicities.
For canonical marked-row classes the corresponding multiplicities
are aggregated exactly as in RI63; alternatively the sums may be
written on all natural marked histories. No uniform weighting is
substituted. Y and P_mu have zero full increment and contribute
zero to(C5). The formula concerns the original objective on a
feasible coefficient variation, not an optimization engine.

In particular every individual kappa or mu objective coefficient
is strictly negative because of its P roles; tau and nu have
additional negative contributions from their other parents.
This still does not assign their canonical allocations.

A sound local exchange criterion follows from the complete incidence.
A proposed variation must keep every changed coordinate nonnegative
and preserve every affected full row, including the fixed other
components in Y,P_mu,P_tau,P_nu. No other parent can be affected.
If it is feasible, all Delta C_P>=0, and all Delta tau and
Delta nu>=0, then(C5) is nonpositive. It is strictly negative
if any displayed mass increment is positive. Such a strict
exchange is impossible at a primary optimum.

For example a purported compensation that preserves P mass but
increases tau or nu cannot be a harmless objective-neutral move;
its other-parent contributions in(C5) matter. Conversely any
claimed kappa-to-mu exchange must check all P records and every
P_mu residual capacity. Its negative coefficient alone is not
permission to increase mu.

## 5. Forced tightness and stronger bounds on kappa

Nonnegativity in(C3), with a0=41/352, immediately gives

    0<=kappa_i<=352/41.                                    (C6)

Every Y row containing kappa therefore has canonical proper mass

    kappa_i/64 <=11/82 <1.                                 (C7)

RI228 proved that kappa is Y's only possible canonical proper
contribution. Consequently all Y rows retain canonical full
slack at least71/82. This is a derived fact about Y, not an
assumption that other companion rows are slack.

Now fix a root sector i. Suppose every P row in that sector were
strictly slack at the canonical optimum. There are finitely many
such rows and each has coefficient a0>0 on kappa_i, so their
minimum allowable positive increment of kappa_i is positive.
All corresponding Y rows also have strictly positive slack by(C7).
The complete incidence in section2 shows no other row is affected.

A sufficiently small increase of this single kappa coordinate
therefore stays feasible. Its objective change is
-a0 times a strictly positive sum of actual P history masses.
It is strictly negative, contradicting primary optimality.

Thus, at the canonical optimum, using its primary optimality,

    for each i, at least one original marked P row
    with root bit i is exactly tight.                      (C8)

This does not say which row, that all such rows are tight,
or that kappa_i is positive. The proof uses the accepted canonical
zero-component facts for P and Y; it does not extend them to all
primary optima, which may have different component allocations.

Put

    R_i(r)=t(r)*mu_(i,l)+v(r)*tau_i+n(r)*nu_(i,j).

Combining all(C3) inequalities with(C8) gives the exact conditional
capacity identity at the unchanged optimum:

    kappa_i=(352/41)*(1-max_(r:r_r=i) R_i(r)).              (C9)

The maximum is over all original compatible P markings. It is
not numerically evaluated. In particular kappa_i=0 exactly
when that maximum competing mass is1. It is invalid to replace
(C9) by kappa_i=352/41 without proving that every competing
mass vanishes.

Equation(C9) is stronger than a generic sign statement: it exhausts
both parent presentations, all incident components in P and every
record, and proves where a binding capacity must occur. The
remaining competing canonical allocations and lower potentials in
(C2) are not supplied by the six-root certificate exception.

## 6. Consequences for the unchanged strict mixture

From zeta_i=(35/36)*gamma_i*kappa_i, gamma_i=1/64 and(C6),

    0<=zeta_i<=(35/36)*(11/82)=385/2952.                    (C10)

The accepted complete Y potential bound theta*U_Y<1/72 still
holds with no evaluation of theta or M5. Therefore

    F_Y=1-zeta_i-theta*U_Y
       >1-385/2952-1/72
       =421/492.                                          (C11)

For a hand check, 1/72=41/2952; subtracting385+41 from2952
gives2526, and2526/2952=421/492. This is a strengthened
full-slot margin for the unchanged actual mixture, not an H30
amplitude choice or a replacement probability law.

The zero branch, both independent root-sector allocations, all
canonical corrections and all full normalized equations in
[SIX_ROOT_WITNESS.md](SIX_ROOT_WITNESS.md) remain. Bound(C11)
does not decide those equations.

## 7. Exact remaining premise and stop

The lower-profile coefficient gap is no longer the six RI41 values.
For this route it is the two actual kappa allocations, equivalently
the two complete maxima in(C9), or a same-source identity controlling
their appearance in(W4)-(W8) sufficiently to give a full witness
or obstruction. Determining the competing mu,tau,nu coordinates
would require their actual coupled optimal-face consequences;
their signs and this one parent row do not determine them.

Even those lower combinations must still be used in every original
normalized row, with all ten unknowns and all connected contrasts.
No full normalized solution or finite signed inconsistency identity
has been proved. No nonderivability or global minimal-information
claim is made.

The proof uses the accepted fixed finite baseline and RI63's primary
optimality, not a DET-native selection theorem or a physical law.
[SOURCE_REFERENCES.json](SOURCE_REFERENCES.json) and
[AUTHOR_VERIFICATION.json](AUTHOR_VERIFICATION.json) record the
bounded literal exception, complete analytic reads and author checks.
No other coordinate/body, numerical amplitude, automatic scientific
arithmetic, graph/LP/runtime, H/z reconstruction, repository/Git/index,
measurement, RET or successor work was undertaken. Stop at the
sealed packet for independent adjudication.
