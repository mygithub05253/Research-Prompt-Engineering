# GIC v14 설계 초안 (논의용)

> 상태: **구현됨(1차) — 2026-06-01.** 양식 HTML 렌더러·pykrx 수집·프롬프트 팩·CLI·테스트 동작. 후속: 피어 재무비율, 주요주주 API, 산업 가로 PPT.
> 작성일: 2026-06-01
> 한 줄 정의: **무료 공개데이터(OpenDART + KRX)로 GIC 공식 양식 HTML을 자동 생성하고,
> 정성 분석은 "데이터가 미리 박힌 엔지니어드 프롬프트"로 사람이 완성하는 하이브리드 리서치 시스템.**

---

## 1. v14는 무엇을 바꾸나 (v13 대비)

| 항목 | v13 | v14 |
|---|---|---|
| 데이터 | OpenDART(재무·공시)만 | OpenDART + **pykrx + FinanceDataReader**(주가·시총·거래량·PER/PBR/배당) |
| 산출물 | 디버그용 preview.html | **GIC 공식 양식과 똑같은 portrait 리포트 HTML** |
| 정성 서술 | rule 텍스트 | **데이터·공식이 미리 채워진 단계별 프롬프트 export** (v9 계보 계승) |
| 시각화 | 없음(표만) | **Chart.js** 주가/재무/피어비교/파이 차트 (HTML 내장, 의존성 0) |
| 근거 강화 | 단일기업 | **피어 벤치마킹**(동종 N개 PER/ROE/PBR 비교) + 경량 크롤링(뉴스/공시 제목) |
| 폴더 | top-level 12개(찾기 어려움) | **번호 매긴 얕은 구조**(초심자 동선) |
| README | 기술 위주 | **초심자용 단계별·스크린샷급 상세** |

---

## 2. 핵심 철학 — "자동 + 프롬프트" 하이브리드

GIC 리서치는 두 종류의 내용으로 나뉜다.

1. **하드 데이터** (주가, 재무, 멀티플, 피어 비교) → 기계가 정확히, 무료로, 재현 가능하게 채운다.
2. **정성 해석** (산업 구조, 투자포인트, 리스크, 밸류에이션 논리) → 사람이 AI 챗봇과 협업해 쓴다.

v14는 (1)을 자동화하되 (2)를 억지로 자동화하지 않는다. 대신 (1)의 결과를 **그대로 인용한 프롬프트**를 만들어 (2)를 돕는다.

> 예) "한화에어로 영업이익률이 FY23 7.2% → FY24 9.8%로 +2.6%p. 이 개선의 원인을 아래 5단계로 분석하라.
> [Step1] … [Step2] … (출처: OpenDART fnlttSinglAcntAll, 2024)" 같은 프롬프트가 자동 생성됨.

이 프롬프트는 **최종 산출물 폴더에 항상 남는다.** 부원은 이를 ChatGPT/Claude/Gemini/Antigravity 어디에 붙여도 동작한다(v9의 복붙 100% 원칙 유지). 즉 코드를 못 다루는 부원도, AI 구독이 없는 부원도 쓸 수 있다.

---

## 3. 데이터 출처 매핑 (양식 칸 → 무료 API)

| 양식 항목 | 출처 | 비고 |
|---|---|---|
| 현재주가, 52주 최고/저, 일평균거래액(60일) | pykrx / FDR | 무료, 키 불필요 |
| 시가총액, 발행주식수 | pykrx | `get_market_cap` |
| PER, PBR, EPS, BPS, DIV(배당수익률) | pykrx | `get_market_fundamental` |
| 외국인 지분율 | pykrx | `get_exhaustion_rates_of_foreign_investment` |
| 주요주주(%) | **OpenDART** | 최대주주현황 API |
| 매출액·영업이익·지배순이익 | **OpenDART** | fnlttSinglAcntAll (이미 v13 구현) |
| ROE 등 파생 | 계산 | v13 calculations 확장 |
| 목표주가·상승여력 | **사람(프롬프트)** | 밸류에이션 판단 → 자동 추정 금지 |
| 피어 비교(PER/ROE/PBR) | OpenDART+pykrx | 벤치마킹 모듈 |
| 산업·기업분석·투자포인트·리스크 서술 | **사람(프롬프트)** | 정성 |

> 원칙(v13 계승): 자동으로 못 채우는 칸은 추정하지 않고 `unavailable`/`사람 입력 필요`로 두고 QA가 표시.

---

## 4. 아키텍처 (파이프라인)

```text
company_request.yaml (기업명·종목코드·연도·피어목록)
  └─> [수집] OpenDART(재무·주주·공시) + pykrx/FDR(시장데이터)   ← 전부 무료
        └─> raw 캐시
  └─> [정규화] canonical facts (v13 재사용)
  └─> [계산] 파생지표 + 멀티플 + YoY/CAGR
  └─> [벤치마킹] 피어 N개 수집 → 상대비교 테이블
  └─> [크롤링(경량)] 뉴스 RSS·DART 공시 제목 → 이벤트 타임라인
  └─> [차트데이터] Chart.js용 JSON (주가/재무/피어/배당)
  └─> 산출물 3종 동시 생성:
       ① report.html      (GIC 양식 그대로, 데이터·차트 채워짐, 서술칸은 [작성 필요] 표시)
       ② prompt_pack.md   (데이터가 박힌 단계별 엔지니어드 프롬프트 — 사람이 챗봇에 붙임)
       ③ qa_report.md     (무엇이 자동/무엇이 사람 몫인지, 근거 추적)
```

