# GIC v12 — Codex / Claude Code Implementation Handoff Prompt

아래 전체 블록은 구현을 시작할 때 Codex 또는 Claude Code에 그대로 붙여넣을 수 있는 착수 프롬프트다. 구현 에이전트는 반드시 저장소 안의 세부 spec과 schema를 먼저 읽고 작업해야 한다.

---

## Copy-Paste Start Prompt

```text
당신은 `GIC_v12_Financial_Research_System` 저장소의 구현 책임 엔지니어다.
이 프로젝트는 PPT를 빠르게 만드는 도구가 아니라, 공개 자료에 기반한 재무 데이터 모델링 결과를 GIC 리서치 보고서로 변환하는 시스템이다.

반드시 먼저 읽을 파일:
1. README.md
2. specs/00_GIC_v12_FINANCIAL_RESEARCH_MASTER_SPEC.md
3. specs/01_SOURCE_AND_EVIDENCE_POLICY.md
4. schemas/02_CANONICAL_DATA_SCHEMA.yaml
5. specs/03_REPORT_AND_DESIGN_CONTRACTS.md
6. schemas/04_SECTOR_FINANCIAL_LENSES.yaml
7. prompts/05_PROMPT_ORCHESTRATION_SPEC.md
8. qa/06_QA_ACCEPTANCE_TESTS.md
9. AGENTS.md 또는 CLAUDE.md

핵심 비즈니스 규칙:
- 세 가지 report mode를 분리한다: COMPANY_REPORT, INDUSTRY_REPORT, INDUSTRY_TOP_PICK.
- 공식 GIC 양식은 디자인 시스템 기준이며 내부 내용 항목을 강제하지 않는다.
- 기업/산업 리포트는 portrait; Top Pick은 16:9 landscape이다.
- deep-research-report.md는 방법론 소스이지 개별 투자 결론의 사실 근거가 아니다.
- 사실, 파생 계산, 가정, 전망, 판단, 반증 조건은 데이터 구조에서 분리한다.
- 핵심 주장마다 evidence link를 가져야 한다.
- 분석 품질을 낮추면서 구현 편의를 얻는 변경을 하지 않는다.

MVP 목표:
A. 소스 ingest/manifest
B. Markdown/JSON normalization scaffold
C. OpenDART 재무 fact loader 인터페이스와 mock test
D. sector lens loader 및 DEFENSE 예시 실행
E. facts → drivers → report_plan JSON pipeline
F. HTML preview renderer prototype
G. QA lint/acceptance test runner

권장 기술 방향:
- Python: ingestion, OpenDART loader, normalization, modeling, validation.
- YAML/JSON: schema, sector lenses, report plans, evidence links.
- MarkItDown: 일반 오피스/텍스트 자료 Markdown 전처리 후보. 고충실도 최종 문서 변환기로 오인하지 않는다.
- Docling: 복잡한 PDF/표/XBRL 후보; 채택 전 간단한 품질 benchmark를 만든다.
- PptxGenJS: 공식 양식에 가까운 편집 가능한 PPTX renderer 후보.
- Marp: Top Pick 빠른 prototype 또는 preview 후보; editable PPTX를 최종 품질 기준으로 사용하지 않는다.

첫 작업 순서:
1. 저장소 파일 구조를 확인하고 구현 계획을 `docs/IMPLEMENTATION_PLAN.md`로 작성한다. 아직 코드를 대량 변경하지 않는다.
2. `src/`, `tests/`, `outputs/`, `data/` 초기 폴더와 기본 config를 제안한다.
3. YAML schema를 검토해 타입 모델(Pydantic 또는 동등 검증 구조)을 설계한다.
4. `sources/reference/`와 `sources/baseline/` 파일을 건드리지 않고 테스트 fixture로 취급한다.
5. DEFENSE sector를 대상으로 dummy facts를 이용한 end-to-end skeleton을 만든다.
6. acceptance tests 중 MVP 대상 테스트를 실행하고 결과를 보고한다.

반드시 멈추고 사용자 확인을 받을 상황:
- 핵심 데이터 스키마 삭제/대폭 변경
- valuation 방법론 변경
- 공식 디자인 파일 자체를 덮어쓰기
- 외부 유료 API 또는 신규 production dependency 추가
- 근거 추적이나 QA gate를 생략하는 설계 선택

첫 응답 형식:
1. 내가 이해한 프로젝트 목적
2. 현재 파일에서 확인한 고정 규칙
3. 구현 architecture 제안
4. MVP milestone과 테스트 계획
5. 변경할 파일 목록
6. 사용자 확인이 필요한 의사결정
```

---

## Codex용 적용 방식

- 저장소 루트에 `AGENTS.md`를 둔다.
- Codex가 실행되기 전에 이 문서와 spec 파일을 읽도록 작업 지시를 준다.
- 하위 모듈에 특별한 규칙이 생기면 해당 폴더에 더 구체적인 `AGENTS.md` 또는 override를 추가한다.

## Claude Code용 적용 방식

- 저장소 루트에 `CLAUDE.md`를 둔다.
- 중복 관리를 줄이기 위해 `CLAUDE.md`에서 `@AGENTS.md`를 import하도록 구성한다.
- Claude 전용 지시가 있을 때만 `CLAUDE.md`에 추가한다.

## 에이전트 선택 권장

두 도구 중 하나로 시작한다. 같은 브랜치에서 두 도구를 동시에 무계획하게 사용하지 않는다.

- Codex로 시작하기 적합한 경우: ChatGPT와 같은 생태계에서 계획→코드→검수 흐름을 이어가고자 할 때.
- Claude Code로 시작하기 적합한 경우: `CLAUDE.md`, hooks, project memory 기반의 장기 로컬 개발 워크플로우를 이미 사용할 계획일 때.
- 어느 쪽을 선택하든 본 spec, schema, QA gate가 도구보다 우선한다.
