# RI155 — strict-capacity comparison for the unchanged prefix

30 September 2026. Author contribution: literal accepted source reading and
manual algebra only. This is not independent acceptance or an executed
scientific qualification.

## 1. Result and precise unresolved condition

For the same fixed C4 component law, C5 mixture and actual-containing cap
`Z` used in RI153, the accepted size-four height theorem implies

\[
 0<YE_{\rm env}<\frac{14256}{370025}<\frac1{25},
 \qquad Yu_3>\frac14.
 \tag{1}
\]

Thus the first strict capacity is proved. The maximum in the second
capacity is exactly one:

\[
 \max\left\{1,\frac{1-Yu_3}{1-YE_{\rm env}}\right\}=1.
 \tag{2}
\]

Both strict capacities therefore hold if and only if

\[
 \boxed{v>B=\frac{12\lambda j_0 Z}{1-Z}.}
 \tag{3}
\]

This note does not decide (3). It supplies a genuine first-capacity proof,
a strict slack result for the second endpoint whenever `B/v<=1`, and an
exact source-bound form of the remaining comparison. It does not construct
another q floor, establish an adequate joint budget, or decide the actual
weighted margin or H30. A failed sufficient envelope would not determine
the sign of the underlying margin.

## 2. Retained complete rows and correlated scale

Write the unchanged C3 row as

\[
 A(0)=A(1)=A(3)=e=1/44,\qquad A(7)=a=41/44.
\]

For the retained root sectors `i=0,1`, write the **complete** C4 row as

\[
 (w,p_i,s_i,b_i,c_i)
 =(B_i(0),B_i(1),B_i(3),B_i(7),B_i(15)),\quad
 w+p_i+s_i+b_i+c_i=1.
 \tag{4}
\]

All entries are positive. Empty-precursor locality makes `w` independent
of records. The accepted order is `b0>b1`; no order on the two singleton
entries or two initial-pair entries is assumed. The notation `s_i` in (4)
denotes a C4 probability, not the size-seven scale.

Retain the actual restoration and full-complement identities

\[
 \begin{aligned}
 \theta&=\frac1{72(1+M_5)}<\frac1{144},&
 K_i&=\sum_{S=0,1,3,7}\frac{B_i(S)^2}{A(S)}+2c_i,\\
 j_i&=1-\theta K_i>71/72,&
 T_i&=\sum_{S=0,1,3,7}\frac{B_i(S)^3}{A(S)^2},\\
 E_i&=3j_i+3\theta^2c_i+\theta^3T_i,&
 V_i&=j_i+2\theta^2c_i+\theta^3T_i.
 \end{aligned}
 \tag{5}
\]

The `E_i` are complete parent sums, not the unindexed envelope coefficient
`E_env`. Define, with the original canonical singleton correction retained,

\[
 \ell_i=1-\theta-N_i>0,\quad N_i\ge0,\quad
 F_i=1+\ell_i^2+N_i^2(1/p_i-1),
\]
\[
 Z=\min\left\{
 \frac1{2(1+\max(E_0,E_1))},\frac1{2(1+F_0)},
 \frac1{2(1+F_1)}\right\}.
 \tag{6}
\]

RI147 proves `0<rho<=Z<12/95<1/4`. The redundant earlier `1/4` cap
has not been dropped by assumption: the inherited `E_i>71/24` proves
it redundant. Neither the actual maximum nor a new scale is evaluated.
In particular `N_i` cannot be changed to improve (6).

The envelope quantities are

\[
 \begin{gathered}
 d(x)=2(3-2x+x^2),\quad Y=1/d(Z)\le8/41,\quad
 u_3=U_{30}(Z),\quad 3/2<u_3<2,\\
 r=\theta^3b_0^3/a^2>0,\quad
 \lambda=1-(b_1/b_0)^3\in(0,1),\quad
 v=V_1-V_0>0,\quad g=\theta^3c_0>0,\\
 B=12\lambda j_0Z/(1-Z),\quad
 E_{\rm env}=12Z^2(1+\eta)(j_0+gZ).
 \end{gathered}
 \tag{7}
\]

Here `eta=epsilon3/r` is the held empty-term ratio. It is derived below;
it is not an independently adjustable positive constant. The analytic
`Y=1/d(Z)` does not change the retained numerical certificate's `Y=1/4`.

## 3. Transport the accepted height theorem to the complete C4 row

The load-bearing quantitative input is the already accepted RI41
NORMALIZATION.md theorem: in **every complete marked four-parent row**,
the sum of all height-raising ideal probabilities is less than `19/40`,
hence less than `1/2`, and every branch is strictly positive. The theorem
has finite-certificate provenance. We reuse its printed statement; we do
not rerun its witness or claim to derive it from general DET axioms.

A birth above a proper ideal of the parent's full height also raises
height. The theorem therefore bounds more than the full-parent slot.
For a C3 diamond involving its full precursor `7` and a proper precursor
`S`, the old probabilities have ratio `a/e=41`. Equality of the two
complete transported history weights gives a factor `41` between the
corresponding next-slot probabilities. Fair newborn factors cancel;
there is no conditioning on a chosen newborn bit or loss of payload.

