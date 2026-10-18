# One root-admitted administrative sidecars action; unchanged RI141 child monitor.
import hashlib, importlib.util, os, sys
from pathlib import Path
expected_environment = {'LC_ALL': 'C', 'MKL_NUM_THREADS': '1', 'NUMEXPR_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'PATH': '/usr/bin:/bin', 'TMPDIR': '/Volumes/AI_DATA/development/det-review-evidence/ri200-root-sidecars-ofv27lvp/tmp', 'TZ': 'UTC', 'VECLIB_MAXIMUM_THREADS': '1', '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'}
if dict(os.environ) != expected_environment: raise RuntimeError('RI170 exact copy environment')
if sys.executable != '/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9' or (sys.flags.isolated, sys.flags.dont_write_bytecode, sys.flags.optimize) != (1, 1, 0): raise RuntimeError('RI170 direct normal isolated vendor')
source_path = Path('/Volumes/AI_DATA/development/det-review-evidence/ri141-white-bootstrap-source-h58ls076/prepare.py')
if source_path.is_symlink() or source_path.resolve(strict=True) != source_path: raise RuntimeError('RI170 literal monitor source')
before = source_path.stat()
with source_path.open('rb') as stream: captured = stream.read(67108865)
state = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
if state(before) != state(source_path.stat()) or len(captured) != 45721 or hashlib.sha256(captured).hexdigest() != '8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe': raise RuntimeError('RI170 complete monitor capture')
module_name = 'ri200_whole_unchanged_ri141_sidecars_monitor'
if module_name in sys.modules: raise RuntimeError('RI170 fresh non-main monitor name')
spec = importlib.util.spec_from_file_location(module_name, source_path)
module = importlib.util.module_from_spec(spec)
exec(compile(captured, str(source_path), 'exec'), module.__dict__)
module.child_run(['/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9', '-I', '-B', '/Volumes/AI_DATA/development/det-review-evidence/ri160-white-fixture-custody-repair-ufok1zpo/adapter.py', '--admission', '/Volumes/AI_DATA/development/det-review-evidence/ri200-root-sidecars-ofv27lvp/ADMIT_SIDECARS.json'], Path('/Volumes/AI_DATA/development/det-review-evidence/ri200-root-sidecars-ofv27lvp/monitor'), 'SIDECARS', 180, expected_environment)
