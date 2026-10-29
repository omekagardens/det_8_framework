# Counter-only joint readout at four births

Independently reviewed and accepted at the fixed conditional scope below. A richer terminal counter observation represents the same joint events as the formal order diagnostic. The original one-bit output cannot recover the actual diagnostic or reproduce the two joint laws through a common stochastic postprocessor. Physical access to the richer observation remains an additional assumption.

## Fixed definitions and dependencies

Use the unchanged positive marked growth law and complete ideal support specified in the [native mark-law statement](../track_b/native_mark_law_geometry_v1.md) and [incidence-register construction](finite_incidence_register.md). A birth increments modulo five every counter in its actual precursor ideal, then appends zero. The prepared counters equal strict-descendant counts; at four vertices these lie between zero and three, so there is no wrap. Immutable source marks and fair later bits, preparation, persistent identities and memory remain as specified there.

The universal predicate question concerns every consistently empty-prepared four-vertex strict order and marking. Let D be the total-chain indicator, Dstar the indicator that the four counter values have multiset {0,1,2,3}, and Y the indicator that some counter equals two. One supplied terminal classical value/multiset observation evaluates (Dstar,Y) from the same register, without order, history, structural tags or source labels.

For the two-law application, the [prepared-source comparison](native_source_readout_response.md) starts at a chain a<b with marks(i,0), i=0 or1, counters(1,0), the same passive unrelated residual and trivial reference, followed by exactly two births. Each comparison begins with unit continuation mass at its own prefix. The accepted joint targets in cell order00,01,10,11 are (246,295,0,779)/1320 and (456,290,0,574)/1320. Their full calculation is in that source; this proof does not repeat it.

A restricted postprocessor receives just one original Y bit, without the source label, source-correlated side information, individual counters or repeated samples. Its deterministic function or stochastic kernel is the same for both preparations; private randomization has one source-independent law. Actual recovery of D and reproduction of synthetic joint distributions are separate questions. The unrestricted stochastic question allows a synthetic second coordinate; preservation of the actual observed Y is a separate restriction.

## 1. Universal predicate proof and transport

Let P be any strict partial order on four vertices with the admitted consistent register preparation. Write

n_P(v)=number of vertices w with v<w in P.

The accepted incidence construction starts each counter at zero and increments it precisely at births of strict descendants. Thus z_v=n_P(v) modulo five. Here0<=n_P(v)<=3, so there is no wrap and z_v=n_P(v) as an ordinary integer. This is where consistent preparation and the fixed horizon enter; an arbitrary four-tuple of counter values would not justify this identification.

If P is a total chain, its four ranks have descendant counts3,2,1,0. Therefore D(P)=1 implies Dstar(z_P)=1.

Conversely, suppose the counter multiset is{0,1,2,3}. Then the sum of descendant counts is6. Each strict comparability contributes exactly once to this sum, at its lower endpoint. A four-element set has exactly six unordered vertex pairs, and a strict partial order can orient at most one comparability per pair. Six comparabilities therefore mean every pair is comparable. P is a total order, so D(P)=1.

Consequently Dstar(z_P)=D(P) for every consistent four-vertex order and every marking. The proof uses no enumeration of order types, the prepared-source comparison terminal examples, q coefficients or source values. It does not recover an arbitrary order from its counts or extend this modulo-five observation to larger horizons.

An order isomorphism carries the descendants of v bijectively to those of its image. It therefore transports its counter value and permutes the multiset. Both Dstar and Y, the existence of a counter equal to two, are unchanged by that permutation; D is invariant under order isomorphism as well. The initial source embedding is transported as in the prepared-source comparison and supplies no extra readout input.

## 2. Joint law and the added observation contract

For every continuation h in the prepared-source comparison, its consistent terminal register satisfies

(Dstar(z_h),Y(z_h))=(D(P_h),Y(z_h)).

The probabilities of all histories remain unchanged. Taking the pushforward of this pointwise equality gives the same joint law under each prepared source, without recomputing any history weights. In cell order00,01,10,11 the inherited laws are exactly

