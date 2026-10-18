# RI-70 — height freedom on the fixed primary defect-optimal face

24 September 2026 UTC. **Exact finite endpoint theorem; independently accepted
after coordinator adjudication.**
This packet retains the actual RI-63 parent-five history distribution, all
1,490 row caps, all 798 components, the primary defect objective and its
certified optimum. It measures height freedom on that existing optimal face;
it does not replace the candidate, canonical tie-break or actual strict law.

## Predeclared discovery and checking envelope

At most two endpoint LP searches are permitted, one for each height endpoint
on the existing parent-five problem. Each discovery/check attempt is limited
to 1,800 seconds and 2 GiB resident memory, with sampled/checkpoint enforcement
and one solver worker. This is not a hard OS allocator limit; unobserved
instantaneous overshoot is not excluded. Available numerical solvers may aid
discovery, but acceptance requires complete exact rational primal/dual
certificates and normal/optimized replay. No threshold will be weakened after
a failure. If exact endpoints cannot be certified within these bounds, record
the concrete obstruction and failed attempt, rather than broadening discovery.

No Pareto sweep, new-layer domain or optimizer, balanced target, law change,
informative QM or physical claim is permitted. Only `HEIGHT_TRADEOFF.md`,
`check.py` and `CERTIFICATE.json` in this directory are assigned. Accepted
sources, records, ledgers, measurement, RET and git/index operations remain
untouched. Stop at stable handoff for coordinator adjudication.

## 1. Fixed face, fixed history weights, and the result

Use the unchanged [RI-63 problem](../native_growth_expected_defect_completion_v1/COMPLETION.md):
all marked parent-five rows j, their actual prefix probabilities pi_j, all
labeled proper ideal occurrences and their positive potentials u_j(S).
The complete passive maps remain `q(S) D/2`, including the entire payload;
height is an unmarked diagnostic, not an informative quantum coupling.

Write A for the original 1,490-by-798 cap matrix, beta for the original
primary defect coefficient, and `B5` for its all-full baseline. The face is

\[
 \mathcal P=\{\alpha\ge0:A\alpha\le\mathbf1,
                    \ \beta\cdot\alpha=b\},\qquad
 b=m_5-B_5=-\frac{1512652301}{37480960000},\quad
 m_5=\frac{6650803}{108900000}. \tag{1}
\]

Every original coordinate remains, **including beta=0 coordinates**. The
canonical lexicographic rule is not imposed on this face. It only identifies
one retained comparison point. Strict positivity of inherited potentials
and a cap occurrence for every component make the original polytope bounded;
the existing canonical certificate supplies a point in the closed face.
Both height extrema are therefore attained.

Let H be the pi-weighted expected **one-birth height increment**, not the
expected terminal height. Exact rational certification gives

\[
 \boxed{\min_{\alpha\in\mathcal P}H(\alpha)
       =\frac{69729502462340410231}{79331762158387200000},\qquad
 \max_{\alpha\in\mathcal P}H(\alpha)
       =\frac{330159038233}{337328640000}.} \tag{2}
\]

| Boundary completion on the same primary-optimal face | Expected height increment |
| --- | ---: |
| Certified minimum | 0.8789607159251585 |
| Existing canonical choice | 0.9658893763118028 |
| Existing retained alternative | 0.9748692095735938 |
| Certified maximum | 0.9787459441125426 |

The order is strict. The interval width is exactly
`7916137989481949609/79331762158387200000`. Thus neither retained point
is height-extremal. No endpoint is adopted as the actual law.

## 2. Affine height objective and intrinsic component factor

Every maximal birth changes longest-chain cardinality by zero or one, while
a full birth adds exactly one. For a proper slot put
`z_j(S)=h(P_j+x_S)-h(P_j)`. Its probability is `u_j(S) alpha_c`, and the
full probability is the complement of the entire proper row sum. Therefore

