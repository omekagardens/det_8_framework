# What can a fresh occupation store gain under full joint reversibility?

**Conditional result.** The single E54 resonance does not follow from joint reversibility and the two conservation laws alone. With the same three carriers and sharp store, positive mean gain is possible exactly when some higher-count carrier string can lose rest energy at the calibrated rate w per lost count. This is a finite pair test. A full joint permutation can use initially unoccupied store levels for its reverse transitions, while its carrier projection on the prepared slice need not be a permutation.

For the stipulated spectrum M/M0=(1,2,4) and independently set w=M0 c², the exact maximum mean store-count gain in this larger class is

    2076/2744 = 519/686.

An attaining control has final store levels 6,7,8,9 with probabilities 1308,860,512,64 divided by 2744. All other levels, including losses, have zero probability for this control. This is the full unconditional law, and it also holds conditional on every complete marked native history. No trials are selected or discarded.

## 1. Fixed preparation, corrected energy ledger and changed premise

Reuse the accepted CL073 and E54 preparation: labelled carrier states A=00, B=10, C=01, D=11 have counts 0,1,1,2, probabilities (5,4,4,1)/14, and masses M0,M1,M1,M2 with 0<M0<M1<M2. Three independent carriers undergo the same two marked native births. Both middle labels and every history remain distinct. The fresh store is exactly at s=6, with levels 0 through 12 and direct terminal readout.

Let X={A,B,C,D}³. For x∈X let J(x) be total carrier count, E(x)=c²∑M_q its additive registered rest energy and W(x) the product of its integer weights 5,4,4,1. The store energy is e0+ws with one independently calibrated w>0 over all 13 levels. Apply Energy's accepted wording correction: the registered carrier rest energy may change by E(y)−E(x). Every other material, kinetic, binding, interaction and support energy term is held fixed. The store offset e0 cancels. Count-zero A still has positive rest energy M0 c².

The sole changed control premise is that the predeclared operation U is an arbitrary permutation on all 64×13=832 carrier/store states, conserving both

    L=J(x)+s,          V=E(x)+e0+ws

on every state. Histories are read-only and U does not depend on them. The carrier output from (x,6) can be written g(x), but g need not be a permutation of X. No feedback, history selection, external ancilla, hidden work or reset capability is introduced. U is a supplied formal control, with no dynamical or apparatus implementation asserted.

## 2. Necessary and sufficient finite criterion for positive gain

Define F_w(x)=E(x)−wJ(x). On a fixed L sector, V=e0+wL+F_w(x). Hence a permitted transition out of (x,6) has exactly the form

    (x,6) -> (y,6+J(x)−J(y)),    F_w(y)=F_w(x).

Every carrier count lies in 0,...,6, so every such output level lies within 0,...,12. A compatible injection on the prepared slice extends to a full joint permutation by matching the unused domain and image states within each finite (L,V) sector. This fact does not require the carrier projection to be injective across different sectors.

**Finite criterion.** There is a strictly positive mean single-use gain if and only if there are x,y∈X such that

    J(x)>J(y),
    E(x)−E(y)=w[J(x)−J(y)].                         (1)

Necessity: without such a pair, every possible transition from every prepared input has J(y)≥J(x), and therefore every store change is nonpositive. Identity is feasible and attains zero, proving a sharp zero bound when (1) fails.

Sufficiency: take one qualifying pair, put d=J(x)−J(y)∈{1,...,6}, and transpose the two full joint states (x,6) and (y,6+d), fixing every other joint state. Their L and V agree by (1), so this permutation preserves both totals pointwise, including its reverse action. Its second endpoint has s>6 and is absent from the prepared sharp slice. Thus among prepared trials only x moves, gaining d; all others stay fixed. Its mean gain is d W(x)/2744>0. The reverse endpoint has not been removed from the operation or its ledger; it has zero initial probability in this experiment.

For a directly checkable condition on w and the masses, use the ten occupation compositions (a,b,d), where a=#A, b=#(B or C), d=#D and a+b+d=3. Define ε=E/c² and j=J as follows.

| (a,b,d) | j | ε |
| --- | ---: | --- |
| (3,0,0) | 0 | 3M0 |
| (2,1,0) | 1 | 2M0+M1 |
| (1,2,0) | 2 | M0+2M1 |
| (2,0,1) | 2 | 2M0+M2 |
| (0,3,0) | 3 | 3M1 |
| (1,1,1) | 3 | M0+M1+M2 |
| (0,2,1) | 4 | 2M1+M2 |
| (1,0,2) | 4 | M0+2M2 |
| (0,1,2) | 5 | M1+2M2 |
| (0,0,3) | 6 | 3M2 |

Form the finite set

    S(M)={ c²(ε_r−ε_t)/(j_r−j_t) : j_r>j_t, ε_r>ε_t }.

