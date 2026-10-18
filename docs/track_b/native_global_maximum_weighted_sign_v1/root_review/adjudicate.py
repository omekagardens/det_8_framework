"""Record completed manual reviews and select the next bounded native question."""
from pathlib import Path
import hashlib,importlib.util,tempfile
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri211-root-global-W-review-xh6eetn1';Q=B/'ri210-native-six-maxima-leicoenm'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=D
metadata=m.load(D/'RI210_ROOT_METADATA_CHECK.json')
for r in metadata['fresh_identities']:assert m.identity(r['path'])==r
with (D/'RI210_ROOT_PROOF_REVIEW.md').open('xb') as f:f.write(Path('/private/tmp/ri211_root_proof_review.md').read_bytes())
review=dict(schema='ri211-nonauthor-ri210-review-v1',agent='/root/qr_opportunities',record_kind='Root-preserved summary of independent final review; original message remains in collaboration transcript',verdict='ACCEPT_ON_NAMED_INHERITED_PREMISES',mathematical_blocker=False,
    findings=[
        'RI185 marked restoration-only A5 proof covers selected sizes3/4; full first precursor in A4 and proper new-layer roles retained.',
        'All63ideal occurrences and64records, empty-parent1, exact parity cancellation, lower full entries and canonical size-four numerators retained.',
        'Literal A3 seed and theta<2^-38 give empty term<2^36; all56 other non-full terms total<1; six record-dependent full complements total<6 without extra theta.',
        'Complete one-through-six-maxima classes exhaust the finite same-law marked domain: M6<463b<465b<T.',
        'Original RI199 weighted identity, positive retained terms and strict U30 bound imply W/r>-1+8lambda*j0/[v(1+2M6)], hence W>0 even at target equality.',
        'Original q/N_i terms, product contrasts and actual correlated pair remain; both individual margins, H30 and physical claims are not established.'
    ],reads=[dict(chunk_id=x,exit_code=0) for x in ['37f0b9','f45096','b176c3','83e4a5','e1b023','fef7b7','91cec9','15a4b6']],
    recovered_diagnostic='Initial combined display clipped; scoped reads recovered complete contents.',
    complete_author_checker_read=True,author_checks_not_reviewer_execution=True,
    reported_author_preseal=dict(chunk_id='4a1283',exit_code=0,fresh_identities=30,selected_references=45),
    externally_reported_author_final=dict(chunk_id='9ff130',exit_code=0,fresh_identities=32,selected_references=48),
    inherited423_replayed=False,scientific_body_or_vector_parsed=False,automatic_proof_arithmetic=False,subject_execution=False,reviewer_writes=False,Git_operations=False,
    final_packet=[m.ref(p) for p in sorted(Q.iterdir())])
print(m.save('RI210_NONAUTHOR_REVIEW.json',review))
decision=dict(schema='ri211-root-ri210-adjudication-v1',status='ACCEPT_COMPLETE_SIX_MAXIMA_GLOBAL_BOUND_AND_STRICT_WEIGHTED_W',
    handoff=m.ref(Q/'HANDOFF.json'),proof=m.ref(Q/'SIX_MAXIMA.md'),global_proof=m.ref(Q/'GLOBAL_W.md'),metadata=m.ref(D/'RI210_ROOT_METADATA_CHECK.json'),root_review=m.ref(D/'RI210_ROOT_PROOF_REVIEW.md'),independent_review=m.ref(D/'RI210_NONAUTHOR_REVIEW.json'),
    root_check=dict(chunk_id='e759ae',exit_code=0),
    theorems=['Every marked six-antichain has U6<2^36+7=68719476743<69000000000.',
              'Exhaustive finite same-law domain has M6<463000000000<465000000000<T=4lambda*j0/v-1/2.',
              'The original weighted quantity satisfies W(rho,s)>0 at the actual correlated pair; the RI199 sufficient implication remains strict even at M6=T.'],
    premises=m.load(Q/'HANDOFF.json')['inherited_premises_not_fresh_verification'],
    actual_W_decided=True,actual_W_positive=True,global_M6_bound_proved=True,both_individual_margins_or_H30_decided=False,physical_correspondence_proved=False,
    scientific_body_decoded=False,scientific_execution=False,automatic_proof_arithmetic=False,qualification_credit=False,RET_paused=True,
    author_final_reported_not_root_execution=dict(chunk_id='9ff130',exit_code=0))
