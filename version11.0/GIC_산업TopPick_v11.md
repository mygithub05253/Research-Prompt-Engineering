# GIC 산업 Top Pick (사전 선정 종목 비교·분석) — v11.0

> **버전**: v11.0 / 2026-05-14
> **출력물**: 산업 진단 + **사전 선정 종목 2~5개 비교·분석** + 최종 추천 1~2개 (HTML **가로 16:9** 8~12p + CSV)
> **디자인 양식**: `templates/산업TopPick_template.html` 학회 양식 베이스 — Pretendard 폰트 + Red Accent + 다크 네이비 표지/섹션 커버
> **핵심 변화 (v9.0 → v11.0)**: AI의 종목 발굴 → **조에서 사전 선정한 종목의 비교·심층 분석**으로 방향성 전환

---

## v11.0 산업 Top Pick의 본질 (재정의)

| 항목 | v9.0 (구) | v11.0 (신) |
|---|---|---|
| 인풋 | 산업 1개 + 후보 5~10개 (AI가 스크리닝) | **산업 1개 + 조에서 사전 선정한 2~5개 종목** |
| AI 역할 | 후보 발굴 + 점수 산출 + 1~2개 추천 | **선정 종목 비교·심층 분석 + 추천 1~2개** |
| 흐름 | 산업 → AI 발굴 → Top Pick | **조의 사전 검토 → AI 비교·분석 → 추천** |
| 깊이 | Top Pick 압축 분석 | **각 종목 6-Lens 점수 + 시나리오 + Risk-Reward** |

**왜 바뀌었나**: 조에서 사전 토론·리서치를 통해 종목을 선정하는 것이 학회 운영 방식. AI의 무작위 스크리닝은 이 흐름과 맞지 않음. 대신 AI는 **선정된 종목의 객관적 비교 + 산업 맥락 + 추천 근거 강화**에 집중.

---

## 출력 양식 — HTML 8~12페이지 (A4 가로, 1280×720 16:9 슬라이드)

| 페이지 | 내용 |
|---|---|
| 1 | 커버 + 산업 한줄 진단 + 비교 종목 리스트 + 최종 추천 1~2개 |
| 2 | 산업 진단 — 시장 규모·CAGR·사이클 위치 (CSV 출력) |
| 3 | 산업 밸류체인 + Porter 5 Forces |
| 4 | **종목 비교 매트릭스** — 핵심 (모든 선정 종목 한눈에) |
| 5 | 종목 #1 심층 카드 (재무·Moat·포인트·리스크) |
| 6 | 종목 #2 심층 카드 |
| 7 | 종목 #3 심층 카드 (선정 종목 수만큼 반복) |
| 8 | **6-Lens 가중 점수 비교** (선정 종목 전체) |
| 9 | Risk-Reward 매트릭스 + 추천 종목 사유 |
| 10 | Red Team — 추천 종목에 대한 반대 시나리오 |
| 11 | 모니터링 체크리스트 + 트리거 이벤트 |
| 12 | 참고문헌 + Disclaimer + 프롬프트 메타 |

> ※ 선정 종목 수가 2개면 7p 슬라이드 생략 → 총 10페이지.
> ※ 5개면 4·5·6·7·7-b·7-c 6장 사용 → 총 13페이지 (양식 유연).

---

## 코드블록 표기 규칙

본 문서도 **외부 4중 백틱 펜스**(```` ```` ````)를 사용합니다.

---

## Top Pick 단일 프롬프트 (전체 복사)

````
당신은 가천대학교 투자 동아리 GIC 소속 산업 애널리스트입니다.
[산업명] 산업의 위클리 Top Pick 보고서를 작성하라.
조에서 사전 선정한 2~5개 종목을 객관 비교 + 산업 맥락에서 분석하라.

[v11.0 핵심 변경]
종목 발굴 X → 조 선정 종목 비교·분석에 집중.
AI는 객관 데이터 수집 + 비교 + 심층 분석 + 추천 강화만 수행.

[v11.0 W원칙 — 웹검색 의무]
챗봇 내장 웹검색을 활성화. 모든 선정 종목의 시총·주가·실적·뉴스는 최신값 + URL.

