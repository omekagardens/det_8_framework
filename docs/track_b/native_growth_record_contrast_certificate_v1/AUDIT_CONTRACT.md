# RI105 — independent saved-arithmetic audit contract

25 September 2026. **Source/design preparation only.** This file specifies
a future independent consumer; it is not that consumer and does not permit
its implementation or execution. No producer, consumer, prefix, helper,
fixture, polynomial calculation or native coefficient is imported, compiled
or executed in preparing this contract. No scientific certificate operands
are read. No certificate, result, descriptor, active freeze, authorization
or successful receipt is created here. The repository is unchanged.

## 1. The exact question and accepted premises

The future consumer must independently reconstruct the complete saved
RI105 arithmetic for the fixed two-record contrast on

\[
 T_1=C_3\oplus A_4=(0,1,3,7,7,7,7),\qquad r\in\{0,1\}.
\]

Only bit zero changes. Every other inherited and maximal record bit is
zero in these two representatives. The accepted maximal-record invariance
and record/label transport justify these representatives; they do not
license replacing the question by arbitrary records or averages.

The only accepted scientific data body is the unchanged RI88 certificate:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| RI88 certificate | 1828149 | ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b |

The load-bearing source identities are:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| RI103 REPAIR.md | 20198 | 8a2a4bf9142341e2511763cbfd799183860e907372d577b9b32d8c1cf24a955c |
| RI94 AMPLITUDE.md | 25150 | 65645454993a81b70a0d9cd278eb137cd6b218055b1cb026f9950b7cb8895844 |
| RI105 check.py | 34820 | 6ff26aef5214ebcbdf13adc62dacdf33ba615769e2e64f3a39cf44368310655e |
| RI105 IMPLEMENTATION.md | 20203 | 7108bdc0d6b0f4dcc9da2acdbea647f1eddea71db1b11529eef780f2e52a8e04 |

These proof bytes, the pinned RI105 producer/protocol bytes, the final
consumer/contract bytes and their accepted source reviews must be concrete
later custody inputs. A mutable repository branch, publication title or
latest-file search cannot replace an admitted byte identity. RI95's prior
consumer and contract were read for source/custody patterns, not as native
arithmetic inputs or modules to execute.

The accepted strict baseline B, whole-map diamonds, complete marked rows,
individual-ideal multiplicities, RI38 potentials, RI94's nonzero
Delta-j premise and RI103's necessary record-constancy condition are
inherited premises. This audit neither reconstructs their earlier executors
nor proves DET entailment, a new physical law or an empirical discriminator.

## 2. Fixed data access and independent coefficient reconstruction

Authenticate the entire RI88 body before JSON parsing, then select exactly
the six complete held rows shown below. No H multiplier or z coordinate is
read into arithmetic or used as a decision premise. No RI91 or RI95
scientific certificate is an arithmetic input. Authenticating a complete
body is not a claim that every field in it was rederived.

| Parent | Complete ideal list | Records | Probability slots |
| --- | --- | --- | ---: |
| C3=(0,1,3) | 0,1,3,7 | 0,1 | 8 |
| C4=(0,1,3,7) | 0,1,3,7,15 | 0,1 | 10 |
| H5=(0,1,3,7,7) | 0,1,3,7,15,23,31 | 0,1 | 14 |

There are six rows and 32 individual probability slots. Each complete row
must be strictly positive and sum exactly to one. Exact selected row
identity, missing/duplicate rows or ideals, marking bounds, inherited
prefix/provenance identities and the record-local/twin equalities used by
the proof must be checked. A proper query restricts the record to its
precursor; a full query retains the whole row record. All type checks
precede lookup or memoization: booleans are not integers, and an unhashable
or out-of-domain object must produce the intended refusal, not an accidental
cache exception. No lookups at parents of size six or seven are allowed.

For r=0,1, independently reconstruct the held scalars

