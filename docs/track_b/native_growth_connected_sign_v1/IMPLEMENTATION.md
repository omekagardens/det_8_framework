# RI128 — bounded connected strict-sign decision (source only)

No source in this packet has been imported, compiled, parsed as an AST, probed
or run. No fabricated case or numerical scientific operand has been evaluated.
This specification and the two proposed targets require complete fresh review,
changed-target qualification and separate owner execution admission.

## Mathematical decision and containing domain

RI127 accepted all connected cancellation/transport identities and reduces
the two local intervals to C2>0 and C3>0. Its positive-denominator identities
give C2=P2/q and C3=P3/((1-rho)v). We retain both cleared targets exactly.
See INPUT_FORMULAS.md for every individual held term; no rank work is repeated.

The original containing domain is 0<rho<=R,0<s<1/2, with
R=1/[2(1+max(E0,E1))]. ANALYTIC_BOUNDS.md proves the additional universal
normalization bounds rho<=1/4,s<=1/4. The ONLY domain used by these sources is
0<rho<=X,0<s<=Y with X=min(R,1/4),Y=1/4. No configurable lower bound, favorable
point, domain search or actual scale is supplied. The proof of containment,
as well as this source, must be accepted before execution.

Write each P=a(x)+y*b(x) with ascending exact coefficients. At y=0 and y=Y
form h=a and h=a+Y*b. For h=c0+...+cn*x^n on the CLOSED enclosure [0,X],

    L=c0+sum_{i>=1,ci<0} ci X^i,
    U=c0+sum_{i>=1,ci>0} ci X^i.

These rigorous bounds include all endpoints. The nonempty actual domain is
contained in that enclosure, and affine interpolation covers every y.
If BOTH endpoint upper bounds are <=0, report UNIFORM_NONPOSITIVE. Otherwise,
if BOTH lower bounds are >0, report UNIFORM_STRICT_POSITIVE. Otherwise report
UNRESOLVED. This is sufficient, not complete: x on (0,X] may be strictly
positive but its enclosure lower bound is zero and is deliberately unresolved.
The identically zero polynomial is uniformly nonpositive, never strictly
positive. Degree drops and zero coefficients are retained in padded arrays.

Either nonpositive target rejects this fixed H30. Both strictly positive
targets certify only these two local intervals. Otherwise no actual-local
decision follows. One shared T1 correction, all remaining connected parents,
all five Di and their strict bounds remain untouched. No all-size or physical
claim follows. B, seed, amplitude 1/4, all30children/16parents stay fixed.

## Fixed inputs, authentication and bounded extraction

Future targets expect exactly five scientific/premise roles in sibling inputs/:
ri88.json, ri88_root.json, ri122_root.json, ri124_root.json, ri127_root.json. Literal whole-byte
length/hash pins in both sources bind the unchanged accepted files. All five
must authenticate before scientific JSON parsing. The RI122/124/127 status
guards and the explicit RI88 root seed acceptance retain complete record-pattern acceptance, conditional full H30 closure
and the accepted strict-sign reduction. These five files alone are not a
replacement for the historical owner custody/dependency closure.

Only C3,C4,C5,H5 records0,1 are converted to rational operands: exactly eight
complete rows/44 individually named ideal slots. All forty held-row keys are
checked for exact order/record inventory, without converting other probability
strings. Selected rows are strictly positive and normalized. The complete
prior forty-row pattern proof remains an indispensable accepted premise.

Only exact_decision.z[1] and z[2] become seed operands. Their positions are
authenticated against structure.ordered_support for all11 canonical classes,
the fixed RI88 source/prefix/dependency identities, its accepted disposition
and amplitude. Both are bounded by [-1,1]. No nullspace, H or z is recomputed;
other seed coordinates and all numerical elimination evidence stay unused.
Empty-slot equality and both H5 cap slots, the twin diamond and the C3 full
equality are checked on the selected rows; none substitutes for full transport.

No inputs, active descriptor, certificate, caller, freeze or admission are
created by this source-preparation packet. Targets have no file-writing code.

## Exact certificate schema

Schema ri128-connected-strict-sign-v1, canonical ASCII JSON with sorted keys,
compact separators and one newline. Exact top-level fields:

schema, checker_sha256, input_identities, held_rows, seed, profiles, scalars,
domain, targets, decision, fixtures, refusal_controls, limits, limitations.

All arithmetic scalars are canonical rational strings; all indices/counts
are exact JSON integers (never booleans). All padding includes zero strings.

