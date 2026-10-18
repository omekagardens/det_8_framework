"""Read-only adaptation of prior reviewer metadata checker; no subject imports."""
from pathlib import Path
import hashlib
D=Path(__file__).parent;old=D.parent/'ri190-current-e-normal-profile-review-zzmi16rs/check_normal_saved.py';b=old.read_bytes()
assert len(b)==37343 and hashlib.sha256(b).hexdigest()=='d275f5e629fab94a2f4689b9840701f8f63b7fc75a127057654ed56bfbeb6d64';s=b.decode()
def sub(a,b):
 global s
 assert a in s,a
 s=s.replace(a,b)
sub('RI190 independent administrative normal-profile saved-evidence checker','RI193 independent administrative optimized/both-mode saved-evidence checker')
sub('ri188-root-endpoint-profile-review-1jg_i948','ri192-root-optimized-profile-gtsq3_01');sub('ri170-current-e-profile-normal-proposed-gikj2giy','ri170-current-e-profile-optimized-proposed-gikj2giy')
sub("A=R/'RI190_REVIEW_ASSIGNMENT.json'","N=B/'ri170-current-e-profile-normal-proposed-gikj2giy'\nA=R/'RI193_REVIEW_ASSIGNMENT.json'")
sub("{'bytes':6859,'sha256':'8bbc25f3bf896d36c87686c96688cf18df1f8304f7a9f46d68addfdfa1cb2d21'}","{'bytes':5739,'sha256':'4d8b4c7157c5a2102c2279212eb60de1c9e843fdb860c1306ed1f25e80040428'}")
sub("[assignment['admission'],assignment['baseline']]+list(assignment['sources'].values())","assignment['inputs']+[assignment['normal_acceptance']]")
sub('PROFILE_NORMAL','PROFILE_OPTIMIZED');sub("'profile_normal'","'profile_optimized'")
sub("'sources':623","'sources':644")
sub("equal([card[k] for k in ('normal_acceptance','profiles_acceptance','guard_admission')],[None]*3,'no later stage admission');equal(card['baseline_acceptance'],assignment['baseline'],'independently accepted baseline required')","equal([card[k] for k in ('profiles_acceptance','guard_admission')],[None]*2,'no later stage admission');equal(card['normal_acceptance'],assignment['normal_acceptance'],'independently accepted normal required');verify(card['normal_acceptance']);equal(card['baseline_acceptance'],{'path':str(RR/'BASELINE_ACCEPTANCE.json'),'bytes':1657,'sha256':'75d30bdc2d03621867ce5a64c229eb619b6183f29b6434dbc04b4a2792e5e06e'},'exact accepted baseline');verify(card['baseline_acceptance'])")
sub("'2b5d3e','genuine initial chunk'","'6d14e9','genuine initial chunk'");sub("63779,'genuine session'","69700,'genuine session'")
sub("{'chunk_id':'9aba56','wall_time_seconds':0.736710916,'exit_code':0,'original_token_count':0,'output':''}","{'chunk_id':'e3f394','wall_time_seconds':0.464672583,'exit_code':0,'original_token_count':0,'output':''}")
# Reuse the complete monitor predicates for BOTH modes, each over its own full saved files.
a=s.index(' monitors=[]\n');z=s.index(" require((C/'PRE.stdout').read_bytes()",a);block=s[a:z]
block=block.replace('C/', 'op/').replace("str(RR/'ADMIT_PROFILE_OPTIMIZED.json')","str(RR/('ADMIT_PROFILE_OPTIMIZED.json' if optimized else 'ADMIT_PROFILE_NORMAL.json'))")
oldcmd="[str(B/'ri73-recovery/recovery-20260924T212511Z-2403d37c/env/bin/python'),'-I','-B',str(B/'ri130-white-qualification-caller-source-Q4Aq7hZg/profile_observe.source-only.py')]"
assert oldcmd in block
block=block.replace(oldcmd,"[str(B/'ri73-recovery/recovery-20260924T212511Z-2403d37c/env/bin/python'),'-I','-B']+(['-O'] if optimized else [])+[str(B/'ri130-white-qualification-caller-source-Q4Aq7hZg/profile_observe.source-only.py')]")
s=s[:a]+' def replay_monitors(op, optimized):\n'+''.join(' '+line+'\n' for line in block.splitlines())+'  return monitors\n monitors=replay_monitors(C,True)\n normal_monitors=replay_monitors(N,False)\n'+s[z:]
# Reconstruct each complete profile independently; do not assume module cache equality.
a=s.index(' # Interpret saved normal runtime/profile');z=s.index(' # Final state/link replay',a);block=s[a:z]
last=" equal([r['samples'] for r in monitors],[52,10,54],'all116 actual monitored samples')\n";assert last in block;block=block.replace(last,'')
block=block.replace("profile=load(C/'PROFILE.stdout')","profile=load(op/'PROFILE.stdout');mode_checks=load(op/'CHECKS.json')")
block=block.replace("'optimize':0","'optimize':optimize").replace("saved_checks['profile'],reconstructed","mode_checks['profile'],reconstructed")
s=s[:a]+' def replay_profile(op,optimize):\n'+''.join(' '+line+'\n' for line in block.splitlines())+"  return profile,reconstructed,descriptors,descriptor_kinds,ordered\n profile,reconstructed,descriptors,descriptor_kinds,ordered=replay_profile(C,1)\n normal_profile,normal_reconstruction,normal_descriptors,normal_descriptor_kinds,normal_ordered=replay_profile(N,0)\n equal([r['samples'] for r in monitors],[53,9,50],'all112 optimized samples')\n equal([r['samples'] for r in normal_monitors],[52,10,54],'all116 retained normal samples')\n"+(D/'normal_relation_fragment.txt').read_text()+s[z:]
sub("'normal_profile_pin':ref(C/'PROFILE.stdout')","'optimized_profile_pin':ref(C/'PROFILE.stdout'),'normal_profile_pin':ref(N/'PROFILE.stdout'),'normal_monitors':normal_monitors,'normal_descriptor_kinds':normal_descriptor_kinds,'both_mode_relation':relation")
with (D/'check_optimized_saved.py').open('x') as f:f.write(s)
print('Administrative both-mode checker written; old reviewer source untouched.')