---

## 5. 산출물 ② — 프롬프트 팩 (이 프로젝트의 핵심 IP)

v9의 자산을 계승·강화한다:

- **단계 완전 세분화**: Step 0~8 (초기설정 → 산업 → 기업 → 포인트 → 리스크 → 밸류 → Red Team → 종합).
- **10개 블록 라이브러리** 유지 (용어번역·Sanity·비유·Mermaid·검증태그·Red Team·Evidence Card·AD-FCoT·5개년모델링·Anti-Hallucination).
- **v14 신규**: 각 Step 프롬프트에 **방금 수집한 실제 수치·공식·출처가 자동 주입**된다.
  - 예: `[자동주입] FY22~24 매출 CAGR = 12.4% (OpenDART)` 가 프롬프트 안에 미리 박혀 있어, 사람이 빈손으로 시작하지 않음.
- **4중 백틱 펜스**(v9 규칙)로 잘림 0건, 복붙 100%.
- **AI별 분기** `[Claude:] [ChatGPT:] [Gemini:]` 유지.
- 계산 공식은 **웹크롤링/표준 정의로 검증된 출처**를 주석으로 부착 (예: EV/EBITDA 정의 + 출처).

---

## 6. 폴더 구조 제안 (초심자 동선)

```text
version14.0/
├─ README.md              ← ★제일 먼저 읽는 곳 (초심자용, 그림 동선)
├─ 시작하기.md             ← 설치 3줄 + 첫 실행 (한글, 막힘 없게)
├─ input/                 ← ✏️ 부원이 건드리는 유일한 곳
│   ├─ company_request.yaml
│   └─ watchlist.yaml
├─ output/                ← 📦 자동 생성 결과 (report.html / prompt_pack.md / qa)
├─ prompts/               ← 🧠 단계별 엔지니어드 프롬프트 원본(템플릿)
├─ templates/             ← 🎨 GIC 양식 HTML/CSS 템플릿
├─ src/gic_v14/           ← ⚙️ 코드 (부원은 안 건드림)
│   ├─ collect/  (opendart, market[pykrx/fdr], crawl)
│   ├─ model/    (calculations, benchmark)
│   ├─ render/   (html, charts)
│   ├─ prompt/   (prompt_pack 생성)
│   └─ qa/
├─ docs/                  ← 📚 상세 문서 (이 설계서 포함)
└─ tests/
```

핵심: **부원은 `input/` 만 만지고 `output/` 만 본다.** 나머지는 안 봐도 됨.

---

## 7. 무료 제약 재확인

| 자원 | 무료? | 비고 |
|---|---|---|
| OpenDART API | ✅ 무료 키 | 재무·공시·주주 |
| pykrx | ✅ 키·결제 없음 | KRX 시장데이터 |
| FinanceDataReader | ✅ 오픈소스 | 가격 보강 |
| Chart.js | ✅ CDN/내장 | 시각화 |
| 정성 서술 | ✅ 부원의 무료 AI | 프롬프트 복붙 |
| 스케줄/메일 | ✅ GitHub Actions + Gmail | v13에서 계승 |

→ **어떤 부원도 추가 결제 0원**으로 전 과정 수행 가능.

---

## 8. pdf-to-md 스킬 활용 (양식 → 템플릿)

`C:\Users\kik32\Downloads\pdf-to-md-student\pdf-to-md` 로 GIC 양식 PDF/PPTX를 1회 변환 →
섹션 구조·표 헤더·문구를 markdown으로 추출 → `templates/`의 HTML 골격과 `prompts/`의 섹션 정의에 반영.
(dev-time 1회 작업이므로 런타임 무료 제약과 무관.)

---

## 9. 합의가 필요한 열린 질문

1. 폴더명을 한글(`시작하기.md`)로 할지 영문으로 할지 — 초심자 친화 vs 호환성.
2. 피어(경쟁사) 목록을 사람이 `input`에 지정할지, 업종코드로 자동 후보를 뽑을지.
3. 1차 구현 대상 기업/섹터 (v13은 DEFENSE·한화에어로 fixture) — v14도 한화에어로로 시작?
4. report.html을 PDF로 뽑는 방식(브라우저 인쇄 vs 자동) — 양식 1:1 재현 수준 목표치.

---

## 10. 구현 순서(제안)

1. version14.0 골격 + 폴더 구조 + 초심자 README.
2. 수집 레이어: pykrx/FDR 시장데이터 (OpenDART는 v13 코드 이식).
3. 양식 HTML 템플릿 + Chart.js 차트.
4. 프롬프트 팩 생성기(데이터 주입).
5. 벤치마킹 모듈.
6. 경량 크롤링(뉴스/공시).
7. QA + 스케줄/메일 이식.
8. 초심자 문서·예제 마무리.
