# Hugging Face·Reddit·오픈소스 AI Shorts 심층 조사 — 통합 보고서 v8

조사 기준일: 2026-09-01 KST
범위: Hugging Face 모델·Spaces·공식 Agent Skills, Reddit 제작 워크플로와 실패 사례, GitHub 영상 생성·편집·모션 그래픽 프로젝트, 현재 Windows 호스트 실행성
주의: 이 문서는 조사·선정 보고서다. 설치, 대형 모델 다운로드, 유료 API 호출, 영상 생성, 자동 게시를 수행하지 않았다.

## 1. 먼저 결론

MCD 금융 쇼츠에 가장 적합한 방식은 **원클릭 생성형 영상 도구 하나로 60초 전체를 만드는 것**이 아니다.

```text
공식 금융 자료·계산
  → claim/source ledger
  → shot contract / DirectorScore
  → 결정론적 9:16 모션 그래픽
  → 선택적 2–4초 무문자 AI plate
  → 한글·숫자·차트·세계지도·M 아치 후합성
  → bbox/safe-zone/자막/ffprobe/full-decode QA
  → 사람 최종 검수 및 수동 게시
```

즉시 채택할 핵심은 기존 MoneyPrinterTurbo의 한국어 내레이션·검토된 SRT·Pillow/FFmpeg 기반을 유지하면서, 숫자와 차트를 frame-seek 가능한 결정론적 renderer로 강화하는 것이다. 여기서 “기존 기반”은 이전에 검증된 MCD 산출물의 증거를 뜻하며, 이번 조사에서 새 환경의 전체 dependency와 Edge TTS 경로를 재실행했다는 뜻은 아니다. 생성형 모델은 건물 내부, 매장 외관, 카메라 이동, 깊이감처럼 **텍스트가 없는 짧은 plate**에만 사용한다.

## 2. 추천 순위

