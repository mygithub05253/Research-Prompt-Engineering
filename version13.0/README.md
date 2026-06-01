# GIC v13 Local Automation System

## 목적

v13은 GIC v12의 리서치 원칙을 유지하면서, ChatGPT/Claude/Gemini 구독이 없는 동아리 부원도 **OpenDART API Key 하나와 로컬 실행 환경**만으로 기업 리서치 초안을 만들 수 있게 하는 자동화 설계다.

v13은 PPT를 빠르게 만드는 도구가 아니다. OpenDART 공시·재무 데이터를 수집하고, 이를 표준 facts/derived metrics/drivers/claims 구조로 변환한 뒤, HTML preview와 QA lint report를 생성하는 로컬 리서치 시스템이다.

## 핵심 방향

- 유료 LLM/API 의존 없음.
- OpenDART API Key만 필수 외부 인증값으로 사용.
- 기본 산출물은 HTML preview와 audit bundle.
- PDF는 브라우저 인쇄 또는 후속 자동화로 처리.
- PPTX는 v13 MVP 범위 밖이며, v14 또는 renderer extension으로 분리.
- 기업/산업/Top Pick 모드는 유지하되, 첫 구현 대상은 `DEFENSE`와 `COMPANY_REPORT`.

## v13에서 자동화하는 것

- OpenDART 고유번호 조회 및 corp_code 매핑.
- 공시검색으로 사업보고서·분기보고서·반기보고서 접수번호 추적.
- 단일회사 전체 재무제표 수집.
- 단일회사 주요 재무지표 수집.
- 재무 facts 정규화.
- OPM, YoY, FCF, net debt 등 파생 계산.
- DEFENSE sector lens 적용.
- rule/template 기반 driver map, claim-evidence matrix, report plan 생성.
- HTML preview 자동 렌더링.
- QA lint 자동화.

## v13에서 자동화하지 않는 것

- 근거 없는 전망 생성.
- 유료 데이터, 증권사 리포트, 비공개 자료 수집.
- OpenDART에 없는 방산 세부 KPI를 임의 추정.
- QA gate 실패 산출물을 release-ready로 표시.
- 최종 PDF/PPTX release 승인.

## OpenDART만으로 가능한 범위

OpenDART API는 공시검색, 기업개황, 고유번호, 정기보고서 재무정보, 주요 재무지표, 원문 XML 등을 제공한다. 따라서 과거 재무제표와 공시 기반 사실은 자동화할 수 있다.

다만 방산의 `수주잔고`, `신규 수출계약`, `제품 믹스`, `생산능력`, `납기`, `승인/현지화 조건`은 표준 재무제표 API에 항상 구조화되어 나오지 않는다. v13은 아래 방식으로 처리한다.

- OpenDART 정기보고서 원문 또는 공시검색 결과에서 자동 후보를 추출한다.
- 자동 추출이 실패하면 `unavailable` 또는 `manual evidence required`로 둔다.
- 사람이 공개 IR/사업보고서 표를 추가할 수 있는 `evidence_inbox`를 제공한다.
- 핵심 KPI가 없으면 결론 강도를 낮추고 QA warning/fail로 표시한다.

## 산출물 구조

```text
outputs/<run_id>/
├─ audit/
│  ├─ source_register.md
│  ├─ evidence_matrix.csv
│  ├─ calculation_checks.md
│  └─ qa_report.md
├─ data/
│  ├─ raw_opendart/
│  ├─ normalized_facts.json
│  ├─ derived_metrics.json
│  ├─ sector_kpi_checklist.json
│  └─ driver_map.json
├─ narrative/
│  ├─ report_plan.json
│  └─ research_thesis.md
└─ deliverables/
   └─ preview.html
```

## 에이전트 모드 (스케줄 자동실행 + 메일발송)

v13은 단일 실행(`run`) 외에, 여러 기업을 한 번에 돌리고 결과를 메일로 보내는 **에이전트 모드**를 제공한다.

```powershell
# 관심종목(watchlist) 일괄 실행 + 메일 발송
python -m gic_v13.cli agent run examples/watchlist.yaml --output-dir outputs --email
```

- 관심종목은 `examples/watchlist.yaml`에서 추가/삭제한다.
- 메일은 무료 SMTP(Gmail 앱 비밀번호) 사용, 유료 메일 API 없음.
- GitHub Actions(`.github/workflows/gic-agent.yml`) 또는 Windows 작업 스케줄러로 주기 실행.
- 자세한 설정은 [docs/AGENT_AUTOMATION_GUIDE.md](docs/AGENT_AUTOMATION_GUIDE.md) 참고.

## 권장 사용 흐름

1. 부원이 OpenDART API Key를 준비한다.
2. `examples/defense_company_request.yaml`에 기업명, 종목코드, 사업연도, 리포트 모드를 입력한다.
3. 로컬 실행 명령으로 OpenDART 데이터를 가져온다.
4. 시스템이 HTML preview와 QA report를 생성한다.
5. QA report가 FAIL이면 source gap 또는 계산 오류를 수정한다.
6. QA가 통과한 초안만 회의·발표 자료의 근거로 사용한다.

## 공식 참조

- OpenDART 오픈API 소개: https://opendart.fss.or.kr/intro/main.do
- OpenDART 공시검색 개발가이드: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001
- OpenDART 고유번호 개발가이드: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018
- OpenDART 단일회사 전체 재무제표 개발가이드: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019020
- OpenDART 단일회사 주요 재무지표 개발가이드: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2022001

