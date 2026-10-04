"""Validate a minimal audio-locked shot contract; does not certify visual quality."""
import argparse,json,math,pathlib,sys

FIELDS=('id','start','end','narration','subject','start_state','action','end_state','camera_purpose','invariants','claim_ids','renderer','reject_if')

def validate(plan):
    errors=[]
    if not isinstance(plan,dict):return ['root must be an object']
    duration=plan.get('audio_duration')
    if not isinstance(duration,(int,float)) or isinstance(duration,bool) or not math.isfinite(duration) or duration<=0:
        errors.append('audio_duration must be positive and finite');duration=None
    shots=plan.get('shots')
    if not isinstance(shots,list) or not shots:return errors+['shots must be a nonempty array']
    seen=set();last=0
    for i,s in enumerate(shots):
        prefix=f'shot {i}'
        if not isinstance(s,dict):errors.append(prefix+': expected object');continue
        missing=[f for f in FIELDS if f not in s or s[f] is None or s[f]=='' or s[f]==[]]
        if missing:errors.append(prefix+': missing '+','.join(missing))
        ident=s.get('id')
        if not isinstance(ident,str):errors.append(prefix+': id must be text')
        elif ident in seen:errors.append(prefix+': duplicate id')
        else:seen.add(ident)
        a,b=s.get('start'),s.get('end')
        if any(not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) for v in [a,b]):errors.append(prefix+': invalid times');continue
        if b<=a or a<0:errors.append(prefix+': invalid interval')
        if abs(a-last)>.08:errors.append(prefix+': gap/overlap exceeds 80 ms')
        last=b
        for k in ('invariants','claim_ids','reject_if'):
            if not isinstance(s.get(k),list):errors.append(prefix+': '+k+' must be a list')
    if duration is not None and abs(last-duration)>.08:errors.append('shots do not end with edited audio')
    return errors

def main():
    p=argparse.ArgumentParser();p.add_argument('plan',type=pathlib.Path);a=p.parse_args()
    errors=validate(json.loads(a.plan.read_text('utf-8-sig')))
    print(json.dumps({'structural_status':'fail' if errors else 'pass','errors':errors,'visual_review_required':True},ensure_ascii=False,indent=2))
    return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