| 등급 | 도구/Skill | MCD에서 맡길 일 | 판정 |
|---|---|---|---|
| NOW | MPT + Pillow/FFmpeg + reviewed SRT | 내레이션, 숫자·차트·SVG overlay, 최종 encode/QA | 기존 MCD artifact로 검증된 기본 경로 유지. 이 조사에서 clean-host 재렌더는 하지 않았으므로 dependency/Edge TTS smoke test는 다음 제작 전에 다시 수행 |
| PoC 0 | iart-ai `map-animation`·`chart-animation`·`short-form-video` Skills | GeoJSON/SVG 세계지도, 정확한 수치 차트, 9:16 pacing·safe area 지침 | Skill pack 자체 MIT. 지침·검증 규칙부터 선택적으로 이식하고 Remotion runtime은 별도 라이선스/Windows gate 통과 후 사용 |
| PoC 1 | HyperFrames `motion-graphics`·`hyperframes-animation` | stat, chart, logo reveal, world-map, seek-safe motion, snapshot QA | Apache-2.0. CLI 최소 도구와 별개로 공식 workflow 전제가 macOS Apple Silicon/Linux x64이므로 native Windows와 WSL 모두 실제 smoke test 전 HOLD |
| PoC 1B | Motion Canvas | MIT 기반 vector chart/count-up/line draw | CPU/Node형 대체 2D 후보. 이번 조사에서 Windows 설치·렌더를 하지 않았으므로 실행 완료로 보지 않음 |
| PoC 1D-browser | WebMotion + `webmotion` Agent Skill | frame-exact DOM/Canvas/Three.js scene, overflow·무동작 beat·asset/font 오류 lint, scene별 proof shot | MIT, 조사 snapshot 106 commits·6 stars·1 fork. MCD layout QA와 잘 맞지만 Windows WebCodecs/OffscreenCanvas MP4 smoke test 전에는 채택하지 않음 |
| PoC 2B | `make-blender-education-video` | fact/claim ledger, 4K approval frame 1장, Blender scene, ASS subtitles, frame-exact assembly | MIT, 8 commits·35 stars·9 forks. MCD 3D explainers와 가장 가까운 공개 Skill이지만 English-only·Blender hard prerequisite이며 현재 `blender`가 PATH에서 확인되지 않아 설치/로컬화 전 HOLD |
| Reference/PoC 2C | `VLM-Generation-Harness` | Blender greybox로 카메라·공간·cut timing을 좌표화하고 review/model render 분리·cut audit | MIT, 3 stars. paid/nonlocal Seedance 2.5 실측을 일반화하지 않고 greybox·audit만 독립 검토 |
| PoC 2 | HF SCoPE 또는 Wan2.2 first/last-frame | 2–4초 무문자 camera-controlled plate | 외부/ZeroGPU 1-shot smoke test만. seed·입력·모델 revision 고정 |
| PoC 3 | Kandinsky 5 Lite distilled16 | 빠른 5초 무문자 plate A/B | MIT, 2B. H100 속도·24GB offload 주장은 특정 환경값이라 현 Windows 실행 보장 아님 |
| PoC 4 | VACE 1.3B 또는 CamI2V | reference edit·저해상도 camera-motion 비교 | Apache/MIT. 480P/연구 해상도부터 검증, 금융 레이어는 후합성 |
| PoC 1C | Remotion + 공식 Skills | text measurement, caption JSON, MapLibre, frame-driven motion 규칙 | 현 라이선스상 개인·직원 3명 이하 영리 조직은 상업 영상 제작도 무료. 더 큰 조직·Remotion 파생 판매는 별도 조건이므로 사용 주체를 manifest에 기록 |
| Reference | OpenReels·Timeline Studio·Revideo | DirectorScore, dry-run, editable timeline, transactional diff, QA manifest | 구조만 차용; 전체 설치는 우선순위 낮음 |
| Reference | `vertical-video-editing-skills` | `FRAME.md` 디자인 토큰, anti-jitter camera contract, init→preview→lint→render→verify, rights/edit report | MIT이지만 HyperFrames 의존으로 동일 OS gate 적용. talking-head stacked split과 0.2초 컷 규칙은 MCD에 그대로 쓰지 않음 |
| Reference | `video-production-skill` | source-grounded brief, segmented narration, Manim/FFmpeg/Pillow, TTS timing, QC frame·archive contract | MIT, 10 commits·15 stars·2 forks의 초기 범용 교육영상 Skill. 세로 Shorts 전용이 아니며 Unix형 예시·선택적 hosting은 그대로 이식하지 않음 |
| Reference-only / HOLD code | Pluviobyte `ai-motion-director`·`reference-video-replica-qc` | motion thesis, beat graph, anti-PPT gate, full-frame reference/candidate diff | 638 stars·81 forks의 강한 관심 신호지만 저장소 루트 LICENSE를 확인하지 못함. 개념만 독립 재작성하고 코드·asset 복사/설치는 라이선스 확인 전 금지 |
| Reference | `animation-principles@video-motion-graphics` | staging, anticipation, easing, overlap, timing을 shot review vocabulary로 사용 | MIT·registry 1.8K installs. 144-Skill 묶음의 범용 원칙이며 MCD용 renderer/QA가 아님. glow·particle·overshoot 같은 예시는 의미가 있을 때만 사용 |
| Reference / API HOLD | `SamurAIGPT/open-ai-video-agent` curiosity 3D explainer | brief·shot·continuity·rights·cost gate의 계약 구조 | repo/Skill은 MIT지만 실제 생성은 muapi.ai MCP/REST provider가 필요. 2 stars·1 fork 초기 프로젝트이며 가격·보관·모델/output license 승인 전 호출 금지. 자체 28-Skill validator는 UTF-8 mode에서 통과했지만 한국어 Windows CP949 기본값에서는 실패 |
| Reference / API HOLD | `Anil-matcha/zack-d-films-ai-video-generator` | `beats.json`, turnaround sheet, keyframe approval, clip-by-clip retry, local FFmpeg assembly | MIT workflow이나 MuAPI·Veo 3.1·MiniMax speech 등 유료/외부 provider가 본체. 특정 크리에이터 스타일·음성 복제 대신 일반 3D explainer 구조만 차용 |
| HOLD | OpenChatCut·OpenMontage/OpenNolan | agent timeline/stage architecture | AGPL 경계와 초기 성숙도 때문에 코드 통합 금지 |
| REJECT | Vex | motion grammar는 좋지만 PolyForm Noncommercial | 수익화 가능 MCD 영상 dependency로 부적합 |
| REJECT | HunyuanVideo-1.5 | 생성 영상 | 모델 라이선스 Territory가 대한민국을 제외하므로 local inference·한국용 hosted output 모두 사용하지 않음 |
| REJECT | MiniMax H3 + `3d-animation-short-generator` | story-first 3D short workflow와 audio-video model | H3 Community License가 대한민국·미국·EU·영국을 제외하고 Output의 역외 사용도 제한. 한국에서는 model·hosted output·repo Skill을 설치·실행하지 않음 |
| REJECT | 로컬 Wan 14B/LTX 22B/Hunyuan/FramePack | 대형 생성 모델 | 현재 AMD iGPU, CUDA 없음, RAM 23.3GB, 디스크 여유와 불일치 |

## 3. Hugging Face에서 건진 것

### 공식 Skills

- `hf-cli`: Hub 검색·모델/Space/Job 관리의 공식 부트스트랩.
- `huggingface-best`: task와 benchmark 기반 후보 비교.
- `hf-mem`: 모델 weights를 전부 받지 않고 load memory를 추정하는 preflight.
- `huggingface-spaces`: Space build·debug·hardware·quota 운영.
- `huggingface-tool-builder`: 반복 가능한 HF API inventory 수집기를 만드는 데 적합.
- `huggingface-zerogpu`: `@spaces.GPU`, quota, process isolation, CUDA wheel 제약.

중요한 구분은, Hugging Face 공식 목록에 현재 “한 번에 Shorts를 완성하는 전용 Skill”이 있는 것이 아니라는 점이다. 공식 Skills는 모델/Space 검색, 메모리 사전 계산, API inventory, 평가, 배포·quota 같은 **실행·검증 기반**이다. 실제 쇼츠의 storyboard·layout·caption·chart·render 규칙은 HyperFrames·Remotion·iart·WebMotion 계열 Skill에서 가져오고, HF는 선택적 생성 plate provider로 연결하는 구조가 맞다.

공식 저장소는 Codex에서도 해당 Skill 폴더를 `.agents/skills`에 복사/심볼릭 링크해 사용할 수 있다고 안내한다. 이번 조사에서는 설치하지 않았다.

### Shorts·차트·지도 전용 공개 Skills

`find-skills` 검색에서 `iart-ai/tiktok-video-skills@short-form-video`와 `heygen-com/hyperframes@motion-graphics`가 상위권 후보로 나왔다. 설치 수는 품질 보증이 아니므로 원본 저장소와 Skill 내용을 다시 확인했다.

