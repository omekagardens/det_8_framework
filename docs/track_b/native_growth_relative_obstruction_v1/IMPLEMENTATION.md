# RI-91 — bounded relative-continuation obstruction checker

25 September 2026 UTC. **Source preparation; no new coefficient result.**
This packet implements only the two-record test in accepted
[RI-89 equations 23–27](../native_growth_relative_continuation_v1/CONTINUATION.md).
That proof note is 21,769 bytes, SHA-256
`56c45bb5aba5e9fa0ab1f09ff959a73235939cc850e6fdde91a4cc39180b5cd1`.
The coordinator owns source acceptance, publication and any later execution.
Writing the checker or this protocol grants no execution authority.

The sole repository reservation is this note and `check.py` in this new
directory. A new `CERTIFICATE.json` must remain absent until genuine,
separately admitted execution. No accepted source, held probability,
coordinator record, core, QR-MAP or RET file is changed. Git/index operations
remain with the coordinator.

## 1. Mathematical question and what is already settled

RI-88 established a positive seven-birth prefix, with record-blind multiplier
h7 on its eleven frozen classes. RI-89 proves an exact continuation
criterion, not an automatic all-size record-blind extension. For common
level-seven scales s=a7^B and t=a7^h, proper-birth terminal ratios are
intrinsic products of h7 over maximal deletions. Full-birth ratios still
require record independence of

\[
 h_7(P)\frac{1-tV(P,r)}{1-sU(P,r)},
 \tag{1}
\]

where U and V are the baseline and modified proper-potential sums.
The unchanged RI-79 two-minimum contrast, as proved in RI-89, already
forces t=s if all relative weights are to remain record-blind. This
checker does not recompute that contrast or its coefficients.

Freeze P_star=C3 ordinal-sum A4=(0,1,3,7,7,7,7) and records r=0,1,
with only the initial stem bit changed. Let rho=a6 remain formal, and
write D_r(rho)=V_r(rho)-U_r(rho). The remaining pair condition is

\[
 F(\rho,s)=A(\rho)-sC(\rho)=0,
 \quad A=D_1-D_0,\quad C=D_1U_0-D_0U_1.
 \tag{2}
\]

The accepted baseline fixes unknown global scales rho and s. Neither is
selected or numerically evaluated by this checker. A nonzero value of F
throughout an outer domain containing the actual scales suffices to
reject record-blindness of this common-scale continuation class. A zero
or inconclusive pair does not establish the universal criterion.

The notation D_r in (2) is a scalar potential difference, not the passive
quantum payload D in the growth maps. No payload is discarded or treated
as a scalar trace by this interpretation.

## 2. Exactly the accepted certificate inputs

The only runtime scientific dependency is
`../native_growth_four_vertex_cap_check_v1/CERTIFICATE.json`, the complete
unmodified accepted RI-88 witness:

- Bytes: 1,828,149.
- SHA-256:
  `ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b`.
- Scientific schema: `ri88-four-vertex-cap-v1`.
- Accepted producer identity:
  `93eb721e933d90ba922b62f8a6844b64529d2acee1ae3bb3e15c81c4de153568`.
- Accepted RI-85 design identity:
  `e0dd0b046d80564ddc4e6ffef78853156f5c418b327917f1d5fadc4e229ab58a`.

Authenticate the whole dependency before extracting any numerical input.
The accepted prefix identities inside it are provenance pins, not modules
to import or probability tables to rebuild. RI-89's proof-note identity
is also provenance, not another executable dependency.

Only the following six complete held rows and three h7 multipliers may
enter new arithmetic:

| Held order | Complete records | Individual ideal masks | Slots |
|---|---|---|---:|
| C3=(0,1,3) | 0,1 | 0,1,3,7 | 8 |
| C4=(0,1,3,7) | 0,1; top zero | 0,1,3,7,15 | 10 |
| H5=(0,1,3,7,7) | 0,1; both tops zero | 0,1,3,7,15,23,31 | 14 |

H1,H2,H3 are the first three accepted entries in RI-88 `admission.h`,
in the frozen T1,T2,T3 order, with H1=5/4. They are positive unmarked
multipliers, not held probabilities. No C5 row or other h coordinate is
used in new arithmetic. Other metadata may be read only to authenticate
the fixed schema/domain/provenance and locate the declared inputs.

