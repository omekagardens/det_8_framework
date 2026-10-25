# Mark-sensitive payloads: compatibility and information limits

This note states two independently reviewed conditional results for a proposed extension of the [admitted finite marked growth law](native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model). The original scalar-passive update remains unchanged. A supplied common qubit, mark-conditioned unitary updates and final preparation/readout can carry mark information while preserving complete marked diamonds. The same restricted final-only family can nevertheless lose distinctions present in the marked endpoint law.

The positive three-birth example and the negative two-birth example use their respective declared kernels and the same admitted structural law; their different scopes are explicit below. Compatibility does not select the coupling or provide physical access. [Passivity as an additional prescription](native_passivity_choice_v1.md) and the [observation/calibration boundary](native_observation_contract_v1.md) remain separate dependencies. No physical detector, selected law, larger-horizon theorem or empirical prediction is established.

# Part I — Compatible two-unitary updates

## Separate proposed object

Keep the actual admitted positive \(q(P,r,S)\), all eligible ideals, finite horizon \(N\), immutable marks, and positive intrinsic mark kernel \(p_b(K(S,r|_S))\). These retain their complete marked scalar diamonds, locality and equivariance. On a separately supplied common two-dimensional complex carrier, with fixed basis and trivial order-relabeling action, replace only the passive payload prescription by
\[
\mathcal B^{P,r}_{S,b}(X)
=q(P,r,S)p_b(K(S,r|_S))\,\mathcal C_b(X),
\qquad \mathcal C_b=\operatorname{Ad}_{U_b},\quad U_b^\dagger U_b=I.
\]
The two unitaries are fixed and depend only on the newborn bit. This is a proposed extension of the admitted intrinsic family, not its passive defining equation.

Each branch is completely positive with Kraus operator \(\sqrt{qp_b}\,U_b\), trace-nonincreasing, and has trace \(qp_b\operatorname{Tr}X\). The complete row preserves trace:
\[
\sum_{S,b}\mathcal B_{S,b}=\sum_b w_b\mathcal C_b,\qquad
w_b=\sum_Sq(P,r,S)p_b(K(S,r|_S))>0,\quad w_0+w_1=1.
\]
The channel reads no old marks beyond those already allowed in its scalar coefficient. The newborn bit is its branch label. Relabeling preserves the coefficient and acts trivially on the carrier.

## Complete marked-diamond characterization

For incomparable births over old ideals \(S,T\), bearing bits \(b,c\), their induced precursor classes are unchanged when the births are exchanged. The scalar \(p_b,p_c\) factors therefore commute; the supplied all-mark \(q\) diamond gives a common positive coefficient \(a\). The two full maps are
\[
a\,\mathcal C_c\mathcal C_b,\qquad a\,\mathcal C_b\mathcal C_c.
\]
Consequently \(\mathcal C_0\mathcal C_1=\mathcal C_1\mathcal C_0\) suffices for every complete marked diamond, including equal precursors, all old markings, and all four bit pairs.

It is also necessary whenever the admitted support contains a positive mixed-bit incomparable diamond. In the present all-ideal positive model starting empty, \(N\ge2\) supplies one: both births have empty precursor and different bits. Cancel its positive scalar coefficient. At \(N=1\) diamonds are vacuous; necessity must not be asserted there, or on restricted support lacking such a diamond.

For unitaries, channel commutation is equivalent to
\[
U_1U_0=e^{i\phi}U_0U_1.
\]
Indeed two conjugations coincide on all matrices iff the quotient of their unitaries commutes with every matrix, hence is a scalar phase. In dimension two, taking determinants forces \(e^{2i\phi}=1\): either commuting or anticommuting matrices are allowed. Exact matrix commutation alone would wrongly discard the second case. This classifies compatibility only within this fixed two-unitary ansatz.

