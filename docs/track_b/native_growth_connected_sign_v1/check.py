#!/usr/bin/env python3
"""RI128 source-only proposal. No execution/qualification claimed.
Fraction/guard framing adapted by textual inspection of RI120 check.py.
New degree5/3 target, two accepted seed coordinates, domain and decisions.
Standard-library imports only; never import a scientific predecessor.
"""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import re
import resource
import signal
import sys
import time

SCHEMA = "ri128-connected-strict-sign-v1"
PINS = {
    "ri88": (1828149, "ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b"),
    "ri88_root": (2783, "15cedc2d7683734450963dc147e2a0deef59f0713a6b9898d806d9dd1240bea6"),
    "ri122_root": (15477, "162949e859b16211106e3c0213a29db290d52ffc7bf7fdaf411d20387a2fdbbc"),
    "ri124_root": (3645, "85b6d5c84139b05d5a18f89614a415ecde962efc429092b914e6f2da33ccde9c"),
    "ri127_root": (4071, "66d274815c101015256ba506f3e6a125375797b1b7946831159d39692ffebd77"),
}
ROOT_STATUSES = {
    "ri88_root": ("ri88-root-finite-result-adjudication-v1", "accepted_positive_finite_width_bias"),
    "ri122_root": ("ri122-root-final-native-mathematical-adjudication-v1",
                   "ACCEPT_FIXED_28_CHILD_POSITIVE_REPAIR_OBSTRUCTION"),
    "ri124_root": ("ri124-root-final-proof-adjudication-v1",
                   "ACCEPT_CONDITIONAL_ANALYTIC_THEOREM_AND_COMPLETE_CLOSURE_ONLY"),
    "ri127_root": ("ri127-root-final-proof-adjudication-v1",
                   "ACCEPT_COMPLETE_CONNECTED_CANCELLATION_AND_CONDITIONAL_STRICT_LOCAL_REDUCTION"),
}
LIMITS = dict(seconds=120, group_rss_bytes=536870912, scientific_bytes=8388608,
              input_bits=32768, working_bits=1048576, transient_bits=2097154,
              operations=200000, rational_text=20000)
LIMITATIONS = dict(conditional_on_accepted_record_pattern=True,
                  coefficient_bounds_are_sufficient_not_complete=True,
                  domain_is_containing_not_actual_scales=True,
                  two_local_intervals_not_full_H30=True,
                  outer_custody_and_fresh_qualification_required=True,
                  physical_or_all_size_claim=False)
C3, C4, C5, H5 = (0, 1, 3), (0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 7)
SHAPES = (C3, C4, C5, H5)
MASKS = ((0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 15, 31),
         (0, 1, 3, 7, 15, 23, 31))
CAPS = ((0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 0, 3), (0, 0, 1, 1),
        (0, 0, 1, 2), (0, 0, 1, 3), (0, 0, 1, 5), (0, 0, 3, 3),
        (0, 1, 1, 1), (0, 1, 1, 3), (0, 1, 3, 3))
WIDTHS = (4, 3, 3, 3, 2, 2, 2, 2, 3, 2, 2)
RI88_KEYS = set("admission checker_sha256 compact_rows coverage dependencies design_sha256 domain exact_decision expanded_rows held_rows parameters prefix refusal_controls schema structure transported_audit width_target".split())
DEPENDENCIES = {
    "ri41_certificate": "3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969",
    "ri63_certificate": "f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b",
    "ri63_checker": "39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b",
    "ri74_checker": "edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c",
}
START, OPS = None, 0


class Refusal(RuntimeError):
    pass


def need(condition, reason):
    if not condition:
        raise Refusal(reason)


def budget():
    need(START is None or time.monotonic()-START <= 120, "wall-budget")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    need((rss if sys.platform == "darwin" else rss*1024) <= 536870912, "rss-budget")


def bounded(a, bits=1048576):
    need(type(a) is Q, "rational-type")
    need(max(abs(a.numerator).bit_length(), a.denominator.bit_length()) <= bits, "rational-bits")
    return a