\[
 A_r(S)=q_B(C_3,r,S),\quad B_r(S)=q_B(C_4,r,S),\quad
 G_r(S)=q_B(H_5,r,S),\qquad S\in\{0,1,3,7\},
\]
\[
 c_r=q_B(C_4,r,15),\quad h_r=q_B(H_5,r,15)=q_B(H_5,r,23),
 \quad j_r=q_B(H_5,r,31),
\]
\[
 E_r=\sum_S A_r(S)G_r(S)^3/B_r(S)^3+3h_r^2/c_r+3j_r,
\]
\[
 v_r=h_r^3/c_r^2,\qquad
 K_r=\sum_S A_r(S)^3G_r(S)^6/B_r(S)^8.
 \tag{1}
\]

Every denominator is a proved positive held probability. The variable v_r
here is the starred held scalar of RI103, not a private full-child
correction. The record difference convention is always value at 1 minus
value at 0.

The consumer must use its own written exact arithmetic, not import the
producer, an inherited checker, a prefix helper, a solver or a supervision
module. Formula (1) is the inherited RI103 theorem route. Independently
rebuild each of its four E summands, the two other E totals, four K
summands, c/h/j/v, and their complete sums. Keep all four specified stem
ideals; a child-class representative or a backward-role count does not
replace one of these terms. The factors 3, 3, 6 and 4 in the accepted
formulas are exact labeled multiplicities, not free weights.

Independently form the padded coefficient vector

\[
 U_r(x)=4-4xE_r+6x^2j_r+4x^3v_r+x^4K_r.
 \tag{2}
\]

There is deliberately no new deletion-factor inventory, symbolic q6/q7
table or direct lower/upper-poset enumeration in this consumer. The
derivation of (1)-(2) remains an accepted source premise. Independent
reconstruction means that no saved RI105 coefficient, sum, sign or result
flag is used to compute another one. Reconstruct P directly from the four
differences in (3), and independently subtract the two padded U vectors
to check the exact x-division identity. A future source review must
identify the separately written arithmetic paths and their limits;
having reviewed the producer is not blind authorship, and using the same
formula alone is not proof of implementation independence.

The concrete independent implementation plan is normalized integer pairs
(numerator, positive denominator), with independently written integer-gcd
reduction and cross-canceling rational operations, and sparse univariate
coefficient maps of bounded degree. This differs from the producer's
Fraction-valued dense lists. Independently rebuild each Euclidean quotient
and remainder by sparse leading-term cancellation and verify it again by
coefficientwise multiplication plus remainder. Evaluate endpoints by the
direct sum of coefficient times endpoint powers, not the producer's Horner
loop. Convert these independent representations to the required ascending
canonical lists only for evidence comparison. This is a plan, not code
already supplied or tested; exact-type, bit and operation guards remain
mandatory on every independent path.

Set

\[
 P(x)=-4\Delta E+6x\Delta j+4x^2\Delta v+x^3\Delta K,
 \quad R=\frac1{2(1+\max(E_0,E_1))}.
 \tag{3}
\]

Check exactly that U_1-U_0=xP, R>0, and 1-R E_r>1/2 for both records.
The native degree is at most three, with coefficient P[1]=6 Delta-j
nonzero. A zero polynomial, vanishing required linear coefficient or
degree above three is a reconstruction/provenance failure, not an
alternative native scientific result. Degree-one and degree-two native
polynomials are allowed; a cubic leading coefficient is not presumed.
R is a rigorous outer-domain endpoint, never a selected actual scale.

## 3. Exact distinct-real-root certificate and endpoint theorem

The single authorized algebraic question is whether P has any real root
in (0,R]. No rational-root algorithm, root approximation, interval
subdivision, extra record, larger support, new parent or selected actual
rho is part of this test.

Compute the formal derivative and monic rational gcd

