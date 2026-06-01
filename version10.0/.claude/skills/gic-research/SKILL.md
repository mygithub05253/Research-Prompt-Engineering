---
name: gic-research
description: GIC 정식 기업리서치 보고서를 학회 양식 ver2 (.pptx 9페이지)로 자동 생성. 부원이 챗봇에서 받은 부록 C yaml을 입력하면 학회 양식 슬라이드 마스터에 변수 자동 매핑 → PPTX + PDF 출력. 이 Skill 없이도 챗봇 복붙으로 동일 결과 가능 (부록 C yaml을 PowerPoint에 직접 매핑하면 됨).
trigger: /gic-research [기업명] [--code=종목코드] [--date=YYYY-MM-DD]
---

# /gic-research — 기업리서치 PPT 자동 생성 Skill

## 사용법

```
/gic-research 삼성전기 --code=009150 --date=2026-05-09
```

또는 인자 생략 시 yaml에서 자동 추출:
```
/gic-research
[그 다음 메시지에 부록 C yaml 붙여넣기]
```

## 입력 (yaml)

부원이 다음 중 하나로 입력:
1. **챗봇 출력 그대로**: `GIC_기업리서치_v10.md` Step 0~8 통과 후 부록 C 형식 yaml 출력 받음
2. **수기 작성**: `data/samples/[기업명].yaml` 직접 편집

yaml 명세는 `prompts/GIC_기업리서치_v10.md` **부록 C** 와 본 Skill의 `columns.md` 가 1:1 동일.

## 출력

```
data/output/[기업명]_GIC리서치_YYYYMMDD/
├── [기업명]_GIC리서치_YYYYMMDD.pptx     # 학회 양식 9페이지
├── [기업명]_GIC리서치_YYYYMMDD.pdf       # LibreOffice 변환
└── verify_report.txt                     # PPTX 호환성 점검 결과
```

## 단계별 플로우 (원칙 7 — 단계별 게이트)

```
1. Intake  ← stages/1_intake.md
   yaml 검증 (변수 누락·형식 오류 체크)
   → 부원 승인 게이트

2. Map     ← stages/2_map.md
   yaml → 양식 슬라이드 9페이지 변수 매핑
   → 매핑 결과 미리보기 + 부원 승인 게이트

3. Render  ← stages/3_render.md
   python-pptx로 templates/기업리서치_9p.pptx (= 양식 마스터) 복제 후 변수 주입
   → 자동 진행

4. Export  ← stages/4_export.md
   PPTX → PDF (LibreOffice headless)
   PPTX 호환성 점검 (design-guide_v10 §11.7)
   → 결과 보고
```

## 의존 자산

- **양식 마스터**: `../../../templates/기업리서치_9p.pptx` (학회 양식 ver2 복제본)
- **컬러 토큰**: `../../../design/GIC_design-guide_v10.md` §3 (Primary Navy `#072A51`, Accent Orange `#E57728`)
- **좌표 명세**: `../../../design/GIC_design-guide_v10.md` §12 + 본 Skill `columns.md`
- **렌더 스크립트**: `scripts/render_research.py`
- **PPTX → PDF**: `scripts/pptx_to_pdf.py` (LibreOffice headless 호출)
- **호환성 점검**: `scripts/verify_pptx.py`

## 안전 룰 (rules.md 참조)

- 학회 양식 컬러 hex 변경 금지
- Pretendard 누락 시 fallback (Apple SD Gothic Neo → Malgun Gothic)
- 표 헤더 행과 본문 행 스타일 분리 (design-guide_v10 §11.6)
- 짧은 라벨 word_wrap=False 후처리 의무 (design-guide_v10 §11.9)
- 텍스트 박스 padding-bottom ≥ 36pt 보장

## v9.0 챗봇 복붙 동등성 (원칙 8)

이 Skill 없이도 부원이 5분 만에 동일 결과 도달:
1. 챗봇에서 yaml 받기
2. PowerPoint 양식.pptx 열기
3. 슬라이드별로 yaml 변수를 텍스트 박스에 매핑 (30~45분)
4. 발표

Skill 사용 시 5분, 수기 매핑 시 30~45분. 결과물은 시각 비교 ≥90% 일치.

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| Skill 실행 시 "yaml 변수 누락" 에러 | 부록 C 자리표시자가 채워지지 않음 | yaml 검증 로그 확인, 누락 변수 채우기 |
| PPTX 폰트가 얇게 출력됨 | Pretendard 누락 | fallback 폰트 자동 적용됨, 출력 폰트 확인 |
| Bold 텍스트가 줄바꿈됨 | 양식 텍스트 박스 폭 부족 | 글자 수 룰 (≤25자, ≤200자) 위반 확인 |
| LibreOffice 미설치로 PDF 변환 실패 | Windows에 LibreOffice 미설치 | `winget install LibreOffice.LibreOffice` 또는 PPTX만 출력하고 부원이 직접 변환 |
| 표 강조 컬럼 컬러 누락 | 양식 마스터 손상 | `templates/기업리서치_9p.pptx` 재빌드 |