After an adjacent incomparable swap, the marked parents agree under transport. Every subsequent precursor, old mark and scalar coefficient is transported identically, and its channel still depends only on its newborn bit. Composing that same suffix preserves full-map equality. Equal-precursor cases and suffixes containing either swapped vertex introduce no extra constraint. Tensoring every channel with the identity on any retained reference preserves the identities, including entangled inputs. This is equality of unnormalized maps, not merely traces.

## Classical law and the normalization distinction

For any admitted history \(h=((S_1,b_1),\ldots,(S_n,b_n))\),
\[
\mathcal B_h(X)=L_p(h)\mathcal C_{b_n}\cdots\mathcal C_{b_1}(X).
\]
Unitary trace preservation gives \(\operatorname{Tr}\mathcal B_h(\rho)=L_p(h)\) for every normalized input, also with retained reference. Thus every classical marked-record probability is unchanged relative to the passive model with the same supplied kernel. Different kernels need not have identical record laws.

An independently required identity nonselective map would instead force both \(\mathcal C_b=\mathrm{id}\). At any row, positive terms \(w_bU_b\rho U_b^\dagger\) summing to a pure state \(\rho\) must each have its one-dimensional support; their traces are \(w_b\). Thus each channel fixes every pure projector, hence every matrix by linearity. Equivalently each \(U_b\) is scalar. Trace normalization permits the proposed alternatives; identity-channel normalization removes them.

## A three-birth informative witness

Use the existing admitted three-birth prefix, unchanged actual \(q\), and constant intrinsic \(p_0=t,\ p_1=1-t\). Supply
\[
U_0=Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},
\qquad U_1=X_{\rm P}=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]
They anticommute, so their conjugation channels commute. Prepare the same \(\rho_0=|0\rangle\langle0|\) under both \(t=1/3\) and \(t=2/3\). After exactly three admitted births use the same binary test \(E_1=|1\rangle\langle1|\), \(E_0=I-E_1\), with the stipulated trace probability rule.

For a fixed bit word \(\mathbf b\) of any already admitted length \(n\le N\),
\[
\sum_{\mathbf S\ \mathrm{admitted\ for}\ \mathbf b}
\prod_{j=1}^{n}q(P_{j-1},r_{j-1},S_j)=1.
\]
Sum the last ideal first using its complete normalized \(q\) row, then repeat backwards. The intermediate rows may depend on all allowed earlier marks and structural choices; no mark-blind or independent structural law is substituted. Hence the marginal word probability is exactly \(\prod_jp_{b_j}\), and the complete unselected payload channel is
\[
(t\mathcal C_0+(1-t)\mathcal C_1)^n.
\]

On \(\rho_0\), a zero bit contributes only a basis-state phase; a one bit flips the basis state. The final basis bit is \(J=\sum_jb_j\bmod2\). Therefore
\[
\Pr_t(Y=1)=\Pr_t(J=1)=\frac{1-(2t-1)^n}{2},\qquad
\rho_{t,n}=\frac{1+(2t-1)^n}{2}|0\rangle\langle0|
+\frac{1-(2t-1)^n}{2}|1\rangle\langle1|.
\]
The parity formula follows from \(\mathbb E[(-1)^{\sum b_j}]=(t-(1-t))^n\). At \(n=3\),
\[
\Pr_{1/3}(Y=1)=14/27,\qquad
\Pr_{2/3}(Y=1)=13/27.
\]
The complementary probabilities are \(13/27\) and \(14/27\); binary-law total variation is \(1/27\). All structural histories were summed, with no chain-event or other postselection.

The witness has limits. At any positive even admitted length, \(t\) and \(1-t\) give the same displayed state and readout law; at odd length this particular exact-law map is injective on \(0<t<1\). No longer horizon is inferred. A different preparation can be blind: \(I/2\) remains unchanged for every \(t\). Nonzero contrast is not perfect single-outcome discrimination or a finite-sample guarantee.

## Permission versus selection

