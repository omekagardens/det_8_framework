# Can an induced three-event action stand in for a genuine stop?

**Author finding.** Keeping the causal predecessor whenever the newcomers are comparable, and drawing fairly when they are incomparable, gives the genuine three-event joint law of action and survivor bit under each preparation. This happens exactly at δ = 0. Choosing the causal successor on every comparable pair erases the entire source contrast, exactly at δ = 1. An incomparable pair with different actions and identical marks gives an explicit failure of trial-by-trial recovery even at δ = 0.

## Preparation and record

Condition on the registered edge a ≺ b with immutable bits (i,0) and descendant counters (1,0), for i = 0 or 1. Every trial starts from that prefix. One native birth gives the stopped experiment. In the detector experiment, two births append x and then y, each maximal at birth with its actual downward-closed precursor as its entire strict past. Each ancestor's counter increments modulo five and the newcomer receives zero. No wrap occurs here. Counters influence neither the weights nor the output. The observer receives prefix roles and terminal comparabilities for selection. The names x,y denote birth order only in the proof. For comparable newcomers the independent selection coin retains the causal successor with probability δ. For incomparable newcomers it retains either with probability 1/2. The detector restricts the full order to the two anchors and the survivor and returns its action together with the survivor's immutable bit. The selector receives no chronological labels, marks, counters or source label. Every trial contributes.

For a survivor z write E, F, C for its strict past restricted to the anchors, respectively ∅, {a}, {a,b}. The two anchors already form a chain, and z cannot precede an anchor, so these exhaust the three induced shapes. With n_j counting ordered comparable pairs having exactly j surviving vertices strictly between their endpoints, the supplied action is S₃ = 3 − 2n₀ + 4n₁ − 2n₂.

| Survivor shape | Induced order | (n₀,n₁,n₂) | S₃ |
| --- | --- | --- | ---: |
| E | a ≺ b, z isolated | (1,0,0) | 1 |
| F | a ≺ b and a ≺ z | (2,0,0) | −1 |
| C | a ≺ b ≺ z | (2,1,0) | 3 |

For example, from a ≺ b ≺ x ≺ y, deleting x retains b ≺ y as a new cover, and the remaining vertex between a and y is b. This tests the chain action 3 using the restricted transitive relation even though the original cover path from b to y passed through x.

## A complete certificate for the 15 structural rows and 60 marked histories per source

Let c = 1/5, e = 1/44. From the two-chain seed the third ideal has weights (c,fᵢ,hᵢ) for (E,F,C), with (f₀,h₀)=(1/6,19/30) and (f₁,h₁)=(1/3,7/15). Write U = 1320 e fᵢ = 5 or 10, V = 1320 e hᵢ = 19 or 14, W = 1320[fᵢ(1−2e)−2e hᵢ] = 172 or 392, and Z = 1320 hᵢ(1−3e) = 779 or 574, with the source-zero value first in each case. The following two matrices list numerators over 1320, before marking. Rows are the anchored type of x and columns are the anchored type of y, both in order E,F,C.

| x, with x ∥ y | y:E | y:F | y:C |
| --- | ---: | ---: | ---: |
| E | 6 | U | V |
| F | U | U | V |
| C | V | V | V |

| x, with x ≺ y | y:E | y:F | y:C |
| --- | ---: | ---: | ---: |
| E | 6 | 33 | 195 |
| F | — | V | W |
| C | — | — | Z |

For row r and column s, the first ideal is the anchor set r. The second is exactly s in the first matrix, exactly s ∪ {x} in the second. A dash violates ideal closure. Thus 9 + 6 entries specify 6 edge-parent, 5 fork-parent and 4 chain-parent continuations. Nothing is divided by an automorphism count.

To derive the entries, multiply each incoming mass by its own native fourth ideal probability. For an edge parent the incomparable conditional probabilities across E,F,C are (e, e fᵢ/c, e hᵢ/c). The comparable probabilities are (e, 1/8, 65/88). Here the {a,x} proper slot is e(11/20)/(1/10) = 1/8 and the full slot is the complement, since fᵢ+hᵢ = 4/5. For a fork the incomparable triple is (e,e,e hᵢ/fᵢ). Its comparable F,C entries are e hᵢ/fᵢ and 1−2e−2e hᵢ/fᵢ. For a chain the incomparable triple is (e,e,e) and the comparable C entry is 1−3e. These relations derive both matrices from the original seed and proper slots. In particular the comparable tables depend on the actual direction of the relation.

Summing across fourth ideals in the two matrices yields the chronological third-type numerators (264,220,836) or (264,440,616). Each triple sums to 1320. Every non-dash entry M has four equally weighted marked histories, with (mₓ,mᵧ) in {(0,0),(0,1),(1,0),(1,1)}, each of mass M/5280. The branch mass is independent of the newcomer marks in these prepared states. On each marked history with selection probability p for x, assign p to (S(r),mₓ) and 1−p to (S(s),mᵧ), adding coincident outputs. Here p = 1/2 in the first matrix and 1−δ in the second. This recipe includes both assignments with unequal marks as well as both equal-mark assignments. At a genuine stop x survives with certainty. Summing every fourth ideal and both fourth marks at fixed r and mₓ gives half the corresponding third-type mass, as direct one-birth growth requires.

