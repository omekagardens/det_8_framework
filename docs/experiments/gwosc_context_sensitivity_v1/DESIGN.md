# RI-55 — finite-context sensitivity of the nominal reference filter

24 September 2026 UTC. **Design and elementary proof; coordinator adjudication
accepted.** No sensitivity implementation, actual-context calculation, rigorous
coefficient-row certificate or physical continuation envelope is supplied by
this note. It freezes the next bounded implementation and qualification target.
All accepted artifacts remain unchanged, and RET remains paused.

The [RI-53 comparison](../gwosc_nr_comparison_v1/COMPARISON.md) filters a supplied
2769-sample reference using an algorithmic boundary condition. Its successful
numerical qualification does not establish what a longer physical waveform
would have produced. This packet separates that missing assumption from a
finite-dimensional question that can be answered without acquiring more data.

**Fixed input and comparison domain.** Use the admitted
[coefficient manifest](../gwosc_nominal_processing_v1/COEFFICIENTS.json), SHA-256
`700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0`,
with its 17 ordered stages, 20 SOS sections and exact coefficient hex strings.
The first stage has four sections and padding 27; each remaining stage has one
section and padding 9. Preserve signed-zero representations in identity checks,
although both signed zeros represent the rational number zero in the proof.
Do not redesign, combine, reorder or retune stages.

Freeze `N=2769`, `L=4096` additional samples on **each** side, and
`T=N+2L=10961`. Filtering uses the existing nominal 4096 Hz index clock.
Neither new time tokens nor a reconstructed uniform grid replace the accepted
printed reference times. The extension is a hypothetical vector on that index
clock, with left indices `-4096,...,-1` and right indices `2769,...,6864`.
The original central vector and its original time metadata remain intact.

The initial implementation target is the eight-row pilot

```text
I = (0, 1, 27, 805, 1384, 2741, 2767, 2768).
```

Index 805 is RI-53's first displayed reference sample; the other indices fix
endpoint, padding-distance and central probes before any sensitivity result.
Every forward qualification compares its complete vector. Row certificates and
nonzero claims in the pilot apply only to the named indices. A full 2769-row
profile requires a separate reviewed resource and output reservation; eight
probes cannot certify an unexamined maximum between them.

**The exact operator.** Interpret each admitted binary64 coefficient as its
exact rational value. For a section `[b0,b1,b2,a0,a1,a2]`, `a0=1` and the
nonzero DC denominator give the exact rational gain

\[
g=(b_0+b_1+b_2)/(a_0+a_1+a_2).
\]

For a pass with input vector `v`, section `s` has constant input prehistory
`c_s=v[0]` times the product of DC gains of preceding sections in that pass.
Initialize `x[-1]=x[-2]=c_s` and `y[-1]=y[-2]=g_s c_s`. Apply, in increasing
sample order and the admitted section order,

\[
y[k]=(b_0x[k]+b_1x[k-1]+b_2x[k-2]
      -a_1y[k-1]-a_2y[k-2])/a_0.
\tag{1}
\]

All operations in this definition are exact. The next section receives the
whole preceding output and its prescribed constant prehistory. Each backward
pass starts a new cascade whose prehistory is derived from the first sample
of the reversed complete forward output. Do not carry final forward states
into the backward pass.

For a length-`m` stage input `v` and its fixed padding `0<=p<m-1`, form the odd extension

```text
(2*v[0]-v[p], ..., 2*v[0]-v[1],
 v[0], ..., v[m-1],
 2*v[m-1]-v[m-2], ..., 2*v[m-1]-v[m-p-1]).
```

For `p=0`, both padding lists are empty and unpadding retains the whole vector.
Apply one ordered cascade, reverse its complete output, apply the same ordered
cascade with fresh initialization, reverse again, then retain `[p:p+m)`.
Repeat this separate extension/filter/unpad procedure for every stage. Padding
is not applied just once around the complete 17-stage cascade.

Write `O` for that stage's odd extension, `A` for its initialized one-pass
cascade, `R` for reversal and `P` for unpadding. The stage is
`S_m=P R A R A O`. Its dimensions include the stage's padding. Define

