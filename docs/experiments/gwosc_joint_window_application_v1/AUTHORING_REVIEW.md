# RI-123 authoring record and scope

This is the design author's own check, not independent acceptance. The parent
coordinator must obtain independent proof review before source implementation.
The author previously reviewed the RI-118/119/121 predecessors; that earlier
independence does not transfer to this new proposal.

The complete proposed DESIGN was read after drafting. The following reductions
were checked symbolically, without evaluating any actual retained coefficient,
PSD-weighted sum or observed statistic:

1. Adjacent first-T windows share exactly coordinates d through T-1 of the
   earlier window and 0 through T-d-1 of the later. Both strips miss the embedded
   short filter support, giving directed C=U H^T using long rows alone.
2. With only adjacent blocks nonzero, the complete centering sum contains n
   diagonal blocks and n-1 of each directed block. This gives a=(n-1)/n and
   b=(n-1)/n^2, rather than an independent-window correction.
3. For v, the two disjoint strip energies are bounded by ||A^T v||^2. Applying
   twice the arithmetic-geometric inequality to their inner product proves
   -Omega <= C+C^T <= Omega and |tr(C)| <= tr(Omega)/2.
4. The interval product error has all three terms, including radius times
   radius. The nonsymmetric directed matrix is retained before any C+C^T sum.
   A four-endpoint product sum and midpoint polarization give distinct checks.
5. The accepted relative Gram enclosure and inverse-norm upper bound imply
   Omega >= (1-rho) I/gamma. Combined with the structural white lower factor,
   this gives the positive ell_n used in the new prospective relative gate.
   This is a sufficient usefulness certificate, not necessary invertibility.
6. A half-period shift has phase (-1)^k, including conjugate partners. Repeated
   even/odd outputs yield pq/n^2 times the squared difference. Its zero-mean
   expectation is 4pq/n^2 times the odd-frequency marginal contribution.
7. The retained spectral centers/errors already contain the conjugate-pair
   weights. PSD factors must be applied once; no extra doubling is introduced.
   The RI100 RESULT lacks PSD values, so admitting RI96's complete source records
   is an essential additional input, not an optional inference from trace.
8. Splitting raw mode terms by parity preserves exact additive identities.
   Subtracting marginal/cross interval boxes loses dependence; it is only a
   deliberately wider oracle route. Negative interval lower endpoints stay.
9. For PSD-weighted errors, both parity contributions are nonnegative, so the
   proposed centered width is at most the stated factor times the raw width.
   This numerical fact says nothing about physical covariance/model error.
10. Trace duality with the PSD matrix D^T Pi D/n gives the eta*kappa covariance
    perturbation bound. Expanding the calibrated factor Frobenius square gives
    the separate 2||Y0||||YDelta||+||YDelta||^2 bound. Neither supplies eta,
    calibration, a mean bound or independence from the actual observed data.
11. The M=4, T=3, d=2 toy follows directly from B=(1,0,-1,0): its periodic
    half-shift is -B, t=2 and h=-2; the shared-white adjacent C=-1 instead.
    Thus the stated values 2, 3/2 and 16/9 follow by the displayed formulas.
    This is a manual toy identity check, not execution of sign enumeration.

The dimension arithmetic and exact file identities in PREDECESSOR_PINS were
checked with reviewer-owned metadata operations. The full 51,891,508-byte RI73
capture was opaque-hashed and matched its historical pin; it was not parsed.
Selected previously accepted result bodies were parsed only to inspect schema,
key locations and counts, without extracting numeric coefficients into a new
calculation. The relevant operator and spectral source routines were read as
text. No target was imported, compiled, probed, executed or rewritten.

The first metadata manifest assembly stopped because it guessed the predecessor
validator basename as `validator.py`; the actual immutable file is `validate.py`.
No manifest was written by that stopped operation. The corrected assembly read
the real path and wrote the final 45-record manifest. A prior result-schema query
encountered an integer where it expected an iterable, then used the actual schema;
neither metadata error executed or changed a scientific target. These do not
constitute qualification failures or new scientific trials.

The design intentionally has no computed real-operator C, kappa, parity sum,
new prediction, hypothesis selection or empirical acceptance threshold. Its new
eps<=10^-12 gate is prospective and separate from inherited gates. The saved
ordinary spectra support a coherent hypothetical periodic completion only;
they cannot identify the real cross-window law. The full physical mean,
calibration and model discrepancy prerequisites remain open.

No repository file, existing source/capture/result, Git state, runtime, active
admission or protected material was changed. This directory is source-only
authoring evidence. All actual runtime/source/input qualification and scientific
execution remain future coordinator-owned actions.
