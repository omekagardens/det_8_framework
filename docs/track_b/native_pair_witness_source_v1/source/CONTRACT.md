# RI191 exact pair witness: source and acceptance contract

30 September 2026. Source-only proposal for independent review. The checker
has not been imported, compiled, AST-parsed, probed or run. No scientific
JSON or selected coefficient has been decoded or evaluated. The actual
pair gap remains unresolved.

## 1. Exact question and three outcome classes

RI189 identifies the original component roots

    k0=(2254,7,0),       k1=(2254,7,1),
    epsilon=alpha(k0)-alpha(k1)>0,
    epsilon_star=44*1147*3875/(41*126280*508644).

The inherited theorem is that epsilon>=epsilon_star strictly excludes
the capacity branch v>B6. Equality at the threshold is sufficient.
The simpler bound epsilon>=1/10000 also suffices, but is stronger than
necessary for this certificate. Neither is a claim about the actual
coefficients until a properly admitted witness supplies their values.

The source [pair_witness.py](pair_witness.py) is intended to distinguish:

| Class | Mathematical meaning | Consequence |
| --- | --- | --- |
| Sufficient separation | epsilon>=epsilon_star after complete binding and validation | The RI189 conditional theorem yields v<B6 strictly |
| Inconclusive smaller positive gap | 0<epsilon<epsilon_star after complete binding and validation | This sufficient route does not decide the contrast ratio or capacity branch |
| Refusal | Malformed input, wrong identity/domain/ordering, unstable read, or conflict with the inherited positive-gap premise | No mathematical acceptance from this checker |

A positive gap between epsilon_star and1/10000 is sufficient even though
the simpler comparison is false. Zero or negative epsilon is an inherited
sign conflict, not an ordinary inconclusive small positive gap. A failed
bound does not prove the opposite ratio; a successful rejection of the
formal endpoint condition does not locate actual W(rho,s), since rho<Z6.
No conclusion about H30, the other parents, full QM or physical geometry
follows.

## 2. Original prescription, not an arbitrary feasible vector

The original RI41 input is identified by whole bytes, not by a caller's
claim to have constructed a feasible law:

    /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/CERTIFICATE.json
    bytes: 2845
    SHA256: 3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969

The current narrow RI191 opaque-prefix admission permits only whole-file
identity observations of that exact path. Main authenticated that authority
and observed these opaque bytes. It does not permit JSON decoding,
selected-table instantiation or execution. It is not a magnitude witness.
No current scientific result is inferred from a matching hash.

The production wrapper binds the unchanged original input and immutable
source/premise records before interpreting the certificate. There is no
CLI option to replace the path, expected hash, threshold or target keys.
The original RI41 `load_certificate` semantics are retained:

1. The declared domain is the original size-four `interior_a` prefix,
   original maximal-deletion potential and original sorted component order.
2. The complete declared list has109 roots, with typed integer triples,
   valid masks, uniqueness and strict lexicographic ordering.
3. Locate k0 and k1 in that complete list. Their exact ordinal indices
   are not inferred from their adjacency or hard-coded from a guess.
4. For each selected index use its override when present, otherwise the
   declared default. Validate the default even if both selected entries
   are overridden, and validate every override key/value, including those
   not used in the final pair calculation.

The original accepted graph reconstruction establishes that the original
declared109-root list is the complete original component list. Merely
checking that an arbitrary list has109 sorted triples would not prove
this. The new checker inherits that finite theorem and authenticates the
unchanged original bytes; it does not reconstruct the graph or accept a
replacement list or a replacement feasible vector.

The immutable source inputs include the original RI41 checker and
normalization manuscript, RI63's unchanged-prefix completion manuscript,
the accepted RI189 routing/coupled proofs and root review/decision, and
the RI191 assignment. They bind the interpretation and mathematical scope.
Their exact identities are recorded in the source and provenance manifest.
Source/interpreter custody for the new executable and complete new packet
is separately root-owned; a program cannot bootstrap trust in its own
possibly changed source through a self-reported hash.

## 3. Exact rational validation and arithmetic

