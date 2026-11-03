# A fixed reciprocal exchange violates a native joint diamond

**Accepted GDM061 conditional obstruction, 3 November 2026.** For the exact interaction J=X(B tensor I2) with fixed source/response coordinates, one lawful singleton-parent diamond has unequal complete joint maps. Its input/output(0,0) entry difference is −epsilon(3+4epsilon)/160, epsilon=1/8448. This rejects the specified attachment. It leaves the accepted primitive B and the broader question of reciprocal interactions intact.

This note is a standalone assembly of the accepted counterexample, not a new calculation. The inherited primitive is the exact [active residual law through four births](../track_b/native_active_residual_v1.md), with original structural q from [Part A of its marked-law source](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix). The proof below displays every q/r coefficient and domain fact needed for this particular obstruction. The full source/domain remains fixed; changed-mark Part B is not an input.

## 1. Exact admitted question and inputs

The independently accepted GDM060 question fixes the source coordinate s and response coordinate y in {0,1}, the whole R_+^4 cone and normalized Delta4 at every parent, and trivial carrier action under native vertex relabeling. Arbitrary correlated and boundary inputs are allowed. The source/response labels cannot alternate between prefixes.

The proposed branch and disabled comparison are exactly

    J_a(s',y' | s,y) = B_a(y' | s) 1_(s'=y),
    C_a(s',y' | s,y) = B_a(s' | s) 1_(y'=y),

where a=(P,S,b) is an actual native branch. J=X(B_a tensor I2), with exchange AFTER B at every birth; C=B_a tensor I2. The fixed exchange is a supplied interaction, not an additional record, observed intermediate state or silent step. A changed source marginal is expressly allowed for J. It does not remove the requirement for equality of complete joint maps at a transported endpoint.

Use only the accepted original active B and original Part A structural q. The active law has

    B_(P,S,b) = [q_P(S)/2] M(r_P(S)),
    M(r) = (1/2) [[1+r+t, 1-r-t],
                  [1+r-t, 1-r+t]],   t=1/2,

    r_P(S) = theta 2^n chi(P)
                 [a_(n+1) 1_(S=empty) - a_n],
    theta=1/32, a_1=1/264, a_2=1/176.

Here n is the parent size and chi is one for an antichain, zero otherwise. The named coefficients are the accepted ones, not new choices. The full source also fixes all remaining parents through size three and the terminal size-four rule. Those coefficients need not be changed or exhaustively recomputed to refute a required identity at size three.

The original q excerpt specifies singleton empty/full probabilities 2/3 and 1/3, two-antichain singleton probabilities 1/10 for EACH actual singleton ideal, and two-chain empty probability 1/5. All newborn bits have their retained factor1/2. These are original Part A rows; no changed-law source is used.

## 2. Full two-step joint composition

Use tensor order (source,response), with basis ordering (0,0),(0,1),(1,0),(1,1). For any two chronological branch matrices B_1 then B_2, the fixed exchange gives

    [J_2 J_1]_(s2,y2;s0,y0)
      = sum_(s1,y1) B_2(y2|s1) 1_(s2=y1)
                        B_1(y1|s0) 1_(s1=y0)
      = B_1(s2|s0) B_2(y2|y0).

Consequently

    J_2 J_1 = B_1 tensor B_2.                         (1)

This is an equality of complete unnormalized four-by-four maps, with all intermediate indices summed. It holds on arbitrary columns, not just factorized preparations. It is not the ordinary native product B_2 B_1 tensored with identity. Thus the accepted native diamond identity by itself cannot certify the exchange attachment.

Equation (1) is the composition used to inspect the required diamond below. No coordinate exchange is appended to the terminal transport: the control fixes the source/response identification at every parent.

## 3. An admitted marked diamond and its transport

Let the base parent P consist of one vertex v, marked0. Choose its two actual ideals E=empty and F={v}. Let the two new vertices be a and d, each marked0. They are incomparable in the final order, whose only strict relation is v<d; a is isolated.

The two chronological paths are:

| Path | First birth | Intermediate parent | Second birth | Final marked order |
| --- | --- | --- | --- | --- |
| Left L | a over E, bit0 | A={v,a}, a two-antichain | d over the actual proper ideal {v}, bit0 | v<d, isolated a; all marks0 |
| Right R | d over F, bit0 | H={v<d}, a two-chain | a over empty, bit0 | v<d, isolated a; all marks0 |

The old vertex v is fixed by the endpoint identification; the newborn natural labels are transported so the semantic vertices a and d match. Their marks match. Carrier coordinates (s,y) are unchanged by that transport. On the left the second precursor excludes a; on the right it excludes d. In particular, the old full ideal F becomes the PROPER ideal {v} in the left intermediate antichain, exactly as the native rule requires. No unavailable future vertex is included in a precursor.

Every parent, ideal and bit in this table is admitted, and every branch has positive native support. The initial joint basis column e_(0,0) is in the declared full Delta4 at P. It need not be obtained by postselecting a history from empty: full-domain consistency is explicitly required at every parent. No additional preparation or measurement premise is used to choose a legal matrix-test input.

This is one required diamond inside the four-birth horizon. Finding it is sufficient to refute universal admission; no assertion that it is the earliest or smallest possible failure is needed.

