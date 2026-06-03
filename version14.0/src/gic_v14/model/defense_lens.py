from __future__ import annotations

from gic_v14.domain import DerivedMetric, FinancialFact, KpiStatus


DEFENSE_KPIS = [
    ("KPI_DEF_001", "수주잔고", ["revenue"], "required"),
    ("KPI_DEF_002", "신규 수출계약 및 파이프라인", ["revenue"], "required"),
    ("KPI_DEF_003", "수출 비중/제품 믹스", ["margin"], "required"),
    ("KPI_DEF_004", "생산능력과 납기", ["revenue", "margin"], "required"),
    ("KPI_DEF_005", "영업이익률 및 현금전환", ["margin", "cash_flow"], "required"),
    ("KPI_DEF_006", "환율/승인/현지화 조건", ["margin", "risk"], "required"),
]


def evaluate_defense_kpis(facts: list[FinancialFact], derived_metrics: list[DerivedMetric]) -> list[KpiStatus]:
    statuses: list[KpiStatus] = []
    opm_ids = [metric.metric_id for metric in derived_metrics if metric.metric_name == "op_margin"]
    fcf_ids = [metric.metric_id for metric in derived_metrics if metric.metric_name == "free_cash_flow"]
    cash_conversion_ids = opm_ids + fcf_ids

    for kpi_id, name, links, policy in DEFENSE_KPIS:
        fact_ids: list[str] = []
        status = "unavailable"
        note = "OpenDART standard financial API did not provide this DEFENSE KPI."
        if kpi_id == "KPI_DEF_005" and cash_conversion_ids:
            fact_ids = cash_conversion_ids
            status = "verified"
            note = "Derived from OpenDART operating income, revenue, operating cash flow, and capex."
        statuses.append(
            KpiStatus(
                kpi_id=kpi_id,
                sector_id="DEFENSE",
                kpi_name=name,
                fact_ids=fact_ids,
                evidence_candidate_ids=[],
                financial_link=links,
                status=status,
                missing_data_policy=policy,
                note=note,
            )
        )
    return statuses
