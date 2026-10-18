"""RI207 archive adapter draft. Root must review and preserve it before execution.

Required preparation by root:
* Preserve this exact draft as D/archive_native.py.
* Copy the reviewed D204 publication_helpers.py unchanged to D/publication_helpers.py.
* Preserve ri207_independent_review.json as D/RI205_NONAUTHOR_REVIEW.json.

Importing this draft has no archive effect. Running the installed adapter invokes
the existing publication helper, which reads Git identity and writes the new
archive and NATIVE_PUBLICATION.json. It does not execute scientific sources.
"""
import hashlib
import importlib.util
from pathlib import Path

B = Path("/Volumes/AI_DATA/development/det-review-evidence")
D = B / "ri207-root-four-maxima-review-rrel_hre"
Q = B / "ri205-native-four-maxima-7gkvoked"
HELPER = D / "publication_helpers.py"
METADATA = B / "ri122-root-execution-review-6whn_vky/metadata.py"
BUNDLE = "docs/track_b/native_four_maxima_bound_v1"
HANDOFF = {
    "path": str(Q / "HANDOFF.json"),
    "bytes": 7882,
    "sha256": "cb9c07c5715b4c5b7aa0b610aa642ffc45c6c93fc8dc1996d67205b1a64a4afe",
}
ROOT_PINS = {
    "RI205_ROOT_PROOF_REVIEW.md": (5493, "15d93856d39de80c95a51fd5adc511ff9b01cee5c8fad354dbf4d8d7f5c429d4"),
    "RI205_ROOT_ADJUDICATION.json": (2407, "ad87953b8f9479e2c29de71f3a5864e7828b59c21bda04f094ef6de06f3f08b9"),
    "RI205_ROOT_METADATA_CHECK.json": (12519, "dad5589bd4f0de1e0274962397e78ba8af4a0180ea3a18991e43019fa2d37bc0"),
    "review_ri205.py": (6446, "f33dda772766c8b9e678066a749291df1e04258afa69845d60de478f4c079dce"),
    "adjudicate_native.py": (9720, "e55d818f86e81f92a0fba93f53f0ce6943e41be1bb53b3e767e8452c129fcbfa"),
    "RI208_NATIVE_ASSIGNMENT.json": (2757, "718f13dc72c67b5c8b0999ad13ea76ebc2cc623decff775086681465fb2d04ea"),
    "ENTRY_DIAGNOSTIC.json": (351, "b8946eb36833e189ce2dcf8fb6eb78a1a12583745c86376b8c0e5b009d92eb0a"),
    "ROOT_COORDINATION.json": (1018, "660d4c03c1a2d90b56109e2ecb0695d63af4418f4c2d06f556a28df77a2e23c0"),
    "RI205_NONAUTHOR_REVIEW.json": (7126, "feaa5e53211da695821b4b2d5c1d8ace2457701c706848adb6057140764154da"),
    "publication_helpers.py": (3490, "8b04758d4e19988f67d0d96e86c93a8eb5405704f5b2a3e3d0b401f33afa4277"),
}
OPTIONAL_COORDINATION = ("NATIVE_ACTUAL_RECEIPTS.json", "QR_DISPATCH.json")

README = """# Complete native four-maxima bound

RI205 is independently root-accepted on its named unchanged finite-prefix
premises. Every actual marked six-parent with exactly four maxima satisfies
U6<4+6K+64K^2+1/128<369,664,456,005<370,000,000,000<465,000,000,000<T,
where K=681472/9 and T is the unchanged same-law target.

The full omission identity retains four single sectors, six double sectors,
four triple sectors and the all-four sector. The retained-cap denominator lemma
is proved for the selected ideals S=A+i; it does not assume that the omitted
precursors cover the retained cap. Full four-parent denominators use the
all-ideal floor, while the coefficient bound is restricted to proper slots.

The finite support lemma connects every proper parent-five role ending in a
six-terminal with at least four maxima to a raising role. Accepted RI63 support
then removes only its canonical boundary term, retaining theta restoration.
The all-four potential includes every extra old maximum and complete parity
factor. Original coverage bounds the correction product; exact cancellation
gives C4<1/128. The target comparison uses the same native antichain witness,
not the published numerical maximum or a newly evaluated canonical vector.

Root's independent manual review and metadata result are preserved with the
root checker and adjudication source. Root metadata receipt990fe0 exit0 checks
15 direct sources/543096 bytes, six current files,29 selected references, both
six-file namespaces and15 preserved boundary objects. Author final0603bd exit0
is externally reported and distinct from the recorded preseal0a19b6 result.
The complete author checker was read; checking identity or proof-status flags
does not verify mathematics. The separate nonauthor review transcript retains
its actual read receipts, manual-proof limits and later receipt-attribution
supplement; it is not a provider-authenticated conversation export.

The original author status-display clipping and root entry typo/recovery are
preserved. Inherited423 and older source collections remain exact references,
not new scientific verification or complete transitive custody.

One through four maxima are now settled. Five/six maxima, the global M6 bound,
actual W, individual margins, shared H30 and physical correspondence remain
open. RI208 was assigned after this adjudication to the existing QR task for
the complete five-maxima class. Its assignment and genuine root coordination
record are included solely as administrative history; no active RI208 source
or result is included or accepted. The RET pause and all original executable
qualification obligations remain unchanged and uncredited.

PUBLICATION_MANIFEST.json identifies exact archived copies. DEPENDENCY_MAP.json
retains all declared direct RI205 source identities plus the root review and
publication dependencies, resolving committed equivalents where available.
The archive includes the reviewed adapter and publication/metadata helpers;
its entry snapshot may remain an external dependency. It is a manual proof
archive, not a complete runtime archive, and does not authorize relocated
execution of any archived source.
"""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_bootstrap(path, size, digest):
    require(path.resolve() == path and not path.is_symlink(), "helper path alias")
    raw = path.read_bytes()
    require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest,
            "helper identity differs: " + str(path))


