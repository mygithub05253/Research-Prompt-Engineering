from __future__ import annotations

from gic_v13.domain import DerivedMetric, FinancialDriver, FinancialFact, KpiStatus, QaReport, ReportPlan
from gic_v13.model.calculations import has_mixed_fs_div, has_mixed_period_type


def lint_run(
    plan: ReportPlan,
    facts: list[FinancialFact],
    derived_metrics: list[DerivedMetric],
    kpi_statuses: list[KpiStatus],
    drivers: list[FinancialDriver],
    human_reviewed: bool,
) -> QaReport:
    fatal_errors: list[str] = []
    warnings: list[str] = []
    gates = {
        "factual_traceability": "PASS",
        "calculation_integrity": "PASS",
        "scenario_transparency": "PASS",
        "narrative_quality": "PASS",
        "design_compliance": "PASS",
        "render_integrity": "PASS",
    }

    if not facts:
        gates["factual_traceability"] = "FAIL"
        fatal_errors.append("No financial facts were collected.")
    if any(not fact.source_id or not fact.source_locator for fact in facts):
        gates["factual_traceability"] = "FAIL"
        fatal_errors.append("A fact is missing source provenance.")

    if has_mixed_fs_div(facts):
        gates["calculation_integrity"] = "FAIL"
        fatal_errors.append("CFS/OFS facts are mixed.")
    if has_mixed_period_type(facts):
        gates["calculation_integrity"] = "FAIL"
        fatal_errors.append("Period bases are mixed.")
    if not derived_metrics:
        gates["calculation_integrity"] = "WARNING"
        warnings.append("No derived metrics were calculated.")

    if any(fact.actual_or_estimate != "actual" for fact in facts):
        gates["scenario_transparency"] = "WARNING"
        warnings.append("Non-actual facts exist and must be separated in narrative.")

    unavailable = [kpi.kpi_name for kpi in kpi_statuses if kpi.status == "unavailable"]
    if unavailable:
        gates["factual_traceability"] = "WARNING" if gates["factual_traceability"] == "PASS" else gates["factual_traceability"]
        warnings.append("DEFENSE KPI unavailable: " + ", ".join(unavailable))

    if any(not driver.falsifiers for driver in drivers):
        gates["narrative_quality"] = "FAIL"
        fatal_errors.append("A driver is missing falsifiers.")
    if any(not driver.description for driver in drivers):
        gates["narrative_quality"] = "WARNING"
        warnings.append("A driver is missing mechanism text.")

    expected_orientation = "landscape" if plan.mode == "INDUSTRY_TOP_PICK" else "portrait"
    if plan.orientation != expected_orientation:
        gates["design_compliance"] = "FAIL"
        fatal_errors.append(f"{plan.mode} expected {expected_orientation}, got {plan.orientation}.")

    for page in plan.pages_or_slides:
        if not page.title:
            gates["render_integrity"] = "FAIL"
            fatal_errors.append(f"Page {page.index} is missing title.")
        for chart in page.charts:
            if not chart.source_label:
                gates["render_integrity"] = "FAIL"
                fatal_errors.append(f"Chart {chart.chart_id} is missing source label.")

    release_approved = not fatal_errors and human_reviewed and not any(value == "FAIL" for value in gates.values())
    return QaReport(
        run_id=plan.run_id,
        gates=gates,
        fatal_errors=fatal_errors,
        warnings=warnings,
        recommended_fixes=_recommended_fixes(fatal_errors, warnings),
        human_reviewed=human_reviewed,
        release_approved=release_approved,
    )


def _recommended_fixes(fatal_errors: list[str], warnings: list[str]) -> list[str]:
    fixes = []
    if fatal_errors:
        fixes.append("Fix all FAIL gates before using the report outside internal review.")
    if warnings:
        fixes.append("Add manual evidence inbox items for unavailable DEFENSE KPIs.")
    if not fixes:
        fixes.append("Human reviewer may approve the HTML draft after checking source labels.")
    return fixes
