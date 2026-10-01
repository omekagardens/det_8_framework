"""Administrative source adaptation; reads prior reviewer source as text only."""
from pathlib import Path
import hashlib
D=Path(__file__).parent;old=D.parent/'ri186-current-e-capture-independent-68ebm0tu/check_saved_capture_v2.py'
b=old.read_bytes();assert len(b)==25686 and hashlib.sha256(b).hexdigest()=='0d4895aa3fc8226e306d674e076c01a5324941f5efb64b387b4643c9418e396a';s=b.decode()
def sub(a,b):
 global s
 assert a in s,a
 s=s.replace(a,b)
sub('RI186 independent administrative saved-evidence checker','RI190 independent administrative normal-profile saved-evidence checker')
sub('ri183-root-parent-capture-review-2mnanskj','ri188-root-endpoint-profile-review-1jg_i948');sub('ri170-current-e-capture-proposed-gikj2giy','ri170-current-e-profile-normal-proposed-gikj2giy');sub('RI186_REVIEW_ASSIGNMENT.json','RI190_REVIEW_ASSIGNMENT.json')
sub("{'bytes':4541,'sha256':'db880dbc1be4d2d315cd301b2a7c14e131cda902be6adcf5fbf3ad93bc28dc4c'}","{'bytes':6859,'sha256':'8bbc25f3bf896d36c87686c96688cf18df1f8304f7a9f46d68addfdfa1cb2d21'}")
sub("for row in assignment['pins']:verify(row)","for row in [assignment['admission'],assignment['baseline']]+list(assignment['sources'].values()):verify(row)")
for a,b in [('CAPTURE_PREFLIGHT','PROFILE_NORMAL_PREFLIGHT'),('CAPTURE_SOURCE_ADJUDICATION','PROFILE_NORMAL_SOURCE_ADJUDICATION'),('CAPTURE_POST_CUSTODY','PROFILE_NORMAL_POST_CUSTODY'),('CAPTURE_ADMISSION_CUSTODY','PROFILE_NORMAL_ADMISSION_CUSTODY'),('ADMIT_CAPTURE','ADMIT_PROFILE_NORMAL')]:sub(a,b)
sub("'sources':612","'sources':623")
sub("for group in ('sources','copies','vendor','tools'):","for group in ('sources','copies','vendor','tools','runtime'):")
sub("genuine=load(R/'GENUINE_CAPTURE_COMPLETE.json');initial=load(R/'GENUINE_CAPTURE_INITIAL.json')","genuine={'dispatch':load(R/'PROFILE_NORMAL_DISPATCH.json'),'initial':load(R/'GENUINE_PROFILE_NORMAL_INITIAL.json'),'terminal':load(R/'GENUINE_PROFILE_NORMAL_COMPLETE.json')};initial=genuine['initial']")
sub("equal([card[k] for k in ('baseline_acceptance','normal_acceptance','profiles_acceptance','guard_admission')],[None]*4,'no later stage admission')","equal([card[k] for k in ('normal_acceptance','profiles_acceptance','guard_admission')],[None]*3,'no later stage admission');equal(card['baseline_acceptance'],assignment['baseline'],'independently accepted baseline required')")
sub("['capture',str(C),str(E)]","['profile_normal',str(C),str(E)]")
sub("equal(initial['dispatch'],genuine['dispatch'],'initial complete dispatch');equal(initial['initial'],genuine['initial'],'initial raw session')","equal(initial['chunk_id'],'2b5d3e','genuine initial chunk')")
sub("66579,'genuine session'","63779,'genuine session'")
sub("{'chunk_id':'5c0651','wall_time_seconds':0.000007542,'exit_code':0,'original_token_count':0,'output':''}","{'chunk_id':'9aba56','wall_time_seconds':0.736710916,'exit_code':0,'original_token_count':0,'output':''}")
sub("GENUINE_CAPTURE_COMPLETE.json","GENUINE_PROFILE_NORMAL_COMPLETE.json")
sub("equal(complete['phase'],'capture','parent phase')","equal(complete['phase'],'profile_normal','parent phase')")
sub("'phase':'capture','sources'","'phase':'profile_normal','sources'")
sub("artifacts={'PRE'","artifacts={'PROFILE':'PROFILE.stdout','PROFILE_completion':'PROFILE.COMPLETION.json','PRE'")
sub("for label in ('PRE','POST') for suffix","for label in ('PRE','PROFILE','POST') for suffix")
sub("'literal twelve outputs'","'literal sixteen outputs'")
sub("equal(load(C/'CHECKS.json'),{'post_metadata':'PASS','source_and_admission_postcheck':'PASS'},'closed checks labels; independently reconstructed below')","saved_checks=load(C/'CHECKS.json');keys(saved_checks,('post_metadata','source_and_admission_postcheck','profile'),'closed checks');equal([saved_checks['post_metadata'],saved_checks['source_and_admission_postcheck']],['PASS','PASS'],'base check labels reconstructed below')")
sub("for label in ('PRE','POST'):\n  child=","for label in ('PRE','PROFILE','POST'):\n  child=")
sub("expected=[vendor,'-I','-B',str(S/'prepare.py'),'--snapshot',str(RR/'ADMIT_PROFILE_NORMAL.json')]","limit=30 if label=='PROFILE' else 180\n  expected=([str(B/'ri73-recovery/recovery-20260924T212511Z-2403d37c/env/bin/python'),'-I','-B',str(B/'ri130-white-qualification-caller-source-Q4Aq7hZg/profile_observe.source-only.py')] if label=='PROFILE' else [vendor,'-I','-B',str(S/'prepare.py'),'--snapshot',str(RR/'ADMIT_PROFILE_NORMAL.json')])")
sub("equal(child['wall_seconds'],180,'child wall bound')","equal(child['wall_seconds'],limit,'child wall bound')")
sub("[expected,env,180,False]","[expected,env,limit,False]")
sub("0<child['elapsed_seconds']<=180","0<child['elapsed_seconds']<=limit")
sub("equal(len(selection),9923,'runtime count')","equal(len(selection),9923,'runtime count');equal(layout['runtime'],load(R/'RUNTIME_POST_IDENTITIES.json')['identities'],'complete preflight runtime versus final identity domain')")
# Insert independently expressed baseline and profile checks before the final identity replay.
addition=(D/'profile_checks_fragment.txt').read_text()
sub(" # Final state/link replay for every opaque file read; excludes atime intentionally.",addition+"\n # Final state/link replay for every opaque file read; excludes atime intentionally.")
sub("'monitors':monitors,'parent_seconds'","'profile_modules':len(profile['modules']),'profile_descriptors':len(descriptors),'profile_descriptor_kinds':descriptor_kinds,'ordered_dyld_attempts':ordered,'normal_profile_pin':ref(C/'PROFILE.stdout'),'monitors':monitors,'parent_seconds'")
sub("'ADMIN_FAILURE_V2.json'","'ADMIN_FAILURE.json'")
with (D/'check_normal_saved.py').open('x') as f:f.write(s)
print('Administrative checker source written; prior source unchanged.')
