# Prospective Protocol — Upstream Pair-Kernel Bridge (Silent Activity, Composition, and Record Stability)

31 October 2026. **PROSPECTIVE_PROTOCOL_FROZEN; CONDITIONAL_MATHEMATICAL_BRIDGE_ONLY.**

This protocol is frozen prior to proof assembly and witness verification in accordance with repository governance ([`GOVERNANCE.md`](../../../GOVERNANCE.md)) and the prospective-freeze requirement recorded in [`NEXT_STEPS.md`](../../../NEXT_STEPS.md). No existing accepted source, registry entry, core module, or branch (`main`, `ret`, `qr-05-bridge`) is modified by this study.

---

## 1. Research Question and Scope

Downstream work already establishes that an admitted complex, Hermitian, biadditive, normalized, strongly positive pair-kernel \(D\) canonically yields a finite Hilbert space \(\mathcal H_D\) and Born-form weights \(K(r)=\|P_r\psi\|_D^2\) on any declared exactly decoherent partition ([`DERIVATION.md`](../t8-q-strict-derivation-2026-09-12/DERIVATION.md)). Upstream composition audits ([RI-20](../../coordination/QR_COMPOSITION_PREMISE_PLAN.md), [RI-21](../../coordination/QR_FINITE_COPY_WITNESS_PLAN.md), [RI-22](../../coordination/QR_COMPOSITION_INDEPENDENCE_PLAN.md)) isolate three unresolved obligations between DET's native record/activity operations and that admitted pair-kernel structure:

1. **Full event-pair composition versus scalar independence:** [RI-22](../../coordination/QR_COMPOSITION_INDEPENDENCE_PLAN.md) proves that unit, associativity, swap covariance, complex whole-carrier marginals, rectangular scalar independence, and real-incidence naturality still admit the non-tensor product \(D\star E = R\otimes S + i(J\otimes S + R\otimes K)\), which drops \(-J\otimes K\) and admits non-PSD kernels.
2. **Exact decoherence versus one-experiment additivity:** Single-experiment additivity \(\mu_D(A_r\sqcup A_s)=\mu_D(A_r)+\mu_D(A_s)\) requires only \(\operatorname{Re} D(A_r,A_s)=0\), leaving purely imaginary cross-relations \(D(A_r,A_s)=it_{rs}\) intact even on positive-definite kernels.
3. **Interference resource admission and separation from classical active residuals:** [RI-21](../../coordination/QR_FINITE_COPY_WITNESS_PLAN.md) characterizes \(D\succeq 0\) via \(n\) candidate copies and a supplied rank-one signed seed \(B=bb^\dagger\) (\(b=(1,-1,1)^T\), \(\operatorname{Tr} B=3\)), while recent native constructions demonstrate active state-to-growth feedback on \(\mathbb R_+^2\) ([`native_active_residual_v1.md`](../../track_b/native_active_residual_v1.md)), commuting classical branch constraints on \(\mathbb R_+^d\) ([`finite_homogeneous_compensation.md`](../../track_b/finite_homogeneous_compensation.md)), and exact classical counter equality \(p_{\mathrm C}(h,y)=p_{\mathrm Q}(h,y)\) ([`finite_pair_incidence_register.md`](../../observables/finite_pair_incidence_register.md)).

**Focused prospective question:**
> *Within the pre-PSD complex Hermitian biadditive event calculus, which minimal operational rules for silent residual activity ([`RECORD_PROCESS_CONTRACT.md`](../../track_b/RECORD_PROCESS_CONTRACT.md)), independent composition, and classical Boolean grouping of committed records force (i) the ordinary event-pair tensor law \(D\otimes E\), (ii) complete vanishing of cross-cell relations \(D(A_r,A_s)=0\), and (iii) a two-cell recordable principal-minor witness generated from a classical diagonal state—and what exact operational signatures separate this structure from every finite-dimensional classical simplicial residual cone \(\Delta_d\subset\mathbb R_+^d\)?*

