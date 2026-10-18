"""Root metadata driver for exactly one admitted profile observation."""
import sys
import time
import subprocess
from pathlib import Path
import importlib.util

D = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('metadata', D/'metadata.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
mode = sys.argv[1]
if mode not in ('normal','optimized'):
    raise ValueError('mode')
card = m.load(D/'PROFILE_ADMISSION.json')
if card['status'] != 'AUTHORIZE_INSTALLED_RUNTIME_OBSERVATION_ONLY':
    raise ValueError('admission status')
for r in card['dependencies']:
    m.verify(r['path'],r)
run = card['runs'][mode]
stdout = D/('PROFILE_'+mode.upper()+'.json')
stderr = D/('PROFILE_'+mode.upper()+'.stderr')
attempt = D/('PROFILE_'+mode.upper()+'_ATTEMPT.json')
m.save(attempt.name,{'admission':m.ref(D/'PROFILE_ADMISSION.json'),'mode':mode,'run':run})
started = time.monotonic()
with stdout.open('xb') as out, stderr.open('xb') as err:
    try:
        result = subprocess.run(run['command'], env=card['environment'],
                                stdin=subprocess.DEVNULL,stdout=out,stderr=err,
                                timeout=30,check=False)
        code = result.returncode
        failure = None
    except subprocess.TimeoutExpired as error:
        code = None
        failure = str(error)
    out.flush(); err.flush()
completion = {'mode':mode,'command':run['command'],'environment':card['environment'],
              'elapsed_seconds':time.monotonic()-started,'returncode':code,'timeout':failure,
              'stdout':m.ref(stdout),'stderr':m.ref(stderr),'admission':m.ref(D/'PROFILE_ADMISSION.json')}
print(m.save('PROFILE_'+mode.upper()+'_COMPLETION.json',completion))
if code != 0 or failure is not None:
    raise SystemExit(1)
