"""Assemble a bounded 3- or 5-shot motion proof from original Blender frames.
No reference-channel media is used. Voice phrases are the first three entries
of the locally generated audio timeline. This is a mechanism test, not a full episode.
"""
import pathlib,json,subprocess,re,wave,math,sys
import numpy as np
import argparse, shutil
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--work-dir',type=pathlib.Path,required=True,help='Directory containing motion-source.mp4, voice files and timeline JSON')
parser.add_argument('--out-dir',type=pathlib.Path,required=True)
parser.add_argument('--ffmpeg',default='ffmpeg',help='Installed FFmpeg executable or command on PATH')
parser.add_argument('--full',action='store_true',help='Use all five original voice phrases and camera sections')
parser.add_argument('--use-motion',action='store_true',help='Use an existing 24fps motion-source.mp4 instead of PNGs')
parser.add_argument('--prepare',action='store_true')
options=parser.parse_args()
P=options.work_dir.resolve();OUT=options.out_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
FF=pathlib.Path(shutil.which(options.ffmpeg) or options.ffmpeg)
if not FF.is_file():raise FileNotFoundError('FFmpeg executable not found')
timeline=json.loads((P/'audio-timeline.json').read_text('utf-8'));rows=timeline['segments'] if '--full' in sys.argv else timeline['segments'][:3];duration=sum(x['duration'] for x in rows)
def run(args):
 p=subprocess.run([str(FF),'-hide_banner','-y',*args],capture_output=True,text=True,encoding='utf-8',errors='replace')
 if p.returncode:raise RuntimeError(p.stderr[-3000:])
 return p.stderr
def stamp(s):
 h,m,v=s.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(v)
def ass_time(t):
 n=round(t*100);return f'{n//360000}:{n//6000%60:02}:{n//100%60:02}.{n%100:02}'
def savewav(p,data,sr=48000):
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())
audio=[];timings=[];cursor=0
for r in rows:
 with wave.open(str(P/r['audio']),'rb') as w:audio.append(np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768)
 # Determine actual leading silence removed from raw audio; provider word times
 # are retained with that offset, not falsely called phonetic forced alignment.
 raw=run(['-i',str(P/f"voice_{r['id']}.mp3"),'-af','silencedetect=noise=-45dB:d=0.02','-f','null','-'])
 match=re.search(r'silence_start: 0\s.*?silence_end: ([0-9.]+)',raw,re.S);lead=float(match[1]) if match else 0
 cues=[]
 for a,b,txt in re.findall(r'(\d\d:\d\d:\d\d,\d+) --> (\d\d:\d\d:\d\d,\d+)\s*\n([^\n]+)',(P/f"voice_{r['id']}.srt").read_text('utf-8')):
  cues.append((stamp(a),stamp(b),txt.strip()))
 group_sizes={0:[3,4],1:[3,2,3],2:[4,3,2],3:[2,2,2],4:[3,3,5]}[r['id']]
 groups=[];idx=0
 for count in group_sizes:groups.append(cues[idx:idx+count]);idx+=count
 for j,g in enumerate(groups):
  a=max(0,g[0][0]-lead);b=max(a+.12,groups[j+1][0][0]-lead) if j+1<len(groups) else r['duration']
  timings.append((cursor+a,min(cursor+b,cursor+r['duration']),' '.join(x[2] for x in g)))
 cursor+=r['duration']
voice=np.concatenate(audio);sr=48000;n=len(voice);t=np.arange(n)/sr
# Original quiet industrial bed and synchronized contact/flow sounds.
rng=np.random.default_rng(42);bed=.006*np.sin(2*np.pi*65.406*t)+.003*np.sin(2*np.pi*98*t)
bed*=np.minimum(1,t/.3)*np.minimum(1,(duration-t)/.35)
for at in ([2.81,4.24,7.24,12.57] if len(rows)==5 else [2.81,4.24,7.24]):
 u=t-at;env=np.where((u>=0)&(u<.18),np.exp(-np.maximum(u,0)*40),0)
 bed+=env*(.015*np.sin(2*np.pi*950*u)+.008*rng.standard_normal(n))
