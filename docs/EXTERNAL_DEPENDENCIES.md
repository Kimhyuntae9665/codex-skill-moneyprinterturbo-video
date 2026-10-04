# 외부 의존성과 재배포 범위

이 패키지는 스킬과 제작 도구를 구분합니다. 모든 참조 스킬 65개는
`distribution/source-inventory.json`에 기록되어 있습니다. 그중 53개는 전체
지원 파일과 개별 라이선스를 동봉하고, 아래 12개는 공식 upstream 설치로 연결합니다.

## Remotion 공식 스킬

- 저장소: https://github.com/remotion-dev/skills
- 고정 커밋: `0b5db9daae40f42c73544d1cc0a8c733bd530eaa`
- 경로: 각 `skills/<skill-name>/`
- 대상: remotion-best-practices, remotion-captions, remotion-create,
  remotion-docs, remotion-interactivity, remotion-maps, remotion-markup,
  remotion-multimedia, remotion-render, remotion-saas, remotion-studio,
  remotion-upgrade.
- 확인일: 2026-10-04. 해당 스킬 저장소에는 재배포 라이선스 파일이 없어 원문을
  본 배포에 복사하거나 MIT로 표시하지 않았습니다. 공식 README는 사용자가
  설치하는 경로를 제공합니다. 설치기는 공식 고정 커밋을 사용자 PC에 받아
  이 12개 폴더의 전체 파일을 설치합니다.
- 일반 공식 설치 안내: [Agent Skills README](https://github.com/remotion-dev/skills/blob/0b5db9daae40f42c73544d1cc0a8c733bd530eaa/README.md).
  그 안내의 `npx skills add remotion-dev/skills`는 최신판을 설치하므로 이
  저장소의 재현용 고정 커밋 설치와 버전이 다를 수 있습니다.
- Remotion 실행 엔진의 [별도 라이선스](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)는
  스킬 문서의 재배포 허가로 간주하지 않습니다. 조직 규모와 사용 방식에 따라
  유료 라이선스가 필요할 수 있으므로 실제 사용 전에 현재 조건을 확인하세요.

## 외부 실행 엔진·서비스

| 구성 요소 | 역할 | 포함/설치 |
| --- | --- | --- |
| [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo/tree/eb8c23757e098a07bbcd93b3b50e252fc8d1869a) | TTS·자막·영상 조립 | 수정 helper와 MIT 고지 포함. 전체 엔진은 최초 실행 시 고정 커밋 설치 |
| [FFmpeg](https://ffmpeg.org/download.html) | 인코딩·탐색·검수 | 실행 파일은 별도 설치; 빌드별 라이선스 확인 |
| [Manim Community](https://www.manim.community/) | 재현 가능한 데이터 애니메이션 | 예제의 pyproject/uv.lock 포함; 실행 패키지 별도 설치 |
| [Blender](https://www.blender.org/download/) | 3D·greybox | Python 소스·예제 포함; 실행 파일·GPU 드라이버 별도 설치 |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | HTML 영상 | 동봉 스킬의 Apache-2.0 고지 유지; Node 실행 환경 별도 설치 |
| [Inkscape](https://inkscape.org/release/) | SVG의 PNG 변환 | 로고 흐름도 renderer는 동봉; Inkscape 실행 파일 별도 설치 |
| [Hugging Face](https://huggingface.co/docs) | 모델 선정·호스팅·생성 후보 | 선택용 스킬 포함; 가중치·계정·토큰·추론 환경 별도 준비 |
| LLM, stock-media, TTS 서비스 | 온라인 생성 | 키·구독 미포함; 선택한 제공자에 한해 별도 설정 |

유료 모델/서비스를 자동 결제하지 않습니다. API 키, 쿠키, 계정 설정,
원격 서버 접속 정보는 배포하지 않습니다. 실제 공식 제품 영상의 출처 표시는
재사용 허가를 대체하지 않습니다. 설치 스킬을 통해 찾은 자료는 사용 조건을
확인하고 최종 영상의 권리 원장에 기록해야 합니다.

## 버전·원문·라이선스

`source-inventory.json`에는 로컬 원본 파일별 해시, 변경 이유, 확인 가능한
upstream 설치 커밋이 있습니다. upstream이 확인되지 않은 항목은 설치된
스냅샷이라고 표시하며 임의의 공식 버전을 주장하지 않습니다. 전체 공개
패키지 해시는 `file-manifest.json`, 외부 링크 목록은 `reference-catalog.json`입니다.

과거 제작 예제는 저장된 시점의 데이터·자막·검수 기록입니다. 최신 금융
수치나 현재 영상 승인 상태로 재사용하지 마세요. 저작물별 라이선스는 본체의
THIRD_PARTY_NOTICES, 각 스킬 LICENSE/NOTICE, 사진 ATTRIBUTION과 폰트 OFL을
함께 따릅니다.
