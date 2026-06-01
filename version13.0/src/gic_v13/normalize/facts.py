from __future__ import annotations

from typing import Any

from gic_v13.domain import FinancialFact


PERIOD_FIELDS = [
    ("thstrm_amount", 0),
    ("frmtrm_amount", -1),
    ("bfefrmtrm_amount", -2),
]


def normalize_single_account_all(
    payload: dict[str, Any],
    corp_name: str,
    endpoint: str,
    raw_payload_path: str,
    retrieved_at: str,
) -> list[FinancialFact]:
    facts: list[FinancialFact] = []
    for record in payload.get("list", []):
        metric_name = _map_metric(record)
        if metric_name is None:
            continue
        base_year = int(record["bsns_year"])
        source_id = f"S_OPENDART_{record['corp_code']}_{record['bsns_year']}_{record['reprt_code']}_{record.get('fs_div', 'NA')}"
        for field, offset in PERIOD_FIELDS:
            if field not in record:
                continue
            value = parse_amount(record.get(field))
            if value is None:
                continue
            period = f"FY{base_year + offset}"
            facts.append(
                FinancialFact(
                    fact_id=f"F_{record['corp_code']}_{period}_{metric_name}",
                    entity=corp_name,
                    metric_group=_metric_group(metric_name),
                    metric_name=metric_name,
                    period=period,
                    period_type="FY",
                    value=value,
                    value_text=None,
                    unit="KRW",
                    currency=record.get("currency"),
                    fs_div=record.get("fs_div", "NA"),
                    actual_or_estimate="actual",
                    source_id=source_id,
                    source_locator=f"{endpoint}:{record.get('account_id') or record.get('account_nm')}:{field}",
                    validation_status="verified",
                    notes=(
                        f"OpenDART rcept_no={record.get('rcept_no')}; reprt_code={record.get('reprt_code')}; "
                        f"raw_payload_path={raw_payload_path}; retrieved_at={retrieved_at}"
                    ),
                )
            )
    return facts


def parse_amount(raw: Any) -> float | int | None:
    if raw is None:
        return None
    text = str(raw).strip()
    if text in {"", "-"}:
        return None
    negative = text.startswith("(") and text.endswith(")")
    text = text.replace(",", "").replace(" ", "").replace("(", "").replace(")", "")
    try:
        value = float(text) if "." in text else int(text)
    except ValueError:
        return None
    return -value if negative else value


def _map_metric(record: dict[str, Any]) -> str | None:
    account_id = str(record.get("account_id", "")).lower()
    account_nm = str(record.get("account_nm", ""))
    if "revenue" in account_id or account_nm in {"매출액", "수익(매출액)"}:
        return "revenue"
    if "operatingincomeloss" in account_id or "영업이익" in account_nm:
        return "operating_income"
    if "cashflowsfromusedinoperatingactivities" in account_id or "영업활동현금흐름" in account_nm:
        return "operating_cash_flow"
    if "purchaseofpropertyplantandequipment" in account_id or "유형자산의 취득" in account_nm:
        return "capex"
    if "cashandcashequivalents" in account_id or "현금및현금성자산" in account_nm:
        return "cash"
    if "borrowings" in account_id or "차입금" in account_nm:
        return "total_debt"
    return None


def _metric_group(metric_name: str) -> str:
    if metric_name in {"revenue", "operating_income"}:
        return "income_statement"
    if metric_name in {"operating_cash_flow", "capex"}:
        return "cash_flow"
    if metric_name in {"cash", "total_debt"}:
        return "balance_sheet"
    return "market_data"
