from __future__ import annotations

from gic_v13.domain import FinancialDriver, KpiStatus


DRIVER_SPECS = [
    (
        "DEFENSE_BACKLOG_TO_REVENUE",
        "수주잔고의 매출 인식 전환",
        ["KPI_DEF_001"],
        "수주잔고가 확인되면 향후 매출 인식 가시성의 선행지표로 해석한다.",
        ["납기 지연", "생산능력 병목", "계약 취소 또는 인도 지연"],
    ),
    (
        "DEFENSE_EXPORT_PIPELINE_TO_GROWTH",
        "신규 수출계약 및 파이프라인의 성장 기여",
        ["KPI_DEF_002"],
        "수출계약과 파이프라인은 미래 인도 물량과 매출 성장의 후보군이다.",
        ["수출 승인 지연", "조달정책 변화", "지정학 완화"],
    ),
    (
        "DEFENSE_EXPORT_MIX_TO_MARGIN",
        "수출 비중과 제품 믹스의 마진 영향",
        ["KPI_DEF_003"],
        "고마진 수출 제품 믹스가 확대되면 영업이익률 개선 가능성이 생긴다.",
        ["원가 상승", "저마진 물량 증가", "환율 악화"],
    ),
    (
        "DEFENSE_CAPACITY_DELIVERY_TO_RECOGNITION",
        "생산능력과 납기의 매출 인식 제약",
        ["KPI_DEF_004"],
        "생산능력과 납기는 수주가 실제 매출로 전환되는 속도를 제한한다.",
        ["생산 병목", "부품 조달 지연", "납기 지연"],
    ),
    (
        "DEFENSE_CASH_CONVERSION_TO_FCF",
        "영업이익률과 현금전환의 FCF 영향",
        ["KPI_DEF_005"],
        "영업이익률과 현금전환은 방산 수주가 주주가치로 이어지는지 검증한다.",
        ["운전자본 악화", "선수금 조건 악화", "CAPEX 증가"],
    ),
    (
        "DEFENSE_FX_APPROVAL_LOCALIZATION_RISK",
        "환율, 승인, 현지화 조건의 리스크",
        ["KPI_DEF_006"],
        "환율, 승인, 현지화 조건은 수출 매출과 마진의 실현 리스크다.",
        ["환율 급변", "수출 승인 지연", "현지화 비용 증가"],
    ),
]


def build_driver_map(kpi_statuses: list[KpiStatus]) -> list[FinancialDriver]:
    by_id = {kpi.kpi_id: kpi for kpi in kpi_statuses}
    drivers: list[FinancialDriver] = []
    for driver_id, name, kpi_ids, description, falsifiers in DRIVER_SPECS:
        linked_kpis = [by_id[kpi_id] for kpi_id in kpi_ids if kpi_id in by_id]
        fact_ids = [fact_id for kpi in linked_kpis for fact_id in kpi.fact_ids]
        status = "verified" if linked_kpis and all(kpi.status == "verified" for kpi in linked_kpis) else "unavailable"
        drivers.append(
            FinancialDriver(
                driver_id=driver_id,
                sector_id="DEFENSE",
                name=name,
                description=description,
                input_fact_ids=fact_ids,
                input_kpi_ids=kpi_ids,
                transmission={
                    "revenue": "인도 물량 및 매출 인식 일정에 따라 증가 가능" if "REVENUE" in driver_id or "GROWTH" in driver_id else None,
                    "margin": "제품 믹스, 생산 레버리지, 원가 조건에 따라 변동",
                    "cash_flow": "선수금, 운전자본, CAPEX 조건에 따라 시차 발생",
                    "balance_sheet": "운전자본과 순차입금에 반영",
                    "valuation": "이익 가시성과 FCF 개선 여부가 멀티플 재평가에 영향",
                },
                lag_or_timing="계약, 생산, 인도, 매출 인식 사이에 시차가 존재",
                falsifiers=falsifiers,
                status=status,
            )
        )
    return drivers