QR-OBS001 assumes \(\Phi_h=L_p(h)\mathrm{id}\). Here it is \(L_p(h)\mathcal C_h\): native marks are explicitly coupled into the payload. With the supplied preparation/test, the hypothetical observation kernel is \(K(1\mid h)=\mathbf1_{\{\text{odd newborn-bit parity}\}}\). The passive factorization theorem is not contradicted; its central update premise has been replaced.

The common carrier, fixed basis/relabeling convention, selected unitaries, preparation, three-birth access, and trace readout rule are additional premises. Coordinate changes must transform the preparation and test too. Birth count supplies no physical clock. Structural compatibility does not select these premises or establish a physical record-to-detector coupling. No Born-rule derivation, energy/action scale, quantum/gravity reconstruction, unique law, empirical-anomaly explanation or Boundary influence follows.

# Part II — Final-only information loss

## Exact factorization and comparison criterion

Retain the actual admitted \(q\), positive intrinsic family, supplied two-dimensional carrier, and fixed conjugation channels \(\mathcal C_b=\operatorname{Ad}_{U_b}\) with \(\mathcal C_0\mathcal C_1=\mathcal C_1\mathcal C_0\). Fix a common already admitted final horizon \(N\). For a history \(h\), let \(k(h)\) be its number of newborn ones. Then
\[
\mathcal B_h=L_p(h)\mathcal A_{k(h)},\qquad
\mathcal A_k=\mathcal C_1^k\mathcal C_0^{N-k}.
\]
Commutativity permits algebraic reordering of the payload maps, including those attached to comparable births. This does not reorder the causal history. Only the normalized conditional payload action factors through counts; the scalar history weight \(L_p(h)\) still contains the actual structural and mark probabilities.