\[
F_m=S_{16,m}\cdots S_{1,m}S_{0,m}.
\tag{2}
\]

Extension, initialization, recurrence, reversal and cropping are linear with
rational constants. Thus `F_m` is an exact rational matrix, also defining a
linear map on real inputs. Finite evaluation needs no infinite-tail limit.
The admitted stability checks are retained as identity/admission requirements;
finite-dimensional linearity alone does not prove stability or physical truth.

The [production filter](../gwosc_nominal_processing_v1/filtering.py) uses rounded
binary64 operations. The independently authored
[reference](../gwosc_nominal_processing_v1/reference.py) rounds Decimal
operations at precision 80. Neither implemented map is exactly linear, nor is
either implementation the exact matrix in (2). Independent numerical agreement
is a diagnostic, not a proof that rounding vanishes. In particular, a matrix
made by filtering floating-point unit impulses is not automatically an exact
representation of production filtering on arbitrary inputs.

**Known center and unknown extension.** Let `x` be the unchanged central vector
of length `N`. In a later actual calculation, its binary64 values are interpreted
exactly as dyadic rationals. For `z` of length `2L`, its first `L` entries are
the chronological left continuation and its last `L` entries the right one.
Define injections and the crop by

\[
Ex=(0_L,x,0_L),\qquad Uz=(z_{0:L},0_N,z_{L:2L}),\qquad
Cy=y_{L:L+N}.
\tag{3}
\]

Consequently `CE=Id`, `CU=0`, and the compared exact outputs differ by

\[
CF_T(Ex+Uz)-F_Nx=d+Bz,\qquad
d=(CF_TE-F_N)x,\qquad B=CF_TU.
\tag{4}
\]

The zeros in `E` define a useful algebraic reference, not a claim that the
missing physical signal is zero. Even `z=0` need not give `d=0`: filtering
the longer zero-filled vector has different endpoint conditions. `B` is an
`N` by `2L` matrix independent of `x`; `d` depends on the retained center.

**Sharp conditional bound.** Suppose an independently declared, finite scalar
`M>=0` imposes `|z_j|<=M` for every extension coordinate. For each row,

\[
\sup_{\|z\|_\infty\le M}|d_i+(Bz)_i|
   = |d_i|+M\sum_{j=0}^{2L-1}|B_{ij}|.
\tag{5}
\]

The triangle inequality proves the upper bound. Set `sigma=sign(d_i)` when
`d_i!=0`, and `sigma=1` otherwise. Choose
`z_j=M*sigma*sign(B_ij)`, taking `sign(0)=0`. This admissible vector attains
the upper bound, including `M=0` and a zero row. Different rows may require
different attaining continuations; no single physical continuation is asserted
to maximize every row simultaneously. With predeclared coordinate envelopes
`|z_j|<=M_j`, the same proof replaces `M*sum|B_ij|` by `sum M_j|B_ij|`.
The pilot implements only the scalar-envelope version unless separately scoped.

If a particular row has a proven nonzero coefficient `B_ij`, taking arbitrarily
large real `z_j` of the appropriate sign proves that no finite bound independent
of an extension envelope exists on the real extension space of (4) for that row.
If the row is exactly zero, the
answer is `|d_i|`, independent of the extension. A rounded nonzero value or an
interval containing zero does not prove a nonzero coefficient. This note proves
neither alternative for any actual admitted row; it does not assume every row
is nonzero.

Equations (4)-(5) concern exact operators. They do not, by themselves, bound
rounded production filtering uniformly over the box. Such a claim would also
need a validated production-roundoff bound over all those inputs. The current
scope supplies none. Similarly, eight certified rows do not supply a supremum
over all `N` rows.

**Tractable row computation and certificate boundary.** Compute selected rows
by transposing the complete finite algorithm, including initialization. For
`e_i` in the central output space, let

\[
v_i=F_T^TC^Te_i,\quad w_i=F_N^Te_i,\quad
b_i=U^Tv_i,\quad a_i=E^Tv_i-w_i.
\tag{6}
\]

Then `b_i` is row `i` of `B`, `d_i=a_i^T x`, and its gain is `||b_i||_1`.
A row can be streamed and discarded after its required identities, enclosures
and summaries are retained. This avoids storing a huge exact dense matrix or
filtering each of 8192 extension basis vectors separately. It does not promise
constant work or constant-size rational numerators.