Input coefficient strings use a bounded positive ASCII decimal integer or
numerator/denominator grammar. Leading zeros and unreduced terms may be
accepted; signs, embedded whitespace, decimal/exponential notation and
zero numerators or denominators are not. Output rationals are reduced
canonically. This grammar is an explicit subset of the old general
`Fraction` parser's language. Its compatibility with the still-undecoded
original input is unverified. An eventual grammar refusal would be a
validator-envelope issue to review, not evidence that the native law fails.

The declared original fields are required. Bounded inert extra metadata
may be retained because the old loader ignores it and whole-file identity
binds it; unknown fields are not allowed to override any required meaning.
Duplicate JSON keys and nonfinite numbers are refused. Booleans must not
pass integer checks through Python's bool/int subtype relation. All root
triples and override indices are checked, not only the two selected roots.

After validation, let the selected exact rationals be n0/d0 and n1/d1,
with positive denominators. The difference is calculated without floats.
For the simpler threshold its sufficient comparison is exactly

    10000*(n0*d1-n1*d0)>=d0*d1.

For epsilon_star, positive denominator clearing gives the corresponding
exact rational comparison. Thresholds are fixed mathematical constants;
no tolerance, rounding, optimization, graph search or coefficient fitting
enters the decision. The source reports both threshold comparisons without
making the simpler one a prerequisite for the exact sufficient outcome.

Soundness is conditional on the input binding, faithful original selector,
accepted RI189 theorem and correctness of the reviewed implementation.
It is not established merely by the provenance checker hashing the source.

## 4. Binding boundary and unbound argument controls

The pure argument-validation boundary is for later synthetic controls.
It must report unbound-argument status and cannot grant fixed-prefix
acceptance to caller-supplied bytes. The production wrapper authenticates
all fixed inputs before decoding, then independently rechecks all of them
after an ordinary result or refusal. An earlier read failure must not
short-circuit independent later postchecks. Primary and secondary failures
are retained without overwriting the original refusal reason. If the bounded
diagnostic cannot hold all secondary details, an explicit omitted count
replaces that list; this is not a claim of complete diagnostic capture.

The actual source boundaries are `evaluate_payload(raw: bytes)` and
`verify_fixed()`. The first emits `binding=UNBOUND_ARGUMENT_ONLY`, an
empty inputs object and an explicitly unbound declared-root-list basis.
Only the production wrapper, after all nine authentications, sets
`binding=FIXED_ORIGINAL_PREFIX_BYTES`, the nine identities and the inherited
pinned-root-list basis. Neither string alone replaces external source and
execution custody. Hard `BaseException` termination is not caught and
relabeled as a completed ordinary postcheck tail.

The no-argument CLI emits a twelve-field result object on stdout with
status `SUFFICIENT` or `INCONCLUSIVE_SMALLER_GAP`; both are valid outcomes
and return zero. `INVALID` diagnostics go to stderr and return two.
`INHERITED_SIGN_CONFLICT` is a refusal reason, never a successful smaller-gap
status. Failed writes/flushes can leave partial output or prevent diagnostic
capture; the external owner must reject incomplete or inconsistent streams,
not consume a partial success prefix.

No output should claim success after a changed/missing input or a failed
required postcheck. Whole-path, ancestor, descriptor and post-read checks
must be distinguished from historical stat observations: old admission
state is provenance, not a requirement that current metadata equal an old
timestamp or inode forever. A changed scientific byte stream never reaches
schema/threshold acceptance in the production binding path.

The result is not a saved-report validator. Source-level tests for malformed
saved results would need a separate actual consuming boundary before they
could earn any coverage credit. Negative specifications in
[NEGATIVE_CASES.md](NEGATIVE_CASES.md) describe future controls; no fixtures,
test harnesses or generated sample coefficient tables are created here.

## 5. Bounded-input and resource design

The checker is standalone standard-library source. Its fixed finite input
set, exact original certificate byte count, maximum file/JSON/string/token/
integer sizes and complete root/override counts bound the work admitted to
the parser and exact arithmetic. The code's actual constants and stages
are the controlling source specification; they are reviewed literally,
not tested or imported in this sitting.

| Source limit | Declared bound |
| --- | ---: |
| Certificate argument / other fixed file | 65,536 / 262,144 bytes |
| JSON depth / lexical tokens / containers | 8 / 4,096 / 512 |
| Items per object or array / raw string characters | 128 / 256 |
| Digits per rational term / JSON integer | 64 / 10 |
| Roots / legal override indices | 109 / 0 through108 |
| Fixed input paths / path length / path components | 9 / 4,096 characters / 64 |
| Result / diagnostic serialization | 16,384 / 8,192 bytes |
| Shared cooperative fixed-input read budget | 20 seconds |

