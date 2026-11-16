# Native field state across a causal diamond

For the unchanged accepted Gaussian attachment, interchanging the two specified incomparable births changes the transported field state. The same common endpoint and the same named marks give different variances of the field at $u$. Nevertheless, the prospectively fixed cover-link quadratic has expectation **2 in both histories**. Thus this attachment does not assign a unique full field state from this marked endpoint alone; this one diagnostic mean agrees on the specified diamond.

This is one conditional finite theorem and counterexample, with no modification of the native law, field formula, state, diagnostic or support.

The mathematical premises are the [prepared continuation ledger](native_source_readout_response.md), its [complete interval table](finite_interval_action_and_source_preparation.md), and the [three-pair Gaussian attachment](gaussian_field_transport_on_native_histories.md). The [spectral covariance result](spectral_covariance_under_native_growth.md) and [Stage 10 status](../coordination/SWARM_INTEGRATION_STATUS.md) concern different consistency questions. The [matter/source registration programme](../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md) identifies the use and physical limits of this finite comparison. No new literature result is needed for the algebra below.

## 1. Two supported histories at one decorated endpoint

The prepared prefix is $a\prec b$, with marks $(0,0)$ and counters $(1,0)$. The named suffix vertices satisfy
$$
 \operatorname{Past}(u)=\{a\},\qquad
 \operatorname{Past}(v)=\{a,b\},\qquad u\parallel v.
$$
The common strict relation matrix, in endpoint order $(a,b,u,v)$ and target-row/source-column convention, is
$$
 C=\begin{pmatrix}
 0&0&0&0\\
 1&0&0&0\\
 1&0&0&0\\
 1&1&0&0
 \end{pmatrix}.
$$
The covers are exactly $(a,b),(a,u),(b,v)$; $a\prec v$ is transitive and is not an extra cover.

Write $H_+$ for birth order $u,v$, and $H_-$ for $v,u$. The published attachment's first and later suffix roles are $x,y$. They are assigned before any endpoint transport:

| History | Actual $x$ | Actual $y$ | $I_x$ | $I_y$ |
| --- | --- | --- | --- | --- |
| $H_+$ | $u$ | $v$ | $\{a\}$ | $\{a,b\}$ |
| $H_-$ | $v$ | $u$ | $\{a,b\}$ | $\{a\}$ |

For $f_0=1/6,\ h_0=19/30,\ e=1/44$, their original structural weights are
$$
 P_0(H_+\text{ structurally})
 =f_0\frac{eh_0}{f_0}=\frac{19}{1320},
 \qquad
 P_0(H_-\text{ structurally})
 =h_0e=\frac{19}{1320}.
$$
The respective fourth-birth probabilities are $19/220$ and $1/44$. Both are supported rows of the original complete law.

All four named suffix-mark assignments are retained:

| Named marks $(m_u,m_v)$ | Chronological marks in $H_+$ | Chronological marks in $H_-$ | Original probability of each marked history |
| --- | --- | --- | --- |
| $(0,0)$ | $(0,0)$ | $(0,0)$ | $19/5280$ |
| $(0,1)$ | $(0,1)$ | $(1,0)$ | $19/5280$ |
| $(1,0)$ | $(1,0)$ | $(0,1)$ | $19/5280$ |
| $(1,1)$ | $(1,1)$ | $(1,1)$ | $19/5280$ |

In $H_+$, the first suffix birth yields counters $(2,0,0)$ on $(a,b,u)$; the second increments $a,b$. In $H_-$, the first yields $(2,1,0)$ on $(a,b,v)$; the second increments $a$. Both terminal counters, transported to $(a,b,u,v)$, are $(3,1,0,0)$, with no modulo-five wrap. The named terminal marks are $(0,0,m_u,m_v)$ in both. The prefix embedding, order, marks and counters therefore match.

The other 52 marked continuation histories remain in the original 60-history law. None is removed or reweighted. No two-history normalization, automorphism division, additional name multiplier or field feedback is introduced. The field comparisons below are conditional on each history; its probability is not a multiplier on its normalized Gaussian state.