Apply three such diamonds.

1. **Empty precursor `(0,7)`.** Full-first gives C4, followed by its
   empty probability `w`. Empty-first gives `C3` disjoint an isolated
   point. Its birth above the complete C3 ideal has probability `41w`
   and raises height from three to four. Thus `41w<1/2`.
2. **Singleton precursor `(1,7)`.** The alternate parent is the hook
   of shape `(3,1)`. Its long C3 ideal has the retained probability
   `41p_i` and raises height. Thus `41p_i<1/2`.
3. **Initial-pair precursor `(3,7)`.** The alternate parent is the
   two-tip order `(0,1,3,3)`. Its two distinct full-arm C3 ideals each
   have probability `41s_i`. The initial-pair records are common to
   both arms; excluded tip marks do not enter that selected C4 pair
   probability. Both occurrences raise height from three to four.
   They must both be counted, even when equivariance identifies their
   values. Therefore `82s_i<1/2`.

C4's own full birth raises height from four to five, so `c_i<1/2`.
All comparisons are in permitted complete marked rows. The companion
CAPACITY_STRUCTURE.md gives the detailed transported incidence argument.
No comparison of historical seed numbers enters the argument.

Consequently

\[
 w<1/82,\quad p_i<1/82,\quad s_i<1/164,\quad c_i<1/2,
\]
\[
 \boxed{b_i>1-1/82-1/82-1/164-1/2=77/164.}
 \tag{8}
\]

These are uniform bounds on the retained rows, not computed actual
probabilities or chosen values of a component vector.

## 4. The empty ratio cancels its restoration power

RI145's held empty coefficient is

\[
 \epsilon_3=A_EG_E^3/B_E^3.
\]

The actual H5 identity is `G_E=theta w^2/e`, with `A_E=e,B_E=w`.
Hence

\[
 \epsilon_3=\theta^3w^3/e^2,\qquad
 \eta=\frac{\epsilon_3}{r}=41^2(w/b_0)^3.
 \tag{9}
\]

The numerator and denominator both contain `theta^3`. The historical C3
proper probability `e` is not `epsilon3`; replacing the latter by the
former would introduce a spurious inverse restoration power.

Using (8) before division gives

\[
 0<\eta<41^2(2/77)^3
   =\frac{13448}{456533}<\frac1{32}.
 \tag{10}
\]

The final bound comparison is the integer identity
`32*13448=430336<456533=77^3`. This is manual bound arithmetic, not
evaluation of an actual empty coefficient, ratio or probability.

## 5. First capacity and the exact disappearance of the multiplier

From `K0>2c0`, `theta^2 Z<2` and positivity,

\[
 0<j_0+gZ=1-\theta K_0+\theta^3c_0Z
 <1-\theta c_0(2-\theta^2Z)<1.
 \tag{11}
\]

All factors in (7) are positive. Combining (10), (11) and the same
inherited cap bounds gives

\[
 0<YE_{\rm env}
 <12(12/95)^2(8/41)(33/32)
 =\frac{14256}{370025}<\frac1{25}.
 \tag{12}
\]

The last exact comparison is `25*14256=356400<370025`.
Thus `1-YE_env>24/25`, independently of which retained row attains the
minimum in (6), whether minima tie, and whether either `N_i` vanishes.

Since `0<Z<1/4`, `d(Z)<6`, so `Y>1/6`. Together with `u3>3/2`,
this proves `Yu3>1/4`. Also `Yu3<1` follows from `Y<=8/41` and
`u3<2`. Thus

\[
 0<\frac{1-Yu_3}{1-YE_{\rm env}}<1.
 \tag{13}
\]

Equation (2) is an exact simplification of RI153's two strict capacity
conditions, not replacement by a larger sufficient factor.

Set

\[
 C_0=1-B/v,\qquad
 C_1=1-(1-Yu_3)B/v-YE_{\rm env}.
\]

Whenever `B/v<=1`, the positive multiplier `1-Yu3` gives

\[
 C_1\ge Y(u_3-E_{\rm env})>1/4-1/25=21/100.
 \tag{14}
\]

Therefore `C0>0,C1>0` is exactly (3). At equality `v=B`, (14)
still holds but `C0=0`: the first budget cannot pass because its other
term `A/mu` is strictly positive. For `v<B`, `C0<0`. Neither case
proves the sign of W. If `v>B`, the adequate q threshold still remains
an additional obligation; this note does not supply it.

## 6. Exact remaining contrast and one conditional obstruction

Retain the complete RI147 contrast identity. For `S=1,3,7`, define

\[
 \begin{aligned}
 d_S&=B_0(S)-B_1(S),&
 P_S&=(B_0(S)+B_1(S))/A(S),\\
 T_S^{\Delta}&=(B_0(S)^2+B_0(S)B_1(S)+B_1(S)^2)/A(S)^2,&
 \mathcal H_S&=P_S+2\theta-2-\theta^2T_S^{\Delta}.
 \end{aligned}
\]

