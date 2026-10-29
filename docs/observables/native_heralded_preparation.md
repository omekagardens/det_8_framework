# Native heralded preparation with failure retained

This finite theorem embeds the two prefixes of the [prepared-source comparison](native_source_readout_response.md) in histories beginning with the empty state. Each source herald has probability 1/12; their total success probability is 1/6, and the remaining 5/6 is retained as an explicit failure outcome. The construction uses the unchanged original fair-mark law in [Part A of the admitted model](../track_b/native_mark_law_geometry_v1.md), the [prepared classical incidence register](finite_incidence_register.md), and the [counter-only joint readout theorem](counter_only_joint_readout.md).

The model runs exactly four births. After the second birth, a supplied nondisturbing observer tests whether the actual first two vertices form a chain with marks (i,0), stores its herald and retains their identities. Every branch then continues through the same horizon without feedback or restart. On success the output is (i,Dstar,Y); otherwise it is one failure symbol. Dstar tests counter multiset {0,1,2,3}; Y tests whether any counter equals two. Addressing, prefix observation/storage and richer terminal counter access are explicit mathematical assumptions, not demonstrated apparatus capabilities. This is stochastic heralded preparation, not an operation choosing a source value at will.

The proof below includes the complete prefix law, conditional applicability, failure-inclusive output law and identity transport. It does not identify native energy, physical time or gravity. The original one-bit obstruction retains its source-blind information restrictions when the herald label is available.

## 1. Complete prefix accounting

The first vertex a is born above the unique empty ideal with structural probability one; each mark i has probability 1/2. At the singleton parent, the second birth b chooses empty with structural weight 2/3 or {a} with weight 1/3. These weights do not depend on i. Each second mark j again has conditional probability 1/2.

Thus, for every ordered pair (i,j) in {0,1}²:

| Second ideal | Two-vertex order | Individual marked-prefix weight | Herald |
|---|---|---:|---|
| empty | a and b incomparable | (1/2)(2/3)(1/2)=1/6 | fail for either j |
| {a} | a<b | (1/2)(1/3)(1/2)=1/12 | i if j=0; fail if j=1 |

These are all actual ideals and all mark pairs. Each row represents four distinct marked history prefixes, not a quotient by terminal isomorphism. Their total weight is 4/6+4/12=1.

For each i, H_i consists of its chain prefix with j=0, so its mass is 1/12. Failures include all four incomparable prefixes, of total mass 2/3, and the two chain prefixes with j=1, of total mass 1/6. Consequently

Pr(H_fail)=2/3+1/6=5/6,

and Pr(H_0)+Pr(H_1)+Pr(H_fail)=1. Both conditioning events have positive mass. No prefix-formation factor has been absorbed into a normalized successful subensemble.

## 2. Exact applicability to the adopted continuation

At a's birth its counter is zero. On H_i, b is born above {a}; this increments only a and appends b with zero. The prefix is therefore exactly a<b, marks (i,0), counters(1,0). Its source is the same actual a and its upper vertex is the same actual b as in the prepared-source comparison's prescribed preparation.

The admitted law reads its specified parent state, not the stored herald. Counter evolution also remains its original update. Under the expressly supplied nondisturbance assumption, observing and retaining h changes none of these inputs. The two remaining birth transitions consequently agree branch by branch with the adopted prepared-source comparison continuation transitions. All ideals and newborn marks remain present, and the horizon and initial reference/residual conditions agree. This verifies applicability; merely seeing a similar terminal shape would not suffice.

The terminal counter state is consistently empty-prepared. The counter-only readout theorem therefore identifies Dstar with the formal total-chain diagnostic D pointwise on this domain. The accepted prepared-source comparison joint distributions of (D,Y) become the joint distributions of (Dstar,Y) after H_i, with no terminal enumeration repeated:

P0=(246,295,0,779)/1320,
P1=(456,290,0,574)/1320,

