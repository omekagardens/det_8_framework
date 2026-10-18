"""RI161 Q/R qualification source, not an executed qualification.

The admitted caller supplies authenticated unchanged subject modules. This
module has no CLI, subject loader, file access or production entry call.
Synthetic bytes and independent expected trees are created only during a later
run_controls call. Explicit rational examples, not either subject, supply the
oracle. case_catalogue lists descriptors without creating those byte fixtures.
"""

import copy
import hashlib
import json


DOMAIN = {
    "schema": "ri41-height-primal-v1", "seed": "interior_a", "parent_size": 4,
    "potential": "RI-38 maximal-deletion",
    "component_order": "increasing minimum canonical-local-key",
}
ROOT_BASIS = "INHERITED_PINNED_RI41_ACCEPTANCE_NOT_RECONSTRUCTED"
SCOPE = "GRID_ONLY_NOT_LAW_CAPACITY_W_H30_OR_PHYSICAL_ACCEPTANCE"
INPUTS = {
    "certificate": {
        "path": "/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/CERTIFICATE.json",
        "bytes": 2845, "sha256": "3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969"},
    "original_source": {
        "path": "/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/check.py",
        "bytes": 13219, "sha256": "f33a2345608867138f1036da6a020beb6608e3f58fc3032ceb1d3c3d5c9f90c5"},
    "original_manuscript": {
        "path": "/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md",
        "bytes": 16243, "sha256": "567596a17c69e20b33328b2d0c39f22d98a78f7d25d81949fd57cd07df5e53c8"},
    "assignment": {
        "path": "/Volumes/AI_DATA/development/det-review-evidence/ri157-root-adjudication-q_wj4pny/NATIVE_SUCCESSOR_ASSIGNMENT.json",
        "bytes": 4916, "sha256": "782b057624a35094093558e52e40a78d3a61b3ff1cbb61d2c3dd675171b1911e"},
    "accepted_predecessor": {
        "path": "/Volumes/AI_DATA/development/det-review-evidence/ri157-root-adjudication-q_wj4pny/RI157_ROOT_ADJUDICATION.json",
        "bytes": 2404, "sha256": "d052d2c1f51691a861792690a89d8175755c8bffd5016a81b892c8d7abd76950"},
    "accepted_manual_review": {
        "path": "/Volumes/AI_DATA/development/det-review-evidence/ri157-root-adjudication-q_wj4pny/ROOT_MANUAL_REVIEW.md",
        "bytes": 4362, "sha256": "3040fadd824a82b8aee1c51338719ff79da7a3eb0d1c56ce9c1816588dba2b05"},
}
TOP_FIELDS = ("schema", "status", "domain", "inputs", "root_order_basis", "default",
              "override_indices", "components", "counts", "off_grid_indices", "scope")
RATIONAL_FIELDS = ("alpha", "scaled_numerator", "scaled_denominator", "on_grid")
COMPONENT_FIELDS = ("index", "root", "origin") + RATIONAL_FIELDS
COUNT_FIELDS = ("components", "defaulted", "overridden", "on_grid", "off_grid")
CERTIFICATE_FIELDS = tuple(DOMAIN) + ("roots", "default_alpha", "overrides")


class QualificationFailure(Exception):
    """Unexpected suite failure; completed records remain available to caller."""

    def __init__(self, message, records):
        super().__init__(message)
        self.records = records