Require strict JSON without duplicate keys, decimals or nonfinite values;
canonical reduced rational strings; exact integers rather than booleans;
complete unique row keys and ideal lists; strictly positive probability
slots; exact row normalization; and the inherited H5 equal-top slot
identity. Missing, extra, duplicated or reordered required entries cannot
be silently repaired. Read-only provenance authentication does not count
as independent derivation of RI-88's held probabilities; their accepted
mathematical and execution evidence remains load-bearing.

## 3. Two different bounded polynomial reconstructions

For S in the four labeled C3 ideals, write A_r(S), B_r(S), G_r(S) for
the C3, C4 and H5 held probabilities. Set
a_r=A_r(7), b_r=B_r(7), g_r=G_r(7),
c_r=q_C4,r(15), h_r=q_H5,r(15)=q_H5,r(23), j_r=q_H5,r(31).
The held h_r is distinct from H_j and h7.

The closed-form reconstruction follows RI-89:

\[
 E_r=\sum_{S\in\{0,1,3,7\}}A_r(S)G_r(S)^3/B_r(S)^3
                  +3h_r^2/c_r+3j_r,
\]
\[
 K_r=\sum_{S\in\{0,1,3,7\}}A_r(S)^3G_r(S)^6/B_r(S)^8,
 \tag{3}
\]

\[
 U_r=4-4\rho E_r+6\rho^2j_r+4\rho^3h_r^3/c_r^2+\rho^4K_r,
 \tag{4}
\]

\[
 D_r=\rho^4(a_r^3g_r^6/b_r^8)(H_1^4-1)
       +4\rho^3(h_r^3/c_r^2)(H_2^3-1)
       +6\rho^2j_r(H_3^2-1).
 \tag{5}
\]

All coefficients are exact rationals; rho is a polynomial variable.
Products and differences must agree coefficientwise, not merely at a
selection of numerical rho values.

The independent reconstruction instead retains every individual proper
ideal of P_star and expands its maximal-deletion product. It does not
reuse the closed U/D formula as its purported independent answer:

| Precursor type | Individual slots per record | Raw deletion factors per slot |
|---|---:|---:|
| A C3 ideal S=0,1,3,7 | 4 | 15 |
| C3 plus one cap vertex | 4 | 7 |
| C3 plus two cap vertices | 6 | 3 |
| C3 plus three cap vertices | 4 | 1 |

This is 18 proper slots and 110 raw factors per record, or 36 slots and
220 raw factors over the two records. The full nineteenth ideal is a
complement, not an omitted proper slot. Its record ratio is precisely
the question being tested. There is no orbit division or merging of
same-child ideals.

Each factor retains the original parent/record/ideal, omitted-maximal
subset, sign, kept vertices, induced order/ideal and transported record.
Its source is either one of the authenticated held probabilities or the
formal six-parent expression prescribed by RI-89. Proper six-parent
factors are rho times their bounded deletion potential; the only
six-parent full factor is 1-rho E_r, occurring as a single-deletion
factor, never as a denominator. Positive lower constant denominators
and rho exponents are tracked exactly through cancellation.

The fixed six-parent P1=C3 ordinal-sum A3 has the four base-ideal slots,
three one-cap slots, three two-cap slots and its full complement. Its
proper potentials and row sum must be independently reconstructed from
the same held leaves before forming the full factor 1-rho E_r, and then
compared with the closed-form E_r. This lower reconstruction has ten
proper slots and 40 raw factors per record: 20 slots /80 factors in total,
separate from the seven-parent 36 slots /220 factors. These nested checks
add no accepted numerical inputs. Reusing the closed E_r inside both
routes would not check that coefficient independently. This is a symbolic
smaller-order identity, not numerical q6 evaluation or a new query.
Unique-top and twin-top invariance are the accepted RI-85 lemmas; the
retained stem record is not discarded.

Multiplying each seven-parent slot by its product of singleton-deletion
h7 values gives its modified polynomial. Summing all individual slots
independently recovers U,V,D, then A,C and both endpoint polynomials
below. Compare full exact coefficient vectors between constructions.
The domain remains these two records on this one parent; no order
catalogue or inherited prefix executor is needed.

## 4. Frozen outer domain and endpoint reduction

Define the exact rational bound

\[
 R=\frac1{2(1+\max(E_0,E_1))}>0.
 \tag{6}
\]

For each formal rho in (0,R], let

\[
 b_i(\rho)=\frac1{2(1+U_i(\rho))},\qquad
 b(\rho)=\min(b_0,b_1).
 \tag{7}
\]

