# Unlabelled terminal field response: exact finite equivalence certificate

**Conditional theorem accepted after independent scientific review on 9 November 2026.** Under exactly the selected graph balance and terminal apparatus, a shared positive scale leaves an observable chain-to-diamond ratio. The covers-only coupling and equal coupling on all comparable pairs are distinguishable. The ratio nevertheless fails to identify every finite coupling: for lambda>1 the nontrivial equivalent partner is 1+8/(lambda-1), except at its fixed point. Nothing here derives a physical field, apparatus, calibrated potential or gravity law.

## 1. Fixed preparation and complete eligibility accounting

Use the prescribed two-chain a<b with immutable marks (0,0), prepared counters (1,0), root zero, and the unchanged fair-mark/all-ideal law for births x,y. This is the normalized law conditional on that prepared prefix; no additional probability for obtaining the prefix is multiplied into it. There are 15 actual structural continuations, each with all four ordered newborn-bit pairs, hence 60 encoded histories h. If p3 is the incoming structural weight and q4 the final structural factor, each such marked history has weight w(h)=p3*q4/4. No name multiplier or automorphism division is introduced.

The newborn y is maximal. A finite order with a unique maximum has every vertex below that maximum, so y can be the unique maximum only when its precursor is the full three-parent. Among those full rows, edge-plus-isolate retains two minima and is ineligible. The fork/full row is the diamond; the chain/full row is the four-chain. These are the only eligible histories.

The root-zero source ledger gives f0=1/6, h0=19/30 and e=1/44. The fork/full factor is
1-2e-2e*h0/f0=43/55; the chain/full factor is 1-3e=41/44. Summing all four newborn-bit assignments gives:

| Terminal class | Marked histories | Complete probability |
| --- | ---: | ---: |
| Four-chain C | 4 | h0*(41/44)=779/1320 |
| Diamond D | 4 | f0*(43/55)=172/1320 |
| Edge-parent continuations, all inactive | 24 | 1/5=264/1320 |
| Fork proper-final continuations, inactive | 16 | f0*(12/55)=48/1320 |
| Chain proper-final continuations, inactive | 12 | h0*(3/44)=57/1320 |

Thus p_C=779/1320, p_D=172/1320, p_perp=369/1320 and p_C+p_D+p_perp=1. Every history and both fair bits remain. Inactive is a distinguished output, not deletion or conditioning on eligibility. In particular the accepted counter-equals-two and chain diagnostics are not an additional diamond/eligibility sensor available to this observer.

## 2. Supplied graph law, ground, uniqueness and covariance

On an eligible terminal order put one undirected edge on each strict comparable pair, once. Each cover has conductance k>0 and each non-cover comparable pair has lambda*k, with finite lambda>=0, including the direct minimum-to-maximum pair. Incomparables have no edge. The graph k is not any coefficient of the birth-law seed. The controller addresses the unique minimum s and maximum t. Its full-order, cover-testing and terminal-addressing access is an additional premise.

In the signal use injection +Q at s, -Q at t, zero at interior vertices, with Q>0; ground u(t)=0. The adopted balance is

    sum_w c_vw [u(v)-u(w)] = f(v).

This is a symmetric static attachment after growth. Its edges are not a derived time-propagating influence. Let v=k*u/Q. The dimensionless edge weights are 1 on covers and lambda otherwise, and the dimensionless load is +1,-1.

For uniqueness, the difference z of two grounded solutions obeys the homogeneous balances. Multiplication by z and summation gives

    sum_{unordered edges {v,w}} c_vw [z(v)-z(w)]^2 = 0.

Both eligible cover graphs are connected, and their cover conductances stay positive at lambda=0. Hence z is constant on all vertices and is zero at the ground; it is identically zero. The explicit solutions below establish existence. Summing all node balances cancels every edge, so zero interior loads and the stated source current require the return to be -Q. The blank has all loads zero and therefore the unique grounded zero solution.

An order relabelling preserves comparabilities, covers and the unique extrema. It permutes the conductance matrix, loads and ground together. Transport of a solution solves the transported equations; uniqueness identifies it with that solution. Consequently u(s)-u(t), and the eligibility/inactive rule, are invariant. No vertex name or shape tag is added to the observer's record.

## 3. Exact node solutions and terminal drops

Write H(lambda)=lambda^2+6lambda+1, which is positive on the entire allowed domain.

For C, name the chain s<p<q<t. The cover edges are sp,pq,qt; its three non-cover edges are sq,st,pt. The grounded dimensionless solution is

    v(s)=(lambda+3)/H,
    v(p)=2/H,
    v(q)=(lambda+1)/H,
    v(t)=0.

The p balance has numerator
[2-(lambda+3)]+[2-(lambda+1)]+2lambda=0.
The q balance has numerator
[(lambda+1)-2]+(lambda+1)+lambda[(lambda+1)-(lambda+3)]=0.
The source balance has numerator
[(lambda+3)-2]+lambda[(lambda+3)-(lambda+1)]+lambda(lambda+3)=H.
The return balance is
-[(lambda+1)+2lambda+lambda(lambda+3)]/H=-1.
Thus the dimensionless terminal response is

    R_C(lambda)=(lambda+3)/H(lambda).

