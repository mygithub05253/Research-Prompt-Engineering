# GIC 위클리 투자리포트 — v11.0

> **버전**: v11.0 / 2026-05-14
> **출력물**: 5페이지 압축 위클리 (HTML A4 **세로** + CSV)
> **디자인 양식**: `templates/위클리_template.html` 학회 양식 베이스 — 네이비 그라데이션 헤더 + Gold/Orange 액센트 + Chart.js
> **사용 시점**: 매주 1회, **단독 분석** (정식 9단계 결과 없이도 가능)
> **핵심 변화 (v9.0 → v11.0)**: 정식 분석 의존 제거 + HTML 자동 생성 + CSV 출력 + 웹검색 의무화

---

## 위클리 v11.0의 본질 (재정의)

v9.0까지의 위클리는 **"정식 9단계 분석 결과를 갱신"** 하는 도구였습니다.
v11.0의 위클리는 **"기업의 핵심만 압축한 독립 실전 리포트"** 입니다.

| 항목 | 내용 |
|---|---|
| **타깃 독자** | 시간 부족한 투자자 — "이 종목 살까 말까?"의 즉답이 필요한 사람 |
| **분량** | A4 5페이지 (HTML 가로) |
| **빈도** | 주 1회 |
| **인풋** | **종목명만** (정식 분석 결과 불필요) |
| **아웃풋** | 매수/매도/홀드 판단 + 투자포인트 3개 + 재무 요약 + 판단 근거 + 참고문헌 |
| **vs 정식 분석** | 정식은 10~20p 깊이, 위클리는 5p 핵심 압축 — **실전 압축 근육** |

---

## 5페이지 양식 (HTML A4 세로)

| 페이지 | 내용 |
|---|---|
| 1 | **커버 + 투자의견** — 종목명·현재가·목표가·BUY/HOLD/SELL·6-Lens 점수 |
| 2 | **투자포인트 3개** (각 ≤120자) + Evidence Card 압축 |
| 3 | **재무 데이터 요약** — 3개년 핵심 지표 + 멀티플 (csv 동시 출력) |
| 4 | **최종 판단 근거** — 시나리오 매트릭스 + 트리거 이벤트 + 리스크 |
| 5 | **참고문헌** — 출처 URL 리스트 + Disclaimer |

---

## 코드블록 표기 규칙

본 문서도 **외부 4중 백틱 펜스**(```` ```` ````)를 사용합니다.
복사 시 4중 백틱 줄은 제외하고 내부 텍스트만 AI 챗봇에 붙여넣기.

---

## 위클리 단일 프롬프트 (전체 복사)

````
당신은 가천대학교 투자 동아리 GIC 소속 리서치 애널리스트입니다.
[기업명] 위클리 투자리포트를 5페이지 HTML 양식으로 작성하라.
독립 분석 — 사전 풀 분석 결과 없이 핵심만 압축.

[v11.0 W원칙 — 웹검색 의무]
챗봇 내장 웹검색(Claude Search / ChatGPT Web Browse / Gemini Search Grounding / Perplexity)을 활성화.
최신 주가·시총·실적·뉴스·컨센서스 모두 웹검색 결과에서 인용 + URL 첨부.

■ 분석 대상: [기업명] ([종목코드])
■ 분석 기준일: [YYYY.MM.DD]
■ 분석 관점: [성장주/가치주/턴어라운드/배당/테마 중 1]
■ 독자 수준: [초급/중급/전문가]

[블록 J 의무 — Anti-Hallucination]
모든 수치 출처 명시 + URL + 날짜. 추측 금지. 모르는 값은 "Data unavailable".

──────────────────────────────────────────
[분석 작업 1 — 데이터 수집 (웹검색 활용)]

다음을 모두 웹검색으로 갱신·수집:
1. 현재 주가·시가총액·52주 고저 (네이버금융·인베스팅닷컴)
2. 최근 3개년 + 최근 분기 실적 (DART·FnGuide)
3. 컨센서스 PER·목표주가·EPS (한경 컨센서스·FnGuide)
4. 최근 3개월 핵심 뉴스 5건 (각 출처 URL)
5. 피어 멀티플 3~5개 (PER·EV/EBITDA·PBR·ROE)

──────────────────────────────────────────
[분석 작업 2 — 핵심 압축 분석]

