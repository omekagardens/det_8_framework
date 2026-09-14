"""Run only this isolated experiment's focused tests, with no DET imports."""

import sys
import unittest
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
sys.path.insert(0, str(BUNDLE))


def main():
    suite = unittest.defaultTestLoader.discover(str(BUNDLE), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