- input_identities: each of the five roles maps to {bytes,sha256}.
- held_rows: original eight complete entries in C3,C4,C5,H5 order, records0,1.
- seed: {z2,z3,source_indices:[1,2],reconstructed:false}.
- profiles: records0,1; each {record,E_terms,c,h,j,m,E,V,E2_terms,C2_terms,
  A2,B2,C2,r2,r3}. E_terms has4, E2_terms8, C2_terms5 individual entries.
- scalars: {epsilon2,epsilon3,D2,D3,v,q_padded,U20_padded,U30_padded}, with
  lengths3,4,3 for the arrays; D2,D3,v are strictly positive.
- domain: {R,X,Y,original:"0<rho<=R;0<s<1/2",
  certified:"0<rho<=min(R,1/4);0<s<=1/4",actual_scales_evaluated:false,
  containment_basis:"RI127 outer bound; RI128 unique-maximum normalization"}.
- targets: list j2,j3, each {label,degree_cap,a_padded,b_padded,degree_a,
  degree_b,endpoints,status}. Caps5,3; all coefficient arrays length cap+1.
  Zero-polynomial degree is -1. endpoints is y=0 then y=Y, each
  {y,coefficients_padded,degree,power_terms,lower,upper}; power_terms lists
  all ci*X^i for i=1..cap including zeros. Degrees ignore trailing zeros.
- decision: {disposition,nonpositive_targets,strict_positive_targets,
  fixed_H30_rejected,two_local_intervals_certified,full_H30_feasibility:false,
  actual_scales_selected:false}; disposition is REJECT_FIXED_H30 if either
  target nonpositive, else LOCAL_INTERVALS_ONLY if both positive, else
  UNRESOLVED. The two booleans follow precisely these branches.
- fixtures: literal cases from QUALIFICATION.md, each {name,a,b,X,Y,cap,
  expected_status,evidence}; evidence is the same target object with label
  equal to fixture name. These are fabricated algebra, not native-law data.
- refusal_controls: ordered {name,first_reason} pairs from QUALIFICATION.md;
  producer executes and requires the exact first refusal before returning.
  Auditor independently reconstructs these declarations and validates saved
  evidence; it does not pretend that reproducing declarations runs producer
  controls or qualifies the new target.
- limits and limitations are literal in both sources and described below.

## Framing, saved reconstruction and resource contract

check.py uses bounded Fraction arithmetic and factored dense-polynomial
assembly. --witness emits the certificate; no flag reconstructs it anew and
compares sibling CERTIFICATE.json by recursive exact-type/value equality AND
whole canonical bytes. Self-hash output is not independent authentication:
the outer owner must bind the executing source to its admitted identity.

audit_saved.py independently expresses integer-pair arithmetic, explicit
coefficient formulas and direct power bounds. It imports neither producer nor
any scientific helper, independently parses authenticated original inputs,
reconstructs every certificate section and requires exact equality/bytes.
Its producer identity is a literal source pin set only after producer seal.
Auditor self-identity must likewise be independently admitted by the owner.
Saved bytes and all sources/inputs are protected and rechecked before success;
the outer owner must also perform failure-path custody checks.

Future reviewed invocations must use isolated/no-site/no-bytecode mode
(-I -S -B, optionally -O); these are requirements, not active commands.

Bounds: 120 seconds active child; externally sampled owned-group 512MiB;
8MiB per scientific body/input/output, bounded aggregate pinned inputs;
32768 input rational bits, 1048576 working bits, 2097154 transient bits,
200000 counted rational operations/comparisons, 20000 input and emitted rational-text characters.
No retry or limit relaxation. Local alarm/self-RSS checks supplement, never
replace, an admitted native outer wall/group-RSS monitor. Canonical parsing
rejects duplicate keys, floats/NaN, boolean integers and unreduced rationals.
Only pinned historical root metadata may contain decimal resource observations:
these are preserved as tagged text lexemes, never floating or scientific operands.
This exception is not enabled for RI88 science, certificates or output;
every denominator is checked before division; all guards survive -O.

Inherited framing is a source reference only. Changed seed extraction,
degree5/3 targets, domain proof, coefficient envelopes, decisions and auditor
all require fresh complete qualification. Nothing in RI120/RI122 qualification
automatically qualifies this target. RET alone remains paused; measurement
implementation remains separate. Source-stable handoff ends this assignment.