- iart-ai의 공개 허브는 Shorts, data-animation, map-animation을 포함한 15개 motion pack과 51개 Skill을 MIT로 공개한다. 결과물을 만드는 Skill은 frame still, contact sheet, MP4 probe를 포함한 deliver-and-verify loop를 표방한다.
- 다만 조사 시점에 `tiktok-video-skills`는 16 commits·8 stars, `map-animation-skills`는 7 commits·8 stars, `data-animation-skills`는 17 commits·5 stars인 초기 프로젝트다. 설치 수·보안 배지·별 수를 성숙도 보증으로 쓰지 않고, Skill 원문을 pinned snapshot으로 검토한 뒤 필요한 규칙만 가져온다.
- `map-animation`은 Google Earth Studio/AE 경로와 GeoJSON/SVG+D3/Remotion 경로를 분리한다. MCD에는 외부 지도 타일에 의존하는 위성형보다, 실제 투영과 좌표 배열을 쓰는 vector 경로가 적합하다. pin·route·label이 같은 projection을 공유하고 라벨은 수평·safe area 안에 두도록 요구한다.
- `chart-animation`은 숫자와 위치를 wall-clock이나 CSS transition이 아니라 현재 frame의 순수 함수로 계산하도록 한다. 이는 배당·자사주매입·beta·상대수익률 카드의 깜빡임과 seek 불일치를 막는 데 직접 유용하다.
- `short-form-video`는 9:16의 첫 3초, pattern interrupt, caption lane을 다루지만 “retention machine” 같은 서술을 바이럴 보장으로 해석하지 않는다. 실제 성과 규칙은 이 Skill이 아니라 게시 후 채널 데이터로 검증한다.
- Skill 지침의 MIT와 렌더 엔진의 라이선스는 별개다. iart-ai 예시는 Remotion을 사용한다. 현 Remotion 라이선스는 개인과 직원 3명 이하 영리 조직에 상업 영상 제작을 무료로 허용하므로 사용자 개인 PoC는 가능하지만, 회사 규모와 Remotion 파생물 판매 여부를 `license_manifest`에 기록한다. 이번 조사에서는 설치·렌더하지 않았다.

Remotion 본체도 현재 `/remotion-create`, `/remotion-markup`, `/remotion-maps`, `/remotion-captions`, `/remotion-render` 등 Codex 호환 공식 Agent Skills를 유지한다. 특히 `/remotion-maps`는 GeoJSON·MapLibre·Mapbox·CesiumJS 경로를 분리하므로, 세계지도 장면은 커뮤니티 예제만 복사하지 말고 공식 map Skill과 iart vector-map 규칙을 함께 검토하는 편이 안전하다.

별도의 MIT 후보인 `superhq-ai/webmotion`은 `skills/webmotion/`을 제공하며, 모든 애니메이션을 frame clock으로 계산하고 labelled sequence의 시작·중간·끝 proof shot을 만든다. `lint`는 두 tween의 동일 property 충돌, text overflow, 화면에 한 번도 나타나지 않는 entity, export hole, 잘못된 font stack, 움직임 없는 labelled beat를 non-zero exit로 잡는다. 이는 사용자가 반복해서 지적한 글자·카드 arrange 문제와 직접 맞닿아 있다. 조사 snapshot은 106 commits·6 stars·1 fork로, 개발 이력은 존재하지만 사용자층 신호는 아직 작다. Windows WebCodecs H.264/`OffscreenCanvas` export를 이번 조사에서 실행하지 않았으므로, HyperFrames/Motion Canvas와 동일한 6초 MCD scene으로만 비교한다. Three.js glTF와 frame-exact video도 지원하지만 처음부터 3D를 넣지 않고 layout lint가 실제로 충돌을 잡는지부터 본다.

Pluviobyte의 `ai-motion-director`와 `reference-video-replica-qc`도 이번 심층 검색에서 발견했다. 전자는 각 beat에 `state change`를 쓰고 최소 80%의 beat가 fade/slide-in을 넘는 실제 상태 변화를 갖도록 요구한다. 후자는 표본 screenshot만으로 복각 성공을 주장하지 않고 asset·runtime·delivery 세 gate와 전체 decode frame 비교를 둔다. 이는 현재 MCD의 “내용과 무관한 광택 효과”와 정적 카드 슬라이드를 거르는 데 직접 유용하다. 다만 조사 시점 GitHub 신호가 638 stars·81 forks여도 루트 LICENSE 파일이 404였으므로, 소스와 asset을 설치·복사하지 않고 `motion_thesis`, `beat_graph`, `anti_ppt_gate`, full-frame diff 개념만 독립 schema로 재작성한다.

`nopefallacy/vertical-video-editing-skills`도 9:16 전용 MIT Skill로 확인했다. 조사 snapshot은 2 commits·47 stars·7 forks라 관심 신호에 비해 구현 이력이 매우 짧다. 장점은 프로젝트별 `FRAME.md`, local font, eased camera의 anti-jitter 규칙, asset manifest, render gate와 edit report를 한 계약으로 묶는 점이다. 반면 HyperFrames를 필수 엔진으로 사용하므로 현재 Windows에서는 같은 OS gate를 통과해야 한다. 또한 talking-head 중심 stacked split과 0.2초까지 내려가는 컷 문법은 금융 데이터 설명에 과도할 수 있어 그대로 채택하지 않고, 디자인 토큰·카메라 안정화·검증 보고서만 차용한다.

