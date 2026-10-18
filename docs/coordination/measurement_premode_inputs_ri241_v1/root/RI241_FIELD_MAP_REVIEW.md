**The runtime13/request5 assembly is ready as unissued administrative metadata. No source repair or new qualification run is needed.** Independent check `9e613a`, exit 0, passed **1,111 predicates over 668 opaque identities**, including all 567 RI160 dependencies and its 12 executable source files.

The important shape distinction is:

- `runtime13.freeze` is **`{bytes, sha256}`**.
- `request5.freeze` is **`{path, bytes, sha256}`**.

This follows `custody_io.py:55`, `mode_verify.py:88`, and `adapter.py:130–137`; using the three-field reference inside runtime13 would refuse.

Use these exact field routes:

| Runtime13 field | Exact value/source |
|---|---|
| `schema` | `"ri156-root-actual-mode-runtime-v1"` |
| `phase` | `"pre"` |
| `mode` | `"normal"` |
| `freeze` | `{bytes:26214, sha256:"9e0c0e4953c7213a76fea291d5f799984422de8628f039eac4e0d7b3c5758b14"}` |
| `runtime_acceptance` | RI204 `FREEZE_REQUEST.json → accepted_adapters.runtime`; reference A below |
| `environment` | Complete ten-field object from accepted RI170 normal `COMPLETE.json → environment`, identical to RI236 `CURRENT_E_AND_MODE_CONTRACT.json → actual_runtime_record.environment` |
| `snapshot` | Current accepted RI236 `COMPLETE.json → artifacts.PRE`; reference B |
| `baseline` | Accepted profiles → normal completion → `artifacts.PRE`; reference C. Do not substitute the new capture acceptance card. |
| `copy_observation` | Accepted RI226 `FROZEN.json`; reference D |
| `vendor_before` | Accepted projection provenance → `records.PRE.projection`; reference E |
| `vendor_after` | Accepted projection provenance → `records.POST.projection`; reference F |
| `genuine_collection_tools` | RI241 next-step record → `genuine_collection_tools`; reference G |
| `observed_dyld_routes` | A’s complete body → `observed_dyld_routes`; reference H |

All references below are the three-field `{path,bytes,sha256}` form:

| Ref | Absolute path | Bytes | SHA256 |
|---|---|---:|---|
| A | `/Volumes/AI_DATA/development/det-review-evidence/ri204-root-adapters-f04k2tg9/accepted_adapters/RUNTIME_ACCEPTANCE.json` | 22342 | `6c11846207bb55f82057a80a63fddce8ba3b00b21550ffc1dc4326203dd15add` |
| B | `/Volumes/AI_DATA/development/det-review-evidence/ri236-current-e-capture-3geu_r1s/PRE.stdout` | 7142026 | `ee672c5014d38656e19230bdd10c9831fabf71387e30248e600a8b6d2d8f378e` |
| C | `/Volumes/AI_DATA/development/det-review-evidence/ri170-current-e-profile-normal-proposed-gikj2giy/PRE.stdout` | 7142026 | `ee672c5014d38656e19230bdd10c9831fabf71387e30248e600a8b6d2d8f378e` |
| D | `/Volumes/AI_DATA/development/det-review-evidence/ri226-freeze-reconciliation-operation-yvfg_p1b/FROZEN.json` | 127298 | `a58eeff7d3652417cc2cb8a80f5a83c21be9779c0c92f412e5a136cfa937426c` |
| E | `/Volumes/AI_DATA/development/det-review-evidence/ri239-root-current-e-capture-mk6vocq1/PRE_SUPPLIER_STABLE.json` | 1260447 | `cf2e2cedecf1e9430081d769be5ae78395f0b1943967a040b9de03b702cfa4c2` |
| F | `/Volumes/AI_DATA/development/det-review-evidence/ri239-root-current-e-capture-mk6vocq1/POST_SUPPLIER_STABLE.json` | 1260447 | `cf2e2cedecf1e9430081d769be5ae78395f0b1943967a040b9de03b702cfa4c2` |
| G | `/Volumes/AI_DATA/development/det-review-evidence/ri239-root-current-e-capture-mk6vocq1/COLLECTION_PROVENANCE.json` | 2789 | `2c96b9f19b43b597111edbb5d439999ed8f0359b137955af5c1d7789b5425202` |
| H | `/Volumes/AI_DATA/development/det-review-evidence/ri156-operation-ri200-sidecars-ofv27lvp/observed_dyld_routes.json` | 771 | `d428c7a943d1d13feecf1e55cbf0a80d80344636b11f922223e77d16b470fb38` |

**H is reusable:** I verified its entire canonical body equals current snapshot `preobserved_dyld_routes`. No new dyld sidecar is needed. E and F satisfy RI160’s whole-object comparison without losing any nested field; raw timestamps and genuine receipts remain bound through G.

The exact request5 is:

```text
freeze         = {path: E_root/AUTHORIZED_FREEZE.json,
                  bytes: 26214,
                  sha256: 9e0c0e4953c7213a76fea291d5f799984422de8628f039eac4e0d7b3c5758b14}
mode           = "normal"
actual_runtime = actual FilePin obtained AFTER exclusive runtime13 write and reread
baseline       = C
copies         = D
```

Here `E_root` is `/Volumes/AI_DATA/development/det-review-evidence/ri154-white-execution-proposed-42_uvw15`. Do not insert a prospective FilePin before the runtime record exists.

I also verified that D still matches the complete current E tree, freeze identity and all 48/124/30 source roles. All three operational directories remain empty and both mode cards absent. The installed freeze was hashed opaquely, not decoded. Its runtime reference was recovered through the accepted RI204 inputs and RI206 actual admission/request chain.

The next root action is to write and reread the exact runtime13, then construct and reread request5 in the RI241 reservation. **These writes issue no operational authority.** Before running `pre_mode`, retain fresh custody and the separate 12-field admission using the unchanged RI160 source manifest, source adjudication and accepted 106-control consumer card. Review its nine-field result before separately authorizing `mode_card`.

Source authentication/read receipts include `e00691`, `d420c0`, `718175`, `081ed4`, `e4cbec`, `0f4162`, and `4022a8`, all exit 0. Preserve two reviewer lookup failures: `094447` assumed a local RI206 request path; `c7ad36` assumed an admission filename. `062add` located the actual `ADMIT_FREEZE_CANDIDATE.json`, which references RI204’s request; the corrected complete check is `9e613a`. Initial oversized historical displays were truncated; current coordination sections were recovered in `8f09fb`, `9716c4`, and `ecf534`.

I authored earlier RI130/RI141 material, not RI160’s adapter or this new assembly. Original semantics inherit separate acceptance. No source execution, scientific-body decoding, files, cards, E mutations or Git operations occurred. This is compatibility review, not operational acceptance.