The test domain is 0<rho<=R, 0<s<=b(rho). These are RI-89's proven
outer bounds, not definitions of the actual scales. On this domain
rho E_i<1/2. All held factors and proper symbolic factors are positive,
and each 1-rho E_i exceeds 1/2, so U_i>0 and both b_i are positive.
For every permitted s, 1-sU_i>1/2. The actual modified law additionally
obeys its complete strict-positivity premise; the outer domain need
not itself impose every modified-row constraint.

Let

\[
 G_i(\rho)=2(1+U_i(\rho))A(\rho)-C(\rho).
 \tag{8}
\]

At s=b_i, F=G_i/[2(1+U_i)]. Fix one orientation sigma in {+1,-1}.
If sigma A>=0 and **both** sigma G_i>0 throughout (0,R], then
sigma F>0 over the entire domain. Indeed choose a binding i with b=b_i
and write lambda=s/b in (0,1]. Since F is affine in s,

\[
 F(\rho,s)=(1-\lambda)A(\rho)
       +\lambda\frac{G_i(\rho)}{2(1+U_i(\rho))}.
 \tag{9}
\]

Weak positivity of A suffices because s=0 is excluded. Strict positivity
of the binding upper-endpoint term is essential because s=b is included.
The frozen test conservatively certifies **both** endpoint polynomials;
it does not switch to another criterion if that sufficient test fails.
The condition is sufficient, not necessary, for nonvanishing of F.

## 5. Fixed exact Bernstein certificate

A has degree at most four and C,G_i at most eight. Each is divisible by
rho^2. Verify that the constant and linear coefficients vanish exactly;
divide by this fixed factor without testing rho=0 or discarding any
other coefficient. No adaptive valuation or root search is used.

Use degree d=2 for A/rho^2 and d=6 for each G_i/rho^2. Pad missing high
coefficients with exact zeros. These degrees are selected in advance
from the analytic bounds, not increased in response to a failed test.
For Q(rho)=sum_(j=0)^d q_j rho^j, put x=rho/R and retain

\[
 \beta_k=\sum_{j=0}^k q_jR^j
                   \frac{\binom{k}{j}}{\binom{d}{j}},
 \qquad k=0,\ldots,d.
 \tag{10}
\]

Then Q(Rx)=sum_k beta_k binom(d,k)x^k(1-x)^(d-k). The checker must
independently expand these basis terms back into ordinary powers and
recover every R-scaled coefficient and the original rho polynomial.
Repeating the forward conversion or comparing a hash is not that check.

Nonnegative beta_k imply Q>=0 on [0,R]. If additionally beta_d>0, Q>0
for every rho in (0,R]: all Bernstein basis functions are positive in
the open interval, while the included x=1 endpoint retains only beta_d.
Zeros at rho=0 are harmless here. A zero final coefficient cannot
certify strictness at rho=R, even if all earlier coefficients are positive.

For a positive F certificate, require every A coefficient in this basis
to be nonnegative, and for each G_i require all coefficients nonnegative
and the final one strictly positive. A may be identically zero. Negative
F uses the same rules after reversing every sign. Record both tested
orientations in a deterministic order, positive first; do not clip
negative coefficients, use tolerances, adapt the degree, subdivide the
interval or move an endpoint. A failed Bernstein sign condition does
not demonstrate a polynomial sign change or a root.

## 6. Exact finite outcome branches

The mathematical report must distinguish these outcomes:

1. A positive or negative uniform certificate from sections 4–5. This
   rejects record-blindness at equal scales. Together with RI-89's
   necessary t=s restriction, it rejects every admissible common-level-
   scale continuation of this fixed seed relative to the fixed baseline.
2. A and C both identically zero, checked coefficientwise. Then F is
   identically zero and this pair is blind. This is not global acceptance.
3. No uniform certificate, but a verified root at the single predeclared
   outer rho boundary R. Report it as an **outer-boundary-root, unresolved
   for the actual selector**, never as the actual unknown scale pair.
4. Neither a uniform certificate nor the two preceding diagnostics:
   **unresolved by the fixed Bernstein test**. No root is thereby claimed.

For the boundary diagnostic only, evaluate the formal polynomials at
the already fixed interval endpoint R. If C(R)!=0, the only candidate
is s_R=A(R)/C(R); verify s_R>0, s_R<=b0(R), s_R<=b1(R), and exact
F(R,s_R)=0. If A(R)=C(R)=0, every permitted s is a root at R, so retain
the deterministic upper boundary s_R=min(b0(R),b1(R)) and check it.
If C(R)=0 but A(R)!=0 there is no root on that boundary. Do not divide
by zero or treat the excluded s=0 as an admissible root.