\[
 g=\gcd(P,P'),\qquad F=P/g.
\]

The consumer independently computes these, verifies exact quotient and
zero-remainder identities, and verifies gcd(F,F')=1. Monic normalization
is for gcds only. Preserve the original P scale in F=P/g; do not replace
F silently by its monic associate. Repeated roots of P are counted once
by F. Record actual degrees, derivative, gcd, quotient and square-free
verification; do not infer root multiplicity from signs alone.

Construct the exact Sturm sequence

\[
 S_0=F,\quad S_1=F',\quad
 S_{k+1}=-\operatorname{rem}(S_{k-1},S_k).
 \tag{4}
\]

Retain the exact rational negative remainders and stop before the first
zero remainder. No per-term monic rescaling or sign flipping is allowed.
Verify each division identity and strictly decreasing nonzero remainder
degree. The degree cap three bounds the nonzero chain by four members.
For a nonzero constant synthetic polynomial, use the one-member chain;
an identically zero polynomial is a domain refusal, never root-free.

Evaluate every chain member at 0 and R exactly. The sign is an exact
integer in {-1,0,1}. Delete zero signs, then count adjacent sign changes
to obtain V(0) and V(R). Rebuild all endpoint values, original sign lists,
zero-deleted lists and variations; do not trust a stored count.

For square-free F, at a root of F the derivative is nonzero. The variation
at that point after zero deletion equals its right-hand limiting value:
the first pair changes from opposite signs on the left to equal signs on
the right. At an intermediate Sturm member's zero, its neighboring values
have opposite signs, so deleting that zero preserves the variation.
Consequently

\[
 N_{(0,R]}=V(0)-V(R)
 \tag{5}
\]

excludes a root at zero and includes a root exactly at R. No infinitesimal
floating evaluation is needed. Check the resulting exact integer lies
between zero and deg(F). Multiplicities are handled by the square-free
reduction, not by counting repeated sign transitions.

There are exactly two successful native audit dispositions:

- `certified-record-contrast` if the distinct root count is zero;
  `restricted_27_child_repair_rejected` is true.
- `unresolved-real-roots-remain` if the count is positive;
  `restricted_27_child_repair_rejected` is false.

An input, arithmetic, resource, reconstruction or custody failure is not
either scientific disposition. In the first case, the actual positive
rho is somewhere in (0,R], so P(rho) is nonzero. With actual s>0,
f_1(1)-f_1(0)=-s*rho*P(rho) is nonzero, and the accepted RI103 condition
rejects only its specified 27-child positive repair at epsilon=1/4.
In the second case nothing identifies a root with actual rho. Even a
sole surviving irrational root remains unresolved in this packet:
rational-root exclusion is deliberately not performed. No sign of the
contrast or numerical actual full probability need be reported.

## 4. Complete saved body, schemas and refusal evidence

The producer and future consumer must share the pinned source's closed
result schema, not computation. Its top-level schema identifier is
`ri105-record-contrast-certificate-v1`; the sixteen sections are:

1. schema
2. accepted_inputs
3. accepted_sources
4. inputs
5. selected_parent
6. records
7. scale_domain
8. contrast
9. root_certificate
10. decision
11. coverage
12. limitations
13. arithmetic_limits
14. checker_sha256
15. fixtures
16. refusal_controls

Every nested key, exact type, array position and scalar is reconstructed
independently. Required evidence includes the fixed six-row/32-slot input
manifest, every summand and padded U vector, direct differences and
independent formal x division, the exact endpoint domain, every Sturm
identity and evaluation, complete synthetic evidence and the restricted
conclusion.
No output field is exempt because it looks like harmless metadata. Fields
declaring source identity, operations limits, scope and absence of actual
scales are checked against the frozen plan and source, not copied from the
candidate. Any later source/schema change requires fresh review before
admission; this prose does not authorize field additions by execution.

The nested reconstruction obligations are exact, not a selective audit:

- `accepted_inputs` contains only the fixed RI88 byte/hash pair;
  `accepted_sources` contains the RI103 and RI94 byte/hash pairs.
- `inputs` contains the six complete `held_rows`, ordered labels
  C3:0,C3:1,C4:0,C4:1,H5:0,H5:1, and false flags for prefix replay and
  H/z-value reads. `selected_parent` is exactly the seven masks above.
- `records` has exactly two entries ordered 0 then 1. Each contains
  `record`, four `E_terms`, `E_one_cap_total`, `E_two_cap_total`, `E`,
  `v_star`, four `K_terms`, `K`, `c`, `h`, `j`, and five `U_padded`
  coefficients. Numeric values use canonical rational strings.
- `scale_domain` fixes R, both selected E values, `0<rho<=R`, both exact
  lower-full margins at R, false actual-rho evaluation, amplitude `1/4`
  and the unchanged-seed flag.
- `contrast` fixes all four deltas, four padded P coefficients, five
  padded U1-minus-U0 coefficients, divisor `rho`, the independently
  verified quotient agreement, actual degree, nonzero-delta-j check and
  rationality-of-actual-rho flag explicitly inherited as a premise.
- `root_certificate` contains `polynomial`, `interval`, `R`, `derivative`,
  `gcd_euclidean`, `gcd_monic`, `square_free`, `square_free_quotient`,
  `square_free_remainder`, `reconstructed_polynomial`,
  `coprime_euclidean`, `coprime_gcd`, `sturm_chain`, `sturm_divisions`,
  `lower`, `upper`, `distinct_real_roots`, `lower_excluded`,
  `upper_included`, `rational_root_decision_performed` and
  `actual_scale_evaluated`. The last two are false.
- Each Euclidean division records exactly dividend, divisor, quotient
  and remainder. Each Sturm division adds the exact negative remainder
  as `next_term`, including its final zero stopping term. Every endpoint
  records x, all values, signs, zero-deleted signs and variation count.
  Polynomial coefficients are ascending, with trailing zeros removed;
  the zero polynomial is `[]`. Only the specifically named padded U/P
  vectors retain fixed lengths. Duplicate square-free/quotient fields
  are independently checked, not treated as optional redundancy.
- `decision` fixes disposition, distinct count, no-real-root flag,
  restricted-27-child rejection and rational-root-exclusion consequence.
  The latter is true only when no real roots exist; it is not a separate
  rational-root algorithm. Rational-roots-remaining, actual-scale-root,
  positive-repair, rejection-of-all-positive-extensions and actual-scale
  computation claims are all false.
- `coverage` fixes six held rows, 32 slots, two records, zero H/z
  arithmetic operands, zero new q6/q7 rows and native degree cap three.
  `limitations` explicitly retains real-versus-rational-root, actual-scale,
  all-size, physics and external-custody boundaries.
- `arithmetic_limits` records all fixed limits in section 6, not an
  invented actual operation count. `checker_sha256` is the separately
  admitted producer source identity, not the consumer's own identity.
- `fixtures` is the exact ordered sixteen-entry list in section 5, with
  each name, expected distinct count, complete root certificate, mechanical
  decision and false native-model flag. `refusal_controls` is the exact
  ordered list of name/reason pairs frozen by the source review.

Use canonical ASCII JSON: sorted object keys, compact separators, no
NaN/Infinity or floating literals, exact canonical rational strings, and
exactly one final newline. Reject duplicate keys, missing or extra fields,
noncanonical fractions, wrong exact types, boolean numeric aliases,
reordered role/record/factor/fixture arrays, padding inconsistent with the
declared polynomial representation, and semantically equivalent but
noncanonical bytes. Reconstruct and compare the entire object and entire
canonical byte body, then report per-section and whole-body identities.

The producer's ordered intended-reason refusal inventory must be frozen
in its reviewed source, checked for exact order/count/uniqueness, and
reconciled by the consumer as a declaration. The independent consumer
must not claim that it reexecuted those producer mutations. Their genuine
execution needs separately accepted producer witness and replay custody.
Independent reconstruction of algebra fixtures is a distinct claim.

The independent audit must reject violations of these invariants. This
list does not claim a separate executable producer mutation for every
item; the precise seventy controls are listed immediately below:

- input byte/source/proof/provenance mismatch; duplicate or missing held
  row/ideal; wrong selected record, order or transport; out-of-scope query;
- invalid rational/type/degree/budget; nonpositive or unnormalized held
  row; corrupted locality or twin equality; wrong labeled multiplicity;
- held summand or labeled multiplicity corruption; omitted E contribution;
  wrong record-difference orientation or failure of U1-U0=xP;
- native zero/constant/overdegree polynomial or lost nonzero linear
  coefficient; wrong radius or endpoint inclusion;
- nonmonic gcd, incorrect quotient or square-free status, omitted repeated
  root, positive instead of negative remainder, sign-changing normalization,
  reordered or prematurely stopped chain, wrong endpoint evaluation,
  zero-deletion variation or root count;
- forged scientific disposition or unrestricted repair/all-size claim;
  altered fixture, control metadata, source pin or canonical saved body;
- each numeric resource cap and malformed descriptor/custody admission.

Each refusal must fail for its specified reason under otherwise admissible
premises; a mutation that instead trips an earlier unrelated schema guard
does not demonstrate the intended algebra check. Later review must trace
all actual mutation paths. None is executed during this preparation.

The reviewed producer has this exact ordered inventory of 70 name/reason
pairs. The saved-evidence mutations intentionally test whole reconstructed
evidence comparison; they are not represented as independently mutated
internal algorithms. For example, `saved-negative-remainder` changes a
known nonempty next-term coefficient in synthetic fixture 7 and expects
`saved-exact-value`, not a fictional direct polynomial-division error.

| # | Name | Required reason |
| ---: | --- | --- |
| 1 | duplicate-json | duplicate-json-key |
| 2 | decimal-json | noninteger-json-number |
| 3 | nonfinite-json | noninteger-json-number |
| 4 | unreduced-rational | noncanonical-rational |
| 5 | boolean-rational | noncanonical-rational |
| 6 | rational-text-bound | rational-text-budget |
| 7 | integer-bit-bound | integer-bit-budget |
| 8 | boolean-polynomial | exact-rational-required |
| 9 | polynomial-degree | polynomial-shape-degree |
| 10 | root-degree | root-polynomial-domain |
| 11 | zero-polynomial | root-polynomial-domain |
| 12 | zero-radius | root-radius-domain |
| 13 | zero-polynomial-divisor | zero-polynomial-divisor |
| 14 | zero-rational-divisor | zero-rational-divisor |
| 15 | boolean-power | power-domain |
| 16 | wrong-size-ri88 | input-size-ri88 |
| 17 | wrong-hash-ri88 | input-hash-ri88 |
| 18 | wrong-size-ri103 | input-size-ri103 |
| 19 | wrong-hash-ri103 | input-hash-ri103 |
| 20 | wrong-size-ri94 | input-size-ri94 |
| 21 | wrong-hash-ri94 | input-hash-ri94 |
| 22 | extra-ri88-field | ri88-fields |
| 23 | missing-ri88-field | ri88-fields |
| 24 | wrong-ri88-source | ri88-source |
| 25 | wrong-dependencies | ri88-dependencies |
| 26 | wrong-admission | ri88-admission |
| 27 | wrong-prefix | ri88-actual-prefix |
| 28 | boolean-coverage | ri88-coverage |
| 29 | boolean-record | held-record-domain |
| 30 | extra-record | held-record-domain |
| 31 | boolean-order | held-order-types |
| 32 | boolean-slot | held-slot-types |
| 33 | missing-slot | held-slot-inventory |
| 34 | duplicate-slot | held-slot-inventory |
| 35 | nonpositive-slot | held-positive-normalized |
| 36 | reordered-rows | selected-row-order |
| 37 | missing-selected-row | selected-row-completeness |
| 38 | duplicate-selected-row | duplicate-selected-row |
| 39 | changed-locality | held-empty-locality |
| 40 | changed-twin | held-twin-symmetry |
| 41 | lookup-C5 | lookup-order-domain |
| 42 | lookup-q6 | lookup-order-domain |
| 43 | lookup-q7 | lookup-order-domain |
| 44 | lookup-record | lookup-record-domain |
| 45 | lookup-slot | lookup-slot-domain |
| 46 | zero-delta-j | accepted-delta-j-nonzero |
| 47 | changed-radius | fixed-radius |
| 48 | wrong-fixed-division | contrast-fixed-division |
| 49 | boolean-decision | decision-count-domain |
| 50 | extra-saved-field | saved-fields |
| 51 | missing-saved-field | saved-fields |
| 52 | saved-boolean-record | saved-exact-type |
| 53 | saved-missing-row | saved-list-coverage |
| 54 | saved-root-count | saved-exact-value |
| 55 | saved-endpoint-sign | saved-exact-value |
| 56 | saved-gcd | saved-exact-value |
| 57 | saved-quotient | saved-exact-value |
| 58 | saved-actual-scale-claim | saved-exact-value |
| 59 | saved-global-rejection | saved-exact-value |
| 60 | saved-positive-repair | saved-exact-value |
| 61 | saved-radius | saved-exact-value |
| 62 | saved-square-free-quotient | saved-exact-value |
| 63 | saved-reconstruction | saved-exact-value |
| 64 | saved-sturm-chain | saved-exact-value |
| 65 | saved-negative-remainder | saved-exact-value |
| 66 | saved-upper-inclusion | saved-exact-value |
| 67 | saved-lower-exclusion | saved-exact-value |
| 68 | saved-variations | saved-exact-value |
| 69 | saved-square-free-remainder | saved-list-coverage |
| 70 | saved-noncanonical | saved-canonical-bytes |

The locality and twin mutations transfer positive mass to the full slot
so their rows remain normalized; the specified equality is the intended
failure. Unknown numeric gcd constants are not guessed: the saved-gcd
mutation uses a guaranteed-different string. Numeric runtime guards are
not all force-triggered by this inventory. Future independent-consumer
parser, descriptor, identity and resource guards require their own source
review; this table must not be misreported as their executed qualification.

## 5. Fixed small synthetic algebra tests

Fixtures are exact artificial polynomials and positive rational radii,
not extra native rows or examples claimed to follow from DET. The ordered
inventory below is fixed, with coefficients listed in ascending powers.
Its expected counts follow by elementary factorization/sign arguments;
no native coefficient evaluation is involved in stating these tests.

| Name | Coefficients | R | Distinct roots in (0,R] |
| --- | --- | --- | ---: |
| constant-positive | [1] | 1 | 0 |
| constant-negative | [-1] | 1 | 0 |
| lower-zero-excluded | [0,1] | 1 | 0 |
| upper-zero-included | [-1,1] | 1 | 1 |
| outside-root | [-2,1] | 1 | 0 |
| double-upper-root | [1,-2,1] | 1 | 1 |
| both-endpoints | [0,-1,1] | 1 | 1 |
| common-zero-endpoint-trap | [-2,5,-4,1] | 1 | 1 |
| triple-upper-root | [-1,3,-3,1] | 1 | 1 |
| three-admissible-roots | [-2/9,11/9,-2,1] | 1 | 3 |
| irrational-positive-root | [-1,-1,1] | 2 | 1 |
| negative-leading | [1,-1] | 1 | 1 |
| no-real-root | [1,0,1] | 1 | 0 |
| all-negative-roots | [6,11,6,1] | 1 | 0 |
| double-interior-root | [1/4,-1,1] | 1 | 1 |
| nonunit-radius | [-1/3,1] | 1/2 | 1 |

The common-zero trap is (x-1)^2(x-2); applying endpoint variations to
the unsquared-free polynomial would be unsafe. The three-root case has
roots 1/3, 2/3 and 1. The irrational-root case must remain unresolved:
the fixture does not trigger a rational-root follow-up. Constant cases
exercise the generic algebra routine but are excluded from the native
branch by its nonzero linear coefficient. Zero polynomials are explicit
refusals, not successful fixtures.

Rebuild all sixteen complete root certificates and mechanical decision
objects, not just expected counts. Each fixture explicitly records
`native_model_claimed=false`: a root-free fixture's mechanically tested
decision fields are not a rejection of any native repair. Repeated roots
are counted once. An altered sign, multiplicity, endpoint or fixture
disposition must not be accepted because its final count happens to match.

## 6. Exact arithmetic, operation accounting and resources

The frozen arithmetic limits are 32768 bits for each accepted rational
input numerator/denominator, 1048576 bits for each internal reduced rational
numerator/denominator, 2097154 bits for transient rational-operation
integers, 200000 wrapped exact-arithmetic operations, 20000 characters per
input rational or JSON integer token, and 8388608 output bytes. Input size/type/digit checks must precede expensive
conversion, and arithmetic guards must cover coefficient construction,
derivatives, division, gcds, square-free and Sturm checks, evaluations,
synthetic evidence and final serialization. No silent truncation,
approximation, modular guess or relaxed limit is permitted.

Wrapped operations are a declared implementation accounting unit, not a
claim to count processor instructions or internal integer-gcd operations.
The later source must define exactly what is counted and protect against
an unchecked helper path. Actual operation counts and runtime success
cannot be inferred from source review. Resource exhaustion preserves a
failure and cannot be reported as a root, no-root or unresolved-root result.

The future consumer uses only the Python standard library and its own
written arithmetic. It must not call an external solver or copy/import the
producer's computed output as its arithmetic. Keep any internal alarm
through canonical output serialization, flush and the last budget check.
No file is written by the consumer; a separately admitted caller captures
stdout/stderr and resource evidence.

The later exact caller must enforce the established 120-second wall
envelope and 536870912-byte sampled owned-process RSS envelope, with 50-ms
waits and monitor calls bounded by min(250ms, remaining deadline). This is
a sampled envelope, not an allocator hard limit or uninterrupted census.
The internal consumer also checks elapsed time/RSS and its bounded
arithmetic counters. No resource-success estimate is made here.

Freeze the interpreter and its literal symlink chain, `/bin/ps`, cwd,
exact argv, source/data/custody bytes and this exact five-entry environment:
`PATH=/usr/bin:/bin`, `LANG=C`, `LC_ALL=C`, `TZ=UTC`,
`__CF_USER_TEXT_ENCODING=0x1F5:0x0:0x0`. The proposed interpreter command
uses `/opt/homebrew/bin/python3 -I -S -B`; an optimized variant, if wanted,
is a separate admission, not an automatic retry. No command is launched
by this contract.

## 7. Concrete future descriptor and custody boundary

The future consumer accepts only DESCRIPTOR, canonical positive decimal
BYTES and lowercase SHA256 after its script name. No probability, parent,
record, radius, actual scale, polynomial, fixture or output-file override
exists. Authenticate the descriptor before parsing. It has exactly
`schema`, `phase`, `files`, `accepted_sources`, `audit_source`, and
`custody_dependencies`.

The prospective schema is `ri105-independent-audit-input-v1`, with phase
`fixed_saved_certificate_audit`. `accepted_sources` has exactly the roles
`ri103`, `ri94`, `checker`, `protocol`, and `contract`. Each source entry
has exactly `path`, `bytes`, and `sha256`: an absolute literal symlink-free
regular-file path, a positive JSON integer byte count (never a boolean),
and a lowercase 64-character hexadecimal SHA-256. The first four byte/hash
pairs are fixed in section 1. The `contract` entry binds the final reviewed
bytes of this document, supplied by the later coordinator descriptor and
independently fixed by its caller/source acceptance. Its hash is not
embedded in this document itself.

`audit_source` is one object with exactly the same `path`, `bytes`, and
`sha256` fields and exact types. It binds the final reviewed consumer and
its path must equal the actual executing consumer's absolute, symlink-free
source path. Its own complete bytes are checked before and after the audit.
No current byte/hash placeholder substitutes for that later source identity;
this contract does not invent an unimplemented consumer's pin.

`files` has exactly `ri88`, `ri103`, `ri94` and `candidate`. Each entry has exactly `path`,
`bytes`, `sha256`, with the same exact path/count/hash types as source
entries. The RI88 pin is fixed
in section 1, as are both proof-source pins. The candidate pin is the later
genuine producer witness, not a current placeholder. Both proofs are
authenticated as raw bytes before any scientific JSON parsing and are
not parsed for numeric operands.

`custody_dependencies` is an exact ordered five-entry list:

1. producer_witness_stdout
2. producer_witness_custody
3. producer_normal_custody
4. producer_optimized_custody
5. consumer_source_review

Each entry has exactly `role`, `path`, `bytes`, `sha256`, with the same
path/count/hash types as source entries and the exact ordered role string.
The `ri103` and `ri94` objects in `accepted_sources` must respectively equal
the corresponding objects in `files`, including their literal paths. These
are two deliberate cross-field references, not extra copies. All other
payload paths must be pairwise distinct and distinct from the descriptor:
there are fifteen role bindings but exactly thirteen unique payload paths.
Capture each unique file once, authenticate every associated role binding,
and repeat the unique-file reads and role checks after reconstruction.
Every source, scientific and custody path has a concrete admitted identity.
Candidate and genuine stdout
must have equal pins and equal complete bytes. No prospective receipt,
null pin or merely named source review can satisfy this descriptor.

The future caller/coordinator must separately authenticate and interpret
the actual custody records and genuine outer completions, including exact
argv/environment, admitted source closure, original/copy bindings,
before/after identities, monitoring/cleanup, actual outer and child exits,
complete output identities and independently accepted source review.
The arithmetic consumer pins those evidence bodies but does not declare
their semantics accepted merely because they hash. Runtime role order is
not interchangeable with receipt role-set semantics; the exact later
adapter must be reviewed against genuine schema and role counts.

No own authorization or own successful output is included as a prerequisite
inside the descriptor. The separately issued external freeze/authorization
binds the concrete descriptor, caller and reviewed source. This avoids
circular self-authorization. Source preparation, publication or accepted
predecessor qualification does not itself authorize a new execution.

Before any scientific JSON is parsed, capture and authenticate all
scientific, proof/source and custody bytes. Require lstat/open/fstat
device/inode/size/mtime/ctime consistency, reject symlink substitutions,
and check complete byte identities. After reconstruction independently
reread every item, descriptor and own source, retaining all checks even
when another postcheck fails. The caller additionally pins runtime symlink
chains and preserves source/input identities on failure. No accepted
source, certificate or historical failed attempt may be overwritten.

## 8. Remaining gates and scope of a future report

This contract has been reconciled by source reading with the 740-line
producer pinned in section 1 and the complete adjacent IMPLEMENTATION.md
protocol, including its sixteen fields, sixteen fixtures and seventy
ordered name/reason pairs. This is a reviewer-authored preparation record,
not coordinator acceptance of this contract or execution qualification.
The coordinator still binds the final protocol and this contract by actual
byte identity in its source adjudication. A future consumer must be authored,
fully read and independently accepted at exact source/contract pins; this
file is not a substitute for that review.

Before any consumer execution the coordinator must separately accept the
genuine producer witness and its unchanged saved normal/optimized replays,
issue a concrete descriptor, review the precise external caller and its
qualified carry-forward or new qualification boundaries, create a fresh
ordered freeze, and issue explicit authorization for one attempt. Genuine
outer completion, raw monitoring, before/after and output custody must then
be independently reconciled before mathematical adjudication. A success
line or receipt by itself is insufficient.

The future consumer report must distinguish: independently reconstructed
native arithmetic; independently rebuilt synthetic algebra; producer
refusals checked only as saved declarations; accepted mathematical
premises; and custody identities pinned but not self-adjudicated. Report
the full input/source/descriptor/output identities and every reconstructed
section identity, exact root certificate and one permitted disposition.

No target or arithmetic execution has occurred in preparing this file.
Its present result is a verification contract, not a record contrast.
Failures remain preserved and do not trigger retries, new roots/records,
rational-root follow-up, all-stem gcd, larger tables or a changed scale.
Even a future root-free result would reject only the specified RI103
27-child family, not every positive h8, every native continuation or QM.
No all-size geometry, mass/gravity, RET or programme-completion claim
follows; Option B and Status M remain unchanged.