──────────────────────────────────────────
■ 분석 산업: [예: 반도체 / 조선 / 방산 / AI / 로봇]
■ 분석 기준일: [YYYY.MM.DD]
■ 조에서 사전 선정한 종목 (2~5개): [기업1(코드), 기업2(코드), 기업3(코드), ...]
■ 분석 관점: [성장주/가치주/턴어라운드/배당/테마]
■ 최종 추천 개수: [기본 1, 최대 2]
■ 사전 선정 사유: [조 내 토론 핵심 — 왜 이 종목들을 후보로 골랐는지 한 줄씩]

[블록 J 의무 — Anti-Hallucination]
모든 시장 규모·점유율·멀티플은 검증 가능한 1차 출처 + URL.
출처 미상 수치는 "Data unavailable" 표기 + 페널티.

──────────────────────────────────────────
[Phase 1 — 산업 진단]

[블록 C 적용 — 핵심 비유]
이 산업을 30자 이내 한 줄 비유로 표현.

A. 산업 사이클 위치
   - 도입기/성장기/성숙기/쇠퇴기 + 근거 1줄
   - 직전 사이클 대비 위치 (블록 H — AD-FCoT 활용)

B. 시장 규모 + CAGR
   - 글로벌 + 국내 시총 (웹검색 최신, 출처 URL)
   - 3~5Y CAGR + 출처 (TrendForce/Yole/KIET 등)

C. 이번 주·이번 달 산업 모멘텀
   - 핵심 변동 1~3개 (출처 URL)
   - 각 변동의 산업 내 영향 매트릭스 (수혜 종목 / 피해 종목)

D. Porter 5 Forces 강도 (각 항목 1줄 + 근거)