## 4. Exact coefficients and differing matrix entry

Write epsilon=1/8448. Substitution of the accepted coefficients gives the four native factors used in this diamond:

| Native branch | q | r |
| --- | ---: | ---: |
| P,empty,0 | 2/3 | (1/16)(1/176-1/264)=epsilon |
| A,{v},0 | 1/10 | -(1/8)(1/176)=-6epsilon |
| P,{v},0 | 1/3 | -(1/16)(1/264)=-2epsilon |
| H,empty,0 | 1/5 | 0, since chi(H)=0 |

The complete scalar factors, including BOTH retained newborn-bit halves, agree:

    [(2/3)(1/10)]/4 = [(1/3)(1/5)]/4 = 1/60.

Using (1), the two transported joint maps are therefore

    L = J_(A,{v},0) J_(P,empty,0)
      = (1/60) M(epsilon) tensor M(-6epsilon),

    R = J_(H,empty,0) J_(P,{v},0)
      = (1/60) M(-2epsilon) tensor M(0).               (2)

These equations retain the full branch weights. There is no normalization by an endpoint probability, averaging over natural labelings, detector projection or trace over the response.

For the admitted input e_(0,0), inspect output coordinate (0,0). Since M(r)_(0|0)=3/4+r/2, (2) yields

    L_00,00 = (1/60)(3/4+epsilon/2)(3/4-3epsilon),
    R_00,00 = (1/60)(3/4-epsilon)(3/4).

Subtracting these exact entries,

    L_00,00 - R_00,00
      = (1/60)[-9epsilon/8-3epsilon^2/2]
      = -epsilon(3+4epsilon)/160 < 0.                 (3)

The strict sign follows from the fixed positive epsilon. Both entries are subnormalized components of legal positive branch compositions. Their inequality proves L is not R as a four-by-four map. One basis entry is enough to refute equality on the whole cone. The corresponding native scalar q diamond has equal weights, and the accepted native B remains its own full-map-consistent model; it is the new interleaved exchange attachment that fails the required joint identity.

Equation (3) is the first failed required identity encountered in this assessment. It closes this candidate. The report records that witness rather than attempting to certify remaining diamonds, longer suffixes or the disabled comparison as a separate new result.

## 5. Stop, scope and what is not concluded

The conjunction required for stage1 admission is false. Neither remaining admission checks nor stage2 directional observations can turn the false joint identity into a lawful instrument on the fixed domain. In particular, a scalar normalization, a selected initial distribution or an observation that hides the differing entry would not meet the stated full-map requirement.

No source-to-response TV, response-to-chain difference, complete detector law or detection-conditioned quantity is evaluated. No claim is made about the signs of those proposed statistics. The failure occurs before they are authorized. No exchange strength, trigger, coordinate transport, noise, reservoir, preparation, readout or horizon is modified. No physical conservation premise is added to rescue the construction.

The rejection is specific to J=X(B tensor I2), applied at every birth with the fixed s,y identification and the exact active B. It is not a theorem forbidding every reciprocal law, every source/probe coupling or all native matter/geometry models. It does not reverse GDM060's question admission: that review admitted this precise test, not a candidate result. It neither repairs nor reopens GDM057, and it uses no GDM059 or CL055 scientific result.

The supplied response bit has no derived geometric, gravitational, mass, clock or energy interpretation. Probability mass is not physical mass. No quantum structure, physical unit, calibration, resource closure, empirical inference or alternative law follows. Option B and Status M remain unchanged. The exact rejection has completed distinct scientific review and coordinator disposition. This publication supplies no replacement law or execution authority.


## Source identity and permanent qualifications

The native active-law dependency has SHA256 `cd6f99fcb2e2d7f52c6fe3a7f42d769ac36931ecaab7ff942e790acbfaf5f48a`. The original-q safe Part A excerpt is3,571 bytes, SHA256 `8cdb20e81203b18ab610d8eda5ec108184e6edcb4c9015dde2d2882ed3ad3c38`, exactly original source bytes1281:4852; original source identity is `0c3cc5a4e1b9ea6dc8d2d2579522c81b4a55f3c7e5040aef11f28ef9d38d4422`. These are inherited exact dependencies, not permission to substitute changed-law material.

The accepted GDM061 author REPORT is11,741 bytes, SHA256 `9716b2b91e969ed628bde834b059b34799a144223fd32a50edc2ebb3341cec01`. Distinct scientific REVIEW is10,459 bytes, SHA256 `b909684e87634b1e63d90134e2af8e0f3b34a682158be5e5c4867f8c760268e3`. Coordinator disposition is2,162 bytes, SHA256 `3738f677f770bfae29cea5f93520412f13f8ca24a39b064b68129550dc0ae120`. Source/payload custody is retained in their frozen packets; identity hashes do not independently prove mathematics or acceptance.

Historical qualifications remain permanent: GDM057's heading-only Part-B intake overread; GDM054 and prior author/reviewer/coordinator timing incidents; and the earlier GDM059 publication author's late persisted-file readback. That earlier readback completed after its substantive cutoff despite timely rendering of written strings. The present assembly neither changes nor retrospectively certifies those procedures. No additional scientific admission is inferred from publication. Software remains paused, and calibration, custody, independent review and execution gates remain unchanged.
