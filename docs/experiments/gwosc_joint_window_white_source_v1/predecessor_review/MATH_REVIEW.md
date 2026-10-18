# RI125 independent static white-kernel mathematical review

**Verdict: no mathematical defect found in the reviewed kernel formulas, conditional on the stated operand/enclosure premises.** This is nonauthor source review only. It does not accept the incomplete application packet, establish qualification, admit an actual input, or supply a physical model.

The full kernel and contract were read as text, with the accepted RI123 design, especially equations (2)–(7). No target was imported, compiled, parsed as Python/AST, evaluated or run. No fixture was generated or executed; no scientific capture, PSD or saved numerical operand was decoded. Only this review was authored; repository, sealed source and Git/index state were untouched.

| Reviewed source | Bytes | SHA-256 |
| --- | ---: | --- |
| /Volumes/AI_DATA/development/det-review-evidence/ri125-joint-window-application-source-fsra3wcw/white_kernel.py | 12790 | b5ce9dd68fe89b09a83bf6e9520f798894b85866f4c48a8a2dfe7449ea0a915f |
| /Volumes/AI_DATA/development/det-review-evidence/ri125-joint-window-application-source-fsra3wcw/CONTRACT.md | 18368 | fc36bcee88c942f1b226fccaa2089d99c9b70dda054b94a4db7f5f93a53c076c |
| /Volumes/AI_DATA/development/det_8_framework-ret/docs/experiments/gwosc_joint_window_application_v1/DESIGN.md | 31586 | 4e725c42d77097e66b5b5cf5c3cc014f97b2a42663b0ef0ee3f78d8b4161699b |

Line references below refer to this pinned white_kernel.py unless explicitly labeled otherwise.

## Lifted interval product and directed coverage

Lines 141–154 preserve each endpoint by lifting to a positive common denominator. For one summand with endpoints [a,b]/d_u and [c,d]/d_h, the code's um=a+b, ur=b-a, hm=c+d, hr=d-c give midpoints um/(2d_u), hm/(2d_h) and nonnegative radii ur/(2d_u), hr/(2d_h). Lines 169–186 therefore accumulate the correct midpoint over denominator 4d_u*d_h and exactly the three required error terms:

`(|um|*hr + ur*|hm| + ur*hr)/(4*d_u*d_h)`.

These are respectively |U0|R_H, R_U|H0| and R_U R_H. No cross-error term is omitted, duplicated or given a signed radius. Summing deterministic absolute bounds is sound even when coefficient errors are correlated; no statistical independence is assumed. Completed lifted sums/products and reduced rational results retain the explicit bit checks; no bound on internal temporary allocations follows.

Lines 177–179 and 187 independently compute each scalar product's four-endpoint minimum/maximum with denominator d_u*d_h, then sum. Bilinearity gives a valid box enclosure. Correlation between different coefficients can make it loose, not unsound. Lines 190–192 check intersection while retaining both complete boxes; they do not replace the primary midpoint-radius box with an opportunistic intersection.

For polarization (lines 165–166, 180–189), with L=lcm(d_u,d_h), pu=um*L/d_u=2L*U0 and ph=hm*L/d_h=2L*H0. Thus `(pu+ph)^2-(pu-ph)^2=16*L^2*U0*H0`; denominator **16L^2** is correct, including unequal strip denominators. This route checks midpoint algebra only, not uncertainty or input provenance.

Lines 195–221 enforce the stated primitive dimensions and row order, then loop over every ordered (i,k) pair and contract `tails[i]` with `heads[k]`. Production size eight yields all **64 directed entries**, each summing all **2769** overlap coordinates. K and E are not silently symmetrized. Diagonal trace fields are formed from the complete matrices. This matches DESIGN lines 83–149 and CONTRACT lines 63–87.

## Gram premises, response and usefulness

Lines 224–257 correctly implement exact unpivoted LDL positivity for symmetric G, both inverse products, symmetric entrywise nonnegative H, delta=max row sum H, gamma=max absolute inverse row sum, and the unchanged rho=delta*gamma<=10^-12 gate. Prior diagonal pivots are checked positive before any later division by them. These checks validate the small recorded matrices, not the inherited claim |Omega-G|<=H or their relationship to a particular captured operator.

Lines 292–299 implement `Z=aG-b(K+K^T)` and `F=aH+b(E+E^T)` with positive a=(n-1)/n and b=(n-1)/n^2. Thus F is symmetric and entrywise nonnegative even when K/E are asymmetric, and `|Xi-Z|<=F` follows from the inherited Gram bound and the newly derived shift bound. Every response entry is retained as [Z-F,Z+F].

Lines 300–305 compute the trace both by summing diagonal interval endpoints and by center `a trG-2b trK`, radius `a trH+2b trE`. These are exactly the contract's opposite-sign endpoint expressions; the equality is algebraic, not a numerical tolerance. Lines 306–310 use the correct structural factors (n-1)^2/n^2 and (n^2-1)/n^2 and retain the primary trace interval after checking intersection. They do not mistake entrywise interval endpoints for Loewner bounds or force PSD by clipping.

For soundness of lines 311–313, symmetry gives `||G^-1||_2<=gamma`. With the accepted Gram-error premise, `||G^-1/2 (Omega-G) G^-1/2||_2<=rho`, hence Omega>=(1-rho)G. Disjoint head/tail support gives Xi>=((n-1)^2/n^2)Omega. Therefore `Xi>=ell*I`, where ell=((n-1)^2/n^2)*(1-rho)/gamma>0. Also the symmetric response error has spectral norm at most delta=max row sum F. Combining these yields the claimed relative Loewner error with eps=delta/ell. These are conditional operator statements, not empirical model-error bounds.

Lines 261–266 and 314–319 distinguish valid enclosure from usefulness: eps above 10^-12 returns the complete result with `accuracy_failed`; it does not refuse, clip, relax the inherited rho gate or trigger a rerun. No numerical usefulness result is established by this source review.

## Remaining premises and qualification coverage

`derive_response`'s equality of saved K/polarization and intersection of saved boxes (lines 278–290) are consistency checks, not authentication or independent recomputation of a supplied Shift. The future wrapper must pass this kernel's own fully derived shift and authenticate the inherited Gram against the same complete accepted operator/capture. Otherwise arbitrary mutually consistent input dictionaries do not prove an actual enclosure. This is already an explicit boundary in the module and CONTRACT lines 75–78 and 125–133; it is not an unreported arithmetic defect.

Meaningful future qualification must exercise the actual unequal-denominator polarization/lifting path, nonzero asymmetric off-diagonal E, and mixed zero/nonzero radii, with an independently authored endpoint/error oracle. Singleton or solely scalar integer-endpoint cases cannot qualify all these paths. The parent is separately reviewing the concrete case/refusal inventory; this mathematical review does not certify that inventory or generate replacement fixtures.

Full-capture parsing and parentage, actual phase/provenance guards, periodic calculations, deterministic join, the independent validator and full qualifier remain expressly unfinished surrounding work. Their absence prevents complete packet/actual application acceptance, but does not change the scoped finding that the reviewed white-kernel interval formulas are sound under their stated premises.
