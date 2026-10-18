"""Root actual caller-guard acceptance after complete independent saved review."""
import importlib.util, tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
R=m.B/'ri152-independent-actual65-review-ssaGIKOi';S=m.B/'ri130-white-qualification-caller-source-Q4Aq7hZg'
read=m.load(m.D/'ROOT_REVIEW_READ.json');m.verify(R/'HANDOFF.json',read['handoff'])
h=m.load(R/'HANDOFF.json');v=m.load(R/'VERDICT.json');assert v['blocking_findings']==[] and v['status']==read['accepted_recommendation']
rows=h.get('payloads',h.get('files',h.get('files_excluding_self')));assert isinstance(rows,list)
assert sorted(p.name for p in R.iterdir())==sorted(['HANDOFF.json']+[Path(r['path']).name for r in rows])
for r in rows:m.verify(r['path'],r)
for r in read['review_objects']:m.verify(r['path'],r)
check=m.load(R/'SAVED_CHECK.json');assert check['status']=='PASS' and len(check['checks'])==87358 and all(x['passed'] is True for x in check['checks']) and len(check['read_inputs'])==1820
for row in check['read_inputs']:m.verify(row['path'],row)
for row in m.load(m.D/'SOURCE_PRE.json')['identities']:assert m.identity(row['path'])==row
op=Path(m.load(m.D/'OPERATION_LAYOUT.json')['operation']);out=op/'output'
for row in m.load(m.D/'OPERATION_FINAL_IDENTITIES.json')['identities']:assert m.identity(row['path'])==row
for key in ('card','guard_card','source_review'):
 row=m.load(m.D/'ADMISSION_CUSTODY.json')[key];assert m.identity(row['path'])==row
# Namespace also includes every empty directory and literal/dangling link.
import os, stat
tree=[]
for p in sorted(op.rglob('*')):
 row=dict(relative=p.relative_to(op).as_posix());st=p.lstat()
 if stat.S_ISLNK(st.st_mode):row.update(kind='symlink',target=os.readlink(p))
 elif stat.S_ISDIR(st.st_mode):row['kind']='directory'
 else:assert stat.S_ISREG(st.st_mode);row.update(kind='file',**m.pure(m.ref(p)))
 tree.append(row)
assert tree==m.load(m.D/'OPERATION_FINAL_IDENTITIES.json')['entries']
summary=check['summary'];assert summary['guard_outcomes']['cases']==65 and summary['guard_outcomes']['scientific_credit'] is False
decision=m.save('RI152_ROOT_ACTUAL_ADJUDICATION.json',dict(schema='ri152-root-actual-caller-guard-adjudication-v1',status='ACCEPT_GENUINE_65_NONSCIENTIFIC_CALLER_GUARDS',independent_review=m.ref(R/'HANDOFF.json'),independent_verdict=m.ref(R/'VERDICT.json'),independent_complete_check=m.ref(R/'SAVED_CHECK.json'),root_review_read=m.ref(m.D/'ROOT_REVIEW_READ.json'),root_manual_review=m.ref(m.D/'ROOT_MANUAL_GUARD_REVIEW.json'),root_custody_check=m.ref(m.D/'ROOT_GUARD_CHECK.json'),root_check_tools=m.ref(m.D/'ROOT_CHECK_TOOL.json'),genuine_outer=m.ref(m.D/'GENUINE_OUTER.json'),genuine_tools=m.ref(m.D/'GENUINE_TOOL_COMPLETE.json'),source_preflight=m.ref(m.D/'PREFLIGHT_ROOT_ADJUDICATION.json'),summary=summary,actual_initial='318cda',actual_session=56357,actual_terminal='2afc57',exit_code=0,subject_retries=0,reviewer_failure='Original failed checker omitted full32_qualified=false and actual_data_admitted=false in its expected worker custody. Preserved original script, failed predicate dump and stderr. Only those two fields added; complete actual evidence unchanged; administrative review rerun succeeds. No target replay.',refusal_evidence_limit='Some in-memory mutated operands and exact exception messages are enforced by the pinned genuinely executed harness, not separately serialized. No independent saved exception trace is claimed.',resource_limitations=['Sole-child sampled RSS, not a hard OS quota or process-tree budget','Unchanged180s/524288KiB/25ms/100ms/50ms; parent900s soft interval excludes final COMPLETE write; genuine960s outer covers return','Stable supplier, source/cache selection, trusted host/kernel/Appleloader and genuine tool-origin premises retained'],fixture_package=m.ref(m.D/'FIXTURE_BYTES.json'),fixture_pack_check=m.ref(m.D/'FIXTURE_PACK_CHECK.json'),scientific_targets_executed=False,white_scientific_qualification=False,actual_data_admitted=False,full32_qualified=False,calibration_or_native_forward_map=False,ret_paused=True))
print(decision)
names=('control.py','runtime_support.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py','profile_observe.source-only.py','guard_controls.source-only.py','TARGET_CLOSURE.source-only.json','HISTORY_CLOSURE.source-only.json')
guard=dict(schema='ri130-root-guard-qualification-v1',status='ACCEPT_EXACT_CALLER_GUARD_EXECUTION',helpers=[dict(path=str(S/n),pin=m.pure(m.ref(S/n))) for n in names],all_declared_guards_passed=True,scientific_targets_executed=False,report=m.ref(out/'GUARD_REPORT.json'),genuine_outer=m.ref(m.D/'GENUINE_OUTER.json'),independent_review=m.ref(R/'HANDOFF.json'))
print(m.save('GUARD_ACCEPTANCE.json',guard))
nextdir=Path(tempfile.mkdtemp(prefix='ri154-white-mode-preparation-',dir=m.B))
print(m.save('MEASUREMENT_NEXT_ACTION.json',dict(schema='ri154-white-mode-preparation-assignment-v1',status='RESERVED_SOURCE_AND_CUSTODY_PREPARATION_NOT_SCIENTIFIC_ADMISSION',owner='root',reservation=str(nextdir),predecessor=decision,guard_acceptance=m.ref(m.D/'GUARD_ACCEPTANCE.json'),next='Prepare and independently review exact source/acceptance bindings for a fresh WHITE execution root and complete external pre/post mode-custody driver. Keep original sealed RI130/RI141 packets immutable; no active freeze/cards/runs may be added there. Carry all30 exact source copies,11 helpers/declarations,124 history originals,17 role bindings and separate accepted current runtime/profile/guard premises. Any relocation, environment TMPDIR or observation adaptation needs explicit review; do not silently reuse fixed-path RI141/old RI121 applicability. Preserve genuine source/runtime authentication before target load, separate normal then accepted-normal-before-optimized ordering, saved reconstruction, whole57artifact/74postcheck/3tree relation, no-descendant scope and unchanged resource limits. Seal concrete source-only preparation and identify any actual blocker before a separate scientific admission. Scientific source acceptance, guards, runtime observations, WHITE15/two179, RI131/full32 and actual public GWOSC calculation/calibration/native forward map remain distinct.',operational_admission_created=False,scientific_execution=False,ret_paused=True)))