---

## 2. Frozen Mathematical Objects and Domains

1. **Pre-PSD candidate space:** For each finite carrier \(\Omega_n=\{0,\dots,n-1\}\) (\(n\ge 1\)), let \(\operatorname{Herm}_n(\mathbb C)\) be decomposed into real symmetric and real skew-symmetric parts \(D=R+iJ\) (\(R^T=R\), \(J^T=-J\)), with biadditive extension \(D(A,B)=\chi_A^\dagger D\chi_B\), scalar event weight \(\mu_D(A)=D(A,A)=\chi_A^T R\chi_A\), and total-entry normalization \(M(D)=\mathbf 1_n^\dagger D\mathbf 1_n = \mathbf 1_n^T R\mathbf 1_n = 1\). Weak positivity requires \(\mu_D(A)\ge 0\) for all \(A\subseteq\Omega_n\); PSD is **not** assumed at input.
2. **Silent residual evolutions (`evolve_residual`):** Same-carrier transformations acting prior to record commitment without appending committed events ([`RECORD_PROCESS_CONTRACT.md`](../../track_b/RECORD_PROCESS_CONTRACT.md)). On the four-atom two-cell carrier \(\Omega_4=\{0,1,2,3\}\) with partition \(\mathcal P_4=\{\{0,1\},\{2,3\}\}\), the reference silent generators are the mass- and recordability-preserving lifted controls \(S_U(D)=W_U D W_U^\dagger\) (\(W_U=\operatorname{diag}(U,ZUZ)\), \(Z=\operatorname{diag}(1,-1)\)) from [RI-08b](../t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md), specifically \(S_H\) and \(S_P\) (\(P=\operatorname{diag}(1,i)\)).
3. **Classical active-residual comparator family:** All finite-dimensional nonnegative cones \(\mathbb R_+^d\) (\(d\ge 1\)) with normalized simplex \(\Delta_d=\{\rho\ge 0:\mathbf 1_d^T\rho=1\}\), column-stochastic silent updates \(S\in\mathrm{Stoch}_d\), and bounded binary readout effects \(e_0,e_1\in[0,1]^d\), \(e_0+e_1=\mathbf 1_d\).

---

## 3. Pre-Registered Targets and Required Countermodels

The analysis and self-contained verification script (`check.py`) must establish or refute the following three paired propositions, retaining explicit countermodels whenever a load-bearing premise is omitted:

### Target T1 — Classification of Real-Incidence-Natural Composition and Selection of \(D\otimes E\)
- **Prospective theorem:** Classify *all* real-bilinear Hermitian composition families \(\{\odot_{n,k}:\operatorname{Herm}_n(\mathbb C)\times\operatorname{Herm}_k(\mathbb C)\to\operatorname{Herm}_{nk}(\mathbb C)\}_{n,k\ge 1}\) satisfying unit (\([1]\odot D=D=D\odot[1]\)) and real-incidence naturality (\((UDU^T)\odot(VEV^T)=(U\otimes V)(D\odot E)(U\otimes V)^T\) for all real rectangular \(U,V\)). Determine the exact parameter subinterval preserving weak Boolean positivity on individually PSD inputs, and test whether **independent silent-control interchange** \((W_1\otimes W_2)(D\odot E)(W_1\otimes W_2)^\dagger = (W_1 D W_1^\dagger)\odot(W_2 E W_2^\dagger)\) for \(S_P\) (or positivity of local product-cell weights under \(S_P\otimes S_P\)) uniquely selects \(D\otimes E\), starting solely from purely real PSD inputs.
- **Required deletion countermodel:** Verify that deleting the phase-bearing silent control \(S_P\) while retaining all real silent controls (\(S_H,S_Z\)) and all real incidence maps leaves a non-singleton interval of alternative associative composition laws (including RI-22's \(\star\)) unexcluded on all PSD inputs.

### Target T2 — Composite Committed-Record Grouping and Exact Cross-Relation Vanishing
- **Prospective theorem:** For any \(k\)-cell partition \(\mathcal P=\{A_0,\dots,A_{k-1}\}\) that is additive on one copy of \(D\), determine the exact discrepancy between coarse-grained coincidence weights \(\mu_{D\odot_\alpha D}((A_r\times A_r)\sqcup(A_s\times A_s))\) and \(\mu_{D\odot_\alpha D}(A_r\times A_r)+\mu_{D\odot_\alpha D}(A_s\times A_s)\) across the classified composition family \(\odot_\alpha\). Prove when classical Boolean grouping of committed product records forces \(D(A_r,A_s)=0\) for all \(r\ne s\).
- **Required countermodels and boundaries:**
  1. Exhibit a strictly positive-definite normalized kernel \(D\succ 0\) whose single-copy partition is additive (\(\operatorname{Re} D(A_0,A_1)=0\)) yet fails orthogonality (\(D(A_0,A_1)\ne 0\)).
  2. Verify that under RI-22's \(\star\)-product (\(\alpha=0\)), all finite-copy Boolean groupings of \(\mathcal P^{\times m}\) remain additive despite \(D(A_0,A_1)\ne 0\), demonstrating that Target T1 is load-bearing for Target T2.
  3. Distinguish cell-summed decoherence \(D(A_r,A_s)=0\) from internal zero-sum cross-block payload \(cZ\) ([RI-08d](../t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md)).

### Target T3 — Classical-to-Seed Principal-Minor Lift and Classical Conical Separation
- **Prospective theorem:**
  1. Test whether applying one silent control \(S_H\) to the classical diagonal state \(D_{+Z}=\operatorname{diag}(1/2,0,1/2,0)\in\mathrm{Diag}_+\) produces a normalized, trace-one, two-cell recordable kernel \(D_{+X}=S_H(D_{+Z})\) whose composite \(D^{\otimes n}\otimes D_{+X}\) yields exact positive multiples of all \(2^n-1\) principal minors \(\det(D_I)\) via ordinary Boolean events, characterizing \(D\succeq 0\) without RI-21's unrecordable trace-three seed.
  2. Establish what separates pair-kernel silent activity from every finite-dimensional classical simplex \(\Delta_d\subset\mathbb R_+^d\):
     - On arbitrary \(d\ge 1\) for extreme preparations under reversible silent evolutions;
     - Explicitly exhibit a mixed-state classical permutation counterexample on \(\Delta_6\) showing why single-system \((1,1/2,0)\) sequential transitions alone do **not** rule out hidden classical dimensions when purity is dropped;
     - Prove a dimension-free (\(d_A,d_B\ge 1\) arbitrary, mixed preparations and noisy effects allowed) bipartite Bell-CHSH separation using **exact rational** local silent controls on the 16-label RI-08d coupled pair-kernel state.

---

## 4. Verification Contract and Claim-Status Boundaries

1. **Exact arithmetic only:** `check.py` must use only the Python standard library (`fractions.Fraction`, `unittest`, and an exact Gaussian-rational type), with zero floating-point approximations or external package imports, and pass identically under both `python3 -B` and `python3 -B -O`.
2. **Governance and non-smuggling discipline:**
   - All results are **conditional mathematical theorems and countermodels** (`TH-DET` / `MATH` at declared scope).
   - Complex scalars \(\mathbb C\), the Hermitian biadditive candidate space, availability of \(S_H,S_P\), independent multi-copy preparation, and composite Boolean event positivity remain explicit premises; none is claimed to be derived from bare causal posets \((V,\prec,r)\) alone.
   - No claim is made regarding native growth-law selection \(q(P,r,S)\), physical time, rest mass, Lorentzian geometry, gravity (Option B unchanged), ontological openness (Status M unchanged), or empirical validation.