### 모델/Space의 실제 판단

- Wan2.2 TI2V-5B는 Apache-2.0이며 first/last-frame과 짧은 I2V 후보로 의미가 있다. 공식 upstream과 ComfyUI의 VRAM 안내 조건은 서로 다른 실행 경로를 설명하므로 “8GB면 무조건 된다”로 단순화하면 안 된다.
- SCoPE는 Wan2.2 기반 camera-control 연구/Space로, preset trajectory·motion scale·FOV·seed를 노출한다. Blender blockout과 결합할 짧은 plate 후보로 가장 직접적이다.
- LTX-2.3은 강력하지만 모델 규모·32GB급 저VRAM 경로·가중치 라이선스 때문에 현재 호스트 로컬 기본값이 아니다.
- Kandinsky 5 Lite는 MIT 2B, 5초 I2V/T2V 변형과 16-step distilled 변형이 있어 외부 GPU 속도 비교 후보로 좋다. 다만 35초 수치는 H100 80GB 제작자 측 측정이고 “24GB offloading”도 특정 pipeline 관찰값이다.
- CamI2V는 MIT, 낮은 연구 해상도에서 정해진 회전·줌 움직임을 A/B하기 좋지만 최종 1080×1920 renderer로 보지 않는다.
- HunyuanVideo-1.5는 원 라이선스 Territory가 대한민국을 제외하므로 MCD 용도에서 **REJECT**한다.
- 공개 Space 검색 결과는 이름만 보고 사용할 수 없다. running 여부, license metadata, 공개 `agents.md`/API, quota, 입력 보관을 각각 확인해야 한다.

HF 상세 조사에는 중복 제거한 직접 링크 108개가 들어갔고, 최종 MCD shortlist는 11개로 좁혔다. 검색어 6개의 상위 후보를 중복 제거해 70개 Space를 API로 다시 확인한 표본에서는 RUNNING 24개(34.3%), RUNTIME_ERROR 27개(38.6%), BUILD_ERROR 7개(10.0%), SLEEPING 8개, PAUSED 3개, CONFIG_ERROR 1개였다. 39개(55.7%)는 카드의 license 필드가 비어 있었다. 이는 HF 전체를 대표하는 통계가 아니라 검색 상위 후보의 health 표본이지만, 제목·좋아요만 보고 채택하면 안 된다는 근거가 된다.

그 뒤 최신 카메라/영상 후보로 의도적으로 좁힌 별도 20개 Space는 2026-09-01 12:45 KST 재확인에서도 20/20 RUNNING·zero-a10g였지만, 다수가 license field 공란이고 대부분 커뮤니티 fork였다. API·canonical page·`agents.md` endpoint는 각각 20/20 접근됐으나 실제 generation POST는 보내지 않았다. 첫 표본과 모순이 아니라 **선별 방식이 다른 snapshot**이다. 실제 사용 직전에는 stage·hardware·SHA·license·API schema를 다시 고정해야 한다.

두 공개 API는 schema까지 확인했다.

- `multimodalart/wan-2-2-first-last-frame`: start/end frame, 0.5–5.1초, steps·guidance·seed를 받는다. 기본 `randomize_seed=true`이므로 반복 가능한 Skill은 이를 false로 고정해야 한다.
- `TencentARC/scope-camera-video-generation`: dolly/orbit/crane/flyover 등 16개 typed trajectory, steps 4–16, motion scale, FOV, seed를 받는다. 자유 문장 카메라 지시보다 shot contract에 넣기 쉽다.

반대로 LTX-2.3 계열 일부 Space의 `agents.md`는 비인증 요청에서 401이었다. `Agents` 표시가 곧 익명 공개 실행 가능을 뜻하지 않는다. 실제 생성 job은 제출하지 않았다.

### ComfyUI·외부 영상 API Skills 추가 판정

Skill registry에서는 `runcomfy-agent-skills@video-inpainting`과 `MCKRUZ/ComfyUI-Expert@comfyui-video-pipeline`도 노출됐다. 설치 수는 검색 노출 신호일 뿐 open-source local 실행이나 품질 보증이 아니다.

