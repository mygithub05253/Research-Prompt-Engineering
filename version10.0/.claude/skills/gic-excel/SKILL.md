---
name: gic-excel
description: GIC 학회 표준 5개년 모델 Excel 양식 빌드 + Step 6 마크다운 표 자동 입력. 8 sheets (Assumptions/IS/BS/CF/Valuation/Scenario/Sensitivity/Summary), Balance Check 자동 검증. 이 Skill 없이도 챗봇 복붙 부원이 빈 Excel 양식을 받아 직접 채울 수 있음.
trigger: /gic-excel [기업명] [--years=5] [--build-template]
---

# /gic-excel — Excel 5개년 모델 자동 생성 Skill

## 사용법

### A. 학회 표준 빈 양식 빌드 (운영진 1회)
```
/gic-excel --build-template
```
→ `templates/Excel_5개년모델_v10.xlsx` 생성 (8 sheets, Balance Check 수식, 컬러 코딩)

### B. yaml 기반 자동 입력 (부원)
```
/gic-excel 삼성전기
[그 다음 yaml 또는 마크다운 표 붙여넣기]
```
→ `data/output/[기업명]_5개년모델_YYYYMMDD.xlsx`

## 8 시트 구성

| # | Sheet | 역할 | 자동화 |
|---|---|---|---|
| 1 | Assumptions | Bear/Base/Bull 가정표 | 입력 셀 색상 구분 (`#FFE9D6` 오렌지 10%) |
| 2 | IS | 5개년 손익계산서 | YoY 성장률 자동 계산 |
| 3 | BS | 5개년 재무상태표 | Balance Check 수식 |
| 4 | CF | 5개년 현금흐름표 | FCF 자동 계산 |
| 5 | Valuation | 4종 밸류에이션 (PER/EV-EBITDA/PBR/DCF) | 목표주가 자동 |
| 6 | Scenario | 시나리오 매트릭스 | EPS × PER 자동 |
| 7 | Sensitivity | 민감도 분석 | ±15% 자동 |
| 8 | Summary | 1페이지 요약 | 다른 시트 참조 |

## 컬러 코딩 (학회 전통)
- 입력 셀: `#FFE9D6` (오렌지 10%) — 부원이 직접 입력
- 수식 셀: `#FFFFFF` (흰색) — 자동 계산
- 참조 셀: `#E8EFFF` (네이비 10%) — 다른 시트 참조
- 헤더 행: `#072A51` 흰 글자
- Balance Check OK: `#22C55E` (초록) / ERROR: `#EF4444` (빨강)

## 의존
- `scripts/build_excel_template.py` — 빈 양식 빌드 (운영진용)
- `scripts/fill_excel_from_yaml.py` — yaml/마크다운 → 자동 입력 (v10.1+)
- 본 Skill v10.0 우선 빌드: `--build-template` 만 동작. 자동 입력은 v10.1.

## 챗봇 복붙 동등성 (원칙 8)
부원이 마크다운 표를 받았을 때:
1. 빈 양식 다운로드 (학회 드라이브)
2. Sheet 1: Bear/Base/Bull 가정 입력 (10분)
3. Sheet 2~4: 5개년 IS/BS/CF 표 직접 붙여넣기 (15분)
4. 자동 계산 확인 → Balance Check OK 검증
5. Sheet 8 Summary로 요약 확인

총 25~30분. v10.1+에서 자동 입력 추가 시 5분으로 단축.

## v10.0 출시 범위
- ✅ 빈 양식 빌드 (`--build-template`)
- ⏳ yaml 자동 입력은 v10.1+
