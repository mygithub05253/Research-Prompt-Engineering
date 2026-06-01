import json
from pathlib import Path

from gic_v13.model.calculations import derive_metrics
from gic_v13.normalize.facts import normalize_single_account_all


def test_normalizes_opendart_financial_records_with_provenance():
    payload = json.loads(Path("tests/fixtures/opendart/fnlttSinglAcntAll_2024.json").read_text(encoding="utf-8"))

    facts = normalize_single_account_all(
        payload,
        corp_name="DEFENSE_FIXTURE_CO",
        endpoint="fnlttSinglAcntAll",
        raw_payload_path="raw.json",
        retrieved_at="2026-05-31T09:00:00+09:00",
    )

    revenue = next(f for f in facts if f.metric_name == "revenue" and f.period == "FY2024")
    assert revenue.value == 1200000
    assert revenue.source_id == "S_OPENDART_00126380_2024_11011_CFS"
    assert revenue.source_locator == "fnlttSinglAcntAll:ifrs-full_Revenue:thstrm_amount"
    assert revenue.fs_div == "CFS"
    assert revenue.actual_or_estimate == "actual"


def test_derived_metrics_include_opm_yoy_fcf_and_net_debt():
    payload = json.loads(Path("tests/fixtures/opendart/fnlttSinglAcntAll_2024.json").read_text(encoding="utf-8"))
    facts = normalize_single_account_all(
        payload,
        corp_name="DEFENSE_FIXTURE_CO",
        endpoint="fnlttSinglAcntAll",
        raw_payload_path="raw.json",
        retrieved_at="2026-05-31T09:00:00+09:00",
    )

    derived = derive_metrics(facts)

    by_name = {(metric.metric_name, metric.period): metric for metric in derived}
    assert by_name[("op_margin", "FY2024")].value == 0.12
    assert by_name[("revenue_yoy", "FY2024")].value == 0.2
    assert by_name[("free_cash_flow", "FY2024")].value == 130000
    assert by_name[("net_debt", "FY2024")].value == 150000