- `runcomfy-agent-skills`의 Skill 문서는 MIT지만 실제 실행은 `@runcomfy/cli` 설치, 로그인/token, RunComfy 외부 endpoint, 원본 영상 URL 업로드와 model별 비용·약관을 요구한다. 즉 “오픈 Skill”과 “무료 local model”은 다르다. MCD에는 `provider adapter` 참고 자료로만 두고, 가격·파일 보관·model/output license·한국 사용권을 승인하기 전에는 호출하지 않는다.
- `ComfyUI-Expert`는 Windows launcher와 REST polling, VRAM inventory, workflow 분리를 제공하는 흥미로운 초기 설계다. 그러나 조사 snapshot은 12 commits이고, Skill 원문이 Wan 2.2와 Wan 2.1의 1.3B/14B 이름을 혼용하며 `FramePack 60초/6GB`, `HunyuanVideo 1.5 대안` 등을 넓게 단정한다. 특히 HunyuanVideo-1.5의 한국 제외 라이선스와 충돌하므로 설정값·모델 선택을 그대로 신뢰하지 않는다. ComfyUI 설치가 실제 확인되고 각 model card/revision/license를 다시 검증할 때만 inventory·REST orchestration 개념을 차용한다.
- `OpenClip-App/agent-skills`는 긴 원본 영상을 captioned short로 재편집하는 데 유용하지만, Skill 파일만 MIT이고 실제 처리는 hosted commercial OpenClip MCP·OAuth account를 사용하며 clipping은 subscription 대상이다. 새 MCD 인포그래픽 장면을 설계하는 주 엔진은 아니다. 향후 실사 인터뷰나 긴 기업분석 원본이 생길 때 데이터 업로드·가격·virality-score 정의를 별도 평가한다.
- `SamurAIGPT/open-ai-video-agent`에는 `curiosity-3d-explainer`, `youtube-shorts`, `storyboard-to-video`, `character-continuity`, `video-assembly` 등 28개의 분리된 MIT Skill과 16개 logical capability가 있다. 3D explainer Skill은 script freeze, shot별 source/acceptance check, recurring object reference sheet, keyframe approval, continuity log, 권리·비용 receipt, 최종 draft-only/no-publish를 요구해 production contract가 좋다. 자체 `validate_package.py`는 `PYTHONUTF8=1`에서 28 Skills/16 capabilities를 통과했지만, 한국어 Windows 기본 CP949에서는 `read_text()`가 encoding을 지정하지 않아 README를 읽다 `UnicodeDecodeError`가 났다. 즉 Windows patch 없이 그대로 설치할 후보가 아니다. 또한 영상 생성은 muapi.ai provider에 연결되므로 가격·업로드 보관·실제 underlying model과 output license가 승인되기 전에는 API를 호출하지 않는다. 조사 snapshot은 2 stars·1 fork·1개 최신 commit의 매우 초기 프로젝트다.
- `Anil-matcha/zack-d-films-ai-video-generator`는 사용자가 보여준 3D curiosity explainer 계열에 가장 노골적으로 맞춘 공개 Skill이다. `beats.json`→character/object turnaround→shot keyframe 승인→각 keyframe I2V→voice/BGM→local FFmpeg 9:16 assembly의 두 승인 gate 구조는 유용하다. 그러나 생성 본체는 MuAPI의 Nano Banana/Flux, Veo 3.1, MiniMax speech 같은 외부 endpoint이고 voice cloning과 특정 크리에이터 스타일 복제를 기본값으로 둔다. 따라서 코드를 설치하거나 스타일/음성을 모방하지 않고, MCD 고유의 기업·부동산 시각 언어로 `beat contract + anchor sheet + keyframe approval + clip retry`만 독립 재작성한다. Reddit의 수익·조회수 자기보고는 affiliate/판매 동기가 섞일 수 있어 성과 근거로 쓰지 않는다.

결론적으로 ComfyUI Skill은 현재 PC의 AMD iGPU에서 대형 로컬 생성 문제를 해결하지 않는다. 대형 model downloader나 community node 설치를 먼저 하지 말고, 생성 plate가 꼭 필요할 때만 외부 GPU 1-shot provider를 명시적으로 승인받아 비교한다.

Skill registry에서 MiniMax 공식 `3d-animation-short-generator`도 확인했다. 이 Skill은 brief→story outline→character/environment card→초 단위 shot table·audio cue·spatial anchor→storyboard→single-shot generation→assembly라는 순서를 제안해 사용자가 원하는 3D 설명형 쇼츠의 production 사고와 가깝다. 그러나 MiniMax H3 원 라이선스의 Excluded Territories에 **Republic of Korea**가 명시되고, H3 Works와 Output을 Applicable Territory 밖에서 사용·표시하지 못하도록 한다. 모델 저장소도 약 498GB라 현재 PC와 맞지 않는다. 따라서 한국에서는 모델과 저장소 Skill을 설치·실행·복사하지 않고, `shot_id / 초 단위 지시 / spatial anchor / audio cue / self-check gate` 같은 일반 제작 원리는 독립 계약으로 새로 작성한다.

### Blender 기반 공개 Skills — 참고 영상과 가장 가까운 발견

`sunxiayi/make-blender-education-video-skill`은 이번 조사에서 사용자 참고 영상과 가장 직접적으로 닮은 permissive 후보였다. 사실 확인→claim ledger→재사용 가능한 Blender 자원 라이선스 확인→대표 4K frame 1장 승인→animation→큰 ASS subtitle→frame-exact master와 최종 media QA를 강제한다. MIT이며 실제 demo 4종을 연결하지만 조사 snapshot은 8 commits·35 stars·9 forks이고 Skill이 English cinematic explainer만 허용한다. 현재 shell에서도 `blender` 실행 파일이 PATH에서 확인되지 않았다. 따라서 지금 설치하지 않고, 한국어 내레이션·9:16·금융 source ledger·MCD safe zone으로 로컬화 가능한지 다음 PoC에서 평가한다.

`7ohnson/VLM-Generation-Harness`는 Blender greybox를 사람용 review render와 생성 모델용 무문자/무윤곽 render로 나누고, camera·object·cut timing을 좌표와 `scene.py`에 고정한다. `check_prompt.py`, `verify_cuts.py`, contact sheet, facts export가 포함된 MIT harness라 “live Blender session이 아니라 재현 가능한 scene.py가 source of truth”라는 규칙이 강점이다. 다만 16초/7-shot에서 cut 오차 최대 0.07초라는 수치는 Seedance 2.5 단일 self-report이고, 작성자도 긴 shot에서 누락·추가 cut 실패를 기록한다. MCD에는 multi-shot AI 생성보다, 건물/아치/임대 흐름의 camera previz와 asset rectangle을 고정하는 용도로만 검토한다.

