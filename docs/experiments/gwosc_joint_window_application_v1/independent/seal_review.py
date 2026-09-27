from pathlib import Path
import json, hashlib, stat, os
P=Path(__file__).resolve().parent
SOURCE=Path('/Volumes/AI_DATA/development/det-review-evidence/ri123-joint-window-application-design-e0qwhenu')
def pin(path):
 p=Path(path);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(name,obj):
 body=(json.dumps(obj,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode()
 with (P/name).open('xb') as f:f.write(body)
 return pin(P/name)
original=json.loads((P/'PIN_REVIEW.json').read_text())
checks=[]
for r in original['records']:
 p=Path(r['path']);before=p.stat();actual=pin(p);after=p.stat()
 assert before==after
 assert actual['bytes']==r['bytes'] and actual['sha256']==r['sha256']
 assert str(p.resolve())==r['resolved_path']
 assert before.st_dev==r['stat']['device'] and before.st_ino==r['stat']['inode'] and before.st_mode==r['stat']['mode'] and before.st_mtime_ns==r['stat']['mtime_ns']
 for q in r['path_chain']:
  f=Path(q['path']);s=f.lstat()
  assert s.st_dev==q['device'] and s.st_ino==q['inode'] and s.st_mode==q['mode']
  assert (os.readlink(f) if stat.S_ISLNK(s.st_mode) else None)==q['link']
 checks.append(actual)
final=save('FINAL_PIN_RECHECK.json',{'schema':'ri123-independent-design-final-pin-recheck-v1','all_50_file_identities_and_path_bindings_unchanged':True,'errors':[],'records':checks,'capture_opaque_only':True})
verdict=save('INDEPENDENT_DESIGN_REVIEW.json',{'schema':'ri123-independent-application-design-review-v1','status':'ACCEPT_CONDITIONAL_APPLICATION_DESIGN_ONLY','blocking_findings':[],'reviewer':'/root/ri123_application_review','independent_of_proposal_author':True,'proposal':pin(SOURCE/'DESIGN.md'),'source_handoff':pin(SOURCE/'HANDOFF.json'),'full_review':pin(P/'INDEPENDENT_DESIGN_REVIEW.md'),'pin_review':pin(P/'PIN_REVIEW.json'),'schema_review':pin(P/'SCHEMA_REVIEW.json'),'final_pin_recheck':final,'accepted_symbolic_results':['Exact disjoint head/tail reduction and directed C=U H^T for the fixed first-T operator.','Complete centered white covariance, Loewner sandwich, deterministic interval propagation and sufficient new usefulness inequality.','Shared periodic-completion parity formula with factors 48/49 and 1, explicit latent mean and interval-dependency handling.','Conditional covariance-discrepancy and calibration-factor bounds with unavailable physical nuisance inputs retained.'],'implementation_clarifications':['The actual RI73 bound matrix field is H; H_G is notation only.','The actual RI116 scenario energy mean term field is M; Mbar is notation only. Bind literal historical keys and exact source-record identities.','Freeze every nested schema, concrete case and first-refusal code before execution; the design is not a complete executable contract.'],'next_step':'Prepare the bounded source-only white-strip, saved-mode and join consumers, independently authored full-field validator and fixed fabricated qualifier; obtain separate complete source review before qualification.','coefficient_capture_decoded':False,'new_scientific_operands_contracted':False,'scientific_targets_executed':False,'qualification_executed':False,'empirical_data_processed':False,'runtime_or_execution_admission_created':False,'repository_or_git_changed':False,'physical_joint_law_selected':False,'calibration_established':False,'protected_validation':False,'native_forward_map':False,'programme_complete':False,'ret_paused':True,'remaining_prerequisites':['Root design adjudication.','Frozen executable contracts, complete independent source review, caller applicability and meaningful qualification controls.','Genuine normal execution and full review before separate optimized admission and complete-output equality.','Separate fresh complete input/source/runtime/host custody and unchanged resources for each real-input stage.','Complete independent mathematical reconstruction of every actual output field.','Physical covariance law/discrepancy, population mean, calibration and a quantitative native forward map remain unavailable.']})
files=[pin(p) for p in sorted(P.iterdir()) if p.is_file()]
handoff=save('HANDOFF.json',{'schema':'ri123-independent-design-review-handoff-v1','status':'ACCEPT_CONDITIONAL_APPLICATION_DESIGN_ONLY','packet_directory':str(P),'files':files,'file_count_excluding_handoff':len(files),'review':verdict,'blockers':[],'all_45_predecessor_and_5_packet_pins_match_twice':True,'scope':'Independent complete design proof and retained schema/source-path review only; no scientific execution, runtime admission, physical acceptance or repository edits.'})
print(json.dumps(handoff,indent=2))
print(json.dumps(verdict,indent=2))
