"""Observable acquisition records. No generator state or inferred state belongs here."""

import json
from dataclasses import dataclass

SETTINGS = ("X", "Y", "Z", "W")
SPLITS = ("training", "heldout", "sequential")
ERASURE_MODEL = "binary-read-then-erasure-v1"


class RecordError(ValueError):
    """A record or its declared acquisition contract is malformed."""


def _text(value, label):
    if type(value) is not str or not value or len(value) > 256:
        raise RecordError(f"{label} must be nonempty text of at most 256 characters")
    return value


def _keys(data, names):
    if type(data) is not dict or set(data) != set(names):
        raise RecordError("record fields do not match the version-1 schema")


@dataclass(frozen=True)
class Command:
    command_id: str
    precursor_id: str
    setting: str
    kind: str = "projective_measure"

    def __post_init__(self):
        _text(self.command_id, "command_id")
        _text(self.precursor_id, "command precursor_id")
        if self.command_id == self.precursor_id:
            raise RecordError("command identity cannot self-link")
        if self.setting not in SETTINGS or self.kind != "projective_measure":
            raise RecordError("unsupported actual command")

    def to_dict(self):
        return {
            "command_id": self.command_id,
            "precursor_id": self.precursor_id,
            "setting": self.setting,
            "kind": self.kind,
        }

    @classmethod
    def from_dict(cls, data):
        _keys(data, ("command_id", "precursor_id", "setting", "kind"))
        return cls(**data)


@dataclass(frozen=True)
class TrialRecord:
    record_id: str
    trial_id: str
    preparation_id: str
    recipe_id: str
    session_id: str
    split: str
    step: int
    precursor_id: str
    commands: tuple[Command, ...]
    setting: str
    frame_id: str
    calibration_id: str
    provenance: str
    acquisition_model: str
    preparation_status: str
    status: str
    measurement_occurred: bool
    outcome: int | None
    reason: str | None = None

    def __post_init__(self):
        for key in (
            "record_id",
            "trial_id",
            "preparation_id",
            "recipe_id",
            "session_id",
            "precursor_id",
            "frame_id",
            "calibration_id",
            "provenance",
            "acquisition_model",
        ):
            _text(getattr(self, key), key)
        if self.split not in SPLITS or self.setting not in SETTINGS:
            raise RecordError("unknown split or setting")
        if type(self.step) is not int or self.step < 0:
            raise RecordError("step must be a nonnegative integer")
        if type(self.commands) is not tuple or len(self.commands) != self.step + 1:
            raise RecordError("actual command prefix must end at this acquisition")
        previous = "prepare:" + self.preparation_id
        if self.record_id == previous or self.record_id == self.precursor_id:
            raise RecordError("record identity cannot reuse its preparation anchor or self-link")
        seen = {previous}
        for command in self.commands:
            if type(command) is not Command or command.precursor_id != previous:
                raise RecordError("broken actual command precursor chain")
            if command.command_id in seen:
                raise RecordError("duplicate command identity")
            seen.add(command.command_id)
            previous = command.command_id
        if self.commands[-1].setting != self.setting:
            raise RecordError("record setting differs from actual last command")
        if self.step == 0 and self.precursor_id != "prepare:" + self.preparation_id:
            raise RecordError("first acquisition must retain preparation precursor")
        if self.preparation_status not in ("successful", "failed", "unknown"):
            raise RecordError("unknown preparation status")
        if type(self.measurement_occurred) is not bool:
            raise RecordError("measurement_occurred must be Boolean")
        if self.status == "detected":
            if (
                not self.measurement_occurred
                or type(self.outcome) is not int
                or self.outcome not in (-1, 1)
                or self.reason is not None
            ):
                raise RecordError("detected record needs an actual binary outcome")
        elif self.status == "missing":
            if (
                not self.measurement_occurred
                or self.outcome is not None
                or self.reason != "outcome_erased"
            ):
                raise RecordError("missing means a binary read occurred then was erased")
        elif self.status == "failed":
            if self.outcome is not None:
                raise RecordError("failure without a forward law cannot invent an outcome")
            _text(self.reason, "failure reason")
        else:
            raise RecordError("unknown acquisition status")

    def to_dict(self):
        result = {name: getattr(self, name) for name in self.__dataclass_fields__}
        result["commands"] = [command.to_dict() for command in self.commands]
        return {"schema_version": 1, **result}

    @classmethod
    def from_dict(cls, data):
        _keys(data, ("schema_version", *cls.__dataclass_fields__))
        if type(data["schema_version"]) is not int or data["schema_version"] != 1:
            raise RecordError("unsupported schema_version")
        values = dict(data)
        del values["schema_version"]
        if type(values["commands"]) is not list:
            raise RecordError("commands must be an ordered JSON array")
        values["commands"] = tuple(Command.from_dict(c) for c in values["commands"])
        return cls(**values)


def canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False)


def decode_record(line):
    def unique_pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise RecordError("duplicate JSON key")
            result[key] = value
        return result

    try:
        data = json.loads(
            line,
            object_pairs_hook=unique_pairs,
            parse_constant=lambda x: (_ for _ in ()).throw(RecordError("nonfinite JSON value")),
        )
    except (json.JSONDecodeError, TypeError) as error:
        raise RecordError("invalid record JSON") from error
    return TrialRecord.from_dict(data)


def fresh_identity(session_id, recipe_id, split, setting, index):
    """The frozen schedule, not surviving detections, fixes every attempt ID."""
    if split not in ("training", "heldout") or setting not in SETTINGS:
        raise RecordError("unsupported fresh schedule")
    if type(index) is not int or index < 0:
        raise RecordError("invalid scheduled index")
    stem = f"{session_id}/{recipe_id}/{split}/{setting}/{index:06d}"
    return stem, "prep:" + stem, "record:" + stem


def validate_sequence(records):
    """Validate a retained actual serial prefix; never manufacture missing steps."""
    if type(records) is not tuple or not records:
        raise RecordError("sequence requires a nonempty tuple of records")
    first = records[0]
    seen = set()
    for step, record in enumerate(records):
        if type(record) is not TrialRecord or record.record_id in seen:
            raise RecordError("invalid or duplicate sequence record")
        seen.add(record.record_id)
        for key in (
            "trial_id",
            "preparation_id",
            "recipe_id",
            "session_id",
            "frame_id",
            "calibration_id",
            "provenance",
            "acquisition_model",
            "preparation_status",
        ):
            if getattr(record, key) != getattr(first, key):
                raise RecordError("sequence changes its source/context")
        if record.split != "sequential" or record.step != step:
            raise RecordError("not a contiguous sequential prefix")
        if step:
            previous = records[step - 1]
            if record.precursor_id != previous.record_id:
                raise RecordError("broken record precursor chain")
            if record.commands[:-1] != previous.commands:
                raise RecordError("actual command history changed")
            if previous.status != "detected":
                raise RecordError("serial continuation after unresolved outcome")
    return records