def _dump(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def _digest(value):
    return hashlib.sha256(_dump(value)).hexdigest()


def _equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(_equal(left[key], right[key]) for key in left)
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(_equal(a, b) for a, b in zip(left, right))
    return left == right


def _fields(tag):
    # Independently specified finite answers; no Fraction/gcd/parser/subject call.
    table = {
        "eighth": ("1/8", "125", "1", True),
        "third": ("1/3", "1000", "3", False),
        "half_scaled": ("1/2000", "1", "2", False),
        "grid_unit": ("1/1000", "1", "1", True),
        "two": ("2/1", "2000", "1", True),
        "large": ("1" + "0" * 63 + "/1", "1" + "0" * 66, "1", True),
    }
    return dict(zip(RATIONAL_FIELDS, table[tag]))


def _certificate(default="1/8", overrides=None, alternate_roots=False):
    result = dict(DOMAIN)
    result.update({"roots": [[i, 1, 1] if alternate_roots else [i, 0, 0]
                              for i in range(109)],
                   "default_alpha": default, "overrides": dict(overrides or {})})
    return result


def _oracle(default="eighth", override_tags=None, alternate_roots=False, root_change=None):
    tags = dict(override_tags or {})
    entries = []
    off = []
    for index in range(109):
        chosen = tags.get(index, default)
        root = [index, 1, 1] if alternate_roots else [index, 0, 0]
        if root_change is not None and index == root_change[0]:
            root[root_change[1]] = root_change[2]
        row = {"index": index, "root": root,
               "origin": "override" if index in tags else "default", **_fields(chosen)}
        entries.append(row)
        if chosen in ("third", "half_scaled"):
            off.append(index)
    domain = {**DOMAIN, "component_count": 109, "grid_denominator": 1000}
    return {"schema": "ri159-final-witness-grid-result-v1",
            "status": "GRID_FAIL" if off else "GRID_PASS", "domain": domain,
            "inputs": copy.deepcopy(INPUTS), "root_order_basis": ROOT_BASIS,
            "default": _fields(default), "override_indices": sorted(tags),
            "components": entries,
            "counts": {"components": 109, "defaulted": 109 - len(tags),
                       "overridden": len(tags), "on_grid": 109 - len(off), "off_grid": len(off)},
            "off_grid_indices": off, "scope": SCOPE}


def _math_payload(envelope, implementation):
    keep = ("status", "default", "override_indices", "components", "counts", "off_grid_indices")
    result = {key: copy.deepcopy(envelope[key]) for key in keep}
    if implementation == "checker":
        result["domain"] = copy.deepcopy(envelope["domain"])
    return result


def _receipt(grid_status="GRID_PASS"):
    return {"schema": "ri159-grid-saved-audit-verdict-v1", "status": "MATCH",
            "reported_grid_status": grid_status, "components_compared": 109,
            "comparison": "ALL_RESULT_FIELDS_EXACT_TYPE_SENSITIVE_RECOMPUTATION",
            "boundary": "DIRECT_ARGUMENTS_NOT_AUTHENTICATED",
            "root_order_basis": ROOT_BASIS, "scope": SCOPE}


def _q_plans():
    plans = []
    def add(family, *variants):
        plans.extend((family, variant) for variant in variants)
    for family in ("Q01", "Q02", "Q03", "Q04", "Q06", "Q07", "Q08", "Q09",
                   "Q11", "Q12", "Q13", "Q15", "Q35"):
        add(family, "main")
    add("Q05", *(str(index).zfill(3) for index in range(109)))
    add("Q10", "unreduced", "leading_zero")
    add("Q14", "grid_unit", "integer")
    add("Q16", "numerator", "denominator", "padded_numerator", "padded_denominator")
    add("Q17", "zero", "zero_numerator", "zero_denominator", "padded_numerator", "padded_denominator")
    add("Q18", "zero", "bad_denominator", "wrong_type")
    add("Q19", "negative", "plus", "leading_space", "trailing_space", "inner_space",
        "decimal", "exponent", "unicode", "multiple_slash")
    add("Q20", "integer", "true", "false", "null", "array", "object")
    add("Q21", *tuple(DOMAIN), "parent_bool", "parent_float", "parent_string")
    add("Q22", *("missing." + key for key in CERTIFICATE_FIELDS), "extra")
    add("Q23", *CERTIFICATE_FIELDS, "override")
    add("Q24", "top", "override")
    add("Q25", "missing", "extra")
    add("Q26", "duplicate", "swap")
    add("Q27", "short", "long", "object", "null", "bool", "string")
    add("Q28", "relation_low", "relation_high", "precursor_low", "precursor_high",
        "marks_low", "marks_high", "subset", "relation_at_limit", "masks_at_limit")
    add("Q29", "negative", "high", "double_zero", "leading_zero", "plus", "empty",
        "space", "unicode", "three_high", "four_digits", "decimal")
    add("Q30", "array", "null", "integer", "string", "bool")
    add("Q31", "utf8", "balanced_bad", "trailing", "incomplete", "unmatched",
        "mismatched", "empty", "argument_type")
    add("Q32", "float", "nan", "infinity", "negative_infinity", "integer_over", "integer_at_limit")
    add("Q33", "bytes_at_limit", "bytes_over", "depth_at_limit", "depth_over", "depth_semantic")
    add("Q34", "quoted_parser", "quoted_rational")
    return plans


def _dictionary_paths():
    pairs = [((), TOP_FIELDS), (("domain",), tuple(DOMAIN) + ("component_count", "grid_denominator")),
             (("inputs",), tuple(INPUTS)), (("default",), RATIONAL_FIELDS), (("counts",), COUNT_FIELDS)]
    pairs.extend((("inputs", role), ("path", "bytes", "sha256")) for role in INPUTS)
    pairs.extend((("components", index), COMPONENT_FIELDS) for index in range(109))
    return pairs


def _r_plans():
    plans = [("R01", "main", ()), ("R02", "main", ())]
    for key in ("schema", "status", "root_order_basis", "scope"):
        plans.append(("R03", key, (key,)))
    for key in tuple(DOMAIN) + ("component_count", "grid_denominator"):
        plans.append(("R04", "domain." + key, ("domain", key)))
    for role in INPUTS:
        for key in ("path", "bytes", "sha256"):
            plans.append(("R04", role + "." + key, ("inputs", role, key)))
    for key in RATIONAL_FIELDS:
        for mode in ("active", "inactive"):
            plans.append(("R05", mode + "." + key, ("default", key)))
    for kind in ("remove", "add", "duplicate", "reorder"):
        plans.append(("R06", kind, ()))
    for index in range(109):
        for key in ("index", "origin"):
            plans.append(("R07", str(index).zfill(3) + "." + key, ("components", index, key)))
        for coordinate in range(3):
            plans.append(("R07", str(index).zfill(3) + ".root." + str(coordinate),
                          ("components", index, "root", coordinate)))
        for key in RATIONAL_FIELDS:
            plans.append(("R08", str(index).zfill(3) + "." + key, ("components", index, key)))
    for key in ("alpha", "scaled_numerator", "scaled_denominator"):
        plans.append(("R09", key, ("components", 54, key)))
    for key in COUNT_FIELDS:
        plans.append(("R10", "count." + key, ("counts", key)))
    for key in ("override_indices", "off_grid_indices"):
        for mode in ("remove", "add", "reverse"):
            plans.append(("R10", key + "." + mode, (key,)))
    for mode in ("true_as_one", "false_as_zero", "count_string", "index_bool", "root_bool"):
        plans.append(("R11", mode, ()))
    plans.append(("R12", "coherent_false", ()))
    for parent, keys in _dictionary_paths():
        parent_label = ".".join(map(str, parent)) or "top"
        plans.append(("R13", "extra." + parent_label, parent))
        for key in keys:
            plans.append(("R13", "missing." + parent_label + "." + key, parent + (key,)))
    for kind in ("duplicate_top", "duplicate_nested", "escaped_duplicate", "float", "nan",
                 "infinity", "utf8", "trailing", "malformed"):
        plans.append(("R14", kind, ()))
    for kind in ("bytes_at_limit", "bytes_over", "depth_at_limit", "depth_over", "depth_semantic"):
        plans.append(("R15", kind, ()))
    for kind in ("object_order", "whitespace"):
        plans.append(("R16", kind, ()))
    return plans


def _parser_case(family, variant):
    return (family == "Q32" and variant == "integer_at_limit" or
            family == "Q33" and variant in ("depth_at_limit", "depth_over") or
            family == "Q34" and variant == "quoted_parser" or
            family == "R15" and variant in ("depth_at_limit", "depth_over"))


def case_catalogue():
    result = []
    for family, variant in _q_plans():
        for implementation in ("checker", "auditor"):
            result.append({"id": family + "." + variant + "." + implementation,
                           "family": family, "implementation": implementation,
                           "boundary": "SYNTHETIC_Q_PARSER" if _parser_case(family, variant)
                           else "SYNTHETIC_Q_RECONSTRUCTION"})
    for family, variant, _ in _r_plans():
        result.append({"id": family + "." + variant + ".auditor", "family": family,
                       "implementation": "auditor",
                       "boundary": "SYNTHETIC_R_PARSER" if _parser_case(family, variant)
                       else "SYNTHETIC_R_SAVED_RESULT"})
    return result


def _nested(depth):
    result = 0
    for _ in range(depth):
        result = [result]
    return result


def _q_fixture(family, variant):
    data = _certificate()
    oracle = _oracle()
    tag = None
    raw = None
    if family in ("Q02", "Q03", "Q04", "Q05"):
        index = {"Q02": 0, "Q03": 54, "Q04": 108}.get(family, None)
        if index is None:
            index = int(variant)
        data["overrides"] = {str(index): "1/3"}
        oracle = _oracle(override_tags={index: "third"})
    elif family in ("Q06", "Q07"):
        default, value, default_tag, value_tag = ("1/3", "1/8", "third", "eighth") if family == "Q06" else ("1/8", "1/3", "eighth", "third")
        data = _certificate(default, {str(i): value for i in range(109)})
        oracle = _oracle(default_tag, {i: value_tag for i in range(109)})
    elif family == "Q08":
        data["overrides"] = {"0": "1/3", "54": "1/3", "108": "1/3"}
        del data["overrides"]["54"]
        oracle = _oracle(override_tags={0: "third", 108: "third"})
    elif family == "Q09":
        data["overrides"] = {"54": "1/8"}
        oracle = _oracle(override_tags={54: "eighth"})
    elif family in ("Q10", "Q11", "Q12", "Q13", "Q14", "Q15"):
        examples = {"Q10": ("2/16" if variant == "unreduced" else "0002/0016", "eighth"),
                    "Q11": ("3/24", "eighth"), "Q12": ("2/6", "third"),
                    "Q13": ("1/2000", "half_scaled"),
                    "Q14": ("1/1000", "grid_unit") if variant == "grid_unit" else ("2", "two"),
                    "Q15": ("1" + "0" * 63 + "/1", "large")}
        value, expected_tag = examples[family]
        data["overrides"] = {"54": value}
        oracle = _oracle(override_tags={54: expected_tag})
    elif family == "Q16":
        values = {"numerator": "1" * 65 + "/1", "denominator": "1/" + "1" * 65,
                  "padded_numerator": "0" * 64 + "1/1", "padded_denominator": "1/" + "0" * 64 + "1"}
        data["default_alpha"] = values[variant]
        tag = "rational_term_length"
    elif family == "Q17":
        data["default_alpha"] = {"zero": "0", "zero_numerator": "0/8", "zero_denominator": "1/0",
                                  "padded_numerator": "000/08", "padded_denominator": "01/000"}[variant]
        tag = "rational_nonpositive"
    elif family == "Q18":
        data = _certificate({"zero": "0", "bad_denominator": "1/0", "wrong_type": None}[variant],
                            {str(i): "1/8" for i in range(109)})
        tag = "rational_type" if variant == "wrong_type" else "rational_nonpositive"
    elif family == "Q19":
        data["default_alpha"] = {"negative": "-1/8", "plus": "+1/8", "leading_space": " 1/8",
                                  "trailing_space": "1/8 ", "inner_space": "1 /8", "decimal": "0.125",
                                  "exponent": "1e-3", "unicode": "١/8", "multiple_slash": "1/2/3"}[variant]
        tag = "rational_multiple" if variant == "multiple_slash" else "rational_syntax"
    elif family == "Q20":
        data["default_alpha"] = {"integer": 1, "true": True, "false": False, "null": None,
                                  "array": [], "object": {}}[variant]
        tag = "rational_type"
    elif family == "Q21":
        if variant.startswith("parent_") and variant != "parent_size":
            if variant == "parent_float":
                raw = _dump(data).replace(b'"parent_size":4', b'"parent_size":4.0')
                tag = "json_float"
            else:
                data["parent_size"] = True if variant == "parent_bool" else "4"
                tag = "parent_domain"
        elif variant == "parent_size":
            data["parent_size"] = 5
            tag = "parent_domain"
        else:
            data[variant] = "changed"
            tag = "domain:" + variant
    elif family == "Q22":
        if variant == "extra":
            data["extra"] = 0
        else:
            del data[variant.split(".", 1)[1]]
        tag = "certificate_fields"
    elif family in ("Q23", "Q24"):
        if variant == "override":
            key = '"0"' if family == "Q23" else '"\\u0030"'
            raw = _dump(data).replace(b'"overrides":{}', ('"overrides":{"0":"1/8",' + key + ':"1/8"}').encode("ascii"))
        else:
            key = variant if family == "Q23" else "schema"
            spelling = _dump(key) if family == "Q23" else b'"\\u0073chema"'
            raw = _dump(data)[:-1] + b"," + spelling + b":" + _dump(data[key]) + b"}"
        tag = "json_duplicate"
    elif family == "Q25":
        if variant == "missing":
            data["roots"].pop()
        else:
            data["roots"].append([109, 0, 0])
        tag = "root_count"
    elif family == "Q26":
        if variant == "duplicate":
            data["roots"][54] = list(data["roots"][53])
        else:
            data["roots"][53], data["roots"][54] = data["roots"][54], data["roots"][53]
        tag = "root_order"
    elif family == "Q27":
        data["roots"][54] = {"short": [54, 0], "long": [54, 0, 0, 0], "object": {},
                              "null": None, "bool": [True, 0, 0], "string": ["54", 0, 0]}[variant]
        tag = "root_members" if variant in ("bool", "string") else "root_shape"
    elif family == "Q28":
        edits = {"relation_low": (0, -1), "relation_high": (0, 65536),
                 "precursor_low": (1, -1), "precursor_high": (1, 16),
                 "marks_low": (2, -1), "marks_high": (2, 16), "subset": (2, 1)}
        if variant == "relation_at_limit":
            data["roots"][108][0] = 65535
            oracle = _oracle(root_change=(108, 0, 65535))
        elif variant == "masks_at_limit":
            data["roots"][54][1:] = [15, 15]
            oracle["components"][54]["root"] = [54, 15, 15]
        else:
            coordinate, value = edits[variant]
            data["roots"][54][coordinate] = value
            tag = "root_subset" if variant == "subset" else "root_bounds"
    elif family == "Q29":
        label = {"negative": "-1", "high": "109", "double_zero": "00", "leading_zero": "01",
                 "plus": "+1", "empty": "", "space": " 1", "unicode": "١",
                 "three_high": "999", "four_digits": "1000", "decimal": "1.0"}[variant]
        data["overrides"] = {label: "1/8"}
        tag = "override_high" if variant in ("high", "three_high") else "override_padding" if variant in ("double_zero", "leading_zero") else "override_label"
    elif family == "Q30":
        data["overrides"] = {"array": [], "null": None, "integer": 1, "string": "x", "bool": False}[variant]
        tag = "override_shape"
    elif family == "Q31":
        raw = {"utf8": b"\xff", "balanced_bad": b'{"x":}', "trailing": b"{}{}",
               "incomplete": b"{", "unmatched": b"}", "mismatched": b"[}",
               "empty": b"", "argument_type": "not-bytes"}[variant]
        tag = {"utf8": "json_utf8", "incomplete": "json_incomplete", "unmatched": "json_unmatched",
               "mismatched": "json_mismatched", "empty": "input_empty", "argument_type": "input_type"}.get(variant, "json_syntax")
    elif family == "Q32":
        raw = {"float": b"1.0", "nan": b"NaN", "infinity": b"Infinity",
               "negative_infinity": b"-Infinity", "integer_over": b"10000000000",
               "integer_at_limit": b"9999999999"}[variant]
        tag = None if variant == "integer_at_limit" else "json_float" if variant == "float" else "json_integer" if variant == "integer_over" else "json_constant"
        oracle = 9999999999
    elif family == "Q33":
        if variant.startswith("bytes"):
            raw = _dump(data)
            raw += b" " * (65536 - len(raw) + (1 if variant == "bytes_over" else 0))
            tag = "input_size" if variant == "bytes_over" else None
        else:
            depth = 9 if variant == "depth_over" else 8
            raw = b"[" * depth + b"0" + b"]" * depth
            oracle = _nested(depth)
            tag = "json_depth" if variant == "depth_over" else "certificate_fields" if variant == "depth_semantic" else None
    elif family == "Q34":
        quoted = "[" * 20 + '}"\\' + "]" * 20
        if variant == "quoted_parser":
            raw, oracle = _dump(quoted), quoted
        else:
            data["default_alpha"] = quoted
            tag = "rational_syntax"
    elif family == "Q35":
        data = _certificate(alternate_roots=True)
        oracle = _oracle(alternate_roots=True)
    return (_dump(data) if raw is None else raw), oracle, tag


def _q_error(tag, implementation):
    # Exact first-refusal strings from the sealed, unchanged RI159 subjects.
    table = {
        "rational_type": (("RATIONAL_TYPE", "coefficient must be a string"), ("AUDIT_RATIONAL_TYPE", "coefficient must be a rational string")),
        "rational_term_length": (("RATIONAL_LENGTH", "rational term exceeds sixty-four digits"), ("AUDIT_RATIONAL_SIZE", "rational term requires one to 64 digits")),
        "rational_nonpositive": (("RATIONAL_POSITIVITY", "coefficient numerator and denominator must be positive"), ("AUDIT_RATIONAL_NONPOSITIVE", "rational terms must be positive")),
        "rational_syntax": (("RATIONAL_SYNTAX", "coefficient must use ASCII digits and optional slash"), ("AUDIT_RATIONAL_SYNTAX", "rational terms require ASCII decimal digits")),
        "rational_multiple": (("RATIONAL_SYNTAX", "coefficient must use ASCII digits and optional slash"), ("AUDIT_RATIONAL_SYNTAX", "rational requires an integer or N/D")),
        "parent_domain": (("CERTIFICATE_DOMAIN", "certificate parent_size must be integer four"), ("AUDIT_CERTIFICATE_DOMAIN", "certificate domain label differs")),
        "certificate_fields": (("CERTIFICATE_KEYS", "certificate requires exactly eight declared fields"), ("AUDIT_CERTIFICATE_FIELDS", "certificate must have exactly the eight declared fields")),
        "root_count": (("ROOT_COUNT", "certificate requires exactly 109 roots"), ("AUDIT_ROOT_COUNT", "certificate requires exactly 109 root triples")),
        "root_order": (("ROOT_ORDER", "root triples must be strictly increasing and unique"), ("AUDIT_ROOT_ORDER_SHAPE", "root triples must be strictly lexicographically increasing")),
        "root_shape": (("ROOT_SHAPE", "root must be a triple of strict integers"), ("AUDIT_ROOT_SHAPE", "each root must be a three-integer array")),
        "root_members": (("ROOT_SHAPE", "root must be a triple of strict integers"), ("AUDIT_ROOT_SHAPE", "root entries must be integers, not booleans")),
        "root_bounds": (("ROOT_MASK", "root integer or record mask is outside the declared shape"), ("AUDIT_ROOT_BOUNDS", "root entry is outside its four-carrier bounds")),
        "root_subset": (("ROOT_MASK", "root integer or record mask is outside the declared shape"), ("AUDIT_ROOT_MARKS", "root marks are not a subset of the precursor")),
        "override_shape": (("OVERRIDE_SHAPE", "overrides must be an object of at most 109 entries"), ("AUDIT_OVERRIDES_TYPE", "overrides must be a bounded index object")),
        "override_label": (("OVERRIDE_INDEX", "override index must be a canonical decimal label"), ("AUDIT_OVERRIDE_LABEL", "override label must be a canonical decimal index")),
        "override_padding": (("OVERRIDE_INDEX", "override index must be a canonical decimal label"), ("AUDIT_OVERRIDE_LABEL", "override label must be a canonical index from zero to 108")),
        "override_high": (("OVERRIDE_INDEX", "override index is outside zero through 108"), ("AUDIT_OVERRIDE_LABEL", "override label must be a canonical index from zero to 108")),
        "json_duplicate": (("JSON_DUPLICATE_KEY", "duplicate JSON object key"), ("AUDIT_JSON_DUPLICATE_KEY", "duplicate JSON object key")),
        "json_float": (("JSON_NUMBER", "floating or nonfinite JSON number is forbidden"), ("AUDIT_JSON_FLOAT", "JSON floating-point numbers are forbidden")),
        "json_constant": (("JSON_NUMBER", "floating or nonfinite JSON number is forbidden"), ("AUDIT_JSON_CONSTANT", "JSON nonfinite constants are forbidden")),
        "json_integer": (("JSON_INTEGER", "JSON integer exceeds ten digits"), ("AUDIT_JSON_INTEGER", "JSON integer token exceeds ten digits")),
        "json_depth": (("JSON_DEPTH", "certificate JSON nesting exceeds eight"), ("AUDIT_JSON_DEPTH", "JSON nesting limit violated")),
        "json_utf8": (("JSON_SYNTAX", "invalid certificate UTF-8 JSON"), ("AUDIT_UTF8", "JSON input is not strict UTF-8")),
        "json_syntax": (("JSON_SYNTAX", "invalid certificate UTF-8 JSON"), ("AUDIT_JSON_SYNTAX", "JSON input has invalid syntax")),
        "json_incomplete": (("JSON_SYNTAX", "unbalanced certificate JSON"), ("AUDIT_JSON_SYNTAX", "JSON input is incomplete")),
        "json_unmatched": (("JSON_SYNTAX", "unbalanced certificate JSON"), ("AUDIT_JSON_SYNTAX", "JSON delimiters are unbalanced")),
        "json_mismatched": (("JSON_SYNTAX", "invalid certificate UTF-8 JSON"), ("AUDIT_JSON_SYNTAX", "JSON delimiters are mismatched")),
        "input_size": (("CERTIFICATE_BYTES", "certificate must be nonempty bounded bytes"), ("AUDIT_INPUT_SIZE", "JSON byte limit violated")),
        "input_empty": (("CERTIFICATE_BYTES", "certificate must be nonempty bounded bytes"), ("AUDIT_INPUT_SIZE", "JSON byte limit violated")),
        "input_type": (("CERTIFICATE_BYTES", "certificate must be nonempty bounded bytes"), ("AUDIT_ARGUMENT_TYPE", "JSON input must be bytes")),
    }
    if tag.startswith("domain:"):
        pair = (("CERTIFICATE_DOMAIN", "certificate domain label changed: " + tag.split(":", 1)[1]),
                ("AUDIT_CERTIFICATE_DOMAIN", "certificate domain label differs"))
    else:
        pair = table[tag]
    return pair[0 if implementation == "checker" else 1]


def _get(tree, path):
    for part in path:
        tree = tree[part]
    return tree


def _set(tree, path, value):
    _get(tree, path[:-1])[path[-1]] = value


def _location(path):
    return "result" + "".join("[" + str(part) + "]" if type(part) is int else "." + part for part in path)


def _different(value):
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return value + "changed"
    raise RuntimeError("unsupported mutation leaf")


def _result_error(kind, path):
    messages = {"VALUE": "saved-result value differs at ", "TYPE": "saved-result type differs at ",
                "KEYS": "saved-result keys differ at ", "LENGTH": "saved-result array length differs at "}
    return "AUDIT_RESULT_" + kind, messages[kind] + _location(path)


def _reverse_objects(value):
    if type(value) is dict:
        return {key: _reverse_objects(value[key]) for key in reversed(tuple(value))}
    if type(value) is list:
        return [_reverse_objects(item) for item in value]
    return value


def _r_fixture(family, variant, path):
    certificate = _certificate()
    saved = _oracle()
    expected = _receipt()
    error = None
    raw = None
    if family == "R02":
        certificate = _certificate(overrides={"108": "1/3"})
        saved = _oracle(override_tags={108: "third"})
        expected = _receipt("GRID_FAIL")
    elif family in ("R03", "R04", "R07", "R08"):
        _set(saved, path, _different(_get(saved, path)))
        error = _result_error("VALUE", path)
    elif family == "R05":
        if variant.startswith("inactive."):
            certificate = _certificate("1/3", {str(i): "1/8" for i in range(109)})
            saved = _oracle("third", {i: "eighth" for i in range(109)})
        _set(saved, path, _different(_get(saved, path)))
        error = _result_error("VALUE", path)
    elif family == "R06":
        if variant == "remove":
            saved["components"].pop(54)
        elif variant == "add":
            saved["components"].append(copy.deepcopy(saved["components"][-1]))
        elif variant == "duplicate":
            saved["components"].insert(54, copy.deepcopy(saved["components"][54]))
        else:
            saved["components"][0], saved["components"][1] = saved["components"][1], saved["components"][0]
        error = _result_error("VALUE", ("components", 0, "index")) if variant == "reorder" else _result_error("LENGTH", ("components",))
    elif family == "R09":
        _set(saved, path, {"alpha": "2/16", "scaled_numerator": "0125", "scaled_denominator": "01"}[variant])
        error = _result_error("VALUE", path)
    elif family == "R10":
        if variant.startswith("count."):
            _set(saved, path, _get(saved, path) + 1)
            error = _result_error("VALUE", path)
        else:
            certificate = _certificate(overrides={"0": "1/3", "108": "1/3"})
            saved = _oracle(override_tags={0: "third", 108: "third"})
            values = _get(saved, path)
            operation = variant.rsplit(".", 1)[1]
            if operation == "remove":
                values.pop()
            elif operation == "add":
                values.append(108)
            else:
                values.reverse()
            error = _result_error("VALUE", path + (0,)) if operation == "reverse" else _result_error("LENGTH", path)
    elif family == "R11":
        if variant == "false_as_zero":
            certificate = _certificate(overrides={"108": "1/3"})
            saved = _oracle(override_tags={108: "third"})
            location, value = ("components", 108, "on_grid"), 0
        else:
            location, value = {"true_as_one": (("components", 54, "on_grid"), 1),
                               "count_string": (("counts", "components"), "109"),
                               "index_bool": (("components", 0, "index"), False),
                               "root_bool": (("components", 0, "root", 0), False)}[variant]
        _set(saved, location, value)
        error = _result_error("TYPE", location)
    elif family == "R12":
        saved = _oracle(override_tags={i: "third" for i in range(109)})
        error = _result_error("VALUE", ("components", 0, "alpha"))
    elif family == "R13":
        if variant.startswith("extra."):
            _get(saved, path)["unexpected"] = 0
            error = _result_error("KEYS", path)
        else:
            del _get(saved, path[:-1])[path[-1]]
            error = _result_error("KEYS", path[:-1])
    elif family == "R14":
        if variant in ("duplicate_top", "escaped_duplicate"):
            key = b'"status"' if variant == "duplicate_top" else b'"\\u0073tatus"'
            raw = _dump(saved)[:-1] + b"," + key + b':"GRID_PASS"}'
            error = _q_error("json_duplicate", "auditor")
        elif variant == "duplicate_nested":
            raw = _dump(saved).replace(b'"default":{', b'"default":{"alpha":"1/8",', 1)
            error = _q_error("json_duplicate", "auditor")
        elif variant in ("float", "nan", "infinity"):
            token = {"float": b"109.0", "nan": b"NaN", "infinity": b"Infinity"}[variant]
            raw = _dump(saved).replace(b'"components":109', b'"components":' + token, 1)
            error = _q_error("json_float" if variant == "float" else "json_constant", "auditor")
        elif variant == "utf8":
            raw, error = b"\xff", _q_error("json_utf8", "auditor")
        elif variant == "trailing":
            raw, error = _dump(saved) + b"{}", _q_error("json_syntax", "auditor")
        else:
            raw, error = b'{"x":}', _q_error("json_syntax", "auditor")
    elif family == "R15":
        if variant.startswith("bytes"):
            raw = _dump(saved)
            raw += b" " * (262144 - len(raw) + (1 if variant == "bytes_over" else 0))
            error = _q_error("input_size", "auditor") if variant == "bytes_over" else None
        else:
            depth = 13 if variant == "depth_over" else 12
            raw = b"[" * depth + b"0" + b"]" * depth
            expected = _nested(depth)
            error = _q_error("json_depth", "auditor") if variant == "depth_over" else _result_error("TYPE", ()) if variant == "depth_semantic" else None
    elif family == "R16":
        raw = _dump(_reverse_objects(saved)) if variant == "object_order" else json.dumps(saved, indent=2, sort_keys=False).encode("ascii")
        if variant == "object_order":
            raw = json.dumps(_reverse_objects(saved), sort_keys=False, separators=(",", ":")).encode("ascii")
    return _dump(certificate), (_dump(saved) if raw is None else raw), expected, error


def _summary(outcome, exception_type=None, code=None, message=None, value=None):
    return {"outcome": outcome, "exception_type": exception_type, "code": code,
            "message": message, "output_sha256": _digest(value) if outcome == "RETURN" else None}


def _perform(descriptor, callback, expected_value, expected_error, refusal_type):
    expected = (_summary("REFUSED", refusal_type.__name__, expected_error[0], expected_error[1])
                if expected_error is not None else _summary("RETURN", value=expected_value))
    full = False
    actual_type_correct = True
    try:
        value = callback()
        observed = _summary("RETURN", value=value)
        full = expected_error is None and _equal(value, expected_value)
    except Exception as error:
        actual_type_correct = type(error) is refusal_type
        if actual_type_correct:
            observed = _summary("REFUSED", type(error).__name__, error.code, str(error))
        else:
            observed = _summary("UNEXPECTED_SUBJECT_ERROR", type(error).__name__,
                                None, str(error)[:512])
    passed = actual_type_correct and _equal(expected, observed) and (expected_error is not None or full)
    return {**descriptor, "status": "PASS" if passed else "FAIL", "expected": expected,
            "observed": observed, "full_output_compared": full}


def run_controls(checker, auditor):
    """Future synthetic controls only; no protected input or subject mutation."""
    descriptors = {item["id"]: item for item in case_catalogue()}
    records = []
    try:
        for family, variant in _q_plans():
            for implementation, subject in (("checker", checker), ("auditor", auditor)):
                identifier = family + "." + variant + "." + implementation
                descriptor = descriptors[identifier]
                try:
                    raw, oracle, tag = _q_fixture(family, variant)
                    parser = _parser_case(family, variant)
                    expected = oracle if parser else _math_payload(oracle, implementation) if tag is None else None
                    error = _q_error(tag, implementation) if tag is not None else None
                    if implementation == "checker":
                        callback = (lambda raw=raw: checker.decode_certificate(raw)) if parser else (lambda raw=raw: checker.reconstruct_certificate(checker.decode_certificate(raw)))
                        refusal_type = checker.GridRefused
                    else:
                        callback = (lambda raw=raw: auditor._bounded_json(raw, 65536, 8)) if parser else (lambda raw=raw: auditor.reconstruct_certificate(raw))
                        refusal_type = auditor.AuditRefusal
                    records.append(_perform(descriptor, callback, expected, error, refusal_type))
                except Exception as error:
                    records.append({**descriptor, "status": "FAIL",
                                    "expected": _summary("CASE_BUILT"),
                                    "observed": _summary("HARNESS_ERROR", type(error).__name__, None, str(error)[:512]),
                                    "full_output_compared": False})
        for family, variant, path in _r_plans():
            descriptor = descriptors[family + "." + variant + ".auditor"]
            try:
                certificate_raw, result_raw, expected, error = _r_fixture(family, variant, path)
                callback = (lambda raw=result_raw: auditor._bounded_json(raw, 262144, 12)) if _parser_case(family, variant) else (lambda c=certificate_raw, r=result_raw: auditor.audit_arguments(c, r))
                records.append(_perform(descriptor, callback, expected, error, auditor.AuditRefusal))
            except Exception as error:
                records.append({**descriptor, "status": "FAIL",
                                "expected": _summary("CASE_BUILT"),
                                "observed": _summary("HARNESS_ERROR", type(error).__name__, None, str(error)[:512]),
                                "full_output_compared": False})
    except Exception as error:
        raise QualificationFailure("unexpected qualification suite failure: " + type(error).__name__, records) from error
    return records