이 두 후보는 `3D를 더 많이 넣자`가 아니라 `3D를 넣기 전에 위치·카메라·수치 lane을 고정하자`는 결론을 강화한다. Blender 설치·Skill 복사는 별도 승인을 받고, 첫 PoC는 6초짜리 매장 단면 한 장면만 만든다.

별도로 `Aaryan-Kapoor/video-production-skill`도 원문을 확인했다. MIT이고 source-grounded brief→segmented narration→Kokoro 등 TTS→Manim/FFmpeg/Pillow visual→audio sync→QC frame→archive 흐름을 제공한다. Python 3.10+·FFmpeg가 필수이고 Manim·Kokoro·Poppler·Pillow는 권장이다. 조사 snapshot은 10 commits·15 stars·2 forks로 초기 단계이며 9:16 safe-zone, scene bbox, 금융 claim-to-screen diff는 없다. 따라서 새 주 엔진이 아니라 `job workspace`, segment timing, 결과물 backup 규칙만 현재 Skill과 비교한다. Unix `export`/`source` 예시와 Tailscale hosting은 Windows용으로 검증하거나 이번 범위에서 제외해야 한다.

## 4. Reddit에서 반복된 제작 패턴

커뮤니티 게시물은 공식 문서나 품질 보증이 아니라 제작자 자기보고다. 다만 여러 독립 글에서 다음 패턴이 반복된다.

세 Reddit 증거 원장은 **139행·고유 직접 URL 138개**다. A 직접 열람 115행/114개 URL, B 검색·교차게시물 19행/19개, C 제한·자기홍보 3행/3개, A/C 혼합 2행/2개로 분리했다. 부록과 제한 기록을 모두 합친 보고서 전체 고유 URL 문자열은 155개지만, 이것이 155개의 독립 강증거라는 뜻은 아니다. 이 중 MCD 배치·모션·금융 QA에 직접 전이 가능한 A급 원문 13개를 다시 선정해 “배울 점/쓰지 말 것” 표로 남겼다.

1. Blender에서 object·camera·timing을 먼저 배치하고, key frame/depth/참조 영상을 생성 모델에 넘긴다.
2. 전체 영상을 한 번에 만들지 않고 장면을 독립 clip으로 분리한다. 실패하면 해당 clip만 다시 만든다.
3. AI 영상 모델은 텍스트·숫자·차트에 약하므로 Remotion/After Effects/코드 합성으로 처리한다.
4. 세로 영상의 실패는 “효과가 적어서”보다 floating text, zero-easing camera, 의미 없는 motion, caption overlap, 플랫폼 UI 침범에서 많이 발생한다.
5. viral 제작자 자기보고는 추천 시스템·주제·계정 상태가 섞여 있으므로 조회수 인과관계로 해석하지 않는다.

성공 사례만 본 것은 아니다. LTX-2.3 depth/first-last-frame 워크플로에서도 3초 이후 reference drift, depth가 색에 번지는 현상, 흰 프레임, flicker, 카메라 추종 실패가 보고됐다. 반면 비교적 성공한 사례도 RunPod와 공식 IC-LoRA workflow를 쓰고 최종 후반 작업을 별도로 했다. 따라서 Blender depth를 넣으면 구조가 “보장”된다고 쓰지 않고, **짧은 1-shot 테스트에서 camera adherence·flicker·중간 프레임 drift를 측정**해야 한다.

비용·속도 주장도 극단적으로 흩어졌다. 8–12GB 카드에서 짧은 clip이 수분이라는 글과 30–60분이라는 글이 동시에 있었고, `$0` 제작 사례도 전기·GPU 감가·재시도·사람의 일주일 노동을 제외했다. 그래서 보고서의 비용은 benchmark가 아니라 범위 신호로만 사용하고, 실제 후보는 동일 4–6초 shot으로 재측정해야 한다.

조회수/retention도 서로 반대 사례가 존재했다. 90% 안팎 retention과 수십만 view가 함께 나온 자기보고가 있는 반면, 100–200% retention인데 1–2천 view에서 멈춘 사례도 있었다. 따라서 “retention X%면 바이럴” 같은 Reddit 공식을 채택하지 않는다. YouTube 공식 정책상 핵심 리스크는 AI 자체보다 원본성 없는 대량·반복·템플릿형 `inauthentic content`와 의미 없는 재사용이다.

정책상 더 중요한 새 경계도 있다. 현재 YouTube 수익화 정책은 AI 생성 인물이 금융·투자 조언을 전문가처럼 제공하는 채널을 수익화 불가 예시로 든다. 따라서 MCD 영상은 합성 AI 진행자/팟캐스트 호스트가 “지금 사라”라고 말하는 형식을 피하고, 출처가 보이는 **교육적 기업 분석 + 반대 위험 + 조건부 판단**으로 구성해야 한다. 현실처럼 보이는 AI 매장/장소 영상을 쓰면 altered/synthetic disclosure도 검토한다. YouTube는 적절한 AI 공개 자체가 도달이나 수익화 자격을 제한하지 않는다고 안내한다.

## 5. 다음 MCD 영상에 적용할 shot contract

