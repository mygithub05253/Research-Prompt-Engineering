from __future__ import annotations

from gic_v13.domain import (
    DerivedMetric,
    FinancialDriver,
    FinancialFact,
    KpiStatus,
    ReportChart,
    ReportPage,
    ReportPlan,
)


def build_report_plan(
    run_id: str,
    mode: str,
    entity: str,
    as_of_date: str,
    facts: list[FinancialFact],
    derived_metrics: list[DerivedMetric],
    kpi_statuses: list[KpiStatus],
    drivers: list[FinancialDriver],
) -> ReportPlan:
    orientation = "landscape" if mode == "INDUSTRY_TOP_PICK" else "portrait"
    source_ids = sorted({fact.source_id for fact in facts})
    source_label = f"Source: OpenDART ({', '.join(source_ids[:2])})" if source_ids else "Source: unavailable"
    warning_notes = [f"{kpi.kpi_name}: {kpi.status}" for kpi in kpi_statuses if kpi.status != "verified"]
    metric_ids = [metric.metric_id for metric in derived_metrics]
    pages = [
        ReportPage(
            index=1,
            section="Investment Summary",
            objective="OpenDART 재무 facts와 DEFENSE lens를 기반으로 초안 thesis를 요약한다.",
            title=f"{entity}: OpenDART 기반 방산 리서치 초안",
            key_claim_ids=["C_SUMMARY_001"],
            charts=[
                ReportChart(
                    chart_id="CH_FIN_001",
                    chart_type="financial_summary_table",
                    fact_or_metric_ids=[fact.fact_id for fact in facts if fact.period == max(f.period for f in facts)][:8],
                    unit="KRW",
                    source_label=source_label,
                )
            ],
            narrative_blocks=[
                "OpenDART에서 확인된 재무 실적은 facts로 분리하고, 방산 KPI가 부족한 항목은 추정하지 않는다.",
                "영업이익률과 현금전환은 verified 지표로 계산되며, 수주잔고와 수출 파이프라인은 추가 evidence가 필요할 수 있다.",
            ],
            visual_qa_notes=warning_notes,
        ),
        ReportPage(
            index=2,
            section="Driver Map",
            objective="DEFENSE 핵심 KPI가 매출, 마진, 현금흐름, 가치평가로 연결되는 경로를 표시한다.",
            title="수주에서 현금흐름까지의 전달 경로",
            key_claim_ids=["C_DRIVER_001"],
            charts=[
                ReportChart(
                    chart_id="CH_DRIVER_001",
                    chart_type="driver_status_table",
                    fact_or_metric_ids=metric_ids,
                    unit="mixed",
                    source_label=source_label,
                )
            ],
            narrative_blocks=[driver.description for driver in drivers],
            visual_qa_notes=warning_notes,
        ),
    ]
    return ReportPlan(
        run_id=run_id,
        mode=mode,
        entity=entity,
        as_of_date=as_of_date,
        design_system="GIC_NAVY_ORANGE",
        orientation=orientation,
        pages_or_slides=pages,
    )