The lexical budget runs before JSON container allocation. Actual parsing
then enforces duplicate-key, integer and float/nonfinite rules, and every
decoded container receives an item-count check. Coefficient parsing is
bounded before integer conversion. A root's precursor mask is proper
(0 through14); its record mask must be a subset. These syntactic bounds
do not substitute for the inherited complete-root-list theorem.

All nine fixed inputs must authenticate before the original certificate
is decoded. Every ordinary result or exception then attempts all nine
postchecks, independently recording failures. A deadline exceeded at an
early postcheck does not imply the later checks succeeded: each later
attempt is made and its own refusal retained. Descriptor-close failures
are secondary errors when an earlier failure already exists.

File access must reject nonregular files and symlink substitutions, enforce
bounded complete reads, and retain read-window stability independently of
historical metadata. Resource checks are cooperative source guards. They
cannot establish an operating-system hard memory/CPU/wall limit or rule
out a blocking syscall. External root-owned execution supervision and a
qualified interpreter/standard-library environment remain prerequisites.

No import graph, interpreter identity, maximum RSS, timing, read-race
behavior, JSON grammar compatibility, return code or output byte count has
been observed by executing this new source. Proposed limits are not
measured limits, and source review does not qualify a runtime.

## 6. Remaining admission and protected-validation obligations

This packet contributes source and manual review only. The following
boundaries are still distinct and separately owned by root:

| Boundary | What still needs an authorized accepted record | Credit from this sitting |
| --- | --- | --- |
| Independent source acceptance | Review the complete checker, contract, negative specifications and exact sealed dependencies | Author-peer review only; root acceptance pending |
| Executable and environment custody | Bind the admitted source, interpreter, import surface, launch configuration and resource supervision | None |
| Scientific-input admission | Explicitly allow decoding this original certificate and validating its complete declared table, with only the two routed values used by this mathematical test | None; current admission is opaque identity only |
| Execution and protected validation | Run only after separate admission, preserve actual outputs/failures/postchecks, and independently validate the claimed result | None |
| Existing qualification/control inventories | Preserve all92 controls,34 recipes and35 mutation families, with their actual identities, coverage and unresolved failures | None waived, replaced or credited |
| Original native prerequisites | Preserve31 focused attempts,139 policy cases,20 native and42 audit deeper obligations | None waived, replaced or credited |
| Mathematical conclusion | Obtain a bound, semantically valid actual output and apply only the accepted conditional theorem | Actual pair magnitude unresolved |

The original31 cases retain23 F01 and8 F02; the139 retain77 native and62
audit. These totals do not supply individual control identities or prove
coverage. The separate selected governance and root-owned qualification
records continue to control those identities and admissions; this packet
does not expand their operational closure or invent replacement members.
The new prose cases are not additions silently counted as executed tests.

Even independent source acceptance would not waive any listed execution
or validation requirement. A qualified run reporting an inconclusive
positive gap would be a legitimate mathematical outcome, not permission
to relabel the pair bound as passed. A refused input or premise conflict
must return to review rather than yield a native conclusion.

## 7. Scientific and ownership limits

Keep the original fixed-law coefficients, theta/M5, all canonical q/N
products, minima, positive parts, complete marked rows, P2/P3,Y=1/4,
shared T1,other eight parents,five Di and all labeled occurrences. The
original 109-vector is not tuned. No actual W/C2/C3/H30 sign, full QM,
geometry, mass/gravity, empirical or ontological promotion is supplied.
RET remains paused; measurement and qualification remain separate.

Only this reserved external source packet is authored. There is no
repository/index/Git or predecessor mutation, new agent/thread, scientific
decoding/evaluation, engine, subject/checker import/compile/AST/probe/run,
fixture, runtime/profile/card or admission artifact from this author.
The one extra original certificate is selected under the explicit opaque
admission only; no other new historical mathematical source is opened.
Root owns independent acceptance, all subsequent admission, publication
and successor selection. Stop at the sealed source handoff.
