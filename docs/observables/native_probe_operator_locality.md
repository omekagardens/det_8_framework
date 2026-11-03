# Native input locality and supplied probe operation locality

GDM059, accepted conditional result, 3 November 2026. Exact original fair-q Part A and [active residual law](../track_b/native_active_residual_v1.md) with [precursor payloads](../track_b/native_precursor_payloads_v1.md) are inherited premises; empty q=1, singleton empty/full q=2/3,1/3. Nonselective M(0) is not identity. No changed-mark Part B.

## 1. Fixed objects and accepted native premises

Let C be an admitted binary-marked strict native order with fewer than four vertices. For every actual downward ideal S and newborn bit b, the accepted active instrument is

\[
B_{C,S,b}=\frac{q_C(S)}2 M(r_C(S)),
\qquad
M(r)=\frac12\begin{pmatrix}1+r+t&1-r-t\\1+r-t&1-r+t\end{pmatrix},
\quad t=\frac12.
\]

Use precisely the source's q and r, old-mark restrictions, full ideal support, immutable records, relabelings and four-birth horizon. With e=(1,1)^T and u=(1/2,1/2)^T, the accepted active-law result supplies

\[
B_{C,S,b}>0\text{ entrywise},\quad
\sum_{S,b}e^TB_{C,S,b}=e^T,\quad
\sum_{S,b}B_{C,S,b}=M(0),\quad
B_{C,S,b}u=\frac{q_C(S)}2u,
\]

and equality of every complete unnormalized native diamond and transported suffix. These accepted native statements are inputs to the extension proof, not a new derivation of the underlying law.

Supply probes H_A=H_B=C², their fixed computational bases and tensor partition. A general source/probe input is a pair of positive operator blocks rho_s on H_A tensor H_B, s in {0,1}; its total mass is sum_s Tr rho_s. The source is classical. Each block may have arbitrary A|B entanglement and may be extended to any retained reference R. No coherent source off-diagonal block is required by the domain.

Let K0 be the singleton-zero marked precursor class. For Q=J,L put

\[
G_J=CZ=\operatorname{diag}(1,1,1,-1),\qquad
G_L=Z_A\otimes Z_B,
\]

and U^Q_(K,b)=G_Q when K=K0 and b=0, otherwise identity. The branch is

