# 원격 GPU를 사용할 때

## 재접속과 품질 개선

현재 사용자의 로컬 설정이 있으면 `~/.codex/local/remote-gpu.sshconfig`의 `video-gpu` 별칭을 사용한다. 상세 런타임 위치는 같은 폴더의 `remote-gpu.md`에서 확인한다. 이 파일들이 없는 다른 컴퓨터에서 주소·계정을 추측하지 않는다. 접속 설정과 전용 개인키는 배포 패키지에 넣지 않는다. 전용 키를 설정한 현재 컴퓨터에서는 배치 접속·파일 전송을 재사용할 수 있으며, 비밀번호 평문 저장은 필요하지 않다.

품질 개선은 [gpu-quality.md](gpu-quality.md)의 동일 장면 비교 → 재질·구도 수정 → 짧은 동영상 검수 순서로 진행한다. 사용자가 승인한 해당 GPU에서 관련 실험은 이어갈 수 있으나, 기존 작업 중단이나 시스템 교체를 포함하는 승인은 아니다.

사용자가 원격 컴퓨터 사용을 요청하고 접속 정보를 제공하면, 렌더링 병목을 해결할 수 있는지 먼저 확인한다. 접속 비밀번호·개인키·토큰은 스킬, 실행 소스, README, 패키지에 저장하지 않는다. 호스트 주소는 사용자가 제공한 값을 사용하고 임의로 네트워크를 탐색하지 않는다.

## 먼저 확인할 실제 상태

기본 `python3`에서 모듈이 없다는 결과만으로 서버에 생성 환경이 없다고 판단하지 않는다. 로컬 원격 프로필에 기록된 작업 루트의 가상환경·모델 캐시를 먼저 확인한다. Hugging Face 캐시는 확장자가 없는 blob과 snapshot symlink일 수 있어 얕은 `*.safetensors` 검색으로 존재 여부를 판정하지 않는다. 기존 캐시를 `local_files_only=True`로 실제 로드해 확인하고, 새 다운로드는 저장소의 파일 목록·정확한 revision·선택한 파일 크기를 먼저 기록한다. FP16 추론에 ONNX/OpenVINO/FP32/루트 단일 체크포인트를 함께 받을 필요는 없다. 중단한 다운로드가 실제 종료됐는지 확인한 뒤 재개하며, 계정의 전체 캐시를 지우지 않는다.

- GPU 모델, VRAM, 현재 사용량: `nvidia-smi`
- 사용 가능한 RAM과 작업 디스크 여유
- 저장장치 종류와 실제 I/O 대기, 프로세스 RSS·시스템 swap. CPU offload를 쓰면 모델 읽기가 추론 호출 안에 포함될 수 있다. 첫 로딩과 캐시가 준비된 뒤의 단계 시간을 구분하며, 설치·다운로드와 추론이 겹친 기록을 순수 GPU 속도로 보고하지 않는다.
- Blender, FFmpeg, 필요한 생성 모델과 런타임의 설치 여부
- 장면에 포함된 이미지·폰트·텍스처의 외부 경로. 필요한 파일만 복사한다.

GPU가 있다는 사실만으로 대형 영상 모델이 돌아간다고 가정하지 않는다. 이번 RTX 4060 8GB에서는 작은 Blender 씬의 Cycles/OptiX 렌더링을 실제 확인했다. Wan 14B 같은 모델의 실행을 확인한 것은 아니다. 원격 서버에는 당시 기본 Python에서 PyTorch와 Diffusers가 발견되지 않았다.

이후 별도 가상환경에 PyTorch와 Diffusers를 설치해 SDXL 이미지 생성도 실행했다. 서버의 기존 Python 환경이나 드라이버를 교체하지 않았다.

## 이번에 검증한 경로

1. 전용 작업 폴더를 만들었다.
2. 공식 Blender 5.2.1 Linux 배포본을 내려받고 공식 SHA-256 값과 일치함을 확인했다. 시스템 패키지나 드라이버 전체 업그레이드는 필요하지 않았다.
3. 원본 `.blend`와 짧은 실행 스크립트만 복사했다.
4. 대표 프레임 두 장으로 GPU를 사용하는지, 속도와 화질이 어떤지 확인했다.
5. OptiX 장치만 사용하도록 지정하고 GPU용 디노이저를 선택했다. CPU로 조용히 대체되면 실패 처리한다.
6. 전체 프레임을 원격에서 렌더·인코딩하고, 작은 MP4와 검수 자료를 로컬로 가져왔다.

`scripts/gpu_render.py`는 이미 열린 이 스킬의 개념 모형 `.blend`를 사용한다. 기본 호출은 270·271 프레임만 시험하며, `-- --full`로 576프레임 전체를 렌더한다. 출력은 `.blend` 옆 `gpu-frames` 폴더와 JSON 실행 기록이다.

```bash
blender -b cooling-proof.blend --python gpu_render.py
blender -b cooling-proof.blend --python gpu_render.py -- --full
ffmpeg -framerate 24 -start_number 1 -i gpu-frames/f_%04d.png \
  -frames:v 576 -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
  -movflags +faststart motion-source.mp4
```

호출 환경에 맞는 실제 실행 파일 경로를 쓴다. 기본 렌더는 1080×1920, 12샘플, OptiX 디노이즈다. GPU 지원과 대표 프레임의 품질을 확인한 뒤 사용한다. 이 설정이 모든 씬의 권장 최종값은 아니다.

## 측정값을 읽는 법

