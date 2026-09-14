# One exact local-to-joint adapter

13 September 2026. RI-15 coordinator integration contract. Current review,
acceptance and launcher source identity belong to the
[coordinator progress record](../../coordination/REVIEW_PROGRESS.md).

This bridge connects the accepted
[RI-08c local record instrument](../t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md)
to the accepted
[RI-08d joint interface](../t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md).
It implements one conditional composition arrow in the
[operational premise ledger](../../coordination/OPERATIONAL_PREMISE_LEDGER.md).
It supplies representation conversion and retained context, without copying
either model implementation or adding a physical operation.

## 1. Scope and source types

The input is the exact RI-08c `State` class loaded from its reviewed model,
containing a normalized full four-label kernel in C, complete local records,
pending actual control word, local controller, source kind and frame. The
reference is a separately supplied exact RI-08d `ReferenceState`, including
its normalized kernel, polarization t, fixed Z orientation, origin and complete
reference records. An explicit RI-08d `Independence` declaration must name the
two distinct input origins. The joint origin must be distinct from both.

The adapter additionally requires named reference provenance. These immutable
key/value pairs record the caller's declaration; neither names nor matrix
factorization certify empirical independence or preparation availability.
No reference-preparation event is invented when the supplied history is empty.

Both accepted `G` classes hold exact real and imaginary `Fraction` components,
but they are different Python types. The adapter constructs each joint-model
entry as `joint_source.G(value.real, value.imag)`. It transfers every entry of
the current full kernel. It never converts through `Phi` and `J2`, discards c,
casts through float, reapplies a pending control or infers an earlier kernel.

The output remains in the separate research interface. This is not a supported
core/RET API, a physical state-conversion device, a global reconstruction or a
general composite calculus. RI-08f's same-image return instrument is outside
this bridge. Old terminal cuts are not converted to reusable states.

## 2. The metadata mismatch and its preservation

RI-08d `LocalState` has only `residual`, `origin` and `records`; its `InputRecord`
does not have RI-08c's explicit axis, controller, source-kind or frame fields.
The exact committed-record mapping is:

| RI-08c field | RI-08d representation |
|---|---|
| `event_id`, `action`, `settings`, `precursor` | Retained with their original values and ordering |
| Integer `outcome` | Canonical string `"0"` or `"1"` |
| `axis` | Payload pair `("ri08c.axis", value)` |
| `controller` | Payload pair `("ri08c.controller", value)` |
| `source_kind` | Payload pair `("ri08c.source_kind", value)` |
| `frame` | Payload pair `("ri08c.frame", value)` |

Those four payload pairs have the stated order. No existing local record is
removed or replaced by an aggregate. Local IDs remain local; the accepted
joint record tags every local/reference predecessor with its origin. The
order used to list the two prefixes does not add a causal ordering between
the independently supplied inputs.

Current pending settings belong to the source snapshot, not to a newly
committed record. A frozen `BridgeContext` therefore retains the exact original
RI-08c `State` object, its deterministic RI-08d `LocalState` conversion, the
reference, independence declaration, three origins and reference provenance.
Every prospective, valid-source and terminal wrapper carries that context.
This also preserves the local frame/controller/source kind and nonempty pending
word when there are no earlier records in which to store them.

Extracting a bare legacy `LocalState` or terminal record from its wrapper gives
only that legacy type's fields. The complete bridge contract requires retaining
the wrapper. It does not claim those older classes gained new fields.

Snapshot constructors check exact cone membership and the supplied record
grammar. They do not prove reachability from an initial preparation or that a
hand-supplied pending word was historically applied. Forward local calls and
their returned probabilities must be retained separately for such a replay.

## 3. Small exact API and forward validation

The [adapter](adapter.py) imports only the fixed aliases `local_source` and
`joint_source`, plus standard-library dataclasses. Those aliases are bound by
the launcher described below; direct unbound imports are not a supported path.

```python
prospective = adapter.prepare(
    local_state,
    reference_state,
    independence,
    local_origin="signal",
    joint_origin="joint-read",
    reference_provenance=(
        ("preparation_id", "declared-reference-A"),
        ("independence_basis", "supplied independent preparation premise"),
    ),
)
product_source = adapter.promote(prospective)
coupled_prospective = adapter.couple(product_source)
coupled_source = adapter.promote(coupled_prospective)
conditional_probability, terminal = adapter.commit(coupled_source, (0, 0))
```

`convert_local_state(state, origin=...)` performs only the lossless numerical
and committed-record conversion. Its bare result must stay with the original
source context when used in a bridge. `prepare` accepts only the bound local
`State`, not a terminal or lookalike class, and requires the separate reference
and independence objects. It returns `ProspectiveJoint(context, target)`.

`promote` delegates exact source validation to RI-08d and returns `JointSource`.
Here promotion means accepting a mathematical input type; it is not scientific
claim promotion. `couple` accepts only a validated product source and delegates
the single supplied shared coupler to RI-08d. A second coupling is refused.
`commit` accepts a validated source and returns its conditional `Fraction`
weight and `JointTerminal`. The accepted model also permits a terminal cut of
the validated product source without the shared coupling; the chosen stage
and coupler remain explicit in the target record.