\[
[\Phi^Q_{C,S,b}(\rho)]_{s'}
=\sum_s B_{C,S,b}(s'\mid s)
U^Q_{K,b}\rho_s(U^Q_{K,b})^\dagger.
\tag{1}
\]

The **precursor and newborn bit**, not the instantaneous residual index s, select U. The native residual can influence native record probabilities through B on general inputs. Probes do not feed back into that native marginal. The Hilbert/Born/unitary framework, partition, gates, preparation and later measurement are supplied assumptions.

## 2. Stage 1: full-cone compatibility through four births

### 2.1 Complete positivity, reference extension and normalization

Embed the classical source in its diagonal basis |s>. For a fixed native branch, a Kraus representation of (1) restricted to this block algebra is

\[
K_{s's}=\sqrt{B_{C,S,b}(s'\mid s)}\,
|s'\rangle\langle s|\otimes U^Q_{K,b}.
\]

Every coefficient is nonnegative. Summing K rho K† over s',s gives exactly (1). Tensoring each Kraus operator with I_R proves complete positivity for every retained quantum reference, including source/probe/reference correlations allowed by the block cone. This representation is a CP realization of the declared classical-source instrument, not a claim that the native source is a coherent qubit.

For arbitrary positive blocks rho_s on ABR, unitary trace invariance gives

\[
\sum_{S,b,s'}\operatorname{Tr}[\Phi^Q_{C,S,b}(\rho)]_{s'}
=\sum_s\left(\sum_{S,b,s'}B_{C,S,b}(s'\mid s)\right)\operatorname{Tr}\rho_s
=\sum_s\operatorname{Tr}\rho_s.
\]

This proves complete trace normalization on the whole cone. Each native ideal/bit branch has positive mass for every nonzero positive input, since its native column sums are strictly positive and at least one input block has positive trace. All declared branches therefore remain eligible; no state or failure branch is removed.

### 2.2 Exact native marginal, records and relabeling

More strongly, keeping any reference R,

\[
\operatorname{Tr}_{AB}[\Phi^Q_{C,S,b}(\rho)]_{s'}
=\sum_s B_{C,S,b}(s'\mid s)\operatorname{Tr}_{AB}\rho_s.
\tag{2}
\]

Thus the native/reference marginal is precisely the original B instrument for every correlated input. For scalar native probabilities, trace R as well. There is no probe-to-source dynamical feedback in the declared construction.

The native branch adjoins the same maximal vertex over the same actual ideal, with the same newborn bit; it never changes old marks or order. B retains its accepted allowed parent/precursor dependence. U reads only the intrinsic marked precursor class and newborn bit. It acquires no access to marks outside a proper precursor or to a future endpoint.

Under a marked-parent relabeling, B transports by the accepted covariance and K is unchanged as an intrinsic class. The residual and probe coordinate actions are stipulated trivial. Therefore (1) is equivariant as a complete map. Probe labels A,B are not vertex names or inferred spatial locations.

### 2.3 All unnormalized diamonds, including correlated inputs

Consider any admitted incomparable-birth diamond, with any old marking, both actual ideals, both bit choices, and the source's transported endpoint identification. Denote the two branch matrices on one side by B_1,B_2 and on the other by B'_1,B'_2. The accepted full native identity is

\[
B_2B_1=B'_2B'_1.
\tag{3}
\]

Each birth's actual strict precursor excludes the other new vertex. Its intrinsic marked precursor class and its own newborn bit are therefore the same in either birth ordering. This includes equal precursors and a full precursor becoming proper after the other birth. The gates on the two sides are the same two gate factors in reverse order.

For either fixed Q, every gate belongs to {I,G_Q}; these matrices commute. For an arbitrary block input on ABR, composition gives

\[
[\Phi_2\Phi_1(\rho)]_t
=\sum_s (B_2B_1)(t\mid s)
(U_2U_1\otimes I_R)\rho_s(U_2U_1\otimes I_R)^\dagger.
\tag{4}
\]

Here the sum over the intermediate classical source index produces the full native matrix product. It can be taken independently of the probe factors because U does not depend on that source index. Equations (3), (4), the transported precursor identities, and U_2U_1=U_1U_2 equate the complete two maps. No scalar normalization, prepared-state restriction, source/probe factorization or projection onto a marginal is used.

### 2.4 Transported suffixes and stage-1 conclusion

After the diamond, the marked parents coincide under the prescribed transport. Every later selected native matrix and marked precursor class is consequently the same after transport, including suffix ideals containing either swapped vertex. Each later full branch map therefore agrees, and composing the entire transported suffix preserves (4). Prefix composition likewise preserves equality. The accepted natural-history swap construction then carries these adjacent identities through every required history in the original four-birth domain.

**Stage 1 passes for both J and L.** The combined maps are CP with arbitrary reference, completely normalized with full branch support, preserve the native marginal and record/mark restrictions, and satisfy all required relabelings, full unnormalized diamonds and suffixes. Only after this proof was completed was the following fixed observation calculation undertaken.

## 3. Stage 2: all eight actual two-birth histories

The prescribed preparation is rho_s=u_s tau_+, where tau_+=|++><++|. The first birth has empty precursor and never triggers a gate. At the second birth, denote its ideal by E for empty and F for the full singleton. Let i be the first bit and j the second bit. A complete naturally labeled history is gamma=(i,E/F,j).

Using the accepted uniform anchor, B_gamma u=w_gamma u. The full weights and trigger indicators are:

| gamma | Native weight w_gamma | Trigger t_gamma |
| --- | ---: | ---: |
| (0,E,0) | 1/6 | 0 |
| (0,E,1) | 1/6 | 0 |
| (1,E,0) | 1/6 | 0 |
| (1,E,1) | 1/6 | 0 |
| (0,F,0) | 1/12 | 1 |
| (0,F,1) | 1/12 | 0 |
| (1,F,0) | 1/12 | 0 |
| (1,F,1) | 1/12 | 0 |

Each E weight is (1/2)(2/3)(1/2); each F weight is (1/2)(1/3)(1/2). The sum is 4/6+4/12=1. The mixed-mark antichain histories (0,E,1) and (1,E,0) remain distinct natural histories; no quotient removes their multiplicities. All native histories have positive weight. The only trigger is the chain with both marks zero.

Define

\[
\tau_- = |--\rangle\langle--|,
\qquad \tau_g=|g\rangle\langle g|,
\qquad |g\rangle=CZ|++\rangle.
\]

The entire subnormalized block output for each history and each source index is

\[
[\Phi^Q_\gamma(\rho_{\rm init})]_s=\frac{w_\gamma}{2}\,\tau^Q_{t_\gamma},
\quad
\tau^J_0=\tau^L_0=\tau_+,
\quad \tau^J_1=\tau_g,
\quad \tau^L_1=\tau_-.
\tag{5}
\]

## 4. Unselected probe states and exact certificates

Summing (5) gives rho_J=(11/12)tau_+ +(1/12)tau_g and rho_L=(11/12)tau_+ +(1/12)tau_-. The trigger contributes 1/12; all seven nontrigger histories together contribute 11/12. Nothing is conditioned on the trigger or on detector success.

### 4.1 J is entangled

In computational basis (00,01,10,11),

\[
\bar\rho_J=\frac1{24}
\begin{pmatrix}
6&6&6&5\\6&6&6&5\\6&6&6&5\\5&5&5&6
\end{pmatrix},
\qquad
\bar\rho_J^{T_B}=\frac1{24}
\begin{pmatrix}
6&6&6&6\\6&6&5&5\\6&5&6&5\\6&5&5&6
\end{pmatrix}.
\]

Let

\[
|v\rangle=\frac{-3|00\rangle+|01\rangle+|10\rangle+|11\rangle}{\sqrt{12}}.
\]

It is normalized. Its quadratic form is

\[
\langle v|\bar\rho_J^{T_B}|v\rangle
=\frac{54-108+48}{24\cdot12}
=-\frac1{48}.
\tag{6}
\]

For any separable state sum_l p_l alpha_l tensor beta_l, the partial transpose is sum_l p_l alpha_l tensor beta_l^T, which is positive. The negative form (6) therefore proves entanglement. No numerical eigensolver, necessary-and-sufficient classification theorem or postselected state is needed.

### 4.2 L is separable

The displayed mixture

\[
\bar\rho_L=\frac{11}{12}
(|+\rangle\langle+|)_A\otimes(|+\rangle\langle+|)_B
+\frac1{12}
(|-\rangle\langle-|)_A\otimes(|-\rangle\langle-|)_B
\tag{7}
\]

is an explicit convex product decomposition. Its coefficients are positive and sum to one. Classical correlation between probes is allowed; entanglement is absent.

### 4.3 A fixed explicit witness for the actual states

Set W=(|v><v|)^(T_B). For every separable state sigma, Tr(W sigma)>=0 by the same positivity argument. Its Pauli expansion is

\[
W=\frac14\left[
I\otimes I
-\frac13(X\otimes I+I\otimes X+X\otimes X)
+\frac23(Z\otimes I+I\otimes Z+Z\otimes Z)
-\frac23(X\otimes Z+Z\otimes X+Y\otimes Y)
\right].
\tag{8}
\]

This follows by expanding |v><v| in Pauli products; partial transposition reverses the second-factor Y sign. Equation (6) gives Tr(W rho_J)=−1/48. For the two product components of L, the expectations are zero on |++> and 1/3 on |-->; hence Tr(W rho_L)=+1/36. Both are expectations of the unselected normalized states.

## 5. Complete setting/outcome law, with all failures and zeros

Choose j,k independently uniformly from {X,Y,Z}. Local outcomes a,b belong to {+1,−1,perp}. The exact supplied effects are

\[
E_{a\mid j}=\frac{I+a\sigma_j}{4}\ (a=\pm1),
\qquad E_{\perp\mid j}=\frac I2,
\qquad\sum_aE_{a\mid j}=I.
\]

The detector factorizes between probes. Its efficiency is 1/2 at each site and is stipulated state-independent, not estimated by discarding failures.

For each of the three normalized pure probe states tau appearing in (5), write

\[
A_j(\tau)=\operatorname{Tr}[(\sigma_j\otimes I)\tau],\quad
B_k(\tau)=\operatorname{Tr}[(I\otimes\sigma_k)\tau],\quad
C_{jk}(\tau)=\operatorname{Tr}[(\sigma_j\otimes\sigma_k)\tau].
\]

All nonzero entries are listed here; every unlisted component is zero:

| tau | A | B | C |
| --- | --- | --- | --- |
| tau_+ | A_X=1 | B_X=1 | C_XX=1 |
| tau_- | A_X=−1 | B_X=−1 | C_XX=1 |
| tau_g | none | none | C_XZ=C_ZX=C_YY=1 |

For tau=tau^Q_(t_gamma), define the nine-outcome response at each setting pair by

\[
F_\tau(j,k,a,b)=
\begin{cases}
[1+aA_j+bB_k+abC_{jk}]/16,&a,b=\pm1,\\
[1+aA_j]/8,&a=\pm1,\ b=\perp,\\
[1+bB_k]/8,&a=\perp,\ b=\pm1,\\
1/4,&a=b=\perp.
\end{cases}
\tag{9}
\]

Then the complete joint law is

\[
\boxed{P_Q(\gamma,j,k,a,b)=\frac{w_\gamma}{9}
F_{\tau^Q_{t_\gamma}}(j,k,a,b).}
\tag{10}
\]

The eight-history table, three-state component table and (9)–(10) unambiguously specify every one of the 8×9×9 cells for each Q, including every zero, single failure and double failure. They are an exhaustive indexed formula, not a favorable-history or endpoint-only table. Histories are the actual natural encodings listed above, and no two histories are merged.

For any tau and setting pair, summing the four both-detected entries gives 1/4; the two A-detected/B-failure entries sum to 1/4; the two A-failure/B-detected entries sum to 1/4; double failure contributes 1/4. Thus sum_(a,b) F_tau=1, then sum_(j,k) 1/9=1 and sum_gamma w_gamma=1 prove normalization of the complete law.

The terminal measurement is supplied external fixed-prefix access after two native births. It is not a third native birth, and no native diamond across it is asserted. It consumes no change of preparation, trigger, gate, detector or native horizon.

## 6. Witness as a linear functional of unconditional probabilities

Define a recorded numerical code c(+1)=+1, c(−1)=−1, c(perp)=0. Every sum below is over all outcomes, including failures, with this code; no trial is discarded. Let

\[
T_Q=\sum_{\gamma,j,k,a,b}P_Q(\gamma,j,k,a,b)=1.
\]

For the unselected probe state, its local and joint Pauli expectations are recovered by the exact fixed-setting/loss relations

\[
\begin{aligned}
\mathcal A_j^Q&=6\sum_{\gamma,k,a,b}c(a)P_Q(\gamma,j,k,a,b),\\
\mathcal B_k^Q&=6\sum_{\gamma,j,a,b}c(b)P_Q(\gamma,j,k,a,b),\\
\mathcal C_{jk}^Q&=36\sum_{\gamma,a,b}c(a)c(b)P_Q(\gamma,j,k,a,b).
\end{aligned}
\tag{11}
\]

The factors are derived from the declared protocol: a chosen local setting has probability 1/3 and local signed-outcome operator sum_a c(a)E_(a|j)=sigma_j/2, giving 1/6 for a local expectation. A specified setting pair has probability 1/9 and the joint signed operator is sigma_j tensor sigma_k/4, giving 1/36. The coefficients in (11) correct known supplied design factors, not observed success fractions.

Consequently the exact witness functional of the complete unconditional law is

\[
\begin{aligned}
\mathcal W(P_Q)=\frac14\big[&T_Q
-\tfrac13(\mathcal A_X^Q+\mathcal B_X^Q+\mathcal C_{XX}^Q)\\
&+\tfrac23(\mathcal A_Z^Q+\mathcal B_Z^Q+\mathcal C_{ZZ}^Q)\\
&-\tfrac23(\mathcal C_{XZ}^Q+\mathcal C_{ZX}^Q+\mathcal C_{YY}^Q)\big].
\end{aligned}
\tag{12}
\]

Every quantity on the right is a linear sum of P_Q cells, so (12) is itself linear, with no detection or history conditioning. For J the nonzero required expectations are A_X=B_X=C_XX=11/12 and C_XZ=C_ZX=C_YY=1/12. This gives −1/48. For L, A_X=B_X=5/6 and C_XX=1, with the other required terms zero, giving +1/36. These checks agree with the state-space certificate.

This is exact population mathematics under a stipulated loss model. It supplies no finite-sample guarantee, error interval, physical calibration, acquisition or claim that real losses obey these effects.

## 7. What locality premise is missing

Three distinct properties are now separated by a concrete example:

1. **Allowed information:** the gate selector reads only the intrinsic marked precursor and newborn bit.
2. **Birth-order consistency:** the full combined maps satisfy the admitted diamonds and transported suffixes.
3. **Probe operation support:** CZ is a joint operation across the supplied A|B partition; the control Z_A tensor Z_B is a product operation.

The first two do not enforce the third's product/local restriction. The joint-phase instrument satisfies the native requirements and still produces the certified entangled unselected state. The resource is the supplied cross-probe gate, selected through a native record. It is not an entangling resource derived from the classical source residual, nor an example of entanglement arising solely from local interactions with a classical mediator.

A sufficient additional operational restriction for a finite local-mediation reading is to permit only probe operations with product Kraus factors A_nu tensor B_nu, selected or mixed using classical information, with initially separable probe blocks, no quantum communication and no direct joint gate. A product factor takes a product positive input to a product positive output; positive classical mixtures retain separability. This explains the finite control (7). It is a supplied restriction on operation support, not a consequence of the precursor-data restriction. No claim is made that every separable Kraus operation is physically implementable by a chosen local apparatus, nor is an all-model mediator theorem or necessity classification proved here.

The physical interpretation remains conditional. A|B is supplied; neither probe is identified as a mass, and neither native order nor gate commutation establishes spacelike separation. The Hilbert framework, gates and measurement rule are not derived from DET. There is no gravitational field, source equation, native action/time/length unit, reciprocal feedback, conservation/cost closure, empirical evidence or efficiency claim. Option B and Status M are unchanged.


## Provenance

Accepted GDM059 report c3cb9b0a6817a8673b6a36b0b492e0f0e51e7afb85c811dcb41378a909c2b8e4; independent review169ea440b346eb32692589eda96daab5286df343a9d06d0d42077427c6f67464; dispositionf3eda6862287f476f171b663a732c7f67df261e959f99cd452bbf0b56b09bcc5. Assembly awaits independent publication review. GDM057 heading-only Part-B overread, GDM054/prior timing and earlier publication/late-handoff qualifications remain permanent. No retrospective certification, software restart, execution authority or automatic successor.
