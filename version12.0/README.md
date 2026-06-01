# GIC v12 Financial Research System — Handoff Pack

## 문서의 목적

이 패키지는 GIC 리서치 프롬프트 엔지니어링 프로젝트를 **재무 데이터 모델링 기반 리서치 생성 시스템**으로 발전시키기 위한 구현 준비 문서이다. 현재 단계의 목표는 코드 완성이 아니라, ChatGPT에서 합의된 분석·데이터·보고서·디자인·QA 규격을 고정하여 이후 Codex 또는 Claude Code가 구현 작업을 시작해도 핵심 품질 기준이 손상되지 않도록 하는 것이다.

## 확정된 사용자 요구사항

1. 기업 리서치 리포트와 산업 리서치 리포트는 제공된 `GIC 리서치 리포트 양식 ver2`의 **디자인 정체성만 유지**한다. 내부 목차·페이지별 논리·지표는 보고서 목적에 맞게 변경할 수 있다.
2. 산업 Top Pick은 별도 공식 양식은 없으며, **가로형 PDF/PPTX** 제출을 원칙으로 한다. 단, GIC의 디자인 정체성은 계승한다.
3. `deep-research-report.md`는 이후 모든 발전 작업에서 **방법론 소스**로 상시 참조한다.
4. v12의 중심은 단순 문장·슬라이드 생성이 아니라 **산업별 KPI → 재무 드라이버 → 실적 전망 → 가치평가 → 리포트 해석**의 흐름이다.
5. 최종 구현은 나중에 Codex/Claude Code로 넘길 수 있으나, 분석 품질·근거성·디자인 규칙은 먼저 문서로 고정한다.

## 읽는 순서

| 순서 | 파일 | 용도 |
|---:|---|---|
| 1 | `specs/00_GIC_v12_FINANCIAL_RESEARCH_MASTER_SPEC.md` | 프로젝트 전체 설계와 의사결정 기준 |
| 2 | `specs/01_SOURCE_AND_EVIDENCE_POLICY.md` | 출처·인용·데이터 추적 규칙 |
| 3 | `schemas/02_CANONICAL_DATA_SCHEMA.yaml` | 구현 가능한 데이터 모델 스키마 |
| 4 | `specs/03_REPORT_AND_DESIGN_CONTRACTS.md` | 세 가지 리포트 모드와 디자인 규격 |
| 5 | `schemas/04_SECTOR_FINANCIAL_LENSES.yaml` | 산업별 KPI·드라이버·밸류에이션 렌즈 |
| 6 | `prompts/05_PROMPT_ORCHESTRATION_SPEC.md` | LLM 프롬프트 체인 및 출력 계약 |
| 7 | `qa/06_QA_ACCEPTANCE_TESTS.md` | 내용·수치·디자인·렌더링 검수 기준 |
| 8 | `prompts/07_HANDOFF_PROMPT_CODEX_CLAUDE.md` | 구현 에이전트에게 그대로 전달할 착수 지시문 |
| 9 | `AGENTS.md` / `CLAUDE.md` | Codex/Claude Code 프로젝트 상시 규칙 |

## 포함된 기준 자료

### 필수 참조 자료
- `sources/reference/GIC 리서치 리포트 양식 ver2 (2).pdf`
- `sources/reference/GIC 리서치 리포트 양식 ver2 (2).pptx`
- `sources/reference/deep-research-report.md`

### 회귀 테스트용 기존 결과물
- `sources/baseline/한화에어로스페이스_GIC_3기_이동원.pptx`
- `sources/baseline/한화에어로스페이스_GIC_Weekly_Report_v1 (1).html`

기존 결과물은 디자인을 그대로 복제하기 위한 기준이 아니라, v12에서 **경영·경제·금융 해석력, 데이터 추적성, 렌더링 완성도**가 실제로 개선되었는지를 비교하는 회귀 테스트 자료로 사용한다.

## 실행 단계의 원칙

- ChatGPT 단계: 분석 규칙 고정, 프롬프트 설계, 실제 샘플 리포트 검증.
- Codex/Claude Code 단계: 데이터 전처리, 모델 계산, 렌더러, 자동 QA를 코드화.
- 구현 중 어떤 편의 기능도 `출처 추적`, `가정 명시`, `반증 조건`, `디자인 QA`를 생략하게 해서는 안 된다.

## 참고한 공개 1차 자료

- 금융감독원 OpenDART 개발가이드: XBRL 기반 재무제표 및 재무지표 API.
- IFRS Foundation: Digital Financial Reporting 및 XBRL 기반 구조화 비교 가능성.
- Microsoft MarkItDown: LLM/텍스트 분석용 Markdown 전처리 도구.
- Docling: 문서 구조·표·멀티포맷 변환 문서 처리 도구.
- PptxGenJS 공식 문서: 객체 기반 PPTX와 Slide Master, Asian font 지원.
- Marp CLI 공식 저장소: Markdown 기반 HTML/PDF/PPTX 변환과 editable PPTX 제한.
- OpenAI Codex 공식 문서: 프로젝트 지침 파일 `AGENTS.md`.
- Anthropic Claude Code 공식 문서: 프로젝트 지침 파일 `CLAUDE.md` 및 `AGENTS.md` import.
