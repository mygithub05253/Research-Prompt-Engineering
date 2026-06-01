"""GIC v13 에이전트 레이어.

단일 리포트 파이프라인(`pipeline.run_pipeline`)을 감싸서
- 관심종목 목록(watchlist)을 한 번에 일괄 실행하고(`batch`)
- 결과 초안/QA를 무료 SMTP(Gmail 등)로 메일 발송한다(`mailer`).

유료 LLM·유료 API에 의존하지 않으며, 표준 라이브러리만 사용한다.
"""
