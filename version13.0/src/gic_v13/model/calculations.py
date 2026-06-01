from __future__ import annotations

from collections import defaultdict

from gic_v13.domain import DerivedMetric, FinancialFact


def derive_metrics(facts: list[FinancialFact]) -> list[DerivedMetric]:
    by_period: dict[str, dict[str, FinancialFact]] = defaultdict(dict)
    for fact in facts:
        by_period[fact.period][fact.metric_name] = fact

    derived: list[DerivedMetric] = []
    for period, metrics in sorted(by_period.items()):
        if {"revenue", "operating_income"} <= metrics.keys():
            derived.append(
                _metric(
                    "op_margin",
                    "operating_income / revenue",
                    [metrics["operating_income"], metrics["revenue"]],
                    safe_div(metrics["operating_income"].value, metrics["revenue"].value),
                    "%",
                    period,
                )
            )
        if {"operating_cash_flow", "capex"} <= metrics.keys():
            derived.append(
                _metric(
                    "free_cash_flow",
                    "operating_cash_flow - capex",
                    [metrics["operating_cash_flow"], metrics["capex"]],
                    metrics["operating_cash_flow"].value - metrics["capex"].value,
                    "KRW",
                    period,
                )
            )
        if {"total_debt", "cash"} <= metrics.keys():
            derived.append(
                _metric(
                    "net_debt",
                    "total_debt - cash",
                    [metrics["total_debt"], metrics["cash"]],
                    metrics["total_debt"].value - metrics["cash"].value,
                    "KRW",
                    period,
                )
            )

    for period in sorted(by_period):
        year = int(period.replace("FY", ""))
        previous_period = f"FY{year - 1}"
        current = by_period[period].get("revenue")
        previous = by_period.get(previous_period, {}).get("revenue")
        if current and previous and previous.value:
            derived.append(
                _metric(
                    "revenue_yoy",
                    "current revenue / previous revenue - 1",
                    [current, previous],
                    round((current.value / previous.value) - 1, 6),
                    "%",
                    period,
                )
            )
    return derived


def safe_div(numerator: float | int | None, denominator: float | int | None) -> float | None:
    if numerator is None or denominator in {None, 0}:
        return None
    return round(numerator / denominator, 6)


def _metric(
    metric_name: str,
    formula: str,
    source_facts: list[FinancialFact],
    value: float | int | None,
    unit: str,
    period: str,
) -> DerivedMetric:
    return DerivedMetric(
        metric_id=f"D_{metric_name}_{period}",
        metric_name=metric_name,
        formula=formula,
        derived_from_fact_ids=[fact.fact_id for fact in source_facts],
        value=value,
        unit=unit,
        period=period,
        validation_status="verified" if value is not None else "unavailable",
    )


def has_mixed_fs_div(facts: list[FinancialFact]) -> bool:
    return len({fact.fs_div for fact in facts if fact.fs_div != "NA"}) > 1


def has_mixed_period_type(facts: list[FinancialFact]) -> bool:
    return len({fact.period_type for fact in facts}) > 1
