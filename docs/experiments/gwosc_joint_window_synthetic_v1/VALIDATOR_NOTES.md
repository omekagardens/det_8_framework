# RI119 separately authored validator — source-only handoff

The distinct validator author implemented `validator.py` after reading the
fixed `CONTRACT.md` and the accepted RI118 design, root adjudication and
independent proof review. The author did not read `primary.py` before finishing
this implementation, and has not read it as of this handoff. No target import,
compilation, AST inspection, probe, sign enumeration, fixture execution,
simulation, empirical read or scientific-output construction was performed.
Only source writing, complete source text inspection and file metadata hashing
were used. No repository, index, git, freeze or admission operation occurred.

## Independent construction

The nine expected case records are reconstructed from the contract's literal
tiny input definitions, using local standard-library `Fraction` matrix
operations. The validator imports neither the primary nor any project module,
and has no data loader, CLI, subprocess or import-time I/O. Its declarations
and formulas are prospective source, not executed evidence.

For each case it independently constructs every M and T selector, the full
unscaled stacked map D, the base factor F and mean mu, and the separately
scaled raw mean and factor. Covariances come from projected factors, so all
raw and within-window matrices, the complete stacked covariance, both directed
cross blocks, finite-mean covariance and centered covariance average are
retained entrywise. The mean term is formed by centering D mu explicitly.
The expected V route is the centered factor's squared Frobenius norm plus mean
dispersion, divided by n. A distinct second-moment identity, E[U] minus the
finite output mean's expected squared energy, reconstructs direct_average_V.
Their equality and the centered-average trace identity are deliberate checks.
Neither construction enumerates the primary's sign cubes or uses a supplied
scientific oracle.

Q09 keeps both output coordinates and the complete oriented cross blocks.
Q10 and periodic Q03 require no inverse or eigenvalue tolerance. Sign counts
are the declared exact support cardinalities, computed from fixed latent
dimensions, not evidence that any support was enumerated by this validator.

The three Q12 records are reconstructed from their dimensioned factors.
The covariance discrepancy bound is eta times the centered map's squared
Frobenius norm divided by n. For the fixed calibration-error toy the baseline
and perturbation factors are identical; their Frobenius norm product equals
the squared norm exactly. This equality is checked before using it, avoiding
floating square roots and without pretending it covers arbitrary factors.

## Guard correspondence

The public `validate_result`, `parse_result`, `canonical` and
`ValidationError.code` follow the fixed contract. Full saved result equality
is required; no subset, scalar-trace-only or tolerance comparison is used.
The public PSD guard accepts only a 2 by 2 list of canonical rational strings.
It is called on supplied Q02/Q03 stacked covariances before case comparisons;
its exact symmetry, diagonal and determinant checks accept singular PSD cases.

The coordinator clarified the following otherwise ambiguous type/refusal
boundaries before this source was finalized:

- Missing or extra case, model or bound keys: SCHEMA.
- Wrong plain-integer type (including bool) or list shape: DIMENSION.
- Fixed model dimension values M/T/stride/n/raw_length/latent_dimension and
  output_dimension, and fixed bound n/output_dimension: DIMENSION.
- Incorrect plain integer starts: MODEL; incorrect selector integer values:
  SHARED_INDEX or CROP; incorrect sign_count integer: ENUMERATION.
- Wrong PSD shape: DIMENSION; wrong scalar types/canonical strings: EXACT;
  resource bounds: RESOURCE; symmetry or semidefiniteness failure: PSD.

Rationals are reduced decimal strings. A character bound and 2467-digit
component bound precede regex and integer parsing; parsed components and every
computed reduced rational are bounded to 8192 bits. Serialized bodies are
limited to 2 MiB. Fixed scientific dimensions are at most raw length 8,
output dimension 2, three windows and latent dimension 8. This is arithmetic
and interface source discipline; it is not a measured runtime fit or OS
allocation guarantee. Later caller review must supply actual resource,
source/runtime identity, admission and serial normal/optimized custody.

`parse_result` refuses duplicates, nonfinite JSON and noncanonical whole bytes.
Canonical serialization does not silently normalize rational strings; those
are checked in the comparator. Type-sensitive equality prevents Python's
bool/integer equivalence from passing a structural or scientific field.
No assert is used as an acceptance check.

After the coordinator's complete source read, two source-only protocol
harmonizations were applied. Every expected string position requires a plain
string first (EXACT), including nonnumeric labels; canonical numeric strings
then pass through the rational parser. The complete typed-shape pass covers
all cases and bounds before any dimension-value comparison. During the
subsequent scientific pass each case's fixed dimension values precede its
PSD and field comparisons, and each bound's dimension values precede its
CALIBRATION/BOUND comparisons. This records first-refusal order; it is not
an executed qualification or cross-implementation result. The validator
author still has not read primary.py or run any target source.

## Remaining boundary

The complete source and its scientific logic require independent source review
and root adjudication. The twelve synthetic groups and later exact refusal
inventory remain unexecuted. This handoff gives no empirical covariance,
calibration envelope, protected validation, actual coefficient contraction,
physical noise model, native forward prediction or RET authorization.

## Final separate-review resource clarification

The separate complete source reviewer identified one general resource-path
asymmetry: the PSD determinant initially bounded only the reduced difference
a*c-b*b, allowing oversized products to cancel. The parent made the one-line
change to bound both products separately before the difference, preserving the
short-circuit nonsymmetric/negative-diagonal refusal. This is a resource-guard
clarification; scientific fixed-model algebra remains independently authored.
The parent also aligned primary scalar component-length checks before regex
with this validator. The reviewer inspects both changes as text before handoff.
No target execution occurred, and earlier hashes above are historical source
states; final SOURCE_PINS.json records the stable bytes.
