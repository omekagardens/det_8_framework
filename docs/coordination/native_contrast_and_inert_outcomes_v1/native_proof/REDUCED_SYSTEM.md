# RI166 — a counterexample to the two-row contrast relaxation

30 September 2026. Manual analytic author contribution, not independent
adjudication. This note does not read the actual 109-component vector or
provide a counterexample to the retained native law.

## 1. Exact conclusion

The explicitly enumerated two-row constraint system below does **not** imply

\[
 D_-\le213d_7.
 \tag{1}
\]

A rational family satisfies its complete row normalization, inherited scalar
margins, coefficient-times-potential identities, and the exact positive
sensitivity identity, while

\[
 D_-=\frac1{1000},\qquad d_7=\varepsilon,
 \qquad 0<\varepsilon\le\frac1{1000000}.
 \tag{2}
\]

Consequently `D_-/d7>=1000`, and this ratio is unbounded in the relaxation.
The family works for **every** `0<theta<1/144`; theta is not adjusted to make
the example work. These are hypothetical rational rows, not evaluations of
the actual law, executed fixtures, or a proposed replacement witness.

The exact native maximum linkage, all other marked rows, and the fixed
component assignment/value table are not checked by this example. The
implication for the actual retained law therefore remains open.

## 2. Fully enumerated reduced premises

Let the fixed old chain row have entries

\[
 A_0=A_1=A_3=e=1/44,\qquad A_7=a=41/44.
\]

Only the following premises are imposed. The component subscripts here are
slot/record labels, not newly reconstructed certificate indices.

1. One shared real parameter satisfies `0<theta<1/144`. There is no
   independently chosen theta for each record.
2. For each `i=0,1`, a complete five-slot row consists of strictly positive
   `(w,p_i,s_i,b_i,c_i)`, with the same `w` in both rows and
   `w+p_i+s_i+b_i+c_i=1`. The four proper entries are
   `B_i(0)=w`, `B_i(1)=p_i`, `B_i(3)=s_i`, `B_i(7)=b_i`.
3. With the exact inherited comparison constants

   \[
   m=1/352,\quad P=113/11480,\quad
   \beta=33901019/474368400,
   \]

   require `m<=w,p_i,s_i`, `w,p_i<P`, `s_i<P/2`,
   `beta<=c_i<19/40`, and

   \[
   11489/22960<b_i<2267/2464<a.
   \tag{3}
   \]

4. Define all four proper coefficients by the exact deletion-potential
   identities `alpha_(S,i)=B_i(S)/A_S` and require each to be at least `1/8`.
   This is a condition on these eight entries (the two empty entries agree),
   not certification of a complete component vector.
5. Retain the complete four-stem sums, without dropping the common empty
   term:

   \[
   Q_i=\sum_{S=0,1,3,7}\frac{B_i(S)^2}{A_S},\qquad
   T_i=\sum_{S=0,1,3,7}\frac{B_i(S)^3}{A_S^2},\qquad
   K_i=Q_i+2c_i,
   \]
   \[
   j_i=1-\theta K_i,\quad
   V_i=j_i+2\theta^2c_i+\theta^3T_i,\quad
   E_i=3j_i+3\theta^2c_i+\theta^3T_i.
   \tag{4}
   \]

   The complete E and V profiles are stated explicitly in RI155
   CAPACITY_STRUCTURE.md section 6; its exact source identity is below.

6. Require `d7=b0-b1>0` and `v=V1-V0>0`. Set
   `d1=p0-p1`, `d3=s0-s1`, and, for `S=1,3,7`, define

   \[
   P_S=\frac{B_0(S)+B_1(S)}{A_S},\qquad
   T_S=\frac{B_0(S)^2+B_0(S)B_1(S)+B_1(S)^2}{A_S^2},
   \]
   \[
   \mathcal H_S=P_S+2\theta-2-\theta^2T_S.
   \tag{5}
   \]

   Keep the exact identity

   \[
   v=\theta(d_1\mathcal H_1+d_3\mathcal H_3+d_7\mathcal H_7).
   \tag{6}
   \]

   It follows algebraically from (4) and complete normalization, rather
   than supplying an independently assigned sensitivity.
7. Retain the RI157 scalar conclusions relevant here:
   `-2<H_S<0`, `71/72<j_i<V_i<1`, `71/24<E_i<3`, and

   \[
   0<v<2\theta D_-<1147/9092160,
   \qquad D_-=(p_1-p_0)_++(s_1-s_0)_+.
   \tag{7}
   \]