For D, the four covers are sp,sq,pt,qt, and the sole non-cover comparable edge is st; p,q are incomparable. Each interior equation gives v(p)=v(q)=v(s)/2. The source balance is
2[v(s)-v(s)/2]+lambda*v(s)=1, giving

    v(s)=1/(1+lambda),  v(p)=v(q)=1/[2(1+lambda)],  v(t)=0,
    R_D(lambda)=1/(1+lambda).

The return load is -[2*v(s)/2+lambda*v(s)]=-1. These explicit signs are source positive, return negative. The physical-symbol drops in the supplied model are (Q/k)*R_C and (Q/k)*R_D, not calibrated physical potentials.

With the common gain b>0, define A=bQ/k>0. The two signal locations are

    z_C=A R_C(lambda),   z_D=A R_D(lambda).

For the blank Q=0, both eligible locations are zero. All finite allowed signal locations are strictly positive. At lambda=0 the responses are (3,1); at lambda=1 they are (1/2,1/2).

## 4. Pushforward of the whole native law, separately by setting

For each of the 60 histories let T_sig(h) be z_C, z_D or perp according to the complete class in Section 1. Let T_blank(h) be zero on both eligible classes and perp otherwise. For either specified setting S and every measurable output set B,

    P_S(B)=sum_{all 60 h} w(h) * 1_[T_S(h) in B].

The full pair of setting-conditional laws is therefore

    P_sig = (369/1320) delta_perp
          + (779/1320) delta_(A R_C)
          + (172/1320) delta_(A R_D),
    P_blank = (369/1320) delta_perp + (951/1320) delta_0.

These are individually normalized probability measures. When signal locations coincide their masses add; delta_perp never merges with a scalar, including zero. This states a pushforward, not observation of the native history, graph, counters, marks or shape. It does not introduce a joint law of paired potential outcomes on the same individual preparation. If a setting randomizer is separately supplied, any fixed positive setting probabilities multiply these two conditional laws without changing the result.

When the two signal locations differ, their unequal exact masses identify which location is C and which is D: 779/1320 labels C and 172/1320 labels D. This uses the ideal law, not a hidden shape record or finite-sample classifier. When the locations coincide only their total mass 951/1320 is visible. Since

    R_C-R_D=2(1-lambda)/[H(lambda)(1+lambda)],

coalescence occurs at exactly lambda=1.

## 5. Invariant, range and all finite equivalence classes

For a distinct pair of signal atoms define the observable ratio using their masses as above,

    r=z_C/z_D
     =(lambda^2+4lambda+3)/(lambda^2+6lambda+1)
     =1+2(1-lambda)/H(lambda).

The same algebraic ratio is 1 at the merged case, although no shape coordinate is observed there. A is free and cancels. Its derivative is

    r'(lambda)=2[(lambda-1)^2-8]/H(lambda)^2.

Set lambda_star=1+2 sqrt(2) and rho=(2+sqrt(2))/4. The ratio decreases from r(0)=3 through r(1)=1 to r(lambda_star)=rho, then increases strictly toward 1 from below as lambda tends to infinity. Consequently its exact finite-domain range is [rho,3]. The lower endpoint and upper endpoint are attained; the large-coupling branch never reaches 1 at finite lambda, but 1 IS attained elsewhere, at lambda=1.

Define equivalence to mean equality of BOTH complete setting laws for some positive common amplitude per world. If the signal is unmerged, unequal masses force association C-to-C and D-to-D; equal laws therefore require equal r. If merged, both worlds must have lambda=1. Conversely equal r permits the common amplitude choice
A'=A*(1+mu)/(1+lambda), which matches the D location and hence also C, while the blank and inactive laws already match. Thus equality of r is necessary and sufficient, including the merged case.

Cross multiplication factors exactly as

    r(lambda)=r(mu)
    iff (mu-lambda)[lambda+mu-lambda*mu+7]=0
    iff mu=lambda OR (lambda-1)(mu-1)=8.

After restricting BOTH parameters to finite nonnegative values, the complete classes are:

- Every lambda in [0,1] is a singleton.
- lambda_star is a singleton (the repeated fixed point).
- Every lambda>1 other than lambda_star has the two-element class
  {lambda, 1+8/(lambda-1)}.

The partner operation is an involution, interchanging (1,lambda_star) with (lambda_star,infinity). No negative root and no infinite parameter is an admissible partner.

## 6. Observable iff compatibility certificate

An observed ideal pair is compatible with this stipulated family if and only if its blank is exactly the blank above, its signal has inactive mass 369/1320 and no other inactive/failure category, and one of the following holds:

1. There is exactly one finite positive scalar signal atom z, of mass 951/1320. Then and only then lambda=1 and A=2z supplies that law.
2. There are exactly two distinct finite positive scalar signal atoms, with masses 779/1320 and 172/1320. Associate them by those masses and set r=z_C/z_D. Compatibility holds exactly for rho<=r<=3, r!=1. For every admissible finite solution lambda below, A=z_D*(1+lambda)>0 constructs a witness.

The parameter equation is

    (r-1)lambda^2+(6r-4)lambda+(r-3)=0.

For r!=1 its candidates are

    lambda=[2-3r +/- sqrt(8r^2-8r+1)]/(r-1),

restricted to finite nonnegative values. On the stated admissible ratio range their counts are: one at r=rho; two for rho<r<1; one for 1<r<=3. At r=1 the equation is linear and gives only lambda=1, which produces the merged law, not two distinct atoms. The range restriction excludes extraneous discriminant branches or negative roots. These statements both exhaust necessities and construct positive-amplitude witnesses, so the certificate is iff.

Wrong masses, extra atoms, nonpositive active signal, or an unmatched blank fail this exact model. The inactive outcome remains in every case. This is population-law compatibility, not an inference guarantee from a finite randomized sample. Actual instrument failures, offsets, noise or incomplete preparation would require a prospectively specified different readout law; no success-only conditioning is allowed here.

There is an important boundary distinction. At fixed finite A, lambda tending to infinity sends both signal locations to zero; its limiting signal equals the blank. That limit is unattained by any finite allowed lambda,A>0. If instead A grows with lambda so A/lambda tends to a positive z, both locations tend to z and the limiting law is the merged positive law, attained by the DIFFERENT finite point lambda=1,A=2z. Neither construction makes infinity an admissible equivalence witness. Similarly the ratio limit 1 on the high-coupling branch does not supply a second finite preimage of r=1.

## 7. Covers versus all comparabilities; gain control

With common positive Q,b,k, lambda=0 has two signal atoms at (3A,A), and lambda=1 has one merged signal atom at A/2. Their ratios 3 and 1 differ and their positive-atom counts differ. No freely chosen common normalization per world can make their full laws equal. This distinguishes these two exact alternatives under the stipulated shared-scale premise.

For the prescribed scope control relax only the gain to independent positive b_C,b_D per shape. Keep Q,k, preparation, growth law, eligibility, scalar observation and blank unchanged. Take the lambda=0 world with common gain b. In the lambda=1 world choose b_C'=6b and b_D'=2b. Its signal locations become

    (6bQ/k)*(1/2)=3bQ/k,  (2bQ/k)*(1/2)=bQ/k,

exactly matching both lambda=0 atoms with their original unequal masses. Both blank locations remain zero and all inactive outcomes retain mass 369/1320. Thus the WHOLE pair of laws agrees, not just selected signals. More generally, each finite lambda has positive responses, so independent gains can match any prescribed positive pair via b_T=z_T*k/(Q R_T). All finite lambda then lose identification under this relaxed control. Shared normalization is therefore an operative observation premise; native history weights alone cannot enforce it.

## 8. Claim, access and resource boundaries

Four ingredients remain separate: (i) the admitted normalized native history law; (ii) the NEW covariant controller, final undirected graph, balanced loads, ground and zero-offset readout; (iii) the derived dimensionless invariant and equivalence classes; (iv) any proposed physical gravity attachment. Only the first is inherited native dynamics. The static graph and apparatus do not follow from record birth probabilities, source-bit preparation or the optional incidence register. No statement about physical distance, mass, transport, clocks, force, energy, dynamical propagation or calibrated gravitational potential follows from A or lambda.

Q is a formal imposed load, not the prepared root bit. A=bQ/k is a free source-to-reading normalization; Q,b,k cannot be individually recovered here. Lambda is a relative conductance parameter of the supplied static model. Its equivalence class can be constrained without making it a uniquely derived native constant.

Required but unobserved resources include exact prefix preparation and reset; structural growth and fair-bit sampling; retained native identities and full-order/cover access; eligibility testing and terminal addressing; conductance setting and repeatability; source/return loading, supports/controllers and blank switching; grounding, zero-offset and common-gain control; scalar/inactive acquisition and retention; failure handling and restoration. No physical or matched-comparator cost was measured. Any comparator receives the same granted preparation, information and operation access. Quantum coherence, software performance and efficiency are not conclusions of these balances.

## Reviewed dependencies

The [prepared-source ledger](native_source_readout_response.md) fixes the geometry probabilities using the [native mark law](../track_b/native_mark_law_geometry_v1.md). The [incidence register](finite_incidence_register.md) specifies the earlier readout. The field calculation requires a controller with additional access to the completed order.

Frozen proof SHA-256 `88efcd1544c54c1691d577e885f25693ac980d03ca8ec34f87a1dd73759f79a6`. Independent scientific review SHA-256 `0e5badee4560a0bb70c3f52d146ccae18d022ad2439f3ea81c248da1aa7b875e`.