in cell order 00,01,10,11. This reuses adopted results; it does not assert a new general conditional-probability theorem.

## 3. Failure continuations and complete output law

For each fixed marked prefix, including every failed one, sum over all actual third ideals and marks and then all actual fourth ideals and marks. At each parent,

sum over (S,b) of q(S)/2 = sum over S of q(S) = 1.

The admitted complete-row normalization applies to every reachable parent. Nested summation over both remaining births therefore preserves each prefix's mass. In particular, the failed incomparable prefixes retain aggregate mass 2/3, and failed chain prefixes retain aggregate mass 1/6 through four births. They are executed mathematically to the same horizon and only then mapped to bottom. No restriction on their terminal orders, marks or counters is imposed.

On H_i, each accepted conditional cell carries the prefix factor 1/12. The full output distribution, including the zero cells, is:

| Output | Probability |
|---|---:|
| (0,0,0) | 246/15840 |
| (0,0,1) | 295/15840 |
| (0,1,0) | 0 |
| (0,1,1) | 779/15840 |
| (1,0,0) | 456/15840 |
| (1,0,1) | 290/15840 |
| (1,1,0) | 0 |
| (1,1,1) | 574/15840 |
| bottom | 13200/15840 = 5/6 |

The first successful block sums to (246+295+779)/15840=1320/15840=1/12. The second sums to (456+290+574)/15840=1320/15840=1/12. Adding bottom gives (1320+1320+13200)/15840=1.

The two zero cells inherit the adopted conditional impossibility of D=1,Y=0 together with the pointwise predicate equality. All other displayed cells are positive. Dividing either successful block by its actual mass 1/12 recovers its accepted target exactly. The failure symbol is a declared coarse-graining of fully retained histories, not discarded data.

## 4. Actual-identity transport

Transport an entire birth history by a bijection of vertex identities: each birth vertex v becomes tau(v), each ideal S becomes tau(S), and marks and counters follow their vertices. Transport the history's first/second-vertex roles and its retained prefix embedding as well. The source a becomes tau(a), not a root newly chosen from the terminal shape.

Admitted q equivariance preserves every branch weight. Actual-ancestor counter updates commute with this transport. The relations a<b and marks (i,0) hold exactly when their transported versions do; therefore the herald label i and failure membership are unchanged. The terminal counter multiset and the existence of an exactly-two counter are likewise invariant. Output and weight are preserved history by history, hence the full law is preserved.

This claim includes the retained preparation interface. A terminal-order-only representation that forgets the prefix does not automatically retain that interface. No additional automorphism division, label multiplicity or redefinition of source is introduced.

## 5. Information, control and remaining gaps

This construction retains i and herald memory. The counter-only readout theorem's source-blind stochastic one-bit obstruction assumed a processor receiving only Y, with no source label or source-correlated side information. It cannot be transferred unqualified to a processor receiving (i,Y) or that memory. Reuse requires imposing and justifying the original information restrictions. Actual hidden-event recovery and synthetic distribution matching remain separate questions. This analysis does not classify any changed-information decoder family.

The construction embeds both prefixes in unchanged histories from the empty preparation, with success mass 1/6 and failure mass 5/6. It supplies no action selecting i at will, no overwrite, feedback or retry. One four-birth trial is the comparison unit; no repeat-until-success expectation or physical time/energy/cost interpretation is made.

Empty initialization, the chosen q, the optional classical register, actual-ancestor addressing, prefix relation/mark access, nondisturbant storage, identity retention and terminal value/multiset access remain supplied mathematical ingredients. The prefix memory is not silently an additional DET commit. A physical acquisition mechanism and its effects remain absent. Existing arbitrary-input quantum claims retain their separate scope.

The construction satisfies the fixed accounting and applicability question under the stated hypotheses. It establishes no physical source availability, energy/action, acceleration, phase, duration, common-energy coupling, live residual feedback, quantum access or gravity identification.
