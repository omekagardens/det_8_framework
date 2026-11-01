# Conditional preparation and transport results

Accepted scope, 1 November 2026. These are separate conditional mathematical and source decisions. Neither supplies a physical DET prediction or an execution permit.

## GDM019: a shared preparation setting is a conditional resource

The target remains the [GDM017 classical response distribution](../gdm017-phase-response-laws-2026-11-01/CALCULATION.md). The proposed conventional Coulomb relative state uses circular basis states |n,l=n-1,m=n-1>, n=140,...,160, coefficients c_n=N exp[-(n-150)^2/100], and rotation

    |psi_phi> = sum_n c_n exp[-i(n-1)phi] |n>_c,
    phi uniform on [0,2pi).

This finite normalized packet is a proposal, not demonstrated positronium synthesis. Distinct occupied n have distinct Coulomb energies E_n=-mu*C^2/(2*hbar^2*n^2), so its energy variance is positive. It cannot literally equal the classical fixed-radius, fixed-energy preparation while preserving that energy observable. This does not rule out a response-specific approximation.

A retained controller setting can be used to prepare fresh atoms within a block while recording only the block identifier. Conditional repeatability and independence are supplied assumptions. For rho_phi=|psi_phi><psi_phi|, the proposed relative block state is Omega_k=integral rho_phi^(tensor k) dphi/(2pi). Single-copy averaging yields sum_n |c_n|^2 |n><n|. For n!=m, Omega_2 retains the |n,m><m,n| element |c_n|^2|c_m|^2, whereas independently averaged copies do not. Thus an unread setting retained across a block differs from redrawing and forgetting it every shot. Repreparing from a retained classical recipe is not cloning an unknown quantum state.

The proposed within-block force/gravity measurements would estimate conditional quantum mean-response derivatives and their matched ratio. That is not a single-atom derivative or the ratio of means over all blocks. It agrees with the desired classical individual-response distribution only if a quantitative response correspondence is established. The block-state inequality alone proves no detector access.

Actual packet synthesis, central/spin preparation, correspondence to classical radius/time, matched controls, ionisation/imaging readout, loss and normalized error bounds remain open. [Yoshida et al.](https://www.osti.gov/pages/servlets/purl/1623709) supplies wave-packet construction language; [Heiss et al.](https://arxiv.org/pdf/1809.07854v1) supplies an excitation/ionisation component precedent. Neither realizes this proposal. GDM020 is a separately assigned necessary response comparison under explicit conventional quantum assumptions; it is not accepted by this note. No physical 0-versus-2/3 probability transfers.

## CL001: a fixed transport law needs additional probability information

Classical independently authored and reviewed this example; the coordinator subsequently reviewed and adopted its transfer assumptions as a QR reference. Matrices act on column probability vectors. Fix

    Q = [[3,1,0,0],[1,2,1,0],[0,1,2,1],[0,0,1,3]] / 4,
    Fp = (p0+p1, p2+p3),
    T = [[7,1],[1,7]] / 8.

Admit the full four-state probability simplex, unchanged controls and separate exhaustive terminal L/R observations after n=0,...,8 updates. No intermediate observation or postselection occurs. The graph and kernel are supplied; update count is dimensionless.

Preparations e0 and e1 share Fp=(1,0), but their one-step terminal laws are (1,0) and (3/4,1/4). Any common coarse-only prediction has worst total-variation error at least 1/8 on that pair. T attains this bound at one step; no all-horizon optimality is claimed. For the fixed T, the whole-simplex maximum over the frozen horizon is 21/128 at n=3.

Let s=p0+p1-p2-p3 and z=p1-p2. Direct row multiplication gives

    s_next = s-z/2,    z_next = s/4,
    s_(n+2) = s_(n+1)-s_n/8,    s1=s0-z0/2.

The feasible domain is |s|<=1 and (s-1)/2<=z<=(s+1)/2. It is the image of the probability simplex and is preserved by the projected stochastic Q. The exact terminal law is ((1+s_n)/2,(1-s_n)/2). This signed summary update is not a stochastic transition on two physical states. Access to z is additional information about a distribution, not something supplied by one L/R sample.

For block-uniform initial preparations, z0=s0/2. The coarse prediction agrees for one step, but the family is not invariant: actual s2=5*s0/8 versus coarse 9*s0/16. The maximum TV error is 1/32 at exactly two updates. Across the whole n=0,...,8 horizon, the block-uniform maximum is 623/8192 at n=6. The distinction matters.

For each horizon the signed binary-law error is linear in p, so the absolute maximum over the full simplex occurs at a vertex; the two endpoints similarly suffice for the block-uniform interval. Author rational arithmetic and a distinct integer-ticket enumeration with an analytic coarse-law oracle agree on all 54 frozen preparation/horizon cases. These are synthetic exact checks. Generic record-fiber sufficiency and closure criteria are reused, not new general theorems. No joint multi-time law, physical access, native diffusion, continuum limit, mass/gravity or computational saving follows.

### Source warning and owned correction

At kernel_continuum.py SHA256 c66650bb4181e3cd0f64a3c07a1acea11c2b30e145e93f0adc0f1cc1c5642ab0, the asymmetric constructor normalizes rows while diffuse evolves column states. For two sites, w=1 and eps=drift=1/4, the update is [[11/16,5/16],[3/16,13/16]]. One update from e0 has total probability 7/8. That asymmetric path is not admitted as conservative probability evolution. CL001's explicit symmetric Q is unaffected. Classical owns the separate CL002 convention/correction recommendation; shared implementation and independent review follow a concrete accepted correction contract. This note changes no model source.

## RET031: the proposed measurement executor mechanism is declined

Distinct review and coordinator disposition accept only the finite direct-launch/original-sole-reaper interface design and its precise current-surface refusal. The supported executor does not supply the identified integration hook and completed launcher usage receipt required by that design. New job-specific accounting costs in a persistent parent cannot be silently excluded. A command-string interface alone does not prove that a separate shell survives; no host-wide impossibility is established.

Reopening requires actual authorized versioned executor/source integration, terminal identity and lifetime/units evidence, and an explicit defensible accounting-boundary decision. The completed-job accounting, failure-byte retention and sampling-cadence defects remain open. The M38 scientific route remains halted at that dependency. No repeated generic capability audit, extra wrapper or qualification is selected. Numeric limits, independent scientific A/B/control/input custody and separate execution admission remain unchanged.