Sections 3–5 prove every one of these premises for the family. Requiring
these consequences explicitly prevents a purported example that evades the
already accepted sensitivity sign or complete-row formulas.

The scale premise is deliberately only its inherited interval. In the
actual law `theta=1/[72(1+M5)]`, where `M5` is the maximum over the complete
parent-five proper-potential table. That table is neither instantiated nor
checked here. Pointwise validity for every allowed theta means the family
does not depend on selecting its value. It does **not** establish that a
hypothetical row pair and any given theta arise from the same native maximum.

## 3. The rational family and all row/margin checks

For any rational `0<epsilon<=1/1000000`, put

\[
 w=s_0=s_1=\frac1{300},\quad
 p_0=\frac1{250},\quad p_1=\frac1{200},\quad
 b_0=\frac34,\quad b_1=\frac34-\varepsilon,
\]
\[
 c_0=\frac{359}{1500},\qquad
 c_1=\frac{143}{600}+\varepsilon.
 \tag{8}
\]

These are exact symbolic rational definitions. In particular

\[
 c_0=1-\frac34-\frac1{150}-\frac1{250},\qquad
 c_1=1-\left(\frac34-\varepsilon\right)
          -\frac1{150}-\frac1{200}.
\]

Thus both rows normalize exactly, including their genuine full slots, and

\[
 c_0-c_1=\frac1{1000}-\varepsilon,
 \quad d_1=-\frac1{1000},\quad d_3=0,\quad d_7=\varepsilon.
 \tag{9}
\]

All entries are strictly positive. Here are finite rational checks of the
remaining inequalities; none concerns an actual selected coefficient.

- `m<1/300`, while both singleton entries exceed `1/300`.
  The largest of `w,p0,p1` is `1/200<P`, since `11480<22600`.
  Also `1/300<P/2`, since `22960<33900`.
- `beta<1/8` follows from
  `8*33901019=271208152<474368400`. Both full slots exceed `1/5`.
  They are below `1/4`: this is immediate for `359/1500`, and
  `143/600+epsilon<144/600<1/4`, because `epsilon<1/600`.
  Hence `beta<c_i<1/4<19/40`.
- `b1>7/10`, since `epsilon<1/20`, and `b0=3/4`.
  The required lower bound is below `3/5`, since
  `5*11489=57445<68880=3*22960`.
  The required upper bound exceeds `3/4`, since `1848<2267`.
  Also `3/4<41/44`.
- At slots `0,1,3`, every coefficient is at least
  `44/300=11/75>1/8`, since `88>75`.
  At slot `7`, `alpha=(44/41)b_i>7/10>1/8`.
  Each of these four coefficient ratios is also strictly below one.

Thus the example respects the potential/probability distinction and the
stronger actual full-complement floor beta, not merely `c_i>0`.

## 4. Complete j, V, E and secant bounds for every theta

All four ratios `B_i(S)/A_S` lie in `(0,1)`. Therefore

\[
 0<T_i<Q_i<\sum_SB_i(S)=1-c_i,
 \qquad 2c_i<K_i<1+c_i<5/4<2.
 \tag{10}
\]

It follows that `j_i>1-2theta>71/72`, while `j_i<1`.
The positive full slot and cubic sum give `V_i>j_i`. Moreover

\[
 V_i=1-\theta[K_i-2\theta c_i-\theta^2T_i]<1,
\]

because `2theta c_i+theta^2 T_i<(theta+theta^2)K_i<K_i`.
Every inequality is strict on the admitted interval. Likewise `E_i>3j_i`,
and

\[
 E_i=3-\theta[3K_i-3\theta c_i-\theta^2T_i]<3:
\]

`3theta c_i+theta^2T_i<[(3/2)theta+theta^2]K_i<3K_i`.
This proves all complete-row bounds in premise 7.

For any slot let `x=B0(S)/A_S`, `y=B1(S)/A_S`. Both are in `(0,1)`,
so `x^2+xy+y^2<(3/2)(x+y)`. Since `(3/2)theta^2<1`,
equation (5) gives `H_S>-2+2theta>-2`.

For the upper signs, this family has

\[
 P_1=\frac{99}{250},\qquad P_3=\frac{22}{75},\qquad
 P_7=\frac{44}{41}\left(\frac32-\varepsilon\right)<\frac{66}{41}.
\]

Dropping only the negative cubic secant term yields

