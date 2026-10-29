# An active residual-to-structure law through four births

This note presents the independently reviewed NM004 finite classical construction. The complete law below has a residual-state update followed by a changed structural probability. It uses an added two-state carrier, numerical choices and preparation/access assumptions; it does not derive physical energy, time, quantum mechanics or gravity. The original passive model remains unchanged.

The reference q is exactly [Part A of the finite marked-law specification](native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix), including its full complements and all actual ideal occurrences. The domain is every binary-marked strict finite order through four births. A birth adjoins one maximal vertex over an actual downward ideal; old marks and order stay fixed. The residual cone is R_+^2, total mass 1^T rho, with both pure basis preparations and mixtures supplied at each prefix. Every ideal and both newborn bits remain eligible; the fourth birth ends the trial. There are no silent steps or early stopping.

Proper precursors may read the whole unmarked parent and only marks inside that precursor; full precursors may read all old marks. Vertex relabeling transports records and ideals while residual coordinates remain identified. The full map, including its unnormalized weight, must commute across every incomparable-birth diamond and its transported suffix.

## 1. Fixed coefficients for every parent and ideal

Use precisely Part A's accepted q_C(S), with every actual ideal and fair newborn mark. Put n=|P|, and let chi(P)=1 if the current unmarked order is an antichain, including the empty order, and zero otherwise. Fix once:
theta=1/32, t=1/2,
(a_0,a_1,a_2,a_3,a_4)=(1/264,1/264,1/176,1/44,1).

For every parent n<4 and every actual ideal S define
r_C(S)=theta 2^n chi(P)[a_(n+1) 1_(S=empty)−a_n],
d_C(S)=q_C(S) r_C(S). (1)

This is a current-prefix rule: it reads only the unmarked P, its size and whether the chosen ideal is empty, together with the already admitted q. The constants do not depend on any actual future outcome or terminal endpoint. No endpoint oracle, auxiliary counter, preparation tag or extra state is an input. The value a_4 is a fixed coefficient for parent-three transitions, not a terminal readout.

Define, for r=r_C(S),
M(r)=(1/2) [[1+r+t, 1−r−t],
             [1+r−t, 1−r+t]],
T_C,S=M(r) diag((1+r)^(-1),(1−r)^(-1)). (2)
Take D_C,S=q_C(S)diag(1+r,1−r), A_C,S=q_C(S)M(r), and B_C,S,b=A_C,S/2 for both b. Thus A=T D exactly. Equations (1)–(2) specify every coefficient on all parents of sizes0–3, all old markings and ideals. Size4 remains terminal.

The scalar-potential notation H(P)=a_n chi(P) is convenient only for proof. Because adjoining a maximal vertex preserves the antichain property exactly when P was an antichain and S was empty,
r_C(S)=theta 2^n[H(P+S)−H(P)]. (3)
The implementable mathematical definition remains (1); evaluating a future history is unnecessary.

## 2. Full support, locality and normalization

All a_n lie in [0,1], so |r_C(S)|<=theta 2^n<=1/4. Consequently |d|<=q/4<q. Every entry of M is at least (1−1/4−1/2)/2=1/8. Its column sums are1+r and1−r, both positive. Equation (2) therefore makes T nonnegative and column-stochastic. Every ideal/bit branch has strictly positive mass on every normalized nonnegative residual state, and conditional normalization is defined.

The only harmonic identity needed is
sum_S q_C(S)H(P+S)=H(P). (4)
For a non-antichain parent, every extension still contains an old comparable pair, so both sides vanish. For an antichain, only S=empty contributes. The exact accepted empty-slot probabilities at parent sizes0,1,2,3 are respectively1,2/3,1/4,1/44. Directly,
a_0=a_1,
a_1=(2/3)a_2,
a_2=(1/4)a_3,
a_3=(1/44)a_4.
Thus (4) holds for every old marking, not merely a selected trajectory.

Equations (1), (4) and sum_S q=1 give sum_S d=0. Hence
sum_(S,b) 1^T B_C,S,b
=sum_S q_C(S)(1+r_C(S),1−r_C(S))
=(1,1). (5)
This proves complete normalization on the full cone. Each individual normalized branch mass is at most one because all masses are nonnegative and sum to one; indeed every branch has another positive branch beside it. Both newborn bits and every continuation remain present.

More strongly, M(r) is affine in r, so sum_(S,b)B_C,S,b=M(0) at every parent. This nonselective map preserves mass but is not identity, exactly as permitted; it is the sum of the declared birth branches, not an added silent update.

The uniform state u=(1/2,1/2)^T obeys M(r)u=u, so A_C,S u=q_C(S)u. This establishes the required uniform-current-state anchor, while neither requiring general inputs to be uniform nor asserting that K delta0 is uniform.

For a proper S, r and T read no marks at all, while d inherits exactly q's permitted dependence on selected marks. Full slots retain q's allowed full-mark dependence. Neither formula uses vertex names or changes old records/order. Under any marked-parent isomorphism, n, chi(P), emptiness of S and q transport identically, proving covariance of d,T,A,B with the stipulated trivial carrier action. Both newborn bits use exactly the same matrix.

## 3. Every full-matrix diamond and suffix

Let v=(1/2,−1/2)^T and W=[u v]. This is an algebraic basis, not a change of allowed states. In it,
W^(-1) M(r) W = [[1,r],[0,t]]. (6)

