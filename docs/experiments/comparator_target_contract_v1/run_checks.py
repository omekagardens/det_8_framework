"""Run only the four-file comparator target contract's independent tests."""

import sys
import unittest
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
sys.path.insert(0, str(BUNDLE))


def main():
    tests = unittest.defaultTestLoader.discover(str(BUNDLE), pattern="test_contract.py")
    if tests.countTestCases() == 0:
        raise RuntimeError("no comparator contract checks collected")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.skipped or result.expectedFailures or result.unexpectedSuccesses:
        return 1
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