\[
 \mathcal H_1<\frac{99}{250}+\frac1{72}-2<-\frac32,
 \qquad
 \mathcal H_3<\frac12+\frac1{72}-2<0,
\]
\[
 \mathcal H_7<\frac{66}{41}+\frac1{72}-2
              =-\frac{1111}{2952}<0.
 \tag{11}
\]

For the stronger first comparison use `99/250<2/5` and `1/72<1/10`.
This proves every secant lies strictly in `(-2,0)` without setting theta
or any coefficient to zero.

## 5. Exact positive sensitivity and failure of the proposed comparison

Factoring the square and cube differences in (4) proves (6), since
`c1-c0=d1+d3+d7` and the empty contrast vanishes. Substitution of (9)
then gives the exact correlated expression

\[
 \frac v\theta=-\frac{\mathcal H_1}{1000}
                         +\varepsilon\mathcal H_7.
\]

It is strictly positive for **every** `0<theta<1/144`:

\[
 \frac v\theta>\frac3{2000}-2\varepsilon
 \ge\frac3{2000}-\frac2{1000000}
 =\frac{1498}{1000000}>0.
 \tag{12}
\]

Conversely `H1>-2` and the strictly negative core contribution imply
`v<2theta/1000=2theta D_-`. The row intervals already checked give

\[
 D_-<(P-m)+(P/2-m)=\frac{1147}{126280},
\]

and `2theta<1/72` gives the last inequality in (7).
This checks the inherited small sensitivity bound as well as its sign.

Nevertheless, by (2),

\[
 213d_7\le\frac{213}{1000000}
                  <\frac{1000}{1000000}=D_-.
 \tag{13}
\]

Taking any sequence of positive rational epsilon tending to zero keeps
every reduced premise and makes `D_-/d7=1/(1000epsilon)` unbounded.
The concrete member `epsilon=1/1000000` is an illustrative rational model
of this system, not a scientific fixture or a value inferred from a source.
No script, numerical engine or rational-arithmetic evaluator was used.

This failure has a precise normalization mechanism. Let

\[
 D_+=(p_0-p_1)_++(s_0-s_1)_+.
\]

Complete normalization gives the zero-safe identity

\[
 D_-=d_7+(c_0-c_1)+D_+.
\]

Thus (1) is equivalent to the genuine missing comparison

\[
 (c_0-c_1)+D_+\le212d_7.
 \tag{14}
\]

Here `D_+=0`, and the left side is `1/1000-epsilon`: the full-complement
decrease almost cancels the singleton increase in the core gap. None of
the checked one-row margins prevents this cancellation. A native-law
argument must control it through additional actual cross-row information.

## 6. Exactly what this counterexample does not check

The reduced system consists only of premises 1–7. In particular it omits:

- The complete RI41 marked parent-four ratio-component graph and all its
  transported local nodes, including which other rows share the illustrated
  component labels. No claim is made that the displayed slot coefficients
  extend to a full 109-component assignment.
- Every other marked row, all distinct ideal occurrences, and the actual
  full-matrix inequalities `A alpha<1` and `B alpha>21/40`. The margins
  imposed here are necessary scalar consequences, not substitutes for
  those complete inequalities or their diamond/locality checks.
- The exact immutable 109-vector, its default/overrides and actual component
  ordering/value bindings. Neither a universal grid nor a selected value
  is assumed. The actual law fixes these entries; this example does not.
- The complete parent-five potential maximum M5 and the linkage of the
  same hypothetical rows to `theta=1/[72(1+M5)]`. Its inherited interval
  is checked; its native table identity is not.
- The complete parent-five primary/canonical optimization, all original
  lexicographic tie-break coordinates, its strict mixture, and the actual
  canonical singleton corrections. Their established actual cap theorem
  remains valid, but it is not a property independently certified for this
  hypothetical extension.
- Global M6, actual rho, the correlated joint q/v budget, W, individual
  C2/C3 and shared H30. No sign or feasibility conclusion about any of
  these follows from a failure of (1) in the relaxation. It does not even
  assert that the family passes the sufficient capacity envelope.

The exact source-law characterization permits one positive scale per
ratio component before the full row constraints and fixed witness are
imposed. It supplies no automatic cross-component value ordering. That
observation motivates checking the missing relation, but is not a proof
that this reduced counterexample is extendible to the full law.

## 7. Literal sources, identities and actual author actions

The RI166 assignment and RI157 root adjudication were read in full and
their requested byte/hash identities matched (fafe49, f997bf, 109e51;
all shell exits zero). Their exact paths are:

