"""Administrative identities/text only. Does not import or parse scientific targets."""
import hashlib
import json
from pathlib import Path
import re

OUT = Path('/Volumes/AI_DATA/development/det-review-evidence/ri125-white-publication-closure-xjTxsfe6')
BASE = Path('/Volumes/AI_DATA/development/det-review-evidence')
REPO = Path('/Volumes/AI_DATA/development/det_8_framework-ret')
PACKETS = {
 'source': ('ri125-white-source-completion-bg27qfdn', 5379, '4f5e547c359b8e1c3e4ee87f7b2351ce8259b705e7a3e033509b4072f3862468'),
 'independent': ('ri125-white-independent-review-z8c0p102', 1529, '8ce87fa9e3bf333b804e8edd27d4c8ec3502f1c77aa517fbc2cf50e0979761bf'),
 'predecessor': ('ri125-joint-window-application-source-fsra3wcw', 3467, '37fb54456a46f724a46b86661ddde512564b6ed2730750e5e811500b78db28ce'),
 'predecessor_review': ('ri125-independent-source-review-mlsKzUKA', 1602, '1005f7cd493ea5903327d012ffec6762563054c28f4a0cc9b25ca9dfde1baadd'),
}

def pin(path):
    p = Path(path)
    h = hashlib.sha256()
    total = 0
    with p.open('rb') as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
            total += len(b)
    return {'path': str(p), 'bytes': total, 'sha256': h.hexdigest()}

def read_metadata(path):
    # Invoked only for four handoff files and one predecessor manifest.
    return json.loads(Path(path).read_text())

checked = []
def check(role, expected, destination=None):
    actual = pin(expected['path'])
    ok = actual['bytes'] == expected['bytes'] and actual['sha256'] == expected['sha256']
    checked.append({'role': role, 'expected': expected, 'actual': actual,
                    'publication_destination': destination, 'matches': ok})
    return actual

packet_members = {}
for category, (directory, size, digest) in PACKETS.items():
    p = BASE / directory / 'HANDOFF.json'
    handoff = {'path': str(p), 'bytes': size, 'sha256': digest}
    check(category + ':HANDOFF.json', handoff, category + '/HANDOFF.json')
    files = read_metadata(p)['files']
    packet_members[category] = [handoff] + files
    for item in files:
        check(category + ':' + Path(item['path']).name, item,
              category + '/' + Path(item['path']).name)

source = BASE / PACKETS['source'][0]
predecessors = read_metadata(source / 'PREDECESSOR_PINS.json')['records']
role_names = ['predecessor_handoff','predecessor_review_handoff',
 'predecessor_review_prose','predecessor_math_review','predecessor_disposition',
 'design_acceptance','design','ri73_source','ri73_result','ri116_consulted_consumer',
 'ri73_reconciliation','ri73_audit_freeze','ri73_final_review','capture']
for role,item in zip(role_names, predecessors):
    check('direct_predecessor:' + role,item)

published_pairs = [
 ('design', predecessors[6], REPO/'docs/experiments/gwosc_joint_window_application_v1/DESIGN.md'),
 ('design_acceptance', predecessors[5], REPO/'docs/experiments/gwosc_joint_window_application_v1/ROOT_ADJUDICATION.json'),
 ('ri73_source', predecessors[7], Path(predecessors[7]['path'])),
 ('ri73_result', predecessors[8], Path(predecessors[8]['path'])),
 ('ri116_consulted_consumer', predecessors[9], Path(predecessors[9]['path'])),
]
for role, original, local in published_pairs:
    expected = dict(original, path=str(local))
    check('existing_repository:' + role, expected, str(local.relative_to(REPO)))

root_disposition = pin(BASE/'ri127-root-proof-review-tz7oyfkj/RI125_WHITE_SOURCE_DISPOSITION.json')
checked.append({'role': 'root_white_disposition', 'actual': root_disposition,
                'matches': True, 'note': 'Fresh identity; complete content manually read.'})

imports = {}
for name in ('white_kernel.py','white_path.py','white_controls.py'):
    lines = (source/name).read_text().splitlines()
    imports[name] = [{'line': i, 'text': x} for i,x in enumerate(lines,1)
                     if re.match(r'^\s*(import |from )',x)]
    suspicious = [{'line': i, 'text': x} for i,x in enumerate(lines,1)
                  if re.search(r'__import__|importlib|\bexec\s*\(|\beval\s*\(',x)]
    if suspicious:
        raise SystemExit('Unreviewed dynamic loading text: '+repr(suspicious))

result = {
 'schema':'ri125-white-publication-closure-metadata-v1',
 'status':'PASS_OPAQUE_IDENTITIES_AND_TEXT_IMPORT_INVENTORY' if all(x['matches'] for x in checked) else 'FAIL',
 'checked_role_count':len(checked),
 'unique_current_paths':len({x['actual']['path'] for x in checked}),
 'packet_member_counts':{k:len(v) for k,v in packet_members.items()},
 'direct_predecessor_role_count':len(predecessors),
 'records':checked,'import_text_inventory':imports,
 'limitations':[
  'Opaque bytes/hash only for all scientific JSON, including RESULT and INTERVALS.',
  'Only handoff/predecessor-manifest administrative JSON decoded.',
  'Text search is not Python parsing, compilation, import, or execution.',
  'No fresh full arithmetic source review, runtime verification, custody replay, qualification or admission.',
  'Current repository bytes compared; no Git/index inspection or mutation and no prospective repository copies yet verified.'
 ],
 'execution_authorized':False,'scientific_decode':False,
}
with (OUT/'METADATA_CHECK.json').open('x') as f:
    json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({k:result[k] for k in ('status','checked_role_count','unique_current_paths','packet_member_counts','direct_predecessor_role_count')},sort_keys=True))
