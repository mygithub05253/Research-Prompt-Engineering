from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from gic_v13.config import get_api_key
from gic_v13.domain import FinancialFact, to_plain
from gic_v13.model.calculations import derive_metrics
from gic_v13.model.defense_lens import evaluate_defense_kpis
from gic_v13.model.drivers import build_driver_map
from gic_v13.normalize.facts import normalize_single_account_all
from gic_v13.opendart.financials import collect_financial_payloads, resolve_company
from gic_v13.qa.lint import lint_run
from gic_v13.render.html import render_html
from gic_v13.report.report_plan import build_report_plan


def run_pipeline(
    request: dict[str, Any],
    output_root: str | Path,
    fixture_dir: str | Path | None = None,
    api_key: str | None = None,
) -> Path:
    run_dir = Path(output_root) / request["run_id"]
    raw_dir = run_dir / "data" / "raw_opendart"
    for folder in ["audit", "data", "narrative", "deliverables"]:
        (run_dir / folder).mkdir(parents=True, exist_ok=True)

    key = get_api_key(api_key, allow_missing=fixture_dir is not None)
    company = resolve_company(request, raw_dir=raw_dir, fixture_dir=fixture_dir, api_key=key)
    payloads = collect_financial_payloads(request, company, raw_dir=raw_dir, fixture_dir=fixture_dir, api_key=key)
    retrieved_at = f"{request.get('as_of_date')}T00:00:00+09:00"
    facts: list[FinancialFact] = []
    for payload in payloads:
        year = payload.get("list", [{}])[0].get("bsns_year", "unknown") if payload.get("list") else "unknown"
        facts.extend(
            normalize_single_account_all(
                payload,
                corp_name=company.corp_name,
                endpoint="fnlttSinglAcntAll",
                raw_payload_path=str(raw_dir / f"fnlttSinglAcntAll_{year}.json"),
                retrieved_at=retrieved_at,
            )
        )
    derived_metrics = derive_metrics(facts)
    kpi_statuses = evaluate_defense_kpis(facts, derived_metrics)
    drivers = build_driver_map(kpi_statuses)
    plan = build_report_plan(
        run_id=request["run_id"],
        mode=request["report_mode"],
        entity=company.corp_name,
        as_of_date=request["as_of_date"],
        facts=facts,
        derived_metrics=derived_metrics,
        kpi_statuses=kpi_statuses,
        drivers=drivers,
    )
    qa_report = lint_run(plan, facts, derived_metrics, kpi_statuses, drivers, human_reviewed=False)

    _write_json(run_dir / "data" / "normalized_facts.json", {"financial_fact": to_plain(facts)})
    _write_json(run_dir / "data" / "derived_metrics.json", {"derived_metric": to_plain(derived_metrics)})
    _write_json(run_dir / "data" / "sector_kpi_checklist.json", {"sector_kpi_status": to_plain(kpi_statuses)})
    _write_json(run_dir / "data" / "driver_map.json", {"financial_driver": to_plain(drivers)})
    _write_json(run_dir / "narrative" / "report_plan.json", to_plain(plan))
    _write_json(run_dir / "audit" / "qa_report.json", to_plain(qa_report))
    _write_source_register(run_dir / "audit" / "source_register.md", facts)
    _write_evidence_matrix(run_dir / "audit" / "evidence_matrix.csv", drivers)
    _write_calculation_checks(run_dir / "audit" / "calculation_checks.md", derived_metrics)
    _write_qa_report_markdown(run_dir / "audit" / "qa_report.md", qa_report)
    _write_research_thesis(run_dir / "narrative" / "research_thesis.md", plan, drivers)
    render_html(plan, facts, derived_metrics, qa_report, run_dir / "deliverables" / "preview.html")
    return run_dir


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_source_register(path: Path, facts: list[FinancialFact]) -> None:
    source_ids = sorted({fact.source_id for fact in facts})
    lines = [
        "# source_register.md",
        "",
        "| source_id | source_type | title | publisher | coverage | reliability_note |",
        "|---|---|---|---|---|---|",
    ]
    for source_id in source_ids:
        covered = ", ".join(sorted({fact.metric_name for fact in facts if fact.source_id == source_id}))
        lines.append(
            f"| {source_id} | PRIMARY_FINANCIAL | OpenDART financial statements | Financial Supervisory Service OpenDART | {covered} | API key not stored; raw payload cached without key. |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_evidence_matrix(path: Path, drivers) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["claim_id", "claim_text", "driver_ids", "fact_ids", "falsifiers", "confidence"])
        for index, driver in enumerate(drivers, start=1):
            writer.writerow(
                [
                    f"C_DRIVER_{index:03d}",
                    driver.description,
                    driver.driver_id,
                    ";".join(driver.input_fact_ids),
                    ";".join(driver.falsifiers),
                    "medium" if driver.status == "verified" else "low",
                ]
            )


def _write_calculation_checks(path: Path, derived_metrics) -> None:
    lines = ["# calculation_checks.md", ""]
    for metric in derived_metrics:
        lines.append(f"- {metric.metric_id}: {metric.formula} = {metric.value} ({metric.validation_status})")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_qa_report_markdown(path: Path, qa_report) -> None:
    lines = [
        "# qa_report.md",
        "",
        "## Gates",
        "",
        "| Gate | Status |",
        "|---|---|",
    ]
    lines.extend(f"| {gate} | {status} |" for gate, status in qa_report.gates.items())
    lines.extend(["", "## Fatal Errors", ""])
    if qa_report.fatal_errors:
        lines.extend(f"- {error}" for error in qa_report.fatal_errors)
    else:
        lines.append("- None")
    lines.extend(["", "## Warnings", ""])
    if qa_report.warnings:
        lines.extend(f"- {warning}" for warning in qa_report.warnings)
    else:
        lines.append("- None")
    lines.extend(["", f"release_approved: {str(qa_report.release_approved).lower()}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_research_thesis(path: Path, plan, drivers) -> None:
    lines = [
        "# research_thesis.md",
        "",
        f"## {plan.entity} DEFENSE Draft Thesis",
        "",
        "이 문서는 OpenDART facts와 rule-based DEFENSE lens로 만든 초안이다. QA 통과 전 release-ready가 아니다.",
        "",
    ]
    for driver in drivers:
        lines.extend(
            [
                f"### {driver.name}",
                "",
                f"- Fact: linked facts = {', '.join(driver.input_fact_ids) if driver.input_fact_ids else 'additional source required'}",
                f"- Mechanism: {driver.description}",
                f"- Financial Impact: {driver.transmission.get('margin')}; {driver.transmission.get('cash_flow')}",
                f"- Judgment: {driver.status} 상태이므로 결론 강도는 evidence 상태에 따른다.",
                f"- Falsifier: {', '.join(driver.falsifiers)}",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")