For each stage, `S_m^T=O^T A^T R A^T R P^T`; reverse the stage order for the
complete adjoint. Unpadding transposes to zero insertion. Reversal is its own
transpose. Odd-extension adjoints add twice each padding adjoint to its endpoint
and subtract it from the corresponding reflected input coordinate, in addition
to the central adjoints. The transpose of a causal recurrence runs through its
dependencies in reverse order. Derivatives of all initial states through the
pass's first sample and the preceding DC gains must be accumulated as well.
Applying `F_m` again or only reversing the input is not this adjoint.

Use an independently implemented exact rational forward/basis construction on
small fixtures to verify the transpose. For admitted-length row certificates,
an exact rational implementation is allowed if it completes. A validated
enclosure implementation is the practical alternative, with initial outward
arithmetic precision fixed at 256 bits for the prospective pilot. Its endpoint
format, rounding, intermediate range and every error propagation inequality
must be independently reviewed before actual input use.

The prospective certificate uses high-precision point recurrences followed by
outward bounds on their local equation residuals. One exact state realization
for each admitted SOS is

\[
s_{k+1}=Hs_k+Jx_k,\quad y_k=c s_k+b_0x_k,\qquad
H=\begin{pmatrix}-a_1&1\\-a_2&0\end{pmatrix},\quad
J=\binom{b_1-a_1b_0}{b_2-a_2b_0},\quad c=(1,0).
\tag{7}
\]

Its constant-prehistory state is
`s_0=h*c_s`, where `h=(g-b0,b2-a2*g)^T` and `c_s` is that section's prescribed
input prehistory. Keep `p` for stage padding: the complete pass has length
`ell=m+2p`. For an output adjoint vector `v` of that length, the terminal state
adjoint is zero and the reverse recursion, for `k=ell-1,...,0`, is

\[
\lambda_\ell=0,\quad
\bar x_k=b_0v_k+J^T\lambda_{k+1},\quad
\lambda_k=c^Tv_k+H^T\lambda_{k+1}.
\tag{8}
\]

Additionally accumulate `h^T lambda_0` times the preceding DC-gain product
into the **original pass input's first coordinate**. Reverse the cascade's
sections and include each section's direct startup contribution; do not lose
it by treating initial states as independent constants. Equation (8) uses
`H^T`, not `H^(-1)`. The exact small-system tests below must reconcile this
state realization with the independently implemented recurrence (1).

Naive interval DFI replay is not an accepted certification argument. Absolute
state-transition powers can grow although the actual complex-pole system is
stable; repeated interval wrapping can destroy useful enclosures. Instead,
propagate the certified local residuals through enclosures of the **signed**
powers of `H` (and the transposed system), taking absolute bounds only after
forming the needed transfers. For input-error propagation retain the scalar
transfer `c H^k J` where applicable; a denominator-only bound may discard the
notch cancellation and become useless. Include direct input/output terms.

Before these numerical envelopes, verify the exact rational Jury inequalities
`|a2|<1`, `1+a1+a2>0`, `1-a1+a2>0` for every denominator. The initial block
search is fixed to `K=2^j`, `j=0,...,20`, at 256-bit outward precision. Choose
the first block with certified `||H^K||_infinity<1`, using outward repeated
squaring, and verify finite remainder-power bounds. Apply the corresponding
construction to the actual adjoint transition as well. This supplies a route
to bounded residual Green functions without iterating `|H|` per sample.
If no useful certificate is obtained within that declared search, report it;
do not assume contraction or raise precision after inspecting actual data.
A verified rational Lyapunov-norm scheme is an alternative only after its
own arithmetic/resource contract is reviewed before actual input use.

Include coefficient conversion, DC divisions, initialization, odd extension,
adjoints, reversals, unpadding, all stages and final absolute-value/summation
rounding in the residual argument. Finite precision alone is no proof of an
enclosure, and stability or block contraction alone is no final numerical
width guarantee. The actual admitted coefficients have not been subjected to
this new certificate construction in RI-55.