A simultaneous renaming transports both anchors in their registered roles, the ideals, marks, counters and order. The matrices encode only the resulting role relations. For an incomparable pair there are two temporal orders of its marked vertices, with transposed entries of the symmetric first matrix and transported marks (mᵧ,mₓ). Each has equal mass. When the two anchor types coincide the transposition stays in the same cell, exchanging the two unequal-mark assignments when present. Identical choices within a cell supply no new structural multiplicity. The uniform coin treats the two alternatives equally, including on a diagonal. For comparable pairs the direction identifies the predecessor, and its causal order permits only that chronological order. Covariance imposes no comparable-pair interchange.

## Joint laws, stopping and source contrast

Use vector order (S₃ = 1, −1, 3). Let Dᵢ be the true stopped action vector, the chronological triple above divided by 1320. Uniform choice on the symmetric incomparable matrix gives its row sums in every action bin, since its row and column sums agree. On the comparable matrix shifting from predecessor to successor transfers precisely δ times each off-diagonal mass from its row to its column. Those transfers are E→F (33), E→C (195) and F→C (W), all over 1320. Consequently the detector's normalized probability vector Lᵢ(δ) has numerators

    1320 L₀(δ) = (264 − 228δ, 220 − 139δ, 836 + 367δ)
    1320 L₁(δ) = (264 − 228δ, 440 − 359δ, 616 + 587δ).

For each m∈{0,1}, Pᵢ(S₃=s, survivor bit=m) = Lᵢ(δ)[s]/2. At a true stop this equals Dᵢ[s]/2. Indeed, at any fixed row, conditional on either survivor choice, exactly two of the four incoming assignments yield a given surviving bit, independently of the selected type. A fair bit with no source contrast by itself is thus an actual output. The calculation does not identify that bit with i. Both triples stay positive and normalized for δ∈[0,1], as each is a convex combination of positive endpoint laws.

| δ | Action numerators for i=0 | Action numerators for i=1 | Denominator |
| ---: | --- | --- | ---: |
| 0 | (264,220,836) | (264,440,616) | 1320 |
| 1/2 | (300,301,2039) | (300,521,1819) | 2640 |
| 1 | (36,81,1203) | (36,81,1203) | 1320 |

Let t∈[0,1] be the probability of preparing i=1 before growth and D(t)=(1−t)D₀+tD₁. With B=(36,81,1203)/1320, the complete mixed action law is L(t,δ)=(1−δ)D(t)+δB. For every true stopped mixture the probability of S₃=1 is 264/1320. For this detector it is (264−228δ)/1320 for every t. Equality with *any* true stopped mixture requires δ=0. At zero, equality with a stopped mixture of parameter t′ then requires t′=t, because the F mass in D(t) is (220+220t)/1320. This includes both pure preparations and all intermediate settings. It also classifies the complete six-cell joint laws by their common fair conditional bit.

The source-one minus source-zero action contrast is (1−δ)(0,1,−1)/6. At each fixed reported mark the contrast is half that vector. Total variation (half the sum of the six absolute differences) is (1−δ)/6. Thus only δ=1 erases every difference between source populations, including with the survivor mark exposed. At δ=0,1/2,1 the distances are 1/6,1/12,0. For two mixtures t,t′ at the same setting, the distance scales further by |t−t′|. A nonzero contrast describes a population difference. Each of the six outputs has positive probability from each preparation, so a single observed output is compatible with either.

## A failure of chronological recovery on positive support

Take Iₓ=∅ and Iᵧ={a}. The newcomers are incomparable. Give both bit 0. The isolated newcomer arrives third here, so the stopped pair is (1,0). In the alternative history Iₓ={a}, Iᵧ=∅ the fork leaf arrives third, so its stopped pair is (−1,0). Swapping the two newcomers across the histories fixes a,b, transports the same immutable marks and gives the same anchored terminal marked order. Each specified history has mass U/5280 > 0 at either preparation. The isolated newcomer and fork leaf remain distinguishable by their order roles. Those roles cannot identify which arrived third. On each of these histories the detector returns the other chronological record with probability 1/2, including at δ=0. Equality of population laws therefore coexists with trial-level mistakes even when the two candidate survivor bits coincide.

## Scope and provenance

This result concerns the stated actual-ideal seed and fair marks, two registered preparations, and the specified family of anchored, rank-blind readouts. Births count events. Both δ and the adopted action are dimensionless. The causal selection and terminal-order access are extra observation premises. Growth weights are native throughout. The E69 horizon calculation compares reweighted ensembles and supplies the three-event action convention here. CL010 concerned an unbiased full-order cover-count estimator under independent retention on a fixed order. Neither prior result is used as a theorem equating this induced observation to native stopping. Physical clock, volume, curvature, mass and dimensional action correspondences would require separate evidence.

The selection record discloses source-informed candidate arithmetic before the control was issued. The derivation above starts from the two-chain and three-parent kernel and sums the separate comparable and incomparable matrices, with the accepted interval article's structural numerators available as a cross-check. No simulation, scientific program or external data entered.

The earlier horizon test changes history weights. Here the dynamics stay fixed while the selection changes the retained observation. Reproducing the population record does not recover the third birth on each realization. [Interval action and stopping horizon](interval_action_and_stopping_horizon.md) · [Finite interval action and source preparation](finite_interval_action_and_source_preparation.md)