## 2. Reapply the unchanged field formula before transport

Use the supplied $\beta>0$, the three canonical pairs on $L^2(\mathbb R^3)$, their common Schwartz domain, and
$$
 R=(Q_0,P_0,Q_x,P_x,Q_y,P_y)^T,\qquad
 [R_j,R_k]=iJ_{jk}\mathbf1,\qquad
 J=\bigoplus_{0,x,y}\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
$$
The common centered Gaussian state has symmetric quadrature covariance $I_6/2$. Its oscillator state is unchanged; the two induced states on the endpoint-labeled fields are what must be compared.

The fixed rule is
$$
 \phi_a=\sqrt\beta Q_0,\quad \phi_b=-\sqrt\beta P_0,\quad
 \phi_x=\sqrt\beta(Q_x-c_{xb}Q_0-c_{xa}P_0),
$$
$$
 \rho=c_{yx}-c_{yb}c_{xa}+c_{ya}c_{xb},\qquad
 \phi_y=\sqrt\beta(Q_y-c_{yb}Q_0-c_{ya}P_0-\rho P_x).
$$

For $H_+$, the bits are
$$
 (c_{xa},c_{xb},c_{ya},c_{yb},c_{yx})=(1,0,1,1,0),
 \qquad \rho_+=-1.
$$
Thus
$$
 \phi_u^+=\sqrt\beta(Q_x-P_0),\qquad
 \phi_v^+=\sqrt\beta(Q_y-Q_0-P_0+P_x).
$$
For $H_-$, the bits are $(1,1,1,0,0)$, so $\rho_-=1$, and after terminal transport,
$$
 \phi_u^-=\sqrt\beta(Q_y-P_0-P_x),\qquad
 \phi_v^-=\sqrt\beta(Q_x-Q_0-P_0).
$$
The $a,b$ operators are identical in both histories.

Writing the transported field columns as $\phi^\pm=\sqrt\beta L_\pm R$, the coefficient matrices are
$$
 L_+=\begin{pmatrix}
 1&0&0&0&0&0\\
 0&-1&0&0&0&0\\
 0&-1&1&0&0&0\\
 -1&-1&0&1&1&0
 \end{pmatrix},\qquad
 L_-=\begin{pmatrix}
 1&0&0&0&0&0\\
 0&-1&0&0&0&0\\
 0&-1&0&-1&1&0\\
 -1&-1&1&0&0&0
 \end{pmatrix}.
$$
These use birth-role oscillator coordinates in both representations. Transport only identifies the endpoint observables $(a,b,u,v)$; it does not replace the chronological construction by a new endpoint-based field rule.

## 3. Common commutator, unequal covariance and Weyl laws

Direct multiplication gives
$$
 K:=L_+JL_+^T=L_-JL_-^T=C-C^T
 =\begin{pmatrix}
 0&-1&-1&-1\\
 1&0&0&-1\\
 1&0&0&0\\
 1&1&0&0
 \end{pmatrix}.
$$
Consequently $D_+=D_-=\beta K$, with $[\phi_r^\pm,\phi_s^\pm]=i\beta K_{rs}\mathbf1$. For example, in $H_+$ the shared pair contributes $i\beta$ to $[\phi_v,\phi_u]$, and $P_x$ against $Q_x$ contributes $-i\beta$. In $H_-$, the chronological commutator $[\phi_u,\phi_v]$ instead has contributions $-i\beta$ and $i\beta$. The incomparable fields commute in each case. Also $[\phi_a,\phi_b]=-i\beta$, fixing the target-first sign.

The two real Gram matrices are
$$
 M_+:=L_+L_+^T=
 \begin{pmatrix}
 1&0&0&-1\\
 0&1&1&1\\
 0&1&2&1\\
 -1&1&1&4
 \end{pmatrix},\qquad
 M_-:=L_-L_-^T=
 \begin{pmatrix}
 1&0&0&-1\\
 0&1&1&1\\
 0&1&3&1\\
 -1&1&1&3
 \end{pmatrix}.