[블록 D 적용 — Mermaid]
산업 밸류체인 다이어그램을 별도 섹션의 ```mermaid 코드로 출력.

[X원칙] 산업 데이터를 csv로:
```csv
# 산업 진단 데이터
항목,값,출처URL
시장규모_글로벌(USDbn),...
시장규모_국내(억원),...
3Y_CAGR(%),...
5Y_CAGR(%),...
사이클위치,...
```

──────────────────────────────────────────
[Phase 2 — 선정 종목 비교 매트릭스 (v11.0 핵심)]

조에서 사전 선정한 2~5개 종목을 객관 데이터로 한 표에 정리.

| 기업 | 종목코드 | 시총(억) | 매출(억) | OPM(%) | ROE(%) | PER(NTM) | EV/EBITDA | 산업 사이클 노출도 | 사전 선정 사유 1줄 |
|---|---|---|---|---|---|---|---|---|---|

[X원칙] csv 동시 출력:
```csv
# 선정 종목 비교
기업,종목코드,시총(억),매출(억),OPM(%),ROE(%),PER_NTM,EV/EBITDA,PBR,사이클노출도(상/중/하),출처URL
[종목1],...
[종목2],...
...
```

각 종목의 사이클 노출도 판정:
- 상: 산업 모멘텀 직접 수혜
- 중: 일부 사업부만 수혜
- 하: 산업 변동에 둔감

[블록 E·J] 모든 수치 출처 URL + 의심 시 [검증 필요].

──────────────────────────────────────────
[Phase 3 — 각 선정 종목 심층 카드 (선정 종목 수만큼 반복)]

각 종목마다 다음 형식의 심층 카드 작성 (HTML 1페이지 분량):

[심층 카드 — 기업명]

A. 사업 한줄 요약 (≤40자, 비유 적용)

B. 재무 핵심 (3개년)
   매출·영업이익·OPM·ROE·EPS 표 + YoY 추이 코멘트

C. Economic Moat
   원가/네트워크/전환비용/무형자산/규모 중 해당 1~2개 + 근거 1줄

D. 투자포인트 2~3개 (각 ≤100자) — Evidence Card 압축 (근거 2건 + URL)

E. 리스크 1~2개 (각 ≤80자)

F. 5개년 시나리오 (간이)
   | 시나리오 | FY1 EPS | 적용 PER | 목표주가 | 상승여력 |

G. 6-Lens 가중 점수 (개별)
   | Lens | 가중치 | 점수 | 근거 1줄 |
   | Business Clarity | 15% | | |
   | Moat Strength | 20% | | |
   | Financials | 30% | | |
   | Growth | 15% | | |
   | Valuation | 10% | | |
   | Promoter Behavior | 10% | | |
   가중 합계: [#.#점] → 의견 [BUY/HOLD/AVOID]

──────────────────────────────────────────
[Phase 4 — 6-Lens 가중 점수 비교 (전 종목)]

선정 종목 전체의 6-Lens 점수를 비교 매트릭스로:

| Lens | 가중치 | [종목1] | [종목2] | [종목3] | ... |
|---|---|---|---|---|---|
| Business Clarity | 15% | | | | |
| Moat Strength | 20% | | | | |
| Financials | 30% | | | | |
| Growth | 15% | | | | |
| Valuation | 10% | | | | |
| Promoter Behavior | 10% | | | | |
| **가중 합계** | 100% | | | | |
| **판정** | — | BUY/HOLD | ... | ... | ... |

[X원칙] csv 출력:
```csv
# 6-Lens 비교
Lens,가중치(%),[종목1]점수,[종목2]점수,[종목3]점수
Business_Clarity,15,...
Moat_Strength,20,...
Financials,30,...
Growth,15,...
Valuation,10,...
Promoter_Behavior,10,...
TOTAL,100,...
판정,,BUY/HOLD,...
```

──────────────────────────────────────────
[Phase 5 — Risk-Reward 매트릭스 + 추천 선정]

| 종목 | 상승여력(Base) | 하방 리스크(Bear) | Risk-Reward 비율 | 추천 비중 |
|---|---|---|---|---|

[Risk-Reward 비율 산식]
RR = (Base 목표주가 - 현재가) / (현재가 - Bear 목표주가)
RR ≥ 2.5 → 매우 매력 / 1.5~2.5 → 매력 / <1.5 → 평이

[추천 종목 선정 — 최종 1~2개]
선정 기준:
1. 6-Lens 가중 점수 상위
2. Risk-Reward 비율 ≥ 1.5
3. 산업 사이클 정합성
4. 조의 사전 선정 사유와 부합

[추천 종목 #1: 종목명]
- 선정 이유 3줄 (Top Pick으로 미는 핵심 근거)
- 6-Lens 점수: [#.#] / Risk-Reward: [#.#]
- 트리거 이벤트 (이걸 보면 매수 확신)
- 위험 신호 (이걸 보면 재검토)

[추천 종목 #2: 종목명] (선택)

──────────────────────────────────────────
[Phase 6 — Red Team (추천 종목 대상)]

추천 종목 1~2개에 대해 Short Seller 페르소나 공격 1~2개 + Bull 방어.

[공격 #1]
- 카테고리: [논리/데이터/가정 중 1]
- 질문: [한 문장]
- 근거: [Phase 3~5 어느 부분 공격]

[방어]
- 핵심 반론
- 근거 데이터 + URL
- 방어 강도 [강/중/약]

[Red Team 결론]
"Bear case 핵심 우려는 [X]였으나 [Y] 근거로 방어 가능"

──────────────────────────────────────────
[Phase 7 — 모니터링 체크리스트]

| 지표 | 기준치 | 발표 예정일 | 트리거 액션 |
|---|---|---|---|

──────────────────────────────────────────
[Phase 8 — 참고문헌 + 메타]

A. 참고문헌 URL 리스트 (카테고리별)
B. 사용한 프롬프트 시스템: GIC 리서치 v11.0 (산업 Top Pick)
C. 적용 블록: A·C·D·E·G·H·J + W·X·P·M
D. 6-Lens 가중치 출처: Hardik Framework (블록 J + Step 7 가중치 점수)

──────────────────────────────────────────
[P원칙 — HTML 자동 생성 · 학회 디자인 양식 베이스]

다음 사양으로 단일 .html 파일 코드를 출력하라.
**`templates/산업TopPick_template.html`을 디자인 베이스로 참조** (Pretendard + 다크 네이비 표지 + Red accent):

@page A4 landscape + .slide 1280×720 (16:9 슬라이드) + page-break-after + break-inside avoid.

[페이지 구성 (선정 종목 N개에 따라 가변)]
- 페이지 1: 커버 + 산업 진단 1줄 + 비교 종목 리스트 + 최종 추천
- 페이지 2: 산업 진단 (시장 규모·사이클·모멘텀)
- 페이지 3: 산업 밸류체인 + Porter 5 Forces
- 페이지 4: 종목 비교 매트릭스 (Phase 2)
- 페이지 5~(4+N): 각 종목 심층 카드 (Phase 3, N장)
- 페이지 (5+N): 6-Lens 가중 점수 비교 (Phase 4)
- 페이지 (6+N): Risk-Reward + 추천 사유 (Phase 5)
- 페이지 (7+N): Red Team (Phase 6)
- 페이지 (8+N): 모니터링 체크리스트 (Phase 7)
- 페이지 (9+N): 참고문헌 + Disclaimer + 메타

──────────────────────────────────────────
[필수 CSS — 학회 양식 베이스 (16:9 슬라이드, 가로)]

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>[산업명] GIC Top Pick v11</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
:root{
  --navy:#1f2a3a;
  --navy-deep:#141c2a;
  --accent:#E63946;
  --gold:#c9a04a;
  --green:#2f9e6b;
}
@page { size: A4 landscape; margin: 0; }
*{ box-sizing:border-box; margin:0; padding:0; }
body{
  background:#2a2f38;
  font-family:'Pretendard','Pretendard Variable','Noto Sans KR',sans-serif;
  color:#111827;
  -webkit-print-color-adjust:exact;
}
.slide{
  width:1280px; height:720px;
  background:#fff;
  position:relative;
  overflow:hidden;
  box-shadow:0 12px 40px rgba(0,0,0,.45);
  border-radius:6px;
  page-break-after:always;
  break-after:page;
  break-inside:avoid;
}
.slide:last-child { page-break-after: auto; }
.cover { background: linear-gradient(110deg, rgba(20,28,42,.92) 0%, rgba(20,28,42,.7) 55%); color:#fff; }
.section-cover { background: linear-gradient(120deg,#0e1626 0%, #1b2941 100%); color:#fff; }
/* ... 학회 양식 베이스 — templates/산업TopPick_template.html 참조 ... */
h1 { font-size: 24pt; margin: 0 0 4mm 0; color: #111827; }
h2 { font-size: 18pt; margin: 0 0 3mm 0; color: #1f2937; }
h3 { font-size: 13pt; margin: 4mm 0 2mm 0; color: #1f2937; }
p, li, td, th { font-size: 10pt; line-height: 1.45; }
table { width: 100%; border-collapse: collapse; font-size: 9.5pt; }
th, td { border: 1px solid #d1d5db; padding: 4px 6px; text-align: left; }
th { background: #f9fafb; }
.compare-row-best { background: #ecfdf5; }
.compare-row-worst { background: #fef2f2; }
.badge-buy { background: #dcfce7; color: #166534; padding: 2px 8px; border-radius: 3px; font-weight: 700; }
.badge-hold { background: #fef9c3; color: #854d0e; padding: 2px 8px; border-radius: 3px; font-weight: 700; }
.badge-avoid { background: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 3px; font-weight: 700; }
.recommend-box { border: 2px solid #059669; background: #ecfdf5; padding: 4mm 6mm; margin: 3mm 0; }
.recommend-title { font-size: 14pt; font-weight: 700; color: #059669; }
.stock-card { border: 1px solid #d1d5db; border-radius: 4px; padding: 4mm; margin: 2mm 0; }
.metaphor { font-size: 13pt; font-style: italic; color: #4f46e5; padding: 3mm 5mm; background: #eef2ff; border-left: 4px solid #4f46e5; margin: 3mm 0; }
.red-team-box { background: #fef2f2; border-left: 4px solid #dc2626; padding: 3mm 4mm; margin: 3mm 0; }
.disclaimer { font-size: 8pt; color: #6b7280; border-top: 1px solid #e5e7eb; padding-top: 3mm; margin-top: auto; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }
.three-col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4mm; }

@media print {
  body { background: white; }
  .page { margin: 0; box-shadow: none; }
}
</style>
</head>
<body>
  <!-- 선정 종목 수에 따라 <section class="page">를 가변 -->
</body>
</html>
```