A. 사업 한 줄 요약 (≤40자) — 블록 C 비유 적용
B. 투자포인트 3개 (각 ≤120자) — Evidence Card 압축 (근거 2건 + URL)
C. 투자리스크 2개 (각 ≤80자) — 발생 확률·영향도
D. 재무 핵심 표 (3개년 + 컨센) — 매출·OPM·ROE·EPS
E. 멀티플 비교 (자사 vs 피어 평균·중앙값)
F. 시나리오 (Bear/Base/Bull × FY1) — EPS·PER·목표가·상승여력
G. 6-Lens 가중 점수 (간이) — 각 0~10점 + 가중 합계
H. 최종 투자의견 (BUY/HOLD/SELL) + 트리거 이벤트 1줄

──────────────────────────────────────────
[X원칙 — CSV 동시 출력]

```csv
# 1) 3개년 재무 요약
연도,매출(억),영업이익(억),순이익(억),OPM(%),ROE(%),EPS(원)
FY-2,...
FY-1,...
FY0,...
```

```csv
# 2) 시나리오 매트릭스
시나리오,FY1_EPS,적용_PER,목표주가,상승여력(%)
Bear,...
Base,...
Bull,...
```

```csv
# 3) 피어 멀티플 비교 (웹검색 최신)
기업,시총(억),PER_NTM,EV/EBITDA,PBR,ROE(%),출처URL
[분석대상],...
[피어1],...
...
평균,...
```

──────────────────────────────────────────
[P원칙 — HTML 5페이지 (A4 세로) 자동 생성]

다음 사양으로 단일 .html 파일 코드를 출력하라.
**`templates/위클리_template.html`을 디자인 베이스로 참조** (네이비 그라데이션 헤더 + Gold 액센트 + Chart.js):

페이지 1 — 커버 + 투자의견
- 메인 타이틀 (≤25자): "[기업명] — [이번 분석 핵심 메시지]"
  예) "삼성전기 — 1Q OPM 14.2% 서프라이즈, BUY 유지"