Each wrapper verifies more than separate constructor validity: its target
must equal the actual accepted forward construction from its retained context.
The product is the accepted regrouped tensor of the complete input kernels;
the coupled target is the accepted single shared congruence of that product.
A hand-constructed target with another residual, reference, input prefix,
origin, permutation or coupler cannot claim the retained context. Terminal
validation reconstructs the actual source cut and complete matching record.
All numerical operations are delegated to the accepted model functions.

The bridge initially retains all of C, including complex nonzero c. For a
polarized reference, the shared prospective kernel can be PSD with mass one
while its cross-cell forms contain nonzero `t*c`. `promote` then refuses it.
The prospective wrapper remains inspectable; there is no c=0 projection or
normalization repair. At t=0 the accepted interface can admit nonzero c; the
adapter does not silently apply RI-08f's smaller-domain restriction.

## 4. Conditional probabilities and terminal outputs

For a validated normalized joint source K and declared cell alpha, the accepted
operation gives the complete raw cut `E_alpha K E_alpha` and its total-entry
weight p. Only p>0 permits normalization, commitment and a `JointTerminal`.
That wrapper retains the original local context, the complete joint source,
the actual full 16-label normalized cut and its complete joint record.
Its `conditional_probability` property equals the p returned by `commit`.

A zero-weight raw cut can be nonzero. The bridge refuses selection rather than
inventing a normalized state or an appended event. Its terminal wrapper has
no reset or continuation method, and the other bridge operations reject it.

All returned weights are **conditional on the supplied normalized local and
reference snapshots**. RI-08c `State` does not contain an initial preparation,
prior branch probabilities or a cumulative local-history weight. Reference
provenance is not a numerical selection model. The bridge neither reconstructs
those missing probabilities from records nor interprets a selected reference
as an unconditional resource. Reporting a full protocol probability would
require the actual earlier local/reference selection weights and their replay
contract. That successor is not implemented here.

## 5. Separate fixed-alias source contract

The [coordinator launcher](../../../scripts/run_qr_local_joint_adapter.py) uses
an explicit four-entry source table:

| Alias | Exact executable source |
|---|---|
| `local_source` | Original RI-08c `model.py` |
| `joint_source` | Original RI-08d `model.py` |
| `adapter` | This bundle's `adapter.py` |
| `check` | This bundle's independent `check.py` |

The two original files both have basename `model.py`; unique aliases prevent
their classes from colliding. Their bytes are neither copied to new source
files nor rewritten. The fixed old-model, old-statement and new adapter/check/
contract SHA-256 pins are embedded in the launcher after independent source
review. It verifies the existing research runner against its fixed reviewed
SHA before executing that helper's captured bytes. The launcher hash is recorded
in coordinator acceptance, avoiding a circular hash inside this contract.

The existing [research runner](../../../scripts/run_research_checks.py) only
registers sibling imports. This adapter is deliberately a **separate coordinator
contract**, not a new registry entry or an implicit extension of `--all`.
Its launcher reuses that runner's pin/path checks, static import-closure audit,
captured-source child loader, side-effect audit hook and endpoint drift checks.
For closure inspection alone, the four aliases form virtual sibling filenames
in memory. An explicit one-to-one mapping connects each alias to its actual
canonical source path. Execution and reported loaded-source identities use
those real paths, not the virtual names. No temporary alias files are created.

All four files must belong to the closed declared import graph and actually
execute. Missing, duplicated or changed aliases, forbidden imports, mismatched
pins, invalid paths, failed/empty/skipped checks, omitted executable sources
and observed source drift prevent success. Two original statement documents,
this contract, all four executables, the runner and launcher participate in
before/after source checks. Standard-library dependencies are identified by
the Python runtime rather than individually frozen. This is reviewed-source
execution, not a hostile-code sandbox or a proof against transient mutations
restored before the final byte comparison.

The launcher reports aliases, canonical paths, source pins, Python/platform
identity, runner and launcher hashes, execution results and observed drift.
New pins require review; a mismatch is never repaired automatically. There is
no CLI root/source override, arbitrary directory discovery or package import
through the supported core. Programmatic root arguments exist for independent
temporary-layout regression fixtures, with the same fixed source contract.

## 6. Reproduction and independent checks

Inventory and pin/closure verification are the default; they do not execute
the adapter or witnesses. Explicit execution is required:

```sh
.venv/bin/python -B scripts/run_qr_local_joint_adapter.py
.venv/bin/python -B scripts/run_qr_local_joint_adapter.py --run
.venv/bin/python -B scripts/run_qr_local_joint_adapter.py --run --optimized
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -p no:cacheprovider \
  det8/tests/test_qr_local_joint_adapter.py
```

The isolated child always uses `-I -S -B`, adding `-O` for the optimized run.
Normal launcher execution writes no evidence files, temporary modules or Python
caches. The regression tests may create their own temporary pytest fixtures;
they do not change the accepted sources or source pins.

The independent [witness checks](check.py) exercise exact complex conversion,
complete records and empty-prefix pending metadata, native tensor/cut oracles,
conditional weights, origin/provenance mismatch refusal, the complex-c viability
obstruction, unpolarized references and zero-weight terminal refusal. The
[launcher regressions](../../../det8/tests/test_qr_local_joint_adapter.py) examine
the source/alias contract and execution failures. Finite checks support this
bounded software interface; the conditional mathematics and physical premise
boundaries remain in the accepted source statements.