For certified intervals `b_ij in [l_j,u_j]`, sum the exact/outward lower and
upper bounds on `|b_ij|` to enclose the gain. A coefficient interval excluding
zero proves that row nonzero; intervals that all contain zero leave the result
unresolved unless a separate exact zero proof is available. Enclose `d_i` using
the certified `a_i` row and exact `x`, including cancellation. The upper endpoint
of `|d_i|+M||b_i||_1` is then a rigorous conservative version of the sharp exact
quantity. Do not label the enclosure endpoint an attained or sharp numerical
value. A rounded sign-vector witness is a diagnostic unless its claimed result
is itself verified with exact or enclosed arithmetic.

**Frozen prospective qualification.** These are future tests, not reported
passes. Preserve the existing RI-44 and RI-53 sources, pins and thresholds.
Normal and optimized interpreter modes must exercise explicit runtime checks,
with deterministic report equality; failures remain failures.

1. **Exact small systems.** Use central lengths `4,7`, side lengths `1,2`, and
   all eight stage configurations: identity `[1,0,0,1,0,0]` with padding 0;
   first-order `[1/2,0,0,1,-1/2,0]` with padding 1; biquad
   `[1/4,1/8,0,1,-1/2,1/8]` with padding 1; a single padding-1 stage containing
   those last two sections in that order; two successive stages containing
   those sections with padding 1 and 0 respectively; FIR
   `[1/2,1/2,0,1,0,0]` with padding 1; zero-DC section
   `[1/2,-1/2,0,1,-1/2,0]` with padding 1; and a padding-1 stage containing
   that zero-DC section followed by the biquad. These include nonunit and zero
   cascade DC gains, without dividing by a preceding gain. Construct every
   forward matrix column independently using exact fractions. Check every adjoint row,
   all injection/crop identities, and (4) exactly. Use `x_k=(k-2)/8`, and
   enumerate every corner of each extension box for `M=0,1/2,2`, checking (5)
   and its attaining witness exactly. The identity configuration verifies the
   zero-row exception. These tests have no floating tolerance.
2. **Complete admitted-length forward checks.** At both `m=N` and `m=T`, use
   seven vectors: zeros, ones, impulses at `0,floor(m/2),m-1`, alternating
   `(-1)^k`, and `((k mod 17)-8)/8`. Compare every production output with the
   unrounded independently authored Decimal-80 output. Require maximum absolute
   error `<=1e-9*max(1,maxabs(input))`, and exact zero output from both production
   and Decimal implementations for zero input.
   These binary-exact, unit-bounded inputs retain the RI-53 criterion and add
   coverage for the new longer context; they provide no rigorous row enclosure.
3. **Admitted adjoint diagnostics.** At lengths `N,T`, use those same seven
   forward vectors and output seeds `e_i` for `i in I` at length `N`, `e_(L+i)`
   for length `T`, plus the binary-exact dense seed `((-1)^k)/16384`. Check the
   transpose inner product against the independent Decimal-80 forward calculation.
   A numerical adjoint's discrepancy must be
   `<=1e-9*max(1,||seed||_1*||input||_infinity)`.
   Form both inner products and their difference as exact Fraction sums of the
   retained finite values: binary64 values convert through their exact integer
   ratios, and Decimal values through their exact decimal tuples or equivalent
   exact conversion. Compute the scale and threshold comparison exactly too.
   Do not introduce ambient Decimal-context or floating summation error, and
   add no dot-product tolerance. Report every residual. This complements the
   exact small-system proof; it does not convert rounded coefficients into
   exact certificates.
4. **Validated enclosure checks.** Independently check the enclosure method's
   arithmetic and stable-state error proof, and require it to contain every
   exact small-system matrix entry, gain and context term. At the admitted
   eight rows, require gain interval width `<=1e-12*max(1,gain_upper)`.
   For each of the seven length-`N` synthetic centers, require context-term
   interval width `<=1e-12*maxabs(center)`, with exactly `[0,0]` for zero center.
   If future actual `x` is admitted, use the same scale-relative width rule
   `<=1e-12*maxabs(x)` without a unit floor. An overly wide enclosure may remain
   mathematically valid, but it fails this pilot's usefulness gate. Failure,
   exhausted resources or an unproved error bound yields no qualified row
   certificate. The 256-bit setting and thresholds are not relaxed after
   inspecting the actual vector or desired result.

