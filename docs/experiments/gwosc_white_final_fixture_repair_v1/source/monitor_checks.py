"""RI156 pure complete RI130 successful monitor-record verifier; source only.
Author ri116_complete_caller_review. No target or runtime observation occurs.
"""
import math

LIMITS={'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05}

def need(ok,message):
    if not ok:raise ValueError('RI156_MONITOR: '+message)

def exact(a,b,message):
    need(type(a) is type(b) and a==b,message)

def number(x,message):need(type(x) in (float,int) and math.isfinite(x) and x>=0,message)

def arithmetic(a,b,message):
    number(a,message);number(b,message)
    # Tolerance only for recomposed saved floating timestamps. Both displayed
    # and recomposed gaps separately obey the unchanged literal resource bound.
    need(abs(a-b)<=8*math.ulp(max(float(a),float(b),1.0)),message)

def verify_monitor(record,limits):
    exact(limits,LIMITS,'unchanged limits')
    need(type(record['child_pid']) is int and record['child_pid']>0,'child pid')
    exact(record['child_exit_code'],0,'genuine zero child exit')
    need(record['error'] is None and record['stop_reason'] is None,'no monitor/parent failure')
    exact(record['ownership_tail'],{'close_stdout':{'value':None,'error':None},'close_stderr':{'value':None,'error':None}},'ordinary ownership tail')
    raw=record['monitor_attempts'];samples=record['samples']
    need(type(raw) is list and type(samples) is list and 0<len(samples)<=len(raw)<=len(samples)+1,'complete attempts/samples')
    duration=record['child_elapsed_seconds'];number(duration,'child duration');need(duration<=180,'child wall limit')
    previous=0;peak=0;numeric=0;terminal=False
    for i,row in enumerate(raw):
        need(type(row) is dict and set(row)=={'elapsed_seconds','returncode','stdout','stderr'},'closed raw monitor attempt')
        stamp=row['elapsed_seconds'];number(stamp,'attempt elapsed');need(previous<=stamp<=duration,'ordered attempt through reap')
        need(type(row['returncode']) is int and type(row['stdout']) is str and type(row['stderr']) is str,'raw result types')
        text=row['stdout'].strip();valid=row['returncode']==0 and text.isdigit()
        if not valid:
            need(i==len(raw)-1 and len(raw)==len(samples)+1 and numeric==len(samples),'only final exit-race malformed record')
            terminal=True;continue
        need(numeric<len(samples),'unmatched numeric attempt');sample=samples[numeric]
        need(type(sample) is dict and set(sample)=={'elapsed_seconds','rss_kib','gap_seconds'},'closed sample')
        exact(sample['elapsed_seconds'],stamp,'raw/sample exact timestamp')
        rss=int(text);need(type(sample['rss_kib']) is int and sample['rss_kib']==rss and 0<=rss<=524288,'exact bounded rss')
        gap=stamp-previous;number(sample['gap_seconds'],'sample gap');arithmetic(sample['gap_seconds'],gap,'gap arithmetic')
        need(gap<=0.1 and sample['gap_seconds']<=0.1,'sample deadline')
        previous=stamp;peak=max(peak,rss);numeric+=1
    need(numeric==len(samples),'every sample matched')
    need(type(record['peak_sampled_rss_kib']) is int and record['peak_sampled_rss_kib']==peak,'peak arithmetic')
    gap=duration-previous;arithmetic(record['final_sample_to_reap_gap_seconds'],gap,'final reap arithmetic')
    need(gap<=0.1 and record['final_sample_to_reap_gap_seconds']<=0.1 and record['final_sample_gap_passed'] is True,'final sample deadline')
    return {'raw_attempts':len(raw),'numeric_samples':numeric,'peak_sampled_rss_kib':peak,'child_elapsed_seconds':duration,
            'final_sample_to_reap_gap_seconds':record['final_sample_to_reap_gap_seconds'],
            'terminal_malformed_exit_race_source_premise':terminal,
            'scope':'Genuine unchanged source/owned-child correlation is external; no hard quota, parent RSS, descendant accounting or independent saved poll-finished bit.'}