bed+=.002*rng.standard_normal(n)*((t>7.23)&(t<duration-.2))
savewav(P/'proof-voice.wav',voice);savewav(P/'proof-bed.wav',bed)
run(['-i',str(P/'proof-voice.wav'),'-i',str(P/'proof-bed.wav'),'-filter_complex','[0:a]loudnorm=I=-16:TP=-2:LRA=7[v];[v][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.84:level=false[out]','-map','[out]','-ar','48000',str(P/'proof-mix.wav')])
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Malgun Gothic,35,&H00FFFFFF,&H00FFFFFF,&H00151B23,&H60000000,-1,0,0,0,100,100,0,0,1,3,1,5,35,35,20,1
Style: Title,Malgun Gothic,27,&H00E2F0F6,&H00FFFFFF,&H00151B23,&H60000000,-1,0,0,0,100,100,0,0,1,2,0,5,30,30,20,1
Style: Note,Malgun Gothic,19,&H00FFFFFF,&H00FFFFFF,&H00151B23,&H60000000,0,0,0,0,100,100,0,0,1,2,0,5,25,25,20,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
events=[]
for a,b,txt in timings:events.append(f'Dialogue: 3,{ass_time(a)},{ass_time(b)},Caption,,0,0,0,,{{\\pos(360,300)\\fad(40,0)}}{txt}')
events.append(f'Dialogue: 2,0:00:00.00,{ass_time(duration)},Title,,0,0,0,,{{\\pos(360,95)}}AI 서버의 숨은 물길')
events.append(f'Dialogue: 2,0:00:00.00,{ass_time(duration)},Note,,0,0,0,,{{\\pos(360,1080)}}냉각 구조 구현 시험 · 개념 모형')
events.append(f'Dialogue: 2,{ass_time(rows[0]["duration"])},{ass_time(duration)},Note,,0,0,0,,{{\\pos(360,1112)}}점은 흐름 표시이며 실제 입자가 아닙니다')
(P/'proof.ass').write_text(header+'\n'.join(events)+'\n','utf-8-sig')
(P/'caption-timing.json').write_text(json.dumps({'method':'provider word boundaries shifted by detected leading trim; listening not performed','cues':timings},ensure_ascii=False,indent=2),'utf-8')
plan=json.loads((P/'shot-plan.json').read_text('utf-8'));plan['shots']=plan['shots'][:len(rows)];plan['audio_duration']=duration
if '--use-motion' in sys.argv:
 for shot in plan['shots']:shot['renderer']='Blender 5.2.1 Cycles OptiX / RTX 4060'
(P/'proof-shot-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),'utf-8')
if '--prepare' in sys.argv:print('PREPARED',duration);sys.exit(0)
if '--use-motion' not in sys.argv:
 count=576 if len(rows)==5 else 336
 missing=[f for f in range(1,count+1) if not (P/'frames'/f'f_{f:04}.png').exists()]
 if missing:raise RuntimeError(f'{len(missing)} required frames missing; first {missing[0]}')
 run(['-framerate','24','-start_number','1','-i',str(P/'frames'/'f_%04d.png'),'-frames:v',str(count),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(P/'motion-source.mp4')])
letters='abcde'[:len(rows)]
filters=[f'[0:v]split={len(rows)}'+''.join(f'[{c}]' for c in letters)]
for name,i,(a,b) in zip(letters,range(len(rows)),[(0,4),(4,9),(9,14),(14,19),(19,24)]):filters.append(f'[{name}]trim=start={a}:end={b},setpts=(PTS-STARTPTS)*{rows[i]["duration"]/(b-a):.9f},fps=24[v{i}]')
filters.append(''.join(f'[v{i}]' for i in range(len(rows)))+f'concat=n={len(rows)}:v=1:a=0,setsar=1[v]')
run(['-i',str(P/'motion-source.mp4'),'-filter_complex',';'.join(filters),'-map','[v]','-c:v','libx264','-preset','fast','-crf','18',str(P/'picture-retimed.mp4')])
dest=OUT/('구조공개_GPU_구현시험.mp4' if len(rows)==5 else '구조공개_3D_구현시험.mp4')
# Relative ASS path avoids Windows drive-colon escaping in libass.
proc=subprocess.run([str(FF),'-hide_banner','-y','-i','picture-retimed.mp4','-i','proof-mix.wav','-vf','ass=proof.ass','-map','0:v','-map','1:a','-t',f'{duration:.6f}','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(dest)],cwd=P,capture_output=True,text=True,encoding='utf-8',errors='replace')
if proc.returncode:raise RuntimeError(proc.stderr[-3000:])
(P/'thumbnail.ass').write_text(header+'\n'.join([
 'Dialogue: 2,0:00:00.00,0:00:02.00,Title,,0,0,0,,{\\pos(360,155)\\fs48}AI 서버의',
 'Dialogue: 2,0:00:00.00,0:00:02.00,Title,,0,0,0,,{\\pos(360,225)\\fs66}숨은 물길',
 'Dialogue: 2,0:00:00.00,0:00:02.00,Note,,0,0,0,,{\\pos(360,1150)\\fs25}냉각 원리 · 개념 모형'
])+'\n','utf-8-sig')
thumb=subprocess.run([str(FF),'-v','error','-y','-ss','12','-i','motion-source.mp4','-vf','setpts=PTS-STARTPTS,ass=thumbnail.ass','-frames:v','1',str(OUT/'구현시험_썸네일.png')],cwd=P,capture_output=True,text=True,encoding='utf-8',errors='replace')
if thumb.returncode:raise RuntimeError(thumb.stderr)
print('ASSEMBLED',dest,duration)