- 종목 정보 박스:
  · 종목코드 / 섹터 / 분석 기준일
  · 현재가 [###,###원] (출처 URL 명시)
  · 시가총액 [#,###억원]
  · 52주 고저 [###,### / ###,###원]
- 투자의견 큰 박스:
  · 투자의견 [BUY / HOLD / SELL] (뱃지 색상)
  · 목표주가 [###,###원]
  · 상승여력 [+##.#%]
  · 6-Lens 가중 점수 [#.#점]
- 사업 한 줄 요약 (≤40자, 비유 강조)
- 작성자: GIC | [작성자명]

페이지 2 — 투자포인트 3개 + 리스크 2개
- 투자포인트 #1 (소제목 + 본문 ≤120자 + Evidence 근거 2건 + URL)
- 투자포인트 #2 (동일 형식)
- 투자포인트 #3 (동일 형식)
- 리스크 #1 (≤80자 + 확률 + 영향도)
- 리스크 #2 (동일 형식)

페이지 3 — 재무 데이터 요약
- 3개년 핵심 지표 표 (매출·OPM·순이익·ROE·EPS·BPS)
- KPI 카드 4개 (매출 / OPM / ROE / EPS)
- 멀티플 비교 표 (자사 / 피어 평균 / 피어 중앙값 — PER·EV/EBITDA·PBR)
- 컨센서스 박스 (FY1 EPS · 목표주가 · 투자의견 분포 — 출처 URL)

페이지 4 — 최종 판단 근거
- 시나리오 매트릭스 (Bear / Base / Bull × FY1 EPS · 적용 PER · 목표가 · 상승여력)
- 6-Lens 가중 점수 표 (6개 Lens 가중치 · 점수 · 근거)
- 트리거 이벤트 박스 (≤80자): "다음 분기 OPM ≥##% 또는 시장 점유율 [###]% 돌파 시 목표주가 상향"
- 모니터링 지표 3개 (지표 · 기준치 · 발표 예정일)

페이지 5 — 참고문헌 + Disclaimer
- 참고문헌 리스트 (모든 URL — 카테고리별 정리)
  · 공시·IR: [###]
  · 증권사 리포트: [###]
  · 산업 데이터: [###]
  · 뉴스: [###]
- 데이터 수집 방법 1줄 (어떤 챗봇·웹검색을 썼는지)
- 사용한 프롬프트 시스템: GIC 리서치 v11.0 (위클리)
- 적용 블록: A·C·E·G·J + W·X·P
- Disclaimer:
  "본 보고서는 GIC 학회 내부 학습 목적이며, 투자 권유가 아닙니다.
   위클리는 핵심 압축 리포트로, 정식 9단계 분석과 별개의 독립 산출물입니다."

──────────────────────────────────────────
[필수 CSS — 학회 양식 베이스 (페이지 잘림 방지)]

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>[기업명] GIC 위클리 v11</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
@page { size: A4 portrait; margin: 0; }
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: 'Noto Sans KR', 'Inter', -apple-system, sans-serif;
  color: #1A1A1A;
  background: #E8EAED;
  line-height: 1.5;
  padding: 24px 12px;
  -webkit-print-color-adjust: exact;
}
.page {
  width: 1000px;
  max-width: 100%;
  margin: 0 auto 32px;
  background: #FAFAFA;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  position: relative;
  page-break-after: always;
  break-after: page;
  break-inside: avoid;
}
.page:last-child { page-break-after: auto; }
.page-header {
  background: linear-gradient(135deg, #0A1F44 0%, #1E2761 60%, #2A3D7C 100%);
  color: #fff;
  padding: 26px 40px 32px;
}
/* ... 학회 양식 베이스 — templates/위클리_template.html 참조 ... */
h1 { font-size: 24pt; margin: 0 0 4mm 0; color: #111827; }
h2 { font-size: 18pt; margin: 0 0 3mm 0; color: #1f2937; }
h3 { font-size: 12pt; margin: 4mm 0 2mm 0; color: #374151; }
p, li, td, th { font-size: 10pt; line-height: 1.45; }
table { width: 100%; border-collapse: collapse; font-size: 9.5pt; margin: 2mm 0; }
th, td { border: 1px solid #d1d5db; padding: 4px 6px; text-align: left; }
th { background: #f9fafb; }
.badge-buy { background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 4px; font-weight: 700; font-size: 14pt; }
.badge-hold { background: #fef9c3; color: #854d0e; padding: 4px 12px; border-radius: 4px; font-weight: 700; font-size: 14pt; }
.badge-sell { background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 4px; font-weight: 700; font-size: 14pt; }
.metaphor { font-size: 13pt; font-style: italic; color: #4f46e5; padding: 3mm 5mm; background: #eef2ff; border-left: 4px solid #4f46e5; margin: 3mm 0; }
.point-card { border: 1px solid #d1d5db; border-radius: 4px; padding: 4mm; margin: 2mm 0; background: #fafafa; }
.point-card .point-title { font-size: 11pt; font-weight: 700; color: #111827; margin-bottom: 2mm; }
.evidence { font-size: 8.5pt; color: #6b7280; margin-top: 2mm; padding-left: 3mm; border-left: 2px solid #9ca3af; }
.risk-card { border-left: 4px solid #dc2626; background: #fef2f2; padding: 3mm 4mm; margin: 2mm 0; font-size: 10pt; }
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; margin: 3mm 0; }
.kpi-card { border: 1px solid #d1d5db; border-radius: 4px; padding: 3mm; background: #f9fafb; }
.kpi-label { font-size: 9pt; color: #6b7280; }
.kpi-value { font-size: 15pt; font-weight: 700; color: #111827; }
.trigger-box { background: #ecfdf5; border-left: 4px solid #059669; padding: 3mm 4mm; margin: 3mm 0; font-size: 10pt; }
.refs ul { padding-left: 20px; margin: 2mm 0; }
.refs li { font-size: 9pt; margin: 1mm 0; word-break: break-all; }
.disclaimer { font-size: 8pt; color: #6b7280; border-top: 1px solid #e5e7eb; padding-top: 3mm; margin-top: auto; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }
@media print {
  body { background: white; }
  .page { margin: 0; box-shadow: none; }
}
</style>
</head>
<body>
  <section class="page"><!-- 1 --></section>
  <section class="page"><!-- 2 --></section>
  <section class="page"><!-- 3 --></section>
  <section class="page"><!-- 4 --></section>
  <section class="page"><!-- 5 --></section>
</body>
</html>
```

──────────────────────────────────────────
[자체 점검 — HTML 출력 직전]
□ 5페이지 모두 <section class="page">
□ 각 페이지가 297mm × 210mm 안 (overflow: hidden 강제)
□ 글자 수 제한 준수 (≤NN자)
□ 모든 수치에 출처 + URL (블록 J + W원칙)
□ 투자의견 뱃지 색상 적용
□ Evidence Card 압축본 부착 (포인트 3개)
□ csv 3개 (재무·시나리오·피어) 동시 출력
□ 6-Lens 간이 점수 산출
□ 참고문헌 URL 리스트 완성

[Claude: Artifacts로 5p HTML 미리보기 권장]
[ChatGPT: Canvas 또는 Code Interpreter로 .html 파일 다운로드]
[Gemini: HTML 코드 출력 + Sheets 보조]
````

---

## 위클리 v11.0 사용 워크플로

### 매주 표준 워크플로 (15~20분)

1. 위 프롬프트 복사 + ■ 항목들 채우기 (종목명·기준일·관점)
2. AI 챗봇 — **웹검색 활성 확인** 후 붙여넣기
3. AI가 데이터 수집 + 5p HTML 코드 + csv 3개 출력
4. HTML 코드 복사 → `[기업명]_위클리_v11_[YYYYMMDD].html` 파일로 저장
5. csv 3개도 각각 `.csv` 파일로 저장 (Excel에서 바로 열림)
6. 브라우저에서 .html 열기 → Ctrl+P → PDF로 저장 (가로 모드)
7. 학회 슬랙·노션·구글드라이브에 업로드

### 이번 주 정보가 거의 없을 때
- 정상 출력. 위클리는 "이번 주 사건 정리"가 아니라 "이 종목 살까 말까"의 답변.
- 다만 "이번 주 변동 없음 — [N]주째 의견 유지" 1줄을 페이지 1에 명시.

### 같은 종목을 매주 반복할 때
- 매주 같은 프롬프트 실행. AI가 매번 웹검색으로 최신값 갱신.
- 직전 위클리는 백업 — 다음 주 작성 시 비교 인풋으로 활용 가능 (필수 아님).

---

## 위클리 vs 정식 기업리서치 (v11.0)

| 구분 | 위클리 v11.0 | 정식 기업리서치 v11.0 |
|---|---|---|
| 인풋 | 종목명만 | 종목명 + 사업보고서 PDF 권장 |
| 분량 | HTML 5p | HTML 10~20p |
| 시간 | 15~20분 | 1시간+ |
| 깊이 | 핵심 압축 — Point 3 + 재무 요약 + 시나리오 + 6-Lens | 9단계 풀 — Step 0~8 + Red Team |
| Red Team | 간이 (포인트 신뢰도로 갈음) | 정식 Step 5.5 |
| Forward 모델 | 시나리오 매트릭스만 | 5개년 IS/BS/CF + Balance Check |
| CSV 출력 | 3개 (재무·시나리오·피어) | 7개 (Step별 모두) |
| Excel 출력 | 옵션 | Code Interpreter 활성 시 자동 |
| 메타 리포트 | — | Step 9 별도 HTML |
| 용도 | 매주 실전 의사결정 | 학회 정식 발표·심층 분석 |

---

## AI별 위클리 활용 팁

### Claude
- Artifacts로 5p HTML을 단계별 미리보기 가능
- Search 도구 자동 ON — 최신 주가·뉴스 자동 갱신
- PDF 첨부 가능 — 분기 실적 발표 자료 직접 분석
- 회의주의 강점 — 컨센서스 변화에 자체 판단 추가

### ChatGPT
- 웹 브라우징으로 최근 7일 뉴스 자동 + URL
- Code Interpreter로 csv → .xlsx 자동 변환·다운로드
- Canvas로 HTML 미리보기 가능

### Gemini
- Search Grounding이 가장 강한 영역 — 출처 URL 자동 첨부
- 2M 토큰 — 사업보고서 PDF 통째 첨부 가능
- 유튜브 분석 — 실적 발표·IR Day 영상 트랜스크립트 (Advanced)
- Google Sheets 연동 — 누적 위클리 자동 기록 (Advanced)

### Perplexity
- 자체 검색 엔진 — 출처 URL이 답변에 자동 첨부
- Pro 모드 — GPT-4·Claude·Sonar 선택 가능
- 사업보고서 PDF 첨부는 제한적

---

## Compliance Notice

본 산출물은 GIC 학회 내부 학습 목적이며, 투자 권유가 아닙니다.
위클리는 핵심 압축 리포트로, 정식 9단계 분석과 별개의 독립 산출물입니다.
투자 결정은 본인 책임이며, 본 시스템은 어떠한 손익에 대해서도 책임지지 않습니다.
