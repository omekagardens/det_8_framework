# A first-birth obstruction to fixed additive balance

This independently reviewed result closes one proposed balance formula for the [fixed active residual law](native_active_residual_v1.md). It does not identify a physical energy or rule out conservation in DET. The existing residual-to-structure and complete-trial source-response results remain unchanged.

## Exact question

Use the unchanged two-state classical instrument through four births, with every actual ideal and both immutable newborn marks. At empty, every normalized input rho=(x,1-x)^T, 0<=x<=1, is admitted. At a nonempty committed marked prefix E, use only normalized residual states reachable by positive-mass histories from those inputs. Size four is terminal.

The proposed quantity is C(E,rho)=V(E)+ell rho. The real row ell=(ell_0,ell_1) is fixed at every prefix and must be nonconstant: ell_0!=ell_1. The real scalar V depends only on the existing committed marked prefix, invariant under marked relabeling. It cannot depend on an unrecorded initial source, the residual state or a separate traversal history. Set V(empty)=0 as an additive gauge; terminal values are unrestricted.

The question requires exact conditional-mean balance at every admitted parent/state of size below four:

    sum_a [V(E_a) 1^T + ell] B_(a|E) rho = V(E) + ell rho.

Here B_(a|E) is the complete unnormalized branch matrix. Thus the record potential is weighted by the actual branch mass. This equation is weaker than conservation on every individual path.

**There is no such pair ell,V for this law and domain.** A necessary condition at the first birth already contradicts nonconstancy.

## Complete first-step proof

At empty there is one actual ideal and two possible newborn marks, b=0,1. The fixed law has q=1 and r=theta(a_1-a_0)=0, because a_1=a_0=1/264. Its t=1/2 gives

    K = [[3/4, 1/4], [1/4, 3/4]],
    B_0 = B_1 = K/2.

Every column of each B_b sums to 1/2. Therefore both marks have actual probability 1/2 for every normalized initial rho, and their conditional residual states are K rho. Both positive-mass branches are included; the equal weights are derived from this instrument, not substituted for general active weights.

The two marked singleton records E_0,E_1 may have separate arbitrary real potentials V_0,V_1. Put vbar=(V_0+V_1)/2. Record-only dependence requires the same vbar for every initial input. The necessary mean equation becomes

    vbar + ell K rho = ell rho.

The admitted initial state delta_0=(1,0)^T requires

    vbar + (3 ell_0 + ell_1)/4 = ell_0,
    vbar = (ell_0 - ell_1)/4.

The also-admitted delta_1=(0,1)^T requires

    vbar + (ell_0 + 3 ell_1)/4 = ell_1,
    vbar = -(ell_0 - ell_1)/4.

These equations force ell_0=ell_1, contradicting the required nonconstant row. Their child states are actual reachable outputs on both marks. No unreachable nonempty state, extra terminal condition or fifth birth was used.

A necessary first-step failure suffices to refute the full universal target. No later-history enumeration is needed. Unequal mark-specific potentials were already allowed, and leaving V(empty) at a different additive gauge would shift the same scalar in both equations without removing the contradiction.

## What this closes

The first record has an input-independent distribution while K changes a fixed nonconstant residual expectation differently on the two initial inputs. Its source-independent record mean cannot compensate both changes. Constant residual rows or record-only identities do not answer the stated question.

The fixed row, record-only potential, full initial interval and particular instrument are essential assumptions. This result does not exclude other native quantities, nonlinear or coupled balance, environmental accounting, clocks, geometry or physical conservation. It supplies no global scalar-energy requirement on arbitrary curved geometry and no inference against GR. It does not change the admitted law or design a replacement.

Physical units, time or symmetry interpretation, source coupling, mass correspondence and preparation/readout calibration remain separate obligations. Mathematical availability of the initial states does not supply a physical preparation certificate. No empirical confirmation, finite-sample guarantee, unique mechanism or computational advantage follows. Independent review, custody, protected evaluation and execution gates remain in force.