$$
Hence the symmetric covariances and ordered second moments are exactly
$$
 V_\pm=\frac\beta2M_\pm,\qquad
 W_\pm=\frac\beta2(M_\pm+iK).
$$
For an explicit common template,
$$
 W_\pm=\frac\beta2
 \begin{pmatrix}
 1&-i&-i&-1-i\\
 i&1&1&1-i\\
 i&1&d_u^\pm&1\\
 -1+i&1+i&1&d_v^\pm
 \end{pmatrix},
 \qquad (d_u^+,d_v^+)=(2,4),\quad(d_u^-,d_v^-)=(3,3).
$$
The displayed construction ensures positivity:
$W_\pm=\frac\beta2L_\pm(I_6+iJ)L_\pm^T$.
Both extend the same prepared $W_2$. No fresh spectral vacuum or commutator-kernel quotient has been imposed; the accepted retained-fluctuation representation is used throughout.

For real $t=(t_a,t_b,t_u,t_v)^T$, let
$\mathcal W_\pm(t)=\exp(i\,t^T\phi^\pm)$. Their complete centered Gaussian characteristic laws are
$$
 \omega(\mathcal W_\pm(t))
 =\exp\!\left[-\frac\beta4\,t^TM_\pm t\right],
$$
with
$$
 t^TM_\pm t=
 t_a^2+t_b^2+d_u^\pm t_u^2+d_v^\pm t_v^2
 -2t_at_v+2t_bt_u+2t_bt_v+2t_ut_v.
$$
Products have the same Weyl phase,
$$
 \mathcal W_\pm(t)\mathcal W_\pm(s)
 =e^{-i\beta t^TKs/2}\mathcal W_\pm(t+s).
$$
These equations specify both state functionals on the same endpoint-labeled Weyl relations.

**Field-state verdict: unequal.** In fact
$$
 V_+-V_-=\frac\beta2\operatorname{diag}(0,0,-1,1).
$$
For the real smearing $t=e_u=(0,0,1,0)^T$,
$$
 \omega(\mathcal W_+(e_u))=e^{-\beta/2}
 \ne e^{-3\beta/4}=\omega(\mathcal W_-(e_u))
 \quad(\beta>0).
$$
Equivalently $\omega((\phi_u^+)^2)=\beta$ while
$\omega((\phi_u^-)^2)=3\beta/2$. Thus a bounded Weyl observable already distinguishes the induced states. Native scalar diamond-weight equality and branchwise preservation of old fields do not remove this endpoint-state ambiguity.

## 4. The fixed diagnostic nevertheless has the same expectation

Keep precisely the preselected positive form
$$
 \mathcal Q_C^\pm=\frac1{2\beta}
 \left[(\phi_b-\phi_a)^2+(\phi_u^\pm-\phi_a)^2
                  +(\phi_v^\pm-\phi_b)^2\right].
$$
Each difference is a real linear field on the common domain. Its squared expectation is
$$
 \omega((\phi_s^\pm-\phi_r^\pm)^2)
 =V^\pm_{ss}+V^\pm_{rr}-2V^\pm_{rs}.
$$
The antisymmetric second-moment part cancels. All moments are finite in the specified Gaussian state.

| Cover | Squared-difference expectation in $H_+$ | In $H_-$ | Contribution to $q_C^+$ | To $q_C^-$ |
| --- | --- | --- | --- | --- |
| $(a,b)$ | $\beta$ | $\beta$ | $1/2$ | $1/2$ |
| $(a,u)$ | $3\beta/2$ | $2\beta$ | $3/4$ | $1$ |
| $(b,v)$ | $3\beta/2$ | $\beta$ | $3/4$ | $1/2$ |

For example, the coefficient vectors of $(\phi_u-\phi_a)/\sqrt\beta$ have squared norms 3 and 4; those of $(\phi_v-\phi_b)/\sqrt\beta$ have squared norms 3 and 2. Multiplication by the quadrature variance $1/2$ gives the table.

**Diagnostic-expectation verdict: equal.**
$$
 q_C^+:=\omega(\mathcal Q_C^+)
 =\frac{\beta+3\beta/2+3\beta/2}{2\beta}=2,\qquad
 q_C^-:=\omega(\mathcal Q_C^-)
 =\frac{\beta+2\beta+\beta}{2\beta}=2.