Then the necessary and sufficient condition is w∈S(M). Multiplicities do not affect existence because every labelled string has strictly positive input probability. Equal-count pairs cannot charge the store; nonpositive spacings are outside the premise. In particular S(M) contains c²(M1−M0)>0 via BAA→AAA. The test does not say every positive spacing is possible: it gives a finite set of slopes for fixed masses and the fixed three-carrier domain.

E54 remains valid in its original, narrower class. A carrier permutation has a fixed number of carrier output slots at each charge within every F_w block; its positive mean is possible only at w=(3M1−M2−2M0)c²>0 and then is 117/2744. Reversibility of the full joint map does not impose that extra slot constraint on g. A store-gain observation therefore cannot establish E54's particular mass-spacing diagnostic unless the carrier-permutation restriction is separately verified. The changed theorem and the accepted E54 theorem have different operation premises.

## 3. Sharp maximum for the one stipulated spectrum and spacing

Set μ=M0 c², M/M0=(1,2,4), w=μ. For a string with b middle labels and d copies of D,

    E(x)=μ(3+b+3d),    J(x)=b+2d,
    F_w(x)=μ(3+d).

Conservation therefore fixes d within each joint sector. For fixed initial d,b the total count is L=6+2d+b. All output strings with the same d are available: for an output with b' middle labels its store level is 6+b−b', which lies between 3 and 9, hence within the supplied range. Different b values have different L sectors even when d agrees.

The number of labelled strings of type (d,b) and their common individual weight are

    N_db = C(3,d) C(3−d,b) 2^b,
    W_db = 5^(3−d−b) 4^b.

The B,C degeneracy is counted explicitly. A sector with fixed initial d,b contains exactly N_db positive-probability inputs on s=6, each of weight W_db. Reversibility demands distinct joint outputs in this sector, but leaves all its other initial states at zero probability. The maximum is obtained by choosing the N_db available output strings with the smallest b'. No different injection can reduce the sum of output counts further: replacing any selected larger b' by an unselected smaller b' lowers that sum. Because the weights within each such input sector are equal, pairing choices among the selected slots do not change the objective. Sector independence makes the sum of these separate minima a global upper bound for all joint permutations.

The following finite table lists the slots that attain that bound. An entry b':n means n distinct output strings with b' middle labels. The last column is the unnormalized contribution to expected gain, N_db W_db b minus W_db times the sum of selected b'.

| d | b | N_db | W_db | Selected output slots b':n | Gain numerator |
| ---: | ---: | ---: | ---: | --- | ---: |
| 0 | 0 | 1 | 125 | 0:1 | 0 |
| 0 | 1 | 6 | 100 | 0:1, 1:5 | 100 |
| 0 | 2 | 12 | 80 | 0:1, 1:6, 2:5 | 640 |
| 0 | 3 | 8 | 64 | 0:1, 1:6, 2:1 | 1024 |
| 1 | 0 | 3 | 25 | 0:3 | 0 |
| 1 | 1 | 12 | 20 | 0:3, 1:9 | 60 |
| 1 | 2 | 12 | 16 | 0:3, 1:9 | 240 |
| 2 | 0 | 3 | 5 | 0:3 | 0 |
| 2 | 1 | 6 | 4 | 0:3, 1:3 | 12 |
| 3 | 0 | 1 | 1 | 0:1 | 0 |

The d=0,1,2,3 groups respectively contain 27,27,9,1 strings; the total is 64. Their probability numerators are 2197,507,39,1, summing to 2744. The gain numerators total 1764+300+12=2076, giving the exact upper bound 2076/2744=519/686. The attaining rule below proves this bound is sharp, with no search or numerical enumeration.

## 4. One unambiguous predeclared full joint permutation

Use the fixed alphabet order A<B<C<D and ordinary lexicographic ordering of three-letter strings. For each d,b, list the N_db prepared input strings in lexicographic order. List all output strings with exactly d copies of D in increasing order of (b', lexicographic string), and retain the first N_db. Map input number i to output number i with store level 6+b−b'. This determines g(x) and its store reading on all 64 prepared inputs without a measurement, branch on a history or discretionary tie choice.

Within a fixed d,b, all output carrier strings are distinct. Across different d,b, the invariant pair (L,F_w) differs, so the full output states remain distinct even if their carrier strings coincide. Each prescribed input and output lies in the same joint (L,V) sector. To define U on every remaining state, in each sector pair the remaining domain states with the remaining image states in lexicographic order of (carrier string, store integer). Fix sectors with no prescribed inputs. Equal complement sizes make this a bijection of all 832 states. This completion also conserves both totals on states not initially occupied. Apply the same U with every history unchanged.

For each prescribed transition, d is fixed and

    Δs=b−b',     E(g(x))−E(x)=μ(b'−b)=−w Δs.

Both ledgers close on every individual transition and on the full completion. All selected b' satisfy b'≤b, so no prepared trial loses store count for this optimal rule. This does not exclude losses from the larger admissible class. For example the legal transposition (AAA,6)↔(BAA,5) instead gives a one-count loss on the prepared AAA trial at these same masses and spacing. Such a control would retain and report that loss. No postselection explains the absence of losses in the maximizing control.