An additional structural check follows from the pinned bandpass sections with
exact numerator `[1,-2,1]`: a constant input, its odd extension and its constant
prehistory remain constant until a zero-DC section annihilates them exactly.
The remaining linear operations preserve zero. Thus the exact admitted operator
satisfies `F_m*1=0` for every admissible length, every exact row sums to zero,
and (4) gives `d+B*1=0` when the central vector is also all ones. The future
exact/validated implementation must check these identities: exact arithmetic
must return zero, and certified interval sums must contain zero. These are
structural identities and prospective checks, not a claim that the new actual
row computation has run. Rounded production or Decimal constant-input outputs
are subject to their numerical gate, not an additional exact-zero requirement.

The first implementation reservation should contain only the selected-row
engine, independently authored qualifier/oracle, a fixed-interface driver and
their guide. Freeze their exact source and arithmetic contract before running
the new admitted-coefficient calculations. Synthetic qualification comes before
reading an actual central export for sensitivity. A failed qualification may
motivate a separately reviewed revised design; it cannot be silently relabeled
as a successful bound.

**Later input, output and refusal contract.** Numerical comparisons retain the
admitted CPython 3.11.6 / NumPy 2.1.3 / SciPy 1.14.1 / h5py 3.12.1 runtime.
Exact/validated arithmetic must use its separately recorded and reviewed
implementation; this design installs no dependency. Bind all dependency source
bytes and the coefficient manifest before parsing or evaluation.

If actual central data are later authorized, consume the already accepted
[RI-53 export](../gwosc_nr_comparison_v1/REFERENCE.json), 1633767 bytes, SHA-256
`24c291c9f4f160fe3cb7ca75926ccbed2ba1fe1559f8badc130f3d14dc3e407d`.
Use its 2769 `input_hex` values unchanged; their little-endian binary64 array
SHA-256 is `e34926cba71051771bdea7a75f26ac207dc45c59a16c9142edacc0b154efc52f`.
Do not substitute the filtered array, a displayed subset, interpolated values
or a newly read waveform. This design has not opened that sample body.

A driver with no envelope should report only context terms, operator gains
and their explicit certification status. An optional scalar envelope must be
a caller-supplied nonnegative finite exact rational, with its assumption/source
label retained. Use canonical coprime numerator/positive-denominator strings,
each integer limited to 4096 bits; refuse malformed or out-of-domain values.
There is no default physical `M`, inferred peak multiplier or automatic
probabilistic interpretation. Hypothetical envelopes must be labeled as such.

Reports must bind source/input/coefficient identities, dimensions, row indices,
runtime/arithmetic precision, all qualification receipts and failures. For every
reported row retain coefficient-enclosure identity, gain and context intervals,
nonzero witness index and interval when proved, or explicit unresolved/zero
status; record `M` and the bound interval only when an envelope was supplied.
Rounded estimates and rigorous certificates need distinct fields/statuses.
Actual sample values and physical amplitudes never select pilot rows or gates.

Refuse changed bytes or coefficients, changed stage order/padding, wrong vector
length, nonfinite values, unrecognized arithmetic configuration, missing or
failed qualification, unsupported rows/context lengths, and invalid envelopes.
Controlled synthetic refusals must include each category, an enclosure missing
an exact toy value, an interval containing zero falsely asserted nonzero, and
an over-wide but valid interval presented as qualified. All must work under
`-O`. Computational enclosure failure is reported explicitly and produces no
qualified bound. Do not create partial accepted artifacts. Any later output
uses a new exclusive destination outside Git checkouts, refuses overwrite,
and retains actual commands/modes and failed-attempt receipts externally.

The finite context still has artificial outer endpoints and the same prescribed
odd-padding procedure. Nothing here bounds an infinite physical continuation,
selects a justified physical envelope, resolves the historical V1-to-V2 time
placement, supplies calibration uncertainty or compares DET with GR. It supplies
a precise conditional sensitivity question, an exact elementary answer in
terms of operator rows, and a prospective route to checking those rows.