$$
The shift $-\beta/2$ in the $u$ variance cancels the $+\beta/2$ shift at $v$ in this particular sum. Both suffix vertices occur in exactly one selected cover, and all contributing cross covariances coincide. This explains the equality without inferring equality of the states.

The formula is independent of suffix marks, so both verdicts hold separately for all four matched mark assignments with their original weights. This is equality of the one specified mean. Equality of diagnostic operators, full diagnostic outcome laws, other observables or other diamonds has not been established or asserted.

## 5. Registration and physical scope

| Object | Finite result | Consequence for this comparison |
| --- | --- | --- |
| Complete endpoint-labeled Gaussian field state | Unequal under the specified swap | The current attachment requires the birth schedule as additional registration; it does not descend to this marked endpoint alone. |
| Fixed cover-link diagnostic expectation | Exactly 2 on both histories, for every matched mark assignment | This one scalar mean agrees at this endpoint under this swap. No general endpoint-descent theorem follows. |

The single common oscillator state, preservation of old operators along each branch and preservation of native record/counter identities all remain intact. The obstruction concerns how the chronological field formula induces a state on endpoint-labeled observables. It is distinct from the earlier [positive-spectral old-marginal obstruction](spectral_covariance_under_native_growth.md) and the [Stage 10 scalar-weight failure](../coordination/SWARM_INTEGRATION_STATUS.md) under another feedback kernel. The result does not prove that the entire birth schedule is a minimal sufficient register.

For the [GD-01 matter/source programme](../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md), the result specifies what can be entered in a matter/source register from this attachment: a history-conditioned field state, and a cover-link mean that happens to agree on this pair. The Gaussian, canonical pairs, $\beta$, field coefficients and the diagnostic itself remain supplied choices. A native physical source interpretation still needs justified dynamics and persistence, a stress/energy assignment with the appropriate balance law, coupling/backreaction, operational readout and dimensional calibration. None is supplied by this diagnostic's positivity or by its value 2. The programme's conventional-GR baseline (Option B) and metric-as-record interpretation (Status M) are unchanged.

The conclusion is limited to these two verdicts for the specified diamond and the fixed diagnostic. It supplies no repaired field assignment, additional diamond, general endpoint-descent theorem, classification of intertwiners or continuum extrapolation.

## Reviewed basis and consultation scope

DET Quantum Relativity supplied the finite derivation. DET Energy Research conducted a distinct, nonblind scientific review of the frozen result and returned PASS within the stated scope, with no correction required. The review reconstructed the actual birth roles and endpoint transport, native support and counters, coefficient and commutator matrices, symmetric and ordered covariances, positivity, Weyl laws, the bounded state witness, and the separate fixed-diagnostic expectation. The earlier DET Relational State Research review admitted the prospective test's design; it did not decide these scientific outcomes. Author-side checks and reviewer-side internal assistance were not counted as separate formal reviews.

The original-law ledger, full interval table and accepted Gaussian construction were read in full for the scientific review and reused at their existing scope. The author read the spectral covariance article in full; the distinct reviewer used its opening construction and marginal contract, and its final zero-mode, decision and scope sections. The review did not rely on the partly truncated middle spectral proof for this new calculation. Both inspected the integration inventory for the different Stage 10 kernel and the status of imported drafts. The geometry/gravity plan was consulted only at lines 1–45 and 165–265 of the accepted 371-line version, covering the mapping boundary, GD-01 source consumer and physical obligations. Those consultations provide context and delimit this result; they do not certify other imported drafts or supply a paper-wide review or a novelty theorem.

The finite comparison uses the supplied Gaussian representation directly. The inherited [Gaussian](gaussian_field_transport_on_native_histories.md) and [spectral](spectral_covariance_under_native_growth.md) articles retain their precise Johnston v2 source and indexing scope. No new primary-literature theorem or source snapshot was required for the diamond result, and this public assembly claims no new primary-source inspection.
