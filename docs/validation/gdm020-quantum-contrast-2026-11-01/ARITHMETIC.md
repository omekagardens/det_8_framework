# GDM021 — fixed finite enclosure method

**Decision:** a finite rational method with proved widths is available for the exact two GDM020 constants and their dimensionless discrepancy. No constants have been evaluated here. The method below gives widths smaller than 2^-106, hence smaller than 10^-6, within explicit finite arithmetic and integer-size caps. Independent method review and separate admission of actual arithmetic remain required.

The prospective premises were saved and fully read before the supported 2026-11-01 17:24:51 UTC checkpoint. The first supported task clock was17:23:38 UTC. All derivation below was manual after that boundary. The model, spectrum, clock, matrix elements and orientation remain the accepted ones. This is a computational resolution proof, not a physical agreement/error criterion.

## 1. Exact dimensionless input and cancellation

Put a_C=hbar^2/(mu C), a=150^2 a_C, and retain n=140,...,158 for pairs and k=140,...,160 for normalization. Define

x_k=(k-150)^2/50,
y_n=((n-150)^2+(n+2-150)^2)/100,
Z=sum_k exp(-x_k), U_n=exp(-y_n).

Thus 0<=x_k<=2, 0<=y_n<=2, Z>=1 because x_150=0, and the exact normalized product c_n c_(n+2)=U_n/Z. This retains the square of the packet normalization; it is not an independently normalized pair ensemble.

Let b_n=B_n/a^2 and r_n=150^3(n+1)/(2 n^2(n+2)^2), so theta_n=pi r_n is the unchanged exact energy-gap phase. The requested constants are

 d_c=(4/Z) sum_n b_n U_n (1-cos(pi r_n)),
 d_s=(4/Z) sum_n b_n U_n sin(pi r_n),
 D=sqrt((d_c-1)^2+(d_s-1)^2).

There is an exact simplification of the accepted radial/angular expression. Substituting K_n,K_(n+2) and beta_n+beta_(n+2)=2(n+1)/(n(n+2)a_C) into GDM020 equation5 gives

 B_n/a_C^2 = [n^(n+4)(n+2)^(n+2)/(16(n+1)^(2n+5))]
  * (2n+4)! * sqrt[n(n+1)/((2n+1)(2n+3)(2n-1)!(2n+3)!)].

The last factorial times square root is exactly 4n(n+1)(n+2). Indeed, dividing the factorials first gives

 (2n+4)!/sqrt((2n-1)!(2n+3)!)
 = (2n+4) sqrt((2n)(2n+1)(2n+2)(2n+3));

multiplication by the angular square root leaves
(2n+4)*sqrt(4 n^2(n+1)^2)=4n(n+1)(n+2), with the positive root fixed by n>0. Consequently

 b_n = n^(n+5)(n+2)^(n+3) / [4*150^4*(n+1)^(2n+4)]
     = [n^2(n+1)^2/(4*150^4)] * [1-1/(n+1)^2]^(n+3).       (A)

These are exact rational numbers: the prospective radical treatment simplifies further, without changing any input. No approximation to a factorial ratio is needed. In particular 0<b_n<1: the bracketed power is below1, and n,n+1<160 with 160^4<4*150^4. Also 0<r_n<1, since its numerator is below160^4 and denominator at least2*140^4, while 160^4<2*140^4. The latter inequality is 8^4<2*7^4 after cancelling20^4. No phase was replaced by a common orbital phase.

## 2. Endpoint conventions and where rounding occurs

Set q=2^-128 and delta=2^-120=256q. These are work resolutions, not physical thresholds. All factorials, powers, polynomial sums and rational endpoints below are exact integers/rationals. Use outward dyadic rounding

 [l,u] -> [floor(2^128 l)/2^128, ceil(2^128 u)/2^128].          (B)

Each use increases width by less than or equal to2q. Floor/ceiling must be mathematical floor/ceiling also for negative numerators. No nearest-rounded float is substituted.