──────────────────────────────────────────
[자체 점검]
□ Phase 1 산업 진단 4개 항목 모두
□ Phase 2 선정 종목 2~5개 모두 비교 표에 포함
□ Phase 3 각 종목 심층 카드 (선정 수만큼)
□ Phase 4 6-Lens 비교 매트릭스
□ Phase 5 추천 1~2개 선정 사유 + Risk-Reward
□ Phase 6 Red Team (추천 종목 대상)
□ Phase 7 모니터링
□ Phase 8 참고문헌 URL 리스트 + 메타
□ csv 3개 (산업·비교·6-Lens) 동시 출력
□ HTML 페이지 분할 안전 CSS 적용
□ 모든 수치 출처 URL (블록 J + W원칙)
□ "조에서 사전 선정한 종목" 명시 — AI가 추가 종목 발굴 금지

[Claude: Artifacts로 종목 비교 매트릭스 인터랙티브 정렬 가능]
[ChatGPT: 웹 브라우징으로 선정 종목 멀티플 일괄 갱신 + Code Interpreter로 Excel]
[Gemini: Search Grounding으로 산업 리포트 자동 검색 + 사업보고서 다중 첨부 (2M 토큰)]
````

---

## 산업 Top Pick v11.0 사용 워크플로

### Step 0. 조 내 사전 선정 (학회 자체 진행)
- 조 회의·토론을 통해 산업 1개 + 후보 종목 2~5개 결정
- 각 종목 선정 사유 1줄씩 작성