print(m.save('RI210_ROOT_ADJUDICATION.json',decision))
paths=[
 'docs/track_b/native_growth_connected_compensation_v1/DECISION_CONTRACT.md',
 'docs/track_b/native_growth_connected_compensation_v1/LOCAL_POSITIVITY.md',
 'docs/track_b/native_growth_connected_compensation_v1/RECORD_TRANSPORT.md',
 'docs/track_b/native_growth_connected_sign_v1/INPUT_FORMULAS.md',
 'docs/track_b/native_growth_connected_sign_v1/ANALYTIC_BOUNDS.md',
 'docs/track_b/native_growth_weighted_margin_interval_v1/source/WEIGHTED_MARGIN_PROOF.md']
historical=m.load(B/'ri197-manual-original-pair-proof-dh668vz_/SOURCE_DEPENDENCIES.json')
rows=[]
for name in paths:
    r=m.ref(m.REPO/name);matches=[x for x in historical['protected_files'] if m.pure(x['identity'])==m.pure(r)]
    assert matches and all(x['classification']=='analytic-source-text-or-review' for x in matches)
    rows.append(dict(identity=r,inherited_matches=[x['identity'] for x in matches],access='accepted-analytic-text',typed_reference_expansion=False))
reservation=Path(tempfile.mkdtemp(prefix='ri212-native-individual-margins-',dir=B))
assignment=dict(schema='ri212-native-individual-margin-assignment-v1',status='ASSIGNED_AFTER_RI210_INDEPENDENT_ADJUDICATION',predecessor=m.ref(D/'RI210_ROOT_ADJUDICATION.json'),reservation=str(reservation),owner_thread='01a074c4-4b09-76a3-8cb2-0caf116f6b9c',
    question='For the unchanged selected law and original fixed seed/amplitude, prove or refute simultaneous strict C2(rho,s)>0 and C3(rho,s)>0 at the same actual correlated pair. Use accepted RI210 global M6 bound as a native lower bound on rho, retain the existing upper cap and s correlation, and keep the original P2/P3 definitions.',
    exact_targets=['C2=z2+4[rho^2*D2/q(rho)]*(1-s*U20(rho))+4s*rho^3*(epsilon2+r2_0)',
                   'C3=z3+4[rho*D3/((1-rho)*v)]*(1-s*U30(rho))+4s*rho^2*(epsilon3+r3_0)'],
    source_admission=rows,
    rationale='The weighted obstruction is now settled positively but does not decide the necessary two local intervals. The new complete-law lower bound on rho changes the prior domain that approached zero, justifying a direct same-law sign analysis.',
    successful_outputs=['A proof of both original strict inequalities with exact signs and shared coefficients; or a proof that an original margin is nonpositive at the actual pair; or substantive reductions with a precise remaining native inequality or held scalar needed, explaining why accepted premises do not yet settle it.'],
    constraints=['Manual analytic source-only work in this exclusive reservation. No scientific body/vector/certificate parsing or automatic proof arithmetic, graph/LP/subject execution, runtime/fixture/card work, repo/Git or RET changes.',
                 'Six explicitly named existing analytic texts are admitted as literal read sources with exact inherited matches. Their scientific/operational/opaque descendants are not newly admitted. Current RI210 packet and root adjudication remain literal current sources; earlier inherited boundaries persist.',
                 'Preserve original z1=1, harmonic seed identity, |z_j|<=1, amplitude1/4, actual q/N_i canonical terms and zero/tied branches. No H/z reconstruction, free coefficient box, favorable scale selection or law retuning.',
                 'Maintain all record/ideal multiplicities, proper/full distinctions, positive denominators, strict endpoint exclusions and fixed actual rho,s dependence. W>0 is not both-margin positivity.',
                 'A local positive result does not solve sharedT1, eight other connected parents, fiveDi or H30. Keep these and physical/executable qualifications separate.',
                 'Do not repeat completed antichain/classification/weighted packets or create a generic containing cap alone. Identify exact new data needed if the bounded question requires an additional literal-source admission; proceed with independent analytic reductions.',
                 'Seal source/provenance/manual checks and actual administrative receipts for root independent review. Root owns successor selection and all publication/index work.'],
    inherited423_by_reference=True,new_scientific_execution_authority=False,qualification_credit=0,RET_paused=True)
print(m.save('RI212_NATIVE_ASSIGNMENT.json',assignment))
with (D/'adjudicate.py').open('xb') as f:f.write(Path(__file__).read_bytes())