## 5. Complete normalized single-use record

Write h_i=(t_i,β_i1,β_i2), t_i∈{E,F}, for the original ideal and two recorded bits on carrier i, and H=(h_1,h_2,h_3). The accepted native preparation gives

    Q(H)=product_i(q_ti/4),    q_E=2/3, q_F=1/3,
    P(x,H)=[W(x)/2744] Q(H).

Each of four E histories has probability 1/6 and each of four F histories has probability 1/12 on a carrier. Thus ∑_H Q(H)=1 over all 8³ histories. The terminal-label law is independent of the entire native marked history for this preparation, as in CL073. No history is a control variable.

For the attaining map above, the absolute full terminal law is

    P(H,x,y,r)=[W(x)/2744] Q(H)
                 ×1{y=g(x)} ×1{r=6+J(x)−J(y)}.    (2)

Summing its deterministic indicators over y,r retains each original x,H cell once. If initial and intermediate microscopic native labels are retained, multiply the same indicators by the original product of native path probabilities

    product_i p_(u_i) [D(0)/2]_(v_i,u_i)
                         [(q_ti/2)D(ξ_ti)]_(x_i,v_i).

The accepted D matrices, ξ_E=1/8448, ξ_F=−1/4224 and supported/forbidden paths are unchanged. In particular A→A, D→D and the B,C block paths retain their absolute masses, and every originally forbidden path remains zero. The terminal operation is appended after these births.

Summing (2) gives the complete direct store readout law:

| Δs | Final level r | P(r), also P(r given H) for every H |
| ---: | ---: | ---: |
| 0 | 6 | 1308/2744 |
| +1 | 7 | 860/2744 |
| +2 | 8 | 512/2744 |
| +3 | 9 | 64/2744 |
| All other changes | 0–5 and 10–12 | 0 |

The joint observed probability is P(H,r)=Q(H)P(r). The numerators sum to 2744. The signed first moment is (860+2·512+3·64)/2744=2076/2744. Loss probabilities at levels below 6 are explicitly zero for this control; they were not excluded from normalization. No extra failure channel or outcome outside the stipulated perfect readout has been silently conditioned away.

For an arithmetic check by conserved d group, the numerators at r=6,7,8,9 are respectively:

| d | r=6 | r=7 | r=8 | r=9 |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1025 | 644 | 464 | 64 |
| 1 | 255 | 204 | 48 | 0 |
| 2 | 27 | 12 | 0 | 0 |
| 3 | 1 | 0 | 0 | 0 |

The mean calibrated store energy gain is w·519/686=μ·519/686, funded exactly by the mean carrier rest-energy decrease. This statement uses the supplied constant store spacing over the reached levels and the corrected registered carrier energy ledger.

## 6. What the record can establish

The larger operation class turns the sharp initially prepared store into an additional register for retaining distinctions. For instance different prepared carrier inputs can produce the same carrier output at different store levels. Full joint reversibility retains those distinctions and assigns reverse transitions at initially unoccupied store levels; it does not require the prepared carrier projection to fill every carrier label once. This is the resource omitted by identifying joint reversibility with a carrier permutation.

The energy in the gained store counts comes from the changed registered carrier rest energy. It does not come from the history marks, relational presence or reversal of an unoccupied transition. Fresh sharp preparation and access to distinguishable joint states are supplied capabilities. Their realization, later restoration, carrier replenishment, acquisition and readout costs have not been measured or optimized. This is a single-use comparison, not a cycle or an efficiency result.

At M/M0=(1,2,4), E54's narrower carrier-permutation class has zero maximum for every w>0 because its resonance is zero. Here the very same spectrum at independently calibrated w=μ has a positive sharp maximum. Thus the earlier single-spacing diagnostic tests the additional carrier-control premise as well as the two conservation laws. The finite set S(M) remains a conditional compatibility test for the larger class; positivity does not license an arbitrary spacing or a universal linear carrier energy law in count.

A terminal count record alone neither verifies the carrier-permutation premise nor measures w, a physical energy unit, a work gain, time/phase scale, action per count or Hamiltonian. An energy interpretation requires independent calibration of the constant store law and the registered masses, together with the closed pointwise ledger. These premises are retained here rather than inferred from the larger mean. No physical apparatus, empirical DET advantage or energy creation is established.

The carrier-permutation result and calibrated sector masses are the comparison used here. [Energy spacing for carrier permutations](occupation_store_rest_energy.md) · [Sector mass ratios](sector_inertial_mass_ratios.md)

## Scientific provenance

- Relational State author SHA-256 db640ff43f5d9f2a2fbeb06adcda1834bafb79e10d75061f0a9cb88b3e8125fa.
- Independent joint-store review SHA-256 cd7e6e7a3644c751a83ee9f564629a0db7cb132df9475a53f62cbceb4c3f95a6.
