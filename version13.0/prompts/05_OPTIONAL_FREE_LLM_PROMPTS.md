# Optional Free LLM Prompt Export

v13은 유료 LLM 없이 작동해야 한다. 다만 부원이 무료 ChatGPT, Claude, Gemini에 접속할 수 있다면, 시스템이 생성한 structured artifacts를 붙여넣어 문장 품질을 보조할 수 있다.

## Rule

- LLM은 source 없는 claim을 추가하면 안 된다.
- LLM output은 QA lint를 다시 통과해야 한다.
- LLM이 만든 문장은 `draft_narrative`로 취급한다.

## Prompt

```text
아래 GIC v13 artifacts만 사용해 한국어 리서치 문장을 다듬어라.
새로운 사실, 숫자, 출처, 전망, 투자 판단을 추가하지 마라.

필수 규칙:
1. 모든 핵심 문단은 Fact -> Mechanism -> Financial Impact -> Judgment -> Falsifier 순서로 유지한다.
2. claim_id와 source_id를 삭제하지 않는다.
3. `unavailable` 또는 `pending`인 KPI를 확정 사실처럼 쓰지 않는다.
4. QA FAIL 원인을 문장으로 숨기지 않는다.
5. 결과는 draft로 표시한다.

입력:
[source_register.md]
[normalized_facts.json]
[driver_map.json]
[claim_evidence_matrix.csv]
[report_plan.json]
[qa_report.md]
```

