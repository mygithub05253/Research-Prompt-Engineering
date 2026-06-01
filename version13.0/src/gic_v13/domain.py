from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any


@dataclass(frozen=True)
class CompanyRecord:
    corp_code: str
    corp_name: str
    stock_code: str | None = None
    modify_date: str | None = None


@dataclass
class FinancialFact:
    fact_id: str
    entity: str
    metric_group: str
    metric_name: str
    period: str
    period_type: str
    value: float | int | None
    value_text: str | None
    unit: str
    currency: str | None
    fs_div: str
    actual_or_estimate: str
    source_id: str
    source_locator: str
    validation_status: str
    notes: str | None = None


@dataclass
class DerivedMetric:
    metric_id: str
    metric_name: str
    formula: str
    derived_from_fact_ids: list[str]
    value: float | int | None
    unit: str
    period: str
    validation_status: str
    notes: str | None = None


@dataclass
class KpiStatus:
    kpi_id: str
    sector_id: str
    kpi_name: str
    fact_ids: list[str]
    evidence_candidate_ids: list[str]
    financial_link: list[str]
    status: str
    missing_data_policy: str
    note: str | None = None


@dataclass
class FinancialDriver:
    driver_id: str
    sector_id: str
    name: str
    description: str
    input_fact_ids: list[str]
    input_kpi_ids: list[str]
    transmission: dict[str, str | None]
    lag_or_timing: str | None
    falsifiers: list[str]
    status: str = "pending"


@dataclass
class ReportChart:
    chart_id: str
    chart_type: str
    fact_or_metric_ids: list[str]
    unit: str
    source_label: str


@dataclass
class ReportPage:
    index: int
    section: str
    objective: str
    title: str
    key_claim_ids: list[str]
    charts: list[ReportChart] = field(default_factory=list)
    tables: list[str] = field(default_factory=list)
    narrative_blocks: list[str] = field(default_factory=list)
    visual_qa_notes: list[str] = field(default_factory=list)


@dataclass
class ReportPlan:
    run_id: str
    mode: str
    entity: str
    as_of_date: str
    design_system: str
    orientation: str
    pages_or_slides: list[ReportPage]
    draft_status: str = "DRAFT - QA NOT APPROVED"


@dataclass
class QaReport:
    run_id: str
    gates: dict[str, str]
    fatal_errors: list[str]
    warnings: list[str]
    recommended_fixes: list[str]
    human_reviewed: bool
    release_approved: bool


def to_plain(value: Any) -> Any:
    if is_dataclass(value):
        return {key: to_plain(item) for key, item in asdict(value).items()}
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    if isinstance(value, dict):
        return {key: to_plain(item) for key, item in value.items()}
    return value