These are exact endpoint identities used to classify a polynomial
certificate. They are not a numerical choice of a6 or a7 for a growth
law, and do not evaluate a q6/q7 probability table. A root in the outer
domain may not obey global modified-law positivity or equal-maxima
constraints. It therefore cannot identify the actual law's scales.
There are no trial interior points, fitted scales or automatic additional
tests after this one fixed diagnostic.

More generally the exact formal root condition is s=A/C when C!=0;
A=C=0 permits every s, while C=0,A!=0 permits none. A prospective ratio
is a domain root only after all positive/domain constraints hold. The
report must preserve this distinction rather than label every symbolic
root locus as a demonstrated root.

No mathematical outcome authorizes another parent, marking, support,
numerical scale, global maximum, adaptive certificate search or new
probability table. An input refusal, code failure, timeout or resource
stop is not a mathematical outcome or permission to retry.

## 7. Refusals, fixtures and saved-certificate replay

The checker is a standard-library, exact-rational, data-only consumer.
All guards must remain active under Python optimization. The planned
refusals cover authenticated input identities, strict JSON and rational
encodings, exact integer/boolean distinctions, complete selected row and
ideal inventories, positivity/normalization, h7 ordering, transported
record provenance, deletion signs/multiplicities, independent polynomial
agreement, correct max-based R, fixed rho^2 factor and degree bounds,
Bernstein conversion and independent reconstruction, weak versus strict
endpoint rules, exact root-domain checks, and forged disposition or
partial saved-certificate fields.

Synthetic algebra-only fixtures exercise positive and negative uniform
certificates, weak A=0 with strict endpoint terms, an identically zero
pair, an included-boundary root and an inconclusive sign representation.
An endpoint-zero G must not pass strictness; an origin-only zero may.
Mixed Bernstein coefficients must not be converted into a root claim.
The fixtures are not DET laws and provide no native coefficient result.
Their implementation and review are not their execution.

Witness mode emits one deterministic complete JSON certificate to stdout;
it writes no certificate file. Default and optimized saved modes rebuild
the complete bounded result from the same authenticated inputs, require
strict full schema/type/domain agreement, and compare every certificate
field. Source identity and input bytes are checked before mathematical
work and remain pinned through the run. A new certificate cannot be
fabricated during preparation or substituted from an older obligation.

Retain all selected input values, both polynomial reconstructions,
individual-slot and factor provenance, exact outer-bound definition,
ordinary and Bernstein coefficients, reverse expansions, each decision
branch's evidence, declared negative-control names and explicit limits.
A final sign flag without this evidence is insufficient. Normal/-O replay
does not replace the separately required independent complete consumer
and coordinator adjudication after actual execution.

## 8. Concrete prospective execution custody

The external source preparation root is
`/Volumes/AI_DATA/development/det-review-evidence/ri91-qr-source-zstwQa`.
Its closure contains only the new checker and the exact accepted RI-88
certificate, in their relative directories. Scientific inputs are the
two original/copy file pairs; runtime/monitor identities are separate.
No producer, optimizer, prefix helper or broader scientific source tree
is imported into this execution closure.

The prospective supervisor adapts the previously reviewed RI-88 source
by changing only its evidence root, new target/directory/checker pin,
two-file dependency inventory and corresponding accepted pins, plus
descriptive header. All process handling, admission, output, signal,
identity, environment and resource rules remain unchanged. The historical
`ri84-...-v1` custody labels identify the retained protocol version, not
RI-91 scientific output. A coordinator must independently review this
complete adaptation and explicitly accept any qualification carry-forward;
neither old execution authorization nor old receipt is reused.

The fixed interpreter is `/opt/homebrew/bin/python3`, with isolated flags
`-I -S -B` and `-O` additionally for optimized replay. The exact child cwd
is the external root's `closure`. All child and monitor environments are
exactly PATH=/usr/bin:/bin, LANG=C, LC_ALL=C, TZ=UTC and
__CF_USER_TEXT_ENCODING=0x1F5:0x0:0x0. Preserve the explicit Darwin entry;
do not silently inherit or drop an environment variable.

The envelope remains 120 active-child seconds and 536,870,912 bytes of
sampled owned-process-group RSS, with 50-ms sample waits and a 250-ms
maximum monitor attempt, additionally bounded by the remaining wall time.
RSS sampling is not an allocator hard limit. The checker also retains
its internal alarm/resource guards through final serialization, flushed
output and its final check; actual nonzero exit invalidates a printed
success. No performance estimate is a measured result.