Empty locality gives `d0=0`, and the retained core theorem gives
`d7=b0-b1>0`. Define only the actual signed ratios

\[
 \gamma_1=d_1/d_7,\quad\gamma_3=d_3/d_7,\quad
 \mathcal H=\mathcal H_7+\gamma_1\mathcal H_1+\gamma_3\mathcal H_3,
 \quad J=b_0^2+b_0b_1+b_1^2>0.
\]

The exact identities are

\[
 v=\theta d_7\mathcal H,\quad
 \lambda=d_7J/b_0^3,\quad
 \frac v\lambda=\frac{\theta b_0^3}{J}\mathcal H.
 \tag{15}
\]

No division by a signed or possibly zero contrast occurs. Positivity
of `v` implies `H>0`, but not a quantitatively sufficient lower bound.
Let

\[
 M_{\rm cap}=\max(E_0,E_1,F_0,F_1),\quad
 t=1/Z=2(1+M_{\rm cap}).
\]

This maximum is the selected cap, not the global six-parent maximum
`M6`. Equations (3) and (15) yield the exact remaining relations

\[
 \boxed{\theta b_0^3(t-1)\mathcal H>12j_0J,}
 \qquad
 \boxed{(1+2M_{\rm cap})v>12\lambda j_0.}
 \tag{16}
\]

Every occurrence of `F_i`, and hence `t`, still uses the same actual
canonical `N_i`. These are not free variables to tune independently
of the contrasts. No lower magnitude for the full signed `H` sufficient
for (16) has been proved here.

There is also a conditional obstruction. Since every `B_i(S)<1`
and `A(S)>=1/44`,

\[
 T_i<44K_i,\qquad 2c_i<K_i.
\]

Substitution in (5), using `theta<1/144`, gives

\[
 E_i<3+\theta K_i[-3+(3/2)\theta+44\theta^2]<3,
\]
\[
 V_i<1+\theta K_i[-1+\theta+44\theta^2]<1.
 \tag{17}
\]

The positive corrections in each bracket sum to less than one.
Since `V_i>j_i>71/72` and `v=V1-V0>0`,

\[
 0<v<1/72.
 \tag{18}
\]

If `max(F0,F1)<=3`, then `M_cap<=3`. A pass of (16) would require

\[
 \lambda<\frac{(1+2M_{\rm cap})v}{12j_0}
 <\frac7{852}.
 \tag{19}
\]

Thus the conjunction `max(F0,F1)<=3` and `lambda>=7/852` would
strictly obstruct this sufficient envelope. Neither premise of that
conjunction has been established at the actual prefix. In particular
(19) is not an actual obstruction, nor a W/H30 sign. If `Fmax>3`, this
conditional argument does not apply; the actual correlated (16) remains.

## 7. Reading, author-peer checks and stopping boundary

Literal historical reads in this contribution were:

- `/Volumes/AI_DATA/development/det-review-evidence/ri153-root-margin-review-sflbzpwj/NATIVE_SUCCESSOR_RESERVATION.json`: complete assignment.
- `/Volumes/AI_DATA/development/det-review-evidence/ri153-root-margin-review-sflbzpwj/RI153_ROOT_ADJUDICATION.json`: complete administrative decision, including its N01 limit on floor-domination claims.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md`: sections 1 and 3–7 selected text, including the all-row height theorem and complete C3 row. Its optional printed component minimum was considered but is not needed by this proof; no certificate body was decoded or run.
- `/Volumes/AI_DATA/development/det-review-evidence/ri147-native-scale-membership-q4lxbpke/ACTUAL_SCALE_BOUND.md`: retained complete sums, cap and sensitivity scope, sections 1–6 and 7–9 selected text; already accepted in the ancestry.
- `/Volumes/AI_DATA/development/det-review-evidence/ri147-native-scale-membership-q4lxbpke/COMPONENT_CONTRASTS.md`: exact contrast and ratio identities, sections 3 and 6 selected text; already accepted in the ancestry.

RI145's empty-term identity and RI153's exact capacity resolvent are
retained accepted premises. The current STRICT_CAPACITY_SYNTHESIS.md was
read completely as an author-peer check; its capacity and cap comparisons
agree with this derivation. This is not independent review. The native
coauthor supplied the detailed height incidence and (17)–(19); those
relations were manually crosschecked here. CAPACITY_STRUCTURE.md was also
read completely: its two-arm transport, positive F=3 threshold, exact cap
alternatives and conditional obstruction agree with this note.

Only this assigned Markdown is authored. No actual probability, component,
history, maximum, scale, H or z is evaluated; no scientific JSON is decoded,
engine used, source/helper imported, compiled, inspected through an AST,
probed or run. No global family enumeration, runtime/controller/fixture,
card/admission, repository/index/Git operation or sealed predecessor edit
is made. The withdrawn FS seed-order inference is not a premise. All
other connected parents, five Di systems, shared T1 recovery, strict
endpoints and original certificate inputs remain binding. RET remains
paused, and measurement remains separate. The sitting stops at the
proved first capacity, exact reduction (3), and unresolved comparison
(16); it does not assign a successor or promote a physical claim.
