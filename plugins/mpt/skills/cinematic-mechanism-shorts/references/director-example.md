# 원본 연출 예제: AI를 식히는 뜨거운 물

이 문서는 재사용 가능한 **제작 설계 예제**다. 아래 90초 편집안 전체가 생성·렌더되었다는 뜻이 아니다. 이번 실제 실행 범위는 README의 실행 기록을 따른다. 원작 채널의 대본·영상·인물을 재사용하지 않는다.

## 질문과 사실의 골격

- 질문: 서버를 식히는데 왜 꼭 얼음처럼 차가운 물이 필요하지 않을까?
- 첫 인상: 뜨거운 호스와 차갑게 유지되어야 할 것 같은 칩의 대비.
- 숨은 원리: 열을 받아 이동시키는 냉각판과 폐회로. 피부가 느끼는 차가움과 칩의 운전 조건은 다르다.
- 답: 냉각수의 절대 온도만 보는 것이 아니라 장비의 검증된 운전 조건과 열을 밖으로 버리는 경로를 본다.
- 범위: 모든 서버가 아니라 NVIDIA가 설명한 Rubin 액체 냉각 사례와, 별도로 표시한 일반 개념 모형.
- 직접 읽은 1차 자료: [NVIDIA, 2026-06-21](https://blogs.nvidia.com/blog/liquid-cooling-ai-factories/). 45°C 유입·약 55°C 유출, 냉각판, 폐회로, 기후·설계에 따른 외기 냉각 조건을 구분한다. 회사의 효율성 홍보 문구를 독립 실험 결과처럼 말하지 않는다.

## 원작의 기능을 우리 소재에 옮긴 대본 뼈대

1. **익숙한 직관:** “서버를 식힌다는데, 마흔다섯 도의 냉각수를 넣습니다.” 화면에서 사례 범위를 먼저 명시한다.
2. **의문:** “사람에게는 꽤 따뜻하죠. 그런데 칩에도 너무 뜨거운 걸까요?”
3. **상상 속 해법:** “무조건 더 차갑게 만들면 좋을 것 같지만, 냉각수를 차갑게 만드는 데도 에너지가 듭니다.” 실제 실패 사건을 꾸며 넣지 않는다.
4. **공간 공개:** “여기서는 칩 위에 물을 붓는 게 아닙니다. 칩에 붙은 금속판 안으로 냉각수가 흐르죠.” 콜드플레이트 방식이라는 범위를 유지한다.
5. **원인과 결과:** “칩의 열이 금속판으로 넘어오고, 그 열을 냉각수가 받아 갑니다.”
6. **하나의 흐름 추적:** “데워진 냉각수는 밖으로 나가 열을 넘기고, 다시 돌아옵니다.” 다른 회로로 전환할 때는 같은 물방울이 벽을 통과하는 그림을 쓰지 않는다.
7. **반전의 답:** “손에 차가운 물이 필요한 게 아닙니다. 장비가 허용하는 온도 안에서, 열을 계속 옮길 수 있으면 됩니다.”
8. **조건과 결과:** “기후와 설계가 맞으면 바깥 공기로 열을 버리며 냉동기 사용을 줄일 수 있습니다.” 사막과 서늘한 지역이 같다는 식으로 확대하지 않는다.
9. **처음의 풍경으로 복귀:** “그래서 이 호스는 서버에 냉기를 배달하는 관보다, 열을 밖으로 운반하는 길에 가깝습니다.”

이 문장을 전부 기계적으로 읽지 않는다. 실제 음성을 만든 뒤 반복을 줄이고 이해에 필요한 동작 시간을 확보한다. 주가·P/E·주주환원은 이 질문을 해결하는 데 필요하지 않으므로 자동으로 끼워 넣지 않는다.

## 약 90초를 목표로 한 편집 설계

아래 시간은 **기획 배분**이며 합성된 음성의 실측 타임코드가 아니다. 최종 타임라인 JSON에는 실제 음성 길이를 사용한다.

| 기획 구간 | 시청자가 새로 알 것 | 주 동작과 카메라 | 생성 경로 / 핵심 검수 |
|---|---|---|---|
| 0–6초 | 따뜻한 냉각수라는 역설 | 호스에서 온도 측정기로 접근 | 사실적 I2V; 숫자는 후합성 |
| 6–12초 | 사람의 감각과 장비 조건은 다름 | 작업자 손과 장비의 크기 관계 | 독창적 작업자 기준 이미지; 접촉 확인 |
| 12–19초 | 차갑게 만드는 일도 비용 | 별도 냉각 장치가 작동하는 개념 컷 | 가상 비교임을 표시; 절감 수치 임의 생성 금지 |
| 19–26초 | 냉각판은 칩 위의 다른 부품 | 보드 → 칩 → 금속판 순서로 분해 | 3D로 부품 순서 통제 |
| 26–34초 | 액체는 금속판 안에 있음 | 뚜껑을 옆으로 이동시켜 통로 공개 | 결정적 구조는 3D; 뚜껑 가림 검사 |
| 34–43초 | 열이 액체로 전달됨 | 측면 단면에서 열 전달 표시 | 정확한 단면 + 후합성; 실제 입자처럼 오인 금지 |
| 43–52초 | 열을 받은 액체가 나감 | 통로를 따라 호스 출구로 이동 | 연결된 경로; 입출구 바뀜 검사 |
| 52–60초 | 장비 밖에도 회로가 있음 | 호스 → 분배·열교환 장치로 확장 | 같은 공간 기준 유지 |
| 60–68초 | 열교환은 회로 구분이 중요 | 벽 양쪽 두 흐름과 열 이동 | 물질이 벽을 통과하는 연출 금지 |
| 68–76초 | 외부로 열을 버리는 조건 | 건물 외부 냉각기로 시선 이동 | 환경 전경은 T2V; 기후 조건 자막 |
| 76–83초 | 차가움보다 운전 조건 | 처음의 측정기를 다른 의미로 재방문 | 후합성 숫자·범위 동일 유지 |
| 83–90초 | 처음 질문의 답 | 내부에서 랙 전경으로 물러남 | 열린 질문을 닫고 끝냄 |

각 구간이 하나의 생성 클립일 필요는 없다. 한 구간 안에 2–3개의 짧은 컷을 사용할 수 있고, 작동을 이해하는 데 필요한 구간은 길게 유지한다. 생성기의 8초 제한을 영상 전체 서사의 8초 규칙으로 바꾸지 않는다.

## 월드 시트

```text
Hero: an ORIGINAL conceptual copper cold plate on a dark green test board.
Geometry: two left-side ports; five alternating attached baffles; six connected lanes.
Identity: copper plate, black hoses, nickel fittings, dark green PCB.
Setting: credible server laboratory; the test object remains dominant.
Axis: inlet at near-left, outlet at far-left in the reference oblique view.
Worker: original fictional Korean engineer; dark work jacket, light protective gloves.
Physics boundary: this is a teaching model, not vendor CAD or CFD.
Text: no generated lettering. Korean captions and any measurements are composited later.
```

세계의 정보는 대본보다 먼저 확정한다. 외부 열교환 회로로 이동하면 단면·회로 색을 다시 정의한다. 한쪽 회로의 상징 입자를 다른 회로로 그대로 보내면 물질 전달과 열 전달을 혼동시킨다.

## 바로 사용할 원본 생성 프롬프트 세트

모델의 실제 입력 형식에 맞춰 이미지와 텍스트를 별도 전달한다. 아래 문장만으로 특정 도구가 실행되는 것은 아니다.

### P01: 현실 맥락 — 독립 전경

```text
Vertical technical documentary shot in a believable modern server laboratory.
A single copper cold plate on a dark green test board is the foreground subject,
with two black coolant hoses connected on its left. Server racks establish scale
in the background. The camera slowly approaches the hose fittings, revealing
their connection to the plate. Restrained industrial lighting, realistic rubber,
machined copper and brushed metal. No captions, logos, interface or speech.
One continuous purposeful camera move. No morphing or extra hose ports.
```

### P02: 공간 공개 — 기준 이미지에서 시작

```text
Continue from the approved reference object. The copper cover rises vertically,
then slides away toward the rear, leaving all connected channels visible.
The cover is removable, NOT hinged; no bending metal. The five alternating
baffles below stay rigid and attached to their respective perimeter walls.
The two hoses stay fixed to the base, never to the moving cover. A controlled
oblique view keeps the open plate in frame. Preserve board, ports and fasteners.
No text or new components. One action, one shot, vertical 9:16.
```

거절 조건: 뚜껑이 경첩처럼 변함, 호스가 뚜껑을 따라 올라감, 통로가 사라짐. 이번 공개 생성 시험의 첫 결과에서 실제로 발생한 유형이다. 문구를 추가했다고 해결되었다고 가정하지 말고 새 결과를 확인한다.

### P03: 흐름 — 이미 공개된 구조에서 시작

```text
The open copper cold plate remains rigid and unchanged. Small blue-to-orange
SYMBOLIC flow markers travel inside the existing connected serpentine passage,
turning only around the free ends of the alternating baffles. The five divider
walls retain their attachment points. The camera holds an unobstructed overhead
oblique view. No lid movement, no new ports, no liquid spills onto the board,
no wall crossing, no text, no speech. A clear technical visualization rather
than a literal view of solid particles in coolant.
```

중요한 연결이 계속 무너지면 더 긴 프롬프트만 반복하지 않는다. 같은 카메라의 검증한 3D 장면으로 바꾸고, 주변 생성 컷과 색·재질·방향을 맞춘다.

### P04: 인물 — 손이 원인을 만든다

```text
Use the approved original engineer reference, showing only gloved hands and
the sleeve of the dark work jacket. The right hand slowly turns the already
visible connector collar while the left hand steadies the hose. The fitting
stays attached to the same test apparatus. Focus on believable contact,
finger placement and the small rotation of the collar. No extra fingers,
no tool penetration, no disconnected hardware, no text or dialogue.
```

인물 시트의 정면 얼굴·사선·손 이미지를 모두 한 화면에 넣고 영상화하지 않는다. 동작에 필요한 단일 뷰를 승인해서 입력한다. 손동작이 필요 없는 장면에 인물 컷을 억지로 넣지 않는다.

## 제작 순서와 다음 판단

1. P02/P03처럼 실패하면 설명이 무너지는 장면부터 시험한다.
2. 한 번의 오류는 기록하고, 원인이 뚜렷하면 입력 상태·동작 수·카메라를 바꿔 한 번 더 시험한다.
3. 통로 구조를 계속 바꾸면 구조 장면은 3D로 확정한다. 생성 모델은 독립 전경·인물·재질 방향에 활용한다.
4. 영상 수신 성공과 장면 채택을 구분한다. `generated=true`여도 `mechanism_acceptance=fail`일 수 있다.
5. 최종 편집은 승인한 구간만 사용하고, 실제 음성과 합친 뒤 다시 검수한다.

## 다른 기업 소재로 변환하기

- 네트워킹: 패킷 하나 → 한 랙의 한계 → 스위치 → 랙 사이 경로 → 처음의 칩을 시스템 일부로 다시 보기.
- 패키징 공급망: 웨이퍼 → 잘라도 완제품이 아님 → 메모리·패키징의 순서 → 병목 → 완성품의 의미 변화.
- 용량 계약: 꺼진 랙 → 누가 비용을 부담하는가 → 실제 계약 조건에 따른 경로 → 장비 판매와 서비스 구매를 분리해 보여주기.

물리적 실물이 없는 계약은 계약서의 권리·의무를 공간적으로 설명할 수 있지만, 소유권·매출·현금흐름을 같은 색의 화살표 하나로 뭉개지 않는다. 물리 비유가 원래 계약보다 더 강한 주장을 하면 수정한다.
