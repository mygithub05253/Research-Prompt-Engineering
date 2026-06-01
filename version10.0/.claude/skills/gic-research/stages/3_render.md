# Stage 3 — Render (PPTX 생성)

## 입력
Stage 2 승인된 매핑 결과 (yaml + 슬라이드별 변수 디스패치)

## 처리
`scripts/render_research.py` 호출:
1. `templates/기업리서치_9p.pptx` (= 학회 양식 ver2 복제) 로드
2. 슬라이드별 텍스트 박스 placeholder를 yaml 변수로 교체
3. 표 셀에 데이터 주입 (Revision·시총·주요주주·재무지표·CONTENTS)
4. 이미지 영역에 PNG 삽입 (주가차트·산업차트·기업 다이어그램·밸류에이션 차트 4개)
5. word_wrap=False 후처리 (rules.md §3.4)
6. 출력 PPTX 저장: `data/output/[기업명]_GIC리서치_YYYYMMDD/[기업명]_GIC리서치_YYYYMMDD.pptx`

## 명령
```bash
python .claude/skills/gic-research/scripts/render_research.py \
  --yaml data/samples/[기업명].yaml \
  --output data/output/[기업명]_GIC리서치_YYYYMMDD/
```

## 출력
- `[기업명]_GIC리서치_YYYYMMDD.pptx`
- `render_log.txt` (변환 로그)

## 자동 진행
긴 작업이지만 게이트 없음. 완료 후 Stage 4로.

## 다음 단계
`stages/4_export.md`
