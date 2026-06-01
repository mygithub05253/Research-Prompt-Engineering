# claim_evidence_matrix.md

| claim_id | report_section | claim_text | claim_type | fact_ids | assumption_ids | driver_ids | falsifier_ids | confidence | citation_text |
|---|---|---|---|---|---|---|---|---|---|
| C_001 | Investment Summary |  | fact |  |  |  |  | medium |  |
| C_002 | Driver Analysis |  | mechanism |  |  |  |  | medium |  |
| C_003 | Financial Impact |  | financial_impact |  |  |  |  | medium |  |
| C_004 | Judgment |  | judgment |  |  |  |  | medium |  |
| C_005 | Risks & Falsifiers |  | risk |  |  |  |  | medium |  |

## Matrix Rules

- 판단 claim은 반드시 driver_id와 falsifier_ids를 가진다.
- 사실 claim은 source_id와 fact_id 없이 작성하지 않는다.
- 근거가 부족하면 claim을 결론으로 쓰지 말고 `additional source required`로 낮춘다.