\[
 H(\alpha)=\sum_j\pi_j\left[1+
       \sum_{S\subsetneq P_j}u_j(S)\alpha_{c(j,S)}(z_j(S)-1)\right]
       =1+\kappa\cdot\alpha,
\]
\[
 \kappa_c=\sum_j\pi_j\sum_{S:c(j,S)=c}u_j(S)[z_j(S)-1]. \tag{3}
\]

The leading one uses `sum pi_j=1`. Neither uniform row weights nor one
representative per isomorphic ideal is substituted for this history sum.
Fair newborn marks sum to one for this mark-independent observable; all
old marks and their history probabilities remain in the coefficients.

For a proper component c with terminal Q, use
[RI-66's marked-fiber factorization](../native_growth_terminal_cost_v1/FACTORIZATION.md).
Its general role-statistic identity gives

\[
 \boxed{\frac{\kappa_c}{U_c}
  =\frac{\sum_{v\in\operatorname{Max}(Q)}e(Q-v)
                   [h(Q)-h(Q-v)-1]}{e(Q)}.} \tag{4}
\]

All concrete maximal-deletion roles retain their e(Q-v) multiplicities.
The positive marked-fiber constant cancels in the ratio, not in U_c or row
caps; components sharing Q are not merged.

In fact `kappa_c<0` for every proper component, not merely nonpositive.
There are at least two maxima in Q. Choose a longest chain ending at one
maximum v, and another maximum w. Deleting w preserves that chain and hence
height, giving a strictly negative term of positive weight in (4); every
other term is nonpositive.

It follows that every height maximum on this primary face has zero
allocation on beta=0 coordinates: removing a positive such coordinate
preserves the primary equality, relaxes all caps, and strictly increases H.
There is no corresponding justification for excluding these coordinates
from the minimum problem. The exhibited minimum uses 70 positive beta=0
coordinates; this is not a claim that every minimizing witness has that
same support.

## 3. Exact original-face primal/dual certificates

The [certificate](CERTIFICATE.json) stores one attained primal and one dual
for each endpoint. For sign `s=+1` at the minimum and `s=-1` at the maximum,
the checker requires

\[
 \alpha\ge0,\quad A\alpha\le\mathbf1,\quad\beta\cdot\alpha=b,
\]
\[
 y\ge0,\quad\lambda\in\mathbb Q,\quad
 g=s\kappa+A^Ty-\lambda\beta\ge0,
\]
\[
 s\kappa\cdot\alpha=-\mathbf1^Ty+\lambda b. \tag{5}
\]

For every feasible x, the dual inequalities give
`s kappa.x >= -sum y + lambda b`. Equality at the supplied primal proves
the respective minimum or maximum, without trusting a numerical solver's
status. The equality multiplier is unrestricted in sign. All 1,490 caps,
798 dual inequalities and the primary equality are checked as exact fractions.
The checker also verifies complementary slackness, rather than using it as
an assumed shortcut.

| Certificate diagnostic | Minimum | Maximum |
| --- | ---: | ---: |
| Positive primal coordinates | 140 | 65 |
| Positive beta=0 coordinates | 70 | 0 |
| Positive dual row multipliers | 183 | 76 |
| Tight original caps | 826 | 434 |
| Zero dual reduced-cost columns | 209 | 76 |
| Equality multiplier lambda | `-9797/3234` | `-7/2` |

The minimum's signed primal/dual objective is
`-9602259696046789769/79331762158387200000`; the maximum's signed objective
is `7169601767/337328640000`. Adding the appropriate height baseline recovers
(2). These certify endpoint values, not uniqueness of either endpoint vector.

## 4. Bounded discovery and exact recovery

Exactly two numerical LP searches were made, one per endpoint. No solver was
installed. Discovery reused the existing external RI-63 proposal packages
at `/private/tmp/ri63-proposal.Hzz43L`, with CPython 3.12.14, NumPy 2.3.5 and
SciPy 1.16.3. HiGHS dual simplex was given one worker, parallel mode off,
one-thread BLAS settings and a time limit inside the predeclared envelope.
The standalone acceptance checker uses none of these numerical packages.

For discovery only, use the accepted primary dual y0 and its reduced costs
`r0=beta+A^T y0>=0`. Because `b=-sum y0`, the exact face is equivalently
the original caps with coordinates outside `C={c:r0_c=0}` fixed to zero and
rows `J={j:y0_j>0}` saturated. This follows by expressing the primary duality
gap as the sum of nonnegative products. Here C has 256 columns, **including
144 beta=0 columns**, and J has 76 rows. This reduction preserves the full
face; it is not canonical lexicographic elimination.

Variables were scaled by their largest cap coefficient and the objective
by 1,000,000 for numerical discovery. Returned supports proposed exact linear
systems. Rational elimination recovered the primal and reduced dual:
the minimum systems had ranks 140/140 and 171/171; the maximum systems had
ranks 65/65 and 67/67. No free approximate rational choice was needed.

For completeness, the exact reduced dual can be returned to the original
face without assuming missing-column inequalities. Suppose its nonnegative
cap multipliers are y and its unrestricted saturated-row multipliers are z.
Pad z by zero outside J, put `q=y-z` and `g=s kappa+A^T q`. The reduced
dual requires `g_c>=0` on C. Choose

\[
 t=\max\left(0,\max_{j\in J}\frac{z_j-y_j}{(y_0)_j},
                   \max_{c:(r_0)_c>0}\frac{-g_c}{(r_0)_c}\right).
\]

Then `y'=q+t y0>=0`, `lambda=-t`, and the original-column reduced costs
are `g+t r0>=0`. The dual value is unchanged because `b=-sum y0`.
The stored certificate contains this **full original-face** dual, which
the verifier checks directly without relying on the reduction or backlift.

| Discovery attempt | Simplex iterations | Elapsed seconds, including exact recovery | Checkpoint peak RSS |
| --- | ---: | ---: | ---: |
| Minimum | 132 | 6.444 | 184,483,840 bytes |
| Maximum | 52 | 6.392 | 178,896,896 bytes |

Both completed inside the unchanged bounds. Alarms, solver time limits and
peak-RSS checkpoints enforced the declared envelope; no hard allocator cap
is claimed. There were no failed endpoint searches, no additional LP calls
for recovery, no Pareto sweep and no higher-layer search.

## 5. Canonical comparison and unchanged strict mixture

The exact retained heights are

\[
 H_{\rm canonical}=\frac{25799901101980099}{26711031029760000},\qquad
 H_{\rm alternative}=\frac{10372327938670249993}{10639712319160320000},
\]
\[
 H_{\rm alternative}-H_{\rm canonical}
 =\frac{37452794291157419}{4170767229110845440}>0. \tag{6}
\]

The current value is therefore not uniquely forced by primary defect
optimality. The canonical tie-break chooses one interior height value;
it does not minimize or maximize height on this face. Conversely, compatibility,
the fixed prefix and primary optimality jointly impose the nontrivial lower
endpoint in (2). This is a one-layer constraint, not an established persistent
high-height bias or a claim about the tie-break's intent.

For arithmetic comparison only, keeping the same `eta5=1/36` and same interior
vector `c5` maps any endpoint to

\[
 H_{\rm hypothetical\ strict}(\alpha)
   =\frac{35}{36}H(\alpha)+\frac1{36}H(\boldsymbol c_5). \tag{7}
\]

The checker reports these counterfactual values exactly. All such mixtures
have the same primary expected defect increment, but their height increments
differ. The actual law still uses the existing canonical vector. Adopting
another point would change q5 and later history probabilities and potentials;
previous later-layer calculations cannot automatically be transferred to it.
No such adoption occurs here.

## 6. Verification and research boundary

The [standard-library checker](check.py) first replays the accepted RI-63
canonical certificate, alternative witness, strict rows, complete diamonds
and its 15 certificate controls through the pinned RI-66 helper interface.
It explicitly reuses the pinned RI-66 terminal/component certificate, rather
than claiming a fresh complete marked-fiber reconstruction. Its extension
counts, terminal factors and component masses are checked against newly
computed height statistics and raw marked weights. All five accepted byte
pins are verified before loading and again before completion.

New coefficient reconstruction covers all 11,424 raw marked histories and
142,944 labeled proper slots, independently reconciled with the 1,490
canonical rows and 15,702 labeled occurrences. It covers all 2,961 local
nodes, 4,467 natural proper terminal orders, 5,181 parent/terminal height
orders and 255 intrinsic terminal types. Heights computed by recurrence
are also checked against exhaustive chain subsets. All 798 coefficients
are strictly negative and satisfy (4). No solver is present in the checker,
and no q6 probability or concrete order above size six is evaluated.

Fourteen intended-reason controls reject dependency corruption, wrong input
manifest, a missing endpoint, a negative primal coordinate, an original cap
violation, a row-feasible point off the primary face, a negative inequality
dual, a full-column dual violation, a positive exact primal-dual gap, an
incorrect claimed height, a noncanonical equality multiplier, a corrupted
intrinsic coefficient, one actually omitted raw marked-slot contribution,
and duplicate JSON keys. The gap control adds a positive row multiplier,
preserving dual feasibility while changing its objective. Negative equality
multipliers are valid and are not rejected merely for their sign.

Independent verification did not rely only on replaying the new checker.
A separate reviewer rebuilt A, beta and kappa from pinned RI-63 data and
all raw marked histories, using an independent exhaustive-chain height
routine and forward ideal-prefix dynamic programming for extension counts.
It checked all 255 terminal types, 671 maximal roles, and both full original
primal/dual certificates, including direct full-complement height expectations.
The audit took 5.752 seconds, with checkpoint peak RSS 113,803,264 bytes;
its height and extension caches contained 4,887 and 352 orders respectively.
Its coefficient hash and endpoint values match exactly. A separate read-only
evaluation also independently recovered both retained heights in (6).

Reproduction from the repository root requires no numerical packages:

```sh
python3 -I -S -B docs/track_b/native_growth_height_tradeoff_v1/check.py
python3 -I -S -B -O docs/track_b/native_growth_height_tradeoff_v1/check.py
```

The main worker ran both commands at the final source pin using CPython
3.14.0 and the predeclared sampled parent watchdog. Both exited zero in
11.890/11.902 seconds, with sampled peak RSS 125,943,808/125,304,832 bytes.
Their 2,723-byte stdout is byte-identical, SHA-256
`b053b8c9c3c964834cc035293cab4b8c7420a006687e870eb59db930953e8b1e`.
The checker author independently replayed the final pin in 11.838/11.853
seconds. The separate reviewer replayed it in 11.840/11.822 seconds with
checker resource checkpoints and an outer timeout, without separate RSS
sampling. All runs passed both endpoint proofs and every new control.
Two independent reviewers read the complete proof, checker and certificate;
the final source adjustment only clarified that file **writes** are absent.

Stable pins:

- `check.py` (24,804 bytes, 448 lines):
  `af145a06b8028533d85be5853a4e840735a2ccf2e673846ad5465cb58b793995`;
- `CERTIFICATE.json` (16,123 bytes, 493 lines):
  `de716ec1e07274ebdb431b6d7e2ccd37ba21af67268d208923db76d95c51c8dd`;
- complete derived height problem:
  `69db0630770c4a0f61ed234e974d8c699e6ea29c6bac4ed9d566ad0a7fad22ba`;
- exact kappa vector:
  `c275ff5a025dac8e02f836511e96c16adf83c0a764eab7a7c6c64db37df49d35`.

**Disposition:** both height endpoints are attained and exactly certified
on the original primary-optimal face. Primary defect optimality does not
determine a unique height; the canonical tie-break selects a nonextremal
value at this layer, and the actual law is unchanged.
The finite interval concerns only the accepted parent-five primary-optimal
face. It neither proves all-size height control nor recovers balanced Ferrers
scaling, dimension, a metric, mass or gravity. In particular it does not
resolve [RI-69's](../native_growth_top_drift_v1/TOP_DRIFT.md) signed recharge
and endpoint-balance problem. Option B and Status M remain unchanged. Exactly
the three assigned files are authored; stop at stable handoff for coordinator
adjudication, with no successor work begun.
