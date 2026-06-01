# Expert 100-Step CLI MVP Checklist

이 체크리스트는 v13 CLI MVP를 확장하거나 검수할 때 쓰는 실무 순서다. 각 항목은 작게 확인 가능한 단위로 유지한다.

## A. Scope and Safety

1. v13의 목표가 PPT 생성기가 아니라 재무 리서치 자동화임을 확인한다.
2. 유료 LLM/API 없이 동작해야 함을 확인한다.
3. OpenDART API Key 외 필수 인증값을 만들지 않는다.
4. API Key를 문서, HTML, JSON, 로그에 저장하지 않는다.
5. `release_approved` 기본값을 false로 둔다.
6. QA 전 산출물을 final로 부르지 않는다.
7. fact, derived metric, assumption, forecast, judgment, falsifier를 분리한다.
8. 핵심 claim마다 evidence link를 둔다.
9. OpenDART에 없는 KPI를 추정하지 않는다.
10. `unavailable` 상태를 정상적인 안전 출력으로 인정한다.

## B. OpenDART Collection

11. `OPENDART_API_KEY` 또는 runtime input으로 key를 받는다.
12. key를 cache payload에 쓰지 않는다.
13. `corpCode.xml`을 받아 corp_code cache를 만든다.
14. 기업명 조회를 지원한다.
15. 종목코드 조회를 지원한다.
16. corp_code 직접 입력을 지원한다.
17. 모호한 기업명은 실패시킨다.
18. `fnlttSinglAcntAll` 요청을 만든다.
19. `fnlttSinglIndx` 요청을 만든다.
20. `reprt_code`를 명시적으로 저장한다.
21. `fs_div`를 명시적으로 저장한다.
22. raw response를 run별로 저장한다.
23. status/message를 보존한다.
24. key 오류 status는 fatal로 처리한다.
25. 데이터 없음 status는 unavailable로 처리한다.

## C. Normalization

26. OpenDART 금액 문자열의 쉼표를 제거한다.
27. 괄호 음수를 처리한다.
28. `-`와 빈 값을 null로 처리한다.
29. `thstrm_amount`를 기준연도 fact로 만든다.
30. `frmtrm_amount`를 전년도 fact로 만든다.
31. `bfefrmtrm_amount`를 전전년도 fact로 만든다.
32. 매출을 `revenue`로 매핑한다.
33. 영업이익을 `operating_income`으로 매핑한다.
34. 영업활동현금흐름을 `operating_cash_flow`로 매핑한다.
35. 유형자산 취득을 `capex`로 매핑한다.
36. 현금을 `cash`로 매핑한다.
37. 차입금을 `total_debt`로 매핑한다.
38. source_id를 모든 fact에 붙인다.
39. source_locator를 모든 fact에 붙인다.
40. raw_payload_path를 notes에 남긴다.

## D. Calculations

41. OPM을 계산한다.
42. Revenue YoY를 계산한다.
43. FCF를 계산한다.
44. Net debt를 계산한다.
45. 0 denominator를 안전 처리한다.
46. CFS/OFS 혼용을 탐지한다.
47. FY/Q/YTD 혼용을 탐지한다.
48. derived metric에 source fact ids를 붙인다.
49. 계산 불가 항목을 unavailable로 둔다.
50. 계산 결과를 audit 파일로 쓴다.

## E. DEFENSE Lens

51. 수주잔고 KPI를 점검한다.
52. 신규 수출계약/파이프라인 KPI를 점검한다.
53. 수출 비중/제품 믹스 KPI를 점검한다.
54. 생산능력/납기 KPI를 점검한다.
55. 영업이익률/현금전환 KPI를 점검한다.
56. 환율/승인/현지화 조건 KPI를 점검한다.
57. verified KPI만 강한 claim에 쓴다.
58. pending KPI는 warning으로 둔다.
59. unavailable KPI는 source gap으로 둔다.
60. conflicted KPI는 결론 사용을 막는다.

## F. Driver Modeling

61. 수주잔고 -> 매출 driver를 만든다.
62. 수출 파이프라인 -> 성장 driver를 만든다.
63. 수출 믹스 -> 마진 driver를 만든다.
64. 생산능력/납기 -> 매출 인식 driver를 만든다.
65. 현금전환 -> FCF driver를 만든다.
66. 환율/승인/현지화 -> 리스크 driver를 만든다.
67. driver마다 input_kpi_ids를 붙인다.
68. driver마다 input_fact_ids를 붙인다.
69. driver마다 transmission을 붙인다.
70. driver마다 falsifier를 붙인다.

## G. Report and HTML

71. COMPANY_REPORT orientation을 portrait로 둔다.
72. INDUSTRY_REPORT orientation을 portrait로 둔다.
73. INDUSTRY_TOP_PICK orientation을 landscape로 둔다.
74. report_plan JSON을 만든다.
75. page objective를 적는다.
76. chart source_label을 붙인다.
77. visual_qa_notes를 남긴다.
78. HTML에 DRAFT 배너를 표시한다.
79. HTML에 API Key를 쓰지 않는다.
80. HTML에 한글 font fallback을 둔다.
81. financial facts table을 렌더링한다.
82. derived metrics table을 렌더링한다.
83. QA gate table을 렌더링한다.
84. source label을 표시한다.
85. browser print는 draft PDF로만 취급한다.

## H. QA Lint

86. G1 Evidence를 검사한다.
87. G2 Calculation을 검사한다.
88. G3 Scenario를 검사한다.
89. G4 Research Quality를 검사한다.
90. G5 Mode & Design을 검사한다.
91. G6 Render Integrity를 검사한다.
92. fatal_errors를 쓴다.
93. warnings를 쓴다.
94. recommended_fixes를 쓴다.
95. human_reviewed 전 release_approved를 false로 둔다.

## I. Distribution

96. fixture offline run을 제공한다.
97. real OpenDART run guide를 제공한다.
98. Windows setup script를 제공한다.
99. pytest 전체 검증을 실행한다.
100. 산출물 목록과 QA 상태를 최종 보고한다.