Use(B) only after each exponential enclosure, the pi enclosure, each sine/cosine enclosure, and the final d_c,d_s enclosures. A final outward rounding of D is allowed and is included in the width bound. All intervening aggregate endpoint operations are exact rational operations. Products use the minimum/maximum of the four endpoint products; sums add endpoints; division is only by the strictly positive Z interval. Intersect enclosures with proved ranges when specified. This is a fixed finite recipe, not an unspecified interval software dependency.

## 3. Forty exponential factors

For each of the21 x_k and19 y_n, with x in[0,2], form the exact positive rational polynomial

 S(x)=sum_(j=0)^128 x^j/j!.

The omitted positive tail is bounded by

 0<=exp(x)-S(x)<= [2^129/129!]/(1-2/130) < 2^-266.          (C)

The ratio bound applies to every term starting with j=129. For the displayed power bound,129!>=64^66=2^396 from its factors64,...,129, and 1/(1-2/130)<2. Thus no numerical exponential fact is assumed. S>=1, and positive reciprocal reverses order, giving

 exp(-x) in [1/(S+2^-266), 1/S].                            (D)

Its width is at most2^-266, because both reciprocal denominators are at least1. After(B), and intersection with[0,1], width is less than3q<delta. For x=0 use the exact singleton[1,1]; in particular the normalization's k=150 term is exactly1. Sum the21 normalization intervals exactly to obtain Z_I subset[1,21], with width at most21delta. Retain the19 pair intervals U_n,I subset[0,1], each width at mostdelta.

This treatment uses positive sums and reciprocals; it does not rely on cancellation of a long alternating exponential series.

## 4. Pi from rational arctangents

Write alpha=atan(1/5), beta=atan(1/239). The tangent double-angle identity gives tan(2alpha)=5/12, tan(4alpha)=120/119, and tan(4alpha-beta)=1. The relevant angle is in(0,pi/2): alpha>=5/26>1/6 by the integral of 1/(1+t^2), beta<1/239<1/6, while4alpha-beta<4/5<1<pi/2. The last inequality follows from pi/2=2 atan(1)>1. Hence

 pi=16 atan(1/5)-4 atan(1/239).                             (E)

The elementary integral also gives2<pi<4. These identities provide an internal justification rather than an unsupplied decimal constant.

For v=5 or239 form

 T_v=sum_(j=0)^127 (-1)^j/((2j+1)v^(2j+1)).

Integrating the finite geometric identity for1/(1+t^2) from0 to1/v proves the alternating enclosure

 atan(1/v) in [T_v,T_v+1/(257 v^257)]
              subset [T_v,T_v+2^-514],                    (F)

since v>=5>4. Combine the two intervals with coefficients16 and-4, preserving the sign reversal. The resulting pi width is at most20*2^-514. After(B) and intersection with[2,4], its width is less than3q. For each n multiply by the exact positive r_n<1, obtaining theta_I in[0,4] with width less than3q. No argument reduction or supplied mesh is needed on this bounded domain.

## 5. Thirty-eight trigonometric factors

For theta_I=[a_n,b_n'] use its exact rational midpoint m_n and half-width h_n. Here b_n' is an interval endpoint, not the matrix element b_n from(A). At m=m_n form

 P_s(m)=sum_(j=0)^127 (-1)^j m^(2j+1)/(2j+1)!,
 P_c(m)=sum_(j=0)^127 (-1)^j m^(2j)/(2j)!.

Both are the Taylor polynomials through degree255, with the odd coefficient at degree255 zero for cosine. For0<=m<=4, Taylor's integral/Lagrange remainder and the derivative bounds |sin|,|cos|<=1 give absolute error at most

 4^256/256! <=2^(512-903)=2^-391 <2^-380.                    (G)

Here256!>=128^129=2^903 from factors128,...,256. The elementary derivative bounds also give |sin x-sin y|<=|x-y| and the same for cosine. Therefore enclose each function at the uncertain theta by

 [P(m)-(2^-380+h_n), P(m)+(2^-380+h_n)].                    (H)

After(B) and intersection with[-1,1], each width is less than
2*2^-380+3q+2q<6q<delta. The cosine-derived interval1-C_n lies in[0,2] with that same width; S_n lies in[-1,1]. The method does not require a sign assumption for sine. All arguments, gaps and orientations are unchanged.

## 6. Propagation to the two constants

Compute the exact rational aggregate intervals

 A_c,I=sum_n b_n U_n,I (1-C_n),
 A_s,I=sum_n b_n U_n,I S_n.

For independent enclosing intervals with U in[0,1], F in[0,2], widths at mostdelta, the product UF has width at most2delta+delta=3delta. For S in[-1,1], the product US has width at mostdelta+delta=2delta. These bounds follow by varying one factor at a time; dependence between actual quantities can only make the attainable set smaller than the enclosing rectangle. Thus

 A_c,I subset[0,38], width<=57delta,
 A_s,I subset[-19,19], width<=38delta.

For z,z' >=1,

 |a/z-a'/z'| <= |a-a'| + max(|a|,|a'|)*|z-z'|.