Summing every complete history, without selection, gives
\[
\mathcal E_p=\sum_{k=0}^N\mu_p(k)\mathcal A_k,\qquad
\mu_p(k)=\sum_{h:k(h)=k}L_p(h).
\]
Complete normalized rows give \(\sum_k\mu_p(k)=1\). Consequently the exact criterion for two kernels to have identical complete final channels for this fixed pair is
\[
\mathcal E_p=\mathcal E_{p'}
\iff
\sum_k[\mu_p(k)-\mu_{p'}(k)]\mathcal A_k=0
\quad\text{as a linear map}.
\]
Equal count distributions suffice for every fixed commuting pair. They are not necessary for one chosen pair: linear dependencies among the \(\mathcal A_k\) can discard further information. A single prescribed readout may discard still more.

For any common kernel-independent normalized preparation \(\rho_{AR}\), including entanglement with a retained reference, the final state is
\((\mathcal E_p\otimes\mathrm{id}_R)(\rho_{AR})\). Equal channels give identical states and outcome laws for every fixed final measurement or instrument. Conversely, unequal channels differ on some density operator, since pure projectors span matrices; some final effect then detects the state difference. This is a mathematical existence statement, not a physical preparation/readout contract. The joint output including native records is excluded.

## Smallest count-matched endpoint counterexample

Choose the fixed final horizon \(N=2\), already within the admitted prefix. There is no intermediate observation. The first birth has \(q=1\). At the singleton parent the two actual ideal probabilities are
\[
q(\varnothing)=2/3,\qquad q(\text{full singleton})=1/3,
\]
independent of its mark. These are the complete eligible rows, not a restricted growth approximation.

Write \(t=p_0(\varnothing)\), \(u=p_0(\text{singleton marked }0)\), and \(v=p_0(\text{singleton marked }1)\). Define two kernels:
\[
p^{F}_0(K)=1/2\quad\text{for every }K,
\]
\[
(t,u,v)_{G}=(9/20,\ 23/30,\ 81/110),
\qquad p^{G}_0(K)=1/2\text{ for all other classes}.
\]
In each case \(p_1=1-p_0\). Every value is strictly between zero and one, is intrinsic to the marked precursor, and belongs to the admitted positive family. All three differing classes are reachable by the second decision. Values on other classes merely complete the definition inside the existing domain; no horizon or \(q\) is extended.

Let \(A_{ij}\) denote a two-vertex antichain with the indicated unordered marks; let \(C_{ij}\) denote a chain whose lower vertex has mark \(i\) and upper vertex mark \(j\). Their complete unlabelled marked endpoint probabilities are
\[
\begin{aligned}
P(A_{00})&=\tfrac23t^2,&
P(A_{01})&=\tfrac43t(1-t),&
P(A_{11})&=\tfrac23(1-t)^2,\\
P(C_{00})&=\tfrac13tu,&
P(C_{01})&=\tfrac13t(1-u),\\
P(C_{10})&=\tfrac13(1-t)v,&
P(C_{11})&=\tfrac13(1-t)(1-v).
\end{aligned}
\]
The mixed antichain has two distinct natural bit-order histories, \(01\) and \(10\), hence the factor two. Equal-mark antichains have one distinct encoding; duplicating their automorphic descriptions would overcount. The two oppositely marked chains are different endpoint events.

The probability in each kernel column is the displayed numerator divided by \(600\):

| Endpoint | Ones | Kernel \(F\): numerator | Kernel \(G\): numerator |
| --- | ---: | ---: | ---: |
| \(A_{00}\) | 0 | 100 | 81 |
| \(C_{00}\) | 0 | 50 | 69 |
| \(A_{01}\) | 1 | 200 | 198 |
| \(C_{01}\) | 1 | 50 | 21 |
| \(C_{10}\) | 1 | 50 | 81 |
| \(A_{11}\) | 2 | 100 | 121 |
| \(C_{11}\) | 2 | 50 | 29 |

Both columns sum to \(600\). Grouping by the number of ones gives, in both worlds,
\[
(\mu(0),\mu(1),\mu(2))=(150,300,150)/600=(1/4,1/2,1/4).
\]
Nevertheless the concrete marked endpoint event \(C_{00}\) has probabilities \(50/600\) and \(69/600\), a nonzero difference \(19/600\). This is a changed allocation between orders at the same mark count, not an unreachable change or a renaming of marks.

Thus, with exactly the same fixed channels under both kernels,
\[
\mathcal E_F=\mathcal E_G
=\tfrac14\mathcal C_0^2
+\tfrac12\mathcal C_1\mathcal C_0
+\tfrac14\mathcal C_1^2.
\]
This defeats every final preparation/readout within the ansatz, including retained references, rather than merely one parity test. At \(N=1\) the sole endpoint is one marked vertex; its count already determines its marked endpoint class. Equal count laws then force equal endpoint laws. Hence two births is the smallest possible horizon for the requested kind of counterexample.

## Separate constant-kernel invariance

If the mark kernel is independently fixed to \(p_0=t\) at every precursor, then for each fixed bit word \(\mathbf b\),
\[
\Pr(\mathbf b)=\Big(\prod_jp_{b_j}\Big)
\sum_{\mathbf S}\prod_jq(P_{j-1},r_{j-1},S_j)
=\prod_jp_{b_j}.
\]
Summing the last complete structural row and proceeding backwards proves the equality even when later structural choices depend on earlier marks. Therefore any separately stipulated normalized structural law through that same horizon would give the same bit-word distribution, count distribution and final channel, with the constant mark probabilities and channels held fixed. This conditional invariance does not establish that another structural law is admitted. No alternative \(q\) is proposed or used in the counterexample.

## Meaning of the limit

The optional mark-sensitive update supplies a mathematical coupling. Final-only access through commuting, mark-only channels discards how marks are arranged in the event order, except insofar as the law changes count probabilities. It can also discard count information. The complete marked endpoint retains distinctions that the final payload loses.

This is an exact finite information limit of the declared ansatz and access, not a universal physical impossibility. Intermediate access, feedback, record postselection and different updates are outside this question. No physical observation bridge, selected dynamics, sample-size guarantee, geometry/gravity recovery or Boundary influence follows. The original passive model remains unchanged.
