"""Independent byte/text checks only; never import or execute subjects."""
import hashlib
import importlib.util
from pathlib import Path
import re

hp=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
raw=hp.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
m.D=Path(__file__).resolve().parent
s=m.B/'ri169-write-would-block-repair-7_868hay';p=m.B/'ri167-native-supervisor-repair-79xn8tjz'
hpin=dict(bytes=8729,sha256='68514ab733813e3de96ffcc0cfc536b7366530018dfea68af47e287630c6523e')
identities=[m.verify(s/'HANDOFF.json',hpin)];h=m.load(s/'HANDOFF.json')
assert sorted(x.name for x in s.iterdir())==sorted(h['namespace'])==sorted(['HANDOFF.json']+[Path(r['path']).name for r in h['payloads']])
for row in h['payloads']:identities.append(m.verify(row['path'],row))
deps=m.load(s/'DEPENDENCY_BINDINGS.json')
assert len(deps['fresh_original_pins'])==26
for row in deps['fresh_original_pins']:identities.append(m.verify(row['path'],row))
old=(p/'supervise_native.py').read_text();new=(s/'supervise_native.py').read_text()
start="    def drain(failed):\n        for name in readable_names(selector, active, failed, deadline, 0.05, pump_issue):\n"
tail="\n    try:\n        for name, suffix in"
def block(text):
 assert text.count(start)==1
 a=text.index(start);b=text.index(tail,a);return text[a:b]
before=block(old);after=block(new)
assert before.count("                chunk = os.read(pipes[name].fileno(), min(65536, CAP + 1 - counts[name]))\n")==1
expected=before.replace("                chunk = os.read(pipes[name].fileno(), min(65536, CAP + 1 - counts[name]))\n", "                read_fd = pipes[name].fileno()\n                try:\n                    chunk = os.read(read_fd, min(65536, CAP + 1 - counts[name]))\n                except BlockingIOError:\n                    continue\n").replace("            except BlockingIOError:\n                continue\n",'')
assert expected==after
assert new.replace(after,before)==old
def spans(text):
 matches=list(re.finditer(r'^def ([A-Za-z_][A-Za-z_0-9]*)\(',text,re.M))
 return {r.group(1):text[r.start():matches[i+1].start() if i+1<len(matches) else len(text)] for i,r in enumerate(matches)}
a,b=spans(old),spans(new);assert a.keys()==b.keys() and len(a)==15
unchanged=[k for k in a if a[k]==b[k]];assert len(unchanged)==14 and 'supervise' not in unchanged
for name in ['FOCUSED_VARIANTS.json','SUPERVISOR_CHECKS.md']:assert (s/name).read_bytes()==(p/name).read_bytes()
ret=m.load(s/'FOCUSED_VARIANTS.json');add=m.load(s/'WRITE_READ_VARIANTS.json')
assert len(ret['retained_groups'])==13 and len(ret['variants'])==28 and len(add['variants'])==6
rows=ret['variants']+add['variants'];assert len({r['id'] for r in rows})==34 and all(r['executed'] is False for r in rows)
assert {r['id'] for r in add['variants']}=={'S04.'+stream+'.'+kind for stream in ('stdout','stderr') for kind in ('write_would_block.zero_progress','write_would_block.after_prefix','read_would_block.transient')}
op=m.load(p/'COMMAND_PROPOSAL.json');np=m.load(s/'COMMAND_PROPOSAL.json')
for key in ('unchanged_native_argv','unchanged_five_sources','unchanged_request','proposed_paths','environment','capture_limits','ordinary_supervisor_source_entry_bound_seconds'):
 assert op[key]==np[key],key
assert not Path(np['unchanged_request']['path']).exists()
assert m.pin(np['command_utf8'].encode())==np['command_pin']
print(m.save('RI169_INDEPENDENT_METADATA_CHECK.json',dict(schema='ri169-root-independent-source-check-v1',status='PASS',identities=identities,subject_files=20,fresh_originals=26,whole_reverse_projection=True,unchanged_functions=unchanged,source_lines=len(new.splitlines()),retained_groups=13,retained_recipes=28,new_recipes=6,actual_checks=0,request='still absent; proposed pin only',subject_execution=False,scientific_decode=False)))
