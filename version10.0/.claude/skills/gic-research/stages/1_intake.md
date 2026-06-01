# Stage 1 — Intake (yaml 검증)

## 입력
부원이 다음 중 하나로 yaml 제공:
- 챗봇 출력 (코드 블록 안 yaml)
- `data/samples/[기업명].yaml` 파일 경로

## 처리
1. yaml 파싱 (PyYAML)
2. 부록 C 필수 변수 누락 체크 (columns.md §검증 룰)
3. 글자 수 룰 위반 체크 (≤25자, ≤200자 등)
4. 자리표시자 미채움 체크 (`[###,###원]` 등이 그대로 남아있으면)
5. 이미지 파일 경로 유효성 체크 (선택)

## 출력
```
[Intake 결과]
- 변수 N/M 채워짐
- WARNING: ##.# 글자 수 룰 위반 (자동 절단 옵션: --auto-truncate)
- ERROR: 종목코드 누락 → 진행 불가
```

## 게이트
- ERROR 0건 → "다음 단계 진행"
- ERROR 1건 이상 → 부원 수정 후 재실행

## 다음 단계
`stages/2_map.md`