Consequently the exact interval divisions4 A_c,I/Z_I and4 A_s,I/Z_I have widths at most

 4(57+38*21)delta =3420delta,
 4(38+19*21)delta =1748delta.                              (I)

After(B), intersect with the proved ranges d_c in[0,152], d_s in[-76,76]. Let the resulting intervals be I_c,I_s and their actual rational widths w_c,w_s. Since2q<delta,

 w_c<3421delta<2^-108,
 w_s<1749delta<2^-109<2^-108.                              (J)

These intentionally loose bounds already exceed the requested computational resolution by a large margin. They are not numerical estimates of the centers of the intervals. The positive normalization lower bound is retained throughout; no near-zero division is hidden.

## 7. Final square root without loss at zero

Let m_c,m_s be the exact midpoints of I_c,I_s and set

 Y=(m_c-1)^2+(m_s-1)^2,
 e=(w_c+w_s)/2.

The ranges above give |m_c-1|<=151 and |m_s-1|<=77, so sqrt(Y)<=228<256. Enclose sqrt(Y) by exactly128 rational bisections of[0,256], selecting the half by exact comparison of its midpoint square with Y. If equality occurs, a singleton is permitted; otherwise the interval invariant follows from monotonicity of x^2 on nonnegative x. The final bracket J=[j_l,j_u] has width at most256*2^-128=delta. This is the sole remaining square-root approximation; the matrix-element roots already cancelled exactly.

For every(d_c,d_s) in I_c times I_s, the reverse triangle inequality for the Euclidean norm gives

 |D-sqrt(Y)| <= sqrt((d_c-m_c)^2+(d_s-m_s)^2)
             <= (w_c+w_s)/2=e.

Hence return

 I_D=[max(0,j_l-e), j_u+e].                                (K)

This remains valid when Y or D is zero; no division by a square root or presumed discrepancy gap is used. Its width is at mostdelta+w_c+w_s. Including an optional final(B),

 width(I_D) <=delta+w_c+w_s+2q <2^-106.                    (L)

Together(J)–(L) prove all three widths are below10^-6: already2^-20<10^-6 since2^20=1048576>10^6. No endpoint or central value of d_c,d_s,D has been computed in this work. In particular these bounds do not establish that1 lies inside or outside either constant's eventual enclosure, or that the actual discrepancy is small.

## 8. Explicit finite cost and integer-size caps

These are conservative, unmeasured bounds for the specified exact arithmetic, not a runtime claim. Count integer addition/subtraction, multiplication, quotient-with-remainder, comparison and sign operations as elementary integer operations. Exact divisions of factorial multiples are included. No gcd algorithm is required: use the common-denominator forms below and the specified dyadic normal form at rounding/bisection boundaries. Powers may be built by repeated multiplication or finite power tables; no transcendental library is assumed.

