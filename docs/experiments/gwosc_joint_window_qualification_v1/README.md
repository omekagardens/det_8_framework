# Exact joint-window synthetic qualification

27 September 2026 UTC. Both genuine serial modes pass all **41 controls per
implementation**, nine scientific cases, three bounds and twelve groups. Their
complete 81,253-byte canonical reports are identical, SHA256
`395f217fda2939d096822f9446d01216db4ac54f1d53fe4275830ddd2d05f70a`.

| Mode | Active child seconds | Peak sampled RSS KiB | Monitor samples |
| --- | ---: | ---: | ---: |
| Normal | 3.149145334 | 54688 | 97 |
| Optimized | 3.127368416 | 52864 | 97 |

Limits remain 180 seconds, 524288 KiB sampled sole-child RSS, 25 ms target
polling, 100 ms maximum successful/final gap and 50 ms monitor timeout.
This is sampled process monitoring, not an allocator or process-tree cap.

The qualification tests shared samples, directed cross-window covariance,
mean dispersion, signed/scaled outputs, canonical parsing, PSD refusals and
the fixed covariance/calibration error fixtures. The actual captured worker
ran both implementations' controls and independently checked its saved report
against a newly enumerated reference. Saved refusal labels alone would not
establish that those controls executed.

A separate root moment calculation reconstructed all twenty fields of every
case and every field of all three bounds. A nonauthor mathematical review found
no defect. For example, equal marginal variances give centered expectations
3/2 for the white-overlap fixture and 2 for the periodic fixture; choosing the
joint law matters. The oriented fixture retains both nonsymmetric cross-block
directions, with centered matrix [[3/2,3/4],[3/4,1]]. No scalar trace substituted
for that complete matrix.

## Runtime and custody

The fresh inventory binds 9923 files/258862951 bytes, complete source/bytecode
trees, interpreter links, eight fixed absences, OpenSSL configuration and eight
loader bindings. Actual normal/optimized runtime observations agree except
optimization. Both observe the Python decimal fallback after a genuine missing
libmpdec3 error. Three additional observed loader routes and the mpdecimal link
are checked separately by root before and after science, together with optional
native namespace membership and source/cache selection metadata. These sidecar
checks are additional external custody; the unchanged v2 in-process helper does
not enforce them. Every production pre/post record must contain the exact
nonnull sidecar reference. Both pairs match byte for byte.

Trusted installed suppliers/cache selection and the Apple kernel/loader/shared
cache remain explicit premises. Existing bytecode is pinned, not proved
equivalent to source. Module descriptors and digest algorithm names are not a
complete dynamic loader trace or provider identities. No Homebrew dependency
is exempted as an Apple system library. Installed binary bytes are not exported
here; paths and complete hash inventories preserve this host-specific evidence.

The metadata-review draft's unused bytes-to-JSON comparison failed before its
checks; its exact draft and repair note are retained. Only that review script
was corrected. No scientific source, output, limit or threshold changed, and
the scientific normal run was not retried.

## Evidence and next action

See [final adjudication](root/ROOT_FINAL_QUALIFICATION_ADJUDICATION.json),
[normal result](normal/RESULT.json), [optimized result](optimized/RESULT.json),
the complete receipts alongside them, and `reviews/`. `COPY_IDENTITIES.json`
maps the published bytes to immutable external evidence. The source dependencies
remain in [the scientific bundle](../gwosc_joint_window_synthetic_v1/CONTRACT.md)
and [the repaired caller bundle](../gwosc_joint_window_caller_v1/EXECUTION_CONTRACT.source-only.md),
already published in c5939d2 and 4554875. Earlier failure and guard evidence remain intact.

Next measurement work is a concrete application design for the existing
RI116 public-data comparison: bind its real operator/overlap and declared
joint covariance/mean model, keep an independently reconstructible computation,
and preserve calibration/model-adequacy prerequisites before any empirical run.
This checkpoint qualifies exact finite synthetic arithmetic. It establishes no
physical noise law, significance, protected validation or native forward map.
Native RI122 source review remains a separate active lane. RET stays paused;
the wider programme remains incomplete.