P0=(246,295,0,779)/1320,
P1=(456,290,0,574)/1320.

These are accepted inputs from the prepared-source comparison, now applicable to the counter-only pair by the predicate proof. The previously accepted nonzero contrasts and event distinction transfer with those laws; no new numerical fit or independent physical channel is inferred.

The supplied observation reads the four terminal counter values or their multiset once, then evaluates both predicates on that same classical register. It needs no whole-order, source-label, history or structural-tag access. This replaces the formal whole-order requirement for this pair of events at this precise scope.

It does add an observation capability. The previous contract's four local equals-two tests and single OR bit do not grant access to the other counter values. Full-value/multiset access is a chosen richer readout, with no demonstrated native availability, physical acquisition, calibration, noise, cost or optimality. Existing quantum complete-map/reference results retain their earlier scope; this prepared classical proof is not arbitrary-input quantum equivalence.

## 3. Actual deterministic recovery from Y: impossible

A common deterministic decoder g(Y) must give the actual D on every supported continuation. Under preparation0, both accepted cells(D,Y)=(0,1) and(1,1) have positive probabilities295/1320 and779/1320. Thus supported histories with the same input Y=1 require respectively g(1)=0 and g(1)=1, a contradiction. Preparation1 also has both cells positive.

This is a pointwise obstruction, already within either preparation. It does not depend on re-enumeration, source inference, numerical approximation or a guessed decoder. Matching frequencies would not repair it.

## 4. Stochastic reproduction preserving observed Y: impossible

Now allow private source-independent randomness but require y'=Y. Let

t=K(1,1|1),

the same conditional output probability under both preparations. The positive Y=1 marginals inherited from the prepared-source comparison are1074/1320 and864/1320. Matching the11 cell would require simultaneously

t=779/1074 and t=574/864.

These values differ:779*864−574*1074=56580>0. No such t exists. Therefore the complete observed-Y-preserving kernel family is excluded, regardless of its other entries. This is distributional impossibility across the two-law family, distinct from the preceding failure to recover actual D.

## 5. Unrestricted stochastic synthetic-pair reproduction: impossible

Do not assume the preceding restriction. Let any source-independent stochastic kernel K(d,y'|y) have nonnegative entries and each input row sum to one. Define its induced probability of synthetic y'=0 by

u=sum_d K(d,0|0), v=sum_d K(d,0|1),

so0<=u,v<=1. Put A_i=P_i(Y=0). The fixed targets give A_0=246/1320 and A_1=456/1320, which are distinct.

Reproducing the full target joint law necessarily reproduces its second-coordinate marginal. Therefore, for both i,

A_i u+(1−A_i)v=A_i.

Subtracting the two equations and dividing by the nonzero A_1−A_0 gives u−v=1. The probability bounds then force u=1 and v=0. Nonnegativity of each K entry implies every output with y' different from the input y has zero probability. Thus any unrestricted solution would necessarily belong to the observed-Y-preserving family already excluded above.

This covers every declared two-input/four-output stochastic kernel, not merely deterministic kernels or a chosen decoder. Allowing a synthetic second coordinate does not evade the simultaneous two-law constraints. The conclusion concerns one source-blind input bit, independent private randomness and these two target laws. It does not classify source-conditioned kernels, side information, repeated samples or other target families.

## 6. Mapping boundary

The counter predicate replaces a formal whole-order requirement for this particular joint event at the fixed horizon. It does not derive availability of the richer readout, physical preparation, addressing, retention, disturbance, calibration or acquisition cost. The one-bit obstruction does not establish that reading every counter value is minimal, or prove a memory, runtime or energy advantage.

The fixed prepared classical result does not extend the earlier quantum branch/reference statements to arbitrary-input observation equivalence. No source record is identified with physical energy or action, no order diagnostic with acceleration, no counter with phase, and no birth count with physical duration. A common-energy coupling and live residual backreaction remain separate unresolved mapping premises. The growth law, support, counter updates and horizon have not been retuned. Earlier conditional scopes and custody qualifications remain; this theorem grants no experimental, implementation or protected-evaluation permission.