| shot | 무문자 시각 plate | 결정론적 overlay | 필수 QA |
|---|---|---|---|
| hook | 매장/도시 slow push | 한 문장 hook | 첫 2초 안 의미 있는 변화 |
| property | 단면 건물·임대 흐름 | rent/royalty/franchise | asset 간 reserved rectangle 충돌 0 |
| global | vector world map + node sequence | 지역/매장 데이터 | 지도·카드·자막 lane 완전 분리 |
| return | split-screen cashflow | 배당·자사주매입·환원률 | 기간·분모·출처 연결 |
| relative | line chart draw | beta·S&P 500/QQQ 대비 | 기간·조정주가·benchmark 명시 |
| valuation | historical band | 현 배당수익률 percentile | trailing/forward 정의 |
| risk | 금리·가맹 비용·소비 둔화 | 위험 3개 | 추천 단정 금지 |
| close | clean M 아치 geometry | 조건부 결론·면책 | 하단 UI dead-zone 밖 배치 |

## 6. 반드시 추가할 자동 품질 게이트

- `safe_rect`와 `reserved_rects`를 scene schema에 필수화한다.
- 모든 text/card/chart/building/map bbox가 서로 겹치면 render fail로 처리한다.
- 숫자와 단위는 source ledger의 `claim_id`에서만 나온다.
- 10% 확대 폰트를 유지하되 최소 글자 크기와 최대 2줄을 동시에 만족하지 못하면 카드를 분할한다.
- 첫 2초 hook 변화, 평균 shot 길이, 1–3초마다 의미 있는 시각 변화를 검사한다.
- opening/signature/final hold와 자막 전환 frame의 contact sheet를 만든다.
- 1080×1920, 30fps, H.264/AAC, duration, audio, freeze, full decode를 검사한다.
- YouTube/Instagram/X는 UI 위치가 달라 하나의 safe zone을 공통 정답으로 쓰지 않는다.

### 현재 `moneyprinterturbo-video`와의 실제 gap

현재 Skill은 이미 evidence freeze, asset license ledger, 한 장면 한 아이디어, quiet caption band, 실제 export manual review, full decode를 요구한다. v7 개별 검증에서는 2초 간격 contact sheet와 freeze detection도 별도로 수행했다. 방향은 맞다. 다만 공용 `validate_video.py`를 코드로 확인하면 다음이 자동화되지 않았다.

- 문서에는 30fps를 요구하지만 validator가 frame rate를 읽어 실패시키지는 않는다.
- full decode는 하지만 freeze/duplicate-frame 검사가 공용 validator에 들어 있지 않아 영상별 수동 명령에 의존한다.
- review frame은 1초·중간·끝 세 장뿐이라 모든 scene boundary와 dense caption 전환을 자동 추출하지 않는다.
- scene schema, text/card/chart bbox, platform별 safe rectangle을 입력으로 받지 않는다.
- 화면 숫자를 source ledger와 대조하는 OCR/data diff가 없다.

그러므로 새 엔진을 붙이는 것보다 먼저 `scene-manifest.json`과 `layout_qa.py`를 추가해 기존 QA 문구를 executable gate로 만드는 편이 우선이다. HyperFrames/Timeline/OpenReels에서 가장 가치 있는 부분도 바로 이 manifest·snapshot·diff 구조다.

### 조사 결과를 Skill로 옮길 최소 단위

```text
moneyprinterturbo-video/
├─ references/
│  ├─ scene-contract.md          # shot/claim/asset/safe rectangles
│  ├─ deterministic-motion.md    # frame-only timing, easing, camera limits
│  └─ generated-plate-policy.md  # textless 2–4s only, provider/license HOLD
├─ schemas/
│  ├─ scene-manifest.schema.json
│  ├─ source-ledger.schema.json
│  └─ provider-run.schema.json
└─ scripts/
   ├─ layout_qa.py               # bbox overlap + platform safe zones
   ├─ frame_probe.py             # scene boundaries/contact sheet/freeze
   └─ claim_diff.py              # 화면 수치와 source ledger 대조
```

`research-only`, `deterministic-motion`, `generated-plate`, `final-verify` 네 mode를 분리한다. `generated-plate`는 모델 revision·license·비용·업로드 데이터 보관·seed가 하나라도 공란이면 HOLD한다. 렌더 엔진을 바꾸더라도 manifest와 QA output은 같아야 하며, 자동 게시 기능은 기본 범위에 넣지 않는다.

## 7. 채택 전 1–2주 PoC 계획

1. 동일한 6초 MCD 장면을 기존 Pillow/FFmpeg, Motion Canvas, HyperFrames로 각각 만든다.
2. WebMotion은 네 번째 후보로 같은 장면을 만들고 `shoot`/`lint`가 overflow·무동작 구간·asset/font 오류를 실제로 잡는지 확인한다.
3. 렌더 시간, 수정 시간, bbox 오류, 글자 선명도, Windows 실행 난이도를 비교한다.
4. Blender blockout 1개를 만들어 SCoPE/Wan first-last-frame에 1회씩 넣어 camera adherence와 artifact를 비교한다.
5. 생성 plate에서는 모든 글자·숫자·브랜드 로고를 제거한다.
6. 승자는 “화려함”이 아니라 수정 가능성·충돌 0·data fidelity·반복 렌더 재현성으로 고른다.

## 8. 조사 증거와 한계