For any supported m-birth history from C, |C|=n, ending at E, chronological multiplication gives
W^(-1)(M_(m−1)...M_0)W
= [[1, r_0+t r_1+...+t^(m−1)r_(m−1)],
   [0,t^m]]
= [[1, theta 2^n(H(E)−H(C))],
   [0,2^(-m)]]. (7)
The last equality is exact telescoping using (3), because t^j 2^(n+j)=2^n. It holds on the whole carrier, not only on u or one tested input. The full marked-history map is (7), conjugated by W, multiplied by 2^(-m) times the product of the actual q factors.

Now take any required base of size<=2, any old marking, ideals S,T including equal ones, and bits b,c. The two incomparable births produce the same transported marked endpoint. Their M-products agree by (7). Their scalar q products agree by the accepted full structural diamond, and both fair-bit factors equal1/4. Thus
B_(C_x),T,c B_C,S,b = B_(C_y),S,b B_C,T,c
as complete two-by-two unnormalized matrices.

No case is excluded: H ignores marks and depends only on the transported unmarked endpoint; q supplies the exact marked identity. A precursor becoming proper after the other birth is still the same actual old subset, so the argument covers full-to-proper transport as well.

After the swap the marked parent is identical under transport. Covariance makes every later selected branch matrix identical, even for suffix ideals containing either swapped vertex. Left multiplication by that entire transported suffix preserves the full equality. Alternatively (7) applies directly to the complete history. Adjacent exchanges of incomparable births connect natural histories of a fixed order: move its chosen first minimal vertex left across incomparable predecessors and repeat on the remainder. Thus all required natural-history equalities through four births follow. Tensoring these equal matrices with identity on a retained classical reference preserves equality on correlated reference inputs. No quantum-reference assertion is used.

## 4. Exact two-birth witness

At empty, r=theta(a_1−a_0)=0 and q=1, so d=0 and
K=T_empty=M(0)=[[3/4,1/4],[1/4,3/4]]. (8)
In particular K_10=1/4 is strictly between zero and one. From known input delta0, the actual first-birth conditional state is K delta0=(3/4,1/4)^T for either first mark. The first mark zero has mass1/2; retaining it selects C_0 without changing this conditional residual.

At the singleton-zero parent and full ideal, q=1/3 and
r_full=−theta·2a_1=−1/4224,
d_full=−1/12672.
The fixed structural test, summing both new marks, is
p(rho)=q+d_full(rho_0−rho_1).
Therefore
p(delta0)=1/3−1/12672,
p(delta1)=1/3+1/12672,
Delta_current=−2d_full=1/6336 !=0. (9)
The actual updated preparation gives
Delta_update=p(K delta0)−p(delta0)
=(1/4)Delta_current=1/25344 !=0. (10)

The comparison copy (C_0,delta0) remains the separately supplied preparation declared above. Nothing overwrites the original record or deletes failed/other branches. The law is complete independently of this conditional witness.

## 5. Controls and precise interpretation

The passive reference d=0,T=I has p(rho)=q for all rho and K=I: both contrasts vanish. A concrete lawful forward-only control is d=0,T=M(0) everywhere. Then A=qM(0), so its full diamonds follow from q's diamonds and the common matrix product; K still mixes delta0, but p(rho)=q and neither contrast appears. More generally any lawful forward-only control has this input-independent p.

For any otherwise lawful static-seed control T=I, the empty-parent K is I because d_empty=0. A pure delta0 also remains delta0 under positive diagonal branch reweighting. Its update contrast is zero regardless of any permissible current-state contrast. The active law's positive off-diagonal T entries and explicit first-birth mixture establish the stipulated update route, not mere posterior reweighting of that pure state.

These comparisons concern the declared two-state instrument and interface. They do not exclude representing a finite classical process using a larger static random seed. The theorem establishes residual update followed by changed structural probability. The two contrasts are affine-linked, not independent signatures. Although this law's coefficients consult current order, no additional controlled test of reciprocal matter/geometry or physical backreaction is supplied.

## 6. Interpretation and remaining correspondence

This complete existence theorem is confined to four births and the declared classical carrier/interface. It is a native-input candidate with added law choices, not a consequence of DET ontology. The two witness contrasts are linked, not independent physical signatures. The separately supplied singleton preparation, retained first mark and access to the chain event are mathematical premises. They supply neither an apparatus nor a cost or error calibration.

The triangular maps also have a prefix-dependent algebraic gauge representation: with V_C=[[1,theta(H(C)-a_0)],[0,2^(-|C|)]], the matrix in (6) equals V_(C+S)V_C^(-1). This transformation generally does not preserve total mass or the entire normalized positive cone, and its inverse need not be positive. It is not the stipulated fixed residual-coordinate relabeling. Transporting states and effects consistently preserves all declared probabilities. Consequently the fixed-interface contrast is valid, without establishing a representation-independent physical mechanism or excluding larger static-seed realizations.

No energy, action, duration, phase, acceleration, metric, physical preparation/readout, quantum or gravity correspondence follows. Birth count is bookkeeping. Status M, Option B and the programme's independent-review, calibration, custody and execution boundaries remain. The next observation question must specify accessible preparations, complete recorded outcomes and a detector channel, keeping erasure and failure mass explicit; it cannot identify a residual bit with energy after the fact. See the [native mapping programme](../coordination/NATIVE_MASS_MAPPING.md).
