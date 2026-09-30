"""Root RI141 opaque identity and complete literal-delta checks only."""
import difflib
import importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
B=m.D.parent;S=B/'ri141-white-bootstrap-source-h58ls076';O=B/'ri135-white-preparation-repair-source-lski1ize'
m.verify(S/'HANDOFF.json',dict(bytes=9366,sha256='40effed085b2b79cd8933d675ec627e51c2910d95ea1f2e02ea75d2927c40f65'))
h=m.load(S/'HANDOFF.json')
assert len(h['files'])==14 and sorted(p.name for p in S.iterdir())==h['exact_namespace']
for row in h['files']:m.verify(row['path'],row)
d=m.load(S/'DEPENDENCIES.source-only.json');old=m.load(O/'DEPENDENCIES.source-only.json');deps=d['opaque_files']
assert len(deps)==442 and len({x['path'] for x in deps})==442
total=0
for row in deps:total+=m.verify(row['path'],row)['bytes']
assert total==25947539 and len(old['opaque_files'])==253 and all(row in deps for row in old['opaque_files'])
c=m.load(S/'SOURCE_CORRESPONDENCE.json');spans=[]
for mode in ['old','new']:
 for row in c['sources'][mode].values():m.verify(row['path'],row)
for row in c['functions']:
 if not row['identical']:continue
 slices=[]
 for mode in ['old','new']:
  lines=Path(c['sources'][mode][row['file']]['path']).read_bytes().splitlines(keepends=True);span=row[mode]
  raw=b''.join(lines[span['start']-1:span['end']]);assert m.pin(raw)==m.pure(span);slices.append(raw)
 assert slices[0]==slices[1];spans.append([row['file'],row['name']])
assert len(spans)==43
assert (S/'fault_controls.source-only.py').read_bytes()==(O/'fault_controls.source-only.py').read_bytes()
diff=''
for name in ['prepare.py','runtime_metadata.py']:
 diff+=''.join(difflib.unified_diff((O/name).read_text().splitlines(keepends=True),(S/name).read_text().splitlines(keepends=True),fromfile=str(O/name),tofile=str(S/name)))
assert diff==(S/'REPAIR.diff').read_text()
assert d['selected_bootstrap_binding']==m.load(d['bootstrap_selection_provenance']['path'])['selected_bootstrap_binding']
assert d['bootstrap_selection_provenance'] in deps
print(m.save('RI141_ROOT_SOURCE_CHECK.json',dict(status='PASS_LITERAL_METADATA_CHECKS_ONLY',source_handoff=m.ref(S/'HANDOFF.json'),payloads=14,namespace_files=15,dependencies=442,dependency_bytes=total,inherited_opaque_pins_preserved=253,added_pins=189,unchanged_top_level_spans=spans,complete_diff_regenerated_exact=True,whole_retained_harness_unchanged=True,current_vendor_or_candidate_observed=False,subject_import_compile_ast_execution=False,source_acceptance=False,independent_review_pending=True)))