- `/Volumes/AI_DATA/development/det-review-evidence/ri164-root-static-review-xr1qffz8/NATIVE_SUCCESSOR_ASSIGNMENT.json`
- `/Volumes/AI_DATA/development/det-review-evidence/ri157-root-adjudication-q_wj4pny/RI157_ROOT_ADJUDICATION.json`

The bound RI157 HANDOFF.json and all three complete manuscripts were read
in `/Volumes/AI_DATA/development/det-review-evidence/ri157-correlated-capacity-proof-tusjyk77`.
The manuscripts' read-window hashes matched that handoff (b2e080):

| Manuscript | Bytes | SHA-256 |
| --- | ---: | --- |
| CORRELATED_CONTRAST_BOUND.md | 13521 | db68169effdd98c500376afd2f93a658ad675e594028bf6348c9257311426524 |
| CANONICAL_CAP_BOUND.md | 12849 | abff2d8a473634532dc8690556a2ce828f80cde0ff1704068ec2445778462125 |
| CORRELATED_CAPACITY_SYNTHESIS.md | 11966 | 25646b02bd021a8de23b89d8841621c70bbcecf97fe59164ac63d620b9cea7dd |

Additional complete literal mathematical reads, with observed byte/hash
identities (ce0308, b5c302), were:

| Absolute source path | Bytes | SHA-256 |
| --- | ---: | --- |
| /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_joint_growth_extension_v1/EXTENSION.md | 18800 | 61423e355f508021f05cd941e5a0dbed62661c76ba750766583fd4b8c619e716 |
| /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md | 16243 | 567596a17c69e20b33328b2d0c39f22d98a78f7d25d81949fd57cd07df5e53c8 |
| /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md | 17102 | e99ea92b13687d7de6ad4db2bec9161397edb8ddacac18f6b32966e58ca85122 |
| /Volumes/AI_DATA/development/det-review-evidence/ri147-native-scale-membership-q4lxbpke/COMPONENT_CONTRASTS.md | 19001 | b982477d162bce2210aabaffe91cc68e52315734c186d2895e67da4736c9a49f |
| /Volumes/AI_DATA/development/det-review-evidence/ri155-strict-capacity-proof-jv0xliup/CAPACITY_STRUCTURE.md | 15579 | 54fa9b1e421520527a2403e20d0e243f257bdc8ef244e945200e4a652ab3d936 |

RI36 section 4 specifies the held smaller-law construction; RI41 sections
1, 3 and 5 give the proper-potential rule, full row matrix obligations and
uniform finite margins. RI63 sections 2–4 bind the unchanged prefix and
define the later actual maximum and canonical mixture. RI147 sections 2,
4 and 6 supply the coefficient meaning and complete contrast identities.
RI155 section 6 explicitly supplies the complete E and V profiles used
in (4). Its complete literal read and byte/hash checks were f7e05b,
29b5a5 and 93349a, all exit zero; this was already an inherited source path.
Reading a printed table is not a new evaluation of its selected entries.
No scientific JSON body was read.

A targeted literal search also inspected matching lines in
`/Volumes/AI_DATA/development/det-review-evidence/ri127-connected-compensation-nMyz57P5/LOCAL_POSITIVITY.md`,
`/Volumes/AI_DATA/development/det-review-evidence/ri128-connected-sign-dvgWLqqv/ANALYTIC_BOUNDS.md`,
and `/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn/ANALYTIC_PREFIX_LEMMAS.md`
(ea19d5). No fresh full read or new premise from those searches is claimed.
RI157 SOURCE_DEPENDENCIES.json was read as administrative provenance only
(91dc1e), not as scientific evidence.

One combined manuscript display was clipped; separate complete reads
1f5cf1, 25a5a9 and 000439 recovered all three before writing. The remaining
literal mathematical reads were complete (a3a716, d8455c, 8a8038).
The complete current CONTRAST_COUPLING.md was read as an author-peer check
(1a63d9): its normalization, three halfspaces, six-component invariant and
full-law exclusions were manually checked without a concrete finding.
All shell reads/hashes reported exit zero. The proof and displayed integer
comparisons were performed manually, not by an imported helper, symbolic or
numerical engine, graph enumeration, fixture, or scientific-value evaluator.

Only this reserved Markdown was edited, through apply_patch. There was no
source import/compile/AST/probe/run, selected vendor startup, new subagent,
runtime/controller/card/admission, repository/index/Git or predecessor edit.
RET remains paused, measurement separate, and actual qualification pending.
This is an author contribution for peer checking and fresh independent
review, not a physical, all-size or actual native-capacity conclusion.