def op(kind, a, b=Q(0)):
    global OPS
    OPS += 1
    need(OPS <= 200000, "operation-budget")
    budget()
    bounded(a)
    bounded(b)
    if kind == "cmp":
        return (a > b)-(a < b)
    if kind == "+":
        c = a+b
    elif kind == "-":
        c = a-b
    elif kind == "*":
        c = a*b
    elif kind == "/":
        need(b != 0, "zero-divisor")
        c = a/b
    else:
        raise Refusal("arithmetic-operation")
    return bounded(c)


def add(a, b): return op("+", a, b)
def sub(a, b): return op("-", a, b)
def mul(a, b): return op("*", a, b)
def div(a, b): return op("/", a, b)
def sign(a): return op("cmp", a)


def power(a, n):
    need(type(n) is int and 0 <= n <= 5, "power-domain")
    result = Q(1)
    for _ in range(n):
        result = mul(result, a)
    return result


def total(xs):
    s = Q(0)
    for x in xs:
        s = add(s, x)
    return s


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)+"\n").encode("ascii")


def decode(raw, historical_metadata=False):
    need(type(raw) is bytes and len(raw) <= 8388608, "json-byte-budget")
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, "duplicate-key")
            out[k] = v
        return out
    def bad(_):
        raise Refusal("noninteger-json")
    def integer(s):
        need(len(s) <= 20000, "integer-text-budget")
        return int(s)
    def decimal(s):
        need(historical_metadata and len(s) <= 20000, "noninteger-json")
        # Historical resource observations are opaque lexemes, never operands.
        return ("historical-decimal-lexeme", s)
    return json.loads(raw, object_pairs_hook=pairs, parse_int=integer,
                      parse_float=decimal, parse_constant=bad)


