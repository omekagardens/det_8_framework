# Actual scale membership and the remaining component comparison

This note strengthens the actual normalization bounds and controls the
previously unresolved singleton residual without treating it as a free
coefficient. Together with COMPONENT_CONTRASTS.md and ACTUAL_SCALE_BOUND.md,
it supplies new conditional analytic comparisons for the fixed baseline.
**It does not prove that the actual weighted margin is nonpositive.** No
actual probability, component coefficient, maximum, scale, seed or H value
has been evaluated. The result is author work requiring nonauthor review.

## Premises and notation

Retain RI145's exact weighted identity, accepted positive q on [0,X],
positive v and D3, X=min(R,1/4), and all fixed baseline and seed premises.
The records i=0,1 differ only at the root. The four ideals S=0,1,3,7 form
the complete C3 row A(S), with A(0)=A(1)=A(3)=1/44 and A(7)=41/44.
They are the four stem entries of the C4 row B_i, whose positive full
complement is c_i. Thus sum A=1 and sum B_i=1-c_i. No repeated labeled
ideal is collapsed in any row sum.

The component definition and strict mixture are the actual RI41 and RI63
ones. In particular, with beta_i=B_i(1),

    theta = 1/[72(1+M5)],
    N_i = kappa_i beta_i,
    kappa_i = (35/36) alpha_min,c5(1,i) >= 0,
    omega_i = theta beta_i/A(1) = 44 theta beta_i.

The symbol beta_i here is a held singleton probability, not either local
pivot ratio. The component index is the accepted complete ratio-graph
assignment, not a new index chosen by this proof. N_i and beta_i cannot be
varied independently. No sign of kappa_0-kappa_1 is presumed.

## A strict size five bound from one complete parent

Consider H5=C3 ordinal-sum A2, with the transported record i. The two
singleton maximal deletions both leave C4, while deleting both maxima
leaves C3. Hence RI38's potential is B_i(S)^2/A(S) for each stem ideal.
For each of the two distinct one-cap ideals its potential is c_i. Its
complete proper-potential sum is therefore

    K_i = sum_S B_i(S)^2/A(S) + 2c_i <= M5.

Put mu_i=1-c_i. Expanding squares and using the two complete row sums gives

    K_i = 1+c_i^2 + sum_S A(S)[B_i(S)/A(S)-mu_i]^2 > 1.

Strictness follows from c_i>0 even if the square sum vanishes. This is a
single-parent analytic inequality, not a reconstruction or evaluation of
the global maximum. It proves, for each i,

    0 < theta <= 1/[72(1+K_i)] < 1/144,
    0 < omega_i < 11/36.

All six proper H5 slots have actual restoration coefficient theta by the
accepted prefix lemmas, including each one-cap slot h_i=theta c_i. Hence
j_i=1-theta K_i, and K_i<=M5 implies

    theta K_i <= M5/[72(1+M5)] < 1/72,
    j_i > 71/72.

RI117's complete proper-potential sum E_i for C3 ordinal-sum A3 is the
positive four-term stem sum plus 3m_i+3j_i. Consequently

    M6 >= E_i > 71/24,
    0 < rho = 1/[2(1+M6)] < 12/95 < 1/4.

This constant comparison does not replace the stronger held E_i bound R.
The companion scale proof also retains the additional C4 ordinal-sum A2
bound, with the actual C5 singleton correction still present. No size-five
common-scale law is substituted for the strict mixture.

## Positive singleton factors with retained correlations

For 0<=x<=1/4 define

    k_i(x) = 2-x-2omega_i+theta x^2 omega_i^2.

The exact singleton part of RI145's q residual is

    (x-2)Delta N + 2Delta(N omega)-theta x^2 Delta(N omega^2)
      = N_0 k_0(x)-N_1 k_1(x),

where Delta means record1 minus record0. Let

    d_1=beta_0-beta_1,
    p_1=(beta_0+beta_1)/A(1),
    t_1=(beta_0^2+beta_0 beta_1+beta_1^2)/A(1)^2,
    h_*(x)=2-x-2theta p_1+theta^3 x^2 t_1,
    delta_kappa=kappa_0-kappa_1.

Factoring differences of the square and cube of beta gives the exact
correlated decomposition

    N_0 k_0-N_1 k_1
      = kappa_0 d_1 h_*(x)+delta_kappa beta_1 k_1(x).       (1)

This identity includes kappa_0=0, kappa_1=0 and d_1=0; none is divided by.
It does not assert that the two singleton slots share a component or that
their canonical coordinates are equal.

The stronger omega bound yields uniform strict factors

    41/36 < k_i(x) < 2,
    19/36 < h_*(x) < 2.                                  (2)