* Exactly19 rational matrix elements(A),21 normalization and19 pair exponentials, two128-term arctangent sums,19 rational phases,38 trigonometric polynomials with128 terms each, two19-term aggregates and one128-step square-root bracket suffice.
* Use factorial tables only through256; exponentials use the common denominator v^128*128! for x=u/v, and numerator sum u^j v^(128-j)*(128!/j!). Here u<=200<2^8 and v<=100<2^7. Including tail and reciprocals, these rational operations need less than3000 bits per integer before comparisons.
* For atan(1/v), use common denominator v^255*255! and numerator sum (-1)^j v^(254-2j)*255!/(2j+1). With v<=239, each individual arctangent enclosure, including its positive remainder bound, needs less than5000 bits per integer. Combining the two different denominators in(E) needs less than10000 bits per integer before comparisons (less than20000 for temporary cross-products).
* The dyadic pi endpoints have denominator2^128. Each r_n has numerator below2^32 and denominator below2^33. Consequently a rational trigonometric midpoint m=u/v can be represented with v<2^162 and u<2^164. Use the single common denominator v^255*255!; numerator terms are the appropriate signed u^k v^(255-k)*(255!/k!) for the128 selected degrees. Since255!<2^2040, each term has fewer than43861 bits and summing128 terms adds at most7 bits. Adding the tail/argument bounds and rounding stays below46000 bits per integer before pairwise comparisons.
* In(A), n<=158, so exponents n+5<=163, n+3<=161,2n+4<=320 and bases below2^8. The numerator and denominator each need fewer than2600 bits. Constructing all19 ratios uses fewer than19*700 integer operations by repeated multiplication.
* After primitive enclosures are dyadic, each aggregate summand has denominator length below2600+256=2856 bits and numerator below2900 bits. Accumulating19 terms even by multiplying their denominators gives fewer than56000 bits per integer. Division by the dyadic Z and final outward rounding stay below57000. Cross-multiplications/comparisons between two such rationals stay below114000 bits. The midpoint norm and dyadic128-step bisection are much smaller. No repeatedly nested unreduced rational denominators are allowed in place of these explicit common forms.

A uniform cap of **200000 bits per signed integer, including temporary products**, is therefore adequate for this recipe. A conservative count is fewer than250000 elementary integer operations: fewer than14000 for(A),60000 for40 exponentials,4000 for the two arctangents,114000 for38 trig polynomials (3000 each including power tables and endpoint formation), and fewer than20000 for factorials, phases, aggregate endpoints, rounding and bisection. Permit an overall cap of **1000000 such operations** to include bookkeeping comparisons and sign cases. The algebra above supplies headroom within both caps; no execution or timing measurement has been performed. Any later method using a different arithmetic organization must justify its own caps rather than inherit these silently.

## 9. Smallest later calculation and distinct check

The later calculation needs only this frozen recipe and the exact GDM020 MODEL/RESULT and identity manifest. It needs no physical constants, data, external decimal pi, fitted phase, new spectrum, runtime/library audit or new scientific premise to form these dimensionless numbers. It is not authorized by this document itself.

The smallest auditable output is exact rational endpoint data for the19 b_n,40 exponential factors (with the normalization singleton), pi and19 phases,38 trig factors, Z,A_c,A_s,I_c,I_s,Y,J and I_D, together with the finite endpoint-inequality witnesses and actual widths. A rounded display value may accompany these but cannot replace them. Preserve the original19-term labels and their normalization. Report whether each resulting constant interval contains1; an exclusion certifies only failure of exact equality in this conditional model. Inclusion does not prove equality. Do not invent an approximation acceptance threshold.

A distinct arithmetic checker must independently reconstruct(A) from the pinned radial/angular expression, verify its positive-root cancellation, reconstruct all exact polynomial/remainder bounds and endpoint operations, and verify the final widths from rational inequalities. It must reconstruct the totals from the frozen inputs rather than trust the producer's stored intermediate values. Exact residual/cross-multiplied inequalities and the bisection invariant are appropriate evidence; agreement of two rounded floats is not. Method review, actual calculation and arithmetic check are separate from root disposition.

Numerical success would still leave individual response laws, preparation/repeatability P0, complete P1 correspondence, physical matched controls P2, readout/calibration P3, physical/model remainders and any empirical/DET/gravity claim unresolved. The original contrast is only a necessary comparison. No new coefficient, law, spectral family, gate program, experiment or automatically authorized successor follows.

**Stop decision:** retain this finite enclosure recipe for distinct review; actual d_c,d_s,D remain unevaluated. No code, pseudocode implementation, scientific execution, tests, new sources, source/shared edits, Git, descendants, other-chat contact or journal operation was performed. Final saved readbacks, identity checks, freeze and supported actual completion follow before handoff.