def rat(text):
    need(type(text) is str, "rational-text-type")
    need(len(text) <= 20000, "rational-text-budget")
    need(re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", text) is not None, "rational-canonical")
    q = Q(text)
    need(str(q) == text, "rational-canonical")
    return bounded(q, 32768)


def qtext(q):
    bounded(q)
    text = str(q)
    need(len(text) <= 20000, "rational-output-text-budget")
    return text


def pin(role, raw):
    need(role in PINS and type(raw) is bytes, "input-role")
    need(len(raw) == PINS[role][0], "input-size-"+role)
    need(sha256(raw).hexdigest() == PINS[role][1], "input-hash-"+role)


def root_status(role, data):
    schema, status = ROOT_STATUSES[role]
    need(type(data) is dict and data.get("schema") == schema and data.get("status") == status,
         "root-status-"+role)


def provenance(d):
    need(type(d) is dict and set(d) == RI88_KEYS, "ri88-fields")
    need(d["schema"] == "ri88-four-vertex-cap-v1"
         and d["checker_sha256"] == "93eb721e933d90ba922b62f8a6844b64529d2acee1ae3bb3e15c81c4de153568"
         and d["design_sha256"] == "e0dd0b046d80564ddc4e6ffef78853156f5c418b327917f1d5fadc4e229ab58a",
         "ri88-source")
    need(type(d["dependencies"]) is dict and d["dependencies"] == DEPENDENCIES, "ri88-dependencies")
    a, p, c = d["admission"], d["prefix"], d["coverage"]
    need(type(a) is dict and a.get("epsilon") == "1/4"
         and a.get("later_h_prescribed") is False and a.get("numerical_a6_evaluated") is False, "ri88-amplitude")
    need(type(p) is dict and p.get("problem_sha256") == "dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c"
         and p.get("actual_probability_manifest_sha256") == "7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378"
         and type(p.get("canonical_lex_stages")) is int and p["canonical_lex_stages"] == 69, "ri88-prefix")
    need(type(c) is dict and type(c.get("held_marked_rows")) is int and c["held_marked_rows"] == 40
         and type(c.get("held_probability_slots")) is int and c["held_probability_slots"] == 224, "ri88-coverage")


def seed(d):
    structure, decision = d.get("structure"), d.get("exact_decision")
    need(type(structure) is dict and type(decision) is dict
         and decision.get("disposition") == "positive-finite-width-bias", "seed-disposition")
    expected = [dict(index=i, cap=list(cap), order=list(C3)+[7+8*p for p in cap], width=WIDTHS[i])
                for i, cap in enumerate(CAPS)]
    need(type(structure.get("ordered_support")) is list
         and encoded(structure["ordered_support"]) == encoded(expected), "seed-support")
    z = decision.get("z")
    need(type(z) is list and len(z) == 11 and all(type(x) is str for x in z), "seed-vector")
    out = [rat(z[i]) for i in (1, 2)]
    need(all(sign(sub(Q(1), q)) >= 0 and sign(add(Q(1), q)) >= 0 for q in out), "seed-bound")
    return out


def row(entry, shape, record):
    need(type(entry) is dict and set(entry) == {"order", "record", "probabilities"}, "row-fields")
    need(type(entry["order"]) is list and all(type(x) is int for x in entry["order"])
         and tuple(entry["order"]) == shape, "row-order")
    need(type(entry["record"]) is int and entry["record"] == record, "row-record")
    pairs = entry["probabilities"]
    need(type(pairs) is list and all(type(p) is list and len(p) == 2 and type(p[0]) is int for p in pairs),
         "slot-types")
    need([p[0] for p in pairs] == list(MASKS[SHAPES.index(shape)]), "slot-inventory")
    qs = {m: rat(t) for m, t in pairs}
    need(all(sign(q) > 0 for q in qs.values()), "row-positive")
    need(total(qs.values()) == 1, "row-normalized")
    return qs


def extract(d):
    provenance(d)
    entries = d["held_rows"]
    need(type(entries) is list and len(entries) == 40, "held-inventory")
    expected = [(s, r) for s in SHAPES for r in range(16 if s == C5 else 8)]
    rows, originals = {}, []
    for e, (s, r) in zip(entries, expected):
        need(type(e) is dict and set(e) == {"order", "record", "probabilities"}
             and type(e["order"]) is list and all(type(x) is int for x in e["order"])
             and tuple(e["order"]) == s and type(e["record"]) is int and e["record"] == r, "held-key-order")
        if r in (0, 1):
            rows[s, r] = row(e, s, r)
            originals.append(e)
    for s in SHAPES:
        need(rows[s, 0][0] == rows[s, 1][0], "empty-locality")
    need(rows[C3, 0][7] == rows[C3, 1][7], "three-chain-full")
    for r in (0, 1):
        b, g, d5 = rows[C4, r], rows[H5, r], rows[C5, r]
        need(g[15] == g[23], "twin-slots")
        need(mul(b[7], g[15]) == mul(b[15], d5[7]), "twin-diamond")
    return rows, originals


def profile(rows, record):
    A, B, D, G = [rows[s, record] for s in SHAPES]
    c, h, j, e, ell = B[15], G[15], G[31], D[15], D[31]
    m = div(power(h, 2), c)
    et = [div(mul(A[k], power(G[k], 3)), power(B[k], 3)) for k in MASKS[0]]
    E = total(et+[mul(Q(3), m), mul(Q(3), j)])
    V = sub(sub(E, m), mul(Q(2), j))
    e2t = [div(mul(D[k], G[k]), B[k]) for k in MASKS[0]]+[div(mul(e, h), c), h, j, ell]
    c2t = [div(mul(mul(A[k], power(G[k], 3)), D[k]), power(B[k], 4)) for k in MASKS[0]]
    c2t.append(div(mul(e, power(h, 2)), power(c, 2)))
    a2 = sub(add(E, mul(Q(2), total(e2t))), j)
    b2, c2 = total([mul(Q(2), m), mul(Q(2), j), ell]), total(c2t)
    r3 = et[3]
    r2 = c2t[3]
    vals = dict(c=c, h=h, j=j, m=m, E=E, V=V, A2=a2, B2=b2, C2=c2, r2=r2, r3=r3)
    evidence = dict(record=record, E_terms=list(map(qtext, et)), E2_terms=list(map(qtext, e2t)),
                    C2_terms=list(map(qtext, c2t)), **{k: qtext(v) for k, v in vals.items()})
    return vals, evidence


def polynomial(p, cap):
    need(type(cap) is int and 0 <= cap <= 5 and type(p) is list and len(p) <= cap+1, "polynomial-degree")
    for c in p:
        bounded(c)
    return p+[Q(0)]*(cap+1-len(p))


def plus(a, b):
    n = max(len(a), len(b))
    return [add(a[i] if i < len(a) else Q(0), b[i] if i < len(b) else Q(0)) for i in range(n)]


def scale(p, q):
    return [mul(c, q) for c in p]


def shift(p, k):
    need(type(k) is int and k >= 0 and len(p)+k <= 6, "polynomial-degree")
    return [Q(0)]*k+p


def degree(p):
    return next((i for i in range(len(p)-1, -1, -1) if p[i] != 0), -1)


def bound(p, x, cap, y):
    padded = polynomial(p, cap)
    terms = [mul(padded[i], power(x, i)) for i in range(1, cap+1)]
    lower = total([padded[0]]+[t for t in terms if sign(t) < 0])
    upper = total([padded[0]]+[t for t in terms if sign(t) > 0])
    return dict(y=qtext(y), coefficients_padded=list(map(qtext, padded)), degree=degree(padded),
                power_terms=list(map(qtext, terms)), lower=qtext(lower), upper=qtext(upper)), lower, upper


def target(label, a, b, x, y, cap):
    need(type(x) is Q and type(y) is Q and sign(x) > 0 and sign(y) > 0, "box-positive")
    a, b = polynomial(a, cap), polynomial(b, cap)
    lo = bound(a, x, cap, Q(0))
    hi = bound(plus(a, scale(b, y)), x, cap, y)
    if sign(lo[2]) <= 0 and sign(hi[2]) <= 0:
        status = "UNIFORM_NONPOSITIVE"
    elif sign(lo[1]) > 0 and sign(hi[1]) > 0:
        status = "UNIFORM_STRICT_POSITIVE"
    else:
        status = "UNRESOLVED"
    return dict(label=label, degree_cap=cap, a_padded=list(map(qtext, a)), b_padded=list(map(qtext, b)),
                degree_a=degree(a), degree_b=degree(b), endpoints=[lo[0], hi[0]], status=status)


FIXTURES = (
    ("positive-constant", ("1",), (), "1", "1/4", 0, "UNIFORM_STRICT_POSITIVE"),
    ("negative-constant", ("-1",), (), "1", "1/4", 0, "UNIFORM_NONPOSITIVE"),
    ("identically-zero", (), (), "1", "1/4", 3, "UNIFORM_NONPOSITIVE"),
    ("excluded-lower-zero-conservative", ("0", "1"), (), "1", "1/4", 1, "UNRESOLVED"),
    ("included-upper-zero", ("-1", "1"), (), "1", "1/4", 1, "UNIFORM_NONPOSITIVE"),
    ("mixed-sign-domain", ("-1", "2"), (), "1", "1/4", 1, "UNRESOLVED"),
    ("affine-endpoint-zero", ("-1",), ("4",), "1", "1/4", 0, "UNIFORM_NONPOSITIVE"),
    ("affine-endpoint-crossing", ("-1",), ("8",), "1", "1/4", 0, "UNRESOLVED"),
    ("affine-positive", ("1",), ("4",), "1", "1/4", 0, "UNIFORM_STRICT_POSITIVE"),
    ("affine-lower-zero-conservative", ("0",), ("4",), "1", "1/4", 0, "UNRESOLVED"),
    ("degree-drop-zero-padding", ("-1", "0", "0", "0", "0", "0"), (), "1", "1/4", 5, "UNIFORM_NONPOSITIVE"),
    ("quintic-upper-zero", ("-1", "0", "0", "0", "0", "1"), (), "1", "1/4", 5, "UNIFORM_NONPOSITIVE"),
    ("cubic-upper-zero", ("-1", "0", "0", "1"), (), "1", "1/4", 3, "UNIFORM_NONPOSITIVE"),
    ("negative-square-conservative", ("-1", "2", "-1"), (), "1", "1/4", 2, "UNRESOLVED"),
    ("nonunit-domain", ("-1", "2"), (), "1/4", "1/4", 1, "UNIFORM_NONPOSITIVE"),
)


def fixtures():
    out = []
    for name, a, b, x, y, cap, status in FIXTURES:
        e = target(name, list(map(rat, a)), list(map(rat, b)), rat(x), rat(y), cap)
        need(e["status"] == status, "fixture-"+name)
        out.append(dict(name=name, a=list(a), b=list(b), X=x, Y=y, cap=cap, expected_status=status, evidence=e))
    return out


def decide(targets):
    need(type(targets) is list and [t["label"] for t in targets] == ["j2", "j3"], "decision-targets")
    negative = [t["label"] for t in targets if t["status"] == "UNIFORM_NONPOSITIVE"]
    positive = [t["label"] for t in targets if t["status"] == "UNIFORM_STRICT_POSITIVE"]
    need(all(t["status"] in ("UNIFORM_NONPOSITIVE", "UNIFORM_STRICT_POSITIVE", "UNRESOLVED") for t in targets), "decision-status")
    disposition = "REJECT_FIXED_H30" if negative else "LOCAL_INTERVALS_ONLY" if len(positive) == 2 else "UNRESOLVED"
    return dict(disposition=disposition, nonpositive_targets=negative, strict_positive_targets=positive,
                fixed_H30_rejected=bool(negative), two_local_intervals_certified=len(positive) == 2,
                full_H30_feasibility=False, actual_scales_selected=False)


def strict(saved, expected):
    need(type(saved) is type(expected), "saved-type")
    if type(expected) is dict:
        need(set(saved) == set(expected), "saved-fields")
        for key in expected:
            strict(saved[key], expected[key])
    elif type(expected) is list:
        need(len(saved) == len(expected), "saved-length")
        for x, y in zip(saved, expected):
            strict(x, y)
    else:
        need(saved == expected, "saved-value")


def saved_check(raw, expected):
    strict(decode(raw), expected)
    need(raw == encoded(expected), "saved-bytes")


def build(data, source_hash):
    rows, originals = extract(data)
    z2, z3 = seed(data)
    v0, ev0 = profile(rows, 0)
    v1, ev1 = profile(rows, 1)
    D2, D3, v = sub(v0["r2"], v1["r2"]), sub(v0["r3"], v1["r3"]), sub(v1["V"], v0["V"])
    need(all(sign(t) > 0 for t in (D2, D3, v)), "native-positive-pivots")
    q = [sub(v1["A2"], v0["A2"]), sub(v0["B2"], v1["B2"]), sub(v0["C2"], v1["C2"])]
    need(sign(q[0]) > 0, "native-q-zero-positive")
    U2, U3 = [Q(3), sub(Q(0), v0["A2"]), v0["B2"], v0["C2"]], [Q(2), sub(Q(-1), v0["V"]), v0["V"]]
    A, B, D, G = [rows[s, 0][0] for s in SHAPES]
    eps3 = div(mul(A, power(G, 3)), power(B, 3))
    eps2 = div(mul(mul(A, power(G, 3)), D), power(B, 4))
    h2, h3 = add(eps2, v0["r2"]), add(eps3, v0["r3"])
    R = div(Q(1), mul(Q(2), add(Q(1), v0["E"] if op("cmp", v0["E"], v1["E"]) >= 0 else v1["E"])))
    need(sign(R) > 0 and op("cmp", R, Q(1, 2)) < 0, "native-radius")
    x, y = (R if op("cmp", R, Q(1, 4)) <= 0 else Q(1, 4)), Q(1, 4)
    a2 = plus(scale(q, z2), shift([mul(Q(4), D2)], 2))
    b2 = scale(plus(shift(scale(q, h2), 3), scale(shift(U2, 2), sub(Q(0), D2))), Q(4))
    den3 = [v, sub(Q(0), v)]
    a3 = plus(scale(den3, z3), [Q(0), mul(Q(4), D3)])
    b3 = scale(plus(shift(scale(den3, h3), 2), scale(shift(U3, 1), sub(Q(0), D3))), Q(4))
    ts = [target("j2", a2, b2, x, y, 5), target("j3", a3, b3, x, y, 3)]
    return dict(schema=SCHEMA, checker_sha256=source_hash,
                input_identities={k: dict(bytes=n, sha256=h) for k, (n, h) in PINS.items()},
                held_rows=originals, seed=dict(z2=qtext(z2), z3=qtext(z3), source_indices=[1, 2], reconstructed=False),
                profiles=[ev0, ev1], scalars=dict(epsilon2=qtext(eps2), epsilon3=qtext(eps3),
                D2=qtext(D2), D3=qtext(D3), v=qtext(v), q_padded=list(map(qtext, q)),
                U20_padded=list(map(qtext, U2)), U30_padded=list(map(qtext, U3))),
                domain=dict(R=qtext(R), X=qtext(x), Y=qtext(y), original="0<rho<=R;0<s<1/2",
                certified="0<rho<=min(R,1/4);0<s<=1/4", actual_scales_evaluated=False,
                containment_basis="RI127 outer bound; RI128 unique-maximum normalization"),
                targets=ts, decision=decide(ts), fixtures=fixtures(), refusal_controls=[],
                limits=LIMITS, limitations=LIMITATIONS)


BASE_CONTROLS = (
    ("duplicate-json", "duplicate-key"), ("float-json", "noninteger-json"), ("nan-json", "noninteger-json"),
    ("rational-boolean", "rational-text-type"), ("rational-unreduced", "rational-canonical"),
    ("rational-text-over", "rational-text-budget"), ("rational-bits-over", "rational-bits"),
    ("division-zero", "zero-divisor"), ("power-boolean", "power-domain"),
    ("degree-six", "polynomial-degree"), ("boolean-coefficient", "rational-type"),
    ("zero-radius", "box-positive"), ("zero-y", "box-positive"),
    ("row-extra", "row-fields"), ("row-order-boolean", "row-order"), ("row-record-boolean", "row-record"),
    ("slot-boolean", "slot-types"), ("slot-missing", "slot-inventory"), ("slot-reordered", "slot-inventory"),
    ("row-zero", "row-positive"), ("row-sum", "row-normalized"),
    ("seed-support-boolean", "seed-support"), ("seed-short", "seed-vector"), ("seed-large", "seed-bound"),
    ("saved-type", "saved-type"), ("saved-fields", "saved-fields"), ("saved-value", "saved-value"),
    ("saved-noncanonical", "saved-bytes"), ("decision-missing", "decision-targets"),
    ("decision-invalid", "decision-status"),
    ("strict-zero-promotion", "saved-value"),
    ("slot-extra", "slot-inventory"),
    ("rational-output-over", "rational-output-text-budget"),
)
SAVED_PATHS = (
    ("saved-q", ("scalars", "q_padded", 0), "changed"),
    ("saved-domain", ("domain", "X"), "changed"),
    ("saved-domain-shrunk", ("domain", "Y"), "1/8"),
    ("saved-target-a", ("targets", 0, "a_padded", 0), "changed"),
    ("saved-target-b", ("targets", 1, "b_padded", 0), "changed"),
    ("saved-degree", ("targets", 0, "degree_a"), -99),
    ("saved-upper", ("targets", 0, "endpoints", 0, "upper"), "changed"),
    ("saved-lower", ("targets", 1, "endpoints", 1, "lower"), "changed"),
    ("saved-status", ("targets", 0, "status"), "INVALID"),
    ("saved-overclaim", ("decision", "full_H30_feasibility"), True),
)
SECTION_KEYS = ("schema", "checker_sha256", "input_identities", "held_rows", "seed", "profiles",
                "scalars", "domain", "targets", "decision", "fixtures", "refusal_controls", "limits", "limitations")
CONTROL_PAIRS = (BASE_CONTROLS
                 + tuple((kind+"-"+role, "input-"+kind+"-"+role) for role in PINS for kind in ("size", "hash"))
                 + tuple(("status-"+role, "root-status-"+role) for role in ROOT_STATUSES)
                 + tuple(("section-"+key, "saved-type") for key in SECTION_KEYS)
                 + tuple((name, "saved-value") for name, _, _ in SAVED_PATHS))


def changed(obj, path, value):
    copy = decode(encoded(obj))
    t = copy
    for key in path[:-1]:
        t = t[key]
    t[path[-1]] = value
    return copy


def controls(raws, witness):
    # Fabricated complete C3 row; direct-boundary controls are not native evidence.
    e = dict(order=list(C3), record=0, probabilities=[[i, "1/4"] for i in MASKS[0]])
    sd = dict(structure=dict(ordered_support=[dict(index=i, cap=list(c), order=list(C3)+[7+8*p for p in c], width=WIDTHS[i]) for i, c in enumerate(CAPS)]),
              exact_decision=dict(disposition="positive-finite-width-bias", z=["0"]*11))
    small = {"a": 1}
    actions = [
        lambda: decode(b'{"a":1,"a":2}'), lambda: decode(b'1.1'), lambda: decode(b'NaN'),
        lambda: rat(True), lambda: rat("2/4"), lambda: rat("1"*20001),
        lambda: bounded(Q(1 << 32768), 32768), lambda: div(Q(1), Q(0)), lambda: power(Q(1), True),
        lambda: polynomial([Q(0)]*7, 5), lambda: polynomial([True], 0),
        lambda: target("x", [], [], Q(0), Q(1), 0), lambda: target("x", [], [], Q(1), Q(0), 0),
        lambda: row(dict(e, extra=0), C3, 0),
        lambda: row(changed(e, ("order", 0), False), C3, 0),
        lambda: row(changed(e, ("record",), False), C3, 0),
        lambda: row(changed(e, ("probabilities", 0, 0), False), C3, 0),
        lambda: row(dict(e, probabilities=e["probabilities"][:-1]), C3, 0),
        lambda: row(dict(e, probabilities=e["probabilities"][::-1]), C3, 0),
        lambda: row(changed(e, ("probabilities", 0, 1), "0"), C3, 0),
        lambda: row(changed(e, ("probabilities", 0, 1), "1/8"), C3, 0),
        lambda: seed(changed(sd, ("structure", "ordered_support", 0, "index"), False)),
        lambda: seed(changed(sd, ("exact_decision", "z"), ["0"])),
        lambda: seed(changed(sd, ("exact_decision", "z", 1), "2")),
        lambda: saved_check(b'{"a":true}\n', small), lambda: saved_check(b'{}\n', small),
        lambda: saved_check(b'{"a":2}\n', small), lambda: saved_check(b'{ "a":1 }\n', small),
        lambda: decide([]), lambda: decide([dict(label="j2", status="INVALID"), dict(label="j3", status="UNRESOLVED")]),
        lambda: saved_check(encoded(dict(witness["fixtures"][2]["evidence"], status="UNIFORM_STRICT_POSITIVE")),
                            witness["fixtures"][2]["evidence"]),
        lambda: row(dict(e, probabilities=e["probabilities"]+[[15, "1/4"]]), C3, 0),
        lambda: qtext(Q(1 << 70000)),
    ]
    for role in PINS:
        raw = raws[role]
        actions.extend([lambda r=role, b=raw: pin(r, b+b" "),
                        lambda r=role, b=raw: pin(r, bytes([b[0] ^ 1])+b[1:])])
    for role in ROOT_STATUSES:
        actions.append(lambda r=role: root_status(r, {}))
    for key in SECTION_KEYS:
        actions.append(lambda k=key: saved_check(encoded(dict(witness, **{k: None})), witness))
    for _, path, replacement in SAVED_PATHS:
        actions.append(lambda p=path, v=replacement: saved_check(encoded(changed(witness, p, v)), witness))
    need(len(actions) == len(CONTROL_PAIRS), "control-inventory")
    out = []
    for (name, reason), action in zip(CONTROL_PAIRS, actions):
        try:
            action()
        except Refusal as exc:
            need(str(exc) == reason, "control-first-reason-"+name)
        else:
            raise Refusal("control-no-refusal-"+name)
        out.append(dict(name=name, first_reason=reason))
    # Qualification semantics explicitly exercise each complete decision branch.
    for statuses, disposition in ((("UNIFORM_NONPOSITIVE", "UNRESOLVED"), "REJECT_FIXED_H30"),
                                  (("UNRESOLVED", "UNIFORM_NONPOSITIVE"), "REJECT_FIXED_H30"),
                                  (("UNIFORM_STRICT_POSITIVE", "UNIFORM_STRICT_POSITIVE"), "LOCAL_INTERVALS_ONLY"),
                                  (("UNIFORM_STRICT_POSITIVE", "UNRESOLVED"), "UNRESOLVED")):
        ds = decide([dict(label=k, status=s) for k, s in zip(("j2", "j3"), statuses)])
        need(ds["disposition"] == disposition and ds["full_H30_feasibility"] is False, "decision-fixture")
    return out


def read(path, cap=8388608):
    need(path.stat().st_size <= cap, "file-byte-budget")
    with path.open("rb") as stream:
        raw = stream.read(cap+1)
    need(len(raw) <= cap, "file-byte-budget")
    return raw


def main():
    global START
    need(sys.argv[1:] in ([], ["--witness"]), "invocation")
    START = time.monotonic()
    def alarm(_n, _f):
        raise Refusal("wall-budget")
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(120)
    sys.set_int_max_str_digits(2097154)
    source = Path(__file__).resolve()
    protected = {source: read(source)}
    paths = {role: source.parent/"inputs"/(role+".json") for role in PINS}
    raws = {role: read(path, PINS[role][0]) for role, path in paths.items()}
    for role in PINS:
        pin(role, raws[role])
        protected[paths[role]] = raws[role]
    for role in ROOT_STATUSES:
        root_status(role, decode(raws[role], historical_metadata=True))
    data = decode(raws["ri88"])  # Every original pin/status precedes science parsing.
    witness = build(data, sha256(protected[source]).hexdigest())
    witness["refusal_controls"] = [dict(name=n, first_reason=r) for n, r in CONTROL_PAIRS]
    need(controls(raws, witness) == witness["refusal_controls"], "control-results")
    out = encoded(witness)
    need(len(out) <= 8388608, "output-budget")
    if not sys.argv[1:]:
        saved = source.with_name("CERTIFICATE.json")
        protected[saved] = read(saved)
        saved_check(protected[saved], witness)
        out = encoded(dict(status="PASS", schema=SCHEMA, checker_sha256=witness["checker_sha256"],
                           certificate_sha256=sha256(protected[saved]).hexdigest(),
                           reconstructed_sha256=sha256(encoded(witness)).hexdigest(),
                           decision=witness["decision"], fixture_count=len(witness["fixtures"]),
                           refusal_count=len(CONTROL_PAIRS), independent_audit=False))
    # Outer caller must independently perform these checks on every failure path too.
    for path, raw in protected.items():
        need(read(path) == raw, "protected-changed")
    budget()
    sys.stdout.buffer.write(out)
    sys.stdout.buffer.flush()
    budget()
    signal.alarm(0)


if __name__ == "__main__":
    main()