def main():
    require(Path(__file__).resolve() == D / "archive_native.py",
            "Root must preserve the reviewed adapter as D/archive_native.py first.")
    check_bootstrap(HELPER, *ROOT_PINS["publication_helpers.py"])
    check_bootstrap(METADATA, 3144,
                    "d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7")
    # The helper binds its own directory to D and checks entry HEAD/empty index.
    spec = importlib.util.spec_from_file_location("ri207_publication", HELPER)
    require(spec is not None and spec.loader is not None, "missing helper loader")
    p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p)
    m = p.m
    require(m.D == D, "publication helper uses the wrong custody directory")

    m.verify(HANDOFF["path"], HANDOFF)
    for name, (size, digest) in ROOT_PINS.items():
        m.verify(D / name, {"bytes": size, "sha256": digest})
    decision = m.load(D / "RI205_ROOT_ADJUDICATION.json")
    require(decision["status"] == "ACCEPT_COMPLETE_FOUR_MAXIMA_CLASS_CONDITIONAL_THEOREM",
            "RI205 root acceptance required")
    require(decision["handoff"] == HANDOFF, "root decision binds a different handoff")
    require(decision["actual_W_decided"] is False and decision["global_M6_bound_proved"] is False,
            "unexpected claim promotion")

    # packet() checks the complete source namespace and every sealed payload.
    origins = p.packet(Q, "source", key="payloads")
    expected = {"AUTHOR_VERIFICATION.json", "FOUR_MAXIMA.md",
                "FOUR_OMISSION_LEMMA.md", "HANDOFF.json",
                "HANDOFF.md", "SOURCE_REFERENCES.json"}
    require(len(origins) == 6 and {path.name for path, _ in origins} == expected,
            "exact six-file RI205 source packet required")
    root_names = list(ROOT_PINS) + ["archive_native.py"]
    included_optional = []
    for name in OPTIONAL_COORDINATION:
        if (D / name).exists():
            require((D / name).is_file(), "coordination record is not a file")
            root_names.append(name)
            included_optional.append(name)
    origins += [(D / name, "root_review/" + name) for name in root_names]
    origins.append((METADATA, "root_review/metadata.py"))

    refs = m.load(Q / "SOURCE_REFERENCES.json")
    require(len(refs["direct_sources"]) == 15, "expected complete15 direct RI205 sources")
    rows = [row["identity"] for row in refs["direct_sources"]]
    rows += [m.ref(path) for path, _ in origins]
    # Required publication context, retained as identity dependencies rather
    # than silently claiming that the complete repository snapshot is copied.
    rows += [m.ref(D / "REPO_ENTRY.json")]
    unique = {}
    for row in rows:
        item = {key: row[key] for key in ("path", "bytes", "sha256")}
        require(item["path"] not in unique or unique[item["path"]] == item,
                "conflicting declared identity: " + item["path"])
        unique[item["path"]] = item
    for row in unique.values():
        m.verify(row["path"], row)

    result = p.archive(BUNDLE, origins, list(unique.values()), README, True)
    result["optional_coordination_archived"] = included_optional
    result["independent_review_transcript"] = "root_review/RI205_NONAUTHOR_REVIEW.json"
    print(m.save("NATIVE_PUBLICATION.json", result))


if __name__ == "__main__":
    main()
