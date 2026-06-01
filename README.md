# GIC 리서치 프롬프트 / 자동화 에이전트 프로젝트

가천대학교 투자동아리 **GIC 4기** 리서치 자동화 프로젝트입니다.
기업 리서치 보고서 작성이라는 **반복 업무를 에이전트로 자동화**하는 것을 목표로,
프롬프트 설계(v1~v12)에서 시작해 **유료 AI 구독 없이 OpenDART API Key 하나로 동작하는
로컬 자동화 시스템(v13)** 으로 발전시킨 기록입니다.

## 한눈에 보기

- **무엇을 자동화하나**: 부원이 손으로 하던 기업 리서치 — DART에서 재무·공시 수집 → 지표 계산(OPM, YoY, FCF, 순부채 등) → 리서치 초안(HTML) + QA 리포트 생성.
- **실사용자**: GIC 동아리 부원 전체. ChatGPT Plus / Claude Pro / Gemini 구독이 **없어도** 쓸 수 있어야 한다는 게 핵심 제약.
- **비용**: 100% 무료. 유일한 외부 인증값은 **무료로 발급되는 OpenDART API Key** 하나뿐.
- **두뇌**: 유료 LLM 호출 없음. 규칙(rule)·템플릿 기반이라 구독 없이도 동일 결과 재생성 가능.

## 왜 이렇게 설계했나

> 동아리 부원 누구나, 결제 없이, OpenDART API Key만으로 실행할 수 있어야 한다.

이 제약이 전체 아키텍처를 결정했습니다. 그래서:

- 유료 LLM/금융데이터 API에 의존하지 않습니다.
- OpenDART에 없는 값(방산 수주잔고 등 비표준 KPI)은 **추정하지 않고** `unavailable`로 남깁니다.
- API Key는 코드·문서·산출물 어디에도 저장하지 않습니다(세션 환경변수 / UI 입력).
- QA gate를 통과하기 전에는 어떤 산출물도 `release-ready`로 표시하지 않습니다.

## 버전 히스토리

| 단계 | 내용 |
|---|---|
| v1.0 ~ v9.0 | 리서치 프롬프트 설계·반복 개선 (프롬프트 엔지니어링 단계) |
| v10.0 ~ v12.0 | 리서치 산출물 구조화(facts / derived metrics / drivers / claims), 양식·템플릿 정립 |
| **v13.0** | **유료 구독 없이 OpenDART API Key만으로 동작하는 로컬 자동화 시스템(MVP)** |

> 최신·권장 버전은 [`version13.0/`](version13.0/) 입니다. 실행법은
> [version13.0/README_QUICKSTART.md](version13.0/README_QUICKSTART.md) 참고.

## v13 빠른 시작 (요약)

```powershell
cd version13.0
python -m pip install -e .

# 1) API Key 없이 fixture로 전체 파이프라인 데모
python -m gic_v13.cli run tests/fixtures/request.yaml --fixture-dir tests/fixtures/opendart --output-dir outputs

# 2) 실제 OpenDART 실행 (키는 현재 세션에만)
$env:OPENDART_API_KEY="여기에_본인_OpenDART_API_KEY"
python -m gic_v13.cli run examples/defense_company_request.yaml --output-dir outputs
```

산출물: `outputs/<run_id>/deliverables/preview.html`, `outputs/<run_id>/audit/qa_report.md`

## 보안 주의

- **OpenDART API Key를 절대 커밋하지 마세요.** `.gitignore`가 `.env`/키 파일을 막아두었지만, 코드·문서·스크린샷에 키를 붙여넣지 않도록 직접 주의해야 합니다.
- OpenDART 키 발급: https://opendart.fss.or.kr/

## 라이선스 / 용도

가천대 GIC 동아리 교육·리서치 목적. 외부 배포 시 동아리 운영진과 상의하세요.