- GitHub 저장소·공식 Skills·HF model card/Space API와 Reddit 게시물을 조사일 기준으로 확인했다.
- 별 수·설치 수·upvote는 건강성/관심의 보조 신호일 뿐 품질 또는 조회수 보장이 아니다.
- Reddit 사례는 creator self-report로 표기하고, 공식 모델 card·license·hardware 문서와 분리했다.
- 공개 HF Space 상태와 quota는 바뀔 수 있어 실제 실행 직전에 다시 확인해야 한다.
- 이 조사에서는 새 패키지·Skill·plugin·모델을 설치하지 않았고 영상도 덮어쓰지 않았다.

## 9. Luna 팀 실행 기록

초기 `luna-team-build` planning council은 7개의 write-disjoint research track을 선택했다. 선택된 예측 스케줄은 worker wall 3,900초, 전체 6,180초, predicted capacity utilization 0.945, balance ratio 0.897, max/median 1.054였다. 그러나 실행 시점에 Windows session의 전역 live-worker ceiling 7을 다른 작업이 이미 점유해 runner가 즉시 실패했고, 7개 worker는 모두 `pending`에서 시작하지 못했다. 이 실패한 run을 완료 작업으로 계산하지 않는다.

대체 실행은 root가 통합·정책·Skill 검색을 맡고 3개의 `gpt-5.6-luna / max / fast` 작업을 병렬로 운영했다.

```text
GPT-5.6 Sol / max — root integration
├─ hf_models_spaces — HF 모델·Spaces·공식 Skills·라이선스·API schema
├─ reddit_workflows_risks — Reddit 제작·실패·비용·정책 경계
└─ github_skill_local — GitHub 도구·재사용 Skill·Windows 실행성·통합 gap review
```

초기 runner는 0/7 worker가 시작된 상태에서 실패했고, 대체 병렬 조사의 3/3 Luna 작업은 모두 완료됐다. 실제 조사 구간은 2026-09-01 11:59:10~13:00:17 KST로 **61분 07초**이며, 이후 최종 문서 QA를 추가 수행했다. 산출물은 HF model/Spaces, Reddit workflow/risk, GitHub Skill/local feasibility, 통합 gap review와 root 교차검증으로 나뉜다. fallback collaboration에는 runner utilization telemetry가 없으므로 실제 utilization 수치를 임의로 만들지 않는다.

## 10. 핵심 출처

### 공식·원본

- https://github.com/huggingface/skills
- https://huggingface.co/docs/hub/en/spaces-agents
- https://huggingface.co/docs/hub/en/spaces-mcp-servers
- https://huggingface.co/docs/hub/spaces-zerogpu
- https://huggingface.co/docs/hub/spaces-gpus
- https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B
- https://huggingface.co/TencentARC/SCoPE
- https://huggingface.co/tencent/HunyuanVideo-1.5/blob/main/LICENSE
- https://github.com/heygen-com/hyperframes
- https://github.com/heygen-com/hyperframes/blob/main/skills/motion-graphics/SKILL.md
- https://github.com/iart-ai/motion-skills
- https://github.com/iart-ai/tiktok-video-skills/blob/main/skills/short-form-video/SKILL.md
- https://github.com/iart-ai/data-animation-skills/blob/main/skills/chart-animation/SKILL.md
- https://github.com/iart-ai/map-animation-skills/blob/main/skills/map-animation/SKILL.md
- https://github.com/remotion-dev/remotion/blob/main/LICENSE.md
- https://github.com/remotion-dev/remotion/blob/main/packages/skills/README.md
- https://github.com/superhq-ai/webmotion
- https://github.com/nopefallacy/vertical-video-editing-skills
- https://github.com/prime-skills/runcomfy-agent-skills
- https://github.com/MCKRUZ/ComfyUI-Expert
- https://github.com/OpenClip-App/agent-skills
- https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/3d-animation-short-generator/SKILL.md
- https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE
- https://github.com/sunxiayi/make-blender-education-video-skill
- https://github.com/7ohnson/VLM-Generation-Harness
- https://github.com/Aaryan-Kapoor/video-production-skill
- https://github.com/Pluviobyte/video-production-skills
- https://github.com/Pluviobyte/video-production-skills/blob/main/ai-motion-director/SKILL.md
- https://github.com/Pluviobyte/video-production-skills/blob/main/reference-video-replica-qc/SKILL.md
- https://github.com/dylantarre/animation-principles
- https://github.com/SamurAIGPT/open-ai-video-agent
- https://github.com/Anil-matcha/zack-d-films-ai-video-generator
- https://github.com/motion-canvas/motion-canvas
- https://github.com/tsensei/OpenReels
- https://github.com/MartinDelophy/ai-video-editor/blob/main/skills/edit-timeline-studio/SKILL.md
- https://support.google.com/youtube/answer/1311392
- https://support.google.com/youtube/answer/14328491

### Reddit 제작자 자기보고·커뮤니티 신호

- https://www.reddit.com/r/comfyui/comments/1t4iqrr/i_used_blender_as_a_layout_tool_for_ai_video/
- https://www.reddit.com/r/comfyui/comments/1s2v55m/nvidia_video_generation_guide_full_workflow_from/
- https://www.reddit.com/r/comfyui/comments/1vsgewj/made_a_90second_ai_short_film_locally_in_about_3/
- https://www.reddit.com/r/comfyui/comments/1v2i0ab/blender_depth_to_final_video_with_ltx23_iclora/
- https://www.reddit.com/r/StableDiffusion/comments/1twg8v8/ltx_23_iclora_union_depth_map_bleeding_into_video/
