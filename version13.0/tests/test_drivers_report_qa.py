import json
from pathlib import Path

from gic_v13.model.calculations import derive_metrics
from gic_v13.model.defense_lens import evaluate_defense_kpis
from gic_v13.model.drivers import build_driver_map
from gic_v13.normalize.facts import normalize_single_account_all
from gic_v13.qa.lint import lint_run
from gic_v13.report.report_plan import build_report_plan


def _facts_and_metrics():
    payload = json.loads(Path("tests/fixtures/opendart/fnlttSinglAcntAll_2024.json").read_text(encoding="utf-8"))
    facts = normalize_single_account_all(
        payload,
        corp_name="DEFENSE_FIXTURE_CO",
        endpoint="fnlttSinglAcntAll",
        raw_payload_path="raw.json",
        retrieved_at="2026-05-31T09:00:00+09:00",
    )
    return facts, derive_metrics(facts)


def test_defense_drivers_mark_missing_non_financial_kpis_without_guessing():
    facts, metrics = _facts_and_metrics()
    kpis = evaluate_defense_kpis(facts, metrics)

    drivers = build_driver_map(kpis)

    assert any(kpi.status == "unavailable" and kpi.kpi_name == "수주잔고" for kpi in kpis)
    assert any(driver.driver_id == "DEFENSE_CASH_CONVERSION_TO_FCF" for driver in drivers)
    assert all(driver.falsifiers for driver in drivers)


def test_report_plan_and_qa_preserve_draft_status_for_missing_defense_kpis():
    facts, metrics = _facts_and_metrics()
    kpis = evaluate_defense_kpis(facts, metrics)
    drivers = build_driver_map(kpis)

    plan = build_report_plan(
        run_id="fixture",
        mode="COMPANY_REPORT",
        entity="DEFENSE_FIXTURE_CO",
        as_of_date="2026-05-31",
        facts=facts,
        derived_metrics=metrics,
        kpi_statuses=kpis,
        drivers=drivers,
    )
    qa_report = lint_run(plan, facts, metrics, kpis, drivers, human_reviewed=False)

    assert plan.orientation == "portrait"
    assert plan.draft_status == "DRAFT - QA NOT APPROVED"
    assert qa_report.release_approved is False
    assert qa_report.gates["factual_traceability"] in {"PASS", "WARNING"}
    assert qa_report.gates["render_integrity"] == "PASS"
    assert qa_report.warnings