For the lower bounds, use 2-x>=7/4, omega_i<11/36 and
theta p_1=omega_0+omega_1<11/18, retaining the nonnegative square terms.
For the upper bounds, both functions strictly decrease on [0,1/4]. Indeed
k_i'=-1+2theta x omega_i^2<0. Also
theta^3 t_1=theta(omega_0^2+omega_0 omega_1+omega_1^2)<1, so
h_*'=-1+2theta^3 x t_1<0. Their values at zero are strictly below two.
The argument covers both endpoints, including the formal zero endpoint;
zero remains excluded as an actual scale.

Write z^+=max(z,0) and z^-=max(-z,0), only for the fixed signed contrasts.
Multiplying (2) with the appropriate inequality direction in (1) proves
the uniform lower bound

    N_0 k_0-N_1 k_1 >= C_N,
    C_N = kappa_0[(19/36)d_1^+ - 2d_1^-]
          +beta_1[(41/36)delta_kappa^+ - 2delta_kappa^-].   (3)

This is a justified lower bound, not a claim that C_N is positive. The
non-strict form includes all zero coefficients and contrasts. In particular,
N_i>=0 alone does not make the residual nonnegative.

## The precise remaining actual component premise

For each stem ideal define d_S=B_0(S)-B_1(S),
p_S=(B_0(S)+B_1(S))/A(S), and
t_S=(B_0(S)^2+B_0(S)B_1(S)+B_1(S)^2)/A(S)^2. The component proof derives

    v = theta sum_S d_S[p_S+2theta-2-theta^2 t_S],
    D3 = theta^3 d_7 t_7 > 0,
    q(x) = T(x)+kappa_0 d_1 h_*(x)
                    +delta_kappa beta_1 k_1(x),
    T(x) = theta sum_S d_S[(4-2theta-2x)p_S
                   -theta^2(1-theta x^2)t_S
                   +5theta-6+(4-2theta)x-theta^2x^2].      (4)

In particular q(x)>=T(x)+C_N on [0,1/4]; dividing by D3 preserves the
direction. Neither this floor nor the signed sum for v has been shown
large enough for the actual weighted obstruction. These expressions keep
the accepted component lookup, the singleton correlations and the actual
normalization. They are not unconstrained positive parameters.

For clarity, any proposed uniform target lower bound q(x)/D3>=b>0 on an
actual-containing interval [0,Z] is equivalent, using beta_1 k_1>0, to
the following *specific actual canonical component comparison*:

    delta_kappa >=
      [b D3-T(x)-kappa_0 d_1 h_*(x)]/[beta_1 k_1(x)]
      for every x in [0,Z].                               (5)

Here b is a conditional bound to justify, not a fitted coefficient or a
chosen native scale. The companion ACTUAL_SCALE_BOUND gives the precise
compensation budget that b and a lower bound for v/D3 must satisfy.
Equation (5) identifies the missing component comparison more sharply than
an unspecified DeltaN; it does not prove it. The canonical coefficient
contrast is fixed by RI63's accepted optimization, and its ordering or
magnitude cannot be inferred merely from nonnegativity or from the graph
definition. We have not proved that no further analytic derivation exists.

## Cases checked and stopping point

All divisions above have named positive denominators A(S), beta_1,
k_1(x), D3, and 1+M_n. The two cap ideals remain separate. If the square
sum in K_i vanishes, c_i>0 still gives strictness. If either canonical
singleton correction is zero, (1)--(5) remain valid. No division by a
signed contrast, N_i or a canonical coefficient occurs. Actual rho is
strictly positive and strictly below 12/95; all displayed formal endpoint
bounds remain valid at x=0 and x=1/4. There is no boundary-law admission.

The exact outcome is a stronger actual scale enclosure and correlated
component reduction. Actual rho<=delta0, actual W<=0, the separate C2/C3
signs and the full shared H30 system remain unresolved. The original
P2/P3 targets and Y=1/4 are unchanged, as are the 31/139/20/42 obligations,
shared T1 recovery, other eight connected parents and all five Di systems.
RET remains paused and measurement remains separate. No new executor,
controller, admission, numerical calculation, gravity/QM promotion or
successor assignment is made. Repository, index, Git and predecessors are
unchanged; this packet stops for nonauthor review and root adjudication.

## Literal source premises

The source selection includes each literal path separately, including
byte-identical external and published counterparts. The load-bearing texts
for this note are:

- `/Volumes/AI_DATA/development/det-review-evidence/ri145-native-weighted-margin-proof-zo96x_ci/WEIGHTED_MARGIN_PROOF.md`
  and ENDPOINT_REDUCTION.md: exact W, q residual and unchanged domains.
- `/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn/ANALYTIC_PREFIX_LEMMAS.md`
  and F2_ANALYTIC_CHECK.md: complete H5 entries and the C5 singleton exception.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md`:
  actual component law, fixed C3 probabilities and complete row sums.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md`:
  actual canonical mixture and M5 definition.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_joint_growth_extension_criterion_v1/CRITERION.md`:
  maximal-deletion potential and global half-scale definition.

The companion notes identify additional literal source reads and preserved
accepted-premise boundaries. Scientific bodies remain opaque; manual algebra
and new administrative byte/reference checks are not scientific execution.