### Step 1. AI 프롬프트 실행
1. 위 프롬프트 복사
2. ■ 항목 채우기 (특히 사전 선정 종목 + 선정 사유)
3. AI 챗봇 — **웹검색 활성** 후 붙여넣기
4. AI가 산업 진단 + 종목 비교 + 6-Lens + Red Team + HTML 코드 출력

### Step 2. 결과물 저장
- HTML 코드 → `[산업명]_TopPick_v11_[YYYYMMDD].html`
- csv 3개 → 각각 `.csv` 파일 (Excel 호환)

### Step 3. PDF 변환
- 브라우저에서 .html 열기 → Ctrl+P → 가로 모드 → PDF 저장

### Step 4. 학회 발표·문서화
- PDF + csv 함께 슬랙·노션·드라이브 업로드

---

## 선정 종목 수별 권장 사용

| 종목 수 | 추천 사용 |
|---|---|
| **1개** | Top Pick보다 `GIC_기업리서치_v11.md` 권장 (단일 종목 풀 분석) |
| **2개** | 양자 비교 — 어느 쪽이 더 매력적인가 |
| **3~4개** | 표준 Top Pick — 비교 매트릭스 + 추천 1~2 |
| **5개** | 최대 사용 — HTML 13p (양식 유연 적용) |
| **6개 이상** | 조에서 5개로 1차 압축 후 사용 |

---

## Top Pick vs 기업리서치 vs 위클리 (v11.0 통합 비교)

| 구분 | 기업리서치 v11 | 위클리 v11 | Top Pick v11 |
|---|---|---|---|
| 인풋 | 단일 종목 + 사업보고서 | 단일 종목 | **산업 + 선정 종목 2~5개** |
| 분량 | HTML 10~20p | HTML 5p | **HTML 8~13p** |
| 흐름 | 기업 → 산업 (bottom-up) | 종목 핵심만 (압축) | **산업 → 종목 (top-down)** |
| 깊이 | 풀 9단계 + Red Team | 핵심 압축 | **종목 비교 + 심층 카드** |
| AI 역할 | 분석 + 검증 + 모델링 | 데이터 수집 + 압축 | **비교 + 추천 강화** |
| 사용 시점 | 학회 정식 발표 | 매주 실전 의사결정 | **산업 변곡점 + 조 사전 토론 후** |
| Red Team | 정식 Step 5.5 | 간이 | Phase 6 (추천 종목 대상) |

---

## AI별 산업 Top Pick 활용 팁

### Claude
- Artifacts로 종목 비교 매트릭스 인터랙티브 정렬
- PDF 다중 첨부 (선정 종목 2~5개 사업보고서) — 200K 토큰
- 회의주의 강점 — 추천 종목 사전 Red Team 가능성 자체 체크
- Search 도구 자동 ON

### ChatGPT
- 웹 브라우징으로 산업 리포트 5건 + 선정 종목 멀티플 자동 수집
- Code Interpreter로 6-Lens 점수 자동 계산 + Excel 다운로드
- GPTs Memory로 매주 같은 산업 추적 시 일관성 유지

### Gemini
- Search Grounding — 산업 동향·정책·M&A 자동 검색 (가장 강력)
- 2M 토큰 — 선정 종목 모두 사업보고서 PDF 통째 첨부
- 유튜브 분석 — 산업 컨퍼런스·IR 영상 (Advanced)
- Google Sheets 연동 — 비교 점수 시트 자동 생성 (Advanced)

---

## Compliance Notice

본 산출물은 GIC 학회 내부 학습 목적이며, 투자 권유가 아닙니다.
Top Pick은 조에서 사전 선정한 후보 종목의 객관 비교·추천 도구로,
정식 발표용 종목별 심층 분석은 `GIC_기업리서치_v11.md`로 별도 진행하세요.
