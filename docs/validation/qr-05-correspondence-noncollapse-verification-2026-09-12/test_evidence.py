"""Bounded evidence-integrity tests; tampering is confined to disposable copies."""

import copy
import os
import signal
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

import study


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.freeze_bytes, cls.freeze, cls.blobs = study.authenticated_sources()
        cls.capture_bytes = study.read_regular(study.ROOT / "results.json", study.ARTIFACT_LIMIT)
        cls.capture = study.validate_capture(cls.capture_bytes)

    def clone(self, directory):
        root = Path(directory) / "verification"
        root.mkdir()
        for name, data in self.blobs.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (root / "source-freeze.json").write_bytes(self.freeze_bytes)
        (root / "results.json").write_bytes(self.capture_bytes)
        return root

    def test_01_nine_source_bindings(self):
        self.assertEqual(len(self.blobs), 9)
        self.assertEqual(set(self.blobs), set(study.SOURCE_PATHS))
        self.assertTrue(study.exact_equal(study.inventory(self.blobs), self.freeze["sources"]))
        self.assertEqual(self.capture["freeze_sha256"], study.sha(self.freeze_bytes))
        self.assertTrue(study.exact_equal(self.capture["sources"], self.freeze["sources"]))

    def test_02_canonical_capture_and_size(self):
        self.assertEqual(study.canonical(self.capture), self.capture_bytes)
        self.assertLess(len(self.capture_bytes), study.ARTIFACT_LIMIT)
        self.assertTrue(all(len(blob) <= study.SOURCE_LIMIT for blob in self.blobs.values()))
        self.assertEqual(self.capture["report"]["schema"], study.REPORT_SCHEMA)

    def test_03_native_type_distinctions(self):
        self.assertFalse(study.exact_equal(True, 1))
        self.assertFalse(study.exact_equal(Fraction(1), 1))
        self.assertFalse(study.exact_equal({"x": [True]}, {"x": [1]}))
        self.assertEqual(study.native_json([Fraction(1), 1, True]), [{"fraction": [1, 1]}, 1, True])
        for bad in (1.0, (1,), {1: 2}, object()):
            with self.subTest(type=type(bad)), self.assertRaises(TypeError):
                study.native_json(bad)

    def test_04_noncanonical_duplicate_and_nonfinite_json(self):
        for data in (
            b'{"a":1,"a":2}\n',
            b'{"a":1.0}\n',
            b'{"a":NaN}\n',
            b'{"a":Infinity}\n',
            b'{"a": 1}\n',
            b'{"a":1}',
            b"\xef\xbb\xbf{}\n",
            b"\xff\n",
        ):
            with self.subTest(data=data), self.assertRaises(ValueError):
                study.parse_canonical(data)

    def test_05_changed_source_rejected_before_loading(self):
        with tempfile.TemporaryDirectory(prefix="qr05-cnv-source-") as tmp:
            root = self.clone(tmp)
            path = root / "primary.py"
            path.write_bytes(self.blobs["primary.py"] + b"\n# negative control\n")
            with (
                mock.patch.object(study, "_module", side_effect=AssertionError("must not load")),
                self.assertRaises(ValueError),
            ):
                study.load_engines(root)

    def test_06_symlink_and_oversize_source_rejected(self):
        with tempfile.TemporaryDirectory(prefix="qr05-cnv-file-") as tmp:
            root = self.clone(tmp)
            path = root / "primary.py"
            path.unlink()
            path.symlink_to(root / "reference.py")
            with self.assertRaises(ValueError):
                study.authenticated_sources(root)
            path.unlink()
            path.write_bytes(b"x" * (study.SOURCE_LIMIT + 1))
            with self.assertRaises(ValueError):
                study.authenticated_sources(root)

    def test_07_malformed_freeze_and_typed_binding_rejected(self):
        variants = []
        bad = copy.deepcopy(self.freeze)
        bad["schema"] = "unknown"
        variants.append(bad)
        bad = copy.deepcopy(self.freeze)
        bad["sources"]["primary.py"]["bytes"] = True
        variants.append(bad)
        bad = copy.deepcopy(self.freeze)
        bad["runtime"]["optimization"] = False
        variants.append(bad)
        for value in variants:
            with tempfile.TemporaryDirectory(prefix="qr05-cnv-freeze-") as tmp:
                root = self.clone(tmp)
                (root / "source-freeze.json").write_bytes(study.canonical(value))
                with self.assertRaises(ValueError):
                    study.authenticated_sources(root)

    def test_08_capture_binding_and_schema_rejections(self):
        for key, value in (
            ("schema", "unknown"),
            ("freeze_sha256", "0" * 64),
            ("sources", {}),
            ("extra", True),
        ):
            bad = copy.deepcopy(self.capture)
            bad[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                study.validate_capture(study.canonical(bad))
        bad = copy.deepcopy(self.capture)
        bad["report"]["schema"] = "unknown"
        with self.assertRaises(ValueError):
            study.validate_capture(study.canonical(bad))

    def test_09_capture_is_write_once(self):
        with tempfile.TemporaryDirectory(prefix="qr05-cnv-write-") as tmp:
            path = Path(tmp) / "artifact.json"
            original = b"{}\n"
            study.write_new(path, original)
            with self.assertRaises(FileExistsError):
                study.write_new(path, b"[]\n")
            self.assertEqual(path.read_bytes(), original)
        with tempfile.TemporaryDirectory(prefix="qr05-cnv-existing-") as tmp:
            root = self.clone(tmp)
            with (
                mock.patch.object(
                    study, "_build_report", side_effect=AssertionError("must not run")
                ),
                self.assertRaises(FileExistsError),
            ):
                study.capture(root)

    def test_10_artifact_byte_caps(self):
        huge = b"x" * (study.ARTIFACT_LIMIT + 1)
        with self.assertRaises(ValueError):
            study.parse_canonical(huge)
        with tempfile.TemporaryDirectory(prefix="qr05-cnv-limit-") as tmp:
            path = Path(tmp) / "artifact.json"
            with self.assertRaises(ValueError):
                study.write_new(path, huge)
            self.assertFalse(path.exists())

    def test_11_alarm_and_elapsed_caps(self):
        for invalid in (True, 0, -1, 1.5):
            with (
                self.subTest(invalid=invalid),
                self.assertRaises(ValueError),
                study.deadline(invalid),
            ):
                pass
        with self.assertRaises(TimeoutError), study.deadline(1):
            os.kill(os.getpid(), signal.SIGALRM)
        with (
            mock.patch.object(study.time, "monotonic", side_effect=[0, 2, 2]),
            self.assertRaises(TimeoutError),
            study.deadline(1),
        ):
            pass

    def test_12_full_native_report_matches_saved_capture(self):
        actual = study.native_json(study.build_report())
        self.assertTrue(study.exact_equal(actual, self.capture["report"]))
        altered = copy.deepcopy(actual)
        cell = altered["comparison_rows"][0]["result"]["relations"][0]["raw"]["errors"][0][0]
        self.assertEqual(cell, {"fraction": [0, 1]})
        altered["comparison_rows"][0]["result"]["relations"][0]["raw"]["errors"][0][0] = 0
        self.assertFalse(study.exact_equal(actual, altered))

    def test_13_route_mismatch_rejected_type_strictly(self):
        a = types_like(True)
        b = types_like(1)
        with self.assertRaises(ValueError):
            study._both((a, b), "value")

        class Mutator:
            def value(self, values):
                values[0] = 2
                return {"value": 2}

        original = [1]
        with self.assertRaises(ValueError):
            study._both((Mutator(), Mutator()), "value", original)
        self.assertEqual(original, [1])

    def test_14_original_evidence_unchanged(self):
        self.assertEqual(
            study.read_regular(study.ROOT / "results.json", study.ARTIFACT_LIMIT),
            self.capture_bytes,
        )
        self.assertEqual(study.authenticated_sources()[0], self.freeze_bytes)

    def test_15_malformed_rational_tags_rejected(self):
        for tag in (
            {"fraction": [1, 0]},
            {"fraction": [True, 1]},
            {"fraction": [2, 2]},
            {"fraction": [0, -1]},
            {"fraction": [0]},
            {"fraction": [1, 1], "extra": 0},
        ):
            bad = copy.deepcopy(self.capture)
            bad["report"]["comparison_rows"][0]["result"]["raw_distance"] = tag
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                study.validate_capture(study.canonical(bad))

    def test_16_snapshot_change_rejected_before_execution(self):
        with (
            mock.patch.object(study, "_module", side_effect=AssertionError("must not load")),
            self.assertRaises(ValueError),
        ):
            study._build_report(study.ROOT, b"different freeze\n")
        with self.assertRaises(ValueError):
            study.validate_capture(self.capture_bytes, expected_freeze=b"different freeze\n")

    def test_17_publication_readback_and_existing_capture_guard(self):
        # This is an evidence I/O control, not an additional mathematical study.
        with tempfile.TemporaryDirectory(prefix="qr05-cnv-readback-") as tmp:
            root = self.clone(tmp)
            with self.assertRaises(FileExistsError):
                study.create_freeze(root)
            (root / "results.json").unlink()
            original_write = study.write_new

            def corrupted_write(path, data):
                original_write(path, data + b" ")

            stub = {
                "schema": study.REPORT_SCHEMA,
                "comparison_rows": [],
                "closure_rows": [],
                "controls": {},
                "census": {},
            }
            with (
                mock.patch.object(study, "_build_report", return_value=stub),
                mock.patch.object(study, "write_new", side_effect=corrupted_write),
                self.assertRaisesRegex(ValueError, "readback"),
            ):
                study.capture(root)


class types_like:
    def __init__(self, value):
        self.stored = value

    def value(self):
        return {"value": self.stored}


if __name__ == "__main__":
    with study.deadline(study.SUITE_SECONDS):
        unittest.main()