2026-09-05의 동일 개념 모형에서 1080×1920·32샘플 시험은 첫 프레임 약 11.75초, 다음 프레임 약 6.75초였다. 12샘플·OptiX 디노이저·낮은 PNG 압축으로 조정한 시험은 약 2.09초와 0.83초였다. 전체 렌더 초반에는 약 0.65초/프레임도 확인했다. GPU 사용률 97%, 약 1.4GB VRAM 사용을 한 시점에서 확인했다.

이는 장면과 설정을 함께 바꾼 실행 기록이다. 로컬 CPU 대비 공정한 동일 설정 벤치마크나 모든 이미지 모델의 속도 향상률로 표현하지 않는다. 첫 프레임의 초기화 시간, 디노이저, 압축, CPU 준비 작업도 체감 속도에 영향을 준다.

## 8GB GPU에서 텍스트 → 이미지 시험

실제 사용한 모델은 [SDXL 1.0 base](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)의 fp16 가중치다. 이것을 원작 채널의 사용 모델이나 현행 최상급 영상 모델로 소개하지 않는다. 설치 당시 라이브러리는 PyTorch 2.14.0+cu130, Diffusers 0.40.0, Transformers 5.16.1, Accelerate 1.14.0이었다.

모델 단위 CPU offload와 VAE tiling으로 메모리를 조절했다. 첫 시험의 768×1344·25단계 이미지는 모델 캐시가 있는 상태에서 로딩 약 1.24초, 실제 생성 약 21.26초, 최대 할당 VRAM 약 5.21GiB였다. 초회 다운로드와 API 오류를 수정한 시간은 이 생성 시간에 포함하지 않는다.

첫 실행은 예전 `pipe.enable_vae_tiling()` 호출이 없어 실패했다. 현행 공식 [메모리 최적화 문서](https://huggingface.co/docs/diffusers/en/optimization/memory)에 맞춰 `pipe.vae.enable_tiling()`으로 고쳐 실행했다. 단순 경고를 숨긴 것이 아니라 실제 오류 원인을 수정했고, 최종 이미지를 확인했다.

```text
python scripts/gpu_image.py --out-dir ./image-proof
python scripts/gpu_image.py --out-dir ./image-proof --context
```

첫 명령은 밸브·손을 요청하는 한 장의 시험, 두 번째는 독립적인 서버실 배경 시험이다. CUDA가 없으면 자동 CPU 대체 없이 중단한다. 모델 캐시와 결과는 명시한 작업 폴더에 저장한다. `torch`, `diffusers`, `transformers`, `accelerate`, `safetensors`, `pillow`가 필요하며, 별도 가상환경을 권장한다. 모델 라이선스는 [공식 모델 카드](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)의 Open RAIL++ 조건을 확인한다.

밸브 시험은 사진 같은 재질을 만들었지만 손이 빠졌고 연결이 부정확했다. 따라서 실행 가능성은 확인했으나 기계 동작을 설명하는 승인 이미지로 채택하지 않았다. GPU의 속도, 모델의 지시 이행, 실제 장면의 정확성은 서로 다른 평가다.

두 번째 서버실 배경 시험은 약 21.30초, 같은 약 5.21GiB 최대 할당 메모리로 생성했다. 전체 이미지에서 통로·랙·천장 구조와 사진 같은 재질을 확인해 **일반적인 분위기·공간 소개용 후보**로 분류했다. 실제 회사 시설 사진이나 특정 냉각 배관의 증거는 아니다. 이 스킬의 설치용 `gpu_image.py --out-dir ... --context` 경로를 원격에서 직접 실행해 확인했다.

## 전체 렌더의 저장 공간 사전 계산

모델 설치 후 남은 공간만 확인하지 말고, 실제 최종 해상도로 렌더한 대표 PNG의 파일 크기 × 전체 프레임 수를 계산한다. 기존 모델·임시 파일·수정 렌더·인코딩 결과와 운영 여유 공간을 더해 착수 여부를 판단한다. 낮은 PNG 압축은 렌더 시간을 줄여도 저장량을 크게 늘릴 수 있다. 2026-09-06 본편에서는 한 장 약 8MB가 누적되어 별도 공간 보완이 필요했다.

PNG 압축률 조정은 픽셀을 바꾸지 않는 저장 최적화다. 완료된 작업 프레임을 재압축할 때는 비트 깊이·색상 모드·크기를 유지하고, 디코딩한 픽셀 해시가 원본과 동일함을 확인한 임시 파일만 원자적으로 교체한다. 같은 파일의 재렌더와 재압축을 동시에 실행하지 않는다. 수정 렌더는 기존 렌더와 압축 작업이 모두 끝난 뒤 실행한다. 사용자 파일 삭제로 공간을 임의 확보하지 않는다.

## 로컬에서 최종 조립 실행

패키지의 `example` 폴더에는 이 시험의 원본 음성·타임라인과 렌더된 `motion-source.mp4`를 함께 둔다. Python의 `numpy`, 설치된 FFmpeg와 한글 폰트가 필요하다.

```text
python scripts/assemble_cooling_proof.py --work-dir example --out-dir output --ffmpeg ffmpeg --full --use-motion
python scripts/validate_shots.py example/proof-shot-plan.json
```

이 조립 스크립트는 냉각 개념 시험용 고정 카메라 구간을 사용한다. 임의의 영상에 그대로 적용하는 범용 편집기가 아니다. 다른 주제에서는 실제 음성과 장면 계약에 맞게 구간·자막을 바꾼다. 인코딩 이후 프레임·청취·스타일 검수를 별도로 수행한다.
