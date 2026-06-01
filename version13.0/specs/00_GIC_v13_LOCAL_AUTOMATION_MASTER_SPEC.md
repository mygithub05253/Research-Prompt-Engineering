# GIC v13 Local Automation Master Spec

## 1. 제품 정의

GIC v13은 OpenDART API와 로컬 HTML 렌더링을 이용해, 구독형 AI 도구 없이도 GIC 리서치 활동의 기본 산출물을 만들 수 있게 하는 로컬 자동화 시스템이다.

목표 사용자는 다음과 같다.

- ChatGPT Plus, Claude Pro, Gemini Advanced를 구독하지 않은 동아리 부원.
- OpenDART API Key는 발급할 수 있는 사용자.
- Python 실행 또는 packaged app 실행은 가능한 사용자.

## 2. 핵심 성공 기준

| 영역 | v13 성공 기준 |
|---|---|
| 접근성 | OpenDART API Key 외 유료 인증값이 없어도 실행 가능 |
| 근거성 | 모든 핵심 수치와 claim에 source/fact/driver link 존재 |
| 자동화 | OpenDART 재무 facts, HTML preview, QA lint를 자동 생성 |
| 보수성 | OpenDART에 없는 값은 추정하지 않고 unavailable 처리 |
| 반복성 | 같은 request config로 같은 run artifact 재생성 가능 |
| 교육성 | 부원이 산출물의 구조와 QA 실패 이유를 이해할 수 있음 |

## 3. 시스템 경계

### 필수 자동화

- API key 입력 및 검증.
- corp code cache 생성.
- 공시검색 및 정기보고서 접수번호 수집.
- `fnlttSinglAcntAll` 기반 전체 재무제표 facts 수집.
- `fnlttSinglIndx` 기반 주요 재무지표 facts 수집.
- canonical facts로 정규화.
- derived metrics 계산.
- DEFENSE sector lens 적용.
- rule-based driver map 생성.
- report plan 생성.
- HTML preview 렌더링.
- QA lint report 생성.

### 선택 자동화

- 공시 원문 XML에서 keyword 기반 방산 KPI 후보 추출.
- 수동 evidence inbox 검증.
- PDF export helper.
- optional free LLM prompt export.

### 제외

- 유료 LLM 호출.
- OpenAI/Anthropic/Gemini API 의존.
- 유료 금융 데이터.
- 근거 없는 target price 자동 생성.
- QA 전 release PDF/PPTX.

## 4. 권장 UX

v13은 CLI와 로컬 HTML UI를 모두 지원하도록 설계한다.

### CLI

```powershell
python -m gic_v13 run examples/defense_company_request.yaml
```

### Local UI

```powershell
python -m gic_v13 serve
```

브라우저에서 `http://127.0.0.1:8713`을 열고 아래를 입력한다.

- OpenDART API Key
- 기업명 또는 종목코드
- 사업연도
- 보고서 모드
- 연결/별도 선택
- 추가 evidence 파일 또는 수동 입력

## 5. 데이터 흐름

```text
run_request.yaml
  -> corp_code resolver
  -> OpenDART collectors
  -> raw payload cache
  -> normalized facts
  -> derived metrics
  -> sector lens
  -> driver map
  -> claim-evidence matrix
  -> report plan
  -> HTML preview
  -> QA lint report
```

## 6. 분석 원칙

v13도 v12의 불변 원칙을 유지한다.

- fact, derived metric, assumption, forecast, judgment, falsifier를 분리한다.
- 핵심 claim마다 evidence link를 둔다.
- 기업 리서치, 산업 리서치, 산업 Top Pick 모드를 분리한다.
- 공식 GIC 양식은 디자인 시스템 기준이지 콘텐츠 템플릿이 아니다.
- 기업/산업 리포트는 portrait, Top Pick은 landscape.
- QA gate 전에는 release-ready로 표시하지 않는다.

## 7. OpenDART-only 한계 처리

OpenDART API만으로도 재무제표 기반 리서치 초안은 가능하다. 그러나 DEFENSE 산업의 핵심 thesis에는 수주잔고, 수출계약, 제품 믹스, 납기, 승인 리스크 같은 비표준 KPI가 필요할 수 있다.

처리 원칙:

- 자동 수집 성공: `verified`.
- 원문 keyword 후보만 있음: `pending`.
- 출처 상충: `conflicted`.
- 공개 확인 불가: `unavailable`.
- 핵심 KPI가 `unavailable`이면 관련 claim은 생성하지 않거나 confidence를 낮춘다.

## 8. v13 MVP 승인 기준

- OpenDART API Key로 corp code cache를 생성할 수 있다.
- 한 기업의 최근 3개년 재무제표 facts를 수집할 수 있다.
- 최소 5개 파생 계산을 수행한다.
- DEFENSE lens가 report plan에 반영된다.
- `preview.html`이 생성된다.
- `qa_report.md`가 PASS/FAIL/WARNING gate를 출력한다.
- OpenDART에 없는 KPI를 임의 추정하지 않는다.

