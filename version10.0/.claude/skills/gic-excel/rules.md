# gic-excel rules.md — Excel 빌드·검증 룰

## 1. 컬러 코딩 (학회 표준)
| 셀 종류 | 배경 hex | 의미 |
|---|---|---|
| 입력 | `#FFE9D6` (오렌지 10%) | 부원이 직접 입력 |
| 수식 | `#FFFFFF` (흰색) | 자동 계산 |
| 참조 | `#E8EFFF` (네이비 10%) | 다른 시트 참조 |
| 헤더 | `#072A51` 흰 글자 | 시트 헤더 행 |
| Balance OK | `#22C55E` 흰 글자 | Balance Check 통과 |
| Balance ERROR | `#EF4444` 흰 글자 | Balance Check 실패 |

## 2. Balance Check 수식
```
=IF(자산총계 = 부채총계 + 자본총계, "OK", "ERROR")
```
조건부 서식: OK이면 초록, ERROR이면 빨강.

## 3. FCF 산식
```
FCF = 영업CF - CAPEX
```

## 4. 목표주가 산식
- PER 적용: `Forward EPS × 적용 PER`
- EV/EBITDA: `EBITDA × 적용 EV/EBITDA - 순차입금) / 발행주식수`
- PBR: `BPS × 적용 PBR`
- DCF: 5개년 FCF 할인 + Terminal Value

## 5. 시나리오 매트릭스
EPS × PER Data Table 활용 (Excel 기본 기능)

## 6. 민감도 분석
매출 ±15% × OPM ±2%p 조합으로 목표주가 변화 표시

## 7. Step 6 마크다운 표 매핑 (v10.1+)
- v9.0 Step 6 출력 5개년 IS 표 → Sheet 2 행 4~12에 자동 입력
- v9.0 Step 6 가정표 → Sheet 1 Bear/Base/Bull 자동 분배