Before witness admission, both new `CERTIFICATE.json` paths must be absent.
The checker may not create either. Exact original/copy/runtime identities,
literal symlink chains, command, cwd, environment, limits and exclusive
attempt directory must be freshly frozen. A preparation freeze with null
authorization hash is intentionally inadmissible. Only the coordinator
can bind the exact payload to a fresh explicit authorization.

A genuine successful witness's unchanged stdout may later become the
candidate under a coordinator-owned saved-certificate addendum. Normal
and optimized replays each require separate frozen authorizations and
exclusive `normal-01` and `optimized-01` destinations. Preserve all raw
stdout/stderr, preparation/admission records, monitor samples, before/after
identities, receipt and actual supervisor exit. A receipt's success flag
without actual outer exit zero is not acceptance. Scientific progress
stderr is judged by content; monitor stderr has its own strict empty rule.

The final source/evidence manifest will bind concrete source bytes and
the preparation state. It grants no execution. Missing authorization,
identity drift, pre-existing attempt, incomplete evidence or resource
failure stops the attempt; no automatic retry, threshold change or
enlarged mathematical domain is authorized.

## 9. Concrete source inventory

The prepared `check.py` is 53,608 bytes /901 lines, SHA-256
`b0a40587be40afa6972664784ec1844f1463564ba93d5ba6cd2b21173986770e`.
This is a source identity, not an executed certificate. The scientific
schema is `ri91-relative-obstruction-v1`. Its fourteen top-level fields
are `schema`, `checker_sha256`, `design_sha256`, `design_bytes`,
`accepted_input`, `inputs`, `selected_parent`, `records`, `scale_domain`,
`cross_multiplication`, `decision`, `coverage`, `limitations` and
`refusal_controls`. Here `design_sha256`/`design_bytes` bind RI-89's
accepted proof, not this implementation note.

The five exact disposition strings are
`certified-positive-obstruction`, `certified-negative-obstruction`,
`identically-zero-pair`, `outer-boundary-root-unresolved` and
`unresolved-fixed-bernstein`. No disposition is preselected by this packet.
Saved replay reconstructs and compares all fields recursively, including
exact Python types, list lengths and every retained coefficient and raw
factor; a matching outcome alone cannot pass.

There are 83 declared intended-reason refusal controls, with a fixed
count/uniqueness guard. Ten separate algebra-only fixtures cover the
two orientations, weak A=0, identically zero F, the two outer-boundary
root cases and an everywhere-positive polynomial whose mixed Bernstein
coordinates leave this fixed test unresolved. They also check unequal
upper bounds (a candidate satisfying only the first bound is rejected),
an excluded s=0 boundary root and an origin-only zero that still permits
strict positivity on (0,R]. Controls retain strict
included-endpoint rejection, reverse-basis reconstruction, immutable
source/input provenance, lower-E reconstruction and labeled multiplicity.
Their complete ordered inventory lives in external `REFUSAL_INVENTORY.json`;
declared controls and fixtures have **not** been run during preparation.

Only nonexecuting AST parsing/compilation may supplement source review at
this stage. Such checks establish syntax, not fixture success, performance
or a scientific outcome. The external source-check and review records
bind the final source, note, adapted supervisor, exact copies and null-
authorization witness preparation. A fresh coordinator source/admission
decision remains required before execution.

## 10. Scope and status

The conditional laws retain complete marked equivariance, strict reads
only within proper precursors, full-complement access to all parent
records, fair marks and equality of the entire unnormalized D/4 in
incomparable-birth diamonds, including equal precursors. The new test
asks about record-independent relative weights, not validity of the
individual RI-38 continuations. Rejection is choice-class-specific,
not universal nonexistence of a record-blind continuation using other
component scales or a different law.

Even a successful first-layer record-independence test would not supply
all-size h, persistent width gain or geometric structure. The explicit
half-scale normalization at all later levels still has the accepted
RI-39 almost-sure height-density lower bound 1/2. This finite test does
not repair that rejected vanishing-height-density target.

No informative quantum growth coupling, physical observable test,
Lorentzian geometry, mass/gravity derivation, metric-as-record promotion,
or unique DET selection is claimed. Option B, Status M and RET's pause
remain unchanged. This is a source-only implementation packet; actual
coefficients, signs, roots, runtime and mathematical disposition remain
uncomputed pending independent review and coordinator admission.
